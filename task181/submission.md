# task181: where the pertussis response team goes this week

## Tags

**Domain:** Epidemiology & Public Health (disease surveillance and outbreak anomaly detection: a regional public health unit's pertussis notifications across ten inland New South Wales local government areas).
**Analytical objective:** Anomaly Detection & Diagnostics.

## 1. Final Recommendation

**Send the response team to Griffith this week.**

On the extract Griffith has 7 cases with specimens collected 21 September to 4 October against 1.4 expected, but 6 of the 7 came through Inland Pathology, which notified 76% of its specimens within 14 days of collection (the hospital laboratory 100%), so at its own route's speed Griffith's fortnight is several times what has been notified and its excess is the largest of the ten areas. Not Wagga Wagga, which leads on the cases notified so far (9 against 1.4) only because its cases go through the hospital laboratory and are nearly all on file. Not Snowy Valleys, level with Griffith at 7 against 1.4, whose cases also go through the hospital laboratory and are nearly all on file.

## 2. Critical Components

1. Cases with specimens collected 21 September to 4 October on the extract: Wagga Wagga **9**, Griffith **7**, Snowy Valleys **7**
2. Expected count (PR-07 4.3): **1.4** for each of Wagga Wagga, Griffith and Snowy Valleys
3. **6** of Griffith's 7 notified cases came through Inland Pathology; all of Wagga Wagga's and Snowy Valleys' came through the hospital laboratory
4. Notified within 14 days of collection, specimens collected August 2025 to July 2026: Inland Pathology **76%**, hospital laboratory **100%**

## 3. Step-by-Step Solution

1. Grouped `pertussis_notifications_2019-2026.csv` into cases per PR-07 3.3 (one person, specimens within 90 days of the episode's first), dated each by its first specimen (3.5), and gave each its area through `postcode_lga_concordance.xlsx` by the larger population share (3.4), dropping non-residents (1.2).
2. Counted each area's cases with specimens collected 21 September to 4 October 2026 (4.2): Wagga Wagga 9, Griffith 7, Snowy Valleys 7, Cootamundra-Gundagai 2, Edward River, Leeton and Narrandera 1 each.
3. Took each area's expected count as the mean of its cases on the same 14 dates in 2021 to 2025 (4.3): 1.4 for Wagga Wagga, Griffith and Snowy Valleys, so on the cases notified so far Wagga Wagga leads.
4. Measured each laboratory's time from specimen collection to notification, with `received_utc` converted to Sydney dates: for specimens collected August 2025 to July 2026, Inland Pathology notified 76% within 14 days and the hospital laboratory 100%.
5. Estimated each area's cases with specimens in the fortnight by dividing each laboratory route's notified cases by that route's own share notified within the days each specimen day has had, from the completed specimens in the line list: Griffith's fortnight is several times its 7 notified, Wagga Wagga's and Snowy Valleys' a little above what is on file, and Griffith's excess over 1.4 is the largest, as it is under per-day and weekly reporting-triangle versions and over 6, 12 or 24 months of history.
6. Clusters (5.1): student cases by interview role with specimens collected 5 September to 4 October, one per episode, free-text school names matched to the roster names in `school_rosters_term3_2026.xlsx`, kept where two or more.
7. Quarterly table (7.1): cases with specimens 1 January to 31 August 2026 by area and status; infants under six months at the specimen (6.1); of those, an admission within 14 days in `respiratory_admissions_2019-2026.csv` on medical record number (6.2), and a dTpa dose in that pregnancy at least 14 days before birth in `antenatal_vaccinations_2019-2026.parquet`, linked through `birth_records_2024-2026.csv` on the mother's Medicare number (6.3).
8. Recommendation: the response team goes to Griffith this week.

## 4. Deliverable Answers

### response_team_brief.pptx

1. The area the team goes to this week: Griffith.
2. School clusters this week, five, each with school, area and cases:
   - Banna Avenue Public School, Griffith, 5
   - Wollundry Public School, Wagga Wagga, 3
   - Blowering Road Public School, Snowy Valleys, 2
   - Bolton Park High School, Wagga Wagga, 2
   - Kooyoo Street Public School, Griffith, 2

### pertussis_cases_by_lga.csv

1. One row per area, specimens collected 1 January to 31 August 2026, as confirmed cases, probable cases, infants under six months, of those admitted to hospital, of those born to a mother vaccinated at least two weeks before the birth:
   - Wagga Wagga: 63, 2, 3, 2, 1
   - Griffith: 25, 3, 2, 1, 1
   - Leeton: 11, 0, 1, 0, 1
   - Narrandera: 5, 0, 1, 0, 0
   - Murrumbidgee: 0, 0, 0, 0, 0
   - Hay: 2, 0, 0, 0, 0
   - Edward River: 7, 1, 1, 1, 0
   - Junee: 3, 1, 1, 0, 1
   - Cootamundra-Gundagai: 15, 2, 1, 1, 1
   - Snowy Valleys: 9, 1, 1, 1, 0
