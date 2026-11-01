# Judge verdict, task140 (C-22 batch guarantee, 2027 Q1), fresh re-judge

Scope: only the shipped bundle under `judge-task140d/target/` plus `prompt.txt` and `graded_blocks.md` were read. No other task or judge directory was opened, so the cross-batch fingerprint check was not run beyond the bundle itself (no overlap visible inside the bundle).

**Verdict:** DETERMINISTIC

**Disposition:** APPROVE. Nothing needs repair and no rerun is required. One residual fork, named below, is optional hardening only.

**Why:** The guarantee follows from CS-3 2.1, 3.2, 3.3, 4.1 and 5.1 and the shipped hardware plan, budgets, rate card, requests and hourly monitoring export. Everything except one input is filed literally. That input is cell-store's busiest-hour forecast, which the prompt does not fix. The data fix it. Cell-store use is 99.26% explained by `machines_in_service` and batch-train's hourly use, and the same model with batch at its guarantee backtests all 8 quarterly busiest hours within +160 to +251 cores. The tier peaks at 99.9 to 100% of its guarantee in every quarter on file. Solved together, 109,000 is the largest feasible whole thousand: at 110,000 the cell-store reservation is 38.2k to 38.3k and the remainder is 109.4k, which is under 110,000. The result is stable to cell-ctl method, rounding order and the peak-hour noise uplift.

## Literal reading and the options where the text is silent

| Silent point | Options | Answer each gives | Closed by |
|---|---|---|---|
| Machines in service | plan 5,220 / actual Dec 4,640 | 726,624 / 645,888 reservable | CS-3 2.1 and memo (the plan); closed |
| Firm reservation | request / request held to budget at 7.42 | 580,200 / 576,972 | CS-3 3.2, 3.3, rate R117 effective 2027-01-01; closed |
| cell-ctl forecast | line through quarterly maxima / machines driver / time trend | 1,999 / 2,026 / 1,960 (all 2,000 to the nearest 1,000) | no fork |
| cell-store forecast method | trend of maxima / machines only / two drivers with batch at 2026 level / two drivers with batch at guarantee | G = 122,000 / 120,000 / 120,000 / 109,000 | data (see Evidence); not stated in text |
| Batch level at cell-store's busiest hour | 2026 level (57k) / ML note 0.6 x 149,100 = 89,460 / guarantee | 120,000 / 113,000 / 109,000 | history (see residual fork) |
| Order of rounding | exact vs rounded platform and firm figures | 109,624 to 109,652 leftover, floor 109,000 in every case | no fork |
| Preemption denominator | July to September clipped / whole-run / runs starting in window | shares differ for 4 of 6 teams at 2 decimals | "for July to September 2026" (minor, see below) |
| Lost-work start | write_started / committed | 121,830 / 117,354 (ranking-ml) | data dictionary: state is snapshotted at write_started; closed |
| Machine pairing | machine_id / asset via inventory Cluster ids | breaks for re-registered machines / correct | inventory sheet "Cluster ids"; Layer 1 |

## Evidence (recomputed from the bundle)

**Main call**
- Machines in service: 261 racks x 20 = 5,220 (`c22_hardware_plan_2027Q1_rev2026-12-11.xlsx`, Racks and By quarter sheets). Reservable = 5,220 x 96 x 1.45 = 726,624. Reproduced.
- Firm reservations: floor(Jan 2027 C-22 budget / 7.42) against each request. Search-api (126,415), pricing (76,819) and reco-serve (52,088) are held. The total is 576,972, which rounds to 577,000. Reproduced from `capacity_requests_2027Q1.csv`, `tech_budgets_2026_Q1-2027_freeze.xlsx` (Compute budgets sheet) and `tenant_directory.json`.
- Monitoring export: 17,081 distinct hours after dropping the re-sent 17 March 2026 day (identical rows), and 7 hours missing on 19 August (01:00 to 07:00 UTC), which matches the operations log in Madrid time. Reproduced.
- Cell-store fit on `machines_in_service` and batch-train over those hours:
  - With an intercept: 2.9402 per machine and 0.2081 per batch core (no-intercept fit: 2.947 and 0.2082).
  - Residual s.d. 62.0, R2 0.9926. Reproduced.
  - Coefficients are stable across 2025, 2026 H1 and after the 21 July cell-store release (2.945 to 2.952 and 0.208).
  - The coupling is directly visible in the drain hours: on 9 Sep 02:00 to 04:00 UTC batch goes to 0 and cell-store falls by about 11.8k.
- Cell-store prediction at 5,220 machines and batch at 109,000 is 38,019 to 38,078 cores, which gives 38,000 to the nearest thousand. Reproduced. Cell-ctl is 2,000 under every method tried. Reproduced.
- Fixed point: G=109,000 has leftover 109,6xx and is feasible. G=110,000 needs cell-store about 38.23k to 38.29k, leaves about 109.4k, and is infeasible. Adding the observed +215 to +265 peak-hour uplift still gives 109,000. The 1.208 reservable cores per guaranteed core reproduces.
- Backtest of the golden's structure: prediction = 2.94 x start-of-quarter plan machines + 0.208 x ledger guarantee. Errors against the actual busiest hour are +229, +171, +229, +160, +217, +219, +225 and +251 for 2025Q1 to 2026Q4. This is a near-constant bias, as expected from peak noise.
- The trend-of-quarterly-maxima route errs by roughly 500 in the same history and cannot see the +640-machine step in 2027 Q1.
- Alternatives produced from the files:

| Route | Guarantee |
|---|---|
| Line through quarterly maxima | 122,000 |
| Machines only (or two drivers, batch at 57k) | 120,000 |
| Two drivers with the load added once at 122,000 | 106,000 |
| ML note 0.6 x 149,100 | 113,000 |
| Golden | 109,000 |

- Counter-evidence to the 113,000 route: the same ML note's monthly plans average 91.2k (Feb) and 93.4k (Mar) cores, which is above 89,460, so 0.6 x sum of peaks cannot be the busiest hour of 2027 Q1.
- C-22 has held 99.9 to 100% of its guarantee at its busiest hour in every quarter on file (`mad1_cells_quarterly_summary_2025-2026.xlsx`; Q3 report 1,578 hours at 99% or more). Cell-store's top-30 hours of 2026Q3 all sit at 99.3 to 99.8% of the guarantee.

**Supplementary answers (all reproduced exactly to the stated rounding)**
- Preemption losses, from `batch_runs`, `batch_checkpoints`, `batch_resizes`. Lost work runs from the restored checkpoint's `write_started_utc` to the preempted run's end, with resizes applied. One chain, job-7204868, has a run that restores another run's checkpoint; the lost interval for that run starts at its own start.

| Team | Lost core-hours | Share |
|---|---|---|
| ranking-ml | 121,830 | 0.398% |
| pricing-ml | 80,513 | 0.369% |
| fraud-ml | 48,525 | 0.311% |
| reco-ml | 144,274 | 0.590% |
| demand-ml | 71,995 | 0.489% |
| nlp-ml | 134,899 | 0.770% |

  These match the golden figures 121,800 / 0.40, 80,500 / 0.37, 48,500 / 0.31, 144,300 / 0.59, 72,000 / 0.49 and 134,900 / 0.77. The golden writes 0.40% for ranking-ml at two decimals, but the exact share is 0.398%, which is 0.40% only after rounding to two decimals.
- Machine-hours: the cluster manager duplicates events on 19 August (4 exact duplicate rows). Machine ids map to assets through the inventory "Cluster ids" sheet. 7 hw_fault removals never came back and are excluded. Hours clipped by month: July hw 748.1 and maintenance 851.3, August 731.2 and 909.2, September 662.1 and 882.7. These give 750/850, 730/910, 660/880. Reproduced. Clipping by month, by start month and by end month agree.
- Chargeback: Q3 ledger reservations, plus the quota changes counted from the first 00:00 UTC after the reconciler run that applied them, at 7.65 until 31 August and 7.70 from 1 September, divided by days in the month. Computed values:

| Tenant | Owed (EUR) |
|---|---|
| search-api | 2,652,993 |
| avail-cache | 2,148,194 |
| pricing | 1,594,272 |
| booking | 1,204,894 |
| payments | 696,703 |
| reviews | 506,815 |
| reco-serve | 1,104,080 |
| ads-listings | 822,907 |
| notify | 409,178 |
| partner-gw | 658,477 |
| settle-batch | 488,499 |

  These match all 11 golden amounts to the nearest 100. Using request time instead of applied time would move several tenants by 200 to 1,000, so policy 2.2 (applied by the quota service) is what closes it.

**Residual forks (neither flips a committed answer under the shipped text)**
1. Batch busiest-hour level. The text never says "batch at its guarantee", and CS-3 5.2 only caps batch use. The files close it as shown above: eight quarters of 99.9 to 100%, the eight-quarter backtest, and the ML note's own monthly plans contradicting its 0.6 estimate. Risk: low to moderate. A one-line pin in the memo, such as "platform reservations are sized with batch running at its guarantee", would file the WHAT without giving the HOW. It would change what solvers see, so it is optional and only worth doing if a returned finding calls for it.
2. Preemption share denominator. "All the core-hours its runs held" is clipped to July to September, which follows the table's period. Using whole-run lifetimes gives reco-ml 0.58% and nlp-ml 0.76%, and using only runs that started in the window gives reco-ml 0.60% and nlp-ml 0.78%. Lost core-hours are unaffected. Risk: low.
3. Non-decisive: the quoted 2.94 per machine reproduces only with an intercept (2.947 without one). Both give 38,0xx for cell-store.

## Files/Hygiene

PASS.
- 24 files in 6 formats: PDF x4, CSV x11, XLSX x5, DOCX x2, JSON x1, TXT x1. The largest file is the usage export at 239,470 rows.
- Operational artefacts read as system exports with real irregularities: re-sent day, collector gap, duplicate cluster-manager events, re-registered machine ids, superseded hardware plan revision, Madrid local time in the log against UTC in the exports.
- Temporal coherence holds. The ledger approval date matches the Q3 report, the Q3 report reserved figures sum to its reservable cores including "Not reserved 484", the quarterly summary matches the ledger and plan, the dates on the drain events align between the log (Madrid) and the run/usage data (UTC), and nothing postdates the 14 December pull.
- No authoring or benchmark language. The README is an in-fiction file list.
- Fictional company and data, so there is no public-data contamination.
- Distractors weighed but unused by the solution: ML Platform demand note, quarterly summary of other cells, Q3 capacity report, the unused reconciler and machine data for the main call. I did not read `metadata.json`.
- No exclusion-level finding.

## Stump power

Moderate to high, for an analytical reason. The easy route reads the quarterly busiest hours the export reports and extends them one quarter. It gives 122,000, because cell-store's busiest hour is in fact driven by the machine count (a +640 step on 1 Jan) and by batch use, and batch use rises with the guarantee being set. A stronger analyst who adds the machine driver but keeps batch at its 2026 level files 120,000. Only the analyst who finds the batch coupling and solves guarantee and reservation together reaches 109,000. Nothing in the pack hands over the coupling. The quarterly summary and Q3 report show the 99.9 to 100% pegging but not the cell-store dependence.

## Stumping type

`mechanism: forecasting` (with method_or_model_selection on honest data), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
The reported quarterly peaks are all correct. The difficulty is a forecast the correctly-read past does not pin, because the future differs by a known structural step and a simultaneity between the decision and the forecast quantity. On perfectly clean data the task still stumps. Banned type not raised.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`.
- Domain: sizing a platform service's peak load from its drivers under the capacity standard, and testing that model against history, is capacity planning. A swap to another field's nouns does not read the same.
- Layer 1: duplicated day, collector gap, UTC against Madrid time, superseded plan revision, re-registered machine ids, checkpoint write against commit times.
- Layer 2: modelling cell-store's busiest-hour use on its two drivers and solving it jointly with the guarantee.
- Easy route and wrong answer: extend the quarterly busiest hours, giving 122,000, or add machines but keep batch at its 2026 level, giving 120,000.
- Planted defects, withheld rules and field semantics sit only in lower steps and the asks (checkpoint write against commit, cluster ids, applied time).

## Fix

none. Optional only: see residual fork 1 (file the batch-at-guarantee condition in the memo), which changes what solvers see and is not required.
