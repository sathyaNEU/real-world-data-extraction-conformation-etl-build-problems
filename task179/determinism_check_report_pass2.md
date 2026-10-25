# determinism-check report, task179, 2026-10-25 (pass 2, portal round 4 rework)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Pack: target.zip 01124ef4 (the cutover notes' section 6 withdrawn after portal round 4 landed the call on c8032390;
every file the call reads is the first ship's). Thread: scratchpad determinism-check-task179-r7, order kept
(blind_derivation.md on disk before graded_blocks.md was opened); the thread's own blind call was 2,250.

## Why
The main call is forced by the 2026 intake's changed class structure. In 2019-2025 the median first-year entrant shared 2+ classes with about 26 other entrants (cohort blocks); in 2026 (ARC timetabling) 3,778 of 8,659 meet nobody twice and the median is 1. In history, entrants with fewer than 10 such peers leave at 43% (5,029 of 11,640, reproduced exactly) against about 20% for the rest. An attributes-plus-week-6 model, or any trailing rate, therefore gives about 2,140 -> 2,250, while the lowest-AIC model gives about 3,245 -> 3,250. The conventions fix the selection rule (lowest AIC over models fitted to the same intakes), and the AIC gap is about 930 points, so the data, not taste, separates the candidates. Asks (group counts) follow literally from conventions s2 and s4.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2026 first-time entrants enrolled at the census | 8,659 | 8,659 | yes |
| 2026 entrants meeting no other entrant in two or more classes | 3,778 | 3,778 | yes |
| 2019 to 2025 entrants meeting fewer than 10 others twice, not enrolled | 5,029 of 11,640 | 5,029 of 11,640 | yes |
| the call (lowest-AIC family) | 3,253.0, 3,250 | 3,239 to 3,259, 3,250 | yes |
| teaching groups, ten faculty and level pairs, two size classes | 20 figures | all 20 | yes |

## Competing answers that survived
None. Attribute-only or trailing-rate routes (about 2,140, 2,250; 2,000 on last year's rate) and other peer definitions
(one shared class 2,250; three shared classes 2,500; class size 2,250; the log count 3,000) are each dominated on the
filed lowest-AIC criterion, by 500 or more points except the log count by 23.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt | yes |
| Large file | one of 25,000 or more rows | census_enrolments_2019_2026.csv 202,053 rows | yes |
| Distractors | 2 or more in metadata.json, none named in a file name | 4 | yes |
| Deliverables | 1 to 3, each in the golden | 2 | yes |
| Asks | multi-dimensional, unit and rounding stated | 20 cells by faculty, level and size class, whole numbers | yes |
| Shape and rubric | identifiable, 25 or more criteria | shape 07, call and components plus 20 cells plus the chart's parts | yes |
| Realism | no LLM tells, goldens as work products | unchanged since the first ship's realism pass | yes |

## Gate G reconciliation
The thread's mechanism (forecasting under a covariate shift, analytical_non_defect, no surface-read dependency, no
sole data defect) matches the card's stump_class analytical and its analyst_test (the attribute model files 2,250).
Gate H: domain pass, layers pass, decisive step analytical.

## Stump power (Gate F)
Strong. The reported, correctly-read past (7 intakes of stable 24.5-25.6% attrition, an attribute model that back-tests perfectly) mispredicts 2026 for a real, supported reason (class-sharing structure collapsed under the ARC timetable). A strong model that cleans the data and fits an attribute/week-6 model, or extrapolates the rate, files 2,250 (or 2,000) instead of 3,250. Rule-reading alone cannot find it; it needs feature construction from the class rosters and a covariate-shift check.

## Findings, ranked
1. Advisory, no fix: none (fix location: none). Optional, if the author wants more insurance on determinism: nothing in the files states that class-sharing is the shift; leaving it unfiled is correct under the "no method filing" rule since the AIC gap decides.

## Next action for the author
Reship target.zip 01124ef4 and send it to the portal.
