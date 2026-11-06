"""Reproducible partial syntax and corpus report, separate from human fidelity."""
import json
from collections import Counter
from pathlib import Path
from check_grammar import parse

ROOT = Path(__file__).resolve().parent


def sentence_parts(text):
    return [s.strip() for s in text.split('.') if s.strip()]


def report():
    rows = json.loads((ROOT / 'translation-cases.json').read_text(encoding='utf-8'))
    counts = Counter(r['fidelity'] for r in rows)
    lines = ['# Ver.0.9 翻訳ストレステスト', '',
             '全60件、自作。外部取得0件。出所と取得失敗の記録は監査記録を参照。', '',
             '保持度は意味に関する人手評価。構文成功は意味の保持を証明しない。', '',
             '／'.join(f'{key}: {value}件' for key, value in counts.items()), '',
             '| ID・分類 | 日本語 | セロハン語 | 逐語訳 | 保持度 | 文法・意味の問題 | 不足概念 | 部分解析 |',
             '| --- | --- | --- | --- | --- | --- | --- | --- |']
    for r in rows:
        statuses = [parse(s)['status'] for s in sentence_parts(r['serohan'] or '')]
        cells = [f"{r['id']} {r['category']}", r['japanese'], r['serohan'] or '未訳',
                 r['literal'] or '—', r['fidelity'], r['issue'], r['missing'],
                 ', '.join(statuses) or '対象外']
        lines.append('| ' + ' | '.join(cells) + ' |')
    (ROOT / 'translation-report.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(dict(counts))


if __name__ == '__main__':
    report()
