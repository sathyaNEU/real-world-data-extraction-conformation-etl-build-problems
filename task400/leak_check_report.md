# leak check, task400

**Verdict: REVIEW.** 14 files read, 10 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: register, firmware, rollout, vendor, alerts, window, asserted, windows, braking, driver, critical, location, junction, incident, warning, records, operator, device, reading, notice, report, traffic, exposure, inside, acknowledgement

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `cas_monthly_report_2026-10.pdf`: carries 7 of 11 distinctive words of the committed call: 'Mount Bracken should fund programme C, the collision avoidance alerting review on the haul truck units, for 2027.'
- **REVIEW** `vi_review_terms_2026.docx`: carries 10 of 11 distinctive words of the committed call: 'Mount Bracken should fund programme C, the collision avoidance alerting review on the haul truck units, for 2027.'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `cas_monthly_report_2026-10.pdf`: 5 of 25 stump-paragraph terms appear (alerts, critical, warning, report, acknowledgement); read whether the document names the move
- **REVIEW** `improvement_notice_IN-2026-0417.pdf`: 5 of 25 stump-paragraph terms appear (register, junction, incident, operator, notice); read whether the document names the move
- **REVIEW** `vi_review_terms_2026.docx`: 8 of 25 stump-paragraph terms appear (register, alerts, driver, junction, incident, operator); read whether the document names the move

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
