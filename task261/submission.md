## Tags

**Domain:** Survey Research & Official Statistics, complex survey estimation and variance (where a life insurer's 2027 retirement range draws its segment boundaries between neighbouring age groups, from a stratified, clustered, multiply imputed household wealth survey released with replicate weights).
**Analytical objective:** Descriptive & Distribution Analysis (how household net worth is distributed across six age groups of the older partner, and which neighbouring groups' medians differ by more than the error of the difference).

## 1. Final Recommendation

**Set Kelvane Life's 2027 retirement range on five segments: under 35, 35 to 44, 45 to 54, 55 to 64, and 65 and over.**
The boundary at 65 decides it: 55 to 64 and 65 to 74 differ by $258,000 in median household net worth, 2.7 times the $95,000 standard error of that difference on the survey's replicate weights, so they stay apart. Not four segments with 55 and over as one, which comes from adding the two groups' own standard errors as if they were independent samples ($165,000, 1.6 times); the groups share the survey's areas and their medians move together. Not six with 75 and over on its own, which needs errors that ignore the clustering; the $233,000 difference between 65 to 74 and 75 and over is only 1.6 times its $149,000 standard error.

## 2. Critical Components

1. Median household net worth by the older partner's age group: under 35 **$69,000**, 35 to 44 **$281,000**, 45 to 54 **$534,000**, 55 to 64 **$790,000**, 65 to 74 **$1,048,000**, 75 and over **$815,000**
2. Standard error of each neighbouring difference, taken from the difference itself on the 200 replicate weights with the implicates' variance added: **$24,000**, **$45,000**, **$77,000**, **$95,000**, **$149,000**, youngest pair first
3. 55 to 64 against 65 to 74: **$258,000**, **2.7** times its standard error, kept apart; 65 to 74 against 75 and over: **-$233,000**, **1.6** times, one segment

## 3. Step-by-Step Solution

1. Placed each household of nhws2025_household_summary.csv by the older of its reference person and partner (relationship codes 1 to 3 in nhws2025_persons.csv), as retirement_range_2027_brief.docx sets out, into the six age groups.
2. As nhws2025_user_guide.pdf sets out for an estimate, took each group's weighted median net worth on each of the five implicates and averaged them: $69,000, $281,000, $534,000, $790,000, $1,048,000 and $815,000.
3. Recomputed each neighbouring difference with each of the 200 weights in nhws2025_replicate_weights.csv on implicate 1 and added 1.2 times the variance of the five implicate differences, the user guide's method applied to the difference: standard errors $24,000, $45,000, $77,000, $95,000 and $149,000.
4. Applied the brief's rule (apart above 1.96 times the standard error): every boundary holds except 65 to 74 against 75 and over (1.6 times), five segments.
5. Counted the households holding a pension in ria_pension_accounts_20261231.csv at 31 December 2026, members alive on that date in crm_clients_20270112.csv with merged numbers followed, a partner whose 2026 death lifetime_annuity_lives_20270112.csv records counted as dead though the register still holds them, a non-client partner placed from ria_nominations_20261231.csv, a member whose rows repeat one balance and payment taken once, and a December death's pension with a reversionary counted with the survivor (retirement_income_account_pds_2026.pdf, section 5): 445, 1,169 and 742 households.
6. Took each contract's life in payment at 31 December 2026 from lifetime_annuity_lives_20270112.csv (a reversionary's amount only after the annuitant's death, so a former partner still named on a contract is not paid, deferred annuities not yet paying left out), took back the January 2027 anniversary increase (lifetime_annuity_key_facts_2026.pdf) and placed the paid life's household the same way: 179, 468 and 280 households.
7. Set the 2027 range on five segments: under 35, 35 to 44, 45 to 54, 55 to 64, and 65 and over.

## 4. Deliverable Answers

### retirement_segments_2027.docx

1. The recommendation: five segments, under 35, 35 to 44, 45 to 54, 55 to 64, and 65 and over.
2. The deciding boundary: 55 to 64 against 65 to 74 differs by $258,000, 2.7 times its $95,000 standard error, so they stay apart; 65 to 74 against 75 and over differs by -$233,000, 1.6 times its $149,000 standard error, so they share a segment.
3. Why the difference's own error: the groups are drawn from the same 120 survey areas and their medians move together across the replicates (correlation 0.70); the two groups' errors added as if independent give $165,000 and four segments.

### retirement_segments_2027.xlsx

1. Each age group's median household net worth and standard error:
   - Under 35: $69,000, $7,000
   - 35 to 44: $281,000, $25,000
   - 45 to 54: $534,000, $50,000
   - 55 to 64: $790,000, $93,000
   - 65 to 74: $1,048,000, $136,000
   - 75 and over: $815,000, $139,000
2. Each neighbouring pair's difference in median, its standard error, the difference over its standard error and the rule's outcome:
   - Under 35 / 35 to 44: $212,000, $24,000, 8.9, kept apart
   - 35 to 44 / 45 to 54: $253,000, $45,000, 5.6, kept apart
   - 45 to 54 / 55 to 64: $256,000, $77,000, 3.3, kept apart
   - 55 to 64 / 65 to 74: $258,000, $95,000, 2.7, kept apart
   - 65 to 74 / 75 and over: -$233,000, $149,000, -1.6, one segment
3. Our customer households in each of the three groups from 55, by the older partner's age at 31 December 2026: households holding a Retirement Income Account pension, their combined balance and their annual payments set for 2026-27; households with a lifetime annuity in payment and the annual income it was paying them:
   - 55 to 64: 445 households, $210,509,000, $11,589,000; 179 households, $3,653,000
   - 65 to 74: 1,169 households, $521,126,000, $30,350,000; 468 households, $9,041,000
   - 75 and over: 742 households, $249,685,000, $18,003,000; 280 households, $5,510,000

### adjacent_differences_2027.svg

1. Each neighbouring pair's difference in median net worth with its 95 per cent interval (the difference plus or minus 1.96 standard errors) against a zero line: four intervals clear of zero, 65 to 74 / 75 and over (-$525,000 to $59,000) crossing it.
