"""scripts/ 配下のスクリプトを読み込む共通処理と、テスト用の README・SVG の雛形。

ネットワークへは接続せず、書き込みは一時ディレクトリだけに行う（リポジトリのファイルは変えない）。
"""
import contextlib
import importlib.util
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
SVG_NS = "http://www.w3.org/2000/svg"
GOOD_SVG = (f'<svg xmlns="{SVG_NS}" viewBox="0 0 400 300"><title>t</title><desc>d</desc>'
            '<style>.a{fill:#000}@media (prefers-color-scheme:dark){.a{fill:#fff}}</style>'
            '<rect class="a" x="0" y="0" width="10" height="10"/></svg>')


def load_script(filename):
    spec = importlib.util.spec_from_file_location(filename.replace("-", "_").removesuffix(".py"),
                                                  ROOT / "scripts" / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def readme_text(portfolio_rows=None, release_rows=None, nl="\n"):
    """掲載表と最新リリース表を持つ最小の README 本文を返す。"""
    p_rows = portfolio_rows or [
        "| alpha | 説明A | アプリ | Kotlin / Android | <https://github.com/filderschoice/alpha> | - | alpha | 2026-01-02 |",
        "| beta | 説明B | ツール | PowerShell / Windows | <https://github.com/filderschoice/beta> "
        "| <https://filderschoice.github.io/beta/> | - | - |",
    ]
    r_rows = release_rows or ["| alpha | - | - | - |", "| beta | - | - | - |"]
    lines = ["# 見出し", "", "<!-- PORTFOLIO:BEGIN -->",
             "| 名前 | 説明 | 種別 | プラットフォーム/言語 | repo | Pages | イラスト | 初回公開日 |",
             "| --- | --- | --- | --- | --- | --- | --- | --- |", *p_rows, "<!-- PORTFOLIO:END -->", "",
             "本文", "", "<!-- RELEASES:BEGIN -->", "| 名前 | 最新リリース | 公開日 | 種類 |", "| --- | --- | --- | --- |",
             *r_rows, "<!-- RELEASES:END -->", "", "末尾", ""]
    return nl.join(lines)


class TempCase(unittest.TestCase):
    """一時ディレクトリ（self.tmp）を用意し、標準出力・標準エラーを捕捉する補助つきの基底クラス。"""

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.addCleanup(self._td.cleanup)
        self.tmp = Path(self._td.name)

    def call(self, func, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                code = func(*args)
            except SystemExit as exc:  # argparse の終了
                code = exc.code
        return code, out.getvalue(), err.getvalue()
