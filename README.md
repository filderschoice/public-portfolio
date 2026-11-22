# 公開ポートフォリオ

GitHub アカウント [filderschoice](https://github.com/filderschoice) が公開しているアプリ・ツールの一覧です。
各アプリの詳細（機能・インストール方法・ライセンス等）は、表の repo リンク先の README を参照してください。

## 公開中のアプリ・ツール

<!-- PORTFOLIO:BEGIN -->
| 名前 | 説明 | 種別 | プラットフォーム/言語 | repo | Pages | イラスト |
| --- | --- | --- | --- | --- | --- | --- |
| sesami-wear | Pixel WatchなどのWear OSスマートウォッチからCANDY HOUSE Sesame 5（+ Hub 3）を施錠・解錠する非公式アプリ。タイルからのワンタップ操作とコンプリケーションでの状態表示に対応。 | アプリ | Kotlin / Wear OS | <https://github.com/filderschoice/sesami-wear> | <https://filderschoice.github.io/sesami-wear/> | sesami-wear |
| ikumemo | 話すだけで買い物メモ。買ったらスワイプで記録、カレンダーで振り返り。使い切りたい物は期限をお知らせするAndroidアプリ（アカウント・通信・広告なし）。 | アプリ | Kotlin / Android | <https://github.com/filderschoice/ikumemo> | <https://filderschoice.github.io/ikumemo/> | ikumemo |
| romcha | Romcha（ロムチャ）— YouTube公式アプリと同期する、見るだけのフローティングチャットビューワー（Android）。 | アプリ | Kotlin / Android | <https://github.com/filderschoice/romcha> | <https://filderschoice.github.io/romcha/> | romcha |
| windows-devenv-setup | wingetとnpmでWindowsの開発環境を冪等に構築するPowerShellスクリプト。 | ツール | PowerShell / Windows | <https://github.com/filderschoice/windows-devenv-setup> | - | windows-devenv-setup |
<!-- PORTFOLIO:END -->

## 最新リリース

各アプリの最新リリースです（種類を問わず最新の1件。プレリリースは種類で区別します）。公開ページのカードへ
`repo` 列の URL に `/releases/tag/<版>` を付けたリンクで表示するため、リリースの URL はここに書きません。
リリースが無い項目は、3列とも `-` にします。

<!-- RELEASES:BEGIN -->
| 名前 | 最新リリース | 公開日 | 種類 |
| --- | --- | --- | --- |
| sesami-wear | v0.17.0 | 2026-11-21 | プレリリース |
| ikumemo | - | - | - |
| romcha | v1.2.0 | 2026-10-15 | 正式 |
| windows-devenv-setup | - | - | - |
<!-- RELEASES:END -->

## 運用方針

- 掲載内容の正本はこの README の表（`PORTFOLIO:BEGIN` と `PORTFOLIO:END` の間）です。
- 公開ページ（`site/index.html`）は、この表から `python scripts/build-pages.py` で生成します。
  整合の確認は `python scripts/build-pages.py --check` です。
- Pages が無い項目は、Pages 列を「-」にします。
- 最新リリース表は、`python scripts/propose-releases.py` で更新します。公開 REST API（認証なし・接続先は
  api.github.com 固定）から各 repo の最新リリース（draft を除く先頭1件）を取得し、RELEASES 表の差分案を表示します。
  差分案を確認し、問題なければ `--apply` を付けて再実行すると RELEASES 表だけが書き換わります。
  その後 `python scripts/build-pages.py` で再生成し、`--check` で一致を確認します。
  `--from-json <ファイル>` で API 応答の保存ファイルを読めば、ネットワークへ接続せずに同じ処理を行えます
  （形式は `{"<repo 名>": <releases API の応答の配列>}`）。リリースが無い repo は空配列で `-` になり、
  応答が不正なとき・掲載表の repo が `https://github.com/filderschoice/<repo>` の形でないときはエラー終了します。
- イラスト列は、各アプリの内容をイメージしやすくする簡易イラストの ID です。実画面ではなく README の説明に基づく
  模式図で、固定の SVG を `site/illustrations/<ID>.svg` に置きます。イラストが無い項目は「-」にします。

## 掲載するリポジトリを追加する手順

公開する repo が増えたら、次の手順で追加します。

1. 掲載表（`PORTFOLIO:BEGIN` と `PORTFOLIO:END` の間）へ1行を追加する。列は 名前・説明・種別・プラットフォーム/言語・repo・Pages・イラスト の順
2. 最新リリース表（`RELEASES:BEGIN` と `RELEASES:END` の間）へも同じ名前の行を1行追加する（リリースが無ければ `-` の3列）。
   名前の過不足・重複はエラーになる
3. 種別は `アプリ` か `ツール` のどちらかだけを書く
4. プラットフォーム/言語は `Kotlin / Android` のように「言語 / 対象環境」で書く
5. repo と Pages の URL は `<https://...>` の形式で書く。https 以外はエラーになる
6. Pages が無い場合は、Pages 列を `-` にする（公開ページにも Pages リンクを出さない）
7. イラストを付ける場合は、手書きの SVG を `site/illustrations/<ID>.svg` に置き、イラスト列へ ID（英数字とハイフンのみ）を書く。
   付けない場合は `-` にする。SVG には script・foreignObject・`on` で始まる属性・href・`url(`・`@import`・外部 URL を
   書けない（SVG を単体で表示するのに必須の `xmlns="http://www.w3.org/2000/svg"` だけは例外）。
   存在しない ID・不正な ID・禁止された記述はエラーになる。描くのは説明に出てくる要素だけにし、
   「実際の画面ではありません」の注記を SVG の title に入れ、ダークモードでも読める配色にする
8. `python scripts/build-pages.py` で `site/index.html` を再生成し、`python scripts/build-pages.py --check` で一致を確認する
9. 説明など、セルの中に `|` は書けない（列数不正としてエラー終了する）
10. `README.md`・`site/index.html`・追加した SVG を、あわせてコミットする

## 公開ページの更新手順

公開は GitHub Actions を使わず、端末から公開用ブランチ `gh-pages` へ push して行います。
`README.md`・`scripts/build-pages.py`・`site/` のいずれかが変わったときだけ実施します。

1. 規定ブランチへ変更をマージした状態で、`python scripts/build-pages.py --check` が成功することを確認する
   （失敗したら `python scripts/build-pages.py` で再生成し、コミットしてからやり直す）
2. `git subtree push --prefix site origin gh-pages` で、`site/` の内容だけを `gh-pages` ブランチの直下へ反映する
   （`site/` に変更が無ければ新しいコミットは作られない）
3. 初回のみ、GitHub の Settings → Pages で公開元を「`gh-pages` ブランチの `/ (root)`」に設定する
