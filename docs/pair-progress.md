# Pair Extraordinaire helper

`scripts/pair_progress.py` checks existing PRs involving `wuser-lab` and
`userwww8`. It uses the existing GitHub CLI login; the second account's password
or token is not needed. Python 3 and an authenticated `gh` CLI are required.

Run an audit:

```sh
python3 scripts/pair_progress.py
```

Choose repositories owned by the signed-in account:

```sh
python3 scripts/pair_progress.py --repo wuser-lab/consent-lens --repo wuser-lab/meridian
```

After reviewing the changes, merge eligible open PRs:

```sh
python3 scripts/pair_progress.py --repo wuser-lab/consent-lens --merge
```

Eligibility requires both accounts to be resolved by GitHub as authors on the
same commit, a nonempty PR authored by one selected account, a clean merge state,
no changes-requested review decision, and successful CI. More than 100 commits
or authors requires manual review. Each merge is pinned to the inspected head.
The merge method preserves original commits and their authorship; repositories
that disable merge commits need manual handling. Every invocation scans fresh
state, so already merged PRs are counted rather than merged again.

The helper audits up to 200 recent open/merged PRs per repository by default;
`--max-prs` changes that bound. Counts cover only the inspected repositories and
PRs. Account aliases belonging to one person do not establish two independent
contributors. Author trailers should describe actual work. This helper creates
no commits, PRs, or author trailers and does not change account privacy settings.

GitHub controls eligibility and award processing. Community-reported Pair
Extraordinaire thresholds are 1, 10, 24 and 48 qualifying merged PRs, but an API
evidence count is not proof of an awarded tier:

- https://github.com/Schweinepriester/github-profile-achievements#tiers
- https://docs.github.com/en/account-and-profile/reference/profile-reference#earning-achievements
