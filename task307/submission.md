## Tags

**Domain:** Energy Systems & Utilities (hydropower asset condition and maintenance).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Sørdal Kraft should spend its 2027 summer runner refurbishment on Nesvik G1, sparing 67,000 MWh of generation in the 2027 to 2031 planning window.**
Its runner R-501 stands at 2,250 cm2 of pitting and passes the repair limit in 2027, so the refurbishment spares 4,650 MWh per NOK million against Sørdal G1's 3,820, a lead of 830. Not Nesvik G2, which carries the most pitting at the oldest inspection but runs little in its restricted band and stays under the limit through 2031. Not Øvre Sørdal G1 or G2, whose winter generation per kroner is the fleet's highest but whose runners stay under the limit in the window.

## 2. Critical Components

1. Pitting per hour run from 30 per cent of rating up to 58 per cent, every inspection pair in the register: **0.24 cm2**
2. Nesvik G1's runner R-501: **1,050 cm2** at its last inspection, **2,250 cm2** at the end of 2026, past the limit in **2027**
3. Generation spared per NOK million: Nesvik G1 **4,650** (67,000 MWh over NOK 14.4 million), Sørdal G1 **3,820**, lead **830**

## 3. Step-by-Step Solution

1. Took each unit's present runner from unit_register.xlsx and its pitting at its last inspection from runner_inspections.xlsx (the total over blades and band as TS-07 defines pitting, after any repair).
2. Put historian_export_2016_2023.csv (Norwegian time) and historian_export_2023_2026.csv (UTC) on one hourly clock, each hour once.
3. Counted each unit's hours with output from 30 per cent of its rating up to 58 per cent (the restricted band in unit_register.xlsx) and found, across every pair of consecutive inspections of a runner in runner_inspections.xlsx, the same pitting per band hour, 0.24 cm2, the Sørdal G3 peaker's pairs included, where pitting per running hour differs tenfold between the peaker and the base-load runners.
4. Carried each present runner from its last inspection to 31 December 2026 at that rate, then year by year at its 2026 band hours as outage_planning_note_2027.docx carries duty: Nesvik G1 in 2027, Sørdal G1 in 2029, Sørdal G3 in 2031 pass the repair limit in the window and no other runner does.
5. Valued each passing runner's 14-week outage at the unit's mean generation over the 14 weeks from 1 December in the winters 2021/22 to 2025/26, as the planning note values an outage, and divided by the quotation excluding VAT in runner_refurbishment_quote_2027.pdf: Nesvik G1 4,650, Sørdal G1 3,820, Sørdal G3 990 MWh per NOK million.
6. Ask: assigned each old historian slot tag, before its station's RTU replacement in maintenance_history.csv, to the unit whose logged overhauls and annual maintenance its zero hours match, rather than through historian_tag_map_2023.csv, which holds the wiring since; then summed each unit's hourly output.
7. Ask: counted starts as production_report_2025.pdf defines them, every run-up from standstill: the hourly record's changes from zero to generation, plus each generator breaker trip in protection_log_2016_2026.csv resynchronised with no standstill hour between (the governor start counters in unit_counter_readings.csv tie between every pair of readings only so); counted trips as each unit's own generator breaker trips plus each 132 kV line breaker trip at its station (unit_register.xlsx, Stasjoner: one line per station) in an hour the unit was generating.
8. Refurbish Nesvik G1 in the 2027 summer window: it spares 67,000 MWh, 4,650 MWh per NOK million.

## 4. Deliverable Answers

### runner_2027.xlsx

1. Each unit's runner, pitting at its last inspection, pitting at 31 December 2026, the year it passes the repair limit if in 2027 to 2031, the generation the outage would then cost and that per NOK million:
   - OSD-G1: R-301, 1,260 cm2 (inspected 6 September 2022), 1,650 cm2 now, not before 2032, 0 MWh, 0 MWh per NOK million
   - OSD-G2: R-302, 650 cm2 (inspected 18 August 2020), 1,250 cm2 now, not before 2032, 0 MWh, 0 MWh per NOK million
   - SDL-G1: R-205, 910 cm2 (inspected 6 July 2021), 1,990 cm2 now, 2029, 55,800 MWh, 3,820 MWh per NOK million
   - SDL-G2: R-410, 570 cm2 (inspected 11 July 2023), 880 cm2 now, not before 2032, 0 MWh, 0 MWh per NOK million
   - SDL-G3: R-208, 0 cm2 (inspected 25 June 2024), 890 cm2 now, 2031, 14,100 MWh, 990 MWh per NOK million
   - NSV-G1: R-501, 1,050 cm2 (inspected 10 August 2021), 2,250 cm2 now, 2027, 67,000 MWh, 4,650 MWh per NOK million
   - NSV-G2: R-502, 1,350 cm2 (inspected 4 June 2019), 1,790 cm2 now, not before 2032, 0 MWh, 0 MWh per NOK million
2. Unit chosen: NSV-G1 (Nesvik G1); runner-up: SDL-G1 (Sørdal G1); gap: 830 MWh per NOK million (4,650 against 3,820)
3. Generation, starts and trips each unit has had since the start of 2016, to 31 December 2026:
   - OSD-G1: 4,542,200 MWh, 427 starts, 22 trips
   - OSD-G2: 4,464,600 MWh, 423 starts, 16 trips
   - SDL-G1: 2,427,200 MWh, 433 starts, 23 trips
   - SDL-G2: 2,710,000 MWh, 501 starts, 20 trips
   - SDL-G3: 557,900 MWh, 6,738 starts, 15 trips
   - NSV-G1: 2,900,000 MWh, 383 starts, 26 trips
   - NSV-G2: 3,370,200 MWh, 400 starts, 18 trips

### runner_2027.svg

1. Bar chart of generation spared in 2027 to 2031 per NOK million by unit, Nesvik G1's bar marked "refurbish 2027": OSD-G1 0, OSD-G2 0, SDL-G1 3,820, SDL-G2 0, SDL-G3 990, NSV-G1 4,650, NSV-G2 0.
