## Tags

**Domain:** Criminology & Justice, recidivism risk assessment (a county's 2027 felony probation revocation admissions under a statute capping felony supervision at 24 months and barring extension past it, forecast from its two probation case systems, the Circuit Court's term orders, violation petitions and offense classes, and the jail's bookings).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Okelan County's 2027 Jail Operations Plan should staff 7 violator pods (448 beds) for felony probation revocation admissions.**
The projection is 1,424 admissions (1,414 to 1,443 across the standing variants of its construction), more than the 1,260 that six pods cover and within the 1,470 of seven under the county's standard of one pod for each 210 admissions or part of 210. A felony term running out with a matter still open is extended where it has room under its class maximum and draws a violation petition where it has none: about two in five of the record's terms reaching their last 120 days at their class maximum drew a petition, in every offense class including drug felony class 4 with its 24-month maximum, against 6 per cent of the terms with room. SB 26-118 leaves no capped term any room, so the 3,114 running terms it ends on 31 March 2027 and every term reaching 24 months end at the at-maximum rate. Not 5 pods, which the two-clock projection at the record's pooled end-of-term rate gives (911): that rate was earned by terms that could mostly still be extended. Not 4, the trailing year's 827 admissions.

## 2. Critical Components

1. **3,114** of the felony terms open at 30 September 2026 end on 31 March 2027 under section 4 of SB 26-118 (supervision begun by 31 March 2025, scheduled expiration later than 31 March 2027), and section 5 lets no order from 1 January 2027 set a term's expiration past its end under the Act, so none of them has room to be extended.
2. Of the record's felony terms reaching their last 120 days before the scheduled expiration in force, **about two in five** of those at their class maximum had a violation petition filed in those days, in every offense class including drug felony class 4 with its 24-month maximum, against **6 per cent** of those with room, more than half of which were extended instead.
3. The 2027 projection is more than **1,260** admissions, the six pods' cover, and no more than **1,470**, the seven pods' cover, under every standing variant of its construction (1,424 as built, 1,414 to 1,443 across the variants) and the standard of one pod for each 210 admissions or part of 210, so **7** pods.

## 3. Step-by-Step Solution

1. Joined the felony terms of cms1_supervision_cases_2016_2023.csv and cms2_supervision_cases_2023_2026.csv (offense class, supervision begin, term), the term orders in circuit_court_term_orders_2016_2026.csv (each scheduled expiration in force and each extension), the longest term for each class in circuit_court_codes.xlsx and the petitions in circuit_court_violation_petitions_2016_2026.csv: 7,841 felony terms open at the extract.
2. Applied sections 3 to 5 of sb26_118_felony_probation_term_act.pdf: each open term ends at the earlier of its scheduled expiration and the later of the day 24 calendar months after supervision began and 31 March 2027 (3,114 of them on 31 March 2027), and no term may be extended past that end.
3. Split the end-of-term windows the record saw (the last 120 days before a scheduled expiration then in force, the term alive and on supervision when they opened) by whether the term in force (imposed plus the extensions ordered before the window opened) had reached its class maximum: about two in five of the windows at the maximum had a petition filed in them, against 6 per cent of the windows with room, more than half of which ended in an extension instead.
4. Projected 2027 under the Act at the record's rates (jail_operations_plan_instructions_2027.pdf, section 4), each term's exposure counted from 1 July 2016, the first day of the extracts: the petition hazard by month on supervision outside the windows, each term leaving as it is revoked or terminated early at the record's rates; each open term's last 120 days before its end under the Act (from 1 January 2027 for the 31 March ends), the window's petition share applied per term on the record's filing days, at the at-maximum share where the Act or the class leaves no room and at the with-room shares otherwise (an extended term running 12 months more, or to the latest end the Act allows if sooner, then ending with no room); pending petitions; new supervision starts at the trailing year's rate; the record's revocation rates and filing-to-decision days: 1,424 admissions.
5. Checked the standing variants (an end-of-term window of 90, 105 or 150 days, the CSRS score as a covariate, one revocation rate, the mean lag, the 31 March windows opening before 1 January 2027, only the windows of terms with nothing pending, a term with room extended 9 months, or to the latest end the Act allows): 1,414 to 1,443 admissions, seven pods throughout; the pooled end-of-term rate gives 911 (5 pods), the lost extensions shared between petition and lapse in proportion 1,140 (6), every one a petition 1,780 (9), and the trailing year's 827 admissions carried forward 4.
6. For the bed-days, read the new jail system's UTC times in county time, chained each person's bookings (annex moves, the system replacement, reclassifications), counted each midnight a person was serving a commitment the court had ordered, from the night after the order (a held probationer stays booked PV-HOLD until the order reaches the jail) to the release the bookings record, and each midnight of a weekend sentence's stays, and took the level from the term revoked: a PV-FEL booking of a misdemeanor revocation is misdemeanor, and a night on a felony and a misdemeanor commitment at once is felony.
7. For the probationers, took each open felony term's officer in cms2_supervision_cases_2023_2026.csv and that officer's office in the assignments in effect on 30 September 2026 (apd_officer_assignments_2016_2026.csv), with time on supervision in completed years at the extract.
8. Applied the county's standard in the instructions' annex (one 64-bed pod for each 210 admissions or part of 210; six pods cover 1,260, seven 1,470): 7 pods for the projection's 1,424 admissions.

## 4. Deliverable Answers

### violator_housing_plan_2027.xlsx

1. Violator pods for 2027: 7 (448 beds).
2. The 2027 projection behind them: more than 1,260 felony probation revocation admissions (six pods' cover) and no more than 1,470 (seven pods' cover).
3. Violator bed-days, whole days:
   - October to December 2025: felony 24,603, misdemeanor 2,272
   - January to March 2026: felony 25,141, misdemeanor 2,228
   - April to June 2026: felony 23,135, misdemeanor 2,043
   - July to September 2026: felony 23,897, misdemeanor 2,475
4. Felony probationers on supervision on 30 September 2026, by supervising office (the office of the officer supervising the term that day) and time on supervision in completed years (under one year, one to under two years, two to under three years, three years or more):
   - Central: 1,029, 926, 672, 769
   - Northgate: 491, 427, 252, 366
   - Riverside: 557, 471, 299, 384
   - Eastfield: 355, 323, 234, 286

### violator_housing_memo_2027.docx

1. The plan's violator housing section: seven pods, the 3,114 terms ending on 31 March 2027 and the capped terms' end-of-term petitions at the rate of the terms already at their class maximum.

### felony_revocation_admissions_2019_2027.png

1. A line chart of monthly felony probation revocation admissions from January 2019 to September 2026 with the 2027 projection by month, peaking in April 2027.
