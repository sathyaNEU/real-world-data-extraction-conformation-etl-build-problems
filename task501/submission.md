## Tags

**Domain:** Epidemiology & Public Health (infectious-disease transmission modeling).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**We should fund option B, the MMR catch-up for those born 2008 to 2012: it is the only option that brings measles' reproduction number in the region below one for winter 2027-28 (0.9, against 1.3 with no catch-up).** Not no catch-up, which the region's 94.6 per cent immunity (0.8 as R0 times the susceptible share) supports only if everyone mixes at random, while the 15 to 19-year-olds, 11.2 per cent susceptible, have about half their contacts with each other. Not D or E, the least immune cohort and the most people made immune, which leave it at 1.3 because adults mix too little among themselves. Not A or C, which leave it at 1.3.

## 2. Critical Components

1. Reproduction number with no catch-up, winter 2027-28, the dominant eigenvalue of the next-generation matrix scaled to R0 15: **1.3**
2. Reproduction number under option B: **0.9**
3. Reproduction number under options A, C, D and E: **1.3** each
4. Susceptible share of 15 to 19-year-olds on 1 January 2028: **11.2 per cent**, against **5.4 per cent** across the region

## 3. Step-by-Step Solution

1. Joined measles_immunity_profile_oriel_2027-05.csv to population_projection_oriel_2028-01-01.csv by year of birth (PS-07 3.3 and 3.4): each survey age group's susceptible share on 1 January 2028, 11.2 per cent for 15 to 19 and 5.4 per cent overall.
2. Built the next-generation matrix from Table 2 of nscs_2023_published_tables.xlsx (contacts per day by age group) times each age group's susceptible share, scaled so that a wholly susceptible region gives the R0 of 15 (PS-07 3.2).
3. Took its dominant eigenvalue: 1.3 with no catch-up, so a catch-up is needed (PS-07 3.6).
4. Took each option's expected people made immune in mmr_catch_up_options_autumn_2027.pdf off the susceptibles of its birth years (PS-07 3.5) and recomputed: option B 0.9; options A, C, D and E 1.3.
5. Counted each option's residents in register_people_active_born_1993-2017.csv, reading each lho_code in the scheme in force on its lho_recorded date (circular 03/2024: LH27 recorded before 1 July 2024 is Monaghan West, in the region).
6. Counted their valid doses in register_mmr_events_born_1993-2017.csv, re-pointed through register_merges_born_1993-2017.csv and without the GP lines gp_return_queries_mmr_2005-2027.csv shows replaced or withdrawn, under guidelines 12.5 at 30 June 2027.
7. Counted confirmed cases with rash onset in the window in nds_measles_cases_oriel_2019-2027.csv by year of birth, each back-entered 2019 outbreak record (its legacy number in the comments) counted once with its migrated record.
8. Recommended option B, the only option below one (PS-07 3.6).

## 4. Deliverable Answers

### winter_measles_2027.xlsx

1. Call: fund option B, the MMR catch-up for those born 2008 to 2012.
2. Reproduction number for winter 2027-28, to one decimal place:
   - No catch-up: 1.3
   - Option A: 1.3
   - Option B: 0.9
   - Option C: 1.3
   - Option D: 1.3
   - Option E: 1.3
3. People born in each option's years whom the register holds as living in the region at 30 June 2027:
   - Option A (born 2013 to 2017): 35,346
   - Option B (born 2008 to 2012): 33,217
   - Option C (born 2003 to 2007): 29,398
   - Option D (born 1993 to 1997): 30,625
   - Option E (born 1993 to 2002): 57,865
4. Of those, people with no valid MMR dose and with exactly one:
   - Option A: 3,542 with no valid dose, 4,724 with exactly one
   - Option B: 4,285 with no valid dose, 6,094 with exactly one
   - Option C: 2,859 with no valid dose, 3,960 with exactly one
   - Option D: 4,971 with no valid dose, 7,302 with exactly one
   - Option E: 8,530 with no valid dose, 11,788 with exactly one
5. Confirmed measles cases with rash onset from 1 January 2019 to 30 June 2027 born in each option's years, and how many of them were imported:
   - Option A: 9 confirmed, 2 imported
   - Option B: 10 confirmed, 2 imported
   - Option C: 11 confirmed, 3 imported
   - Option D: 10 confirmed, 3 imported
   - Option E: 16 confirmed, 5 imported

### measles_readiness_2027.pptx

1. Slide 1 opens with the call: fund option B, the catch-up for those born 2008 to 2012, the only option that brings the winter's reproduction number below one (0.9).
2. Slide 2: bar chart of the six reproduction numbers (no catch-up 1.3, A 1.3, B 0.9, C 1.3, D 1.3, E 1.3) against a dashed line at one, option B's bar the only one under it.
