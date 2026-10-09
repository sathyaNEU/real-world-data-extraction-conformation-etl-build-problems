# solver round: round 5, plain

**Proxy score 28.5 / 100** (recommendation 1.2 of 35, instruction 7.0 of 7, asks 20.3 of 58). Main call missed. 0 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: File 110 kW as the contracted demand for the first contract year, April 2027 to March 2028.

solver: File a first-contract-year Contract Demand of 130 kW (Apr 2027–Mar 2028). The forecast peak billing demand is 129 kW. It comes from the 2026 base month of December: the Tue 8 Dec 2026 12:00 quarter-hour carries 115.3 kW once each charge is re-run on the 11.5 kW pedestals at the January 2027 permit vehicles' onboard-charger limits, and FES-07's 1.12 factor takes that to 129 kW. NSPL's planners will propose 225 kW (32 × 11.5 kW × 0.60 diversity, taken to the next 5 kW above), which is 95 kW more than our filing.

tokens matched 1 of 4 (110, File, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| contract_demand_note.pdf | 1 | 1 | 2 | 50% |
| contract_demand_note.pdf | 2 | 10 | 24 | 42% |
| contract_demand_note.pdf | 3 | 0 | 1 | 0% |
| contract_demand_note.pdf | 4 | 2 | 4 | 50% |
| contract_demand_note.pdf | 5 | 2 | 3 | 67% |
| deck_load_day.png | 1 | 0 | 3 | 0% |
| deck_load_day.png | 2 | 1 | 3 | 33% |
| deck_load_day.png | 3 | 0 | 1 | 0% |
| deck_load_day.png | 4 | 1 | 2 | 50% |
| deck_load_day.png | 5 | 2 | 4 | 50% |
| civic_service_demand.xlsx | 1 | 6 | 35 | 17% |
| civic_service_demand.xlsx | 2 | 50 | 82 | 61% |

## Solver's path

1. Read the request, FES-07 Rev 4, Schedule 26, NSPL guide section 7 and the draft agreement. Billing window: weekdays 12:00–19:45, excluding Schedule 26 holidays. Base months: latest 12 closed months = Jan–Dec 2026. Growth factor in force for a forecast made in Feb 2027: 1.12. Equipment: 32 units at 11.5 kW.
2. Kept deck sessions only where the session date falls inside the station's in-service dates in station_register.csv. This handles the 1 Apr 2025 ID migration and drops reused IDs 105085/097/108/227/240/250, which moved to Ferry Terminal and Market Square. Dropped auth_code redeliveries. Took the in-force version from restatement_decisions_2025 (ACCEPTED replaces the earlier version, REJECTED leaves it). Result: 29,655 charges.
3. Found that the 10:00 settlement run splits charges: 8,879 records end and restart on the same permit and position at 10:02–10:04, both at the full 6.6 kW. Merged them into 20,776 charges. The merged 2026 counts and kWh match ev_permit_charging_statements_2026 exactly on all 875 permit-months.
4. Checked that a constant-rate model re-creates session_intervals exactly (maximum difference about 1e-8). Re-ran every 2026 charge from plug-in at min(11.5 kW, onboard charger) for the permit vehicle at its January 2027 renewal check (vehicle_reference_list; fleet cards use city_fleet_roster). Took the maximum 15-minute deck total in the window for each month, multiplied by 1.12 and rounded to whole kW. December was highest at 115.3 kW, giving 129 kW, which rounds to 130 kW on the 5 kW grid. The same method at 6.6 kW gives a December peak of 132 kW; with 2026 vehicles on 11.5 kW pedestals, Feb sets it at 132.6 kW, giving 149 kW.
5. NSPL sizing: 32 × 11.5 = 368 kW × 0.60 (21–40 units) = 220.8, taken to 225 kW. Gap to our figure: 95 kW.
6. Backtest: the 2024 base is the export as it stood in Jan–early Mar 2025 (v1 of 2024 sessions, before the March 2025 restatements), plus gateway B sessions Jan–Apr 2024 and 40 pre-migration fleet-card sessions at the decks that are missing from the export. Forecast = base × 1.08 (the factor in force before 8 Apr 2025), rounded to whole kW. Actual 2025 billing demand uses the final in-force versions. Error = (forecast − actual) / actual, from whole-kW figures.
7. Meter check: took the Reads sheet, kept the later read on 31 Dec 2026 SM-2232 (198027.4), and applied the Corrections sheet. Read times are fixed PST (meter DST disabled) and were converted to local time. Session kWh for each read period was summed by quarter-hour from export sessions plus the courtesy weekend/holiday sessions, excluding N-11 from 1 Jun to 12 Jul 2026, when it ran on HP-N 14/16. Residual = meter delta − session kWh. The residuals are smooth and seasonal, consistent with the roof lighting on each panel (2400/2100 VA).

confidence: Medium-high. The filed figure depends on using the January 2027 renewal vehicles and on merging the 10:00 split charges; both are well supported by the data. The backtest depends on taking the forecast date as January 2025 (factor 1.08, unrestated 2024 records).

notes: The files don't say when the hypothetical 2025 forecast was made; I took Jan–early Mar 2025, which gives factor 1.08 and the unrestated 2024 records. The deck kW in the setting quarter-hour is given with the 1.12 growth applied (North 83, South 46); before growth it is 74.0 and 41.3 kW.

### contract_demand_note.pdf (solver's answers)
- Contracted demand to file, first contract year: 130 kW (forecast maximum is 129 kW, rounded to the nearest 5 kW)
- Forecast billing demand for each contract-year month (whole kW): Apr 2027 90; May 85; Jun 79; Jul 72; Aug 75; Sep 87; Oct 94; Nov 103; Dec 129; Jan 2028 109; Feb 68; Mar 98. Each month is built from the same 2026 base month times 1.12. The 2026 base maxima are: Jan 97.4, Feb 60.6, Mar 87.4, Apr 80.6, May 75.8, Jun 70.6, Jul 64.4, Aug 66.8, Sep 77.8, Oct 84.0, Nov 92.2, Dec 115.3 kW.
- Month that sets the figure: December (December 2027, built from base month December 2026). The setting quarter-hour is Tue 8 Dec 2026, 12:00–12:15.
- kW each deck carries in the setting quarter-hour: North Deck 83 kW, South Deck 46 kW (forecast total 129 kW). Before the 1.12 growth factor the split is North 74.0 kW and South 41.3 kW, a total of 115.3 kW.
- NSPL planners' figure and gap to ours: NSPL proposes 225 kW (368 kW nameplate × 0.60 = 220.8, taken to the next 5 kW above). The gap to our 130 kW is 95 kW.

### deck_load_day.png (solver's answers)
- Day behind the figure: Tuesday 8 December 2026, by quarter-hour
- What the decks drew that day (6.6 kW pedestals): 737 kWh for the day. Peak 146 kW at 09:45, outside the billing window. At the setting 12:00 quarter-hour they drew 132 kW.
- Forecast draw on new pedestals that day: 826 kWh for the day (737.2 × 1.12). Peak 197 kW at 09:45, outside the billing window. The load is 129 kW from 11:30 through 12:00, then drops to 69 kW at 12:30, 20 kW at 12:45 and 4 kW at 13:00.
- Contracted figure line and marked quarter-hour: Line at 130 kW. The marked quarter-hour is 12:00–12:15 at 129 kW forecast (North 83, South 46).
- Quotable title: Civic Center decks: we file 130 kW, set by a forecast 129 kW at noon on a December weekday (8 Dec 2026 base day)

### civic_service_demand.xlsx (solver's answers)
- 2025 backtest: forecast from 2024 (factor 1.08) vs recorded billing demand and error % of actual: Forecast / actual (kW) / error: Jan 111/112 −0.9%; Feb 121/119 +1.7%; Mar 104/106 −1.9%; Apr 101/101 0.0%; May 101/103 −1.9%; Jun 82/81 +1.2%; Jul 82/84 −2.4%; Aug 81/81 0.0%; Sep 106/109 −2.8%; Oct 113/112 +0.9%; Nov 120/119 +0.8%; Dec 113/115 −1.7%
- SM-2231 (CP-N) unaccounted kWh per 2026 reading: Jan 30: 1069; Feb 27: 908; Mar 31: 910; Apr 30: 725; May 29: 594; Jun 30: 592; Jul 31: 599; Aug 31: 691; Sep 30: 791; Oct 30: 914; Nov 30: 1063; Dec 31: 1133 kWh
- SM-2232 (CP-S) unaccounted kWh per 2026 reading: Jan 30: 934; Feb 27: 799; Mar 31: 794; Apr 30: 633; May 29: 520; Jun 30: 517; Jul 31: 523; Aug 31: 606; Sep 30: 693; Oct 30: 799; Nov 30: 932; Dec 31: 990 kWh
