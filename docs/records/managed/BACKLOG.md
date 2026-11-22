<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用未対応事項記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.backlog.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
```yaml
- id: BL-013
  区分: 品質ゲート
  タスク内容: >-
    CLAUDE.md「本リポジトリの品質ゲート定義」の単体テストの行（現在は replace-me）を
    python -m unittest discover -s tests にするか、ユーザーが判断する。tests/ には scripts/ 配下の検証コードの
    unittest（標準ライブラリのみ、ネットワーク接続なし、一時ディレクトリのみ書き込み）を追加済み。
    採用する場合は CLAUDE.md の表を更新する（CLAUDE.md は自律ループでは変更しないため、ユーザーの承認を得て行う）
  優先度: P3
  状態: 要確認
  担当: ユーザー
  完了条件: >-
    単体テストの行を python -m unittest discover -s tests にする、または replace-me のままにする、のどちらかを
    ユーザーが決め、採用する場合は CLAUDE.md の表と、ゲートの合否基準（全件成功）が更新されている
  依存: []
  根拠: >-
    品質ゲート定義は全エージェント共通の正本で、自律ループ内で変更してはならないため、起票して保留する。
    既存の他のゲートの行（replace-me の例）の扱いも含めて人が決める
```
<!-- COPILOT_RECORDS:END -->
