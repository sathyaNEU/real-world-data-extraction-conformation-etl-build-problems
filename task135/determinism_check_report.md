# determinism-check report, task135, 2026-10-13

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (judge thread: no repair, no rerun)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread: general-purpose, sonnet, medium, one pass, reading only /tmp/determinism-check-task135-869192/target/. The thread's verdict is at /tmp/determinism-check-task135-869192/verdict.md and its brief at judge_brief.md. It was spawned by the main session because this runtime had no Agent tool.

## Why
Every graded figure reproduces from the bundle. The main call is forced by policy 4.1 (the standard deviation of the twelve-month return) together with the key facts PDF (funds dealt at 12 noon at latest available prices) and the shipped returns: the mandate's daily return correlates 0.196 with the North American fund's same-day return and 0.488 with its next-day return. Every estimator that carries the serial covariance into the twelve-month variance puts 60 inside the 10% cap and 70 outside it. Only the iid sqrt(252) scaling gives 70, and the shipped pricing facts contradict it. Watch item: the filed text never names the lag-adjusted estimator; the judge calls the sqrt(252) route and the shift-then-scale route (9.43 at 70) analytically wrong, not equally licensed, so this is a thin Gate C fork that the data separates, not a semantic one.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Mandate daily returns | 505 | 505, no jump above 3.3% | yes |
| Mandate 12m volatility to 30 Sep 2026 | Fernside 15.3% | 15.31% | yes |
| Vol at 60%: one-day lag / NW4 / NW5 | 9.3 to 9.6 | 9.59 / 9.30 / 9.28 | yes |
| Vol at 70%: same estimators | 10.6 to 11.0 | 10.98 / 10.64 / 10.64 | yes |
| Vol at 70%, iid sqrt(252) | 9.4 | 9.40 | yes |
| Vol at 80%, EWMA 0.94 | wrong 80 | 9.44 (90% is 10.58) | yes |
| Other multi-day estimators at 60 / 70 | inside / over | 21d 9.27 / 10.56, 252d 9.31 / 10.73, monthly x sqrt(12) 9.53 / 10.82 | yes |
| Mandate yield | 3.70% | £408,291 / £11,029,641 | yes |
| 2027 grant payments | £1,260,000 | £1,260,071 (35, 70 and midpoint lags all equal) | yes |
| Running costs | £328,949 | £328,949 | yes |
| Portfolio | £32,908,401 | £32,908,401 | yes |
| Income and release, 20 to 100% | nine pairs | all nine match to the nearest thousand | yes |
| Chart title step | 40% | 40% (£1,294,761 covers; 50% £1,221,261 does not) | yes |

## Competing answers that survived
- 63-day overlapping returns give 11.1 at 60 per cent, which would put the answer at 50. The judge does not count it: it is an unrequested quarterly horizon on two years of data, the policy specifies daily returns, and every other estimator agrees. Residual risk, not a surviving fork.
- Margin is clean across estimators: 0.4 to 0.7 points under the cap at 60, 0.6 to 1.0 over at 70.
- No other fork survived. The dividend dedup (one amount per designation, security and event; cash reconciles within £0.01), the 1 Dec 2025 window start and the grant lag range do not move any figure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 18 | yes |
| Formats | 3 or more | 5 (csv, txt, pdf, xlsx, docx) | yes |
| Large file | 25,000 or more rows | valuation lots 42,894 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | 3 named (benchmark index levels, Kestwick factsheets, Fernside report); no file name labels one | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | index levels refused by policy 4.2; factsheet and Fernside single-holding vols reproduce under daily scaling but name no portfolio volatility; none answers a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | grant payments and nine-step income and release in pounds to the nearest thousand; chart title rule | yes |
| Prompt shape and 25 or more criteria | yes | about 27 gradable figures (call, grants, 18 income and release, chart elements, plus critical components); the rubric itself was not generated in this pass, count is from the golden | yes, by count |
| Reads real, not LLM generated | yes | judge found none; hygiene PASS, nothing exclusion-level | yes |

## Gate G reconciliation
Thread: `method_or_model_selection`, `analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Design note and card: Gate G `method_or_model_selection`, stump strategy nonsynchronous pricing, surface_read_dependency no, sole_data_defect no, with the clean-data test asserting the default stays at 70 and the golden at 60 with every Layer 1 device repaired. These match. The thread names the iid sqrt(252) scaling and the EWMA as the easy routes, not the declared distractor (the benchmark index levels, refused by policy 4.2). Fernside's 15.3% daily-scaled figure is the cue to the easy route but does not carry the task: it is not a graded quantity and the data refutes the scaling it implies. No distractor-too-load-bearing finding.

## Gate H
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Layer 1: the custody export's per-lot repeated entitlements, corporate actions, euro and sterling mixes, mixed date formats. Layer 2: the twelve-month variance estimated with serial covariance from non-synchronous pricing against the policy cap. Easy route: same-day daily covariance times sqrt(252), which files 70 (9.4%); EWMA files 80. This matches the design note's Three rules (No decoy, Not semantics, Not rule application) and the card's analyst and domain tests.

## Stump power (Gate F)
Moderate to good, roughly half of strong runs estimated to fall. A model that cross-correlates the funds with the mandate finds the trap, and the files let it. The supplementary asks add the dividend dedup and window, and the 35 to 70 day payment lag with euro conversion.

## Findings, ranked
1. Watch item: the lag-adjusted estimator is not named in the filed text. The judge advises against naming it, as that would hand over the decisive step. Per CLAUDE.md, file the WHAT, not the HOW.
2. Residual: the 63-day overlapping estimate puts 60 over the cap (11.1). Dismissed by the judge as an unrequested horizon.
3. The rubric criteria count is inferred from the golden, not from a generated rubric.

## Next action for the author
Proceed to ship; no generator or prompt change is needed.
