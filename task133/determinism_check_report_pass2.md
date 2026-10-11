# determinism-check report, task133, 2026-10-11, pass 2

Judge pass 2, run at `/build` stage 7 after the pass 1 FIX_NOW. The standard is `/home/user/wt133/guidelines/determinism_judge_system_prompt.md` (v3 Gate G, with the 2026-10-10 Gate H), applied as written. The scratch copy at `/tmp/determinism-check-task133-pass2-20261011T073715Z-a7999a43/target/` is byte-identical to `target/` (combined sha256 `f1b41422...b27e`, rechecked at 07:53 UTC). The verdict is `/tmp/determinism-check-task133-pass2-20261011T073715Z-a7999a43/verdict.md` (sha256 `d2c5fa09...b45e`). It was written before any author-intent file was opened.

**What was judged.** `prompt.md` and `submission.md` changed on disk at 07:37:56 UTC (commit `cce5b57`, "forum redrawn to the board ... rebuild pending after judge pass 2"). That was 41 seconds after the scratch copy was cut and the blocks first extracted. The pass re-read both files and judged the edited versions (prompt sha256 `008ee243...f540`, submission `d9f47125...e4c3`). In them the audience is the board and the deck is `board_ecl_q3_2026.pptx`; no figure changed. `target/` and `golden/` were not rebuilt. The bundle judged is therefore the pre-redraw one, in which CRM-ECL-04 section 5 still reports the allowance to the Audit and Risk Committee.

**Run note, a deviation from the agent contract (as in pass 1).** This runtime has no `Agent` tool, so the judge pass ran in the orchestrator thread, with isolation kept by ordering.

- **Read before `verdict.md` was written:** `prompt.md`, `submission.md` (for the blocks), the judge system prompt, the scratch copy, and the author's per-author file (branch rules only).
- **Opened only afterwards:** `DESIGN_NOTE.md`, `metadata.json`, `golden/`, the pass 1 report, and the git log. From the log, only the diff of `cce5b57` to the design note, prompt and submission was read. Its generator diff was not.
- **Never opened:** `generator/`, `START_HERE.md`, `pipeline.json`, `leak_check_report.md` and `solver_rounds/`.

One git log subject line summarises a solver round. It was seen after the verdict and is not used here. No server-side tools, web access or subagents were used.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE (the judge's call: no repair, no rerun). The build is not ship-ready as the folder stands, because the golden-deliverables spec gate fails until the rebuild deferred by `cce5b57` lands (finding 1).
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Three rules (Gate H):** domain: pass, layers: pass, decisive_step: analytical

## Why
CRM-ECL-04 pins every step but one:

- staging (2.1 to 2.3);
- the remaining term and the past-maturity rule (3.2);
- LGD (3.3), the re-amortised EAD (3.4) and the contract-rate discount (3.5);
- the scenario weighting (section 4).

The Q1 FY27 sheet, the migration note and the curve header pin the inputs. The open step is turning a curve indexed from origination into "the probability of default in the k-th month after the reporting date" for a loan that has not defaulted. That step has one expert answer: [C(m+k) - C(m+k-1)] / (1 - C(m)). Under it, the independent rebuild gives AUD 13,772,790.12 and reproduces the call and every supplementary line, both slides included.

The pass 1 FIX_NOW is closed. The deck answers now commit only to the content the prompt pins, and step 5 states the 12-month-or-remaining-term horizon.

## Recomputation ledger
Every value was recomputed per loan with pandas from the book CSV (`days_past_due`, `origination_score`, `origination_scorecard`, `current_score_v4`, `first_repayment_date`, `term_months`, `contract_rate`, `current_balance`, `drawdown_date`). The other inputs were:

- the hardship register (`arrangement_start`, `arrangement_end`, `cancelled_date`, `arrangement_status`);
- the migration formula, v4 = 1.12 x v3 - 18, rounded;
- the PLPD-2026.06 curve and the `Q1 FY27 scenarios` sheet;
- CRM-ECL-04 sections 1 to 4.

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Collective allowance (main call; workbook ask 1) | AUD 13,773,000 | 13,772,790.12 | yes |
| Stage 1 allowance (component 3) | 10,933,000 | 10,932,850.94 | yes |
| Stage 2 allowance (component 3) | 2,840,000 | 2,839,939.19 | yes |
| Loans in stage 2 (component 1) | 3,265 | 3,265 (458 at 30+ dpd, 612 with hardship in force by dates, 2,635 with a 60-point fall; overlapping) | yes |
| Weighted PD multiplier (component 2) | 1.06 | 0.55x1.00 + 0.30x1.30 + 0.15x0.80 = 1.06; weighting three scenario ECLs gives the same total to the cent | yes |
| Stage 3 loans (workbook ask 4; step 1) | 343 | 343 (dpd 90+; maximum dpd on the book is 176) | yes |
| S1 PL36: loans / GCA / allowance / coverage | 17,109 / 138,349,000 / 3,202,000 / 2.31% | 17,109 / 138,349,212.40 / 3,201,918.70 / 2.3144% | yes |
| S1 PL60: loans / GCA / allowance / coverage | 20,180 / 330,436,000 / 7,731,000 / 2.34% | 20,180 / 330,435,952.35 / 7,730,932.23 / 2.3396% | yes |
| S2 PL36: loans / GCA / allowance / coverage | 1,421 / 11,728,000 / 681,000 / 5.81% | 1,421 / 11,727,965.30 / 681,060.01 / 5.8071% | yes |
| S2 PL60: loans / GCA / allowance / coverage | 1,844 / 28,735,000 / 2,159,000 / 7.51% | 1,844 / 28,735,138.23 / 2,158,879.18 / 7.5130% | yes |
| 2023 and earlier, PL36 / PL60 | 5,000 / 641,000 | 5,301.31 / 641,408.18 | yes |
| 2024, PL36 / PL60 | 159,000 / 1,073,000 | 158,698.08 / 1,073,124.78 | yes |
| 2025, PL36 / PL60 | 940,000 / 2,412,000 | 939,827.81 / 2,412,266.65 | yes |
| 2026, PL36 / PL60 | 2,779,000 / 5,763,000 | 2,779,151.51 / 5,763,011.80 | yes |
| `board_ecl_q3_2026.pptx` ask 1 (slide 1) | AUD 13,773,000 with the four stage and product lines | same values as above | yes |
| `board_ecl_q3_2026.pptx` ask 2 (slide 2) | the eight drawdown-year values | same values as above | yes |

The margins are thin but clean. Once the method is fixed, no step leaves estimation freedom:

- The total sits AUD 290 inside its bin.
- 2023-and-earlier PL60 sits AUD 92 under 641,500.
- S1 PL36 coverage sits 0.0006 points under 2.315.

Coverage comes out the same at two decimals from rounded and from unrounded figures. The business-day rule moves no loan's count at 30 September 2026, which is a Wednesday. No first repayment falls after day 28, so there is no month-end schedule ambiguity.

## Competing answers that survived
None. Tested and closed:

| Fork | Answer it produces | Shipped fact that closes it |
|---|---|---|
| Curve read from origination for every loan | 19,772,000 | 3.2 defines PD(k) from the reporting date; seasoned loans have already come through those months |
| Curve shifted to months on book, no survival division | 13,318,000 | A performing loan has survived m months; the curve header says "a new loan" (the analytical step) |
| Monthly hazard used as PD(k), no survival product | 14,076,000 | The ECL sum needs the marginal probability from the reporting date |
| Multiplier applied to the cumulative curve before conditioning | 13,817,000 | Section 4: each scenario "scales PD(k)" |
| Prior-quarter scenarios (1.04); base only (1.00) | 13,513,000; 12,993,000 | Prompt: "this quarter's approved scenarios"; the sheet is dated 30 September 2026 and was approved 18 September |
| Hardship in force by the Active label (614) rather than by dates (612) | 13,773,000, but stage 2 count 3,266 (BPL2555407, PL36) | 2.2 is date-based; the dictionary's Tuesday-night status batch explains the lag |
| Hardship including cancelled arrangements | 13,806,000 | 2.2: "not cancelled" |
| v3 conversion unrounded; no conversion | 13,769,000 (stage 2 3,246); 13,651,000 | Migration note: "rounded to the nearest whole point" (19 loans); 2.3 |
| Scorecard inferred from the drawdown date | 13,771,000 (stage 2 3,260) | The `origination_scorecard` field; 167 v3 loans were funded after 1 July 2024 |
| Months on book as calendar months since drawdown | 13,753,000 | Curve header and 3.2: repayments fallen due, pause dates included |
| Past-maturity loans at nil ECL | 13,773,000 (28 loans, AUD 221.65) | 3.2: final month, one month remaining; no reported line moves |
| Stage 1 on a lifetime horizon; no 2.4 scalar; PL60 LGD 74%; no hardship trigger | 18,588,000; 12,116,000; 13,513,000; 13,515,000 | 3.1; 3.2; 3.3; 2.1 and version 4.1 |
| Fiscal-year drawdown split | July to September 2026 loans get no line | Only calendar years cover the book with the prompt's lines |

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10 or more | 10 | PASS |
| Distinct formats | 3 or more | 6: csv, txt, docx, xlsx, pdf, parquet | PASS |
| Largest file | 25,000+ rows or a large database | `personal_loan_book_2026-09-30.csv`, 40,897 rows (development sample 42,032) | PASS |
| Distractors declared, unlabelled | 2+ in `metadata.json`; no file name or content labels one | 3 declared (development sample, write-offs, roll rates); no label in any file name or in any extracted text, XML part or parquet metadata | PASS |
| Distractors relevant and unused | same world, weighed, unused by the solution | all three are credit-loss evidence on the same book; none feeds the solution | PASS |
| Distractor that answers a graded quantity is ruled out | it reproduces, and a shipped fact rules it out | none states an allowance. The write-offs give a loss-rate basis (trailing 12 months net AUD 15,253,053), ruled out by section 3. The roll rates give bucket PDs, ruled out by 3.2. The sample re-fits near the curve (within 0.0075), ruled out by 3.2 and 7.1 | PASS |
| Deliverable count | 1 to 3 | 2 (`ecl_allowance_2026Q3.xlsx`, `board_ecl_q3_2026.pptx`) | PASS |
| Format family | none required | xlsx and pptx | n/a |
| Multi-dimensional asks | not stacked lookups | a 16-cell stage x product x measure grid, an 8-cell drawdown-year split, the allowance, and the stage 3 count | PASS |
| Golden deliverables present | every file the prompt names | `ecl_allowance_2026Q3.xlsx` is present and matches. **`board_ecl_q3_2026.pptx` is absent**: `golden/` holds `arc_ecl_q3_2026.pptx` (figures match; its footer reads "Audit and Risk Committee, 23 October 2026"), and `metadata.json` still lists `arc_ecl_q3_2026.pptx` | **FAIL** (pending rebuild, finding 1) |
| Units and rounding stated | in every ask | AUD to the nearest thousand, coverage in per cent to two decimals, counts | PASS |
| Prompt shape, 25-criteria floor | shape identifiable, 25+ criteria | about 32 (the call, 16 grid cells, 8 drawdown-year cells, the stage 3 count, 3 components, 2 slides). The design note files Shape 02 as forward cuts; from outside it reads as a grid | PASS |
| Realism | no LLM tells; goldens read as work products | Pack: Office containers, AEST job times stamped in UTC, about 1.2% grade overrides, blank pre-July-2020 reasons, case-number gaps, a lagging status batch. Goldens: a plain four-sheet workpaper and a two-slide deck with action titles. No em dashes in the prompt, submission, metadata or pack | PASS (the deck footer is stale against the new prompt, finding 1) |

## Gate G reconciliation
| | mechanism | stumping_family | surface_read_dependency | sole_data_defect |
|---|---|---|---|---|
| Judge, pass 2 | forecasting | analytical_non_defect | no | no |
| Design note | forecasting (the conditional PD as the decisive construction) | analytical_non_defect | no | no |
| Judge, pass 1 (for reference) | method_or_model_selection | analytical_non_defect | no | no |

The judge and the design note agree on all four fields. The pass 1 mechanism label differed but was also a passing shape, so this build sits on the forecasting / method-selection boundary when read from outside. Both readings name the same decisive step, and neither puts Gate G at risk. The card's `forecasting` label now matches the outside reading.

Gate H agrees as well. The design note's analyst test (about AUD 13.32 million, curve shifted without survival division) is the judge's easy route (13,318,000). Its domain swap test and its two layers match the judge's.

**Distractors.** The judge named none of the three declared distractors as a surface read carrying the task. It treated them, and the prior-quarter sheet, as alternative-method inputs that CRM-ECL-04 sets aside. No distractor is too load-bearing.

## Stump power (Gate F)
Plausible. A strong model that reads every rule correctly can still take any of three wrong routes:

- shift the curve without conditioning on survival: 13,318,000, 3.3 per cent low;
- use monthly hazards: 14,076,000;
- read the curve from origination: 19,772,000.

Each route fails the call, the four stage and product allowances, the four coverage ratios and the eight drawdown-year cells at once. Loan counts and gross carrying amounts survive.

The lower steps cost precision at the thousand but do not carry the call:

- the 19 rounding loans;
- the 167 late-funded v3 loans;
- the two lagging hardship statuses;
- counting repayments fallen due rather than calendar months.

One too-easy signal is present but contained. The dictionary and 2.2 pre-disarm the hardship status lag, and that is a lower step only. Solver rounds were not read, per the contract.

## Findings, ranked
1. **Ship hold, spec gate, `golden/` and `metadata.json`.** The prompt names `board_ecl_q3_2026.pptx`, but the golden still ships as `arc_ecl_q3_2026.pptx`. Its slide footers read "Audit and Risk Committee, 23 October 2026", `metadata.json` still lists `arc_ecl_q3_2026.pptx`, and `target/` CRM-ECL-04 section 5 still reports to the Audit and Risk Committee. Commit `cce5b57` changed `generator/docs.py`, `golden.py` and `build.py` but deferred the rebuild until after this pass. The fix is the rebuild. Nothing in the prompt or the submission needs to change.
2. **Scope of this verdict.** Pass 2 judged the post-redraw prompt and submission against the pre-redraw bundle. The verdict carries over to the rebuilt pack only under three conditions:
   - the rebuilt `target/` differs from the judged copy only in CRM-ECL-04 section 5's reporting line (and the docx's own metadata);
   - the rebuilt deck differs only in its name and footer;
   - every graded figure is unchanged.

   If any data file or figure moves, this verdict does not cover the pack.
3. **Process: the package moved mid-pass.** The brief said the fix was in `submission.md` only. The prompt and the submission were then edited and committed while the judge was running. This pass caught the edit, pinned the new versions and judged those. A judge pass should still run on a frozen package: hold `prompt.md`, `submission.md`, `target/` and `golden/` until it returns.
4. **Solver-round question, the author's call.** After solver round 2, the redraw moves the prompt's forum, and the rebuild will move one sentence of a shipped document. No figure, rung or decisive clause moves. On the judge's own scale this is a note-level edit that keeps the analytic surface equivalent. The pipeline rule asks for a fresh solver round when a fix moves "a figure, a rung or a document"; whether a reporting-line sentence counts is yours to decide.
5. **Optional polish, `submission.md` step 5, no rerun.** Step 5 cites CRM-ECL-04 "3.3 to 3.5", but the horizon it applies is set by 3.1. Cite "3.1, 3.3 to 3.5".
6. **Scope.** The cross-batch reference check was not run inside the judge, which is confined to the scratch path. The fingerprint guard and the stage 5 `/clone-check` own it.

## Next action for the author
Run the rebuild that `cce5b57` left pending. Then diff the rebuilt `target/` and `golden/` against the judged copy at `/tmp/determinism-check-task133-pass2-20261011T073715Z-a7999a43/target/` and ship only if four things hold:

- the only differences are CRM-ECL-04 section 5's reporting line and the deck's name and footer;
- `golden/board_ecl_q3_2026.pptx` exists with the same figures;
- `metadata.json` lists `board_ecl_q3_2026.pptx`;
- every figure is unchanged.
