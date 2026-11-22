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
