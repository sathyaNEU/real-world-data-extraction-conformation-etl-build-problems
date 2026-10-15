## Tags

**Domain:** Sociology & Demography, social mobility and inequality measurement (which of a province's eight regions a foundation's 2027 mobility program goes to, by the intergenerational elasticity of children's adult earnings on their parents' long-run income, from a census-linked extract with one census year of parents' income for every family and five tax years for the families in which a parent filed every year).
**Analytical objective:** Descriptive & Distribution Analysis (how strongly children's earnings at 30 to 34 are tied to their parents' long-run income in each region, with the year-to-year swing in one year's income separated from the spread of long-run income).

## 1. Final Recommendation

**Opportunity Pathways goes to Selvane Valley in 2027.**
Selvane Valley's elasticity of children's earnings at 30 to 34 on their parents' long-run income is 0.49, against 0.40 in Torvale Metro, the next highest, a gap of 0.09. Not Halverston, which leads only when the slope is measured on the families with a five-year tax history, a narrower and better-off slice in most regions. Not Torvale Metro on the census year as it stands, whose wide spread of incomes hides less of its slope behind the year-to-year swing than Selvane Valley's narrow spread does. Not Kestry North, which leads only when the census year is rescaled by the filers' own reliability ratio, a ratio that belongs to their narrower spread.

## 2. Critical Components

1. Each region's elasticity across every child, the census year's spread less the region's year-to-year swing: Selvane Valley **0.49**, Torvale Metro **0.40**, Kestry North **0.39**, Halverston **0.39**, Wendmoor **0.38**, Danholt Lakes **0.37**, Ostler Plains **0.34**, Caskell Coast **0.29**
2. The children each elasticity rests on: Selvane Valley **6,106**, Torvale Metro **15,320**, Kestry North **4,220**, Halverston **6,868**, Wendmoor **5,261**, Danholt Lakes **7,726**, Ostler Plains **7,152**, Caskell Coast **5,549**, **58,202** in all
3. Selvane Valley leads Torvale Metro by **0.09**

## 3. Step-by-Step Solution

1. Took the children of linked_cohort_extract_2026.csv as opportunity_pathways_brief_2027.docx defines them (parents' census income above zero, earnings in at least one year at 30 to 34), each child's outcome the log of the average of the five years at 30 to 34 in child_earnings_2014_2022.csv in 2005 dollars by consumer_price_index_2000_2022.csv, a year without earnings counted as zero, each placed in its 2001 region through region_recode_2001_2021.csv: 58,202 children.
2. Took the log of each child's parents' 2000 census income, in 2005 dollars, as one year's measure of the family's long-run income.
3. Measured each region's year-to-year swing in parent_income_history_2001_2005.csv as the variance of each family's log income around its own 2001 to 2005 mean, four degrees of freedom a family, over the region's families with a history.
4. Divided each region's covariance of children's log earnings with the log census income by the variance of the log census income less the region's swing: Selvane Valley 0.49, Torvale Metro 0.40, the rest lower.
5. Counted each young person in bridges_participants_2019_2023.csv once, at the office where they first enrolled (bridges_program_guidelines_2019.pdf), following transfer_from back to the first record and joining each CaseTrack record left active at the April 2021 move to Northstar to the Northstar record at the same office with the same intake date and date of birth (day and month swapped in some CaseTrack entries), regions from bridges_offices.csv: 1,353 young people.
6. Took each region's spending from bridges_program_ledger_2019_2024.csv through the March 2024 close-out as its office's lines less the December year-end accruals (reversed in January at the central cost centre, the December invoices posted in January), plus the central team's other costs shared by the young people each region started (the guidelines).
7. Opportunity Pathways goes to Selvane Valley in 2027.

## 4. Deliverable Answers

### opportunity_pathways_2027.pdf

1. The recommendation: Opportunity Pathways goes to Selvane Valley in 2027, elasticity 0.49 against 0.40 in Torvale Metro, a gap of 0.09, with each region's elasticity and children and the Bridges figures below.

### opportunity_pathways_2027.xlsx

1. Each region's elasticity, to two decimals, and the children it rests on:
   - Selvane Valley: 0.49, 6,106 children
   - Torvale Metro: 0.40, 15,320 children
   - Kestry North: 0.39, 4,220 children
   - Halverston: 0.39, 6,868 children
   - Wendmoor: 0.38, 5,261 children
   - Danholt Lakes: 0.37, 7,726 children
   - Ostler Plains: 0.34, 7,152 children
   - Caskell Coast: 0.29, 5,549 children
2. Each region's Bridges young people started from 2019 to 2023 and spending, to the nearest thousand dollars:
   - Torvale Metro: 318 young people, $1,442,000
   - Halverston: 151 young people, $830,000
   - Kestry North: 117 young people, $682,000
   - Selvane Valley: 163 young people, $818,000
   - Danholt Lakes: 193 young people, $973,000
   - Caskell Coast: 128 young people, $689,000
   - Ostler Plains: 171 young people, $853,000
   - Wendmoor: 112 young people, $621,000

### region_elasticities_2027.png

1. A bar chart of the eight regions' elasticities, highest first, each bar labelled with its value to two decimals and its children, Selvane Valley highlighted.
