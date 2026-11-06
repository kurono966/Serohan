"""Fetch a random public sample and freeze it; never filter for translatability.

Network step is manual, not CI. Stored source IDs/text are the reproducible input.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

PAGES = range(1, 11)
ROOT = Path(__file__).resolve().parent


def fetch(page):
    url = 'https://tatoeba.org/en/api_v0/search?' + urlencode(
        {'from': 'jpn', 'query': '', 'to': 'und', 'sort': 'random', 'page': page})
    with urlopen(url, timeout=40) as response:
        data = json.load(response)
    return page, url, data['results']


def main():
    rows, seen, requests = [], set(), []
    with ThreadPoolExecutor(max_workers=3) as executor:
        for page, url, results in executor.map(fetch, PAGES):
            requests.append({'page': page, 'url': url,
                             'returned_ids': [r['id'] for r in results]})
            selected = 0
            for r in results:
                if r['id'] in seen or len(r['text']) < 8:
                    continue
                seen.add(r['id'])
                rows.append({'id': r['id'], 'japanese': r['text'],
                             'url': f"https://tatoeba.org/en/sentences/show/{r['id']}",
                             'author': (r.get('user') or {}).get('username'),
                             'license': r.get('license'), 'correctness': r.get('correctness')})
                selected += 1
                if selected == 6:
                    break
            if selected != 6:
                raise RuntimeError(f'page {page}: only {selected} unique sentences; no substitute invented')
    result = {'retrieved_at_utc': datetime.now(timezone.utc).isoformat(),
              'selection': '日本語ランダム順10ページ×各先頭6件。ID重複と8文字未満のみ除外。翻訳可能性では選別しない。',
              'requests': requests, 'sentences': rows}
    (ROOT / 'tatoeba-source.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)
                                            + '\n', encoding='utf-8')
    for row in rows:
        print(row['id'], row['japanese'])


if __name__ == '__main__':
    main()
