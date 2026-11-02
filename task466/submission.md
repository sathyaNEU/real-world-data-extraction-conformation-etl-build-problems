## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (landfill methane).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Breck Hollow's 2026 return puts the Authority in Tier 2 of the closed landfill methane charge, so the 2027 budget should carry $118,000.**
The landfill released 410 t of methane in 2026, between the 375 t and 450 t thresholds. Not Tier 3 at 478 t, which scales the year's capture up by the share of hours the blowers ran and so counts the methane drawn off after each restart a second time. Not Tier 1 at 348 t, which divides the capture by 0.90 as if the waste generated nothing while the blowers were down.

## 2. Critical Components

1. Methane captured in 2026 is **3,166 t**.
2. Methane generated in 2026 is **3,600 t** (nearest 100).
3. Methane released in 2026 is **410 t** (nearest 10), in Tier 2.

## 3. Step-by-Step Solution

1. Summed each hour's FT-101 flow at normal conditions times its AT-101 methane content times 0.7168 kg (rule 1.3) in BH_gas_plant_hourly_2024-2026.csv over the 2026 local year (rule 1.1): 3,166 t captured.
2. Set the 38 blower outages of BH_gas_plant_outage_log_2024-2026.xlsx (343.65 hours down) against the historian: after each restart the capture runs above its pre-outage level while the wells draw off methane the waste held during the stop, 66 t over the year.
3. Read the waste's generation from the steady hours (full blower hours outside the outages and those recoveries), month by month at the 0.90 collection efficiency of Schedule 2 for the geomembrane cap (BH_site_register_2025.xlsx), over every hour of the year (rule 1.2): 3,600 t.
4. Applied rule 1.6 with Schedule 2's 0.10 cap oxidation and 0.99 destruction efficiency: 410 t released, Tier 2 at $118,000 under rule 5.1.
5. Engine hours and starts (rules 1.7 and 1.8) from BH_engine_plant_events_2026.txt: synchronised time from RUNNING to the next STOP or TRIP, both engines running when the year opens, each utility power failure ending the run at the failure's start in the outage log (the controller writes only CONTROLLER POWER UP when the supply returns), and a RUNNING after BREAKER OPEN not counted as a start.
6. Flare figures: its gas by difference at the plant (FT-101 less FT-201 and FT-202, all normal cubic metres) times the methane content, 0.7168 kg and 0.99 (rule 1.5); its hours from TEMP PERMISSIVE or TEMP NORMAL to the next LOW TEMP or FLARE STOP in the event log, with the flare lit when the year opens.
7. Surface monitoring from BH_surface_emissions_monitoring_2026.xlsx: readings above 503 ppm (500 over the background), the third quarter's readings between the passing morning check and the failed midday check in SEM_analyser_checks_2026.csv void under plan section 7.3, each location's first re-monitoring matched by position after converting its WGS84 fix to the site grid by the site register's tie.
8. The 2027 budget carries $118,000 for the Tier 2 charge.

## 4. Deliverable Answers

### breck_hollow_charge_brief_2026.pdf

1. Tier 2 of the closed landfill methane charge.
2. Charge for the 2027 budget: $118,000.
3. Chart of the 2026 methane released (410 t) as a bar against the 375 t and 450 t tier thresholds, the tier bands shaded and labelled.

### breck_hollow_methane_return_2026.xlsx

1. Methane generated in 2026: 3,600 t.
2. Methane captured in 2026: 3,166 t.
3. Methane released in 2026: 410 t.
4. Each engine's operating hours and starts by quarter:
   - Q1: Engine 1 2,016 h and 17 starts; Engine 2 2,017 h and 16 starts
   - Q2: Engine 1 2,040 h and 16 starts; Engine 2 2,073 h and 16 starts
   - Q3: Engine 1 2,120 h and 12 starts; Engine 2 2,082 h and 14 starts
   - Q4: Engine 1 2,119 h and 16 starts; Engine 2 2,112 h and 17 starts
5. The flare's operating hours and methane destroyed in it by quarter:
   - Q1: 1,994 h, 53 t
   - Q2: 2,054 h, 55 t
   - Q3: 1,765 h, 35 t
   - Q4: 780 h, 24 t
6. Each quarterly walkover's locations over 500 ppm and those still over at their first re-monitoring:
   - Q1: 7 locations, 2 still over
   - Q2: 8 locations, 4 still over
   - Q3: 7 locations, 2 still over
   - Q4: 6 locations, 2 still over
