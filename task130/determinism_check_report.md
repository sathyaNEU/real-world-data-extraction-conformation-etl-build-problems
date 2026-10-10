# determinism-check report, task130, 2026-10-10

Pass 1 on the v2 architecture (Tenter House call-off). The judge applied `guidelines/determinism_judge_system_prompt.md` v3. Its verdict file is at `/tmp/determinism-check-task130-1791675610/verdict.md`, and the bundle was copied fresh from `target/` into `/tmp/determinism-check-task130-1791675610/target/`. There is no `target.zip`, so the unzipped `target/` was used.

**How this pass deviates from the protocol.** This runtime has no `Agent` tool, so no separate judge thread could be spawned. I ran the judge pass inline instead, under the same read discipline:
- Until `verdict.md` was written, the only things read were the scratch copy of the bundle, `prompt.md`, the graded blocks of `submission.md` and the judge system prompt.
- `DESIGN_NOTE.md`, `metadata.json`, `pipeline.json`, `leak_check_report.md`, `golden/` and `generator/` were opened only after the verdict was fixed. `generator/` was never opened.

The isolation is therefore procedural, not structural. If the author wants a structurally isolated verdict, re-invoke from a runtime that has `Agent`.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW. One non-decisional wording change in `dps_lot2_lot3_price_schedule.xlsx`, plus one optional clarification in a submission block. No rate, count or decisive artifact changes, and no model rerun is needed.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The call-off of 46 units (0 one-bed / 7 two-bed / 20 three-bed / 19 four-bed) follows from three things in the pack:
- **Who is in the block, and at what size.** The 170 live Tenter House placements come from `ta_placements_2018-04_2026-09.csv`. Their current need comes from `bedroom_need_reviews.csv`, which closure procedure point 5 and the prompt make the basis.
- **The order lets follow.** Nothing in the pack states it, but the history pins it completely. If you replay every one of the 5,262 started lets in `moveon_lets_2018-04_2026-09.csv` at its tenancy start date, each one went to the open main-duty case on that bedroom-size list with the earliest `decision_date` (ties broken by `case_ref`). That list includes households living at home. All 5,262 reproduce. Ordering by application date instead fails 5,011 times. A list limited to households in TA fails all 234 lets that went to households at home.
- **How many lets there will be.** Working the plan sheet "Revised 14 Sep 2026" down those lists gives exactly the golden month-end table.

Every competing answer is ruled out by a shipped fact. No tie in decision date falls on any month-end cut-off. Households that close for other reasons (own arrangements, moved away, contact lost) have done so only at list position 145 or later, which is behind every Tenter House household still waiting, so attrition does not move the count.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Households in Tenter House, 30 Sep 2026 (CC1) | 170: 28 / 66 / 50 / 26 | 170: 28 / 66 / 50 / 26 (`ta_placements` with no placement_end, accommodation_type Tenter House; need from latest review, otherwise need at decision) | yes |
| Every household there owed the main duty (step 1) | 170 of 170 | 170 of 170 are Main duty accepted and Open (`homelessness_cases`) | yes |
| Lets replayed front-of-list (step 3) | 5,262 | 5,262 of 5,262 (`moveon_lets` Tenancy started, ordered by tenancy_start; list = open main-duty cases by `decision_date` then `case_ref`, need at that date) | yes |
| Accepted October lets at the front of their lists (step 4) | yes | yes in all four sizes (6 / 8 / 3 / 1 accepted; one two-bed starts 3 Nov, which makes no difference) | yes |
| Oct-Mar plan lets (step 5) | 89 / 117 / 56 / 19 | 89 / 117 / 56 / 19 (`moveon_plan_2026-27.xlsx`, sheet Revised 14 Sep 2026) | yes |
| Plan Apr-Sep actuals against the lets log | n/a | match cell for cell | yes |
| Still there 31 Mar 2027 (CC2, Final Recommendation, deliverable answer 1) | 46: 0 / 7 / 20 / 19 | 46: 0 / 7 / 20 / 19 | yes |
| Weekly cost at Lot 3 2027/28 rates (deliverable answer 2) | GBP 21,615 | 7 x 374.93 + 20 x 444.06 + 19 x 532.08 = 21,615.23, so 21,615 (`dps_lot2_lot3_price_schedule.xlsx`, 2027/28 column) | yes |
| Month-end one-bed (deliverable answer 3) | 20, 13, 8, 0, 0, 0 | 20, 13, 8, 0, 0, 0 | yes |
| Month-end two-bed | 57, 46, 42, 32, 21, 7 | 57, 46, 42, 32, 21, 7 | yes |
| Month-end three-bed | 46, 42, 38, 34, 29, 20 | 46, 42, 38, 34, 29, 20 | yes |
| Month-end four-bed | 26, 25, 24, 23, 21, 19 | 26, 25, 24, 23, 21, 19 | yes |
| Chart totals (PNG answer 1) | 170, 149, 126, 112, 89, 71, 46 | 170, 149, 126, 112, 89, 71, 46 | yes |
| Golden workbook and PNG | same figures | both agree with the submission to the unit and the penny | yes |

## Competing answers that survived
None. Each fork below was tested and closed:

| Fork | Answer it produces | What closes it |
|---|---|---|
| No run-off (a unit for every household now in the block) | 170 | six months of planned lets; the lets log |
| Proportional share of the plan's lets over each list | about 141 | 100 per cent decision-date order in the lets log |
| Trailing Apr-Sep 2026 let rate run for six months | 43 (0 / 0 / 22 / 21) | the revised plan is the forward supply and names the Brook Meadow handovers |
| Queue ordered by application date | 65 (3 / 17 / 26 / 19) | the replay: 5,011 lets go out of order |
| Queue of households in TA only | 34 (0 / 0 / 17 / 17) | 234 historical lets went to households at home |
| Need at decision, ignoring reviews | 52 (2 / 11 / 29 / 10) | prompt ("current assessed bedroom need") and procedure point 5 |
| Original March plan | 56 (0 / 7 / 26 / 23) | the sheet is titled "(superseded)" |
| Accepted October lets counted again on top of the October plan | 40 (0 / 4 / 17 / 19) | plan Notes: "October 2026 includes lets already offered and accepted" |
| Flat sizes instead of need | 28 / 67 / 57 / 18 basis | prompt and procedure point 5 |
| 2026/27 rates | GBP 20,824 | price schedule note: 2027/28 rates apply from 1 April 2027 to every unit; procedure point 6 |
| 171 households (weekly position, 27 Sep) | starting stock off by one two-bed | `ta_placements`: HPR/24/01511 left TH-234 on 30 Sep 2026 for a social let; no effect on any month-end figure |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 13 | yes |
| Distinct formats | 3 or more | 5 (csv, xlsx, docx, pdf, txt) | yes |
| Large file | one file of 25,000+ rows, or a large database | `ta_placements_2018-04_2026-09.csv`, 27,981 rows | yes |
| Distractors declared | 2 or more in `metadata.json`, none labelled in the pack | 3 (`housing_register_lets_2025-26.csv`, `ta_spend_monitoring_2026-27_q1.xlsx`, `ta_weekly_position_2026-09-28.xlsx`); no file name or content labels them | yes |
| Distractors relevant but unused | same world, has to be weighed | all three are TA and lettings artefacts for the same borough and period; the solution uses none | yes |
| A distractor that answers a graded quantity reproduces and is ruled out | arithmetic plus a shipped fact | the weekly position (171; 28 / 67 / 50 / 26; flats 30 / 72 / 58 / 18, occupied 28 / 68 / 57 / 18) reproduces exactly from `ta_placements` and the register at 27 Sep; ruled out by the 30 Sep extract (one two-bed let that day) and by the six months of lets | yes |
| Deliverables | 1 to 3 | 2 (xlsx, png) | yes |
| Format family | none required | n/a | n/a |
| Multi-dimensional asks | not stacked lookups | call-off by four sizes plus total, cost, a 24-cell month-end grid, chart | yes |
| Golden deliverables present | every file the prompt names | both present in `golden/`, figures agree | yes |
| Units and rounding stated | inside each ask | "whole numbers throughout", "in pounds to the nearest pound" | yes |
| Prompt shape and 25-criteria floor | identifiable shape, 25+ | shape 02, forecast across many periods; about 34 (5 call-off + 1 cost + 24 cells + about 4 chart parts) | yes |
| Realism | nothing reads as LLM-generated | pack reads as council extracts and documents; golden workbook and chart read as a real work product. One temporal flag (Finding 1). The lets log being 100 per cent FIFO is tidier than a real allocation log (Finding 3) | yes, with flags |

## Gate G reconciliation
| Field | Judge | Design note | Match |
|---|---|---|---|
| mechanism | forecasting | method_or_model_selection | label differs, same family |
| stumping_family | analytical_non_defect | analytical_non_defect | yes |
| surface_read_dependency | no | no | yes |
| sole_data_defect | no | no | yes |

The mechanism labels differ in name only. The design note calls the stump picking a rank-and-supply model over a rate or survival model. The judge calls it a forward run-off the trailing rate does not pin. Both are FINE-numbers shapes that pass Gate G, and both describe the same decisive rung, so this does not predict a send-back. If the portal reviewer has to pick one label, forecasting fits the prompt better (a forward quantity across six periods). Method selection is how the forecast is reached.

`metadata.json` check: the judge did not name any declared distractor as the surface read carrying the task. The weekly position is correct and is not the stump; the stump is the rate model a solver would build from `ta_placements` and `homelessness_cases`. The distractor is not too load-bearing.

The design note itself is out of step with the shipped build (Finding 2):
- Its stump sentence and ladder answer row still say 48 (0 / 8 / 21 / 19), and its R0 still says 173. It also says "the build record at the end carries the shipped values", but there is no build record section.
- Rungs R6 and R6' are still marked "to measure". Measured here, they are 56 (0 / 7 / 26 / 23) and 40 (0 / 4 / 17 / 19).
- Both of those rungs break the property the note says is asserted, that no rung matches the answer in more than one size. R6 matches the answer for one-bed and two-bed; R6' matches for one-bed and four-bed.

## Stump power (Gate F)
Good. The rung that decides the task is realising that a Tenter House household leaves only when the plan's lets reach its place in a borough-wide queue ordered by decision date, a queue that also holds households living at home. Each wrong path files a far-off answer: a leaving rate or proportional share gives about 140, application-date order 65, a TA-only queue 34, the trailing let rate 43.

Too-easy signals are present but none touches that rung: the March plan sheet is titled superseded, the prompt and procedure point 5 pin the need basis, and the price schedule note pins the 2027/28 year. The deciding rule is not written down anywhere; it is found by asking who got each let. That is computation, not rule-discovery, so the "single derivable fact" warning does not apply.

## Findings, ranked
1. **Temporal coherence, `dps_lot2_lot3_price_schedule.xlsx` (FIX_NOW).** The note row reads "uplift by September 2026 CPI, 3.8 per cent", but the file was last modified 22 September 2026, before any September CPI figure could exist (it is published in mid-October).
   - Fix in the generator: change "September 2026 CPI" to "August 2026 CPI". No rate changes.
   - Make the same change in the golden workbook's Call-off note ("September 2026 CPI uplift of 3.8 per cent").
   - The text is not decisional, so the analytic surface stays equivalent.
2. **Design note out of step with the build (bookkeeping, not shipped).**
   - Update the stump sentence and ladder to 46 (0 / 7 / 20 / 19) and R0 to 170 (28 / 66 / 50 / 26).
   - Fill in R6 = 56 (0 / 7 / 26 / 23) and R6' = 40 (0 / 4 / 17 / 19).
   - Add the build-record section the note promises.
   - Either drop the "no rung equals the answer in more than one size" claim or note that R6 and R6' break it. If the generator really asserts this, check why it passed.
   - The ask-pair arithmetic is barely affected: on the 24-cell grid, R6 misses 14 cells and R6' misses 16.
3. **Realism risk, `moveon_lets_2018-04_2026-09.csv` (low, no change advised).** Every one of 5,262 lets goes exactly to the front of the queue: no refusals, no direct offers, no management moves. A reviewer may read that as too tidy for a real allocation log. Adding exceptions would weaken the determinism the replay gives, so leave it unless a reviewer objects.
4. **Submission CC1 wording (optional, solution block only).** HPR/24/01511 moved out on 30 September, so "living in Tenter House on 30 September" could be read as 171. Saying "at the end of 30 September 2026" closes the reading. No figure changes.

## Next action for the author
In the generator, change the price schedule's uplift note to "August 2026 CPI" and make the same change in the golden workbook's Call-off note. Rebuild the pack, then re-judge once, as the FIX_NOW loop allows.
