## Tags

**Domain:** General Statistics & Data Science, data integration, record linkage and entity resolution (four Continuums of Care's HMIS exports, a domestic violence coalition's comparable database, a homeless clinic's encounters and a city outreach team's contacts, resolved through a state linkage unit's pairwise findings into the people the Halvering Valley region served in FY2026, the basis of its 2027 fund split).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Under policy RF-2027 the 2027 Fund pays Halvering City and County CoC $7,993,704 on 17,774 people served; Melbray County CoC $4,283,337 on 9,524 people served; Ondrava County CoC $2,962,447 on 6,587 people served; Pyrenna County CoC $2,125,478 on 4,726 people served; Halvering Valley Coalition for Survivors $635,035 on 1,412 people served.**
The region served 40,023 people in FY2026, each counted once across the seven sources. Not the 39,874 people that merging every chain of the linkage unit's links gives, which pays Halvering $7,964,889, $28,815 less: a record carrying only a year of birth links to every client of that name, year and sex, so 225 merged groups hold two records of one source.

## 2. Critical Components

1. The region served **40,023** people in FY2026, each counted once across the HMIS exports, the coalition's database, the clinic's encounters and the outreach app.
2. By recipient: Halvering City and County CoC **17,774**, Melbray County CoC **9,524**, Ondrava County CoC **6,587**, Pyrenna County CoC **4,726**, Halvering Valley Coalition for Survivors **1,412**.

## 3. Step-by-Step Solution

1. Read the four Continuums' HMIS client, enrollment, exit and services files stacked as sent (Melbray's dates month/day/year), dvc_comparable_db_export.xlsx, wsh_hch_encounters_fy2025_fy2026.csv, hot_field_app_contacts.jsonl and sdlu_linkage_pairs_run_20261008.csv, each record by its source and its own key: 77,238 records.
2. Flagged each record's FY2026 service under section 3 of regional_fund_policy_RF-2027.docx (an enrollment entered by 30 September 2026 and not exited before 1 October 2025, a coalition stay with a night in the year, a clinic encounter in the year at Street, Homeless Shelter or Transitional status, an outreach contact in the year, on local dates): 51,149 records.
3. Took the unit's 24,952 LINK findings strongest first and joined two records' people unless that put two records of one source in one person, since partnership_extract_guide.txt has each source hold a person once: 40,023 people with FY2026 service (merging every chain instead leaves 225 groups with two records of one source and gives 39,874).
4. Placed each person under section 4 (the Continuum of the latest HMIS enrollment open in the year, else the coalition for a coalition stay in the year, else the Continuum of the latest contact or encounter): Halvering 17,774, Melbray 9,524, Ondrava 6,587, Pyrenna 4,726, the coalition 1,412.
5. Split $18,000,000 (the $18,750,000 Fund less the Partnership's 4 per cent, section 2) in proportion and rounded each amount to the dollar: $18,000,001 together, the Partnership's share taking the extra dollar.
6. For the shelter nights, counted each person's night once across their emergency shelter and safe haven stays in the register's project types, from entry to the night before exit (an open stay to 30 September 2026), with the winter respite's bed-night services from hmis_services_fy2025_fy2026.csv, so a night on a stay left open after the person entered another shelter counts once: the 16 cells below.
7. For the rapid re-housing waits, took each head of household's FY2026 move-in date, followed that person back through any rapid re-housing project of the Continuum they left on the day the next one began, whatever their relationship to the head there, and averaged the days from that first entry to the move-in by Continuum and household type, the region over all its move-ins: the 10 averages below.
8. The 2027 Fund is split as in the Final Recommendation.

## 4. Deliverable Answers

### halvering_2027_fund_allocation.xlsx

1. People served in FY2026 and 2027 amounts, whole people and whole dollars:
   - Halvering City and County CoC: 17,774 people, $7,993,704
   - Melbray County CoC: 9,524 people, $4,283,337
   - Ondrava County CoC: 6,587 people, $2,962,447
   - Pyrenna County CoC: 4,726 people, $2,125,478
   - Halvering Valley Coalition for Survivors: 1,412 people, $635,035
   - Region: 40,023 people
2. Nights people spent in emergency shelters (night-by-night included) and safe havens, FY2026 by quarter, whole nights:
   - Halvering City and County CoC: Oct to Dec 2025 91,851; Jan to Mar 2026 93,815; Apr to Jun 2026 93,703; Jul to Sep 2026 95,992
   - Melbray County CoC: Oct to Dec 2025 46,860; Jan to Mar 2026 50,582; Apr to Jun 2026 46,167; Jul to Sep 2026 47,301
   - Ondrava County CoC: Oct to Dec 2025 42,354; Jan to Mar 2026 41,466; Apr to Jun 2026 43,578; Jul to Sep 2026 44,077
   - Pyrenna County CoC: Oct to Dec 2025 27,750; Jan to Mar 2026 27,612; Apr to Jun 2026 30,484; Jul to Sep 2026 29,590
3. Average days from a household's entry into rapid re-housing to its move-in, FY2026 move-ins, one decimal:
   - Halvering City and County CoC: households with children 43.6, adults without children 45.9
   - Melbray County CoC: households with children 42.7, adults without children 47.0
   - Ondrava County CoC: households with children 44.0, adults without children 43.2
   - Pyrenna County CoC: households with children 46.8, adults without children 42.9
   - Region, over all its move-ins: households with children 43.8, adults without children 45.3
