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

1. Took the last submission of each personal link in kestrava_brackenmere_2026_responses.csv (the repeated-link rule of survey_reporting_standard_2025.pdf), dropped Kestrava's test tokens (status test in kestrava_brackenmere_2026_submissions.csv), mapped the French item codes to the items through the French numbers in engagement_survey_2026_questionnaire.pdf, and tied each token to an employee through kestrava_brackenmere_2026_distribution_list.csv or, for a kiosk session, the employee number in kiosk_sessions_2026-09.jsonl.
2. Kept the answers given before the close at the employee's site (the respondent definition in survey_reporting_standard_2025.pdf; the site held on 14 September in hris_assignment_history_2026.csv and its time zone in site_directory_2026-10.csv), a printed form counting by its envelope's sealed date in paper_returns_engagement_2026.xlsx: 13,717 respondents.
3. Coded the five-point answers 0 to 4 with the four negatively worded statements reversed, yes 1 and no 0, does-not-apply missing, and estimated the latent correlation of every pair of items (tetrachoric for two yes or no questions, polychoric otherwise; two-step maximum likelihood, pairwise).
4. Compared the eigenvalues (9.75, 6.01, 2.21, 0.78) with the 95th percentile of the eigenvalues of random normal data of the same size (1.07 at the fourth): three dimensions, as eigenvalues above one and Velicer's MAP also give.
5. Fitted three factors (principal-axis factoring, promax rotation) and placed each item under its largest loading: the workload statements with the tools questions, the manager statements with the growth questions, and the belonging and recognition items together; minres or maximum-likelihood extraction with varimax, oblimin or geomin rotation gives the same placements.
6. The same test on Pearson correlations of the answers keeps five (fourth and fifth eigenvalues 1.49 and 1.34 against 1.07 and 1.06), splitting off the tools questions (93.7 to 95.0 per cent yes) and the growth questions (4.5 to 6.7 per cent yes), whose correlations are capped by their splits.
7. Placed each store employee under the store and department of the row in force on 14 September in hris_assignment_history_2026.csv, reading each September department code through the 1 October reorganisation rows (every employee holding a code on 30 September passes to one new code, which the report names as it now stands) and not through the report's department names, which are those of its 16 October run; then counted, under the standard's reporting, showing and response-rate rules, the respondents, their share of the employees assigned on 14 September and the stores where a department has 10 or more respondents: 12,245 store respondents.
8. Report three sub-scales: Resources, Manager and growth, and Connection.

## 4. Deliverable Answers

### engagement_subscales_2027.xlsx

1. Each item's sub-scale, 30 items (the grouping is the answer; the sub-scale names are labels):
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
2. Each store department's respondents, the stores where its results can be shown and its response rate:
   - Grocery: 3,301 answered at least one item before the survey closed; results shown in 134 stores; 63.8 per cent of its employees on 14 September answered
   - Produce: 1,334 answered at least one item before the survey closed; results shown in 67 stores; 63.4 per cent of its employees on 14 September answered
   - Meat and Seafood: 1,070 answered at least one item before the survey closed; results shown in 46 stores; 61.9 per cent of its employees on 14 September answered
   - Deli: 902 answered at least one item before the survey closed; results shown in 24 stores; 61.8 per cent of its employees on 14 September answered
   - Bakery: 862 answered at least one item before the survey closed; results shown in 21 stores; 63.5 per cent of its employees on 14 September answered
   - Front End: 3,262 answered at least one item before the survey closed; results shown in 137 stores; 63.4 per cent of its employees on 14 September answered
   - Receiving: 623 answered at least one item before the survey closed; results shown in 2 stores; 63.6 per cent of its employees on 14 September answered
   - Store Management: 891 answered at least one item before the survey closed; results shown in 24 stores; 74.4 per cent of its employees on 14 September answered

### engagement_dimensions_2026.png

1. A scree chart of the 30 eigenvalues of the items' tetrachoric and polychoric correlations (9.75, 6.01, 2.21, 0.78 and below), the first three marked as kept, with the 95th percentile of random data of the same size as a dashed line.

### engagement_subscales_2027.md

1. The number of sub-scales: three (Resources, Manager and growth, Connection).
2. How it was reached: tetrachoric and polychoric correlations of the 30 items among the 13,717 respondents, three eigenvalues above random data of the same size; Pearson correlations of the answers would keep five, the tools and growth questions split off by their lopsided answers.
