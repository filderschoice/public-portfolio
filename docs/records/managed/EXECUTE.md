<!-- markdownlint-disable-file MD041 -->
<!-- AIエージェント専用実施記録ファイル（ユーザ編集禁止） -->
<!-- このファイルはAIエージェントがプロンプト指示の処理実行時のみ自動更新します。 -->
<!-- schema: records.execute.v1 -->

<!-- COPILOT_RECORDS:BEGIN -->
```yaml
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
