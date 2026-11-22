<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用未対応事項記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.backlog.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
```yaml
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
