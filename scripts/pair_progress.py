#!/usr/bin/env python3
"""Audit existing coauthored PRs; optionally merge checked work in owned repos."""
import argparse
import json
import re
import subprocess
import sys

QUERY = """query($owner:String!,$repo:String!,$after:String) {
  repository(owner:$owner,name:$repo) {
    pullRequests(first:20,after:$after,states:[OPEN,MERGED],orderBy:{field:CREATED_AT,direction:DESC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number url state isDraft additions deletions mergeable mergeStateStatus reviewDecision
        author { login }
        commits(first:100) {
          pageInfo { hasNextPage }
          nodes { commit {
            oid
            authors(first:100) { pageInfo { hasNextPage } nodes { user { login } } }
            statusCheckRollup { state contexts(first:1) { totalCount } }
          } }
        }
      }
    }
  }
}"""


def gh_api(endpoint, payload=None, method=None):
    command = ["gh", "api", "--hostname", "github.com", endpoint]
    if method:
        command += ["--method", method]
    if payload is not None:
        command += ["--input", "-"]
    result = subprocess.run(command, input=json.dumps(payload) if payload is not None else None,
                            text=True, capture_output=True, timeout=90)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "GitHub request failed")
    data = json.loads(result.stdout)
    if isinstance(data, dict) and data.get("errors"):
        raise RuntimeError(str(data["errors"]))
    return data


def classify(pr, accounts):
    commits = pr["commits"]
    if commits["pageInfo"]["hasNextPage"]:
        return "manual: more than 100 commits"
    nodes = commits["nodes"]
    if any(n["commit"]["authors"]["pageInfo"]["hasNextPage"] for n in nodes):
        return "manual: incomplete author list"
    # Require both GitHub-resolved users on the SAME commit, not one commit each.
    coauthored = any(accounts <= {
        author["user"]["login"].lower()
        for author in node["commit"]["authors"]["nodes"] if author.get("user")
    } for node in nodes)
    if not coauthored:
        return "no shared author evidence"
    if pr["state"] == "MERGED":
        return "merged with shared author evidence"
    if not pr.get("author") or pr["author"]["login"].lower() not in accounts:
        return "manual: PR author outside selected accounts"
    if pr["isDraft"] or pr["additions"] + pr["deletions"] == 0:
        return "skip: draft or empty diff"
    if pr["reviewDecision"] == "CHANGES_REQUESTED":
        return "skip: changes requested"
    if pr["mergeable"] != "MERGEABLE" or pr["mergeStateStatus"] != "CLEAN":
        return "skip: merge state not clean"
    checks = nodes[-1]["commit"].get("statusCheckRollup")
    if not checks or checks["state"] != "SUCCESS" or not checks["contexts"]["totalCount"]:
        return "skip: passing checks required"
    return "ready"


def repository_prs(repository, maximum):
    owner, repo = repository.split("/")
    after = None
    found = []
    while len(found) < maximum:
        data = gh_api("graphql", {"query": QUERY, "variables": {
            "owner": owner, "repo": repo, "after": after,
        }})["data"]["repository"]
        if data is None:
            raise RuntimeError(f"Repository unavailable: {repository}")
        page = data["pullRequests"]
        found.extend(page["nodes"][:maximum - len(found)])
        if not page["pageInfo"]["hasNextPage"]:
            return found, False
        after = page["pageInfo"]["endCursor"]
    return found, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--account", action="append", help="Use exactly twice; default: wuser-lab, userwww8")
    parser.add_argument("--repo", action="append", help="Owned OWNER/REPO; repeat for multiple repositories")
    parser.add_argument("--max-prs", type=int, default=200, help="Maximum PRs inspected per repository")
    parser.add_argument("--merge", action="store_true", help="Merge ready PRs, preserving original commits")
    args = parser.parse_args()
    accounts = {a.lower() for a in (args.account or ["wuser-lab", "userwww8"])}
    if len(accounts) != 2 or args.max_prs < 1:
        parser.error("Supply two distinct accounts and a positive --max-prs")
    repos = list(dict.fromkeys(args.repo or ["wuser-lab/consent-lens", "wuser-lab/meridian"]))
    viewer = gh_api("user")["login"].lower()
    if viewer not in accounts:
        parser.error(f"Signed in as {viewer}; expected one of the selected accounts")
    for repo in repos:
        if not re.fullmatch(r"[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", repo) or repo.split("/")[0].lower() != viewer:
            parser.error("Only repositories owned by the signed-in account are supported")
    matched = merged_now = 0
    incomplete = False
    for repo in repos:
        prs, truncated = repository_prs(repo, args.max_prs)
        incomplete |= truncated
        for pr in prs:
            status = classify(pr, accounts)
            matched += status == "merged with shared author evidence"
            if status != "no shared author evidence":
                print(f"{status}: {pr['url']}")
            if args.merge and status == "ready":
                # Pin the mutation to the exact head that was inspected.
                head = pr["commits"]["nodes"][-1]["commit"]["oid"]
                result = gh_api(f"repos/{repo}/pulls/{pr['number']}/merge", {
                    "sha": head, "merge_method": "merge",
                }, method="PUT")
                if not result.get("merged"):
                    raise RuntimeError(f"Merge not confirmed for {pr['url']}")
                merged_now += 1
                print(f"Merged: {pr['url']}")
    print(f"Matching merged PRs in inspected scope: {matched}; merged this run: {merged_now}.")
    if incomplete:
        print("Scan limited by --max-prs; this is a partial count.")
    print("This is contribution evidence, not a confirmed GitHub achievement count.")
    print("Reported tier thresholds: 1 / 10 / 24 / 48. Check the live profile for awards.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, subprocess.TimeoutExpired, KeyError, ValueError) as error:
        print(f"Stopped: {error}", file=sys.stderr)
        sys.exit(1)
