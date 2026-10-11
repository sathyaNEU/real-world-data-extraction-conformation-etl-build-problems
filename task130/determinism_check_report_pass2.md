# determinism-check report, task130, 2026-10-10 (pass 2)

This is the one re-judge allowed after the pass-1 FIX_NOW. The judge standard is `guidelines/determinism_judge_system_prompt.md` v3. There is no `target.zip`, so `target/` was copied fresh to `/tmp/determinism-check-task130-pass2-1791676437/target/`. The judge output is at `/tmp/determinism-check-task130-pass2-1791676437/verdict.md`.

**Isolation, read this first.** This runtime has no `Agent` tool, so no separate judge thread could be spawned. The judge pass ran inline under procedural isolation, the same way as pass 1:

- Until `verdict.md` was written, the only inputs read were the scratch copy of the bundle, `prompt.md`, the graded blocks of `submission.md` and the judge system prompt.
- `DESIGN_NOTE.md`, `metadata.json`, `golden/` and the pass-1 report were opened only after the verdict was fixed. `generator/` was never opened.

If the author wants a structurally isolated verdict, re-invoke from a runtime that has `Agent`.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (metadata only: the saved date of `moveon_plan_2026-27.xlsx`. No cell changes and no rerun.)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
All eleven claimed figures and all 24 cells of the month-end table reproduce from the bundle.

Three findings force the call:

1. **The allocation rule is pinned by history.** Replaying `moveon_lets_2018-04_2026-09.csv` in tenancy-start order against open main-duty cases puts 5,262 of 5,262 lets at the front of their size list. The lists are ranked by decision_date then case_ref, use the need in force on the let date, and include households wherever they live. Every alternative ordering fails the replay.
2. **The need definition is pinned** by the prompt and by procedure point 5, and no review falls after 18 September.
3. **The plan's Notes sheet states that October includes the accepted lets.**

The gates pass. The one finding is hygiene (temporal coherence) in the move-on plan workbook. It is not exclusion-level.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| CC1 households at end of 30 Sep (ta_placements, Tenter House, placement_end empty) | 170 | 170 (HPR/24/01511, ended 2026-09-30, excluded) | yes |
| CC1 by need 1/2/3/4+ (latest review, else bedrooms_needed_at_decision) | 28/66/50/26 | 28/66/50/26 | yes |
| All 170 owed main duty, case open (homelessness_cases) | yes | 170/170 | yes |
| Step 3 lets replayed (moveon_lets, Tenancy started) | 5,262 | 5,262, all at list front | yes |
| Step 4 accepted lets at list fronts | yes | 18 accepted (17 Oct, 1 on 3 Nov), each exactly at its list's front | yes |
| Step 5 Oct-Mar reach (moveon_plan, Revised 14 Sep 2026) | 89/117/56/19 | 89/117/56/19 | yes |
| CC2 / main call, households on 31 Mar | 46 | 46 | yes |
| Units 1/2/3/4+ | 0/7/20/19 | 0/7/20/19 | yes |
| Run-off 1-bed Oct-Mar | 20,13,8,0,0,0 | same | yes |
| Run-off 2-bed Oct-Mar | 57,46,42,32,21,7 | same | yes |
| Run-off 3-bed Oct-Mar | 46,42,38,34,29,20 | same | yes |
| Run-off 4-bed Oct-Mar | 26,25,24,23,21,19 | same | yes |
| PNG totals 30 Sep to 31 Mar | 170,149,126,112,89,71,46 | same | yes |
| Weekly cost, Lot 3 2027/28 (dps price schedule) | GBP 21,615 | 7x374.93 + 20x444.06 + 19x532.08 = 21,615.23 | yes |
| Lot 3 uplift (dps price schedule) | 3.8% | all four 2027/28 rates = 2026/27 x 1.038 to the penny | yes |

Golden workbook (`golden/tenter_house_replacement_units.xlsx`) and chart (`golden/tenter_house_runoff.png`): every figure agrees with the ledger to the same rounding.

## Competing answers that survived
None survived. Each fork below was tested on the files.

| Fork | Answer it produces | What closes it |
|---|---|---|
| List order by application_date | 65 | Replay matches 251/5,262 |
| Need at decision, reviews ignored | 52 | Replay matches 2,071/5,262; procedure point 5 |
| Lists limited to households in TA | 34 (0/0/17/17) | 828 historical lets went to households not in TA |
| Superseded March plan | 56 | Sheet labelled "superseded" |
| No lets, every current household | 170 (171 from weekly position) | Plan lets; placement ended 30 Sep |
| Rate or proportional share | about 136 to 141 | Cohort sits near list fronts (2-bed positions 0 to 128 of 468) |
| Attrition of cases ahead (850 non-let main-duty closures) | fewer than 46 | Every such closure fell within 120 days of decision, at rank 156 or deeper, and none within 20 places of any reach |
| Accepted lets added on top of October plan | 39 (0/3/17/19) | Plan Notes: "October 2026 includes lets already offered and accepted". This is the closure the temporal finding below weakens. |
| Future need reviews Oct-Mar | noise | Unpredictable case by case; every solver treats it alike |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10+ | 13 | yes |
| Distinct formats | 3+ | 5 (csv, xlsx, docx, pdf, txt) | yes |
| Large file | 25,000+ rows or large DB | ta_placements 27,981 rows | yes |
| Distractors declared, unlabelled | 2+ in metadata.json, none named as such | 3 (housing_register_lets_2025-26.csv, ta_spend_monitoring_2026-27_q1.xlsx, ta_weekly_position_2026-09-28.xlsx); no "distractor" string in any file name or content | yes |
| Distractors relevant, unused | same world, weighed by solver | all three are council TA/lettings artifacts the solution does not use | yes |
| Distractor answering a graded quantity reproduces and is ruled out | arithmetic + shipped fact | the weekly position's 171 (28/67/50/26) = 170 + one 2-bed-need household leaving 30 Sep; placement_end 2026-09-30 and its own 27 Sep stamp rule it out | yes |
| Deliverable count | 1 to 3 | 2 | yes |
| Format family | none required | xlsx + png | n/a |
| Multi-dimensional asks | not stacked lookups | 4-size call-off, cost, 24-cell run-off grid, chart | yes |
| Golden deliverables present | every named file | both present in golden/ | yes |
| Units and rounding stated | every ask | "whole numbers throughout", "pounds to the nearest pound" | yes |
| Prompt shape, 25+ criteria | identifiable, 25+ | shape 02 (forecast across many periods): 24 grid cells + 5 unit counts + cost + call + 2 CCs + chart items, about 35+ | yes |
| Realism | nothing reads LLM-generated | pack and goldens read as council work products. CSVs are very clean. Golden workbook dated 2 November (Finding 2) | yes, with flags |

## Gate G reconciliation
| Field | Judge | Design note |
|---|---|---|
| mechanism | forecasting | method_or_model_selection |
| stumping_family | analytical_non_defect | analytical_non_defect |
| surface_read_dependency | no | no |
| sole_data_defect | no | no |

The flags agree exactly. The mechanism label differs, but both labels are FINE-numbers shapes that pass Gate G. The design note's own description, a rate or survival model against a rank-and-supply model for a run-off forecast, is method selection inside a forecast, which is what the judge read. So this is a naming difference, not a build that reads as one shape from inside and another from outside, and it does not predict a send-back. If the author wants the labels to match, the design note could say `forecasting` (primary), since the ask is a forward run-off.

Distractor check: the judge did not name any declared distractor as the surface read carrying the task. The weekly position appears only as an honest-number decoy (171, correct for 27 September).

The judge's competing-answer set independently reproduced the design note's ladder: R4 34, R5 52, R5' 65, R6 56, R6' 39 and R2 141.

## Stump power (Gate F)
Moderate to good. Reaching 46 needs three independent correct choices that only the lets log reveals:

- decision-date order (getting it wrong files 65)
- current need (wrong files 52)
- lists that include households outside TA (wrong files 34)

The rate or proportional reading lands near 136 to 141, and any wrong path fails the 24-cell grid wholesale.

Too-easy signals:

- Procedure point 3 ("carry on exactly as for every other household") points toward a list model.
- Point 5 and the prompt hand out the need definition.
- A strong model that replays the log will reach 46. The 100 per cent FIFO log is tidy, as pass 1 also noted.

No text should be added. Keep the rule discoverable only by replay.

## Findings, ranked
1. **Temporal coherence, `target/moveon_plan_2026-27.xlsx` (FIX_NOW, metadata only).**
   - The problem: the workbook was last modified 2026-09-14 16:40 (docProps `dcterms:modified` and file mtime), and its title says "revised 14 September 2026". But its "Sep 2026 (let)" column holds full-month actuals, including 25 tenancies that started 15 to 30 September. Its Notes also say October includes accepted lets, and all 18 of those offers were made 15 to 30 September. A file saved on 14 September cannot contain either.
   - Why it matters: this is the only foothold for the 39-unit double-count fork (R6').
   - Fix, in the generator: set the workbook's modified date and file mtime to the 1 October extract run (for example 2026-10-01 07:45). Keep "revised 14 September 2026" as the plan-revision title. No cell changes.
2. **Golden date, `golden/tenter_house_replacement_units.xlsx` (golden only).** The subtitle and docProps say "Prepared ... 2 November 2026", yet the run-off sheet presents 31 October as an expectation, from extracts that stop on 30 September. Re-date it to early October (for example 2 October 2026). No figure moves.
3. **Label, `target/accommodation_register_2026-09.csv` (optional, generator).** The Tenter House contract reads "Block lease 2021-2026", while Corvane's letter has the 1 April 2021 lease running until notice ends it on 31 March 2027. Suggested label: "Block lease from April 2021 (notice served 15 Sep 2026)". This is non-decisional.
4. **Submission step 4 wording (optional, solution block).** "the October lets already accepted" should read "the 18 lets already accepted (17 starting in October, one on 3 November)". The November one also sits at its list's front, so no figure changes.

Pass-1 fixes confirmed in place:

- The price schedule now reads "August 2026 CPI", saved 22 September.
- The golden note matches it.
- CC1 reads "at the end of 30 September 2026".
- The workbook rename is reflected in the prompt, the submission and golden/.

## Next action for the author
In the generator, set `moveon_plan_2026-27.xlsx`'s saved date (docProps modified and file mtime) to 2026-10-01 and re-date the golden workbook to early October. Rebuild, and confirm by diff that no cell in `target/` changed. The verdict and every figure stand as they are. Whether that metadata-only repair needs a third judge pass is your call: the pipeline's one re-judge has been used, and this report does not license another.
