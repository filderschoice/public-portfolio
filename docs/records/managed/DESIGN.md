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
- イラスト: 各項目の簡易イラストを `site/illustrations/<ID>.svg` の固定資産（手書き SVG、viewBox 400x300）として持つ。
  README の説明に出てくる要素だけを描いた模式図で、実画面ではない旨を SVG の title と図中、カードの注記に出す

## 実装済み機能要件

- FR-001: README.md の冒頭に概要を置き、`PORTFOLIO:BEGIN` と `PORTFOLIO:END` のマーカーで囲んだ Markdown 表に掲載項目を並べる
- FR-002: 表の列は 名前・説明・種別（アプリ/ツール）・プラットフォーム/言語・repo・Pages（無ければ「-」）・イラスト
  （SVG の ID。無ければ「-」。ID は `^[A-Za-z0-9-]+$` で、`site/illustrations/<ID>.svg` が実在すること）
- FR-003: `python scripts/build-pages.py`（標準ライブラリのみ）が表を読み、単一ファイルの `site/index.html` を生成する。
  生成物もコミットする（CI を使えない環境でも `--check` で整合を確認でき、ワークフロー導入後は公開元にそのまま使える）
- FR-004: `--check` は生成物が README と一致すれば終了コード0、不一致なら1。生成は冪等（2回実行して差分なし）。
  比較はバイト単位のため、`.gitattributes` で `site/index.html` を LF に固定する（`core.autocrlf=true` の Windows で
  CRLF に変換され、`--check` が誤って不一致になるのを防ぐ。他のファイルの改行方針は変えない）
- FR-005: 次の場合はエラー終了（終了コード2）する。マーカーが1組でない、見出しが FR-002 の列と一致しない、データ行が無い、
  行が `|` で始まり終わらない、列数が7でない、名前・説明・プラットフォームが空、種別が アプリ/ツール 以外、
  repo・Pages（`-` を除く）が https の URL でない、イラストの ID が正規表現に合わない・SVG が実在しない・
  SVG に script・foreignObject・`on` で始まる属性・href/xlink:href・`url(`・`@import`・http が含まれる
  （検査の前に、単体表示に必須の名前空間宣言 `xmlns="http://www.w3.org/2000/svg"` だけを取り除く）。説明などのセルに `|` は使えない（列数不正になる）。
  検査しないもの: 名前の重複、URL 内の空白・制御文字、repo が `https://github.com/filderschoice/` 配下かどうか

## 設計方針

- 単一正本: 掲載データは README.md の表だけが持つ。別データファイルは作らず、他の成果物はすべてここから導出する。URL は `<https://...>` 形式で書く（MD034 対策）
- repo 列は `https://github.com/filderschoice/` 配下の実 repo 名を指す
- 説明文は各 repo の description を元にする

## 非機能要件

- セキュリティ: 資格情報を含めない。リンクは https のみ。表の値は `html.escape` で必ずエスケープして出力する。
  イラストは `<img src="illustrations/<ID>.svg">` で読み込み（index.html へ埋め込まない。img として読まれた SVG は
  スクリプトが動かず外部資源も読まれない）、生成スクリプトは SVG の中身を組み立てず固定資産を参照するだけにする。
  src は Pages が `/public-portfolio/` 配下のため相対パス。`head` に CSP の meta を置く:
  `default-src 'none'; img-src 'self'; style-src 'unsafe-inline'`（外部資源を読まない既存方針の機械的な担保。
  style は `<style>` へのインライン埋め込みのため `unsafe-inline` のみ許可し、script・フォント・外部画像は許可しない）
- UI/UX: 掲載項目をカード（`.card`）で表示する。幅 40rem 以下で1列、それ以上で2列。`prefers-color-scheme: dark` で配色を切り替える。
  種別はバッジ（アプリ/ツール）の文字と色で判別でき、Pages が無い項目は Pages リンクを出さない。
  CSS は生成スクリプト内の定数 `CSS` に持ち、`<style>` へインラインで埋め込む。
  イラストはカード上部の枠（`.illust`。配色は `--ill-bg` でライト/ダークを切り替え、幅いっぱいに縮小）に出し、
  img に width・height（400x300）と alt（「<名前> の画面イメージ（簡易イラスト。実際の画面ではありません）」）を指定する。
  カードに「イメージ図。実際の画面ではありません」、ページの lead に同趣旨の一文を出す。SVG は style 内の
  `prefers-color-scheme` でダークに対応する
- 公開ページは外部 CSS・フォント・JS を読み込まない。出力先は `site/`（`docs/` はガードレール文書の置き場のため公開元にしない）

## 実装制約

- 文書は日本語で記述する
- 記録ファイルは `docs/records/spec/FORMAT.md` に従う

## エージェント実装指示

- 掲載項目を増やすときは README の表へ1行追加し（イラストを付けるなら SVG も `site/illustrations/` へ置く）、品質ゲートを通す
- 要件 FR-001・FR-002 を変更する場合は本書を更新する
<!-- COPILOT_RECORDS:END -->
