"""Inventory inactive roots in preserved pre-v0.9 teaching documents."""
import json
import re
from check_grammar import ROOT, UNUSED, split


def inventory():
    findings = []
    # Path ordering is case-insensitive on Windows, case-sensitive on Linux.
    for path in sorted((ROOT / 'history').glob('*-pre-v0.9.md'), key=lambda p: p.as_posix()):
        for number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
            for word in re.findall('[가-힣]', line):
                root, _ = split(word)
                if root in UNUSED:
                    findings.append(dict(file=path.relative_to(ROOT).as_posix(), line=number,
                                         surface=word, root=root))
    return findings


if __name__ == '__main__':
    findings = inventory()
    (ROOT / 'history' / 'audit-lexemes.json').write_text(json.dumps(findings, ensure_ascii=False, indent=2)
                                          + '\n', encoding='utf-8')
    print(f'{len(findings)} inactive-root occurrences in historical teaching documents')
