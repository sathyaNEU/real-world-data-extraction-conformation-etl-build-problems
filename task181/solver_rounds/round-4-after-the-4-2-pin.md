# solver round: round 4 after the 4.2 pin

**Proxy score 96.8 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 54.8 of 58). Main call LANDED. 3 of 3 ask items cracked (80 per cent of tokens).

## Main call

golden: Send the response team to Griffith this week.

solver: Send Janice Barker's response team to Griffith: on the 07:00 5 Oct 2026 extract, Griffith's cases with first specimens 21 Sep-4 Oct 2026, adjusted for reporting delay, come to about 60.6 against a five-year (2021-2025) expected count of 1.4, an excess of about 59.2. That is well above Wagga Wagga (about 9.3 vs 1.4, excess about 7.9), which only leads on cases received so far (9 vs 7). Griffith's school clusters are Banna Avenue Public School (5 student cases) and Kooyoo Street Public School (2).

tokens matched 2 of 2 (Send, Griffith)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| response_team_brief.pptx | 1 | 1 | 1 | 100% |
| response_team_brief.pptx | 2 | 5 | 5 | 100% |
| pertussis_cases_by_lga.csv | 1 | 10 | 12 | 83% |

## Solver's path

1. Mapped postcodes to areas with postcode_lga_concordance.xlsx; split postcodes go to the area with the larger share; kept the 10 unit areas. This reproduces the week-35 report (162 year to date, Wagga Wagga 73, 25 in the last 4 weeks).
2. Built cases from pertussis_notifications_2019-2026.csv: same person, specimens within 90 days of the episode's first specimen = one case (1,118 notifications to 1,053 cases); confirmed if any notification is confirmed; each case dated by its first specimen.
3. Extract day 5 Oct 2026 (run 07:00 AEDT = 4 Oct 20:00 UTC); window 21 Sep-4 Oct. Cases received so far: Wagga Wagga 9, Griffith 7, Snowy Valleys 7, Cootamundra-Gundagai 2, others 0-1. Expected = mean of 2021-2025 on the same dates (Wagga Wagga 1.4, Griffith 1.4, Snowy Valleys 1.4).
4. Allowed for reporting delay using each lab's historical delay from first specimen to first receipt (cases before Jul 2026). Inland Pathology median about 12 days, 62.8% complete at 13 days; hospital lab about 2 days. Each case weighted by 1/completeness at its age: Griffith 60.61 (excess 59.21), Wagga Wagga 9.29 (excess 7.89). The 14-day average-completeness method gives Griffith about 32, also first.
5. Clusters: student cases (school_role = Student) with first specimen 5 Sep-4 Oct, school names normalised and checked against the roster sheets (school LGA): Griffith = Banna Avenue Public School 5, Kooyoo Street Public School 2.
6. Quarterly 1 Jan-31 Aug 2026: 150 unit cases (140 confirmed, 10 probable). Infants (<6 months at first specimen): 11 on line-list birth dates, but birth_records shows day/month swaps for two cases, confirmed by the mothers' dTpa due dates, so 9 infants.
7. Admissions (medical record number zero-padded to 8 digits, admission within 14 days of specimen) plus the two Aug-27 infants linked by birth date, sex and postcode = 5. Vaccinated mother (birth record mother number = card + IRN; dTpa for that pregnancy at least 14 days before birth): only Cootamundra-Gundagai = 1.

confidence: High for Griffith and the two clusters (any delay adjustment makes Griffith first; only raw counts favour Wagga Wagga). High for confirmed/probable counts. Moderate for the infant columns.

notes: Two Aug-27 infants carry medical record numbers found in no linked file; linked by birth date, sex and postcode plus a whooping-cough admission. The delay-adjusted counts are model estimates; the ranking does not depend on the method.

### response_team_brief.pptx (solver's answers)
- area the team goes to: Griffith. Delay-adjusted cases 21 Sep-4 Oct 2026 = 60.61 (7 received so far); expected = 1.4 (mean of 2021-2025: 0, 0, 0, 5, 2); excess = 59.21. Runner-up Wagga Wagga: delay-adjusted 9.29 (9 received), expected 1.4, excess 7.89. Snowy Valleys: 7 received, expected 1.4, excess about 5.7.
- school clusters in that area with case counts: Banna Avenue Public School: 5 student cases (first specimens 18 Sep-1 Oct 2026; a parent case at the school is excluded). Kooyoo Street Public School: 2 student cases (22 Sep and 30 Sep 2026). Window 5 Sep-4 Oct 2026.

### pertussis_cases_by_lga.csv (solver's answers)
- confirmed, probable, infants, infants admitted, infants with vaccinated mother per LGA, 1 Jan-31 Aug 2026 (whole counts): Wagga Wagga 63,2,2,1,0; Griffith 25,3,1,1,0; Leeton 11,0,1,0,0; Narrandera 5,0,1,0,0; Murrumbidgee 0,0,0,0,0; Hay 2,0,0,0,0; Edward River 7,1,1,1,0; Junee 3,1,1,0,0; Cootamundra-Gundagai 15,2,1,1,1; Snowy Valleys 9,1,1,1,0. Unit totals: confirmed 140, probable 10, infant cases 9, infants admitted 5, born to a vaccinated mother 1.
