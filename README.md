# GitHub Badges Quest

A small guide to the next achievements for [@wuser-lab](https://github.com/wuser-lab).

## Verified status — 4 November 2026

The owner-supplied screenshot and live profile both show four distinct achievements:

- [x] Pull Shark — x3, Silver
- [x] Pair Extraordinaire — base award
- [x] Quickdraw — earned; no tier ladder
- [x] YOLO — earned; no tier ladder

[Check the live achievements page](https://github.com/wuser-lab?tab=achievements) for actual awards. A merged-PR API count does not establish an awarded tier. The next Pull Shark tier is Gold, but it is not claimed here.

## Next targets

| Achievement | Next milestone | Current evidence |
| --- | --- | --- |
| Pair Extraordinaire | Bronze: 10 qualifying co-authored merged PRs, according to the community catalogue. | Base award verified; qualifying event count has not been audited. Credit only actual contributions. |
| Galaxy Brain | Two accepted answers in eligible repository discussions. | Existing pnpm answers #10128 and #9827 were both still unaccepted on 4 November. Acceptance belongs to the question author or maintainers. |
| Starstruck | One created repository reaches 16 stars, according to the community catalogue. | Consent Lens has 2 stars as of 4 November; 14 more would reach the reported threshold. |
| Pull Shark | Gold: 1,024 qualifying merged PRs, according to the community catalogue. | Silver is visible. A previous search count above 1,024 has not established a Gold award. |

The scope remains free-only. Public Sponsor requires a separate spending decision and is not an active target. The account holder's minimal profile README stays unchanged.

## Preserve co-author credit

Use the actual contributor's GitHub-associated email in a commit trailer, after a blank line:

```text
Co-authored-by: Contributor Name <their-github-associated-email>
```

For a squash merge, keep the trailer in the final commit message. This update credits Codex for its research and writing.

## Pull Shark tiers

The community-maintained thresholds are 2, 16, 128 and 1,024 merged pull requests. The live profile is the authority on the awarded tier.

## PR tracking runner

For existing coauthored work, use the [Pair Extraordinaire helper](docs/pair-progress.md).
It audits both accounts and can merge checked PRs in owned repositories while
preserving the original commits and author credit.

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
