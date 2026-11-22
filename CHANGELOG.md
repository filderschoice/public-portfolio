# 変更履歴

このリポジトリの主要な変更は本ファイルに記録します。

## 2026-11-22

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
