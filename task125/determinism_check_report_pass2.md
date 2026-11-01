# Determinism verdict, task125 (pass 2)

- **Verdict:** DETERMINISTIC (SOLUTION_WRONG, minor: three cells of patrol_figures_2026.csv do not reproduce, see Evidence).
- **Disposition:** FIX_NOW. The 20-segment designation, the come-in and drop-out lists and the chart are forced. Re-derive the three Q1 hour cells (or find the unstated rule behind them) and correct the solution blocks. No model rerun is needed if the blocks only change to the literal figures. If the generator rule behind the three cells is a real convention, it must be filed in the pack instead.
- **Why:** Read literally, the protocol designates the 20 segments with the highest expected 2027 patrol crimes. Over 2022-2026 the five Lakeshore segments and the five Gardens segments carry large, venue-specific event-night excesses. The register shows the Mariners' last Gardens game on 20 Dec 2026 and 16 Lakeshore home games booked from 8 Jan 2027. The cut falls in a 23-crime gap (57.1 against 34.1), so the 20 are forced for every reasonable event-night estimate I tried.

## Evidence (recomputed from the shipped files)

| Item | Result |
|---|---|
| Conformed patrol crimes | Latest version per occurrence (59,388 occurrences), legacy codes read through the crosswalk, legacy day-first dates parsed, UNFOUNDED out, occurred_from or the report date. 29,756 patrol crimes; 5,859 to 5,981 per year over 2022-2026. All have a segment_id that is in the segment file. |
| Candidates (at least 25 in some year) | 52. Reproduced. |
| 2026 ranking | Top 20 ends at 162877 (48), and 109465 follows at 38. The 2026 top 20 holds 145175, 162095, 162877, 168732 and 171145, which the golden drops. Reproduced. |
| Event nights, 2022-2026 | Gardens 200 distinct dates, Lakeshore 61, no overlap. Counts are the same whether or not cancelled lines are excluded. Reproduced. |
| 2027 register sheet | 16 Mariners dates at Lakeshore, Jan to Mar. 2027 Lakeshore dates total 32 and Gardens dates 2. The Mariners play Jan-Mar and Oct-Dec (2026: 35 Gardens dates). Reproduced. |
| Critical component 2 | Five Gardens segments: 801 of 1345 crimes on 200 nights (11.0%). Reproduced. |
| Critical component 3 | Five Lakeshore segments: 410 of 822 on 61 nights. Reproduced. |
| Critical component 4 | 112148 has 116 of 354 on Gardens nights. Its fit gives a steady rate of 0.15 a day and a modest Gardens excess of 0.43; its expected 2027 count is 57.3 and it stays in. |
| Fit | Per-segment least squares on a constant and the two venue-night indicators, expected 2027 = 365 x steady rate + excess x nights. With 48 Lakeshore and 6 Gardens nights I get exactly the golden 20. Rank 20 is 185090 (57.13) and rank 21 is 186587 (34.08). |
| Robustness of the 20 | Identical set for 32/2 (2027 sheet only), 20/0, 30/0, 29/0, 61/0, 60/10, 48/6, fits from 2024, 2025 or 2026 only, and crimes from 14:00 to 03:00 only. Different only under wrong readings: 13 Lakeshore and 41 Gardens (no venue move) gives the 2026-style set. 0/0 and Mariners removed from Gardens but not added to Lakeshore (13/6) also differ. |
| Come-in and drop-out lists | Reproduced: 124511, 158663, 150449, 176470, 109465 in; 162095, 171145, 168732, 145175, 162877 out. |
| Officer-hours CSV | 29 of 32 cells reproduce after rounding. Method: non-OFFICER calls, received in 2026 local time (America/Toronto), segment_id in the file, ward from the segment, dispatch-to-clear hours times roster crew on the tour covering the dispatch local time (night tour dated by the evening it starts). Ward is the same whether taken from segment or district. |
| Cells that do not reproduce | Ward 2 Q1: I get 455.5, the golden says 453. Ward 5 Q1: I get 911.8, the golden says 911. Ward 6 Q1: I get 1029.7, the golden says 1028. All other cells match. I could not find a rule explaining the gap: it is not DST handling, cancelled dispositions, duplicates, the UTC quarter, a fixed UTC offset, or a missing roster tour. |

## Literal-reading forks
- "Expected" is not defined as a method. The naive 2026 count or five-year average reads as a defensible literal "expected" to a careless reader, but it ignores the 2027 register, which is in the pack and is what the protocol's "expected in the year the designation covers" calls for. Both are listed in the design as the wrong easy route.
- The 2027 event-night count is not fixed. The result is invariant across the whole defensible range, so no fork.
- Whether hours are quarter-bounded by local or UTC receipt is closed by the directive ("local date on which it was received").

## Files/Hygiene: PASS
11 files, 4 formats (6 CSV, 2 PDF, 1 XLSX with six sheets, 1 EML). One file is 82k rows (the RMS) and one 37.9k rows (the CAD). The register carries two different layouts across years and mixed date formats (day-first text and ISO). The RMS carries legacy codes, day-first legacy dates and multiple versions. Distractors: streetlight_service_requests_2026.csv and ward_profiles_2021_census.csv, both unused. Temporal coherence holds (protocol approved 10 Nov 2026, email 6 Jan 2027, extract to 6 Jan 2027, 2027 sheet booked). No authoring or provenance leakage and no public-data contamination seen. The email names the files but not the venue effect.

## Stump power (Gate F)
Good. A strong analyst that cleaned everything and ranks on 2026 or the five-year average files the 2026 top 20, wrong on five segments. The register's venue move (Gardens' last Mariners game 20 Dec 2026, Lakeshore bookings from 8 Jan 2027) is in a file the email names. Strong models read every file, so the part likely to stump is carrying the venue-specific excess forward rather than discovering the register. Nothing in the prompt, email or protocol names event nights.

## Stumping type (Gate G)
mechanism: forecasting
stumping_family: analytical_non_defect
surface_read_dependency: no
sole_data_defect: no
Reported counts are all correct; the difficulty is a forward projection that the correctly-read past does not pin because the nights that carried it move venue. On clean data it still stumps.

## Three rules (Gate H)
domain: pass | layers: pass (Layer 1: legacy codes and dates, record versions, unfounded, two register layouts, UTC against local time. Layer 2: event-night-adjusted expected counts for 2027) | decisive_step: analytical
The field's own analysis is a hot-spot forecast of crime by place with a known exposure change. The easy route (rank on 2026 or the five-year average) keeps the five Gardens segments and drops the five Lakeshore ones. Swap test: replace crimes with another measure and the register and event excess no longer mean anything, so the domain is not a backdrop.

## Fix
solution: correct or re-derive the Q1 cells for wards 2, 5 and 6 of patrol_figures_2026.csv, or pin the rule that produces them in the protocol or directive text if one exists. Everything else is none.
