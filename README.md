# セロハン語（Serohan）

ハングル一音節の語根に終声を付け、概念・行為・属性・修飾・実体を切り替える人工言語。セロ語の姉妹言語として、規則性と小さな文法を目指す。

## ウェブ版の開き方

[index.html](index.html) をブラウザーで開くと、全7章をウェブサイト形式で閲覧できる。サーバーやインターネット接続は不要。語根辞書はハングル・ラテン転写・日本語で検索できる。JavaScriptが無効でも本文は読める。

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

나 록 아 호 에 헤
私は山から海へ行く。
```

## 読む順番

1. [設計概要](overview.md)：理念・文字・語形成。
2. [基本文法](grammar.md)：語順・修飾・句のまとまり・読み方。
3. [Ver.0.6 文法拡張仕様](grammar-v0.6.md)：全語根の属性化、後置助詞후の関連関係、文末티疑問。
4. [語根辞書](dictionary.md)：104語根と意味領域。
5. [助詞](particles.md)：採用済み5語と予約語。
6. [動詞活用案](verb-inflection.md)：複合終声の割り当て。
7. [例文集](examples.md)：文法の使用例。

## 現在の範囲

2026-11-06 整理版。基本語順はSVO。語根は8母音系列、助詞はㅎ系列を用いる。複合終声による動詞活用は試案として掲載する。

Ver.0.6ではYes/No疑問文のみ追加。疑問詞・命令、数と数量、関係節、従属節、活用の重ね合わせは未定。日本語訳だけを根拠に未定の文法や韓国語の語彙を補わない。

## 今回の整理

- 概要と辞書の母音範囲を統一し、予約母音を区別。
- 他者を表す네と、世帯바／建物제の使い分けを統一。
- 願望・完了・継続のハングル表記を修正。
- 身体部位による手段に히を付け、感情の修飾にㅂを使用。
- 未定の関係節を前提とした断片を、完結したSVO文に変更。

## Ver.0.6 文法拡張（2026-11-06）

[grammar-v0.6.md](grammar-v0.6.md) に暫定採用した3規則を記録：全104語根の属性形（ㄹ）による自由な複数修飾、`후` の所有・所属を含む一般的関連関係、文末 `티?` によるYes/No疑問文。否定の汎用マーカー・存在文・等値文・疑問詞などは未採用の検討事項と区別する。

**注意**：`index.html` は `build.py` で生成する別ファイルです。Markdown変更時はGitHub Actions（`.github/workflows/build-docs.yml`）が `python build.py` を実行し、変更がある場合に `index.html` を自動コミットします。手動でも `python build.py` で再生成できます。

## GitHub Pagesで公開する

想定URL： https://kurono966.github.io/Serohan/ 

初回のみGitHubの **Settings → Pages → Build and deployment** で、**Source: Deploy from a branch**、**Branch: main / (root)** を選択して保存する。公開が有効になると上記URLからWeb版を開ける。

Markdownの更新時は `.github/workflows/build-docs.yml` が `index.html` を再生成し、コミットするため、公開ページにも変更が反映される。サイトはリポジトリ直下の `index.html` と `assets/` で構成され、`.nojekyll` によりJekyll変換を無効化している。

