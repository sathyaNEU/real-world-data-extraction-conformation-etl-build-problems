# determinism-check report, task267, 2026-11-01 (pass 5)

Judged on the prompt after the pass 4 repair (billing ask "for each month from March to November"). target/ and submission.md unchanged since pass 4.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (verification-bias reweighting), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed figure reproduces. Protocol 4.2 and 6.2 force the partial-verification weighting. The pass 4 December fork is closed by the March to November window.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Adults | 37,269 | 37,269 | yes |
| Complete OGTT / diabetes | 10,715 / 1,117 | same | yes |
| Six rule shares | 51/79/80/62/90/93; 8.4/24.9/28.2/35.9/36.3/49.3 | same | yes |
| Cartridges A01 to A12, total | 40,248 | same | yes |
| Billing March to November, net / adults screened | 415,800.00 / 409,255.00 | same, all nine pairs | yes |

## Competing answers that survived
None that moves a committed answer. Weighting variants (x5 draw, month x group strata, inverse draw probability) give the same call. Residual forks: credit month (memo date versus the reversed test's date), which the ask resolves as the test done that month; unfiled UTC twins, which are discoverable from the exact 4h/5h pattern; zero-padding of six-digit IDs, which is forced by protocol 4.3.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files, formats, rows | 10+, 3+, 25k+ | 12, 4, run log 49k | yes |
| Distractors | 2+ in metadata, none in a file name | feedback, 2024 profile named | yes |
| Deliverables | 1 to 3 | 2 | yes |
| Unit and rounding in asks | yes | yes | yes |
| Rubric 25+ criteria | 25+ | not verifiable from the pack | open |
| Realism | no LLM tells | none found | yes |

## Gate G reconciliation
The thread's mechanism and stumping_family match pass 4 and the design note. No declared distractor carries the task.

## Gate H
domain pass, layers pass, decisive_step analytical.

## Stump power (Gate F)
The easy route (unweighted among complete tests) gives R26A60 at 94% and is wrong. Protocol 6.2 states the denominator ("counting every adult screened"), so a strong analyst may weight correctly. The thread flags a risk that the main call is too easy. The asks carry heavy independent difficulty (UTC twins, loaner serials, credits). The main thread should weigh this against the design note's ladder.

## Findings, ranked
1. No determinism finding.
2. Stump-power watch: the 6.2 wording hands over the weighting.
3. The rubric count is unverified.

## Next action for the author
Ship. Optionally weigh the 6.2 wording against the ladder.
