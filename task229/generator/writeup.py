"""task229 generator: submission.md from figures.json (every figure emitted, never typed).

    python3 task229/generator/writeup.py"""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MLAB_LONG = {"Oct 2025": "October 2025", "Nov 2025": "November 2025", "Dec 2025": "December 2025", "Jan 2026": "January 2026",
             "Feb 2026": "February 2026", "Mar 2026": "March 2026", "Apr 2026": "April 2026", "May 2026": "May 2026",
             "Jun 2026": "June 2026", "Jul 2026": "July 2026", "Aug 2026": "August 2026", "Sep 2026": "September 2026"}


def months_text(ms):
    """January to April and July to December, from a list of month names"""
    idx = [MON.index(m) for m in ms]
    runs, cur = [], [idx[0]]
    for i in idx[1:]:
        if i == cur[-1] + 1:
            cur.append(i)
        else:
            runs.append(cur)
            cur = [i]
    runs.append(cur)
    parts = ["%s to %s" % (MON[r[0]], MON[r[-1]]) if len(r) > 2 else " and ".join(MON[x] for x in r) for r in runs]
    return " and ".join(parts)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c = f["call_first"]
    lo, hi = f["bias_range_pct"]
    least = f["bias_least"]
    sab = f["sable"]
    sm = f["short_months"]
    mr = f["min_release"]
    out = []
    out.append("# task229 submission\n")
    out.append("## Tags\n")
    out.append("**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: the error a stream gauging "
               "network's published daily discharge carries when each station's stage-discharge rating is read at the day's "
               "mean water level below hydropeaking plants).")
    out.append("**Analytical objective:** Data Quality Monitoring & Alerting (from which month of 2027 each station's published "
               "daily discharge carries the below-grade-B flag).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Flag the published daily discharge at Corriston River below Talbot Canyon (C104) and at Hollis Bridge (C105) "
               "from %s 2027, at Sable Creek (C107) from %s, and at Merrin Creek below Merrin Falls (C112) and at Dunlop Road "
               "(C113) from %s; the other %d stations hold grade B through December.**\n" % (c["C104"], c["C107"], c["C112"], f["holding_stations"]))
    out.append("Below the two peaking plants each station's rating, read at the day's mean water level, publishes %d to %d per cent "
               "under the day's mean flow in every peaking month, against grade B's %d per cent. Not Sable Creek alone, which is "
               "what taking each published daily discharge as the day's mean flow files. Not C112 and C113 from June: Merrin Falls "
               "generates continuously until 30 June.\n" % (lo, hi, f["grade_b_pct"]))
    out.append("## 2. Critical Components\n")
    out.append("1. In every peaking month the published daily discharge at C104 and C105 below Talbot Canyon and C112 and C113 "
               "below Merrin Falls falls **%d to %d per cent** below the day's mean flow, the least at %s (%s) in %s (**%s per cent**)" % (
                   lo, hi, W.ST[least["station"]]["name"], least["station"], least["month"], least["pct"]))
    out.append("2. At Merrin Creek near the mouth (C124) the Vardy River's inflow damps the swing, and the published daily "
               "discharge stays within **%s per cent** of the day's mean flow in every month" % f["c124_max_pct"])
    out.append("3. Talbot Canyon peaks in every month but May and June; Merrin Falls, in service from 1 June, peaks from **%s**" % c["C112"])
    out.append("4. Sable Creek's May and June flows (**%s** and **%s** m3/s) exceed one and a half times its largest gauging "
               "(**%s** m3/s)\n" % (sab["may"], sab["june"], sab["top"]))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Graded each station-month of 2027 under sections 3 and 4 of hydrometric_data_standard_ed2.pdf on the flows of "
        "water_supply_outlook_2027.xlsx and corriston_hydro_operating_plan_2027.pdf (data_plan_2027.docx, section 2).",
        "Took each station's published daily discharge as data_dictionary.csv defines it, the rating in force applied to the "
        "day's mean water level, unchanged in 2027 (data plan, section 1), with the ratings of rating_book_issue2_2026.pdf.",
        "Built each peaking day at C104 and C105 below Talbot Canyon and C112, C113 and C124 below Merrin Falls from the "
        "operating plan: the minimum release (%s and %s m3/s) outside %s, the rest of the day's forebay or headpond inflow inside them "
        "with 30-minute ramps, plus the local inflow (the outlook's station flow less its TAL-FB or MER-HP row)." % (
            mr["talbot"], mr["merrin"], f["windows"]),
        "Carried each day's flow through the station's rating to the water level and read the rating at the day's mean water "
        "level: %d to %d per cent below the day's mean flow at C104 and C105 from January to April and July to December, and at "
        "C112 and C113 from July, after Merrin Falls' continuous generation through June; at C124 the Vardy River's inflow keeps "
        "it within %s per cent." % (lo, hi, f["c124_max_pct"]),
        "Applied the extrapolation rule against each rating's gauged top in the rating book: Sable Creek (C107) in May and June "
        "only; every other station's flow is steady through the day, so its published discharge equals the month's flow.",
        "Counted the 2026 water year's station-days in daily_records_wy2023_wy2026.csv holding a water level measured on the day: "
        "one per station and day, Mattin Creek once across its move (station_register.xlsx), and no row received before the day "
        "it covers had ended (the GOES ingest's held messages).",
        "Compared each 2026-water-year gauging in gaugings_2016_2026.csv (litres converted, channel rows summed, days in local "
        "standard time) with the rating in force on its day: before 1 April 2026 the 2019 ratings, recovered from the record's "
        "published water levels and discharges before that date; from 1 April the rating book's.",
        "Recommendation: flag C104 and C105 from %s 2027, C107 from %s, C112 and C113 from %s; the other %d stations hold." % (
            c["C104"], c["C107"], c["C112"], f["holding_stations"]),
    ]
    for i, s in enumerate(steps, start=1):
        out.append("%d. %s" % (i, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### discharge_grades_2027.png\n")
    out.append("1. Grid of the %d stations against January to December 2027 with every month short of grade B shaded: C104 and C105 "
               "%s; C107 %s; C112 and C113 %s; no other cell shaded\n" % (
                   f["stations"], months_text(sm["C104"]), months_text(sm["C107"]), months_text(sm["C112"])))
    out.append("### record_review_wy2026.xlsx\n")
    out.append("1. Station-days holding a water level measured on that day, 2026 water year:")
    for k in MLAB_LONG:
        out.append("   - %s: %s" % (MLAB_LONG[k], "{:,}".format(f["ask_a"][k])))
    out.append("2. Mean of each station's 2026-water-year gauging differences from the rating in force on the gauging day, per "
               "cent of the rating's discharge, one decimal place:")
    for no in W.CURRENT:
        out.append("   - %s %s: %.1f" % (no, W.ST[no]["name"], f["ask_b"][no]))
    out.append("")
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(out))
    print("wrote submission.md")


if __name__ == "__main__":
    main()
