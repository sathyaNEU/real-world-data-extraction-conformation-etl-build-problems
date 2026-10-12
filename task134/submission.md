# task134: Strathallan, council-funded care home residents for the 2027-28 budget

## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting: council-funded long-stay care home places).
**Analytical objective:** Forecasting & Predictive Modeling (council-funded residents at the four quarter ends of 2027-28).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Budget for 760, 770, 780 and 790 council-funded long-stay care home residents at 30 June, 30 September and 31 December 2027 and 31 March 2028.**

The caseload rises because the self-funders admitted in 2025-26 reach the months in which their capital runs down to the upper limit during 2027-28. Not conversions at their 2024 to 2026 run rate, which gives 740 at 31 March 2028 because the past conversions came from a smaller self-funding pool weighted to long stays. Not a pooled conversion rate per self-funder applied to today's pool, which spreads the conversions over members still in their first year. Not one less the survival curve of time to conversion with deaths censored, which counts conversions for residents who die first.

## 2. Critical Components

1. Council-funded long-stay residents on 31 December 2026: **745**
2. Self-funding residents receiving free personal care on 31 December 2026: **599**
3. Council-funded direct admissions: **15.94 a month** (2024 to 2026)
4. Residents converted from self-funding after 31 December 2026 still in place on 31 March 2028: **130.8**

## 3. Step-by-Step Solution

1. Stitched the permanent episodes in `care_home_placements_2021-2026.csv` into stays per person through `client_id_crosswalk_2023.csv`, closed open stays at the date of death in `nrs_death_linkage_2027-01-15.csv`, and counted the council-funded residents in place at the end of 31 December 2026 as the budget definitions (sections 1 and 2) state: 745.
2. Read each self-funder's award in `fpnc_payment_lines_2021-2026.csv` (end reason CF a conversion from the day after `award_end`, DIED or LEFT an exit, open awards less linked deaths the pool): 599 self-funders on 31 December 2026.
3. Fitted death and discharge hazards by month since admission on the council-funded stays from 1 April 2021, left-truncated, and carried each current resident forward: 474.2 still in place on 31 March 2028.
4. Added direct admissions at the 2024 to 2026 rate of 15.94 a month, each surviving from admission: 183.9 in place on 31 March 2028.
5. Estimated the conversion hazard and the self-funders' exit hazard by month since admission from the payment lines, applied them to each self-funder's own admission date with deaths and discharges competing, and carried each conversion forward on the exit hazard: 130.8 in place on 31 March 2028.
6. Summed the three parts at each quarter end: 759.07, 770.52, 780.08 and 788.96, to the nearest 10 760, 770, 780 and 790.
7. For the residents in place on 31 December 2026, took each home's locality from `care_home_register_2026-12.xlsx` and `postcode_locality_lookup.csv`, the contribution in force on 31 December 2026 in `charging_assessments_2021-2026.csv` across every debtor reference the person holds, and the placement's contracted weekly fee, and averaged by locality and care type.
8. Recommendation: budget for 760, 770, 780 and 790 council-funded residents.

## 4. Deliverable Answers

### care_home_funding_forecast_2027-28.xlsx

1. Council-funded long-stay residents, nearest 10:
   - 30 June 2027: 760
   - 30 September 2027: 770
   - 31 December 2027: 780
   - 31 March 2028: 790
2. Council-funded residents in each locality's care homes on 31 December 2026, average weekly contribution and weekly cost to the partnership after contributions, pounds to the nearest pound:
   - Allanvale, residential: contribution £280, cost to the partnership £673
   - Allanvale, nursing: contribution £259, cost to the partnership £819
   - Braeburn, residential: contribution £246, cost to the partnership £709
   - Braeburn, nursing: contribution £259, cost to the partnership £821
   - Carsefield, residential: contribution £238, cost to the partnership £713
   - Carsefield, nursing: contribution £251, cost to the partnership £822
   - Dunmorrow, residential: contribution £275, cost to the partnership £680
   - Dunmorrow, nursing: contribution £248, cost to the partnership £834
   - Kirkhallam, residential: contribution £252, cost to the partnership £703
   - Kirkhallam, nursing: contribution £254, cost to the partnership £837

### care_home_costs_by_locality.png

1. Residential and nursing bars side by side for each locality, ordered from the dearest nursing place: Kirkhallam, Dunmorrow, Carsefield, Braeburn, Allanvale.
2. Each bar labelled with its value: Kirkhallam residential £703, nursing £837; Dunmorrow residential £680, nursing £834; Carsefield residential £713, nursing £822; Braeburn residential £709, nursing £821; Allanvale residential £673, nursing £819.
3. Title naming Kirkhallam: "Kirkhallam's nursing places cost the partnership most: £837 a week after contributions".
