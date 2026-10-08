# RC25 — CI failures jumped from 12% to 21% of builds: flaky tests, broken dependencies, or worse code?

| Field | Value |
|---|---|
| Category | Root Cause Analysis |
| Mirrors | Build and deploy pipeline reliability at large engineering organisations (Google TAP, Meta Sandcastle, Microsoft CloudBuild), where flaky tests and upstream breakages masquerade as code defects |
| Domain | Software engineering / developer productivity |
| Task shape | 18 · Hypotheses versus evidence (failed builds × evidence: same-commit outcome disagreement, cross-branch simultaneous breakage fixed by build-file changes, source-change failures fixed by source changes, build-type mix; the remediation funded) |
| Core method | Classify each failed build of the project by deterministic evidence rules: flaky (the same commit has both passed and failed builds, or the failed tests pass on the next build with no source or test change), dependency (failures across ≥ 3 different branches/PRs within 24 h that end with a commit touching only build or dependency files), code (failed build whose commit changed source files and the next passing build changes source files); bridge the failure-rate change into build-type mix (PR vs push) and class-specific rate changes |
| Analytical stump | Failure rate is read as a code-quality signal and attributed to recent changes. But PR builds fail far more often than push builds, so a shift toward PR-heavy development raises the overall rate with no change in either rate; flaky failures recur on unchanged commits; dependency breakages hit many unrelated branches at once. Attributing each failure to the commit that triggered it double-counts these shared causes |
| Primary sources | TravisTorrent (Beller, Gousios & Zaidman, MSR 2017): Travis CI build metadata joined with GitHub commit and pull-request data |

## 1. The real-world situation

The platform team of a mid-size open-source project saw the CI failure rate rise from 12% to 21% of builds over a quarter. Maintainers blamed
newer contributors' code quality and proposed stricter review gates. Others pointed to intermittent tests and an upstream library that broke the
build several times. The team has budget for one of three programmes: flaky-test remediation, dependency pinning with automated upgrade PRs, or
tighter pre-merge review.

## 2. The decision (one deterministic recommendation)

**The programme funded — flaky-test remediation, dependency pinning, or review gates — according to which failure class contributes most to the
increase in the failure rate, after removing the build-type mix effect, with the classified failure counts.**

Rules (platform memo):

* Data: TravisTorrent builds for the memo's project; reference and current quarters by build start time; one row per build (deduplicate jobs to
  builds by build ID; a build fails if its status is failed; errored and cancelled builds excluded).
* Build type: PR build if the PR flag is true, else push build.
* Failure classes, applied in order: flaky → dependency → code → unclassified.
  * Flaky: another build of the same trigger commit has passed; or the next build on the same branch passes with zero source and test churn.
  * Dependency: within 24 hours, failed builds on ≥ 3 different branches/PRs; the first subsequent passing build on any of them changes only files
    matching the memo's build-file patterns (dependency manifests, lockfiles, CI configuration).
  * Code: the trigger commit has source churn > 0 and the next passing build on the branch has source churn > 0.
* Bridge of the failure rate F = Σ_type share_type × F_type: mix = Σ Δshare × F_ref,type; within = Σ share_cur × ΔF_type; each type's within change
  is split across classes by the change in class-specific failure rates.
* Fund the programme mapped to the class with the largest within contribution (flaky → remediation, dependency → pinning, code → review gates).

## 3. Why capable analysts get it wrong

* Failure rate looks like a property of the code.
* PR and push builds have very different base rates.
* Shared causes (one broken dependency) produce many failed builds that look independent.
* Flakiness needs same-commit comparisons, not per-build views.

## 4. Input package

| # | File | Format | Approx. rows | Source | Licence | Role |
|---|---|---|---|---|---|---|
| 1 | `travistorrent_8_2_2017.csv` | CSV | ~3.7M job rows | TravisTorrent (MSR 2017 data showcase) | CC BY 4.0 (dataset terms; verify) | Build and commit data |
| 2 | `travistorrent_field_descriptions.html` | HTML | ~60 fields | TravisTorrent | Same | Field definitions |
| 3 | `project_commit_files.json` | JSON | ~20k commits | GitHub REST API (public repository commit file lists) | Repository licence for metadata; GitHub API terms | File paths changed per commit |
| 4 | `platform_memo.pdf` | PDF | — | Task author | — | Rules in §2, build-file patterns |
| 5 | `maintainer_review_gate_proposal.xlsx` | XLSX | — | Task author | — | The code-quality claim |
| 6 | `beller_2017_citation.pdf` | PDF | — | Cite | Cite | Dataset paper |

## 5. Deterministic solution path

1. Filter the project; collapse jobs to builds; exclude errored/cancelled; assign quarters and build types.
2. Join commit file lists; compute churn categories and build-file-only flags.
3. Apply the class rules in order; count by class, type and quarter.
4. Bridge F into mix and within-type changes by class.
5. Fund the mapped programme; contrast with the review-gate proposal.

## 6. Wrong paths (method errors, not misreadings)

**A — failure rate by contributor or commit.** Attributes shared causes to whoever triggered the build.

**B — ignoring PR/push mix.** A shift in build mix is read as worse code.

**C — job-level counting.** Matrix jobs multiply failures for multi-environment builds.

**D — flakiness from test names alone.** Without same-commit evidence, intermittent and genuine failures cannot be separated.

## 7. Why the stump is analytical, not semantic

Classification rules use commit identity, timing and file patterns; nothing depends on reading logs. The trap is attributing shared and
non-deterministic failures to individual changes and ignoring build-mix.

## 8. Draft task prompt (prose)

> CI failures nearly doubled and maintainers want stricter review. Classify the failures with the platform memo's rules, separate build-mix effects,
> and tell me which programme to fund. Provide `failure_classification.csv` (build: type, class, evidence), `failure_rate_bridge.png`, and a one-page
> `ci_reliability_decision.pdf`.

## 9. Deliverables

* `failure_classification.csv` — every failed build with its class and evidence fields.
* `failure_rate_bridge.png` — waterfall from F_ref to F_cur: mix, then within-type changes by class.
* `ci_reliability_decision.pdf` — programme funded, counts by class, and why the review-gate proposal is or is not supported.

## 10. Where 25+ rubric criteria come from

* Build counts after deduplication and exclusions by quarter and type: 6.
* Class counts by quarter: 8.
* F_type and shares by quarter: 6.
* Bridge components and closure: 5.
* Decision and contrast: 3.

## 11. Golden-output checklist

* Jobs collapsed to builds; errored/cancelled excluded.
* Class precedence; 24-hour and ≥ 3-branch dependency rule; build-file patterns.
* Mix/within bridge with closure.

## 12. Build notes (scope tuning)

* Choose a project whose PR share rose sharply between quarters and which had at least one multi-branch dependency breakage; confirm that code
  failures are not the largest within contributor.
