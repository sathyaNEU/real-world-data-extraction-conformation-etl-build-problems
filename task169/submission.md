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
2. Linked sbi_arrests_released_persons_2019-2026.parquet to Department numbers through sbi_doc_number_crosswalk.csv and counted, for each release, arrests and days out of Department custody (ADM to the next release movement in doc_admission_movements_2019-2026.csv) in four bands of time since release; fitted a Poisson model of arrests per day on age, prior commitments, offence, sex and district.
3. Took from aoc_case_dispositions_2019-2026.csv each court-decided arrest's chance of a DOC sentence by grade class (felony A-B, felony C-E, misdemeanour), arrests to 30 June 2024, leaving out the arrests the Board revoked on in its two case files, and the arrest-to-ADM time of those sentenced.
4. For each person in doc_projected_releases_2027.csv, combined the arrest rate by time since release with that class mix, conversion and timing over 730 days: the cohort's rate is 20 per cent.
5. Took REVOKE and REVOKED decisions dated 1 July 2025 to 30 June 2026, dropped the legacy entries dated after the legacy system closed on 2 January 2026 and those rescinded by 30 June 2026, and counted one recommitment per parolee per hearing date (two cases decided together are one order), on a reported arrest when any of its cases cites an arrest number.
6. Took each detainer once (one per legacy case; a carried-over case from the new system), ended a legacy detainer with no lift date at the person's next ADM in doc_admission_movements_2019-2026.csv, merged each parolee's overlapping detainers, and counted days from the lodge day to the day before the end in each half of 2025 by the district of the county jail.
7. Ended each writ trip (a WRO in doc_admission_movements_2019-2026.csv; no person has two open at once) at the person's next WRI or, where a release movement in doc_release_movements_2019-2026.csv comes first, at the release, and counted days from the day out to the day before the trip ended in each half of 2025 by the WRO's institution.
8. Carried 20 per cent in the projection.

## 4. Deliverable Answers

### returns_projection_2027.xlsx

1. Two-year return rate of the 2027 parole releases under Act 26-114: 20 per cent.
2. Recommitments the Board ordered from 1 July 2025 to 30 June 2026 and had not rescinded by 30 June 2026:
   - D1 (Garrison): 1,277 that took up a reported arrest, 261 on conditions alone
   - D2 (Ridgway): 621 that took up a reported arrest, 210 on conditions alone
   - D3 (Linwood): 368 that took up a reported arrest, 172 on conditions alone
   - D4 (Corliss): 116 that took up a reported arrest, 149 on conditions alone
3. Parolee-days held on Board detainers in each district's county jails, 2025:
   - Garrison: January to June 34,632, July to December 35,505
   - Ridgway: January to June 21,448, July to December 23,962
   - Linwood: January to June 17,928, July to December 19,236
   - Corliss: January to June 10,265, July to December 10,627
4. Days people spent out on court writs, by the institution they left, 2025:
   - SCI-KTR: January to June 3,443, July to December 4,237
   - SCI-FNW: January to June 3,838, July to December 4,166
   - SCI-DNM: January to June 3,896, July to December 4,122
   - SCI-LKV: January to June 3,957, July to December 4,546
   - SCI-BRW: January to June 3,947, July to December 4,497
