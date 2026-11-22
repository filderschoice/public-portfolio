#!/usr/bin/env python3
"""README.md の掲載表から公開用の静的ページ site/index.html を生成する（標準ライブラリのみ）。

使い方:
  python scripts/build-pages.py          # site/index.html を生成する
  python scripts/build-pages.py --check  # 生成物が README と一致するか確認する（一致 0・不一致 1）

不正な入力（マーカー欠落・必須列の欠落・https 以外のリンク等）は終了コード2で停止する。
"""
import argparse
import datetime
import html
import io
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUTPUT = ROOT / "site" / "index.html"
ILLUSTRATIONS = ROOT / "site" / "illustrations"
BEGIN = "<!-- PORTFOLIO:BEGIN -->"
END = "<!-- PORTFOLIO:END -->"
REL_BEGIN = "<!-- RELEASES:BEGIN -->"
REL_END = "<!-- RELEASES:END -->"
REL_COLUMNS = ["名前", "最新リリース", "公開日", "種類"]
REL_KINDS = ("正式", "プレリリース")
VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]*$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
COLUMNS = ["名前", "説明", "種別", "プラットフォーム/言語", "repo", "Pages", "イラスト"]
KINDS = ("アプリ", "ツール")
ILLUSTRATION_ID = re.compile(r"^[A-Za-z0-9-]+$")
SVG_NS = "http://www.w3.org/2000/svg"
# SVG は XML として解析して検査する。要素・属性は許可リスト方式（現行の固定資産に必要な最小限）
SVG_ELEMENTS = {"svg", "title", "desc", "defs", "style", "g", "rect", "circle", "ellipse", "line", "path",
                "polygon", "polyline", "text", "tspan"}
SVG_ATTRIBUTES = {"class", "id", "style", "viewBox", "role", "aria-labelledby", "transform", "text-anchor",
                  "x", "y", "width", "height", "rx", "ry", "cx", "cy", "r", "x1", "y1", "x2", "y2", "d", "points"}
# 解析前の生の文字列で禁止するもの: DOCTYPE・ENTITY・処理命令（XML 宣言を含む）・CDATA・XML コメント
# （コメントは ElementTree が黙って捨てて検査できないため、生の文字列で拒否する）。名前空間の宣言は解析時に検査する
SVG_RAW_FORBIDDEN = re.compile(r"<!\s*(?:doctype|entity)|<\?|<!\[cdata\[|<!--", re.IGNORECASE)
# 解析後の属性値・style 要素の中身に禁止するもの（実体参照・文字参照は解析で解決済みの値を検査する）
SVG_VALUE_FORBIDDEN = re.compile(r"url\s*\(|@(?!media\b)|[\\]|expression|javascript:|/\*", re.IGNORECASE)
ILLUSTRATION_SIZE = (400, 300)
# 外部資源を読まない方針の機械的な担保。style はインライン埋め込みのため unsafe-inline のみ許可する
CSP = "default-src 'none'; img-src 'self'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"

CSS = """
:root{color-scheme:light dark;--bg:#f6f8fa;--card:#fff;--text:#1f2328;--muted:#57606a;--border:#d0d7de;
--link:#0550ae;--ill-bg:#eaeef2;--app-bg:#ddf4ff;--app-fg:#0a3069;--tool-bg:#fff1d6;--tool-fg:#5c3d00}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--muted:#9da7b3;
--border:#30363d;--ill-bg:#0d1117;--link:#79c0ff;--app-bg:#10304f;--app-fg:#cae8ff;--tool-bg:#3a2a07;--tool-fg:#ffe0a3}}
*{box-sizing:border-box}
body{margin:0;padding:1.5rem 1rem;background:var(--bg);color:var(--text);
font-family:system-ui,-apple-system,"Segoe UI","Hiragino Sans","Yu Gothic",sans-serif;line-height:1.6}
main{max-width:64rem;margin:0 auto}
h1{font-size:1.6rem;margin:0 0 .5rem}
.lead{color:var(--muted);margin:0 0 1.5rem}
.cards{list-style:none;margin:0;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(2,minmax(0,1fr))}
.card{background:var(--card);border:1px solid var(--border);border-radius:.75rem;padding:1rem 1.25rem;
display:flex;flex-direction:column;gap:.5rem;overflow-wrap:anywhere}
.illust{margin:0;border:1px solid var(--border);border-radius:.5rem;background:var(--ill-bg);overflow:hidden}
.illust img{display:block;width:100%;height:auto}
.note{color:var(--muted);font-size:.8rem}
.release{color:var(--muted);font-size:.9rem}
.card h2{font-size:1.2rem;margin:0}
.card p{margin:0}
.meta{display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;color:var(--muted);font-size:.9rem}
.badge{display:inline-block;padding:.1rem .6rem;border-radius:999px;font-weight:700;font-size:.85rem}
.badge-app{background:var(--app-bg);color:var(--app-fg)}
.badge-tool{background:var(--tool-bg);color:var(--tool-fg)}
.links{margin-top:auto;display:flex;flex-wrap:wrap;gap:1rem}
a{color:var(--link)}
@media (max-width:40rem){.cards{grid-template-columns:minmax(0,1fr)}}
"""
KIND_CLASS = {"アプリ": "badge-app", "ツール": "badge-tool"}


class BuildError(Exception):
    pass


def split_row(line):
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        raise BuildError(f"表の行が | で始まり終わっていません: {line[:40]}")
    return [c.strip() for c in line[1:-1].split("|")]


def parse_url(value, label):
    url = value.strip()
    if url.startswith("<") and url.endswith(">"):
        url = url[1:-1]
    parts = urlsplit(url)
    if parts.scheme != "https" or not parts.netloc:
        raise BuildError(f"{label} は https の URL だけを指定できます: {value!r}")
    if parts.query or parts.fragment or "?" in url or "#" in url or re.search(r"[\s\x00-\x1f\x7f]", url):
        raise BuildError(f"{label} に ?・#・空白・制御文字を含められません: {value!r}")
    return url


def svg_problem(text):
    """SVG を XML として解析して検査し、問題の説明（無ければ None）を返す。"""
    found = SVG_RAW_FORBIDDEN.search(text)
    if found:
        return f"禁止された記述 {found.group()!r}（DOCTYPE・ENTITY・処理命令・CDATA・コメント）があります"
    root = None
    try:
        for event, data in ET.iterparse(io.BytesIO(text.encode("utf-8")), events=("start-ns", "start")):
            if event == "start-ns":
                prefix, uri = data
                # 宣言された名前空間は、接頭辞なしの SVG の名前空間だけを許可する（xlink 等は許可しない）
                if prefix != "" or uri != SVG_NS:
                    return "SVG の名前空間以外の名前空間（xmlns:接頭辞 を含む）は宣言できません"
            elif root is None:
                root = data
    except ET.ParseError as exc:
        return f"XML として解析できません: {exc}"
    if root.tag != f"{{{SVG_NS}}}svg":
        return "ルート要素が SVG の svg ではありません"
    for el in root.iter():
        ns, _, local = el.tag.partition("}")
        if ns != "{" + SVG_NS or local not in SVG_ELEMENTS:
            return f"許可されていない要素 {el.tag!r} があります"
        for key, val in el.attrib.items():
            low = key.lower()
            # 名前空間付きの属性は、宣言できる名前空間が SVG のみのため xml:lang など暗黙の xml 接頭辞でだけ到達する
            if "}" in key:
                return f"名前空間付きの属性 {key!r} は使えません"
            if low.startswith("on"):
                return f"イベントハンドラ属性 {key!r} は使えません"
            if "href" in low:
                return f"リンク属性 {key!r} は使えません"
            if key not in SVG_ATTRIBUTES:
                return f"許可されていない属性 {key!r} があります"
            if SVG_VALUE_FORBIDDEN.search(val):
                return f"属性 {key!r} の値に禁止された記述があります"
        if local == "style":
            body = "".join(el.itertext())
            if SVG_VALUE_FORBIDDEN.search(body):
                return "style 要素に禁止された記述（url(・@import・エスケープ・expression 等）があります"
    return None


def check_illustration(value, name):
    """イラスト列の値（SVG の ID）を検証し、固定資産 site/illustrations/<ID>.svg を確認する。"""
    if not ILLUSTRATION_ID.fullmatch(value):
        raise BuildError(f"{name} のイラストは英数字とハイフンの ID か - だけを指定できます: {value!r}")
    path = ILLUSTRATIONS / f"{value}.svg"
    if not path.is_file():
        raise BuildError(f"{name} のイラスト site/illustrations/{value}.svg がありません")
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        raise BuildError(f"{name} のイラストを読めません: {exc}")
    problem = svg_problem(text)
    if problem:
        raise BuildError(f"{name} のイラスト {value}.svg が不正です: {problem}")
    return value


def table_lines(text, begin, end):
    if text.count(begin) != 1 or text.count(end) != 1:
        raise BuildError(f"{begin} と {end} が1組ありません")
    start = text.index(begin) + len(begin)
    stop = text.index(end)
    if stop < start:
        raise BuildError(f"{begin} のマーカーの順序が不正です")
    return [ln for ln in text[start:stop].splitlines() if ln.strip()]


def parse_releases(text, names):
    """最新リリース表を検証し、{名前: (版, 公開日, 種類) または None} を返す。"""
    lines = table_lines(text, REL_BEGIN, REL_END)
    if len(lines) < 3:
        raise BuildError("最新リリース表に見出し・区切り・データ行がありません")
    if split_row(lines[0]) != REL_COLUMNS:
        raise BuildError(f"最新リリース表の見出しが {' | '.join(REL_COLUMNS)} と一致しません")
    result = {}
    for line in lines[2:]:
        cells = split_row(line)
        if len(cells) != len(REL_COLUMNS):
            raise BuildError(f"最新リリース表の列数が {len(REL_COLUMNS)} ではありません: {line[:40]}")
        name, ver, day, kind = cells
        if name not in names:
            raise BuildError(f"最新リリース表に掲載表にない名前があります: {name!r}")
        if name in result:
            raise BuildError(f"最新リリース表で名前が重複しています: {name}")
        if ver == "-":
            if day != "-" or kind != "-":
                raise BuildError(f"{name} は版が - のとき公開日・種類も - にしてください")
            result[name] = None
            continue
        if not VERSION.fullmatch(ver):
            raise BuildError(f"{name} の版が不正です（英数と . _ - のみ、先頭は英数）: {ver!r}")
        if not DATE.fullmatch(day):
            raise BuildError(f"{name} の公開日は YYYY-MM-DD で指定してください: {day!r}")
        try:
            datetime.date.fromisoformat(day)
        except ValueError:
            raise BuildError(f"{name} の公開日が実在しません: {day!r}")
        if kind not in REL_KINDS:
            raise BuildError(f"{name} の種類は {' / '.join(REL_KINDS)} のいずれかです: {kind!r}")
        result[name] = (ver, day, kind)
    missing = [n for n in names if n not in result]
    if missing:
        raise BuildError(f"最新リリース表に行がない名前があります: {', '.join(missing)}")
    return result


def parse_readme(text):
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise BuildError(f"{BEGIN} と {END} が1組ありません")
    start = text.index(BEGIN) + len(BEGIN)
    stop = text.index(END)
    if stop < start:
        raise BuildError("掲載表のマーカーの順序が不正です")
    lines = [ln for ln in text[start:stop].splitlines() if ln.strip()]
    if len(lines) < 3:
        raise BuildError("掲載表に見出し・区切り・データ行がありません")
    if split_row(lines[0]) != COLUMNS:
        raise BuildError(f"表の見出しが {' | '.join(COLUMNS)} と一致しません")
    items = []
    for line in lines[2:]:
        cells = split_row(line)
        if len(cells) != len(COLUMNS):
            raise BuildError(f"列数が {len(COLUMNS)} ではありません: {line[:40]}")
        name, desc, kind, platform, repo, pages, illust = cells
        if not name or not desc or not platform:
            raise BuildError(f"空の必須セルがあります: {name or line[:40]}")
        if kind not in KINDS:
            raise BuildError(f"種別は {' / '.join(KINDS)} のいずれかです: {kind!r}")
        items.append({
            "name": name,
            "desc": desc,
            "kind": kind,
            "platform": platform,
            "repo": parse_url(repo, f"{name} の repo"),
            "pages": None if pages == "-" else parse_url(pages, f"{name} の Pages"),
            "illust": None if illust == "-" else check_illustration(illust, name),
        })
    names = [it["name"] for it in items]
    if len(set(names)) != len(names):
        raise BuildError("掲載表で名前が重複しています")
    releases = parse_releases(text, names)
    for it in items:
        it["release"] = releases[it["name"]]
    return items


def release_html(it):
    e = html.escape
    if not it["release"]:
        return '<p class="release">最新リリース -</p>'
    ver, day, kind = it["release"]
    url = f"{it['repo'].rstrip('/')}/releases/tag/{quote(ver, safe='')}"
    return (f'<p class="release">最新リリース <a href="{e(url)}">{e(ver)}</a>'
            f"（{e(day)}・{e(kind)}）</p>")


def render(items):
    e = html.escape
    out = [
        "<!DOCTYPE html>",
        '<html lang="ja">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="color-scheme" content="light dark">',
        f'<meta http-equiv="Content-Security-Policy" content="{e(CSP)}">',
        "<title>公開ポートフォリオ</title>",
        "<style>" + CSS + "</style>",
        "</head>",
        "<body>",
        "<main>",
        "<h1>公開ポートフォリオ</h1>",
        '<p class="lead">filderschoice が公開しているアプリ・ツールの一覧です。詳細は各リポジトリを参照してください。'
        "掲載のイラストは内容をイメージしやすくするための模式図で、実際の画面ではありません。</p>",
        '<ul class="cards">',
    ]
    for it in items:
        links = f'<a href="{e(it["repo"])}">repo</a>'
        if it["pages"]:
            links += f'<a href="{e(it["pages"])}">Pages</a>'
        out.append('<li class="card">')
        if it["illust"]:
            w, h = ILLUSTRATION_SIZE
            alt = f"{it['name']} の画面イメージ（簡易イラスト。実際の画面ではありません）"
            out += [
                f'<div class="illust"><img src="illustrations/{e(it["illust"])}.svg" alt="{e(alt)}" '
                f'width="{w}" height="{h}"></div>',
                '<p class="note">イメージ図。実際の画面ではありません</p>',
            ]
        out += [
            f"<h2>{e(it['name'])}</h2>",
            f'<div class="meta"><span class="badge {KIND_CLASS[it["kind"]]}">{e(it["kind"])}</span>'
            f"<span>{e(it['platform'])}</span></div>",
            f"<p>{e(it['desc'])}</p>",
            release_html(it),
            f'<div class="links">{links}</div>',
            "</li>",
        ]
    out += ["</ul>", "</main>", "</body>", "</html>", ""]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="生成物が README と一致するか確認する")
    args = ap.parse_args()
    try:
        content = render(parse_readme(README.read_text(encoding="utf-8")))
    except (BuildError, OSError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 2
    data = content.encode("utf-8")
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != data:
            print("site/index.html が README.md と一致しません。python scripts/build-pages.py を実行してください",
                  file=sys.stderr)
            return 1
        print("site/index.html は README.md と一致しています")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(data)
    print(f"生成しました: {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
