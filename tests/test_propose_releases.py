"""scripts/propose-releases.py の検証（検証・--from-json・--apply・リダイレクト・--live なしで接続しないこと）。

ネットワークへは接続しない。接続する経路（fetch・opener）はすべて mock に差し替える。
"""
import json
import os
import sys
import unittest
import urllib.request
from unittest import mock

from helpers import TempCase, load_script, readme_text

pr = load_script("propose-releases.py")


def rel(tag, pre=False, draft=False, pub="2026-11-21T10:00:00Z"):
    return {"tag_name": tag, "prerelease": pre, "draft": draft, "published_at": pub}


GOOD = {
    "alpha": [rel("v0.18.0", pre=True), rel("v0.17.0", pre=True)],
    "beta": [rel("v9", draft=True, pub=None), rel("v1.0.0+5", pub="2026-01-02T03:04:05+09:00")],
}


class PickReleaseTest(unittest.TestCase):
    def test_first_non_draft_with_prerelease_flag(self):
        self.assertEqual(pr.pick_release("a", GOOD["alpha"]), ("v0.18.0", "2026-11-21", "プレリリース"))

    def test_draft_is_skipped_and_plus_version_allowed(self):
        self.assertEqual(pr.pick_release("b", GOOD["beta"]), ("v1.0.0+5", "2026-01-02", "正式"))

    def test_empty_means_no_release(self):
        self.assertIsNone(pr.pick_release("a", []))

    def test_invalid_responses(self):
        cases = {
            "not a list": {"a": 1},
            "draft only": [rel("v1", draft=True)],
            "bad version chars": [rel("v 1")],
            "version starts with symbol": [rel("-x")],
            "date not ISO": [rel("v1", pub="2026-10-15")],
            "date not real": [rel("v1", pub="2026-13-40T00:00:00Z")],
            "missing date": [rel("v1", pub=None)],
            "prerelease not bool": [{"tag_name": "v1", "prerelease": "yes", "draft": False,
                                     "published_at": "2026-01-01T00:00:00Z"}],
            "element not object": ["v1"],
        }
        for label, data in cases.items():
            with self.subTest(label):
                with self.assertRaises(pr.ProposeError):
                    pr.pick_release("a", data)


class ParseReposTest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(pr.parse_repos(readme_text()), [("alpha", "alpha"), ("beta", "beta")])

    def test_rejects_other_owner_and_odd_urls(self):
        for url in ("https://github.com/other/alpha", "http://github.com/filderschoice/alpha",
                    "https://github.com/filderschoice/alpha?x=1", "https://github.com/filderschoice/alpha/x",
                    "https://example.com/filderschoice/alpha"):
            row = f"| alpha | 説明A | アプリ | Kotlin / Android | <{url}> | - | - | - |"
            with self.subTest(url):
                with self.assertRaises(pr.ProposeError):
                    pr.parse_repos(readme_text(portfolio_rows=[row], release_rows=["| alpha | - | - | - |"]))


class RunTest(TempCase):
    def setUp(self):
        super().setUp()
        self.readme = self.tmp / "README.md"
        self.write_readme(readme_text())
        patcher = mock.patch.object(pr, "README", self.readme)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.saved = self.tmp / "saved.json"
        self.save(GOOD)

    def write_readme(self, text):
        self.readme.write_bytes(text.encode("utf-8"))

    def save(self, obj):
        self.saved.write_text(json.dumps(obj), encoding="utf-8")

    def run_main(self, *args):
        with mock.patch.object(sys, "argv", ["propose-releases.py", *args]):
            return self.call(pr.main)

    def test_proposal_without_apply_does_not_change_readme(self):
        before = self.readme.read_bytes()
        code, out, _ = self.run_main("--from-json", str(self.saved))
        self.assertEqual(code, 0)
        self.assertIn("+| alpha | v0.18.0 | 2026-11-21 | プレリリース |", out)
        self.assertEqual(self.readme.read_bytes(), before)

    def test_apply_changes_only_releases_table_and_is_idempotent(self):
        before = self.readme.read_text(encoding="utf-8")
        self.assertEqual(self.run_main("--from-json", str(self.saved), "--apply")[0], 0)
        after = self.readme.read_text(encoding="utf-8")
        head_b, rest_b = before.split("<!-- RELEASES:BEGIN -->")
        head_a, rest_a = after.split("<!-- RELEASES:BEGIN -->")
        self.assertEqual(head_a, head_b)
        self.assertEqual(rest_a.split("<!-- RELEASES:END -->")[1], rest_b.split("<!-- RELEASES:END -->")[1])
        self.assertIn("| beta | v1.0.0+5 | 2026-01-02 | 正式 |", after)
        code, out, _ = self.run_main("--from-json", str(self.saved), "--apply")
        self.assertEqual((code, self.readme.read_text(encoding="utf-8")), (0, after))
        self.assertIn("差分なし", out)

    def test_apply_keeps_crlf(self):
        self.write_readme(readme_text(nl="\r\n"))
        self.assertEqual(self.run_main("--from-json", str(self.saved), "--apply")[0], 0)
        data = self.readme.read_bytes()
        self.assertEqual(data.count(b"\r\n"), data.count(b"\n"))
        self.assertIn(b"v0.18.0", data)

    def test_no_release_becomes_dashes(self):
        self.save({**GOOD, "beta": []})
        self.run_main("--from-json", str(self.saved), "--apply")
        self.assertIn("| beta | - | - | - |", self.readme.read_text(encoding="utf-8"))

    def test_invalid_inputs_exit_2_and_keep_readme(self):
        before = self.readme.read_bytes()
        cases = {
            "invalid json": "{bad",
            "top-level array": "[]",
            "unknown repo": json.dumps({**GOOD, "zzz": []}),
            "missing repo": json.dumps({"alpha": GOOD["alpha"]}),
            "response not array": json.dumps({**GOOD, "beta": {"a": 1}}),
            "bad version": json.dumps({**GOOD, "beta": [rel("v 1")]}),
            "bad date": json.dumps({**GOOD, "beta": [rel("v1", pub="2026-13-40T00:00:00Z")]}),
            "draft only": json.dumps({**GOOD, "beta": [rel("v1", draft=True)]}),
        }
        for label, raw in cases.items():
            with self.subTest(label):
                self.saved.write_text(raw, encoding="utf-8")
                self.assertEqual(self.run_main("--from-json", str(self.saved), "--apply")[0], 2)
                self.assertEqual(self.readme.read_bytes(), before)
        self.assertEqual(self.run_main("--from-json", str(self.tmp / "nothing.json"))[0], 2)

    def test_non_owner_repo_in_readme_exits_2(self):
        row = "| alpha | 説明A | アプリ | Kotlin / Android | <https://github.com/other/alpha> | - | - | - |"
        self.write_readme(readme_text(portfolio_rows=[row], release_rows=["| alpha | - | - | - |"]))
        self.save({"alpha": []})
        self.assertEqual(self.run_main("--from-json", str(self.saved))[0], 2)

    def test_failed_replace_keeps_readme_and_leaves_no_temp_file(self):
        before = self.readme.read_bytes()
        with mock.patch.object(pr.os, "replace", side_effect=OSError("boom")):
            code, _, _ = self.run_main("--from-json", str(self.saved), "--apply")
        self.assertEqual(code, 2)
        self.assertEqual(self.readme.read_bytes(), before)
        self.assertEqual(sorted(p.name for p in self.tmp.iterdir()), ["README.md", "saved.json"])


class NetworkSafetyTest(TempCase):
    """接続しないこと・接続先とヘッダーの制約。実際の接続は mock で防ぐ。"""

    def setUp(self):
        super().setUp()
        self.readme = self.tmp / "README.md"
        self.readme.write_bytes(readme_text().encode("utf-8"))
        patcher = mock.patch.object(pr, "README", self.readme)
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_main(self, *args):
        with mock.patch.object(sys, "argv", ["propose-releases.py", *args]):
            return self.call(pr.main)

    def test_no_arguments_does_not_connect_and_exits_2(self):
        with mock.patch.object(pr, "fetch", side_effect=AssertionError("接続した")) as fetch, \
                mock.patch.object(urllib.request, "build_opener", side_effect=AssertionError("接続した")):
            code, _, err = self.run_main()
        self.assertEqual(code, 2)
        fetch.assert_not_called()
        self.assertIn("--live", err)

    def test_from_json_does_not_connect(self):
        saved = self.tmp / "s.json"
        saved.write_text(json.dumps({"alpha": [], "beta": []}), encoding="utf-8")
        with mock.patch.object(pr, "fetch", side_effect=AssertionError("接続した")), \
                mock.patch.object(urllib.request, "build_opener", side_effect=AssertionError("接続した")):
            self.assertEqual(self.run_main("--from-json", str(saved))[0], 0)

    def test_live_and_from_json_are_exclusive(self):
        with mock.patch.object(pr, "fetch", side_effect=AssertionError("接続した")):
            self.assertEqual(self.run_main("--live", "--from-json", "x.json")[0], 2)

    def test_live_uses_fetch_for_each_repo(self):
        with mock.patch.object(pr, "fetch", return_value=[]) as fetch:
            self.assertEqual(self.run_main("--live")[0], 0)
        self.assertEqual([c.args[0] for c in fetch.call_args_list], ["alpha", "beta"])

    def test_fetch_request_is_fixed_to_api_host_without_credentials(self):
        captured = {}

        class FakeResponse:
            def __init__(self, body):
                self.body = body

            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def read(self, limit):
                return self.body[:limit]

        class FakeOpener:
            def __init__(self, body):
                self.body = body

            def open(self, req, timeout):
                captured["req"], captured["timeout"] = req, timeout
                return FakeResponse(self.body)

        with mock.patch.object(urllib.request, "build_opener", return_value=FakeOpener(b"[]")):
            self.assertEqual(pr.fetch("alpha"), [])
        req = captured["req"]
        self.assertEqual(req.full_url, "https://api.github.com/repos/filderschoice/alpha/releases?per_page=5")
        self.assertEqual(req.get_method(), "GET")
        headers = {k.lower(): v for k, v in req.header_items()}
        self.assertEqual(set(headers), {"user-agent", "accept"})
        self.assertNotIn("@", headers["user-agent"])
        self.assertEqual(captured["timeout"], pr.TIMEOUT_SEC)
        with mock.patch.object(urllib.request, "build_opener",
                               return_value=FakeOpener(b"x" * (pr.MAX_BYTES + 10))):
            with self.assertRaises(pr.ProposeError):
                pr.fetch("alpha")
        with mock.patch.object(urllib.request, "build_opener", return_value=FakeOpener(b"not json")):
            with self.assertRaises(pr.ProposeError):
                pr.fetch("alpha")

    def test_redirect_only_to_https_api_host(self):
        handler = pr._SafeRedirect()
        req = urllib.request.Request("https://api.github.com/a")
        for url in ("https://evil.example/x", "http://api.github.com/x", "https://api.github.com.evil.com/x",
                    "https://api.github.com:8443/x", "ftp://api.github.com/x"):
            with self.subTest(url):
                with self.assertRaises(pr.ProposeError):
                    handler.redirect_request(req, None, 302, "", {}, url)
        new = handler.redirect_request(req, None, 302, "", {}, "https://api.github.com/b")
        self.assertEqual(new.full_url, "https://api.github.com/b")


if __name__ == "__main__":
    unittest.main()
