"""Emit submission.md from figures.json, so no figure in the write-up is typed."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import world as W   # noqa: E402

ORDER = [k for k, *_ in W.STREAMS]
NAME = {k: n for k, n, _p, _m, _c in W.STREAMS}


def t(n):
    return "{:,}".format(int(n))


def main():
    f = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    g = f["stream_metal"]
    L = []
    w = L.append
    w("## Tags")
    w("")
    w("**Domain:** Survey Research & Official Statistics (anomaly detection in official waste statistics).")
    w("**Analytical objective:** Anomaly Detection & Diagnostics.")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**The 2027 supplementary collection module goes to %s, the only stream whose 2026 recovery "
      "rate is established below its plan target.**" % f["call"])
    w("")
    w("Its rate is %.1f per cent against a %.1f per cent target, a %.1f point shortfall at %.2f "
      "standard errors, and its 95 per cent interval of %.1f to %.1f per cent excludes the target. "
      "Not %s, which leads on the size of the shortfall at %.1f points but stands at only %.2f "
      "standard errors because its arisings estimate is the least precise of the eight. Not any of "
      "the remaining six streams, none of which reaches %.2f standard errors."
      % (f["call_rate_pct"], f["call_target_pct"], f["call_shortfall_pp"], f["call_z"],
         f["call_interval_pct"][0], f["call_interval_pct"][1], f["runner_up"],
         f["runner_up_shortfall_pp"], f["runner_up_z"], f["runner_up_z"]))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Tonnage confirmed received at a recovery operation for %s is **%s t**" % (f["call"], t(g["recovered_t"])))
    w("2. Its estimated arisings are **%s t**" % t(g["arisings_t"]))
    w("3. Its 2026 recovery rate is **%.1f per cent** against a plan target of **%.1f per cent**"
      % (g["rate_pct"], g["target_pct"]))
    w("4. The rate's 95 per cent interval is **%.1f to %.1f per cent**, which lies wholly below the target"
      % (g["interval_pct"][0], g["interval_pct"][1]))
    w("5. The shortfall for %s is **%.1f points** at **%.2f standard errors**, so it is not established"
      % (f["runner_up"], f["runner_up_shortfall_pp"], f["runner_up_z"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Mapped the renamed columns of waste_movement_legs_2026_h2.csv onto "
      "waste_movement_legs_2026_h1.csv and resolved every waste code through "
      "waste_code_crosswalk.csv, honouring its mid-year revision: %s legs for consignments "
      "despatched in the reference year." % t(f["register_legs_2026"]))
    w("2. Chained each producer consignment to its final treatment using facility_register.csv for "
      "the facility role and treatment_operation_codes.xlsx for the operation kind, and counted each "
      "tonnage once at the producer's despatch leg: %s t confirmed at a recovery operation for %s."
      % (t(g["recovered_t"]), f["call"]))
    w("3. Estimated each stream's arisings from bws_2026_microdata.csv by applying the design weight "
      "to every usable return in each stratum, the reported zeros included: %s t for %s."
      % (t(g["arisings_t"]), f["call"]))
    w("4. Divided the two: a %.1f per cent recovery rate." % g["rate_pct"])
    w("5. Took the rate's sampling error as its denominator's alone, the register tonnage being a "
      "complete administrative total, and computed that error over each stratum of "
      "bws_2026_design_and_weighting.pdf with the stratum's own finite-population correction, so the "
      "completely enumerated large-enterprise stratum, which holds %.1f per cent of this stream's "
      "arisings, contributes none of it: a standard error of %.2f points."
      % (f["golden_take_all_share_pct"], f["call_se_pp"]))
    w("6. Read each stream's target from national_waste_management_plan_targets.pdf and tested the "
      "shortfall against the standard error: %.1f points at %.2f standard errors."
      % (f["call_shortfall_pp"], f["call_z"]))
    w("7. Repeated for the other seven streams: %s is the only one established below target, and the "
      "larger %.1f point shortfall for %s stands at %.2f standard errors."
      % (f["call"], f["runner_up_shortfall_pp"], f["runner_up"], f["runner_up_z"]))
    w("8. Committed the module to %s." % f["call"])
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### recovery_attainment_2026.xlsx")
    w("")
    w("1. Attainment, a row per stream with confirmed recovered tonnage, estimated arisings, the "
      "recovery rate, its 95 per cent interval, the plan target and the shortfall:")
    for k in ORDER:
        d = f["stream_%s" % k]
        w("   - %s: %s t recovered, %s t arising, %.1f per cent, interval %.1f to %.1f per cent, "
          "target %.1f per cent, shortfall %.1f points"
          % (NAME[k], t(d["recovered_t"]), t(d["arisings_t"]), d["rate_pct"],
             d["interval_pct"][0], d["interval_pct"][1], d["target_pct"], d["shortfall_pp"]))
    w("2. Stage chain, a row per stream with the tonnage at each movement chain stage and the "
      "stage to stage pass through rate:")
    for k in ORDER:
        c = f["chain_%s" % k]
        w("   - %s: %s t arising, %s t despatched, %s t confirmed at a final treatment operation, "
          "%s t confirmed at a recovery operation, pass through %.1f per cent, %.1f per cent, "
          "%.1f per cent"
          % (NAME[k], t(c["arisings_t"]), t(c["despatched_t"]), t(c["confirmed_t"]),
             t(c["recovered_t"]), c["pass_1_2_pct"], c["pass_2_3_pct"], c["pass_3_4_pct"]))
    w("3. Collection effort, a row per region with the field days consumed and the usable returns "
      "per field day:")
    for r in W.REGIONS:
        a = f["a1_%s" % r]
        w("   - %s: %.2f field days, %.2f usable returns per field day" % (r, a["field_days"], a["returns_per_day"]))
    w("4. Tonnage confirmed received at a recovery operation in the prior reference year, per stream:")
    for k in ORDER:
        w("   - %s: %s t" % (NAME[k], t(f["a2_%s" % k])))
    w("5. Municipal reconciliation, a row per region with the gap between reported collections and "
      "licensed facility receipts on a receipt date basis, and that gap as a share of collections:")
    for r in W.REGIONS:
        a = f["a3_%s" % r]
        w("   - %s: %s t collected, %s t received, gap %s t, %.1f per cent of collections"
          % (r, t(a["collections_t"]), t(a["receipts_t"]), t(a["gap_t"]), a["gap_share_pct"]))
    w("")
    w("### attainment_against_target_2026.png")
    w("")
    w("1. One horizontal bar per stream giving the 2026 recovery rate, a whisker for the 95 per cent "
      "interval and a vertical mark at the plan target, ordered by standard errors from target, with "
      "%s drawn in the darker fill and labelled as established below target." % f["call"])
    w("")
    out = os.path.join(TASK, "submission.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote %s (%d lines)" % (out, len(L)))


if __name__ == "__main__":
    main()
