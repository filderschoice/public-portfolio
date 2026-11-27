# 変更履歴

このリポジトリの主要な変更は本ファイルに記録します。

## 2026-11-28

- 掲載に mimiduku（アプリ、v0.1.0 プレリリース 2026-11-27）を追加し、手書きの簡易イラスト `site/illustrations/mimiduku.svg` を追加。
  最新リリース表と公開ページを更新
- 掲載表へ「初回公開日」列（最初のリリースの公開日。無ければ `-`）を追加し、公開ページのカードへ「初回公開 YYYY-MM-DD」を表示。
  build-pages.py に日付の検査を追加し、propose-releases.py の列定義とテストの表を8列へ合わせた。値は手で書く（propose-releases.py は更新しない）

## 2026-11-22

- ユーザーの決定で BL-013 を完了とし、`CLAUDE.md` の品質ゲート表の単体テスト行を `python -m unittest discover -s tests`（全件成功）へ変更。
  BL-013 を BACKLOG から削除し、BACKLOG は空。DESIGN の記述を合わせた
- ユーザーの指示で BL-011（人手検証）を完了として BACKLOG から削除。公開ページ（gh-pages `f1ac976`、ビルド成功・HTTP 200）で
  ikumemo の v0.1.0 リンクを含む表示を確認済み。BACKLOG は BL-013（要確認）のみ
- ユーザーの決定（実 API を自律ループでも使えるようにする）を、ガードレール 9 章の期限付き例外 EX-001 として `CONTRIBUTING.local.md` へ記録
  （最新リリースの取得に限り `--live` を許可。条件5点・期限 2027-11-22・責任者 `@filderschoice`）。`rules/` の本文は変更していない。
  portfolio-update の Skill・README・DESIGN・propose-releases.py の記述を合わせた
- 最新リリースの反映手順の確認として、ikumemo の v0.1.0（2026-11-22、プレリリース）を RELEASES 表へ反映し、`site/index.html` を再生成。
  API 応答は対話側で保存し（認証なし・GET のみ）、ループ内は `propose-releases.py --from-json` と `--apply` のみで実施。
  gh-pages への反映はユーザーが `git subtree push --prefix site origin gh-pages` で行う
- SVG の生文字列拒否のテストが別の分岐で通る偽陽性を修正（拒否メッセージの固有化と、分岐間でメッセージが重ならない自己検査の追加）
- 再点検の指摘の修正: SVG 検査の拒否テストを想定の分岐の理由まで確かめる形へ作り直し、名前空間の検査を iterparse の start-ns へ変更
  （本文中の xmlns の誤検出を解消）、XML コメントを拒否、デッドコードを削除、`.gitignore`（`__pycache__/`・`*.pyc`）を追加
- scripts/ 配下の検証コード（build-pages.py・propose-releases.py）の単体テストを tests/ へ追加（unittest、35件）。
  品質ゲート表へ載せるかの判断を BL-013（要確認）として起票
- レビュー指摘の修正: SVG 検査を XML 解析による許可リスト方式へ変更、版に + を許可、掲載表の名前重複と repo・Pages URL の ?・# の検査、
  CSP へ base-uri・form-action を追加、propose-releases.py は --live を明示したときだけ接続する仕様へ変更、
  SVG の具体名を汎用化し薄い文字色を AA（4.5:1）以上へ変更、Skill の scan-secrets の使い方を品質ゲート定義に合わせた
- ポートフォリオ更新の手順を固定するプロジェクト用 Skill portfolio-update を追加（BL-012）。対話モードの手順と
  自律ループ内の制約（実 API を呼ばず --from-json のみ、push はユーザー）を記述
- 最新リリース表の更新補助スクリプト scripts/propose-releases.py を追加（BL-010）。公開 REST API（認証なし）または
  --from-json の保存ファイルから差分案を出し、--apply で RELEASES 表だけを書き換える。README・DESIGN の更新手順を反映
- README へ最新リリース表を追加し、公開ページのカードへ最新リリース（版・日付・種類、リンク付き）を表示。
  build-pages.py へ表の検証を追加（BL-009）
- ユーザーの決定を反映: 最新リリースの取得は gh ではなく公開 REST API（認証なし）を urllib で GET する補助スクリプト
  propose-releases.py を作る方向とし、BL-010 を要確認から未着手へ改めた。更新依頼の手順を固定する Skill
  portfolio-update を BL-012 として起票し、BL-011 の依存と完了条件を更新
- README の掲載表へイラスト列を追加し、公開ページのカードへ簡易イラストと「実際の画面ではありません」の注記を表示。
  build-pages.py へイラストの ID・実在・禁止記述の検査と CSP の meta を追加（BL-008）
- 掲載4件の簡易イラスト（SVG）を `site/illustrations/` へ追加し、`.gitattributes` で LF に固定（BL-007）。
  実際の画面ではない模式図で、ダークモードに対応
- 公開ページへ簡易イラストと最新リリース情報を加える作業計画を `docs/records/managed/BACKLOG.md` へ起票
  （BL-007〜BL-011）。SVG 資産の追加（BL-007）、イラスト列と表示（BL-008）、最新リリース表と表示（BL-009）、
  gh を使うリリース取得の補助スクリプトの要否（BL-010）は要確認、実ブラウザでの見た目確認と gh-pages への反映（BL-011）は人手検証
- 公開ポートフォリオ（README.md を正本とし GitHub Pages へ公開）の作業計画を
  `docs/records/managed/BACKLOG.md` へ起票（BL-001〜BL-006）。ワークフロー追加（BL-005）は要確認、
  Pages の有効化と初回デプロイ（BL-006）は人手検証として扱う
- ポートフォリオの正本 README.md（掲載表4件）を追加し、DESIGN.md へ方針を記載（BL-001）
- 公開ページ生成スクリプト scripts/build-pages.py と生成物 site/index.html を追加（BL-002）
- 公開ページをカード表示・レスポンシブ・ダークモードに対応（BL-003）
- README に掲載リポジトリの追加手順を追記（BL-004）
- レビュー指摘の修正として .gitattributes で site/index.html を LF に固定し、README・DESIGN の記述を整理
- BACKLOG の BL-005 へ CODEOWNERS のプレースホルダの確認事項、BL-006 へ Pages 公開元の注記を追記
- ユーザーの決定を反映: デプロイは GitHub Actions を使わず端末から `gh-pages` ブランチへ push する方式とし、
  README に「公開ページの更新手順」を追記（BL-005 は不要となり削除、BL-006 の依存を解除）。
  repo は public にする。`.github/CODEOWNERS` を `* @filderschoice` に変更（sesami-wear・ikumemo と同じ形）
- GitHub の repo 設定を適用（main のブランチ保護、脆弱性の非公開報告、Dependabot、Actions のトークンを読み取り専用、
  説明文・topics・homepage、Wiki 無効化、マージ後のブランチ自動削除）。`gh-pages` を push して Pages を公開
  （`https://filderschoice.github.io/public-portfolio/`、ビルド成功・HTTP 200）
- 公開ページの掲載4件・Pages リンク3件を確認し、ユーザーの指示で BL-006（人手検証）を完了として削除。BACKLOG は空
