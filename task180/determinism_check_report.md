# determinism-check report, task180 (architecture 5), 2026-11-02

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (one optional prompt-only pin on the cardlock month, see Findings)
**Stumping type:** mechanism: decomposition_attribution, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The isolated judge thread (one pass, reading only a fresh unzip of target.zip, md5 c5cd86cf...) reproduced every graded figure. PD-07 s.4 defines the loss as product that left the tank system other than through a nozzle, so the book shortfall overstates it by the meters' over-delivery. That over-delivery is pinned by one drift (6.1 mL per 20 L per 100,000 L, 324 tank-quarters, 2024Q1 to 2026Q3). Taking it out leaves exactly two systems over 0.75 L/h: Ituna regular 1.213 and Canora regular 0.914. The next highest system is 0.019. Hours: 2,208 (SK) and 2,209 (MB, clocks back 1 Nov); no Manitoba system is near the line. Nine estimator variants (with a constant, without the two leaking tanks, with Q4, 2025 or 2026 onward, median ratio, swaps as resets, reset the day after) all keep the same two systems and the same rounded figures; Canora's margin to 0.75 is about 0.16 under all. The "shortfall = loss" reading (1.3, 1.0, 1.7, 1.5, four systems) contradicts s.4 literally, so it is the intended easy route and not a licensed second reading. The cardlock cells reproduce exactly.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ituna reg Q4 shortfall | 1.3 L/h | 1.347 | yes |
| Canora reg shortfall | 1.0 | 1.021 | yes |
| Kamsack reg / Foam Lake dsl shortfall | 1.7 / 1.5 | 1.681 / 1.541 | yes |
| Meter give-away Canora / Kamsack / Foam Lake | 0.1 / 1.7 / 1.6 | 0.107 / 1.693 / 1.647 | yes |
| Fit quarters | 324 | 324 | yes |
| Drift | 6.1 mL | 6.083 (6.100 if swaps reset) | yes |
| Ituna / Canora loss | 1.2 / 0.9 | 1.213 / 0.914 | yes |
| Other systems | near zero | max 0.019 | yes |
| Touchwood Oct/Nov/Dec | 20/20/-70 | 20/20/-70 | yes |
| Whitesand Oct/Nov/Dec | 1,810/3,010/2,040 | same | yes |
| CL-401 / 404 / 407 / 412 (3 months each) | 270/350/360; 790/780/730; 400/1,580/240; 370/330/650 | same, all 12 | yes |

## Competing answers that survived
One, low severity: the month of a drop. Under arrival month (report start or hourly rise) the table is as filed. Dating by the bill's loaded date moves three cells: CL-401 Dec 340 (filed 360), Whitesand Dec 2,030 (filed 2,040), CL-407 Nov 1,570 (filed 1,580); Touchwood unchanged. The prompt does not say which month. Other cardlock readings: gauge increase alone with no draws gives 550 to 8,990 L per cell, but the files do not license it (the gauge rise excludes sales during the drop); counting overlapping rather than starting transactions gives identical cells; gross-short instead of net differs (Touchwood Dec +70) but the prompt says net. Main call: no surviving fork (December preliminary export would put Roblin regular near 0.4, still under 0.75).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files / formats | 10+ / 3+ | 14 / 4 (csv, pdf, xlsx, json) | yes |
| Large file | 25,000 rows | POS file 175,812 rows | yes |
| Distractors | 2+ in metadata.json, none named in a file name | 4 (weather, cathodic survey, line leak tests, vacuum manifests); none labelled by file name | yes |
| Distractors unused yet weighable | yes | CP survey and LLD tests weigh on a leak but do not answer the quantity; judge found Ituna's CP failure consistent but not decisive | yes |
| Deliverables | 1 to 3, all in golden | 2, both present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 18 cells of carrier/cardlock by month; "litres an hour to one decimal", "nearest 10 litres" | yes |
| Prompt shape, rubric 25+ | identifiable, 25+ | shape 01, design note counts 33 criteria (not independently regenerated) | yes |
| Not LLM-read | yes | judge saw no authoring leakage; realistic Layer 1 mess | yes |

## Gate G reconciliation
Thread: mechanism decomposition_attribution, family analytical_non_defect, surface_read no, sole_data_defect no. Design note: strategy and Gate G `decomposition_attribution`, Layer 2 `estimation_fit`. Match. The thread names the book shortfall (rung 1, four systems) as the surface read and the Ituna-only SIR filing as the second route, which are the note's rungs 1 and 0; the declared distractors are not named as carrying the task. Gate H: domain pass, layers pass, decisive_step analytical, agreeing with the note's Three rules (drift fitted on the network's earlier quarters, litres clock). The card's `stump_class`/`analyst_test` fields were not separately inspected. No mismatch.

## Stump power (Gate F)
The decisive step is estimating a network-wide drift from earlier quarters and per-hose exposure (work orders, config serials, register dispenser numbers) and subtracting it. This is an estimate the data must settle, not a stated rule. The thread rates the easy routes (face-value shortfall files four; SIR files Ituna alone; flat or per-site meter correction misses) as plausible failures. It did not class the step as a textbook method with no judgment, so the main thread weighs it against the ladder as designed.

## Findings, ranked
1. Cardlock month of a drop is not filed (3 cells move by 10 to 20 L under loaded-date dating). The design note says no drop crosses a month and SF22 only covers Russell's wall clock; the loaded-date alternative is not in the fork table. Optional prompt-only pin: "by the month each drop arrived", plus a fork-table row.
2. Borderline noted by the thread: "the shortfall overstates the loss" has a surface-read flavour, held as fine since the shortfall is correct and the work is a decomposition. Portal-confirmable.

## Next action for the author
Optionally add the arrival-month pin to prompt.txt (and an SF row asserted in checks.py), then continue to ship; no figure changes.
