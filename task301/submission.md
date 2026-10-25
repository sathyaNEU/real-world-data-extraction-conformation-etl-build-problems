## Tags

**Domain:** Epidemiology and public health (health burden and impact modelling).
**Analytical objective:** Opportunity sizing and decision support.

## 1. Final Recommendation

**Place the 2027 quit outreach team in Inner South: it will help about 550 patients there to quit.**
About 85 per cent of Inner South's 5,456 recorded smokers will still smoke when the team calls. Not Coastal Hinterland, which lists the most (8,422) but whose records are older and whose smokers stop more than twice as fast, so only about half its list still smokes in 2027. Not Western Plains, whose list is at least as current but smaller (4,957). Not Northern Corridor, with a smaller list (4,855) whose smokers stop faster.

## 2. Critical Components

1. Inner South's practices record **5,456** active patients as current smokers in the 30 September 2026 extract.
2. About **85** per cent of them will still smoke when called in 2027, read from Inner South's own consecutive status recordings.
3. The 2025 team helped about **12** per cent of the listed patients who still smoked when it called to quit.

## 3. Step-by-Step Solution

1. Counted each candidate's active patients whose status in active_patients_2026-09-30.csv is daily, weekly or irregular smoker or smoker (data_dictionary_2026.docx): Coastal Hinterland 8,422, Inner South 5,456, Northern Corridor 4,855, Western Plains 4,957.
2. Kept the last entry of each day in smoking_status_history_2012-2026.parquet, paired every smoker or ex-smoker entry with the patient's next entry (never smoked read as not smoking) and fitted each sub-region's yearly rates of stopping and of relapse to its own pairs as a two-state Markov process by maximum likelihood: stopping about 11 per cent a year in Coastal Hinterland, 5 in Inner South, 7 in Northern Corridor and 6 in Western Plains, relapse about 1.5 per cent.
3. Averaged each listed patient's chance of still smoking over calls spread evenly through 2027 from the date of their status: about 85 per cent of Inner South's list, about half of Coastal Hinterland's.
4. In quit_outreach_calls_eastern_shore_2025.csv the team reached 4,149 of its 5,489 patients (75.6 per cent) and 393 told it they had stopped; 609 of the 3,756 smokers it reached (16.2 per cent) were not smoking four weeks after their quit date, lost to follow-up counted as smoking per quit_outreach_plan_2027.docx: about 12 per cent of the listed patients still smoking when called.
5. Multiplied each list's expected smokers at the call by that rate: Inner South about 550 quits, the most of the four.
6. Matched quitline_referrals_2023-2025.csv's practice names to practices.csv (case, Pty Ltd, Med Centre and GP spellings aside) and summed 2025's referrals by the register's sub-region and quarter, Quitline's phn_sub_region column still holding four practices in the sub-regions they belonged to before July 2025.
7. In dialler_legs_2025.csv dropped the 675 legs that start inside an earlier answered leg for the same patient (the nurse's part of a handed-over call, whose minutes the first leg already holds) and added an hour to stamps before 6 April and from 5 October 2025, the dialler stamping standard time while the team worked to New South Wales daylight time (team_roster_2025.csv); then counted calls from 5 pm and the answered ones by weekday, and answered calls' minutes per patient reached by month.

## 4. Deliverable Answers

### quit_outreach_placement_2027.docx

1. Place the team in Inner South for 2027: about 550 quits.
2. Horizontal bar chart of the four candidate sub-regions' expected 2027 quits, Inner South highlighted and labelled about 550.

### quit_outreach_placement_2027.xlsx

1. Quitline referrals from each candidate sub-region's practices in 2025 (January to March, April to June, July to September, October to December):
   - Coastal Hinterland: 228, 255, 214, 191
   - Inner South: 162, 196, 173, 158
   - Northern Corridor: 188, 165, 138, 132
   - Western Plains: 153, 129, 140, 149
2. Calls the 2025 team made from 5 pm local time, and patients reached in them, by weekday:
   - Monday: 596 calls, 226 patients reached
   - Tuesday: 605 calls, 241 patients reached
   - Wednesday: 581 calls, 232 patients reached
   - Thursday: 599 calls, 246 patients reached
   - Friday: 605 calls, 240 patients reached
3. Minutes on answered calls per patient reached, by month of 2025:
   - February: 14.2
   - March: 14.5
   - April: 14.2
   - May: 14.5
   - June: 14.4
   - July: 14.5
   - August: 14.4
   - September: 14.6
   - October: 14.9
   - November: 14.4
