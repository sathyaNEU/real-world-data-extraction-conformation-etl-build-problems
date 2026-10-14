# task255 submission

## Tags

**Domain:** Actuarial Science & Insurance, claims frequency and severity (a ground-up liability severity curve fitted to a risk pool's claims record, open suits included, which holds an occurrence only above its member's deductible and only up to the pool's retention, to set the pool's excess attachment).
**Analytical objective:** Descriptive & Distribution Analysis (the tail of the ground-up severity distribution at each quoted attachment).

## 1. Final Recommendation

**Keep the first $4,000,000 of each 2027 liability occurrence: Fallowmere's 2027 retention is the $4.0 million quoted attachment, which the pool expects 0.74 of its 2027 occurrences to cost more than.**

The next quote down, $3.0 million, expects 1.25, more than the risk financing policy's one a year. Not $3.0 million from the same fit run on the closed files alone, which leaves out the 20 suits of 2014 to 2021 still open while the excess insurer defends them: each has used the pool's whole layer, so dropping them takes a fifth of the occurrences that reached the retention out of the record and leaves 0.70 above $3.0 million. Not $2.0 million, where a lognormal fitted to the recorded costs as if they were every occurrence's full cost points, because the record holds only occurrences that used up their member's deductible and stops at the pool's retention. Not $2.5 million, where treating the occurrences stopped at the retention as censored, but not the deductible as a floor, points.

## 2. Critical Components

1. The record the curve is fitted to: **820** occurrences of accident years 2014 to 2021, **800** closed and **20** suits still open with the pool's layer paid, **108** of them stopped at the pool's retention (**67** at $250,000 and **41** at $500,000).
2. The ground-up severity curve at 2027 cost: lognormal with log mean **10.18** and log standard deviation **1.71**.
3. Expected 2027 occurrences costing more than $3.0 million: **1.25**; more than $4.0 million: **0.74**.

## 3. Step-by-Step Solution

1. Took every liability occurrence of accident years 2014 to 2021 from liability_closed_claims_tallowmark_2014-2020.xlsx (421, closed before the July 2020 conversion) and liability_loss_run_brisbrook_2026-09-30.csv (399, 20 of them still open), the years risk_financing_policy_2026.pdf names: 820 occurrences.
2. Read each occurrence's recorded cost as its member's deductible plus what the pool has paid and still reserves, indemnity and defense, the policy's cost from the first dollar: the 20 open suits have the pool's whole layer paid, and 108 occurrences sit at the retention liability_coverage_memorandum_2026.pdf gives for their year, 67 at $250,000 and 41 at $500,000.
3. Brought every cost, deductible and retention to 2027 cost by the ratio of the 2027 claim cost index to the accident year's, from the index in actuarial_study_2026_selected_exhibits.pdf, as the policy sets.
4. Fitted the policy's lognormal by maximum likelihood to the record as the memorandum says it comes to exist (an occurrence reaches the pool only once its member has paid the deductible, and nothing above the retention is recorded), each occurrence truncated at its deductible and the 108 at the retention censored there: log mean 10.18, log standard deviation 1.71.
5. Turned the curve into expected 2027 occurrences above each attachment in excess_liability_indications_2027.pdf by the policy's formula from the actuary's 228.7 above $25,000: 1.25 above $3.0 million and 0.74 above $4.0 million.
6. Applied the policy's retention test, the lowest quoted attachment with one or fewer: $4.0 million.
7. Priced each attachment at its two indicated rates on the members' 2027 total operating expenditures from exposure_declarations_2027.xlsx, each member's total once ($5,668,433,420), and the units on vehicle_schedule_log_2022-2026.csv at September 30, 2026, one per vehicle under the latest unit number added for it (5,649).
8. Recommended keeping the first $4,000,000 of each 2027 liability occurrence.

## 4. Deliverable Answers

### retention_2027.xlsx

1. Recommended 2027 retention: $4,000,000 per occurrence, from the first dollar.
2. Expected 2027 occurrences costing more than each quoted attachment (two decimals) and the 2027 premium each would carry (nearest dollar):
   - $1,000,000: 7.46 occurrences, $1,770,565
   - $1,500,000: 4.03 occurrences, $1,414,020
   - $2,000,000: 2.53 occurrences, $1,180,073
   - $2,500,000: 1.73 occurrences, $1,017,817
   - $3,000,000: 1.25 occurrences, $881,870
   - $4,000,000: 0.74 occurrences, $735,429
   - $5,000,000: 0.48 occurrences, $641,333
3. The exposure the quotes are rated on, by class of member (members, 2027 operating expenditures to the nearest thousand dollars, scheduled vehicles):
   - City: 33 members, $4,992,928 thousand, 4,207 vehicles
   - Fire district: 9 members, $121,458 thousand, 301 vehicles
   - Water-sewer district: 6 members, $126,705 thousand, 241 vehicles
   - Port district: 3 members, $141,394 thousand, 189 vehicles
   - Transit authority: 2 members, $218,248 thousand, 541 vehicles
   - Park and recreation district: 4 members, $50,231 thousand, 143 vehicles
   - Library district: 3 members, $17,470 thousand, 27 vehicles
   - All members: 60 members, $5,668,433 thousand (rounded from the exact total), 5,649 vehicles

### attachment_test_2027.png

1. Bar chart of the expected 2027 occurrences costing more than each quoted attachment from $1.0 million to $5.0 million, each bar labelled to two decimals, the risk financing policy's one-a-year line drawn across, and the $4.0 million bar highlighted and marked as recommended.
