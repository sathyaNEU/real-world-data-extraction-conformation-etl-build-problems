## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: a water district's lead service line replacement programme).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**At $25.4 million a year from 2027 every zone in the plan is finished inside the deadline: the last, RZ-10 Lakeview Terrace, is finished in programme year 2037, before 1 November 2037.**
The running plan cost reaches $274.1 million after 10.79 years of the appropriation, with each unknown line carried at the share expected among the district's Lead Status Unknown lines of its construction era (0.497, 0.279, 0.075): the share found on the 78 main segments verified whole (0.556, 0.316, 0.083) applied to every line of the era with no tap card, less what the verifications have already found, over the lines still unknown. Not the whole-segment shares carried straight to the unknown lines, which count again the lead the single-line visits have already taken out of them and run the last zone to 2038. Not the shares across every verification (0.763, 0.585, 0.217), which come from digs prompted by evidence of lead and run it to 2040, nor a model on era, construction year and zone fitted to those verifications, which keeps the same selection (2040), nor one pooled share on the segments verified whole, which drops the plan's era grouping (2039).

## 2. Critical Components

1. Share found lead or GRR on the no-tap-card lines of the 78 main segments verified whole: **0.556** built before 1930, **0.316** built 1930 to 1949, **0.083** built 1950 to 1988
2. Share of lead or GRR expected among the district's Lead Status Unknown lines: **0.497** built before 1930, **0.279** built 1930 to 1949, **0.075** built 1950 to 1988
3. Plan cost of the twelve zones: **$274.1 million**, **10.79** programme years of the appropriation
4. Last zone finished: **RZ-10 Lakeview Terrace, programme year 2037**

## 3. Step-by-Step Solution

1. Joined sl_field_verifications_2021_2026.csv to hfrwd_service_line_inventory_20270108.csv, customer-system premise numbers through cis_gis_crosswalk_2023.csv with the eight-digit padding restored and result codes through sl_material_result_codes.csv, each line at its first result: 4,911 verified lines have no tap card and were built before 1989.
2. Grouped the verified lines by main segment against the inventory: on 78 segments every service line has a verification, the mains replaced from 2023 whose every service was exposed (lsl_extract_field_notes_2027-01.md), while every other verification is a visit to one line raised by a report, a leak, a sampling site or the 2024 ranking; on the 78 segments' no-tap-card lines the share found lead or GRR is 0.556, 0.316 and 0.083 in the plan's three construction eras.
3. The plan's cost rule carries each Lead Status Unknown line at the share expected among the district's Lead Status Unknown lines of its era (HFRWD_LSLR_plan_rev2_2026-10.pdf): for each era, the whole-segment share times the district's no-tap-card lines built before 1989, less the lead or GRR the verifications have found among them, over the lines still Lead Status Unknown: 0.497, 0.279 and 0.075.
4. Counted each plan zone's Lead and GRR lines and its Lead Status Unknown lines by era in the inventory, and carried the unknown lines at those shares as full replacements and the rest as digs that find no lead, per the plan's cost rule.
5. Priced each zone at its unit costs in unit_cost_schedule_2027.xlsx with one $160,000 mobilisation: $274.1 million for the twelve zones.
6. For the 2026 payments, took each site's latest closing in lsl_completions_2026.csv, converted completed_utc to Eastern time for the quarter, added each change order once from change_orders_2026.xlsx (co_amount repeats a change order's total on every site it covers) and divided by full replacements completed, by contract number (Tri-County's two vendor numbers are one contract).
7. For the agreements, counted distinct service lines with a SIGNED form in access_agreements_2022_2026.csv, premise numbers mapped through the crosswalk, in the zone the inventory gives each line, its replacement zone under plan revision 2 (lsl_extract_field_notes_2027-01.md), rather than zone_on_form, the zone printed on the form.
8. Ran the zones in the plan's priority order against $25.4 million a year from 2027 (the capital improvement plan's construction line), each finished in the year the running appropriation covers its running cost, per the plan's schedule rule: the last zone, RZ-10 Lakeview Terrace, is finished in 2037 after 10.79 programme years, inside the 1 November 2037 deadline because each season closes on 31 October.

## 4. Deliverable Answers

### lslr_2027_programme.xlsx

1. Zone schedule, twelve zones in plan order (lead and GRR lines to replace, plan cost, finish year):
   - RZ-07 Orchard Ridge: 1,560 lines, $21,500,000, 2027
   - RZ-02 Canal Street: 2,020 lines, $33,700,000, 2029
   - RZ-11 Southgate: 1,830 lines, $28,500,000, 2030
   - RZ-04 North Linden: 1,420 lines, $23,800,000, 2031
   - RZ-09 Burkhart: 1,730 lines, $27,100,000, 2032
   - RZ-01 Foundry Hill: 1,840 lines, $27,300,000, 2033
   - RZ-05 Depot Square: 1,640 lines, $25,700,000, 2034
   - RZ-03 Millrace: 1,230 lines, $19,600,000, 2035
   - RZ-12 Kittering Village: 890 lines, $14,800,000, 2035
   - RZ-08 Elm Park: 1,310 lines, $21,400,000, 2036
   - RZ-06 Wexley: 1,040 lines, $18,000,000, 2037
   - RZ-10 Lakeview Terrace: 750 lines, $12,700,000, 2037
2. Paid per full replacement completed in each quarter of 2026:
   - 2026-LSL-01 Brannigan Excavating Inc: Q1 $13,890, Q2 $13,494, Q3 $13,416, Q4 $13,673
   - 2026-LSL-02 Tri-County Underground: Q1 $14,509, Q2 $13,937, Q3 $13,903, Q4 $13,568
   - 2026-LSL-03 Kestrel Pipe and Utility: Q1 $14,488, Q2 $14,459, Q3 $15,008, Q4 $14,784
3. Service lines with a signed access agreement, by zone:
   - RZ-07 Orchard Ridge: 975
   - RZ-02 Canal Street: 1,217
   - RZ-11 Southgate: 1,118
   - RZ-04 North Linden: 954
   - RZ-09 Burkhart: 1,017
   - RZ-01 Foundry Hill: 857
   - RZ-05 Depot Square: 889
   - RZ-03 Millrace: 626
   - RZ-12 Kittering Village: 518
   - RZ-08 Elm Park: 663
   - RZ-06 Wexley: 539
   - RZ-10 Lakeview Terrace: 368

### lslr_2027_board_paper.pdf

1. The call: every zone is finished by 2037; the last, RZ-10 Lakeview Terrace, in programme year 2037, inside the 1 November 2037 deadline, at $274.1 million of plan cost.
2. One chart of the twelve zones across programme years 2027 to 2038 in plan order, each bar running from the zone's start to its finish and labelled with its finish year, the deadline marked at the close of the 2037 season.
