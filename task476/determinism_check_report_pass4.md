# determinism-check report, task476, 2026-11-01

## Verdict
NOT_DETERMINISTIC (Gate C/E fork on the start of a survey-found leak)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Guidelines 2.2 pin the start only for odor-called leaks. The 613 survey-found 2026 leaks (69 percent of 891) have no filed start. The golden needs the expected start between the 2025 survey and the find, weighted by the odor-call month profile; no shipped text says so. The designated set depends on it: seasonal 5, midpoint 3 (Ashby, Elmwood, Ivers), find 0, previous survey 12. Governing label: underspecified_objective. Full thread output: /tmp/determinism-check-task476-73667/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Leaks found per district (12) | 72,78,68,49,114,89,68,88,79,70,52,64 | same | yes |
| Dec-Mar start share | 62.6% | 62.60% local | yes |
| Designated set | 5 | 5 under golden convention only | yes, convention unfiled |
| Costs (12) | per submission | end-2026 less end-2025 matches to the dollar | yes |
| Interruptions (12) | per submission | dedupe, meters per line, match | yes |

## Competing answers that survived
Start of a survey-found leak. Seasonal expectation (golden) gives 5. Midpoint or uniform gives 3. Find gives 0. Previous survey gives 12. No shipped rule closes it. Design note SF9 closes only day-versus-month weighting, not the start convention. Lesser points (cumulative cost lines, shared service lines) are inferable and recorded as semantics.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10 / 3 / 25k rows | 12 / csv, pdf, xlsx / 100,932 and 71k rows | yes |
| Distractors | 2+ named, none in a file name | customer_counts xlsx, lauf report pdf (in metadata.json) | yes |
| Deliverables | 1 to 3 | 2 (xlsx, pdf) | yes |
| Asks with unit and rounding | yes | yes | yes |
| Rubric 25+ criteria, no LLM tells | yes | not checkable here (generated downstream) | not assessed |

## Gate G reconciliation
Thread: method_or_model_selection, analytical_non_defect, surface_read no, defect no. Design note: Layer 2 estimation_fit, ladder R0 to R2 then G, declared distractors are per-customer normalisation only. Match; no distractor carries the task. The mismatch is on determinism, not classification.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical (expected start under the odor-call profile; the midpoint route files 3 districts).

## Stump power (Gate F)
Real: the textbook midpoint route lands wrong (Ashby over, Brennan Hill and Fenwick out). Fork-is-the-stump test FIRES. The decisive step is choosing the seasonal expected start over the midpoint, and the sentence that closes the fork ("expected start given the seasonal pattern of confirmed-call starts") names exactly that step. Filing it makes the call rule application; leaving it open is a semantic fork. The design note's Layer 2 and SF table say the same: the start convention is both the open fork and the stump. The thread's suggested Fix (filing the expectation) would therefore convert the stump into rule application.

## Findings, ranked
1. Unfiled start convention for survey-found leaks decides the call (SEND_BACK).
2. The only closing sentence files the HOW, so a closing repair breaks Rule 3. Needs a re-root or a different closure: the data must separate the candidates, e.g. a filed selection criterion plus back-test over the 2016 to 2025 calls (see determinism-check section 1), not a filed method.
3. Minor: cumulative cost lines and line-sharing are inferable, not stated.

## Next action for the author
Do not file the seasonal expectation. Either file a selection criterion (for example, the start estimate must reproduce the called leaks' known starts out of sample) that forces the method with data separating the candidates, or re-root the decisive step.
