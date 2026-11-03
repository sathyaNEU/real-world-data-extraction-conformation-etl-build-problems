# determinism-check report (pass 2), task194, 2026-11-03

## Verdict
DETERMINISTIC, plus SOLUTION_WRONG (one supplementary cell: ask 4, Ashworth Fold)
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution (borderline, area water balance), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no (borderline)

## Why
Executed word for word, LP04 gives Kestle Hill an own-leakage rise of 0.94 l/s, the largest of 18 areas. It is a hydraulic transfer: about 09:00 UTC on 6 Oct, KH01_FT steps up 3.4 m3/h at night and MLW_INLET_FT1 steps down 3.4 m3/h, the two-inlet sum is unchanged (15.4 m3/h), the whole-day hourly changes mirror each other (daytime up to 27 m3/h), and Moorend Low's un-netted comparison leakage is -0.28 m3/h, which is impossible. Netting the 0.945 l/s crossing leaves both areas at 0.0 and Thrushgate (0.61) ahead of Ashworth Fold (0.31). Calvert Rise and Pellow Bridge fall to 0.0 under LP04 5.1 and 4.3. The main call and every graded figure but one reproduce; both pass-1 forks (supp 4 meter scope, supp 5 class after CONV) are now closed.
Only the golden's Ashworth Fold ask-4 figure is exposed: the local-October consumption is exactly 2,756.5 m3, and the golden prints 2,756, one of two valid roundings.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Own leakage change, 18 areas (l/s) | listed set | Thrushgate 0.610, Ashworth Fold 0.306, Barrowfold 0.186, Gorsey Bank 0.103, Lidden 0.100, Hennick -0.201, Ravensclough -0.198, Oakshaw -0.106, Tollbar -0.096, Whinlow -0.096, Stanecroft -0.024, Calvert Rise 0.010, others within 0.004 | yes, all 18 |
| Kestle Hill / Moorend Low before netting | +0.9 / -0.9 | +0.943 / -0.947 | yes |
| Night crossing | 0.9 | 0.945 (rise only, fall only or mean all give 0.0 for both areas at one decimal) | yes |
| Gap Thrushgate to Ashworth Fold | 0.3 | 0.304 | yes |
| Ask 4 large-user October m3 | 18 values | 17 of 18 match | Ashworth Fold is a tie at 2,756.5 |
| Ask 5 occupied households | 18 values | all 18 match (account-level last OCC/VAC, class of the property's latest row, D3305 folded into D3341, effective date to 31 Oct) | yes |
| Ask 6 mains repairs | 18 values | all 18 match | yes |
| Robustness | n/a | per-night vs set-mean normalisation, check meters in the subtraction, area by supply point vs account, hour-stamp convention: Thrushgate stays first; Kestle Hill lead without netting is 0.943 vs 0.610, so the call is binary on netting | yes |

## Competing answers that survived
All sit in the asks; none touches the main call.
1. Ask 4, Ashworth Fold: 2,756.5 exactly. Half-up gives 2,757, banker's rounding or truncation gives 2,756 (the golden). The prompt says "whole cubic metres" but no half rule. underspecified_objective; the only fork on the golden.
2. October as local month vs UTC stamp: 745 vs 744 hours, 1 to 2 m3 in about 9 cells (Gorsey Bank 4,437 vs 4,436, Barrowfold 4,630 vs 4,629, Upper Sowden 4,851 vs 4,849). LP04 3 fixes local clock only for the night hour. Local is the natural reading; no sentence closes it.
3. R. Pennock meter exchange (17A679699 to 15A637161, 14 Oct): the 10:00Z to 11:00Z hour is unmetered. The golden sums metered advances only ("metered consumption" supports it); an estimate gives another tie (Gorsey Bank 4,437.5).
4. Check meters (Kalder, bottling hall sub-meter, Barrowfold Rail Maintenance) excluded; including them gives Thrushgate 1,103, Barrowfold 5,122, Stanecroft 3,768. The judge reads this as closed by the register's Supply points sheet (one Revenue meter per supply point) and not stated in words. The design note says the account list now carries a Meter role (SF12); the judge did not cite it, so confirm the role column is in the shipped xlsx.
5. Large-user area by account vs supply point: moves most ask-4 cells (Hennick 5,673 vs 2,867). Closed by the register's supply-point area; the accounts file column "Area (account)" could split a literal reader.
6. Ask 5: posted vs effective cut-off differs by 1 in Barrowfold and Pellow Bridge; a property-level latest-OCC/VAC reading differs by 543 properties, but every difference is a same-day handover where the new OCC posted before the old VAC, so the account-level golden is correct. CONV is defined nowhere, but its rows carry class NHH.
7. Stanecroft -0.024 prints as -0.0 against 0.0 (cosmetic).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (PDF 1, CSV 8, XLSX 4, GeoJSON 1) | yes |
| Large file | 25,000 rows or more | historian 180,405; AMR 57,188; billing 46,131 | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | raingauge_hv03, customer_contacts, find_and_fix_outcomes (3); unused by the solution; prv_setpoint_log corroborates Calvert Rise only | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pdf), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 18-area cuts; units and rounding in the prompt; no half-rounding rule | yes (rounding gap noted above) |
| Prompt shape, 25 or more criteria | identifiable | per-area cuts clear 25 by count; no generated rubric seen | yes (by count) |
| Reads as real, not LLM generated | yes | no authoring leakage found | yes |
Hygiene notes (non-stump): every historian Quality is GOOD; LP04 Appendix A refers to a Friday 6 Nov export but data end 2 Nov; xlsx carry an empty workbook-protection element (openpyxl signature). Prompt unchanged from pass 1 (no count the data hold, one paragraph).

## Gate G reconciliation
Judge: decomposition_attribution (borderline), analytical_non_defect, surface_read_dependency no, sole_data_defect no (borderline). Design note: analytical stump, default path R2 names Kestle Hill, decisive R3 names Thrushgate. These agree. No metadata distractor is named as the surface read, so none is too load-bearing. Not banned. Borderline flag: on clean data with no crossing there is no stump, and the stale GIS status (CLOSED) is the only wrong record a solver can lean on; a stricter reader could set sole_data_defect yes.

## Gate H reconciliation
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Explicit ruling (a): an analytical method of the field, reconciling the boundary-valve crossing so own leakage excludes foreign water (area water balance). Not rule application: LP04 files the estimand (own leakage, 6.1) and the legitimate-use and pressure rules, and states no netting rule; the WHAT is filed, the HOW is left. Not data semantics: no field or unit read changes the call. Discoverable only from the data (equal-and-opposite mirrored step, constant sum, day shift four times the night shift) and signalled by Moorend Low's negative leakage when LP04 is run literally. Easy route: stop at LP04 sections 3 to 5, file Kestle Hill 0.9 l/s. Swap test passes. Matches the design note's `## Three rules`.
Counter-case recorded by the judge: a reviewer applying the client's definition strictly could call it (b), since the GIS says CLOSED, no document records the opening and discovery rests on one cross-area anomaly. Tipping factors for (a): every series is a correct measurement, nothing is falsified or copied, the transfer is real hydraulics, the amount must be estimated from the night mirror, and a 2024 last-operated date certifies nothing about October 2026. The call is close.

## Stump power (Gate F)
Plausibly moderate. A solver who executes LP04 without cross-checking neighbours files Kestle Hill; the word "own" and the negative Moorend Low leakage are trip-wires. The asks carry real silent hardness (check meters, supply-point vs account area, five-digit rollover, the Pennock exchange, DST, CONV, same-day handovers, legacy asset ids and TC jobs, bar loggers, the old Gorsey Bank code), so a main-call miss likely pairs with ask losses. Water balance across boundaries is a textbook route a strong solver can reach (stumping 1.3); the main thread weighs this against the ladder. No lever needed for determinism.

## Findings, ranked
1. FIX_NOW, solution only: ask 4 Ashworth Fold is exactly 2,756.5; record it as 2,756.5 in the golden and rubric and accept 2,756 or 2,757. No prompt or input change, no rerun.
2. Optional: accept plus or minus 1 m3 on ask 4 for the local-vs-UTC month and Pennock changeover forks (about 9 cells at 1 to 2 m3).
3. Close-call Gate H counter-case ((b), stale GIS CLOSED status); judge held (a). Residual portal risk.
4. sole_data_defect borderline: with no crossing, no stump.
5. Check-meter closure is reasoned from the register's Supply points sheet by the judge, who found no stated words; verify the Meter role column added in the r1 repair is visible in the shipped large_user_accounts.xlsx.
6. Cosmetic: Stanecroft -0.0; xlsx workbook-protection element; Appendix A export date vs data end.

## Next action for the author
Fix the golden (generator/golden.py and the rubric) so ask 4 Ashworth Fold reads 2,756.5 with 2,756 or 2,757 accepted, optionally widen ask 4 to plus or minus 1 m3, and leave the prompt, target and main call untouched.
