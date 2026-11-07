# determinism-check report, task165, 2026-11-07

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (thread's disposition; main-thread notes under Findings)
**Stumping type:** mechanism: binding_constraint (etl_conformance on the asks), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Author-side note: the main thread is closing two residual ask forks before ship, (a) the monthly rainfall months filed in Eastern local time, and (b) the RG-1 8 July install day made free of rain tips. They are the thread's residual forks 2 and 4. This pass judged the bundle as rebuilt at target.zip sha256 b8c8ebc1...c5197; the closures change the bundle or prompt, so the rainfall ask rows should be re-confirmed after they land (the thread's own note: a prompt change after judging needs a rerun of the affected ask).

## Why
One isolated Sonnet thread (medium) rebuilt the replay from the shipped files only and got A 9.67, B 6.83, C 2.92, D 1.33 events a year, matching the golden at one decimal. C is the least-cost alternative at or under 4 (TM-7 cost difference to D, 30.4). B meets the limit (2.83) only if pump-back ignores the Southside headworks room. The call survived every convention varied (reading-time convention, BAD influent rows, pump start delay, 23 h gap, 24 h wait C 3.42, FM-0142 clock misread C 2.83). All 48 rainfall cells and the five Northside returns reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Events a year A, B, C, D | 9.7, 6.8, 2.9, 1.3 | 9.67, 6.83, 2.92, 1.33 (116, 82, 35, 16 events) | yes (flow parquet, WRP influent CSV, TM-7, Decree 2.2 to 2.3) |
| Pump-back at firm capacity (competing) | B 2.8 | A 5.83, B 2.83, C 0.58, D 0.08 | yes, the easy route |
| Cost D minus C | 30.4 | 30.4 | yes (TM-7 3.1) |
| Rainfall 2025, 48 gauge-months | per submission | all 48 to the hundredth | yes (tips CSV, field-service xlsx, inventory) |
| Northside returns 2021 to 2025 | 261, 214, 300, 302, 372 | same | yes (SCADA, O&M Table 4-1, CMMS) |
| 2025 events vs notices (clock check) | n/a | 54 built, 54 notices match | yes |

## Competing answers that survived
1. Pump-back room rule: no sentence states return flow is limited to 140 MGD minus influent. A literal reader pumping at firm capacity files B (2.8). Closed only by inference (Decree 1.3 headworks rating, influent flat at 140.00 in 10.7 percent of hours, TM-7 3.2 "treated with the plant's influent"). Design fork SF8 covers the 140 figure, not the rule. This is the designed stump, but see Findings.
2. Rainfall month basis: Eastern civil time (golden) vs fixed EST, differing 0.03 in for March and April (RG-1 March 7.54 vs 7.57). Being closed by the main thread.
3. Northside returns method: golden is the level and inflow mass balance; pump curve times runtime gives 263, 245, 336, 350, 429. Files separate them (P-2 impeller trimmed March 2023, WO 2023-01149; curve tested only at commissioning; decree says volume "returned"), but the prompt does not name the method. NOT on the main thread's closing list.
4. RG-1 July switch time: counting the 09:45 to 09:59 tips at 0.01 in adds 0.09 in to July. Being closed by the main thread.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 13 | yes |
| Formats | 3 or more | 4 (CSV, PDF, parquet, xlsx) | yes |
| Large file | 25,000 rows or more | rain tips CSV 219,584 rows (WRP influent 210,385) | yes |
| Distractors | 2 or more in metadata.json, none labelled by file name | wennick_river_stage_daily, cso_overflow_notifications_2025; names are plain data names | yes |
| Distractor weight | unused, relevant, ruled out by a shipped fact | river stage plausible for discharge but the meter records discharge; notices count 2025 without a tank and match the replay, so they do not answer a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, pptx), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 48 rainfall cells, 5 yearly returns, 4 events; one decimal, hundredth of an inch, nearest million gallons stated | yes |
| Prompt | one paragraph under 1,000 chars, question first, no data count | 802 chars; no gauge or alternative count stated | yes |
| Prompt shape and 25 criteria | identifiable, 25 or more | card shape 08; graded figures well over 60 (4 events, selection, 48 rainfall, 5 returns, chart items); the generated rubric itself was not inspected | yes (inferred) |
| Reads as real work product | no LLM tells | thread found no authoring language in PDFs, xlsx notes or CMMS; golden sheets Selection, Events by year, Rainfall 2025, Northside returns; golden-realism not re-run here | yes (thread) |

## Gate G reconciliation
Thread: mechanism binding_constraint, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note and card: allocation under real constraints, drawdown bounded by the receiving plant's room, stump_class analytical, analyst test files B 2.8 on the rating replay and C 2.9 only with the hourly headroom bound. These match. The thread did not name either declared distractor as the surface read, so neither is too load-bearing. Gate H: thread `domain: pass, layers: pass, decisive_step: analytical`; the note's Three rules (task type hydrology-flood-frequency, hospital-ward swap fails, Layer 1 clocks and units, Layer 2 constrained drawdown) agree. No mismatch.

## Stump power (Gate F)
Moderate per the thread: B at 2.8 is cheaper and plausible, but strong models that join the influent record will probably get the call, so some difficulty sits in the exactness of the asks (clock reconciliation, pour removal, 0.2 mm change, level offset). The decisive step is not "the field's standard method applied": it needs a judgment (the room bound) the data must settle, so it is not a plain textbook route; the main thread weighs this against the note's ladder.

## Findings, ranked
1. Pump-back room limit is inferred, not filed. The thread calls it forced by the files but borderline. The design note records that the Appendix C 1.3 sentence stating the holding-back mechanism was deliberately cut to the plant's rating alone. Under CLAUDE.md, a decisive rule left unstated against a stated one is a guard concern; here the filed text (TM-7 3.2, Decree 1.3 rating, influent record) supports it but no sentence says it. Main thread to weigh whether to file the WHAT (the receiving plant's headworks limit applies to the return) without filing the HOW.
2. Northside returns method fork (fork 3) is open and not on the closing list; differs at the nearest MG in every year. Thread suggests "from the tank's own level and inflow record" in the ask.
3. Forks 2 and 4 are being closed by the main thread; re-confirm the affected rainfall cells after the change.
4. Cfs to MGD constant 0.646317 is not in the package; thread treats it as domain knowledge (Gate B passes).
5. Cross-batch fingerprint not checked by the thread (only this bundle readable).

## Next action for the author
Close the two named forks, decide whether to pin the Northside method in the prompt (fork 3), then re-run any ask recomputation touched by the Eastern-time and RG-1 changes before ship; no rerun of the main-call judge is needed unless the main-call text moves.

## Main-thread disposition (round 1)

APPROVE stands; the build ships on this verdict. Each finding:

1. **Pump-back room limit unfiled: kept unfiled (coordinator's call).** It is the stump's own constraint. The files
   force it: Appendix C 1.3 gives the headworks rating, the historian shows Southside's influent flat at 140, and TM-7
   3.2 says the returned flow is "treated with the plant's influent". Filing it would turn the decisive step into rule
   application.
2. **Northside returns method (fork 3): kept unpinned (coordinator's call).** The pump-curve route is the device's
   designed wrong path: P-2's impeller was trimmed in March 2023 and the curve was tested only at commissioning. The
   files point to the mass balance. Pinning "from the tank's own level and inflow record" would hand over the leak-by
   device.
3. **Forks 2 and 4: closed in the generator, not by a sentence on the method.**
   - Fork 2: the prompt files the months "on local Eastern time" (the WHAT). It does not name the UTC loggers.
   - Fork 4: every gauge's mechanism install now falls on a day with no rain at that gauge (RG-1 9 July, RG-2 14 July,
     RG-3 18 July, RG-4 23 July 2025), so the only tips that day are the cal-check pour after the install.
   - `checks.py` asserts both closures. Moving the install days shifted six rainfall cells by 0.01 in each, through
     the bucket remainder: RG-1 November, RG-2 August, September and October, and RG-3 December. All 48 cells were
     re-confirmed against the world's truth. Every main-call figure, the stump and the ladder are unchanged
     (freeze.py rubric PASS).
4. **Cfs to MGD:** domain knowledge, as the thread found (Gate B passes).
5. **Cross-batch fingerprint:** guard.py heart WARN and surface exit 0 on the final cut.

The leak reader's realism notes are fixed in the generator:
- The 2025 notification log gives each outfall its own times and varied action text; Outfall 014's rows are
  unchanged.
- The work orders' task texts now fit each asset class and order type.
- The field service log's creator is the field maintenance contractor, created at its June 2025 mobilisation.

The prompt changed, so one leak re-read runs on the final pack.
