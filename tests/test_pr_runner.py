import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import pr_runner as runner


VIEWER = {"login": "owner", "databaseId": 123, "pullRequests": {"totalCount": 35}}


def pending_state():
    state = runner.new_state("owner/quest", VIEWER)
    state["pending"] = {"branch": "automation/test", "sha": "a" * 40,
                        "base": "master", "title": "Test", "sequence": 1, "number": None}
    return state


class FakeAPI:
    def __init__(self):
        self.pr = None
        self.created = self.merged = 0
        self.lose_create = self.lose_merge = self.reject_merge = False

    def viewer(self):
        return copy.deepcopy(VIEWER)

    def request(self, method, endpoint, payload=None):
        if endpoint == "repos/owner/quest":
            return {"owner": {"login": "owner"}, "archived": False,
                    "fork": False, "default_branch": "master", "allow_squash_merge": True}
        if method == "GET" and "/pulls?" in endpoint:
            return [copy.deepcopy(self.pr)] if self.pr else []
        if method == "POST" and endpoint.endswith("/pulls"):
            self.created += 1
            self.pr = {"number": 22, "head": {"sha": "a" * 40}, "base": {"ref": "master"},
                       "user": {"login": "owner"}, "state": "open", "merged": False,
                       "merged_at": None, "merge_commit_sha": None,
                       "html_url": "https://github.com/owner/quest/pull/22"}
            if self.lose_create:
                self.lose_create = False
                raise runner.ApiError(0, {}, {"message": "Connection lost after creation"})
            return copy.deepcopy(self.pr)
        if method == "GET" and endpoint.endswith("/22"):
            return copy.deepcopy(self.pr)
        if method == "PUT" and endpoint.endswith("/merge"):
            if self.reject_merge:
                return {"merged": False, "message": "Required checks have not passed"}
            self.merged += 1
            self.pr.update(merged=True, state="closed", merged_at="2026-10-31T12:00:00Z",
                           merge_commit_sha="b" * 40)
            if self.lose_merge:
                self.lose_merge = False
                raise runner.ApiError(0, {}, {"message": "Connection lost after merge"})
            return {"merged": True}
        raise AssertionError((method, endpoint, payload))


class CountAndTransportTests(unittest.TestCase):
    def test_invalid_counts_cannot_be_used_as_success(self):
        for value in (True, -1, "35", "INFO: found 35\n35", None, 35.0):
            with self.subTest(value=value), self.assertRaises(ValueError):
                runner.count_value(value)
        self.assertEqual(runner.count_value(1025), 1025)

    def test_json_quotes_newlines_and_unicode_are_encoded_on_stdin(self):
        payload = {"title": 'A "quoted" title', "body": "Line 1\nLine 2: 🏆\\path"}
        response = subprocess.CompletedProcess([], 0, 'HTTP/2.0 201 Created\ncontent-type: application/json\n\n{"number": 22}', "")
        with patch.object(runner.subprocess, "run", return_value=response) as run:
            self.assertEqual(runner.GitHub().request("POST", "repos/owner/quest/pulls", payload), {"number": 22})
        self.assertEqual(json.loads(run.call_args.kwargs["input"]), payload)
        self.assertNotIn(payload["title"], run.call_args.args[0])

    def test_empty_204_response_is_valid(self):
        response = subprocess.CompletedProcess([], 0, "HTTP/2.0 204 No Content\n\n", "")
        with patch.object(runner.subprocess, "run", return_value=response):
            self.assertIsNone(runner.GitHub().request("DELETE", "repos/owner/quest/git/refs/heads/test"))

    def test_count_uses_total_count_above_1000(self):
        api = runner.GitHub()
        viewer = copy.deepcopy(VIEWER)
        viewer["pullRequests"]["totalCount"] = 1025
        with patch.object(api, "request", return_value={"data": {"viewer": viewer}}) as request:
            self.assertEqual(api.viewer()["pullRequests"]["totalCount"], 1025)
        query = request.call_args.args[2]["query"]
        self.assertIn("totalCount", query)
        self.assertIn("MERGED", query)

    def test_malformed_json_stops_instead_of_claiming_success(self):
        response = subprocess.CompletedProcess([], 0, 'HTTP/2.0 200 OK\n\n{"number": "unterminated', "")
        with patch.object(runner.subprocess, "run", return_value=response):
            with self.assertRaises(runner.ApiError):
                runner.GitHub().request("GET", "repos/owner/quest")

    def test_backoff_respects_retry_after_and_reset(self):
        error = runner.ApiError(429, {"retry-after": "120"}, {"message": "Slow down"})
        self.assertEqual(error.retry_delay(1), 120)
        error = runner.ApiError(403, {"x-ratelimit-remaining": "0", "x-ratelimit-reset": "500"}, {})
        with patch.object(runner.time, "time", return_value=100):
            self.assertEqual(error.retry_delay(1), 402)
        self.assertIsNone(runner.ApiError(403, {}, {"message": "Permission denied"}).retry_delay(1))
        self.assertEqual(runner.ApiError(503, {}, {}).retry_delay(3), 240)

    def test_count_command_has_only_a_number_on_stdout(self):
        with tempfile.TemporaryDirectory() as directory:
            out = io.StringIO()
            with patch.object(runner, "git", return_value=directory), \
                    patch.object(runner.GitHub, "viewer", return_value=VIEWER), \
                    contextlib.redirect_stdout(out):
                self.assertEqual(runner.main(["count"]), 0)
            self.assertEqual(out.getvalue(), "35\n")


class ResumeTests(unittest.TestCase):
    def finish(self, api, state):
        with patch.object(runner, "git"), contextlib.redirect_stderr(io.StringIO()):
            runner.finish_pending(api, Path("."), state, lambda: None, "squash")

    def test_lost_create_response_does_not_create_duplicate_pr(self):
        api, state = FakeAPI(), pending_state()
        api.lose_create = True
        with self.assertRaises(runner.ApiError):
            self.finish(api, state)
        self.assertIsNone(state["pending"]["number"])
        # Simulate loading the checkpoint after process termination.
        state = json.loads(json.dumps(state))
        self.finish(api, state)
        self.assertEqual((api.created, api.merged, len(state["merged"])), (1, 1, 1))
        self.assertEqual(runner.verified_count(state), 36)

    def test_lost_merge_response_is_reconciled_without_merging_twice(self):
        api, state = FakeAPI(), pending_state()
        api.lose_merge = True
        with self.assertRaises(runner.ApiError):
            self.finish(api, state)
        self.assertEqual(len(state["merged"]), 0)
        self.finish(api, state)
        self.assertEqual((api.created, api.merged, len(state["merged"])), (1, 1, 1))
        self.assertIsNone(state["pending"])

    def test_failed_merge_does_not_advance_count(self):
        api, state = FakeAPI(), pending_state()
        api.reject_merge = True
        with self.assertRaises(ValueError):
            self.finish(api, state)
        self.assertEqual(runner.verified_count(state), 35)
        self.assertIsNotNone(state["pending"])

    def test_changed_head_is_never_merged(self):
        api, state = FakeAPI(), pending_state()
        api.reject_merge = True
        with self.assertRaises(ValueError):
            self.finish(api, state)
        api.pr["head"]["sha"] = "c" * 40
        with self.assertRaisesRegex(ValueError, "head changed"):
            self.finish(api, state)
        self.assertEqual(api.merged, 0)

    def test_target_reached_performs_no_pr_writes_and_does_not_claim_badge(self):
        api = FakeAPI()
        state = runner.new_state("owner/quest", VIEWER)
        with contextlib.redirect_stderr(io.StringIO()):
            runner.run_loop(api, Path("."), state, lambda: None, 35, 30, None)
        self.assertEqual(state["status"], "target_reached")
        self.assertEqual(state["badge_status"], "unverified")
        self.assertEqual((api.created, api.merged), (0, 0))

    def test_lagging_remote_count_does_not_double_count_verified_merges(self):
        state = runner.new_state("owner/quest", VIEWER)
        state["merged"] = [{"number": 22}, {"number": 23}]
        self.assertEqual(runner.verified_count(state), 37)
        state["observed_count"] = 37
        self.assertEqual(runner.verified_count(state), 37)

    def test_merges_outside_the_run_update_the_verified_floor(self):
        state = runner.new_state("owner/quest", VIEWER)
        runner.observe_count(state, 36)
        state["merged"].append({"number": 22})
        self.assertEqual(runner.verified_count(state), 37)
        runner.observe_count(state, 37)
        self.assertEqual(runner.verified_count(state), 37)

    def test_pending_merge_is_reconciled_before_changing_the_floor(self):
        state = pending_state()
        runner.observe_count(state, 36)
        self.assertEqual(state["baseline"], 35)
        state["merged"].append({"number": 22})
        state["pending"] = None
        runner.observe_count(state, 36)
        self.assertEqual(runner.verified_count(state), 36)


class LocalGitTests(unittest.TestCase):
    def test_prepare_commit_preserves_dirty_working_tree_and_index(self):
        with tempfile.TemporaryDirectory() as directory:
            remote, root = Path(directory) / "remote.git", Path(directory) / "checkout"
            subprocess.run(["git", "init", "--bare", "--initial-branch=master", str(remote)], check=True, capture_output=True)
            subprocess.run(["git", "clone", str(remote), str(root)], check=True, capture_output=True)
            runner.git(root, "config", "user.name", "Test")
            runner.git(root, "config", "user.email", "test@example.invalid")
            (root / "README.md").write_text("Original\n")
            runner.git(root, "add", "README.md")
            runner.git(root, "commit", "-m", "Initial")
            runner.git(root, "push", "origin", "master")
            original = runner.git(root, "rev-parse", "HEAD")
            (root / "README.md").write_text("Staged user work\n")
            runner.git(root, "add", "README.md")
            (root / "README.md").write_text("More unstaged user work\n")
            (root / "untracked.txt").write_text("Keep me\n")
            status = runner.git(root, "status", "--porcelain")
            staged = runner.git(root, "diff", "--cached")
            state = runner.new_state("owner/quest", VIEWER)
            pending = runner.prepare_commit(root, state, VIEWER, "master", 1024)
            self.assertEqual(runner.git(root, "status", "--porcelain"), status)
            self.assertEqual(runner.git(root, "diff", "--cached"), staged)
            self.assertEqual(runner.git(root, "rev-parse", "HEAD"), original)
            record = json.loads(runner.git(root, "show", f"{pending['sha']}:automation/progress.json"))
            self.assertEqual(record["target_merged_prs"], 1024)
            self.assertEqual(record["sequence"], 1)

    def test_saved_state_is_complete_json(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            state = pending_state()
            runner.save_state(path, state)
            self.assertEqual(json.loads(path.read_text())["pending"]["sha"], "a" * 40)
            self.assertFalse(path.with_suffix(".tmp").exists())


if __name__ == "__main__":
    unittest.main()
