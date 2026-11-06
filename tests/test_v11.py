import json
import unittest
from check_grammar import AUX, ACTIVE, UNUSED, GRAMMAR, LINKS, ROOT, parse, split

BY = {v:k for k,v in AUX.items()}

class IntegrationTests(unittest.TestCase):
    def one(self, sentence):
        result = parse(sentence)
        self.assertEqual(result['status'], 'parsed', (sentence, result))
        return result['analyses'][0]

    def test_inventory_and_pronounceable_markers(self):
        self.assertEqual((len(ACTIVE),len(UNUSED)),(80,24))
        self.assertFalse(GRAMMAR & (ACTIVE | UNUSED))
        for word in AUX:
            self.assertEqual((ord(split(word)[0])-0xAC00)//28%21,14) # ㅝ

    def test_each_auxiliary_in_positive_negative_question_tense_and_clause(self):
        for word in AUX:
            for sentence in [f'나 {word} 렉 치',f'나 퍄 {word} 렉 치',
                             f'나 {word} 퍄 렉 치', f'나 {word} 렉 치 훠',
                             f'나 틱 허 네 {word} 렉 치 혀']:
                with self.subTest(sentence=sentence): self.one(sentence)
            if word not in {BY['past'],BY['future']}:
                self.one(f'나 뤇 {word} 렉 치')
                self.one(f'나 뤅 {word} 렉 치')

    def test_scope_distinctions(self):
        for a,b in [('not','wish'),('not','obligation'),('not','ability'),('wish','ability')]:
            wa = '퍄' if a=='not' else BY[a]
            self.assertNotEqual(self.one(f'나 {wa} {BY[b]} 렉 치')['predicate'],
                                self.one(f'나 {BY[b]} {wa} 렉 치')['predicate'])
        self.assertNotEqual(self.one(f'나 뤇 {BY["wish"]} 렉 치')['predicate'],
                            self.one(f'나 뤇 {BY["intend"]} 렉 치')['predicate'])
        self.assertNotEqual(self.one(f'나 뤇 {BY["ability"]} 렉 치')['predicate'],
                            self.one('나 렋 치')['predicate'])

    def test_semantic_type_and_repetition_restrictions(self):
        for sentence in [f'나 {BY["ability"]} 칼',f'나 {BY["wish"]} {BY["wish"]} 렉 치']:
            self.assertEqual(parse(sentence)['status'],'unsupported')

    def test_nested_clause_and_case_attachment(self):
        self.one('나 틱 허 네 릭 허 나 뤇 렗 치 혀 혀')
        for word in LINKS:
            self.one(f'허 네 퍄 렉 치 혀 {word} 나 뤅 릭')
            self.one(f'허 네 렉 혀 {word} 허 나 록 혀 톼 나 릭')
        a=self.one('나 릭 허 네 멕 오 혀 제 히')
        b=self.one('나 릭 허 네 멕 오 제 히 혀')
        self.assertNotEqual(a,b)
        for bad in ['나 릭 허 네 멕 오','나 릭 네 멕 오 혀','나 멕 허 네 렉 훠 혀']:
            self.assertEqual(parse(bad)['status'],'unsupported')

    def test_serial_has_shared_arguments_without_success_inference(self):
        a=self.one('나 뤇 략 롸 륙 기')
        self.assertEqual(a['predicate'][0],'past')
        self.assertEqual(a['predicate'][1][0],'serial')
        self.assertEqual(a['object'],('head','기'))
        self.assertEqual(parse('나 략 기 륙 기')['status'],'unsupported')

    def test_questions_quantifiers_and_comparison(self):
        for sentence in ['훼 니 렉 기 훠','나 렉 훼 가 훠',
                         '나 록 훼 소 히 훠','나 렉 훼 사 히 훠',
                         '나 렉 훼 가 돠 훠','나 렉 훼 라 히 훠',
                         '나 렉 훼 기 훠','나 렉 훼 시 훠',
                         '훤 니 퍄 멕 오','훔 니 멕 오',
                         '옴 훌 칼 제 효','옴 훗 칼 제 효','옴 훙 칼 노 효']:
            self.one(sentence)
        self.assertEqual(parse('나 렉 훼 가')['status'],'unsupported')
        self.assertEqual(parse('나 멕 티')['status'],'ambiguous')
        self.assertEqual(parse('나 멕 티 훠')['status'],'parsed')

    def test_relative_roles(self):
        self.one('허 훍 렉 체 후 기 혀 후 니 각')
        self.one('허 니 렉 기 훍 히 혀 후 제 각')
        self.assertEqual(parse('훍 렉 기')['status'],'unsupported')
        self.assertEqual(parse('나 멕 허 훍 렉 기 혀')['status'],'unsupported')

    def test_round_trips(self):
        rows=json.loads((ROOT/'v1.1-translations.json').read_text(encoding='utf8'))
        self.assertGreaterEqual(len(rows),30)
        for r in rows:
            self.assertIn(r['grade'],[1,2,3,4])
            if r['serohan']:
                self.one(r['serohan'])
                self.assertTrue(r['back_translation'])
            else:
                self.assertEqual(r['grade'],4)
                self.assertTrue(r['reason'])
