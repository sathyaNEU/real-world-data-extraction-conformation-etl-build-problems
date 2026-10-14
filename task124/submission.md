## Tags

**Domain:** Energy Systems & Utilities (asset condition and maintenance: a water district's lead service line replacement programme).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**At $25.4 million a year from 2027 every zone in the plan is finished inside the deadline: the last, RZ-06 Wexley, is finished in programme year 2037, before 1 November 2037.**
The running plan cost reaches $268.3 million after 10.56 years of the appropriation, with each Lead Status Unknown line carried at the share found on the verified lines with no tap card on mains of its own kind (13 in 14 where the main's tap cards read lead or galvanized, 1 in 19 where they read only copper or plastic), so the unknown lines carry 0.389, 0.268 and 0.074 by era. Not the shares across every verification (0.852, 0.703, 0.225), nor a model on era, construction year and zone fitted to them, which run the last zone to 2042; not the shares on the 78 main segments verified whole, with or without the lead already found taken out, which run it to 2040; not the share of tap cards that read lead or galvanized, which runs it to 2039: the verified lines, the surviving cards and, before 1950, the lines on the mains verified whole sit on lead or galvanized mains far more often than the lines still unknown do.

## 2. Critical Components

1. Share of the verified lines with no tap card found lead or GRR, by the kind of main they tap: **13 in 14** where the main's tap cards read lead or galvanized, **1 in 19** where they read only copper or plastic
2. Lead Status Unknown lines on lead or galvanized mains: **3,822** of 9,939 built before 1930, **2,215** of 9,023 built 1930 to 1949, **359** of 14,569 built 1950 to 1988
3. Share of lead or GRR expected among the district's Lead Status Unknown lines: **0.389** built before 1930, **0.268** built 1930 to 1949, **0.074** built 1950 to 1988
4. Plan cost of the twelve zones: **$268.3 million**, **10.56** programme years of the appropriation
5. Last zone finished: **RZ-06 Wexley, programme year 2037**

## 3. Step-by-Step Solution

1. Joined sl_field_verifications_2021_2026.csv to hfrwd_service_line_inventory_20270108.csv, customer-system premise numbers through cis_gis_crosswalk_2023.csv with the eight-digit padding restored and result codes through sl_material_result_codes.csv, each line at its first result: 3,409 verified lines have no tap card and were built before 1989.
2. Read each main's kind from the inventory's tap cards on it (lead or galvanized when any card on the main reads LEAD or GALV, otherwise copper or plastic): on the verified lines with no tap card, 13 in 14 proved lead or GRR on lead or galvanized mains and 1 in 19 on copper or plastic mains, in every construction era and alike on the 78 mains where every service was verified and on single-line visits.
3. Counted the district's Lead Status Unknown lines by era and kind of main and carried each at its main's share, which gives the share expected among the district's Lead Status Unknown lines of each era that the costing rule in HFRWD_LSLR_plan_rev2_2026-10.pdf asks for: 0.389, 0.268 and 0.074.
4. Counted each plan zone's Lead and GRR lines and its Lead Status Unknown lines by era in the inventory, the unknown lines carried at those shares as full replacements and the rest as digs that find no lead, priced at each zone's unit costs in unit_cost_schedule_2027.xlsx with one $230,000 mobilisation: $268.3 million for the twelve zones.
5. For the 2026 payments, took each site's latest closing in lsl_completions_2026.csv, converted completed_utc to Eastern time for the quarter, added each change order once from change_orders_2026.xlsx (co_amount repeats a change order's total on every site it covers) and divided by full replacements completed, by contract number (Tri-County's two vendor numbers are one contract).
6. For the agreements, counted distinct service lines with a SIGNED form in access_agreements_2022_2026.csv, premise numbers mapped through the crosswalk, together with the lines lslr_outreach_tracker_20270108.csv shows E-SIGNED that have no form at all in the agreement file, in the zone the inventory gives each line (its zone under plan revision 2) rather than zone_on_form.
7. Ran the zones in the plan's priority order against $25.4 million a year from 2027 (the capital improvement plan's construction line), each finished in the year the running appropriation covers its running cost, per the plan's schedule rule: the last zone, RZ-06 Wexley, is finished in 2037 after 10.56 programme years, inside the 1 November 2037 deadline because each season closes on 31 October.

## 4. Deliverable Answers

### lslr_2027_programme.xlsx

1. Zone schedule, twelve zones in plan order (lead and GRR lines to replace, plan cost, finish year):
   - RZ-07 Orchard Ridge: 1,250 lines, $20,700,000, 2027
   - RZ-02 Canal Street: 1,820 lines, $34,000,000, 2029
   - RZ-11 Southgate: 1,650 lines, $28,400,000, 2030
   - RZ-04 North Linden: 1,180 lines, $23,000,000, 2031
   - RZ-09 Burkhart: 1,380 lines, $25,000,000, 2032
   - RZ-01 Foundry Hill: 1,540 lines, $26,000,000, 2033
   - RZ-05 Depot Square: 1,390 lines, $24,500,000, 2034
   - RZ-12 Kittering Village: 760 lines, $14,700,000, 2034
   - RZ-03 Millrace: 1,050 lines, $19,100,000, 2035
   - RZ-08 Elm Park: 1,170 lines, $21,500,000, 2036
   - RZ-10 Lakeview Terrace: 670 lines, $13,300,000, 2036
   - RZ-06 Wexley: 890 lines, $18,100,000, 2037
2. Paid per full replacement completed in each quarter of 2026:
   - 2026-LSL-01 Brannigan Excavating Inc: Q1 $14,395, Q2 $13,488, Q3 $13,407, Q4 $13,344
   - 2026-LSL-02 Tri-County Underground: Q1 $14,634, Q2 $13,985, Q3 $13,922, Q4 $13,867
   - 2026-LSL-03 Kestrel Pipe and Utility: Q1 $15,294, Q2 $14,515, Q3 $14,636, Q4 $14,444
3. Service lines with a signed access agreement, by zone:
   - RZ-07 Orchard Ridge: 960
   - RZ-02 Canal Street: 1,186
   - RZ-11 Southgate: 1,077
   - RZ-04 North Linden: 1,020
   - RZ-09 Burkhart: 991
   - RZ-01 Foundry Hill: 878
   - RZ-05 Depot Square: 846
   - RZ-12 Kittering Village: 504
   - RZ-03 Millrace: 633
   - RZ-08 Elm Park: 685
   - RZ-10 Lakeview Terrace: 386
   - RZ-06 Wexley: 607

### lslr_2027_board_paper.pdf

1. The call: every zone is finished by 2037; the last, RZ-06 Wexley, in programme year 2037, inside the 1 November 2037 deadline, at $268.3 million of plan cost.
2. One chart of the twelve zones across programme years 2027 to 2038 in plan order, each bar running from the zone's start to its finish and labelled with its finish year, the deadline marked at the close of the 2037 season.
