## Tags

**Domain:** Education & Learning Sciences, psychometrics (generalizability theory: how many stations Callowfield's 2027 final OSCE needs for its total mark to rank candidates with a reliability of 0.80 on a blueprint that draws the same number of stations from each of four skill domains, each candidate meeting one examiner a station in three parallel circuits).
**Analytical objective:** Descriptive & Distribution Analysis (how the variance of the 2026 sitting's station marks divides among candidates, their strengths by domain, the stations within each domain, the examiners and the residual, recombined for the blueprint and the way 2027 will examine).

## 1. Final Recommendation

**Set the 2027 final OSCE at 13 stations.**
On the blueprint, which draws the same domains every year, with one examiner a station in each of three circuits, the total mark ranks candidates with a reliability of 0.81 at 13 stations and 0.79 at 12, against the 0.80 standard. Not 16 stations, which a decision study treating the stations as drawn from one undivided bank asks for, because it books each candidate's strength in a domain as error when every form carries the same domains. Not 12 stations, which one examiner's 2026 marks support (0.80 on the lead examiners' marks, 0.81 on the second examiners'), because in 2026 the same two examiners marked every candidate at a station, while in 2027 different candidates meet different examiners and the stringency variance of 1.06 is error. Not the 2026 sitting's own reliability of 0.84 over 12 stations, which rests on two examiners' marks averaged at every station.

## 2. Critical Components

1. Variance among candidates in one examiner's station mark (marks out of 20, squared): **0.92**; candidate by domain: **0.76**, part of what the total mark measures on the fixed blueprint
2. Error in the 2027 total: case specificity within domain **1.36**, examiner within station (stringency) **1.06**, residual **1.08**
3. Reliability of the total mark under the 2027 arrangement: **0.81** at 13 stations, **0.79** at 12

## 3. Step-by-Step Solution

1. Took each examiner's mark for each candidate at each station from osce2026_marks_export.csv as policy 3.2 defines it (points scored over the points the available items carry, out of 20, an item marked not applicable not available), station 7's item 14 removed from every candidate's mark (policy 3.4, the minutes, item 2), and day 2's case codes and staff numbers matched to day 1's stations and badges through osce2026_station_sheet.xlsx and osce2026_examiner_allocation.xlsx: 84 candidates, 12 stations (three from each domain on the station sheet), the same two examiners at each station.
2. Split the variance of those marks by expected mean squares on the balanced design of candidates crossed with examiners nested in stations nested in domains: candidate 0.92, candidate by domain 0.76, domain 0.22, station within domain 0.49, candidate by station within domain 1.36, examiner within station 1.06, residual 1.08.
3. Policy 4.2 draws the same number of stations from each of the four domains every year, the remainder in its order, so the domains are fixed in every form and a candidate's strength in a domain is part of what the total measures (policy 4.3), weighted by the domains' shares of the stations; under final_osce_2027_delivery_plan.docx each candidate meets one examiner a station and every circuit runs the same stations, so the stringency is error and station and domain difficulty are not.
4. Reliability at n stations is (0.92 + S x 0.76) / (0.92 + S x 0.76 + (1.36 + 1.06 + 1.08) / n), S the sum of the squared domain shares of the n stations: 0.79 at 12 stations rising to 0.85 at 18, 13 the fewest reaching 0.80 within the eighteen rooms.
5. Counted, per blueprint domain, the cases in case_bank_export_2026-11-30.xlsx that policy 4.4 allows in May 2027: Active or Active - edits pending, last reviewed on or after 11 May 2024 (dates typed in the old bank read day first), and not set at a 2025 or 2026 sitting in case_usage_history_2021_2026.csv; SP and SP and task trainer cases need a simulated patient.
6. A CV-25 record above version 1 is a record re-created at the November 2025 cut-over (casebank_migration_report_2025-11.pdf, section 2; a case written in the new bank starts at version 1, the bank's Fields tab), whatever its title or review date: it keeps the sittings of the retired record of the same domain, specialty and resources at the version before, never those of another retired record of its specialty or of a retired case of the same title; cases that can be set and of them needing a simulated patient: History taking 13 and 13, Physical examination 16 and 13, Communication 14 and 14, Procedural skills 14 and 6.
7. Counted, per site and session, the examiners eligible at the allocation on 7 December 2026 (final_osce_2027_delivery_plan.docx; policy 5.2: Active on examiner_register_2026-11-30.xlsx, an eligible grade, and the examiner training or a refresher attended on or after 7 December 2023 in examiner_training_attendance_2021_2026.csv, a refresher booked and not attended not counting) whose latest response in examiner_availability_2027_responses.csv, matched by email or else by name without titles, accents or punctuation, offers that site and session.
8. Training rows under hospital (H) or Fennabeg (F) staff numbers, signed in at the hospital's and Fennabeg's own sessions, are their own staff's: they belong to the register examiner of that name on the hospital's staff (a Callowfield academic may hold a hospital post) or Fennabeg's, never to a GP trainer in general practice who shares the name, so their attendance counts: Clinical Skills Centre 28, 28, 29, 30; Simulation Suite 33, 33, 34, 34; Clinical Skills Unit 22, 24, 21, 19; set the 2027 final OSCE at 13 stations.

## 4. Deliverable Answers

### osce2027_station_plan.xlsx

1. Stations the 2027 final OSCE needs for its total mark to meet the 0.80 standard: 13
2. Reliability of the total mark under the 2027 arrangement, by number of stations (two decimals):
   - 12 stations: 0.79
   - 13 stations: 0.81
   - 14 stations: 0.82
   - 15 stations: 0.83
   - 16 stations: 0.84
   - 17 stations: 0.84
   - 18 stations: 0.85
3. Cases in the bank that can be set in May 2027; of them, cases needing a simulated patient:
   - History taking: 13; 13
   - Physical examination: 16; 13
   - Communication: 14; 14
   - Procedural skills: 14; 6
4. Examiners eligible at the December allocation who offered each session:
   - Clinical Skills Centre, Callowfield: Tuesday morning 28, Tuesday afternoon 28, Wednesday morning 29, Wednesday afternoon 30
   - Simulation Suite, Callowfield University Hospital: Tuesday morning 33, Tuesday afternoon 33, Wednesday morning 34, Wednesday afternoon 34
   - Clinical Skills Unit, Fennabeg Clinical School: Tuesday morning 22, Tuesday afternoon 24, Wednesday morning 21, Wednesday afternoon 19

### osce2027_reliability_chart.png

1. Line chart of the total mark's reliability at 12 to 18 stations, with the 0.80 standard and the eighteen-room limit drawn and 13 stations marked at 0.81.
