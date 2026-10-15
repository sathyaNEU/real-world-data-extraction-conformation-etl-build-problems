## Tags

**Domain:** General Statistics & Data Science, Bayesian modeling and posterior inference (the posterior predictive for the members of new groups: the chance that the weakest of a Model K pack's three cells, taken from one new formation tray, falls below the warranty line).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Reserve 400 of lot ZC2638's 7,200 Model K packs at Friday's release.**
The expected number of packs below 80 per cent of rated capacity within 600 cycles is 398.9 (5.5 per cent), because most of RL-3's error is a formation tray's, which the three tray-mates of a pack share. Not 500 (514 packs), the release-test cells' chance of 2.4 per cent compounded over three independent cells, which counts a tray's shared shortfall as three separate ones. Not about 150, the finished lots' own tray-mate packs as they lived, whose cells outlived this lot's.

## 2. Critical Components

1. RL-3's error on the finished lots is mostly the formation tray's: standard deviation **0.160** shared by a tray's cells and **0.086** each cell's own, **78** per cent of the variance at the tray
2. The pack line builds from tray-mates: **7,063** of the 7,200 packs are three cells from one formation tray
3. A pack's chance of falling below 80 per cent of rated capacity within 600 cycles is **5.5** per cent, **398.9** packs expected

## 3. Step-by-Step Solution

1. Stacked qp3_first100_cycles_fleet_a.csv (cycle 0 is the protocol's first) and qp3_first100_cycles_fleet_b.csv (a row repeated by overlapping pulls taken once), stitched each continued test after the first in time order and computed F1 and F2 as qm07_release_model_rl3_zp4820.pdf section 3 defines them: RL-3 predicts every one of lot ZC2638's 120 release-test cells to outlive 600 cycles.
2. Took RL-3's error, the log of each EOL cell's cycles in qp3_life_monitoring_results.csv less its predicted log life, for the 2,373 cells of the twenty finished lots and split it by formation tray within lot (qp3_release_register.csv): standard deviation 0.160 shared by a tray's cells and 0.086 each cell's own, 78 per cent at the tray, while the release test's own predictions carry 2 per cent at the tray.
3. Joined model_k_genealogy_zc2638.csv to the formation trays of zelvora_cell_data_zc2638.csv: 7,063 packs are three tray-mates, 136 take two cells from one tray and one from another, and one pack takes a cell from each of three trays.
4. Gave each pack the chance that any of its cells falls below 80 per cent within 600 cycles (model_k_pack_specification_rev_d.pdf section 4, the weakest cell), averaged over a new tray's shared error and the release-test cells' predicted lives, and summed it over the lot's packs (fin_rs04_battery_warranty_reserve_policy.pdf clauses 2.2, 3.2 and 3.3): 5.5 per cent a pack, 398.9 packs.
5. Rounded to the nearest 50 packs (clause 3.4): 400 packs.
6. Took the partners' capacity replacements under the warranty (service_cases_2024-09_2026-09.csv: CAP, WTY, REPLACED) in the service period of the invoice line billing each, October 2025 to September 2026, Tolley Marsh Repair's March invoice as reissued (TM-2603-R1), and costed each at its invoice line in euros at treasury_month_end_rates_2025-2026.csv for that period, its battery's share of its consignment's charge in carrier_statement_inbound_returns_2025-09_2026-10.csv (the consignment from depot_returns_log_2024-09_2026-09.xlsx; none for a battery scrapped where it was removed, as extract_note_service_operations_2026-10-09.txt files it) and the service pack's standard cost in service_cost_sheet_fy2026.xlsx.
7. Counted each month's capacity replacements under the warranty: the DACH depot's by Techn. Abschluss in depot_service_orders_2024-09_2026-03.xlsx and by closing day in the case system from 2 March 2026 (an order completed in SAP counted once), the partners' by invoice service period: 488 in the twelve months.
8. Reserve 400 packs.

## 4. Deliverable Answers

### z2638_warranty_reserve.xlsx

1. The reserve: 400 packs.
2. Each repair partner's capacity replacements under the warranty carried out from October 2025 to September 2026 and what one cost on average, to the nearest euro:
   - Dauvergne Réparation (FRB): 99 replacements, 99 euros
   - Tolley Marsh Repair (UKI): 81 replacements, 102 euros
   - Ljungqvist Service (NOR): 58 replacements, 112 euros
   - Ferrucci Assistenza (SOU): 79 replacements, 96 euros
3. Capacity replacements under the warranty carried out in each month, all five service regions:
   - October 2025: 8
   - November 2025: 17
   - December 2025: 23
   - January 2026: 25
   - February 2026: 26
   - March 2026: 39
   - April 2026: 41
   - May 2026: 51
   - June 2026: 57
   - July 2026: 56
   - August 2026: 74
   - September 2026: 71

### z2638_reserve_note.docx

1. Opens with the reserve: book a reserve of 400 packs for the 7,200 Model K packs built from lot ZC2638.
2. Stacked bar chart of the twelve months' capacity replacements under the warranty, one bar per month from October 2025 to September 2026 split into the five service regions, each bar labelled with its total.
