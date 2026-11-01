## Tags

**Domain:** Urban & Regional Science (forecasting: a forestry company's FY2028 log truck loads to its export port once the 50MAX route limits apply).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The FY2028 harvest plan needs 29,100 export log loads to Port Kowhai under the 50MAX route limits.**
By grade: A grade 4,900; Pruned 2,500; K grade 7,550; KI grade 8,050; KIS grade 6,100 loads. Not 26,900, the figure from letting every 50MAX unit's load rise to 50 tonnes gross less its tare, which the short grades cannot reach because their bunks are full a few tonnes above today's payloads. Not 27,300, which lifts only the loads that sat at the 44-tonne limit and still carries them to the new mass limit. Not 25,700, which adds six tonnes to the fleet's average payload.

## 2. Critical Components

1. FY2026 port loads as recorded: **29,981 loads** carrying **764,046 tonnes**.
2. The FY2028 plan's export tonnes: **808,900 tonnes**.
3. **71 per cent** of FY2026 port loads were hauled by units holding a 50MAX permit.

## 3. Step-by-Step Solution

1. Matched each ticket in weighbridge_tickets_port_kowhai_FY2026.csv to the scaling record in log_scaling_port_kowhai_FY2026.csv of the same truck within the following hour, giving each load's JAS volume and density: 29,981 loads, 764,046 tonnes.
2. Read each load's unit from fleet_register_2026-06-30.xlsx by registration (previous registrations included), with its tare, 50MAX permit and full-bunk volume for the grade's length in export_log_grade_specifications_2025.pdf.
3. Set each load's FY2028 payload (planning basis 3.1 and 3.2, RDC-2026-114) as the lesser of its unit's FY2028 gross limit (50 tonnes with a permit, 44 without) less tare and its full-bunk volume times the load's density.
4. Divided harvest_plan_FY2028.xlsx's export tonnes for each grade by the grade's average FY2028 payload and summed: 29,100 loads.
5. Cartage: summed cartage_invoices_FY2026.csv lines, credit notes included, against the fleet register's carrier of the unit on each line's port weighbridge ticket (subcontracted units are billed under their head contractor's code).
6. Domestic deliveries: summed gross less tare in mill_weighbridge_logs_FY2026.csv for loads carrying a Matiri docket (MFP), by quarter of the weigh-in date (planning basis 4.2); mill_dockets_FY2026.csv dates loads when the docket was posted.
7. FY2028 needs 29,100 export log loads under the 50MAX route limits.

## 4. Deliverable Answers

### matiri_fy2028_log_cartage_loads.xlsx

1. Export log loads needed in FY2028: 29,100.
2. FY2028 loads by grade, nearest 50:
   - A grade: 4,900
   - Pruned: 2,500
   - K grade: 7,550
   - KI grade: 8,050
   - KIS grade: 6,100
3. Per-load working: each FY2026 port load with its unit, tare, JAS volume, density, full-bunk volume and FY2028 payload.
4. FY2026 export cartage by the carrier whose unit hauled the load, NZD thousand:
   - Ruahine Log Cartage Ltd: 2,073
   - Kereru Haulage Ltd: 1,811
   - Tutaekuri Transport Ltd: 1,632
   - Wilson & Heke Trucking Ltd: 1,158
   - Kinross Contracting Ltd: 1,008
   - Patoka Logging Haulage Ltd: 1,012
5. FY2026 domestic deliveries by mill and quarter, tonnes, nearest 10:
   - Mohaka Sawmills: July to September 2025 14,090, October to December 2025 12,000, January to March 2026 12,600, April to June 2026 13,130
   - Ahuriri Timber Processors: July to September 2025 10,870, October to December 2025 8,680, January to March 2026 8,700, April to June 2026 9,780
   - Heretaunga Box and Lumber: July to September 2025 5,340, October to December 2025 4,610, January to March 2026 5,610, April to June 2026 5,440

### fy2028_loads_by_grade.svg

1. Grouped bar chart of loads by grade, FY2026 recorded beside FY2028 needed, each FY2028 bar labelled with its rounded figure and the total in the title.
