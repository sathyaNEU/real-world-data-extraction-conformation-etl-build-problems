## Tags

**Domain:** General Statistics & Data Science (exploratory data analysis and distribution assessment), in supply chain and logistics (offshore installation transport).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Stand NM Atlas at Skarvgrund for the 1 November 2026 to 28 February 2027 campaign; it avoids 42 days of floating-vessel weather downtime there.**
That is 3 days more than at Lillevig Banke (39). Not Fjernhav (38), whose vessel loses the most downtime of its own but whose release changes no other vessel's. Not Lillevig Banke, whose vessel's passages on to Kalvholm are imposed by Skarvgrund's vessel holding Bramso Havn's one heavy-lift berth and stop only when Skarvgrund's vessel is gone. Not Osterrev (32), the roughest buoy, whose vessel shares Tranevig's two berths with nobody's delay.

## 2. Critical Components

1. With every site floating, Lillevig Banke's vessel goes on to the Kalvholm storm moorings whenever Skarvgrund's holds Bramso Havn's heavy-lift berth on its arrival, as all 26 such arrivals in the 2023/24 to 2025/26 progress reports did.
2. Own floating-vessel downtime with every site floating is **36 days** at Skarvgrund and **38 days** at Lillevig Banke.
3. Downtime avoided with NM Atlas there is **42 days** at Skarvgrund, **39 days** at Lillevig Banke and **38 days** at Fjernhav.

## 3. Step-by-Step Solution

1. Stacked buoy_hm0_2008_2017.csv and buoy_hs_2016_2026.csv through buoy_stations.csv (centimetres to metres, the 2016/17 winter once) and cut each of the 18 winters to 1 November 00:00 to 28 February 24:00 Danish time (UTC+1).
2. Replayed all floating vessels together, hour by hour, with the weather procedure in campaign_plan_2026_27.pdf section 3, the limits in vessel_register_2026.xlsx and the passage hours and heavy-lift berths in port_register_2026.xlsx.
3. Took the practice at a taken berth from daily_progress_reports_2023_2026.csv: the 26 arrivals that found the other Bramso Havn vessel alongside went on to Kalvholm and every other arrival berthed.
4. Computed the placement basis in the plan's section 4, the fleet's downtime with every site floating and with NM Atlas at each site, averaged over the 18 winters: 42 days avoided at Skarvgrund, 39 at Lillevig Banke, 38 at Fjernhav, 32 at Osterrev, 29 at Molleflak.
5. Ask 1 (developer_standby_statements.csv): kept a revised statement's restated line in place of the same vessel and category line of the statement its reference names, dated a line whose vessel worked elsewhere in that month (progress reports) to its last month at that site, and summed by developer and winter.
6. Ask 2 (atlas_shift_reports.json): counted WW and WS as weather standby before the 15 January 2026 go-live (the old WS hours rise and fall with the buoy's sea state) and WX after it, and filled the 15 to 25 January gap with atlas_final_hire_statement.pdf's reduced-rate hours less the WX hours reported in its hire period.
7. Ask 3 (ap_port_charges_2023_2026.csv): counted a Tranevig call's charge once across weekly lines whose berth times run on from one another, and one Hjortby Havn invoice per call where a re-keyed copy repeats the number, vessel and berth time.
8. Recommended Skarvgrund, 3 days ahead of Lillevig Banke.

## 4. Deliverable Answers

### placement.xlsx

1. Downtime avoided with NM Atlas there, whole days:
   - Skarvgrund: 42
   - Lillevig Banke: 39
   - Fjernhav: 38
   - Osterrev: 32
   - Molleflak: 29
2. Own floating-vessel downtime with every site floating, whole days:
   - Skarvgrund: 36
   - Lillevig Banke: 38
   - Fjernhav: 38
   - Osterrev: 32
   - Molleflak: 29
3. Pick Skarvgrund, runner-up Lillevig Banke, gap 3 days.
4. Standby acknowledged by each developer, days:
   - Vestkyst Vind A/S, 2023/24: 72.50
   - Vestkyst Vind A/S, 2024/25: 68.75
   - Vestkyst Vind A/S, 2025/26: 65.50
   - Osterhav Energi A/S, 2023/24: 26.00
   - Osterhav Energi A/S, 2024/25: 28.50
   - Osterhav Energi A/S, 2025/26: 27.50
   - Fjernhav Offshore ApS, 2024/25: 34.50
   - Fjernhav Offshore ApS, 2025/26: 29.00
5. NM Atlas weather standby, whole hours:
   - 2023/24: 389
   - 2024/25: 460
   - 2025/26: 249
6. Port dues paid for shelter calls, euros to the nearest 10:
   - Tranevig, 2023/24: 43,560
   - Tranevig, 2024/25: 40,340
   - Tranevig, 2025/26: 41,950
   - Hjortby Havn, 2023/24: none (no shelter call)
   - Hjortby Havn, 2024/25: 46,970
   - Hjortby Havn, 2025/26: 31,350

### panel_deck.pptx

7. One column chart of downtime avoided by site in days, sorted, Skarvgrund marked as the pick, value labels on every bar (slide 2).
