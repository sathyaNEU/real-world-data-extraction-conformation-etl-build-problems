## Tags

**Domain:** Criminology & Justice (recidivism risk assessment).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Reserve 500 GPS enrolments in Region 4's 2027 Belvantis order: 500 people on the 31 December 2026 caseload will be booked on a new Category V charge in 2027 while still supervised.** Not the 400 a risk model on the caseload's own records gives, which misses the roughly 530 supervisees the Halverton police recorded as victims of violence in 2026.

## 2. Critical Components

1. The caseload at the end of 31 December 2026 is **7,688** people.
2. About **530** of them were recorded by the Halverton police as victims of a violent incident that occurred in 2026, against about **210** on the 2025 year-end caseload for incidents in 2025.
3. On the 2018 to 2025 year ends, supervisees with a police victim record in the prior twelve months were booked on a Category V charge the next year at **30.7%**, against **4.4%** for the rest.

## 3. Step-by-Step Solution

1. Read darrow_county_jail_booking_notices_2018-2026.csv (one booking per booking_no) and keswick_county_jail_bookings_2018-2026.xlsx (UTC converted to Merrow time), kept new arrests per Directive 26-07 section 2, read former sections through criminal_code_conversion_table_2024.pdf and flagged Category V charges by the directive's Appendix: 5,676 Category V new-arrest bookings of supervisees from 2018 to 2026.
2. Built each year end's caseload from cms_supervision_episodes_2018-2026.csv, an episode open from its start date through its close date and each person counted once: 7,688 people at the end of 2026.
3. Matched the individual victims in hpd_violent_incident_victims_2018-2026.csv to the caseload on surname, the first word of the given name and date of birth, the names in capitals with the suffixes JR, SR, II, III and IV and every character but a letter dropped, each victimization dated by the incident's occurred date: about 530 of the 2026 year-end caseload victims in 2026, about 210 of the 2025 year-end caseload in 2025.
4. Fitted a logistic model of a Category V new-arrest booking in the next calendar year while supervised on the 2018 to 2025 year ends (age, sex, prior felonies, lead offence family, supervision type, county, city residence, months to expiration, first year of supervision, latest MRAS total with legacy numbers through oms_cms_person_crosswalk_2022.csv, prior-year new-arrest and Category V bookings, and a police victim record in the prior twelve months), where victims book at 30.7% against 4.4%.
5. Scored the 2026 year-end caseload and summed the probabilities: 495.0, 500 to the nearest 100 (the same model without the victim records gives 413.7).
6. Rebuilt each client's held days in belvantis_r4_device_events_2025-2026.json from effective dates with voided events dropped, a legacy offender number and its case-management id per oms_cms_person_crosswalk_2022.csv read as one client, removed suspended days, every day the client spent any part of in either jail per both booking files and every day after Region 4's supervision ended per cms_supervision_episodes_2018-2026.csv, a transfer between Darrow and Keswick counties continuing it (Schedule C, belvantis_service_schedule_2025.pdf): 75,758 enrolment days in 2026.
7. For each supervisee's Halverton police Category V arrest, once per supervisee and incident at its first booking, counted the distinct Halverton residences of the incident's individual victims in hpd_violent_incident_victims_2018-2026.csv across the original report and its supplements (Directive 26-07 section 4, unit marks and street types read alike) in the month of that booking: 143 zones in 2026.
8. Reserve 500 enrolments for 2027.

## 4. Deliverable Answers

### region4_2027_category_v_forecast.docx

1. 500 people booked on a new Category V charge in 2027 while still supervised, to the nearest 100.

### region4_2027_gps_order.xlsx

1. Forecast: 500.
2. Enrolment days owed to Belvantis for 2026, whole days:
   - January: 6,256
   - February: 5,669
   - March: 6,334
   - April: 6,140
   - May: 6,348
   - June: 5,872
   - July: 6,241
   - August: 6,418
   - September: 6,093
   - October: 6,572
   - November: 6,820
   - December: 6,995
3. Exclusion zones the directive would have set in 2026 for the Halverton police's Category V arrests of supervisees, whole zones:
   - January: 9
   - February: 17
   - March: 16
   - April: 13
   - May: 13
   - June: 11
   - July: 13
   - August: 11
   - September: 11
   - October: 13
   - November: 8
   - December: 8
