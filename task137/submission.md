## Tags

**Domain:** Healthcare delivery and health economics (utilization, access and demand forecasting).
**Analytical objective:** Forecasting and predictive modelling.

## 1. Final Recommendation

**Plan for 45,000 GP-referred visits at the community phlebotomy hub in 2027-28.**
Underlying 2025-26 GP-referred demand was about 41,800 to 42,000 visits, about 2,600 to 2,800 more than the walk-in clinic saw or turned away, because practices with their own phlebotomy clinics kept patients in-house for eight weeks after the clinic's run-out weeks; grown 3.5 per cent a year for two years it is about 44,800 to 45,000. Not 42,500, from 2025-26's seen plus turned away (39,218 grown), which leaves out the patients the practices kept, or from a model of the previous week's run-outs or ten days of them, which sees only the start of the fall. Not 40,000, from the patients seen alone, which also leaves out the patients turned away.

## 2. Critical Components

1. GP-referred visits seen in 2025-26: **37,853**.
2. GP-referred patients turned away in 2025-26: **1,365**, on **56** of 253 clinic days the tickets ran out.
3. How long the run-outs hold GP-referred arrivals down, the window the record's fit picks from one to twelve weeks: **eight weeks**.
4. 2025-26 underlying GP-referred demand, with that window's run-outs taken out: **about 41,800 to 42,000**.

## 3. Step-by-Step Solution

1. Counted each clinic day's GP-form and hospital-form visits from walkin_tickets_legacy_2023-04_to_2024-11.csv (Outcome Seen) to 17 November 2024 and from the CHECKED_IN events in phlebotomy_queue_events_2024-11-18_to_2026-09-30.csv (UTC read as UK time) from 18 November 2024: 37,853 GP-referred visits seen in 2025-26.
2. Read both layouts of reception_turned_away_log.xlsx (the GP and hospital boxes of both shifts in the 2023-24 and 2024-25 sheets, one line per run-out day from 2025-26, month totals left out): 1,365 GP-form patients turned away on 56 clinic days in 2025-26.
3. Took each Monday-to-Friday week's run-out share (its logged run-out days over its clinic days) and modelled each clinic day's GP-referred arrivals (seen plus turned away), April 2023 to September 2026, as Poisson in weekday, month, a linear trend, the day after a bank holiday and the mean share of the previous L weeks, L from one to twelve by AIC: eight weeks, every window of five weeks or fewer at least 67 worse, coefficient about -0.37 (standard error 0.026), the fall sitting with the practices whose phlebotomy_les_2025-26 is Y in gp_practices_catchment.csv.
4. Took the GP-referred arrivals of every clinic day of 2025-26 with that effect removed: about 41,800 to 42,000 visits (the eight-week window and the nine-week window next to it in fit), grown 3.5 per cent a year for two years to about 44,800 to 45,000, 45,000 to the nearest 2,500.
5. Named each 2025-26 hospital request's clinic code: forms issued before 16 March 2026 carry the old PAS's codes, which outpatient_clinic_codes.csv does not hold, and each old code is the new code whose forms issued in the second half of March 2026 fall on the same weekdays as the old code's, before the clinics changed their sessions in April (the register's clinic_days name all seven wrongly); then counted hospital-form visits by specialty and financial quarter of the visit date.
6. Counted sickness in eroster_phlebotomy_2023-04_to_2026-09.csv as the holders' Sickness lines plus the lines shown unassigned (Vacant line Y) from a sickness's sixth clinic day until the same holder returns, which are filled posts, the one vacant post being the post the annual report names (vacant from 14 July to 12 September 2025, as section 4 states); working days lost at 7.5 hours each and the rate over every clinic day of every filled post, by financial quarter.
7. Charted each Monday-to-Friday week of 2025-26, GP-referred visits seen, turned away and kept in-house, in gp_demand_2025-26.png.

## 4. Deliverable Answers

### hub_plan_2027-28.xlsx

1. GP-referred blood-test visits to plan for at the hub in 2027-28: 45,000.
2. Hospital-clinic visits to the walk-in clinic in 2025-26 by financial quarter of the visit, Q1 to Q4:
   - Cardiology: 1,797, 389, 357, 397
   - Diabetes and endocrinology: 632, 675, 3,280, 651
   - Gastroenterology: 240, 257, 250, 286
   - General medicine: 330, 320, 334, 323
   - Haematology: 424, 437, 454, 495
   - Renal medicine: 378, 361, 398, 440
   - Rheumatology: 406, 376, 343, 2,192
3. Working days lost to sickness and the sickness absence rate, by financial quarter of 2025-26:
   - Q1 (April to June): 29 days, 6.8 per cent
   - Q2 (July to September): 23 days, 5.6 per cent
   - Q3 (October to December): 39 days, 8.7 per cent
   - Q4 (January to March): 23 days, 5.2 per cent

### gp_demand_2025-26.png

1. Stacked bars for each Monday-to-Friday week of 2025-26: GP-referred visits seen, turned away and kept in-house by the practices with their own phlebotomy clinics.
