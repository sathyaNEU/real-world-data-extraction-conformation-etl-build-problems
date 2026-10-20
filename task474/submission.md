## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: an ozone-season NOx inventory from continuous emissions monitor records whose gaps include hours without NOx control).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate seven of the nine combined-cycle units for the 2027 SCR Upgrade Program: AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1.**
Each emitted 0.170 lb of NOx per gross MWh or more over the 2026 ozone season once the hours its analyzers were out are filled by the emission state the unit was in. In the hours a plant lost its instrument air (most of them at Cutler Bend and Ashfork), the first measured hour after each loss reads about twenty times the unit's usual NOx per MMBtu and falls back over the next hour or two, so the SCR was not removing NOx while the air was out; those hours are filled at that first-hour NOx per MMBtu, times the hour's heat input; every other hour without a measurement is filled from the unit's measured hours at the same hour after a start or, later in a run, at the same load. Not a fill of every gap from the unit's measured hours in the same start state and load, nor the average of the hours either side of each gap: both put controlled NOx into uncontrolled hours and designate AF-2, CB-1, DF-1, DF-3 and SR-1, leaving CB-2 and AF-1 under the target.

## 2. Critical Components

1. Units at or above 0.170 lb per MWh: **7** of 9.
2. Season operating hours without a NOx measurement: **817**, of which **300** inside an instrument air ticket.

## 3. Step-by-Step Solution

1. Took the combined-cycle units from generating_unit_register_2026.xlsx (rule 2.1) and their operating hours (OP_TIME above zero) from 1 May to 30 September 2026 in dahs_hourly_export_2026.csv, standard time (rule 2.2), counting each unit's hours since its start along the whole year's record.
2. Marked as air-loss hours the operating hours with a blank NOX_MASS_LB inside a cems_maintenance_tickets_2026.csv ticket whose description names the plant instrument air or its compressor, the ticket's local times moved back an hour to standard time.
3. Filled every air-loss hour, its own run measured on its return or not, with its HEAT_INPUT_MMBTU times the unit's mean NOX_MASS_LB over HEAT_INPUT_MMBTU across the clock hours right after its runs of air-loss hours in which the unit was still operating and measured (a unit with none takes the same mean over its plant's units).
4. Filled every other blank hour: in hours 1 to 3 after a start with the mean NOX_MASS_LB of the unit's own measured hours at the same hour after a start (the units' start-up levels differ well beyond chance); later, from the unit's quadratic fit of NOX_MASS_LB on GLOAD_MW over its measured hours more than 3 hours after a start.
5. Divided each unit's measured and filled NOx by its GLOAD_MW summed over the same hours and designated every unit at or above 0.170 (rule 2.3): AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1.
6. Took each unit's ozone-season terms on local time from 1 May to 30 September 2026 (rule 3.2), the DAHS hours moved forward an hour, each event number in gads_event_report_2026.csv taken as one event at its latest-reported line: FOH, the hours inside a U1, U2 or U3 event, a later-filed full forced outage replacing an earlier one it overlaps on the unit, and the number of those outages; SH, OP_TIME summed; RSH, the hours outside a full outage less their OP_TIME; the starts, the operating hours that follow a hour without operation; EFDH, each D1 or D2 hour outside a full outage at derate_mw over the register's nameplate MW, of which EFDHRS falls in reserve shutdown (that share times one less OP_TIME).
7. Equivalent forced outage rate, in per cent: (FOH + EFDH) / (FOH + SH + EFDHRS). Demand rate, in per cent: (f FOH + fp EFDH) / (SH + f FOH), with f = (1/r + 1/T) / (1/r + 1/T + 1/D), r = FOH per forced outage, T = RSH per attempted start, D = SH per actual start (every start attempted succeeded), fp = SH / (SH + RSH).

## 4. Deliverable Answers

### cc_unit_nox_inventory_2026.xlsx

1. Every combined-cycle unit: designated or not, 2026 ozone-season equivalent forced outage rate and demand equivalent forced outage rate (per cent, one decimal):
   - AF-1: designated; equivalent forced outage rate 27.0%; demand equivalent forced outage rate 14.4%
   - AF-2: designated; equivalent forced outage rate 24.3%; demand equivalent forced outage rate 11.7%
   - CB-1: designated; equivalent forced outage rate 14.7%; demand equivalent forced outage rate 7.4%
   - CB-2: designated; equivalent forced outage rate 12.8%; demand equivalent forced outage rate 9.2%
   - DF-1: designated; equivalent forced outage rate 24.3%; demand equivalent forced outage rate 14.1%
   - DF-2: not designated; equivalent forced outage rate 32.8%; demand equivalent forced outage rate 19.3%
   - DF-3: designated; equivalent forced outage rate 19.0%; demand equivalent forced outage rate 8.6%
   - SR-1: designated; equivalent forced outage rate 14.7%; demand equivalent forced outage rate 8.1%
   - SR-2: not designated; equivalent forced outage rate 16.6%; demand equivalent forced outage rate 9.2%

### scr_upgrade_designations_2027.pdf

1. The designated units for the Board: AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1.
2. Bar chart of every combined-cycle unit's 2026 ozone-season NOx rate (lb per gross MWh) against the 0.170 target line, the designated units' bars in orange.
