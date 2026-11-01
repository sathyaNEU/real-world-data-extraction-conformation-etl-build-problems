## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: the grid emission factor that credits an on-site solar array, the operating margin of the store's balancing area in the hours the array generates).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Corvane should site its 2027 on-site solar pilot at its Gorsefield store (store 2291).**
Its array would have avoided 0.89 t of grid carbon dioxide per MWh it generated in 2025, the area's coal fleet following the load from 5 am to 6 pm while gas carries the nights; Halvane is the first store left out at 0.58, 0.31 below. Not Brackwell, highest on the agency's 2025 average output emission rate (0.85 t/MWh): by day its coal runs at full output and gas follows the load, so its array avoids 0.40. Not Quillbury, highest on the non-baseload rate (1.11): its old coal units run on winter evenings, after sunset, and its array avoids 0.39. Not Tennaford, highest on a marginal rate fitted to every hour of 2025: coal follows its load at night and gas through its business day, and its array avoids 0.41.

## 2. Critical Components

1. Gorsefield's array avoids **0.89** t of carbon dioxide per MWh of its 2025 output.
2. Halvane is the first store left out at **0.58** t/MWh, **0.31** below Gorsefield.
3. Quillbury, highest on the agency's 2025 non-baseload output emission rate (**1.11** t/MWh), avoids **0.39** t/MWh: its old coal units run after sunset.

## 3. Step-by-Step Solution

1. Matched each store to its balancing area through its delivery utility in utility_balancing_area_map.csv, reading Kestrel Point's rows filed under its former code KPLP as KSTP (balancing_area_codes.csv).
2. Put balancing_area_hourly_operating_data_2025.csv (each hour named by its end, UTC) and pilot_array_output_model_2025.csv (each hour named by its start, local standard time) on one UTC clock.
3. Computed each area's hourly fossil carbon dioxide from its coal, gas and oil net generation at the 2025 fuel output emission rates in edc_generation_emission_rates_2025.xlsx, pounds per MWh converted to tonnes.
4. Estimated each area's marginal emission rate for each season and local standard hour as the slope of the hour-to-hour change in that carbon dioxide on the change in the area's net generation, interchange being scheduled a day ahead (solar_pilot_siting_charter_2027.pdf).
5. Weighted each hour's rate by the store's modelled output, as the charter's measure of what an array avoids: Gorsefield 0.89, Halvane 0.58, the other six 0.39 to 0.41 t/MWh.
6. Took each meter's 2025 metered kWh, each bill's days in 2025 pro rata, from its delivery utility's distribution energy quantity in corvane_electricity_invoice_lines_fy2025.csv (Tennaford's blocks summed) where the utility's own invoice reached accounts payable, and for the cycles after the store's main account moved to Halworth Utility Payment Services (lines without a quantity) from Ardley Retail Energy's bill for the same cycle, its first-term bills (those with the renewable portfolio standard line) over the meter's loss factor (its quantity over the meter's in the cycles both bill, 1.0365 to 1.0623) and its second-term bills as billed, as the two garden-centre meters confirm: uses of 1,976 to 2,862 MWh, the array's output over them 23.0 to 30.2 per cent.
7. Divided every payment for each store's 2025 electricity, the utilities' invoices, the service's lines and Ardley's invoices each counted by its days in 2025 and as made (the bill paid twice at each move was credited against the bills after it), Halvane Gas & Electric's gas charges left out, by that use: $122 to $225 per MWh.
8. Recommended Gorsefield, the store whose array would have avoided the most.

## 4. Deliverable Answers

### solar_pilot_site_recommendation_2027.pdf

1. Pilot store: Gorsefield; first store left out: Halvane, 0.31 t/MWh below.
2. Grid carbon dioxide avoided per MWh of the array's 2025 output, tonnes per MWh:
   - Gorsefield: 0.89
   - Halvane: 0.58
   - Tennaford: 0.41
   - Brackwell: 0.40
   - Quillbury: 0.39
   - Kestrel Point: 0.39
   - Faraview: 0.39
   - Ostlemere: 0.39
3. 2025 metered electricity use, MWh:
   - Gorsefield: 2,570
   - Halvane: 2,507
   - Tennaford: 2,458
   - Brackwell: 2,373
   - Quillbury: 2,338
   - Kestrel Point: 2,462
   - Faraview: 1,976
   - Ostlemere: 2,862
4. Share of 2025 use the array would have supplied, per cent:
   - Gorsefield: 28.5
   - Halvane: 27.1
   - Tennaford: 27.0
   - Brackwell: 26.6
   - Quillbury: 23.0
   - Kestrel Point: 27.6
   - Faraview: 24.0
   - Ostlemere: 30.2
5. Paid for electricity per MWh used in 2025, dollars:
   - Gorsefield: 146
   - Halvane: 142
   - Tennaford: 137
   - Brackwell: 155
   - Quillbury: 183
   - Kestrel Point: 225
   - Faraview: 122
   - Ostlemere: 170
6. Chart: each store's 2025 monthly metered use against its array's modelled monthly output, one panel per store, on page 2.

### pilot_sites_hourly_avoided_emissions_2025.csv

1. 70,080 rows, one per store and local standard hour of 2025: store, balancing area, the hour's start in UTC and local standard time, the array's output in kWh, the hour's marginal carbon dioxide rate in t/MWh and the carbon dioxide avoided in kg.
2. Each store's avoided carbon dioxide over its array's output equals its figure in the memo.
