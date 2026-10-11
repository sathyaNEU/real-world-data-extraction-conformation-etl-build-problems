# determinism-check report, task445, 2026-10-11

**How this pass ran.** The orchestrator had no `Agent` tool in this session, so no judge thread could be spawned. The judge pass was therefore run in the orchestrator's own thread, under the judge's isolation rules: a fresh unzip at `/tmp/determinism-check-task445-1791736070/target/`, the full v3 + Gate H system prompt applied as written, every load-bearing figure recomputed with pandas, and the verdict written to `/tmp/determinism-check-task445-1791736070/verdict.md` before `DESIGN_NOTE.md`, `metadata.json`, the card or the golden files were opened. One exposure to disclose: `pipeline.json` was read during input checks, before the verdict was written. It carries the stump sentence (also in `submission.md`) and the round-1 brief line "bridge ties except the start bar basis", which may have pointed the pass toward Finding 1. The solver round log was not read. If an isolated thread is required, re-invoke from a session that has `Agent`.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (solution-block wording only, no file or prompt change, no rerun)
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main call is forced by four shipped facts: OM-4 s.2 (ownership counts every manager that files for the period), the SEC readme's 45-day window, the daily build's 3 Feb cut (`data_sources.md`), and the prompt's never-reissue clause. 125 managers have a September report and no December report (91 of them hold watchlist names). Carrying each at its September position gives WHII 88.6, GLI 84.4, OTF 83.4, JEMS 84.8 and SAF 91.4 above 80.0, with FENN (77.3) and AMRB (76.2) the nearest below. The in-pack back-test on the September window at day 34, completed from June (every June filer filed for September), selects holder-level carry: MAE 0.66 and max 2.59 points, against 0.92 and 2.61 for carry scaled by the filers' same-holder change, about 1.0 and 3.1 for a per-name completion share, and 16 to 23 points for any single aggregate share. All three holder-level methods give the same five flags, so the call does not depend on which estimator is used. Every graded figure in both deliverables reproduced.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Sep filers with no Dec report by 3 Feb (SUBMISSION x COVERPAGE, HR + combination) | 125 | 125 (91 hold watchlist names) | yes |
| Dec shares outstanding, 12 names (fsds num.txt, latest ddate on or before 31 Dec, Oct/Nov-dated) | 41,820,557 ... 31,052,683 | identical, all 12 | yes |
| Sep shares outstanding, 12 names (latest on or before 30 Sep, Jul/Aug-dated) | 42,344,280 ... 31,369,971 | identical, all 12 | yes |
| Dec ownership: WHII, GLI, OTF, AMRB, TAAV, JEMS | 88.6, 84.4, 83.4, 76.2, 74.3, 84.8 | 88.56, 84.37, 83.38, 76.23, 74.31, 84.83 | yes |
| Dec ownership: FENN, ABBB, OLPD, SAF, HAMR, NOPR | 77.3, 62.3, 71.1, 91.4, 55.2, 67.2 | 77.30, 62.31, 71.14, 91.42, 55.20, 67.20 | yes |
| Dec flags | Y: WHII, GLI, OTF, JEMS, SAF | same | yes |
| Sep ownership, 12 names (RESTATEMENT 0001567619-22-000946 replaces; NEW HOLDINGS 0001060173-23-000274 adds) | 86.3, 83.2, 78.7, 74.8, 76.9, 82.7, 81.6, 61.1, 70.1, 89.9, 53.8, 66.2 | identical | yes |
| Largest holder + value, 12 names (Wexley 0001085146-23-000343 x1000) | Prescott 275,146,453 / Wexley 288,595,000 / ... / Prescott 149,577,226 | identical to the dollar, all 12; no carried holder can overtake (largest carried estimate $148.5M vs $270.3M, SAF) | yes |
| Bridge start (every Sep-period line, CUSIP as written, all three drops) | 568,922,286 | 568,922,286 | yes |
| Put and call lines | -5,183,600 | -5,183,600 | yes |
| Lines in superseded reports | -16,011,685 | -16,011,685 | yes |
| Lines under malformed CUSIP (zero-stripped OLPD/OTF/AMRB, 359y60106, check-digit 805185108) | +9,304,719 | +9,304,719 (the three sets are disjoint, so bar order cannot change a value) | yes |
| Sep institutional shares, 12 names | 557,031,720 | 557,031,720 | yes |
| Back-test, holder carry max error | 2.6 | 2.59 | yes |
| Back-test, "one aggregate completion share" max error | 22.3 | in-thread: not reproduced under eight count/share definitions (15.7 to 26.7). After the verdict, using the design note's definition (prior window's day-34 share of final 13F value, June 0.8147): 22.3 | yes once the definition is supplied, which the submission does not do |
| Aggregate rival flags (Final Recommendation sentence) | flags AMRB, TAAV, FENN; misses GLI, OTF | September-window value factor 0.820 applied to Dec on-file: WHII, AMRB, TAAV, JEMS, FENN, SAF | yes once the definition is supplied |

## Competing answers that survived
None on the main call. The rivals checked were:
- **Reports in hand:** WHII and JEMS (JEMS at 80.1). Ruled out by the OM-4 s.2 population, the 14 Feb deadline and s.8 (no reissue).
- **September flags:** ruled out because the December lines on file show the shareholder registers moved.
- **Aggregate gross-ups:** ruled out by the back-test.
- **Per-name completion and scaled carry:** produce the same five flags.

One supplementary fork was weighed and judged not to survive (Finding 1). The bridge start bar is "every September-quarter information-table line" (568,922,286, January build included). A weaker reading takes "tie to the SEC's own files" literally: it starts from the SEC data sets only (544,752,819) and adds a January-build bar of +24,169,467.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count | 10+ | 19 | yes |
| Distinct formats | 3+ | 7 (tsv, txt, csv, xlsx, pdf, htm, md) | yes |
| Large file | 25,000+ rows | form13f_2022q4/INFOTABLE.tsv, 39,301 rows | yes |
| Distractors declared, none labelled in a name | 2+ in metadata.json | short_interest_20221230.csv, 13flist2022q4.txt; neither name says so | yes |
| Distractors relevant but unused | same world, has to be weighed | short interest on the same twelve names (a crowding signal); the 13(f) list, a CUSIP reference beside the CUSIP repair | yes |
| Distractor answering a graded quantity | must be ruled out by a shipped fact | neither answers the flag or any ask | n/a |
| Deliverable count | 1 to 3 | 2 (CSV, PNG) | yes |
| Asks multi-dimensional | not stacked lookups | 12-row flag file across two periods plus a bridge | yes |
| Goldens present | every named deliverable | golden/crowded_flags_2022q4.csv, golden/sep_quarter_bridge.png | yes |
| Units and rounding stated | inside the ask | percent to one decimal, whole dollars, whole shares; share counts whole per the v3 layout | yes |
| Prompt shape and 25-criteria floor | shape identified, 25+ | shape 03 (bridge) inside a twelve-row file, about 90 criteria | yes |
| Prompt length | under 1,000 characters | 987 | yes (tight) |
| Realism | no LLM tells; goldens read as work product | PNG is a clean desk chart with an action title and a source line; the CSV follows the v3 layout. One mildly didactic line in data_sources.md, already deferred by the leak reader. | yes |

## Gate G reconciliation
- **Judge:** mechanism `forecasting` (nowcasting a right-censored filing population), with method selection by back-test as the supporting move; `analytical_non_defect`; surface_read_dependency no; sole_data_defect no.
- **Design note and card:** `gate_g: method_or_model_selection`, with forecasting support; family analytical_non_defect; surface read no; sole defect no.
- **Comparison:** the primary label differs, but both labels are FINE-numbers shapes on the same step (choosing how to complete the open window, validated out of sample). No file in the pack misstates anything. The on-file figures are correct but incomplete. Neither declared distractor carries a surface read. No mismatch that predicts a send-back.
- **Gate H:** judge says `domain: pass, layers: pass, decisive_step: analytical`. The card says `stump_class: analytical`, and its analyst_test and domain_test match the judge's easy route (on-file ownership flags WHII and JEMS).
- **One caveat for the portal:** reporting-lag completion is a domain-general move (IBNR, late registrations), so a strict swap-test reader could probe H1. The 13F-specific apparatus (45-day window, manager-level carry, cover-page denominator, amendment types) is what answers it, and the design note's swap-test line already says so.

## Stump power (Gate F)
Strong. A solver that conforms every Layer 1 device correctly still files the reports-in-hand set (WHII, JEMS). JEMS at 80.1 on file looks like a confirmed flag, and no document mentions completing late filers. A solver that does think of completion and reaches for an aggregate gross-up files WHII, AMRB, TAAV, JEMS, FENN, SAF. No too-easy signal sits on the decisive step. One residual on the asks: the December one-decimal figures sit on the estimator. OTF is 83.4 under carry, 85.0 scaled and 85.2 per-name, so a solver on a non-carry holder-level method loses those criteria while keeping the flags. That is the intended estimator-selection penalty, but grading tolerance matters.

## Findings, ranked
1. **Bridge start-bar wording, supplementary ask 2 (Gate E risk, optional, rerun cost).** In `prompt.md`, "how our September numbers tie to the SEC's own files" sits beside the defining clause "every September-quarter information-table line". `data_sources.md` says the January build is "parsed by our loader", which licenses a weaker start that leaves out the four September-period filings in the January build (544,752,819, plus a +24,169,467 bar). The golden's reading is the stronger one, so this is not FIX_NOW. If the portal grader splits on the start bar, the fix is a prompt pin: "every information-table line in a report for the quarter ended 30 September, our January build included". That change needs a fresh solver round.
2. **FIX_NOW: define the aggregate rival in `submission.md`.** Final Recommendation ("Not one aggregate completion share, which flags AMRB, TAAV and FENN and misses GLI and OTF") and Step 5 ("one aggregate completion share by up to 22.3") never say which aggregate is meant. Under natural readings (manager count, holder count, watchlist shares, all-security shares) the 22.3 and the flag list do not reproduce. Both reproduce exactly with the design note's definition, which a reviewer cannot see. Name it in both places: "the share of the prior quarter's final 13F value on file by the same day (0.820 from the September window; 0.815 from June in the back-test)". Optionally note that the aggregate also flags SAF, at 80.3.
3. **Estimator spread on the December one-decimal figures (watch, no change).** Carry is selected by the back-test (MAE 0.66 vs 0.92 vs 1.0), but the margin between estimators is one quarter on twelve names. If the portal QC calls the one-decimal ownership figures contested, whole-percent rounding is already logged in Tried and rejected. Do not reopen it unless the QC asks.

## Next action for the author
Run `submission-writeup` and apply Finding 2 to the Final Recommendation and Step 5 of `task445/submission.md`. Then re-invoke the determinism check for pass 2 (`determinism_check_report_pass2.md`), from a session where the `Agent` tool is available so the judge thread is isolated.
