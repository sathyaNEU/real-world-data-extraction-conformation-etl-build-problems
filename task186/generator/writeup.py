"""Emits submission.md from figures.json and the golden's own tables (no figure is typed here).

    python3 task186/generator/writeup.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import golden as GD  # noqa: E402
import params as P  # noqa: E402

MONTH = GD.MONTH_NAME
QNAME = {"Q1": "Dec-Feb", "Q2": "Mar-May", "Q3": "Jun-Aug", "Q4": "Sep-Nov"}


def main(fig_path=os.path.join(HERE, "figures.json"), out=os.path.join(TASK, "submission.md")):
    f = json.load(open(fig_path))
    off = f["call_off"]
    names = ", ".join("%s (%s)" % (x["name"], x["staff_no"]) for x in off)
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Human Factors & Ergonomics (safety incident and error analysis: an airport's X-ray screening "
             "officers' missed threat items, read from the CT lanes' threat image projection records).")
    L.append("**Analytical objective:** Anomaly Detection & Diagnostics.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Take %s off X-ray duty from 1 January 2027 for remedial training; recertify every other officer "
             "holding an X-ray endorsement on 30 November 2026.** Read on the threat objects each officer had not been "
             "shown before, their detection performance is below %d per cent against the %d per cent standard, and "
             "every other endorsed officer's is above %d per cent. Not only the %d casual officers whose hit rate over "
             "every projection in the year is under %d per cent: that rate counts projections of objects the officer "
             "had already been shown and told were threats, which officers detect %.1f per cent of the time against "
             "%.1f per cent for objects new to them, so it carries the officers shown the library most over the line."
             % (names, f["designated_below_pct"], f["standard_pct"], f["others_at_least_pct"], f["raw_off_count"],
                f["standard_pct"], f["pooled_repeat_pct"], f["pooled_first_pct"]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. **%d** officers hold an X-ray endorsement on 30 November 2026." % f["endorsed_population"])
    L.append("2. A projection is a first showing when no orientation of its threat object had been projected to the "
             "officer since the CT lanes opened: first showings are detected **%.1f per cent** of the time and repeat "
             "showings **%.1f per cent**." % (f["pooled_first_pct"], f["pooled_repeat_pct"]))
    L.append("3. The officers coming off detect fewer than **%d per cent** of their first showings; every other endorsed "
             "officer detects more than **%d per cent**." % (f["designated_below_pct"], f["others_at_least_pct"]))
    L.append("4. **%d** of the officers coming off clear %d per cent on their hit rate over every projection, "
             "**%d** of them full-time." % (f["masked_count"], f["standard_pct"], f["masked_ft_count"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Read SCS-04_screening_officer_competency_standard_rev6.pdf: detection performance is the probability "
             "that the officer detects a prohibited item carried in a passenger's cabin bag, assessed over the "
             "screening year 1 December 2025 to 30 November 2026 in Sydney time for every officer the register "
             "(screening_officer_register.xlsx) shows as Current on 30 November, %d officers." % f["endorsed_population"])
    L.append("2. Conformed tip_events_20250701_20261130.csv: dropped the D3 records of 17 February 2026 that appear "
             "twice, moved event_utc to Sydney time, mapped every operator_login (the OP7 international logins used "
             "before 1 March 2026 included) to its staff_no through ct_operator_logins.csv, and every image_no, padded "
             "to six digits, to its object_code through the Images sheet of tip_library_catalogue_r1.xlsx.")
    L.append("3. Ordered each officer's projections from 1 July 2025 and marked a first showing where no image of the "
             "same object_code had been projected to that officer before: first showings in the screening year are "
             "detected %.1f per cent of the time, repeat showings %.1f per cent." % (f["pooled_first_pct"],
                                                                                      f["pooled_repeat_pct"]))
    L.append("4. Took each endorsed officer's detection performance as their first showings detected over their first "
             "showings in the screening year: the officers in the recommendation fall below %d per cent and every "
             "other officer is above %d per cent." % (f["designated_below_pct"], f["others_at_least_pct"]))
    L.append("5. For currency, shared each lane's rostered time in lane_roster_20251201_20261130.csv among the "
             "officers rostered on it at each moment, leaving out an officer on Personal leave that day in "
             "hr_leave_taken_20251201_20261130.csv (payroll_no to staff_no through the register), and counted the "
             "officers endorsed for the whole month with under 20 hours.")
    L.append("6. For throughput, placed each unit in ct_unit_bag_counts_hourly_utc.csv on the lane it stood on each "
             "day (KX6-0413 on D2 until 2 March 2026 and on D5 from 20 April, KX6-0416 on D5 until 19 April and on "
             "each lane for its two retrofit days, KX6-0590 on D2 from 5 March), kept the Sydney hours inside the "
             "lane's rostered time, which leaves out each retrofitted unit's count before the first officer starts, "
             "and summed by quarter of the screening year.")
    L.append("7. Recommended taking the officers named in the recommendation off X-ray duty from 1 January 2027 and "
             "recertifying the rest.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % GD.CSV)
    L.append("")
    L.append("1. Officers coming off X-ray duty from 1 January 2027:")
    for x in off:
        L.append("   - %s, %s" % (x["staff_no"], x["name"]))
    L.append("2. Every other officer holding an X-ray endorsement on 30 November 2026 is recertified and keeps "
             "X-ray duty (%d officers)." % f["recertified_count"])
    L.append("")
    L.append("### %s" % GD.PDF)
    L.append("")
    L.append("1. Call: the officers listed above come off X-ray duty from 1 January 2027 for remedial training; every "
             "other endorsed officer is recertified.")
    L.append("2. Chart on page 1: each endorsed officer's detection performance against the 80 per cent line, the "
             "officers coming off marked in red, each officer's hit rate over every projection shown beside it.")
    L.append("3. Endorsed officers short of 20 hours of X-ray time, whole officers:")
    for (y, m) in A.MONTHS:
        L.append("   - %s %d: %d" % (MONTH[m], y, f["ask_a"]["%d-%02d" % (y, m)]))
    L.append("4. Passenger bags screened, nearest thousand:")
    for ln in P.LANES:
        L.append("   - %s: %s" % (ln, ", ".join("%s %s" % (QNAME[q], "{:,}".format(f["ask_b"]["%s %s" % (ln, q)]))
                                         for q, _, _ in A.QUARTERS)))
    L.append("")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    main()
