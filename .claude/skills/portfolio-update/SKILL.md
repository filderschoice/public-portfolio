---
name: portfolio-update
description: 公開ポートフォリオ（README.md の掲載表・最新リリース表・イラストと、そこから生成する site/index.html）を更新する手順。「ポートフォリオを更新して」「最新リリースを反映して」「掲載にアプリを追加して」「公開ページを更新して」等の依頼で参照する。更新内容の振り分け、scripts/propose-releases.py による差分案→確認→--apply、build-pages.py の再生成と --check、品質ゲート、コミット案の提示までを扱う。実 API は --live を明示したときだけで（対話モード、または自律ループ内では CONTRIBUTING.local.md の例外 EX-001 の期限内・条件内に限る）、git push と gh-pages への反映はユーザーが行う。
---

# ポートフォリオ更新手順

詳細な記述規則は `README.md`（「運用方針」「掲載するリポジトリを追加する手順」「公開ページの更新手順」）が正本です。
本スキルは依頼を受けたときの進め方だけを定め、規則は複製しません。

## 0. 前提と禁止（MUST）

- 正本は `README.md` の表。`site/index.html` は生成物なので直接編集しない（`build-pages.py` で再生成する）
- `git push` と gh-pages への反映（`git subtree push --prefix site origin gh-pages`）はユーザーが実行する。エージェントは行わない
- 資格情報・トークンは使わない。`propose-releases.py` は認証なしの公開 API だけを使い、`--live` を明示したときだけ接続する
  （`--live` も `--from-json` も無いときは接続せず終了コード2）
- SVG は手書きの模式図で、実画面ではない（注記を SVG の title とカードに出す）。実画面のキャプチャを置かない

## 1. 更新内容の振り分け

| 依頼 | やること |
| --- | --- |
| 最新リリースの反映 | 手順2（対話）または手順3（ループ）。RELEASES 表だけが変わる |
| 掲載する repo の追加・説明の修正 | 掲載表を直す。新しい repo は README の追加手順どおり、掲載表と RELEASES 表へ1行ずつ追加し、イラストの要否を決める |
| イラストの追加・修正 | `site/illustrations/<ID>.svg` を手書きし、掲載表のイラスト列へ ID を書く（禁止記述・注記・ダーク対応は README 参照） |

## 2. 対話モード（ユーザーが更新を依頼したとき）

1. `git branch --show-current` で作業ブランチ（規定ブランチ以外）を確認する。規定ブランチなら作成してから着手する
2. 掲載表・イラストの変更があれば先に直す。変更が README の規則を満たすかは手順5の生成でも検出される
3. 最新リリースを反映する場合: `python scripts/propose-releases.py --live` を実行する（実 API を GET。自律ループ内の `--live` は手順3の例外 EX-001 の条件内に限る）。
   出力された差分案（版・公開日・種類）が妥当か、プレリリース・正式の別を含めて確認してから、
   `python scripts/propose-releases.py --live --apply` で RELEASES 表だけを書き換える
4. エラー終了（終了コード2）したときは、メッセージの原因（取得失敗・掲載表の repo 列の形など）を直す。README は壊れない
5. `python scripts/build-pages.py` で再生成し、`python scripts/build-pages.py --check` で一致を確認する
6. `CLAUDE.md`「本リポジトリの品質ゲート定義」の markdownlint・validate-records を実行する（`replace-me` のゲートは対象外）
7. 記録（`docs/records/managed/`・`CHANGELOG.md`）を `docs/records/spec/FORMAT.md` に従って更新する
8. 対話モードでは `git add` / `git commit` をせず、コミット案（Conventional Commits、タイトルに絵文字）を提示する。
   案を提示する前に `python scripts/scan-secrets.py --include-unstaged` を実行して終了コード0を確かめる。
   `README.md`・`site/index.html`・追加した SVG は同じコミットに含める案とする
9. 公開するときは、push と gh-pages への反映をユーザーへ案内する（README「公開ページの更新手順」。ユーザーが実行する）

## 3. 自律ループ内

- 実 API は原則として呼ばない（guardrails 12.5）。`--live` は、`CONTRIBUTING.local.md`「例外の追跡」の EX-001 が**期限内**で、
  その条件（ユーザーがその回のループで最新リリースの反映を指示している／認証なし・資格情報不使用／GET のみ・接続先固定／
  実行はオーケストレータ本人で、サブエージェントへ委任しない／失敗時は再試行せず BACKLOG へ `要確認` で記録）を
  **すべて満たすときだけ**使える。期限切れ・条件不足のときは `--from-json <保存ファイル>` だけを使う
  （形式は `{"<repo 名>": <releases API の応答の配列>}`）。保存ファイルも無ければ最新リリースの更新は行わず、
  人手（対話モード）で行う項目として BACKLOG へ残す
- 例外を使った場合は、実施記録（`CHANGELOG.md`）へ「EX-001 により --live を実行した」と書く
- 掲載表・イラスト・build-pages.py の検証など、ネットワークを使わない更新は手順2の2・5〜7と同じに進め、
  ループの規約（Skill `autonomous-loop`）どおり作業ブランチへ 1 タスク 1 コミットする。作業ブランチへコミットする前に
  `git add` の後で `python scripts/scan-secrets.py --require-changes` を実行して終了コード0を確かめる
- push・gh-pages への反映・実画面の確認（見た目、実 API の結果が最新リリースと一致するか）は人手検証として残し、完了判定から除外する
