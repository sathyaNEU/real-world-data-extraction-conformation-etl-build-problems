## Tags

**Domain:** Epidemiology & Public Health (infectious-disease transmission modeling).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**We should fund option B, the MMR catch-up for those born 2008 to 2012: it is the only option that brings measles' reproduction number in the region below one for winter 2027-28 (0.9, against 1.3 with no catch-up).** Not no catch-up: the region is 95.2 per cent immune (0.7 as R0 times the susceptible share) and every diary in the contact survey together gives 0.9, but two thirds of those diaries were kept in the school summer holidays, when the 15 to 19-year-olds, 11.2 per cent susceptible, have under a fifth of their contacts with each other against more than half in term, and the winter runs in term. Not D or E, the least immune cohort and the most people made immune, which leave it at 1.3. Not A or C, which leave it at 1.3.

## 2. Critical Components

1. Reproduction number with no catch-up, winter 2027-28, from the survey's term-time diaries scaled to R0 15: **1.3**
2. Reproduction number under option B: **0.9**
3. Reproduction number under options A, C, D and E: **1.3** each
4. Susceptible share of 15 to 19-year-olds on 1 January 2028: **11.2 per cent**, against **4.8 per cent** across the region

## 3. Step-by-Step Solution

1. Joined measles_immunity_profile_oriel_2027-05.csv to population_projection_oriel_2028-01-01.csv by year of birth (PS-07 3.3 and 3.4): each age band's susceptible share on 1 January 2028, 11.2 per cent for 15 to 19 and 4.8 per cent overall.
2. Built the contact matrix (mean contacts per day by participant and contact age band) from the diaries in nscs_2023_participants.csv and nscs_2023_contacts.csv kept in school term, 2 to 26 May 2023, since the 3 July to 18 August 2023 diaries fell in the school summer holidays and PS-07 3.1 needs the figure below one throughout a winter that runs in term.
3. Multiplied it by each band's susceptible share and scaled it so that a wholly susceptible region gives the R0 of 15 (PS-07 3.2): its dominant eigenvalue is 1.3 with no catch-up, so a catch-up is needed (PS-07 3.6).
4. Took each option's expected people made immune in mmr_catch_up_options_autumn_2027.pdf off the susceptibles of its birth years (PS-07 3.5) and recomputed: option B 0.9; options A, C, D and E 1.3.
5. Counted each option's residents in register_people_active_born_1993-2017.csv by the year each was born, reading each lho_code in the scheme in force on its lho_recorded date (circular 03/2024: LH27 recorded before 1 July 2024 is Monaghan West, in the region) and reading a date_of_birth ten years on where the child was registered 6 to 45 days after the date ten years on and had its first GP dose 12 to 17 months after it (a birth registration and the schedule's first dose, the decade keyed one early).
6. Counted each person's valid doses in register_mmr_events_born_1993-2017.csv, re-pointed through register_merges_born_1993-2017.csv and without the GP lines gp_return_queries_mmr_2005-2027.csv shows replaced or withdrawn, giving the second of two GP lines one registration holds from one day to its twin (the other registration with its date of birth, sex, practice, registration date and address, which holds no GP line), under guidelines 12.5, given by 30 June 2027.
7. Recommended option B, the only option below one (PS-07 3.6).

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
   - Option A (born 2013 to 2017): 35,840
   - Option B (born 2008 to 2012): 33,665
   - Option C (born 2003 to 2007): 29,810
   - Option D (born 1993 to 1997): 31,016
   - Option E (born 1993 to 2002): 58,570
4. Of those, people with no valid MMR dose by that date and with exactly one:
   - Option A: 3,576 with no valid dose, 4,795 with exactly one
   - Option B: 4,354 with no valid dose, 6,155 with exactly one
   - Option C: 2,897 with no valid dose, 4,005 with exactly one
   - Option D: 5,029 with no valid dose, 7,414 with exactly one
   - Option E: 8,597 with no valid dose, 11,964 with exactly one

### measles_readiness_2027.pptx

1. Slide 1 opens with the call: fund option B, the catch-up for those born 2008 to 2012, the only option that brings the winter's reproduction number below one (0.9).
2. Slide 2: bar chart of the six reproduction numbers (no catch-up 1.3, A 1.3, B 0.9, C 1.3, D 1.3, E 1.3) against a dashed line at one, option B's bar the only one under it.
