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
  依存:
    - BL-010
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
    - BL-010
    - BL-012
  根拠: >-
    見た目の判読性と gh-pages への push は自動検証できず、push はユーザーが実行する決まりのため人手検証とする
- id: BL-010
  区分: 機能追加
  タスク内容: >-
    scripts/propose-releases.py を追加する（ユーザー決定: ポートフォリオの更新依頼時にあわせて最新リリースも更新できるようにする）。
    標準ライブラリのみを使い、subprocess と gh は使わない。GitHub の公開 REST API
    （https://api.github.com/repos/<owner>/<repo>/releases?per_page=<小さい数>）へ urllib で GET する。
    資格情報・トークンは一切使わず、ホストは api.github.com に固定し、タイムアウトと応答サイズの上限を設ける。
    owner/repo は README の掲載表の repo 列 URL（https://github.com/filderschoice/<repo> の形のみ）から検証して導出する。
    下書き（draft）は除外し、先頭の1件（プレリリースを含む）を採る。
    出力は README の RELEASES 表の置き換え案（差分）を標準出力へ出す。--apply を付けたときだけ、README の
    RELEASES マーカー間の表だけを書き換える（一時ファイルへ書いてアトミックに置換し、改行は元のファイルに合わせ、
    他の箇所は変えない）。--from-json <ファイル> で API 応答の保存ファイルを読み、ネットワーク無しで同じ処理を行える。
    build-pages.py とは分離し、ネットワークが無くても build-pages.py の生成と --check は変わらず通る。
    ループ内では実 API を呼ばない（guardrails 12.5）。実 API の実行は、対話モードでユーザーが更新を依頼したときに限る
  優先度: P3
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    --from-json で、差分案の出力・--apply による RELEASES 表だけの書き換え（他の箇所と改行が変わらない）・
    冪等（2回目の --apply で差分なし）を確かめる。不正な入力（掲載表の repo が対象外の URL、不正な JSON、
    版・日付の不正、draft のみ）で終了コード2になることを一時ファイルで確かめる（確認後に一時ファイルを残さない）。
    build-pages.py の生成と --check が変わらず通る。markdownlint・validate-records・scan-secrets が合格
  依存: []
  根拠: >-
    ユーザーが「スクリプトを作る方向で」と決定したため要確認を外した。公開 REST API を認証なしで GET するだけで、
    ユーザーの gh 認証情報は使わない。ループ内の検証は --from-json の保存ファイルだけで行い、実 API は呼ばない
    （12.5）。実 API の実行は対話モードのユーザー依頼時に限り、BL-011 で確認する。
    読み取りの 60 回/時の未認証レートでも掲載数（現在4件）には十分
```
<!-- COPILOT_RECORDS:END -->
