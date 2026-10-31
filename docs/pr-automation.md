# Resumable PR tracking runner

This runner creates and merges explicitly automated tracking PRs in the authenticated
owner's own badge-quest repository. Each PR replaces `automation/progress.json` with
the next run entry. These entries are activity records, not feature contributions,
human reviews, collaboration, or evidence of an awarded badge.

Requires macOS or Linux, Python 3.10+, Git, and GitHub CLI authenticated to
`github.com` with repository write access. It runs on your computer; it does not
use paid services or GitHub Actions minutes.

```sh
# Check the account's actual merged-PR total. Stdout is a single integer.
bash scripts/gold_bot.sh count

# Read current progress as JSON (default command).
bash scripts/gold_bot.sh status

# Run one checked cycle before a longer run.
bash scripts/gold_bot.sh run --target 1024 --max-merges 1

# Start or resume toward the target.
bash scripts/gold_bot.sh run --target 1024
```

Logs go to stderr. Counts and JSON go to stdout. JSON request bodies are encoded
with Python's JSON serializer and passed on stdin; no shell-built JSON is used.
The account count comes from `viewer.pullRequests(states: MERGED).totalCount`,
so it covers repositories visible to the signed-in account and is not truncated
by a PR-list limit or the 1,000-result search cap. API totals and achievement
eligibility are different things.

Progress is stored in the clone's `.git/gold-runner/state.json`. Keep that file
and the clone to resume after interruption. One runner can hold the local lock
at a time. The saved pending commit and PR are reconciled with GitHub before
counting, so losing a response does not create a duplicate PR or count a failed
merge. A changed PR head, closed unmerged PR, permission failure, or invalid count
stops the run with a nonzero exit code and preserves progress.

The runner builds Git objects using a temporary index. It never changes the
checkout branch or includes staged, unstaged, or untracked user files. It does
not force-push, bypass branch rules, or request other people's reviews. Merges
use the saved head SHA. Generated branches are deleted after verified merges.

Cycles start at least 30 seconds apart. Writes are serial and separated by at
least one second. Rate-limit responses honor `Retry-After` and reset headers;
otherwise retry delays increase from one minute, with at most five consecutive
failures. GitHub may apply lower limits, so completion time is not guaranteed.
See GitHub's [rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
and [API best practices](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api).

Ctrl-C stops the foreground runner. Run the same command to resume. A count at or
above the target is reported as `target_reached`; `badge_status` stays `unverified`.
Only the [live achievements page](https://github.com/wuser-lab?tab=achievements)
can confirm the badge. The community-reported Gold threshold is 1,024 merged PRs;
this runner cannot promise that generated tracking PRs qualify.

```sh
python3 -m unittest discover -s tests -v
```
