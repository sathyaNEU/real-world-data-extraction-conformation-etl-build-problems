## Tags

**Domain:** Education & Learning Sciences, psychometrics (generalizability theory: how many stations Callowfield's 2027 final OSCE needs for its total mark to rank candidates with a reliability of 0.80 when each candidate meets one examiner a station in three parallel circuits).
**Analytical objective:** Descriptive & Distribution Analysis (how the variance of the 2026 sitting's station marks divides among candidates, stations, examiners and the residual, recombined for the way 2027 will examine).

## 1. Final Recommendation

**Set the 2027 final OSCE at 15 stations.**
With one examiner a station in each of the three circuits, the total mark ranks candidates with a reliability of 0.804 at 15 stations and 0.793 at 14, against the 0.80 standard. Not 12 stations, where one examiner's 2026 marks reach 0.816 with the examiner's stringency left out of the error, as the 2026 sitting allowed because the same two examiners marked every candidate at a station; in 2027 different candidates meet different examiners at a station, so the stringency variance of 0.960 is error. Not the 2026 sitting's own reliability of 0.845 over 12 stations, which rests on two examiners' marks averaged at every station. Not more stations than the eighteen rooms hold, which an absolute coefficient asks for by counting station difficulty as error, although every circuit runs the same stations.

## 2. Critical Components

1. Variance among candidates in one examiner's station mark (marks out of 20, squared): **1.010**
2. Examiner within station (stringency): **0.960**, error in 2027 with candidate by station **1.704** and residual **1.033**
3. Reliability of the total mark under the 2027 arrangement: **0.804** at 15 stations, **0.793** at 14

## 3. Step-by-Step Solution

1. Took each examiner's mark for each candidate at each station from osce2026_marks_export.csv as policy 3.2 defines it (points scored over the points the available items carry, out of 20, an item marked not applicable not available), station 7's item 14 removed from every candidate's mark (policy 3.4, the minutes, item 2), and day 2's case codes and staff numbers matched to day 1's stations and badges through osce2026_station_sheet.xlsx and osce2026_examiner_allocation.xlsx: 84 candidates, 12 stations, the same two examiners at each station.
2. Split the variance of those marks by expected mean squares on the balanced candidates by examiners-within-stations design: candidates 1.010, stations 1.364, candidate by station 1.704, examiner within station 0.960, residual 1.033.
3. Read the 2027 arrangement from final_osce_2027_delivery_plan.docx: one examiner a station in each of three circuits, examiners allocated by site and session, and the same stations in every circuit, so different candidates meet different examiners at a station and an examiner's stringency is error in ranking them (policy 4.3), while a station's difficulty, common to every candidate, is not.
4. Reliability of the total mark at n stations is 1.010 / (1.010 + (1.704 + 0.960 + 1.033) / n): 0.766 at 12 stations rising to 0.831 at 18, with 0.793 at 14 and 0.804 at 15, so 15 is the fewest stations meeting 0.80 within the eighteen rooms.
5. Counted, per blueprint domain, the cases in case_bank_export_2026-11-30.xlsx that policy 4.4 allows in May 2027: Active or Active - edits pending, last reviewed on or after 11 May 2024 (dates typed in the old bank read day first), and not set at a 2025 or 2026 sitting in case_usage_history_2021_2026.csv, a record re-created at the November 2025 cut-over (a CV-25 code carrying a retired record's title, domain, specialty, resources and review date, one version on; casebank_migration_report_2025-11.pdf, section 2) keeping its retired record's sittings; SP and SP and task trainer cases need a simulated patient.
6. Counted, per site and session, the examiners eligible at the 7 December 2026 allocation (policy 5.2: Active on examiner_register_2026-11-30.xlsx, an eligible grade, and the examiner training or a refresher attended on or after 7 December 2023, attendance read from examiner_training_attendance_2021_2026.csv, a refresher booked and not attended not counting) whose latest response in examiner_availability_2027_responses.csv, matched to the register by email or else by name without titles, accents or punctuation, offers that site and session.
7. Set the 2027 final OSCE at 15 stations.

## 4. Deliverable Answers

### osce2027_station_plan.xlsx

1. Stations the 2027 final OSCE needs for its total mark to meet the 0.80 standard: 15
2. Reliability of the total mark under the 2027 arrangement, by number of stations (three decimals):
   - 12 stations: 0.766
   - 13 stations: 0.780
   - 14 stations: 0.793
   - 15 stations: 0.804
   - 16 stations: 0.814
   - 17 stations: 0.823
   - 18 stations: 0.831
3. Cases in the bank that can be set in May 2027; of them, cases needing a simulated patient:
   - History taking: 18; 18
   - Physical examination: 24; 18
   - Communication: 19; 19
   - Procedural skills: 18; 7
4. Examiners eligible at the 7 December 2026 allocation who offered each session:
   - Clinical Skills Centre, Callowfield: Tuesday morning 24, Tuesday afternoon 27, Wednesday morning 28, Wednesday afternoon 25
   - Simulation Suite, Callowfield University Hospital: Tuesday morning 28, Tuesday afternoon 22, Wednesday morning 34, Wednesday afternoon 28
   - Clinical Skills Unit, Fennabeg Clinical School: Tuesday morning 34, Tuesday afternoon 30, Wednesday morning 26, Wednesday afternoon 30

### osce2027_reliability_chart.png

1. Line chart of the total mark's reliability at 12 to 18 stations, with the 0.80 standard and the eighteen-room limit drawn and 15 stations marked at 0.804.
