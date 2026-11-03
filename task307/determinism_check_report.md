# determinism-check report, task307, 2026-11-03

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every committed answer reproduces from the shipped bundle (14 files, fresh unzip, one judge thread, no retry). The call is forced by one empirical fact the files separate: pitting accrues at 0.24 cm2 per hour inside the 30 to 58 per cent band across every inspection pair the historian covers (0.2391 to 0.2409). Applied to 2026 band hours and the 2021/22 to 2025/26 winter outage means, Nesvik G1 gives 4,650 MWh per NOK million against Sørdal G1 at 3,820, lead 830. Per-running-hour and calendar-year routes file other units. No Gate A to E failure.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pitting per band hour | 0.24 | 0.2391 to 0.2409 over 6 pairs | yes |
| Pitting now, OSD-G1 / OSD-G2 / SDL-G1 / SDL-G2 / SDL-G3 / NSV-G1 / NSV-G2 | 1,650 / 1,250 / 1,990 / 880 / 890 / 2,250 / 1,790 | 1,651 / 1,249 / 1,989 / 883 / 889 / 2,253 / 1,791 | yes |
| Last-inspection pitting | 1,260 / 650 / 910 / 570 / 0 / 1,050 / 1,350 | match register totals (blade+band sums) | yes |
| Year past 2,400 | NSV-G1 2027, SDL-G1 2029, SDL-G3 2031, others none | same (SDL-G1 end-2028 2,391 / end-2029 2,592) | yes |
| Outage MWh | 67,000 / 55,800 / 14,100 | 67,020 / 55,833 / 14,127 | yes |
| MWh per NOK million (quote excl. VAT 14.4 / 14.6 / 14.2) | 4,650 / 3,820 / 990 | 4,654 / 3,824 / 995 | yes |
| Gap | 830 | 829.9 | yes |
| Generation since 2016 (MWh) | 4,542,600 / 4,464,900 / 2,427,400 / 2,710,200 / 558,000 / 2,900,300 / 3,370,400 | 4,542,579 / 4,464,876 / 2,427,423 / 2,710,214 / 558,015 / 2,900,258 / 3,370,419 | yes |
| Starts | 419 / 417 / 428 / 492 / 6,729 / 375 / 394 | identical | yes |
| Pre-RTU tag remap | per maintenance log | confirmed by unit_counter_readings.csv deltas (starts and hours, all 7 units) | yes |

## Competing answers that survived
None on the main call. Residuals tested and closed: rate range 0.2391 to 0.2409 keeps SDL-G1 in 2029 (max end-2028 2,396.7); band edge convention moves about 1 cm2, no rounding change; inspection-day start no change; including VAT scales both candidates by 1.25, winner holds, and planning note 4.1 pins excl. VAT. Minor residual: NSV-G1 pitting now rounds to 2,250 under pooled or own-pair rate but 2,260 under the single highest pair rate (0.2409), an unnatural choice.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 14 | yes |
| Formats | 3 or more | 4 (csv, xlsx, docx, pdf) | yes |
| Large file | 25,000+ rows | historian 63,264 rows | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | 3 (day-ahead prices, reserve contracts, reservoir inflow); no file name labels one | yes |
| Distractors unused yet weighty | unused by solution; if answering a graded quantity, ruled out by a shipped fact | none answers a graded quantity; reserve contracts explain the 2022 band-hour step but the duty is read from the units' own output; prices contradicted by planning note valuing outage in MWh | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | per-unit multi-cell tables, units and rounding in the prompt sentence | yes |
| Prompt shape and rubric | shape identifiable, 25+ criteria | shape 01 ranked list with one pick, 62 graded figures per design note | yes |
| Not LLM-generated, realistic goldens | | judge: Norwegian headers, decimal commas, mixed WO prefixes, DST export; no authoring language | yes (golden-realism not independently re-read here) |

## Gate G reconciliation
Judge: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: strategy `other` (wear in one output band), Layer 2 family `estimand_identification`, `stump_class: analytical`, forecasting named the honest mechanism. Consistent: no mismatch on class, mechanism or defect. The declared distractors (prices, reserve contracts, inflow) were not named by the judge as a surface read carrying the task; the reserve contracts only explain a duty step. Gate G class: pass (analytical, non-defect).

Gate H line (judge): domain: pass, layers: pass, decisive_step: analytical. Matches the design note's `## Three rules` (decisive step: band hours from hourly output vs rate per running hour; no decoy, not semantics, not rule application) and the card's analyst_test and domain_test.

One discrepancy to note: the design note's default path (per running hour, peaker set aside) ends on Nesvik G2 (2030); the judge's easy route (per running hour) filed SDL-G3 (2031), and calendar-year trend filed no unit. All are wrong answers, so the stump holds, but the ladder's R0 end-point is the pooled-by-hour reading with the peaker set aside, which the judge did not run explicitly. Not a finding against determinism.

## Stump power (Gate F)
Good per judge. Run-hour and calendar-year extrapolations (the field's reflex) each file a wrong unit or none. The band-hour driver is not named in any shipped document; it is found by calibrating across inspection pairs (spread under 1 per cent, versus 13 per cent for per-hour, tenfold peaker gap). This is not a landable textbook route: the field's equivalent-hours method files the wrong unit, so the main thread need not discount for a standard-method golden. Caveats for the main thread to weigh against the ladder: unit_register.xlsx's Driftsområder names the 30 to 58 per cent band, which makes the band a visible candidate; the 0.24 rate cannot be checked on pre-2016 pairs (no historian), so the fit rests on the six in-historian pairs.

## Findings, ranked
1. No blocking finding. DETERMINISTIC, APPROVE.
2. Minor: NSV-G1 pitting now is 2,260 under the single highest pair rate (0.2409); natural estimators give 2,250.
3. Minor: the rate is calibrated on six pairs only (pre-2016 pairs have no historian); band-edge and inspection-day conventions move values by about 1 cm2 with no rounding change.
4. Note: ask 3's generation and starts depend on remapping the old historian slots by overhaul pattern (SDL 3-cycle U1=G2, U2=G3, U3=G1), forced by maintenance_history.csv and unit_counter_readings.csv (exact match on all 7 units); reading historian_tag_map_2023.csv as valid throughout contradicts both. Ask-level, not the main call.
5. Note: NSV-G2 2024 and OSD-G2 2025 overhauls have no inspection rows; not a fork (the register is the universe).
6. Judge's default-path end (SDL-G3) differs from the design note's R0 (Nesvik G2); both wrong, stump holds.

## Next action for the author
Record the judge verdict (DETERMINISTIC, APPROVE) and this report path in pipeline.json's judge block and proceed to the ship checks; no fix needed.
