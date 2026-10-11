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
    L.append("The %d is the %d groups times %s, the share reaching the list that this year's %s flagged share "
             "implies once the early-warning screen's capture and false-alarm rates are taken from the 2022 to 2025 "
             "cohorts. Not the hit and miss rates those cohorts report, carried onto this year's flags: the hit rate "
             "rises and falls with the share of each year's book that reaches the list, and this year's flagged share "
             "is above every closed cohort's. Not the latest or the most stressed cohort on its own: the standard "
             "measures the screen on the four closed cohorts taken together."
             % (F["call"], F["N1"], pct(F["p1"]), pct(F["a1"])))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The monitored book at 30 September 2026 is **%d** groups, **%d** of them flagged" % (F["N1"], F["F1"]))
    L.append("2. Over the 2022 to 2025 cohorts taken together the capture rate is **%s** and the false-alarm rate "
             "**%s**" % (pct(m["capture"]), pct(m["false_alarm"], 2)))
    L.append("3. The flagged share of **%s** implies **%s** of the book reaches the watch list within the year"
             % (pct(F["a1"]), pct(F["p1"])))
    L.append("4. A flagged group reaches it with probability **%s**, a group not flagged with **%s**"
             % (pct(F["p_flag"]), pct(F["p_unflag"])))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    steps = [
        "Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and "
        "watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): %d groups at 30 September 2026." % F["N1"],
        "Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the "
        "obligor master's LEI and Companies House keys and the GLEIF relationship records in force at the date "
        "(CRM-07 2.2, 2.3, 3.2): %d of the %d are flagged." % (F["F1"], F["N1"]),
        "Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2) and "
        "measured them taken together (4.3): capture rate %s, false-alarm rate %s."
        % (pct(m["capture"]), pct(m["false_alarm"], 2)),
        "Re-ran each closed cohort from the other three: capture and false-alarm rates reproduce its arrivals within "
        "3%, while hit and miss rates miss two of the four by more than a third, because the hit rate moves with the "
        "share of each year's book that reaches the list.",
        "Solved this year's %s flagged share for the share of the book that will reach the list through those two "
        "rates: %s, so a flagged group reaches it with probability %s and a group not flagged with %s (CRM-07 5.2)."
        % (pct(F["a1"]), pct(F["p1"]), pct(F["p_flag"]), pct(F["p_unflag"])),
        "Summed the probabilities over the %d groups: %.1f expected arrivals, %d to the nearest whole group "
        "(CRM-07 5.3)." % (F["N1"], F["expected"], F["call"]),
        "Built each group's committed exposure at 30 September 2026 under CRM-07 6.1 from "
        "facility_extract_hbplc_20260930_rerun.csv (the record for 30/09 per "
        "reference_data_extract_log_20261008.txt) and facility_extract_hbdac_20260930.csv, counting active "
        "facilities that mature after 30 September and dividing non-sterling limits by the per-pound rates in "
        "treasury_closing_rates_20260930.csv, then summed probabilities and probability-weighted exposure within "
        "each 6.2 band for the workbook.",
        "Recommendation: put a 2027 caseload of %d groups to the committee." % F["call"],
    ]
    for i, s in enumerate(steps, start=1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % deliver.XLSX)
    L.append("1. Heading figure: %d obligor groups expected to reach the watch list by 30 September 2027" % F["call"])
    L.append("2. One row per caseload band, smallest first (expected arrivals from groups flagged in September, "
             "expected arrivals from groups not flagged, expected committed exposure arriving):")
    for r in rows:
        L.append("   - %s: %.1f flagged, %.1f not flagged, %s" % (r["band"], r["flagged"], r["unflagged"],
                                                                money(r["exposure"])))
    L.append("3. Total row: %.1f flagged, %.1f not flagged, %s" % (tot["flagged"], tot["unflagged"],
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
