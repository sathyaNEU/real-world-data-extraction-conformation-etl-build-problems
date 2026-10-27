# leak check, task307

**Verdict: REVIEW.** 16 files read, 47 golden figures and 11 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: network, no-build, street, equilibrium, center, documentation, loaded, bridge, volumes, widening, capacity, decisive, window, asserted, planning, volume-delay, traffic, counts, functions, re-route, sentence, screen, dropped, manual, domain

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `MAMPO_TDM_v4.2_documentation_ch4-6.pdf`: \bthe model\b x3: ...d in passenger-car equivalents, a heavy vehicle counting as 2.0, with the model's heavy-vehicle percentage for the link alongside. 6.4 Validation. Th...

## 3 answer figures in the pack (REVIEW 7)
- **REVIEW** `ATR_hourly_volumes_2025.csv`: golden figure 15,291 appears: ...0102,EB,02/07/2025,14,274,OK S-0102,EB,02/07/2025,15,291,OK S-0102,EB,02/07/2025,16,259,OK S-0102,EB,02/07...
- **REVIEW** `ATR_hourly_volumes_2025.csv`: golden figure 19,396 appears: ...03R,EB,09/05/2025,18,437,OK S-0103R,EB,09/05/2025,19,396,OK S-0103R,EB,09/05/2025,20,373,OK S-0103R,EB,09/...
- **REVIEW** `ATR_hourly_volumes_2025.csv`: golden figure 10,188 appears: ...-0102,EB,06/19/2025,9,140,OK S-0102,EB,06/19/2025,10,188,OK S-0102,EB,06/19/2025,11,209,OK S-0102,EB,06/19...
- **REVIEW** `ATR_hourly_volumes_2025.csv`: golden figure 13,859 appears: ...0105,NB,07/26/2025,12,768,OK S-0105,NB,07/26/2025,13,859,OK S-0105,NB,07/26/2025,14,804,OK S-0105,NB,07/26...
- **REVIEW** `MAMPO_CMP_reliability_measures_2026.pdf`: golden figure 2.2 appears: ...only when every segment of the corridor reports. 2.2 The planning time index for a peak hour is the 95...
- **REVIEW** `MAMPO_TDM_v4.2_documentation_ch4-6.pdf`: golden figure 100 appears: ...in Table 4.2. 4.2 Zones are numbered by district: 100s on the west bank, 200s downtown, 300s east, 400s...
- **REVIEW** `MAMPO_TIP_project_scoring_guidance_2026.pdf`: golden figure 2.2 appears: ...s not credit trips a project would add or remove. 2.2 The annual benefit is the AM peak-hour reduction...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `MAMPO_TDM_v4.2_documentation_ch4-6.pdf`: 11 of 25 stump-paragraph terms appear (network, equilibrium, documentation, bridge, volumes, capacity); read whether the document names the move
- **REVIEW** `MAMPO_TIP_project_scoring_guidance_2026.pdf`: 3 of 25 stump-paragraph terms appear (network, no-build, planning); read whether the document names the move
- **REVIEW** `MAMPO_traffic_count_program_manual_2024.pdf`: 3 of 25 stump-paragraph terms appear (planning, traffic, manual); read whether the document names the move

## 6 ranking artifacts (REVIEW 6)
- **REVIEW** `ATR_station_inventory_2025.xlsx`: names 10 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `CMP_probe_segment_reference.csv`: names 7 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `FY2028_TIP_congestion_relief_candidates.xlsx`: names 6 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `MAMPO_v42_subarea_links_2028NB.csv`: names 8 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `MRTA_route_ridership_FY2025.csv`: names 3 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `crash_summary_by_segment_2021_2025.xlsx`: names 10 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Three isolated reads (sonnet, medium), each on a fresh copy of prompt.txt and target/ only.

- Read 1 (pack as first cut): no decisive-step sentence; no file ranks the candidates; no helper beyond the no-build
  loaded network as a check on a solver's own run; nothing reads as the answer. Question 5: guidance 2.1 and 2.2 with
  documentation 6.1 (equilibrium) fix the estimand and the method. Question 6: mainly following a stated procedure.
  Every REVIEW line harmless. Realism tells: erratic transit boardings, identical heavy-vehicle shares, costs stored as
  text, regular work-order numbers (all fixed in the generator).
- Read 2 (after the stage 4 repair): the same answers on questions 1 to 5; question 6 mostly a stated procedure with an
  analytical element; it named the Route 9 description ("the weaving between the ramps remains") as a mild nudge
  (made neutral). Every REVIEW line harmless.
- Read 3 (final pack): question 1 none; question 2 none; question 3 none; question 4 none; question 5 guidance 2.1 and
  2.2 with documentation 6.1, executing to the golden's construction; question 6 an analytical choice ("executing a
  full user-equilibrium assignment on the no-build and build networks is the method an expert would use; the easy route
  is to read the benefit off the shipped no-build loaded volumes"). The candidate descriptions and manual 3.2 harmless.
