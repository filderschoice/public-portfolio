<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用実施記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.execute.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
```yaml
- date: 2026-11-22 23:30
  summary: 最新リリース取得の実 API 利用を、ガードレール 9 章の期限付き例外 EX-001 として記録し、関連する記述を合わせた
  details:
    変更内容: >-
      ユーザーの決定（実 API を自律ループでも使えるようにする）に基づき、CONTRIBUTING.local.md を新規作成して例外 EX-001 を記録した
      （最新リリースの取得に限り --live を許可。条件は、その回のループで反映を指示済み・認証なしで資格情報を使わない・GET のみで接続先固定・
      実行はオーケストレータ本人でサブエージェントへ委任しない・失敗時は再試行せず要確認で記録。期限 2027-11-22、責任者 @filderschoice）。
      rules/ の本文は変更していない。Skill portfolio-update の手順3、README の運用方針、DESIGN、propose-releases.py の説明文
      （docstring とエラーメッセージの文言のみ。挙動は不変）を例外に合わせた
    変更ファイル:
      - CONTRIBUTING.local.md
      - .claude/skills/portfolio-update/SKILL.md
      - README.md
      - scripts/propose-releases.py
      - docs/records/managed/DESIGN.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python -m unittest discover -s tests、build-pages.py --check、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 36件すべて成功、各ゲート合格。例外を使った --live の実行自体は未実施
- date: 2026-11-22 22:30
  summary: SVG の生文字列拒否のテストが別分岐で通る偽陽性を修正
  details:
    変更内容: >-
      生文字列の拒否メッセージを「SVG に使えない構文」へ変え、属性値・style の分岐のメッセージと部分文字列で重ならないようにした。
      拒否テストへ、各分岐の期待文字列が他の分岐のメッセージに含まれないことの自己検査と、DOCTYPE なしの ENTITY のケースを追加した。
      SVG_RAW_FORBIDDEN の各項目（DOCTYPE・ENTITY・処理命令・CDATA・コメント）を一時的に外すと対応するテストだけが落ちることを確認し、元へ戻した
    変更ファイル:
      - scripts/build-pages.py
      - tests/test_build_pages.py
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python -m unittest discover -s tests、build-pages.py の再生成と --check、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 36件すべて成功、各ゲート合格
- date: 2026-11-22 22:00
  summary: SVG 検査の拒否テストの偽陽性・デッドコード・名前空間検査の誤検出を修正し、.gitignore を追加
  details:
    変更内容: >-
      build-pages.py の SVG 検査を整理した。名前空間の宣言は生文字列の正規表現をやめ、ElementTree.iterparse の start-ns で
      取得して接頭辞なしの SVG の名前空間以外（xlink を含む）を拒否する（title・desc・text の本文に xmlns="..." と書いても
      誤検出しない）。XML コメントは ElementTree が黙って捨てるため生の文字列で拒否し、デッドコードの isinstance 判定を削除した。
      属性の拒否理由を名前空間付き・イベントハンドラ・リンクに分けた。拒否テストは、想定の分岐の理由メッセージまで確かめる
      形へ作り直し（XML として不正な入力は解析の分岐として分離）、コメント・xmlns の本文・名前空間宣言・xml:lang・on* 大文字混在・
      文字参照による url( と javascript: のケースを追加した。各分岐を一時的に壊すと対応するテストが落ちることを確認し元へ戻した。
      xlink:href 属性は名前空間の宣言で先に拒否されるため属性側の分岐には到達せず、その旨を DESIGN へ記した。
      リポジトリ直下へ .gitignore（__pycache__/ と *.pyc のみ）を追加した。README・DESIGN の記述を実装に合わせた
    変更ファイル:
      - scripts/build-pages.py
      - tests/test_build_pages.py
      - .gitignore
      - README.md
      - docs/records/managed/DESIGN.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python -m unittest discover -s tests、build-pages.py の再生成と --check、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 36件すべて成功、各ゲート合格
- date: 2026-11-22 21:00
  summary: scripts/ 配下の検証コードの単体テスト（unittest）を tests/ へ追加
  details:
    変更内容: >-
      標準ライブラリの unittest だけで、build-pages.py（SVG 検査の許可・拒否24種、掲載表と最新リリース表の検証、
      生成の冪等と --check、CSP）と propose-releases.py（応答の検証、--from-json、--apply の表だけの更新・冪等・CRLF・
      置換失敗時に README を壊さないこと、リダイレクト検証、ヘッダーとホストの固定、応答上限、--live なしで接続しないこと）の
      テスト35件を tests/ へ追加した。ネットワークへは接続せず（接続経路は mock）、書き込みは一時ディレクトリだけで、
      リポジトリのファイルは変えない。実行方法を README の運用方針と DESIGN へ記載した。CLAUDE.md の品質ゲート表は
      変更せず、ゲートへ載せるかを BL-013（要確認）として起票した
    変更ファイル:
      - tests/helpers.py
      - tests/test_build_pages.py
      - tests/test_propose_releases.py
      - README.md
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python -m unittest discover -s tests、build-pages.py の --check、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 35件すべて成功、各ゲート合格。テスト実行後にリポジトリのファイルに変更なし
    関連ID:
      - BL-010
      - BL-013
- date: 2026-11-22 20:00
  summary: レビュー指摘の修正（SVG 検査の XML 解析化・版の + 許可・名前重複と URL 検査・CSP 強化・--live の明示化・SVG の整理）
  details:
    変更内容: >-
      build-pages.py の SVG 検査を部分一致の正規表現から xml.etree.ElementTree による解析へ置き換えた（DOCTYPE・ENTITY・
      処理命令・CDATA の禁止、要素と属性の許可リスト、on* と href 系と名前空間付き属性の禁止、xmlns は SVG の名前空間のみ、
      style 要素と属性値の url(・@import 以外の at 規則・バックスラッシュ・expression・コメントの禁止。解析後の値を検査するため
      文字参照や svg/onload の変形も弾き、description 等の本文は誤検出しない）。版の文字種へ + を許可（build-pages.py と
      propose-releases.py で同じ規則。リンクは quote で %2B）。掲載表の名前重複と、repo・Pages の URL に ?・#・空白・制御文字を
      含むものを終了コード2にした。CSP へ base-uri 'none'; form-action 'none' を追加。propose-releases.py は --live を明示した
      ときだけ接続し、--live も --from-json も無ければ案内を出して終了コード2（同時指定は不可）にした。
      windows-devenv-setup.svg の説明に無い具体名を汎用の実行行へ変え、全 SVG の薄い文字色（--mu のライト）を #57606a へ
      変更し、未使用の CSS を削除した。README・DESIGN・Skill・BACKLOG（BL-011）の記述を実装に合わせた。
      Skill の scan-secrets の使い方を CLAUDE.md の品質ゲート定義に合わせた。
      コントラスト（相対輝度から計算。48個の text を対象に、背景は直下の矩形・円と不透明度から算出）: ライトの最小 4.87、
      ダークの最小 6.64（すべて 4.5 以上）。例: ライトの --mu #57606a は背景 #eaeef2 で 5.48・パネル #f0f3f6 で 5.74、
      ダークの --mu #9da7b3 は #0d1117 で 7.76、完了表示の文字（#1f2328）は薄緑の背景で 11.96。修正前はライトの --mu が
      3.90 と 4.08 で基準未満だった
    変更ファイル:
      - scripts/build-pages.py
      - scripts/propose-releases.py
      - site/illustrations/ikumemo.svg
      - site/illustrations/romcha.svg
      - site/illustrations/sesami-wear.svg
      - site/illustrations/windows-devenv-setup.svg
      - site/index.html
      - README.md
      - .claude/skills/portfolio-update/SKILL.md
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      build-pages.py の2回実行と --check、SVG 検査の異常系17件（svg/onload、文字参照 scr&#105;pt、CDATA、style 内の url(・@import・
      バックスラッシュ・expression、href と xlink、大文字の ONCLICK、DOCTYPE・ENTITY、処理命令、不正な xmlns、script・foreignObject、
      style 属性の url(）と desc に description を含む正常系、版に + を含む表示と pick_release、掲載表の名前重複・URL の ?・#・空白、
      propose-releases.py の引数なしと --live/--from-json 同時指定（接続せず終了コード2）、markdownlint-cli2、validate-records.py、
      scan-secrets.py。異常系の確認は一時的な文字列・メモリ上の README で行い、リポジトリのファイルは変えていない
    検証結果: >-
      成功 - 異常系はすべて拒否（終了コード2またはエラー）、正常系は通り、再生成は冪等で --check 一致、各ゲート合格。
      実 API には接続していない
    関連ID:
      - BL-010
      - BL-012
- date: 2026-11-22 19:00
  summary: ポートフォリオ更新の手順を固定するプロジェクト用 Skill portfolio-update を追加
  details:
    変更内容: >-
      .claude/skills/portfolio-update/SKILL.md を新規追加した（frontmatter は name と description のみ、model は指定しない）。
      更新依頼の振り分け（最新リリース・掲載 repo の追加と修正・イラスト）、対話モードの手順（差分案の確認→--apply→
      build-pages.py の再生成と --check→品質ゲート→コミット案の提示）、自律ループ内の手順（実 API を呼ばず --from-json のみ）、
      push と gh-pages への反映はユーザーが行うことを記述した。詳細な規則は README を参照させ、複製しない。
      スキルは手順の記述のみで、権限・設定・hooks は変えていない。「守る側」に近いため、diff-reviewer での点検をオーケストレータへ依頼する
    変更ファイル:
      - .claude/skills/portfolio-update/SKILL.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      markdownlint-cli2（対象 30 ファイルが git ls-files の件数と一致）、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - いずれも合格
    関連ID:
      - BL-012
- date: 2026-11-22 18:00
  summary: 最新リリース表の更新補助スクリプト propose-releases.py を追加
  details:
    変更内容: >-
      scripts/propose-releases.py を新規追加した（標準ライブラリのみ）。掲載表の repo 列
      （https://github.com/filderschoice/<repo> の形のみ許可）から公開 REST API（認証なし、api.github.com 固定、
      リダイレクト先も検証、タイムアウト10秒、応答上限1MiB、汎用の User-Agent）で各 repo の最新リリース
      （draft を除く先頭1件）を取得し、RELEASES 表の差分案を出力する。--apply のときだけ RELEASES マーカー間を
      一時ファイル経由のアトミック置換で書き換え（改行保持・冪等）、--from-json でネットワーク無しの同じ処理ができる。
      不正な入力は終了コード2。README の運用方針と DESIGN（FR-007・実装指示）を実際の手順へ更新した。
      ループ内では実 API を呼ばず、検証は --from-json の一時ファイルだけで行った
    変更ファイル:
      - scripts/propose-releases.py
      - README.md
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      --from-json の保存ファイル（一時ファイル）での差分案の出力・--apply・2回目の --apply、draft の除外、
      プレリリース判定、リリース無し、CRLF の README、不正入力10種と repo 列が対象外の URL、リダイレクト検証、
      build-pages.py の生成と --check、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 差分案どおりに RELEASES 表だけが変わり、2回目は差分なし、CRLF も保持、不正入力はすべて終了コード2、
      http 以外・api.github.com 以外へのリダイレクトは拒否、--apply した README で build-pages.py の生成と --check が通った。
      実 API は呼んでいない（BL-011 の人手検証で確認する）
    関連ID:
      - BL-010
- date: 2026-11-22 17:00
  summary: 最新リリース表を追加し build-pages.py でカードへ表示・検証
  details:
    変更内容: >-
      README に「最新リリース」表（RELEASES:BEGIN/END。名前・最新リリース・公開日・種類）を追加し、値は確認済みの事実を
      手で書いた（sesami-wear は v0.17.0・2026-11-21・プレリリース、romcha は v1.2.0・2026-10-15・正式、
      ikumemo と windows-devenv-setup は -）。build-pages.py が表を検証し（名前の過不足・重複・未知、版・公開日・種類の
      形式、版が - のとき他列も -。不正は終了コード2）、カードへ「最新リリース 版（日付・種類）」を repo 列の URL と
      /releases/tag/版（quote）から導出したリンクで表示する。無ければ「最新リリース -」。値は html.escape。
      README の運用方針・追加手順と DESIGN（FR-005・FR-006・非機能要件・実装指示）を更新し、site/index.html を再生成した。
      更新補助スクリプトは未作成のため、README・DESIGN には手で直す旨だけを書いた（BL-010 完了後に追記する）
    変更ファイル:
      - scripts/build-pages.py
      - README.md
      - site/index.html
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python scripts/build-pages.py の2回実行と cmp、--check、README を一時的に書き換えた異常系（名前不足・重複・未知の名前、
      不正な版・先頭が記号の版・実在しない日付・日付形式・不正な種類・版が - で他列あり・版があり他列が -・マーカー欠落）の
      終了コード確認（確認後に復元）、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 生成は冪等で --check 一致、異常系11件はすべて終了コード2、4件のカードにリリース表示が出て、各ゲート合格
    関連ID:
      - BL-009
- date: 2026-11-22 16:00
  summary: README にイラスト列を追加し build-pages.py でカードへ表示・検証
  details:
    変更内容: >-
      README の掲載表へ「イラスト」列（Pages 列の右。SVG の ID か「-」）を追加し、build-pages.py がカードへ
      img 要素（相対パス illustrations/ID.svg、width と height、alt を html.escape）で表示するようにした。
      ID は ^[A-Za-z0-9-]+$ かつ site/illustrations/ID.svg が実在するものだけを受け付け、SVG に script・foreignObject・
      on で始まる属性・href・url(・@import・http があれば終了コード2とする。カードとページの lead に
      「実際の画面ではありません」の注記を出し、CSS へイラスト枠の配色（ライト/ダーク）を追加した。
      head へ CSP の meta（default-src 'none'; img-src 'self'; style-src 'unsafe-inline'）を加えた。
      README の列説明・追加手順、DESIGN の FR-002・FR-005・非機能要件を更新し、site/index.html を再生成した。
      既定値: 名前空間宣言 xmlns="http://www.w3.org/2000/svg" は http の検査前に取り除く。
      イラストの alt とカードの注記は SVG 内の注記と重複するが、画像が読めない場合の代替のため両方残した
    変更ファイル:
      - scripts/build-pages.py
      - README.md
      - site/index.html
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python scripts/build-pages.py の2回実行と cmp、--check、不正 ID・存在しない ID・スラッシュ入り ID と
      禁止要素（script・href・on 属性・foreignObject・url(・@import・http）を一時的に混入させた SVG での終了コード確認
      （確認後に元へ復元）、ヘッドレス Edge での描画確認、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 生成は冪等で --check 一致、異常系はすべて終了コード2、4件のカードにイラストと注記が表示され、各ゲート合格
    関連ID:
      - BL-008
- date: 2026-11-22 15:00
  summary: 掲載4件の簡易イラスト（SVG）を site/illustrations/ へ追加
  details:
    変更内容: >-
      sesami-wear・ikumemo・romcha・windows-devenv-setup の模式図を手書きの SVG（viewBox 400x300）として追加した。
      README の説明に出てくる要素（ウォッチのタイルと状態表示、音声入力・買い物リスト・スワイプ・カレンダー・期限、
      動画に重なる見るだけの浮動チャット窓、winget と npm の実行行と完了表示）だけを描き、各 SVG に role="img"・title・desc・
      「実際の画面ではありません」の注記を入れた。配色は style 内の prefers-color-scheme でダークに対応した。
      script・foreignObject・イベント属性・href・url(・@import・外部フォント・埋め込み画像は使っていない。
      .gitattributes へ site/illustrations/*.svg の eol=lf を追加した。
      既定値: SVG を単体で表示するには名前空間宣言 xmlns="http://www.w3.org/2000/svg" が必須のため、
      完了条件の「http を含まない」は、この宣言だけを除いて検査する意味に解釈した（BL-008 の検査も同様に記述を補った）
    変更ファイル:
      - site/illustrations/sesami-wear.svg
      - site/illustrations/ikumemo.svg
      - site/illustrations/romcha.svg
      - site/illustrations/windows-devenv-setup.svg
      - .gitattributes
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      xml.etree.ElementTree による4件の解析、禁止要素・属性・http の検索、ヘッドレス Edge での描画確認、
      python scripts/build-pages.py --check、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 4件が XML として解析でき、禁止語の検索は0件（名前空間宣言を除く）、ライト/ダークとも描画を確認、各ゲート合格
    関連ID:
      - BL-007
- date: 2026-11-22 14:00
  summary: レビュー指摘の修正（site/index.html の改行固定と README・DESIGN の記述整理）
  details:
    変更内容: >-
      .gitattributes を新規作成し site/index.html を LF に固定した（core.autocrlf=true の Windows で --check が
      誤って不一致になるのを防ぐ。スクリプトは変更なし）。README の追加手順へセル内に | を書けない制約を追記し、
      DESIGN.md の FR を番号順に直して FR-005 の検査範囲と非検査項目を実装どおりに書き、設計方針の文意を整えた
    変更ファイル:
      - .gitattributes
      - README.md
      - docs/records/managed/DESIGN.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      git check-attr、python scripts/build-pages.py の2回実行と --check、markdownlint-cli2、validate-records.py、
      scan-secrets.py
    検証結果: >-
      成功 - 属性が text eol=lf と解決され、生成は冪等で --check 一致、各ゲート合格
    関連ID:
      - BL-002
      - BL-003
      - BL-004
- date: 2026-11-22 13:30
  summary: README に掲載リポジトリの追加手順を追記
  details:
    変更内容: >-
      README.md へ「掲載するリポジトリを追加する手順」（表への1行追加、種別・プラットフォームの書き方、Pages が無い場合、
      再生成と --check、コミット対象）を追記した。架空の1行を一時追加して手順どおりに生成と --check が成功することを確かめ、
      行と生成物を元に戻した
    変更ファイル:
      - README.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      架空行の追加後に python scripts/build-pages.py と --check、復元後に --check、markdownlint-cli2、
      validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 架空行で生成と --check が成功し Pages 列が - の行は Pages リンクを出さず、復元後も --check は一致、各ゲート合格
    関連ID:
      - BL-004
- date: 2026-11-22 13:00
  summary: 公開ページをカード表示・レスポンシブ・ダークモードに対応
  details:
    変更内容: >-
      build-pages.py にインライン CSS を追加し、カード表示、幅 40rem 以下で1列、prefers-color-scheme のダークモード、
      種別バッジを実装した。Pages が無い項目はリンクを出さない。site/index.html を再生成した
    変更ファイル:
      - scripts/build-pages.py
      - site/index.html
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python scripts/build-pages.py を2回実行して差分なし、--check、生成物の外部参照と prefers-color-scheme の grep、
      markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 冪等性と --check 一致、外部リソース参照0件、各ゲート合格。ブラウザでの表示は未確認
    関連ID:
      - BL-003
- date: 2026-11-22 12:30
  summary: 公開ページ生成スクリプト scripts/build-pages.py と site/index.html を追加
  details:
    変更内容: >-
      README の掲載表から site/index.html を生成する build-pages.py（--check 付き、HTML エスケープ、https のみ許可、
      マーカー・列の検証）を追加し、生成物をコミット対象とした。DESIGN.md に生成方式と出力先を反映した
    変更ファイル:
      - scripts/build-pages.py
      - site/index.html
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      python scripts/build-pages.py を2回実行して差分なし、python scripts/build-pages.py --check、不正入力（http リンク・
      マーカー欠落・見出し不一致・javascript スキーム）での停止確認、markdownlint-cli2、validate-records.py、scan-secrets.py
    検証結果: >-
      成功 - 生成は冪等で --check は一致時0・不一致時1、不正入力は終了コード2で停止、各ゲート合格
    関連ID:
      - BL-002
- date: 2026-11-22 12:00
  summary: ポートフォリオの正本 README.md を作成
  details:
    変更内容: >-
      README.md に概要と掲載表（PORTFOLIO マーカーで囲む4件）を作成し、DESIGN.md へ目的・掲載項目・単一正本の方針を記載した
    変更ファイル:
      - README.md
      - docs/records/managed/DESIGN.md
      - docs/records/managed/BACKLOG.md
      - docs/records/managed/EXECUTE.md
      - CHANGELOG.md
    検証コマンド: >-
      npx markdownlint-cli2、python scripts/validate-records.py、python scripts/scan-secrets.py --require-changes
    検証結果: >-
      成功 - 3コマンドとも合格
    関連ID:
      - BL-001
```
<!-- COPILOT_RECORDS:END -->
