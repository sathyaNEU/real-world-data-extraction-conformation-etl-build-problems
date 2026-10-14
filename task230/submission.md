# task230 submission

## Tags

**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: the coding bias of a census release's occupation counts).
**Analytical objective:** Data Quality Monitoring & Alerting (the coding quality warning each occupation sub-major group carries in the census's first occupation release).

## 1. Final Recommendation

**Six occupation sub-major groups should carry the coding quality warning in the first occupation release: 24 Business and administration professionals (-3.1 per cent), 25 Information and communications technology professionals (-2.5), 35 Information and communications technicians (+4.6), 41 General and keyboard clerks (+3.2), 71 Building and related trades workers, excluding electricians (-2.3) and 93 Labourers in mining, construction, manufacturing and transport (+6.9).**

Each is the group's coding bias in the release, built route by route from the coding quality study and carried to the 103,367 write-ins still to code on 13 November, 53,112 of them follow-up proxy returns, under the 0.80 acceptance score in force from 16 November; every other group stays within plus or minus 2.0 per cent. Not the study's coded-so-far bias taken as the release's, which warns only 35 and 93. Not the follow-up batches carried as one, which also warns 24 and 41 but leaves 25 and 71 inside the lines. Not the routes carried under the 0.90 score the study saw, which warns 24, 35, 71 and 93 and leaves 25 and 41 inside.

## 2. Critical Components

1. Write-ins coded by 13 November, by response route: online self-response **321,660**, paper self-response **122,864**, follow-up household member **71,258**, follow-up proxy **15,330**
2. Write-ins still to code on 13 November, by response route: online self-response **3,344**, paper self-response **1,925**, follow-up household member **44,986**, follow-up proxy **53,112**
3. Write-ins in the release population: **634,479**

## 3. Step-by-Step Solution

1. Gave each form in census2026_receipt_register.csv its response route: online and paper by capture mode, and each FIELD form the outcome of the call in field_visit_log_jun_oct_2026.csv that completed its questionnaire (10 household member, 20 proxy; field manual 5.3 and 5.5).
2. Counted by route the write-ins coded by 13 November in census2026_occupation_coding_extract.parquet and the register's write-ins not yet coded: 531,112 coded and 103,367 still to code, 634,479 in the release population (OQ-4 2.1).
3. Weighted each write-in in census2026_coding_quality_study.csv by its selection interval (OQ-4 3.3) and summed, by route and sub-major group, the write-ins coded to the group, the write-ins the reference coding puts there, and the write-ins the group gets under the 0.80 acceptance score (the autocoder's suggestion where it scores 0.80 or more, else the production code; processing plan, Decision).
4. Built each group's coding bias in the release (OQ-4 3.1): the coded write-ins as the study weights them, plus each route's still-to-code write-ins at that route's study rates under the 0.80 score, against the reference count built the same way: 24 -3.1, 25 -2.5, 35 +4.6, 41 +3.2, 71 -2.3 and 93 +6.9 per cent, every other group within plus or minus 2.0.
5. Warned every group whose unrounded bias is beyond plus or minus 2.0 per cent (OQ-4 4.1): 24, 25, 35, 41, 71 and 93.
6. Counted the CLERICAL write-ins in the extract coded in October by each team, each coder id on each day placed in a team by coding_staff_movements_2026.csv, and summed the OCC hours in coding_timesheets_21sep_01nov2026.csv for shifts that started in October, placed by the same movements, correction lines included: Coding Team 1 4,160 write-ins and 295.75 hours, Coding Team 2 3,746 and 270.75, Coding Team 3 4,206 and 283.00, Coding Team 4 3,112 and 229.50, Coding Team 5 2,680 and 176.00.
7. Counted by region (enumeration_districts_2026.csv) the follow-up calls made in September and those that made no contact (outcome 31), each call once where a replacement tablet re-sent it under a new call number (same address, call time and outcome, later sync): calls Port Aldmere 20,016, Ardvale 10,468, Brackenmoor 9,289, Kilmarran 10,084, Fernholt 8,380, Rathcolm 8,867, Strathmoyle 8,438, Glenwarren 7,435.

## 4. Deliverable Answers

### occupation_coding_warnings_2026.xlsx

1. Groups carrying the coding quality warning: 24, 25, 35, 41, 71 and 93
2. Coding bias in the release, every sub-major group, per cent:
   - 11 Chief executives, senior officials and legislators: -0.2
   - 12 Administrative and commercial managers: -0.4
   - 13 Production and specialised services managers: 0.0
   - 14 Hospitality, retail and other services managers: -0.8
   - 21 Science and engineering professionals: -0.3
   - 22 Health professionals: -0.7
   - 23 Teaching professionals: 0.0
   - 24 Business and administration professionals: -3.1
   - 25 Information and communications technology professionals: -2.5
   - 26 Legal, social and cultural professionals: -1.1
   - 31 Science and engineering associate professionals: 0.6
   - 32 Health associate professionals: -0.2
   - 33 Business and administration associate professionals: 0.9
   - 34 Legal, social, cultural and related associate professionals: 0.1
   - 35 Information and communications technicians: 4.6
   - 41 General and keyboard clerks: 3.2
   - 42 Customer services clerks: 0.0
   - 43 Numerical and material recording clerks: 1.0
   - 44 Other clerical support workers: 0.1
   - 51 Personal service workers: 0.0
   - 52 Sales workers: 0.0
   - 53 Personal care workers: 0.8
   - 54 Protective services workers: -0.2
   - 61 Market-oriented skilled agricultural workers: -0.2
   - 62 Market-oriented skilled forestry, fishery and hunting workers: -0.1
   - 63 Subsistence farmers, fishers, hunters and gatherers: 0.0
   - 71 Building and related trades workers, excluding electricians: -2.3
   - 72 Metal, machinery and related trades workers: -1.1
   - 73 Handicraft and printing workers: 0.0
   - 74 Electrical and electronic trades workers: -0.1
   - 75 Food processing, wood working, garment and other craft and related trades workers: -0.2
   - 81 Stationary plant and machine operators: -0.9
   - 82 Assemblers: 0.0
   - 83 Drivers and mobile plant operators: 0.3
   - 91 Cleaners and helpers: -0.1
   - 92 Agricultural, forestry and fishery labourers: 0.6
   - 93 Labourers in mining, construction, manufacturing and transport: 6.9
   - 94 Food preparation assistants: -0.2
   - 95 Street and related sales and service workers: 0.0
   - 96 Refuse workers and other elementary workers: -0.8
3. October, by clerical coding team, occupation write-ins coded and hours spent on occupation coding:
   - Coding Team 1: 4,160 write-ins, 295.75 hours
   - Coding Team 2: 3,746 write-ins, 270.75 hours
   - Coding Team 3: 4,206 write-ins, 283.00 hours
   - Coding Team 4: 3,112 write-ins, 229.50 hours
   - Coding Team 5: 2,680 write-ins, 176.00 hours
4. September, by region, follow-up calls enumerators made and calls that made no contact:
   - Port Aldmere: 20,016 calls, 8,208 that made no contact
   - Ardvale: 10,468 calls, 4,215 that made no contact
   - Brackenmoor: 9,289 calls, 3,798 that made no contact
   - Kilmarran: 10,084 calls, 4,163 that made no contact
   - Fernholt: 8,380 calls, 3,367 that made no contact
   - Rathcolm: 8,867 calls, 3,611 that made no contact
   - Strathmoyle: 8,438 calls, 3,471 that made no contact
   - Glenwarren: 7,435 calls, 3,055 that made no contact

### occupation_coding_bias_2026.png

1. One horizontal bar per sub-major group (40 bars) of its coding bias in the release, warning lines at -2.0 and +2.0, the six warned groups in red with their bias labelled.
