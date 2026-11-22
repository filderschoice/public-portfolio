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
        "<title>公開ポートフォリオ</title>",
        "</head>",
        "<body>",
        "<h1>公開ポートフォリオ</h1>",
        "<p>filderschoice が公開しているアプリ・ツールの一覧です。詳細は各リポジトリを参照してください。</p>",
        "<ul>",
    ]
    for it in items:
        links = f'<a href="{e(it["repo"])}">repo</a>'
        if it["pages"]:
            links += f' / <a href="{e(it["pages"])}">Pages</a>'
        out += [
            "<li>",
            f"<h2>{e(it['name'])}</h2>",
            f"<p>{e(it['kind'])} / {e(it['platform'])}</p>",
            f"<p>{e(it['desc'])}</p>",
            f"<p>{links}</p>",
            "</li>",
        ]
    out += ["</ul>", "</body>", "</html>", ""]
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
