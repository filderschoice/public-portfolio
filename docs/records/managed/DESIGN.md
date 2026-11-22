<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用設計記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.design.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
# 実装用プロンプト設計書

## 目的

- filderschoice が GitHub で公開しているアプリ・ツールを一元管理し、何を公開しているかをすぐ見られる
  ポートフォリオを再実装するための設計書。詳細は各 repo の README を参照させ、ここでは一覧だけを持つ。

## 対象システム概要

- 対象: README.md（正本）と、そこから生成する公開ページ
- 掲載項目: sesami-wear・ikumemo・romcha（アプリ）、windows-devenv-setup（ツール）の4件。公開物が増えたら表へ1行追加する
- 最新リリース: 掲載表とは別の「最新リリース」表（`RELEASES:BEGIN` と `RELEASES:END` で囲む。列は 名前・最新リリース・公開日・種類）を
  README に持ち、各項目の最新1件（種類を問わず。プレリリースは種類で明示）をカードへ表示する。リリースが無ければ3列とも「-」
- イラスト: 各項目の簡易イラストを `site/illustrations/<ID>.svg` の固定資産（手書き SVG、viewBox 400x300）として持つ。
  README の説明に出てくる要素（品目などの例示は除く）だけを描いた模式図で、実画面ではない旨を SVG の title と図中、カードの注記に出す

## 実装済み機能要件

- FR-001: README.md の冒頭に概要を置き、`PORTFOLIO:BEGIN` と `PORTFOLIO:END` のマーカーで囲んだ Markdown 表に掲載項目を並べる
- FR-002: 表の列は 名前・説明・種別（アプリ/ツール）・プラットフォーム/言語・repo・Pages（無ければ「-」）・イラスト
  （SVG の ID。無ければ「-」。ID は `^[A-Za-z0-9-]+$` で、`site/illustrations/<ID>.svg` が実在すること）
- FR-003: `python scripts/build-pages.py`（標準ライブラリのみ）が表を読み、単一ファイルの `site/index.html` を生成する。
  生成物もコミットする（CI を使えない環境でも `--check` で整合を確認でき、ワークフロー導入後は公開元にそのまま使える）
- FR-004: `--check` は生成物が README と一致すれば終了コード0、不一致なら1。生成は冪等（2回実行して差分なし）。
  比較はバイト単位のため、`.gitattributes` で `site/index.html` を LF に固定する（`core.autocrlf=true` の Windows で
  CRLF に変換され、`--check` が誤って不一致になるのを防ぐ。他のファイルの改行方針は変えない）
- FR-006: 最新リリースのリンク先は repo 列の URL に `/releases/tag/<版>`（版は `urllib.parse.quote(safe='')` で `+` なども符号化）を付けて導出し、
  README に URL を持たない。カードには「最新リリース v0.17.0（2026-11-21・プレリリース）」の形で版をリンクにして出し、
  無ければ「最新リリース -」とする。値は `html.escape` で出力する
- FR-007: `python scripts/propose-releases.py`（標準ライブラリのみ。subprocess・gh・資格情報は使わない）が、掲載表の各 repo
  （`https://github.com/filderschoice/<repo>` の形のみ許可）について公開 REST API
  `https://api.github.com/repos/filderschoice/<repo>/releases?per_page=5` を GET し、draft を除く先頭1件（プレリリースを含む）を
  RELEASES 表の行（版・公開日 YYYY-MM-DD・正式/プレリリース）にした置き換え案を diff で標準出力へ出す。
  空配列は「-」の3列。`--apply` のときだけ RELEASES マーカー間を、同ディレクトリの一時ファイルへ書いてから `os.replace` で
  置換する（改行は元のファイルに合わせ、他の箇所は変えない。同じ内容なら「差分なし」で書き込まない＝冪等）。
  `--from-json FILE`（`{repo 名: 応答の配列}`、全 repo のキーが必要）で保存ファイルを読み、ネットワークへ接続しない。
  実 API へ接続するのは `--live` を明示したときだけで、`--live` も `--from-json` も無い（同時指定も不可）ときは接続せず案内を出して終了コード2。
  接続先は api.github.com（https）固定で、リダイレクト先も同ホスト以外は追従しない。タイムアウト10秒・応答上限1MiB・
  User-Agent は汎用名で、ヘッダーに資格情報・個人情報を含めない。JSON 不正・応答が配列でない・版/日付/prerelease の不正・
  draft のみ・未知の repo・repo 欠落・repo 列が対象外の URL・取得失敗はエラー終了（終了コード2）。build-pages.py とは分離し、
  ネットワークが無くても build-pages.py の生成と `--check` は変わらない
- FR-005: 次の場合はエラー終了（終了コード2）する。マーカーが1組でない、見出しが FR-002 の列と一致しない、データ行が無い、
  行が `|` で始まり終わらない、列数が7でない、名前・説明・プラットフォームが空、種別が アプリ/ツール 以外、
  repo・Pages（`-` を除く）が https の URL でない、イラストの ID が正規表現に合わない・SVG が実在しない・
  SVG が検査に通らない（XML として解析できない、生の文字列に DOCTYPE・ENTITY・処理命令・CDATA・XML コメント〔`<!--`。ElementTree が黙って捨てるため生の文字列で拒否〕がある、
  解析時（`iterparse` の `start-ns`）に取得した名前空間の宣言が、接頭辞なしの SVG の名前空間以外〔xlink を含む〕、ルート要素が SVG の svg でない、
  要素が許可リスト〔svg・title・desc・defs・style・g・rect・circle・ellipse・line・path・polygon・polyline・text・tspan〕外、
  属性が許可リスト外または `on` で始まる・href を含む・名前空間付き〔宣言できる名前空間が SVG のみのため、`xlink:href` は名前空間の宣言の段階で拒否され、
  属性の検査の名前空間付き分岐へ到達するのは暗黙の `xml:` 接頭辞〔`xml:lang` 等〕だけ〕、属性値または style 要素の中身に `url(`・`@import` など
  `@media` 以外の at 規則・バックスラッシュ・expression・javascript:・コメントがある。文字参照・実体参照は解析後の値で検査する。
  title・desc・text の本文は検査しないため、説明文に description や `xmlns="..."` 等が入っても誤検出しない）。repo・Pages の URL に `?`・`#`・空白・制御文字が含まれる。
  掲載表の名前が重複する。説明などのセルに `|` は使えない（列数不正になる）。
  最新リリース表は、`RELEASES` マーカーが1組でない、見出しが不一致、列数が4でない、名前が掲載表にない・重複・不足、
  版が英数と `.` `_` `+` `-` 以外を含む・先頭が英数でない、公開日が YYYY-MM-DD の実在日でない、種類が 正式/プレリリース 以外、
  版が「-」なのに公開日・種類が「-」でない、のいずれかでエラー終了する（FR-006）。
  検査しないもの: repo が `https://github.com/filderschoice/` 配下かどうか

## 設計方針

- 単一正本: 掲載データは README.md の表だけが持つ。別データファイルは作らず、他の成果物はすべてここから導出する。URL は `<https://...>` 形式で書く（MD034 対策）
- repo 列は `https://github.com/filderschoice/` 配下の実 repo 名を指す
- 説明文は各 repo の description を元にする

## 非機能要件

- セキュリティ: 資格情報を含めない。リンクは https のみ。表の値は `html.escape` で必ずエスケープして出力する。
  イラストは `<img src="illustrations/<ID>.svg">` で読み込み（index.html へ埋め込まない。img として読まれた SVG は
  スクリプトが動かず外部資源も読まれない）、生成スクリプトは SVG の中身を組み立てず固定資産を参照するだけにする。
  src は Pages が `/public-portfolio/` 配下のため相対パス。`head` に CSP の meta を置く:
  `default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'`（外部資源を読まない既存方針の機械的な担保。
  style は `<style>` へのインライン埋め込みのため `unsafe-inline` のみ許可し、script・フォント・外部画像は許可せず、base と form も禁止する）
- UI/UX: 掲載項目をカード（`.card`）で表示する。幅 40rem 以下で1列、それ以上で2列。`prefers-color-scheme: dark` で配色を切り替える。
  種別はバッジ（アプリ/ツール）の文字と色で判別でき、Pages が無い項目は Pages リンクを出さない。
  CSS は生成スクリプト内の定数 `CSS` に持ち、`<style>` へインラインで埋め込む。
  イラストはカード上部の枠（`.illust`。配色は `--ill-bg` でライト/ダークを切り替え、幅いっぱいに縮小）に出し、
  img に width・height（400x300）と alt（「<名前> の画面イメージ（簡易イラスト。実際の画面ではありません）」）を指定する。
  カードに「イメージ図。実際の画面ではありません」、ページの lead に同趣旨の一文を出す。SVG は style 内の
  `prefers-color-scheme` でダークに対応する
- 公開ページは外部 CSS・フォント・JS を読み込まない。出力先は `site/`（`docs/` はガードレール文書の置き場のため公開元にしない）

## テスト

- `tests/` に標準ライブラリの unittest だけで scripts/ 配下の検証コードのテストを置く（実行は `python -m unittest discover -s tests`）。
  build-pages.py は SVG 検査（許可・拒否の各入力。拒否は想定の分岐の理由メッセージまで確かめる）・掲載表と最新リリース表の検証・生成の冪等と `--check`、
  propose-releases.py は応答の検証・`--from-json`・`--apply`（表だけの更新・冪等・CRLF・置換失敗時に README を壊さない）・
  リダイレクト検証・ヘッダーとホストの固定・`--live` なしで接続しないことを検証する。ネットワークへは接続せず
  （接続する経路は mock）、書き込みは一時ディレクトリだけで、リポジトリのファイルは変えない
- 品質ゲート表（`CLAUDE.md`）の単体テスト行は `replace-me` のまま。ゲートへ載せるかは BACKLOG の BL-013（要確認）で判断する

## 実装制約

- 文書は日本語で記述する
- 記録ファイルは `docs/records/spec/FORMAT.md` に従う

## エージェント実装指示

- 掲載項目を増やすときは README の掲載表と最新リリース表へ1行ずつ追加し（イラストを付けるなら SVG も `site/illustrations/` へ置く）、品質ゲートを通す
- リリースのたびに `python scripts/propose-releases.py --live`（対話で依頼されたとき、またはループ内では例外 EX-001 の期限内・条件内だけ）
  で差分案を出して確認し、`--live --apply` で最新リリース表を更新して、生成と `--check` を実行する（FR-007）。
  ループ内の実 API は `CONTRIBUTING.local.md` の例外 EX-001（期限 2027-11-22）の条件内だけで、それ以外は `--from-json` だけを使う
- 要件 FR-001・FR-002 を変更する場合は本書を更新する
<!-- COPILOT_RECORDS:END -->
