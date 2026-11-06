# セロハン語（Serohan）

ハングル一音節の語根に終声を付け、概念・行為・属性・修飾・実体を切り替える人工言語。セロ語の姉妹言語として、規則性と小さな文法を目指す。

## ウェブ版の開き方

[index.html](index.html) をブラウザーで開くと、全9章をウェブサイト形式で閲覧できる。サーバーやインターネット接続は不要。語根辞書はハングル・ラテン転写・日本語で検索できる。JavaScriptが無効でも本文は読める。

資料を編集するときはMarkdownを更新し、このフォルダーで `python build.py` を実行してHTMLを再生成する。Python 3の標準ライブラリのみ使用し、追加パッケージは不要。

| ファイル | 内容 |
| --- | --- |
| `index.html` | ブラウザーで読むウェブ版 |
| `assets/style.css` | 画面・スマートフォン・印刷用のスタイル |
| `assets/site.js` | 辞書検索と章リンクの選択表示 |
| `build.py` | MarkdownからHTMLを再生成するスクリプト |

ファイル名は `abstract.md` → `overview.md`、`joshi.md` → `particles.md`、`doublepacchim.md` → `verb-inflection.md` に変更し、資料内の参照も更新した。

```text
메       愛という概念
멕       愛する
멜       愛情深い
멥       愛をもって
멤       愛の具体的な現れ

나 멕 네
私はあなたを愛する。

나 록 아 호 칼 이 헤
私は山から大きな水域へ行く。
```

## 読む順番

1. [設計概要](overview.md)：理念・文字・語形成。
2. [基本文法](grammar.md)：語順・修飾・句のまとまり・読み方。
3. [Ver.0.6 文法拡張仕様](grammar-v0.6.md)：属性化、後置助詞후の関連関係、文末티疑問。
4. [Ver.0.7 複合修飾仕様](grammar-v0.7-compounds.md)：複数修飾と、후による階層名詞句・角括弧のスコープ。
5. [語根辞書](dictionary.md)：Ver.0.7の使用80語根・未使用24枠。
6. [語根移行表](lexicon-v0.7-migration.md)：廃止した24語根の代替表現と課題。
7. [助詞](particles.md)：採用済み5語と予約語。
8. [動詞活用案](verb-inflection.md)：複合終声の割り当て。
9. [例文集](examples.md)：旧版の語根を含む参考資料。

## 現在の辞書（Ver.0.7 圧縮案）

104枠のうち使用80語根・未使用24枠。`dictionary.md` が現在の語彙案、`dictionary-v0.3.md` は旧104語根の保存版、`lexicon-v0.7-migration.md` は未使用枠と代替表現の対応表です。海 `에`・川 `유` は未使用となり、液体 `이` を修飾して説明します。母音の意味体系は検証中です。`examples.md` には旧辞書の語根を用いる過去の例文が含まれ、現在語彙の模範例文ではありません。

## 現在の範囲

2026-11-06 整理版。基本語順はSVO。語根は8母音系列、助詞はㅎ系列を用いる。複合終声による動詞活用は試案として掲載する。

Ver.0.6ではYes/No疑問文のみ追加。疑問詞・命令、数と数量、関係節、従属節、活用の重ね合わせは未定。日本語訳だけを根拠に未定の文法や韓国語の語彙を補わない。

## 今回の整理

- 概要と辞書の母音範囲を統一し、予約母音を区別。
- 他者を表す네と、世帯바／建物제の使い分けを統一。
- 願望・完了・継続のハングル表記を修正。
- 身体部位による手段に히を付け、感情の修飾にㅂを使用。
- 未定の関係節を前提とした断片を、完結したSVO文に変更。

## Ver.0.7 複合修飾（2026-11-06）

[grammar-v0.7-compounds.md](grammar-v0.7-compounds.md) に、修飾された名詞句の `후` の左側への配置と、角括弧 `[ ]` による入れ子を試験採用した規則を掲載。複数のㄹ属性形は引き続き同一中心語への並列修飾とする。音声での括弧の表現は未定。

## Ver.0.6 文法拡張（2026-11-06）

[grammar-v0.6.md](grammar-v0.6.md) に暫定採用した3規則を記録：全使用語根の属性形（ㄹ）による自由な複数修飾、`후` の所有・所属を含む一般的関連関係、文末 `티?` によるYes/No疑問文。否定の汎用マーカー・存在文・等値文・疑問詞などは未採用の検討事項と区別する。

**注意**：`index.html` は `build.py` で生成する別ファイルです。Markdown変更時はGitHub Actions（`.github/workflows/build-docs.yml`）が `python build.py` を実行し、変更がある場合に `index.html` を自動コミットします。手動でも `python build.py` で再生成できます。

## GitHub Pagesで公開する

想定URL： https://kurono966.github.io/Serohan/ 

初回のみGitHubの **Settings → Pages → Build and deployment** で、**Source: Deploy from a branch**、**Branch: main / (root)** を選択して保存する。公開が有効になると上記URLからWeb版を開ける。

Markdownの更新時は `.github/workflows/build-docs.yml` が `index.html` を再生成し、コミットするため、公開ページにも変更が反映される。サイトはリポジトリ直下の `index.html` と `assets/` で構成され、`.nojekyll` によりJekyll変換を無効化している。

