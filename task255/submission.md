# task255 submission

## Tags

**Domain:** Actuarial Science & Insurance, claims frequency and severity (the ground-up severity of a public entity risk pool's liability occurrences, law enforcement liability against the other coverage parts, fitted to a record held above each member's deductible and up to the pool's retention, to set the pool's excess attachment).
**Analytical objective:** Descriptive & Distribution Analysis (the tail of the ground-up severity distribution at each quoted attachment).

## 1. Final Recommendation

**Keep the first $4,000,000 of each 2027 liability occurrence: Fallowmere's 2027 retention is the $4.0 million quoted attachment, which the pool expects 0.8 of its 2027 occurrences to cost more than.**

The next quote down, $3.0 million, expects 1.2, more than the risk financing policy's one a year. Not $2.0 million, where one lognormal fitted to every occurrence and carried by the actuary's 460.0 occurrences above $25,000 points: law enforcement occurrences run a far longer tail than the other coverage parts, the record rejects one curve for both, and the one curve takes its shape from the other parts. Not $2.5 million, where law enforcement is given its own log mean but the other parts' spread.

## 2. Critical Components

1. The record of accident years 2014 to 2021: **1,071** occurrences, **314** of them law enforcement liability (every one of the **25** stopped at the pool's retention among them, **8** still open with the pool's layer paid) and **757** under the other four coverage parts.
2. The actuary's expected 2027 occurrences costing more than $25,000: **85.0** law enforcement liability and **375.0** under the other parts.
3. Expected 2027 occurrences costing more than $3.0 million: **1.2**; more than $4.0 million: **0.8**.

## 3. Step-by-Step Solution

1. Took every liability occurrence of accident years 2014 to 2021 from liability_closed_claims_tallowmark_2014-2020.xlsx (610, closed before the July 2020 conversion) and liability_loss_run_brisbrook_2026-09-30.csv (461, 8 of them still open), the years risk_financing_policy_2026.pdf names: 1,071 occurrences.
2. Read each occurrence's cost as its member's deductible plus what the pool has paid and still reserves, indemnity and defense, the policy's cost from the first dollar; 25 sit at the retention liability_coverage_memorandum_2026.pdf gives for their year, 15 at $500,000 and 10 at $1,000,000, all of them law enforcement liability (LEL in the legacy run, LAWE in the current one).
3. Brought every cost, deductible and retention to 2027 cost by the ratio of the 2027 claim cost index to the accident year's, from actuarial_study_2026_selected_exhibits.pdf, as the policy sets.
4. Fitted the lognormal by maximum likelihood to the record as it comes to exist, each occurrence truncated at its deductible and the 25 at the retention censored there, separately for law enforcement liability (log mean 8.52, log standard deviation 2.37) and for the other four parts (9.89 and 1.14); one curve for every occurrence fits the record far worse (twice the log likelihood difference 158.2 on two degrees of freedom) and so does a common spread (28.8 on one).
5. Carried Exhibit 6's 85.0 law enforcement and 375.0 other occurrences above $25,000 by their own curves to each attachment in excess_liability_indications_2027.pdf and added them, the policy's expected number: 1.2 above $3.0 million and 0.8 above $4.0 million; each layer's expected 2027 losses are the same projections times each group's expected cost between the attachment and the attachment plus the indications' $10,000,000 limit for an occurrence above $25,000.
6. Applied the policy's retention test, the lowest quoted attachment with one or fewer: $4.0 million.
7. Recommended keeping the first $4,000,000 of each 2027 liability occurrence.

## 4. Deliverable Answers

### retention_2027.xlsx

1. Recommended 2027 retention: $4,000,000 per occurrence, from the first dollar.
2. Expected 2027 occurrences costing more than each quoted attachment (one decimal) and the 2027 losses its $10,000,000 layer should be expected to pay (nearest hundred thousand dollars):
   - $1,000,000: 4.6 occurrences, $8,300,000 expected layer losses
   - $1,500,000: 2.8 occurrences, $6,600,000 expected layer losses
   - $2,000,000: 2.0 occurrences, $5,500,000 expected layer losses
   - $2,500,000: 1.5 occurrences, $4,700,000 expected layer losses
   - $3,000,000: 1.2 occurrences, $4,100,000 expected layer losses
   - $4,000,000: 0.8 occurrences, $3,300,000 expected layer losses
   - $5,000,000: 0.6 occurrences, $2,700,000 expected layer losses

### attachment_test_2027.png

1. Bar chart of the expected 2027 occurrences costing more than each quoted attachment from $1.0 million to $5.0 million, each bar labelled to one decimal, the risk financing policy's one-a-year line drawn across, and the $4.0 million bar highlighted and marked as recommended.
