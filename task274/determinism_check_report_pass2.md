# determinism-check report (pass 2), task274, 2026-11-02

## Verdict
DETERMINISTIC (no SOLUTION_WRONG). Re-judge after the pass-1 FIX_NOW (Resolution s3 now says unreached cases count "by how it will end, not as a case without a conviction").
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread executed the revised s3 and landed on the filed call: completing the 1,018 active participants through a life table (final review 23%, 91% of terminated cases convicted) gives 56% not offered, 38% offered, 18 points, pilot scale. The pass-1 fork (as-recorded 35.6 pp full scale) is closed by the new sentence; the thread lists it as a wrong easy route, not a licensed reading. No shipped file changed after the judged copy was cut (rebuild byte-identical, per the coordinator).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Lists | 1,801 / 1,807 | same | yes |
| Not offered convicted | 56% | 964 convicted, 89 pending, 56.1% | yes |
| P(terminated in term) | 39% | 38.6% | yes |
| Terminated convicted | 91% | 205/225 | yes |
| Offered convicted / reduction | 38% / 18 pp | 37.9% / 18.2 | yes |
| FY2026 classes | 1,962 / 655 / 1,219 / 1,125 / 947 | identical | yes |
| Divisions | 2,325 / 1,445 / 1,219 / 919 | identical (offense-date rule: 4,778 conversions, zero misses) | yes |
| Hours by site | 8,051 / 5,194 / 4,926 / 3,339 | identical | yes |
| Restitution by site | 37,165 / 33,175 / 25,530 / 19,325 | identical (old and new January reports have zero payers in common; new divided by 0.95) | yes |

## Competing answers that survived
1. 73 September 2025 starters whose term ends on the cut: left facing the final review gives 38.7% / 17.4 pp (asks could read 39 and 17). Same call. The thread flagged it; the design note's fork row SF23 closes it by data (the cohort's review terminations are dated before 31 August 2026, 16 of 110, and the provider's August report shows the other 73 Completed on 31 August 2026), asserted in `generator/checks.py`. Closed by a shipped fact, not by author intent; accepted.
2. Chart curve form (cumulative or not, window): concerns the chart ask only, no graded figure; consistency with the memo shares is the check.
3. Wrong-but-tested readings (drop pending 0 pp lapse; pending unconvicted 35.6 full; completed-cohort rate on all active 11.0 lapse; terminated undisposed at 56% about 26 full) are analytically wrong, not equally licensed.
4. January restitution pairing: superseding old with new gives 35,050 / 31,230 / 24,385 / 18,105 by site; the files rule it out (new January alone under half a normal month).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / large file | 10+ / 3+ / 25,000 rows | 28 files, csv xlsx pdf docx, 53,371 and 49,380 docket rows | yes |
| Distractors | 2+ named, no file name label | district_court_annual_statistics_fy2025.pdf, county_jail_population_2025_2026.csv | yes |
| Deliverables | 1 to 3, all in golden | 2 | yes |
| Asks with unit and rounding | yes | stated in prompt | yes |
| Prompt | under 1,000 chars | 949, unchanged | yes |
| Rubric 25+ | 25+ | not generated at this stage | not verified |
| Realism / not LLM generated | yes | thread: no authoring language, coherent dates | yes |

## Gate G reconciliation
Thread matches the card (maturity_censoring, analytical, gate_g forecasting). The declared distractors are not the surface read; the surface read is the as-recorded 36 pp. No finding.

## Gate H
domain pass, layers pass, decisive_step analytical; matches the card's `analyst_test` and `domain_test` and the note's Three rules. The thread reached the golden by building the life table the data required, not by executing a filed method.

## Stump power (Gate F)
Good. 1,236 of 1,801 offered cases open against 89 not offered; the recorded gap and the closed-case route both file the wrong tier. Margin 18 vs 15 holds across survival-conditioned variants (17 to 18). A strong solver can still diverge on estimator or January pairing, which lowers ask scores, not the call.

## Findings, ranked
1. Rubric count unverified (not a determinism matter).
2. Chart ask leaves curve form open; low risk.

## Next action for the author
Proceed to ship stage with the pass-2 pack; confirm the rubric reaches 25 criteria.
