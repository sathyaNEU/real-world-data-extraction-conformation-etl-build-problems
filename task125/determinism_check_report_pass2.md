# determinism-check report, task125 (architecture 4, pass 2), 2027-01-06 extract, run 2026-11-01

Re-judge after the pass 1 FIX_NOW repair. target.zip sha256 d5c73e26832037af09d43e4a69c997433a118b7231d4ffad9841d57eba7f3ef9. One isolated sonnet thread (medium) on a fresh unzip at /tmp/determinism-check-task125-pass2/target/; its verdict is /tmp/determinism-check-task125-pass2/verdict.md. The thread saw neither pass 1's report nor the repair's description.

## Verdict
DETERMINISTIC, with SOLUTION_WRONG (minor): three cells of patrol_figures_2026.csv do not reproduce.
**Disposition (thread):** FIX_NOW.
**Disposition (reconciled):** FIX_NOW. Gates G and H both pass, so there is no SEND_BACK. The gate that fails is Gate A (every figure recomputes from the shipped files), which fails as `solution_incorrect` and is fixable. The fault is neither G nor H.
**Stumping type:** mechanism: forecasting, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no
**Gate H line (thread):** domain: pass | layers: pass (Layer 1: legacy codes and dates, record versions, unfounded, two register layouts, UTC against local time. Layer 2: event-night-adjusted expected counts for 2027) | decisive_step: analytical

## Why
Read literally, the protocol designates the 20 segments with the highest expected 2027 patrol crimes. The thread reproduced the main call and every deck answer:
- The 20 designated segments reproduce.
- The five segments that come in and the five that drop out reproduce.
- The chart's 52 candidates reproduce.
- Critical components 2, 3 and 4 reproduce.

The cut falls in a 23-crime gap (57.13 for 185090 against 34.08 for 186587). The same 20 come out under 48/6, 32/2, 20/0, 30/0, 29/0, 61/0 and 60/10 Lakeshore/Gardens nights, under fits from 2024, 2025 or 2026 only, and under crimes from 14:00 to 03:00 only. The wrong readings differ: 13/41 (no venue move), 0/0, and 13/6 (Gardens removed, Lakeshore not added).

The only failure is the officer-hours ask: 29 of 32 cells reproduce and three Q1 cells do not.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Candidate segments | 52 | 52 | yes |
| 2026 top-20 (default path) | drops 162095, 171145, 168732, 145175, 162877 | same | yes |
| Gardens event nights, 2022-26 | 200 | 200 | yes |
| Lakeshore event nights, 2022-26 | 61 | 61 | yes |
| Gardens five | 801 of 1345 (11 per cent of nights) | same | yes |
| Lakeshore five | 410 of 822 | same | yes |
| 112148 stays | in | 116 of 354 on Gardens nights; steady 0.15 a day; expected 57.3; stays in | yes |
| 2027 register | 16 Mariners home games at Lakeshore from 8 Jan 2027; 32 Lakeshore and 2 Gardens dates | same | yes |
| Rank 20 / rank 21 | 185090 / 186587 | 57.13 / 34.08 | yes |
| Officer-hours, 29 cells | as filed | match after rounding | yes |
| Officer-hours Ward 2 Q1 | 453 | 455.5 | NO |
| Officer-hours Ward 5 Q1 | 911 | 911.8 | NO |
| Officer-hours Ward 6 Q1 | 1028 | 1029.7 | NO |

Method behind the officer-hours recomputation:
- Calls with source not OFFICER, received in 2026 local time (America/Toronto).
- Only calls whose segment_id is in the segment file; ward taken from the segment (the same as the district).
- Each unit's hours run dispatch to clear.
- Hours are multiplied by the roster crew on the tour covering the dispatch local time, with a night tour dated by the evening it starts.

The thread ruled out DST handling, cancelled dispositions, duplicates, the UTC quarter, a fixed UTC offset and a missing roster tour as the cause. It found no rule that explains the gap. The three misses differ by 2.5, 0.8 and 1.7 hours, all in Q1, the quarter that holds the 8 and 9 March clock change.

## Competing answers that survived
- Main call: none. "Expected 2027" is not defined as a method, but the result is invariant across the defensible range of 2027 nights and fit windows. The naive 2026 or five-year-average route is the declared wrong route and is not a literal reading, because the register's 2027 sheet contradicts it.
- Officer-hours Q1, wards 2, 5 and 6: the golden and the thread's literal execution of Directive PO-14 and the roster differ by under 3 hours. Whichever side is wrong, a solver following the filed text may file a different whole number. This is an open fork on three graded cells, not a closed one.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Files | 10 or more | 11 | yes |
| Formats | 3 or more | 4 (CSV, PDF, XLSX, EML) | yes |
| Large file | 25,000 rows or more | RMS 82,436 rows; CAD 37,874 | yes |
| Distractors | two or more in metadata.json, none labelled by file name | ward_profiles_2021_census.csv and streetlight_service_requests_2026.csv; the file names do not say "distractor" | yes |
| Distractor use | unused by the solution but relevant enough to weigh; none answers a graded quantity | the thread found both unused. The ward profiles are the 2021 census, a ward-level context file. The streetlight requests are 2026 service requests. Neither reproduces a graded quantity. | yes |
| Deliverables | 1 to 3, all in golden | 2 (pptx, csv), both in golden/ | yes |
| Asks | multi-dimensional, unit and rounding stated | one ask of 32 ward-quarter cells; "Crimes and hours are whole numbers" is in the prompt | yes (a single ask family, but it is a grid) |
| Prompt shape and rubric | identifiable shape; 25 or more criteria | shape 01, a ranked list under a cap; 20 designated + 5 in + 5 out + chart + 32 cells gives well over 25 | yes |
| Reads as real and not LLM generated | no | thread saw no authoring leakage; the golden .pptx and .csv are plain business products | yes |

## Gate G reconciliation
Thread: mechanism forecasting, stumping_family analytical_non_defect, surface_read_dependency no, sole_data_defect no.

Design note and card:
- Strategy `composition_mix`, Gate G `method_or_model_selection`, family estimation_fit.
- `stump_class: analytical`, with the analyst test and domain test filed.
- The decisive step is splitting each segment's record into its steady rate and venue excess and carrying the excess by the 2027 calendar.
- The declared distractors (ward profiles, streetlight requests) carry nothing.

The two agree. No distractor is the surface read. The thread's "forecasting" is the same mechanism as the note's composition-mix forecast; the card's objective tag is Anomaly Detection & Diagnostics, so the objective label is a main-thread question and not a determinism finding. The thread read the decisive step as analytical, not as semantics or rule application.

The field's standard hot-spot forecast (last year's count, or the mean) is the default path and lands the wrong set, so the thread is not describing a landable textbook call. No stump-power discount is needed.

## Gate H reconciliation
The thread's Gate H line matches the note's `## Three rules` (domain test, Layer 1 and 2 split, decisive step analytical). No mismatch.

## Stump power (Gate F)
Good, and consistent with the note.
- The default path ends on the five Gardens segments in and the five Lakeshore segments out: 5 wrong segments.
- The venue move is in the register and nothing in the prompt, email or protocol names event nights.
- The half-aware routes miss (2b, 2c), and the standing family is unanimous.
- The thread judges that the part likely to stump strong models is carrying the venue excess forward, not finding the register.
- The ask weight is the 32 ward-quarter cells; the unreproduced Q1 cells do not move Gate F.

## Findings, ranked
1. **Gate A, `solution_incorrect`:** three Q1 officer-hours cells (ward 2: 453 vs 455.5; ward 5: 911 vs 911.8; ward 6: 1028 vs 1029.7) do not reproduce under the thread's literal execution of Directive PO-14 and the roster. The design note says "the judge's own pandas method reproduces all 32" and that Q1's ward 2 gap came from a night tour dated by subtracting a day of elapsed time on 9 March. Pass 2 reproduces only 29, so either the golden reckons something the filed text does not state, or the golden is off by a hair. Only Q1 fails, which makes the 8 and 9 March clock change and the night-tour dating the first things to check. The thread excluded plain DST handling, so the main thread should re-derive those cells from the generator's per-call table rather than assume a cause.
2. No Gate G, H, B, C, D or E finding. The main call, its stump and the deck's answers hold.

## Next action for the author
Re-derive the three Q1 officer-hours cells (ward 2, ward 5, ward 6) from the shipped CAD and roster files with the judge's method. Rebuild every Q1 call whose dispatch falls on or near 8 and 9 March, and find which rule yields 453, 911 and 1028. Then do one of two things:
- Correct the golden CSV and the solution blocks to the literal figures. The main call and the deck do not move.
- If a real convention explains them, file it in Directive PO-14 so the literal reading reaches them.

Keep every cell a quarter hour from its rounding edge. Re-judge once, only if the repair moves anything beyond these three numbers. A repair that changes only the figures needs no new judge pass; run `verify` and `figures_check.py`.
