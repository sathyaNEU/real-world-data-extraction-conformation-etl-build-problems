## Tags

**Domain:** Criminology & Justice (crime incidence and hot spot analysis: a municipal police service designating the street segments its directed patrols cover for a year).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Designate the 20 street segments listed below for the 2027 hot spot patrols: the five segments around the Lakeshore Centre come in and the five around the Memorial Gardens drop out, because the Mariners play their 2027 home games at the Lakeshore Centre and those segments' street crime follows the venue's event nights.** From 2022 to 2026 the five Lakeshore segments recorded 410 of their 822 founded patrol crimes on the Lakeshore Centre's 61 event nights. Not the ranking of 2026's or the five years' counts, which keeps the Gardens segments on crime the Gardens' event nights carried (801 of their 1345 on 200 nights) and leaves out the segments the 2027 calendar loads.

## 2. Critical Components

1. The paid-duty register books **16** Mariners home games at the Lakeshore Centre from 8 January 2027; the Mariners' last Memorial Gardens game was on 20 December 2026.
2. The five Gardens segments that drop out recorded **801 of 1345** founded patrol crimes from 2022 to 2026 on the Gardens' **200** event nights, about **11 per cent** of the nights.
3. The five Lakeshore segments that come in recorded **410 of 822** on the Lakeshore Centre's **61** event nights.
4. 112148 (King Street, Wellington to Albert, ward 1) stays designated on its steady crime with the Gardens' event nights gone.

## 3. Step-by-Step Solution

1. Conformed mps_rms_occurrences_2022_2026.csv under the protocol: each occurrence once on its latest version, legacy codes through rms_offence_code_crosswalk_2023.csv, legacy dates day first, unfounded out, dated by occurred_from or the report date where blank, on the segments of mountjoy_street_segments.csv.
2. Took each venue's event nights from the EVENT duties at the Memorial Gardens and the Lakeshore Centre in every sheet of mps_paid_duty_register_2022_2027.xlsx: 200 Gardens and 61 Lakeshore nights from 2022 to 2026, and the 2027 sheet's 16 Mariners home games at the Lakeshore Centre.
3. Fitted each segment's daily founded patrol crimes from 2022 to 2026 by least squares on a constant and the two venues' event-night indicators: its steady rate and its excess on each venue's nights.
4. Took 2027 as 2026's calendar with the Mariners' 35 home games at the Lakeshore Centre (48 Lakeshore nights, 6 Gardens nights), each segment's expected count 365 days at its steady rate plus each excess times its venue's nights, and designated the 20 highest.
5. Officer-hours: for each call in mps_cad_calls_2026.csv (source not OFFICER) received in 2026 local time on a segment of the street file (so not Elmvale's events, whose districts repeat the ward numbers), each unit's hours from dispatch to clear times its crew in mps_patrol_roster_2026.csv on the tour covering the dispatch (a night tour is dated by the evening it starts), by ward and quarter of receipt.
6. Priority 1 medians: the same calls at priority 1, the first onscene_utc of any unit minus received_utc, median by the ward of the call's segment.

## 4. Deliverable Answers

### hot_spot_patrols_2027.pptx

1. Designated segments, 20:
   - 190643 (Northgate Drive, Lake to Pier, ward 5)
   - 124511 (Harbour Road, Ontario to Simcoe, ward 4)
   - 158663 (Simcoe Street, Front to King, ward 4)
   - 150449 (Harbour Road, Simcoe to Mill, ward 4)
   - 176470 (Front Street, Simcoe to Mill, ward 4)
   - 153464 (King Street, Clarence to Market, ward 3)
   - 109465 (Front Street, Peel to Ontario, ward 3)
   - 176794 (Victoria Street, George to Charlotte, ward 3)
   - 165151 (George Street, Victoria to Clarence, ward 3)
   - 197721 (Cedar Street, Durham to Murray, ward 6)
   - 198000 (Bethune Street, Romaine to Sophia, ward 8)
   - 135435 (Sherbrooke Street, Orchard to Maple, ward 6)
   - 125703 (King Street, Market to Brock, ward 3)
   - 145090 (Parkhill Road, Rubidge to Aylmer, ward 8)
   - 182379 (Market Street, York to George, ward 3)
   - 102787 (Dundas Street, Clarence to Market, ward 3)
   - 109489 (Lansdowne Street, Maple to Rideau, ward 6)
   - 116925 (Wolfe Street, Peel to Ontario, ward 7)
   - 112148 (King Street, Wellington to Albert, ward 1)
   - 185090 (Simcoe Street, Sherbrooke to Hunter, ward 8)
2. Come in against the 2026 ranking:
   - 124511 (Harbour Road, Ontario to Simcoe, ward 4)
   - 158663 (Simcoe Street, Front to King, ward 4)
   - 150449 (Harbour Road, Simcoe to Mill, ward 4)
   - 176470 (Front Street, Simcoe to Mill, ward 4)
   - 109465 (Front Street, Peel to Ontario, ward 3)
3. Drop out against the 2026 ranking:
   - 162095 (Albert Street, King to Queen, ward 3)
   - 171145 (Queen Street, Wellington to Albert, ward 1)
   - 168732 (Wellington Street, King to Queen, ward 1)
   - 145175 (Wellington Street, Queen to Princess, ward 1)
   - 162877 (King Street, Water to Wellington, ward 1)
4. Bar chart on slide 2 of each of the 52 candidate segments' expected 2027 patrol crimes, designated in navy, the cut between 185090 and 186587.

### patrol_figures_2026.csv

1. Officer-hours on calls for service in 2026, whole hours:
   - Ward 1: Q1 602, Q2 566, Q3 509, Q4 555
   - Ward 2: Q1 453, Q2 402, Q3 437, Q4 430
   - Ward 3: Q1 773, Q2 748, Q3 817, Q4 815
   - Ward 4: Q1 545, Q2 557, Q3 559, Q4 597
   - Ward 5: Q1 910, Q2 824, Q3 838, Q4 895
   - Ward 6: Q1 1024, Q2 1120, Q3 1176, Q4 1229
   - Ward 7: Q1 874, Q2 814, Q3 886, Q4 827
   - Ward 8: Q1 1277, Q2 1261, Q3 1384, Q4 1215
2. Median minutes in 2026 from the receipt of a priority 1 call to the first officer's arrival, one decimal:
   - Ward 1: 5.7
   - Ward 2: 6.3
   - Ward 3: 5.7
   - Ward 4: 7.0
   - Ward 5: 6.9
   - Ward 6: 7.4
   - Ward 7: 7.1
   - Ward 8: 7.9
