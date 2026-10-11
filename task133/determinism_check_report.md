# determinism-check report, task133, 2026-10-11

Judge pass 1, run at `/build` stage 7. The judge standard is `/home/user/wt133/guidelines/determinism_judge_system_prompt.md` (the Gate H edition), applied as written. The scratch copy at `/tmp/determinism-check-task133-20261011T071917Z/target/` is byte-identical to `target/` (checked by sha256). The judge's verdict is `/tmp/determinism-check-task133-20261011T071917Z/verdict.md` (sha256 `fa9f379c...bece33`). It was locked before any author-intent file was opened.

**Run note, a deviation from the agent contract.** The orchestrator's runtime had no `Agent` tool, so no separate judge thread could be spawned. The judge pass ran in the orchestrator thread instead, with isolation kept by ordering. Until `verdict.md` was written and hashed, the only files read were `prompt.md`, `submission.md` (to extract the blocks), the judge system prompt and the scratch copy. `DESIGN_NOTE.md`, `metadata.json` and `golden/` were opened only afterwards. `generator/`, `START_HERE.md`, `pipeline.json`, `leak_check_report.md` and `solver_rounds/` were never opened. No server-side tools, web access or subagents were used. If you want the separate-thread form, re-invoke in a runtime that provides the `Agent` tool.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (solution wording only, no model rerun)
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical

## Why
CRM-ECL-04 pins every step of the build:

- stage 3 at 90 or more days past due;
- the three stage 2 triggers, and the dates-and-cancellation rule for when a hardship arrangement is in force;
- the remaining term counted from repayments fallen due, including the past-maturity rule;
- LGD, the re-amortised EAD and the contract-rate discount;
- rounding only at reporting, and the scenario weighting.

The Q1 FY27 sheet, the migration note and the curve header pin the inputs. The one step left to the analyst is turning the curve, which is indexed from origination, into a performing loan's forward PD: [C(m+k) - C(m+k-1)] / (1 - C(m)). That follows from the curve's own definition ("a new loan"). Under it, the main call and every workbook figure reproduce exactly (allowance AUD 13,772,790.12). The FIX_NOW is a Gate E caution on the two pptx committed answers, which grade presentation choices the prompt does not pin.

## Recomputation ledger
Every value was recomputed per loan with pandas from the book CSV (`current_balance`, `days_past_due`, `origination_score`, `origination_scorecard`, `current_score_v4`, `first_repayment_date`, `term_months`, `contract_rate`, `drawdown_date`). The other inputs were the register's `arrangement_start`, `arrangement_end` and `cancelled_date`, the PLPD-2026.06 curve, the `Q1 FY27 scenarios` sheet, the migration formula and CRM-ECL-04.

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Collective allowance (main call; workbook ask 1) | AUD 13,773,000 | 13,772,790.12 | yes |
| Stage 1 allowance (component 3) | 10,933,000 | 10,932,850.94 | yes |
| Stage 2 allowance (component 3) | 2,840,000 | 2,839,939.19 | yes |
| Loans in stage 2 (component 1) | 3,265 | 3,265 (458 at 30+ dpd, 612 hardship in force, 2,635 score fall, overlapping) | yes |
| Weighted PD multiplier (component 2) | 1.06 | 0.55x1.0 + 0.30x1.3 + 0.15x0.8 = 1.0600 | yes |
| S1 PL36 loans / GCA / allowance / coverage | 17,109 / 138,349,000 / 3,202,000 / 2.31% | 17,109 / 138,349,212.40 / 3,201,918.70 / 2.3144% | yes |
| S1 PL60 loans / GCA / allowance / coverage | 20,180 / 330,436,000 / 7,731,000 / 2.34% | 20,180 / 330,435,952.35 / 7,730,932.23 / 2.3396% | yes |
| S2 PL36 loans / GCA / allowance / coverage | 1,421 / 11,728,000 / 681,000 / 5.81% | 1,421 / 11,727,965.30 / 681,060.01 / 5.8071% | yes |
| S2 PL60 loans / GCA / allowance / coverage | 1,844 / 28,735,000 / 2,159,000 / 7.51% | 1,844 / 28,735,138.23 / 2,158,879.18 / 7.5130% | yes |
| 2023 and earlier, PL36 / PL60 | 5,000 / 641,000 | 5,301.31 / 641,408.18 | yes |
| 2024, PL36 / PL60 | 159,000 / 1,073,000 | 158,698.08 / 1,073,124.78 | yes |
| 2025, PL36 / PL60 | 940,000 / 2,412,000 | 939,827.81 / 2,412,266.65 | yes |
| 2026, PL36 / PL60 | 2,779,000 / 5,763,000 | 2,779,151.51 / 5,763,011.80 | yes |
| Stage 3 loans (workbook ask 4) | 343 | 343 (PL36 157, PL60 186; max dpd on the book 176) | yes |
| pptx ask 1, slide 1 | AUD 13,773,000 with the four lines | values match; the golden slide carries them | yes (wording, finding 1) |
| pptx ask 2, slide 2 | eight drawdown-year values, largest 2026 PL60 5,763,000 | values match; the golden chart series equal them | yes (wording, finding 1) |

Margins are thin but clean. Once the method is fixed, no step leaves any estimation freedom:

- The allowance sits $290 inside its bin.
- The thinnest cell is 2023-and-earlier PL60, $92 from 641,500.
- S1 PL36 coverage is 0.0006 points from its edge.

Coverage at two decimals comes out the same from unrounded and from rounded figures. Both goldens carry exactly these figures.

## Competing answers that survived
None.

Tested and closed, for reference:

| Fork | Answer it produces | Shipped rule that closes it |
|---|---|---|
| Curve read from origination for every loan | 19,772,000 | 3.2 indexes k from the reporting date; the curve header indexes by repayments fallen due |
| Curve increment at months on book, no survival division | 13,318,000 | Curve header: "a new loan". A performing loan has survived m months (the analytical step) |
| Monthly hazard without survival weighting | 14,076,000 | Probability error |
| Conditioning on all-cause survival (curve read as a competing-risk incidence) | not computable from the curve | 3.2 makes the curve the source. The development sample shows the curve is net of prepayment. 7.4 does not model payouts |
| Prior-quarter scenarios (multiplier 1.04) | 13,513,000 | Prompt "this quarter's approved scenarios"; the sheet carries the 30 September 2026 reporting date and was approved 18 Sep |
| Hardship in force by the "Active" status label | 13,773,000 (+$172.53), but loan BPL2555407 (PL36) moves to stage 2 and four PL36 cells move | 2.2's dates rule; the dictionary's Tuesday status batch |
| Hardship ignoring cancellation | 13,806,000 | 2.2 "not cancelled" |
| No hardship condition (pre-4.1) | 13,515,000 | Version 4.1, effective for reporting dates from 30 June 2026 |
| Unrounded v3 conversion / no conversion | 13,769,000 / 13,651,000 | Migration note "rounded to the nearest whole point"; 2.3 |
| Scorecard inferred from drawdown date | 13,771,000 | The `origination_scorecard` field and the application-date rule. The 167 July 2024 v3 loans match the v3 grade bands (98.8%) |
| Strict ">60" points | 13,730,000 | 2.1 "60 or more" |
| Months on book as calendar months since drawdown | 13,753,000 | Curve header definition |
| Past-maturity loans at zero ECL | 13,773,000 ($221.65 at stake) | 3.2, one month remaining |
| Stage 3 plus the 101 September write-offs | 444 | 1.4 (written off and closed); no loan on the book is at 180+ dpd |
| Fiscal-year drawdown split | Jul to Sep 2026 has no line | Only calendar years cover the book |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 10 | PASS |
| Distinct formats | 3 or more | 6: csv, txt, docx, xlsx, pdf, parquet | PASS |
| Largest file | 25,000+ rows or a large database | `personal_loan_book_2026-09-30.csv` 40,897 rows (development sample 42,032) | PASS |
| Distractors declared, unlabelled | 2+ in `metadata.json`, no name or file labels one | 3 declared (development sample, write-offs, roll rates); no label in any file name or content | PASS |
| Distractors relevant and unused | same world, weighed, unused by the solution | all three are credit-loss evidence on the same book (PD development, loss history, arrears migration); none feeds the solution | PASS |
| A distractor that answers a graded quantity is ruled out | reproduces, and a shipped fact rules it out | write-offs give a loss-rate basis (trailing 12 months net AUD 15,253,052.85), ruled out by 3.1 and s.4; roll rates give bucket PDs, ruled out by 3.2; the sample gives a re-estimated curve, ruled out by 3.2 and 7.1 | PASS |
| Deliverable count | 1 to 3 | 2 (`ecl_allowance_2026Q3.xlsx`, `arc_ecl_q3_2026.pptx`) | PASS |
| Multi-dimensional asks | not stacked lookups | stage x product x four measures (16 cells), drawdown year x product (8 cells), the allowance; the stage 3 count is the one single lookup | PASS |
| Golden deliverables present | every named file | both in `golden/`, figures equal to the recomputation | PASS |
| Units and rounding stated | in every ask | AUD to the nearest thousand, coverage in per cent to two decimals, counts | PASS |
| Prompt shape, 25-criteria floor | shape identifiable, 25+ | about 32 criteria (26 workbook figures, the call, 3 components, 2 slides); the design note files Shape 02, but the prompt reads as a grid of cuts, closer to 07 (finding 3) | PASS |
| Realism | no LLM tells; goldens read as work products | Office containers, document control, AEST and UTC stamps, July 2024 v3 tail, status lag; goldens are plain committee outputs (static workbook values, action titles); a few tutorial "because" clauses in the policy and dictionary (finding 5); no em dashes anywhere | PASS |

## Gate G reconciliation
| | mechanism | stumping_family | surface_read_dependency | sole_data_defect |
|---|---|---|---|---|
| Judge | method_or_model_selection | analytical_non_defect | no | no |
| Design note | forecasting (conditional PD as the decisive construction) | analytical_non_defect | no | no |

The flags agree on all three. The mechanism labels differ, but both are shapes that pass Gate G, and both name the same decisive step: rebasing the origination curve and conditioning on survival. The mismatch comes from where the forward PDs come from. From outside, they are pinned by a filed curve rather than projected from history, and the history files are the declared distractors. So a reviewer applying Gate G's definitions strictly reads the difficulty as choosing the right derivation. The disposition does not change.

Two practical consequences:

1. The card records `forecasting`, and its guard WARN against task132 was answered on that label.
2. The Forecasting & Predictive Modeling tag is still earned, because the committed figure is a forward 12-month and lifetime expected loss. Defend it as a PD term structure applied to each loan's remaining life, not as a trend projection.

**Distractors (`metadata.json`).** The judge did not name any declared distractor as the surface read carrying the task. It did use the development sample, as a reviewer would, to close the all-cause-survival reading. That is support for determinism, not a load-bearing use, since 3.2 already makes the curve the PD source. The design note's survival property 2, "rebuilding the curve from it returns the filed curve", overstates this. The filed curve sits within 0.0075 of the sample's prepayment-censored Kaplan-Meier (below it from month 6) and up to 0.026 above the competing-risk incidence.

**Other drift seen while reconciling:**

- Closure-table axis 5 says "Q3 FY27"; the sheet is "Q1 FY27 scenarios".
- The Tried-and-rejected line "Stale arrangement_status labels ... not built" is superseded by repair B4. The judge found the two stale Active labels B4 describes.
- The judge's numbers otherwise match the design note's ladder and closure claims: rung 0 is +43.6%, rung 3 is -3.3%, the hardship and conversion devices move 470 and 786 loans, the status-label slip moves one PL36 loan within the bin, and the nearest bin edge is 6.3%.

## Stump power (Gate F)
Plausible. The judge's two easy routes are 13,318,000 (no survival division) and 19,772,000 (curve read from origination). Each fails the main call and every allowance-bearing cell (four stage and product allowances, four coverages, eight drawdown-year cells), while loan counts and gross carrying amounts survive. Exactness also punishes staging slips: a strict ">60" gives 13,730,000, ignoring cancellation 13,806,000, and dropping the hardship condition 13,515,000.

Too-easy signals: the policy and the dictionary document every Layer 1 quirk, so those are pre-disarmed. That leaves the stump resting on one conceptual step, and its pin ("a new loan") is in plain sight. If live runs show the task too easy, the lever is to put more of the asks on the rebasing (for example a 12-month versus lifetime split by stage), never a planted device. Solver rounds were not read, per the contract.

## Findings, ranked
1. **FIX_NOW, `submission.md`, Deliverable Answers, `arc_ecl_q3_2026.pptx` asks 1 and 2.** The committed answers grade "in its title", "a column chart" and "the largest bar ... named in the title". The prompt asks none of this: it says "the first states the allowance with the stage and product table, the second charts the allowance by drawdown year for each product". Restate them as:
   - Ask 1: slide 1 states the collective allowance of AUD 13,773,000 with the stage and product table (the four lines of workbook ask 2).
   - Ask 2: slide 2 charts the allowance by drawdown year (2023 and earlier, 2024, 2025, 2026) for PL36 and PL60, with the eight values of workbook ask 3.

   The golden deck keeps its column chart and action titles; they just stop being graded.
2. **Optional, same edit, `submission.md` Step-by-Step Solution step 5.** It says "over 12 months for stage 1". CRM-ECL-04 3.1 reads "the next 12 months or the remaining term if shorter", which is what the figures already use.
3. **`DESIGN_NOTE.md` accuracy, no pack change.** Correct four things:
   - survival property 2's claim about rebuilding the curve;
   - axis 5's "Q3 FY27";
   - the superseded stale-label line (add a new line to the append-only section rather than editing it);
   - the shape label, which says 02 while the prompt reads as a grid of cuts.
4. **Card.** If the Gate G mechanism or the shape is re-recorded to match the outside reading, re-run `guard.py` on the new values.
5. **Mild hygiene, leave it.** CRM-ECL-04 2.4 and 3.2 and the dictionary's hardship note carry rationale clauses that read slightly tutorial. This is not a fail. Editing a shipped document would change what solvers saw and would need a fresh solver round.
6. **Scope.** The cross-batch reference check was not run inside the judge, which is confined to the scratch path. The fingerprint guard and the stage 5 `/clone-check` own that question.

## Next action for the author
Invoke `submission-writeup` and restate the two `arc_ecl_q3_2026.pptx` answers in `submission.md` as the content the prompt pins (finding 1), folding in the step 5 wording. Then run determinism-check pass 2. No figure, file or rung moves, so no fresh solver round is needed first.
