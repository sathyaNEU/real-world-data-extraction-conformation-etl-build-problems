# determinism-check report, task460, 2026-11-01 (pass 3, rubric reship)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Judge thread read target.zip sha256 b0a46e28 (verified equal to the folder's zip). Raw verdict: /tmp/determinism-check-task460-224220/verdict.md.

## Why
Charter 3.2 and 3.3 file the estimand (marginal generation displaced, interchange fixed day ahead, per MWh of the Lumen Ridge array output). Every differenced estimator reproduces Gorsefield 0.89, Halvane 0.58 (gap 0.31) and the same two-decimal figure for the other six. The rebuilt ask layer (use, share, price) reproduces for all eight stores.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Avoided t/MWh G/H/T/B/Q/K/F/O | 0.89/0.58/0.41/0.40/0.39/0.39/0.39/0.39 | 0.889-0.891/0.579-0.581/0.408-0.412/0.401-0.402/0.390-0.392/0.389-0.392/0.388-0.391/0.386-0.388 (4 season groupings) | yes |
| Gap | 0.31 | 0.312 | yes |
| Brackwell avg rate / Quillbury non-baseload | 0.85 / 1.11 | 0.851 / 1.111 | yes |
| Use MWh (same store order, G..O) | 2,570 2,507 2,458 2,373 2,338 2,462 1,976 2,862 | 2570.3 2507.3 2458.3 2372.9 2338.0 2462.2 1975.9 2861.9 | yes |
| Share % | 28.5 27.1 27.0 26.6 23.0 27.6 24.0 30.2 | 28.514 27.086 27.006 26.595 22.990 27.612 24.013 30.199 | yes |
| USD per MWh | 146 142 137 155 183 225 122 170 | 146.09 141.84 136.96 155.10 182.79 224.78 122.24 170.21 | yes |

## Competing answers that survived
- Levels regression (CO2 level on net generation level) instead of first differences: winner and first-left-out unchanged, gap 0.32, six of eight t/MWh figures move (Quillbury 0.41, Tennaford 0.44, Faraview 0.47, Kestrel Point 0.27, Halvane 0.57, Gorsefield 0.89 holds). Data discourage it (Kestrel Point gas-only grid at 0.27 is below the gas rate). Method choice the data separate, not a semantic fork; moves ask 2 and the gap, not the call.
- Hourly CSV: per-row rate not unique (season grouping unfiled; last 5 to 8 local hours of 2025 have no grid hour). Aggregate matches the memo; low severity.
- Loss factor on second Ardley term, raw Ardley quantity, remove-duplicate-payment, invoice-date-year attribution were all closed by data or prompt text (each would move use or price by 2 to 9 percent or dollars; none survives).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats / big file | 10 / 3 / 25,000 rows | 11 / csv, pdf, xlsx / 70,080 | yes |
| Distractors in metadata.json, none named in a file | 2+ | 2024 EDC workbook, Ardley content label | yes |
| Distractors unused, relevant, ruled out by a shipped fact | yes | 2024 rates and label are the wrong-basis reads; ruled out by charter 3.2/3.3 | yes |
| Deliverables | 1 to 3 | 2 (pdf, csv) | yes |
| Asks multi-dimensional with unit and rounding | yes | 8 stores x 4 measures, units and rounding in the prompt | yes |
| Prompt shape, 25+ criteria | shape 01 identifiable | shape 01; criteria count not enumerated by me (generated rubric) | shape yes, count unverified |
| Reads as real work product | yes | judge found no tell | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and metadata: stump_class analytical, distractors (2024 workbook, label) declared as wrong basis, not carrying the call; the surface reads that fail (published average/non-baseload/all-hours fit) are the EDC 2025 rates, not the declared distractors. Match. Gate G: pass.

## Stump power (Gate F)
Published EDC rates point to Brackwell or Quillbury, a pooled fit to Tennaford; the call needs a within-area hour-of-day margin. The judge expects a strong solver reading charter 3.3 can land the call (partial stumping on the call), with loss on the asks (Halworth move, loss factor, double payment). Main call frozen from the earlier passes; the ladder in the design note governs. The differenced-estimator family is the field's standard approach, a landable route; weigh against the ladder.

## Findings, ranked
1. Levels-regression fork on the t/MWh list and gap (low, filing the estimator would convert the decisive step to rule application; leave).
2. Hourly CSV row-level rate not unique (low).
3. Rubric criteria count not checked here.

## Next action for the author
Proceed to ship; no repair needed.
