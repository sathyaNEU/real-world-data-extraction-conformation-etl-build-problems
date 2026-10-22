## Tags

**Domain:** Criminology & Justice (recidivism and risk assessment).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Carry a two-year return rate of 20 per cent for the 6,466 people the Department expects to release to parole in 2027, highest in Garrison and lowest in Corliss.** Under Act 26-114 the Board recommits no one, so every parolee's arrest goes to court and comes back as a new commitment at the courts' own rate. Not the record's new-commitment returns, which count only the arrests the Board left to the courts. Not the record's return rate of every kind, which counts recommitments the Act ends.

## 2. Critical Components

1. The 2027 cohort is **6,466** people on the projected-release extract.
2. The two-year return rate under the Act is **20 per cent**.
3. The district with the highest rate is **Garrison** and the lowest **Corliss**.

## 3. Step-by-Step Solution

1. Read release movements PAR and RPR (PAROLE and REPAROLE before the 2022 upgrade) dated 1 January 2019 to 30 September 2024 in doc_release_movements_2019-2026.csv, each followed 730 days: 35,818 releases.
2. Linked sbi_arrests_released_persons_2019-2026.parquet to Department numbers through sbi_doc_number_crosswalk.csv and counted, for each release, arrests and days out of Department custody (ADM to the next release movement in doc_admission_movements_2019-2026.csv) in four bands of time since release; fitted a Poisson model of arrests per day on age, prior commitments, offence, sex and district.
3. Took from aoc_case_dispositions_2019-2026.csv each court-decided arrest's chance of a DOC sentence by grade class (felony A-B, felony C-E, misdemeanour), arrests to 30 June 2024, leaving out the arrests the Board revoked on in its two case files, and the arrest-to-ADM time of those sentenced.
4. For each person in doc_projected_releases_2027.csv, combined the arrest rate by time since release with that class mix, conversion and timing over 730 days; the cohort's rate is 20 per cent, Garrison highest and Corliss lowest.
5. Counted REVOKE and REVOKED decisions dated 1 July 2025 to 30 June 2026 by office, removing rescinded ones and the legacy entries dated after the legacy system closed on 2 January 2026, which repeat carried-over cases the new system decided; a decision citing an arrest number is on a reported arrest.
6. Took each detainer once (one per legacy case, whose action rows repeat it, and a carried-over case from the new system), ended a legacy detainer with no lift date at the person's next ADM in doc_admission_movements_2019-2026.csv, and counted days from the lodge day to the day before the end in each quarter, by the district of the county jail.
7. Drew each district's 2025 detainer days from step 6 as a bar stacked by quarter in detainer_days_2025.png, labelled with its total.
8. Carried 20 per cent in the projection, Garrison highest and Corliss lowest.

## 4. Deliverable Answers

### returns_projection_2027.xlsx

1. Two-year return rate of the 2027 parole releases under Act 26-114: 20 per cent; highest district Garrison, lowest district Corliss.
2. Revocations the Board ordered from 1 July 2025 to 30 June 2026 and did not rescind:
   - D1 (Garrison): 1,586 on a reported arrest, 295 on conditions alone
   - D2 (Ridgway): 709 on a reported arrest, 259 on conditions alone
   - D3 (Linwood): 427 on a reported arrest, 176 on conditions alone
   - D4 (Corliss): 157 on a reported arrest, 137 on conditions alone
3. Days parolees were held on Board detainers in each district's county jails, 2025:
   - Garrison: January to March 22,746, April to June 22,034, July to September 24,883, October to December 24,606
   - Ridgway: January to March 15,421, April to June 14,827, July to September 13,663, October to December 14,005
   - Linwood: January to March 9,962, April to June 10,029, July to September 10,630, October to December 11,139
   - Corliss: January to March 6,338, April to June 6,391, July to September 6,354, October to December 6,151

### detainer_days_2025.png

1. One bar per parole district, stacked by quarter of 2025, labelled with its year's detainer days: Garrison 94,269, Ridgway 57,916, Linwood 41,760, Corliss 25,234.
