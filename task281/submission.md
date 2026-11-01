## Tags

**Domain:** General Statistics & Data Science (robustness analysis: whether an autonomous diabetic retinopathy screening AI's validated sensitivity holds at each clinic of a community health center network).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**In 2027 run RetinaCheck at Standard at Orrin Falls, Pellsbury, Quarry Hill, Sallow Creek, Thistlebrook, Wendmere and Yarrowby, at Enhanced at Kestle Road and Veldane, and at High at Brackenfield, Hollinmoor and Rookwood; on the 2025-26 screenings these points imply 6,630 referrals, within Pellam's capacity of 7,200.** Not Standard everywhere: the pooled validation sensitivity of 89.4% at Standard mixes images from two camera models, 73.3% on the NR-40 and 95.7% on the NR-70, and five clinics screened mostly or wholly on an NR-40. Not High at Kestle Road and Veldane, where the register now shows NR-40 loaners: 68% and 58% of their year ran on an NR-40, which puts both above 85% at Enhanced and below it at Standard.

## 2. Critical Components

1. Validation sensitivity by camera model at Standard, Enhanced, High and Maximum: NR-40 **73.3%, 82.2%, 90.1%, 96.0%**; NR-70 **95.7%, 97.3%, 98.8%, 98.8%**.
2. Share of each clinic's 2025-26 screenings captured on an NR-40: **100%** at Brackenfield, Hollinmoor and Rookwood, **68%** Kestle Road, **58%** Veldane, **18%** Sallow Creek, **8%** Pellsbury, **6%** Orrin Falls, **6%** Yarrowby, **0%** at Quarry Hill, Thistlebrook and Wendmere.
3. Brackenfield, Hollinmoor and Rookwood reach **90%** at High after **82%** at Enhanced; Kestle Road and Veldane clear 85% at Enhanced and fall short at Standard; the other seven clinics are at **92%** or more at Standard.
4. The points chosen for 2027 imply **6,630** referrals on the 2025-26 screenings against Pellam's **7,200**; High at every clinic would imply 9,204.

## 3. Step-by-Step Solution

1. Placed every image on its camera: validation images by the protocol's site letters (validation_study_protocol_2025.pdf) and capture_date, 2025-26 screenings by Site (clinic_directory.csv) and Captured (UTC) moved to Pacific local date; the camera is the serial the Location History sheet of biomed_asset_register_2026-09-30.xlsx places at the clinic's location that day, its model from the Assets sheet.
2. From local_validation_study_2025.csv, counted as referable a final_level of moderate NPDR or worse or a final_dme of Y, and as referred an Ungradable result or a dr_score at or above the point's threshold (the CAI-03 definitions of referable disease and sensitivity, retinacheck_operating_points.pdf): NR-40 73.3% and NR-70 95.7% at Standard.
3. Weighted each model's sensitivity at every point by its share of the clinic's screenings in retina_ai_results_2025-10_2026-09.csv (a screening belongs to the clinic where it was captured): Brackenfield, Hollinmoor and Rookwood 90% at High, the seven Standard clinics 92% or more at Standard.
4. Took each clinic's least sensitive point at or above 85% (CAI-03 section 3) and counted the screenings it would have referred, an Ungradable result or a DR Score at or above its threshold: 6,630, within the 7,200 in pellam_reading_agreement_2027.pdf.
5. For the reading center figures, kept the cases in pellam_overread_log_2025-26.csv whose Referral Order is a REF7734 referral in ehr_retinal_screening_orders_2025-26.csv (the IMG92250 teleretinal reads are not AI referrals), took each referral order as one referral closed by its last Referable or Not referable grade, and counted days from its first case's Image Date to the closing grade's Graded (UTC) on the Pacific calendar, as CAI-03 section 4 states the measure.
6. For the camera faults, took the retinal camera tickets in biomed_service_tickets_2025-26.csv, ended each outage when the Location History moved the next camera into the clinic (not at the ticket's Closed date), and counted the weekdays after the fault day with no screening in the result export (the fault day itself had screenings before the camera failed).
7. Recommended Standard at seven clinics, Enhanced at Kestle Road and Veldane and High at Brackenfield, Hollinmoor and Rookwood.

## 4. Deliverable Answers

### ai_operating_points_2027.xlsx

1. 2027 operating point by clinic:
   - Brackenfield: High
   - Hollinmoor: High
   - Kestle Road: Enhanced
   - Orrin Falls: Standard
   - Pellsbury: Standard
   - Quarry Hill: Standard
   - Rookwood: High
   - Sallow Creek: Standard
   - Thistlebrook: Standard
   - Veldane: Enhanced
   - Wendmere: Standard
   - Yarrowby: Standard
2. Referrals each clinic's point implies on the 2025-26 screenings, whole counts:
   - Brackenfield: 754
   - Hollinmoor: 791
   - Kestle Road: 518
   - Orrin Falls: 540
   - Pellsbury: 410
   - Quarry Hill: 488
   - Rookwood: 686
   - Sallow Creek: 447
   - Thistlebrook: 451
   - Veldane: 578
   - Wendmere: 496
   - Yarrowby: 471
3. Network: 6,630 referrals against Pellam's 2027 capacity of 7,200, within capacity.
4. AI referrals Pellam read from the 2025-26 screenings, whole counts, and the share whose closing grade is Referable, whole per cent:
   - Brackenfield: 423 read, 49%
   - Hollinmoor: 420 read, 43%
   - Kestle Road: 392 read, 47%
   - Orrin Falls: 523 read, 53%
   - Pellsbury: 395 read, 48%
   - Quarry Hill: 471 read, 47%
   - Rookwood: 366 read, 49%
   - Sallow Creek: 423 read, 48%
   - Thistlebrook: 436 read, 56%
   - Veldane: 411 read, 48%
   - Wendmere: 483 read, 48%
   - Yarrowby: 462 read, 55%
5. Average days from screening to Pellam's closing grade by quarter of screening, one decimal:
   - Oct-Dec 2025: 6.3
   - Jan-Mar 2026: 6.2
   - Apr-Jun 2026: 6.4
   - Jul-Sep 2026: 6.3
6. Clinic days with no AI screening after each camera fault in the reference year, whole days:
   - Kestle Road, fault reported 2026-01-28: 7
   - Orrin Falls, fault reported 2026-02-10: 3
   - Veldane, fault reported 2026-03-05: 6
   - Sallow Creek, fault reported 2026-03-30: 4
   - Yarrowby, fault reported 2026-05-01: 5
   - Pellsbury, fault reported 2026-06-03: 7

### operating_points_2027_committee.pptx

1. Heatmap on the slide with one row per clinic and one column per vendor point (Standard, Enhanced, High, Maximum), each cell the clinic's estimated sensitivity and each clinic's point for 2027 outlined: Standard at seven clinics, Enhanced at Kestle Road and Veldane, High at Brackenfield, Hollinmoor and Rookwood.
