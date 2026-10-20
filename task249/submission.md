## Tags

**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: turbidity surrogates for the suspended-sediment loads a consultancy publishes for a hydropower company).  
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**Re-issue the published 2027 loads of four stations, SKB, JVB, FND and ESK, all over by more than 15 per cent; the other ten stand.** At those four the calibration samples were taken mostly on rising water, when a unit of turbidity carries more sediment, and the published regression carries that into every hour of the year. Not the published regression refitted, which reproduces every load; not discharge, season or the trip type added to it, which leave the rising-water samples' excess in the year's other hours.

## 2. Critical Components

1. The procedure's regression refitted on the same samples reproduces all 14 published loads to within **0.1 per cent**.
2. With an indicator of rising water at each sample, the relation of concentration to turbidity is higher on rising water at SKB, JVB, FND and ESK, and the trip type then adds nothing at any station.
3. Over by more than 15 per cent: **SKB, JVB, FND and ESK**; under: none; within: the other **ten**.

## 3. Step-by-Step Solution

1. Joined field_samples_2025-2027.csv to lims_ssc_results_2025-2027.xlsx on year and bottle number (final results; both sheets) and paired each sample, at its UTC time, with the station's nearest 15-minute turbidity reading in sediment_stations_15min_2025-2027.parquet.
2. Refitted SMP-03 section 6 (log10 concentration on log10 turbidity, Duan's smearing) and applied it to 2027's intervals (section 7): every load in suspended_sediment_loads_2027.pdf to within 0.1 per cent.
3. Marked each sample and each 2027 interval as on rising water when the 15-minute discharge's rate of rise, averaged over the hour, exceeded 1.5 per cent an hour (any threshold from 0 to 3 per cent an hour gives the same four), and added that indicator to each station's regression with Duan's smearing.
4. Applied each station's relation to every 15-minute interval of 2027 with that interval's own indicator, summed concentration times discharge times 900 seconds, and compared the published load with it (section 8, 15 per cent either way): SKB, JVB, FND and ESK over, none under.
5. Counted, per station, the 15-minute intervals of 2025 and 2026 with no row, flagged fouled or sonde out (F and M, and G and O before the data team's migration of 14 April 2026, which the maintenance log's cleaning visits match; K and C are checks and usable), or at 1,000 FNU before the station's TS-40W was installed (station register, maintenance log), re-sent rows once, and divided by four.
6. Took each 2027 batch in lab_batch_export_2027.csv once, computed each control aliquot as net mass over volume against its lot's concentration in SMA_quality_statement_2027.pdf (KS-26-11 50.0, KS-27-06 54.0 mg/L), applied section 4's three checks, and counted each station's sample lines in the 12 failed batches.
7. Re-issue the 2027 loads of SKB, JVB, FND and ESK.

## 4. Deliverable Answers

### sediment_load_review_2027.xlsx

1. Verdict on each station's published 2027 load (15 per cent either way):
   - SKB Skardbreelvi ved Fossbru: over by more than 15 per cent, re-issue
   - KVF Kvitfonnelvi ovf. inntak: within 15 per cent, stands
   - MKE Morkaelvi ved Steinbru: within 15 per cent, stands
   - JVB Juvbreelvi ved Juvstøl: over by more than 15 per cent, re-issue
   - HGE Hogstølelvi: within 15 per cent, stands
   - FND Fonnadalselvi ved Bruhaug: over by more than 15 per cent, re-issue
   - ESK Eskelandselvi: over by more than 15 per cent, re-issue
   - TVE Tverrelvi ved Lid: within 15 per cent, stands
   - GRV Grovelvi: within 15 per cent, stands
   - SVK Sandvikelvi: within 15 per cent, stands
   - HSD Haugsdalselvi: within 15 per cent, stands
   - BLU Blåvatn utløp: within 15 per cent, stands
   - SLU Svartevatn utløp: within 15 per cent, stands
   - LLU Langevatn utløp: within 15 per cent, stands
2. Hours in 2025 and 2026 without a usable turbidity reading, whole hours:
   - SKB: 702
   - KVF: 459
   - MKE: 647
   - JVB: 238
   - HGE: 460
   - FND: 757
   - ESK: 507
   - TVE: 400
   - GRV: 450
   - SVK: 433
   - HSD: 696
   - BLU: 543
   - SLU: 340
   - LLU: 673
3. 2027 samples weighed in a batch that failed its quality control:
   - SKB: 5
   - KVF: 0
   - MKE: 6
   - JVB: 5
   - HGE: 12
   - FND: 9
   - ESK: 10
   - TVE: 12
   - GRV: 9
   - SVK: 6
   - HSD: 12
   - BLU: 5
   - SLU: 10
   - LLU: 8

### station_loads_2027.png

1. Each of the 14 stations' published 2027 load against the review's estimate on a log scale, the four outside the tolerance (SKB, JVB, FND, ESK) in bold.
