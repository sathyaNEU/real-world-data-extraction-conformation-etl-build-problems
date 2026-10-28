## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error: a censored lifetime distribution read past its follow-up).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Put conversion phases P1, P3, P5, P7 and P9 into the 2027 group driver replacement program, 20,922 luminaires still on their original driver.**
Each of the five is projected at 60 to 70 per cent of its original-driver luminaires failing before their twelfth year against the 45 per cent trigger, because only Vantrel's drivers wear out and these phases were built mostly from Vantrel lots. Not all ten, which one Weibull over every conversion driver files at 68 to 71 per cent each: it reads Corvane's survivors as failures still to come, expecting more than 500 Corvane failures by the close against the 16 recorded. Not P4 or P2, the highest of the rest at 35 and 30 per cent, built mostly from Corvane lots.

## 2. Critical Components

1. Driver failures on record to 31 December 2026: **Vantrel 1,327** of 22,646 drivers and **Corvane 16** of 21,040, against the **more than 500** Corvane failures one Weibull over every driver expects
2. Vantrel's original-driver lifetime: Weibull shape **3.3**, characteristic life **9.8 years**; Corvane's drivers show no wear-out
3. Projected share failing before year 12, to the nearest 5 per cent: **P1 60, P3 70, P5 60, P7 65, P9 60**; P2 30, P4 35, P6 15, P8 15, P10 15
4. Luminaires on their original driver on 1 January 2027 in the five phases: **20,922**

## 3. Step-by-Step Solution

1. Took each luminaire's retrofit date, phase and lot from brayle_install_logs_2021-2025.xlsx (both sheet layouts, every pole-tag form) and each lot's LED driver maker from halberd_certificates_of_conformance_2020-2025.pdf: 22,646 Vantrel and 21,040 Corvane drivers.
2. Dated each original driver's failure at the completion of the first driver-replacement order on its pole (DRVR in wms_legacy_work_orders_2021-01_2023-06.csv, SL-DRV-RPL in work_orders_2023-07_2026-12.csv, the legacy orders open at the cutover counted once as MIGRATED) and each exit at its knockdown, warranty swap or pole removal order, per tpl_streetlight_lifecycle_model_note.pdf 2.2 to 2.4, every other luminaire suspended at its age on 31 December 2026.
3. Fitted the two-parameter Weibull by maximum likelihood to each driver maker's drivers (the note's 3.1): Vantrel shape 3.3 and characteristic life 9.8 years on 1,327 failures; Corvane's 16 failures show no wear-out, where one fit over both makers expects more than 500.
4. Averaged, over each phase's luminaires on their original driver on 1 January 2027, the probability of failure before the twelfth anniversary of installation given survival to their age that day, under their maker's fit: P1, P3, P5, P7 and P9 above 45 per cent, every other phase at 35 per cent or less.
5. Energy saved: each converted pole's sodium fixture from the installer's Removed column at schedule_sl_street_lighting_tariff_2026.pdf input watts against its LED at the catalog's input watts, the LED at 70 W from the completion of a glare order without a shield part where streetlight_register_2026-12-31.csv shows the pole at 70 W, to its removal order's day, for the tariff's monthly burning hours by days in service, Corrinvale's LEDs at the dimmed level for the hours corrinvale_nlc_dimming_profiles_2026.csv records.
6. Late repairs: every outage order completed in 2026, timed from the first report of the outage in customer_outage_reports_2026.csv (portal stamps converted from UTC to the local time the orders carry, phone reports placed by pole number or register address), an underground cable order's reports taken from every pole on its riser's feed in the register, an order the crews found from its creation; counted those over 72 hours (the tariff's 4.2).
7. Designated the five phases above 45 per cent: 20,922 luminaires.

## 4. Deliverable Answers

### 2027_group_driver_replacement.xlsx

1. The 2027 program: P1, P3, P5, P7 and P9, 20,922 luminaires on their original driver.
2. Projected share failing before year 12, to the nearest 5 per cent, and whether the phase goes in:
   - P1: 60 per cent, in
   - P2: 30 per cent, out
   - P3: 70 per cent, in
   - P4: 35 per cent, out
   - P5: 60 per cent, in
   - P6: 15 per cent, out
   - P7: 65 per cent, in
   - P8: 15 per cent, out
   - P9: 60 per cent, in
   - P10: 15 per cent, out
3. Energy the converted poles saved in 2026 against the sodium fixtures, whole MWh:
   - Ambrosine: 1,824
   - Corrinvale: 2,263
   - Dalwinter: 1,942
   - Fallowmere: 1,684
   - Garrick Hollow: 1,888
   - Halverne Bend: 2,188
   - Kesterbrook: 2,558
   - Larkhaven: 2,304
4. Outages repaired in 2026 that missed the 72-hour standard:
   - Ambrosine: 186
   - Corrinvale: 187
   - Dalwinter: 156
   - Fallowmere: 153
   - Garrick Hollow: 149
   - Halverne Bend: 161
   - Kesterbrook: 193
   - Larkhaven: 133

### driver_failure_projection_by_phase.png

1. One bar per phase of its projected share, the 45 per cent trigger drawn across, the five program phases set apart in colour, each bar labelled with its share to the nearest 5 per cent.
