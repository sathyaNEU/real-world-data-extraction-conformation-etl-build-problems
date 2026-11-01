"""task125 submission.md, written from figures.json (every figure emitted, none typed)."""
import datetime as dt


def _d(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s" % (d.day, d.strftime("%B %Y"))


def _seg(fig, s):
    return "%s (%s, ward %d)" % (s, fig["labels"][str(s)], fig["wards"][str(s)])


def write(path, fig):
    lab = fig["labels"]
    ent = fig["entering"]
    lea = fig["leaving"]
    stay = fig["staying_gardens"]
    L = ["## Tags", "",
         "**Domain:** Criminology & Justice (crime incidence and hot spot analysis: a municipal police service "
         "designating the street segments its directed patrols cover for a year).",
         "**Analytical objective:** Anomaly Detection & Diagnostics.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Designate the 20 street segments listed below for the 2027 hot spot patrols: the five segments around "
          "the Lakeshore Centre come in and the five around the Memorial Gardens drop out, because the Mariners "
          "play their 2027 home games at the Lakeshore Centre and those segments' street crime follows the "
          "venue's event nights.** From 2022 to 2026 the five Lakeshore segments recorded %d of their %d founded "
          "patrol crimes on the Lakeshore Centre's %d event nights. A ranking on 2026's counts or on the five-year "
          "average is the wrong basis for 2027: it would keep the five Gardens segments, whose counts the Gardens' "
          "event nights carried (%d of their %d crimes on %d nights), and leave out the five Lakeshore segments."
          % (fig["entering_on_lakeshore_nights"], fig["entering_total"], fig["lakeshore_nights_2022_2026"],
             fig["leaving_on_gardens_nights"], fig["leaving_total"], fig["gardens_nights_2022_2026"]), ""]
    L += ["## 2. Critical Components", "",
          "1. The paid-duty register books **%d** Mariners home games at the Lakeshore Centre from %s; the "
          "Mariners' last Memorial Gardens game was on %s."
          % (fig["mariners_2027_booked"], _d(fig["mariners_first_lakeshore"]), _d(fig["mariners_last_gardens"])),
          "2. The five Gardens segments that drop out recorded **%d of %d** founded patrol crimes from 2022 to 2026 "
          "on the Gardens' **%d** event nights, about **%d per cent** of the nights."
          % (fig["leaving_on_gardens_nights"], fig["leaving_total"], fig["gardens_nights_2022_2026"],
             fig["gardens_nights_share_pct"]),
          "3. The five Lakeshore segments that come in recorded **%d of %d** on the Lakeshore Centre's **%d** "
          "event nights." % (fig["entering_on_lakeshore_nights"], fig["entering_total"],
                             fig["lakeshore_nights_2022_2026"]),
          "4. %s stays designated on its steady crime with the Gardens' event nights gone."
          % "; ".join(_seg(fig, s) for s in stay), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Conformed mps_rms_occurrences_2022_2026.csv under the protocol: each occurrence once on its latest "
          "version, legacy codes through rms_offence_code_crosswalk_2023.csv, legacy dates day first, unfounded "
          "out, dated by occurred_from or the report date where blank, on the segments of "
          "mountjoy_street_segments.csv.",
          "2. Took each venue's event nights from the EVENT duties at the Memorial Gardens and the Lakeshore "
          "Centre in every sheet of mps_paid_duty_register_2022_2027.xlsx: %d Gardens and %d Lakeshore nights from "
          "2022 to 2026, and the 2027 sheet's %d Mariners home games at the Lakeshore Centre."
          % (fig["gardens_nights_2022_2026"], fig["lakeshore_nights_2022_2026"], fig["mariners_2027_booked"]),
          "3. Fitted each segment's daily founded patrol crimes from 2022 to 2026 by least squares on a constant "
          "and the two venues' event-night indicators: its steady rate and its excess on each venue's nights.",
          "4. Took each segment's expected 2027 count as %d days at its steady rate plus each excess times its "
          "venue's 2027 event nights, the nights read from the register: 2026's %d Lakeshore and %d Gardens nights "
          "with the Mariners' %d Gardens nights of 2026 at the Lakeshore Centre, where the 2027 sheet books the team "
          "(%d and %d); the same 20 come out of the 2027 sheet's own bookings (%d and %d) and of any count from %d "
          "to %d Lakeshore and %d to %d Gardens nights, and designated the 20 highest."
          % (fig["days_2027"], fig["lakeshore_nights_2026"], fig["gardens_nights_2026"], fig["mariners_2026"],
             fig["nights_2027_lakeshore"], fig["nights_2027_gardens"], fig["register_2027_lakeshore"],
             fig["register_2027_gardens"], fig["robust_lakeshore"][0], fig["robust_lakeshore"][1],
             fig["robust_gardens"][0], fig["robust_gardens"][1]),
          "5. Officer-hours: for each call in mps_cad_calls_2026.csv (source not OFFICER) received in 2026 local "
          "time at an address on a segment of mountjoy_street_segments.csv, its ward the segment's (a call at an "
          "address outside the City's wards belongs to none, Directive PO-14), each unit's hours from dispatch to "
          "clear times its crew in mps_patrol_roster_2026.csv on the tour covering the dispatch (a night tour is "
          "dated by the evening it starts), by ward and quarter of receipt.",
          ""]
    L += ["## 4. Deliverable Answers", "", "### hot_spot_patrols_2027.pptx", "",
          "1. Designated segments, 20:"]
    for s in fig["designated_ranked"]:
        L.append("   - %s" % _seg(fig, s))
    L += ["2. Come in against the 2026 ranking:"]
    for s in ent:
        L.append("   - %s" % _seg(fig, s))
    L += ["3. Drop out against the 2026 ranking:"]
    for s in lea:
        L.append("   - %s" % _seg(fig, s))
    L += ["4. Bar chart on slide 2 of each of the %d candidate segments' expected 2027 patrol crimes, designated in "
          "navy, the cut between %s and %s." % (fig["pool_size"], fig["cut_20th"], fig["cut_21st"]), "",
          "### patrol_figures_2026.csv", "",
          "1. Officer-hours on calls for service in 2026, whole hours:"]
    for w in range(1, 9):
        L.append("   - Ward %d: %s" % (w, ", ".join("Q%d %d" % (q, fig["ask_officer_hours"]["%d Q%d" % (w, q)])
                                                 for q in range(1, 5))))
    open(path, "w").write("\n".join(L) + "\n")
