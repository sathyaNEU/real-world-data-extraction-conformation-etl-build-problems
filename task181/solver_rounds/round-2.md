# solver round: round 2

**Proxy score 65.2 / 100** (recommendation 5.0 of 35, instruction 7.0 of 7, asks 53.2 of 58). Main call missed. 2 of 3 ask items cracked (80 per cent of tokens).

## Main call

golden: Send the response team to Griffith this week.

solver: Send Janice Barker's response team to Wagga Wagga, which has the largest excess under PR-07 §4: 9 cases with first specimens collected 21 Sep to 4 Oct 2026 against an expected 1.4 (mean of 0,0,1,3,3 for 2021-2025), an excess of 7.6, ahead of Griffith (7 vs 1.4, excess 5.6) and Snowy Valleys (7 vs 1.4, excess 5.6); this week's school clusters are Banna Avenue Public School (Griffith, 5), Wollundry Public School (Wagga Wagga, 3), Bolton Park High School (Wagga Wagga, 2), Blowering Road Public School (Snowy Valleys, 2) and Kooyoo Street Public School (Griffith, 2).

tokens matched 2 of 2 (Send, Griffith)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| response_team_brief.pptx | 1 | 1 | 1 | 100% |
| response_team_brief.pptx | 2 | 11 | 11 | 100% |
| pertussis_cases_by_lga.csv | 1 | 9 | 12 | 75% |

## Solver's path

1. Checked SIPHU_PERTUSSIS_LINELIST_job_20261005_0700.txt against pertussis_notifications_2019-2026.csv: 1118 rows, sha256 and bytes match; latest receipt 2026-10-03, before the run start of 2026-10-04T20:00Z; extract day is Mon 5 Oct 2026
2. PR-07 §3.3: grouped notifications by person_id into 90-day episodes from the first specimen -> 1053 cases (65 with more than one notification); case confirmed if any notification confirmed; dated by first specimen (§3.5)
3. §3.4: mapped each case's postcode with postcode_lga_concordance.xlsx, sending split postcodes to the area with the larger share (2652 Wagga Wagga, 2655 Lockhart, 2665 Coolamon, 2706 Murrumbidgee, 2722/2727 Cootamundra-Gundagai, 2729 Snowy Valleys); kept the 10 UNIT_AREA=Y areas -> 1034 resident cases
4. §4.2-4.3: counted cases with first specimen 21 Sep-4 Oct 2026 by area; expected = mean of the same dates in 2021-2025 -> Wagga Wagga 9 vs 1.4 (excess 7.6), Griffith 7 vs 1.4 (5.6), Snowy Valleys 7 vs 1.4 (5.6), Cootamundra-Gundagai 2 vs 0.6 (1.4), others under 1
5. §5.1: cases with school_role=Student and first specimen 5 Sep-4 Oct 2026; matched written school names to school_rosters_term3_2026.xlsx sheet titles (all student cases also matched a roster row on dob/sex/postcode); school area taken from the roster LGA -> Banna Avenue 5, Wollundry PS 3, Bolton Park HS 2, Blowering Road 2, Kooyoo Street 2; Fernleigh Road, Hurley Street, Canal Road (one person notified twice), Twynam Street and Wollundry Preschool have 1 each
6. §7.1: cases with first specimen 1 Jan-31 Aug 2026 -> 150 (140 confirmed, 10 probable) by area
7. §6.1: infant = first specimen before dob + 6 months -> 11 infants, all with MRN
8. §6.2: matched infant MRN (leading zeros dropped) to respiratory_admissions_2019-2026.csv with admission_date (dd/mm/yyyy) within 14 days either side of first specimen -> 6 admitted
9. §6.3: matched infant MRN to birth_records baby_mrn; mother_medicare_no split into 10-digit card + IRN, joined to the parquet register (card spaces removed); dTpa dose in that pregnancy at least 14 days before birth -> 5 (2 doses 10-11 days before birth and 2 from a 2024 pregnancy excluded)

confidence: High: the extract checks out, the protocol rules apply cleanly, Wagga Wagga leads the next areas by 2.0 cases, and every cluster student matches the school roster.

notes: Case status is taken as notified (serology-only before July 2024 stays confirmed, per §2.3). The week 35 report counts notifications by date received, so its area figures differ from these case counts by design.

### response_team_brief.pptx (solver's answers)
- area the team goes to: Wagga Wagga: 9 cases in the 14 days 21 Sep to 4 Oct 2026; expected 1.4 cases; excess 7.6 cases (next: Griffith and Snowy Valleys, excess 5.6 each)
- school clusters (school, area, cases): Banna Avenue Public School, Griffith, 5 cases; Wollundry Public School, Wagga Wagga, 3 cases; Bolton Park High School, Wagga Wagga, 2 cases; Blowering Road Public School, Snowy Valleys, 2 cases; Kooyoo Street Public School, Griffith, 2 cases

### pertussis_cases_by_lga.csv (solver's answers)
- Wagga Wagga row: confirmed 63; probable 2; infants under 6 months 3; infants admitted 2; infants born to vaccinated mother 1
- Griffith row: confirmed 25; probable 3; infants 2; admitted 1; vaccinated mother 1
- Leeton row: confirmed 11; probable 0; infants 1; admitted 0; vaccinated mother 1
- Narrandera row: confirmed 5; probable 0; infants 1; admitted 0; vaccinated mother 0
- Murrumbidgee row: confirmed 0; probable 0; infants 0; admitted 0; vaccinated mother 0
- Hay row: confirmed 2; probable 0; infants 0; admitted 0; vaccinated mother 0
- Edward River row: confirmed 7; probable 1; infants 1; admitted 1; vaccinated mother 0
- Junee row: confirmed 3; probable 1; infants 1; admitted 0; vaccinated mother 1
- Cootamundra-Gundagai row: confirmed 15; probable 2; infants 1; admitted 1; vaccinated mother 1
- Snowy Valleys row: confirmed 9; probable 1; infants 1; admitted 1; vaccinated mother 0
- unit totals: confirmed 140; probable 10; infants 11; admitted 6; vaccinated mother 5

## Miss classification (main thread)

Missed at the decisive analytical step. The solver read every field and applied every stated rule correctly (the 90-day
episode rule, case status, split postcodes to the larger share, the extract day from the run report, the five-year
expected count) and stopped at rung 1: the PR-07 excess on the cases notified so far, Wagga Wagga 7.6 against Griffith
and Snowy Valleys 5.6. Its path and notes never mention the time a notification takes. This is the card's analyst test
exactly, so the round counts as a stump under the three rules. Every ask figure was right (the five clusters and all 50
quarterly cells; the token grader's 75 per cent on the CSV item is a matching artefact), so the ask layer is independent
of the call: the slide's cluster list is tied to the area the team goes to before the judge.
