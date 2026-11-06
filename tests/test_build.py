from html.parser import HTMLParser
import re
import unittest

import build
from check_grammar import ROOT


class DocumentLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.targets = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.targets.append(attrs['href'][1:])


class BuildTests(unittest.TestCase):
    def test_site_sections_and_links(self):
        build.build()
        html = (ROOT / 'index.html').read_text(encoding='utf-8')
        parser = DocumentLinks()
        parser.feed(html)
        self.assertEqual(len(build.PAGES), 13)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        self.assertFalse(set(parser.targets) - set(parser.ids))
        self.assertIn('Ver.0.9', html)
        self.assertIn('歴史資料', html)
        self.assertNotIn('<span>010</span>', html)
        for _, _, filename in build.PAGES:
            self.assertTrue((ROOT / filename).is_file())

    def test_readme_chapter_order_matches_build(self):
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        files = re.findall(r'^\| (?:\d+|歴史\d+) \| \[([^]]+)\]', readme, re.M)
        self.assertEqual(files, [row[2] for row in build.PAGES])

    def test_local_markdown_links_exist(self):
        files = [ROOT / 'README.md'] + [ROOT / r[2] for r in build.PAGES]
        for path in files:
            for target in re.findall(r'\[[^]]+\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if not re.match(r'(https?://|#)', target):
                    self.assertTrue((path.parent / target).exists(), (path.name, target))

    def test_local_heading_links_support_japanese_and_repeated_headings(self):
        source = '[参照](#ver10-意味領域ガイド80語根試験運用)\n\n' + (
            '# Ver.1.0 意味領域ガイド（80語根・試験運用）\n\n' * 2)
        parser = DocumentLinks()
        parser.feed(build.render(source, 'dictionary'))
        target = 'dictionary-ver10-意味領域ガイド80語根試験運用'
        self.assertIn(target, parser.targets)
        self.assertIn(target, parser.ids)
        self.assertIn(target + '-1', parser.ids)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))


if __name__ == '__main__':
    unittest.main()
