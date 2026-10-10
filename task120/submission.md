# task120 · TY2025 income tax tier schedule

## Tags

**Domain:** Economics (public finance: state income tax revenue estimating, the top of the household income distribution).
**Analytical objective:** Descriptive & Distribution Analysis (household federal AGI cut at the top 10, 5 and 1 per cent marks, on the household unit the Conference's published tables count).

## 1. Final Recommendation

**Adopt TY2025 tier floors of $214,000, $318,000 and $742,000 for the top 10, 5 and 1 per cent of full-year resident household units.**

The household construction behind them reproduces 69 of 69 published cells, the methodology's condition for adoption. Not the floors off this year's returns, which split couples and count dependents as units of their own and match no published class cell. Not the federal filing unit the Legislative Fiscal Office tiers on, which leaves dependents' own returns outside the households that claim them and misses the $500,000 to $1M class every year. Not dropping dependents' returns, which misses every published total. Not the Department's all-filer table, which counts part-year residents and nonresidents.

## 2. Critical Components

1. **41,862** couples' separate TY2025 state returns are recombined on the federal primary TIN
2. **94,807** TY2025 resident returns are dependents' own returns, attached to the households that claim them
3. TY2025 has **582,544** full-year resident household units
4. The household construction reproduces **69 of 69** cells of the TY2022 to TY2024 Household Income Tables

## 3. Step-by-Step Solution

1. Kept full-year residents (residency code 1, methodology s.2) in `returns_processed_ty2022.parquet` to `returns_processed_ty2025.parquet` and joined each spouse's separate return to its partner's on `federal_primary_tin`: 41,862 TY2025 couples recombined.
2. Attached every resident return whose `filer_tin` is a `dependent_tin` in `dependents_schedule_tyYYYY.parquet` to the household of its `claimant_return_id`: 94,807 TY2025 returns attached, 582,544 household units.
3. Rebuilt every cell of `household_income_tables_ty2022.xlsx` to `household_income_tables_ty2024.xlsx`, Appendix A counties by the primary filer's county, in the published units: 69 of 69 reproduced, which methodology s.3 requires.
4. Took the TY2025 household AGI at the 10, 5 and 1 per cent marks: $214,000, $318,000 and $742,000 to the nearest $1,000.
5. Placed each payment and wage statement by its TIN as reported or through a resolved case in `tin_match_cases.csv`, and each Schedule D by `return_id`, into the tier of its household on the adopted floors.
6. Binned TY2025 estimated payments in `estimated_payments_ledger_2025.parquet` by Central-time arrival against the record layouts' due dates (the June instalment due Monday 16 June 2025), dropping items in `returned_items_2025.csv` not re-presented and paid, adding transfers of misapplied payments at the original payment's time and excluding TY2024 credit elections (methodology s.4): the twelve receipt cells below.
7. Summed withholding over `wage_statements_efile_ty2025.parquet` and `w2_paper_keyed_ty2025.txt`, and net capital gain as `amount_in_agi` on each return's latest accepted version in `amended_returns_log_ty2025.csv` over `schedule_d_extract_ty2025.csv`: the tier figures below.
8. Recommendation: adopt floors of $214,000, $318,000 and $742,000.

## 4. Deliverable Answers

### tier_schedule.xlsx

1. Schedule: top 10 per cent $214,000, top 5 per cent $318,000, top 1 per cent $742,000, on 582,544 full-year resident household units
2. The 69 published cells of the TY2022 to TY2024 tables beside their rebuild in the same units (household units, AGI in $ thousands, Appendix A county units): 69 of 69 matched
3. Estimated-tax receipts by tier and instalment, whole dollars:
   - Tier 1: instalment 1 $57,100,430, instalment 2 $60,982,470, instalment 3 $59,690,330, instalment 4 $62,279,690
   - Tier 2: instalment 1 $27,130,950, instalment 2 $28,344,190, instalment 3 $28,273,480, instalment 4 $29,413,200
   - Tier 3: instalment 1 $12,597,420, instalment 2 $13,026,520, instalment 3 $13,083,940, instalment 4 $13,625,350
4. Withholding, whole dollars:
   - Tier 1: $135,364,253
   - Tier 2: $229,035,640
   - Tier 3: $184,720,391
5. Net capital gain, whole dollars, and its share of the tier's AGI:
   - Tier 1: $3,147,270,635, 30.4%
   - Tier 2: $995,783,766, 10.1%
   - Tier 3: $339,052,645, 4.5%

### tier_floors.png

1. Household units at or above each AGI from $100,000 up, both axes on log scales
2. The three floors as vertical lines labelled $214,000, $318,000 and $742,000
3. Each tier's band labelled with its capital-gain share: tier 3 4.5%, tier 2 10.1%, tier 1 30.4%
4. The schedule in the title: TY2025 tier floors: $214,000 / $318,000 / $742,000
