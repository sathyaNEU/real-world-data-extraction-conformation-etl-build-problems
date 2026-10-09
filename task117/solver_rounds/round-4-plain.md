# solver round: round 4, plain

**Proxy score 25.6 / 100** (recommendation 1.2 of 35, instruction 7.0 of 7, asks 17.3 of 58). Main call missed. 0 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: File 110 kW as the contracted demand for the first contract year, April 2027 to March 2028.

solver: File a first-contract-year Contract Demand of 130 kW in Schedule 1. December sets it: the December 2026 base month, re-simulated on the 32 new 11.5 kW Exhibit A units with the vehicles registered at the January 2027 renewals and scaled by the FES-07 2027 growth factor of 1.12, gives a forecast billing demand of 129 kW (115.3 kW × 1.12), which rounds up to the 5 kW multiple of 130 kW. That is 95 kW below the 225 kW NSPL's planners will propose (32 × 11.5 kW × 0.60 diversity = 220.8 kW, taken to the next 5 kW).

tokens matched 1 of 4 (110, File, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| contract_demand_note.pdf | 1 | 1 | 2 | 50% |
| contract_demand_note.pdf | 2 | 7 | 24 | 29% |
| contract_demand_note.pdf | 3 | 0 | 1 | 0% |
| contract_demand_note.pdf | 4 | 2 | 4 | 50% |
| contract_demand_note.pdf | 5 | 2 | 3 | 67% |
| deck_load_day.png | 1 | 0 | 3 | 0% |
| deck_load_day.png | 2 | 0 | 3 | 0% |
| deck_load_day.png | 3 | 0 | 1 | 0% |
| deck_load_day.png | 4 | 1 | 2 | 50% |
| deck_load_day.png | 5 | 1 | 4 | 25% |
| civic_service_demand.xlsx | 1 | 10 | 35 | 29% |
| civic_service_demand.xlsx | 2 | 48 | 82 | 59% |

## Solver's path

1. Read the prompt, Schedule 26 (billing demand is the highest 15-minute load from 12:00 to 19:45 on weekdays, excluding the listed holidays; contract demand is set in multiples of 5 kW and resets upward if exceeded), FES-07 Rev 4 (base is the latest 12 closed months, prepared for the equipment the service will supply, and uses the factor in force on the day the forecast is made: 1.12 for a January 2027 forecast), NSPL guide Section 7 and the draft agreement (32 units at 11.5 kW replacing 6.6 kW units; Contract Year 1 starts in the first full month after energization on about 1 April 2027).
2. Cleaned settled_sessions_2024-2026.csv. Took version 1 unless a later version was ACCEPTED in restatement_decisions_2025.csv (the highest accepted version stands; REJECTED versions are ignored). Removed re-delivered rows by auth_code, keeping the first delivery. Assigned each station_id to a garage and position using the station_register in-service dates, which handles the April 2025 ID migration and the reuse of six old Civic IDs at Ferry Terminal and Market Square. 2026 Civic result: 10,142 sessions, 89,551 kWh.
3. Added Civic sessions missing from the settlement export: 299 gateway B sessions (Jan to Apr 2024) and 40 fleet card transactions at Civic stations (2024 to Mar 2025) whose NETWORK_REF matches no auth_code. Gave both a flat 6.6 kW quarter-hour profile, which matches the observed interval shape.
4. Found that the settlement run cuts any session in progress at about 10:03 into two records with the same permit or card and a gapless join. For the re-simulation, merged these back into single plug-ins: 10,142 records became 7,046 sessions.
5. Re-simulated 2026 on the new units. Each merged session delivers its kWh from plug-in at min(11.5 kW, the vehicle's onboard charger rating). Vehicles come from the latest permit_vehicle_checks entry (the January 2027 renewals moved 18 county pool permits from 2020 Bolt EVs at 7.2 kW to 2023 Bolt EVs at 11.0 kW) and from city_fleet_roster for fleet cards, with ratings looked up in vehicle_reference_list. Took the monthly maximum quarter-hour in the window using 2026 holidays, multiplied by 1.12 and rounded to whole kW. December is the highest: 115.3 kW × 1.12 = 129 kW at 12:00 on 8 Dec 2026, which rounds up to 130 kW. As cross-checks, 2026 vehicles give 149 kW and unmerged records give 155 kW.
6. NSPL planner figure: 32 × 11.5 × 0.60 = 220.8 kW, which goes to 225 kW. The gap to our filing is 95 kW.
7. 2025 backtest: the 2024 base uses records as delivered before the March 2025 restatements (FES-07 says forecasts are not restated), plus gateway B and the fleet extras, × 1.08 (the factor in force in January and February 2025), rounded to whole kW. Actual 2025 billing demand uses final accepted versions plus fleet extras, rounded to whole kW. Error = (forecast - actual) / actual, giving between -2.8% and +1.7%.
8. Meter check: took the later reading where a meter was read twice in a day (31 Dec CP-S at 09:45), then applied the Corrections sheet. Converted the meter clock (PST, DST disabled) to local time, which adds an hour during PDT. Summed quarter-hour session kWh between reads for each panel, including courtesy sessions on a 6.6 kW profile and excluding N-11 from 1 Jun to 12 Jul 2026 while it ran on the HP-N temporary feed. Unaccounted kWh = meter delta - session kWh. CP-S/CP-N comes out at about 0.875 every month, close to the 2.1/2.4 kVA ratio of the photocell roof-light circuits, which supports the method.

confidence: Medium-high on the 130 kW call and the meter residuals; medium on the 2025 backtest. Its errors depend on dating the forecast before 8 April 2025 (factor 1.08 rather than 1.09) and before the 2024 restatements.

notes: The contract-year month labels assume energization in early April 2027, which makes May 2027 to April 2028 Contract Year 1. If April 2027 counts instead, the labels shift but the December maximum, and so 130 kW, does not change. Per-deck kW at the setting quarter-hour are forecast values after the 1.12 factor; before it they are 74.0 and 41.3 kW.

### contract_demand_note.pdf (solver's answers)
- Contracted demand to file, first contract year: 130 kW (whole multiple of 5 kW, rounded up from a 129 kW December forecast)
- Forecast billing demand for each month of the contract year (May 2027 to Apr 2028, each built from the same 2026 month × 1.12): May 2027 85 kW; Jun 2027 79 kW; Jul 2027 72 kW; Aug 2027 75 kW; Sep 2027 87 kW; Oct 2027 94 kW; Nov 2027 103 kW; Dec 2027 129 kW; Jan 2028 109 kW; Feb 2028 68 kW; Mar 2028 98 kW; Apr 2028 90 kW
- Month that sets the figure: December (Dec 2027 forecast, from base day Tuesday 8 December 2026): 129 kW
- kW each deck carries in the setting quarter-hour (12:00 to 12:15): North Deck 83 kW, South Deck 46 kW, total 129 kW (forecast; before the 1.12 factor: North 74.0 kW, South 41.3 kW, total 115.3 kW)
- Figure NSPL planners will propose: 225 kW (32 units × 11.5 kW = 368 kW × 0.60 diversity factor for 21 to 40 units = 220.8 kW, taken to the next 5 kW)
- Gap between NSPL's figure and ours: 95 kW (225 kW minus 130 kW)
- Base months and factor stated: Base months Jan to Dec 2026; growth factor 1.12 (2027 factor, adopted 15 Sep 2026)

### deck_load_day.png (solver's answers)
- The day behind the figure: Tuesday 8 December 2026, by quarter-hour
- What the decks drew that day: Peak of 146 kW at 09:45; 132 kW from 11:15 to 12:15, which was the day's billing-window peak and December 2026's actual billing demand at 12:00; 737 kWh delivered that day
- Forecast draw on the new pedestals: Peak of 197 kW at 09:45 (outside the billing window); 129 kW in the 12:00 quarter-hour, falling to 126 kW at 12:15, 69 kW at 12:30 and 0 kW from 13:15; same 737 kWh before the 1.12 factor
- Contracted figure line: 130 kW
- Setting quarter-hour marked: 12:00 to 12:15 on 8 December 2026, at 129 kW forecast (North 83 kW, South 46 kW)
- Quotable title: New chargers finish most morning charging before noon: the decks' highest forecast billing quarter-hour is 129 kW, so we contract 130 kW, not NSPL's 225 kW

### civic_service_demand.xlsx (solver's answers)
- 2025 backtest: forecast from 2024 base × 1.08, against actual billing demand, error % of actual: Jan 111 vs 112 kW, -0.9%; Feb 121 vs 119 kW, +1.7%; Mar 104 vs 106 kW, -1.9%; Apr 101 vs 101 kW, 0.0%; May 101 vs 103 kW, -1.9%; Jun 82 vs 81 kW, +1.2%; Jul 82 vs 84 kW, -2.4%; Aug 81 vs 81 kW, 0.0%; Sep 106 vs 109 kW, -2.8%; Oct 113 vs 112 kW, +0.9%; Nov 120 vs 119 kW, +0.8%; Dec 113 vs 115 kW, -1.7%
- 2024 base billing demand used for the backtest (records as they stood in early 2025): Jan 102.9; Feb 112.1; Mar 96.7; Apr 93.8; May 93.6; Jun 76.3; Jul 76.2; Aug 75.4; Sep 98.2; Oct 105.1; Nov 111.2; Dec 104.7 kW
- SM-2231 / CP-N, kWh the meter recorded that sessions don't account for, per 2026 reading: 30 Jan 1069; 27 Feb 908; 31 Mar 910; 30 Apr 725; 29 May 594; 30 Jun 592; 31 Jul 599; 31 Aug 691; 30 Sep 791; 30 Oct 914; 30 Nov 1063; 31 Dec 1133 kWh
- SM-2232 / CP-S, kWh the meter recorded that sessions don't account for, per 2026 reading: 30 Jan 934; 27 Feb 799; 31 Mar 794; 30 Apr 633; 29 May 520; 30 Jun 517; 31 Jul 523; 31 Aug 606; 30 Sep 693; 30 Oct 799; 30 Nov 932; 31 Dec 990 kWh
