# solver round: round 6 arch3

**Proxy score 81.6 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 39.6 of 58). Main call LANDED. 2 of 5 ask items cracked (80 per cent of tokens).

## Main call

golden: Open the formal assessment on corinurad (Uralexa) and acute kidney injury.

solver: Recommend opening the formal assessment for acute kidney injury with corinurad (Uralexa): it is the only signal where the month after starting (days 1-30) raises the risk, with an age-adjusted self-controlled rate ratio of 2.58 (95% CI 2.10-3.18), 21 kidney-injury admissions in that month among 2025 starters and about 13 of them caused by corinurad; falls with tasorexant (Somnevo; 0.99, 0.84-1.17) and acute pancreatitis with velaglutide (Gravera; 0.93, 0.52-1.64) are not supported.

tokens matched 2 of 2 (Open, Uralexa)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| signal_refinement_note.docx | 1 | 1 | 1 | 100% |
| signal_refinement_note.docx | 2 | 3 | 12 | 25% |
| signal_refinement_note.docx | 3 | 1 | 2 | 50% |
| signal_refinement_note.docx | 4 | 2 | 3 | 67% |
| new_users_by_year.csv | 1 | 11 | 11 | 100% |

## Solver's path

1. prescription_registry_2018-2026.parquet: matched each negative-package return to the latest earlier dispensing of the same pnr and package number and dropped both (7,699 returns, all full returns); combined M04AX02 and M04AB06 as corinurad using atc_ddd_index_2026.csv
2. New users per SOP-PV-14 section 5: no dispensing of the substance in the 365 days before, resident for all 365 days (civil_registration_extract.csv emigration and immigration dates), repeat starts allowed; 1,724 starts excluded for residency; this gives the new_users_by_year counts
3. Events per annex A from patient_registry_contacts joined to patient_registry_diagnoses on kontakt_id and kilde: LPR3 physical contacts merged when one starts within 4 hours of the previous end, LPR2 records merged when one starts on the day the previous ends; inpatient means 12 hours or more (LPR3) or pattype 0; the event needs the action diagnosis DN17 (or DK85; or DS00-DT14 plus a DW00-DW19 fall code on an emergency or inpatient admission); events dated by admission start
4. Events by 30-day block around the start among new users: corinurad 93 kidney-injury admissions in days 1-30 against about 35-40 in other months; tasorexant falls flat at about 140 a month (148); velaglutide pancreatitis flat (12)
5. Comparisons between different people (allopurinol, zopiclone and orlistat starters; matched_comparators.csv; national rates from population_and_admissions_2022-2025.csv) give tasorexant 2.27 / 3.77 / 3.51, but tasorexant users already had 3.43 times the national rate in the year before starting and corinurad users 0.60, so these mix up who starts the drug with what the drug does; rejected
6. Self-controlled case series (cases only, days 1-30 against all other observed time from 1 January 2018 or immigration to death, emigration or 30 June 2026, adjusted for age by calendar year): corinurad 2.58 (2.10-3.18); tasorexant 0.99 (0.84-1.17); velaglutide 0.93 (0.52-1.64); corinurad without age adjustment 2.75 (2.24-3.38)
7. Corinurad SOP new users in 2025 (13,461), kidney-injury admissions in days 1-30 censored at death or emigration: 21 (35 unmerged contact rows); caused = 21 x 1.58 / 2.58 = 12.86, rounded to 13

confidence: High that corinurad and acute kidney injury is the signal to recommend (robust across every self-controlled variant). Medium-high on the exact ratio: 2.58 rests on adjusting for age, and the unadjusted ratio is 2.75; the 21 admissions and 13 caused are the same under both.

notes: The SOP does not say how the rate ratio is estimated or whether to adjust for age, so 2.58 against 2.75 depends on that choice. The request does not say whether the CSV should list only the three signal medicines or the comparators too; the comparators' counts before 2022 are incomplete because they were extracted from 2022 onward.

### signal_refinement_note.docx (solver's answers)
- signal named: Acute kidney injury with corinurad (Uralexa); falls with tasorexant and acute pancreatitis with velaglutide not supported
- rate ratio for days 1-30 after the start with 95% CI: rate ratio 2.58, 95% CI 2.10 to 3.18 (two decimals; self-controlled case series adjusted for age by calendar year; 2.75, 2.24 to 3.38 without the age adjustment)
- admissions for the event in the month after the start among 2025 starters: 21 inpatient acute kidney injury admissions (whole admissions)
- admissions caused by the medicine: 13 admissions (21 x (2.58-1)/2.58 = 12.86, rounded to the nearest whole admission)

### new_users_by_year.csv (solver's answers)
- new users of corinurad, 2022-2025: 2022: 11,182; 2023: 12,903; 2024: 13,712; 2025: 13,461 persons
- new users of tasorexant, 2022-2025: 2022: 1,946; 2023: 3,895; 2024: 4,546; 2025: 4,625 persons
- new users of velaglutide, 2022-2025: 2022: 6,153; 2023: 18,338; 2024: 21,376; 2025: 20,070 persons
- comparator medicines, if included: allopurinol 7,339 / 7,026 / 6,505 / 6,375; orlistat 19,406 / 18,153 / 17,389 / 16,523; zopiclone 8,260 / 8,108 / 8,137 / 7,910 persons for 2022 / 2023 / 2024 / 2025
