# leak check, task400

**Verdict: REVIEW.** 14 files read, 10 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, firmware, vendor, window, rollout, asserted, driver, braking, alerts, critical, location, junction, windows, operator, notice, warning, records, report, acknowledgement, incident, reading, nothing, traffic, dispatch, root-cause

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `cas_monthly_report_2026-10.pdf`: carries 7 of 11 distinctive words of the committed call: 'Mount Bracken should fund programme C, the collision avoidance alerting review on the haul truck units, for 2027.'
- **REVIEW** `vi_review_terms_2026.docx`: carries 10 of 11 distinctive words of the committed call: 'Mount Bracken should fund programme C, the collision avoidance alerting review on the haul truck units, for 2027.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `cas_monthly_report_2026-10.pdf`: 6 of 25 stump-paragraph terms appear (alerts, critical, warning, report, acknowledgement, dispatch); read whether the document names the move
- **REVIEW** `improvement_notice_IN-2026-0417.pdf`: 5 of 25 stump-paragraph terms appear (register, junction, operator, notice, incident); read whether the document names the move
- **REVIEW** `vi_review_terms_2026.docx`: 8 of 25 stump-paragraph terms appear (register, driver, alerts, junction, operator, notice); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read (round 1, target.zip 36837e7e; round 2 pending on 954bd646)

1. Decisive step: none. vi_review_terms_2026.docx 3.2 says "The review names the driver that accounts for most of that rise, and the committee funds the programme in section 4 that answers that driver." That states the goal, not the method. Nothing names which driver or how to apportion the rise.
2. No file ranks or scores the programmes. The five programmes A to E (docx section 4) are only listed. cas_monthly_report_2026-10.pdf shows monthly alert rates but does not rank anything.
3. None exists only to help. The improvement notice and the terms of reference are context. The PDF report is a vendor monthly report. Nothing is a worked helper.
4. None reads as the answer. The nearest are the October 2026 row of cas_monthly_report_2026-10.pdf ("Oct 2026 ... 41.0") and the programme list. Neither gives a result.
5. Filed sentences that fix the population or unit: docx 2.1 "A vehicle interaction incident is a collision between two vehicles, or a significant potential incident between two vehicles, entered in the site incident register under classification VI-COL or VI-SPI. Each register entry is one incident, counted in the month in which it occurred, Western Australian time." Also 2.2 "A haul truck is one of the mine's rear dump trucks carrying a DT fleet number. A light vehicle is any vehicle on the light vehicle register." and 3.1 "The review explains the rise in vehicle interaction incidents in July to October 2026 against July to October 2025." Read literally, these fix the incident count as register entries with those two classifications, binned by WA-local month, over Jul-Oct 2026 vs Jul-Oct 2025. No sentence fixes how the driver is apportioned. I computed nothing.
6. The main answer is decided by an analytical choice (how to attribute the rise to a driver, from the sources), not by one field reading, a stated rule or a planted item. Nothing filed says how to apportion. The closest text is docx 3.2 "names the driver that accounts for most of that rise". Definitions in 2.1 and 2.2 and the programme texts are context. Caveat: the pack has nothing visibly planted. The PDF report states "All haul truck units are on the current release" and "Hardware replacements: 5 haul truck units over the period", which could be read as a distractor or a fact to be checked against the register and firmware sheet. It is not an official decoy that blesses a wrong answer, and it does not name any driver.
7. Terms in the prompt that read two ways:
   - Month and time basis: "July to October" could be read in UTC or WA time. docx 2.1 settles incidents ("counted in the month in which it occurred, Western Australian time"). Settles incident counts only. For the gate reads, the speeding events and the trips, no filed sentence names the time basis (the register xlsx "Occurred" is local, the CAS parquet is UTC by its column names, FMS trigger_time and gate read_time carry no zone). Possible gap for the extra figures.
   - "Incident counts": settled by docx 2.1 (VI-COL or VI-SPI only; other classes excluded).
   - "Light-vehicle trips into the pits": which readers count as pit entry (NG-1, NG-2, SG-IN, the OUT readers), direction IN, and repeated reads of one vehicle. No filed sentence defines a trip or which readers are pit gates, and I found no explicit sentence in the pack. direction=IN exists as a column, and site_location_codes.csv does not list readers. Both readings are defensible: any IN read, or only reads inside a shift or de-duplicated per visit. Light vehicle is settled by docx 2.2 (on light_vehicle_register.csv).
   - "Collision avoidance tag the gate did not detect": settled only in the data by blank cas_tag on the gate read. Whether a tag that reads but does not match the device register (cas_device_register xlsx, installed/removed dates) counts as not detected is not stated.
   - "Times haul trucks went over the speed limit in force there": the limit in force depends on the date, via haul_road_speed_limits.csv effective_from (NRP changes 2026-06-09, SRP changes 2026-08-18). The word "in force" settles that the dated limit applies. Whether an event is the trigger OVERSPEED row or a sustained run in the speed trace is not stated, and fms trigger and limit_kmh columns are also in the data.
   - "more than 5 km/h over it": strictly greater is settled by the word "more than"; the peak is over the event window is implied by "peaked", but the gps_fix NONE and missing-speed rows are not addressed by any filed sentence.
   - "Pit ramp": NRP and SRP are the pit ramps by code and name in site_location_codes.csv. The North ramp junction (NRJ) could be mistaken for a ramp, a reading the prompt does not settle beyond the location file.
   - "Every count is a whole number" settles rounding only.

## Mechanical sweep items
- cas_monthly_report_2026-10.pdf: harmless as a leak, as far as I can read. It is a vendor monthly alert table (a real-looking report with a preparer line). It names no programme and no driver. Shared numbers with the write-up are monthly alert counts and rates, which are context from the vendor's side and would be recomputable from the CAS events parquet. Distinctive words overlap because the topic is collision avoidance alerts. Its two lines ("current release", "Hardware replacements: 5") are context. Minor note: the Sep 2025 row has 32 units against 30 on either side, a plausible-looking vendor quirk.
- vi_review_terms_2026.docx: harmless. It is the client's terms of reference. It lists programmes and definitions and states no result. The overlap with the committed call is because the programmes and the call share vocabulary. It carries no hidden text, comments or tracked changes; the properties show author Shari Jefferson and a thumbnail.jpeg, which is ordinary Word output.

## Generated look
- incident_register xlsx: 626 rows with 583 distinct descriptions, and VI descriptions come from a small set of templated sentences filled with fleet numbers and distances (for example the "LV X entered the haul road in front of loaded X" sentence appears 31 times). That reads templated but is plausible for an incident-register free-text field. Non-VI rows repeat "isolation lock missing" and "graze to knuckle" templates.
- cas_device_register xlsx: the earliest rows share the same Installed date (2023-05-02) and the firmware sheet has the same 2024-09-30 02:10 applied time for the first block (batch rollouts, plausible). dispatch_shift_summary and the dust CSV look like regular exports. The claim in the prompt about vi_programme_paper_2027.docx and vi_workings_2026.xlsx refers to files absent from target/; they are presumably the deliverables to be produced, not the pack, so that is not a leak. If they are meant to ship in the pack, they are missing.

## Solver's-eye read (round 1, target.zip 36837e7e)

1. Decisive step: none. vi_review_terms_2026.docx 3.2 says "The review names the driver that accounts for most of that rise, and the committee funds the programme in section 4 that answers that driver." That states the goal, not the method. Nothing names which driver or how to apportion the rise.
2. No file ranks or scores the programmes. The five programmes A to E (docx section 4) are only listed. cas_monthly_report_2026-10.pdf shows monthly alert rates but does not rank anything.
3. None exists only to help. The improvement notice and the terms of reference are context. The PDF report is a vendor monthly report. Nothing is a worked helper.
4. None reads as the answer. The nearest are the October 2026 row of cas_monthly_report_2026-10.pdf ("Oct 2026 ... 41.0") and the programme list. Neither gives a result.
5. Filed sentences that fix the population or unit: docx 2.1 "A vehicle interaction incident is a collision between two vehicles, or a significant potential incident between two vehicles, entered in the site incident register under classification VI-COL or VI-SPI. Each register entry is one incident, counted in the month in which it occurred, Western Australian time." Also 2.2 "A haul truck is one of the mine's rear dump trucks carrying a DT fleet number. A light vehicle is any vehicle on the light vehicle register." and 3.1 "The review explains the rise in vehicle interaction incidents in July to October 2026 against July to October 2025." Read literally, these fix the incident count as register entries with those two classifications, binned by WA-local month, over Jul-Oct 2026 vs Jul-Oct 2025. No sentence fixes how the driver is apportioned. I computed nothing.
6. The main answer is decided by an analytical choice (how to attribute the rise to a driver, from the sources), not by one field reading, a stated rule or a planted item. Nothing filed says how to apportion. The closest text is docx 3.2 "names the driver that accounts for most of that rise". Definitions in 2.1 and 2.2 and the programme texts are context. Caveat: the pack has nothing visibly planted. The PDF report states "All haul truck units are on the current release" and "Hardware replacements: 5 haul truck units over the period", which could be read as a distractor or a fact to be checked against the register and firmware sheet. It is not an official decoy that blesses a wrong answer, and it does not name any driver.
7. Terms in the prompt that read two ways:
   - Month and time basis: "July to October" could be read in UTC or WA time. docx 2.1 settles incidents ("counted in the month in which it occurred, Western Australian time"). Settles incident counts only. For the gate reads, the speeding events and the trips, no filed sentence names the time basis (the register xlsx "Occurred" is local, the CAS parquet is UTC by its column names, FMS trigger_time and gate read_time carry no zone). Possible gap for the extra figures.
   - "Incident counts": settled by docx 2.1 (VI-COL or VI-SPI only; other classes excluded).
   - "Light-vehicle trips into the pits": which readers count as pit entry (NG-1, NG-2, SG-IN, the OUT readers), direction IN, and repeated reads of one vehicle. No filed sentence defines a trip or which readers are pit gates, and I found no explicit sentence in the pack. direction=IN exists as a column, and site_location_codes.csv does not list readers. Both readings are defensible: any IN read, or only reads inside a shift or de-duplicated per visit. Light vehicle is settled by docx 2.2 (on light_vehicle_register.csv).
   - "Collision avoidance tag the gate did not detect": settled only in the data by blank cas_tag on the gate read. Whether a tag that reads but does not match the device register (cas_device_register xlsx, installed/removed dates) counts as not detected is not stated.
   - "Times haul trucks went over the speed limit in force there": the limit in force depends on the date, via haul_road_speed_limits.csv effective_from (NRP changes 2026-06-09, SRP changes 2026-08-18). The word "in force" settles that the dated limit applies. Whether an event is the trigger OVERSPEED row or a sustained run in the speed trace is not stated, and fms trigger and limit_kmh columns are also in the data.
   - "more than 5 km/h over it": strictly greater is settled by the word "more than"; the peak is over the event window is implied by "peaked", but the gps_fix NONE and missing-speed rows are not addressed by any filed sentence.
   - "Pit ramp": NRP and SRP are the pit ramps by code and name in site_location_codes.csv. The North ramp junction (NRJ) could be mistaken for a ramp, a reading the prompt does not settle beyond the location file.
   - "Every count is a whole number" settles rounding only.

## Mechanical sweep items
- cas_monthly_report_2026-10.pdf: harmless as a leak, as far as I can read. It is a vendor monthly alert table (a real-looking report with a preparer line). It names no programme and no driver. Shared numbers with the write-up are monthly alert counts and rates, which are context from the vendor's side and would be recomputable from the CAS events parquet. Distinctive words overlap because the topic is collision avoidance alerts. Its two lines ("current release", "Hardware replacements: 5") are context. Minor note: the Sep 2025 row has 32 units against 30 on either side, a plausible-looking vendor quirk.
- vi_review_terms_2026.docx: harmless. It is the client's terms of reference. It lists programmes and definitions and states no result. The overlap with the committed call is because the programmes and the call share vocabulary. It carries no hidden text, comments or tracked changes; the properties show author Shari Jefferson and a thumbnail.jpeg, which is ordinary Word output.

## Generated look
- incident_register xlsx: 626 rows with 583 distinct descriptions, and VI descriptions come from a small set of templated sentences filled with fleet numbers and distances (for example the "LV X entered the haul road in front of loaded X" sentence appears 31 times). That reads templated but is plausible for an incident-register free-text field. Non-VI rows repeat "isolation lock missing" and "graze to knuckle" templates.
- cas_device_register xlsx: the earliest rows share the same Installed date (2023-05-02) and the firmware sheet has the same 2024-09-30 02:10 applied time for the first block (batch rollouts, plausible). dispatch_shift_summary and the dust CSV look like regular exports. The claim in the prompt about vi_programme_paper_2027.docx and vi_workings_2026.xlsx refers to files absent from target/; they are presumably the deliverables to be produced, not the pack, so that is not a leak. If they are meant to ship in the pack, they are missing.

## Solver's-eye read (round 2, target.zip 954bd646)

Scope note: prompt.txt names vi_programme_paper_2027.docx and vi_workings_2026.xlsx. Neither is in target/. I read all 14 files that are there. I computed no figures.

1. Decisive step: none. No file or sentence names it.
   - vi_review_terms_2026.docx 3.2 says "The review names the driver that accounts for most of that rise, and the committee funds the programme in section 4 that answers that driver." That is the task's question restated, not a method.
   - improvement_notice_IN-2026-0417.pdf says "Identify the cause of the increase in vehicle interaction incidents at the mine." Same: the question, not the step.
   - The terms never say how to attribute the rise to drivers.

2. Ranking or scoring of the candidates: none.
   - The terms list programmes A to E with one neutral "Answers ..." clause each.
   - cas_monthly_report_2026-10.pdf is a per-month fleet table with no ranking and no verdict.
   - Nothing scores or orders the programmes.

3. Files that exist only to help the analyst: none.
   - site_location_codes.csv and haul_road_speed_limits.csv are small lookups but read as ordinary site reference data.
   - light_vehicle_register.csv is an ordinary register.
   - The distractor-type files (dust PM10, road maintenance log, dispatch summary, CAS device register, firmware sheet, CAS monthly report) look like real exports.

4. Answer-like figure or name: none.
   - The monthly report's alerts per 100 h rise from 38 to 41 in Jun 2026. That is context, not a conclusion.
   - Programme C ("Collision avoidance alerting review") is the nearest the terms come to echoing a candidate, but all five are listed neutrally.
   - The notice names "the North ramp junction" in its grounds (a collision on 7 July 2026). That favours programme B only as a lead, not as an answer, and it sits in a regulator's grounds.

5. Filed sentence that fixes the computation or population:
   - vi_review_terms_2026.docx 2.1: "A vehicle interaction incident is a collision between two vehicles, or a significant potential incident between two vehicles, entered in the site incident register under classification VI-COL or VI-SPI. Each register entry is one incident, counted in the month in which it occurred, Western Australian time." Literal result: the population is VI-COL plus VI-SPI register rows, counted by AWST month.
   - 2.2: "A haul truck is one of the mine's rear dump trucks carrying a DT fleet number. A light vehicle is any vehicle on the light vehicle register."
   - 3.1: "The review explains the rise in vehicle interaction incidents in July to October 2026 against July to October 2025." This fixes the window and comparison.
   - 3.2 files the estimand (the driver accounting for most of the rise) without filing how to attribute it.
   - prompt.txt: "A trip is one vehicle entering a pit, and a time over the limit is one continuous run above it."
   - The register's classifications are only VI-COL and VI-SPI in the VI family. Some VI rows involve non-LV, non-DT plant (WC, GR, DZ). That is covered by 2.1 ("between two vehicles") and 2.2.

6. What decides the main answer: an analytical choice. Which driver accounts for most of the rise needs a rise decomposed across candidate mechanisms using the gate reads, CAS tag detection, speed windows and the register. Nothing filed gives that procedure. The terms give only the estimand, in 3.1 and 3.2.
   - The inputs include several mess layers (UTC against AWST, a limit change stamped retroactively on older event windows, a regenerated register).
   - The programmes map to candidate drivers, so choosing among them takes judging the evidence.
   - It does not turn on one field, one unit or a stated rule, and I see nothing planted.
   - The one thing that looks like a trap: fms_event_windows limit_kmh shows NRP 32 and SRP 35 on every row back to 2025-01. haul_road_speed_limits.csv shows NRP 40 until 2026-06-09 and SRP 40 until 2026-08-18. This is layer 1 mess. It bears on the ask figures (over-the-limit counts), not on the call.

7. Ask-figure terms that read two ways:
   - "Incident counts": settled by terms 2.1 (classes VI-COL and VI-SPI, month of occurrence, AWST). The register's Occurred column is not labelled with a zone in the header, which is the only open point. Terms 2.1 says "Western Australian time", which settles it.
   - "Light-vehicle trips into the pits": settled by prompt.txt "A trip is one vehicle entering a pit". The gate reads carry IN and OUT directions and several readers (NG-1, NG-2, SG-IN, NG-OUT, SG-OUT), plus repeated plates, so counting only IN reads is the defensible reading. Terms 2.2 settles that a light vehicle is anything on light_vehicle_register.csv. Some plates in the gate reads are not on that register, so that definition filters them.
   - "No tag detected": the reads carry a cas_tag column with nulls. The prompt says "vehicles whose collision avoidance tag the gate did not detect", which reads as a null cas_tag. No further sentence handles the case where the tag is read but is not the tag the register assigns. cas_device_register_2026-10-31.xlsx gives the asset-to-tag map. I see no filed sentence that picks between "tag blank" and "tag differs from registered", and a careful solver could defend either. Possible ambiguity, low severity.
   - "Times over the speed limit in force": the speed-limit file's effective_from column settles which limit applies. The event windows' limit_kmh column is stamped with the current limit, so it conflicts. The prompt's phrase "in force there" plus the limits file settles it. "A time over the limit is one continuous run above it" settles the event grain, but event_ref windows are short samples, and no sentence says how to judge the run from the windows.
   - "More than 5 km/h over": strictly greater, from the prompt. It does not say whether this is peak speed or any sample. "Peaked" in the prompt settles it as the peak.
   - "Each month": the event windows use trigger_time_awst and the CAS alert events use UTC. The prompt's months and the terms' "Western Australian time" settle the AWST reading.

## Mechanical sweep items

- cas_monthly_report_2026-10.pdf: harmless. It is a vendor's generic monthly fleet table (alert rates, acknowledgement) and shares words like "collision avoidance" and "haul truck" with the call only because those are the domain's nouns. It names no cause, ranks nothing, and sets no decision. Its Fleet status line ("All haul truck units are on the current release") is neutral context.
- vi_review_terms_2026.docx: harmless. It is the governing document that must name the programmes and the definitions, so it must share the call's words. It states the question, the definitions and the neutral candidate list, with no weighting or method. I flag one thing for the author's judgment, not as a leak: programme C's "Answers the alerts the haul trucks' collision avoidance units give their operators" is worded slightly more specifically than the others, and B names a specific junction. Both stay within neutral description.

## Generated-looking check

- incident_register_2025-01_2026-10.xlsx: the descriptions read as authored. They vary in length (31 to 190 characters) and carry optional suffixes ("Supervisor notified.", "Photos taken and investigation opened."). They use one clause template per scenario with substituted slots. Some rows are deliberately terse ("Near miss DT454 and 1SVH168, South haul road."). Only 8 of 617 descriptions are exact duplicates, and the repeats are the generic injury lines (e.g. a laceration line appearing 3 times). The incident numbers rise monotonically with gaps. This is plausible for a real register and I see no tell.
- Weak tells: the monthly report's per-month counts and its 30 units reporting with 30 flat for many months are regular, and light_vehicle_register.csv is uniform (97 rows, four Toyota variants). Neither is a leak.
- No hidden sheets or odd document properties found. The authors/creators are plausible (Halcyon Portal, Shari Jefferson, Mines Safety Inspectorate).
