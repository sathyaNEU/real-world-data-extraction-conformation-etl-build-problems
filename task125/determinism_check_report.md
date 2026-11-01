# Determinism verdict, task125 (Mountjoy hot spot patrols 2027)

- **Verdict:** NOT_DETERMINISTIC (supplementary answers on patrol_figures_2026.csv only; the main recommendation and the pptx answers are forced).
- **Disposition:** SEND_BACK. Close the 8 March 2026 spring-forward timestamp defect in mps_cad_calls_2026.csv (or file the convention in Directive PO-14) and regenerate the hours golden so every cell reproduces under the literal reading. This changes data solvers see, so a rerun is needed.
- **Why:** The main call is forced, but the CSV officer-hours ask fails Gates A and C. Three CAD unit rows on 2026-03-08 (E26-006286 F2, E26-006287 F2, E26-006288 D2; wards 6, 6, 8) have cleared_utc before dispatched_utc (hours -0.10, -1.07, -0.69 crew-weighted), and E26-006289 has dispatch before receipt. No shipped file says how to treat them. Read literally (negative interval kept) Ward 6 Q1 is 1024.9, which rounds to 1025, not the golden 1024. Dropping or clipping the rows gives 1026.07 for Ward 6 Q1 and 1278 for Ward 8 Q1 (golden 1277). Ward 2 Q1 reproduces as 455.2 (455), not the golden 453, and I found no convention that gives 453. Taxonomy label: underspecified_objective (an unfiled data convention) plus solution_incorrect for the two unreproduced cells.

## Evidence (recomputed from the bundle)

| Item | Result |
|---|---|
| RMS conformance (latest version, ISO and dd/mm dates parsed, crosswalk, unfounded out, occurred_from else reported, street file segments) | 29,568 founded patrol crimes 2022-2026; 52 candidate segments (at least 25 in a year), as the golden's 52. Latest-by-version equals latest-by-entered. |
| Event nights (EVENT duties at Gardens and Lakeshore, all sheets; no cancelled venue bookings exist) | Gardens 200, Lakeshore 61. Reproduced. |
| 410 of 822 (Lakeshore five) and 801 of 1345 (Gardens five) | Reproduced exactly. |
| Mariners | 2027 sheet has 16 Mariners games at Lakeshore (8 Jan to 20 Mar); last Gardens game 20 Dec 2026. Reproduced. |
| Constant plus two venue indicators per segment, 2027 = 6 Gardens and 48 Lakeshore nights | Top 20 identical to the golden list; rank 19 is 112148 at 57.25, rank 20 is 185090 at 57.13, rank 21 is 186587 at 34.08. Cut between 185090 and 186587 as stated. |
| Come in and drop out versus 2026 top 20 | Exactly the golden's five and five. The 2026 and five-year rankings give the same set. |
| Robustness of the 20 | Same set for Lakeshore nights 20 to 60 and Gardens nights 0 to 10, and for the literal 2027 register (2 Gardens, 32 Lakeshore). The "35 home games / 2026 calendar" assumption is not in any file but does not move the set. Keeping the Gardens nights at 41 flips it (the intended wrong route). |
| Weak spot | A per-segment linear-trend variant swaps 116925 for 162095 (46.9 vs 50.4 for the last place). Counts are flat citywide and the non-event counts of 162095 are noisy, so this is a poor method rather than a licensed reading. Residual note only. |
| Medians (first onscene_utc of any unit minus received_utc, priority 1, non-OFFICER, segment-file wards) | 5.7, 6.3, 5.7, 7.0, 6.9, 7.4, 7.1, 7.9: all eight reproduced. Ward 2 is 6.325 and Ward 8 is 7.925 unrounded, which sit on rounding edges. |
| Officer-hours (non-OFFICER, local-time receipt, dispatch-to-clear times crew on the tour covering the dispatch, night tour dated by start evening, segment-file ward) | 30 of 32 ward-quarters match the golden. Ward 2 Q1 and Ward 6 Q1 do not (above). |
| Rural-address fork | 3,444 CAD rows (about 9 percent) have segment ids 4xxxxx not in the street file, on CONCESSION, SIDEROAD, COUNTY RD and ELMVALE LINE addresses, with district values 1-8. Reading "ward" as the district column would add 50 to 120 hours per ward-quarter (Ward 2 Q1 558, Ward 8 Q1 1360). The literal text ("addresses in that ward of the City of Mountjoy", wards only from the street file) supports the golden. No shipped file mentions Elmvale by name. Residual risk, not a fail. |

## Files/Hygiene
PASS. 11 files: 5 CSV, xlsx, 2 PDF, eml (4 formats). The RMS file has 82,436 rows and the CAD file has 37,874 rows. Two distractors (ward profiles, streetlight requests) are unused by the solution. Dates are coherent (email 6 Jan 2027, 2027 register booked to 26 Jun 2027). The DST artifact on 8 March is a Layer 1 mess, but it is left without any rule for the three negative rows. No exclusion-level finding.

## Stump power
Good. The reported 2026 and five-year counts are correct and give a wrong 2027 set (same wrong five in, five out), and the signal is a venue exposure shift visible in the 2027 duty sheet. Only the analyst who estimates event-night excess per segment and re-exposes it to the 2027 calendar gets the right 20. The 2027 sheet shows the move at a glance, so a strong model may well find it. The modelling step (separating steady crime from event-night excess) is what separates answers.

## Stumping type
`mechanism: forecasting` (with method selection), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The trailing counts are fine; the decision turns on a forward exposure shift the history does not pin. Passes Gate G.

## Three rules
`domain: pass`, `layers: pass`, `decisive_step: analytical`. Hot spot designation by expected crime is the crime-analysis core; Layer 1 is RMS versions, legacy codes, dd/mm dates, UTC and DST; Layer 2 is the event-conditioned forecast. The easy route (rank 2026 or five-year counts) keeps the Gardens five and misses the Lakeshore five.

## Fix
`input_files` and `solution`. Either repair the three 8 March CAD rows (and the dispatch-before-receipt row), or file the convention for negative or implausible unit intervals in PO-14. Then regenerate the officer-hours golden so all 32 cells reproduce under a literal run. Re-verify Ward 2 Q1 (literal 455, golden 453) and Ward 6 Q1 (literal 1025 with the rows kept, 1026 with them dropped or clipped, golden 1024). Optionally note in the design that the 2027 calendar's game count is not filed, although the designation is robust to it. The main call, the pptx answers and the medians need no change.
