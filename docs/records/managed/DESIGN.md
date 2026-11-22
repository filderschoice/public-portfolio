<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用設計記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.design.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
# 実装用プロンプト設計書

## 目的

- filderschoice が GitHub で公開しているアプリ・ツールを一元管理し、何を公開しているかをすぐ見られる
  ポートフォリオを再実装するための設計書。詳細は各 repo の README を参照させ、ここでは一覧だけを持つ。

## 対象システム概要

- 対象: README.md（正本）と、そこから生成する公開ページ
- 掲載項目: sesami-wear・ikumemo・romcha（アプリ）、windows-devenv-setup（ツール）の4件。公開物が増えたら表へ1行追加する

## 実装済み機能要件

- FR-001: README.md の冒頭に概要を置き、`PORTFOLIO:BEGIN` と `PORTFOLIO:END` のマーカーで囲んだ Markdown 表に掲載項目を並べる
- FR-002: 表の列は 名前・説明・種別（アプリ/ツール）・プラットフォーム/言語・repo・Pages（無ければ「-」）
- FR-003: `python scripts/build-pages.py`（標準ライブラリのみ）が表を読み、単一ファイルの `site/index.html` を生成する。
  生成物もコミットする（CI を使えない環境でも `--check` で整合を確認でき、ワークフロー導入後は公開元にそのまま使える）
- FR-004: `--check` は生成物が README と一致すれば終了コード0、不一致なら1。生成は冪等（2回実行して差分なし）。
  比較はバイト単位のため、`.gitattributes` で `site/index.html` を LF に固定する（`core.autocrlf=true` の Windows で
  CRLF に変換され、`--check` が誤って不一致になるのを防ぐ。他のファイルの改行方針は変えない）
- FR-005: 次の場合はエラー終了（終了コード2）する。マーカーが1組でない、見出しが FR-002 の列と一致しない、データ行が無い、
  行が `|` で始まり終わらない、列数が6でない、名前・説明・プラットフォームが空、種別が アプリ/ツール 以外、
  repo・Pages（`-` を除く）が https の URL でない。説明などのセルに `|` は使えない（列数不正になる）。
  検査しないもの: 名前の重複、URL 内の空白・制御文字、repo が `https://github.com/filderschoice/` 配下かどうか

## 設計方針

- 単一正本: 掲載データは README.md の表だけが持つ。別データファイルは作らず、他の成果物はすべてここから導出する。URL は `<https://...>` 形式で書く（MD034 対策）
- repo 列は `https://github.com/filderschoice/` 配下の実 repo 名を指す
- 説明文は各 repo の description を元にする

## 非機能要件

- セキュリティ: 資格情報を含めない。リンクは https のみ。表の値は `html.escape` で必ずエスケープして出力する
- UI/UX: 掲載項目をカード（`.card`）で表示する。幅 40rem 以下で1列、それ以上で2列。`prefers-color-scheme: dark` で配色を切り替える。
  種別はバッジ（アプリ/ツール）の文字と色で判別でき、Pages が無い項目は Pages リンクを出さない。
  CSS は生成スクリプト内の定数 `CSS` に持ち、`<style>` へインラインで埋め込む
- 公開ページは外部 CSS・フォント・JS を読み込まない。出力先は `site/`（`docs/` はガードレール文書の置き場のため公開元にしない）

## 実装制約

- 文書は日本語で記述する
- 記録ファイルは `docs/records/spec/FORMAT.md` に従う

## エージェント実装指示

- 掲載項目を増やすときは README の表へ1行追加し、品質ゲートを通す
- 要件 FR-001・FR-002 を変更する場合は本書を更新する
<!-- COPILOT_RECORDS:END -->
