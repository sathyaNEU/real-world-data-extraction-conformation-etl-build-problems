## Tags

**Domain:** Physical & Environmental Sciences (hydrology: the drawdown a groundwater abstraction causes at neighbouring licensed boreholes over a licence term).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Apply for 1,300 cubic metres a day: the 1,800 a day the new line needs fails the derogation test, and Lower Hay Farm limits the quantity.**
At 1,800 a day Lower Hay Farm's predicted drawdown on 31 March 2039 is 10 m against its 7.53 m available drawdown. Not the unbounded aquifer the June 2014 test fits, which never reached the Coldharbour Fault and lets 1,800 pass with Kilnbrook Nurseries limiting. Not an unbounded aquifer refitted or scaled to the observation boreholes' record since 2015, which still puts the limit at Kilnbrook Nurseries and above 1,300.

## 2. Critical Components

1. The June 2014 constant-rate test gives a transmissivity of **206 m2/d** and a storage coefficient of **0.00036**.
2. The Coldharbour Fault closes the aquifer east of Borehole 2, so each protected borehole's drawdown includes that of Borehole 2's image across the fault.
3. Lower Hay Farm's predicted drawdown on 31 March 2039 at 1,800 a day is **10 m** against **7.53 m** available.

## 3. Step-by-Step Solution

1. Fitted Theis to the drawdown at OB1, OB2 and OB3 in bh2_crt_june2014.xlsx (OB3's kPa converted and its local clock set to UTC, the rate the field sheet's flow checks give): transmissivity 206 m2/d, storage coefficient 0.00036.
2. Took the Coldharbour Fault's trace from the two grid references in brackenholt_geology_and_borehole_records.pdf, where it throws the sandstone down 260 m to the east against Mercia Mudstone, and placed Borehole 2's image across it.
3. Set both models against ob_monthly_levels_2015-2026.csv less the Windle Cross regional movement in windle_cross_obh_daily_levels.csv, under the returns' abstraction: the closed aquifer fits to 0.03 m rms against 0.31 m for the unbounded one, and Windle Cross shows no response.
4. Ran the pre-application letter's derogation test with the image well: at 1,800 a day the predicted drawdowns are 10 m at Lower Hay Farm, 11 m at Kilnbrook Nurseries and 10 m at Hollin Bank Golf Club, each above its available drawdown.
5. Solved each protected borehole's quantity at its available drawdown: Lower Hay Farm limits, and the largest daily quantity that passes is 1,300 cubic metres.
6. For the returns check, set each ticket in teme_valley_bulk_tickets_2026.xlsx on its run in bh2_wellhead_controller_events.csv (a time in before noon belongs to the next calendar day, the haulier's night shift), added the bulk loads to FM-1's volume from bh2_site_telemetry_15min_2025-2026.csv by local day, and counted the days above 1,200 m3.
7. For line 3, divided FM-L3's water by local month by the good bottles in bottling_runs_2025-2026.csv times each bottle's size, as line5_project_brief.docx sizes it, with BSG-1101 at the 750 ml its fill weights in qc_fill_weights_2025-2026.csv show through March 2026, not the export's 700.
8. Apply for 1,300 cubic metres a day.

## 4. Deliverable Answers

### bh2_licence_variation_note.pdf

1. Largest daily quantity that passes the derogation test: 1,300 cubic metres a day.
2. Protected borehole that limits it: Lower Hay Farm.
3. Whether 1,800 cubic metres a day passes: no.
4. Predicted drawdown on 31 March 2039 at 1,800 cubic metres a day:
   - Lower Hay Farm: 10 m
   - Kilnbrook Nurseries: 11 m
   - Hollin Bank Golf Club: 10 m
5. Chart on page 1: Lower Hay Farm's predicted drawdown at each 31 March from 2016 to 2039, at 1,300 and at 1,800 cubic metres a day, against its 7.53 m available drawdown.
6. Litres of water line 3 took per litre packed, cleans included:
   - April 2025: 2.38
   - May 2025: 2.32
   - June 2025: 2.38
   - July 2025: 2.33
   - August 2025: 2.40
   - September 2025: 2.33
   - October 2025: 2.39
   - November 2025: 2.34
   - December 2025: 2.35
   - January 2026: 2.37
   - February 2026: 2.36
   - March 2026: 2.33

### bh2_returns_check.csv

1. Volume taken from Borehole 2 and days above 1,200 cubic metres, by month from April to September 2026:
   - April 2026: 23,300 m3, 6 days
   - May 2026: 23,700 m3, 8 days
   - June 2026: 26,600 m3, 5 days
   - July 2026: 27,600 m3, 5 days
   - August 2026: 20,200 m3, 5 days
   - September 2026: 26,500 m3, 5 days
