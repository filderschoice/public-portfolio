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
    - BL-003
    - BL-004
    - BL-005
  根拠: >-
    Pages の設定変更・push・デプロイは外部への公開を伴い、guardrails 12.2 でエージェントに禁止されているため
    人手検証として完了判定から除外する
- id: BL-005
  区分: 機能追加
  タスク内容: >-
    README.md の更新に合わせて公開ページを生成・デプロイする GitHub Actions ワークフロー（.github/workflows/ 配下）を追加する。
    方式（Actions で生成してデプロイ／コミット済みの site/ をそのままデプロイ）、トリガー（規定ブランチへの push で
    README.md・scripts/build-pages.py が変わったとき）、本 repo を public にしてよいか（rules/ や CLAUDE.md 等の
    テンプレ一式も公開される）をユーザーが判断する
  優先度: P2
  状態: 要確認
  担当: ユーザー
  完了条件: >-
    ユーザーが方式・トリガー・公開範囲を決定し、承認されたワークフローが追加されて
    actions/upload-pages-artifact と actions/deploy-pages で site/ が公開される
  依存:
    - BL-002
  根拠: >-
    CI/CD 定義の変更は guardrails 12.2 で自律ループでは禁止のため、ループ内で実施せず要確認とする。
    repo の公開範囲は外部影響を伴う判断のため併せて人の判断を求める
- id: BL-004
  区分: 機能追加
  タスク内容: >-
    README.md に「掲載するリポジトリを追加する手順」を追記する（掲載表への1行追加、種別・プラットフォームの書き方、
    Pages が無い場合の書き方、python scripts/build-pages.py での再生成と --check での整合確認、コミット対象）
  優先度: P2
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    手順どおりに架空の1行を追加すると生成と --check が成功することを確かめ（確認後に行は戻す）、
    markdownlint・validate-records・scan-secrets が合格する
  依存:
    - BL-002
- id: BL-003
  区分: UX改善
  タスク内容: >-
    生成する site/index.html の見た目をカード表示・レスポンシブ（スマートフォン幅で1列）・ダークモード
    （prefers-color-scheme）に対応させる。CSS は生成スクリプト内にインラインで持ち、外部 CSS・フォント・JS を読み込まない
  優先度: P2
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    再生成した site/index.html がカード表示・メディアクエリ・ダークモードの指定を含み、外部リソースを参照しない。
    種別（アプリ/ツール）がカード上で判別でき、Pages が無い項目はリンクを出さない。--check が成功し、
    scan-secrets が合格する
  依存:
    - BL-002
- id: BL-002
  区分: 機能追加
  タスク内容: >-
    README.md の掲載表を読み、公開用の静的ページ site/index.html を生成する scripts/build-pages.py を作成する
    （Python 標準ライブラリのみ）。生成物と README の不一致を検出する --check オプションを持たせ、生成物もコミットする
  優先度: P1
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    生成が冪等（2回実行して差分なし）で、--check は一致時に終了コード0・不一致時に1を返す。表の値は HTML
    エスケープし、リンクは https の URL だけを許可する（それ以外はエラーで停止）。掲載表のマーカーや必須列が
    欠けていればエラーで停止する。DESIGN.md に生成方式と出力先を反映し、validate-records・scan-secrets が合格する
  依存: []
  根拠: >-
    出力先は既定値として site/ を選んだ。docs/ は既存のガードレール文書の置き場で、Pages の公開元にすると
    それらまで公開されるため避ける。生成物をコミットするのは、CI を使えないループ内で --check による整合確認を
    可能にするためで、ワークフロー導入後もそのまま公開元に使える
```
<!-- COPILOT_RECORDS:END -->
