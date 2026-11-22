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

## 設計方針

- 単一正本: 掲載データは README.md の表だけが持つ。URL は `<https://...>` 形式で書く（MD034 対策）（別データファイルを作らない）。他の成果物はすべてここから導出する
- repo 列は `https://github.com/filderschoice/` 配下の実 repo 名を指す
- 説明文は各 repo の description を元にする

## 非機能要件

- セキュリティ: 資格情報を含めない。リンクは https のみ

## 実装制約

- 文書は日本語で記述する
- 記録ファイルは `docs/records/spec/FORMAT.md` に従う

## エージェント実装指示

- 掲載項目を増やすときは README の表へ1行追加し、品質ゲートを通す
- 要件 FR-001・FR-002 を変更する場合は本書を更新する
<!-- COPILOT_RECORDS:END -->
