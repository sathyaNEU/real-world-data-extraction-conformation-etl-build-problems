# solver round: round 3, plain

**Proxy score 90.4 / 100** (recommendation 35.0 of 35, instruction 7.0 of 7, asks 48.4 of 58). Main call LANDED. 6 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: File 130 kW as the contracted demand for the first contract year, April 2027 to March 2028.

solver: File a first-contract-year Contract Demand of 130 kW. That is the December forecast of 129 kW, rounded to the nearest 5 kW. The 129 kW comes from the 2026 base (12:00-12:15 quarter-hour on Tue 8 Dec 2026, 115.3 kW simulated on the new 11.5 kW pedestals with each permit's 2027-renewal vehicle) times the FES-07 2027 growth factor of 1.12. It is 95 kW below the 225 kW that North Sound's planners will propose (32 units x 11.5 kW x 0.60 diversity, taken up to the next 5 kW).

tokens matched 2 of 4 (130, File, April, March)

## Asks

| file | item | tokens hit | of | share |
|---|---|---|---|---|
| contract_demand_note.pdf | 1 | 2 | 2 | 100% |
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
| civic_service_demand.xlsx | 2 | 54 | 82 | 66% |

## Solver's path

1. Read the request, the draft agreement, Schedule 26, NSPL Guide Sec. 7 and FES-07. Contract year is the 12 billing months from energisation (about 1 Apr 2027), i.e. Apr 2027-Mar 2028. Billing demand is the maximum 15-minute kW, weekdays, interval starts 12:00-19:45, with Schedule 26 holidays excluded. Base is Jan-Dec 2026, factor 1.12 (in force Jan 2027), and the forecast is built for the new 11.5 kW units.
2. Cleaned settled_sessions: kept the version given by restatement_decisions_2025 (highest ACCEPTED version, else v1). Deduplicated 84 redelivered auth_codes, keeping the earliest delivery. Mapped station_id to deck and position by plug-in date within the station_register in-service dates; this handles the 1 Apr 2025 renumbering and six old Civic IDs reused at Ferry and Market from Aug/Oct 2025.
3. Found that the 10:00 settlement run splits sessions: 8,741 pieces where plug_in equals the previous plug_out at the same position with the same card. Merged them into 20,497 physical sessions. ev_permit_charging_statements_2026 confirms this: charges equal merged sessions in 100% of permit-months, and kWh ties exactly.
4. Checked that session_intervals reproduce a constant 6.6 kW draw from plug-in. Recomputed actual 2024-2026 billing demand from the intervals. Added 301 gateway_b sessions (Jan-Apr 2024, North Deck, local time) and 40 Civic fleet-card charges missing from the export (2024-Mar 2025; fleet file START/END are in UTC), built at 6.6 kW. North 2024 monthly maxima then match the sub-meter max demand of 105.6 kW.
5. Forecast: re-ran each 2026 merged session's energy from plug-in at min(11.5 kW, on-board charger). The charger rating comes from the permit's Jan 2027 renewal vehicle via vehicle_reference_list (18 Bolt EVs move from 2020 at 7.2 kW to 2023 at 11.0 kW); fleet vehicles come from city_fleet_roster. Took monthly billing demand, multiplied by 1.12 and rounded to whole kW. The maximum is Dec at 115.3 x 1.12 = 129.136, i.e. 129 kW, so 130 kW at the nearest 5 kW. Peak quarter-hour is 8 Dec 2026 12:00 (North 74.0, South 41.3 kW before growth).
6. Sensitivities, not used: with 2026 vehicles the maximum would be 149 kW; with unmerged session pieces it would be 155 kW; actual 2026 billing demand on the old units reached 158.4 kW (Feb).
7. NSPL planner sizing: 32 x 11.5 = 368 kW x 0.60 (21-40 units) = 220.8 kW, taken to the next 5 kW above = 225 kW. Gap to our 130 kW is 95 kW.
8. Backcast: 2025 forecast = 2024 actual monthly billing demand x 1.08, the factor in force when a 2024-based forecast is made (Jan 2025, before the Apr 2025 revision to 1.09), rounded to whole kW. Compared with 2025 actual (restatements applied, fleet fixes Jan-Mar), rounded to whole kW. Error = (forecast - actual)/actual, to one decimal.
9. Meter check: meter_log reads converted from meter-clock PST (no DST) to UTC; where a meter was read twice in a day the later read was used (CP-S 31 Dec 09:52). For each 2026 read period, subtracted from the register delta the session kWh charged through the panel: settled pieces plus courtesy sessions, split at the read instant using the continuous 6.6 kW profile. N-11 sessions from 1 Jun to 12 Jul 2026 (24 sessions, 233.7 kWh) were left out of CP-N because the circuit schedule and WO-26-0418 put N-11 on HP-N then. The residual follows the roof pole lights (2.4 vs 2.1 kW, a ratio of 1.14).

confidence: Medium-high. The filed 130 kW holds as long as the 2026 sessions are merged across the 10:00 settlement split and simulated with the 2027-renewal vehicles. The backcast factor (1.08 vs 1.09) and the contract-year start month (April vs May) are the interpretive points; the start month does not change the maximum.

notes: The contract year is taken as Apr 2027-Mar 2028; if it starts in May the monthly labels shift but the 129 kW maximum stays. The backcast uses factor 1.08; with 1.09 the errors would be 0.0/+3.5/-0.9/+2.9/0.0/+3.5/0.0/+3.4/0.0/+2.7/+1.8/0.0%. The 31 Dec CP-S later read (197,675.4) is below the earlier one; it was used as the meter-log rule directs.

### contract_demand_note.pdf (solver's answers)
- Contracted demand to file, first contract year: 130 kW (nearest 5 kW; the forecast maximum billing demand is 129 kW)
- Forecast billing demand for each month of the contract year (Apr 2027-Mar 2028), whole kW: Apr 2027 90; May 85; Jun 79; Jul 72; Aug 75; Sep 87; Oct 94; Nov 103; Dec 129; Jan 2028 109; Feb 68; Mar 98 kW
- Month that sets the figure: December 2027 forecast month (base December 2026). The setting quarter-hour is 12:00-12:15 on Tuesday 8 Dec 2026.
- kW each deck carries in the setting quarter-hour: North Deck 83 kW, South Deck 46 kW (forecast, total 129 kW). The 2026 base before the 1.12 growth factor was North 74.0 kW and South 41.3 kW, total 115.3 kW.
- North Sound planners' figure and gap to ours: NSPL planners: 225 kW (32 x 11.5 kW = 368 kW x 0.60 = 220.8 kW, taken to the next 5 kW). Gap: 95 kW above our 130 kW filing (96 kW above the 129 kW forecast).
- Base and factor stated: Base months Jan-Dec 2026; county EV growth factor 1.12 (2027 factor, adopted 15 Sep 2026)

### deck_load_day.png (solver's answers)
- Headline contracted figure (line label): 130 kW contract demand line
- Day behind it: Tuesday 8 December 2026 (base day for December 2027)
- What the decks drew that day in the setting quarter-hour (old 6.6 kW pedestals): 132 kW at 12:00-12:15 (North 66, South 66). The day's actual peak was 152 kW at 09:30, outside the billing window. The day's energy was 704 kWh.
- Forecast on the new pedestals in the setting quarter-hour: 129 kW at 12:00-12:15 (115.3 kW simulated x 1.12; North 83, South 46). The day's forecast peak is 206 kW at 09:15, outside the noon-7:45 pm billing window. The load is about zero after 13:15.
- Marked quarter-hour: 12:00-12:15 on 8 Dec 2026
- Quotable title: Civic Center decks: a 130 kW contract covers the busiest billed quarter-hour, noon on a December weekday, on the new pedestals

### civic_service_demand.xlsx (solver's answers)
- 2025 backcast: FES-07 forecast from 2024 (factor 1.08) vs actual billing demand, kW, with error % of actual: Jan 112 vs 113 (-0.9%); Feb 117 vs 114 (+2.6%); Mar 107 vs 109 (-1.8%); Apr 106 vs 104 (+1.9%); May 88 vs 89 (-1.1%); Jun 88 vs 86 (+2.3%); Jul 82 vs 83 (-1.2%); Aug 90 vs 88 (+2.3%); Sep 106 vs 107 (-0.9%); Oct 114 vs 112 (+1.8%); Nov 113 vs 112 (+0.9%); Dec 111 vs 112 (-0.9%)
- 2024 base billing demand used (kW, unrounded): Jan 103.6; Feb 108.4; Mar 99.1; Apr 98.2; May 81.7; Jun 81.4; Jul 76.0; Aug 83.2; Sep 98.3; Oct 105.4; Nov 104.8; Dec 103.0
- SM-2231 (CP-N) unaccounted kWh per 2026 reading: 30 Jan 1069; 27 Feb 908; 31 Mar 910; 30 Apr 725; 29 May 594; 30 Jun 592; 31 Jul 599; 31 Aug 691; 30 Sep 791; 30 Oct 914; 30 Nov 1065; 31 Dec 1130 kWh
- SM-2232 (CP-S) unaccounted kWh per 2026 reading: 30 Jan 934; 27 Feb 798; 31 Mar 794; 30 Apr 633; 29 May 520; 30 Jun 517; 31 Jul 523; 31 Aug 606; 30 Sep 693; 30 Oct 799; 30 Nov 932; 31 Dec 990 kWh (31 Dec uses the later 09:52 read)
