# 公開ポートフォリオ

GitHub アカウント [filderschoice](https://github.com/filderschoice) が公開しているアプリ・ツールの一覧です。
各アプリの詳細（機能・インストール方法・ライセンス等）は、表の repo リンク先の README を参照してください。

## 公開中のアプリ・ツール

<!-- PORTFOLIO:BEGIN -->
| 名前 | 説明 | 種別 | プラットフォーム/言語 | repo | Pages |
| --- | --- | --- | --- | --- | --- |
| sesami-wear | Pixel WatchなどのWear OSスマートウォッチからCANDY HOUSE Sesame 5（+ Hub 3）を施錠・解錠する非公式アプリ。タイルからのワンタップ操作とコンプリケーションでの状態表示に対応。 | アプリ | Kotlin / Wear OS | <https://github.com/filderschoice/sesami-wear> | <https://filderschoice.github.io/sesami-wear/> |
| ikumemo | 話すだけで買い物メモ。買ったらスワイプで記録、カレンダーで振り返り。使い切りたい物は期限をお知らせするAndroidアプリ（アカウント・通信・広告なし）。 | アプリ | Kotlin / Android | <https://github.com/filderschoice/ikumemo> | <https://filderschoice.github.io/ikumemo/> |
| romcha | Romcha（ロムチャ）— YouTube公式アプリと同期する、見るだけのフローティングチャットビューワー（Android）。 | アプリ | Kotlin / Android | <https://github.com/filderschoice/romcha> | <https://filderschoice.github.io/romcha/> |
| windows-devenv-setup | wingetとnpmでWindowsの開発環境を冪等に構築するPowerShellスクリプト。 | ツール | PowerShell / Windows | <https://github.com/filderschoice/windows-devenv-setup> | - |
<!-- PORTFOLIO:END -->

## 運用方針

- 掲載内容の正本はこの README の表（`PORTFOLIO:BEGIN` と `PORTFOLIO:END` の間）です。
- 公開ページ（`site/index.html`）は、この表から `python scripts/build-pages.py` で生成します。
  整合の確認は `python scripts/build-pages.py --check` です。
- Pages が無い項目は、Pages 列を「-」にします。

## 掲載するリポジトリを追加する手順

公開する repo が増えたら、次の手順で追加します。

1. 掲載表（`PORTFOLIO:BEGIN` と `PORTFOLIO:END` の間）へ1行を追加する。列は 名前・説明・種別・プラットフォーム/言語・repo・Pages の順
2. 種別は `アプリ` か `ツール` のどちらかだけを書く
3. プラットフォーム/言語は `Kotlin / Android` のように「言語 / 対象環境」で書く
4. repo と Pages の URL は `<https://...>` の形式で書く。https 以外はエラーになる
5. Pages が無い場合は、Pages 列を `-` にする（公開ページにも Pages リンクを出さない）
6. `python scripts/build-pages.py` で `site/index.html` を再生成し、`python scripts/build-pages.py --check` で一致を確認する
7. 説明など、セルの中に `|` は書けない（列数不正としてエラー終了する）
8. `README.md` と `site/index.html` を、あわせてコミットする

## 公開ページの更新手順

公開は GitHub Actions を使わず、端末から公開用ブランチ `gh-pages` へ push して行います。
`README.md`・`scripts/build-pages.py`・`site/` のいずれかが変わったときだけ実施します。

1. 規定ブランチへ変更をマージした状態で、`python scripts/build-pages.py --check` が成功することを確認する
   （失敗したら `python scripts/build-pages.py` で再生成し、コミットしてからやり直す）
2. `git subtree push --prefix site origin gh-pages` で、`site/` の内容だけを `gh-pages` ブランチの直下へ反映する
   （`site/` に変更が無ければ新しいコミットは作られない）
3. 初回のみ、GitHub の Settings → Pages で公開元を「`gh-pages` ブランチの `/ (root)`」に設定する
