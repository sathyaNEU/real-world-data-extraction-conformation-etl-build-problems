"""task181 submission.md, written from figures.json (every figure emitted, none typed)."""
import common as C


def _list(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(path, fig):
    ref = fig["call"]["referred"]
    dflt = fig["call"]["default_path"]
    out = [c for c in C.CONSULTANTS if c not in ref]
    exp_only = [c for c in dflt if c not in ref]
    n, t = fig["naive"], fig["traced"]
    L = ["## Tags", "",
         "> **Domain:** Healthcare delivery and health economics, provider quality and risk adjustment.",
         "> **Analytical objective:** Anomaly detection and diagnostics.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Refer %s to professional practice review for the site infections after their April to September 2027 "
          "operations, and no other consultant.** Their infections stand above the Centre's control limit in the "
          "procedures steriliser 3's faulty loads never reached. Not %s, whose excess came from instrument trays "
          "steriliser 3 sterilised after its 12 May 2027 repair: with those operations set aside, each sits inside "
          "the limit." % (_list(ref), _list(exp_only)), ""]
    L += ["## 2. Critical Components", "",
          "1. Counted against the Centre's upper control limit on all their procedures, %s are above it." %
          _list(dflt),
          "2. From the 12 May 2027 repair, operations whose tray was last sterilised by steriliser 3 had %d infections "
          "against %.1f expected, %.1f times the rate of the department's other procedures." %
          (fig["exposed"]["observed"], fig["exposed"]["expected"], fig["exposed_ratio"]),
          "3. Steriliser 3 is the CSSD's one chamber for instrument containers over 10 kg, so it sterilises every "
          "preference tray %s and %s own and half of GS-21's, and their operations carry most of the exposure." %
          tuple(exp_only),
          "4. With the exposed operations set aside, %s stay above the limit (%s) and %s fall inside it (%s)." %
          (_list(ref), "; ".join("%s %d against %d" % (c, t[c]["observed"], t[c]["limit"]) for c in ref),
           _list(exp_only), "; ".join("%s %d against %d" % (c, t[c]["observed"], t[c]["limit"]) for c in exp_only)),
          ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. From theatre_operations_2022_2027.csv, kept completed procedures in the Centre's categories on their "
          "principal line, dropped returns to theatre, merged an add-on booked on its own (same patient, theatre and "
          "incision) into its operation, read GS-41 as GS-14, and took each risk index and expected infection from "
          "haisc_procedure_rates_2026.pdf (incision to closure against the cut-point).",
          "2. From ssi_surveillance_2022_2027.csv, kept each infection's latest confirmed record and linked it to its "
          "procedure (by booking from 2025; before that by patient, category and the procedure up to three days "
          "after the recorded date), inside 30 days or 90 with an implant, once per procedure at its deepest level.",
          "3. Set each consultant's April to September 2027 infections against the upper control limit, the 97.5th "
          "centile of a Poisson count at their expected number: %s above it." % _list(dflt),
          "4. Matched each theatre scan in instrument_tracking_scans_2027.csv (UTC, read in Melbourne time) to its "
          "operation by patient and theatre, and took each scanned item's last passed load before the scan from "
          "steriliser_cycles_2027.csv: %d window procedures had an item from steriliser 3 after its return to "
          "service at 14:40 on 12 May 2027 (cssd_equipment_log_2026_2027.xlsx), at %.1f times the rate." %
          (fig["exposed_procedures"], fig["exposed_ratio"]),
          "5. Compared each consultant's infections in the procedures left with the limit for their expected number: "
          "%s above it, every other consultant inside; giving the exposed procedures their own rate instead files "
          "the same consultants." % _list(ref),
          "6. Ask figures: each consultant's procedures in 2022 to 2024 as in step 1, and the infections linked to "
          "those procedures as in step 2, each under the procedure's responsible consultant.",
          "7. Recommendation: refer %s." % _list(ref), ""]
    L += ["## 4. Deliverable Answers", "", "### ssi_review_response_2027.docx", "",
          "1. Consultants referred to professional practice review: %s." % _list(ref),
          "2. Every other consultant marked out: %s." % _list(out),
          "3. Chart: each consultant's infections in the procedures the steriliser 3 fault did not reach against their "
          "upper control limit, with %s, the only bars over it, in red." % _list(ref),
          "4. Finding outside the consultants' practice: steriliser 3, from its repair on 12 May 2027.", "",
          "### ssi_review_figures_2027.csv", "",
          "1. Procedures, whole numbers:"]
    for c in C.CONSULTANTS:
        L.append("   - %s: 2022 %d, 2023 %d, 2024 %d" % (c, fig["ask_a"]["%s 2022" % c], fig["ask_a"]["%s 2023" % c],
                                                      fig["ask_a"]["%s 2024" % c]))
    L.append("2. Infections after them, whole numbers:")
    for c in C.CONSULTANTS:
        L.append("   - %s: 2022 %d, 2023 %d, 2024 %d" % (c, fig["ask_b"]["%s 2022" % c], fig["ask_b"]["%s 2023" % c],
                                                      fig["ask_b"]["%s 2024" % c]))
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
