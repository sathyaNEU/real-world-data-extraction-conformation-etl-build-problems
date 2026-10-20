## Tags

> **Domain:** Physical & Environmental Sciences (emissions inventory).
> **Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate five of the 12 districts for the 2027 to 2029 Accelerated Main Replacement Program: Brennan Hill, Elmwood, Fenwick, Harlow and Ivers.**
Each emitted 3.30 tonnes or more of 2026 leak methane per mile of cast-iron and bare-steel main once each surveyed leak is dated from the season leaks begin in. Not Ashby, which the midpoint start between surveys puts over the line: leaks begin mostly in December to March (62.6 per cent of odor-reported starts), so a district walked in spring finds young leaks, while Brennan Hill, Fenwick, Harlow and Ivers, walked late in the year, found leaks that had emitted since the winter.

## 2. Critical Components

1. Odor-reported leak starts in December to March: **62.6%** of the 2016 to 2026 starts.
2. Districts at or above the line: **5** of 12.

## 3. Step-by-Step Solution

1. Read the guidelines (amr_program_guidelines_2027.pdf): leaks found in 2026 on cast-iron and bare-steel mains, each from its start to its repair or 31 December 2026 at its Table 1 rate for the grade when found, per mile of in-service cast-iron and bare-steel main, designated at 3.30 or more.
2. Took the 2026 leaks from leak_survey_finds_2016_2026.csv (survey finds) and odor_call_log_2016_2026.csv (confirmed calls, UTC converted to local time), each leak's segment and district from gis_main_segments_2026-12-31.csv, and its repair from the REPAIRED visit in leak_repair_orders_2016_2027.csv.
3. Took the monthly profile of leak starts from the confirmed odor calls of 2016 to 2026 (a called leak starts at the call, guidelines 2.2): 62.6 per cent in December to March.
4. Dated each surveyed leak's start as its expected start between its segment's 2025 survey (leak_survey_schedule_2015_2026.csv) and the find, each day weighted by its month's share of the profile.
5. Summed each leak's rate times its hours from start to repair or year end by district, and divided by the district's cast-iron and bare-steel miles in gis_main_segments_2026-12-31.csv: Brennan Hill, Elmwood, Fenwick, Harlow, Ivers at or above the line.
6. From work_order_cost_lines_2025_2026.csv, took each work order's cost of each type at the end of 2026 less at the end of 2025 (each line is the cost to date, as the closing totals in work_order_closeouts_2025_2026.csv confirm), by the leak's own district: the repair costs below.
7. From service_interruption_tickets_2026.csv, took each service line shut off for a leak repair once per leak (dispatch and the field crew sometimes both opened a ticket), and counted the meters of every premise that line feeds in meter_premises_2027-03.csv (a shared service line feeds two to four premises): the customer interruptions below.
8. Designated the districts at or above the line: Brennan Hill, Elmwood, Fenwick, Harlow, Ivers.

## 4. Deliverable Answers

### leak_methane_inventory_2026.xlsx

1. Each district: leaks found in 2026, designated, 2026 leak repair cost, 2026 customer interruptions:
   - Ashby: 72; no; $391,294; 134
   - Brennan Hill: 78; yes; $392,367; 177
   - Calder: 68; no; $372,257; 182
   - Dorrance: 49; no; $246,769; 116
   - Elmwood: 114; yes; $617,746; 248
   - Fenwick: 89; yes; $350,452; 122
   - Glenmora: 68; no; $365,620; 112
   - Harlow: 88; yes; $370,241; 142
   - Ivers: 79; yes; $437,290; 160
   - Juniper: 70; no; $414,327; 186
   - Kessel: 52; no; $266,418; 133
   - Lockwood: 64; no; $352,142; 195

### main_replacement_designations_2027.pdf

1. Designates five of 12: Brennan Hill, Elmwood, Fenwick, Harlow, Ivers.
2. Bar chart of the 12 districts' methane per mile against the 3.30 line, designated districts highlighted, on page 1; the district table beneath it.
