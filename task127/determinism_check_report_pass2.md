# determinism-check report, task127, pass 2, 2026-10-12

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: binding_constraint (borderline: a lens-swap reading is possible), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Bundle integrity (pass 1 finding closed)
md5 of all 16 files in /tmp/determinism-check-task127-1791804577/target/ compared with a fresh unzip of task127/target.zip: all 16 identical, file by file (diff of the two md5 lists is empty). The shipped task127/target/ folder also matches the zip. The pass-1 stale-bundle problem (5 files differing) does not recur, so every figure below, including the ward-stay and ward_reference figures, was recomputed on the shipped pack.

## Why
Every committed answer reproduces from the shipped files. The 1,200-package split is forced by the filed rules: cohort = pathway 1, New package, a practice in gp_practices under NHS Marchshire ICB, ready date in the window, latest submission per spell, valued at the average nights a package would have shortened the stay, filled in value order up to each hospital's covered patients. The values (6.65, 6.24, 5.26, 4.36, 3.60) are well separated. Royal Marchford 508, Wendlebury 350 and Holmford 120 hit their caps, Cleeve Park takes the remaining 222 and Ashby Vale gets none. The one place the text is silent is that equipment gates discharge. The data settles it: all 789 equipment-matched pathway-1 patients left on or after delivery and none before. The literal-nights reading (10,425 bed-days, Ashby Vale and Cleeve Park first) is contradicted by that evidence. The thread rates the residual fork low to moderate and calls it the intended analytical step, not a semantic one.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Latest-submission cohort by hospital (RMC01, RMC02, RSM01, RSM02, RSM03) | total 1,624; 508 / 350 / 361 / 285 / 120 | 1,624; 508 / 350 / 361 / 285 / 120 | yes |
| Equipment-matched pathway-1 patients | 789, none left before delivery | 789; 0 before; 129 + 101 + 12 left on the delivery day at Ashby Vale, Cleeve Park, Holmford | yes |
| Mean nights saved (Royal Marchford, Wendlebury, Holmford, Cleeve Park, Ashby Vale) | 6.65 / 6.24 / 5.26 / 4.36 / 3.60 | 6.648 / 6.240 / 5.258 / 4.361 / 3.598 (min vs max delivery over lines gives the same) | yes |
| Packages | 508 / 350 / 120 / 222 / 0 | same | yes |
| Bed-days | 3,377 / 2,184 / 631 / 968 / 0 = 7,160 | same; unrounded 7,160.23, sum of rounded 7,160 | yes |
| Wrong-basis total (nights after ready) | 10,425 | 10,425 (Ashby Vale 361, Cleeve Park 285, Wendlebury 350, Royal Marchford 204) | yes |
| Delayed nights Dec 2025 to Feb 2026 | 23,541 | 23,541 | yes |
| Delayed bed-days and patients, 15 hospital-month cells each | as in the golden chart table | all 15 cells match for both bed-days and patients | yes |
| Brokerage within 7 days (Ashby / Marchford / Teme Valley), Dec | 34 / 169 / 92 | same | yes |
| Brokerage, Jan | 35 / 189 / 96 | same | yes |
| Brokerage, Feb | 39 / 146 / 77 | same | yes |

The ward-attribution method is latest submission, nights from the ready date to the discharge date, each night dated to the evening it began, hospital = ward site at that midnight (every night matched to exactly one ward stay), patients = distinct patients with at least one such night. The brokerage method is month received, district from the postcode lookup after case and space normalisation, start = start_date else first service_start in the spot invoices (242 closed referrals).

## Competing answers that survived
None survive as defensible. The thread tested and closed:
- No spot starts: counts drop (for example Ashby 28 / 32 / 31). Closed by the council notes and the spot-invoice note, which make the first service_start the care start.
- Month by start month, or the wait as "fewer than 7": different counts. Closed by the council notes (month received, calendar days) and the prompt ("no more than seven days").
- Cohort window as "ready state overlapping the window": 540 / 369 / 387 / 312 / 122, which would change the split. Closed by the filed field ("date the patient was medically optimised", a single date). Low risk.
- Delayed nights by discharging site instead of ward at midnight: many cells move (for example Ashby Dec 1,809 vs 1,891). Closed by "occupied bed-days" meaning physical occupancy and by the ward-stay file's purpose. Low risk.
- Resubmissions affect only pathway 2 and 3 spells (541 spells), so the chart only. The latest submission is the stated correction.
- Literal "nights after ready" for the allocation: 10,425 bed-days with a different order. Contradicted by the delivery evidence in the data (residual low-to-moderate fork, the intended analytical step).

Pass-1 forks that this pass did not re-raise (strict order-date test moving asks 2 and 3 to 7,218; the midnight-gap point-in-time join; 168-hour test; min vs max spot start) were not reported as live by the thread on the shipped pack. The thread's min-vs-max delivery test and its all-orders-match check (all 10,055 hospital-route orders match a discharge NHS number) cover the first. The shipped notes still do not pin the order-date test, so keep it in mind as a watch item.

## Spec gates (against the shipped target.zip and metadata.json)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv, txt, xlsx, pdf) | yes |
| Large file | 25,000 rows or more | acute_ward_stays 138,450 rows; acute_discharges 65,496; ices_order_lines 32,943 | yes |
| Distractors | 2 or more, in metadata.json, none labelled in file names or files | 3 named (discharge_delays_weekly_return, bed_census_daily, reablement_91_day_outcomes); no file name or note text labels them | yes |
| Distractor relevance and ruling out | relevant, unused, ruled out by a shipped fact | the weekly return carries trust-level nights after ready with no hospital split; the thread names its basis as the surface read, which is trust-level only and cannot rank hospitals; the basis is ruled out by the data (no pathway-1 patient left before delivery) and by the package definition | yes |
| Deliverables | 1 to 3, all present | 2 (xlsx, svg), both in golden/ | yes |
| Asks multi-dimensional, units and rounding stated | stated in the asking sentence | prompt: "whole numbers"; split of 5 hospitals, 9 brokerage cells, 15 bed-day cells, 15 patient cells | yes |
| Prompt | one paragraph, under 1,000 characters | 911 characters | yes |
| Prompt shape and 25-criteria floor | identifiable shape, 25 or more | shape 05 (allocation to a fixed total); about 40 gradable cells plus the call | yes |
| Licence and source recorded | per file | metadata.json records source, date and CC BY 4.0 for all 16 files | yes |
| Realism | no LLM tells | thread found no authoring or provenance leakage; dates coherent with the 5 Oct 2026 extract and the 28 Sep 2026 allocation note | yes |

## Gate G reconciliation
Card: gate_g and stump_strategy decomposition_attribution, stump_class analytical, decisive_rule_filed false, official_decoy false. Thread: mechanism binding_constraint, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The labels differ but the underlying move is the same: the recorded wait fuses the replaced step with a concurrent equipment step, so the package's saving is the per-patient excess over delivery, valued then filled under the cap. The card concedes the equipment gate is in no filed sentence, only in the data, and sets decisive_rule_filed false. The thread treats this as analysis (a per-patient counterfactual that survives on clean data) and not a hidden rule or planted defect. Risk: a stricter reviewer may read the swap from "nights after ready" to "nights saved" as a lens change. The thread suggests live testing in that case. No mismatch that predicts a send-back.

## Gate H
domain pass, layers pass, decisive_step analytical. Layer 1: mixed dd/mm/yyyy and ISO dates in the ward stays, spaced and mixed-case postcodes, NHS numbers with spaces, resubmitted spells, merged practices. Layer 2: the equipment-bounded counterfactual saving per package and the cap fill. The easy route a strong analyst who read every rule would take is nights after the ready date, which gives 10,425 bed-days with Ashby Vale and Cleeve Park first. This matches the card's analyst_test and domain_test.

## Stump power (Gate F)
Credible. A strong model that runs the national-collection "nights after the ready date" the notes define (and the weekly return aggregates) funds Ashby Vale and Cleeve Park first and claims 10,425. It misses that delivery bounds when a pathway-1 patient could leave. The Marchshire-practice filter, latest-submission rule and cap fill add chances to fail, and the asks (ward-at-midnight attribution, spot-purchase starts, dd/mm parsing) add independent ones. The trap is reachable from the data and does not collapse on clean data. The pass-1 worry (a solver who reads the ICES file finds the join) is a real chance of success on the main call, so the asks carry the separation.

## Findings, ranked
1. None blocking. The pass-1 stale-bundle finding is resolved: the judged bundle is byte-identical to the shipped target.zip.
2. Watch item, optional: the equipment gate is evidenced only by data, not by a filed sentence (per-patient counterfactual, not a hidden rule). Any pin in ices_export_notes.txt that "required_by is the discharge ready date" would close the strict order-date fork but risks handing over the mechanism, so leave it unless the portal flags it.
3. Watch item, optional: the pass-1 notes pins (midnight-gap rule, calendar-day wait, earliest service_start) are not needed by the thread on the shipped pack. The council notes already fix month received, calendar days and the first service_start as the care start.

## Next action for the author
Ship as is. No generator or notes change is required; if a portal finding later cites the equipment gate or the order-date test, route it to /fix-determinism.
