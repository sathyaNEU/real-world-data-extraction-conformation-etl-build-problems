# determinism-check report, task132, 2026-10-11

Pass 1, stage 7 of the author's `/build` run. The bundle was copied fresh from `task132/target/` to `/tmp/determinism-check-task132-20261011T092622Z/target/` (there is no `target.zip`). The verdict is at `/tmp/determinism-check-task132-20261011T092622Z/verdict.md`.

**This pass did not use a separate judge thread.** No `Agent` tool was available inside this orchestrator subagent, so it could not spawn one. The orchestrator ran the judge pass itself, under the same restrictions a thread would have had:
- The judge system prompt (`guidelines/determinism_judge_system_prompt.md`, Gate H included) was applied word for word.
- Inputs were `prompt.md`, the four graded blocks of `submission.md`, and the scratch copy. Nothing else was read.
- Every figure was recomputed with pandas, scipy and openpyxl.
- No server-side tools were used.
- `verdict.md` was written before the orchestrator opened the design note, the card, `metadata.json`, `golden/` or anything else of the author's.

The isolation therefore held, but the pass did not run through the mechanism the agent contract names. If you need a pass from a separately spawned thread, re-invoke from a context that has the `Agent` tool.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (submission wording only: no model rerun, nothing solvers see changes)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical

## Why
The main call is forced. AM-PC-014 pins every input:
- **Failures (5.1):** 210 CM/EM work orders with status COMP or CLOSE, failed component PSU, on VPR-340 relays.
- **Band rates (5.2, 5.3):** module-age rates over the January 2021 to September 2026 module-months.
- **Support (4.1, 4.2):** set by bay from the Approved 2026 sheet.
- **Available modules (section 7):** 12 serviceable plus 3 at Veldtek repair, so 15.
- **The buy (8.1, 8.2):** a Poisson 95 per cent test in whole 25-module lots.

The expected-failure mean of 298.6 sits in the middle of the 287.3 to 311.2 window where 13 lots is the smallest order that passes. 12 lots gives 83.6 per cent and 13 lots gives 99.1 per cent. Every supplementary answer reproduces to its stated decimal.

The one defect is wording, in Step-by-Step Solution step 4: "counting its band rate over twelve while it is likely to survive". Read naturally, that is a cutoff: the present module's rate until its survival falls below one half, then the 0-9 rate. That reading gives 328.8 expected failures and 14 lots. 298.6 reproduces only under the probability-weighted monthly recursion that 6.2's "module-months expected in each band" implies.

## Recomputation ledger
| Figure | Claimed | Judge recomputed (file, field) | Reproduced |
|---|---|---|---|
| PSU failures (5.1) | 210 (workbook) | 210 CM/EM, COMP/CLOSE, `failed_component` PSU, VPR-340 by `asset_id` in the register; all 210 match a FAILED removal by `removal_wo` | yes |
| Rate 0-9 | 0.0052 /module-yr | 15 / 2,905.83 = 0.00516 (module-months on first-of-month status, Jan 2021 to Sep 2026) | yes |
| Rate 10-14 | 0.0233 | 49 / 2,104.42 = 0.02328 | yes |
| Rate 15-19 | 0.0508 | 68 / 1,337.42 = 0.05084 | yes |
| Rate 20-24 | 0.1186 | 66 / 556.33 = 0.11863 | yes |
| Rate 25+ | 0.2945 | 12 / 40.75 = 0.29448 | yes |
| Expected failures to end of support | 298.6 | 298.606 (1,178 relays; each maps to exactly one Approved 2026 row by bay: 1,075 dated, 103 "Not in program period" through Dec 2035) | yes |
| Modules available | 15 | 12 SERVICEABLE + 3 AT REPAIR (`spares_stock`); the 3 equal the 3 OPEN RMAs in the Veldtek register; the 7 in QUARANTINE are excluded | yes |
| Lots / modules / cost | 13 / 325 / CAD 638,625 | 13 / 325 / 325 x 1,965 = 638,625 (EOL-2026-07, HST excluded) | yes |
| 8 lots: cover / cost | 0.0% / 393,000 | 0.0000 / 393,000 | yes |
| 9 lots | 0.0% / 442,125 | 0.0259 / 442,125 | yes |
| 10 lots | 2.6% / 491,250 | 2.6000 / 491,250 | yes |
| 11 lots | 32.2% / 540,375 | 32.2206 / 540,375 | yes |
| 12 lots | 83.6% / 589,500 | 83.6014 / 589,500 | yes |
| 13 lots | 99.1% / 638,625 | 99.1349 / 638,625 | yes |
| 14 lots | 100.0% / 687,750 | 99.9911 / 687,750 | yes |
| 15 to 22 lots | 100.0% / 736,875 to 1,080,750 | 100.0000 / 49,125 per lot | yes (all 8) |
| Oct to Dec 2026 | 11.6 | 11.586 | yes |
| 2027 | 45.1; 1,163 relays | 45.065; 1,163 | yes |
| 2028 | 44.7; 1,094 | 44.675; 1,094 | yes |
| 2029 | 42.9; 973 | 42.881; 973 | yes |
| 2030 | 40.6; 884 | 40.638; 884 | yes |
| 2031 | 36.1; 783 | 36.082; 783 (DS-088's 5 relays out from 1 Jan) | yes |
| 2032 | 30.0; 695 | 30.028; 695 | yes |
| 2033 | 23.9; 564 | 23.876; 564 | yes |
| 2034 | 16.0; 373 | 15.964; 373 (DS-081's 6 relays out from 1 Jan) | yes |
| 2035 | 7.8; 201 | 7.811; 201 | yes |
| North | 117.5 | 117.474 (`substations.csv` region from April 2024) | yes |
| Central | 54.7 | 54.705 | yes |
| South | 126.4 | 126.427 | yes |
| Memo ask 1 | opens on 13 lots, 99.1 vs 83.6 | golden memo opens that way | yes |
| Memo ask 2 | bar chart by year, labels to one decimal | `word/media/image1.png`, 10 bars labelled 11.6 to 7.8 | yes |

The golden workbook's Failure rates sheet (expected module-years 2,206.2 / 1,466.2 / 1,704.6 / 868.9 / 215.1 and expected failures 11.4 / 34.1 / 86.7 / 103.1 / 63.3) also reproduces.

## Competing answers that survived
None. Each fork tested, what it gives, and what closes it:

| Fork | Gives | Closed by |
|---|---|---|
| Present module's aging band rate in every remaining month, no replacement | 431.4, 19 lots | 6.2 counts the module-months *expected* in each band; section 3 ages a replacement from its own fitted date (the stump, not a fork) |
| Band frozen at the count date | 244.5, 11 lots | 5.2 and 6.1, band of the module's age each month |
| Rates by relay age from `install_date` | 249.9, 11 lots | section 3: module age is counted from the module's fitted date |
| Module-age rates applied to relay age | 491.8 with renewal (21 lots), 819.4 without (35) | section 3 |
| Repaired module aged from its first-ever fitted date | 309.3, 13 lots, but every graded figure moves | section 3 and dictionary: "fitted to that relay" |
| Continuous survival exp(-h) instead of S(1 - h) | 299.2, 13 lots; cover 2.4 / 31.0 / 82.7 at 10 / 11 / 12 lots; 2030 to 2033 each +0.1; regions +0.1 to +0.3 | section 3 (in service on the first of the month) with 6.1 pins the discrete monthly recursion; residual rubric-tolerance risk (finding 3) |
| Superseded 2025 plan sheet | 262.5, 11 lots | 4.1, the approved program current at the count date; the sheet is labelled superseded |
| Staged station sent whole to stage 1 / last stage | 273.7 (12) / 324.6 (14) | 4.1, the stage that lists the relay's bay |
| Availability 12 (no at-repair) / 20 (+5 failed modules on returns shelves) / 22 (+7 quarantine) | 13 lots in each case | section 7; only quarantine and shelf together (27) reach 12 lots (P = 95.11%), and both are excluded by section 7 and by the dictionary ("not stock") |
| January commissioning counted as supported on 1 January | 788 (2031), 379 (2034) | 4.1 "up to, but not including", and program Notes row 5 "out of service from that day" |
| Asset-record region | four legacy regions (Lakeshore 67.6, Valley 71.3, Ridge 69.6, Harbour 90.1) | the prompt's "three operating regions" points to the `substations.csv` region |
| Step 4 read as a cutoff at survival 0.5 | 328.8, 14 lots | not a reading of the task, a wording defect in the solution block (finding 1) |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files in the pack | 10+ | 12 | yes |
| Distinct formats | 3+ | 5 (CSV x6, XLSX x3, DOCX, PDF, TXT) | yes |
| Largest file | 25,000+ rows or a large DB | `eam_work_orders_protection_2021-01_2026-09.csv`, 32,569 rows | yes |
| Distractors named in `metadata.json`, none labelled in `target/` | 2+ | 3 (`veldtek_rma_log_vpr340_psu.xlsx`, `feeder_relay_operations_2025.csv`, `pc_relay_maintenance_compliance_2025.xlsx`); grep of every file, including docx/xlsx XML, finds no label | yes |
| Each distractor unused but relevant | same world, has to be weighed | RMA register for the same part (repair outcomes, a tempting failure source); the same relays' 2025 trip duty; the same relays' 2025 test compliance. The solution uses none of them | yes |
| A distractor that answers a graded quantity reproduces and is ruled out | if any | none answers the call or a graded figure. The compliance file's VPR-340 rows (192 / 85 / 173) reproduce from the work orders. RMA receipts as a failure count would undercount (93 failed modules were scrapped by the stores and never reached Veldtek), and 5.1 rules them out | yes |
| Deliverables | 1 to 3 | 2 (`vpr340_psu_final_buy.xlsx`, `psu_last_time_buy_memo.docx`) | yes |
| Format family | none required | data workbook and text memo | n/a |
| Multi-dimensional asks | not stacked lookups | cover and cost over 15 orders, 10 periods with 9 supported counts, 3 regions, all off the one renewal forecast, so the stump route misses all of them together | yes |
| Goldens present | every named file | both in `golden/` | yes |
| Unit and rounding stated | in the asking sentence | stated for every ask. The cost column inherits "in dollars to the nearest dollar" from the sentence before, and its values are whole dollars by construction | yes |
| Prompt shape, 25+ criteria | shape identifiable, 25+ | a single dial (lots against a 95% bar) with a period forecast underneath (shape 04). About 59 criteria (3 + 30 + 10 + 9 + 3 + 2 memo + 2 files) | yes |
| Realism, pack and goldens | no LLM tells | pack: crew shorthand by person, cancelled duplicates, follow-up fitting orders, mixed RMA customer names and reference formats, 1 July conversion dates, the region recode, Excel and LibreOffice containers. Memo: letterhead, To/From/Re, signature line, chart, no em dashes. Workbook: notes cite the procedure. None found | yes |

## Gate G reconciliation
| Field | Judge (fixed before reading the design) | Design note / card | Match |
|---|---|---|---|
| mechanism | forecasting | forecasting (`gate_g`) | yes |
| stumping_family | analytical_non_defect | analytical_non_defect | yes |
| surface_read_dependency | no | no | yes |
| sole_data_defect | no | no | yes |
| Gate H domain | pass | `domain_test`: renewal forecast of PSU failures over each relay's support, utility asset-condition and spares work | yes |
| Gate H layers | pass (go-live dates, region recode, PSU order noise, staged bays, superseded sheet, stock states / renewal forecast) | Layer 1 list and the `own:renewal-of-replaced-modules-in-a-spares-forecast` pattern | yes |
| Gate H decisive_step | analytical; easy route 431.4, 19 lots | `stump_class` analytical; `analyst_test` 431.4, 19 lots instead of 13 | yes |
| Distractor as surface read | none of the three named | `metadata.json` declares them unused | yes |

The task reads the same shape from outside as from inside, and the same wrong route lands on the same figure. One note from the design that the judge could not see: in round 2 (seed-150 world) both solvers named the renewal reading (about 298, 13 lots) and declined it "because the procedure does not spell it out", and the design note asks the judge to rule on that. The ruling here is that it is forced, not a fork. Section 1 and the prompt say failed modules are replaced from the buy. Section 3 ages a module from the date it was fitted to that relay and counts it in service only while fitted. 6.2 applies the rates to the module-months expected in each band. Keeping the old module's age after a failure therefore contradicts section 3.

The portal reviewer, though, applies the contrasting-model rule ("a model that reaches the intended insight and still disagrees is not stumped" unless the golden re-derives from the rules read literally). The blocks should carry that literal chain so the reviewer finds it without reconstructing it (finding 2).

## Stump power (Gate F)
The renewal step is the trap. Read directly, 6.1 says "each month a module is in service it is expected to fail at the monthly failure rate of its band". That invites charging every present module its aging band rate for every remaining month. 152 present modules are already in the 20-24 and 25+ bands, at 0.119 and 0.294 failures a year. On that route expected failures come to 431.4 and the order to 19 lots, and the same error misses every year from 2027 and every region (North 174.3, Central 77.2, South 179.9).

Too-easy signals:
- The task rests on one rung. AM-PC-014 narrates every other step (failure definition, exposure period, support by bay, availability, Poisson 95%), which disarms the Layer 1 devices.
- For any mean near 298.6, 9 of the 15 cover cells are 100.0 and 2 are 0.0, so the cover column grades only routes that move the mean a long way. The stump route does that.

No lever is required for determinism. Hardening, if the portal says so, belongs to the solver loop, not this pass.

## Findings, ranked
1. **FIX_NOW, `submission.md` Step-by-Step Solution step 4.**
   - **Problem:** "counting its band rate over twelve while it is likely to survive" reads as a cutoff. Implemented literally it gives 328.8 and 14 lots, not 298.6 and 13. A reviewer checking that "the numbered path leads to the recommendation" can file SOLUTION_WRONG on it.
   - **Fix:** state the recursion. For each relay, S = 1 on 1 October 2026. Each month, expected failures = S x (band rate / 12) + (1 - S) x (0-9 rate / 12), then S becomes S x (1 - band rate / 12), to the month before support ends. A replacement is in service from the next first of the month and is aged from its own fitted date (AM-PC-014 3, 6.1, 6.2).
   - **Same wording in the memo:** the memo's "How the figure is built" paragraph says "for as long as it is likely to still be there". The workbook's Notes row 3 already has it right ("by the chance it has not yet failed").
2. **FIX_NOW, `submission.md` steps 4 and 8 and the Final Recommendation's "Not the present module's band rate..." sentence.**
   - **Why:** round-2 solvers declined the renewal as unstated, so a portal response may do the same.
   - **Fix:** cite the chain that forces the renewal: section 1 and the prompt (failed modules are replaced from the buy), section 3 (age from the fitted date, in service only while fitted), and 6.2 (module-months expected in each band). That gives the reviewer the literal re-derivation the contrasting-model rule asks for. No prompt or file change.
3. **Risk, rubric tolerance.**
   - **Problem:** the one-decimal cover and failure figures assume the discrete monthly survival. exp(-h) gives cover 2.4 / 31.0 / 82.7 at 10 / 11 / 12 lots (against 2.6 / 32.2 / 83.6), 2030 to 2033 each +0.1, and regions +0.1 to +0.3, while staying on 13 lots.
   - **Fix:** the recursion in finding 1 pins it for the rubric generator. Nothing else is needed.
4. **Optional, Critical Components.** The block carries three items. The five band rates (15, 49, 68, 66 and 12 failures over 2,905.8, 2,104.4, 1,337.4, 556.3 and 40.8 module-years) are the most load-bearing intermediates and are already on the workbook's Failure rates sheet. Listing them gives the critical-components weight more to grade.
5. **Not checked here.** The cross-batch reference check was not run (this pass was isolated from other task folders), and the adjudicated duplicate check belongs to stage 5.

## Next action for the author
Rewrite step 4 of `submission.md` (through `submission-writeup`) to state the survival-weighted monthly recursion and cite AM-PC-014 sections 1, 3, 6.1 and 6.2. Then re-judge once. No figure, rung or input document moves, so no fresh solver round is needed first.
