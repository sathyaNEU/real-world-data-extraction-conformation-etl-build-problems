# task134: Strathallan, council-funded care home residents for the 2027-28 budget

## Tags

**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting: council-funded long-stay care home places).
**Analytical objective:** Forecasting & Predictive Modeling (council-funded residents at the four quarter ends of 2027-28).
**Reasoning phases:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.

## 1. Final Recommendation

**Budget for 760, 770, 780 and 790 council-funded long-stay care home residents on 30 June, 30 September and 31 December 2027 and 31 March 2028.**

The caseload rises from 745 because 505 of the 599 self-funders were admitted from 1 January 2025 and are now reaching the months after admission in which savings run down to the upper capital limit: 131 residents converted from self-funding after 31 December 2026 are still in place on 31 March 2028. Not conversions at their 2024 to 2026 run rate, which came from smaller self-funding pools weighted to long stays and keep the caseload flat. Not a pooled conversion rate per self-funder month applied to today's pool, which gives residents in their first year the rate of residents in their peak years. Not one less the survival curve of time to conversion with exits censored, which counts conversions for self-funders who die first.

## 2. Critical Components

1. Council-funded long-stay residents on 31 December 2026: **745**
2. Self-funding residents with an open free personal care award on 31 December 2026: **599**
3. Residents converted from self-funding after 31 December 2026 and still in place on 31 March 2028: **131**

## 3. Step-by-Step Solution

1. Stitched the PERM episodes of `care_home_placements_2021-2026.csv` into stays per person, resolving old and merged client numbers through `client_id_crosswalk_2023.csv`, closed open stays at the date of death in `nrs_death_linkage_2027-01-15.tsv`, and counted the council-funded residents in place at the end of 31 December 2026 under sections 1 and 2 of `care_home_budget_definitions_2027-28.docx`: 745.
2. Took one award per debtor reference from `fpnc_payment_lines_2021-2026.csv` (end reason CF a move to council funding from the day after `award_end`, DIED or LEFT an exit, an open award closed at a death linked through the crosswalk): 599 self-funders on 31 December 2026, 505 of them admitted from 1 January 2025.
3. Estimated the exit hazard of council-funded stays by month since admission (one-month bands, each stay at risk from the later of 1 April 2021 and its funding start to the earlier of its exit and 31 December 2026) and carried each current resident forward on it: 474 still in place on 31 March 2028.
4. Added council-funded direct admissions at their 2024 to 2026 rate, 15.94 a month, each surviving on the same hazard from admission: 184 in place on 31 March 2028.
5. Estimated the self-funders' conversion and exit hazards by month since admission the same way from the awards, applied both to each of the 599 from their months since admission at 31 December 2026, exit competing with conversion, and carried each conversion forward on the council-funded exit hazard: 131 in place on 31 March 2028.
6. Summed the three parts at each quarter end: 759.1, 770.5, 780.1 and 789.0 council-funded residents.
7. For the council-funded residents in place on 31 December 2026, placed each home in its locality by its postcode in `care_home_register_2026-12.xlsx` through `postcode_locality_lookup.csv`, took the contribution in force on 31 December 2026 in `charging_assessments_2021-2026.csv` over every debtor reference the person holds and the episode's contracted weekly fee (definitions section 3), and averaged both by locality and care type: Kirkhallam's nursing places cost the partnership most, £837 a week.
8. Recommendation: budget for 760, 770, 780 and 790 council-funded residents.

## 4. Deliverable Answers

### care_home_funding_forecast_2027-28.xlsx

1. Council-funded long-stay residents, nearest 10:
   - 30 June 2027: 760
   - 30 September 2027: 770
   - 31 December 2027: 780
   - 31 March 2028: 790
2. Council-funded residents in each locality's care homes on 31 December 2026, average weekly contribution and average weekly cost to the partnership after contributions, pounds to the nearest pound:
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
