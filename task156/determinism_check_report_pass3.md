# determinism-check report, task156, 2026-10-27 (pass 3, run r3, target.zip f17b387d)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated thread (verdict at /tmp/determinism-check-task156-r3/verdict.md) reproduced the 32-FTE request, the per-site split 5/2/6/4/4/2/4/3/2, the 6 FTE over the 26-FTE envelope, and tables 4, 5 and 6 cell for cell (27, 27 and 9 cells). The charter fixes the estimand, the handbook's invitation-only clause closes the "no new reviewers" premise, and the data separate the method candidates. The total stays 32 across every reasonable variant; the nearest site is 0.17 FTE from a .5 boundary (Frontend & Web 5.33).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Reviews per reviewer per month (101 saturated site-months) | about 40 | 39.83 pooled, 39.73 mean | yes |
| Tenure hazard, year 1 / from year 4 | about 9% / under 1% | 9.1% / 0.9% falling to 0.5% | yes |
| Active reviewers 2027 mean | about 8,800 | 8,814 (monthly) / 8,778 (yearly) | yes |
| Site FTE (unrounded) | 5,2,6,4,4,2,4,3,2 | 5.33, 1.85, 6.23, 4.14, 4.13, 1.99, 4.00, 3.00, 2.00 | yes |
| Request / over envelope | 32 / +6 | 32 / +6 | yes |
| Ask 4 (24-hour response) | 27 cells | 27 cells exact | yes |
| Ask 5 (hours by quarter) | 27 cells | 27 cells exact | yes |
| Ask 6 (2026 vs 2022 questions) | 9 values | 9 values exact | yes |
| Slide 2 envelope line | 3,467 h/month | 3,466.7 | yes (the 48-month series was not rebuilt cell by cell) |

## Competing answers that survived
None on the main call. Routes the thread priced: constant 10,607 pool 24, pooled flat lapse 40, tenure curve from access date 27. Each is a method error the data exposes. Advisory on ask 5 only: the WFM `site` column equals each person's current site, so it contradicts the effective-dated assignments for 1,194 approved lines (the six movers' pre-move shifts). The assignments file and the handbook sentence "site the moderator worked for on that shift" close it. Low residual risk, not a fork.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / big file | 10+ / 3+ / 25,000 rows | 22 / csv, pdf, xlsx / 49,530 rows (question_moves) | yes |
| Distractors | 2+ in metadata.json, none named in a file | pageviews csv, AI-assistants survey pdf; the file names do not label them | yes |
| Distractors unused yet weighty | yes | thread found them unused; a second superseded 2 Oct pull is dominated by the 8 Oct pull | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | three 9-site by period tables; the prompt states whole FTE, nearest hour, one decimal | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape is identifiable; criteria count is generated downstream and was not checked here (rubric not in folder) | partial, not checked |
| Not LLM-flavoured; goldens realistic | yes | thread found no authoring disclosure; golden realism was cleared by earlier gates | yes (not independently re-read) |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.
Card and note: stump_class analytical; the stump is the stop rate read off the open pool versus the closed pool's tenure curve. Match. The declared distractors (pageviews, survey) are not the surface read carrying the task. Minor numeric difference: the note's R3 default is 41 (per-site lapse rate), and the thread's flat network lapse route gave 40. This is the same family and lands on the same side of the golden, so it is not a finding.
Gate H: domain pass, layers pass, decisive_step analytical. The card's analyst_test and domain_test agree with it: survival by tenure from a left-truncated roster, not a pooled churn rate. The design note's Three rules section is present.

## Stump power (Gate F)
Weighed against the design note's ladder only (no solver was run, per the STOP block). The golden 32 is bracketed by 22 to 27 below and 38 to 47 above, and the nearest wrong request is 27, five FTE away. The note puts P(one strong solver lands) at about 0.25 and P(both) at about 0.08. The thread independently priced the wrong routes at 24, 27 and 40, consistent with the ladder. The thread did not class the decisive step as analytical merely because the method is standard: the left-truncation handling and the saturated-month capacity are judgment calls the data had to settle. No concern.

## Findings, ranked
1. Advisory only (ask 5): stale WFM site label, closed by the assignments file and the handbook sentence. An optional handbook pin would change what solvers see and would need a rerun; not recommended.
2. The 48-month chart series was not rebuilt cell by cell by the thread. The inputs are pinned.
3. The 25-criteria rubric count was not verified in this pass.

## Next action for the author
No FIX_NOW item. Proceed to ship the build at target.zip f17b387d.
