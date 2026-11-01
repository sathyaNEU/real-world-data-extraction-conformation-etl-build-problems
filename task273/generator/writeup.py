"""Writes submission.md from figures.json, so every figure in blocks 1 to 4 is one the generator computed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MON = ["December", "January", "February", "March"]
QL = ["Jul-Sep 2025", "Oct-Dec 2025", "Jan-Mar 2026", "Apr-Jun 2026"]
BORES = ["PB%d" % k for k in range(1, 9)]


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    lv, mol, dd = f["lowest_level_m_bmp"], f["min_operating_level_m_bmp"], f["pb9_drawdown_on_neighbour_m"]
    fail = f["call"]["failing"]
    assert fail == ["PB3 February", "PB3 March"]
    L = []
    a = L.append
    a("## Tags\n")
    a("**Domain:** Energy Systems & Utilities (asset condition and maintenance: a dairy processing site's production "
      "bores, the lowest level each reaches through the design drought on the summer bore plan).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    a("## 1. Final Recommendation\n")
    a("**Do not adopt the 2026-27 summer bore plan as drafted: it fails the drought test at PB3, whose lowest pumping "
      "water level reaches %.1f m below measuring point in February and in March against a minimum operating level "
      "of %.1f m.** PB9's October 2026 constant-rate test drew PB3 down by %.1f m (to the nearest half metre) at the plan's %.2f ML/d. Not the "
      "plan holding: each bore's own drought curve leaves out PB9's draw on its neighbours. Not PB4 failing: PB4 "
      "sits nearer PB9 on the map, but the test moved it %.1f m."
      % (lv["PB3 February"], mol["PB3"], dd["PB3"], f["pb9_take_ml_d"], dd["PB4"]))
    a("")
    a("## 2. Critical Components\n")
    a("1. At its planned %.2f ML/d PB9 lowers PB3 by **%.1f m** and PB4 by **%.1f m** (to the nearest half metre), the dip its 7 to 14 October "
      "2026 constant-rate test left in their daily levels." % (f["pb9_take_ml_d"], dd["PB3"], dd["PB4"]))
    a("2. PB3's lowest level is **%.1f m** below measuring point in February and **%.1f m** in March, against its "
      "minimum operating level of %.1f m." % (lv["PB3 February"], lv["PB3 March"], mol["PB3"]))
    a("3. Every other bore, PB9 included, stays above its minimum operating level in every month.\n")
    a("## 3. Step-by-Step Solution\n")
    a("1. Conformed kaitanga_bores_daily_2014-2026.csv: mapped the KTG-BH tags used before 14 May 2019 to PB1 to PB8, "
      "dropped the August 2021 batch the gateway sent twice, and turned each level into a reduced level with the "
      "bore register's ground level and measuring-point height.")
    a("2. Moved PB9_logger_LT5-2408817_2026-10.csv from UTC to NZDT, summed its discharge into each local day's take, and "
      "took PB9's own drawdown and static level from the last day of the constant-rate stage and the hours before "
      "the step test.")
    a("3. Fitted each existing bore's level less MB1's level (MRC_MB1_groundwater_level_daily.csv) on every bore's "
      "daily take, PB9's test days included, by least squares over 2014 to 2026; PB9's coefficient on each bore is "
      "its drawdown there per ML/d.")
    a("4. Took MB1's lowest level in each month from December 2019 to March 2020 (SWS-03 section 3) and each bore's "
      "planned take from kaitanga_summer_bore_plan_2026-27.xlsx, and computed each bore's lowest pumping water level "
      "by month, PB9's from its test with its neighbours' takes carried by reciprocity.")
    a("5. Compared each with the register's minimum operating level (SWS-03 section 4): PB3 fails in February and "
      "March, and nothing else fails.")
    a("6. For the permit meters, differenced each meter's 15-minute totaliser in MRC_permit_meter_telemetry_2025-26."
      "csv across its rollovers, moved NZST to NZ local time, and gave each meter to the bore whose SCADA daily take "
      "it tracks: WM-30455 reads PB2, WM-30456 PB1, WM-33119 PB6, WM-33120 PB5, and WM-40958 is PB4's meter from 17 "
      "February 2026.")
    a("7. For electricity, moved pump_icp_interval_data_2025-26.csv from UTC to NZ local time, read the PB2 meter "
      "fitted on 11 February 2026 at x%d (kaitanga_icp_meter_register.csv), split switchboards SB-3 and SB-4 between "
      "their pumps by daily run hours times motor kW, and divided by the metered megalitres."
      % f["constants"]["pb2_ct_multiplier"])
    a("8. Recommended not adopting the plan as drafted: PB3 fails the drought test in February and March.\n")
    a("## 4. Deliverable Answers\n")
    a("### kaitanga_summer_test_2026-27.xlsx\n")
    a("1. Result: the plan fails the drought test; PB3 falls below its minimum operating level in February and "
      "March.")
    a("2. Lowest pumping water level by month, metres below measuring point, nearest 0.5 m:")
    for b in BORES:
        a("   - %s: %s" % (b, ", ".join("%s %.1f" % (m, lv["%s %s" % (b, m)]) for m in MON)))
    a("3. PB9 holds in every month.")
    a("4. Pump electricity per megalitre the permit meters measured, whole kWh/ML:")
    for b in BORES:
        a("   - %s: %s" % (b, ", ".join("%s %d" % (QL[q], f["energy_kwh_per_ml"]["%s Q%d" % (b, q + 1)])
                                       for q in range(4))))
    a("5. Volume by bore as the permit meters measured it, whole ML:")
    for b in BORES:
        a("   - %s: %s" % (b, ", ".join("%s %d" % (QL[q], f["permit_meter_ml"]["%s Q%d" % (b, q + 1)])
                                       for q in range(4))))
    a("")
    a("### borefield_plan_2026-27.pptx\n")
    a("1. Call: do not adopt the plan as drafted; PB3 falls below its minimum operating level in February and March.")
    a("2. Chart on slide 1: each bore's margin over its minimum operating level by month, PB3 below zero in February "
      "and March.")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
