"""Write task446/submission.md from the same figures the golden deliverables carry.

    python3 task446/generator/writeup.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import deliver  # noqa: E402

OUT = os.path.join(HERE, "..", "submission.md")


def pct(x, nd=1):
    return ("%." + str(nd) + "f%%") % (x * 100)


def money(x):
    return "£{:,.1f}m".format(x)


def build(F):
    m = F["measures"]
    rows, tot = F["rows"], F["total"]
    test = F["test"]
    err_ans = test[F["model"]][1]
    err_hm = test["hit_and_miss"][1]
    L = []
    L.append("# task446 submission")
    L.append("")
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Banking, Credit & Financial Risk (early-warning and watch-list monitoring of corporate "
             "obligor groups).  ")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Put a 2027 caseload of %d groups to the committee: %d of the %d obligor groups in the monitored book "
             "at 30 September 2026 are expected to reach the watch list by 30 September 2027.**"
             % (F["call"], F["call"], F["N1"]))
    L.append("")
    L.append("The %d comes from the basis CRM-07 5.2's test selects: the early-warning screen's capture and "
             "false-alarm rates over the 2022 to 2025 cohorts, with this year's share of the book reaching the list "
             "backed out of this year's %s flagged share. Not the hit and miss rates those cohorts report, carried "
             "onto this year's flags: the hit rate moves with each year's share of the book reaching the list, and "
             "that basis misses a closed cohort by %s. Not the latest or the most stressed cohort on its own, nor "
             "rates trended on the flagged share: 5.2 sets the probabilities from the last four closed cohorts "
             "taken together, on the basis with the smallest largest miss."
             % (F["call"], pct(F["a1"]), pct(err_hm)))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The monitored book at 30 September 2026 is **%d** groups, **%d** of them flagged" % (F["N1"], F["F1"]))
    L.append("2. On 5.2's test the capture and false-alarm basis misses no closed cohort by more than **%s**; the hit "
             "and miss rates miss one by **%s**" % (pct(err_ans), pct(err_hm)))
    L.append("3. Over the 2022 to 2025 cohorts taken together the capture rate is **%s** and the false-alarm rate "
             "**%s**" % (pct(m["capture"]), pct(m["false_alarm"], 2)))
    L.append("4. The flagged share of **%s** implies **%s** of the book reaches the watch list within the year"
             % (pct(F["a1"]), pct(F["p1"])))
    L.append("5. A flagged group reaches it with probability **%s**, a group not flagged with **%s**"
             % (pct(F["p_flag"]), pct(F["p_unflag"])))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    steps = [
        "Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and "
        "watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): %d groups at 30 September 2026." % F["N1"],
        "Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the "
        "obligor master's LEI and Companies House keys and the GLEIF relationship records in force at the date "
        "(CRM-07 2.2, 3.2): %d of the %d are flagged." % (F["F1"], F["N1"]),
        "Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2) and "
        "measured them taken together (4.3): capture rate %s, false-alarm rate %s."
        % (pct(m["capture"]), pct(m["false_alarm"], 2)),
        "Ran 5.2's test, each closed cohort predicted from the other three taken together: the capture and "
        "false-alarm basis has the smallest largest miss, %s, against %s for the hit and miss rates."
        % (pct(err_ans), pct(err_hm)),
        "Solved this year's %s flagged share for the share of the book that will reach the list through those two "
        "rates: %s, so a flagged group reaches it with probability %s and a group not flagged with %s."
        % (pct(F["a1"]), pct(F["p1"]), pct(F["p_flag"]), pct(F["p_unflag"])),
        "Summed the probabilities over the %d groups: %.1f expected arrivals, %d to the nearest whole group "
        "(CRM-07 5.3)." % (F["N1"], F["expected"], F["call"]),
        "Built each group's committed exposure under CRM-07 1.3 and 6.1 from facility_obligor_extract_20260930.csv, "
        "each facility (booking entity and number) once in every group with an obligor on it and customers not yet "
        "grouped placed through GLEIF (2.2), at the limit in facility_limit_history_20261008.csv as at the end of 30 "
        "September UK time, in sterling at the units_per_gbp rates, then banded it under 6.2 for the workbook.",
        "Recommendation: put a 2027 caseload of %d groups to the committee." % F["call"],
    ]
    for i, s_ in enumerate(steps, start=1):
        L.append("%d. %s" % (i, s_))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % deliver.XLSX)
    L.append("1. Heading figure: %d obligor groups expected to reach the watch list by 30 September 2027" % F["call"])
    L.append("2. One row per caseload band, smallest first (groups the band holds, their committed exposure, expected "
             "arrivals from groups flagged in September, expected arrivals from groups not flagged, expected "
             "committed exposure arriving):")
    for r in rows:
        L.append("   - %s: %s groups, %s committed, %.1f flagged, %.1f not flagged, %s arriving"
                 % (r["band"], "{:,}".format(r["groups"]), money(r["committed"]), r["flagged"], r["unflagged"],
                    money(r["exposure"])))
    L.append("3. Total row: %s groups, %s committed, %.1f flagged, %.1f not flagged, %s arriving"
             % ("{:,}".format(tot["groups"]), money(tot["committed"]), tot["flagged"], tot["unflagged"],
                money(tot["exposure"])))
    L.append("")
    L.append("### %s" % deliver.CHART)
    L.append("1. One stacked bar per band, smallest first, with the flagged and not-flagged segments labelled with "
             "the band figures above")
    L.append("2. The caseload, %d groups, written on the chart" % F["call"])
    L.append("3. Title: \"%s\"" % (deliver.TITLE % (F["call"], F["N1"])))
    return "\n".join(L) + "\n"


def check(text, F):
    assert "—" not in text and "–" not in text
    for banned in ("deteriorat", "robust", "leverage", "comprehensive", "it is worth noting"):
        assert banned not in text.lower(), banned
    names = set(re.findall(r"[a-z0-9_\-]+\.(?:csv|xlsx|txt|pdf|docx|md|png|svg)", text))
    target = set(os.listdir(os.path.join(HERE, "..", "target")))
    for n in names:
        assert n in target or n in (deliver.XLSX, deliver.CHART), n
    assert text.count("### ") == 2


def main():
    F = deliver.figures()
    text = build(F)
    check(text, F)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(text)


if __name__ == "__main__":
    main()
