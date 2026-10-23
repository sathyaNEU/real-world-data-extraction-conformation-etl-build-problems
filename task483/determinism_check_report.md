# determinism-check report, task483, 2026-10-23 (round 4)

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

Thread: one general-purpose sonnet/medium thread, run id r41792769182, fresh unzip of the final target.zip; verdict at /tmp/determinism-check-task483-r41792769182/verdict.md.

## Why
Executed word for word, the standard gives a pooled median across campuses and both award years (3.1), CPI 1.0294 on 2024 cells (3.2), work status on the 180th day for grant completers (4.1) and the 75 per cent rule on 2024-25 completers of tested programs (5.1, 5.2): 71 per cent (1,021 of 1,441), so the designation lapses. No gate A to E failure. The new round-4 pieces (whole-hour attendance, ask B loan totals) reproduce.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Credit-program earnings (11 tested; Paralegal suppressed) | 44/40/28/27/28/52/50/33/65/71/47 | same (Medical Assisting 33.06; 33.03 under monotone spline) | yes |
| Short-term placement (10 tested; Forklift 18, untested) | CDL 63, EMT 44, Coding 50, others 83 to 92 | same (CDL 50/79); nearest dated start/exit 17 days from day 180 | yes |
| Designation share | 71 (1,021 of 1,441) | 70.85 | yes |
| Either correction alone | 77 / 78 | 77.8 / 76.9 (both fixed 83.8) | yes (consistent) |
| Clock hours (11 programs) | CDL 13,127 ... Welding Fund. 16,485 | same; 333 repeated rows dropped; decimal reading would differ | yes |
| Loan median and total (12 each) | RN 14,750 / 1,422,960; MA 7,250 / 369,390; Paralegal 9,860 / 66,980 etc. | all 24 match; window end 30 Jun 2025 changes nothing | yes |

## Competing answers that survived
None. Considered and closed: averaged cell medians (MA 36, pass) closed by "taken as one group"; any pay in the quarter (CDL 91) closed by "working on the 180th day"; decimal-hours attendance closed by fractional parts never above .55 in steps of .05; loan rows as installments closed by the annual limits in the cost of attendance pdf. Strict whole-quarter job reading (CDL 59.5) still lapses, so the call is unaffected (it would flip Phlebotomy, but that reading ignores starts and exits the pay records show). Note: the attendance `hours` field is unlabelled in the files, but the data forces the HH.MM reading.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 14 | yes |
| Formats | 3+ | csv, xlsx, pdf | yes |
| Large file | 25,000+ rows | attendance 53,563; wage records 27,704 | yes |
| Distractors | 2+ named in metadata, none labelled in a file name | state OEWS wage estimates, in-demand occupations list; names do not label them | yes |
| Distractor use | unused, weighable, ruled out by a shipped fact | neither answers a graded quantity (verified by thread; statewide pay / outreach list, no test reads them) | yes |
| Deliverables | 1 to 3, all in golden | 2 (xlsx, svg), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | 9 numbered items, units and rounding in the prompt sentence | yes |
| Prompt shape / rubric | identifiable shape, 25+ criteria | shape 16; about 11+11+12+12+... per-program figures plus call, share, chart gives well over 25 | yes |
| Reads as real | no LLM tells, goldens real | thread found none; minor: PDFs very short and tidy | yes |

## Gate G reconciliation
Thread: mechanism method_or_model_selection, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card: stump_strategy grain_or_unit, layer2_family estimation_fit, stump_class analytical. Consistent (pooling released percentiles and dating a job inside a quarter are both estimation under a coarser recorded grain). The thread did not name either declared distractor as the surface read; no ranking artifact gets the decision wrong. The design note's stump sentence (default 84 per cent, either correction alone keeps) matches the thread's 77.8 / 76.9 / 83.8.

## Gate H line
domain: pass, layers: pass, decisive_step: analytical. Matches the card's analyst_test and domain_test (pooled half point of rebuilt cell distributions, and day-180 status dated from partial-quarter pay). Caution recorded by the thread: the dating step is close to data semantics, but it is the unit-of-analysis choice between interval and quarter reading.

## Stump power (Gate F)
Strong per the thread: each shortcut alone still renews, only both corrections together lapse. The pooled-median method is a field-standard route; the main thread should weigh this with the scored readers' result.

## Findings, ranked
1. None blocking.
2. Minor: unlabelled `hours` field in the attendance export (data forces HH.MM; fork SF17 closed in the note).
3. Minor: dating step sits near data semantics (Gate H caution).

## Next action for the author
Proceed to ship; no repair or re-judge needed.
