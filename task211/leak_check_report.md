# leak check, task211

**Verdict: REVIEW.** 18 files read, 75 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: stations, natural, decisive, carries, cleared, excess, report, screen, increase, radiation, showers, university, export, analyst, shipped, physical, quantity, coastal, designation, driver, family, decides, points, gauges, procedure

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `air_filter_gamma_spectrometry_2026Q3.pdf`: golden figure 97.6 appears: ...25.8 I-131 8.02 d 364.5 81.5 Cs-134 2.065 y 604.7 97.6 Cs-137 30.05 y 661.7 85.1 Am-241 432.6 y 59.5 35....
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 99.5 appears: ...135 Moor Road 82.5 96.4 MV214 Moor Top Mast 123.2 99.5 MV226 Summit Transmitter 118.0 98.1 MV231 Upper R...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 99.3 appears: ...e Depot 93.4 97.8 MV112 School Playing Field 80.2 99.3 MV142 University Campus 80.7 97.5 MV171 Village G...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 98.6 appears: ...MV158 Crossroads 80.9 96.3 MV243 Fell Road Cairn 98.6 97.4 MV207 High Quarry 110.7 98.0 MV135 Moor Road...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 97.8 appears: ...River Bridge 72.8 98.5 MV184 Riverside Depot 93.4 97.8 MV112 School Playing Field 80.2 99.3 MV142 Univer...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 99.4 appears: ...ransmitter 118.0 98.1 MV231 Upper Reservoir 109.3 99.4 MV176 Beck Side 78.0 97.5 MV166 Carr Lane Allotme...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 97.5 appears: ...1 Upper Reservoir 109.3 99.4 MV176 Beck Side 78.0 97.5 MV166 Carr Lane Allotments 76.6 97.0 MV103 Grange...
- **REVIEW** `MVJC_service_agreement_schedule2.pdf`: carries 8 of 12 distinctive words of the committed call: 'Yes: notify increases of artificial origin at MV334 Headland Lookout on 6 days (08/07/2026, 17/07/2026, 20/07/2026, 22/0'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `MVGN-OP-04_network_operating_procedure.pdf`: 7 of 25 stump-paragraph terms appear (stations, carries, report, increase, radiation, university); read whether the document names the move
- **REVIEW** `MVJC_service_agreement_schedule2.pdf`: 7 of 25 stump-paragraph terms appear (stations, natural, report, increase, radiation, university); read whether the document names the move
- **REVIEW** `air_filter_gamma_spectrometry_2026Q3.pdf`: 3 of 25 stump-paragraph terms appear (report, university, analyst); read whether the document names the move
- **REVIEW** `mvgn_annual_report_2025.pdf`: 3 of 25 stump-paragraph terms appear (report, radiation, university); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 describing content (REVIEW 1)
- **REVIEW** `mvgn_annual_report_2025.pdf`: names 4 column(s) of the data files verbatim (Beck Side, Carr Lane Allotments, MV166, MV176): confirm it is the organisation's own record and not a note written for the analyst

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated reader, 2026-11-07 (general-purpose, sonnet, medium), architecture 1, on a fresh copy of prompt.txt and target/ (target.zip sha256 4c5bcbb4a4425d67873bb2563649ea6e76f07d279b47acd76bfb96ce6bfe06b3). Sweep 4's lines were kept out of the brief and ruled in the main thread (OP-04 files the investigation level, statuses, source checks and air sampling; no file states a washout screen or any rule for telling natural from artificial origin). Verdict: no leak; question 6 an analytical choice; only minor realism tells (empty Creator and Producer, exact-minute creation times).

1. Decisive step: none states it. Closest: MVJC_service_agreement_schedule2.pdf 2.2 "every increase in the ambient dose equivalent rate recorded at a network station that is of artificial origin ... Increases of natural origin, and the Contractor's own source checks, are not notified." It does not say how to tell them apart.
2. None. No file ranks or scores stations; the alarm config JSON holds only referenceLevel/investigationLevel/alertLevel per site.
3. None built for the analyst. The nearest context files are MVGN-OP-04 (procedure) and station_code_migration_2025.csv (code map), both ordinary operating documents.
4. None reads as an answer. Context only: annual report table, the gamma spectrometry table (all Cs-137 and I-131 "<" values), the stated "There were no notifications under Schedule 2 in 2025."
5. MVGN-OP-04 s3: "A ten-minute value 30 nSv/h or more above the reference level is an investigation-level value." (fixes the investigation level per station as reference plus 30, not the artificial-origin test). s2: status T is "not monitoring data", F has no dose rate, "Every other value carries the status V". s4: "A probe passes when its check reading is within 10 per cent of the expected reading ... Where a check is repeated at the same visit, the repeat is the check." s5: "gross beta activity divided by the volume of air drawn"; "reported in the quarter in which the filter is taken off". Schedule 2 2.3: timeliness is "the percentage of the quarter's ten-minute intervals for which the platform received the station's value by telemetry within sixty minutes of the end of the interval." These fix the source-check, gross beta and timeliness asks literally; for the main call nothing filed fixes how origin is judged or what an "increase" is (no sentence on the method).
6. Main answer: an analytical choice (judging origin of increases, with rain gauge, gamma spectrometry and dose record as evidence). No file states the procedure and nothing is flagged as planted. Nearest decider text: Schedule 2 2.2 "of artificial origin" / "Increases of natural origin ... are not notified". The asks (source check, timeliness, gross beta) are rule application from OP-04 s4/s5 and Schedule 2 2.3.

a. harmless, because it covers calendar 2025 only (annual means, data capture), carries no 2026 Q3 value, and says "There were no notifications under Schedule 2 in 2025". Annual means are not answers; MV135 and MV103 share 82.5, coincidence only.
b. harmless, because it names no station, date or value; only the generic duty (station, date, highest ten-minute value), service levels and credits.
c. harmless, because it is the network's own annual report (NUERL MVGN header, prepared Hazel Lambert, approved Cameron Brown, report ref, page footer to the Committee), not a data note. Station codes and names are just its table.
d. none. No file says how natural versus artificial is told apart or how an increase is screened. OP-04 and Schedule 2 only say natural increases are not notified. Spectrometry PDF gives nuclide concentrations without comment.

Realism: minor tells only. All six PDFs have empty Creator and Producer metadata and creation/mod times on exact minutes (e.g. MVJC 14:30:00, spectrometry 14:30:00); the spectrometry PDF header wraps "Sample / r" in its table; PDFs share one letterhead/footer style ("Page n of n", Prepared/Approved block) across the laboratory, committee, radiochemistry and metrology unit, though the two NUERL ones are consistent and the committee/metrology ones differ in styling. Logs: pump log flow is noisy and the ingest log has gaps in batch ids, not too uniform. Otherwise none.
