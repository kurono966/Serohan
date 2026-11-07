"""Build the offline documentation site with Python's standard library."""
from html import escape
from pathlib import Path, PurePosixPath
from posixpath import normpath
import re
import unicodedata

ROOT = Path(__file__).resolve().parent
PAGES = [
    ('overview', '設計概要', 'overview.md'),
    ('grammar', '基本文法', 'grammar.md'),
    ('grammar-v09', 'Ver.0.9 否定・設計判断', 'grammar-v0.9.md'),
    ('grammar-v11', 'Ver.1.1 統合仕様', 'grammar-v1.1.md'),
    ('auxiliaries', '助動詞の採用履歴', 'auxiliaries-v1.0.md'),
    ('clauses', '節の採用履歴', 'clauses-v1.0.md'),
    ('roundtrips', 'Ver.1.1 翻訳検証', 'v1.1-translations.md'),
    ('dictionary', '語根辞書', 'dictionary.md'),
    ('particles', '助詞', 'particles.md'),
    ('verb-inflection', '動詞活用（試験運用）', 'verb-inflection.md'),
    ('examples', '現行例文集', 'examples.md'),
    ('translations', '翻訳ストレステスト', 'translation-report.md'),
    ('grammar-v06', '歴史資料 Ver.0.6', 'history/grammar-v0.6.md'),
    ('grammar-v07', '歴史資料 Ver.0.7', 'history/grammar-v0.7-compounds.md'),
    ('grammar-v08', '歴史資料 Ver.0.8', 'history/grammar-v0.8-existence.md'),
    ('migration', '歴史資料 語根移行表', 'history/lexicon-v0.7-migration.md'),
]


<<<<<<< HEAD
def inline(text, source_dir):
=======
def heading_fragment(text):
    return ''.join(c for c in text.lower() if c in '-_' or
                   not unicodedata.category(c).startswith(('P', 'S'))).replace(' ', '-')


def inline(text, slug=None):
>>>>>>> 24f66a7c90d4983d7a7b3f767027fd75b6bebbf0
    text = escape(text)
    # Protect inline code before applying other inline syntax.
    codes = []
    def code(match):
        codes.append('<code>' + match[1] + '</code>')
        return f'\x00{len(codes) - 1}\x00'
    text = re.sub(r'`([^`]+)`', code, text)
    def link(match):
        label, target = match.groups()
<<<<<<< HEAD
        if not re.match(r'(?:[A-Za-z][A-Za-z0-9+.-]*:|[\/#])', target):
            target = normpath((source_dir / target).as_posix())
        for slug, _, filename in PAGES:
=======
        if slug and target.startswith('#'):
            target = '#' + slug + '-' + target[1:]
        for page_slug, _, filename in PAGES:
>>>>>>> 24f66a7c90d4983d7a7b3f767027fd75b6bebbf0
            if target == filename:
                target = '#' + page_slug
        return f'<a href="{target}">{label}</a>'
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    return re.sub(r'\x00(\d+)\x00', lambda m: codes[int(m[1])], text)


def render(source, slug, filename):
    source_dir = PurePosixPath(filename).parent

    def render_inline(text):
        return inline(text, source_dir)

    lines = source.splitlines()
    output, i, heading = [], 0, 0
    fragments = {}
    def special(line):
        return bool(re.match(r'^(#{1,6} |```|\||> |[-*] |\d+\. |---+$)', line))
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith('```'):
            i += 1
            block = []
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i])
                i += 1
            output.append('<pre><code>' + escape('\n'.join(block)) + '</code></pre>')
            i += 1
        elif line.startswith('#'):
            match = re.match(r'^(#{1,6}) (.*)', line)
            level = min(len(match[1]) + 1, 6)
            heading += 1
<<<<<<< HEAD
            output.append(f'<h{level} id="{slug}-{heading}">{render_inline(match[2])}</h{level}>')
=======
            fragment = heading_fragment(match[2])
            count = fragments.get(fragment, 0)
            fragments[fragment] = count + 1
            if count:
                fragment += '-' + str(count)
            alias = f'<span id="{slug}-{fragment}"></span>'
            output.append(f'<h{level} id="{slug}-{heading}">{alias}{inline(match[2], slug)}</h{level}>')
>>>>>>> 24f66a7c90d4983d7a7b3f767027fd75b6bebbf0
            i += 1
        elif line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r':?-+:?', c) for c in cells):
                    rows.append(cells)
                i += 1
            table = '<div class="table-wrap"><table><thead><tr>'
<<<<<<< HEAD
            table += ''.join('<th scope="col">' + render_inline(c) + '</th>' for c in rows[0])
            table += '</tr></thead><tbody>'
            for row in rows[1:]:
                table += '<tr>' + ''.join('<td>' + render_inline(c) + '</td>' for c in row) + '</tr>'
=======
            table += ''.join('<th scope="col">' + inline(c, slug) + '</th>' for c in rows[0])
            table += '</tr></thead><tbody>'
            for row in rows[1:]:
                table += '<tr>' + ''.join('<td>' + inline(c, slug) + '</td>' for c in row) + '</tr>'
>>>>>>> 24f66a7c90d4983d7a7b3f767027fd75b6bebbf0
            output.append(table + '</tbody></table></div>')
        elif re.fullmatch('-{3,}', line):
            output.append('<hr>')
            i += 1
        elif line.startswith('> '):
<<<<<<< HEAD
            output.append('<blockquote>' + render_inline(line[2:]) + '</blockquote>')
=======
            output.append('<blockquote>' + inline(line[2:], slug) + '</blockquote>')
>>>>>>> 24f66a7c90d4983d7a7b3f767027fd75b6bebbf0
            i += 1
        elif re.match(r'^([-*] |\d+\. )', line):
            ordered = bool(re.match(r'^\d+\.', line))
            tag = 'ol' if ordered else 'ul'
            items = []
            pattern = r'^\d+\. ' if ordered else r'^[-*] '
            while i < len(lines) and re.match(pattern, lines[i].strip()):
<<<<<<< HEAD
                items.append('<li>' + render_inline(re.sub(pattern, '', lines[i].strip())) + '</li>')
=======
                items.append('<li>' + inline(re.sub(pattern, '', lines[i].strip()), slug) + '</li>')
>>>>>>> 24f66a7c90d4983d7a7b3f767027fd75b6bebbf0
                i += 1
            output.append(f'<{tag}>' + ''.join(items) + f'</{tag}>')
        else:
            paragraph = [line]
            i += 1
            while i < len(lines) and lines[i].strip() and not special(lines[i].strip()):
                paragraph.append(lines[i].strip())
                i += 1
<<<<<<< HEAD
            output.append('<p>' + render_inline(' '.join(paragraph)) + '</p>')
=======
            output.append('<p>' + inline(' '.join(paragraph), slug) + '</p>')
>>>>>>> 24f66a7c90d4983d7a7b3f767027fd75b6bebbf0
    return '\n'.join(output)


def build():
    navigation = ''.join(f'<a href="#{slug}"><span>{i:02d}</span>{label}</a>' for i, (slug, label, _) in enumerate(PAGES, 1))
    articles = []
    for slug, label, filename in PAGES:
        search = ''
        if slug == 'dictionary':
            search = '<div class="search"><label for="dictionary-search">語根を探す</label><input id="dictionary-search" type="search" placeholder="ハングル・ラテン転写・日本語で検索" autocomplete="off"><p id="search-status" role="status" aria-live="polite"></p></div>'
        articles.append(f'<section class="chapter" id="{slug}" aria-label="{label}"><div class="chapter-label">SEROHAN / {label}</div>{search}' + render((ROOT / filename).read_text(encoding='utf-8'), slug, filename) + '</section>')
    html = '''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="ハングル一音節に、概念と役割を。人工言語セロハン語の文法・80語根・例文を読むための資料サイト。"><title>Serohan — セロハン語</title><link rel="stylesheet" href="assets/style.css"><script src="assets/site.js" defer></script></head>
<body><a class="skip" href="#main">本文へ移動</a><header class="topbar"><a class="brand" href="#home">세로한 <span>SEROHAN</span></a><span class="edition">LANGUAGE NOTES · 2026</span></header>
<div class="layout"><aside><nav aria-label="章ナビゲーション"><a class="home-link" href="#home">はじめに</a>''' + navigation + '''</nav><div class="sidebar-note">概念 → 役割 → 関係<br>小さな規則で、豊かな表現を。</div></aside>
<main id="main"><section id="home" class="hero"><div class="eyebrow">A CONSTRUCTED LANGUAGE</div><h1>一音節から、<br>広がることば。</h1><p class="intro">ハングルの構造から生まれた人工言語、セロハン語。<br>一つの概念に終声を添えて、表現のかたちを変える。</p><div class="word-study"><div><b lang="ko">메</b><span>概念 / 愛</span></div><span class="arrow" aria-hidden="true">→</span><div><b lang="ko">멕</b><span>行為 / 愛する</span></div><span class="arrow" aria-hidden="true">→</span><div><b lang="ko">멥</b><span>修飾 / 愛をもって</span></div></div><div class="hero-bottom"><a class="button" href="#grammar">基本文法から読む <span aria-hidden="true">↗</span></a><p>80 語根 <span> / </span> 5 基本助詞 <span> / </span> SVO 語順</p></div><p class="scope">基本体系と活用の試案を収録。未定の規則は各章に明記しています。</p></section>''' + ''.join(articles) + '''<footer>Serohan · セロハン語 <a href="#home">ページの先頭へ ↑</a></footer></main></div></body></html>'''
    (ROOT / 'index.html').write_text(html, encoding='utf-8')
    print(f'Built index.html: {len(PAGES)} chapters')


if __name__ == '__main__':
    build()
