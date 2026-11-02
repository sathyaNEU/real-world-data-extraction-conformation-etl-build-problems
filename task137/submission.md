## Tags

**Domain:** Actuarial Science & Insurance (claims frequency and severity: a self-insured delivery fleet's collision claims for a year on a new route schedule, priced per kilometre on clock time and light).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The delivery trucks will make 350 collision claims in 2027: 150 from April to September and 200 in the other six months.**
The 2027 schedule drives 23.3 per cent of its kilometres before sunrise or after sunset, against 7.6 per cent in the record, at about 2.6 times the daylight collision rate at the same clock time. Not 300, the record's rate per kilometre by time of day, which prices the small hours at the summer schedule's daylight rate.

## 2. Critical Components

1. Kilometres planned for 2027 driven before sunrise or after sunset (driver handbook Appendix C, UK clock time): **23.3 per cent**, against **7.6 per cent** of the kilometres driven October 2023 to September 2026
2. A kilometre driven in the dark carries about **2.6 times** the collision rate of a daylight kilometre in the same clock band

## 3. Step-by-Step Solution

1. Read both Gridtrak exports (miles to kilometres, the overlap week once, UTC to UK clock time by the handbook's summer-time rule) with each truck's depot from fleet_register_2026-10.xlsx, to 30 September 2026.
2. Took the trucks' claims from ravensby_fleet_claims_listing_2026-10-31.xlsx per the fund terms (cars, duplicates and withdrawn notifications out) to 30 September 2026: 840 claims.
3. Spread each run's kilometres evenly over its clock hours and split them at its depot's sunrise and sunset from driver_handbook_2026.pdf Appendix C: 7.6 per cent of the record's kilometres in the dark.
4. Fitted a Poisson rate per kilometre on clock band and light: a dark kilometre at 2.6 times a daylight one; the 04:00 to 07:00 dark kilometres of the May to August schedule had 48 claims against 37.6 expected by that model fitted without them and 23.2 at the 04:00 to 07:00 rate.
5. Carried the rates onto every route and delivery day of route_schedule_2027.xlsx: 346.9 claims, 150.7 of them from April to September and 196.3 in the other six months.
6. Counted each Brantwick invoice once in ap_ledger_brantwick_2023-10_2026-10.csv: identical lines (job, invoice date, description, net) are one invoice posted twice, except two identical ADAS calibration lines on a job for a truck the register shows with camera and radar, which are one per sensor; summed net by the truck's depot and the collision's incident date through brantwick_jobs_2023-10_2026-10.csv.
7. Placed each other insurer's receipt in claims_recovery_account_2024-10_2026-10.csv on its collision: by our claim number where quoted, else on the one claim of that payer whose net repair cost, in full for a non-fault claim or at a quarter, a third, a half, two thirds or three quarters for a split one, equals the amount to the penny; summed by the collision's quarter.
8. The fund should be set for 350 collision claims in 2027.

## 4. Deliverable Answers

### claims_fund_2027.xlsx

1. Collision claims in 2027: 350
2. April to September: 150; January to March and October to December: 200
3. Paid back by other insurers towards each quarter's collisions, received to 31 October 2026:
   - January to March 2025 collisions: £73,000
   - April to June 2025 collisions: £60,000
   - July to September 2025 collisions: £43,200
   - October to December 2025 collisions: £64,500
   - January to March 2026 collisions: £58,000
   - April to June 2026 collisions: £81,100
4. Brantwick repair cost of each depot's collisions:
   - Cramlington: £102,100 for January to June 2025 collisions, £133,000 for July to December 2025 collisions, £148,800 for January to June 2026 collisions
   - Gateshead (Team Valley): £100,600 for January to June 2025 collisions, £105,800 for July to December 2025 collisions, £110,700 for January to June 2026 collisions
   - Carlisle: £91,700 for January to June 2025 collisions, £127,400 for July to December 2025 collisions, £92,500 for January to June 2026 collisions
   - Darlington: £89,600 for January to June 2025 collisions, £67,700 for July to December 2025 collisions, £114,800 for January to June 2026 collisions

### claims_note_2027.docx

1. One-page note to the board giving 350 claims for 2027, split between April to September and the other six months, with the reason (the new schedule's dark early hours from October to March)
2. Chart of collision claims by month of incident, October 2023 to September 2026 in blue and the months of 2027 in orange as expected on the new schedule
