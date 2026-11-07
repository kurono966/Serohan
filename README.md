# セロハン語（Serohan）Ver.1.1

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

[index.html](index.html)を開くとオフラインで全16章を読める。辞書検索はJavaScriptを使用し、本文は無効でも読める。

| 章 | ファイル | 内容 |
| --- | --- | --- |
| 1 | [overview.md](overview.md) | 設計概要 |
| 2 | [grammar.md](grammar.md) | 基本文法 |
| 3 | [grammar-v0.9.md](grammar-v0.9.md) | Ver.0.9 否定・設計判断 |
| 4 | [grammar-v1.1.md](grammar-v1.1.md) | Ver.1.1 統合仕様 |
| 5 | [auxiliaries-v1.0.md](auxiliaries-v1.0.md) | 助動詞の採用履歴 |
| 6 | [clauses-v1.0.md](clauses-v1.0.md) | 節の採用履歴 |
| 7 | [v1.1-translations.md](v1.1-translations.md) | Ver.1.1 翻訳検証 |
| 8 | [dictionary.md](dictionary.md) | 語根辞書 |
| 9 | [particles.md](particles.md) | 助詞 |
| 10 | [verb-inflection.md](verb-inflection.md) | 動詞活用（試験運用） |
| 11 | [examples.md](examples.md) | 現行例文集 |
| 12 | [translation-report.md](translation-report.md) | 翻訳ストレステスト |
| 13 | [history/grammar-v0.6.md](history/grammar-v0.6.md) | 歴史資料 Ver.0.6 |
| 14 | [history/grammar-v0.7-compounds.md](history/grammar-v0.7-compounds.md) | 歴史資料 Ver.0.7 |
| 15 | [history/grammar-v0.8-existence.md](history/grammar-v0.8-existence.md) | 歴史資料 Ver.0.8 |
| 16 | [history/lexicon-v0.7-migration.md](history/lexicon-v0.7-migration.md) | 歴史資料 語根移行表 |

## 検証と設計判断

[audit-v0.9.md](history/audit-v0.9.md)に矛盾、取得失敗、採用履歴を記録。[grammar-v0.9.md](grammar-v0.9.md)に接続・否定の採否と理由を記載する。節接続、補文、等値否定、量化、3項並列、후と하の混在は未採用／未定。文末티の音声上の曖昧性も残る。

実行結果と変更ファイル一覧は[validation-results.md](history/validation-results.md)。

```text
python -m unittest discover -s tests -v
python translation_data.py
python verify.py
python audit_lexicon.py
python build.py
python check_grammar.py 나 퍄 멚 오
```

Python 3.10以降の標準ライブラリだけで実行できる。`parsed`は部分文法内の解析成功であり、翻訳精度や言語全体の正当性の証明ではない。テストはCIでも実行する。

## 保存資料

整理前のREADME・概要・基本文法・助詞・活用・例文を[history/README-pre-v0.9.md](history/README-pre-v0.9.md)などに原文のまま保存した。[dictionary-v0.3.md](history/dictionary-v0.3.md)は旧104語根辞書。旧仕様・旧辞書・当時の監査記録は [history](history/) にまとめた。

Web版の生成は `build.py`、表示は `assets/style.css`・`assets/site.js`。Markdownや翻訳データを変更したら生成物も更新する。main反映後は既存GitHub ActionsがHTMLを更新する。GitHub Pagesの想定公開先は [kurono966.github.io/Serohan](https://kurono966.github.io/Serohan/)。


## Ver.1.1統合

最新版は[統合仕様](grammar-v1.1.md)。採用・試験運用・保留、語形と作用域、旧表現との対応を記載。`python integrate_v11.py`で仕様の助動詞表と33件の自作翻訳を再生成できる。旧版の意味評価は再評価前の記録として保持する。
