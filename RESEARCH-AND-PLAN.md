# GitHub achievement research and public action plan

Prepared for [wuser-lab](https://github.com/wuser-lab), 30 October 2026 (Europe/Brussels). Research and drafting assisted by Codex. This is a dated plan, not a claim that further badges have been awarded.

## Recommended outcome

Work toward the seven ordinary profile achievements through useful contributions, a focused Consent Lens launch, and optional public sponsorship. Keep Finishing Touch as a research item until an accessible qualifying route is established. Retired, disabled and staff-only awards are outside the achievable target.

Publishing this plan is the immediate public deliverable. Launch posts, discussion answers, support submissions and payments are separate actions; the schedule below does not mean they have happened or will run automatically.

## 1. Verified starting point

| Evidence checked on 30 October | Observation | Meaning |
| --- | --- | --- |
| [Live profile](https://github.com/wuser-lab?tab=achievements) | Pull Shark, Quickdraw and YOLO visible; no higher tier displayed | Three awards confirmed in the interface |
| [Merged PR search](https://github.com/pulls?q=is%3Apr+author%3Awuser-lab+is%3Amerged) | Connected GitHub search returned 18 merged PRs | An observed API count, not an authoritative count of qualifying achievement events |
| [Badge guide PR #6](https://github.com/wuser-lab/github-badges-quest/pull/6) | Merged at 22:19:53 UTC on 30 October; GitHub links both wuser-lab and Codex | A candidate Pair Extraordinaire event; no award verified |
| [Final commit](https://github.com/wuser-lab/github-badges-quest/commit/c1d15ede9331748d0fe39e307d3d941756d98380) | The co-author trailer survived the squash merge | Attribution is preserved; AI co-author eligibility remains unconfirmed |
| [Consent Lens](https://github.com/wuser-lab/consent-lens) | 2 stars; description and three discovery topics updated | 14 additional stars needed to reach the community-reported base threshold |
| [Consent Lens package](https://github.com/wuser-lab/consent-lens/blob/main/package.json) | Uses the TCF core library, Vite and jsdom | Relevant contribution and audience areas are consent tooling, browser workflows and frontend tooling |
| Consent Lens repository metadata | GitHub reports no detected license | Decide on an appropriate license before describing the source as open source; public code visibility alone does not establish a license |

Correction to the earlier shorthand: 18 merged PRs exceeding a published threshold does **not** establish that GitHub owes a bronze award. The connected search may have visibility limits, and GitHub does not publish a complete counting contract. Record the count and the awarded tier separately.

GitHub's official documentation says achievements are automatic and remain in public preview. A community-manager incident update reports delays of several days without a promised fix date. This makes delayed processing plausible for this account, but does not prove the cause. [Official profile reference](https://docs.github.com/en/account-and-profile/reference/profile-reference); [GitHub incident](https://github.com/orgs/community/discussions/203416).

## 2. Complete achievement map

The numerical thresholds and nonstandard award classifications below come from a community-maintained catalogue, not a current official GitHub specification. [Catalogue and tiers](https://github.com/Schweinepriester/github-profile-achievements#achievements).

| Achievement | Target or availability | Current action |
| --- | --- | --- |
| Pull Shark | 2 / 16 / 128 / 1,024 merged PRs | Investigate the tier discrepancy; continue useful work |
| Quickdraw | One tier | Already visible; complete |
| YOLO | One tier | Already visible; complete |
| Pair Extraordinaire | 1 / 10 / 24 / 48 co-authored merged PRs | Verify the existing candidate; pursue substantive collaboration |
| Galaxy Brain | 2 / 8 / 16 / 32 accepted answers | Build a queue of questions where a tested answer adds value |
| Starstruck | 16 / 128 / 512 / 4,096 stars on one repository | Focus on Consent Lens, starting at 2 |
| Public Sponsor | One tier | Optional public sponsorship after recipient and budget approval |
| Finishing Touch | Catalogue describes GitHub UI quality contributions | No accessible public qualification route verified; no delivery promise |
| Arctic Code Vault Contributor | Retired | Exclude |
| Mars 2020 Contributor | Retired | Exclude |
| Heart On Your Sleeve | Disabled | Exclude |
| Open Sourcerer | Disabled | Exclude |
| Proxima Pioneer | Internal | Exclude |
| Proxima Staffshipper | Internal | Exclude |
| Proxima Staffuser | Internal | Exclude |

GitHub separately confirms the Mars event has ended. Program highlights such as Pro, Campus Expert and security credits are a different system; Pro is already visible on this account. [Official reference](https://docs.github.com/en/account-and-profile/reference/profile-reference).

## 3. First: investigate the missing awards

Owner: account holder, assisted by Codex. Effort budget: 45–90 minutes initially.

1. Record the live badge view, PR URL, merge date, default branch, final commit and linked authors. Use PR #6 above as the Pair candidate. Preserve its history.
2. Export the returned merged-PR list with URLs and dates. Check public visibility, PR authorship, actual merged state and account-linked commit attribution. Keep inaccessible activity out of a public evidence packet.
3. Recheck the profile once after 48–72 hours, around 2 November. This is a practical checkpoint, not GitHub's promised processing window.
4. If still absent around 6 November, check the incident for updates and prepare one concise report through GitHub's available support or feedback route. Availability and investigation are not guaranteed. Do not create duplicate reports.
5. Record an award only after the live profile displays it. Do not count repeated refreshes, additional trailers or duplicate test PRs as a fix.

For Pair Extraordinaire, a next real collaboration should involve another contributor's substantive work and their correct linked credit. Codex's recognized credit in PR #6 proves attribution display, not award eligibility. If a human collaborator is available, jointly implement one independently useful change and preserve both authors on the final merged commit. Do not add uninvolved people or create a second identity.

### Evidence report draft

> My profile is https://github.com/wuser-lab. Pull Shark, Quickdraw and YOLO are visible. Connected GitHub search returned 18 merged PRs, but the profile still displays the base Pull Shark badge; I understand the API count may differ from qualifying achievement activity. PR https://github.com/wuser-lab/github-badges-quest/pull/6 merged on 30 October 2026 at 22:19:53 UTC. Its final commit c1d15ede9331748d0fe39e307d3d941756d98380 retains linked Codex co-author attribution. Pair Extraordinaire is not visible in the last profile check. Could you clarify whether these events qualify and whether this matches the reported processing delay? I am not claiming that linked AI attribution guarantees eligibility.

Refresh the dates and observed state before using this draft. Never include billing details, private repository contents or personal email addresses in a public report.

## 4. Galaxy Brain: solve questions people actually have

Owner: account holder for each published answer; Codex can research and reproduce. Planning budget: two 45-minute triage sessions and up to two hours of reproduction work per week. Goal: two independently accepted answers, with no guaranteed response date.

Start with [Vite Q&A](https://github.com/vitejs/vite/discussions/categories/q-a) and [Vitest Q&A](https://github.com/vitest-dev/vitest/discussions/categories/q-a). Vite is a direct project dependency; Vitest is an adjacent testing community. Prefer questions about project-path deployment, static assets, browser test behavior and reproducible JavaScript failures.

GitHub explicitly disabled achievements in its own Community Discussions on 6 February 2024; the announcement says other projects and communities are unaffected. Use Community only for appropriate GitHub feedback, not as the Galaxy Brain work queue. [Staff announcement](https://github.com/orgs/community/discussions/106536).

### Triage checklist

1. Open the latest Q&A list and read the complete thread, including replies and linked issues. Prefer recent activity rather than reviving dormant threads.
2. Choose a question with a reproducible gap and no equivalent complete answer. An "Unanswered" label only means no reply has been accepted.
3. Read that project's contribution and AI-content rules. If assistance is restricted, follow those rules and let the account holder write the permitted response.
4. Reproduce the problem at the author's stated versions. Write down the exact command, actual result, proposed change and result after the change.
5. Prepare a concise answer with the explanation, minimal fix, primary documentation link and honest testing limits. Include AI disclosure where required. Never invent a successful reproduction.
6. Publish only after the answer has been reviewed and posting is authorized. Respond to follow-up questions; do not ask for acceptance for badge purposes.
7. Log the answer permalink. Count it only when the discussion author or maintainer actually accepts it. Check the badge separately.

### Threads reviewed during this research

| Thread | Finding | Decision |
| --- | --- | --- |
| [Vitest #11415: Angular library migration](https://github.com/vitest-dev/vitest/discussions/11415) | Existing detailed configuration replies; still labeled unanswered | Skip a generic migration answer; revisit only with a tested unresolved case |
| [Vitest #11579: wrapper CLI completion](https://github.com/vitest-dev/vitest/discussions/11579) | Maintainer replies address the stability question | Skip; a third-party answer cannot promise a maintainer's API contract |
| [Vite #20690: file-size logging](https://github.com/vitejs/vite/discussions/20690) | Existing replies already discuss configuration | Skip a duplicate answer |

These are research exclusions, not a claim that two ready-to-post solutions have been found. The next session should select fresh questions using the checklist.

## 5. Starstruck: one useful project and a measured public launch

Owner: wuser-lab. Focus: [Consent Lens](https://github.com/wuser-lab/consent-lens), not the badge quest repository. Goal: 16 genuine stars on this repository. The present gap is 14; growth is not guaranteed.

The concrete audience is developers comparing consent signals, CMP implementers and technical reviewers who need documented before/after evidence. Lead with the workflow and its limits. Real adoption and time savings have not been measured, according to the [project README](https://github.com/wuser-lab/consent-lens/blob/main/README.md).

### Launch readiness, before external promotion

- [x] Public project and hosted demo already exist.
- [x] Synthetic examples, workflow screenshots and offline edition are documented.
- [x] Project description and discovery topics updated.
- [ ] Confirm a cold visitor can load the synthetic example, compare signals, download a redacted summary, explicitly export a full JSON backup and reopen it.
- [ ] Verify the offline download and latest release links at launch time. Use synthetic data in shared screenshots.
- [ ] Record a short walkthrough showing the comparison, reviewer decisions and export choices.
- [ ] Decide whether to license the source, and add the chosen license if appropriate. Until then use "public source repository" rather than an open-source licensing claim.
- [ ] Check issue templates or contribution instructions so feedback has a useful destination.

### Public distribution sequence

1. Keep this sourced plan public in the existing badge repository.
2. After the readiness checks, prepare one project-relevant post for [Vite's Show and tell category](https://github.com/vitejs/vite/discussions/categories/show-and-tell), which was present in the live discussion index. Read current category rules and the code of conduct before posting; the category's existence does not guarantee moderator approval.
3. Ask for feedback on the export and review workflow. Link the running demo first and the public source second. Respond with concrete fixes or explanations.
4. If useful feedback produces a meaningful release, publish a changelog update and one follow-up in the original thread. Do not repost the same announcement across unrelated Q&A threads.
5. Record stars at launch, after seven days and after fourteen days. Also record actionable feedback and confirmed workflow trials. Avoid adding tracking to sensitive consent inputs just to measure promotion.
6. If stars do not grow, improve onboarding from observed feedback and reconsider audience fit. More announcement volume is not a substitute for a useful demo.

### Reviewable launch draft — GitHub Show and tell only

**Title:** Consent Lens: a browser workspace for comparing TCF v2 signals

I’m building Consent Lens to compare consent strings before and after a user action, document review decisions, and export the resulting evidence report.

You can try it with bundled synthetic examples: https://wuser-lab.github.io/consent-lens/

The workflow includes vendor-disclosure and publisher-restriction comparisons, optional lookup using a local matching vendor list, redacted summaries by default, full JSON backups for resuming a review, and a downloadable offline edition. The site uses Vite for its static build.

I’d welcome feedback on whether the comparison and export steps are clear, especially the distinction between a redacted summary and a full backup. It is a technical review aid; it does not certify legal compliance. The hosted page reaches GitHub, while the saved offline edition avoids those hosting requests.

Public source and current limitations: https://github.com/wuser-lab/consent-lens

This draft was prepared with Codex assistance using the project's documented behavior. The account holder should verify the launch checks before posting.

### Channels researched and excluded from automated promotion

- **Hacker News:** Show HN fits a runnable demo, but the current HN guidelines prohibit generated posts and automated posting. A future submission would need the account holder's own writing and manual participation. This draft is not intended for HN. [Show HN rules](https://news.ycombinator.com/showhn.html); [HN guidelines](https://news.ycombinator.com/newsguidelines.html).
- **DEV:** Disclosure alone is insufficient. Its AI guidelines restrict promotional and clout-seeking AI articles and prohibit generated comments. Do not post this badge-driven launch draft there. A future technical article would need a genuinely educational purpose, the author's understanding and compliance with the then-current rules. [DEV AI guidelines](https://dev.to/guidelines-for-ai-assisted-articles-on-dev).

## 6. Public Sponsor: optional, bounded and reviewable

A concrete candidate is [Anthony Fu's GitHub Sponsors page](https://github.com/sponsors/antfu?frequency=one-time). The official [Vite team page](https://vite.dev/team) lists him as a core contributor, and Vite is a direct Consent Lens dependency. The inspected sponsor page offers a custom one-time amount.

Proposal only: a one-time payment with a maximum total of US$5, if accepted by checkout and explicitly approved by the account holder. No payment is authorized by this plan. If fees, tax or a recipient minimum would exceed the approved total, stop and revise the proposal.

At checkout verify the paying account is wuser-lab, frequency is one-time and visibility is public. Review the recipient, final total and payment details before completing. Store the receipt privately, then verify the award on the live profile. Do not publish billing data. GitHub documents one-time and recurring choices and a sponsorship visibility choice. [Official sponsorship instructions](https://docs.github.com/en/sponsors/sponsoring-open-source-contributors/sponsoring-an-open-source-contributor-through-github).

## 7. Useful contribution queue and higher tiers

Existing upstream work is a better starting point than manufactured PR volume. Recheck the live status of these existing submissions before doing more work:

| Existing PR | Next useful action | Who controls merge |
| --- | --- | --- |
| [IAB TCF #515](https://github.com/InteractiveAdvertisingBureau/iabtcf-es/pull/515) | Review new feedback on listener-error isolation; rerun affected checks if changed | Upstream maintainers |
| [IAB TCF #516](https://github.com/InteractiveAdvertisingBureau/iabtcf-es/pull/516) | Keep package-migration documentation aligned with maintainer feedback | Upstream maintainers |
| [IAB TCF #517](https://github.com/InteractiveAdvertisingBureau/iabtcf-es/pull/517) | Address feedback on service-specific encoding and its regressions | Upstream maintainers |

These links are work candidates, not permission to merge upstream or a prediction of acceptance. Keep each future PR independently useful, with appropriate validation and accurate co-author credit. For higher tiers, use the catalogue milestones in section 2 and the profile's actual awarded tier. Do not plan hundreds of trivial PRs or pressure maintainers to satisfy a counter.

## 8. Schedule and decision points

This is a proposed 28-day work schedule beginning 31 October 2026. It is not an automation or an award deadline. Initial effort budget: approximately 8–12 hours across the first two weeks, then adjust to feedback.

| When | Work and deliverable | Checkpoint |
| --- | --- | --- |
| 30 October | Publish this research plan; preserve the starting evidence | Public plan readable |
| 31 October–2 November | Badge evidence packet, cold-visitor demo check, first Q&A triage | Actual badge state recorded; launch defects listed |
| 3–6 November | Fix launch blockers; prepare one permitted showcase post; reproduce one suitable question | Tested answer or documented reason to skip |
| Around 6 November | Recheck awards and the GitHub incident | One support/feedback report if still warranted |
| 7–13 November | Run the reviewed launch; answer follow-ups; reproduce further useful questions | Feedback log and accepted-answer links |
| 14–20 November | Make a release responding to real feedback; continue relevant Q&A | Repeatable demo and seven-day growth reading |
| 21–27 November | Review fourteen-day growth, actual awards and effort spent | Continue, revise audience, or close low-value work |

Public sponsorship can be completed separately once the recipient and final spending cap are approved. Human writing and participation are required for any future HN activity. External public posts should be reviewed in their exact destination before submission.

## 9. Scoreboard and definition of done

| Metric | Baseline | Completion evidence |
| --- | --- | --- |
| Ordinary achievements visible | 3 | Live profile displays each award; candidate activity alone is insufficient |
| Pair Extraordinaire candidate | One verified merged co-authored guide update | Award visible, or GitHub clarifies eligibility |
| Pull Shark | Base tier visible; API search returned 18 merges | Profile displays bronze, or discrepancy is investigated with evidence |
| Galaxy Brain | No accepted answers verified in this audit | Two accepted-answer permalinks and a separate profile check |
| Consent Lens stars | 2 | Repository reaches 16 and profile award is checked |
| Sponsorship | No new sponsorship executed | Approved public one-time sponsorship and live award verification |
| Public launch | Draft only | Actual post URL plus launch-readiness record |
| Finishing Touch | Public qualification route unverified | Credible qualifying route established before any execution promise |

Update the scoreboard after meaningful events, not every refresh. Keep launch drafts and planned tasks visibly separate from completed actions. A realistic success target is the seven ordinary achievements over time; eight cannot be promised while Finishing Touch access is unresolved, and all fifteen cannot be acquired through ordinary new activity.

## 10. Decisions still needed

Only decisions that affect execution remain: the license choice if the source is to be offered under an open-source license; approval of a specific sponsor and final spending cap; and review of the exact external post or answer before submission. Research, public-plan publication and preparation do not require those decisions.

All sources were checked on 30 October 2026. Recheck changing community rules and live thread state immediately before external publication. This plan intentionally contains only public project information and public account activity.
