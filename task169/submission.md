## Tags

**Domain:** Criminology & Justice (recidivism and risk assessment).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Carry a two-year return rate of 20 per cent for the 6,466 people the Department expects to release to parole in 2027.** Under Act 26-114 the Board recommits no one, so every parolee's arrest goes to court and comes back as a new commitment at the courts' own rate. Not the record's new-commitment returns, which count only the arrests the Board left to the courts. Not the record's return rate of every kind, which counts recommitments the Act ends.

## 2. Critical Components

1. The 2027 cohort is **6,466** people on the projected-release extract.
2. The two-year return rate under the Act is **20 per cent**.

## 3. Step-by-Step Solution

1. Read release movements PAR and RPR (PAROLE and REPAROLE before the 2022 upgrade) dated 1 January 2019 to 30 September 2024 in doc_release_movements_2019-2026.csv, each followed 730 days: 30,959 releases.
2. Linked sbi_arrests_released_persons_2019-2026.parquet to Department numbers through sbi_doc_number_crosswalk.csv and counted, for each release, every arrest (the ones the Board revoked on included) and the days out of Department custody (ADM to the next release movement in doc_admission_movements_2019-2026.csv) in four bands of time since release; fitted a Poisson model of arrests per day on age, prior commitments, offence, sex and district.
3. Matched every arrest linked to a Department number and dated on or before 30 June 2024 (25,117, arrests on a release day included) to its case in aoc_case_dispositions_2019-2026.csv on otn (a docket's latest entry): the 9,410 the Board revoked on (an arrest_otn on a REVOKE or REVOKED decision in its two case files) were all nolle prossed (9,410 of 9,410, against 374 of the 15,707 others), so their record outcome is the Board's, not a court's; of the 15,707, 3,483 ended in a DOC sentence (sentence_type DOC; CJ and PROB are not returns), by the arrest's top charge grade felony A-B 1,622 of 2,594, felony C-E 1,673 of 6,400, misdemeanour 188 of 6,713, with the arrest-to-ADM time of those sentenced.
4. Checked that rate where the Board could not revoke: of the 10,576 arrests made on or after the maximum expiration date of the parole release before them, 2,357 ended in a DOC sentence (felony A-B 1,092 of 1,748, felony C-E 1,143 of 4,338, misdemeanour 122 of 4,490), the same rates; every arrest with the revoked ones in gives 3,483 of 25,117, which counts the Board's revocations as court outcomes.
5. For each person in doc_projected_releases_2027.csv, sent every arrest the model expects in 730 days at liberty through those courts' rates for the grade mix of the person's governing offence, each timed by the arrest-to-ADM time, and took the share with a return (1 minus e to the minus the expected returns): 20.4 per cent, 20 per cent to the step.
6. Took REVOKE and REVOKED decisions dated 1 July 2025 to 30 June 2026, dropped the legacy entries dated after the legacy system closed on 2 January 2026 and those rescinded by 30 June 2026, and counted one recommitment per parolee per hearing date (two cases decided together are one order), on a reported arrest when any of its cases cites an arrest number.
7. Took each detainer once (one per legacy case; a carried-over case from the new system), ended a legacy detainer with no lift date at the person's next ADM in doc_admission_movements_2019-2026.csv, merged each parolee's overlapping detainers, and counted days from the lodge day to the day before the end in each half of 2025 by the district of the county jail.
8. Ended each writ trip (a WRO in doc_admission_movements_2019-2026.csv; no person has two open at once) at the person's next WRI or, where a release movement in doc_release_movements_2019-2026.csv comes first, at the release, and counted days from the day out to the day before the trip ended in each half of 2025 by the WRO's institution.

## 4. Deliverable Answers

### returns_projection_2027.xlsx

1. Two-year return rate of the 2027 parole releases under Act 26-114: 20 per cent.
2. Recommitments the Board ordered from 1 July 2025 to 30 June 2026 and had not rescinded by 30 June 2026:
   - D1 (Garrison): 1,277 that took up a reported arrest, 261 on conditions alone
   - D2 (Ridgway): 621 that took up a reported arrest, 210 on conditions alone
   - D3 (Linwood): 368 that took up a reported arrest, 172 on conditions alone
   - D4 (Corliss): 116 that took up a reported arrest, 149 on conditions alone
3. Parolee-days held on Board detainers in each district's county jails, 2025:
   - Garrison: January to June 34,613, July to December 35,500
   - Ridgway: January to June 21,409, July to December 23,962
   - Linwood: January to June 17,928, July to December 19,163
   - Corliss: January to June 10,241, July to December 10,611
4. Days people spent out on court writs, by the institution they left, 2025:
   - SCI-KTR: January to June 3,443, July to December 4,237
   - SCI-FNW: January to June 3,838, July to December 4,166
   - SCI-DNM: January to June 3,896, July to December 4,122
   - SCI-LKV: January to June 3,957, July to December 4,546
   - SCI-BRW: January to June 3,947, July to December 4,497
