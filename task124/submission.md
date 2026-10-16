## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: a water district's lead service line replacement programme).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**At $25.4 million a year from 2027 every zone in the plan is finished inside the deadline: the last, RZ-06 Wexley, is finished in programme year 2037, before 1 November 2037.**
The plan cost of the twelve zones is $267 million, 10.5 years of the appropriation, with each Lead Status Unknown line carried at the share found on the verified lines with no tap card on mains of its own kind built in its own era (99.2, 95.0 and 60.6 per cent where the main's tap cards read lead or galvanized; 1 of 1,014, 2 of 1,123 and none of 1,666 where they read only copper or plastic), so the unknown lines carry 0.47, 0.26 and 0.01 by era. Not the shares across all of those verified lines by era (0.735, 0.524, 0.061), nor a model on era, construction year and zone fitted to them; not the shares on the main segments verified whole, with or without the lead already found taken out; not the share of tap cards that read lead or galvanized: each runs the last zone past the 1 November 2037 deadline, because the verified lines, the replaced mains and the surviving cards sit on lead or galvanized mains far more often than the lines still unknown do. Nor one rate for each kind of main across all eras, which keeps RZ-06 Wexley in 2037 but changes the rounded lines in nine zones, because the share on lead or galvanized mains falls from 99.2 to 60.6 per cent across the eras.

## 2. Critical Components

1. Share of the verified lines with no tap card found lead or GRR, by the kind of main they tap and the era they were built: **99.2, 95.0 and 60.6 per cent** where the main's tap cards read lead or galvanized (built before 1930, 1930 to 1949, 1950 to 1988); **1 of 1,014, 2 of 1,123 and none of 1,666** where they read only copper or plastic
2. Lead Status Unknown lines on lead or galvanized mains: **4,212** of 8,890 built before 1930, **2,121** of 7,851 built 1930 to 1949, **261** of 13,200 built 1950 to 1988
3. Share of lead or GRR expected among the district's Lead Status Unknown lines: **0.47** built before 1930, **0.26** built 1930 to 1949, **0.01** built 1950 to 1988
4. Plan cost of the twelve zones: **$267 million**, **10.5** programme years of the appropriation
5. Last zone finished: **RZ-06 Wexley, programme year 2037**

## 3. Step-by-Step Solution

1. Joined sl_field_verifications_2021_2026.csv to hfrwd_service_line_inventory_20270108.csv, customer-system premise numbers through cis_gis_crosswalk_2023.csv with the eight-digit padding restored and result codes through sl_material_result_codes.csv, each line at its first result: 8,255 verified lines have no tap card and were built before 1989.
2. Read each main's kind from the inventory's tap cards on it (lead or galvanized when any card on the main reads LEAD or GALV, otherwise copper or plastic) and took the share of the verified lines with no tap card found lead or GRR by kind of main and construction era: 99.2, 95.0 and 60.6 per cent on lead or galvanized mains and 1 of 1,014, 2 of 1,123 and none of 1,666 on copper or plastic mains, alike on the 316 mains where every service was verified and on single-line visits; the falling shares on lead or galvanized mains refute one rate per kind across the eras.
3. Counted the district's Lead Status Unknown lines by era and kind of main and carried each at the share for its kind and era, which gives the share expected among the district's Lead Status Unknown lines of each era that the costing rule in HFRWD_LSLR_plan_rev2_2026-10.pdf asks for: 0.47, 0.26 and 0.01.
4. Counted each plan zone's Lead and GRR lines and its Lead Status Unknown lines by era in the inventory, the unknown lines of each era carried at that era's share, unrounded, as full replacements and the rest as digs that find no lead, priced at each zone's unit costs in unit_cost_schedule_2027.xlsx with one $230,000 mobilisation: $267 million for the twelve zones.
5. For the 2026 payments, took each site's latest closing in lsl_completions_2026.csv, converted completed_utc to Eastern time for the quarter, added each change order once from change_orders_2026.xlsx (co_amount repeats a change order's total on every site it covers) and divided by full replacements completed, by contract number (Tri-County's two vendor numbers are one contract).
6. For the agreements, counted distinct service lines with a SIGNED form in access_agreements_2022_2026.csv, premise numbers mapped through the crosswalk, together with the lines lslr_outreach_tracker_20270108.csv shows E-SIGNED that have no form at all in the agreement file (an E-SIGNED line whose form was withdrawn is not added), in the zone the inventory gives each line (its zone under plan revision 2) rather than zone_on_form.
7. Ran the zones in the plan's priority order against $25.4 million a year from 2027 (the capital improvement plan's construction line), each finished in the year the running appropriation covers its running cost, per the plan's schedule rule: the last zone, RZ-06 Wexley, is finished in 2037 after 10.5 programme years, inside the 1 November 2037 deadline because each season closes on 31 October.

## 4. Deliverable Answers

### lslr_2027_programme.xlsx

1. Zone schedule, twelve zones in plan order (lead and GRR lines to replace, plan cost, finish year):
   - RZ-07 Orchard Ridge: 1,210 lines, $20,800,000, 2027
   - RZ-02 Canal Street: 1,710 lines, $34,300,000, 2029
   - RZ-11 Southgate: 1,570 lines, $28,900,000, 2030
   - RZ-04 North Linden: 1,070 lines, $22,900,000, 2031
   - RZ-09 Burkhart: 1,440 lines, $26,100,000, 2032
   - RZ-01 Foundry Hill: 1,730 lines, $29,900,000, 2033
   - RZ-05 Depot Square: 1,320 lines, $24,900,000, 2034
   - RZ-12 Kittering Village: 550 lines, $11,900,000, 2034
   - RZ-03 Millrace: 1,020 lines, $19,500,000, 2035
   - RZ-08 Elm Park: 1,080 lines, $21,200,000, 2036
   - RZ-10 Lakeview Terrace: 450 lines, $10,100,000, 2036
   - RZ-06 Wexley: 710 lines, $16,600,000, 2037
2. Paid per full replacement completed in each quarter of 2026:
   - 2026-LSL-01 Brannigan Excavating Inc: Q1 $13,944, Q2 $13,378, Q3 $13,402, Q4 $13,303
   - 2026-LSL-02 Tri-County Underground: Q1 $14,401, Q2 $13,741, Q3 $14,096, Q4 $13,944
   - 2026-LSL-03 Kestrel Pipe and Utility: Q1 $15,545, Q2 $14,166, Q3 $14,328, Q4 $14,260
3. Service lines with a signed access agreement, by zone:
   - RZ-07 Orchard Ridge: 862
   - RZ-02 Canal Street: 1,147
   - RZ-11 Southgate: 1,084
   - RZ-04 North Linden: 1,000
   - RZ-09 Burkhart: 906
   - RZ-01 Foundry Hill: 854
   - RZ-05 Depot Square: 762
   - RZ-12 Kittering Village: 403
   - RZ-03 Millrace: 613
   - RZ-08 Elm Park: 642
   - RZ-10 Lakeview Terrace: 300
   - RZ-06 Wexley: 541

### lslr_2027_board_paper.pdf

1. The call: every zone is finished by 2037; the last, RZ-06 Wexley, in programme year 2037, inside the 1 November 2037 deadline, at $267 million of plan cost.
2. One chart of the twelve zones across programme years 2027 to 2038 in plan order, each bar running from the zone's start to its finish and labelled with its finish year, the deadline marked at the close of the 2037 season.
