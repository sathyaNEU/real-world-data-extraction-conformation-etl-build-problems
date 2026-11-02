## Tags

**Domain:** Epidemiology & Public Health (health burden and impact modelling: an occupational noise control).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Brolga should install the 2027 induct-line enclosure at Kewdale.** It brings 102 workers from at or above 85 dB(A) to below it, against 69 at Truganina. Not Larapinta, which leads only when every worker is given their job title's place, because at Kewdale the inductors and the rotation's loaders share the induct hours. Not Eastern Creek, which has the most workers at or above the standard (114) but brings only 30 below, its line staying above it for anyone at induct most of the shift.

## 2. Critical Components

1. Kewdale: **102** workers at or above 85 dB(A) in the reference weeks, **102** of them brought below by the enclosure (induct area **86.4** dB(A) after it).
2. Truganina, the runner-up: **69** brought below.
3. Eastern Creek: **114** at or above, **30** brought below.

## 3. Step-by-Step Solution

1. Took every employee with a WORKED shift in ta_shift_records_20260928_20261108.csv and every labour-hire operative in labour_hire_timesheets_oct_nov_2026.xlsx whose shift began 12 October to 8 November 2026 (Schedule 2, clause 2.2), with each worker's hub and shifts worked.
2. Converted wcs_operator_sessions_export_20261116.csv from UTC to each hub's local time, placed each session in the shift it began in, and joined its badge to a payroll or labour-hire number through badge_register_20261113.xlsx at the session's date (reissued badges by their issue and cancel dates, contractors left out).
3. Summed each worker's induct hours over the reference weeks, divided by their shifts worked, and computed their LAeq,8h per Schedule 2, clause 2.3, from the induct, floor and amenities levels in noise_survey_report_2026.pdf, before and with the induct level in induct_enclosure_design_report_rev2.pdf.
4. Counted by hub the workers at 85 dB(A) or more and those brought below it: Kewdale 102 brought below, Truganina 69.
5. Placed each EP-01 vend in ppe_vending_transactions_2026q3.json at the hub its machine stood at, from the sites of its visits in ppe_vending_service_visits_2026q3.csv (moving on its COMMISSION visit, not the asset list's current site), in that hub's local time, at one pair a vend before the machine's RANGE CHANGE visit and five pairs from it.
6. Replayed each client's tests in audiometry_results_2025_2026.csv from their first test per Schedule 3, each confirming retest becoming the reference (not the reference in audiometry_clients_20261106.xlsx), and placed each shift confirmed in 2026 at the worker's hub on the retest date from hr_site_transfers_2026.csv.
7. Placed the enclosure at the hub with the most workers brought below: Kewdale.

## 4. Deliverable Answers

### induct_enclosure_2027.pptx

1. The hub: Kewdale.
2. Workers at or above 85 dB(A) in the reference weeks, and brought below it by the enclosure, by hub:
   - Larapinta: 66 at or above, 66 brought below
   - Eastern Creek: 114 at or above, 30 brought below
   - Truganina: 69 at or above, 69 brought below
   - Wingfield: 39 at or above, 39 brought below
   - Kewdale: 102 at or above, 102 brought below
   - Beresfield: 49 at or above, 49 brought below
3. Bar chart of the workers brought below by hub on slide 3, Kewdale's bar marked.

### hearing_program_2026.csv

1. Earplug pairs issued at each hub in July, August and September 2026, local time:
   - Larapinta: July 2,468; August 2,276; September 2,470
   - Eastern Creek: July 3,170; August 2,619; September 3,060
   - Truganina: July 2,192; August 1,901; September 1,935
   - Wingfield: July 1,846; August 1,813; September 1,820
   - Kewdale: July 2,008; August 1,849; September 1,785
   - Beresfield: July 1,477; August 1,225; September 1,535
2. Workers whose 2026 hearing tests confirmed a standard threshold shift:
   - Larapinta: 9
   - Eastern Creek: 9
   - Truganina: 5
   - Wingfield: 3
   - Kewdale: 4
   - Beresfield: 4
