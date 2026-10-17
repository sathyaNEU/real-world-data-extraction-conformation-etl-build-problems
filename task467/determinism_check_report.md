# determinism-check report, task467, 2026-10-17

## Verdict
NOT_DETERMINISTIC (ledger file only; the main recommendation and memo figures are forced and reproduce). SOLUTION_WRONG does not apply.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The $6.50 call, 74,724 recorded pickups, 84,000 restated (83,939 recomputed), 11 per cent share, and the surplus and shortfall all reproduce from the bundle, and the competing answers ($5.75 and $7.00) are reached only by analytic shortcuts. The ledger is open: 1,774 store-and-forward re-sends in the 2026 monthly files are copies of earlier records (seconds truncated to :00, sf_flag Y). The dictionary, By-law GT-3 and the prompt never say re-sends exist or that a trip counts once; s.3(2) bills pickups "as the Vehicle-for-Hire Office's records show them". The golden removes copies matched on licence and minute (51,070 pickups in 2026). Dropping only exact-second duplicates gives 51,934 and no removal gives 51,993. Each alternative differs from the golden on 48 of 120 rows (by 864 and 923 trips). Ledger ask 1 is the only item affected. The chart's 2026 pickup series carries the same dependency but is not numerically graded.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2025 fee-liable pickups as recorded | 74,724 | 74,724 (pu_zone=1, 2025 parquet) | yes |
| Pickup/drop-off ratio change, station zones | -10.8% | -10.8% | yes |
| Pickup/drop-off ratio change, other zones | -11.1% | -11.1% | yes |
| Restated 2025 | 84,000 | 83,939 | yes (nearest thousand) |
| Share the rank cost | 11% | 10.98% | yes |
| Budget line 12 | $535,027 | $535,027 | yes |
| Lowest 25-cent step | $6.50 | $6.50 (holds for 82,312 to 85,604) | yes |
| Surplus at $6.50 | $10,000 | 10,576 (83,939) or 10,973 (84,000) | yes |
| Shortfall at $6.25 | $10,000 | 10,408 or 10,027 | yes |
| Ledger 2025, 60 rows | as filed | all match (brokerage by start-date affiliation) | yes |
| Ledger 2026, 60 rows | as filed | match only under dedup on licence+minute+zones+total, $6.75 | no, convention not filed |

## Competing answers that survived
- Ledger 2026 pickups: (a) copies matched on licence and minute removed (golden, 51,070); (b) exact-record duplicates only (51,934); (c) no removal (51,993). The shipped text does not close it; no shipped rule states that a trip counts once or that re-sends exist. The fix is one clause in the prompt (see Next action).
- Closed by the files: station-zone mapping (4 named zones; per-zone analysis lands on 83.9k), brokerage attribution (s.3(2) plus affiliations), local time (s.2), fee in force per year (s.3(3)), voids (s.2 and dictionary).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 23 | yes |
| Formats | 3 or more | 4 (parquet, csv, pdf, xlsx) | yes |
| Large file | 25,000 rows or more | 169,876 (2024 parquet), 138,108 (2025) | yes |
| Distractors in metadata.json, none labelled by file name | 2 or more | 2 (passenger statistics xlsx, 2023 ground access survey pdf); file names carry no label | yes |
| Distractors unused yet weighable; a graded-quantity one rules out by a shipped fact | yes | pickups per arriving passenger gives $5.50, ruled out by the bulletin and drop-off structure (design note); volume grew ~3% a year, no fall | yes |
| Deliverables | 1 to 3, all in the golden | 2 (docx, csv), both in golden/ | yes |
| Asks multi-dimensional, unit and rounding stated | yes | 120-cell grid plus memo asks; prompt states whole trips, nearest thousand, whole per cent, nearest $10,000, dollars and cents | yes |
| Prompt shape and 25+ criteria | identifiable, 25+ | shape 07 grid (6 brokerages by 20 months plus memo figures); count not independently generated | yes (by shape) |
| Reads as real, not LLM generated | yes | judge found no authoring disclosure; goldens not independently re-audited here | yes (not independently re-audited) |

## Gate G reconciliation
Judge: mechanism decomposition_attribution, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: gate_g decomposition_attribution, stump_strategy composition_mix, stump_class analytical, analyst_test ($5.75 from the whole fall, $7.00 from all pickups against all drop-offs, $6.50 from the within-zone comparison). Design note Three rules: No decoy, Not semantics, Not rule application all stated. Match: the judge reached the same two easy-route wrong answers and the same grouping step as the card. Neither declared distractor (passenger statistics, ground access survey) carries the task; the judge named no distractor as the surface read. The design note declares the re-send device (D1) as an intended silent ask-side device that "survives every key check" and does not list it as a main-call fork; the judge's finding is that, for the ledger, the shipped text does not close the population, which the note's own stops table treats as the intended trap. Finding: the device is legitimate Layer 1 on the ask side but the ledger needs the WHAT filed to be determinate.

## Stump power (Gate F)
Moderate to good. Pooled ratio (3.6%, $7.00) and the whole 22 per cent fall ($5.75) are natural and wrong; only the station-zone split gives $6.50. Restated 84,000 and the 11 per cent share are exact-graded. Judge estimate: about 1 to 2 of 4 responses stumped.

## Findings, ranked
1. Ledger 2026 re-send population is not filed (competing_defensible_answer, 48 of 120 rows). FIX_NOW.
2. The chart's 2026 pickup series shares the dependency (not numerically gradable, no separate action).
3. No finding on the main call, memo figures, 2025 ledger rows or hygiene.

## Next action for the author
In the ledger sentence of prompt.txt, add a clause filing the population, for example "each trip counted once, a record the meter sent again counting once", without naming the minute key or the flag. Keep the prompt under 1,000 characters (currently 913), re-run voice-check.py, then re-check the 120 ledger rows against the golden. The memo and main call stay frozen; one re-judge is allowed after the fix.
