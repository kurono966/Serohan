from collections import Counter
import json
import unittest

from check_grammar import ROOT, parse
from tatoeba_analysis import analyze


class TatoebaTests(unittest.TestCase):
    def test_source_snapshot_and_attribution(self):
        source, rows = analyze()
        self.assertEqual(len(source['sentences']), 60)
        self.assertEqual(len({r['id'] for r in rows}), 60)
        self.assertEqual(len(source['requests']), 10)
        for i, request in enumerate(source['requests']):
            sample = source['sentences'][i * 6:i * 6 + 6]
            self.assertTrue(all(r['id'] in request['returned_ids'] for r in sample))
        for row in rows:
            self.assertEqual(row['source'], 'Tatoeba')
            self.assertGreaterEqual(len(row['japanese']), 8)
            self.assertTrue(row['author'])
            self.assertEqual(row['license'], 'CC BY 2.0 FR')
            self.assertEqual(row['url'], f"https://tatoeba.org/en/sentences/show/{row['id']}")

    def test_originals_are_not_modified_by_analysis(self):
        source, rows = analyze()
        original = {r['id']: r for r in source['sentences']}
        for row in rows:
            for field in ['japanese', 'author', 'license', 'url']:
                self.assertEqual(row[field], original[row['id']][field])
        self.assertEqual(original[155213]['japanese'], '私は大学に行きたい。')

    def test_fidelity_and_missing_translations_are_explicit(self):
        _, rows = analyze()
        self.assertEqual(Counter(r['fidelity'] for r in rows), {'部分': 10, '不能': 50})
        for row in rows:
            self.assertTrue(row['issue'])
            self.assertTrue(row['missing'])
            if row['fidelity'] == '不能':
                self.assertIsNone(row['serohan'])
                self.assertIsNone(row['literal'])

    def test_partial_translations_use_defined_syntax(self):
        _, rows = analyze()
        for row in rows:
            if row['serohan']:
                self.assertEqual(parse(row['serohan'])['status'], 'parsed', row['id'])
                self.assertTrue(row['literal'])

    def test_parse_success_does_not_promote_failed_candidates(self):
        _, rows = analyze()
        for row in rows:
            if row['rejected_candidate']:
                self.assertEqual(parse(row['rejected_candidate'][0])['status'], 'parsed', row['id'])
                self.assertEqual(row['fidelity'], '不能')
                self.assertIsNone(row['serohan'])
        by_id = {r['id']: r for r in rows}
        self.assertNotIn('W', by_id[5404545]['issue_types'])  # Ability, not a WH question.
        self.assertNotIn('W', by_id[176812]['issue_types'])  # Six o'clock is numeric.

    def test_saved_evaluation_matches_generated_review(self):
        _, rows = analyze()
        saved = json.loads((ROOT / 'tatoeba-cases.json').read_text(encoding='utf-8'))
        # JSON represents the optional candidate tuple as an array.
        expected = json.loads(json.dumps(rows, ensure_ascii=False))
        self.assertEqual(saved, expected)
        report = (ROOT / 'tatoeba-report.md').read_text(encoding='utf-8')
        self.assertIn('CC BY 2.0 FR', report)
        self.assertIn('忠実に全文を保持：0件', report)
        for row in rows:
            self.assertIn(row['url'], report)


if __name__ == '__main__':
    unittest.main()
