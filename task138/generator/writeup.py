"""Writes submission.md from figures.json, so every figure in blocks 1 to 4 is one the generator computed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def c(v):
    return "{:,}".format(int(v))


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    call, k = f["call"], f["constants"]
    yrs = [str(y) for y in range(k["first_year"], k["last_year"] + 1)]
    tr = [call[y]["transfer_mw"] for y in yrs]
    pk = [call[y]["planning_peak_mw"] for y in yrs]
    assert tr == [1.0, 2.0, 3.0, 4.0, 5.0] and pk == [105, 106, 107, 108, 109]
    rel = f["relief_pct"]
    r1, r2 = f["rungs_transfer_mw"]["R1_all_hours"], f["rungs_transfer_mw"]["R2_daily_peak_hour"]
    bands = f["bands"]
    L = []
    a = L.append
    a("## Tags\n")
    a("**Domain:** Energy Systems & Utilities (load forecasting: a distribution substation's summer planning peak "
      "once conservation voltage reduction runs on every feeder).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    a("## 1. Final Recommendation\n")
    a("**Breckwater must transfer %.1f MW off Dunraith in summer %s, %.1f MW in %s, %.1f MW in %s, %.1f MW in %s "
      "and %.1f MW in %s.** With the voltage cut taking %.1f per cent off at the planning peak, the planning peaks "
      "are %s MW against the firm rating. Not the pilot's relief over every hour (%.1f per cent, %s MW in "
      "%s), which carries the night's voltage-sensitive load into the peak; not the relief at each day's peak hour "
      "(%.1f per cent, %.1f MW in %s), which carries mild days whose peak holds less air conditioning."
      % (tr[0], yrs[0], tr[1], yrs[1], tr[2], yrs[2], tr[3], yrs[3], tr[4], yrs[4], rel["golden"],
         ", ".join(str(p) for p in pk[:-1]) + " and %d" % pk[-1], rel["all_hours"],
         "%.1f" % r1[0], yrs[0], rel["daily_peak_hour"], r2[0], yrs[0]))
    a("")
    a("## 2. Critical Components\n")
    a("1. The weather-normal peak (criteria 3.2) is **%.1f MW** at the 2024 level, **%.1f MW** in %s before the "
      "voltage cut." % (f["weather_normal_2024_mw"], f["weather_normal_mw"][yrs[0]], yrs[0]))
    a("2. The %.1f per cent voltage cut takes **%.1f per cent** off the load at the planning peak (**%.2f MW** in "
      "%s), read from the 2025 pilot's hours beginning 16:00 to 20:00 on days at %d F or more."
      % (k["voltage_cut_pct"], rel["golden"], f["relief_mw"][yrs[0]], yrs[0], k["hot_f"]))
    a("3. The planning peaks for %s to %s are **%s MW**." % (yrs[0], yrs[-1], ", ".join(str(p) for p in pk[:-1]) +
                                                          " and %d" % pk[-1]))
    a("")
    a("## 3. Step-by-Step Solution\n")
    a("1. Joined DUNRAITH_FDR_KW_2022-2023.csv (kW, each hour labelled at its end) to "
      "dunraith_feeder_mw_2024-2026.csv (MW, labelled at its start; Bad hours left out per criteria 5) and took "
      "each day's highest hourly sum of the feeders.")
    a("2. Took each local day's maximum from mossford_ap_obs_2022-2026.csv (DATE_LST, local standard time, an hour "
      "behind the historian's daylight time; DRY_BULB_C in Celsius) and fitted criteria "
      "3.2's line over the %d days at %d F or more: %.2f MW per F, %.1f MW at %d F, carried from 2024 at the "
      "BEC_load_forecast_2025.xlsx base case, %.2f per cent a year compounded: %.1f MW in %s."
      % (f["days_in_fit"], k["threshold_f"], f["slope_mw_per_f"], f["weather_normal_2024_mw"], k["design_f"],
         k["growth_pct"], f["weather_normal_mw"][yrs[0]], yrs[0]))
    a("3. Rebuilt each hour's setting from VR_event_log_DUN_2025.csv and compared the ratio of DUN-2, DUN-5 and "
      "DUN-7 to the other feeders in CVR hours and normal hours, over the hours beginning 16:00 to 20:00: the relief "
      "falls from %.1f per cent on days under %d F to %.1f per cent on days at %d F or more (%d CVR and %d normal "
      "hours), the conditions of the planning peak."
      % (bands[0]["relief_pct"], bands[0]["to_f"], rel["golden"], k["hot_f"], f["hot_hours"]["on"],
         f["hot_hours"]["off"]))
    a("4. Took %.1f per cent off each summer's weather-normal peak for the 2027 operating plan's CVR on every "
      "feeder (criteria 3.3): planning peaks %s MW." % (rel["golden"], ", ".join(str(p) for p in pk)))
    a("5. Rounded each planning peak's excess over the %.1f MW firm rating up to whole %.1f MW switching blocks "
      "(criteria 4.1): %s MW." % (k["firm_mw"], k["block_mw"], ", ".join("%.1f" % t for t in tr)))
    ea = f["feeder_energy_mwh"]
    a("6. Ask A: multiplied each day's KWH in mdms_xfmr_daily_kwh_20260601_20260930.csv by METER_MULT in "
      "DUN_transformer_register_2026-10.xlsx from the transformer's METER_SET date and by 1 before it (the three "
      "multiplier-20 meters set in June 2026 read about twenty times their later daily KWH before that date), and "
      "counted 1 to 30 June on the old feeder for every transformer whose PROTECTIVE_DEVICE lies below S-4471, "
      "S-6120 or S-1302 in the register's Devices sheet (SO-2026-114_Dunraith.pdf: carried on the new feeders from "
      "00:00 on 1 July): %s MWh." % ", ".join("%s %s" % (x, c(v)) for x, v in ea.items()))
    hd = f["hot_days"]
    a("7. Ask B: summed recorders 41-2207 and 41-2208 of MV90_DP0417_202606-202609.csv (the transformers' %.1f kV "
      "side in WPC_Exhibit_A_delivery_points.pdf, not the %d kV line terminal 41-2391), moved 41-2208's stamps "
      "from its repeated stamp of 9 June onward 15 minutes later (only then do the two recorders' hourly energy tie "
      "to the historian's feeder total), put the UTC interval ends on CDT and took each of the ten hottest local "
      "days' highest 15-minute demand: %s MW."
      % (f["ids"]["low_side_kv"], f["ids"]["line_kv"],
         ", ".join("%s %.1f" % (d, v["peak_mw"]) for d, v in sorted(hd.items()))))
    a("8. Transfer %s MW off Dunraith in the summers %s to %s." % (", ".join("%.1f" % t for t in tr), yrs[0],
                                                                   yrs[-1]))
    a("")
    a("## 4. Deliverable Answers\n")
    a("### dunraith_planning.xlsx\n")
    a("1. Transfer requirement by summer, MW:")
    for y, t in zip(yrs, tr):
        a("   - %s: %.1f" % (y, t))
    a("2. Planning peak by summer, MW to the nearest MW:")
    for y, p in zip(yrs, pk):
        a("   - %s: %d" % (y, p))
    a("3. Energy each feeder delivered to members' meters, June to September 2026, MWh to the nearest 10:")
    for x, v in ea.items():
        a("   - %s: %s" % (x, c(v)))
    a("4. Peak 15-minute demand of the feeders on the ten hottest days of summer 2026, MW to one decimal:")
    for d, v in sorted(hd.items()):
        a("   - %s: %.1f" % (d, v["peak_mw"]))
    a("5. Chart sheet: the planning peak for each summer from %s to %s in columns against the firm rating line, "
      "with the weather-normal peak before the voltage cut as a dashed line." % (yrs[0], yrs[-1]))
    text = "\n".join(L) + "\n"
    assert "—" not in text
    open(os.path.join(TASK, "submission.md"), "w").write(text)


if __name__ == "__main__":
    main()
