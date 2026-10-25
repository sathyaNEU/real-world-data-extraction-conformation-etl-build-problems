# determinism-check report, task179, 2026-10-25

One isolated judge thread (general-purpose, sonnet, medium) on a fresh unzip of target.zip c8032390, licensed by
`/fix-determinism` step 6 after portal round 3. The thread's own report is `scratchpad/determinism-check-task179-r6/verdict.md`,
with `blind_derivation.md` beside it.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The order was kept: the blind derivation went to disk before the graded blocks were opened, and the blind call was
2,250 (attributes and week-6 ratings, with or without class size), wrong against the golden. The thread then built the
peer-exposure count from the class extracts and confirmed the golden independently: the filed lowest-AIC criterion
picks the count (about 1,100 AIC units better than the attribute models), and every AIC-competitive form lands inside
3,125 to 3,375. The round-3 portal fork (the count read as measured differently across the cutover) did not survive:
the cutover notes' section 6 files the class record as the same in both systems, and the record's own entrants meeting
fewer than 10 others twice (11,640, 5,029 not enrolled) are under-predicted by the count-free model (4,165.9 against
the write-up's 4,166.2).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Call, not enrolled at the 2027 census (nearest 250) | 3,250 (3,253.0) | 3,252 to 3,254 (3,253.7) | yes |
| First-time entrants enrolled at the 2026 census | 8,659 | 8,659 | yes |
| 2026 entrants meeting no other entrant twice | 3,778 | 3,778 | yes |
| 2019 to 2025 entrants meeting fewer than 10 twice, not enrolled | 11,640, 5,029 | 11,640, 5,029 | yes |
| Count-free model's prediction for them | 4,166.2 | 4,165.9 | yes (the mean-rating specification) |
| Teaching-group cells (20) | as filed | all 20 exact (575 groups) | yes |

## Competing answers that survived
none. Tested: the pooled or last-intake rate and a trend (2,117 to 2,146, 2,000 or 2,250), class size added (2,194),
a log count (3,118, 3,000, loses on AIC to the step forms), flags at 3 to 18 (3,193 to 3,254, all 3,250), the
low-exposure stratum alone (a different sample from "the same intakes"); for ask 2, the list without the census filter
(closed by the conventions' sections 2 and 4), per class or per meeting set (closed by the prompt's clause and the
three-groups sentence).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 15 | yes |
| Formats | 3 or more | csv, xlsx, pdf, txt | yes |
| Large file | 25,000 rows or more | census history 202,053 rows | yes |
| Distractors | 2 or more, named in metadata.json | hall occupancy, school leavers, transfers, catalogue | yes |
| Deliverables | 1 to 3, all in the golden | xlsx and png | yes |
| Asks | unit and rounding stated | nearest 250; whole numbers | yes |
| Rubric | 25 or more criteria | the call, 2 components, 20 cells, the chart, 2 files | yes |

## Gate G reconciliation
The thread's mechanism (method or model selection under a covariate shift in a structural predictor), family
(analytical_non_defect) and Gate H line (domain pass, layers pass, decisive step analytical) match the card
(`stump_class` analytical; the analyst test files 2,250 from the validated early-warning model) and the design note's
`## Three rules`. No distractor named as the surface read.

## Stump power (Gate F)
Strong on the thread's own evidence: its blind call was the default path's 2,250. The scored reader on the same zip
also filed 2,250 and kept 0 of 20 cells.

## Findings, ranked
none blocking. The thread's thin spot (a solver who fits only a log count files 3,000) is SF13, closed by SELECT_PIN.

## Next action for the author
Reship: the repair moved no frozen figure (`freeze.py check --mode determinism` PASS).
