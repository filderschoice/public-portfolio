<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用未対応事項記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.backlog.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
```yaml
- id: BL-012
  区分: 機能追加
  タスク内容: >-
    プロジェクト用 Skill .claude/skills/portfolio-update/SKILL.md を作る。ユーザーが「ポートフォリオを更新して」と
    依頼したときの手順を書く: 掲載表の追加・修正、propose-releases.py で差分案を出す→内容を確認→--apply、
    build-pages.py の再生成と --check、品質ゲート、コミット案の提示。実 API の実行は対話モードのみで、
    自律ループ内では --from-json だけを使うこと、push はユーザーが行うことを明記する。
    書式は既存スキルに倣い、frontmatter は name と description のみとし、model は指定しない
  優先度: P3
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    SKILL.md が既存スキルと同じ書式で、上記の手順と制約を含む。markdownlint・validate-records・scan-secrets が合格。
    「守る側」に近い変更のため、実装担当とは別の担当（diff-reviewer）で点検する
  依存: []
  根拠: >-
    更新の依頼ごとに手順を思い出す手間と、実 API をループ内で呼んでしまう事故を避けるため、手順を Skill に固定する。
    スキルは手順の記述のみで、権限や設定は変えない
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
    propose-releases.py の実 API 実行（--from-json ではない）を行い、差分案が実際の最新リリースと一致することを確認する
  依存:
    - BL-012
  根拠: >-
    見た目の判読性と gh-pages への push は自動検証できず、push はユーザーが実行する決まりのため人手検証とする
```
<!-- COPILOT_RECORDS:END -->
