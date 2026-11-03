## Tags

**Domain:** Marketing & Consumer Research, customer satisfaction driver analysis (a GB domestic energy supplier's six-month new-customer satisfaction tracker).  
**Analytical objective:** Root-Cause Analysis (what pulled six-month satisfaction down between the first halves of 2025 and 2026, and whether any of the fall belongs to the new billing platform before phase 2 cuts over).

## 1. Final Recommendation

**The fall in six-month satisfaction from 76.2 to 67.1 per cent belongs to the quote journey relaunched in May 2025, which stopped pre-filling each meter point's industry annual quantity, not to the billing platform, so phase 2 can cut over on 1 February 2027.**

More than half of the 9.1-point fall sits with customers whose meter points' annual quantities cost more than their quote, while customers whose quote covered that cost held their H1 2025 level on the new platform. Not the billing platform, which the billing ratings point at only because those bills ran above the quote. Not the October 2025 tariff rise or the November 2025 contact centre move, each a point or two at most. Not the survey vendor change, across which the covered customers held their level.

## 2. Critical Components

1. Share satisfied (4 or 5 on the overall question, first answered response per account): **76.2 per cent** in H1 2025 and **67.1 per cent** in H1 2026, a fall of **9.1 points**.
2. The quote journey's quotes, costed against the annual quantities each customer's meter points then carried, carry **more than half** of the fall.
3. Customers whose quote covered that cost were as satisfied in H1 2026 on the new platform as in H1 2025 on the legacy one.

## 3. Step-by-Step Solution

1. Read six_month_survey_2025H1.csv and survey_export_6m_2026-01-01_2026-06-30.csv per the measurement framework (labels by its scale table, 2026 times in UK time, the first answered response per account): 76.2 and 67.1 per cent satisfied, a fall of 9.1 points.
2. Linked each respondent to the accepted quote its registration names in supply_registrations_2024-07_2025-12.csv (2026 platform numbers back to legacy numbers through phase1_migration_loads.jsonl) and costed, at that quote's rates in tariff_rates_2024-04_2026-06.xlsx, the annual quantities in force on the response date in meter_point_annual_quantities.parquet.
3. Fitted satisfaction on the metered cost against the quote (kinked at zero) with the tariff rise, the contact centre and the 2026 term, and split the fall over the four causes in every order: the quote's part is more than half, and customers whose quote covered the cost held their level.
4. Phase 2 scope: replayed switching_flows_2026-05_2026-10.csv to 1 November 2026 (a meter point returned after an erroneous transfer is ours), gave each meter point to the account in legacy_accounts_extract_2026-10-31.csv that took it on last (a leaving occupier's account waiting for its final bill no longer counts), and summed each meter point's registers on its latest revision on or before that day: the regional counts, 101.4 GWh of electricity and 230.6 GWh of gas.
5. Phase 1 moves: walked each load in phase1_migration_loads.jsonl back through the platform number it was sourced from, took each account's last load in UK time with that load's fuels, and left out accounts still on the legacy extract (loaded and returned, never moved): the weekly counts below.
6. Switches: one per accepted quote in the registrations with withdrawn registrations out, in the month its first supply started, credited to the channel of the prospect's quote in quote_log_2024-06_2025-12.csv dated on or before the registration (a later phone re-quote does not move it): the monthly counts below.
7. The platform is not the cause of the fall; phase 2 can cut over on 1 February 2027 and the fix is the quote journey.

## 4. Deliverable Answers

### six_month_satisfaction_review.pdf

1. The fall belongs to the quote journey's quotes since the May 2025 relaunch, not to the billing platform; phase 2 can cut over.
2. Share satisfied 76.2 per cent in H1 2025 and 67.1 per cent in H1 2026, a fall of 9.1 points, more than half of it the quote journey's.
3. Bridge chart on page 1 from 76.2 to 67.1 per cent, the quote journey's quotes the largest step.

### phase2_readiness.xlsx

1. Accounts phase 2 will move, by region, whole numbers:
   - East Midlands: 2,520
   - Eastern: 3,213
   - London: 2,923
   - North East: 1,560
   - North Scotland: 906
   - North Wales and Mersey: 1,646
   - North West: 2,881
   - South East: 2,555
   - South Scotland: 2,007
   - South Wales: 1,200
   - South West: 2,000
   - Southern: 3,287
   - West Midlands: 2,551
   - Yorkshire: 2,931
2. Annual quantity of the meter points phase 2 will move, GWh to one decimal: electricity 101.4, gas 230.6.
3. Accounts phase 1 moved each week, whole numbers:
   - Week commencing 1 September 2025: electricity-only 1,757, dual fuel 4,478
   - Week commencing 8 September 2025: electricity-only 2,897, dual fuel 7,401
   - Week commencing 15 September 2025: electricity-only 3,827, dual fuel 9,848
   - Week commencing 22 September 2025: electricity-only 4,309, dual fuel 10,874
   - Week commencing 29 September 2025: electricity-only 4,018, dual fuel 10,481
   - Week commencing 6 October 2025: electricity-only 4,213, dual fuel 11,155
   - Week commencing 13 October 2025: electricity-only 3,885, dual fuel 10,412
   - Week commencing 20 October 2025: electricity-only 3,914, dual fuel 10,341
   - Week commencing 27 October 2025: electricity-only 3,643, dual fuel 9,665
4. Switches each sales channel brought in, by the month first supply started, whole numbers:
   - July 2025: Direct web 1,800, Comparison site 1,712, Phone 600, Broker 729
   - August 2025: Direct web 1,749, Comparison site 1,715, Phone 598, Broker 707
   - September 2025: Direct web 1,751, Comparison site 1,664, Phone 548, Broker 689
   - October 2025: Direct web 1,743, Comparison site 1,721, Phone 590, Broker 689
   - November 2025: Direct web 1,606, Comparison site 1,701, Phone 595, Broker 692
   - December 2025: Direct web 1,806, Comparison site 1,710, Phone 545, Broker 660
