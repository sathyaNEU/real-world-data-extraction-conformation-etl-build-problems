## Tags

**Domain:** Biomedical & Clinical Research, diagnostic and biomarker accuracy (which of six candidate referral rules Sallowfield Health's community diabetes screening tablets carry in the 2027 season, by each rule's sensitivity for undiagnosed diabetes among everyone screened in 2026 when the confirmatory OGTT reached everyone the 2026 rule referred and a random fifth of the rest).
**Analytical objective:** Descriptive & Distribution Analysis (how the adults with undiagnosed diabetes among everyone screened are distributed across what each candidate rule would have flagged).

## 1. Final Recommendation

**Load HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher (A57G120), into the 2027 tablets.**
Among everyone screened in 2026 it would have referred 90% of the adults with undiagnosed diabetes, above the protocol's 85%, while referring 36.3% of the adults screened, the fewest of the two rules that qualify. Not the 2026 rule, or HbA1c of 6.0% or higher, which reads 94% among the adults with a complete OGTT but 79% among everyone screened, because the test reached the adults it does not refer only through the one-in-five draw. Not HbA1c of 5.7% or higher, which refers 28.2% but finds 80%. Not HbA1c of 5.5% or higher, which qualifies at 93% but refers 49.3%.

## 2. Critical Components

1. HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher, would have referred **90%** of the adults with undiagnosed diabetes among everyone screened and **36.3%** of the adults screened.
2. The 2026 rule, or HbA1c of 6.0% or higher, would have referred **79%** among everyone screened, under the 85% target.
3. HbA1c of 5.7% or higher, the closest rule with fewer referrals, would have referred **80%**.

## 3. Step-by-Step Solution

1. Took each adult's first screening of the 2026 season from screening_encounters_2026.csv, re-sent rows and return visits dropped per protocol 2.2: 37,269 adults.
2. Joined the complete tests in ogtt_results_2026.txt on the seven digits of PROGRAM_ID and read diabetes per protocol 5.1: 10,715 adults with a complete OGTT.
3. Let each adult with a complete OGTT stand for the adults of their 2026 group (referred by the 2026 rule, or not referred), at the group's adults over its complete tests, since protocol 6.2 counts every adult screened and the not-referred were tested only through the draw.
4. Applied each rule's tablet logic in candidate_referral_rules_2027.xlsx to the first screening's values: its share of the adults screened and its weighted share of the adults with undiagnosed diabetes.
5. Every rule referring fewer adults than A57G120 falls short of 85%: HbA1c of 6.0% at 51%, the 2026 rule or HbA1c of 6.0% at 79%, HbA1c of 5.7% at 80%, a risk score of 5 at 62%.
6. Counted each analyzer's cartridges in gq200_run_log_2026.csv: a run held twice (a copy stamped in UTC, four hours later in summer and five before 8 March, every other field the same) once, each run on the asset tag analyzer_asset_register.xlsx gives its serial that day, runs stopped at the cartridge check (gq200_error_codes.pdf) excluded, season days only: 40,248 in all.
7. Netted thessler_invoice_lines_2026.csv by the month each test was done, each credit memo line at the amount of the invoice line it applies to, tests of adults screened being the accessions in ogtt_results_2026.txt: $415,800.00 net, $409,255.00 for adults screened.
8. Per protocol 6.3 the qualifying rule with the fewest referrals is HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher, at 90% with 36.3% referred.

## 4. Deliverable Answers

### referral_rule_review_2027.xlsx

1. Each rule's share of adults with undiagnosed diabetes it would have referred (whole percent) and share of all adults screened it would have referred (one decimal place):
   - HbA1c of 6.0% or higher (A60): 51%; 8.4%
   - 2026 rule, or HbA1c of 6.0% or higher (R26A60): 79%; 24.9%
   - HbA1c of 5.7% or higher (A57): 80%; 28.2%
   - Risk score of 5 or higher (SC5): 62%; 35.9%
   - HbA1c of 5.7% or higher, or random glucose of 120 mg/dL or higher (A57G120): 90%; 36.3%
   - HbA1c of 5.5% or higher (A55): 93%; 49.3%
2. HbA1c test cartridges each analyzer used over the season:
   - A01: 3,486
   - A02: 2,686
   - A03: 2,966
   - A04: 4,216
   - A05: 3,735
   - A06: 3,535
   - A07: 3,692
   - A08: 3,864
   - A09: 2,588
   - A10: 3,449
   - A11: 3,071
   - A12: 2,960
3. What the laboratory billed, net of its credits, for the glucose tolerance tests done each month, and the part for tests of adults screened, in dollars:
   - March 2026: $14,630.00; $14,129.50
   - April 2026: $45,276.00; $44,506.00
   - May 2026: $43,120.00; $42,542.50
   - June 2026: $43,043.00; $42,234.50
   - July 2026: $40,463.50; $39,616.50
   - August 2026: $75,036.50; $74,151.00
   - September 2026: $55,286.00; $54,670.00
   - October 2026: $51,436.00; $50,666.00
   - November 2026: $47,509.00; $46,739.00

### referral_rule_2027_memo.docx

1. Recommendation: load HbA1c of 5.7% or higher, or a random glucose of 120 mg/dL or higher (A57G120), at 90% of the adults with undiagnosed diabetes and 36.3% of the adults screened.
2. Chart of each rule's two shares, the share of adults screened referred against the share of adults with undiagnosed diabetes referred, with the 85% target as a dashed line and the chosen rule ringed.
