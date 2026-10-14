# task459 submission

## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (ten offered gas plants' carbon dioxide per net megawatt-hour, built from EPA's hourly emissions records and the plants' revenue meters and read at each offer's Contract Capacity).
**Analytical objective:** Data Extraction & Conformation (ETL) (EPA's hourly emissions per turbine stack, the sellers' revenue meters, the EIA generator inventory and the offers conformed into each plant's emission rate under its commitment, with its 2025 forced outages from the GADS records and its substitute-data hours from EPA's measure indicators).

## 1. Final Recommendation

**Fill 990 MW of the 1,000 MW need with Juniper Draw (500 MW), Kessling Creek (245 MW) and Ashby Gulch (245 MW): seven offered plants emit 791 to 892 pounds of CO2 per net megawatt-hour at their Contract Capacities, and taken in order of capacity price, each whole, these three fit the need while Sorrel Butte, second by price, would take it to 1,030 MW.**

The deciding figure is each plant's rate at its Contract Capacity, the output the commitment holds it at in every hour, read from the 294 to 1,020 hours of 2024 and 2025 in which its revenue meter shows it delivering that capacity; Tamarack Landing (971), Coldbrook (982) and Brenmoor Mill (1,064) emit more than 925 and cannot be signed. Not the 2025 annual averages: Sorrel Butte, Ashby Gulch and Kessling Creek average 986 to 998 because their starts and part-load hours are in them, and Tamarack Landing averages 902 on its unfired base load though its 630 MW Contract Capacity needs its duct burners in every hour, so the averages fill the need with Tamarack Landing and Moraine Point, 905 MW. Not the plants' highest-output hours: Juniper Draw's are duct-fired (940) though it offers its unfired capability, and they fill it with Sorrel Butte and Kessling Creek, 775 MW.

## 2. Critical Components

1. Seven offers, **2,375 MW**, comply: Sorrel Butte, Kessling Creek, Ochre Flat, Juniper Draw, Lindgren Hill, Ashby Gulch and Moraine Point emit at or under 925 pounds per net megawatt-hour at their Contract Capacities.
2. Tamarack Landing emits **971** pounds per net megawatt-hour at its **630 MW** Contract Capacity (957 to 985 across the windows and curves), above the standard, though its 2025 average is 902.
3. Sorrel Butte, Kessling Creek and Ashby Gulch emit **892**, **884** and **885** at their Contract Capacities (889 to 893, 882 to 887 and 882 to 887), under the standard their 2025 averages exceed.
4. In order of capacity price, Juniper Draw is taken (**500 MW**), Sorrel Butte passed over (**1,030 MW**), Kessling Creek taken (**745 MW**), Moraine Point passed over (**1,020 MW**) and Ashby Gulch taken (**990 MW**); Lindgren Hill and Ochre Flat would make **1,255** and **1,305 MW**.

## 3. Step-by-Step Solution

1. Read section 5 of calder_pud_rp7_resource_procurement_procedure.pdf and sections 1, 3 and 5 of rfo2026_baseload_request_for_offers.pdf: a plant complies if the CO2 it emits per megawatt-hour of net generation it delivers under the commitment does not exceed 925 pounds, compared unrounded; the commitment is the plant's entire output at its Contract Capacity in every hour; the 1,000 MW need is filled from the complying offers in order of capacity price, each taken whole, passing over any that would take the total above 1,000 MW.
2. Joined each offer in rfo2026_offers_received.xlsx to its plant by EIA plant code, Kessling Creek and Ashby Gulch by name and county in eia860_2025_generator_offered_plants.xlsx.
3. Summed each plant's stacks' CO2 in camd_hourly_emissions_offered_units_2024-2025.csv by facility ID and local standard hour (Moraine Point's CT-1 and 1A together) and matched each hour to rfo2026_offer_meter_data_2024-2025.csv by its start and UTC offset.
4. Because each plant's rate moves with its output (below 75 per cent of their Contract Capacities Sorrel Butte, Kessling Creek, Ashby Gulch and Brenmoor Mill emit 14 to 20 per cent more per megawatt-hour than at them), divided each plant's CO2 by its metered net generation over the 2024 and 2025 hours its meter shows it within 2 per cent of its Contract Capacity, every stack operating the full hour (294 to 1,020 hours a plant); windows of 1, 3 and 5 per cent, 2025 alone and curves fitted from 80 or 90 per cent of the Contract Capacity leave every plant on the same side of 925.
5. Compared each rate with 925 unrounded: seven offers comply, 2,375 MW; Tamarack Landing (971), Coldbrook (982) and Brenmoor Mill (1,064) do not.
6. Filled the need from the seven in order of the capacity prices in rfo2026_offers_received.xlsx: Juniper Draw, Kessling Creek and Ashby Gulch taken, 990 MW; Sorrel Butte, Moraine Point, Lindgren Hill and Ochre Flat passed over.
7. For the workbook, took each plant's forced outages (types U1, U2, U3 and SF) from rfo2026_offer_gads_events_2025.csv, each unit's latest entry for an outage's start standing (EPA's hourly records show the plant running inside the three first estimates that ran long), the whole plant off line when every combustion turbine or the single-shaft unit is out, hours in 2025 Pacific time per rfo2026_evaluation_data_dictionary.txt; and counted the 2025 clock hours in which an operating stack's Heat Input Measure Indicator reads Substitute, EPA's CO2 being calculated from heat input (camd_monitoring_plans_offered_units.csv).
8. Recommendation: sign Juniper Draw, Kessling Creek and Ashby Gulch, 990 MW of the 1,000 MW need.

## 4. Deliverable Answers

### eps_determination_rfo_2027.pdf

1. 990 MW of the 1,000 MW need can be filled under the 925-pound standard, from Juniper Draw (500 MW), Kessling Creek (245 MW) and Ashby Gulch (245 MW); Sorrel Butte, Moraine Point, Lindgren Hill and Ochre Flat comply and are passed over; Tamarack Landing, Coldbrook and Brenmoor Mill do not comply.
2. Bar chart of every offered plant's rate against the 925 line on page 2 of the determination, the three plants signed darkest and the complying offers passed over lighter.

### offered_plants_eps_2027.xlsx

3. Every offered plant's emission rate at its Contract Capacity, in whole pounds of CO2 per net megawatt-hour, any figure in the bracketed range correct:
   - Tamarack Landing (BL26-01, 630 MW): 971 (957 to 985)
   - Juniper Draw (BL26-02, 500 MW): 890 (886 to 891)
   - Sorrel Butte (BL26-03, 530 MW): 892 (889 to 893)
   - Coldbrook (BL26-04, 415 MW): 982 (978 to 984)
   - Moraine Point (BL26-05, 275 MW): 876 (872 to 877)
   - Ochre Flat (BL26-06, 315 MW): 791 (788 to 792)
   - Lindgren Hill (BL26-07, 265 MW): 876 (875 to 878)
   - Ashby Gulch (BL26-08, 245 MW): 885 (882 to 887)
   - Kessling Creek (BL26-09, 245 MW): 884 (882 to 887)
   - Brenmoor Mill (BL26-10, 170 MW): 1,064 (1,064 to 1,067)
4. Each plant's forced outage hours and forced outages in 2025, Pacific time (the whole plant off line):
   - Tamarack Landing: 23 hours, 2 outages
   - Juniper Draw: 15 hours, 2 outages
   - Sorrel Butte: 22 hours, 3 outages
   - Coldbrook: 17 hours, 1 outage
   - Moraine Point: 85 hours, 7 outages
   - Ochre Flat: 193 hours, 5 outages
   - Lindgren Hill: 46 hours, 2 outages
   - Ashby Gulch: 16 hours, 3 outages
   - Kessling Creek: 84 hours, 5 outages
   - Brenmoor Mill: 56 hours, 4 outages
5. The clock hours each plant operated in 2025 with its CO2 resting on substitute data:
   - Tamarack Landing: 73
   - Juniper Draw: 93
   - Sorrel Butte: 81
   - Coldbrook: 124
   - Moraine Point: 22
   - Ochre Flat: 23
   - Lindgren Hill: 53
   - Ashby Gulch: 33
   - Kessling Creek: 15
   - Brenmoor Mill: 37
