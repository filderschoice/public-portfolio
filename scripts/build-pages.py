#!/usr/bin/env python3
"""README.md の掲載表から公開用の静的ページ site/index.html を生成する（標準ライブラリのみ）。

使い方:
  python scripts/build-pages.py          # site/index.html を生成する
  python scripts/build-pages.py --check  # 生成物が README と一致するか確認する（一致 0・不一致 1）

不正な入力（マーカー欠落・必須列の欠落・https 以外のリンク等）は終了コード2で停止する。
"""
import argparse
import html
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OUTPUT = ROOT / "site" / "index.html"
BEGIN = "<!-- PORTFOLIO:BEGIN -->"
END = "<!-- PORTFOLIO:END -->"
COLUMNS = ["名前", "説明", "種別", "プラットフォーム/言語", "repo", "Pages"]
KINDS = ("アプリ", "ツール")

CSS = """
:root{color-scheme:light dark;--bg:#f6f8fa;--card:#fff;--text:#1f2328;--muted:#57606a;--border:#d0d7de;
--link:#0550ae;--app-bg:#ddf4ff;--app-fg:#0a3069;--tool-bg:#fff1d6;--tool-fg:#5c3d00}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--muted:#9da7b3;
--border:#30363d;--link:#79c0ff;--app-bg:#10304f;--app-fg:#cae8ff;--tool-bg:#3a2a07;--tool-fg:#ffe0a3}}
*{box-sizing:border-box}
body{margin:0;padding:1.5rem 1rem;background:var(--bg);color:var(--text);
font-family:system-ui,-apple-system,"Segoe UI","Hiragino Sans","Yu Gothic",sans-serif;line-height:1.6}
main{max-width:64rem;margin:0 auto}
h1{font-size:1.6rem;margin:0 0 .5rem}
.lead{color:var(--muted);margin:0 0 1.5rem}
.cards{list-style:none;margin:0;padding:0;display:grid;gap:1rem;grid-template-columns:repeat(2,minmax(0,1fr))}
.card{background:var(--card);border:1px solid var(--border);border-radius:.75rem;padding:1rem 1.25rem;
display:flex;flex-direction:column;gap:.5rem;overflow-wrap:anywhere}
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
    return url


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
        name, desc, kind, platform, repo, pages = cells
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
        })
    return items


def render(items):
    e = html.escape
    out = [
        "<!DOCTYPE html>",
        '<html lang="ja">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<meta name="color-scheme" content="light dark">',
        "<title>公開ポートフォリオ</title>",
        "<style>" + CSS + "</style>",
        "</head>",
        "<body>",
        "<main>",
        "<h1>公開ポートフォリオ</h1>",
        '<p class="lead">filderschoice が公開しているアプリ・ツールの一覧です。詳細は各リポジトリを参照してください。</p>',
        '<ul class="cards">',
    ]
    for it in items:
        links = f'<a href="{e(it["repo"])}">repo</a>'
        if it["pages"]:
            links += f'<a href="{e(it["pages"])}">Pages</a>'
        out += [
            '<li class="card">',
            f"<h2>{e(it['name'])}</h2>",
            f'<div class="meta"><span class="badge {KIND_CLASS[it["kind"]]}">{e(it["kind"])}</span>'
            f"<span>{e(it['platform'])}</span></div>",
            f"<p>{e(it['desc'])}</p>",
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
