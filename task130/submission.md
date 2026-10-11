# task130 · Red Cedar Valley Schools, the Northcourt care management baseline for 2027-28

## Tags

**Domain:** Actuarial Science & Insurance (claims frequency and severity: a self-insured school district's baseline for its care management vendor's share of savings).
**Analytical objective:** Forecasting & Predictive Modeling (the allowed claims per member month that 140 members chosen on their 2026 claims would incur in a programme year that has not started, by tier, medical and pharmacy).

## 1. Final Recommendation

**Certify a programme baseline of $3,541 per member per month for the 140 enrolled members ($2,157 medical, $1,384 pharmacy), built tier by tier from what the 140 members Northcourt's model flagged on 2024 claims for its 2025 proposal, never enrolled, cost from April 2025 to March 2026, trended 24 months.**

Not the enrolled members' own 2026 claims carried forward at the renewal trend, which treats the year they were picked for as a year they will repeat. Not the renewal letter's plan-wide projection, which prices the average member rather than the 140 at the top of the plan.

## 2. Critical Components

1. The untreated comparison is the **140** members on Northcourt's RFP 2025-07 list, matched to Ellery member IDs through the conversion crosswalk
2. Their allowed claims per member month are taken over **1 April 2025 to 31 March 2026**, by tier, medical and pharmacy
3. That experience is trended **24 months** at **6.5%** medical and **9.0%** pharmacy
4. The tiers are weighted by the final list's enrolled members, **18, 38, 41 and 43**
5. The programme baseline is **$2,157** medical and **$1,384** pharmacy, **$3,541** in total

## 3. Step-by-Step Solution

1. Netted the Ellery claim lines as the extract dictionary describes (a frequency 7 claim drops the claim it replaces, a void reverses its amounts, a denied line has no allowed amount) and the Quarrystone B2 reversals against their fills, linking pharmacy to members on employee number and person code.
2. Counted member months from the eligibility spans and dated each claim by first date of service or fill date, both as Schedule C.1 defines them.
3. Took the 140 members and tiers on the final stratification list of 5 March 2027 (the January draft is superseded) and computed their 2026 allowed PMPM paid through 28 February 2027, without completion per Schedule C.2: tier 1 runs at $15,338 medical and $2,780 pharmacy.
4. Matched all 140 Bramwell member numbers on the RFP 2025-07 list to Ellery member IDs through the conversion crosswalk; the award was suspended in April 2025, so none of them was ever in the programme.
5. Divided each bid tier's allowed claims from 1 April 2025 to 31 March 2026 by its member months and trended them 24 months, midpoint to midpoint, per Schedule C.1(g) at the renewal letter's 6.5% and 9.0%: tier 1's baseline is $4,177 medical and $899 pharmacy.
6. Weighted the four tier baselines by enrolled members per Schedule C.1(h): $2,157 medical and $1,384 pharmacy, $3,541 in total.
7. Recommendation: certify a programme baseline of $3,541 per member per month.

## 4. Deliverable Answers

### cohort_baseline_2027.xlsx
1. One row per tier, whole dollars per member per month:
   - Tier 1: 18 enrolled members, 2026 allowed PMPM $15,338 medical and $2,780 pharmacy, baseline PMPM $4,177 medical and $899 pharmacy
   - Tier 2: 38 enrolled members, 2026 allowed PMPM $8,182 medical and $1,242 pharmacy, baseline PMPM $2,729 medical and $2,072 pharmacy
   - Tier 3: 41 enrolled members, 2026 allowed PMPM $4,828 medical and $1,603 pharmacy, baseline PMPM $1,172 medical and $1,484 pharmacy
   - Tier 4: 43 enrolled members, 2026 allowed PMPM $3,413 medical and $1,262 pharmacy, baseline PMPM $1,745 medical and $884 pharmacy
2. Programme baseline across all 140 members, whole dollars per member per month: $2,157 medical, $1,384 pharmacy, $3,541 in total

### baseline_certification_memo.docx
1. One page for the board, opening with the total programme baseline to certify: $3,541 per member per month ($2,157 medical, $1,384 pharmacy)
2. Bar chart of each tier's 2026 allowed PMPM against its baseline PMPM, medical and pharmacy in two panels, in dollars per member per month
