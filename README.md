# セロハン語（Serohan）Ver.0.9

ハングル一音節の80語根と終声で意味を組み立てる人工言語。SVO、複数属性、후右結合、所在所有を維持し、否定の作用域を整理した。24未使用枠は変更していない。

```text
나 멚 오
私は木を愛していない。
나 멣 퍄 칼 오
私は大きくない木を愛している。
나 퍄 멚 오
私は木を愛していないわけではない。
```

## 読む順番とWeb版

[index.html](index.html)を開くとオフラインで現行9章・歴史4章を読める。辞書検索はJavaScriptを使用し、本文は無効でも読める。

| 章 | ファイル | 内容 |
| --- | --- | --- |
| 1 | [overview.md](overview.md) | 現行概要・文字・語形成 |
| 2 | [grammar.md](grammar.md) | 基本文法 |
| 3 | [grammar-v0.9.md](grammar-v0.9.md) | 否定の新規則・接続の比較・未解決事項 |
| 4 | [dictionary.md](dictionary.md) | 語根配置Ver.0.7を維持（80使用・24未使用） |
| 5 | [particles.md](particles.md) | 5助詞と予約語 |
| 6 | [verb-inflection.md](verb-inflection.md) | 7種の試験運用活用 |
| 7 | [examples.md](examples.md) | 80語根による現行例文 |
| 8 | [translation-report.md](translation-report.md) | 自作60件の検証 |
| 9 | [tatoeba-report.md](tatoeba-report.md) | 外部取得60件の翻訳試行・不足分析 |
| 歴史1 | [grammar-v0.6.md](grammar-v0.6.md) | 暫定採用の記録 |
| 歴史2 | [grammar-v0.7-compounds.md](grammar-v0.7-compounds.md) | 複数修飾・후右結合 |
| 歴史3 | [grammar-v0.8-existence.md](grammar-v0.8-existence.md) | 存在・所在所有・照応 |
| 歴史4 | [lexicon-v0.7-migration.md](lexicon-v0.7-migration.md) | 旧語根の移行候補 |

## 検証と設計判断

[audit-v0.9.md](audit-v0.9.md)に矛盾、取得失敗、採用履歴を記録。[grammar-v0.9.md](grammar-v0.9.md)に接続・否定の採否と理由を記載する。節接続、補文、等値否定、量化、3項並列、후と하の混在は未採用／未定。文末티の音声上の曖昧性も残る。

実行結果と変更ファイル一覧は[validation-results.md](validation-results.md)。

```text
python -m unittest discover -s tests -v
python translation_data.py
python verify.py
python audit_lexicon.py
python tatoeba_analysis.py
python build.py
python check_grammar.py 나 퍄 멚 오
```

Python 3.10以降の標準ライブラリだけで実行できる。`parsed`は部分文法内の解析成功であり、翻訳精度や言語全体の正当性の証明ではない。テストはCIでも実行する。

Tatoeba実例は`tatoeba-source.json`にID・原文・投稿者・ライセンス付きで保存。ランダム標本のため再取得結果は変わる。`fetch_tatoeba.py`は手動のネットワーク取得用で、CIは保存標本を使う。自作60件と混ぜず、部分訳・不能・意味を変える却下候補を区別する。

## 保存資料

整理前のREADME・概要・基本文法・助詞・活用・例文を[history/README-pre-v0.9.md](history/README-pre-v0.9.md)などに原文のまま保存した。[dictionary-v0.3.md](dictionary-v0.3.md)は旧104語根辞書。0.6～0.8の仕様ファイルは改変していない。

Web版の生成は `build.py`、表示は `assets/style.css`・`assets/site.js`。Markdownや翻訳データを変更したら生成物も更新する。main反映後は既存GitHub ActionsがHTMLを更新する。GitHub Pagesの想定公開先は [kurono966.github.io/Serohan](https://kurono966.github.io/Serohan/)。
