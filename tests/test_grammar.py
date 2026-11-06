import hashlib
import json
import re
import unittest

from check_grammar import ACTIVE, UNUSED, CODAS, FORMS, ROOT, parse, validate
from verify import sentence_parts


class GrammarTests(unittest.TestCase):
    def one(self, text):
        result = parse(text)
        self.assertEqual(result['status'], 'parsed', (text, result))
        return result['analyses'][0]

    def test_inventory_is_80_plus_24(self):
        self.assertEqual(len(ACTIVE), 80)
        self.assertEqual(len(UNUSED), 24)
        self.assertFalse(ACTIVE & UNUSED)
        expected = json.loads((ROOT / 'lexicon-baseline.json').read_text(encoding='utf-8'))
        self.assertEqual(sorted(ACTIVE), expected['active'])
        self.assertEqual(sorted(UNUSED), expected['unused'])

    def test_every_licensed_form_and_unused_derivation(self):
        for root in ACTIVE:
            for coda in FORMS:
                self.assertFalse(validate([chr(ord(root) + CODAS.index(coda))]))
        for root in UNUSED:
            for coda in FORMS:
                self.assertTrue(validate([chr(ord(root) + CODAS.index(coda))]))

    def test_reserved_particles_and_codas(self):
        for text in ['나 록 제 햐', '나 멞 오', '나 멙 오', '한 각', '너 멕 나', '나 멕 [ 오 ]']:
            self.assertEqual(parse(text)['status'], 'invalid_lexeme', text)

    def test_hu_right_association(self):
        subject = self.one('나 후 기 후 제 각')['subject']
        self.assertEqual(subject, ('related', ('head', '나'),
                                  ('related', ('head', '기'), ('head', '제'))))

    def test_multiple_attributes(self):
        subject = self.one('살 툘 차 후 기 각')['subject']
        self.assertEqual(subject[1], ('modify', ('attribute', '사'),
                                     ('modify', ('attribute', '툐'), ('head', '차'))))

    def test_negative_predicate_and_legacy_are_equivalent(self):
        self.assertEqual(self.one('나 멚 오'), self.one('나 퍄 멕 오'))

    def test_negative_attribute_has_local_scope(self):
        node = self.one('나 멣 퍄 칼 콜 오')
        self.assertEqual(node['predicate'], ('verb', '메', 'continuing'))
        self.assertEqual(node['object'], ('modify', ('not', ('attribute', '카')),
                                         ('modify', ('attribute', '코'), ('head', '오'))))

    def test_past_and_double_negation(self):
        self.assertEqual(self.one('나 퍄 멗 오')['predicate'], ('not', ('verb', '메', 'past')))
        self.assertEqual(self.one('나 퍄 멚 오')['predicate'],
                         ('not', ('not', ('verb', '메', 'unmarked'))))
        self.assertEqual(self.one('옴 퍄 칼')['predicate'], ('not', ('attribute', '카')))

    def test_existence_negation_and_valence(self):
        self.assertEqual(self.one('자 갆 나 히'), self.one('자 퍄 각 나 히'))
        self.assertEqual(parse('자 각 나')['status'], 'unsupported')

    def test_pya_keeps_lexical_role(self):
        self.assertEqual(self.one('나 멕 퍄')['object'], ('head', '퍄'))
        self.assertEqual(self.one('퍄 각')['subject'], ('head', '퍄'))
        self.assertEqual(self.one('퍄 퍄 칼 옴 각')['subject'],
                         ('modify', ('not', ('not', ('attribute', '카'))), ('head', '옴')))

    def test_ti_ambiguity_survives_question_mark(self):
        for text in ['나 멕 티', '나 멕 티?', '나 멕 티.']:
            result = parse(text)
            self.assertEqual(result['status'], 'ambiguous')
            self.assertEqual(len(result['analyses']), 2)
            self.assertEqual({a['question'] for a in result['analyses']}, {True, False})
        self.assertTrue(self.one('네 멕 나 티')['question'])

    def test_unadopted_structures_stay_unsupported(self):
        for text in ['나 멕 오 하 네 멕 아', '나 록 아 호 네 록 제 헤',
                     '나 멕 타 네 멕 오', '나 릭 네 멕 오', '나 믹 오 칼',
                     '나 네', '나 하 네 하 니 록', '나 후 기 하 제 각']:
            self.assertEqual(parse(text)['status'], 'unsupported', text)
        self.one('나 멕 타')
        self.one('나 하 네 록 제 헤')

    def test_stress_corpus(self):
        rows = json.loads((ROOT / 'translation-cases.json').read_text(encoding='utf-8'))
        self.assertGreaterEqual(len(rows), 50)
        self.assertEqual([r['id'] for r in rows], list(range(1, len(rows) + 1)))
        self.assertGreaterEqual(len({r['category'] for r in rows}), 9)
        self.assertTrue(any(r['fidelity'] == '不能' for r in rows))
        for row in rows:
            self.assertEqual(row['source'], '自作')
            if row['fidelity'] == '不能':
                self.assertIsNone(row['serohan'])
                self.assertIsNone(row['literal'])
            else:
                self.assertTrue(row['literal'])
                for text in sentence_parts(row['serohan']):
                    self.assertIn(parse(text)['status'], {'parsed', 'ambiguous'}, (row['id'], text))
                    if row['fidelity'] == '保持':
                        self.assertEqual(parse(text)['status'], 'parsed', row['id'])

    def test_current_teaching_documents_use_active_roots(self):
        # Explicit candidate/rejected examples in the specification and audit are excluded.
        for file in ['README.md', 'overview.md', 'grammar.md', 'particles.md',
                     'verb-inflection.md', 'examples.md']:
            for word in re.findall('[가-힣]', (ROOT / file).read_text(encoding='utf-8')):
                base = chr(ord(word) - (ord(word) - 0xAC00) % 28)
                self.assertNotIn(base, UNUSED, (file, word))

    def test_history_text_is_preserved(self):
        manifest = json.loads((ROOT / 'history-manifest.json').read_text(encoding='utf-8'))
        for file, expected in manifest.items():
            # Git normalizes CRLF/LF across Windows and Linux; content must be identical.
            content = (ROOT / file).read_text(encoding='utf-8').encode('utf-8')
            self.assertEqual(hashlib.sha256(content).hexdigest(), expected, file)

    def test_audit_order_is_platform_independent(self):
        from audit_lexicon import inventory
        files = [row['file'] for row in inventory()]
        self.assertEqual(files, sorted(files))


if __name__ == '__main__':
    unittest.main()
