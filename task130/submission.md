# task130 · Red Cedar Valley Schools, the Northcourt care management baseline for 2027-28

## Tags

**Domain:** Actuarial Science & Insurance (claims frequency and severity: a self-insured school district's baseline for its care management vendor's share of savings).
**Analytical objective:** Forecasting & Predictive Modeling (the allowed claims per member month that 140 members chosen on their 2026 claims would incur in a programme year that has not started, by tier, medical and pharmacy).

## 1. Final Recommendation

**Certify a programme baseline of $4,060 per member per month for the 140 enrolled members ($1,438 medical, $2,622 pharmacy), built tier by tier from what the 140 members Northcourt's model flagged on 2024 claims for its 2025 proposal, never enrolled, cost from April 2025 to March 2026, trended 24 months.**

Not the enrolled members' own 2026 claims, medical or pharmacy, carried forward at the renewal trend, which treats the year they were picked for as a year they will repeat. Not the renewal letter's plan-wide projection, which prices the average member rather than the 140 at the top of the plan.

## 2. Critical Components

1. The untreated comparison is the **140** members on Northcourt's RFP 2025-07 list, matched to Ellery member IDs through the conversion crosswalk
2. Their allowed claims per member month are taken over **1 April 2025 to 31 March 2026**, by tier, medical and pharmacy
3. That experience is trended **24 months** at **6.5%** medical and **9.0%** pharmacy
4. The tiers are weighted by the final list's enrolled members, **34, 37, 38 and 31**
5. The programme baseline is **$1,438** medical and **$2,622** pharmacy, **$4,060** in total

## 3. Step-by-Step Solution

1. Netted the Ellery claim lines as the warehouse readme describes (a frequency 7 claim drops the claim it replaces, a void reverses its amounts, a denied line, exact duplicates included, has no allowed amount) and the Quarrystone B2 reversals against their fills, linking pharmacy to members on the employee number and person code in effect on the fill date.
2. Counted member months from the eligibility spans, each member for the months enrolled, and dated each claim by first date of service or fill date, keeping a claim incurred in a month that is not a member month (a newborn's month of birth), all as Schedule C.1 defines them.
3. Took the 140 members and tiers on the final stratification list of 5 March 2027 (the January draft is superseded) and computed their 2026 allowed PMPM paid through 28 February 2027, without completion per Schedule C.2: tier 1 runs at $9,613 medical and $2,696 pharmacy.
4. Matched all 140 Bramwell member numbers on the District's copy of the RFP 2025-07 list to Ellery member IDs through the conversion crosswalk, each in the tier that list gives it per Schedule C.1(e), members also on the final list included; the District cancelled RFP 2025-07 before an award, so none of them was ever in the programme.
5. Divided each bid tier's allowed claims from 1 April 2025 to 31 March 2026, the programme year the list was drawn for, by its member months and trended them 24 months, midpoint to midpoint, per Schedule C.1(h) at the renewal letter's 6.5% and 9.0%: tier 1's baseline is $3,017 medical and $3,231 pharmacy.
6. Weighted the four tier baselines by enrolled members per Schedule C.1(i): $1,438 medical and $2,622 pharmacy, $4,060 in total.
7. Recommendation: certify a programme baseline of $4,060 per member per month.

## 4. Deliverable Answers

### cohort_baseline_2027.xlsx
1. One row per tier, whole dollars per member per month:
   - Tier 1: 34 enrolled members, 2026 allowed PMPM $9,613 medical and $2,696 pharmacy, baseline PMPM $3,017 medical and $3,231 pharmacy
   - Tier 2: 37 enrolled members, 2026 allowed PMPM $4,335 medical and $3,242 pharmacy, baseline PMPM $1,247 medical and $2,335 pharmacy
   - Tier 3: 38 enrolled members, 2026 allowed PMPM $3,495 medical and $2,551 pharmacy, baseline PMPM $656 medical and $2,771 pharmacy
   - Tier 4: 31 enrolled members, 2026 allowed PMPM $1,919 medical and $4,556 pharmacy, baseline PMPM $893 medical and $2,113 pharmacy
2. Programme baseline across all 140 members, whole dollars per member per month: $1,438 medical, $2,622 pharmacy, $4,060 in total

### baseline_certification_memo.docx
1. One page for the board, opening with the total programme baseline to certify: $4,060 per member per month ($1,438 medical, $2,622 pharmacy)
2. Bar chart of each tier's 2026 allowed PMPM against its baseline PMPM, medical and pharmacy in two panels, in dollars per member per month
