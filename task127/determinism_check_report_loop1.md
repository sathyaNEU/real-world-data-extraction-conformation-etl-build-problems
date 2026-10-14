# determinism-check report, task127, 2026-10-14 (loop 1, architecture 2)

## Verdict
NOT_DETERMINISTIC (every golden figure reproduces; the package split is not forced by the shipped text)
**Disposition:** SEND_BACK
**Stumping type:** mechanism: binding_constraint plus counterfactual cohort and estimand selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The split of the 1,200 packages, and every figure in d2a_package_split_winter_2026-27.xlsx, rests on two readings that no shipped file states.
1. Cohort. Allocation note SF-2026-14 s.3 covers patients "medically optimised for discharge home on pathway 1" who "need a new package". The golden adds 86 patients who left on pathway 2 or 3, picked out only by a Cancelled hospital referral received on the ready date or the day before. No file says a withdrawn referral means pathway-1 intent.
2. Value. "Nights by which a package would have shortened their stay" is credited only from the later of the ready date and the ICES equipment delivery. No file says equipment gates discharge (the records show it; no sentence files it).
Each reading alone flips the split. Gates C and E fail. Taxonomy: underspecified_objective. The thread ran on a fresh unzip of target.zip with the judge system prompt inlined; verdict at /tmp/determinism-check-task127-loop1/verdict.md.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pathway-1 new-package patients, ready 1 Dec 2025 to 28 Feb 2026, Marchshire ICB practice (latest submission per spell; acute_discharges, gp_practices) | 1,538 (RM 484, W 329, H 112, C 265, A 348) | same | yes |
| Cancelled-referral pathway 2/3 patients (brokerage_referrals) | 86 (RM 24, W 21, H 8, C 20, A 13); covered 508/350/120/285/361 | same; they average 23 to 26 nights against about 8 for the rest | yes |
| Nights saved per covered patient (ices_order_lines) | 7.37 / 7.24 / 6.34 / 5.23 / 4.04 | 7.374 / 7.240 / 6.342 / 5.228 / 4.044; 789 with delivery; min or max line gives the same | yes |
| Split and bed-days | 508/350/120/222/0; 3,746/2,534/761/1,161/0; 8,202 | same (8,201.63 unrounded) | yes |
| Delayed bed-days and patients grid (ward at midnight, night dated to its evening; acute_ward_stays, ward_reference) | 15 cells; total 24,777 | match in all 15 cells, both measures | yes |
| Referrals with care start within 7 days, by district and month (brokerage_referrals, spot_care_invoice_lines, postcode_districts) | 9 cells | match in all 9 cells | yes |

## Competing answers that survived
| Reading | Split RM / W / H / C / A | Bed-days |
|---|---|---|
| Golden | 508 / 350 / 120 / 222 / 0 | 8,202 |
| Pathway 1 only, equipment-adjusted | 484 / 329 / 112 / 265 / 10 | 6,751 |
| Pathway 1 only, ready date to discharge (the literal s.2 and s.4 wording) | 258 / 329 / 0 / 265 / 348 | 10,199 |
| 86 included, ready date to discharge | 204 / 350 / 0 / 285 / 361 | 11,333 |

Ashby Vale is first or last depending on the reading. Smaller forks, less contestable: the delayed grid attributes each night to the ward's hospital at midnight, not the discharging site_code (638 of 24,777 nights differ); "took" is read as Started plus Closed with spot care; the spot-care start is the earliest invoice line.

## Spec gates
Items marked (thread) come from the thread's hygiene read; (not checked) were not independently verified in this pass.
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | csv, txt, xlsx, pdf | yes |
| Large file | 25,000 rows or more | acute_ward_stays 138,831 rows; acute_discharges 65,559 | yes |
| Distractors | 2 or more in metadata.json, none labelled in a file name | weekly return, bed census, reablement xlsx (names carry no label); relevance and arithmetic ruled-out (thread) | yes |
| Deliverables | 1 to 3, all in the golden | 2 (xlsx, svg); both present in golden/ | yes |
| Asks multi-dimensional with unit and rounding | yes | split by hospital, 3x3 district-month grid, 5x3 chart; prompt states whole numbers | yes |
| Prompt shape and 25 or more rubric criteria | identifiable, 25+ | shape 05 named in metadata; rubric count | shape yes; count not checked |
| Reads as real, not LLM generated | yes | no authoring language, coherent dates (thread); golden realism not reviewed here | yes (thread) |

## Gate G reconciliation
Thread: mechanism binding_constraint plus counterfactual cohort and estimand selection; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no. Design note and card: decomposition_attribution with estimand_identification (binding constraint), analytical non-defect, no surface-read dependency; pass 2 of loop 0 said the same. These agree, and the declared distractors are not named as carrying the task, so there is no distractor finding.
Mismatch that matters: the note's fork table SF3 states the covered patients as "optimised for discharge home on pathway 1 with a new package" without the 86, and its Determinism item 3 says "the note never mentions equipment and puts the population at optimisation; the counterfactual is forced by the records". The thread found the population in the shipped note is pathway 1, so the records do not force the 86: they are an unfiled extension. The design note's own Watch item (equipment gate evidenced by records, not a filed sentence) is the failure the thread confirms.
Gate H (thread): domain pass; layers pass; decisive_step analytical, with the caveat that inferring intended pathway 1 from a withdrawn referral and "equipment gates discharge" approach data semantics and hidden-rule reading because no file states either. The easy route (pathway = 1, ready date to discharge) gives 258/329/0/265/348, so the call is not rule application. The fix must file the WHAT without turning the decisive step into a filed HOW.

## Stump power (Gate F)
Strong if the fork is closed. The naive route puts Ashby Vale and Cleeve Park first and gives 10,199 bed-days; the equipment constraint is what makes Ashby Vale none. The gap between readings is wide, but today part of it is interpretive, not clean analytical error.

## Findings, ranked
1. The cohort extension (86 withdrawn-referral patients on pathway 2 or 3) is not filed anywhere; the shipped note reads as pathway 1 only. Moves Ashby Vale from 10 packages to none.
2. The equipment-gated counterfactual value is not filed; the literal "nights a package would have shortened" reading gives ready date to discharge. Moves the call.
3. Gate H caveat: both unfiled readings sit near semantics or hidden-rule reading.
4. Minor forks (midnight ward attribution, "took", earliest spot start): less contestable, worth a sentence each.

## Next action for the author
Close the two forks by filing the estimand, not the method: in allocation note SF-2026-14 (or the prompt) state that the covered population is every patient medically optimised for discharge home who needed a new package to go home, whatever pathway they ultimately left on, and that a package's value counts only the nights the wait for home care alone caused; or ship an in-world council or trust note saying what a withdrawn hospital referral represents and that equipment must be in place before discharge. Then rebuild, update the fork table and checks.py to match, and run /fix-determinism for one re-judge. Prior solver runs are invalid once the text changes.
