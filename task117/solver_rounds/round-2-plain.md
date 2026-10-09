# solver round: round 2, plain

**Proxy score 89.2 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 47.2 of 58). Main call LANDED. 6 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: File 130 kW as the contracted demand for the first contract year, April 2027 to March 2028.

solver: File a first-contract-year Contract Demand of 130 kW. That is the forecast December billing demand of 129 kW, rounded to the 5 kW step. The December figure comes from the 12:00 quarter-hour on Tuesday 8 December 2026: 115.3 kW once the 2026 deck sessions are re-run on the 11.5 kW pedestals with each permit's January-2027 vehicle, times the FES-07 2027 factor of 1.12. NSPL's planners will propose 225 kW (32 x 11.5 kW x 0.60 diversity), which is 95 kW above ours.

tokens matched 2 of 4 (130, File, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| contract_demand_note.pdf | 1 | 1 | 2 | 50% |
| contract_demand_note.pdf | 2 | 14 | 24 | 58% |
| contract_demand_note.pdf | 3 | 1 | 1 | 100% |
| contract_demand_note.pdf | 4 | 4 | 4 | 100% |
| contract_demand_note.pdf | 5 | 2 | 3 | 67% |
| deck_load_day.png | 1 | 3 | 3 | 100% |
| deck_load_day.png | 2 | 2 | 3 | 67% |
| deck_load_day.png | 3 | 1 | 1 | 100% |
| deck_load_day.png | 4 | 2 | 2 | 100% |
| deck_load_day.png | 5 | 4 | 4 | 100% |
| civic_service_demand.xlsx | 1 | 24 | 35 | 69% |
| civic_service_demand.xlsx | 2 | 54 | 82 | 66% |

## Solver's path

1. Read the prompt, Schedule 26 (billing demand is the highest 15-minute kW, starting 12:00-19:45 on weekdays, holidays excluded; contract demand in 5 kW steps), FES-07 Rev 4 (base is the latest 12 closed months at the equipment the service will supply; use the factor in force on the forecast date, which gives 1.12 now) and NSPL Guide 7.3 (nameplate x diversity, rounded to the next 5 kW).
2. Built the deck sessions from settled_sessions. Kept version 1 or the ACCEPTED restated version from restatement_decisions_2025. Dropped re-delivered duplicates by auth_code (45). Joined station_register by station_id and session date within the in-service dates, because ids 105085/097/108/227/240/250 were reused at Ferry Terminal and Market Square after 2025. Result: 21,217 deck sessions (no PUBLIC).
3. Gave each session a vehicle onboard-charger rating: permit_vehicle_checks matched to vehicle_reference_list by make, model, trim and model year, and fleet cards through city_fleet_roster. Checked that the intervals parquet equals a constant min(6.6 kW, OBC) draw from plug-in until the session's kWh is delivered: 0 mismatches in a 300-session sample.
4. Forecast base = Jan-Dec 2026 (December had settled by 10 Jan 2027). Re-simulated each 2026 session at min(11.5 kW, OBC), using the vehicle on the permit at the January 2027 renewal (18 County Bolt EVs went from 2020 at 7.2 kW to 2023 at 11.0 kW). Took the monthly maximum of the deck total in the billing window and applied x1.12. December gives 115.3 -> 129 kW, at 12:00 on 8 Dec 2026 (North 74.0, South 41.3 kW). The filing is 130 kW. For comparison, the old pedestals with 2026 vehicles peak at 158 kW in Feb, and new pedestals with 2026 vehicles give 149 kW.
5. NSPL sizing: 32 x 11.5 = 368 kW x 0.60 (21-40 units) = 220.8 -> 225 kW. Gap is 95 kW.
6. Backtest: monthly billing demand for 2024 and 2025 on the old pedestals. Added the 301 gateway_b sessions (Jan-Apr 2024, North Deck) and 40 Civic fleet-card transactions whose NETWORK_REF is missing from the settlement export (2024 to Mar 2025). The 2025 forecast is round(2024 month x 1.08), the factor in force in January 2025 when 2024 was the latest closed year. Error = (forecast - round(actual)) / round(actual).
7. Meter reconciliation: meter reads are on PST with no DST, so I converted them to UTC. Where a meter was read twice on 31 Dec, the later CP-S read stands. Session kWh between reads comes from the exact constant-rate profile, not 15-minute bins. EVSE N-11 sessions from 1 Jun to 12 Jul 2026 are taken off CP-N because N-11 was on the HP-N temporary feed (WO-26-0418). Residual = meter delta - session kWh. It follows the photocell lighting pattern (2.4 kW North, 2.1 kW South).

confidence: medium-high: the contract figure (130 kW) depends on using the January-2027 renewal vehicles. With 2026 vehicles it would be 150 kW. The backtest percentages depend on using factor 1.08 rather than the April-2025 revision to 1.09; with 1.09, six months show 0.0% error.

notes: The deck kW split at the setting quarter-hour is given after growth (83/46); before growth it is 74.0/41.3. Whether the first contract year starts in April or May 2027 does not move the figure, because December sets it either way.

### contract_demand_note.pdf (solver's answers)
- Contract demand to file, first contract year: 130 kW (forecast maximum billing demand 129 kW, rounded to the 5 kW step)
- Forecast billing demand by month of the contract year (base month 2026 x 1.12, whole kW): Apr 2027 90 kW; May 85 kW; Jun 79 kW; Jul 72 kW; Aug 75 kW; Sep 87 kW; Oct 94 kW; Nov 103 kW; Dec 2027 129 kW; Jan 2028 109 kW; Feb 2028 68 kW; Mar 2028 98 kW
- Month that sets the figure: December (base day Tuesday 8 Dec 2026, quarter-hour 12:00-12:15 PST; base 115.3 kW x 1.12 = 129 kW)
- kW each deck carries in the setting quarter-hour: North Deck 83 kW, South Deck 46 kW (forecast, after growth; before growth on the base day: North 74.0 kW, South 41.3 kW)
- NSPL planners' figure and gap to ours: NSPL 225 kW (32 units x 11.5 kW = 368 kW x 0.60 = 220.8, rounded up to the next 5 kW); gap 95 kW above our 130 kW

### deck_load_day.png (solver's answers)
- Day behind the figure: Tuesday 8 December 2026, by quarter-hour
- What the decks drew at the setting quarter-hour (old 6.6 kW pedestals): 132 kW at 12:00-12:15 (North 66 kW, South 66 kW); this was also the actual December 2026 billing demand
- Forecast draw at the setting quarter-hour on the new pedestals: 129 kW (115.3 kW base x 1.12)
- Contracted line: 130 kW
- Setting quarter-hour marked: 12:00 PST, 8 Dec 2026
- Title: Civic Center decks: file 130 kW. The new pedestals' noon draw on 8 Dec sets a 129 kW peak

### civic_service_demand.xlsx (solver's answers)
- 2025 backtest: FES-07 forecast from 2024 (factor 1.08), actual billing demand, error % of actual: Jan 112 vs 113, -0.9%; Feb 117 vs 114, +2.6%; Mar 107 vs 109, -1.8%; Apr 106 vs 104, +1.9%; May 88 vs 89, -1.1%; Jun 88 vs 86, +2.3%; Jul 82 vs 83, -1.2%; Aug 90 vs 88, +2.3%; Sep 106 vs 107, -0.9%; Oct 114 vs 112, +1.8%; Nov 113 vs 112, +0.9%; Dec 111 vs 112, -0.9% (2024 base kW: 103.6, 108.4, 99.1, 98.2, 81.7, 81.4, 76.0, 83.2, 98.3, 105.4, 104.8, 103.0)
- SM-2231 (CP-N) unaccounted kWh per 2026 reading: Jan 30: 1069; Feb 27: 908; Mar 31: 910; Apr 30: 725; May 29: 594; Jun 30: 592; Jul 31: 599; Aug 31: 691; Sep 30: 791; Oct 30: 914; Nov 30: 1065; Dec 31: 1130 kWh
- SM-2232 (CP-S) unaccounted kWh per 2026 reading: Jan 30: 934; Feb 27: 798; Mar 31: 794; Apr 30: 633; May 29: 520; Jun 30: 517; Jul 31: 523; Aug 31: 606; Sep 30: 693; Oct 30: 799; Nov 30: 932; Dec 31 (later 09:52 read): 990 kWh
