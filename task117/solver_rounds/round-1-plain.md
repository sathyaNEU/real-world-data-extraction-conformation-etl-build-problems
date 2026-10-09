# solver round: round 1, plain

**Proxy score 88.1 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 46.1 of 58). Main call LANDED. 5 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: File 150 kW as the contracted demand for the first contract year, April 2027 to March 2028.

solver: File 150 kW as the first-contract-year Contract Demand. The forecast peaks at 149 kW in the February month: the decks' 2026 settled sessions were re-run on the 11.5 kW pedestals, each vehicle capped at its own onboard-charger rating, and grown by the FES-07 2027 factor of 1.12. The peak falls in the 12:00 quarter-hour on Tue 17 Feb 2026, with North carrying 99 kW and South 50 kW. That sits 75 kW below NSPL's planner sizing of 225 kW.

tokens matched 2 of 4 (150, File, April, March)

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
| deck_load_day.png | 5 | 3 | 4 | 75% |
| civic_service_demand.xlsx | 1 | 24 | 35 | 69% |
| civic_service_demand.xlsx | 2 | 56 | 82 | 68% |

## Solver's path

1. Read the prompt, the agreement draft (32 x 11.5 kW units replacing 6.6 kW units; first Contract Year starts at energization around 1 Apr 2027), Schedule 26 (billing demand is the highest 15-minute load in intervals starting 12:00-19:45 on non-holiday weekdays, calendar month; Contract Demand in 5 kW multiples), FES-07 Rev 4 (latest 12 closed months, so the 2026 base; same calendar month; forecast for the equipment the service will supply; factor in force on the forecast date, 1.12 adopted 15 Sep 2026; whole kW; error = forecast less actual as a % of actual), and NSPL Guide Sec 7 (nameplate x diversity, next 5 kW above).
2. settled_sessions: mapped station_id to garage using station_register in-service dates, because six old Civic IDs were reused at Ferry/Market garages after Aug 2025. Applied restatement_decisions_2025: an ACCEPTED version replaces the earlier one, a REJECTED version is ignored. Removed 71 redelivered duplicates by auth_code. This left 21,217 Civic sessions (6,867 / 7,143 / 7,207 for 2024 / 2025 / 2026), all PERMIT or FLEET.
3. Validated the profile model: re-simulating each 2026 session at a constant 6.6 kW from plug_in until its kWh is delivered reproduces session_intervals exactly (max difference 1e-9). Actual 2026 monthly billing demand: Jan 138.6, Feb 158.4, Mar 125.4, Apr 125.4, May 112.2, Jun 105.6, Jul 92.4, Aug 99.0, Sep 118.8, Oct 118.8, Nov 132.0, Dec 132.0 kW, every peak in the 12:00 quarter-hour.
4. Vehicle limits: matched each permit session to the vehicle on its latest permit_vehicle_checks entry on or before the session date, and fleet cards to city_fleet_roster. Looked up onboard_charger_kw in vehicle_reference_list by make, model, trim and model year: Bolt EV/Kona/Niro <=2022 7.2; Model 3 SR+ 7.7; ID.4/XC40/Polestar 2/Bolt EUV/Niro 2023 11.0. The new rate is min(11.5, onboard).
5. Re-simulated the 2026 sessions at the new rates with the same plug_in and kWh, then computed billing demand under Schedule 26 with the 2026 holidays. February peaks at 133.1 kW at 12:00 on 17 Feb 2026 (N 88.4, S 44.7). Multiplied each month by 1.12 and rounded to whole kW: the maximum is Feb at 149 kW, so the filing is 150 kW. This holds whether the contract year runs Apr-Mar or May-Apr.
6. NSPL sizing: 368 kW x 0.60 = 220.8 kW, giving 225 kW and a gap of 75 kW.
7. Backtest: the 2024 base used settled intervals plus the 302 gateway_b sessions (Jan to 22 Apr 2024, North units, built at 6.6 kW from Start). Computed monthly 2024 billing demand, x 1.08 (in force when a forecast from closed 2024 months would have been made in Jan 2025), rounded, and compared with actual 2025 billing demand from the in-force session versions, rounded to whole kW. Errors range from -2.9% to +2.3%.
8. Panel meters: read the meter log, keeping the later read when a meter has two reads on one day. Converted meter times from fixed PST (DST disabled) to UTC. Summed each panel's in-force session interval kWh between consecutive reads, moving N-11 to HP-N for 1 Jun to 12 Jul 2026 per the circuit schedule and WO-26-0418. Unaccounted = register delta - session kWh, rounded to whole kWh.

confidence: medium-high

notes: Two judgement calls could change figures. First, the backtest uses factor 1.08, the one in force in Jan 2025; using the Apr 2025 mid-year 1.09 shifts each 2025 forecast by about 1 kW. Second, the 31 Dec 2026 South read uses the later but lower register value (197585.6) because the log's rule says the later read stands. The filed 150 kW is the same under rounding to the nearest 5 kW or rounding up.

### contract_demand_note.pdf (solver's answers)
- Contract demand to file, first contract year: 150 kW (forecast maximum 149 kW, rounded to the nearest 5 kW; rounding up to the next 5 kW also gives 150 kW)
- Forecast billing demand by month of the contract year (Apr 2027 to Mar 2028), whole kW: Apr 2027 115; May 2027 106; Jun 2027 98; Jul 2027 90; Aug 2027 91; Sep 2027 108; Oct 2027 116; Nov 2027 124; Dec 2027 130; Jan 2028 132; Feb 2028 149; Mar 2028 123 kW. Each is the same-month 2026 billing demand on the new pedestals x 1.12. The unrounded 2026 bases, in the same order, are Apr 102.8, May 94.6, Jun 87.4, Jul 80.2, Aug 81.2, Sep 96.6, Oct 103.8, Nov 110.5, Dec 116.2, Jan 117.7, Feb 133.1, Mar 110.0 kW
- Month that sets the figure: February (Feb 2028, built from Feb 2026). The quarter-hour is 12:00-12:15 on Tuesday 17 Feb 2026, at 149 kW
- kW each deck carries in the setting quarter-hour: North Deck 99 kW; South Deck 50 kW (total 149 kW). The unrounded figures are 99.0 and 50.1 kW, from bases of 88.4 and 44.7 kW x 1.12
- NSPL planners' proposed figure and gap to ours: NSPL 225 kW: 32 units x 11.5 kW = 368 kW, x 0.60 diversity for 21-40 units = 220.8 kW, then the next 5 kW above. Gap = 225 - 150 = 75 kW above our filing

### deck_load_day.png (solver's answers)
- Day behind the figure: Tuesday 17 February 2026, combined North + South decks, plotted by quarter-hour
- What the decks drew in the setting quarter-hour (actual, old 6.6 kW pedestals): 158 kW at 12:00-12:15 (158.4 kW, all 24 connected units drawing 6.6 kW). This was also the actual Feb 2026 billing demand. The day's actual peak was 162 kW at 09:15, outside the billing window. Actual day energy 780 kWh
- Forecast draw on the new pedestals in the setting quarter-hour: 149 kW at 12:00-12:15 (North 99 kW, South 50 kW). The forecast day peak is 223 kW at 10:30-11:00, before the 12:00 start of the billing window. Forecast day energy 874 kWh (780 x 1.12)
- Contracted figure line: 150 kW
- Marked setting quarter-hour: 12:00-12:15, 17 Feb 2026 (first quarter-hour of the Schedule 26 weekday 12:00-19:45 billing window)
- Quotable title: New Civic Center deck chargers: contract 150 kW. The forecast peak is 149 kW at noon on a February weekday

### civic_service_demand.xlsx (solver's answers)
- 2025 backtest: FES-07 forecast from 2024 base (factor 1.08 in force Jan 2025) vs actual 2025 billing demand, error % of actual to 1 dp: Jan F114 vs A115, -0.9%; Feb 121 vs 119, +1.7%; Mar 108 vs 110, -1.8%; Apr 103 vs 102, +1.0%; May 96 vs 97, -1.0%; Jun 88 vs 86, +2.3%; Jul 82 vs 84, -2.4%; Aug 90 vs 89, +1.1%; Sep 101 vs 104, -2.9%; Oct 111 vs 110, +0.9%; Nov 114 vs 113, +0.9%; Dec 109 vs 110, -0.9%. The 2024 base billing demands, which include the gateway B sessions for Jan-Apr, were Jan 105.4, Feb 112.2, Mar 99.9, Apr 95.5, May 89.1, Jun 81.5, Jul 76.1, Aug 83.2, Sep 93.7, Oct 102.9, Nov 105.5, Dec 101.1 kW
- SM-2231 (CP-N) unaccounted kWh per 2026 reading (meter delta minus session kWh through CP-N): 30 Jan 1069; 27 Feb 909; 31 Mar 910; 30 Apr 725; 29 May 594; 30 Jun 592; 31 Jul 599; 31 Aug 691; 30 Sep 791; 30 Oct 914; 30 Nov 1065; 31 Dec 1130 kWh. N-11 sessions from 1 Jun to 12 Jul 2026 were on HP-N and are excluded from CP-N (240.5 kWh in total)
- SM-2232 (CP-S) unaccounted kWh per 2026 reading: 30 Jan 933; 27 Feb 800; 31 Mar 794; 30 Apr 633; 29 May 520; 30 Jun 517; 31 Jul 523; 31 Aug 606; 30 Sep 693; 30 Oct 799; 30 Nov 932; 31 Dec 990 kWh. The 31 Dec figure uses the later 09:45 read of 197585.6 per the log rule
