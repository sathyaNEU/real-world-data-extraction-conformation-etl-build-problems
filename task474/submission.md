## Tags

**Domain:** Physical & Environmental Sciences (emissions inventory: an ozone-season NOx inventory from continuous emissions monitor records with gaps).
**Analytical objective:** Data Extraction & Conformation (ETL).

## 1. Final Recommendation

**Designate seven of the nine combined-cycle units for the 2027 SCR Upgrade Program: AF-1, AF-2, CB-1, DF-1, DF-3, SR-1 and SR-2.**
Each emitted 0.170 lb of NOx per gross MWh or more over the 2026 ozone season once every hour without a NOx measurement is filled from the same unit's measured hours at the same number of hours after its start. Not a fill from each unit's NOx at the same load, nor the measured hours alone: the analyzers were out mostly in the first hours after a start, when the cold catalyst lets NOx run several times its steady level, so those routes put steady-state NOx into start-up hours and leave the units that cycle hardest under the target.

## 2. Critical Components

1. Units at or above 0.170 lb per MWh: **7** of 9.
2. Season operating hours without a NOx measurement: **542**, of which **405** in the first three hours after a start.

## 3. Step-by-Step Solution

1. Took the combined-cycle units from generating_unit_register_2026.xlsx (rule 2.1) and their operating hours (OP_TIME above zero) from 1 May to 30 September 2026 in dahs_hourly_export_2026.csv, standard time (rule 2.2).
2. Counted each unit's hours since its start along the whole year's record (the first operating hour after an offline hour is hour 1).
3. Filled each operating hour with a blank NOX_MASS_LB: in hours 1 to 3 after a start, with the mean NOX_MASS_LB of the unit's measured hours at the same hour after a start; later, from the unit's quadratic fit of NOX_MASS_LB on GLOAD_MW over its measured hours more than 3 hours after a start.
4. Divided each unit's measured and filled NOx by its GLOAD_MW summed over the same hours and designated every unit at or above 0.170 (rule 2.3): AF-1, AF-2, CB-1, DF-1, DF-3, SR-1 and SR-2.
5. Priced each operating hour's HEAT_INPUT_MMBTU at the gas_supply_daily_invoices_2026.csv price for the gas day it falls in, the hour moved from standard time to Central clock time and then back 9 hours (gas_supply_agreement_excerpt.pdf, Section 1; rule 3.1); a gas day with no invoice line at a delivery point (one month at each) priced at another point's price that day plus the constant difference between the two points' prices (Section 6, a common Daily Index plus each point's adder): $32,743,316 in all.
6. Counted the hours from 1 May to 30 September 2026 in which gads_event_report_2026.csv shows the unit in a U1, U2 or U3 event, where two full outages on one unit overlap keeping the later-reported one (rule 3.2): 1,276 hours in all.

## 4. Deliverable Answers

### cc_unit_nox_inventory_2026.xlsx

1. Every combined-cycle unit: designated or not, 2026 ozone-season fuel cost (nearest dollar), forced outage hours:
   - AF-1: designated; $3,584,023; 61 forced outage hours
   - AF-2: designated; $3,151,161; 179 forced outage hours
   - CB-1: designated; $2,643,651; 89 forced outage hours
   - CB-2: not designated; $4,459,104; 192 forced outage hours
   - DF-1: designated; $4,313,387; 65 forced outage hours
   - DF-2: not designated; $3,686,805; 258 forced outage hours
   - DF-3: designated; $3,324,141; 164 forced outage hours
   - SR-1: designated; $3,782,581; 164 forced outage hours
   - SR-2: designated; $3,798,463; 104 forced outage hours

### scr_upgrade_designations_2027.pdf

1. The designated units for the Board: AF-1, AF-2, CB-1, DF-1, DF-3, SR-1 and SR-2.
2. Bar chart of every combined-cycle unit's 2026 ozone-season NOx rate (lb per gross MWh) against the 0.170 target line, the designated units' bars in orange.
