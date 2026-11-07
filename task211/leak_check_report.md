# leak check, task211

**Verdict: REVIEW.** 18 files read, 75 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: stations, natural, report, decisive, carries, cleared, excess, analyst, screen, annual, increase, radiation, showers, university, export, shipped, physical, quantity, coastal, designation, driver, family, decides, points, gauges

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `air_filter_gamma_spectrometry_2026Q3.pdf`: golden figure 97.6 appears: ...25.8 I-131 8.02 d 364.5 81.5 Cs-134 2.065 y 604.7 97.6 Cs-137 30.05 y 661.7 85.1 Am-241 432.6 y 59.5 35....
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 99.3 appears: ...e Depot 93.4 97.8 MV112 School Playing Field 80.2 99.3 MV142 University Campus 80.7 97.5 MV171 Village G...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 97.5 appears: ...1 Upper Reservoir 109.3 99.4 MV176 Beck Side 78.0 97.5 MV166 Carr Lane Allotments 76.6 97.0 MV103 Grange...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 99.4 appears: ...ransmitter 118.0 98.1 MV231 Upper Reservoir 109.3 99.4 MV176 Beck Side 78.0 97.5 MV166 Carr Lane Allotme...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 98.6 appears: ...MV158 Crossroads 80.9 96.3 MV243 Fell Road Cairn 98.6 97.4 MV207 High Quarry 110.7 98.0 MV135 Moor Road...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 99.5 appears: ...135 Moor Road 82.5 96.4 MV214 Moor Top Mast 123.2 99.5 MV226 Summit Transmitter 118.0 98.1 MV231 Upper R...
- **REVIEW** `mvgn_annual_report_2025.pdf`: golden figure 97.8 appears: ...River Bridge 72.8 98.5 MV184 Riverside Depot 93.4 97.8 MV112 School Playing Field 80.2 99.3 MV142 Univer...
- **REVIEW** `MVJC_service_agreement_schedule2.pdf`: carries 8 of 12 distinctive words of the committed call: 'Yes: notify increases of artificial origin at MV334 Headland Lookout on 6 days (08/07/2026, 17/07/2026, 20/07/2026, 22/0'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `MVGN-OP-04_network_operating_procedure.pdf`: 6 of 25 stump-paragraph terms appear (stations, report, carries, increase, radiation, university); read whether the document names the move
- **REVIEW** `MVJC_service_agreement_schedule2.pdf`: 6 of 25 stump-paragraph terms appear (stations, natural, report, increase, radiation, university); read whether the document names the move
- **REVIEW** `air_filter_gamma_spectrometry_2026Q3.pdf`: 3 of 25 stump-paragraph terms appear (report, analyst, university); read whether the document names the move
- **REVIEW** `mvgn_annual_report_2025.pdf`: 4 of 25 stump-paragraph terms appear (report, annual, radiation, university); read whether the document names the move

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

### Second read, on the FIX_NOW cut

Isolated reader, 2026-11-07 (general-purpose, sonnet, medium), on a fresh copy of prompt.txt and target/ (target.zip sha256 d9bf3d82abf772638c5cc32bbea29f89367744b8dc763586522958d45e63d165), after the spectrometry report's nuclide library, Schedule 2.3's test-mode sentence, the instruments' field names and the source register row were added. Verdict: no leak; the nuclide library lists natural and artificial nuclides together and says nothing of dose rates or origin; question 6 an analytical choice; no realism tell.

# Leak read, task211 (r2). Read and quoted, nothing solved.

1. Decisive step: none states it. Nearest is MVJC_service_agreement_schedule2.pdf 2.2: "notifies ... every increase in the ambient dose equivalent rate recorded at a network station that is of artificial origin, giving the station, the date of the increase and the highest ten-minute value recorded during it. Increases of natural origin, and the Contractor's own source checks, are not notified." That is the ask, not the method for telling origin.

2. No file ranks or scores candidates. The nearest is mvgn_alarm_config_2026Q3.json (per-station "referenceLevel", "investigationLevel", "alertLevel"), which are thresholds and not a ranking, and which MVGN-OP-04 section 3 explains ("30 nSv/h or more above the reference level"). none.

3. Files that only help the analyst: station_code_migration_2025.csv (outstation code to platform code), field_kits_register.csv (kit to source to jig), sealed_source_register_2026.csv (the CS-0583 transfer out and in), check_source_certificates.pdf. Each is a plausible lab record. The raingauge files (northvale_water_raingauges_15min_2026Q3.csv, northvale_water_raingauge_sites.csv) look like an external utility's record and are unlabelled. I found no analyst-addressed note.

4. Nothing reads as the answer. The annual report states "There were no notifications under Schedule 2 in 2025", which is 2025 and not this quarter. No file carries a Q3 detection, station, date or peak.

5. Filed sentences that fix the figures literally:
 - Timeliness, Schedule 2 2.3: "percentage of the quarter's ten-minute intervals for which the platform received the station's value by telemetry within sixty minutes of the end of the interval. A value recorded while the station is in test mode for a source check is the station's value for its interval and counts." This fixes the population as every ten-minute interval in the quarter (the denominator), the timing as received_at within 60 minutes of interval end, and counts test-mode values.
 - Source check, OP-04 s4: "the check reading is the reading with the source less the background. The expected reading is the reading on the source's calibration certificate for the jig used, corrected for the source's decay from the certificate's reference date to the date of the check. A certificate applies from its date of issue ... passes when its check reading is within 10 per cent ... Where a check is repeated at the same visit, the repeat is the check." This fixes the percentage, the certificate choice, the decay correction and the repeat rule.
 - Gross beta, OP-04 s5: "gross beta activity divided by the volume of air drawn through it"; "reported in the quarter in which the filter is taken off". This fixes the population as filters taken off in the quarter, and the quotient.
 - Dose rate, OP-04 s2/s3: interval start in UTC; status T is "not monitoring data"; F has no dose rate; investigation level is reference level plus 30 nSv/h. It fixes data semantics, and does not say how to judge origin.

6. The main answer (artificial origin) is decided by an analytical choice: how to tell an artificial increase from a natural one, using the dose-rate record against the rain gauges, the filter gamma spectrometry and the I-131 and Cs lines. No file states the test. Schedule 2 2.2 only says natural ones are not notified. The mechanical parts (units, UTC, test and fault status, uSv/h against nSv/h, station codes, certificate supersession, volume counter rollovers) are semantics or rule application, but they feed the asks. The only file that discriminates the origin is the spectrometry report, and it gives monthly composites.

## Items

a. Harmless, because the nuclide library is a plain table of half-life, gamma energy and emission probability "as held in the analysis software". It says nothing on dose rates, increases, rain or origin, and reads as a laboratory's own report. The library lists Pb-212, Pb-214, Bi-214 and Ac-228 alongside Cs-134 and Am-241, so it does not point to one nuclide. Mild note: the Cs-137 and I-131 columns are results rows, and all values are "<MDA". Monthly composites may or may not separate any event, but that is a data fact and not a leak.

b. Harmless, because Schedule 2 names no station, date or value, and gives no method for judging origin. It only states that natural increases are not notified (a policy statement) and that test-mode values count for timeliness (a definition the ask needs).

c. Harmless, because the labels read as instrument or system field names: controller export "run_totaliser_at_set_flow_m3" (a totaliser that counts at the set flow, not measured flow) and the AS2 sheet's "Hour meter on/off" with "Volume at set flow (m3)". They are terse and plausible. They do say what the counter is, but as a field name and not as a note to the analyst. Remarks such as "Pump fault 18/08; controller replaced 20/08" are field-engineer remarks.

d. Harmless, because the annual report carries only 2025 annual means and data capture per station, and says "There were no notifications under Schedule 2 in 2025" and "no artificial radionuclide above its minimum detectable activity" for 2025. It gives no Q3 2026 value and does not read as an answer. The 2025 annual means are context for reference levels.

## Realism
none. Possible weak tell: mixed units and mixed codes across the two engineers' sheets (uSv/h and MDV codes against nSv/h and MV codes) and the 15-minute totaliser export are plausible. Consistent author metadata ("Julia French" as creator of the field sheets and visit sheet) is plausible. The raingauge CSV uses a different external column style ("Time (GMT/BST)"), which reads as another organisation's export.
