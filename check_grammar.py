"""Conservative v0.9 subset parser; no third-party dependencies.

An unsupported result is not a proof of ungrammaticality. All complete
analyses in this subset are retained, including lexical/question ti.
"""
from pathlib import Path
from functools import lru_cache
import json
import re
import sys

ROOT = Path(__file__).resolve().parent
CODAS = ('', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
         'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ',
         'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')
FORMS = {'', 'ㄱ', 'ㄹ', 'ㅂ', 'ㅁ', 'ㄳ', 'ㄺ', 'ㄼ', 'ㄶ', 'ㄾ', 'ㅀ', 'ㅄ'}
VERBS = {'ㄱ', 'ㄳ', 'ㄺ', 'ㄼ', 'ㄶ', 'ㄾ', 'ㅀ', 'ㅄ'}
ASPECT = {'ㄱ': 'unmarked', 'ㄳ': 'past', 'ㄺ': 'future', 'ㄼ': 'wish',
          'ㄶ': 'negative', 'ㄾ': 'complete', 'ㅀ': 'continuing', 'ㅄ': 'obligation'}
PARTICLES = {'하', '헤', '히', '호', '후'}


def lexicon():
    rows = re.findall(r'^\| ([가-힣]) \|[^\n]*\| (使用|未使用) \|\s*$',
                      (ROOT / 'dictionary.md').read_text(encoding='utf-8'), re.M)
    active, unused = set(), set()
    for root, status in rows:
        (unused if status == '未使用' else active).add(root)
    return active, unused


ACTIVE, UNUSED = lexicon()


def split(word):
    if len(word) != 1 or not 0xAC00 <= ord(word) <= 0xD7A3:
        raise ValueError('一語はハングル一音節: ' + word)
    offset = ord(word) - 0xAC00
    return chr(ord(word) - offset % 28), CODAS[offset % 28]


def validate(tokens):
    errors = []
    for word in tokens:
        if word in PARTICLES:
            continue
        try:
            root, coda = split(word)
            if root not in ACTIVE:
                errors.append('未使用または未採用の語根・助詞: ' + word)
            elif coda not in FORMS:
                errors.append('未採用の終声: ' + word)
        except ValueError as error:
            errors.append(str(error))
    return errors


def parse(text):
    # Final punctuation carries no syntactic information, including ?.
    tokens = tuple(text.strip().rstrip('.。?!？！').split())
    errors = validate(tokens)
    if errors:
        return {'status': 'invalid_lexeme', 'errors': errors, 'analyses': []}

    def form(i):
        return split(tokens[i])[1] if i < len(tokens) and tokens[i] not in PARTICLES else None

    @lru_cache(None)
    def attributes(i):
        out = []
        j = i
        while j < len(tokens) and tokens[j] == '퍄':
            j += 1
        if form(j) == 'ㄹ':
            node = ('attribute', split(tokens[j])[0])
            for _ in range(j - i):
                node = ('not', node)
            out.append((j + 1, node))
        return tuple(out)

    @lru_cache(None)
    def simple(i):
        out = []
        if form(i) in {'', 'ㅁ'}:
            out.append((i + 1, ('head', tokens[i])))
        for end, attr in attributes(i):
            for stop, tail in simple(end):
                out.append((stop, ('modify', attr, tail)))
        return tuple(out)

    @lru_cache(None)
    def np(i):
        out = list(simple(i))
        for end, left in simple(i):
            if end < len(tokens) and tokens[end] == '후':
                for stop, right in np(end + 1):
                    # Mixed ha/hu association remains unspecified.
                    if not contains(right, 'and'):
                        out.append((stop, ('related', left, right)))
            if end < len(tokens) and tokens[end] == '하':
                for stop, right in simple(end + 1):
                    out.append((stop, ('and', left, right)))
        return tuple(out)

    def pred(i):
        j = i
        while j < len(tokens) and tokens[j] == '퍄':
            j += 1
        if form(j) in VERBS | {'ㄹ'}:
            coda = form(j)
            node = ('attribute', split(tokens[j])[0]) if coda == 'ㄹ' else (
                'verb', split(tokens[j])[0], 'unmarked' if coda == 'ㄶ' else ASPECT[coda])
            if coda == 'ㄶ':
                node = ('not', node)
            for _ in range(j - i):
                node = ('not', node)
            yield j + 1, node, coda in VERBS

    @lru_cache(None)
    def cases(i, limit):
        if i == limit:
            return ((),)
        out = []
        for end, obj in np(i):
            if end < limit and tokens[end] in {'헤', '히', '호'}:
                for rest in cases(end + 1, limit):
                    out.append(((tokens[end], obj),) + rest)
        return tuple(out)

    analyses = []
    limits = [(len(tokens), False)]
    if tokens and tokens[-1] == '티':
        limits.append((len(tokens) - 1, True))
    for limit, question in limits:
        for end, subject in np(0):
            j, adverbs = end, []
            while j < limit and form(j) == 'ㅂ':
                adverbs.append(tokens[j])
                j += 1
            for stop, predicate, verbal in pred(j):
                # Existence has a specified intransitive frame (v0.8).
                core = predicate
                while core[0] == 'not':
                    core = core[1]
                transitive = verbal and core[1] != '가'
                objects = [(stop, None)] + (list(np(stop)) if transitive else [])
                for after, obj in objects:
                    for adjuncts in cases(after, limit):
                        analyses.append({'subject': subject, 'predicate': predicate,
                                         'object': obj, 'adverbs': tuple(adverbs),
                                         'cases': adjuncts, 'question': question})
    # Keep structural alternatives, remove duplicate derivations only.
    unique = {json.dumps(a, ensure_ascii=False, sort_keys=True): a for a in analyses}
    analyses = list(unique.values())
    status = 'ambiguous' if len(analyses) > 1 else 'parsed' if analyses else 'unsupported'
    return {'status': status, 'errors': [], 'analyses': analyses}


def contains(node, tag):
    return isinstance(node, tuple) and (node[0] == tag or any(contains(n, tag) for n in node[1:]))


if __name__ == '__main__':
    print(json.dumps(parse(' '.join(sys.argv[1:])), ensure_ascii=False, indent=2))
