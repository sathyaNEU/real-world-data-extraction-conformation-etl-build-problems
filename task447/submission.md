# task447 submission

## Tags

**Domain:** Healthcare Delivery & Health Economics, payment, claims and health-plan analytics (the spending effect of a hospital system buying a physician group, projected from all-payer claims).
**Analytical objective:** Data Extraction & Conformation (ETL) (two claims layouts, eligibility spans, an ownership register, NPI reassignment spans, a rate exhibit and carrier tier filings conformed into the projection rule OHCCR 4 defines).

## 1. Final Recommendation

**Proceed to a cost and market impact review of notice N25-014: Ledgestone Health's purchase of Brightwater Medical Group raises commercial spending by $2.2 million in 2026, above the $2.0 million threshold in rule OHCCR 4.06.**

The deciding figure is the $2.2 million projected increase against the $2.0 million threshold. Not a share of referrals measured on Ledgestone's own purchases, pooled, by carrier or product by product, which carries Bayfield's 2021 to 2024 second-tier placement of Ledgestone into 2026, although Wolf River's acquired practices show the share following the tier when Norbridge placed Wolf River first in 2024. Not Ledgestone Medical Group's or Mishicot Family Practice's own referral share, neither of which has the before and after that rule 4.05 requires.

## 2. Critical Components

1. Brightwater's professional services at Ledgestone Medical Group's Exhibit C schedules add **$610,000**.
2. After the 2021 to 2023 acquisitions, **86%** of the outside referrals of patients whose plan placed the acquiring system in its first tier, or had no tiers, moved to that system, and **none** of second-tier patients' referrals.
3. Bayfield's Value Tier PPO places Ledgestone in its **first** tier from plan year 2025.
4. Brightwater's referred services add **$1,600,000** in 2026.
5. The projected 2026 increase is **$2.2 million**.

## 3. Step-by-Step Solution

1. Conformed the 2021 to 2023 extract (layout 2.4) to layout 3.1 and kept each claim's latest version net of voids, as the data dictionary sets out.
2. Took Brightwater's 2024 baseline under OHCCR 4.03: professional lines billed under the number the notice gives, and outpatient facility lines whose referring physician billed under that number on the date of service, paid by 30 June 2025.
3. Repriced the professional lines at Exhibit C's Ledgestone Medical Group schedules: $610,000.
4. Took the physicians who joined Ledgestone and Wolf River by acquisition in 2021 to 2023 (appendix A5; Northpoint's orthopedists moved one at a time) from the register and the NPI reassignment history, and gave each referral its tier for the acquiring system from the member's benefit period and the tier filings.
5. In every acquired practice and product, 86% of the outside referrals of first-tier or untiered patients moved and none of second-tier patients', and Norbridge's Tiered EPO patients at Wolf River moved only once the plan placed Wolf River first in plan year 2024, which pooled, carrier and product shares miss by eight points or more.
6. Applied those shares, in whole per cent as OHCCR 4.05 states them, to Brightwater's referrals for codes Ledgestone bills, by each member's product's 2026 placement, priced at Exhibit C with Bayfield at its percent of the CY2025 Medicare amounts: $1,600,000.
7. Added the two parts: $2.2 million, against the $2.0 million threshold in OHCCR 4.06.
8. Recommendation: proceed to a cost and market impact review.

## 4. Deliverable Answers

### N25-014_preliminary_review.pdf

1. Proceed to a cost and market impact review.
2. The increase in commercial spending the deal will cause in 2026: $2.2 million.
3. The increase split, each to the nearest $10,000:
   - Professional prices: $610,000
   - Referred imaging: $500,000
   - Referred echocardiography: $130,000
   - Referred endoscopy: $670,000
   - Referred arthroscopy: $240,000
   - Referred laboratory: $60,000
4. Chart on the first page: the six parts stacked to the $2.2 million total, with a dashed line at the $2.0 million review threshold.
5. Ledgestone's share of commercial outpatient services for county residents, in 2024 and once Brightwater's referrals move, percent to one decimal:
   - Manitowoc County, imaging: 9.6% in 2024, 40.5% after
   - Manitowoc County, endoscopy: 6.6% in 2024, 46.9% after
   - Manitowoc County, arthroscopy: 8.1% in 2024, 41.2% after
   - Kewaunee County, imaging: 10.0% in 2024, 52.0% after
   - Kewaunee County, endoscopy: 10.5% in 2024, 81.4% after
   - Kewaunee County, arthroscopy: 9.1% in 2024, 73.6% after
6. Ledgestone's physician count on 1 January: 2020, 57; 2021, 68; 2022, 73; 2023, 81; 2024, 90; 2025, 89.
7. Physicians who joined by acquisition: 2020, 10; 2021, 5; 2022, 7; 2023, 8; 2024, 0.
