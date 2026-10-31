## Tags

**Domain:** Actuarial Science & Insurance (reinsurance and capital: a county farm-and-home mutual's 2027 windstorm reinsurance, a cover bought when the capital it releases is worth more than it costs).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**We should add Penwarden's second-event cover to the 2027 windstorm programme.**
It releases £7 million of 1-in-200 windstorm capital, worth £0.8 million a year at 12 per cent against a margin of £0.7 million, so it adds £0.1 million a year. Not on one incurred-over-hindcast ratio for every storm of record, which undercosts the storms that strike within weeks of the one before and leaves the cover looking dearer than its release is worth. Not on each storm's place in its year or season, which the record's later storms on quiet seasons, costing what the model says, rule out.

## 2. Critical Components

1. Storms of record that struck within six weeks of the storm before cost **1.62** times their hindcast, every other storm **0.98** times.
2. The 1-in-200 annual windstorm loss is **£113 million** gross, **£94 million** net of the occurrence cover and **£87 million** net of both covers.
3. The second-event cover's margin is **£0.7 million** a year: its premium of **£1.3 million** and expected reinstatement premium of **£0.1 million**, less expected recoveries of **£0.7 million**.

## 3. Step-by-Step Solution

1. Linked each storm in windstorm_experience_2001-2025.xlsx to the storm in seaborne_windstorm_hindcast_2001-2025.csv whose peak falls on its first damage date or the day after, all 43 storms of record, and classed each by the days since the storm before it (every gap is 24 days or less, or 70 or more): the 9 within six weeks cost 1.62 times their hindcast and the rest 0.98, incurred over hindcast for the storms like it per CP-04 section 2.
2. Classed each storm of seaborne_windstorm_ylt_2027_portfolio.csv the same way against the storm before it in its simulated year and costed it at its class's ratio.
3. Netted each simulated year of the occurrence cover (quotation A, 18,000,000 xs 12,000,000 each loss occurrence, one reinstatement at 100 per cent pro rata as to amount), each storm one loss occurrence per CP-04: the 1-in-200, the average of the 50 worst of the 10,000 years, is £113 million gross and £94 million net.
4. Added the second-event cover (quotation B, 7,500,000 xs 4,000,000 of the loss retained under the occurrence cover on each year's second and later loss occurrences, one reinstatement): the 1-in-200 falls to £87 million, a release of £7 million.
5. Took the cover's margin per CP-04 section 3 over the 10,000 years: £0.7 million.
6. Dated each 2026 storm claim line in claims_extract_2026-10-31.csv by date_of_damage in loss_adjuster_instructions_2026.csv (insurer_ref without its spaces), a reopened claim's lines in notification order against its instructions in instruction order, and grouped the days into the 72-hour loss occurrences that maximise the expiring cover's recovery (wording clause 3): it recovers £12,015,000 and calls £1,402,000 of reinstatement premium.
7. Summed the Holdings sheet of farm_policies_and_locations_2026-10-31.xlsx by each holding's county, each coinsured policy at its share in coinsurance_register_2026.csv, matched on its main holding's CPH or, for a renumbered holding, its previous_cph, and applied to every holding on the policy.
8. Valued the cover at 12 per cent of the release, £0.8 million, less the margin: it adds £0.1 million a year, so it is added to the programme.

## 4. Deliverable Answers

### windstorm_programme_board_paper_2027.pdf

1. Recommendation: add the second-event cover to the 2027 programme.
2. Bar chart on page 1 of the 1-in-200 annual windstorm loss: £113 million gross, £94 million net of the occurrence cover, £87 million net of both covers.
3. Capital the second-event cover releases: £7 million.
4. The cover's margin £0.7 million; its worth to us a year £0.1 million.
5. 2026 loss occurrences of £1 million or more, home and farm policies:
   - 11 to 13 January: home £13,067,000, farm £2,510,000
   - 8 to 9 February: home £16,898,000, farm £3,541,000
   - 15 to 16 February: home £3,943,000, farm £931,000
6. The expiring cover recovers £12,015,000 on 2026 and calls a reinstatement premium of £1,402,000.
7. Our share of the farm sums insured, buildings and farm contents:
   - Cornwall: buildings £1,302.1 million, farm contents £618.2 million
   - Devon: buildings £1,502.4 million, farm contents £746.3 million
   - Somerset: buildings £863.7 million, farm contents £396.8 million
   - Dorset: buildings £389.0 million, farm contents £184.3 million

### windstorm_programme_2027.xlsx

1. The same figures: sheet Capital 2027 carries the call, the three 1-in-200 losses, the release, the margin and the worth; Storms 2026 each occurrence's home and farm cost, the recovery and the reinstatement premium; Farm sums insured each county's buildings and farm contents; Record the storms of record with their ratios.
