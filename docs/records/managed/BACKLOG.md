<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用未対応事項記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.backlog.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
```yaml
- id: BL-006
  区分: 人手検証
  タスク内容: >-
    GitHub Pages の有効化（Settings の Pages で公開元を設定）、作業ブランチの push と規定ブランチへのマージ、
    初回デプロイを行い、公開ページを実ブラウザで確認する
  優先度: P2
  状態: 未着手
  担当: ユーザー
  完了条件: >-
    公開URLで4件のカードが表示され、各 repo リンクと Pages リンク（sesami-wear・ikumemo・romcha）が開ける。
    windows-devenv-setup は Pages リンクが表示されない。スマートフォン幅とダークモードで表示が崩れない
  依存: []
  根拠: >-
    Pages の設定変更・push・デプロイは外部への公開を伴い、guardrails 12.2 でエージェントに禁止されているため
    人手検証として完了判定から除外する。デプロイ方式はユーザーの決定により、Actions を使わず
    README の「公開ページの更新手順」（git subtree push で gh-pages ブランチへ反映）に従う。
    公開先ブランチを gh-pages としたのは担当の既定値で、ユーザーが別のブランチを指定する場合は README を直す
```
<!-- COPILOT_RECORDS:END -->
