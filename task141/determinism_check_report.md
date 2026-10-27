# determinism-check report, task141, 2026-10-27

(Replaces the stale report of the superseded architecture 2, at the coordinator's instruction; it stays in git history.
Bundle sha256 prefix 7cd8129f3a06c789. Judge: one general-purpose sonnet medium thread, brief
/tmp/determinism-check-task141-053423/judge_brief.md, verdict /tmp/determinism-check-task141-053423/verdict.md.)

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (solution wording only; prompt, bundle and goldens untouched, no rebuild)
**Stumping type:** mechanism: forecasting (design note: gap time then population), stumping_family: analytical_non_defect (note: estimation_fit), surface_read_dependency: no, sole_data_defect: no

## Why
The shipped files force 6 pods and 1,200 admissions. Felony petitions cluster in the last 90 days before the expiration in
force (hazard per term-month 0.074, 0.136, 0.057 in the 0-30, 30-60, 60-90 day bins, then 0.012 for 90-120 = base rate).
SB 26-118 moves the expirations of 3,373 open terms to 31 March 2027, so the petitions and their revocations land in
Q1/Q2 2027. The trailing-year run rate (912, 5 pods) and a months-on-supervision survival projection both miss the second
clock. 1,186 and 1,200 both give 6 pods under the Annex (one 64-bed pod per 220 or part of 220). The judge's own day-profile
model gave about 1,190, the no-Act model about 954.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Open felony terms | 7,620 | 7,620 (cms2 OPEN+FELONY) | yes |
| Terms ended 31 Mar 2027 | 3,373 | 3,373 | yes |
| Trailing-year admissions | 912 | 912 | yes |
| 2027 projection | 1,186 | about 1,190 (day-profile model) | yes, within model spread |
| Average term imposed, office and tenure | 53.4/53.1/53.5/52.8; 48.3/50.0/53.9/62.9 | identical (alt bucketings same; inclusive-day moves one cell 50.0 to 49.9, not a reasonable fork) | yes |
| Bed-days Q4 2025 to Q2 2026 | felony 29,375 / 26,462 / 26,086; misd 2,228 / 2,478 / 2,321 | identical | yes |
| Bed-days Q3 2026 | felony 27,929; misd 2,088 | 27,931; 2,086 | no, by 2 days: one person (SO2220631) reclassified PV-FEL to PV-MIS on 14 Sep 2026; judge carried the felony level, golden takes the level of the booking in force (instructions 5.3), so the golden is the better reading |
| Survival comparator "607" | 607 | naive runs gave 830 and 1,026 | no (direction holds, wrong call either way) |
| 26.4 per cent against 4.5 per cent | stated | hazard shape confirmed (end-window 0.064-0.073 per term-month every fiscal year against 0.016-0.017 outside); the two percentages not separately recomputed | shape yes |

## Competing answers that survived
- Window-shape fork (thin): flat 90-day window 1,201 (6 pods); flat 120-day per-day rate truncated at 1 Jan 1,115 (5 pods); flat 150-day per-day rate 1,044 (5 pods); profile without revocation exit 1,277 (6 pods, 1,300). The 5-pod answers need the end-window mass spread uniformly over 120 or 150 days and cut at 1 January; the shipped petitions refute that (zero excess in days 90-120). Closed by the data, not by a filed sentence. The submission's "window of 90 to 150 days: 1,169 to 1,203, six pods throughout" holds only under a per-term probability reading; step 4's "last 120 days ... from 1 January" invites the per-day reading. The design note's SF12 asserts the family in `checks.py`; the judge could not reproduce that under the per-day reading.
- Margin to the 1,150 rounding line is about 36 admissions (3 per cent).
- Other forks (admission day, Act timing, supervision start, pod count) closed.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10+ | 13 | yes |
| Formats | 3+ | 3 (9 csv, 3 pdf, 1 xlsx) | yes |
| Large file | 25,000+ rows | detention_probation_bookings 48,177 rows (petitions 25,879) | yes |
| Distractors | 2+ named in metadata.json, none in a file name | apd_annual_report_2025.pdf, detention_daily_headcount_2025_2026.csv; names not labelling | yes |
| Distractors unused yet weighable, ruled out by a shipped fact | yes | annual report counts FY2025 petitions only; headcount is a 06:00 count against midnight bed-days; judge used them as weighable distractors | yes |
| Deliverables | 1 to 3, all in golden | 3 (xlsx, docx, png), all present in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | prompt states nearest 100, whole days, months to one decimal; asks are quarter x level and office x tenure grids | yes |
| Prompt shape, 25+ criteria | identifiable; 25+ | one paragraph, 927 characters; criterion count not generated here (grid asks give well over 25 cells) | yes, count unverified |
| Not LLM generated, goldens business-realistic | yes | judge found no authoring or provenance language; golden realism not re-read by me | yes (judge) |

## Gate G reconciliation
The judge: mechanism forecasting, family analytical_non_defect, surface_read_dependency no, sole_data_defect no. The design note: gap time then population, family `estimation_fit`, Gate G `forecasting`, strategy `time_semantics`. Same class, no mismatch. The judge did not name a declared distractor (annual report, headcount) as carrying the task, so they are not too load-bearing. The judge named the run rate (912) and the survival projection as the easy routes, which matches the note's default path (607, 3 pods). Gate G holds: no shipped artifact ranks candidates wrongly; 912 is a true trailing count.

## Stump power (Gate F)
Moderate to high per the judge: a strong analyst's survival projection or run rate files the wrong pod count, and reading the second clock needs petitions aligned on a time-varying expiration rebuilt from the term orders. Gate H line: domain pass, layers pass, decisive_step analytical. This matches the card's `stump_class: analytical` and the note's `## Three rules`. The judge's swap test breaks the task and it classed applying the Act to the 3,373 terms as a lower rule-application step. Caveat for the main thread: the judge's own survival runs reached 830 and 1,026 (the latter is 5 pods), so the naive route does not always file 3 pods; it files a wrong call either way (4 or 5 pods against 6).

## Findings, ranked
1. Window-shape fragility (Gate C margin): the "six pods throughout" claim for 90-150 day windows holds only under a per-term probability reading; a per-day rate over 120 or 150 days truncated at 1 January gives 1,115 / 1,044 and 5 pods. The data separate them (zero excess in days 90-120), so a rigorous solver lands 6, but the solution text invites the other reading. Fix: in step 4, step 5 and the Final Recommendation, state the variant ranges under the per-term end-of-term probability (about 0.27 of terms petition in the last 90 days), and say a uniform per-day rate over 120 or 150 days contradicts the day profile. Keep it wording only; do not file the HOW into the prompt (CLAUDE.md rule on determinism repairs).
2. Critical components do not show why the 1 January truncation loses no mass. Fix: quote the day-bin hazards (0.074 / 0.136 / 0.057 / 0.012) in the critical components.
3. The "607" survival comparator and the "Not 3 pods" sentence do not reproduce in the judge's naive runs (830, 1,026). Fix: cite 607 only if `generator/golden.py` reproduces it on this bundle, with the exact specification (exposure from 1 July 2016, pooled, with CSRS); otherwise say the naive route files a lower, non-six-pod count.
4. Bed-days Q3 2026 differ by 2 days from a felony-level-carried reading (SO2220631). Golden is the better reading; no change, but the memo or xlsx may state that the level follows the booking in force.

## Next action for the author
Reword solution step 4 and 5 and the Final Recommendation per findings 1 to 3 in submission.md and the memo (no prompt, bundle or figure change, no rebuild), confirm 607 against generator/golden.py, then re-judge once only if the main thread wants it.
