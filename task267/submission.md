## Tags

**Domain:** Biomedical & Clinical Research, diagnostic and biomarker accuracy (which of six candidate referral rules Sallowfield Health's community diabetes screening tablets carry in the 2027 season, by each rule's sensitivity for undiagnosed diabetes among everyone screened in 2026 when the confirmatory OGTT reached everyone the 2026 rule referred and a random fifth of the rest).
**Analytical objective:** Descriptive & Distribution Analysis (how the adults with undiagnosed diabetes among everyone screened are distributed across what each candidate rule would have flagged).

## 1. Final Recommendation

**Load HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher (A57G120), into the 2027 tablets.**
Among everyone screened in 2026 it would have referred 91.3% of the adults with undiagnosed diabetes, above the protocol's 85%, while referring 35.9% of the adults screened, the fewest of the two rules that qualify. Not the 2026 rule, or HbA1c of 6.0% or higher, which reads 93.5% among the adults with a complete OGTT but 77.1% among everyone screened, because the test reached the adults it does not refer only through the one-in-five draw. Not HbA1c of 5.7% or higher, which refers 28.1% but finds 79.1%. Not HbA1c of 5.5% or higher, which qualifies at 92.6% but refers 48.7%.

## 2. Critical Components

1. HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher, would have referred **91.3%** of the adults with undiagnosed diabetes among everyone screened and **35.9%** of the adults screened.
2. The 2026 rule, or HbA1c of 6.0% or higher, would have referred **77.1%** among everyone screened, under the 85% target.
3. HbA1c of 5.7% or higher, the only rule with fewer referrals that comes close, would have referred **79.1%**.

## 3. Step-by-Step Solution

1. Took each adult's first screening of the 2026 season from screening_encounters_2026.csv, re-sent rows and return visits dropped per protocol 2.2: 38,601 adults.
2. Joined the complete tests in ogtt_results_2026.txt on the seven digits of PROGRAM_ID and read diabetes per protocol 5.1: 11,168 adults with a complete OGTT.
3. Let each adult with a complete OGTT stand for the adults of their 2026 group (referred by the 2026 rule, or not referred), at the group's adults over its complete tests, since protocol 6.2 counts every adult screened and the not-referred were tested only through the draw.
4. Applied each rule's tablet logic in candidate_referral_rules_2027.xlsx to the first screening's values: its share of the adults screened and its weighted share of the adults with undiagnosed diabetes.
5. Every rule referring fewer adults than A57G120 falls short of 85%: HbA1c of 6.0% at 50.9%, the 2026 rule or HbA1c of 6.0% at 77.1%, HbA1c of 5.7% at 79.1%, a risk score of 5 at 59.0%.
6. Counted each analyzer's cartridges in gq200_run_log_2026.csv: a run held twice (a copy four hours later, every other field the same) once, each run on the asset tag analyzer_asset_register.xlsx gives its serial that day, runs stopped at the cartridge check (gq200_error_codes.pdf) excluded, season days only: 41,713 in all.
7. Netted thessler_invoice_lines_2026.csv by the month each test was done, each credit memo line at the amount of the invoice line it applies to, tests of adults screened being the accessions in ogtt_results_2026.txt: $435,088.50 net, $428,274.00 for adults screened.
8. Per protocol 6.3 the qualifying rule with the fewest referrals is HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher, at 91.3% with 35.9% referred.

## 4. Deliverable Answers

### referral_rule_review_2027.xlsx

1. Each rule's share of adults with undiagnosed diabetes it would have referred and share of all adults screened it would have referred, per cent to one decimal place:
   - HbA1c of 6.0% or higher (A60): 50.9%; 8.5%
   - 2026 rule, or HbA1c of 6.0% or higher (R26A60): 77.1%; 24.5%
   - HbA1c of 5.7% or higher (A57): 79.1%; 28.1%
   - Risk score of 5 or higher (SC5): 59.0%; 35.6%
   - HbA1c of 5.7% or higher, or random glucose of 120 mg/dL or higher (A57G120): 91.3%; 35.9%
   - HbA1c of 5.5% or higher (A55): 92.6%; 48.7%
2. HbA1c test cartridges each analyzer used over the season:
   - A01: 3,602
   - A02: 4,068
   - A03: 3,661
   - A04: 3,134
   - A05: 3,879
   - A06: 3,547
   - A07: 3,036
   - A08: 3,243
   - A09: 3,040
   - A10: 3,511
   - A11: 3,560
   - A12: 3,432
3. What the laboratory billed, net of its credits, for the glucose tolerance tests done each month, and the part for tests of adults screened, in dollars:
   - March 2026: $15,207.50; $14,630.00
   - April 2026: $43,428.00; $42,812.00
   - May 2026: $51,513.00; $50,781.50
   - June 2026: $46,585.00; $45,699.50
   - July 2026: $44,660.00; $43,890.00
   - August 2026: $77,731.50; $76,769.00
   - September 2026: $58,866.50; $57,981.00
   - October 2026: $47,355.00; $46,585.00
   - November 2026: $49,742.00; $49,126.00

### referral_rule_2027_memo.docx

1. Recommendation: load HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher (A57G120), at 91.3% of the adults with undiagnosed diabetes and 35.9% of the adults screened.
2. Chart of each rule's two shares, the share of adults screened referred against the share of adults with undiagnosed diabetes referred, with the 85% target as a dashed line and the chosen rule ringed.
