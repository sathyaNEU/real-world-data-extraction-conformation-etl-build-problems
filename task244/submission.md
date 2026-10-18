## Tags

**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error adjustment).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**No: the 2027 annual flows tables cannot go out without the classification-error warning; 13 of the 24 district rates carry it, the job-finding rates of Industrial Corridor, Cocoa Belt East, Cocoa Belt West, Northern Savanna, Central Hills and Creeks, and the job-loss rates of Lagoon Coast, Cocoa Belt East, Cocoa Belt West, Northern Savanna, Central Hills, River Basin and University Towns.**

The deciding figure is each rate's share of counted moves that are not real moves, read through the reconciled reinterview's classification error at both quarters of each pair: 45.1 to 69.0 per cent for the 13 warned rates against the one-third line, 11.9 to 23.2 per cent for the other 11. Not the reinterview's predictive values of the two recorded statuses multiplied, which puts every rate at 18.1 per cent and warns none; not the chances that each status is recorded correctly multiplied, which puts every rate at 17.0 per cent and warns none.

## 2. Critical Components

1. The reinterview's classification error, 15,221 persons reinterviewed within the window over 2026Q4 to 2027Q4: recorded correctly **98.82%** of the employed, **83.96%** of the unemployed and **97.73%** of those outside the labour force; an unemployed person recorded employed **5.87%** and outside the labour force **10.17%**, an employed person recorded unemployed **0.44%**, a person outside the labour force recorded unemployed **1.40%**.
2. Each rate's share of counted moves that are not real moves: **45.1 to 69.0%** for the 13 warned rates, **11.9 to 23.2%** for the other 11.

## 3. Step-by-Step Solution

1. Read Table F1 of elfs_2027_annual_flows_tables.xlsx: each district's persons in each pair of statuses in two consecutive quarters, the average of the four quarter pairs (methodology note, section 7).
2. Tabulated the 15,221 persons in elfs_reinterview_results_2026q4_2027q4.csv by reconciled status and the status the original interview recorded, each person once and unweighted (reinterview protocol, sections 4 and 7): the chance each true status is recorded as each status, carried unrounded into every share.
3. For each district, took that classification error out of Table F1 at both quarters of each pair (each quarter's interview by a different interviewer, methodology note section 3) to get the true flows.
4. For each rate, the share of counted moves that are not real moves is one less the true flow times the two statuses' chances of a correct record, over the counted flow (methodology note, section 8.1): 13 rates at a third or more.
5. Match rates: each person interviewed in a dwelling due another visit, found at the dwelling's next visit as section 8.2 files; each person once, so the 2027Q2 records of 14 May received again under the dwelling's next household numbers (every field but the household number repeated) and Market Towns area 5's batch received twice count once; districts as from 1 April 2027 (elfs_district_gazetteer_2027.csv).
6. Reinterview timing: each 2027 person's own interview date to the date of the visit that completed the household's reinterview, from visit_start in elfs_reinterview_fieldwork_log_2026q4_2027q4.csv (from each tablet's app update, taken at a Friday sync between 18 June and 9 July 2027, the log's call date is the next Friday sync); section 8.3.
7. The tables carry the warning on 13 of the 24 rates.

## 4. Deliverable Answers

### elfs_2027_flows_quality.xlsx

1. Each rate's share of counted moves that are not real moves (per cent) and the warning, 24 rows:
   - Metropolitan Core (D01) job-finding: 13.4, no warning
   - Metropolitan Core (D01) job-loss: 15.2, no warning
   - Metropolitan Fringe (D02) job-finding: 11.9, no warning
   - Metropolitan Fringe (D02) job-loss: 14.6, no warning
   - Lagoon Coast (D03) job-finding: 19.3, no warning
   - Lagoon Coast (D03) job-loss: 45.1, warning
   - Industrial Corridor (D04) job-finding: 58.6, warning
   - Industrial Corridor (D04) job-loss: 22.0, no warning
   - Cocoa Belt East (D05) job-finding: 60.8, warning
   - Cocoa Belt East (D05) job-loss: 69.0, warning
   - Cocoa Belt West (D06) job-finding: 50.7, warning
   - Cocoa Belt West (D06) job-loss: 62.1, warning
   - Northern Savanna (D07) job-finding: 61.1, warning
   - Northern Savanna (D07) job-loss: 60.7, warning
   - Central Hills (D08) job-finding: 68.4, warning
   - Central Hills (D08) job-loss: 67.1, warning
   - River Basin (D09) job-finding: 20.3, no warning
   - River Basin (D09) job-loss: 48.9, warning
   - Creeks (D10) job-finding: 46.7, warning
   - Creeks (D10) job-loss: 23.2, no warning
   - Market Towns (D11) job-finding: 15.5, no warning
   - Market Towns (D11) job-loss: 17.7, no warning
   - University Towns (D12) job-finding: 17.3, no warning
   - University Towns (D12) job-loss: 47.2, warning
2. Each district's match rate (per cent) and the persons it is based on, summed over the four quarter pairs 2026Q4 to 2027Q4:
   - Metropolitan Core: 92.0, 11,266 persons
   - Metropolitan Fringe: 90.8, 11,221 persons
   - Lagoon Coast: 91.2, 11,264 persons
   - Industrial Corridor: 91.6, 11,034 persons
   - Cocoa Belt East: 90.4, 11,012 persons
   - Cocoa Belt West: 90.3, 11,275 persons
   - Northern Savanna: 91.2, 10,967 persons
   - Central Hills: 91.1, 11,271 persons
   - River Basin: 92.0, 11,259 persons
   - Creeks: 91.1, 11,227 persons
   - Market Towns: 90.8, 10,915 persons
   - University Towns: 91.1, 10,777 persons
3. Each district's mean days from interview to reinterview, interviews of 2027:
   - Metropolitan Core: 7.3 days
   - Metropolitan Fringe: 6.3 days
   - Lagoon Coast: 6.9 days
   - Industrial Corridor: 6.6 days
   - Cocoa Belt East: 7.1 days
   - Cocoa Belt West: 6.9 days
   - Northern Savanna: 6.8 days
   - Central Hills: 6.7 days
   - River Basin: 6.6 days
   - Creeks: 6.1 days
   - Market Towns: 6.7 days
   - University Towns: 6.1 days

### elfs_2027_flows_note.docx

1. The answer: the tables cannot go out without the warning; 13 of the 24 rates carry it, each named.
2. Chart: each of the 24 rates' share of counted moves that are not real moves, with the one-third warning line and the warned rates marked.
