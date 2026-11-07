## Tags

> **Domain:** Healthcare delivery and health economics, provider quality and risk adjustment.
> **Analytical objective:** Anomaly detection and diagnostics.

## 1. Final Recommendation

**Refer GS-16 and GS-21 to professional practice review for the site infections after their April to September 2027 operations, and no other consultant.** Their infections stand above the Centre's control limit in the procedures steriliser 3's faulty loads never reached. Not GS-05 and GS-12, whose excess came from instrument trays steriliser 3 sterilised after its 12 May 2027 repair: with those operations set aside, each sits inside the limit.

## 2. Critical Components

1. Counted against the Centre's upper control limit on all their procedures, GS-05, GS-12, GS-16 and GS-21 are above it.
2. From the 12 May 2027 repair, operations whose tray was last sterilised by steriliser 3 had 115 infections against 21.7 expected, 4.3 times the rate of the department's other procedures.
3. Steriliser 3 is the CSSD's one chamber for instrument containers over 10 kg, so it sterilises every preference tray GS-05 and GS-12 own and half of GS-21's, and their operations carry most of the exposure.
4. With the exposed operations set aside, GS-16 and GS-21 stay above the limit (GS-16 35 against 22; GS-21 26 against 16) and GS-05 and GS-12 fall inside it (GS-05 4 against 11; GS-12 5 against 12).

## 3. Step-by-Step Solution

1. From theatre_operations_2022_2027.csv, kept completed procedures in the Centre's categories on their principal line, dropped returns to theatre, merged an add-on booked on its own (same patient, theatre and incision) into its operation, read GS-41 as GS-14, and took each risk index and expected infection from haisc_procedure_rates_2026.pdf (incision to closure against the cut-point).
2. From ssi_surveillance_2022_2027.csv, kept each infection's latest confirmed record and linked it to its procedure (by booking from 2025; before that by patient, category and the procedure up to three days after the recorded date), inside 30 days or 90 with an implant, once per procedure at its deepest level.
3. Set each consultant's April to September 2027 infections against the upper control limit, the 97.5th centile of a Poisson count at their expected number: GS-05, GS-12, GS-16 and GS-21 above it.
4. Matched each theatre scan in instrument_tracking_scans_2027.csv (UTC, read in Melbourne time) to its operation by patient and theatre, and took each scanned item's last passed load before the scan from steriliser_cycles_2027.csv: 362 window procedures had an item from steriliser 3 after its return to service at 14:40 on 12 May 2027 (cssd_equipment_log_2026_2027.xlsx), at 4.3 times the rate.
5. Compared each consultant's infections in the procedures left with the limit for their expected number: GS-16 and GS-21 above it, every other consultant inside; giving the exposed procedures their own rate instead files the same consultants.
6. Ask figures: each consultant's procedures in 2022 to 2024 as in step 1, and the infections linked to those procedures as in step 2, each under the procedure's responsible consultant.
7. Recommendation: refer GS-16 and GS-21.

## 4. Deliverable Answers

### ssi_review_response_2027.docx

1. Consultants referred to professional practice review: GS-16 and GS-21.
2. Every other consultant marked out: GS-03, GS-05, GS-08, GS-11, GS-12, GS-14, GS-19 and GS-23.
3. Chart: each consultant's infections in the procedures the steriliser 3 fault did not reach against their upper control limit, with GS-16 and GS-21, the only bars over it, in red.
4. Finding outside the consultants' practice: steriliser 3, from its repair on 12 May 2027.

### ssi_review_figures_2027.csv

1. Procedures, whole numbers:
   - GS-03: 2022 552, 2023 556, 2024 525
   - GS-05: 2022 501, 2023 489, 2024 526
   - GS-08: 2022 563, 2023 536, 2024 563
   - GS-11: 2022 536, 2023 540, 2024 573
   - GS-12: 2022 515, 2023 536, 2024 505
   - GS-14: 2022 556, 2023 561, 2024 550
   - GS-16: 2022 515, 2023 513, 2024 528
   - GS-19: 2022 561, 2023 566, 2024 550
   - GS-21: 2022 497, 2023 484, 2024 530
   - GS-23: 2022 541, 2023 560, 2024 542
2. Infections after them, whole numbers:
   - GS-03: 2022 17, 2023 17, 2024 14
   - GS-05: 2022 28, 2023 29, 2024 26
   - GS-08: 2022 16, 2023 24, 2024 22
   - GS-11: 2022 18, 2023 17, 2024 17
   - GS-12: 2022 27, 2023 26, 2024 34
   - GS-14: 2022 26, 2023 15, 2024 15
   - GS-16: 2022 28, 2023 30, 2024 36
   - GS-19: 2022 16, 2023 22, 2024 26
   - GS-21: 2022 33, 2023 29, 2024 23
   - GS-23: 2022 15, 2023 20, 2024 11
