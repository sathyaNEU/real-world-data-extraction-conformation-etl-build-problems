## Tags

**Domain:** Economics & Econometrics (forecasting and forecast evaluation: an employer business formation forecast from business applications after three states' filing reforms changed who applies).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Put 2,300 new first-time employers in the 2027 plan's first-time-employer line for the twelve core states.**
About half a million of Ohio's, Pennsylvania's and Michigan's applications in the twelve months to September 2026 were added by their integrated EIN filings, and set against the nine other states before and after each go-live the added applications, pooled over the three states, form employers within four quarters at under a fifth of the ordinary rate. Not each state's latest closed formation rate carried onto the twelve months, which prices the added applications at the share the closed cohorts held. Not the three states' own level before go-live as the counterfactual, which counts the rise every state shared as added applications. Not the filing's effect on formations carried as a monthly level, which misses that the twelve months hold far more added applications than the closed cohorts. Not 2025's first-time employers grown with applications, which grows formations as fast as applications.

## 2. Critical Components

1. About **half a million** of the three states' applications in the twelve months to September 2026 were added by the integrated filing (to the nearest 100,000).
2. Pooled over the three states, the added applications in the closed cohorts since go-live formed employers within four quarters at **under a fifth** of the rate of the applications the states would have had anyway.
3. The twelve states' applications in the twelve months will produce about **105,000** employer formations within four quarters (to the nearest 5,000).
4. Ohio, Pennsylvania and Michigan carry about **four fifths** of the 2,300.

## 3. Step-by-Step Solution

1. Read plan_2027_sizing_standard.docx and the Share 2025 tab of plan_2027_workbook.xlsx: each state's line is its 2025 share times the business formations within four quarters that the twelve months of applications to September 2026 will produce, the twelve added and rounded to the nearest 100.
2. Took the unadjusted BA_BA and BF_BF4Q rows of bfs_state_api_2026-10-14.json, whose formations close at June 2025 applications, and the integrated EIN filings' go-live dates in state_filing_changes_log.xlsx (Ohio 5 February 2024, Pennsylvania 13 May 2024, Michigan 12 August 2024).
3. Set each of the three states' ordinary applications at its 2022-2023 level for the calendar month times the nine other states' applications against their 2022-2023 level, the rest from the go-live month being added: 473,205 added of 1,073,402 applications in the twelve months.
4. Divided the closed cohorts' formations since go-live, less the ordinary applications at each state's pre-go-live rate (Ohio 7.21, Pennsylvania 7.37, Michigan 7.02 per cent), by the added applications at that rate, pooled over the three states: 0.163.
5. Counted 2024 first-time employers by business as first_time_employer_counting_notes.docx counts them (an EIN's accounts and its successors in suta_successor_transfers_2022-2025.csv as one, first pay date in 2024, no liability date before it in state_tax_registrations_2026-01-09.csv), each in the territory in sales_territories_2025.csv of its earliest registration's state.
6. Took wages from quarterly_wages_2024Q2-2025Q4.csv and from legacy_quarterly_wages_2022Q1-2024Q2.csv through client_migration_crosswalk_2024-06-15.csv at pay group 00 (the client's total), cents to dollars, leaving out quarters an account spent on Tax filing only, for the fourth quarter of 2025, each business's first quarter on payroll and 2024.
7. Read each business's signup channel from its first account, an account opened on the legacy system by its legacy_source_code in the crosswalk.
8. Priced the twelve months' ordinary applications in the three states at the state's rate and the added at 0.163 of it, the nine states' applications at their rate over every closed cohort, and added each state's formations times its share: 2,305.5, which goes into the plan as 2,300.

## 4. Deliverable Answers

### first_time_employer_plan_2027.xlsx

1. The first-time-employer line for 2027, to the nearest 100: 2,300.
2. 2024 first-time employers by sales territory (signed in 2024; still with us in the fourth quarter of 2025; gross wages we ran for them in their first quarter on payroll; gross wages we ran for them in 2024):
   - Ohio: 724 signed, 594 still with us, $6,303,064.11 in the first quarter, $24,995,811.51 in 2024
   - Pennsylvania: 410 signed, 341 still with us, $3,448,677.54 in the first quarter, $12,317,539.17 in 2024
   - Michigan: 419 signed, 334 still with us, $3,839,377.24 in the first quarter, $14,092,742.08 in 2024
   - Indiana-Kentucky: 197 signed, 153 still with us, $1,702,845.52 in the first quarter, $6,565,923.84 in 2024
   - Upper Midwest: 134 signed, 108 still with us, $1,086,114.72 in the first quarter, $4,391,458.26 in 2024
   - South and Plains: 157 signed, 128 still with us, $1,090,881.60 in the first quarter, $4,049,158.45 in 2024
3. 2024 first-time employers by signup channel:
   - accountant referral: 481
   - bank partner: 241
   - outbound: 277
   - partner marketplace: 242
   - web sign-up: 800

### first_time_employer_plan_2027_note.docx

4. One page stating the line, 2,300 new first-time employers for 2027, with the reason in two short paragraphs.
5. A bar chart under the text: two bars per sales territory, the 2024 first-time employers signed and those still with us in the fourth quarter of 2025, each labelled with its count as in item 2.
