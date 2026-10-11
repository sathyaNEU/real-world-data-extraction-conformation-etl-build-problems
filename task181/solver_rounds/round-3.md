# solver round: round 3

**Proxy score 59.0 / 100** (recommendation 5.0 of 35, instruction 7.0 of 7, asks 47.0 of 58). Main call missed. 2 of 3 ask items cracked (80 per cent of tokens).

## Main call

golden: Send the response team to Griffith this week.

solver: Send Janice Barker's team to Wagga Wagga this week: 9 cases with specimens collected 21 Sep–4 Oct 2026 against an expected 1.4 (2021–2025 mean) give the largest excess, 7.6, ahead of Griffith and Snowy Valleys (7 vs 1.4, excess 5.6 each); the school clusters there are Wollundry Public School (3 student cases) and Bolton Park High School (2 student cases).

tokens matched 2 of 2 (Send, Griffith)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| response_team_brief.pptx | 1 | 1 | 1 | 100% |
| response_team_brief.pptx | 2 | 3 | 5 | 60% |
| pertussis_cases_by_lga.csv | 1 | 10 | 12 | 83% |

## Solver's path

1. Run report SIPHU_PERTUSSIS_LINELIST_job_20261005_0700.txt: extract day Mon 5 Oct 2026 (Labour Day); sha256 and 1118 rows match pertussis_notifications_2019-2026.csv; no row received after run start
2. PR-07 s3.3: grouped notifications by person_id into 90-day cases, confirmed if any notification confirmed -> 1053 cases (988 single-notification, 65 with two)
3. PR-07 s3.4 + postcode_lga_concordance.xlsx: postcode to LGA, split postcodes to the larger share (2652 Wagga Wagga, 2655 Lockhart, 2665 Coolamon, 2706 Murrumbidgee, 2722/2727 Cootamundra-Gundagai, 2729 Snowy Valleys); dropped cases outside the ten unit LGAs
4. PR-07 s4.2-4.3: observed = first specimen 21 Sep–4 Oct 2026; expected = sum over 2021–2025 of the same dates / 5 -> Wagga Wagga 9-1.4=7.6, Griffith 7-1.4=5.6, Snowy Valleys 7-1.4=5.6, Cootamundra-Gundagai 2-0.6=1.4, others <=0.6
5. PR-07 s5.1: Wagga Wagga cases with role Student and specimen 5 Sep–4 Oct; normalised school names and checked against school_rosters_term3_2026.xlsx (dob/sex/postcode all match) -> Wollundry Public School 3, Bolton Park High School 2; excluded Bolton Park staff case, Wollundry Preschool child, Fernleigh Road (1 in window)
6. PR-07 s7.1: cases with first specimen 1 Jan–31 Aug 2026 in unit LGAs -> 150 (140 confirmed, 10 probable)
7. PR-07 s6.1: infant = first specimen before dob + 6 months -> 11 infants
8. PR-07 s6.2: respiratory_admissions mrn (numeric) = case mrn, admission within ±14 days of the first specimen -> 6 admitted
9. PR-07 s6.3: case mrn = birth_records baby_mrn -> mother_medicare_no = antenatal register card (spaces removed) + irn; dTpa dose in that pregnancy (from birth date minus gestation) at least 14 days before birth -> 5 vaccinated (two late doses at 10-11 days and prior-pregnancy doses excluded)
10. Reconciled with cd_weekly_report_2026_wk35.pdf: notifications by local received date 1 Jan–30 Aug = 162 (Wagga Wagga 73, Griffith 29, etc.), last 4 weeks = 25, 2025 same period = 242 — all match

confidence: High: the area call holds under window-boundary variations, cluster students all match the rosters, and the notification counts reproduce the week 35 report exactly.

notes: Murrumbidgee had no cases in the period and is kept as a row of zeros; 5 period cases living in Lockhart (3) and Albury (2) are excluded under PR-07 s1.2. Probable counts are serology-only cases because the extract has no probable cases without laboratory evidence.

### response_team_brief.pptx (solver's answers)
- area the team goes to: Wagga Wagga — observed cases 21 Sep–4 Oct 2026 = 9; expected = 1.4 (mean of 2021–2025, same dates); excess = 7.6 cases (runner-up Griffith and Snowy Valleys, excess 5.6 each)
- school clusters in that area with case counts: Wollundry Public School: 3 student cases; Bolton Park High School: 2 student cases (specimens 5 Sep–4 Oct 2026)

### pertussis_cases_by_lga.csv (solver's answers)
- Wagga Wagga: confirmed 63; probable 2; infants <6 months 3; infants admitted 2; infants born to vaccinated mother 1
- Griffith: confirmed 25; probable 3; infants 2; admitted 1; vaccinated mother 1
- Leeton: confirmed 11; probable 0; infants 1; admitted 0; vaccinated mother 1
- Narrandera: confirmed 5; probable 0; infants 1; admitted 0; vaccinated mother 0
- Murrumbidgee: confirmed 0; probable 0; infants 0; admitted 0; vaccinated mother 0
- Hay: confirmed 2; probable 0; infants 0; admitted 0; vaccinated mother 0
- Edward River: confirmed 7; probable 1; infants 1; admitted 1; vaccinated mother 0
- Junee: confirmed 3; probable 1; infants 1; admitted 0; vaccinated mother 1
- Cootamundra-Gundagai: confirmed 15; probable 2; infants 1; admitted 1; vaccinated mother 1
- Snowy Valleys: confirmed 9; probable 1; infants 1; admitted 1; vaccinated mother 0
- unit totals: confirmed 140; probable 10; infants 11; admitted 6; vaccinated mother 5 (cases, 1 Jan–31 Aug 2026)

## Miss classification (main thread)

**Landed: no.** The token match reads 2 of 2 because the solver names Griffith as the runner-up, so `--landed no` was passed by the main thread after reading both sentences.

**Where it missed: the decisive analytical step (rung 1), the same place as round 2.** Every reading step held: the run report and extract day (Labour Day), PR-07 3.3 episodes, 3.4 split postcodes, the 4.2 to 4.3 five-year expected count, the 5.1 roster checks, and all CSV figures. It then set the cases notified so far against the expected count and called Wagga Wagga (9 against 1.4, excess 7.6) ahead of Griffith and Snowy Valleys (5.6 each). It said nothing about specimens collected in the window and not yet notified, or about Inland Pathology's slower route into the extract. That is a valid analytical miss under the three rules: nothing planted, no data-semantics trap, and no stated rule left unapplied.

**Call-dependence works.** Because the area was wrong, the slide carried Wagga Wagga's clusters (Wollundry 3, Bolton Park High School 2), not the golden Griffith list (Banna Avenue 5, Kooyoo Street 2). The proxy fell from 65.2 to 59.0. The remaining partial slide hits are token overlap (the runner-up mention, and "Public School"), not right answers.

**Isolation note.** While this round ran, the task180 builder's working files (calib.py, t1/, t2/) were under the scratchpad beside the sandbox. They belong to a different task and hold nothing about task181, so they could not inform this solver. The round stands.

**Decision: PASS.** The task goes to stage 7, the determinism judge.
