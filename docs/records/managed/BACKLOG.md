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
- id: BL-011
  区分: 人手検証
  タスク内容: >-
    イラストと最新リリースを加えた公開ページを実ブラウザで確認し、gh-pages へ反映する。
    ライト/ダーク両方の配色、幅 40rem 以下（スマホ）と以上の表示、SVG の読みやすさ、
    「実際の画面ではありません」の注記が見えること、リリースリンクの遷移先を確かめる。
    反映は README「公開ページの更新手順」の git subtree push --prefix site origin gh-pages をユーザーが実行し、
    公開URLで site/illustrations/ 配下の SVG が配信される（HTTP 200）ことを確かめる
  優先度: P2
  状態: 未着手
  担当: ユーザー
  完了条件: >-
    ローカルの site/index.html と公開ページの両方で、4件のカードのイラスト・注記・リリース表示が
    ライト/ダーク・狭幅/広幅で判読でき、SVG とリリースリンクが正しく開く。あわせて、対話モードで
    propose-releases.py の実 API 実行（--live を明示する。--from-json ではない）を行い、差分案が実際の最新リリースと一致することを確認する
  依存: []
  根拠: >-
    見た目の判読性と gh-pages への push は自動検証できず、push はユーザーが実行する決まりのため人手検証とする
```
<!-- COPILOT_RECORDS:END -->
