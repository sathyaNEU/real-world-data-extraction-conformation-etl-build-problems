# leak check, task183

**Verdict: REVIEW.** 14 files read, 23 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: failure, section, quarry, decisive, in-service, second, sutter, asserted, planned, replaced, report, forecast, window, harrow, states, history, architecture, carries, outage, population, forward, sentence, hospital, method, recurrence

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `asset_analytics_extract_notes_2026-10.md`: \bthe model\b x1: ...- Device list in-service dates are blank for devices in service since the model went live (Nov 2014)....

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `2025_annual_reliability_report_sec6_ug_cable.pdf`: carries 7 of 7 distinctive words of the committed call: 'Quarry Hill 21 will have the most failures of the cable itself in 2027, so it is the feeder for the 2027 cable program.'
- **REVIEW** `asset_analytics_extract_notes_2026-10.md`: carries 6 of 7 distinctive words of the committed call: 'Quarry Hill 21 will have the most failures of the cable itself in 2027, so it is the feeder for the 2027 cable program.'

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `2025_annual_reliability_report_sec6_ug_cable.pdf`: 7 of 25 stump-paragraph terms appear (failure, section, quarry, sutter, replaced, report); read whether the document names the move
- **REVIEW** `TVE-RS-04_reliability_reporting_standard_rev6.pdf`: 6 of 25 stump-paragraph terms appear (quarry, sutter, report, harrow, outage, method); read whether the document names the move
- **REVIEW** `asset_analytics_extract_notes_2026-10.md`: 7 of 25 stump-paragraph terms appear (section, quarry, in-service, sutter, replaced, harrow); read whether the document names the move
- **REVIEW** `prompt`: prompt sentence carries two or more stump terms: 'Which of the eight feeders on our underground network will have the most failures of the cable itself in 2027, counting insulation, splice and termination failures on the sections in service at the end of September 2026 '

## 6 ranking artifacts (REVIEW 3, INFO 2)
- **REVIEW** `2025_annual_reliability_report_sec6_ug_cable.pdf`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `TVE-RS-04_reliability_reporting_standard_rev6.pdf`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `feeder_device_list.json`: names 4 of 5 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `asset_analytics_extract_notes_2026-10.md`: names 4 of 5 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `major_event_days_RY2021-RY2025.csv`: names 4 of 5 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 3)
- **REVIEW** `feeder_device_list.json`: columns a generator names and an organisation does not: device_id, device_type, parent_device_id, device_id, device_type, parent_device_id, device_id, device_type
- **REVIEW** `oms_outage_export_2020-10_2026-09.csv`: columns a generator names and an organisation does not: device_id, device_type
- **REVIEW** `oms_restoration_steps_2020-10_2026-09.csv`: columns a generator names and an organisation does not: device_id, restoring_device_id

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 1 file names (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read (pass 1, Sonnet, 2026-10-12)

Q1. none. Nearest hints are field documentation, not the move: the 2025 annual reliability report says counts are
"repaired in the year on the cable in service on the feeder at the time" and that Harrow Road 12's PILC cable was
replaced April to November 2025 with its 2025 count including failures on that cable before it was retired; the
extract notes document the GIS retire-and-replace convention (new cable added as a new section with a predecessor id)
and that a REPL order's completed_date is the day the new cable was energised.

Q2. Partly: the annual report's Table 6.1 gives failures by feeder and year 2021 to 2025 with totals (Quarry Hill 21
8 9 11 9 12 = 49; Harrow Road 12 total 146). It is a correct, labelled history on all cable in service at the time,
not a 2027 ranking; its ordering points to Harrow Road 12, then Mill Lane 7 and Harrow Road 14 (the R0 surface).

Q3. none strictly; nearest is the extract notes file, plausible but unusually thorough (the GIS convention, the OMS
clock difference legacy local against ADMS UTC, connectivity eff_to semantics).

Q4. none. Closest: Table 6.1 shows Quarry Hill 21 and Sutter Park 5 rising while Harrow Road 12, Harrow Road 14 and
Mill Lane 7 decline; no name flagged; the prompt names no feeder.

Q5. TVE-RS-04 governs the three reliability asks (3.3 a customer's own restoration time over five minutes; 3.2
customers served are the connectivity model's metered points on the last day; 2.1 and 2.2 the reliability year in
Eastern local time, ADMS UTC converted; 4.2 own-device outages and a bank outage's customers on the feeder; 5.1 and
5.2 the 2.5 beta method on RY2021 to RY2025, the RY2026 threshold computed; 6.1 CEMIn with major event days included,
under the feeder the point is on at 30 Sep 2026). Nothing in the standard fixes the 2027 failure forecast; the prompt
fixes its population (sections in service at the end of September 2026, INS, SPL and TRM failures, TPD out), whose
literal execution is the counts on current in-service sections only.

REVIEW lines: all harmless except the 2025 report's candidates-beside-numbers line, read as "leak, mild": Table 6.1 is
a historic-count surface (R0, Harrow Road 12) that does not rank the 2027 answer; confirm it is the intended past-
quantity table, correct and labelled. Column-name lines: plausible export names.

Realism tells:
1. The extract notes are unusually thorough and tidy (a table row per file with source system, run date, coverage and
   exact row counts, plus a field glossary); real hand-off notes are thinner.
2. Work-order crew_note values are heavily templated and repeat verbatim dozens of times ("failed splice, repaired",
   "cable faulted, section replaced"), with all-caps duplicates that look injected; a few notes contradict their codes.
3. Feeder-level numbers are too smooth: Table 6.2 circuit miles identical for every feeder in all five years, 6.3
   customers rising in small uniform steps, Sutter Park 9 exactly 1 failure every year, and the cable-in-service total
   never changing despite the PILC replacement note.
4. Synthetic numbering: GIS structure ids (PMT, MH) echo the section id digits; work-order descriptions such as
   "replaced section PMT-24159 to PMT-19113 (265 ft)" follow the same pattern.
5. Identical export formatting across systems (clean ISO dates, consistent column naming, no encoding artefacts, tidy
   OMS cause codes); vault inspector initials very uniform.

Repair (2026-10-12): the five tells fixed in the generator (design note, Build record, stage 4 repair); no graded figure moved; Table 6.1 kept as the labelled past quantity. A second read follows because the documents changed.

## Solver's-eye read (pass 2, Sonnet, 2026-10-12)

1. none. No file names the decisive step. Closest context only: prompt.txt "counting insulation, splice and termination failures on the sections in service at the end of September 2026"; 2025 report sec 6.1 "repaired in the year on the cable in service on the feeder at the time"; notes "A retired section keeps the feeder it was on when it was retired." These define population/cause, not a method.
2. none. The 2025 report Table 6.1 gives past counts by feeder (2021-2025) and totals, but no 2027 expectation or ranking; its raw counts are a surface-read candidate ranking by history only (Harrow Road 12 leads at 146).
3. none clear. Closest: asset_analytics_extract_notes_2026-10.md (a file index with "Things to know", reads like an analyst's hand-off note, plausible from a real asset-management request); wo_cause_repair_codes.csv is a plain code lookup a utility would have. feeder_peak_loading and vault_manhole_inspections read as the stated distractors ("as asked"), not helpers.
4. none. Nothing reads as the answer; the closest figures are the Table 6.1 counts (e.g. "Quarry Hill 21 8 9 11 9 12 49", "Harrow Road 12 ... 146"), which are history, not a call.
5. prompt.txt: "counting insulation, splice and termination failures on the sections in service at the end of September 2026 and leaving out damage done by others". Literal execution: population = GIS sections with STATUS IS at 30 Sep 2026 (retired sections and their history excluded, new REPL sections included), cause in INS/SPL/TRM (TPD and OTH excluded), counted per feeder for calendar 2027. It fixes population and cause set only; the forecasting method (rate by section vintage/insulation etc.) is not fixed by any filed sentence. Report 6.1 ("repaired in the year on the cable in service on the feeder at the time") is a different (as-filed, in-year, then-current cable) basis and would give another number if read literally, but it describes the 2025 filing, not the 2027 ask.
6. Realism, most noticeable first:
 - Major event day list: tmed_saidi_min is identical within each RY (5.79, 7.73...), and RY2021/RY2022 have 10 MEDs each, mostly labelled "Feeder lockout"; plausible for a filing but the heavy repetition of one label reads templated.
 - OMS export: outage_id format differs by source (OMS-yymmdd-nnn vs INC26nnnnn), fine; but cust_minutes in OMS has fractions only on some rows and device_ids are all "FU-31xxxx"/"CB-xxxx" in tidy sequence; mild.
 - Work-order crew_notes are mostly clean and hand-typed-looking, with truncations at ~40 chars ("NEW CABLE PM-2"); realistic. Repeated stock phrases ("cable faulted, section replaced" x18) are slightly templated.
 - 2025 report and TVE-RS-04 are short, tidy and each clause maps neatly to a data-handling issue (e.g. rev 6 "moves the reliability year ... and adds clause 6"); a little too convenient but plausible.
 - cis file: fixed-width padded RATE_CLASS values, uniform 7 columns, meter_ids evenly random 10-digit; fine.
 - Table 6.2 footnote on plat vs GIS lengths and the 2023 re-measurement is a nice realistic touch, not a tell.

Mechanical sweep lines:
- asset_analytics_extract_notes "the model went live (Nov 2014)": harmless, refers to the network model and gives no analytical step.
- 2025 report carries 7 of 7 words of committed call: harmless as far as I can read; the report contains no such sentence and no 2027 statement, only 2021-2025 counts (word overlap is the feeder and cable vocabulary).
- notes 6 of 7 words of committed call: harmless, same reason; it states no call.
- 2025 report 7 of 25 stump terms: harmless, it states counts and the 6.2 note that Harrow Road 12's PILC cable was replaced (context), but does not say how to forecast or which basis to use.
- TVE-RS-04 6 of 25 stump terms: harmless, it is an index/MED/CEMI standard and says nothing about cable failure forecasting.
- notes 7 of 25 stump terms: harmless; the REPL/retired/predecessor handling note is data description (it tells how retirement and predecessor links work), not the move. Marginal: it does explain that a retired section keeps its old feeder, which is a schema fact.
- prompt sentence with stump terms: harmless, it states the estimand's population and cause set; it names no method.
- 2025 report names 4 of 5 candidates beside numbers: harmless, historic counts per feeder, no ranking on the 2027 question.
- TVE-RS-04 names 4 of 5 candidates beside numbers: harmless, only feeder/substation names with circuit voltage; no ranking.
- feeder_device_list.json names 4 of 5 candidates beside numbers: harmless, kva/circuit numbers, no ranking.
- feeder_device_list.json columns device_id, device_type, parent_device_id: harmless, normal for a network-model export.
- oms_outage_export columns device_id, device_type: harmless, normal OMS fields.
- oms_restoration_steps columns device_id, restoring_device_id: harmless, normal for a step table.

Repair after pass 2 (2026-10-12): the major event day list names each lockout's feeder or substation, and the replaced-section crew notes draw from more crews' wordings; both are data files, so no third read; leak.py re-run on the final build (REVIEW, the same lines).

## Determinism repair, 12 October 2026: leak.py rerun

`leak.py task183 --asof 2026-10-06`: REVIEW, the same kinds as the stage 3 and stage 4 sweeps (the organisation's
"the model", the call's words in the report and the notes, the domain's ordinary vocabulary in the documents, ranking
artifacts that rank nothing on 2027, the network model's and the OMS's own column names), plus "second" from the two
new sentences on the Kessler Avenue loop's second feed (report 6.3, extract notes) and Harrow Road 14's ended elbow run (report 6.4). Those sentences name the causes of
Sutter Park 5's 2024 to 2026 failures and Harrow Road 14's 2021 to 2024 run and when they ended, rungs' causes; neither names a section's failure order,
and the readability regex in `generator/checks.py` (recurrence, second failure, failed twice, failure count and the
rest) still finds nothing in the pack.
