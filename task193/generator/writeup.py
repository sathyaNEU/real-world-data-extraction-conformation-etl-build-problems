"""submission.md, drafted from figures.json so every number in it is one the generator computed."""
import os

import pack as PK
import world as W

NAME = {"chloride": "chloride", "sodium": "sodium", "boron": "boron"}
UNIT = {"chloride": "mg/L", "sodium": "mg/L", "boron": "ug/L"}


def _join(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(task, f):
    L = f["limits"]
    n = f["background_n"]
    win = f["window_n"]
    rv = f["reversed_events"]
    d0 = f["default_limits"]
    ex = f["exceed"]
    call = f["call"]
    lines = []
    a = lines.append
    a("## Tags")
    a("")
    a("**Domain:** Physical & Environmental Sciences, environmental monitoring and exceedance (groundwater detection "
      "monitoring at a closed municipal solid waste landfill).  ")
    a("**Analytical objective:** Anomaly Detection & Diagnostics.")
    a("")
    a("## 1. Final Recommendation")
    a("")
    a("**Yes: the October 2026 event sends %s to verification resampling, MW-7 on sodium at %s mg/L against a %s mg/L "
      "limit and MW-9 on boron at %s ug/L against %s ug/L.** Not MW-6 alone, which limits built on every background "
      "result give (sodium %s mg/L, boron %s ug/L), because MW-1 and MW-2 sampled water from beneath the waste in the "
      "events their heads fell below their boundary piezometers'; not MW-10 as well, which only a background taken from "
      "MW-3 alone puts over a limit."
      % (_join(call), f["october"]["MW-7 sodium"], L["sodium"], f["october"]["MW-9 boron"], L["boron"],
         d0["sodium"], d0["boron"]))
    a("")
    a("## 2. Critical Components")
    a("")
    a("1. MW-1's head stood below PZ-1's on **%d** of the %d background events and MW-2's below PZ-2's on **%d**; MW-3 "
      "never stood below PZ-3, so **%d** background results are not background." % (rv["MW-1"], f["background_events"],
                                                                                  rv["MW-2"], rv["total"]))
    a("2. Background results: **%d** chloride, **%d** sodium, **%d** boron." % (n["chloride"], n["sodium"], n["boron"]))
    a("3. Upper prediction limits: chloride **%s mg/L**, sodium **%s mg/L**, boron **%s ug/L**." %
      (L["chloride"], L["sodium"], L["boron"]))
    a("")
    a("## 3. Step-by-Step Solution")
    a("")
    a("1. Took the primary samples' reportable chloride, dissolved sodium and dissolved boron from %s (boron in mg/L, "
      "wells coded MW-01) and %s (boron in ug/L, field duplicates under the parent well's code), with MW-5R in MW-5's "
      "place." % (PK.FILES["edd_a"], PK.FILES["edd_b"]))
    a("2. Took the background window of SAP section 4, April 2018 to April 2026: %d chloride, %d sodium and %d boron "
      "results at MW-1, MW-2 and MW-3." % (win["chloride"], win["sodium"], win["boron"]))
    a("3. Computed each event's heads from %s and the survey in force on the gauging date in %s, and compared each "
      "background well with its boundary piezometer: MW-1 below PZ-1 on %d events, MW-2 below PZ-2 on %d, MW-3 never "
      "below PZ-3." % (PK.FILES["gauging"], PK.FILES["points"], rv["MW-1"], rv["MW-2"]))
    a("4. Left out those %d results, water drawn from beneath the waste and so not groundwater the landfill has not "
      "affected (SAP section 4), keeping %d, %d and %d." % (rv["total"], n["chloride"], n["sodium"], n["boron"]))
    a("5. Computed SAP section 5's limits from the natural logarithms with t at the 99th percentile: %s mg/L, %s mg/L "
      "and %s ug/L." % (L["chloride"], L["sodium"], L["boron"]))
    a("6. Compared every compliance well's October 2026 result with the unrounded limits (SAP section 6): %s." %
      "; ".join("%s over on %s" % (w, _join(ex[w])) for w in call))
    a("7. From %s, read each well's reading set marked sample collected, corrected R-4471's logged conductivity to "
      "25 C at %s per cent a degree (FS-03 section 4), and took the purge volume as the controller counter at the "
      "sample less the counter when the pump last stopped that day (a decon rinse or bottles filled entry, zero for "
      "the day's first well), in gallons of %s litres." % (PK.FILES["purge"], f["temp_coef_pct"], f["litres_per_gallon"]))
    a("8. Resample %s within %d days of their October samples." % (_join(call), f["resample_days"]))
    a("")
    a("## 4. Deliverable Answers")
    a("")
    a("### detection_eval_2026-10.xlsx")
    a("")
    a("1. Wells to resample: %s." % _join(call))
    a("2. Upper prediction limits, with the background results behind each:")
    for k, label in (("chloride", "Chloride"), ("sodium", "Sodium, dissolved"), ("boron", "Boron, dissolved")):
        a("   - %s: %s %s, %d results" % (label, L[k], UNIT[k], n[k]))
    a("3. October 2026 results at the compliance wells against the limits:")
    for w in W.COMPLIANCE:
        over = ex[w]
        a("   - %s: chloride %s mg/L, sodium %s mg/L, boron %s ug/L; %s" %
          (w, f["october"]["%s chloride" % w], f["october"]["%s sodium" % w], f["october"]["%s boron" % w],
           ("over on " + _join(over)) if over else "under every limit"))
    order = [w for d in W.SAMPLING_ORDER for w in d]
    a("4. Specific conductance at sampling, microsiemens per centimetre at 25 C, whole:")
    for w in sorted(order, key=lambda x: (x[:2], int(x[3:].rstrip("R")))):
        a("   - %s: %d" % (w, f["spc_25c"][w]))
    a("5. Purge volume before the sample, gallons, one decimal:")
    for w in sorted(order, key=lambda x: (x[:2], int(x[3:].rstrip("R")))):
        a("   - %s: %s" % (w, f["purge_gal"][w]))
    a("")
    a("### october_results_vs_limits.svg")
    a("")
    a("1. One panel each for chloride, sodium and boron, every compliance well's October 2026 result a point and the "
      "upper prediction limit a dashed line labelled at its value, with %s marked as over a limit." % _join(call))
    a("")
    open(os.path.join(task, "submission.md"), "w").write("\n".join(lines))
