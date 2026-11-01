"""Writes submission.md from figures.json, so every figure in blocks 1 to 4 is one the generator computed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REACH = {"R1": "north tie-in to Pump Station 1", "R2": "Riverside Park",
         "R3": "Front Street to the Main Street closure", "R4": "Main Street closure to Cedar Street",
         "R5": "Cedar Street to the railroad closure", "R6": "railroad closure to the grain terminal",
         "R7": "grain terminal to Pump Station 2", "R8": "Pump Station 2 to the south tie-in"}


def c(v):
    return "{:,}".format(int(v))


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    call, aep, st, ld = f["call"], f["aep_pct_by_raise"], f["settlement_ft"], f["lead_time_h"]
    k, r1k = f["constants"], f["rungs_1k"]
    w, hg, fb = f["warning"], f["halbrook_gauge"], f["freeboard"]
    assert call["raise_ft"] == 2 and call["design_discharge_cfs"] == 110000
    L = []
    a = L.append
    a("## Tags\n")
    a("**Domain:** Physical & Environmental Sciences (hydrology and flood frequency: the 1 per cent annual chance "
      "flood at a gauged river town and the levee crown raise it calls for).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    a("## 1. Final Recommendation\n")
    a("**Raise the Orrinsford levee crown by %d ft before the 2027 flood season.** The design flood for the river as "
      "it now runs is %s cfs at the Orrinsford gauge and the railroad closure is %.2f ft short of it with freeboard; "
      "a 1 ft raise leaves a %.1f per cent annual chance of exceeding what the levee holds, %d ft brings it to %.1f "
      "per cent. Not no raise: the fit to the published Orrinsford record (%s cfs) keeps floods the upstream "
      "floodplains cut before their levees were raised. Not 1 ft: the %d water years since the last raise alone "
      "(%s cfs) set aside Coyle Bridge's %d earlier years."
      % (call["raise_ft"], c(call["design_discharge_cfs"]), f["shortfall_118_70_ft"], aep["1 ft"], call["raise_ft"],
         aep["2 ft"], c(r1k["R0_at_site"]), f["post_raise_years"], c(r1k["R2_post_raise_only"]),
         f["pre_raise_years"]))
    a("")
    a("## 2. Critical Components\n")
    a("1. Every levee between Coyle Bridge and Orrinsford was raised by October 2008, so water year **%d** is the "
      "first of the river as it now runs." % f["first_fully_raised_wy"])
    a("2. The present river's 1 per cent annual chance discharge at Orrinsford is **%s cfs**." %
      c(call["design_discharge_cfs"]))
    a("3. Against it the railroad closure's crown is **%.2f ft** short of the design water surface plus freeboard."
      % f["shortfall_118_70_ft"])
    a("")
    a("## 3. Step-by-Step Solution\n")
    a("1. From the Segments and Gauges sheets of DNR_levee_inventory_Tamsen_2025.xlsx, took the six segments "
      "between river miles %.1f and %.1f: their crown raises, the last in October 2008, were all in force from "
      "water year %d." % (f["river_miles"]["coyle"], f["river_miles"]["halbrook"], f["first_fully_raised_wy"]))
    a("2. Read each water year's annual peak at Orrinsford and Coyle Bridge from "
      "SWS_annual_peaks_Tamsen_basin_2026-10-28.csv (an October to December peak counts in the next water year) and "
      "fitted Orrinsford on Coyle Bridge through the origin over water years %d to 2026: %.3f; before %d the great "
      "floods sit well below it (1970: %s against %s cfs)."
      % (f["first_fully_raised_wy"], f["present_relation"], f["first_fully_raised_wy"], c(k["halbrook_1970"]),
         c(k["coyle_1970"])))
    a("3. Took Orrinsford's peaks from %d and Coyle Bridge's times %.3f before, and fitted LS-02's log-Pearson "
      "Type III by moments with the station skew weighted with the SW-16-03 region 2 skew (%.2f, mean square error "
      "%.2f): the 1 per cent discharge is %s cfs, %s to the nearest 5,000."
      % (f["first_fully_raised_wy"], f["present_relation"], k["regional_skew"], f["regional_skew_mse"],
         c(round(f["design_discharge_raw"])), c(call["design_discharge_cfs"])))
    a("4. Read HWE-1907_hydraulic_update_2019_Table4.pdf linearly in discharge, added LS-02 freeboard (%.1f ft, "
      "%.1f ft within %d ft of a bridge, plus the upstream allowance) and set it against the 2024 crown in the "
      "inventory's Orrinsford crown sheet: the railroad closure is %.2f ft short, so the smallest whole-foot raise "
      "is %d ft." % (fb["general_ft"], fb["bridge_ft"], fb["within_ft"], f["shortfall_118_70_ft"],
                     call["raise_ft"]))
    a("5. For each uniform raise, found the discharge the levee then holds with freeboard at every cross-section "
      "(the railroad closure governs) and its annual chance on the present-river curve: %s per cent for 0 to 4 ft."
      % ", ".join("%.1f" % aep["%d ft" % r] for r in range(5)))
    a("6. Ask A: took %d ft off each station of the 2016 survey (the four structures both surveys shot sit %d ft "
      "apart), put its shots on NAVD 88 with OLDD_benchmark_list.csv (+%.2f ft) and averaged 2016 less 2024 by the "
      "2024 survey's reach: %s ft."
      % (f["station_offset_ft"], f["station_offset_ft"], f["datum_shift_ft"],
         ", ".join("%s %.2f" % (r, st[r]) for r in sorted(st))))
    a("7. Ask B: took OP-04's warning level, %.2f ft NGVD 29, on the Coyle Bridge gauge datum in force (%.1f ft "
      "before the %.2f ft step in stage against discharge on 19 October 2021, %.2f ft after on the %.2f ft datum), "
      "moved ORF2 stamps before the June 2021 logger swap from CST to UTC (+%d h, from the published peak times), "
      "put the Main Street sill at %.2f ft on the ORF2 gauge and interpolated both crossings within the hour: %s "
      "hours." % (w["elev_ngvd29"], w["stage_2014_ft"], w["step_ft"], w["stage_now_ft"], w["datum_now"],
                  hg["clock_shift_h"], hg["sill_stage_ft"], ", ".join(str(v) for v in ld.values())))
    a("8. Raise the crown %d ft before the 2027 flood season." % call["raise_ft"])
    a("")
    a("## 4. Deliverable Answers\n")
    a("### levee_raise_review.xlsx\n")
    a("1. Crown raise: %d ft." % call["raise_ft"])
    a("2. Design discharge at the Orrinsford gauge: %s cfs." % c(call["design_discharge_cfs"]))
    a("3. Annual chance the river exceeds what the levee holds with its freeboard, by uniform raise:")
    for r in range(5):
        a("   - %d ft: %.1f%%" % (r, aep["%d ft" % r]))
    a("4. Crown settlement between the 2016 and 2024 surveys, by reach:")
    for r in sorted(st):
        a("   - %s (%s): %.2f ft" % (r, REACH[r], st[r]))
    a("5. Hours from the Coyle Bridge warning level to the Main Street sill at Orrinsford, floods since October 2016:")
    import datetime as dt
    for d, h in ld.items():
        a("   - %s: %d hours" % (dt.date.fromisoformat(d).strftime("%B %Y"), h))
    a("")
    a("### levee_raise_memo.pdf\n")
    a("1. One page recommending a %d ft raise, with the chart of the present-river and published-record frequency "
      "curves at Orrinsford against the discharge each raise from 0 to 4 ft holds, the 1 per cent line marked, and the "
      "raise table." % call["raise_ft"])
    txt = "\n".join(L) + "\n"
    assert "\u2014" not in txt and "\u2013" not in txt
    open(os.path.join(TASK, "submission.md"), "w").write(txt)


if __name__ == "__main__":
    main()
