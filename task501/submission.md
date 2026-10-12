## Tags

**Domain:** Quantitative Finance (liquidity, funding and balance-sheet risk: a pension foundation's standby facility for the capital calls of its private-markets programme).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Elect a standby facility of CHF 225 million for 2027.**
Expected capital calls of CHF 326.6 million in 2027, plus one tenth and less the CHF 150 million reserve, leave CHF 209.2 million for the facility to cover, CHF 9.2 million more than CHF 200 million. Not CHF 125 million, where the programme's age-band call rates on unfunded commitment land (CHF 235.6 million of calls): they give Loschwitz Equity III, Juneau Infrastructure Partners II, Rosenthal Buyout Partners II and Tessin Private Credit I the pace of funds their age, CHF 77.2 million, when those four must draw to 92.6 per cent of commitment before their investment periods close between September and December 2027 and call CHF 165.5 million. Not CHF 200 million, which the programme's 2026 calls of CHF 305.0 million carried forward would give: it leaves CHF 9.2 million of the requirement uncovered.

## 2. Critical Components

1. Loschwitz Equity III, Juneau Infrastructure Partners II, Rosenthal Buyout Partners II and Tessin Private Credit I end their investment periods on 20 September, 22 October, 24 November and 18 December 2027 with **57.6, 60.2, 63.3 and 47.8 per cent** of commitment drawn at 31 December 2026 and **CHF 196.8 million** undrawn at the plan-date rates
2. The **27** funds whose investment periods ended by 31 December 2026 had drawn **91.8 to 93.8 per cent** of commitment by the end of them, **92.6 per cent** on average
3. Expected 2027 calls are **CHF 326.6 million**, **CHF 165.5 million** of them from the four funds, and the requirement is **CHF 209.2 million**, above CHF 200 million and within CHF 225 million

## 3. Step-by-Step Solution

1. Took the issued capital-call lines of kapitalabrufe_ausschuettungen_2015-2026.csv (investments, management fees and partnership expenses; cancelled notices out) by value date for the 51 commitments in fondsregister_2026-12-31.xlsx, in francs at the 31 December 2026 reference rates of fx_referenzkurse_tagesende.csv (USD 0.7906, EUR 0.9339), per RL-PM-05 sections 2 and 4.
2. For the 27 funds whose investment_period_end is on or before 31 December 2026, divided the calls value-dated by that day by commitment: 91.8 to 93.8 per cent, 92.6 on average, including Corvisart Equity VI, Brantwood Partners II, Ulmenhof Capital II, Quendel Partners III and Isenring Private Capital II, which were 49.6 to 70.0 per cent drawn a year before.
3. Estimated the programme's monthly call rate on unfunded commitment in 12-month bands of age from each fund's first call, summed calls over summed unfunded commitment across the record; run from the ends of 2024 and 2025 it forecasts the next year's calls within 1.6 and 3.0 per cent.
4. Found the ten funds whose investment periods end in 2027: the four are 47.8 to 63.3 per cent drawn with CHF 196.8 million undrawn, the other six 84.3 to 92.2 per cent.
5. Forecast 2027 month by month: each of the ten calls the balance to 92.6 per cent of commitment by its period end and the band rate on what remains after it, every other fund its band rate on its unfunded commitment, capped at what is undrawn: CHF 326.6 million, CHF 165.5 million from the four (the band rates alone give them CHF 77.2 million and the year CHF 235.6 million).
6. Applied RL-PM-05 section 4: CHF 326.6 million plus one tenth, CHF 359.2 million, less the CHF 150 million reserve is CHF 209.2 million, and the smallest amount on the term sheet's menu that covers it is CHF 225 million.
7. Took the term sheet's 0.30 per cent commitment fee and 0.15 per cent arrangement fee on the amount: CHF 1,012,500 at CHF 225 million and CHF 900,000 at CHF 200 million.
8. Matched each 2026 credit "Gutschrift Ausschuettung" on programmkonto_lindenhof_2025-2026.csv to its notice in the ledger (Transaktionsreferenz for the custodian's advice, the notice number in Referenz for a keyed notice), counted each credit once and valued the notice's cash amount at the reference rate of the credit's value date, by the fund's strategy and the quarter of the credit: Buyout returned the most, CHF 95,970 thousand.

## 4. Deliverable Answers

### facility_election_2027.docx

1. Facility amount for 2027: CHF 225 million
2. Fees for 2027 at CHF 225 million: CHF 1,012,500 (commitment fee CHF 675,000, arrangement fee CHF 337,500)
3. Fees for 2027 at CHF 200 million: CHF 900,000 (commitment fee CHF 600,000, arrangement fee CHF 300,000)
4. Chart of the cash received from distributions in 2026: one stacked bar per quarter with a segment per strategy, the bars labelled CHF 104,639, 59,250, 69,198 and 73,721 thousand, the title naming Buyout as the strategy that returned the most

### distributions_received_2026.xlsx

1. Distributions received in 2026 by strategy, CHF thousand (Q1, Q2, Q3, Q4, year):
   - Buyout: 33,264, 19,030, 19,695, 23,981, 95,970
   - Growth: 15,950, 8,017, 10,193, 15,788, 49,948
   - Private credit: 19,184, 22,454, 19,764, 19,240, 80,642
   - Infrastructure: 36,241, 9,749, 19,546, 14,712, 80,248
