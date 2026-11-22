"""scripts/build-pages.py の検証（SVG 検査・表検証・生成と --check）。"""
import sys
import unittest
from unittest import mock

from helpers import GOOD_SVG, ROOT, SVG_NS, TempCase, load_script, readme_text

bp = load_script("build-pages.py")
NS = f'xmlns="{SVG_NS}"'
BS = chr(92)  # バックスラッシュ（CSS のエスケープの検査用）
ALPHA = "| alpha | 説明A | アプリ | Kotlin / Android | <{url}> | - | {ill} |"
ALPHA_ONLY_RELEASE = ["| alpha | - | - | - |"]


class SvgProblemTest(unittest.TestCase):
    def test_valid_svg_passes(self):
        self.assertIsNone(bp.svg_problem(GOOD_SVG))

    def test_all_repository_illustrations_pass(self):
        files = sorted((ROOT / "site" / "illustrations").glob("*.svg"))
        self.assertTrue(files)
        for path in files:
            with self.subTest(path.name):
                self.assertIsNone(bp.svg_problem(path.read_text(encoding="utf-8")))

    def test_description_text_is_not_a_false_positive(self):
        svg = f"<svg {NS}><title>t</title><desc>description と onload= と href の説明</desc></svg>"
        self.assertIsNone(bp.svg_problem(svg))

    def test_text_content_with_xmlns_is_not_a_false_positive(self):
        for body in ('xmlns="http://x"', "xmlns:xlink='http://www.w3.org/1999/xlink'"):
            with self.subTest(body):
                self.assertIsNone(bp.svg_problem(f"<svg {NS}><title>t</title><desc>{body}</desc></svg>"))

    def test_rejected_inputs(self):
        """各入力が、想定した検査の分岐（理由メッセージの識別子）で拒否されることまで確かめる。"""
        raw, nsdecl, parse, root = "SVG に使えない構文", "名前空間以外", "XML として解析", "ルート要素"
        elem, unknown, nsattr = "許可されていない要素", "許可されていない属性", "名前空間付きの属性"
        handler, link, value, style = "イベントハンドラ属性", "リンク属性", "の値に禁止", "style 要素に禁止"
        cases = {
            "script element": (f"<svg {NS}><script>1</script></svg>", elem),
            "foreignObject": (f"<svg {NS}><foreignObject/></svg>", elem),
            "a element": (f'<svg {NS}><a/></svg>', elem),
            "CDATA": (f"<svg {NS}><style><![CDATA[.a{{}}]]></style></svg>", raw),
            "DOCTYPE": (f"<!DOCTYPE svg><svg {NS}></svg>", raw),
            "ENTITY without DOCTYPE": (f'<!ENTITY a "b"><svg {NS}></svg>', raw),
            "ENTITY": (f'<!DOCTYPE svg [<!ENTITY a "b">]><svg {NS}>&a;</svg>', raw),
            "processing instruction": (f'<?xml version="1.0"?><svg {NS}></svg>', raw),
            "comment": (f"<svg {NS}><!-- c --></svg>", raw),
            "comment in text": (f"<svg {NS}><desc>a<!-- c -->b</desc></svg>", raw),
            "foreign default xmlns": ('<svg xmlns="http://evil.example/"></svg>', nsdecl),
            "xlink xmlns declaration": (
                f'<svg {NS} xmlns:xlink="http://www.w3.org/1999/xlink"><rect/></svg>', nsdecl),
            "prefixed svg xmlns": (f'<svg {NS} xmlns:s="{SVG_NS}"></svg>', nsdecl),
            "xmlns declared on a child": (f'<svg {NS}><g xmlns:x="http://x"/></svg>', nsdecl),
            "namespaced attribute (xml:lang)": (f'<svg {NS}><rect xml:lang="ja"/></svg>', nsattr),
            "namespaced href (xml:href)": (f'<svg {NS}><rect xml:href="x"/></svg>', nsattr),
            "onload on root": (f'<svg {NS} onload="alert(1)"></svg>', handler),
            "onclick on rect": (f'<svg {NS}><rect onclick="x"/></svg>', handler),
            "mixed-case OnLoad": (f'<svg {NS}><rect OnLoad="x"/></svg>', handler),
            "upper-case ONCLICK": (f'<svg {NS}><rect ONCLICK="x"/></svg>', handler),
            "href attribute": (f'<svg {NS}><rect href="x"/></svg>', link),
            "mixed-case Href": (f'<svg {NS}><rect Href="x"/></svg>', link),
            "unknown attribute": (f'<svg {NS}><rect fill="red"/></svg>', unknown),
            "attribute value with url": (f'<svg {NS}><rect style="fill:url(#a)"/></svg>', value),
            "attribute value url via character reference": (
                f'<svg {NS}><rect style="fill:u&#114;l(#a)"/></svg>', value),
            "attribute value javascript via character reference": (
                f'<svg {NS}><rect id="java&#115;cript:x"/></svg>', value),
            "style url": (f"<svg {NS}><style>.a{{fill:url(#x)}}</style></svg>", style),
            "style url with space": (f"<svg {NS}><style>.a{{fill:url (#x)}}</style></svg>", style),
            "style import": (f'<svg {NS}><style>@import "a.css";</style></svg>', style),
            "style other at-rule": (f"<svg {NS}><style>@font-face{{}}</style></svg>", style),
            "style escape": (f"<svg {NS}><style>.a{{fill:u{BS}72l(x)}}</style></svg>", style),
            "style expression": (f"<svg {NS}><style>.a{{width:expression(1)}}</style></svg>", style),
            "style comment": (f"<svg {NS}><style>.a{{fill:u/**/rl(x)}}</style></svg>", style),
            "not svg root": (f"<g {NS}></g>", root),
            "no namespace root": ("<svg></svg>", root),
            # XML として不正な入力は、解析の段階で拒否される（検査の各分岐には到達しない）
            "malformed (unclosed)": (f"<svg {NS}><rect></svg>", parse),
            "svg/onload (not well-formed)": (f"<svg/onload=alert(1) {NS}></svg>", parse),
            "character reference in tag name": (f"<svg {NS}><scr&#105;pt>x</scr&#105;pt></svg>", parse),
            "undeclared prefix (xlink:href)": (f'<svg {NS}><use xlink:href="#a"/></svg>', parse),
        }
        problems = {}
        for label, (svg, expected) in cases.items():
            with self.subTest(label):
                problem = bp.svg_problem(svg)
                self.assertTrue(problem, f"{label} が通ってしまった")
                self.assertIn(expected, problem, f"{label} が想定外の分岐で拒否された: {problem}")
                problems[label] = problem
        # 自己検査: 各分岐の期待文字列が、他の分岐のメッセージに含まれない（別の分岐で通る偽陽性を防ぐ）
        for label, (_, expected) in cases.items():
            for other, (_, other_expected) in cases.items():
                if expected != other_expected and label in problems and other in problems:
                    with self.subTest(f"{expected} not in {other}"):
                        self.assertNotIn(expected, problems[other])


class ReadmeParseTest(TempCase):
    def setUp(self):
        super().setUp()
        (self.tmp / "alpha.svg").write_text(GOOD_SVG, encoding="utf-8")
        patcher = mock.patch.object(bp, "ILLUSTRATIONS", self.tmp)
        patcher.start()
        self.addCleanup(patcher.stop)

    def parse(self, **kw):
        return bp.parse_readme(readme_text(**kw))

    def assert_error(self, **kw):
        with self.assertRaises(bp.BuildError):
            self.parse(**kw)

    def test_valid(self):
        items = self.parse()
        self.assertEqual([i["name"] for i in items], ["alpha", "beta"])
        self.assertIsNone(items[0]["release"])

    def test_duplicate_name_in_portfolio(self):
        row = ALPHA.format(url="https://github.com/filderschoice/alpha", ill="alpha")
        self.assert_error(portfolio_rows=[row, row], release_rows=ALPHA_ONLY_RELEASE)

    def test_repo_url_must_not_have_query_fragment_or_space(self):
        for suffix in ("?x=1", "#a", " x"):
            row = ALPHA.format(url="https://github.com/filderschoice/alpha" + suffix, ill="alpha")
            with self.subTest(suffix):
                self.assert_error(portfolio_rows=[row], release_rows=ALPHA_ONLY_RELEASE)

    def test_non_https_url(self):
        row = ALPHA.format(url="http://github.com/filderschoice/alpha", ill="alpha")
        self.assert_error(portfolio_rows=[row], release_rows=ALPHA_ONLY_RELEASE)

    def test_illustration_must_exist(self):
        row = ALPHA.format(url="https://github.com/filderschoice/alpha", ill="missing")
        self.assert_error(portfolio_rows=[row], release_rows=ALPHA_ONLY_RELEASE)

    def test_release_with_plus_in_version(self):
        rows = ["| alpha | v1.2.0+build.5 | 2026-10-15 | 正式 |", "| beta | - | - | - |"]
        items = self.parse(release_rows=rows)
        self.assertEqual(items[0]["release"], ("v1.2.0+build.5", "2026-10-15", "正式"))
        self.assertIn("v1.2.0%2Bbuild.5", bp.release_html(items[0]))

    def test_invalid_release_rows(self):
        dash_beta = "| beta | - | - | - |"
        bad_rows = {
            "missing row": ALPHA_ONLY_RELEASE,
            "duplicate": ["| alpha | - | - | - |", "| alpha | - | - | - |", dash_beta],
            "unknown name": ["| alpha | - | - | - |", dash_beta, "| gamma | - | - | - |"],
            "bad version": ["| alpha | v 1 | 2026-10-15 | 正式 |", dash_beta],
            "version starts with symbol": ["| alpha | -v1 | 2026-10-15 | 正式 |", dash_beta],
            "bad date format": ["| alpha | v1 | 2026/10/15 | 正式 |", dash_beta],
            "nonexistent date": ["| alpha | v1 | 2026-02-30 | 正式 |", dash_beta],
            "bad kind": ["| alpha | v1 | 2026-10-15 | 不明 |", dash_beta],
            "dash version with date": ["| alpha | - | 2026-10-15 | - |", dash_beta],
            "wrong column count": ["| alpha | v1 | 2026-10-15 |", dash_beta],
        }
        for label, rows in bad_rows.items():
            with self.subTest(label):
                self.assert_error(release_rows=rows)

    def test_missing_marker(self):
        with self.assertRaises(bp.BuildError):
            bp.parse_readme(readme_text().replace("<!-- PORTFOLIO:END -->", ""))


class MainCheckTest(TempCase):
    def setUp(self):
        super().setUp()
        (self.tmp / "illustrations").mkdir()
        (self.tmp / "illustrations" / "alpha.svg").write_text(GOOD_SVG, encoding="utf-8")
        self.readme = self.tmp / "README.md"
        self.output = self.tmp / "site" / "index.html"
        self.readme.write_text(readme_text(), encoding="utf-8", newline="")
        for name, value in (("README", self.readme), ("OUTPUT", self.output),
                            ("ILLUSTRATIONS", self.tmp / "illustrations"), ("ROOT", self.tmp)):
            patcher = mock.patch.object(bp, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def run_main(self, *args):
        with mock.patch.object(sys, "argv", ["build-pages.py", *args]):
            return self.call(bp.main)

    def test_generate_is_idempotent_and_check_passes(self):
        self.assertEqual(self.run_main()[0], 0)
        first = self.output.read_bytes()
        self.assertEqual(self.run_main()[0], 0)
        self.assertEqual(self.output.read_bytes(), first)
        self.assertEqual(self.run_main("--check")[0], 0)

    def test_generated_page_has_strict_csp(self):
        self.run_main()
        page = self.output.read_text(encoding="utf-8")
        for token in ("img-src &#x27;self&#x27;", "base-uri &#x27;none&#x27;", "form-action &#x27;none&#x27;"):
            self.assertIn(token, page)

    def test_check_fails_when_output_differs_or_missing(self):
        self.assertEqual(self.run_main("--check")[0], 1)  # 生成物が無い
        self.run_main()
        self.output.write_text("changed", encoding="utf-8")
        self.assertEqual(self.run_main("--check")[0], 1)

    def test_invalid_readme_exits_with_2(self):
        self.readme.write_text(readme_text().replace("アプリ", "不明"), encoding="utf-8", newline="")
        self.assertEqual(self.run_main()[0], 2)
        self.assertFalse(self.output.exists())


if __name__ == "__main__":
    unittest.main()
