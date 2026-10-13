# task452 submission

## Tags

**Domain:** Physical & Environmental Sciences, emissions inventory (a lake commission's water year 2026 inventory of the total phosphorus each tributary carried into the lake, estimated from grab samples and the gage record and set against the tributary allocations of its phosphorus agreement).
**Analytical objective:** Data Extraction & Conformation (ETL) (two organisations' laboratory results across a change of laboratory, the gage operator's approved 15-minute and daily discharge records, the station register, the permitted facilities' monthly and quarterly discharge monitoring reports and the farm practice contracts with their field overlay conformed into each tributary's water year 2026 load, its upstream permitted wastewater phosphorus and its cover crop acres).

## 1. Final Recommendation

**Fund the 2027 tributary restoration projects in the Kestle River, the Hessick River and Varrow Brook.**

With each day's concentration estimated from its discharge by a rating curve fitted to the record's samples, their water year 2026 loads stand 2,160 to 2,640 kg (Kestle River), 1,140 to 1,270 kg (Hessick River) and 1,110 to 1,220 kg (Varrow Brook) above their Schedule 1 allocations, against 340 to 370 kg for Ambrey River, the next. Not Ambrey River, Orrinwood Brook and Varrow Brook, which interpolating the samples between sampling days funds: the tenth of days with the highest discharge carry 34 to 63 per cent of each tributary's load and hold 4 to 15 per cent of its water year 2026 samples, so interpolation prices them at the readings of the days around them and puts the Kestle River 4,160 kg and the Hessick River 1,060 kg under their allocations.

## 2. Critical Components

1. Kestle River's water year 2026 load is **2,160 to 2,640 kg** above its allocation, Hessick River's **1,140 to 1,270 kg** and Varrow Brook's **1,110 to 1,220 kg**.
2. Ambrey River (**340 to 370 kg**) and Orrinwood Brook (**210 to 230 kg**) are the only other tributaries above their allocations.

## 3. Step-by-Step Solution

1. Took the total phosphorus results (fraction Total) in blc_water_quality_results_2027-01-08.csv from both organisations the agreement names in 1.4, the Commission's BLC stations and the college's ACWL stations, joined to the tributaries through the Stations sheet of blc_station_register.xlsx; kept routine samples with result status Accepted and converted results reported in ug/L to mg/L: 79 to 81 samples a station over water years 2024 to 2026.
2. Built each station's daily mean discharge from the approved records, merrifield_daily_values_wy2024-wy2025.csv before water year 2026 and merrifield_unit_values_wy2026_approved.csv averaged over local calendar days in it (merrifield_data_transmittal_2026-12-14.txt; the provisional July to September file is superseded), with Dunmarsh Brook's carried from its gage by the ratio of the two drainage areas in the register.
3. Fitted at each station a rating curve of log concentration on log daily discharge with the sine and cosine of the day of the year, on every sample from step 1: concentration rises with discharge at every station (slopes 0.31 to 0.86), and the tenth of days in water year 2026 with the highest discharge carry 34 to 63 per cent of the load while holding 4 to 15 per cent of the year's samples.
4. Applied each curve to every day from 1 October 2025 to 30 September 2026, retransformed to the mean with the smearing factor (1.032 to 1.053), multiplied by the day's discharge and summed: Kestle River 16,820 kg, Hessick River 6,910 kg and Varrow Brook 4,360 kg, 44,480 kg across the ten tributaries; the same curve without the seasonal terms, with a quadratic term in discharge or with the normal-theory correction gives the full-record ranges, rounded outward to 10 kg.
5. Set each load against its allocation in Schedule 1 of brannoch_lake_phosphorus_agreement.pdf on unrounded loads (2.2) and took the three largest excesses (3.1): Kestle River 2,540 kg, Hessick River 1,250 kg and Varrow Brook 1,120 kg over, then Ambrey River 350 kg and Orrinwood Brook 210 kg, the other five under; interpolating the water year's samples across its days instead funds Ambrey River, Orrinwood Brook and Varrow Brook.
6. For each tributary's upstream permitted wastewater phosphorus (4.1(a)), kept the monthly average rows of npdes_dmr_phosphorus_wy2026.csv at each report's latest submission, converted each report to kilograms (concentration times flow, or the reported mass, times the days of its monitoring period: a month, or a calendar quarter at the smaller dischargers), and counted each outfall that the register's Streams and Facilities sheets place upstream of the compliance station on the tributary's stream network while it was in service.
7. For each watershed's cover crop acres (4.1(b)), took the contracts in farm_practice_contracts_2024-2027.csv in force for crop year 2026 at their latest amendment and shared each enrolled field's acres in practice_field_watershed_acres.csv among the watersheds it lies in; a contract's contracted acres, repeated on each of its field lines, are its fields' acres together.
8. Recommendation: fund the 2027 tributary restoration projects in the Kestle River, the Hessick River and Varrow Brook.

## 4. Deliverable Answers

### restoration_slate_2027.docx

1. The three tributaries funded for 2027: Kestle River, Hessick River and Varrow Brook.
2. Each tributary's water year 2026 load against its Schedule 1 allocation, as a range across the full-record rating curves rounded outward to 10 kg, with 10 kg of tolerance at each end (the memo's own load inside it), in the memo table's order:
   - Kestle River: 16,440 to 16,920 kg (16,820 kg) against 14,280 kg, over
   - Hessick River: 6,800 to 6,930 kg (6,910 kg) against 5,660 kg, over
   - Varrow Brook: 4,350 to 4,460 kg (4,360 kg) against 3,240 kg, over
   - Ambrey River: 3,720 to 3,750 kg (3,730 kg) against 3,380 kg, over
   - Orrinwood Brook: 2,600 to 2,620 kg (2,600 kg) against 2,390 kg, over
   - Pellow Brook: 730 to 740 kg (740 kg) against 800 kg, under
   - Fallowmere Brook: 1,070 to 1,080 kg (1,070 kg) against 1,200 kg, under
   - Dunmarsh Brook: 1,660 to 1,690 kg (1,660 kg) against 1,830 kg, under
   - Corriden River: 3,560 to 3,580 kg (3,570 kg) against 3,930 kg, under
   - Tamsell River: 3,000 to 3,020 kg (3,010 kg) against 3,490 kg, under
3. Figure 1 in the memo: a horizontal bar chart of each tributary's load with its allocation marked, the three funded tributaries in dark bars.

### tributary_loads_wy2026.csv

4. Whether each tributary gets a 2027 project: Yes for Kestle River, Hessick River and Varrow Brook; No for Fallowmere Brook, Orrinwood Brook, Tamsell River, Pellow Brook, Ambrey River, Dunmarsh Brook and Corriden River.
5. The phosphorus permitted facilities upstream of each tributary's compliance station discharged in water year 2026, to the nearest 10 kg, in the file's order:
   - Fallowmere Brook: 80 kg
   - Kestle River: 1,040 kg
   - Orrinwood Brook: 340 kg
   - Tamsell River: 310 kg
   - Varrow Brook: 480 kg
   - Hessick River: 1,050 kg
   - Pellow Brook: 170 kg
   - Ambrey River: 320 kg
   - Dunmarsh Brook: 280 kg
   - Corriden River: 540 kg
6. Each tributary's 2026 cover crop acres under the farm practice program, to the nearest 10 acres, in the file's order:
   - Fallowmere Brook: 630 acres
   - Kestle River: 1,030 acres
   - Orrinwood Brook: 1,040 acres
   - Tamsell River: 690 acres
   - Varrow Brook: 900 acres
   - Hessick River: 1,500 acres
   - Pellow Brook: 660 acres
   - Ambrey River: 1,180 acres
   - Dunmarsh Brook: 840 acres
   - Corriden River: 750 acres
