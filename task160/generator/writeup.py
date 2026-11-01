"""Writes submission.md from the cut pack through analysis.py and checks it against figures.json, so every figure
in the write-up is one the generator computed from target/."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import golden as GD  # noqa: E402


def main():
    P = A.Pack(os.path.join(TASK, "target"))
    g = P.golden()
    f = json.load(open(os.path.join(HERE, "figures.json")))["figures"]
    assert f == A.figures(P)
    net, qt, pre = f["call_net_change"], f["qt_reviews_added"], f["current_reviews_removed"]
    cp, pp = round(100 * g["c"]), round(100 * g["p"])
    L = []
    a = L.append
    a("## Tags\n")
    a("**Domain:** Healthcare Delivery & Health Economics (utilization, access and demand forecasting: a remote "
      "pharmacy desk's override review volume when a hospital takes a medication alert package live on every adult "
      "ward).")
    a("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    a("## 1. Final Recommendation\n")
    a("**Plan for about %d more override reviews (to the nearest 100) from Quillfield's adult wards in the first 13 "
      "weeks of the hospital-wide go-live than the desk would get over those weeks without it.** The go-live is on "
      "4 January 2027. The QT "
      "combination alert adds about %d reviews; the duplicate PRN opioid alert, answered by removing the new order "
      "%d per cent of the time on the pilot units, takes about %d of today's reviews off the desk. Not %d: the "
      "background log counts the package's own alerts, and a removed order carries no alerts of its own and has "
      "no severe interaction alert fire against it later in the stay." % (net, qt, cp, pre, qt))
    a("")
    a("## 2. Critical Components\n")
    a("1. The QT combination alert adds about **%d** reviews over the 13 weeks (to the nearest 100): the background "
      "log's QT alerts on the wards going live, overridden at the pilot units' %d per cent." % (qt, pp))
    a("2. About **%d** of today's reviews no longer reach the desk (to the nearest 100): overridden alerts on an "
      "order, or fired against an order, that the duplicate PRN opioid alert would have removed at the pilot units' "
      "%d per cent." % (pre, cp))
    a("3. Net change **+%d** reviews (to the nearest 100), on the volume plan's admissions for the 13 weeks.\n" % net)
    a("## 3. Step-by-Step Solution\n")
    a("1. Conformed QRMC_MedAlertHistory_20250101-20261025.csv: mapped the department names used before 9 November "
      "2025 to the rule register's unit codes, dropped the boundary day each quarterly pull repeated, and moved the "
      "background log's UTC stamps to Eastern time.")
    a("2. On the pilot units (7W, 5E, 8N) over the whole history: %d per cent of duplicate PRN opioid alerts answered "
      "by removing the order, %d per cent of QT combination alerts overridden." % (cp, pp))
    a("3. Base period 6 July to 25 October 2026 on the units going live: %d QT combination alerts in the background "
      "log on orders not removed, times %d per cent, %.0f reviews added." % (g["qt_rows_B"], pp, g["qt_add_B"]))
    a("4. For each of the %d overridden high-severity alerts on those units in the base period, the chance it no "
      "longer reaches the desk: its own order or its interacting order carries a background duplicate-opioid alert "
      "(each removed at %d per cent), or its own order a QT alert (removed at %d per cent); %.0f reviews lost."
      % (g["reviews_B"], cp, 100 - pp, g["pre_B"]))
    a("5. Scaled by the volume plan's admissions for the 13 weeks from 4 January 2027 over the census admissions "
      "in the base period (%s over %s): %.0f added, %.0f lost, net %.0f, about %d."
      % (format(g["plan_adm"], ","), format(g["adm_B"], ","), g["qt_add"], g["pre"], g["net"], net))
    a("6. Desk hours: every queue session closing 1 July to 30 September 2026 Eastern, claim to close (returned "
      "sessions included), each given the department of the alert its alert_ref names in the alert history; the "
      "point of care follows the bed, and five pairs of wards exchanged wings between 20 July and 14 September.")
    a("7. Signed-off reviews: each signed-off task counted as the overridden high-severity alerts on its order at "
      "the same signing, by the month and shift of sign-off in Eastern time.")
    a("8. Recommended planning for about %d more reviews in the 13 weeks.\n" % net)
    a("## 4. Deliverable Answers\n")
    a("### %s\n" % GD.BOOK)
    a("1. Net change in override reviews, 13 weeks from 4 January 2027: +%d (QT combination alert +%d, current "
      "reviews lost %d), to the nearest 100." % (net, qt, pre))
    a("2. Desk hours, July to September 2026, nearest whole hour:")
    for u in P.going_live:
        a("   - %s %s: %d" % (u, GD.NAMES[u], f["desk_hours_%s" % u]))
    a("3. Reviews signed off, July, August and September 2026, by shift:")
    for s in A.SHIFTS:
        a("   - %s shift: July %d, August %d, September %d" % (s, f["signed_off_2026-07_%s" % s.lower()],
                                                              f["signed_off_2026-08_%s" % s.lower()],
                                                              f["signed_off_2026-09_%s" % s.lower()]))
    a("")
    a("### %s\n" % GD.MEMO)
    a("1. Net change: about %d more override reviews in the 13 weeks from 4 January 2027." % net)
    a("2. Chart: reviews signed off by shift and month, July to September 2026, the values in item 3 above.")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")
    print("submission.md written (%d lines)" % len(L))


if __name__ == "__main__":
    main()
