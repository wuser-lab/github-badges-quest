# GitHub Badges Quest

A small guide to the next achievements for [@wuser-lab](https://github.com/wuser-lab).

## Starting point

The profile showed these three achievements on 30 October 2026, before this guide update:

- [x] Pull Shark
- [x] Quickdraw
- [x] YOLO

[Check the live achievements page](https://github.com/wuser-lab?tab=achievements) for current awards and tiers. GitHub awards achievements automatically; a qualifying contribution is not proof that a badge has appeared.

## Next targets

| Achievement | What to do | What is needed |
| --- | --- | --- |
| Pair Extraordinaire | Co-author a commit in a pull request that gets merged. | A real shared contribution and correctly linked co-author credit. This guide is a candidate contribution. |
| Galaxy Brain | Have two discussion answers marked as accepted. | Helpful answers in eligible repository Q&A discussions. GitHub's own Community Discussions no longer award achievements. |
| Starstruck | Create a repository that reaches 16 stars. | Other people finding and starring a useful project. |
| Public Sponsor | Publicly sponsor an open-source contributor through GitHub Sponsors. | A separate choice of recipient and payment amount. |

## Preserve co-author credit

Use the actual contributor's GitHub-associated email in a commit trailer, after a blank line:

```text
Co-authored-by: Contributor Name <their-github-associated-email>
```

For a squash merge, keep the trailer in the final commit message. This update credits Codex for its research and writing.

## Pull Shark tiers

The community-maintained thresholds are 2, 16, 128 and 1,024 merged pull requests. The live profile is the authority on the awarded tier.

## PR tracking runner

The [resumable runner](docs/pr-automation.md) provides strict account counting,
saved progress, JSON request encoding, and verified merges. It creates clearly
labelled automated tracking entries in this repository. Reaching an API count
does not prove that GitHub has awarded a badge.

## Sources

- [GitHub: profile and achievement reference](https://docs.github.com/en/account-and-profile/reference/profile-reference)
- [GitHub: creating a commit with multiple authors](https://docs.github.com/en/pull-requests/how-tos/commit-changes/creating-a-commit-with-multiple-authors)
- [Community-maintained achievement requirements and tiers](https://github.com/Schweinepriester/github-profile-achievements#achievements)

## Contributors

- [wuser-lab](https://github.com/wuser-lab) 🚀
- [Codex](https://github.com/codex) — research and writing assistance for this guide
