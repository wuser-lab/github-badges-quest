#!/usr/bin/env python3
"""Resumable, serial PR tracking for the repository owner's personal quest."""

import argparse
import datetime as dt
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
from urllib.parse import quote, urlencode
import uuid


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def log(message):
    print(f"[{now()}] {message}", file=sys.stderr, flush=True)


def count_value(value):
    if type(value) is not int or value < 0:
        raise ValueError("GitHub returned an invalid merged-PR count; refusing to continue")
    return value


class ApiError(RuntimeError):
    def __init__(self, status, headers, body):
        self.status, self.headers, self.body = status, headers, body
        message = body.get("message", str(body)) if isinstance(body, dict) else str(body)
        super().__init__(f"GitHub HTTP {status}: {message[:600]}")

    def retry_delay(self, attempt):
        limited = self.status == 429 or (
            self.status == 403 and (
                "rate limit" in str(self.body).lower()
                or "retry-after" in self.headers
                or self.headers.get("x-ratelimit-remaining") == "0"
            )
        )
        if not limited and self.status not in (0, 500, 502, 503, 504):
            return None
        delay = 60 * 2 ** (attempt - 1)
        if "retry-after" in self.headers:
            delay = max(delay, float(self.headers["retry-after"]))
        if self.headers.get("x-ratelimit-remaining") == "0":
            delay = max(delay, float(self.headers.get("x-ratelimit-reset", 0)) - time.time() + 2)
        return delay


class GitHub:
    def __init__(self):
        self.last_write = 0.0

    def request(self, method, endpoint, payload=None):
        if method != "GET":
            time.sleep(max(0, 1.1 - (time.monotonic() - self.last_write)))
        command = ["gh", "api", "--hostname", "github.com", "--include", "--method", method, endpoint]
        if payload is not None:
            command += ["--input", "-"]
        try:
            result = subprocess.run(
                command, input=json.dumps(payload) if payload is not None else None,
                text=True, capture_output=True, timeout=90,
            )
        except subprocess.TimeoutExpired as error:
            raise ApiError(0, {}, {"message": "Request timed out; reconcile before retrying"}) from error
        if method != "GET":
            self.last_write = time.monotonic()
        header_text, separator, body_text = result.stdout.partition("\n\n")
        if not separator or not header_text.startswith("HTTP/"):
            raise ApiError(0, {}, {"message": result.stderr.strip() or "Missing HTTP response"})
        status = int(header_text.splitlines()[0].split()[1])
        headers = dict(
            (key.lower(), value.strip())
            for line in header_text.splitlines()[1:] if ":" in line
            for key, value in [line.split(":", 1)]
        )
        try:
            body = json.loads(body_text) if body_text.strip() else None
        except json.JSONDecodeError as exc:
            raise ApiError(status if status >= 400 else 0, headers, {"message": "Invalid JSON response"}) from exc
        if result.returncode or status >= 400:
            raise ApiError(status, headers, body)
        return body

    def viewer(self):
        body = self.request("POST", "graphql", {
            "query": "query { viewer { login databaseId pullRequests(states: MERGED) { totalCount } } }"
        })
        if body.get("errors"):
            raise ValueError(f"GitHub count query failed: {body['errors']}")
        viewer = body["data"]["viewer"]
        count_value(viewer["pullRequests"]["totalCount"])
        return viewer


def git(root, *arguments, data=None, extra_env=None):
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    result = subprocess.run(
        ["git", "-C", str(root), *arguments], input=data, text=True,
        capture_output=True, env=env, timeout=120,
    )
    if result.returncode:
        raise RuntimeError(f"git {arguments[0]} failed: {result.stderr.strip()[:800]}")
    return result.stdout.strip()


def save_state(path, state):
    state["updated_at"] = now()
    temporary = path.with_suffix(".tmp")
    with temporary.open("w") as stream:
        json.dump(state, stream, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def verified_count(state):
    return max(count_value(state["observed_count"]),
               count_value(state["baseline"]) + len(state["merged"]))


def observe_count(state, value):
    state["observed_count"] = count_value(value)
    # Include merges made outside this run. A pending PR may already be merged
    # remotely after a lost response, so reconcile it before adjusting this floor.
    if state["pending"] is None:
        state["baseline"] = max(state["baseline"], value - len(state["merged"]))


def new_state(repo, viewer):
    count = count_value(viewer["pullRequests"]["totalCount"])
    return {
        "version": 1, "repo": repo, "login": viewer["login"],
        "run_id": uuid.uuid4().hex[:12], "baseline": count,
        "observed_count": count, "merged": [], "pending": None,
        "status": "ready", "badge_status": "unverified", "created_at": now(),
        "next_write_at": 0,
    }


def prepare_commit(root, state, viewer, base, target):
    """Build a commit with a private index; never switch or overwrite the checkout."""
    git(root, "fetch", "--quiet", "origin", base)
    parent = git(root, "rev-parse", "FETCH_HEAD")
    sequence = len(state["merged"]) + 1
    branch = f"automation/gold-{state['run_id']}-{sequence:04d}"
    record = {
        "schema_version": 1, "run_id": state["run_id"], "sequence": sequence,
        "created_at": now(), "target_merged_prs": target,
        "observed_merged_prs_before_creation": state["observed_count"],
        "note": "Automatically generated tracking entry for the owner's personal badge quest. "
                "This is not a feature contribution or proof of an awarded achievement.",
    }
    blob = git(root, "hash-object", "-w", "--stdin", data=json.dumps(record, indent=2) + "\n")
    with tempfile.TemporaryDirectory(prefix="quest-index-") as directory:
        index_env = {"GIT_INDEX_FILE": str(Path(directory) / "index")}
        git(root, "read-tree", parent, extra_env=index_env)
        git(root, "update-index", "--add", "--cacheinfo", "100644", blob,
            "automation/progress.json", extra_env=index_env)
        tree = git(root, "write-tree", extra_env=index_env)
    login = viewer["login"]
    identity = {"GIT_AUTHOR_NAME": login, "GIT_COMMITTER_NAME": login,
                "GIT_AUTHOR_EMAIL": f"{viewer['databaseId']}+{login}@users.noreply.github.com",
                "GIT_COMMITTER_EMAIL": f"{viewer['databaseId']}+{login}@users.noreply.github.com"}
    title = f"chore: record automated quest entry {sequence:04d}"
    sha = git(root, "commit-tree", tree, "-p", parent, data=title + "\n", extra_env=identity)
    return {"branch": branch, "sha": sha, "base": base, "title": title,
            "sequence": sequence, "number": None}


def finish_pending(api, root, state, save, merge_method):
    """Reconcile remote state before every write, including after uncertain responses."""
    pending = state["pending"]
    repo, login = state["repo"], state["login"]
    # A repeated push of exactly the saved commit is safe; no force-push is used.
    git(root, "push", "--quiet", "origin", f"{pending['sha']}:refs/heads/{pending['branch']}")
    if pending["number"] is None:
        query = urlencode({"state": "all", "head": f"{login}:{pending['branch']}",
                           "base": pending["base"], "per_page": 100})
        existing = api.request("GET", f"repos/{repo}/pulls?{query}")
        if len(existing) > 1:
            raise ValueError("Multiple PRs use the saved branch; inspect them before resuming")
        if existing:
            pr = existing[0]
        else:
            pr = api.request("POST", f"repos/{repo}/pulls", {
                "head": pending["branch"], "base": pending["base"], "title": pending["title"],
                "body": "Updates the generated quest tracking record in `automation/progress.json`.\n\n"
                        "This PR is automatically created and merged by the repository owner for a "
                        "personal achievement quest. It does not claim a product improvement, human "
                        "review, collaboration, or an awarded badge.\n\n"
                        f"Run: `{state['run_id']}`; entry: `{pending['sequence']}`. "
                        "The runner verifies the merge before counting it.",
            })
        pending["number"] = pr["number"]
        save()
    endpoint = f"repos/{repo}/pulls/{pending['number']}"
    pr = api.request("GET", endpoint)
    if (pr["head"]["sha"] != pending["sha"] or pr["base"]["ref"] != pending["base"]
            or pr["user"]["login"].lower() != login.lower()):
        raise ValueError("Saved PR's author, base or head changed; refusing to merge")
    if not pr["merged"]:
        if pr["state"] != "open":
            raise ValueError("Saved PR was closed without merging; inspect it before resuming")
        result = api.request("PUT", endpoint + "/merge", {
            "sha": pending["sha"], "merge_method": merge_method,
        })
        if result.get("merged") is not True:
            raise ValueError(f"Merge was not successful: {result.get('message')}")
        pr = api.request("GET", endpoint)
    if pr.get("merged") is not True or not pr.get("merged_at"):
        raise ValueError("GitHub has not verified the merge; count unchanged")
    if not any(item["number"] == pr["number"] for item in state["merged"]):
        state["merged"].append({"number": pr["number"], "url": pr["html_url"],
                                "merged_at": pr["merged_at"], "sha": pr["merge_commit_sha"]})
    state["pending"] = None
    state["cleanup_branch"] = pending["branch"]
    save()
    log(f"Verified merge: {pr['html_url']} ({verified_count(state)} merged PRs)")


def cleanup_branch(api, state, save):
    branch = state.get("cleanup_branch")
    if branch:
        try:
            api.request("DELETE", f"repos/{state['repo']}/git/refs/heads/{quote(branch, safe='')}")
        except ApiError as error:
            if error.status != 404:
                raise
        state.pop("cleanup_branch")
        save()


def run_loop(api, root, state, save, target, interval, max_merges):
    repository = api.request("GET", f"repos/{state['repo']}")
    if repository["owner"]["login"].lower() != state["login"].lower():
        raise ValueError("This runner only operates on the authenticated user's own repository")
    if repository["archived"] or repository.get("fork"):
        raise ValueError("Use an active, non-fork repository owned by the authenticated user")
    base = repository["default_branch"]
    method = "squash" if repository.get("allow_squash_merge") else "merge"
    completed_at_start = len(state["merged"])
    failures = 0
    while True:
        try:
            if state.get("retry_at", 0) > time.time():
                time.sleep(min(30, state["retry_at"] - time.time()))
                continue
            cleanup_branch(api, state, save)
            viewer = api.viewer()
            if viewer["login"] != state["login"]:
                raise ValueError("Authenticated account changed; refusing to continue")
            observe_count(state, viewer["pullRequests"]["totalCount"])
            save()
            # Never leave a created PR behind just because the account count changed.
            if not state["pending"]:
                if state["observed_count"] >= target:
                    state["status"] = "target_reached"
                    save()
                    log(f"GitHub reports {state['observed_count']} merged PRs; target {target} reached. "
                        "The actual achievement remains unverified.")
                    return
                if max_merges is not None and len(state["merged"]) - completed_at_start >= max_merges:
                    state["status"] = "batch_complete"
                    save()
                    return
                if verified_count(state) >= target:
                    log("Verified local merges reach the target; waiting for GitHub's count to catch up")
                    time.sleep(30)
                    continue
                wait = state.get("next_write_at", 0) - time.time()
                if wait > 0:
                    time.sleep(min(30, wait))
                    continue
                state["pending"] = prepare_commit(root, state, viewer, base, target)
                state["next_write_at"] = time.time() + interval
                state["status"] = "running"
                save()
            finish_pending(api, root, state, save, method)
            failures = 0
            state.pop("last_error", None)
            state.pop("retry_at", None)
            save()
        except ApiError as error:
            failures += 1
            delay = error.retry_delay(failures)
            if delay is None or failures >= 5:
                raise
            state.update(status="retrying", last_error=str(error), retry_at=time.time() + delay)
            save()
            log(f"{error}; saved progress, retrying after {delay:.0f} seconds")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("status", "count", "run"), nargs="?", default="status")
    parser.add_argument("--target", type=int, default=1024)
    parser.add_argument("--interval", type=float, default=30,
                        help="Seconds between new PR cycles (minimum 30)")
    parser.add_argument("--max-merges", type=int, help="Optional limit for a checked batch")
    args = parser.parse_args(argv)
    if args.target <= 0 or args.interval < 30 or (args.max_merges is not None and args.max_merges <= 0):
        parser.error("target and max-merges must be positive; interval must be at least 30 seconds")
    root = Path(__file__).resolve().parents[1]
    state_dir = Path(git(root, "rev-parse", "--absolute-git-dir")) / "gold-runner"
    state_dir.mkdir(exist_ok=True)
    path = state_dir / "state.json"
    api = GitHub()
    state = None
    with (state_dir / "lock").open("w") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            if args.command == "status" and path.exists():
                print(path.read_text(), end="")
                return 0
            log("Another runner is active; refusing to start a second copy")
            return 1
        try:
            viewer = api.viewer()
            if args.command == "count":
                print(count_value(viewer["pullRequests"]["totalCount"]))
                return 0
            # Resolve the actual remote through gh rather than assuming its owner/name.
            result = subprocess.run(["gh", "repo", "view", "--json", "nameWithOwner"],
                                    cwd=root, capture_output=True, text=True, check=True, timeout=90)
            repo = json.loads(result.stdout)["nameWithOwner"]
            state = json.loads(path.read_text()) if path.exists() else new_state(repo, viewer)
            if state["version"] != 1 or state["repo"] != repo or state["login"] != viewer["login"]:
                raise ValueError("Saved progress belongs to a different account or repository")
            count_value(state["baseline"])
            observe_count(state, viewer["pullRequests"]["totalCount"])
            state["target"] = args.target
            save = lambda: save_state(path, state)
            save()
            if args.command == "run":
                def stop(signum, frame):
                    raise KeyboardInterrupt
                signal.signal(signal.SIGTERM, stop)
                signal.signal(signal.SIGINT, stop)
                state.update(pid=os.getpid(), started_at=now())
                save()
                log(f"Starting/resuming {repo}: {state['observed_count']} merged PRs; target {args.target}")
                run_loop(api, root, state, save, args.target, args.interval, args.max_merges)
                state.pop("pid", None)
                save()
            print(json.dumps(state, indent=2))
            return 0
        except (Exception, KeyboardInterrupt) as error:
            if state is not None:
                state.pop("pid", None)
                state.update(status="stopped" if isinstance(error, KeyboardInterrupt) else "failed",
                             last_error=str(error) or type(error).__name__)
                save_state(path, state)
            log(f"Stopped: {error or type(error).__name__}. Progress is preserved; no success is claimed.")
            return 130 if isinstance(error, KeyboardInterrupt) else 1


if __name__ == "__main__":
    sys.exit(main())
