# solver round: round 5, skeptic

**Proxy score 29.3 / 100** (recommendation 1.2 of 35, instruction 7.0 of 7, asks 21.1 of 58). Main call missed. 0 of 12 ask items cracked (80 per cent of tokens).

## Main call

golden: File 110 kW as the contracted demand for the first contract year, April 2027 to March 2028.

solver: File a first-year Contract Demand of 130 kW for the Civic Center decks' Schedule 26 service. That is the highest forecast monthly billing demand, 129 kW in December, rounded to the nearest 5 kW. The 129 kW comes from 2026 settled sessions re-simulated on the 32 new 11.5 kW units, using the vehicles registered at the January 2027 permit renewals and the FES-07 Rev 4 growth factor of 1.12. NSPL's planner sizing of 225 kW is 95 kW above it.

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
| deck_load_day.png | 2 | 1 | 3 | 33% |
| deck_load_day.png | 3 | 0 | 1 | 0% |
| deck_load_day.png | 4 | 1 | 2 | 50% |
| deck_load_day.png | 5 | 1 | 4 | 25% |
| civic_service_demand.xlsx | 1 | 24 | 35 | 69% |
| civic_service_demand.xlsx | 2 | 52 | 82 | 63% |

## Solver's path

1. Mapped settled_sessions to garages with station_register by session date, because old deck IDs 105085, 105097, 105108, 105227, 105240 and 105250 were reassigned to Ferry Terminal and Market Square later in 2025. This gave 29,720 deck rows (29,636 PERMIT and 84 FLEET).
2. Built the current session set: the latest ACCEPTED version from restatement_decisions_2025 (otherwise v1), then one row per auth_code, keeping the first delivered (16 rows re-delivered in Oct and Dec 2025). Stitched the 10:00 settlement splits (same station and payer, plug_out equal to the next plug_in) into 20,776 charges. Test: rebuilt every 2026 permit-month charge count and kWh in ev_permit_charging_statements_2026 (875 of 875 exact).
3. Assigned each permit the onboard charger rating (OBC) of its vehicle at the January 2027 renewal check (permit_vehicle_checks joined to vehicle_reference_list by make, model, trim and model-year range). Fleet cards took their city_fleet_roster vehicle.
4. Re-simulated each 2026 charge on the new 11.5 kW units: same kWh, starting at plug-in, at min(OBC, 11.5) kW, split into quarter-hours by deck.
5. Billing demand per Schedule 26 sec. 3: the highest quarter-hour starting 12:00 to 19:45 on weekdays, excluding the 2026 observed holidays. Applied the FES-07 2027 factor 1.12 (adopted 15 Sep 2026, in force when the Jan 2027 forecast is made) and rounded to whole kW. Monthly maximum is December, 129 kW (base 115.3 kW at 12:00 on 8 Dec 2026, North 74.0 and South 41.3). Contract demand to the nearest 5 kW is 130 kW.
6. NSPL sizing per Planning Guide 7.3: 32 x 11.5 = 368 kW, x 0.60 (21 to 40 units) = 220.8 kW, to the next 5 kW is 225 kW. Gap to 130 kW is 95 kW.
7. 2025 backtest. The 2024 base uses records as they stood after December 2024 closed (last v1 delivered 2025-01-20): v1 rows, so the 12 restatements received in March 2025 are left out. Added the gateway_b sessions (Jan to Apr 2024, local time, built at 6.6 kW) and 33 fleet-card deck charges missing from the settlement export (their times are UTC, which matched rows confirm). Factor 1.08 (in force in Jan 2025), rounded. Actual 2025 uses the current set plus 7 fleet-card-only charges from Jan to Mar 2025, rounded. Error = (forecast - actual) / actual, to one decimal.
8. Meter reconciliation. Meter reads are taken in Pacific Standard Time with DST disabled, so read times were converted to local time. Where a meter was read twice on 31 Dec, the later SM-2232 read stands (198,027.4), and the Corrections-sheet values were applied. Each residual is the register change less the quarter-hour session kWh through that panel in [previous read, read), less courtesy-session kWh. N-11 sessions from 1 Jun to 12 Jul 2026 (216.8 kWh) are excluded because N-11 was fed from HP-N. The residuals scale North/South at about 1.14, the ratio of the roof-lighting loads (2400/2100 VA).

confidence: Medium-high. The 2026 permit statements reproduce exactly, and the meter residuals track the lighting-load ratio. The main judgment call is using the January 2027 renewal vehicles. With the vehicles in use at session time instead, the peak would be 149 kW in February (filing 150 kW).

notes: The folder publishes no prior forecast table to test the backtest against. Its correctness rests on three choices: base records as they stood in January 2025 (v1, without the March 2025 restatements), factor 1.08, and including the fleet-card charges that are missing from the settlement export. In gateway_b, 13 sessions show 21,000 Wh, which looks like a capped register, but none falls on a peak day, so no billing demand moves.

### contract_demand_note.pdf (solver's answers)
- Contracted demand to file, first contract year: 130 kW (highest monthly forecast 129 kW rounded to the nearest 5 kW)
- Forecast billing demand per month of the contract year (Apr 2027 to Mar 2028, each built from the same 2026 month x 1.12, whole kW): Apr 90 kW; May 85 kW; Jun 79 kW; Jul 72 kW; Aug 75 kW; Sep 87 kW; Oct 94 kW; Nov 103 kW; Dec 129 kW; Jan 109 kW; Feb 68 kW; Mar 98 kW
- Month that sets the figure: December (December 2027, built from base day Tuesday 8 December 2026)
- kW each deck carries in the setting quarter-hour (12:00 to 12:15): North Deck 83 kW, South Deck 46 kW, total 129 kW forecast. Before the 1.12 factor these are 74 kW North and 41 kW South (74.0 and 41.3, total 115.3 kW)
- NSPL planners' proposed figure and the gap to ours: NSPL 225 kW (32 units x 11.5 kW = 368 kW x 0.60 diversity = 220.8 kW, taken to the next 5 kW above). Gap 95 kW above our 130 kW

### deck_load_day.png (solver's answers)
- Headline figure and day plotted: Contract demand line at 130 kW. Day plotted is Tuesday 8 December 2026, by quarter-hour
- Setting quarter-hour marked: 8 Dec 2026, 12:00 to 12:15. Forecast 129 kW (83 kW North, 46 kW South). On the old 6.6 kW pedestals the decks drew 132 kW in that quarter-hour (66 kW North, 66 kW South)
- Actual vs forecast shape: Old pedestals: daily peak 146 kW at 09:45, still 132 kW from 11:15 through 12:15, then falling to 0 by 15:00. Forecast on new pedestals x 1.12: peak 197 kW at 09:45 (outside the billing window), then 129 kW at 11:30 to 12:00 and 3 kW by 13:00. Suggested title: 'Decks need 130 kW: not everyone is charged by lunch, and the noon quarter-hour on 8 Dec sets 129 kW'

### civic_service_demand.xlsx (solver's answers)
- 2025 backtest: FES-07 forecast from 2024 (factor 1.08), recorded actual, and error % of actual: Jan forecast 112 vs actual 113, -0.9%; Feb 122 vs 120, +1.7%; Mar 105 vs 107, -1.9%; Apr 102 vs 101, +1.0%; May 102 vs 103, -1.0%; Jun 83 vs 81, +2.5%; Jul 83 vs 84, -1.2%; Aug 82 vs 81, +1.2%; Sep 107 vs 109, -1.8%; Oct 114 vs 112, +1.8%; Nov 121 vs 119, +1.7%; Dec 114 vs 115, -0.9%
- SM-2231 (CP-N, North) unaccounted kWh per 2026 reading: 30 Jan 1069; 27 Feb 908; 31 Mar 910; 30 Apr 725; 29 May 594; 30 Jun 592; 31 Jul 599; 31 Aug 691; 30 Sep 791; 30 Oct 914; 30 Nov 1063; 31 Dec 1133 kWh
- SM-2232 (CP-S, South) unaccounted kWh per 2026 reading: 30 Jan 934; 27 Feb 799; 31 Mar 794; 30 Apr 633; 29 May 520; 30 Jun 517; 31 Jul 523; 31 Aug 606; 30 Sep 693; 30 Oct 799; 30 Nov 932; 31 Dec 990 kWh
