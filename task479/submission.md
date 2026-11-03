## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**EU-P1 did not keep within its 2026 VOC limit: it emitted 3.2 tons against the 2.5-ton calendar-year limit, over by 0.7 tons.**
The vents' summed flow went above RTO-1's 3,800 scfm fan in short coincidences, and the VOC above the fan's draw left untreated through PSV-31. Not the controlled figure of 1.9 tons, which applies the tested 99.4 per cent destruction to every vented pound as if the closed-vent system captured all of it. Not the hourly capacity check at 2.1 tons, which averages away coincidences that last minutes.

## 2. Critical Components

1. VOC emitted from EU-P1 in each quarter of 2026 (tons): Q1 **1.4**, Q2 **0.7**, Q3 **0.5**, Q4 **0.6**
2. Calendar 2026 total **3.2 tons** against the **2.5-ton** limit, over by **0.7 tons**
3. VOC released untreated at PSV-31 in 2026, the share of each minute's header VOC above RTO-1's 3,800 scfm draw: about **2,700 lb**

## 3. Step-by-Step Solution

1. Put batchwise4_batch_steps_2026-01-01_to_2026-07-01.csv (plant local time) and orbitas_process_operations_2026H2.parquet (UTC) on one clock with each step once, the in-flight batches' migrated history in Orbitas taken in place of their Batchwise rows, and keyed every step to vent_calculation_basis_rev7.xlsx by product and step number, the PX line's Nm3/h and kg/h converted to scfm at 68 F and to lb/hr.
2. Summed every vent's flow and VOC rate minute by minute over 2026, with RTO-1's mode from rto1_dahs_1min_2026.csv (Eastern Standard Time all year).
3. In each minute RTO-1 was in RUN, took the share of the header's VOC above the fan's 3,800 scfm (cvs1_closed_vent_system_register.xlsx) as released at PSV-31 and applied 99.4 per cent destruction (BST-25-0418_RTO-1_destruction_efficiency_report.pdf) to the rest; minutes not in RUN were uncontrolled.
4. Summed by local calendar quarter under permit B.5 and D.1: 1.4, 0.7, 0.5, 0.6 tons, 3.2 tons for 2026, over the 2.5-ton limit by 0.7 tons.
5. Ask: took each delivery once by its bill of lading, its solvent from the supplier's invoice line in ap_invoice_lines_2025-12-01_to_2027-01-29.xlsx (material SOL-07 was n-heptane drums before June 2026), its date the invoice's delivery date (the warehouse posts after its stock counts), its quantity from wms_receipts_2025-12-15_to_2027-01-08.csv, gallons at erp_material_master_2027-01-04.csv's density and kilograms at 2.20462 lb/kg.
6. EU-P1 was over its limit in 2026: 3.2 tons, 0.7 tons over.

## 4. Deliverable Answers

### eu_p1_2026_aq117.xlsx

1. AQ-117, VOC emitted from EU-P1 in each quarter of 2026 and calendar year to date (tons):
   - Q1 (Jan-Mar): 1.4 this quarter, 1.4 year to date
   - Q2 (Apr-Jun): 0.7 this quarter, 2.1 year to date
   - Q3 (Jul-Sep): 0.5 this quarter, 2.6 year to date
   - Q4 (Oct-Dec): 0.6 this quarter, 3.2 year to date
2. Pounds of each solvent delivered to the plant in 2026 (nearest 100 lb):
   - Methanol: 1,435,200
   - Toluene: 855,300
   - Isopropanol: 55,100
   - Ethyl acetate: 108,700
   - n-Heptane: 295,500
   - Isohexane: 47,900
   - Tetrahydrofuran: 88,700
3. Pounds of all solvents delivered in each quarter of 2026 (nearest 100 lb):
   - Q1: 659,500
   - Q2: 660,600
   - Q3: 775,200
   - Q4: 791,100

### eu_p1_2026_determination.docx

1. EU-P1 was over its limit: 3.2 tons of VOC in calendar 2026 against the 2.5-ton limit, over by 0.7 tons.
