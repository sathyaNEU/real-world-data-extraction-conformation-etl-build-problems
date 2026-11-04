## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Convert the separator level controllers at Elmworth 10-11, Elmworth 7-2, Kakwa 1-14, Kakwa 11-22, Kakwa 14-16, Kakwa 16-23, Kakwa 3-9 and Kakwa 6-27 in 2027.**
Each pad's intermittent-vent controllers vented more than the plan's 0.5 t of methane in 2026, the lowest being Kakwa 1-14 at 0.62 t, and the highest pad left out is Elmworth 14-24 at 0.41 t. Not Elmworth 12-15, Elmworth 5-3 and Kakwa 8-10, whose plunger slugs overfill their separators' level band: each slug empties the band in one dump, so the liquid-over-band count every flowing separator and the five dump counters support overstates them. Not Elmworth 4-27, Elmworth 9-34 and Kakwa 13-22, whose dry plunger wells bring slugs far smaller than the band: many arrivals go into each dump, so one dump per arrival overstates them.

## 2. Critical Components

1. Kakwa 1-14, the lowest pad in the conversion, vented **0.62 t**; Elmworth 14-24, the highest pad out, **0.41 t**.
2. The pads whose plunger slugs exceed their band vented **Elmworth 12-15 0.37 t, Elmworth 5-3 0.40 t, Kakwa 8-10 0.24 t**.
3. The pads whose dry plunger wells bring slugs far smaller than their band vented **Elmworth 4-27 0.02 t, Elmworth 9-34 0.36 t, Kakwa 13-22 0.31 t**.

## 3. Step-by-Step Solution

1. Took each separator's level band from its bore and controller span in deep_basin_equipment_register.xlsx (Vessels) and each level controller's supply gas per dump cycle from its maker's data sheet (MRS-03 4.2), at 0.02826 m3 per scf, the pad's 2026 methane fraction in gas_analyses_2025_2026.csv and 0.678 kg per m3 (MRS-03 3.3, 4.4).
2. Counted the five automated separators' dump cycles from scada_dump_counters_2026.csv over the production days (MRS-03 3.2, 4.2), each counter wrapping at 65,536.
3. Divided each flowing well's 2026 condensate and water in daily_well_volumes_2026.csv by its separator's band.
4. For each plunger well, shared each production day's liquid over that day's arrivals in plunger_cycles_2026.csv (each cycle once by controller serial and cycle count, the moved controllers placed on their wells by deep_basin_work_orders_2026.csv) and replayed the level arrival by arrival: a slug at or above the band is one dump, smaller slugs accumulate until the band fills.
5. Summed each pad's intermittent-vent methane and took the pads above 0.5 t (methane_reduction_plan_2027.docx, section 3).
6. Counted each plunger well's cycles without an arrival as the rise in its controller's cycle count less the rise in its arrival count over the production days (the PCX-300 counters), on the well each unit was on.
7. Gave each sales gas pressure controller the survey's reading where sheldrake_pneumatic_survey_2026.pdf measured that device (found by pad, model and survey date, since the re-piped pads' tags were renumbered after the survey), its maker's rating otherwise, over its own stint as the work orders and the register date it and for the hours its supply was on (MRS-03 4.3), and summed by maker and area.
8. Recommended converting the 8 pads above the line.

## 4. Deliverable Answers

### larchmere_source_inventory_2026.xlsx

1. Methane each intermittent-vent controller vented in 2026, kilograms:
   - Elmworth 10-11 LC-101101: 662 kg
   - Elmworth 10-11 LC-101102: 52 kg
   - Elmworth 10-32 LC-103201: 56 kg
   - Elmworth 10-32 LC-103202: 44 kg
   - Elmworth 11-20 LC-112001: 223 kg
   - Elmworth 12-15 LC-121501: 291 kg
   - Elmworth 12-15 LC-121502: 79 kg
   - Elmworth 14-24 LC-142401: 412 kg
   - Elmworth 15-8 LC-150801: 185 kg
   - Elmworth 15-8 LC-150802: 92 kg
   - Elmworth 2-5 LC-020501: 121 kg
   - Elmworth 3-29 LC-032901: 59 kg
   - Elmworth 4-27 LC-042701: 5 kg
   - Elmworth 4-27 LC-042702: 6 kg
   - Elmworth 4-27 LC-042703: 7 kg
   - Elmworth 5-3 LC-050301: 265 kg
   - Elmworth 5-3 LC-050302: 71 kg
   - Elmworth 5-3 LC-050303: 62 kg
   - Elmworth 6-17 LC-061701: 322 kg
   - Elmworth 7-18 LC-071801: 155 kg
   - Elmworth 7-18 LC-071802: 49 kg
   - Elmworth 7-18 LC-071803: 4 kg
   - Elmworth 7-2 LC-070201: 583 kg
   - Elmworth 7-2 LC-070202: 61 kg
   - Elmworth 9-34 LC-093401: 352 kg
   - Elmworth 9-34 LC-093402: 8 kg
   - Kakwa 1-14 LC-011401: 618 kg
   - Kakwa 1-14 LC-011402: 4 kg
   - Kakwa 11-22 LC-112201: 863 kg
   - Kakwa 12-36 LC-123601: 5 kg
   - Kakwa 12-36 LC-123602: 5 kg
   - Kakwa 13-12 LC-131201: 101 kg
   - Kakwa 13-12 LC-131202: 75 kg
   - Kakwa 13-12 LC-131203: 122 kg
   - Kakwa 13-22 LC-132201: 303 kg
   - Kakwa 13-22 LC-132202: 5 kg
   - Kakwa 13-22 LC-132203: 6 kg
   - Kakwa 14-16 LC-141601: 404 kg
   - Kakwa 14-16 LC-141602: 349 kg
   - Kakwa 16-23 LC-162301: 699 kg
   - Kakwa 16-23 LC-162302: 2 kg
   - Kakwa 16-23 LC-162303: 2 kg
   - Kakwa 3-9 LC-030901: 952 kg
   - Kakwa 5-1 LC-050101: 202 kg
   - Kakwa 5-1 LC-050102: 149 kg
   - Kakwa 6-27 LC-062701: 527 kg
   - Kakwa 6-27 LC-062702: 211 kg
   - Kakwa 8-10 LC-081001: 81 kg
   - Kakwa 8-10 LC-081002: 72 kg
   - Kakwa 8-10 LC-081003: 88 kg
   - Kakwa 8-35 LC-083501: 4 kg
2. Each pad's 2026 intermittent-vent methane on the pads sheet, tonnes:
   - Elmworth 10-11: 0.71 t, in the conversion
   - Elmworth 10-32: 0.10 t
   - Elmworth 11-20: 0.22 t
   - Elmworth 12-15: 0.37 t
   - Elmworth 14-24: 0.41 t
   - Elmworth 15-8: 0.28 t
   - Elmworth 2-5: 0.12 t
   - Elmworth 3-29: 0.06 t
   - Elmworth 4-27: 0.02 t
   - Elmworth 5-3: 0.40 t
   - Elmworth 6-17: 0.32 t
   - Elmworth 7-18: 0.21 t
   - Elmworth 7-2: 0.64 t, in the conversion
   - Elmworth 9-34: 0.36 t
   - Kakwa 1-14: 0.62 t, in the conversion
   - Kakwa 11-22: 0.86 t, in the conversion
   - Kakwa 12-36: 0.01 t
   - Kakwa 13-12: 0.30 t
   - Kakwa 13-22: 0.31 t
   - Kakwa 14-16: 0.75 t, in the conversion
   - Kakwa 16-23: 0.70 t, in the conversion
   - Kakwa 3-9: 0.95 t, in the conversion
   - Kakwa 5-1: 0.35 t
   - Kakwa 6-27: 0.74 t, in the conversion
   - Kakwa 8-10: 0.24 t
   - Kakwa 8-35: 0.00 t
3. Each plunger lift well's 2026 cycles that ended without the plunger arriving:
   - LRL ELMWORTH 10-11 #2: 261 cycles
   - LRL ELMWORTH 10-32 #1: 520 cycles
   - LRL ELMWORTH 10-32 #2: 295 cycles
   - LRL ELMWORTH 12-15 #2: 305 cycles
   - LRL ELMWORTH 3-29 #1: 326 cycles
   - LRL ELMWORTH 4-27 #1: 920 cycles
   - LRL ELMWORTH 4-27 #2: 1,236 cycles
   - LRL ELMWORTH 4-27 #3: 1,856 cycles
   - LRL ELMWORTH 5-3 #2: 571 cycles
   - LRL ELMWORTH 5-3 #3: 267 cycles
   - LRL ELMWORTH 7-18 #2: 643 cycles
   - LRL ELMWORTH 7-18 #3: 834 cycles
   - LRL ELMWORTH 7-2 #2: 813 cycles
   - LRL ELMWORTH 9-34 #2: 923 cycles
   - LRL KAKWA 1-14 #2: 407 cycles
   - LRL KAKWA 12-36 #1: 713 cycles
   - LRL KAKWA 12-36 #2: 982 cycles
   - LRL KAKWA 13-22 #2: 1,310 cycles
   - LRL KAKWA 13-22 #3: 581 cycles
   - LRL KAKWA 16-23 #2: 696 cycles
   - LRL KAKWA 16-23 #3: 583 cycles
   - LRL KAKWA 8-10 #1: 744 cycles
   - LRL KAKWA 8-10 #2: 214 cycles
   - LRL KAKWA 8-10 #3: 880 cycles
   - LRL KAKWA 8-35 #1: 331 cycles
4. The sales gas pressure controllers' 2026 methane for each maker in each area, kilograms:
   - Aldous Valve and Instrument, Elmworth: 518 kg
   - Aldous Valve and Instrument, Kakwa: 256 kg
   - Corrigan Controls, Elmworth: 380 kg
   - Corrigan Controls, Kakwa: 427 kg

### controller_conversion_2027.pptx

1. Slide 1 lists the pads in the conversion with each pad's 2026 intermittent-vent methane: Kakwa 3-9 0.95 t; Kakwa 11-22 0.86 t; Kakwa 14-16 0.75 t; Kakwa 6-27 0.74 t; Elmworth 10-11 0.71 t; Kakwa 16-23 0.70 t; Elmworth 7-2 0.64 t; Kakwa 1-14 0.62 t.
2. Slide 2 is a bar chart of every pad's 2026 intermittent-vent methane in descending order against a dashed line at the plan's 0.5 t, the conversion pads in blue.
