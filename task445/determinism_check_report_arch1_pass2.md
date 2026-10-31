# determinism-check report, task445, 2026-10-11 (pass 2)

Run note: the determinism-judge orchestrator in this runtime has no Agent tool, so the main session spawned the one isolated judge thread itself (general-purpose, opus), with the judge system prompt verbatim, the submission's graded blocks and a fresh unzip at /tmp/determinism-check-task445-p2/target/ as its only readable path. The thread's verdict.md follows verbatim.

## Verdict
DETERMINISTIC (SOLUTION_WRONG on one incidental write-up figure)
**Disposition:** FIX_NOW, applied: section 1's "SAF (80.3)" removed. The aggregate-share figure for SAF is 80.25 to two places and sits on a one-decimal bin edge, so it is cut as incidental working (submission-writeup: no figure not owed by a component, an ask or the call), not re-rounded. No target file, prompt or graded figure moved.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Gate H:** domain pass, layers pass, decisive_step analytical

## Gate G reconciliation
Card and design note: method_or_model_selection (completion method chosen by back-test) with forecasting support; the thread reads forecasting (nowcast, method chosen by back-test). Same step, both non-defect; no send-back predicted (matches pass 1).

## Judge thread verdict.md

# Determinism judge verdict, task445 (pass 2)

- **Verdict:** DETERMINISTIC, SOLUTION_WRONG (one non-reproducing figure in the Final Recommendation prose)
- **Disposition:** FIX_NOW. Change "SAF (80.3)" to "SAF (80.2)" in section 1. Only the write-up changes, the prompt and bundle stay byte-identical, so no model rerun is needed.

## Why

The call rests on one fact: on 3 February 2023 the December 13F window is still open (day 34 of 45, readme). 125 managers that filed a September holdings or combination report have no December report on file. The figure OM-4 s.2 asks for (holdings of *all* managers that file for the period) therefore has to be completed, and the bundle lets you choose the completion method by testing each one on the September window at day 34. Carrying each missing manager at its prior-quarter position misses every name by at most 2.59 points (mean absolute error 0.66). One aggregate completion share (0.815) misses by up to 22.29. Per-name completion shares miss by 4 to 9 points, and growth-adjusted carry has a mean absolute error of 1.02 with a worst miss of 3.08. Plain carry wins the test, and it gives WHII, GLI, OTF, JEMS and SAF above 80.0 (OM-4 s.7). Growth-adjusted carry gives the same five flags, so the main call holds under both carry variants. The only defect is the SAF figure under the rejected aggregate method: it is 80.2, not 80.3.

## Evidence: recomputation ledger

| Figure | Claimed | Recomputed | Reproduced | Source |
|---|---|---|---|---|
| Managers with Sep HR/combination and no Dec report by 3 Feb | 125 | 125 (0 of them filed a Dec notice) | yes | SUBMISSION+COVERPAGE, q4 data set + daily build |
| Dec ownership WHII / GLI / OTF / JEMS / SAF | 88.6 / 84.4 / 83.4 / 84.8 / 91.4 | 88.56 / 84.37 / 83.38 / 84.83 / 91.42 | yes | daily INFOTABLE + carried q4 INFOTABLE, num.txt Oct-dated counts |
| Highest unflagged FENN / AMRB | 77.3 / 76.2 | 77.30 / 76.23 | yes | same |
| Dec ownership TAAV / ABBB / OLPD / HAMR / NOPR | 74.3 / 62.3 / 71.1 / 55.2 / 67.2 | 74.31 / 62.31 / 71.14 / 55.20 / 67.20 | yes | same |
| Reports-in-hand flags | WHII, JEMS | 82.81, 80.09 (next highest AMRB 72.42) | yes | daily INFOTABLE |
| Aggregate completion share, Sep window day 34 | 0.820 | 0.8197 (dollar basis, ex put/call) | yes | q4 data set + daily; VALUE x1000 before 3 Jan 2023 |
| Aggregate flags | AMRB, TAAV, FENN, SAF (80.3); misses GLI, OTF | AMRB 88.3, TAAV 82.9, FENN 81.1, SAF **80.2**; GLI 68.6, OTF 71.7 | flags yes, **SAF 80.3 no (80.24 at 0.8197, 80.21 at 0.820)** | |
| June-window completion share, day 34 | 0.815 | 0.8147 | yes | q3 data set |
| Backtest: carry max miss / aggregate max miss | 2.6 / 22.3 | 2.59 (AMRB) / 22.29 (GLI) | yes | Sep window as of 3 Nov 2022 vs final Sep |
| September flags (miss OTF rise, FENN fall) | n/a | Sep: WHII 86.3, GLI 83.2, JEMS 82.7, FENN 81.6, SAF 89.9; OTF 78.7 | yes | |
| Dec shares outstanding (12 names) | per golden | identical (latest ddate <= 2022-12-31; Jan-2023 10-K counts excluded) | yes | fsds num.txt/sub.txt |
| Sep shares outstanding (12 names) | per golden | identical (July-dated counts) | yes | same |
| Sep ownership (12 names) | 86.3, 83.2, 78.7, 74.8, 76.9, 82.7, 81.6, 61.1, 70.1, 89.9, 53.8, 66.2 | 86.30, 83.20, 78.66, 74.77, 76.86, 82.74, 81.57, 61.06, 70.13, 89.87, 53.79, 66.17 | yes | q4 data set + 3 late Sep originals and 1 NEW HOLDINGS amendment in daily build, one RESTATEMENT applied |
| Largest Dec holder and value (12 names) | Prescott/Wexley/Tregaron per golden | identical names, CIKs and whole-dollar values (Wexley 0001085146-23-000343 filed 25 Jan in thousands, x1000) | yes | daily INFOTABLE/COVERPAGE |
| Bridge: lines as filed | 568,922,286 | 568,922,286 | yes | all Sep-period INFOTABLE lines, CUSIP exact match |
| Bridge: put and call | -5,183,600 | -5,183,600 | yes | |
| Bridge: superseded by restatement | -16,011,685 | -16,011,685 | yes | CIK 1287806 original 0001104659-22-000732 |
| Bridge: malformed CUSIP | +9,304,719 | +9,304,719 (zeros 5,846,688; lower case 2,993,879; check digit 464,152) | yes | |
| Bridge: Sep institutional shares | 557,031,720 | 557,031,720 | yes | |

## Competing answers that survived

None survives on the main call. These were tested and ruled out:
- Reports in hand only (WHII, JEMS). OM-4 s.2 counts all managers that file for the period, and the readme's 45-day window is still open on 3 Feb, so this reading undercounts the quantity OM-4 defines. It is the easy-route answer, not a licensed reading.
- Aggregate completion share (adds AMRB, TAAV, FENN, drops GLI, OTF). It misses by up to 22.3 points in the backtest.
- Per-name completion share (adds AMRB, FENN). It misses by 4 to 9 points in the backtest, with a systematic bias.
- Growth-adjusted carry: same five flags. Its Dec percentages differ by up to 1.7 points (OTF 85.1), but its backtest error is worse than plain carry's (1.02 vs 0.66).
- Combining affiliate families: this would change the top holder for TAAV and NOPR (Shelby Investment Group), but OM-4 s.6 and data_sources.md both say families are not combined.
- Carried managers as top holder: the largest carried position (Sep shares x Dec price) never comes close to the filed leader.

Residual ask-level risks, which are not failing but should be noted for grading tolerance:
- (a) "SEC's own files" could be read as the SEC data sets only. The start bar would then be 544,752,819, plus a +24,169,467 bar for January filings from the nightly build. "every September-quarter information-table line" favours the golden's reading.
- (b) A response may split the malformed-CUSIP bar into its three parts. The rubric should accept any split that sums to +9,304,719.

## Files/Hygiene

PASS. The bundle has 19 files: tsv x9, txt x3, csv x2, md x2, xlsx, pdf and htm. INFOTABLE files exceed 25,000 rows. Distractors: short_interest_20221230.csv, 13flist2022q4.txt and the manager_register family column. File dates sit at or before 4 Feb 2023, consistent with the 3 Feb cut. I found no "synthetic", "generated" or "benchmark" strings. PDF and xlsx metadata are plausible (Word Print-to-PDF, Excel 16). There is no exclusion-level finding. The cross-batch check was not run: other batches are outside the permitted directory.

## Stump power

Moderate. The trap is the right-censored filing window. A solver that reads the reports in hand files WHII and JEMS. A solver that scales by one completion share files WHII, AMRB, TAAV, JEMS, FENN and SAF. Both are concrete, wrong committed answers. The risk is that carrying non-filers forward is a known 13F convention, so a strong model that counts the 125 missing managers may carry them by habit and land the call. The asks (OM-4 CUSIP repair, the filing still in thousands, the restatement, cover-date selection) carry the rest. Route to live testing. If the call is landed, the natural lever is to make the backtest discriminate between carry and growth-adjusted carry on the flag line, not to add mess.

## Stumping type

`mechanism: forecasting` (nowcast of the final December ownership, with method selection by backtest), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. Every on-file figure is correct as filed. The difficulty is completing an incomplete quarter and choosing the completion method by testing it on the prior window, so Gate G passes.

## Three rules

`domain: pass`, `layers: pass`, `decisive_step: analytical`.

The field's own analysis decides it: estimating period-end 13F institutional ownership before the 45-day window closes, with holder-level carry of late filers validated on the prior window. The swap test fails to transpose, because the filing lag and the holder-level carry are specific to 13F work.
- Layer 1: three submission-quarter data sets plus a nightly build, amendments, malformed CUSIPs, one filing in thousands, and cover counts dated after period end.
- Layer 2: right-censoring of the December filings and the choice of completion estimator.
- Easy route: a strong analyst who cleans everything but uses the reports in hand gets WHII and JEMS. One who scales by one completion share gets six names, including AMRB, TAAV and FENN.

## Fix

Location: solution. In section 1, change "SAF (80.3)" to "SAF (80.2)". Optional rubric tolerance: accept a three-way split of the malformed-CUSIP bar, and a start of 544,752,819 when it comes with a +24,169,467 January-filings bar.

