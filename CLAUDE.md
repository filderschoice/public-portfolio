# CLAUDE.md

Claude Code 固有の差分と追加規約です。全エージェント共通規約の正本（`.github/copilot-instructions.md`）と
ガードレールは下記の `@import` で同時に読み込まれます。共通規約と矛盾する場合は本ファイルを優先します。
その他の参照先と読むタイミングは、共通規約「参照するドキュメント」を参照してください。

@rules/guardrails-unified.v1.md
@.github/copilot-instructions.md

## 共通規約に対する Claude Code 固有の差分（MUST）

| 項目 | Claude Code での差分 |
| --- | --- |
| git操作 | 自律ループ実行モード中の作業ブランチへの `git add` / `git commit` のみ実行してよい。`git push` はモードを問わず常にユーザーが実行する |
| PR説明文・コードレビュー・PR作成 | `.github/instructions/pr.instructions.md` を自動適用する機構が無いため、Skill `pr-create` の手順で同ファイルを**明示的に読んでから**従う |

## 本リポジトリの品質ゲート定義（MUST）

全エージェント共通で使用する正本です。`区分: 人手検証` のBACKLOGタスクは合否判定から除外します。

<!-- 導入時の記入方法（本ファイルは常時読み込まれるため、導入完了後はこのコメントごと削除してよい）:
- 本リポジトリの技術スタックへ合わせて下表を書き換える。表のプレースホルダを残さないこと、括弧内の例を削除する
  ことが導入の完了条件（`docs/guidelines/ADOPTION.md`「2. クイックスタート」）。
- 該当するゲートが無い場合も行は削除せず、コマンド欄へ `(対象外)`、合否基準欄へ理由を書く。
  「実行コードを持たないため」のように現状の事実として書き、未確認のまま空欄にしない。
- ローカル実行手順が未定義のゲートは「未定義（未確認）」と明記する。推測でコマンドを書かない。
- 全ゲートの実行に時間がかかる場合は、表へ「段階」列を足してよい（任意）。例 `毎回`（全イテレーション）・`コード`
  （ソースやビルド設定を変えたイテレーションで追加）・`最後`（自律ループの最後と PR 作成前）。表の直後に各段階の
  対象を書く。段階を定めても、ループの最後と PR 作成前は最後のコミットの状態で全ゲートを実行する
  （Skill `autonomous-loop`・`pr-create`）。段階を定めなければ毎回すべて実行する。
-->

| ゲート | コマンド | 合否基準 |
| --- | --- | --- |
| フォーマット/静的解析 | `replace-me`（例 `npm run lint` / `cargo fmt --check && cargo clippy` / `./gradlew ktlintCheck`） | 終了コード0、指摘0件 |
| 型検査 | `replace-me`（例 `npx tsc --noEmit` / `./gradlew compileKotlin`） | 終了コード0 |
| 単体テスト | `replace-me`（例 `npm test` / `cargo test` / `./gradlew test`） | 全件成功 |
| 脆弱性チェック | `replace-me`（例 `npm audit` / `cargo audit`） | 新規の高危険度の指摘が0件 |
| Markdown の静的解析 | `npx markdownlint-cli2 "**/*.md" --config .markdownlint-cli2.yaml` | `Summary: 0 issues`、かつ出力の `Linting: N files` が `git ls-files --cached --others --exclude-standard "*.md"` の件数と一致（対象漏れの検出） |
| 記録ファイルの検証 | `python scripts/validate-records.py`（PyYAMLが必要） | 終了コード0 |
| 秘密情報スキャン | ステージ済みの変更がある場面（コミット前）は `git add` の後に `python scripts/scan-secrets.py --require-changes`、ステージしない場面（対話実行・Copilot など）は `python scripts/scan-secrets.py --include-unstaged`、PR作成前・ループの最後は `python scripts/scan-secrets.py --range <規定ブランチ>...HEAD --require-changes`（標準ライブラリのみ。未コミットの変更とコミット範囲の両方を確かめるときは2回に分けて実行する。ファイルの削除だけをコミットする場面は検査対象が空になるため `--require-changes` を外す） | 終了コード0（検出時は値を出さずにファイル・行・規則名を表示し1。`--require-changes` 付きで検査対象が空のとき、git の実行に失敗したときは2） |

## 記録ファイルの権限設定（MUST）

`docs/records/managed/` 配下の3ファイルは `.claude/settings.json` の `permissions.allow` により権限プロンプトなしで
編集できます（妥当性はコミット前の差分確認と `FORMAT.md` 準拠で担保する）。それ以外の編集は確認を挟みます。
3ファイルを編集すると、`.claude/settings.json` の `hooks` に登録した PostToolUse フック
（`.claude/hooks/validate-records-after-edit.py`）が `scripts/validate-records.py` を実行します。検証に失敗したと
伝えられたら、一連の編集を終えた時点で `FORMAT.md` に沿って直します（フックは編集を取り消しません）。

<!-- 配布バンドルの .claude/settings.json は記録ファイル関連の許可のみを含む。本リポジトリ固有の許可を追加する
場合は、確認を挟まずに編集させてよい範囲かを判断してから permissions.allow へ追記する。 -->

## 自律ループ実行モード（Loop Engineering）

人の応答を待たずに複数イテレーションを連続実行する、Claude Code 固有の運用モードです（Copilot は対象外）。

<!-- 本モードを採用しない場合は、本節と .claude/skills/autonomous-loop/ を削除する
（採否の判断は docs/guidelines/ADOPTION.md「1.2 自律ループ実行モードの採否」）。 -->

- **適用条件（MUST）**: ユーザーが開始を明示的に指示していること。指示されたスコープ内でのみ有効で、
  ループ終了と同時に通常の対話モードへ戻る。満たさない場合は `git add` / `git commit` を実行してはならない
- **起動方法（MUST）**: Skill `autonomous-loop` を起動し、その手順に従う。手順を記憶や推測で代用しない
- 統制要件（禁止操作・停止条件・秘密情報の取り扱い。サブエージェントへの委任時は 12.7）は常時読み込みの
  `rules/guardrails-unified.v1.md` セクション12、ブランチ・コミット規約は `CONTRIBUTING.md`「自律ループ実行モードの
  ブランチ・コミット規約」が正本

## 保守

共通規約の変更は `.github/copilot-instructions.md` へ、Claude Code 固有の変更は本ファイルへ反映します
（役割分担は `CONTRIBUTING.md`「エージェント指示ファイルの構成規約」）。

<!-- 本ファイルは配布元の templates/CLAUDE-template.md を基にしている。配布元の更新へ追従する場合は、
CHANGELOG.md で差分を確認し、本リポジトリ固有に書き換えた節（品質ゲート定義など）を上書きしないようマージする。 -->
