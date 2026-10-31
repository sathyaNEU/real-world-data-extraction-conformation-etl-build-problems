## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: a secondary aluminium works' product carbon intensities under a car maker's supplier carbon requirement).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Velden pays Brackwell Alloys EUR 342,000 in low-carbon premium on its 2027 call-offs: EUR 38 a tonne on 7,200 t of 6063 extrusion billet and 1,800 t of LM25 foundry ingot, the two families at or under SCR-2's 0.235 t CO2/t in 2026.**
6082 extrusion billet (0.26 t CO2/t) and the LM25-TF sand castings (0.50) are over the limit and earn nothing on their 3,000 t and 650 t. The homogenizing furnace burns gas by the hours its loads soak, and a 6082 load soaks about 15 hours against about 6 for 6063; shared by tonnes, the two billet alloys come out level and 6082 would wrongly qualify.

## 2. Critical Components

1. 2026 specific direct emissions, t CO2 per tonne produced: 6063 billet **0.21** and LM25 ingot **0.17**, at or under 0.235; 6082 billet **0.26** and LM25-TF castings **0.50**, over it.
2. The homogenizing furnace's gas follows its firing hours, not its tonnes: 6082 loads take **47 per cent** of its hours on 26 per cent of its billet.
3. 2026 production, tonnes that passed final inspection (each lot at its last result): 6063 billet 22,897, 6082 billet 8,205, LM25 ingot 12,816, LM25-TF castings 2,044.
4. 2027 call-offs: 6063 billet 7,200 t, 6082 billet 3,000 t, LM25 ingot 1,800 t, castings 650 t; premium EUR 38 x 9,000 t = EUR 342,000.

## 3. Step-by-Step Solution

1. Gas: the 15-minute export moved from UTC to local time, hundreds of cubic feet x 2.83 to cubic metres before the 14 April 10:30 meter exchange, and each interval converted at the volume correction factor and calorific value of the invoice period it falls in (kWh = m3 x 1.02264 x CV / 3.6).
2. Logs: one row kept per furnace and heat (re-keyed rows dropped), each heat's tonnes spread from charge to melt-out, tower melter charges in kg, homogenizing furnace and solution oven hours from door closed or start to door opened or end, all local time.
3. Regressed each local day's kWh on casthouse tonnes melted, tower melter tonnes, homogenizing furnace hours, solution oven hours and heating degree days (base 15.5 C on the daily mean), with a constant.
4. Each family carries its casthouse heats' tonnes melted at the melting rate and its homogenizing loads' hours at the furnace's hourly rate; the castings carry the tower melter and the solution oven; the rest of the year's gas (pilot flames, heating) is shared by tonnes produced.
5. Production from the lots file at each lot's last result, PASS only; CO2 at 0.18296 kg/kWh over each family's production.
6. Premium: EUR 38 on the 2027 schedule's call-offs (months summed) of each family at or under 0.235.
7. Scrap: accepted goods-in lines joined to the weighbridge on ticket and date (tickets restart on 29 June); a one-grade load is in-weigh less out-weigh, a two-grade load's grades are the drops across its two tips, matched to the lines by their declared weights; summed by quarter of the goods-in date.
8. Dross: Midland's waste-out tickets, the out-weigh less the weighing just before the skip was lifted (the second weighing where returned metal came off first); summed by quarter.

## 4. Deliverable Answers

### velden_low_carbon_premium_2027.docx

1. Premium on the 2027 call-offs: EUR 342,000.
2. Families earning it: 6063 extrusion billet (7,200 t) and LM25 foundry ingot (1,800 t).
3. Families over the limit: 6082 extrusion billet and LM25-TF sand castings.
4. 2026 specific direct emissions, t CO2/t: 6063 extrusion billet 0.21, 6082 extrusion billet 0.26, LM25 foundry ingot 0.17, LM25-TF sand castings 0.50.
5. Chart of each family's 2026 emissions per tonne against the 0.235 limit.

### brackwell_scr2_figures_2026.csv

1. Scrap bought in, tonnes as weighed, by grade and quarter of 2026:
   - old cast aluminium: Q1 2,186, Q2 2,214, Q3 2,121, Q4 2,299
   - extrusion offcuts: Q1 2,299, Q2 2,110, Q3 1,773, Q4 2,041
   - turnings and swarf: Q1 2,024, Q2 1,845, Q3 2,200, Q4 2,188
   - used beverage cans: Q1 2,376, Q2 2,521, Q3 2,009, Q4 2,020
2. Dross sent off for recovery, tonnes as weighed: Q1 286, Q2 262, Q3 251, Q4 270.
