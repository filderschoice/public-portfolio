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
  依存:
    - BL-005
  根拠: >-
    Pages の設定変更・push・デプロイは外部への公開を伴い、guardrails 12.2 でエージェントに禁止されているため
    人手検証として完了判定から除外する
    注記として、Pages の公開元は / か /docs のみと見られる（リポジトリ内では未確認）ため、site/ を公開するには
    BL-005 のワークフロー方式の確定が前提となる
- id: BL-005
  区分: 機能追加
  タスク内容: >-
    README.md の更新に合わせて公開ページを生成・デプロイする GitHub Actions ワークフロー（.github/workflows/ 配下）を追加する。
    方式（Actions で生成してデプロイ／コミット済みの site/ をそのままデプロイ）、トリガー（規定ブランチへの push で
    README.md・scripts/build-pages.py が変わったとき）、本 repo を public にしてよいか（rules/ や CLAUDE.md 等の
    テンプレ一式も公開される）をユーザーが判断する。あわせて .github/CODEOWNERS が実在しない組織のプレースホルダ
    （@your-org/ai-platform 等）のままで、repo を public にする場合に公開されるため、削除するか、
    プレースホルダだと分かる状態にするかもユーザーが決める
  優先度: P2
  状態: 要確認
  担当: ユーザー
  完了条件: >-
    ユーザーが方式・トリガー・公開範囲を決定し、承認されたワークフローが追加されて
    actions/upload-pages-artifact と actions/deploy-pages で site/ が公開される
  依存: []
  根拠: >-
    CI/CD 定義の変更は guardrails 12.2 で自律ループでは禁止のため、ループ内で実施せず要確認とする。
    repo の公開範囲は外部影響を伴う判断のため併せて人の判断を求める
```
<!-- COPILOT_RECORDS:END -->
