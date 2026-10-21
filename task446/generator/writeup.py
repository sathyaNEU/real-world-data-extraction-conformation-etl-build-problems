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
    err_split, err_single = F["split"][1], F["single"][1]
    L = []
    L.append("# task446 submission")
    L.append("")
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Banking, Credit & Financial Risk (early-warning and watch-list monitoring of corporate "
             "obligor groups).  ")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Put a 2027 caseload of %d groups to the committee: %d of the %d obligor groups in the monitored book "
             "at 30 September 2026 are expected to reach the watch list by 30 September 2027.**"
             % (F["call"], F["call"], F["N1"]))
    L.append("")
    L.append("The %d prices each September flag by where in the group it was raised. Over the 2022 to 2025 cohorts a "
             "group whose flag sat on a customer we lend to reached the list within the year %s of the time, and one "
             "flagged only through a parent or sister company we do not lend to %s, and this September %d of the %d "
             "flags sit on customers, a far larger share than in any closed cohort. Predicting each closed cohort from "
             "the other three, that basis misses none by more than %s. Not one rate for every flagged group, which "
             "gives %d and misses a closed cohort by %s because it carries the cohorts' mix of the two kinds of flag "
             "onto a book that holds far more of the first; nor the colour or covenant-trigger splits, the latest or "
             "most stressed cohort, or the screen's capture and false-alarm rates with this year's arrival share "
             "backed out of the flagged share, which gives %d."
             % (F["call"], pct(F["p_d"]), pct(F["p_i"], 2), F["D1"], F["F1"], pct(err_split),
                round(F["single"][2]), pct(err_single), round(F["test"]["capture_false_alarm"][2])))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The monitored book at 30 September 2026 is **%d** groups; **%d** of them are flagged, **%d** of those "
             "flags raised on a customer the bank lends to" % (F["N1"], F["F1"], F["D1"]))
    L.append("2. Over the 2022 to 2025 cohorts taken together a flag raised on a customer reached the watch list "
             "**%s** of the time, a flag raised only on a member the bank does not lend to **%s**, and a group not "
             "flagged **%s**" % (pct(F["p_d"]), pct(F["p_i"], 2), pct(F["p_unflag"], 2)))
    L.append("3. Predicting each closed cohort from the other three, the split by where the flag was raised misses "
             "none by more than **%s**; one rate for every flagged group misses one by **%s**"
             % (pct(err_split), pct(err_single)))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    steps = [
        "Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and "
        "watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): %d groups at 30 September 2026." % F["N1"],
        "Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the "
        "group register's ultimate parent LEI, the obligor master's LEI and Companies House keys and the GLEIF "
        "relationship records in force at the date (CRM-07 2.2, 3.2), and marked each flag by whether an AMBER or RED "
        "entity is a customer on credit_obligor_master_20260930.csv opened by the date: %d flagged, %d of them on a "
        "customer." % (F["F1"], F["D1"]),
        "Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2): of "
        "%d flags raised on customers %d reached the list, of %d raised only on other members %d, of %s groups not "
        "flagged %d." % (m["D"], m["D_R"], m["I"], m["I_R"], "{:,}".format(m["U"]), m["U_R"]),
        "Back-tested the bases on the closed cohorts, each predicted from the other three: the split by where the "
        "flag was raised misses by at most %s, one rate for every flagged group by %s." % (pct(err_split),
                                                                                           pct(err_single)),
        "Gave each group in the 30 September 2026 book the share for its kind over the four cohorts taken together "
        "(4.3) and summed: %.1f expected arrivals, %d to the nearest whole group (CRM-07 5.3)."
        % (F["expected"], F["call"]),
        "Built each group's committed exposure under CRM-07 1.3 and 6.1 from facility_obligor_extract_20260930.csv, "
        "each facility (booking entity and number) once in every group with a member on it, counting the facility of "
        "a company booked to one group and consolidated through GLEIF into another's ultimate parent in both groups "
        "and placing customers not yet grouped through GLEIF (2.2), at the limit in facility_limit_history_20261008.csv "
        "as at the end of 30 September UK time, in sterling at the units_per_gbp rates, and banded it under 6.2.",
        "Summed each band's groups, flags, probabilities and probability-weighted committed exposure for the workbook "
        "and the chart.",
        "Recommendation: put a 2027 caseload of %d groups to the committee." % F["call"],
    ]
    for i, s_ in enumerate(steps, start=1):
        L.append("%d. %s" % (i, s_))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### %s" % deliver.XLSX)
    L.append("1. Heading figure: %d obligor groups expected to reach the watch list by 30 September 2027" % F["call"])
    L.append("2. One row per caseload band, smallest first (groups the band holds, their committed exposure, groups "
             "flagged in September, expected arrivals, expected committed exposure arriving):")
    for r in rows:
        L.append("   - %s: %s groups, %s committed, %d flagged, %.1f expected arrivals, %s arriving"
                 % (r["band"], "{:,}".format(r["groups"]), money(r["committed"]), r["flagged"], r["arrivals"],
                    money(r["exposure"])))
    L.append("3. Total row: %s groups, %s committed, %d flagged, %.1f expected arrivals, %s arriving"
             % ("{:,}".format(tot["groups"]), money(tot["committed"]), tot["flagged"], tot["arrivals"],
                money(tot["exposure"])))
    L.append("")
    L.append("### %s" % deliver.CHART)
    L.append("1. One bar per band, smallest first, labelled with the band's expected arrivals above")
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
    write_figures(text)
    print(text)


def write_figures(text):
    """figures.json: every figure blocks 1 to 4 state, as the code above formatted them from the solver's objects"""
    import json
    body = text[text.index("## 1."):]
    toks = re.findall(r"£?\d[\d,]*(?:\.\d+)?%?m?", body)
    seen = []
    for t in toks:
        if t not in seen:
            seen.append(t)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump({"source": "writeup.py from deliver.figures() and solve.golden()", "figures": seen}, fh, indent=1)
        fh.write("\n")


if __name__ == "__main__":
    main()
