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
    ライト/ダーク・狭幅/広幅で判読でき、SVG とリリースリンクが正しく開く
  依存:
    - BL-008
    - BL-009
  根拠: >-
    見た目の判読性と gh-pages への push は自動検証できず、push はユーザーが実行する決まりのため人手検証とする
- id: BL-010
  区分: 機能追加
  タスク内容: >-
    gh で各 repo の最新リリースを取得し、README の最新リリース表（BL-009）の置き換え案を標準出力へ出すだけの
    補助スクリプト scripts/propose-releases.py を追加するかを決める。追加する場合は build-pages.py と分離し、
    標準ライブラリと gh のみを使い、README を書き換えず、gh へは引数リストで渡す（シェルを介さない）。
    対象は repo 列が https://github.com/filderschoice/ 配下の行に限る
  優先度: P3
  状態: 要確認
  担当: ユーザー
  完了条件: >-
    ユーザーが追加の要否を決める。追加する場合は、ネットワーク無しでも build-pages.py の生成と --check が
    変わらず通り、補助スクリプトの実行（gh の認証を使う）はユーザーが行う
  依存:
    - BL-009
  根拠: >-
    ユーザーの gh 認証情報で外部サービス（GitHub API）を呼ぶため要確認とした。掲載は4件で手更新の負担は小さく、
    無くても BL-009 は成立する。ループ内では実行も疎通確認もしない
- id: BL-009
  区分: 機能追加
  タスク内容: >-
    README に掲載表とは別の「最新リリース」表（RELEASES:BEGIN と RELEASES:END のマーカー、列は
    名前・最新リリース・公開日・種類）を追加し、build-pages.py が読んでカードへ表示する。
    値はオーケストレータ確認済みの事実を手で書く（sesami-wear は v0.17.0・2026-11-21・プレリリース、
    romcha は v1.2.0・2026-10-15・正式、ikumemo と windows-devenv-setup はすべて「-」）。
    リンク先は repo 列の URL に /releases/tag/<版> を付けて導出し（版は urllib.parse.quote）、README に URL を持たない。
    検証（不正時は終了コード2）は、掲載表の名前が過不足なく1行ずつあること、版が英数と . _ - だけで先頭が英数、
    公開日が YYYY-MM-DD の実在日、種類が 正式/プレリリース、版が「-」なら他の列も「-」であること。
    カードには「最新リリース v0.17.0（2026-11-21・プレリリース）」のようにリンク付きで出し、
    リリースが無ければ「最新リリース -」とする。値は html.escape で出力する。
    README の運用方針・追加手順へリリース表の更新方法（リリースのたびに表を直し、生成と --check を実行）を追記し、
    DESIGN.md の FR-005 と非機能要件・エージェント実装指示へリリース表の仕様を反映する
  優先度: P2
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    python scripts/build-pages.py の再実行で差分が出ず（冪等）、--check が終了コード0。
    名前の不足・重複・未知の名前、不正な版・日付・種類を与えると終了コード2になることを一時ファイルで確かめる。
    markdownlint・validate-records・scan-secrets が合格
  依存:
    - BL-008
  根拠: >-
    既定値として、掲載表の列を増やさず別表にした（リリースは頻繁に変わり、行単位の手更新と BL-010 の置き換え案の
    貼り付けがしやすい。掲載表の肥大化も避けられる）。表示するのは種類を問わず最新の1件とし、
    プレリリースは文字で明示する（sesami-wear の最新は v0.17.0 のプレリリースで、隠すと最新の開発状況が伝わらない）。
    URL を README に持たず repo 列から導出するため、新たな外部リンクの入口が増えない
- id: BL-008
  区分: 機能追加
  タスク内容: >-
    README の掲載表へ「イラスト」列（Pages 列の右。値は SVG の ID か「-」）を追加し、
    build-pages.py がカードへ img 要素で表示する。ID は正規表現 ^[A-Za-z0-9-]+$ に一致し、
    site/illustrations/<ID>.svg が実在するものだけを受け付ける（それ以外は終了コード2）。
    参照する SVG に script・foreignObject・on で始まる属性・href/xlink:href・url(・@import・http が含まれれば
    終了コード2とする（固定資産の混入対策）。img の src は相対パス illustrations/<ID>.svg（Pages は
    /public-portfolio/ 配下のため絶対パスにしない）、alt は「<名前> の画面イメージ（簡易イラスト。実際の画面ではありません）」を
    html.escape して出し、width と height を指定する。カードに「イメージ図。実際の画面ではありません」の注記を、
    ページの lead にも同趣旨の一文を出す。CSS 定数へイラストの枠の配色（ライト/ダーク）を追加する。
    head に Content-Security-Policy の meta（default-src 'none'、img-src 'self'、style-src 'unsafe-inline'）を加える。
    README の列説明・追加手順（イラストの ID、SVG の置き場所と禁止要素、無い場合は「-」）と、
    DESIGN.md の FR-002・FR-005・非機能要件を更新し、site/index.html を再生成する
  優先度: P1
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    4件のカードにイラストと注記が出る。build-pages.py の再実行で差分が出ず（冪等）、--check が終了コード0。
    不正な ID・存在しない ID・禁止要素を含む SVG で終了コード2になることを一時ファイルで確かめる
    （確認後に一時ファイルを残さない）。markdownlint・validate-records・scan-secrets が合格
  依存:
    - BL-007
  根拠: >-
    既定値として、SVG は index.html へ埋め込まず img で読み込む方式にした（img として読まれた SVG ではスクリプトが
    動かず外部資源も読まれないため安全で、生成スクリプトが SVG の中身を組み立てないので XSS 面が増えない）。
    イラストの対応付けは名前からの暗黙導出ではなく列で明示し、共有や「-」を書ける形にした。
    CSP は外部資源を読まない既存方針を機械的に担保するだけで、公開範囲や外部への影響は変わらない
- id: BL-007
  区分: 機能追加
  タスク内容: >-
    掲載4件の簡易イラストを手書きの SVG として site/illustrations/ へ追加する（sesami-wear.svg・ikumemo.svg・
    romcha.svg・windows-devenv-setup.svg）。描くのは README の説明に由来する要素だけで、
    sesami-wear は丸いウォッチ画面に施錠/解錠のタイル（ワンタップのボタン）と状態を示すコンプリケーション、
    ikumemo はスマホ画面にマイクと買い物リスト・スワイプで記録する行・小さなカレンダー、
    romcha はスマホ画面の動画領域に重なる浮動チャット窓（見るだけで入力欄を描かない）、
    windows-devenv-setup はターミナル窓に winget と npm の実行行と完了表示を描く。
    各 SVG は viewBox を持ち、role="img" と aria-labelledby で参照する title・desc を入れ、
    title には「イメージ図（実際の画面ではありません）」を含める。自前の背景を敷き、
    style 内の prefers-color-scheme の切り替えでダークでも判読できる配色にする。
    script・foreignObject・イベント属性・href・外部 URL・外部フォント・埋め込み画像を使わず、文字は最小限にする。
    改行を LF に固定するため .gitattributes へ site/illustrations/*.svg の eol=lf を追加する
  優先度: P1
  状態: 未着手
  担当: AIエージェント
  完了条件: >-
    4つの SVG が XML として解析でき（python の xml.etree.ElementTree で読める）、禁止要素・属性・http を含まない
    （検索で0件）。markdownlint・validate-records・scan-secrets が合格し、build-pages.py --check が変わらず終了コード0
  依存: []
  根拠: >-
    実機画面ではなく説明文に基づく模式図とし、実画像と誤解されないよう SVG 自体の title にも注記を持たせる。
    参照の追加（BL-008）と分けたのは、資産の作成と生成スクリプトの変更を別々にレビューできるようにするため
```
<!-- COPILOT_RECORDS:END -->
