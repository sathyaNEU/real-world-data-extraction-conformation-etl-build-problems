# task117 · Contracted demand for the Civic Center decks' new service

## Tags

**Domain:** Supply Chain & Logistics (sourcing and procurement: the contracted demand a city commits to a single utility for the dedicated service feeding its two permit-only charging decks, under a twelve-month demand ratchet).
**Analytical objective:** Forecasting & Predictive Modeling (each month's billing demand over the first contract year on the replacement charging units, replayed from settled sessions with the cars the permits carry into that year).

## 1. Final Recommendation

**File 130 kW as the contracted demand for the first contract year, April 2027 to March 2028.**

December 2027 sets it at 129.1 kW of forecast billing demand, ahead of January 2028 at 109 kW. Not the 225 kW North Sound's planners will propose, which sizes nameplate times a diversity factor rather than the decks' load. Not the 2026 meter peaks scaled up by the new units' rating, because a faster unit shortens a session instead of multiplying its load and the panel registers count morning hours the tariff does not bill. Not a replay of every session at the full 11.5 kW, which assumes every car can take it. Not a replay of each 2026 session with the car that made it, because 18 county permits were renewed in January onto cars that charge at 11.0 kW.

## 2. Critical Components

1. On the new units each 2026 deck session draws the lower of **11.5 kW** and its car's onboard charger rating until its delivered energy
2. The car is the one the permit carries in the contract year: **18** county permits moved from 7.2 kW to 11.0 kW Bolt EVs at the January 2027 renewal
3. The replay's highest billing-hours quarter-hour in 2026 is **115.3 kW**, at 12:00 on Tuesday 8 December 2026
4. The growth factor in force for the forecast is **1.12**
5. December 2027's forecast billing demand is **129.1 kW**, the highest contract month

## 3. Step-by-Step Solution

1. Kept the sessions of record in `settled_sessions_2024-2026.csv` (the ACCEPTED version in `restatement_decisions_2025.csv`, one row per `auth_code`) and placed each on its unit by the `station_register.csv` assignment in service that day: the 2026 sessions at the 32 deck units.
2. Took each permit's car from its January 2027 renewal row in `permit_vehicle_checks.csv` and its `onboard_charger_kw` from `vehicle_reference_list.csv` (fleet cards through `city_fleet_roster.csv`): 18 county permits now carry 2023 Bolt EVs at 11.0 kW where 2020 Bolt EVs at 7.2 kW made their 2026 sessions.
3. Replayed each 2026 deck session from `plug_in` at the lower of 11.5 kW (Exhibit A of `civic_center_ev_service_agreement_draft.docx`) and that car's rating until `kwh_delivered`, summing both decks per quarter-hour behind the one meter.
4. Took each 2026 month's highest quarter-hour beginning 12:00 to 19:45 on the billing days of `nspl_schedule_26_ev_charging_service.pdf`: 115.3 kW at 12:00 on 8 December 2026 is the year's highest.
5. Grew each month by the 1.12 factor in Table 1 of `fes-07_load_forecasting_standard_rev4.pdf`: December 2027 is 129.1 kW, which files 130 kW in Schedule 26's 5 kW steps whether rounded to the nearest step or up.
6. Back-tested FES-07 on 2025 from the 2024 deck billing demand, including `gateway_b_sessions_jan-apr2024.csv` and the fleet card charges in `fleet_card_ev_transactions_2024-2026.csv` the export does not carry, times the 1.08 factor in force when that forecast was made, in whole kW against 2025's recorded whole kW per FES-07 section 4: errors run from -1.8% to +2.6%, six over and six under.
7. Set each 2026 read span in `deck_panel_meter_log_2024-2026.xlsx` on the meters' standard-time clock (`deck_submeter_nameplates.csv`), the later 31 December South read standing, against the session energy on the units `deck_panel_circuit_schedule.csv` places on each panel, the quarter-hour a read falls inside split at the read on the sessions' constant 6.6 kW draw: 517 to 1,130 kWh unaccounted per read.
8. Recommendation: file 130 kW as the contracted demand for April 2027 to March 2028.

## 4. Deliverable Answers

### contract_demand_note.pdf

1. Contracted demand for the first contract year: 130 kW
2. Forecast billing demand by contract month, whole kW:
   - April 2027: 90 kW
   - May 2027: 85 kW
   - June 2027: 79 kW
   - July 2027: 72 kW
   - August 2027: 75 kW
   - September 2027: 87 kW
   - October 2027: 94 kW
   - November 2027: 103 kW
   - December 2027: 129 kW
   - January 2028: 109 kW
   - February 2028: 68 kW
   - March 2028: 98 kW
3. The month that sets the figure: December 2027
4. In the quarter-hour that sets it: North Deck 83 kW, South Deck 46 kW
5. North Sound's planners' figure: 225 kW, 95 kW above ours

### deck_load_day.png

1. Tuesday 8 December 2026, the basis day for December 2027, both decks combined by quarter-hour
2. Two series: what the decks drew on the 6.6 kW units that day, and the forecast on the 11.5 kW units for December 2027
3. The contracted figure as a line labelled 130 kW
4. The 12:00 quarter-hour marked at 129 kW
5. Title: "File 130 kW: the decks' busiest billed quarter-hour on the new units comes to 129 kW at noon"

### civic_service_demand.xlsx

1. 2025 forecast from 2024 under FES-07, and its error as a percentage of the actual:
   - January 2025: 112 kW, -0.9%
   - February 2025: 117 kW, +2.6%
   - March 2025: 107 kW, -1.8%
   - April 2025: 106 kW, +1.9%
   - May 2025: 88 kW, -1.1%
   - June 2025: 88 kW, +2.3%
   - July 2025: 82 kW, -1.2%
   - August 2025: 90 kW, +2.3%
   - September 2025: 106 kW, -0.9%
   - October 2025: 114 kW, +1.8%
   - November 2025: 113 kW, +0.9%
   - December 2025: 111 kW, -0.9%
2. Metered kWh the sessions do not account for, per 2026 reading:
   - North Deck panel CP-N, read 1 (January 30): 1,069 kWh
   - North Deck panel CP-N, read 2 (February 27): 908 kWh
   - North Deck panel CP-N, read 3 (March 31): 910 kWh
   - North Deck panel CP-N, read 4 (April 30): 725 kWh
   - North Deck panel CP-N, read 5 (May 29): 594 kWh
   - North Deck panel CP-N, read 6 (June 30): 592 kWh
   - North Deck panel CP-N, read 7 (July 31): 599 kWh
   - North Deck panel CP-N, read 8 (August 31): 691 kWh
   - North Deck panel CP-N, read 9 (September 30): 791 kWh
   - North Deck panel CP-N, read 10 (October 30): 914 kWh
   - North Deck panel CP-N, read 11 (November 30): 1,065 kWh
   - North Deck panel CP-N, read 12 (December 31): 1,130 kWh
   - South Deck panel CP-S, read 1 (January 30): 934 kWh
   - South Deck panel CP-S, read 2 (February 27): 798 kWh
   - South Deck panel CP-S, read 3 (March 31): 794 kWh
   - South Deck panel CP-S, read 4 (April 30): 633 kWh
   - South Deck panel CP-S, read 5 (May 29): 520 kWh
   - South Deck panel CP-S, read 6 (June 30): 517 kWh
   - South Deck panel CP-S, read 7 (July 31): 523 kWh
   - South Deck panel CP-S, read 8 (August 31): 606 kWh
   - South Deck panel CP-S, read 9 (September 30): 693 kWh
   - South Deck panel CP-S, read 10 (October 30): 799 kWh
   - South Deck panel CP-S, read 11 (November 30): 932 kWh
   - South Deck panel CP-S, read 12 (December 31): 990 kWh
