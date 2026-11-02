## Tags

**Domain:** General Statistics & Data Science, regression and classification model diagnostics (a resource model's estimates against grade control at the selection cut-off).
**Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Budget 150,000 ounces of gold for the ore Kessock Lake mines in 2027 at the 0.90 g/t cut-off.** Grade control will keep about 2.8 Mt at 1.7 g/t from the 2027 schedule, because its block grades spread more widely than the resource model's and a 0.90 g/t cut on them keeps more gold than the model's own curve shows. Not the plan's 126,200 oz on the model's estimates, and not that figure times the reconciliation reports' 1.02, a factor measured on ore cut at 0.50 g/t.

## 2. Critical Components

1. The plan's Schedule at 0.90 g/t on the resource model holds **2.7 Mt at 1.45 g/t, 126,200 oz**.
2. Over January 2023 to October 2026, grade control's gold over the model's is **1.02** with both sides cut at 0.50 g/t and **about 1.2** with both cut at 0.90 g/t.
3. The 2027 ore on grade control is **2.8 Mt at 1.7 g/t**.

## 3. Step-by-Step Solution

1. Moved every primary blast-hole assay in gc_assays_lims_export_20261105.csv from UTM to the mine grid with kessock_mine_grid_control.txt, read below-detection results at half the limit and over-range results from AU_GRAV_GPT, and averaged each block's holes per the budget basis memo: 21,616 blocks pair with kl_mz_resource_model_2026R.csv.
2. Re-cut the paired record at 0.90 g/t on both sides: grade control holds about 1.2 times the model's gold there, against 1.02 at the reconciliation reports' 0.50 g/t.
3. Took each block on the Schedule sheet of kessock_mine_plan_2027_v3.xlsx through every grade-control-to-model ratio in the record and kept the gold where grade control reads 0.90 g/t or more: 2.8 Mt at 1.7 g/t, 150,000 oz to the nearest 10,000.
4. Added each haul in dispatch_loads_to_lgsp_2023-2026.csv, its time moved from UTC to local, at the nominal payload of the truck that carried that number on the haul's date (haul_fleet_register_2026-10.xlsx, Fleet and Disposals sheets), counted a truck's second record from the same source within ten minutes once, and started from the 2022 year-end balance in stockpile_inventory_2022-12-31.csv.
5. Rebuilt the ball mill's run state from both of its tags in dcs_event_export_grinding_2025-2026.csv (UTC to local) and counted every shutdown in cmms_work_orders_grinding_2025-2026.csv as down, including the shutdowns the historian did not store.
6. Shared each lot's fine gold in refinery_outturn_statements_2025-2026.csv among the bars on its lines by their gross weights in goldroom_bar_register_2025-2026.csv (a bar melted as two lots takes both) and summed by pour date.
7. Budget gold for 2027 is 150,000 oz.

## 4. Deliverable Answers

### kessock_2027_budget_gold.xlsx

1. Gold in the ore mined in 2027: 150,000 oz.
2. Grade of that ore: 1.7 g/t.
3. Low-grade stockpile, tonnes and contained gold:
   - 31 December 2023: 3,629,000 t, 45,500 oz
   - 31 December 2024: 5,417,000 t, 68,200 oz
   - 31 December 2025: 7,196,000 t, 90,700 oz
   - 31 October 2026: 8,802,000 t, 110,900 oz
4. Hours the ball mill ran, by quarter (local time):
   - 2025 Q1: 2,044 hours
   - 2025 Q2: 2,094 hours
   - 2025 Q3: 2,080 hours
   - 2025 Q4: 2,131 hours
   - 2026 Q1: 2,042 hours
   - 2026 Q2: 2,086 hours
   - 2026 Q3: 2,070 hours
5. Fine gold in the bars poured, by quarter (local time):
   - 2025 Q1: 24,600 oz
   - 2025 Q2: 26,300 oz
   - 2025 Q3: 29,600 oz
   - 2025 Q4: 28,900 oz
   - 2026 Q1: 30,300 oz
   - 2026 Q2: 27,900 oz
   - 2026 Q3: 29,400 oz

### lg_stockpile_2023-2026.svg

1. Bar chart of the low-grade stockpile's tonnes at the four dates, each bar labelled with its tonnes and contained gold.
