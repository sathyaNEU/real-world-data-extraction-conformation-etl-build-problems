## Tags

**Domain:** General Statistics & Data Science (robustness analysis: whether an autonomous diabetic retinopathy screening AI's validated sensitivity holds at each clinic of a community health center network).
**Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**In 2027 run RetinaCheck at Standard at Orrin Falls, Pellsbury, Quarry Hill, Sallow Creek, Thistlebrook, Wendmere and Yarrowby, and at High at Brackenfield, Hollinmoor, Kestle Road, Rookwood and Veldane; on the 2025-26 screenings these points imply 7,076 referrals, within Pellam's capacity of 7,500.** Not Standard everywhere: the validation study pooled images from two camera models, and at Standard the AI referred 58 of 90 referable patients imaged on the NR-40 against 378 of 390 on the NR-70, while five clinics screened 90% or more of their year on an NR-40. Not Standard at Kestle Road and Veldane, where the register now shows their NR-70s back: 90% and 91% of their year ran on NR-40 loaners.

## 2. Critical Components

1. Validation study, referable patients the AI referred at Standard, Enhanced, High and Maximum: NR-40 **58, 70, 80 and 89 of 90**; NR-70 **378, 389, 390 and 390 of 390**.
2. Share of each clinic's 2025-26 screenings captured on an NR-40: **100%** at Brackenfield, Hollinmoor and Rookwood, **91%** Veldane, **90%** Kestle Road, **11%** Sallow Creek, **8%** Pellsbury, **6%** Orrin Falls, **6%** Yarrowby, **0%** at Quarry Hill, Thistlebrook and Wendmere.
3. Weighted by those shares, the five clinics stay under 85% at Enhanced and clear it at High; the other seven clear it at Standard.
4. The points chosen for 2027 imply **7,076** referrals on the 2025-26 screenings against Pellam's **7,500**; High at every clinic would imply 9,261.

## 3. Step-by-Step Solution

1. Placed every image on its camera: validation images by the protocol's site letters (validation_study_protocol_2025.pdf) and capture_date, 2025-26 screenings by Site (clinic_directory.csv) and Captured (UTC) moved to Pacific local date; the camera is the serial the Location History sheet of biomed_asset_register_2026-09-30.xlsx places at the clinic's location that day, its model from the Assets sheet.
2. From local_validation_study_2025.csv, counted as referable a final_level of moderate NPDR or worse or a final_dme of Y, and as referred an Ungradable result or a dr_score at or above the point's threshold (the CAI-03 definitions of referable disease and sensitivity, retinacheck_operating_points.pdf), referred over referable cases by camera model: NR-40 58 of 90 and NR-70 378 of 390 at Standard.
3. Weighted each model's proportion at every point by its share of the clinic's screenings in retina_ai_results_2025-10_2026-09.csv (a screening belongs to the clinic where it was captured): Brackenfield, Hollinmoor, Kestle Road, Rookwood and Veldane fall short of 85% at Enhanced and clear it at High; the other seven clear it at Standard.
4. Took each clinic's least sensitive point at or above 85% (CAI-03 section 3) and counted the screenings it would have referred, an Ungradable result or a DR Score at or above its threshold: 7,076, within the 7,500 in pellam_reading_agreement_2027.pdf.
5. For the reading center figures, kept the cases in pellam_overread_log_2025-26.csv whose Referral Order is a REF7734 referral in ehr_retinal_screening_orders_2025-26.csv (the IMG92250 teleretinal reads are not AI referrals), took each referral order as one referral closed by its last Referable or Not referable grade, and counted days from its first case's Image Date to the closing grade's Graded (UTC) on the Pacific calendar, as CAI-03 section 4 states the measure.
6. For the camera faults, took the retinal camera tickets in biomed_service_tickets_2025-26.csv, ended each outage when the Location History moved the next camera into the clinic (not at the ticket's Closed date), and counted the weekdays after the fault day with no screening in the result export (the fault day itself had screenings before the camera failed).
7. Recommended Standard at seven clinics and High at Brackenfield, Hollinmoor, Kestle Road, Rookwood and Veldane.

## 4. Deliverable Answers

### ai_operating_points_2027.xlsx

1. 2027 operating point by clinic:
   - Brackenfield: High
   - Hollinmoor: High
   - Kestle Road: High
   - Orrin Falls: Standard
   - Pellsbury: Standard
   - Quarry Hill: Standard
   - Rookwood: High
   - Sallow Creek: Standard
   - Thistlebrook: Standard
   - Veldane: High
   - Wendmere: Standard
   - Yarrowby: Standard
2. Referrals each clinic's point implies on the 2025-26 screenings, whole counts:
   - Brackenfield: 755
   - Hollinmoor: 793
   - Kestle Road: 705
   - Orrin Falls: 549
   - Pellsbury: 415
   - Quarry Hill: 498
   - Rookwood: 690
   - Sallow Creek: 452
   - Thistlebrook: 464
   - Veldane: 763
   - Wendmere: 508
   - Yarrowby: 484
3. Network: 7,076 referrals against Pellam's 2027 capacity of 7,500, within capacity.
4. AI referrals Pellam read from the 2025-26 screenings, whole counts, and the share whose closing grade is Referable, whole per cent:
   - Brackenfield: 391 read, 43%
   - Hollinmoor: 395 read, 39%
   - Kestle Road: 355 read, 41%
   - Orrin Falls: 521 read, 54%
   - Pellsbury: 395 read, 48%
   - Quarry Hill: 484 read, 48%
   - Rookwood: 336 read, 44%
   - Sallow Creek: 440 read, 49%
   - Thistlebrook: 442 read, 56%
   - Veldane: 366 read, 43%
   - Wendmere: 486 read, 49%
   - Yarrowby: 461 read, 57%
5. Average days from screening to Pellam's closing grade by quarter of screening, one decimal:
   - Oct-Dec 2025: 6.3
   - Jan-Mar 2026: 6.3
   - Apr-Jun 2026: 6.8
   - Jul-Sep 2026: 6.5
6. Clinic days with no AI screening after each camera fault in the reference year, whole days:
   - Kestle Road, fault reported 2025-10-13: 4
   - Veldane, fault reported 2025-10-16: 6
   - Orrin Falls, fault reported 2026-02-10: 3
   - Sallow Creek, fault reported 2026-03-30: 4
   - Yarrowby, fault reported 2026-05-01: 5
   - Pellsbury, fault reported 2026-06-03: 7

### operating_points_2027_leadership.pptx

1. Heatmap on the slide with one row per clinic and one column per vendor point (Standard, Enhanced, High, Maximum), each cell the clinic's estimated sensitivity and each clinic's point for 2027 outlined: Standard at seven clinics, High at Brackenfield, Hollinmoor, Kestle Road, Rookwood and Veldane.
