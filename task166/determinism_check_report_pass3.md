# determinism-check report, task166, 2026-10-27 (pass 3, /build stage 4 round 3)

## Verdict
NOT_DETERMINISTIC (underspecified_objective, onboarding_staffing_2025.xlsx ask 1 only). The main call, asks 2 and 3 and the critical components pass. SOLUTION_WRONG does not apply.
**Disposition:** FIX_NOW
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Round 2's two forks are closed. The group templates are filed in the data dictionary and the dated pod assignments are in the roster (pod by date is clean, boundary day inclusive). Every leaving deactivation now carries a reason, and CC1 and CC3 reproduce as about-figures. One fork remains in ask 1. The golden hours (West one-to-one Q1 323.00) hold only if a specialist listed on a colleague's two-specialist booking, while holding an overlapping session of their own, gets zero time on that booking. No shipped file states this. The dictionary says only "a booking with two specialists has a row for each". Literal readings:
- keep both rows: West one-to-one Q1 326.25 (Central 429.25, East 293.50);
- golden whole-hour drop on 59 clashes (60.5 h removed): 323.00;
- union of non-overlapped minutes: removes only 30.25 h, giving a third table, defensible because the overlaps are partial (30 or 45 minutes).
All 59 clashers are the first-listed row of the booking, and 16 own the case, so file order and ownership do not settle it.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| 2025 new paying customers | 1,744 | 1,744 (SW 303, SE 288, T&G 388, MW 264, NE 222, PAC 279) | yes |
| Ask 2, 18 plan counts | block 4 | identical | yes |
| Ask 3, 18 contract values | block 4 | identical (ACV/list ratio exactly 1, .95, .90 or .85 on all 1,744 under old SKU numbering) | yes |
| CC1 SW removals Apr-Sep 2026 | about 6,500, about 4x | 6,488, 4.05x (others 1.10 to 1.22x) | yes |
| CC2 founders share | about two in five; 10 to 11 months | 756 of 1,721 (44%); median 331 days (10.9 months) | yes |
| Founders linked | 4,451 | 4,451 | yes |
| Step 3 lag / yield | 333 days, 5.7 per hundred | 331 days, about 5.6 | immaterial drift |
| CC3 SW founded by leavers / usual intake | about 400 / 150 to 200 | 401 / 142 | yes |
| 2027 SW total / second | about 600, T&G second | about 590, rounds to 600; T&G about 420, rounds to 400 | yes |
| Ask 1 hours, 24 cells | block 4 | reproduced only after dropping the whole second-listed hour on 59 clashes | no (unfiled rule) |

## Competing answers that survived
- Ask 1: 326.25 (both rows kept) versus 323.00 (golden) versus a non-overlapped-minutes table. The golden's rule is filed nowhere. Closing line: one dictionary or prompt sentence.
- Main call: Texas & Gulf at about 400 is the intended wrong route, not a surviving answer. No other region is close; the Southwest leads by 150 or more, and 520 to 620 stays inside the 500 to 700 band.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 16 | yes |
| Formats | 3 or more | 4 (csv, xlsx, pdf, docx) | yes |
| Large file | 25,000 rows or more | 256,204-row user directory | yes |
| Distractors | 2 or more, in metadata.json, none named by file | board deck 2023 and CSAT responses; neither file name labels it | yes |
| Distractor role | unused by solution, relevant enough to weigh, ruled out by a shipped fact | the judge reports no use of either; the board deck's old-map history is superseded by the March 2024 map | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, xlsx), both golden | yes |
| Asks | multi-dimensional, unit and rounding stated | 24 + 18 + 18 cells; hours 2 dp, value in thousands to 1 dp, counts whole | yes |
| Rubric | 25 or more criteria | about 60 graded figures plus the call | yes |
| Prompt | one paragraph, under 1,000 chars | 907 | yes |
| Reads as LLM generated | none | judge found none; metadata, producers and dates consistent | yes |
| Golden determinism | every figure forced by shipped text | ask 1 fails | NO |

## Gate G reconciliation
Thread: mechanism forecasting, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. Card and design note: stump_class analytical, with a lagged-spillover forecast (founders from unconverted removals). They match. The judge did not name either declared distractor (board deck, CSAT) as the surface read. The stump is not carried by Layer-1 mess: on clean data it still holds. No Gate G mismatch.

## Gate H
domain pass, layers pass, decisive_step analytical. This matches the design note's Three rules (adoption carried between organisations, a lagged yield per removal). Counting, SKU roll-back and amendment ordering are lower rule-application steps, not decisive.

## Stump power (Gate F)
Strong. The judge's own route reaches the golden only by linking the user directory to removals by mobile. The history-only route (trend, season, log spend, small flat referral source) gives Texas & Gulf at about 400 to 500. The judge was not shown that route's number. The planning basis's Seats line is the only pointer to the censored removals. No "textbook method" caveat applies, because the judge needed the linkage and not a standard method. The scored readers' results should be weighed on the main thread.

## Findings, ranked
1. Ask 1 double-booking treatment is unfiled (underspecified_objective). Three literal readings give three tables, and the golden is the strictest. This is the only blocker.
2. Step 3 states 333 days and 5.7 per hundred, while the judge recomputes 331 and 5.6. This is immaterial. Restate as "about 331 days" and "about 5.6", or keep as about-figures.
3. The design note's A7 forcing figure (each of the 130 overlapping pairs has exactly one booking listing a second specialist who holds nothing else then) is a reconstruction the judge did not find as forced. The overlaps are partial, and whole-hour versus non-overlapped-minutes remains open.

## Next action for the author
Add one sentence to data_dictionary.pdf (or the prompt). It should say that a specialist listed on a booking whose time overlaps a session of their own spends no time on that booking, and that a second specialist with no clash keeps their own hour. Rebuild so the golden is unchanged, then re-judge once. If the author will not file it, re-key ask 1 to the literal count (326.25 and so on). The main call, asks 2 and 3 and the critical components need no change.
