## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: an ozone-season NOx inventory from continuous emissions monitor records whose gaps include hours without NOx control).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate seven of the nine combined-cycle units for the 2027 SCR Upgrade Program: AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1.**
Each emitted 0.170 lb of NOx per gross MWh or more over the 2026 ozone season once the hours its analyzers were out are filled by the control state the unit was in. In the hours a plant lost its instrument air (most of them at Cutler Bend and Ashfork), the SCR's air-operated ammonia flow was down with the analyzers' dilution probes, so those hours are filled at the NOx per MMBtu the analyzer measured in the first hour after each loss, times the hour's heat input; every other hour without a measurement is filled from the unit's measured hours at the same hour after a start or, later in a run, at the same load. Not a fill of every gap from the unit's measured hours in the same start state and load, nor the average of the hours either side of each gap: both put controlled NOx into uncontrolled hours and designate AF-2, CB-1, DF-1, DF-3 and SR-1, leaving CB-2 and AF-1 under the target.

## 2. Critical Components

1. Units at or above 0.170 lb per MWh: **7** of 9.
2. Season operating hours without a NOx measurement: **817**, of which **300** inside an instrument air ticket.

## 3. Step-by-Step Solution

1. Took the combined-cycle units from generating_unit_register_2026.xlsx (rule 2.1) and their operating hours (OP_TIME above zero) from 1 May to 30 September 2026 in dahs_hourly_export_2026.csv, standard time (rule 2.2), counting each unit's hours since its start along the whole year's record.
2. Marked as air-loss hours the operating hours with a blank NOX_MASS_LB inside a cems_maintenance_tickets_2026.csv ticket whose description names the plant instrument air or its compressor, the ticket's local times moved back an hour to standard time.
3. Filled each air-loss hour with its HEAT_INPUT_MMBTU times the unit's mean NOX_MASS_LB over HEAT_INPUT_MMBTU in the clock hour right after each run of air-loss hours, where the unit was still operating and that hour was measured (a unit with none takes the same mean over its plant's units).
4. Filled every other blank hour: in hours 1 to 3 after a start with the mean NOX_MASS_LB of the unit's measured hours at the same hour after a start; later, from the unit's quadratic fit of NOX_MASS_LB on GLOAD_MW over its measured hours more than 3 hours after a start.
5. Divided each unit's measured and filled NOx by its GLOAD_MW summed over the same hours and designated every unit at or above 0.170 (rule 2.3): AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1.
6. Priced each operating hour's HEAT_INPUT_MMBTU at the gas_supply_daily_invoices_2026.csv price for the gas day it falls in, the hour moved from standard time to Central clock time and then back 9 hours (gas_supply_agreement_excerpt.pdf, Section 1; rule 3.1); a gas day with no invoice line of its own at the delivery point takes the price on the point's next line, whose quantity is the burn of every gas day since the point's previous line (weekend and holiday gas, traded together): $35,180,600 in all.
7. Counted the hours from 1 May to 30 September 2026 in which gads_event_report_2026.csv shows the unit in a U1, U2 or U3 event (rule 3.2), the later-filed report standing where two reports are the same outage: two full outages overlapping on one unit, or one repeating another's event type, cause, length and clock hours under other dates (rule 3.2): 2,096 hours in all.

## 4. Deliverable Answers

### cc_unit_nox_inventory_2026.xlsx

1. Every combined-cycle unit: designated or not, 2026 ozone-season fuel cost (nearest hundred dollars), forced outage hours:
   - AF-1: designated; $3,843,200; 349 forced outage hours
   - AF-2: designated; $3,278,600; 221 forced outage hours
   - CB-1: designated; $2,891,500; 117 forced outage hours
   - CB-2: designated; $4,678,200; 100 forced outage hours
   - DF-1: designated; $4,658,300; 198 forced outage hours
   - DF-2: not designated; $3,936,200; 522 forced outage hours
   - DF-3: designated; $3,651,100; 265 forced outage hours
   - SR-1: designated; $4,159,600; 100 forced outage hours
   - SR-2: not designated; $4,083,900; 224 forced outage hours

### scr_upgrade_designations_2027.pdf

1. The designated units for the Board: AF-1, AF-2, CB-1, CB-2, DF-1, DF-3 and SR-1.
2. Bar chart of every combined-cycle unit's 2026 ozone-season NOx rate (lb per gross MWh) against the 0.170 target line, the designated units' bars in orange.
