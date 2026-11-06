# Ver.0.9 検証結果と変更一覧

2026-11-06。ブランチ `grammar/v0.9-consistency`。開始点 `bdb04e4`。Python 3.10.6、Windowsで検証。

## 結果

- `python -m unittest discover -s tests -v`：18テスト成功。
- 使用80語根・未使用24枠を基準集合と照合。80語根すべての採用終声形を受理し、24未使用枠すべての派生を拒否。
- 후右結合、複数属性、動詞・属性否定、否定過去、二重否定、퍄の語彙用法、각の項構造、未採用構文の扱いを確認。
- `나 멕 티`の2解析を保持し、疑問符でも一方を隠さない。
- 自作翻訳60件：保持30、部分8、不能22。訳を付けた38件は部分文法で解析可能。うち1例は構文上曖昧。複数文を含むため解析する文の個数は訳の件数より多い。
- `python translation_data.py`、`python verify.py`、`python audit_lexicon.py`：生成成功。外部取得は0件、理由は監査記録を参照。
- `python build.py`：12章を生成。READMEの章順・全章の入力ファイル・HTML内部リンクを自動確認。
- 旧説明資料6ファイルの保存内容を開始点のGit内容と照合。一致（改行コードの差は除外）。旧0.6～0.8・旧辞書・移行表の本文ハッシュもテスト。
- `git diff --check`：空白エラーなし。

部分解析器は意味や照応先を検証しない。音声実験、外部話者評価、外部日本語コーパスによる再検証は未実施。全称否定や焦点否定を実現したとは主張しない。

## 変更ファイル

| 種類 | ファイル |
| --- | --- |
| 現行案内・仕様 | README.md、overview.md、grammar.md、grammar-v0.9.md、particles.md、verb-inflection.md、examples.md |
| 辞書の表修正 | dictionary.md（語根・語義・使用状態に変更なし） |
| 分析・検証記録 | audit-v0.9.md、validation-results.md、audit-lexemes.json |
| 翻訳データ・報告 | translation_data.py、translation-cases.json、verify.py、translation-report.md |
| 部分パーサー・監査 | check_grammar.py、audit_lexicon.py、lexicon-baseline.json、history-manifest.json |
| 自動テスト・CI | tests/test_grammar.py、tests/test_build.py、.github/workflows/verify.yml |
| Web生成 | build.py、index.html |
| 改訂前本文の原文保存 | history/README-pre-v0.9.md、history/overview-pre-v0.9.md、history/grammar-pre-v0.9.md、history/particles-pre-v0.9.md、history/verb-inflection-pre-v0.9.md、history/examples-pre-v0.9.md |

辞書と0.6～0.8の語義・採用履歴を勝手に置き換えず、Ver.0.9の差分で現在の適用範囲を明示する。PRはmain向けに作成し、mainへ直接反映しない。
