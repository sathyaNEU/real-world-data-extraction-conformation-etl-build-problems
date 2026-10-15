## Tags

**Domain:** Criminology & Justice (recidivism risk assessment: each pretrial risk score's new-offense rate for all the eligible defendants a presumptive release tier would release, estimated past the outcome record's selective labels).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The 2027 presumptive release tier should reach Pretrial Assessment Scale new-criminal-activity score 3: scores 1 to 3 meet the 85 per cent safety floor and score 4 does not.**
With every eligible defendant released, read from the 32 magistrates' release shares, under 80 per cent of score-4 defendants would complete the pretrial period without a new-offense arrest, against about 90 per cent at score 3. Not scores 1 to 4, which takes score 4 at its released defendants' 87.9 per cent and leaves out the 26.0 per cent of eligible score-4 defendants magistrates held, the ones they judged riskiest; not scores 1 and 2, which counts every held defendant as arrested.

## 2. Critical Components

1. With every eligible defendant released, score 4's safety rate is **under 80 per cent**, below the 85 per cent floor.
2. Score 3's is **about 90 per cent**, above the floor, and scores 1 and 2 are higher still.

## 3. Step-by-Step Solution

1. Stacked first_appearances_2021-10-01_2024-03-03.csv (legacy codes through offense_code_crosswalk.xlsx, magistrate initials through magistrate_roster.xlsx) with first_appearances_2024-03-04_2026-09-30.csv and first_appearance_charges_2024-03-04_2026-09-30.csv, and kept the appearances from 1 October 2021 to 30 September 2025 eligible under draft 2.1 with a screen in pas_screens_2021-10-01_2026-09-30.csv (booking number, else the state number within 12 hours): 55,005 appearances, 7,439 at score 4.
2. Took release at first appearance as leaving the detention center within 24 hours on a releasing type in jail_bookings_2021-10-01_2026-09-30.csv (UTC read in Eastern time), and a new-offense arrest per draft 2.4 from state_arrest_extract_2026-10-02.csv (type NEW, offense after the release day, within 365 days or by the last charge's disposition in court_case_index_2021-10-01_2026-09-30.csv).
3. Among the released, score 4's safety rate is 87.9 per cent and score 5's 78.0 per cent, a tier of scores 1 to 4 on that rate; but magistrates held 26.0 per cent of eligible score-4 defendants, and their outcomes are not on file.
4. For each score, fitted each of the 32 magistrates' new-offense arrests per eligible appearance on the magistrate's release share, weighted by caseload, and read the line at a release share of 100 per cent: scores 1 to 6 at 95.1, 93.1, 90.3, 75.8, 63.6 and 61.6 per cent.
5. Scores 1 to 3 meet the 85 per cent floor of draft 2.3 and score 4 does not, so the tier's top score under draft 2.5 is 3.

## 4. Deliverable Answers

### presumptive_release_tier_2027.docx

1. The tier's top score is new-criminal-activity score 3 (scores 1 to 3); score 4 falls below the 85 per cent floor with every eligible defendant released.

### presumptive_release_tier_2027.xlsx

2. Bed-days in custody to 30 September 2026 of eligible defendants held after a first appearance from 1 October 2025 to 30 September 2026, by new-criminal-activity score:
   - Score 1: 2,210
   - Score 2: 4,660
   - Score 3: 5,950
   - Score 4: 8,330
   - Score 5: 3,440
   - Score 6: 2,040
3. Days on electronic monitoring to 30 September 2026 of every defendant released at a first appearance in that year, by new-criminal-activity score:
   - Score 1: 28,620
   - Score 2: 26,820
   - Score 3: 16,250
   - Score 4: 10,380
   - Score 5: 4,660
   - Score 6: 2,220
4. Releases at a first appearance from 1 October 2025 to 30 June 2026 followed within 90 days by a missed court date on that appearance's charges, by failure-to-appear score:
   - Score 1: 260 of 6,860 releases, 3.8%
   - Score 2: 349 of 5,525 releases, 6.3%
   - Score 3: 340 of 3,364 releases, 10.1%
   - Score 4: 308 of 1,976 releases, 15.6%
   - Score 5: 78 of 338 releases, 23.1%
   - Score 6: 20 of 77 releases, 26.0%

### missed_court_dates_by_fta_score.png

5. Bar chart of the six shares by failure-to-appear score, each bar labelled with its share and its count of releases.
