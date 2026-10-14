# task134: Strathallan, council-funded care home residents for the 2027-28 budget

## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting: council-funded long-stay care home places).
**Analytical objective:** Forecasting & Predictive Modeling (council-funded residents at the four quarter ends of 2027-28).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Budget for 790, 800, 810 and 810 council-funded long-stay care home residents on 30 June, 30 September and 31 December 2027 and 31 March 2028.**

The upper capital limit rises by £7,000 on 5 April 2027, which brings every self-funder's capital to the limit 6.73 weeks sooner: the £5,000 rise of 6 April 2026 brought 8 conversions in one day against 1.62 in an ordinary week, 4.81 weeks of conversions, and 145 residents converted from self-funding after 31 December 2026 are still in place on 31 March 2028. Not the conversion hazard by months since admission projected as fitted (770, 780, 790 and 790), which has no 2027 rise in it. Not the 6 April 2026 conversions added again on 5 April 2027, as they stand or scaled by the rises, which leaves the rest of the pool's clocks where they were and ignores how many of today's 581 self-funders are near the limit. Not conversions at their run rate or a pooled rate per self-funder, which come from smaller pools weighted to long stays.

## 2. Critical Components

1. Council-funded long-stay residents on 31 December 2026: **757**
2. Self-funding residents with an open free personal care award on 31 December 2026: **581**
3. The 6 April 2026 rise in the upper capital limit: **8** conversions that day against **1.62** in an ordinary week, **4.81** weeks of conversions; the 5 April 2027 rise: **6.73** weeks
4. Residents converted from self-funding after 31 December 2026 and still in place on 31 March 2028: **145**

## 3. Step-by-Step Solution

1. Stitched the PERM episodes of `care_home_placements_2021-2026.csv` into stays per person, resolving old and merged client numbers through `client_id_crosswalk_2023.csv`, closed open stays at the date of death in `nrs_death_linkage_2027-01-15.tsv`, and counted the council-funded residents in place at the end of 31 December 2026 under sections 1 and 2 of `care_home_budget_definitions_2027-28.docx`: 757.
2. Took one award per debtor reference from `fpnc_payment_lines_2021-2026.csv` (end reason CF a move to council funding from the day after `award_end`, DIED or LEFT an exit, an open award closed at a death linked through the crosswalk): 581 self-funders on 31 December 2026.
3. Estimated the exit hazard of council-funded stays and the self-funders' conversion and exit hazards by month since admission (one-month bands, each record at risk from the later of 1 April 2021 and its start to the earlier of its end and 31 December 2026), carried each current resident forward on the exit hazard (483 still in place on 31 March 2028) and added direct admissions at their 2024 to 2026 rate, 15.94 a month, each surviving from admission (184 in place on 31 March 2028).
4. Read the upper capital limit's rises in `charging_policy_2026-27.pdf` (£28,750 to £33,750 on 6 April 2026, £40,750 from 5 April 2027) and counted the conversions taking effect on 6 April 2026, 8, against the 84 of the 52 weeks before it, 1.62 a week: the 2026 rise was worth 4.81 weeks of conversions, so the 2027 rise, 7,000 against 5,000, is 6.73 weeks.
5. Projected each of the 581 self-funders from their months since admission at 31 December 2026, conversion and exit competing, the 375 of them in the pool on 6 April 2026 4.81 weeks further on, and on 5 April 2027 moved every self-funder's clock on 6.73 weeks, those the jump carries past the limit converting that day; each conversion survives on the council-funded exit hazard: 145 in place on 31 March 2028.
6. Summed the three parts at each quarter end: 791.5, 801.0, 808.3 and 812.3 council-funded residents.
7. For the council-funded residents in place on 31 December 2026, placed each home in its locality by its postcode in `care_home_register_2026-12.xlsx` through `postcode_locality_lookup.csv`, priced each place at the fee payable under its contract (definitions section 3: the 2026-27 rate agreed on 6 November 2026 in `nchc_rates_2021-22_to_2026-27.xlsx` plus the supplement, which is the episode's fee less the interim rate it still carries), took the contribution in force on 31 December 2026 in `charging_assessments_2021-2026.csv` over every debtor reference the person holds, and averaged both by locality and care type.
8. Recommendation: budget for 790, 800, 810 and 810 council-funded residents.

## 4. Deliverable Answers

### care_home_funding_forecast_2027-28.xlsx

1. Council-funded long-stay residents, nearest 10:
   - 30 June 2027: 790
   - 30 September 2027: 800
   - 31 December 2027: 810
   - 31 March 2028: 810
2. Council-funded residents in each locality's care homes on 31 December 2026, average weekly fee and average weekly cost to the partnership after contributions, pounds to the nearest pound:
   - Allanvale, residential: fee £954, cost to the partnership £674
   - Allanvale, nursing: fee £1,079, cost to the partnership £819
   - Braeburn, residential: fee £959, cost to the partnership £717
   - Braeburn, nursing: fee £1,080, cost to the partnership £821
   - Carsefield, residential: fee £951, cost to the partnership £702
   - Carsefield, nursing: fee £1,074, cost to the partnership £821
   - Dunmorrow, residential: fee £954, cost to the partnership £682
   - Dunmorrow, nursing: fee £1,083, cost to the partnership £829
   - Kirkhallam, residential: fee £955, cost to the partnership £700
   - Kirkhallam, nursing: fee £1,091, cost to the partnership £846

### care_home_costs_by_locality.png

1. Residential and nursing bars side by side for each locality: Allanvale, Braeburn, Carsefield, Dunmorrow, Kirkhallam.
2. Each bar labelled with its value: Allanvale residential £674, nursing £819; Braeburn residential £717, nursing £821; Carsefield residential £702, nursing £821; Dunmorrow residential £682, nursing £829; Kirkhallam residential £700, nursing £846.
