import copy
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
import contextlib
import io

spec = importlib.util.spec_from_file_location("pair_progress", Path(__file__).parents[1] / "scripts/pair_progress.py")
pair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pair)
ACCOUNTS = {"wuser-lab", "userwww8"}


def commit(*accounts):
    return {"commit": {"oid": "abc", "authors": {
        "pageInfo": {"hasNextPage": False},
        "nodes": [{"user": {"login": name}} for name in accounts],
    }, "statusCheckRollup": {"state": "SUCCESS", "contexts": {"totalCount": 1}}}}


def pr():
    return {"state": "OPEN", "isDraft": False, "additions": 10, "deletions": 1,
            "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN", "reviewDecision": None,
            "author": {"login": "userwww8"},
            "commits": {"pageInfo": {"hasNextPage": False}, "nodes": [commit(*ACCOUNTS)]}}


class PairProgressTests(unittest.TestCase):
    def test_default_audit_never_mutates_a_ready_pr(self):
        item = pr()
        item["url"] = "https://github.com/wuser-lab/meridian/pull/99"
        with patch.object(pair.sys, "argv", ["pair_progress.py", "--repo", "wuser-lab/meridian"]), \
             patch.object(pair, "gh_api", return_value={"login": "wuser-lab"}) as api, \
             patch.object(pair, "repository_prs", return_value=([item], False)), \
             contextlib.redirect_stdout(io.StringIO()):
            pair.main()
        api.assert_called_once_with("user")

    def test_merge_uses_put_and_pins_the_inspected_head(self):
        item = pr()
        item.update(number=99, url="https://github.com/wuser-lab/meridian/pull/99")
        with patch.object(pair.sys, "argv", ["pair_progress.py", "--repo", "wuser-lab/meridian", "--merge"]), \
             patch.object(pair, "gh_api", side_effect=[{"login": "wuser-lab"}, {"merged": True}]) as api, \
             patch.object(pair, "repository_prs", return_value=([item], False)), \
             contextlib.redirect_stdout(io.StringIO()):
            pair.main()
        api.assert_called_with("repos/wuser-lab/meridian/pulls/99/merge", {
            "sha": "abc", "merge_method": "merge",
        }, method="PUT")

    def test_real_shared_commit_is_ready_and_merged_is_counted(self):
        item = pr()
        self.assertEqual(pair.classify(item, ACCOUNTS), "ready")
        item["state"] = "MERGED"
        self.assertEqual(pair.classify(item, ACCOUNTS), "merged with shared author evidence")

    def test_separate_single_author_commits_are_not_coauthored(self):
        item = pr()
        item["commits"]["nodes"] = [commit("wuser-lab"), commit("userwww8")]
        self.assertEqual(pair.classify(item, ACCOUNTS), "no shared author evidence")

    def test_incomplete_evidence_requires_manual_review(self):
        item = pr()
        item["commits"]["pageInfo"]["hasNextPage"] = True
        self.assertTrue(pair.classify(item, ACCOUNTS).startswith("manual:"))
        item = pr()
        item["commits"]["nodes"][0]["commit"]["authors"]["nodes"] = [{"user": None}]
        self.assertEqual(pair.classify(item, ACCOUNTS), "no shared author evidence")

    def test_unready_work_is_never_eligible(self):
        for field, value in [("isDraft", True), ("additions", 0),
                             ("reviewDecision", "CHANGES_REQUESTED"),
                             ("mergeable", "UNKNOWN"), ("mergeStateStatus", "BLOCKED")]:
            item = pr()
            item[field] = value
            if field == "additions":
                item["deletions"] = 0
            self.assertNotEqual(pair.classify(item, ACCOUNTS), "ready")
        for checks in [None, {"state": "PENDING", "contexts": {"totalCount": 1}},
                       {"state": "SUCCESS", "contexts": {"totalCount": 0}}]:
            item = copy.deepcopy(pr())
            item["commits"]["nodes"][-1]["commit"]["statusCheckRollup"] = checks
            self.assertNotEqual(pair.classify(item, ACCOUNTS), "ready")


if __name__ == "__main__":
    unittest.main()
