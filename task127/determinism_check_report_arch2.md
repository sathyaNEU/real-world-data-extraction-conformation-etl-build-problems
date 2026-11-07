# determinism-check report, task127, 2026-10-12

## Verdict
DETERMINISTIC on the thread's evidence, but the pass is INVALID FOR FIVE FILES: the thread judged a bundle that is not the shipped target.zip.
**Disposition:** FIX_NOW (re-run once on a fresh unzip of the shipped target.zip, plus the three one-line note pins below)
**Stumping type:** mechanism: binding_constraint (borderline single_conceptual_flip), stumping_family: analytical_non_defect (borderline), surface_read_dependency: no (borderline), sole_data_defect: no

## Bundle mismatch (found first)
md5 comparison of /tmp/determinism-check-task127-1791803880/target/ against a fresh unzip of task127/target.zip (built 2026-10-12 11:25; task127/target/ equals the zip):
- IDENTICAL (11): acute_discharges, ices_order_lines, brokerage_referrals, spot_care_invoice_lines, gp_practices, postcode_districts, discharge_delays_weekly_return, the three notes txt files, the PDF.
- DIFFERENT (5): acute_ward_stays (7,569,908 vs 7,572,618 bytes), bed_census_daily.xlsx, reablement_91_day_outcomes.xlsx, ward_reference.csv (27 lines, different beds and ward list, vs the shipped 54 rows), data_request_log.csv.
The judge's scratch copy is a stale build. Consequences: the main allocation (508/350/120/222/0, 7,160) rests on files that are identical, so that reproduction stands. Every figure that touches ward stays or ward_reference (23,541 lost bed-days, the 15 bed-day chart cells, the ward-gap fork) and the "data_request_log row counts match" hygiene line were NOT verified against the shipped pack. Distractor reads of the census and reablement files are also against stale copies.

## Why
Run word for word, SF-2026-14 gives Royal Marchford 508, Wendlebury 350, Holmford 120, Cleeve Park 222, Ashby Vale 0, 7,160 bed-days (values 6.648/6.240/5.258/4.361/3.598); wrong basis (nights after ready) gives Ashby Vale and Cleeve Park first, 10,425. The ranking survives every equipment-join variant except the strict "ordered on or after admission" reading, which leaves the split but moves supplementary asks 2 and 3 (7,218).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Covered patients RM/W/H/CP/AV | 508/350/120/285/361 | identical (identical files) | yes |
| Mean nights saved | 6.65/6.24/5.26/4.36/3.60 | 6.6476/6.2400/5.2583/4.3614/3.5983 | yes |
| Packages | 508/350/120/222/0 | identical | yes |
| Bed-days | 3,377/2,184/631/968/0 = 7,160 | identical | yes |
| Wrong-basis total | 10,425 | 10,425 | yes |
| Brokerage 7-day cells (9) and 242 closed-with-spot | as filed | identical (identical files) | yes |
| Lost bed-days Dec-Feb 23,541 and 15 bed-day cells | as filed | reproduced on the STALE ward_stays/ward_reference | NOT VERIFIED on shipped |
| 15 patients-delayed cells | as filed | reproduced (acute_discharges identical, ward join not needed for distinct spells) | yes, likely; confirm on rerun |

## Competing answers that survived (all unpinned in the shipped notes)
1. Strict order-date test on ICES lines (order on or after admission) drops 24 patients: values 3.853/4.544/5.325/6.652/6.260, total 7,218 (asks 2 and 3; allocation unchanged). Closure: state that an order's required_by is the ready date.
2. Ward-stay midnight gap: literal point-in-time join gives 23,518 and 11 of 15 cells off by 1 to 5 (stale files; recheck).
3. Seven-day test: calendar days (golden) vs 168 hours vs "<7"; month attribution received vs start; spot start min vs max of service_start. All named by the thread as unpinned.

## Spec gates (against the shipped target.zip)
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 16 | yes |
| Formats | 3+ | 4 (csv, txt, xlsx, pdf) | yes |
| Large file | 25,000+ rows | acute_ward_stays 138,450 rows; discharges 65,496 | yes |
| Distractors | 2+, named in metadata, none labelled in files | 3 named; no file name or content label | yes |
| Distractor relevance and ruling out | relevant, unused, ruled out by a shipped fact | weekly return (trust-level nights after ready, no hospital split), census, reablement; the naive basis is ruled out by "no pathway-1 patient left before delivery" (data, not a stated sentence) | yes, see finding 3 |
| Deliverables | 1 to 3 | 2 (xlsx, svg), both present in golden/ | yes |
| Asks multi-dimensional, units and rounding | stated | prompt states whole numbers; 15+15+9 cells plus split | yes |
| Prompt | one paragraph, under 1,000 chars | 911 chars | yes |
| Rubric 25+ criteria | 25+ | about 40 gradable cells plus call | yes |
| Realism | no LLM tells | thread found none (on a partly stale pack) | yes, recheck on rerun |

## Gate G reconciliation
Card: gate_g and stump_strategy decomposition_attribution, stump_class analytical. Thread: binding_constraint, analytical_non_defect borderline, flagged as a possible lens swap (rank by nights saved, not nights waiting). Mismatch in label, same underlying move; the reviewer may read the build as a cap plus an estimand choice rather than a decomposition. The card's own text concedes the equipment gate is in no filed sentence, only in the data; the risk is that it is read as an unstated hidden rule rather than analysis.

## Gate H
domain pass, layers pass (Layer 1: resubmissions, mixed date formats, postcodes, BRK refs; Layer 2: avoidable-nights valuation of a package under a cap), decisive_step analytical. The thread names the weekly return's nights-after-ready basis as the surface read, which is the declared-distractor family but trust-level only, so it is not the distractor carrying the task (acute_discharges itself produces the wrong answer). Consistent with the card's analyst_test.

## Stump power (Gate F)
Moderate. A strong solver who reads the ICES file finds the join, so the main call may not hold the top two under 50; the asks (dedupe, midnight ward attribution, spot-invoice start dates) carry the separation.

## Findings, ranked
1. Judge ran on a stale bundle (5 files differ). Re-judge once on a fresh unzip of task127/target.zip; ward-based figures must be reverified. The /tmp unzip was not made from the shipped zip.
2. Pin in acute_extract_notes.txt: a night with the patient between wards at midnight stays at the hospital of the adjoining stays; in council_extract_notes.txt: "within seven days" and the month are counted in calendar days from the received date; a spot purchase starts at the earliest service_start. Pins change the notes, not the figures (re-zip target.zip afterward).
3. Optional: state in ices_export_notes.txt that an order's required_by is the discharge ready date, closing the strict-order-date fork that moves asks 2 and 3 to 7,218.
4. Gate G label risk: equipment gate evidenced only by data; keep it as analysis (per-patient counterfactual), not a hidden rule.

## Next action for the author
Apply the notes pins (finding 2, plus 3), rebuild twice byte-identically, rezip, and re-run the determinism judge once on a fresh unzip of the new target.zip.
