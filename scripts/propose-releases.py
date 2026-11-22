#!/usr/bin/env python3
"""README.md の掲載表の各 repo の最新リリースを調べ、RELEASES 表の置き換え案を出す（標準ライブラリのみ）。

使い方:
  python scripts/propose-releases.py                       # 公開 REST API から取得し、差分案を標準出力へ出す
  python scripts/propose-releases.py --apply               # 差分案どおりに README の RELEASES 表だけを書き換える
  python scripts/propose-releases.py --from-json FILE      # API 応答の保存ファイルを読む（ネットワークへ接続しない）

--from-json の形式: {"<repo 名>": <releases API の応答（配列）>, ...}。掲載表の全 repo のキーが必要。

終了コード: 0 = 正常（差分の有無を問わない）、2 = 不正な入力・取得失敗。
接続先は https://api.github.com 固定（資格情報・トークンは使わない。リダイレクト先も検証する）。
実 API を呼ぶのは、ユーザーが対話で更新を依頼したときに限る（自律ループ内では --from-json だけを使う）。
"""
import argparse
import datetime
import difflib
import json
import os
import re
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
BEGIN = "<!-- PORTFOLIO:BEGIN -->"
END = "<!-- PORTFOLIO:END -->"
REL_BEGIN = "<!-- RELEASES:BEGIN -->"
REL_END = "<!-- RELEASES:END -->"
REL_HEADER = ["名前", "最新リリース", "公開日", "種類"]
COLUMNS = ["名前", "説明", "種別", "プラットフォーム/言語", "repo", "Pages", "イラスト"]
OWNER = "filderschoice"
API_HOST = "api.github.com"
PER_PAGE = 5
TIMEOUT_SEC = 10
MAX_BYTES = 1024 * 1024
MAX_REDIRECTS = 3
USER_AGENT = "portfolio-release-proposer/1.0"
VERSION = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
DATE_TIME = re.compile(r"^(\d{4}-\d{2}-\d{2})T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
REPO_URL = re.compile(r"^https://github\.com/" + re.escape(OWNER) + r"/([A-Za-z0-9][A-Za-z0-9._-]*)$")


class ProposeError(Exception):
    pass


def split_row(line):
    line = line.strip()
    if not (line.startswith("|") and line.endswith("|")):
        raise ProposeError(f"表の行が | で始まり終わっていません: {line[:40]}")
    return [c.strip() for c in line[1:-1].split("|")]


def block_span(text, begin, end):
    if text.count(begin) != 1 or text.count(end) != 1:
        raise ProposeError(f"{begin} と {end} が1組ありません")
    start = text.index(begin) + len(begin)
    stop = text.index(end)
    if stop < start:
        raise ProposeError(f"{begin} のマーカーの順序が不正です")
    return start, stop


def parse_repos(text):
    """掲載表から [(名前, repo 名)] を返す。repo 列は https://github.com/filderschoice/<repo> の形のみ許す。"""
    start, stop = block_span(text, BEGIN, END)
    lines = [ln for ln in text[start:stop].splitlines() if ln.strip()]
    if len(lines) < 3 or split_row(lines[0]) != COLUMNS:
        raise ProposeError("掲載表の見出し・データ行が不正です")
    result = []
    for line in lines[2:]:
        cells = split_row(line)
        if len(cells) != len(COLUMNS):
            raise ProposeError(f"掲載表の列数が {len(COLUMNS)} ではありません: {line[:40]}")
        url = cells[4]
        if url.startswith("<") and url.endswith(">"):
            url = url[1:-1]
        m = REPO_URL.fullmatch(url)
        if not m:
            raise ProposeError(f"{cells[0]} の repo が https://github.com/{OWNER}/<repo> の形ではありません: {cells[4]!r}")
        result.append((cells[0], m.group(1)))
    names = [n for n, _ in result]
    if len(set(names)) != len(names):
        raise ProposeError("掲載表で名前が重複しています")
    return result


class _SafeRedirect(urllib.request.HTTPRedirectHandler):
    """リダイレクト先が https://api.github.com 以外なら追従しない。"""
    max_redirections = MAX_REDIRECTS

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parts = urlsplit(newurl)
        if parts.scheme != "https" or parts.hostname != API_HOST or parts.port not in (None, 443):
            raise ProposeError(f"api.github.com 以外へのリダイレクトは許可しません: {parts.scheme}://{parts.hostname}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(repo):
    url = f"https://{API_HOST}/repos/{OWNER}/{repo}/releases?per_page={PER_PAGE}"
    req = urllib.request.Request(url, method="GET", headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
    })
    opener = urllib.request.build_opener(_SafeRedirect)
    try:
        with opener.open(req, timeout=TIMEOUT_SEC) as resp:
            body = resp.read(MAX_BYTES + 1)
    except ProposeError:
        raise
    except (urllib.error.URLError, OSError, ValueError) as exc:
        raise ProposeError(f"{repo} の取得に失敗しました: {exc}")
    if len(body) > MAX_BYTES:
        raise ProposeError(f"{repo} の応答が上限 {MAX_BYTES} バイトを超えました")
    try:
        return json.loads(body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as exc:
        raise ProposeError(f"{repo} の応答が JSON ではありません: {exc}")


def pick_release(repo, data):
    """応答（配列）から (版, 公開日, 種類) または None（リリース無し）を返す。draft は除外する。"""
    if not isinstance(data, list):
        raise ProposeError(f"{repo} の応答が配列ではありません")
    if not data:
        return None
    for item in data:
        if not isinstance(item, dict):
            raise ProposeError(f"{repo} の応答に不正な要素があります")
        if item.get("draft") is True:
            continue
        tag = item.get("tag_name")
        if not isinstance(tag, str) or not VERSION.fullmatch(tag):
            raise ProposeError(f"{repo} の版が不正です（英数と . _ - のみ、先頭は英数）: {tag!r}")
        published = item.get("published_at")
        m = DATE_TIME.fullmatch(published) if isinstance(published, str) else None
        if not m:
            raise ProposeError(f"{repo} の公開日が ISO 8601 形式ではありません: {published!r}")
        try:
            datetime.date.fromisoformat(m.group(1))
        except ValueError:
            raise ProposeError(f"{repo} の公開日が実在しません: {published!r}")
        pre = item.get("prerelease")
        if not isinstance(pre, bool):
            raise ProposeError(f"{repo} の prerelease が真偽値ではありません: {pre!r}")
        return (tag, m.group(1), "プレリリース" if pre else "正式")
    raise ProposeError(f"{repo} の応答が draft だけで、採れるリリースがありません")


def load_saved(path, repos):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ProposeError(f"--from-json の読み込みに失敗しました: {exc}")
    if not isinstance(data, dict):
        raise ProposeError("--from-json の内容は {repo 名: 応答の配列} の JSON オブジェクトにしてください")
    known = set(repos)
    unknown = [k for k in data if k not in known]
    if unknown:
        raise ProposeError(f"--from-json に掲載表にない repo があります: {', '.join(map(str, unknown))}")
    missing = [r for r in repos if r not in data]
    if missing:
        raise ProposeError(f"--from-json に次の repo の応答がありません: {', '.join(missing)}")
    return data


def build_block(entries, results, nl):
    lines = ["| " + " | ".join(REL_HEADER) + " |", "| " + " | ".join("---" for _ in REL_HEADER) + " |"]
    for name, repo in entries:
        rel = results[repo]
        cells = [name, "-", "-", "-"] if rel is None else [name, *rel]
        lines.append("| " + " | ".join(cells) + " |")
    return nl + nl.join(lines) + nl


def write_atomic(path, text):
    """同じディレクトリの一時ファイルへ書いてから os.replace で置換する（失敗時は元のファイルを残す）。"""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".propose-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            f.write(text)
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def run(args):
    with open(README, encoding="utf-8", newline="") as f:
        text = f.read()
    nl = "\r\n" if "\r\n" in text else "\n"
    entries = parse_repos(text)
    repos = [r for _, r in entries]
    if args.from_json:
        saved = load_saved(args.from_json, repos)
        results = {r: pick_release(r, saved[r]) for r in repos}
    else:
        results = {r: pick_release(r, fetch(r)) for r in repos}
    start, stop = block_span(text, REL_BEGIN, REL_END)
    old_block = text[start:stop]
    new_block = build_block(entries, results, nl)
    if old_block == new_block:
        print("差分なし: RELEASES 表は最新リリースと一致しています")
        return 0
    diff = difflib.unified_diff(old_block.splitlines(), new_block.splitlines(),
                                "README.md (現在)", "README.md (案)", lineterm="")
    print("\n".join(diff))
    if not args.apply:
        print("\n上記は差分案です。反映するには --apply を付けて再実行してください")
        return 0
    write_atomic(README, text[:start] + new_block + text[stop:])
    print("README.md の RELEASES 表を更新しました。python scripts/build-pages.py と --check を実行してください")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--apply", action="store_true", help="差分案を README の RELEASES 表へ反映する")
    ap.add_argument("--from-json", metavar="FILE", help="API 応答の保存ファイルを読む（ネットワークへ接続しない）")
    args = ap.parse_args()
    try:
        return run(args)
    except (ProposeError, OSError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
