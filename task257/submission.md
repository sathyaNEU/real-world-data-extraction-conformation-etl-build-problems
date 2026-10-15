## Tags

**Domain:** Psychology & Behavioral Science, psychometric measurement and scale validation (how many distinct dimensions of employees' views a grocery chain's 30 engagement survey items measure, from the latent correlations of their yes or no and five-point answers, to fix the sub-scales its 2027 dashboard reports).
**Analytical objective:** Descriptive & Distribution Analysis (how the employees' views are composed: the number of dimensions the items measure and the items under each).

## 1. Final Recommendation

**Report three sub-scales on Brackenmere Markets' 2027 engagement dashboard: Resources (11 items: the workload statements and the tools questions), Manager and growth (11 items: the manager statements and the growth questions) and Connection (8 items: the belonging and recognition items).**
On the tetrachoric and polychoric correlations of the 30 items among the 13,717 respondents, three eigenvalues (9.75, 6.01 and 2.21) stand above random data of the same size and the fourth (0.78) falls below its 95th percentile of 1.07. Not five, which Pearson correlations of the answers give (fourth and fifth eigenvalues 1.49 and 1.34 against 1.07 and 1.06): the two extra dimensions are the tools questions, answered yes by 93.7 to 95.0 per cent, and the growth questions, answered yes by 4.5 to 6.7 per cent, split off by their lopsided answers rather than by what they measure. Not six, the questionnaire's areas read off the wording, which the answers do not separate.

## 2. Critical Components

1. Respondents: **13,717** employees answered at least one of the 30 items before the survey closed at their site
2. Eigenvalues of the items' tetrachoric and polychoric correlations: **9.75, 6.01 and 2.21**, then **0.78** against random data's 95th percentile of **1.07** at the fourth: **three dimensions**
3. Items under each dimension: Resources **11**, Manager and growth **11**, Connection **8**

## 3. Step-by-Step Solution

1. Took the last submission under each token of kestrava_brackenmere_2026_responses.csv, dropped the test tokens (status test in kestrava_brackenmere_2026_submissions.csv), mapped the French item codes to the items through kestrava_brackenmere_2026_codebook.xlsx, and tied each token to an employee through kestrava_brackenmere_2026_distribution_list.csv or, for a kiosk session, the employee number in kiosk_sessions_2026-09.jsonl.
2. Kept the answers given before the close at the employee's site (the respondent definition in survey_reporting_standard_2025.pdf; the site held on 14 September in hris_assignment_history_2026.csv and its time zone in site_directory_2026-10.csv), a printed form counting by its envelope's sealed date in paper_returns_engagement_2026.xlsx: 13,717 respondents.
3. Coded the five-point answers 0 to 4 with the four negatively worded statements reversed, yes 1 and no 0, does-not-apply missing, and estimated the latent correlation of every pair of items (tetrachoric for two yes or no questions, polychoric otherwise; two-step maximum likelihood, pairwise).
4. Compared the eigenvalues (9.75, 6.01, 2.21, 0.78) with the 95th percentile of the eigenvalues of random normal data of the same size (1.07 at the fourth): three dimensions, as eigenvalues above one and Velicer's MAP also give.
5. Fitted three factors (principal-axis factoring, promax rotation) and placed each item under its largest loading: the workload statements with the tools questions, the manager statements with the growth questions, and the belonging and recognition items together; minres or maximum-likelihood extraction with varimax, oblimin or geomin rotation gives the same placements.
6. The same test on Pearson correlations of the answers keeps five (fourth and fifth eigenvalues 1.49 and 1.34 against 1.07 and 1.06), splitting off the tools questions (93.7 to 95.0 per cent yes) and the growth questions (4.5 to 6.7 per cent yes), whose correlations are capped by their splits.
7. Counted, by the district of each employee's 14 September store, the respondents and those whose answers before the close cover all 30 items, an employee's kiosk sessions taken together and a does-not-apply answer counting as an answer: 12,245 and 10,055 across the 12 store districts.
8. Report three sub-scales: Resources, Manager and growth, and Connection.

## 4. Deliverable Answers

### engagement_subscales_2027.xlsx

1. Each item's sub-scale, 30 items:
   - Q01 My manager treats me with respect: Manager and growth
   - Q02 My workload is manageable on a normal shift: Resources
   - Q03 I feel part of a team at work: Connection
   - Q04 In the past four weeks, was your scanner or till working whenever you needed it: Resources
   - Q05 I get credit for the work I do: Connection
   - Q06 Do you have a written development plan agreed with your manager: Manager and growth
   - Q07 Enough people are scheduled on my shifts to get the work done: Resources
   - Q08 My manager keeps me informed about changes that affect my work: Manager and growth
   - Q09 In the past four weeks, was your schedule posted at least two weeks ahead: Resources
   - Q10 I sometimes feel like an outsider where I work: Connection
   - Q11 In the past twelve months, have you been offered training beyond what your role requires: Manager and growth
   - Q12 Good work in my department usually goes unnoticed: Connection
   - Q13 I often have to skip or cut short my breaks: Resources
   - Q14 Do you have the safety gear your job requires: Resources
   - Q15 My manager is hard to approach about problems: Manager and growth
   - Q16 People here treat each other fairly whatever their background: Connection
   - Q17 In the past twelve months, have you been put forward for a promotion or a lead role: Manager and growth
   - Q18 The people I work with appreciate what I do: Connection
   - Q19 Were your last three pays correct and on time: Resources
   - Q20 My schedule gives me enough rest between shifts: Resources
   - Q21 My manager gives me useful feedback on my work: Manager and growth
   - Q22 In the past twelve months, have you shadowed or covered a role in another department to learn it: Manager and growth
   - Q23 In the past four weeks, has a coworker helped you without being asked: Connection
   - Q24 Can you get into the scheduling and pay app when you need to: Resources
   - Q25 In the past four weeks, has anyone thanked you for your work: Connection
   - Q26 In the past twelve months, has someone outside your store or site talked with you about your career: Manager and growth
   - Q27 In the past four weeks, were you able to leave on time at the end of every shift: Resources
   - Q28 In the past four weeks, has your manager talked with you one to one about how you are doing: Manager and growth
   - Q29 Do you know who to call when equipment in your department breaks down: Resources
   - Q30 Have you been invited to apply to the Brackenmere Leaders programme: Manager and growth
2. For each of the 12 store districts, employees who answered at least one item before the survey closed and how many of them answered all 30:
   - Ottawa-Gatineau: 1,130 answered at least one item before the survey closed; 921 of them answered all 30
   - Eastern Ontario: 568 answered at least one item before the survey closed; 464 of them answered all 30
   - Kingston and Quinte: 635 answered at least one item before the survey closed; 526 of them answered all 30
   - Durham and Kawartha: 903 answered at least one item before the survey closed; 731 of them answered all 30
   - Toronto East: 1,597 answered at least one item before the survey closed; 1,311 of them answered all 30
   - Toronto West: 1,474 answered at least one item before the survey closed; 1,225 of them answered all 30
   - Hamilton and Niagara: 1,061 answered at least one item before the survey closed; 867 of them answered all 30
   - Northern Ontario: 829 answered at least one item before the survey closed; 685 of them answered all 30
   - Montréal: 1,558 answered at least one item before the survey closed; 1,264 of them answered all 30
   - Laval and Laurentides: 895 answered at least one item before the survey closed; 744 of them answered all 30
   - Montérégie and Estrie: 1,005 answered at least one item before the survey closed; 830 of them answered all 30
   - New Brunswick: 590 answered at least one item before the survey closed; 487 of them answered all 30

### engagement_dimensions_2026.png

1. A scree chart of the 30 eigenvalues of the items' tetrachoric and polychoric correlations (9.75, 6.01, 2.21, 0.78 and below), the first three marked as kept, with the 95th percentile of random data of the same size as a dashed line.

### engagement_subscales_2027.md

1. The number of sub-scales: three (Resources, Manager and growth, Connection).
2. How it was reached: tetrachoric and polychoric correlations of the 30 items among the 13,717 respondents, three eigenvalues above random data of the same size; Pearson correlations of the answers would keep five, the tools and growth questions split off by their lopsided answers.
