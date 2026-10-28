## Tags

**Domain:** Economics & Econometrics (elasticity, welfare and policy impact estimation: a fixed Budget envelope given to the excise duty whose cut removes the most excess burden in the Budget year).
**Analytical objective:** Opportunity Sizing & Decision Support.

## 1. Final Recommendation

**Give the 2027 Budget's GBP 1.5 million envelope to spirits duty, cutting its 2027 rate of GBP 10.82 a litre by about a fifth from 1 January 2027, which removes about GBP 0.9 million of excess burden in 2027; the next best, cider, would remove about GBP 0.4 million.**
Not road fuel, whose duty and GST are the largest share of its price but whose drivers make under a third of their response to a price cut within 2027. Not cider, the most price-responsive duty, whose small wedge leaves little gain on the extra litres a cut buys. Not beer or wine, each about a quarter of the spirits figure.

## 2. Critical Components

1. Excess burden removed in 2027 by the envelope: **spirits about GBP 0.9 million**, cider about GBP 0.4 million
2. The gain is counted on every extra litre at the whole of the duty and GST still charged on it, not only on the cut itself
3. Buyers' response is the part made within 2027 from a demand model with lagged adjustment: spirits nearly all of their long-run response by the fourth quarter, road fuel under a third

## 3. Step-by-Step Solution

1. Stacked excise_clearances_prices_quarterly_2008-2011.xlsx (2008 to 2011, one sheet per duty) and excise_clearances_prices_quarterly_2012-2026.csv (2012 to 2026 Q3, preliminary quarters included) into one quarterly series per duty, 75 quarters at constant 2026 prices.
2. For each duty fitted least squares of log clearances on four quarter dummies, log shelf price and the previous quarter's log clearances; the response to a price change from 1 January 2027 by quarter k is the first-quarter coefficient times (1 - adjustment^k) / (1 - adjustment).
3. Baseline (manual, section 5): the four quarters 2025 Q4 to 2026 Q3, each standing for its quarter of 2027; producer price = the 2026 Q3 shelf price net of 5 per cent GST less the duty then in force; the 2027 rate from excise_duty_rates_2008-2027.xlsx.
4. For each duty solved for the cut at which duty and GST received in 2027, on the litres bought each quarter after the response, fall by GBP 1.5 million (spirits by about a fifth of its rate).
5. Excess burden removed: each quarter, the area between the fitted constant-elasticity demand curve and the producer price over the extra litres, summed over 2027: spirits 0.9, cider 0.4 GBP million.
6. Excise on releases (customs_excise_declarations_2025-07_2026-09.csv, CE14): exact duplicate rows dropped; procedure 4071 not cancelled; a declaration that a later one names as its related declaration is replaced by it, so each release counts once, as the last declaration of its chain, in the quarter the chain's first declaration was accepted (Eskerholm date, UTC to UK time).
7. Each item priced at quantity times the rate in force on that first day (duty_gbp repeats the declaration's total on every item row); less 6171 repayments (duty_gbp) in the quarter accepted; plus 7171 removals to premises with no approval in force that day (EKW171 from 14 November 2025, EKW157 from 9 October 2025) at that day's rate; GBP thousand to one decimal.

## 4. Deliverable Answers

### budget_2027_duty_cut_paper.docx

1. The duty: spirits, its 2027 rate of GBP 10.82 a litre cut by about a fifth, removing about GBP 0.9 million of excess burden in 2027.
2. The next best: cider, about GBP 0.4 million.
3. A bar chart of the excess burden each duty's cut would remove in 2027, spirits marked.

### budget_2027_duty_envelope.xlsx

1. Excise accounted for on releases from bonded warehouses, GBP thousand:
   - Beer, October to December 2025: 916.8
   - Beer, January to March 2026: 720.9
   - Beer, April to June 2026: 866.5
   - Beer, July to September 2026: 1,006.6
   - Cider, October to December 2025: 469.9
   - Cider, January to March 2026: 424.1
   - Cider, April to June 2026: 560.0
   - Cider, July to September 2026: 650.8
   - Wine, October to December 2025: 1,460.1
   - Wine, January to March 2026: 1,189.0
   - Wine, April to June 2026: 1,247.3
   - Wine, July to September 2026: 1,270.6
   - Spirits, October to December 2025: 1,829.9
   - Spirits, January to March 2026: 1,311.4
   - Spirits, April to June 2026: 1,476.7
   - Spirits, July to September 2026: 1,515.2
   - Road fuel, October to December 2025: 9,395.0
   - Road fuel, January to March 2026: 10,062.6
   - Road fuel, April to June 2026: 10,492.8
   - Road fuel, July to September 2026: 10,775.3
