<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用実施記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.execute.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
```yaml
- date: 2026-11-22 12:30
  summary: 公開ページ生成スクリプト scripts/build-pages.py と site/index.html を追加
  details:
    変更内容: >-
      README の掲載表から site/index.html を生成する build-pages.py（--check 付き、HTML エスケープ、https のみ許可、
      マーカー・列の検証）を追加し、生成物をコミット対象とした。DESIGN.md に生成方式と出力先を反映した
    変更ファイル:
      - scripts/build-pages.py
      - site/index.html
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python scripts/build-pages.py を2回実行して差分なし、python scripts/build-pages.py --check、不正入力（http リンク・
      マーカー欠落・見出し不一致・javascript スキーム）での停止確認、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 生成は冪等で --check は一致時0・不一致時1、不正入力は終了コード2で停止、各ゲート合格
    関連ID:
      - BL-002
- date: 2026-11-22 12:00
  summary: ポートフォリオの正本 README.md を作成
  details:
    変更内容: >-
      README.md に概要と掲載表（PORTFOLIO マーカーで囲む4件）を作成し、DESIGN.md へ目的・掲載項目・単一正本の方針を記載した
    変更ファイル:
      - README.md
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      npx markdownlint-cli2、python scripts/validate-records.py、python scripts/scan-secrets.py --require-changes
    検証結果: >-
      成功 - 3コマンドとも合格
    関連ID:
      - BL-001
```
<!-- COPILOT_RECORDS:END -->
