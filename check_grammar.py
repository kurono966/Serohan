"""Conservative v0.9 subset parser; no third-party dependencies.

An unsupported result is not a proof of ungrammaticality. All complete
analyses in this subset are retained, including lexical/question ti.
"""
from pathlib import Path
from functools import lru_cache
import json
import re
import sys
from itertools import product

ROOT = Path(__file__).resolve().parent
CODAS = ('', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ',
         'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ',
         'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')
FORMS = {'', 'ㄱ', 'ㄹ', 'ㅂ', 'ㅁ', 'ㄳ', 'ㄺ', 'ㄼ', 'ㄶ', 'ㄾ', 'ㅀ', 'ㅄ'}
VERBS = {'ㄱ', 'ㄳ', 'ㄺ', 'ㄼ', 'ㄶ', 'ㄾ', 'ㅀ', 'ㅄ'}
ASPECT = {'ㄱ': 'unmarked', 'ㄳ': 'past', 'ㄺ': 'future', 'ㄼ': 'wish',
          'ㄶ': 'negative', 'ㄾ': 'complete', 'ㅀ': 'continuing', 'ㅄ': 'obligation'}
PARTICLES = {'하', '헤', '히', '호', '후'}
AUX = {chr(ord(root) + CODAS.index(coda)): meaning for root, coda, meaning in [
    ('뤄', 'ㄳ', 'past'), ('뤄', 'ㄱ', 'future'), ('뤄', 'ㅀ', 'continuing'),
    ('뤄', 'ㄾ', 'complete'), ('꿔', 'ㄱ', 'ability'), ('붜', 'ㄱ', 'permission'),
    ('퉈', 'ㄱ', 'possible'), ('퉈', 'ㄺ', 'probable'), ('뭐', 'ㄱ', 'wish'),
    ('뭐', 'ㄺ', 'intend'), ('붜', 'ㄳ', 'obligation'), ('쿼', 'ㄱ', 'recommend'),
    ('숴', 'ㄱ', 'begin')]}
LINKS = {'톼': 'condition', '솨': 'time', '돠': 'reason', '퐈': 'contrast',
         '롸': 'sequence', '놔': 'result', '뫄': 'purpose'}
NP_MARKERS = {'훼': 'query', '훤': 'all', '훔': 'some'}
COMPARE = {'훌': 'greater', '훗': 'equal', '훙': 'maximum'}
GRAMMAR = set(AUX) | set(LINKS) | set(NP_MARKERS) | set(COMPARE) | {'허', '혀', '훠', '효', '훍'}


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
        if word in PARTICLES | GRAMMAR:
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


def parse(text, _gap=False):
    # Final punctuation carries no syntactic information, including ?.
    tokens = tuple(text.strip().rstrip('.。?!？！').split())
    errors = validate(tokens)
    if errors:
        return {'status': 'invalid_lexeme', 'errors': errors, 'analyses': []}

    # Close the innermost spoken clause first; every bracket has audible content.
    if '훍' in tokens and not _gap:
        depth = 0
        for word in tokens:
            depth += word == '허'
            depth -= word == '혀'
            if word == '훍' and depth == 0:
                return pack([])
    embedded = {}
    work = list(tokens)
    stack = []
    for i, word in enumerate(work):
        if word == '허':
            stack.append(i)
        elif word == '혀':
            if not stack:
                return {'status': 'unsupported', 'errors': ['unmatched 혀'], 'analyses': []}
            start = stack.pop()
            if not stack:
                inner = parse(' '.join(work[start + 1:i]), _gap=True)
                if '훍' in work[start + 1:i] and (i + 1 >= len(work) or work[i + 1] != '후'):
                    return pack([])
                if not inner['analyses'] or any(a.get('question') for a in inner['analyses']):
                    return {'status': 'unsupported', 'errors': ['invalid embedded clause'], 'analyses': []}
                embedded[start] = (i, inner['analyses'])
    if stack:
        return {'status': 'unsupported', 'errors': ['unmatched 허'], 'analyses': []}
    if embedded and 0 in embedded:
        end, left = embedded[0]
        if end + 1 < len(tokens) and tokens[end + 1] in LINKS:
            right = parse(' '.join(tokens[end + 2:]))
            analyses = [{'link': LINKS[tokens[end + 1]], 'left': a, 'right': b}
                        for a in left for b in right['analyses']]
            return pack(analyses)
    values = {}
    compact, i = [], 0
    while i < len(tokens):
        if i in embedded:
            end, analyses = embedded[i]
            key = '§' + str(i)
            values[key] = analyses
            compact.append(key)
            i = end + 1
        else:
            compact.append(tokens[i])
            i += 1
    tokens = tuple(compact)

    def form(i):
        if i >= len(tokens):
            return None
        if tokens[i] in values:
            return ''
        if tokens[i] == '훍':
            return ''
        return split(tokens[i])[1] if tokens[i] not in PARTICLES | GRAMMAR else None

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
        if i < len(tokens) and tokens[i] in NP_MARKERS:
            for end, node in simple(i + 1):
                out.append((end, (NP_MARKERS[tokens[i]], node)))
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
        if i < len(tokens) and tokens[i] in set(AUX) | set(COMPARE) | {'퍄'}:
            for end, node, verbal in pred(i + 1):
                op = AUX.get(tokens[i], COMPARE.get(tokens[i], 'not'))
                if tokens[i] in AUX and node[0] == op:
                    continue
                if tokens[i] in COMPARE and verbal:
                    continue
                if tokens[i] in AUX and not verbal and op not in {'past', 'future', 'possible', 'probable'}:
                    continue
                yield end, (op, node), verbal
            return
        j = i
        if form(j) in VERBS | {'ㄹ'}:
            coda = form(j)
            node = ('attribute', split(tokens[j])[0]) if coda == 'ㄹ' else (
                'verb', split(tokens[j])[0], 'unmarked' if coda == 'ㄶ' else ASPECT[coda])
            if coda == 'ㄶ':
                node = ('not', node)
            yield j + 1, node, coda in VERBS
            if j + 1 < len(tokens) and tokens[j + 1] == '롸' and coda in VERBS:
                for end, second, verbal in pred(j + 2):
                    if verbal:
                        yield end, ('serial', node, second), True

    @lru_cache(None)
    def cases(i, limit):
        if i == limit:
            return ((),)
        out = []
        for end, obj in np(i):
            if end < limit and tokens[end] in {'헤', '히', '호', '효', '돠'}:
                for rest in cases(end + 1, limit):
                    out.append(((tokens[end], obj),) + rest)
        return tuple(out)

    analyses = []
    limits = [(len(tokens), False)]
    if tokens and tokens[-1] == '티':
        limits.append((len(tokens) - 1, True))
    if tokens and tokens[-1] == '훠':
        limits = [(len(tokens) - 1, True)]
    for limit, question in limits:
        for end, subject in np(0):
            j, adverbs = end, []
            while j < limit and form(j) == 'ㅂ':
                adverbs.append(tokens[j])
                j += 1
            for stop, predicate, verbal in pred(j):
                # Existence has a specified intransitive frame (v0.8).
                core = predicate
                while len(core) == 2 and core[0] != 'attribute':
                    core = core[1]
                transitive = verbal and core[1] != '가'
                objects = [(stop, None)] + (list(np(stop)) if transitive else [])
                for after, obj in objects:
                    for adjuncts in cases(after, limit):
                        if any(contains(predicate, op) for op in COMPARE.values()) and not any(c[0]=='효' for c in adjuncts):
                            continue
                        analyses.append({'subject': subject, 'predicate': predicate,
                                         'object': obj, 'adverbs': tuple(adverbs),
                                         'cases': adjuncts, 'question': question})
    # Keep structural alternatives, remove duplicate derivations only.
    unique = {json.dumps(a, ensure_ascii=False, sort_keys=True): a for a in analyses}
    analyses = list(unique.values())
    status = 'ambiguous' if len(analyses) > 1 else 'parsed' if analyses else 'unsupported'
    def expand(node):
        if isinstance(node, tuple):
            if len(node) == 2 and node[0] == 'head' and node[1] in values:
                return ('clause', chosen[node[1]])
            return tuple(expand(x) for x in node)
        if isinstance(node, dict):
            return {k: expand(v) for k, v in node.items()}
        return node
    analyses = [a for a in analyses if a['question'] or not any(
        contains(a[k], 'query') for k in ('subject', 'object')) and not any(
        contains(c[1], 'query') for c in a['cases'])]
    expanded = []
    for combination in product(*values.values()):
        chosen = dict(zip(values, combination))
        expanded.extend(expand(a) for a in analyses)
    return pack(expanded)


def pack(analyses):
    return {'status': 'ambiguous' if len(analyses) > 1 else 'parsed' if analyses else 'unsupported',
            'errors': [], 'analyses': analyses}


def contains(node, tag):
    return isinstance(node, tuple) and (node[0] == tag or any(contains(n, tag) for n in node[1:]))


if __name__ == '__main__':
    print(json.dumps(parse(' '.join(sys.argv[1:])), ensure_ascii=False, indent=2))
