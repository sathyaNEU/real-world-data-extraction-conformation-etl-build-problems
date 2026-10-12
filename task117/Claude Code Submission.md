# task117 · Contracted demand for the Civic Center decks' new service

## Tags

**Domain:** Supply Chain & Logistics (sourcing and procurement: the contracted demand a city commits to a single utility for the dedicated service feeding its two permit-only charging decks, under a twelve-month demand ratchet).
**Analytical objective:** Forecasting & Predictive Modeling (each month's billing demand over the first contract year on the replacement charging units, replayed from settled sessions with the cars the permits carry into that year).

## 1. Final Recommendation

**File 110 kW as the contracted demand for the first contract year, April 2027 to March 2028.**

January 2028 sets it at 109.1 kW of forecast billing demand, ahead of December 2027 at 97 kW. Not the 225 kW North Sound's planners will propose, which sizes nameplate times a diversity factor rather than the decks' load. Not the 2026 meter peaks scaled up by the new units' rating, because a faster unit shortens a session instead of multiplying its load and the panel registers count morning hours the tariff does not bill. Not a replay of every session at the full 11.5 kW, which assumes every car can take it. Not a replay with the cars that made the 2026 sessions, because 18 county permits were renewed in January onto cars that charge at 11.0 kW. Not a replay of each settlement record as a charge of its own, because the daily settlement run carries a charge that is still running into a second record that would restart at full power. Not a replay that keeps every 2026 start time, because the county pool's attendant puts the next pool car on a unit when the car ahead finishes, and on the new units the car ahead finishes sooner.

## 2. Critical Components

1. On the new units each 2026 deck charge, its settlement records joined end to start, draws the lower of **11.5 kW** and its car's onboard charger rating until its delivered energy
2. The car is the one the permit carries in the contract year: **18** county permits moved from 7.2 kW to 11.0 kW Bolt EVs at the January 2027 renewal
3. At each of the **101** pool-car hand-offs on North Deck units in 2026, the next car starts once the car ahead finishes at its new draw, after the same wait
4. The replay's highest billing-hours quarter-hour in 2026 is **97.4 kW**, at 12:00 on Wednesday 21 January 2026
5. Grown by the **1.12** factor in force, January 2028's forecast billing demand is **109.1 kW**, the highest contract month

## 3. Step-by-Step Solution

1. Kept the sessions of record in `settled_sessions_2024-2026.csv` (the ACCEPTED version in `restatement_decisions_2025.csv`, one row per `auth_code`) and placed each on its unit by the `station_register.csv` assignment in service that day.
2. Joined each record that starts at its unit the second another ends there, on the same permit or card, into one charge (the pairs meet at the daily 10 a.m. settlement run in `curbline_export_field_notes.txt`), which reproduces every permit-month's charge count in `ev_permit_charging_statements_2026.csv`.
3. Took each permit's car from its January 2027 renewal row in `permit_vehicle_checks.csv` and its `onboard_charger_kw` from `vehicle_reference_list.csv` (fleet cards through `city_fleet_roster.csv`): 18 county permits now carry 2023 Bolt EVs at 11.0 kW where 2020 Bolt EVs at 7.2 kW made their 2026 sessions.
4. Replayed each 2026 deck charge from its 2026 start at the lower of 11.5 kW (Exhibit A of `civic_center_ev_service_agreement_draft.docx`) and that car's rating until its delivered energy, summing both decks per quarter-hour, except at the 101 pool-car hand-offs, where the attendant put a county pool car on a North Deck unit within ten minutes of another coming off (cars going on under 39 county permits in `ev_permit_registry.csv`; swaps noted on WO-26-0529 in `facilities_work_orders_2026.csv`): in every one the car ahead came off 6 to 20 minutes after finishing, while the decks' other charges stayed plugged in a median 6.7 hours after finishing, so the next car starts once the car ahead finishes at its new rate, after the same wait.
5. Took each month's highest quarter-hour beginning 12:00 to 19:45 on the billing days of `nspl_schedule_26_ev_charging_service.pdf` and grew it, unrounded, by the 1.12 in Table 1 of `fes-07_load_forecasting_standard_rev4.pdf` (one rounding, per its section 4): 97.4 kW at 12:00 on 21 January 2026 makes January 2028 109.1 kW, which files 110 kW in Schedule 26's 5 kW steps whether rounded to the nearest step or up.
6. Back-tested FES-07 on 2025 from the 2024 deck billing demand as its records stood when that forecast was made (FES-07 section 4, so the twelve 2024 sessions restated in March 2025 count at their earlier version), including `gateway_b_sessions_jan-apr2024.csv` and the fleet card charges in `fleet_card_ev_transactions_2024-2026.csv` the export does not carry (stamped in UTC, placed in local time), times the 1.08 factor in force then and rounded once, in whole kW against 2025's actual billing demand in whole kW, built the same way from the accepted 2025 versions in `restatement_decisions_2025.csv` with the January to March 2025 fleet card charges included: errors run from -1.9% to +2.5%, six over and six under.
7. Set each 2026 read span in `deck_panel_meter_log_2024-2026.xlsx`, its Corrections sheet applied, on the meters' standard-time clock (`deck_submeter_nameplates.csv`), the later 31 December South read standing, against the energy of the sessions on the units `deck_panel_circuit_schedule.csv` places on each panel, the weekend and holiday sessions in `curbline_courtesy_sessions_civic_decks_2024-2026.csv` included: 517 to 1,133 kWh unaccounted per read.
8. Recommendation: file 110 kW as the contracted demand for April 2027 to March 2028.

## 4. Deliverable Answers

### contract_demand_note.pdf

1. Contracted demand for the first contract year: 110 kW
2. Forecast billing demand by contract month, whole kW:
   - April 2027: 74 kW
   - May 2027: 77 kW
   - June 2027: 87 kW
   - July 2027: 80 kW
   - August 2027: 67 kW
   - September 2027: 95 kW
   - October 2027: 86 kW
   - November 2027: 79 kW
   - December 2027: 97 kW
   - January 2028: 109 kW
   - February 2028: 76 kW
   - March 2028: 82 kW
3. The month that sets the figure: January 2028
4. In the quarter-hour that sets it, forecast on the new units for January 2028: North Deck 56 kW, South Deck 53 kW
5. North Sound's planners' figure: 225 kW, 115 kW above our 110 kW

### deck_load_day.png

1. Wednesday 21 January 2026, the basis day for January 2028, both decks combined by quarter-hour
2. Two series: what the decks drew on the 6.6 kW units that day, and the forecast on the 11.5 kW units for January 2028
3. The contracted figure as a line labelled 110 kW
4. The 12:00 quarter-hour marked at 109 kW
5. Title: "File 110 kW: the decks' busiest billed quarter-hour on the new units comes to 109 kW at noon"

### civic_service_demand.xlsx

1. 2025 forecast from 2024 under FES-07, and its error as a percentage of the actual:
   - January 2025: 112 kW, -0.9%
   - February 2025: 122 kW, +1.7%
   - March 2025: 105 kW, -1.9%
   - April 2025: 102 kW, +1.0%
   - May 2025: 102 kW, -1.0%
   - June 2025: 83 kW, +2.5%
   - July 2025: 83 kW, -1.2%
   - August 2025: 82 kW, +1.2%
   - September 2025: 107 kW, -1.8%
   - October 2025: 114 kW, +1.8%
   - November 2025: 121 kW, +1.7%
   - December 2025: 114 kW, -0.9%
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
   - North Deck panel CP-N, read 11 (November 30): 1,063 kWh
   - North Deck panel CP-N, read 12 (December 31): 1,133 kWh
   - South Deck panel CP-S, read 1 (January 30): 934 kWh
   - South Deck panel CP-S, read 2 (February 27): 799 kWh
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
