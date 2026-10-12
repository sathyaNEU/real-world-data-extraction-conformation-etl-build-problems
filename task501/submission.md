## Tags

**Domain:** Quantitative Finance (liquidity, funding and balance-sheet risk: a pension foundation's standby facility for the capital calls of its private-markets programme).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Elect a standby facility of CHF 225 million for 2027.**
Expected capital calls of CHF 329.3 million in 2027, plus one tenth and less the CHF 150 million reserve, leave CHF 212.2 million for the facility to cover, CHF 12.2 million more than CHF 200 million. Not CHF 125 million, where the programme's age-band call rates on unfunded commitment land (CHF 236.1 million of calls): they give Loschwitz Equity III, Juneau Infrastructure Partners II, Rosenthal Buyout Partners II and Tessin Private Credit I the pace of funds their age, CHF 79.7 million, when those four must draw to 92.6 per cent of commitment before their investment periods close between September and December 2027 and call CHF 170.1 million. Not CHF 200 million, which the programme's 2026 calls carried forward would give (CHF 310.0 million at the plan-date rates, the franc commitments at par): it leaves CHF 12.2 million of the requirement uncovered.

## 2. Critical Components

1. Loschwitz Equity III, Juneau Infrastructure Partners II, Rosenthal Buyout Partners II and Tessin Private Credit I end their investment periods on 20 September, 22 October, 24 November and 18 December 2027 with **56.4, 61.2, 61.8 and 45.6 per cent** of commitment drawn at 31 December 2026 and **CHF 201.2 million** undrawn at the plan-date rates
2. The **27** funds whose investment periods ended by 31 December 2026 had drawn **92.2 to 93.3 per cent** of commitment by the end of them, **92.6 per cent** on average
3. Expected 2027 calls are **CHF 329.3 million**, **CHF 170.1 million** of them from the four funds, and the requirement is **CHF 212.2 million**, above CHF 200 million and within CHF 225 million

## 3. Step-by-Step Solution

1. Took the issued capital-call lines of kapitalabrufe_ausschuettungen_2015-2026.csv (investments, management fees and partnership expenses; cancelled notices out) by value date for the 51 commitments in fondsregister_2026-12-31.xlsx, in francs at the 31 December 2026 reference rates of fx_referenzkurse_tagesende.csv (USD 0.7906, EUR 0.9339), per RL-PM-05 sections 2 and 4.
2. For the 27 funds whose investment_period_end is on or before 31 December 2026, divided each fund's calls value-dated by the end of its investment period by its commitment: 92.2 to 93.3 per cent, 92.6 on average, including Corvisart Equity VI, Brantwood Partners II, Ulmenhof Capital II, Quendel Partners III and Isenring Private Capital II, which were 49.6 to 69.6 per cent drawn a year before.
3. Estimated the programme's monthly call rate on unfunded commitment in 12-month bands of age from each fund's first call, summed calls over summed unfunded commitment across the programme's whole record from 2015, the basis RL-PM-05 sets for the plan; run from the ends of 2024 and 2025 it forecasts the next year's calls within 4.6 and 0.9 per cent.
4. Found the ten funds whose investment periods end in 2027: the four are 45.6 to 61.8 per cent drawn with CHF 201.2 million undrawn, the other six 84.5 to 91.9 per cent.
5. Forecast 2027 month by month: each of the ten calls the balance to 92.6 per cent of commitment by its period end and the band rate on what remains after it, every other fund its band rate on its unfunded commitment, capped at what is undrawn: CHF 329.3 million, CHF 170.1 million from the four (the band rates alone give them CHF 79.7 million and the year CHF 236.1 million).
6. Applied RL-PM-05 section 4: CHF 329.3 million plus one tenth, CHF 362.2 million, less the CHF 150 million reserve is CHF 212.2 million, and the smallest amount on the term sheet's menu that covers it is CHF 225 million, within the term sheet's covenants on the programme's net asset value.
7. Took the term sheet's 0.30 per cent commitment fee and 0.15 per cent arrangement fee on the amount: CHF 1,012,500 at CHF 225 million and CHF 900,000 at CHF 200 million.
8. Matched each 2026 credit "Gutschrift Ausschuettung" on programmkonto_lindenhof_2025-2026.csv to its notice in the ledger (Transaktionsreferenz for the custodian's advice, the notice number in Referenz for a keyed notice), counted each credit once and valued the notice's cash amount at the reference rate of the credit's value date, by the fund's strategy and the quarter of the credit: Buyout returned the most, CHF 91,926 thousand.

## 4. Deliverable Answers

### facility_election_2027.docx

1. Facility amount for 2027: CHF 225 million
2. Fees for 2027 at CHF 225 million: CHF 1,012,500 (commitment fee CHF 675,000, arrangement fee CHF 337,500)
3. Fees for 2027 at CHF 200 million: CHF 900,000 (commitment fee CHF 600,000, arrangement fee CHF 300,000)
4. Chart of the cash received from distributions in 2026: one stacked bar per quarter with a segment per strategy, the bars labelled CHF 92,183, 62,803, 70,260 and 86,537 thousand, the title naming Buyout as the strategy that returned the most

### distributions_received_2026.xlsx

1. Distributions received in 2026 by strategy, CHF thousand (Q1, Q2, Q3, Q4, year):
   - Buyout: 34,270, 18,990, 19,757, 18,909, 91,926
   - Growth: 16,007, 8,123, 10,143, 19,696, 53,969
   - Private credit: 19,513, 21,248, 18,973, 18,630, 78,364
   - Infrastructure: 22,393, 14,442, 21,387, 29,302, 87,524
