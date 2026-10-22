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
    L.append("**Set the 2027 watch-list caseload at %d groups: %d of the %d obligor groups in the monitored book "
             "at 30 September 2026 are expected to reach the watch list by 30 September 2027.**"
             % (F["call"], F["call"], F["N1"]))
    L.append("")
    L.append("The %d prices each September flag by the member that raised it: over the 2022 to 2025 cohorts a group "
             "flagged on a customer we lend to reached the list within the year %s of the time and one flagged only on "
             "a parent or sister company we do not lend to %s, and %d of the %d groups flagged this September were "
             "flagged on a customer. Not one rate for every flagged group, which carries the cohorts' mix of the two "
             "kinds of flag onto a book holding far more of the first and misses one closed cohort by %s where the "
             "split's largest miss is %s; not the colour or covenant-trigger splits or the latest or most stressed "
             "cohort, which do the same; not the screen's capture and false-alarm rates with this year's arrival share "
             "backed out of the flagged share, which read a rise in customer flags as a rise in the base rate."
             % (F["call"], pct(F["p_d"]), pct(F["p_i"], 2), F["D1"], F["F1"], pct(err_single), pct(err_split)))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The monitored book at 30 September 2026 is **%d** groups; **%d** of them are flagged, **%d** of those "
             "flagged on a customer the bank lends to" % (F["N1"], F["F1"], F["D1"]))
    L.append("2. Over the 2022 to 2025 cohorts taken together a group flagged on a customer reached the watch list "
             "within the year **%s** of the time, a group flagged only on members the bank does not lend to **%s**, "
             "and a group not flagged **%s**" % (pct(F["p_d"]), pct(F["p_i"], 2), pct(F["p_unflag"], 2)))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    steps = [
        "Built the monitored book at each 30 September from credit_group_register_20260930.xlsx and "
        "watch_list_history_2020-01_to_2026-09.csv (CRM-07 4.1): %d groups at 30 September 2026." % F["N1"],
        "Carried each September publication in ews_entity_signals_2022-09_to_2026-09.csv to groups through the "
        "group register's ultimate parent LEI, the obligor master's LEI and Companies House keys and the GLEIF "
        "relationship records in force at the date (CRM-07 2.2, 3.2), and marked each flagged group by whether any of "
        "its AMBER or RED members is a customer on credit_obligor_master_20260930.csv opened by the date: %d "
        "flagged, %d of them on a customer." % (F["F1"], F["D1"]),
        "Matched the 2022 to 2025 cohorts to watch-list placements in the following twelve months (CRM-07 4.2): of "
        "%d groups flagged on a customer %d reached the list, of %d flagged only on other members %d, of %s groups "
        "not flagged %d." % (m["D"], m["D_R"], m["I"], m["I_R"], "{:,}".format(m["U"]), m["U_R"]),
        "Back-tested the bases on the closed cohorts, each forecast from the other three taken together: the largest "
        "miss, as a share of the cohort's actual arrivals, is %s for the split by where the flag was raised and %s "
        "for one rate for every flagged group." % (pct(err_split), pct(err_single)),
        "Gave each group in the 30 September 2026 book the cohorts' share for its kind of flag, or for groups not "
        "flagged, over the four cohorts taken together (CRM-07 4.3) and summed: %.1f expected arrivals, %d to the "
        "nearest whole group (CRM-07 5.3)."
        % (F["expected"], F["call"]),
        "Built each group's committed exposure under CRM-07 1.3 and 6.1 from facility_obligor_extract_20260930.csv: "
        "each facility (booking entity and number) once in every group with a member on it, counting the facility of "
        "a company booked to one group and consolidated through GLEIF into another's ultimate parent in both groups "
        "and placing customers not yet grouped through GLEIF (2.2), at the limit in facility_limit_history_20261008.csv "
        "as at the end of 30 September UK time, in sterling at the units_per_gbp rates.",
        "Left out the %d facilities the ledger booked twice, each undrawn and repeating stamp for stamp, limit for "
        "limit and user for user the limit history of the facility numbered just before it for the same customer and "
        "terms, kept the same-day tranches whose histories differ, banded the groups under 6.2 and summed each band's "
        "groups, flagged groups, probabilities and probability-weighted committed exposure for the workbook and the "
        "chart." % F["twice"],
        "Recommendation: set the 2027 watch-list caseload at %d groups." % F["call"],
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
    assert "\u2014" not in text and "\u2013" not in text
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
    write_figures(F)
    print(text)


BAND_KEYS = ("under_5m", "5m_to_15m", "15m_to_40m", "40m_to_100m", "100m_and_over")


def figures_doc(F):
    """figures.json: every figure blocks 1 to 4 state, keyed, at the precision the write-up states it. The keys
    under workbook and chart are the prompt's own asks, the ones a reader is asked to report back."""
    m = F["measures"]

    def row(r):
        return dict(groups=r["groups"], committed_gbp_m=round(r["committed"], 1), flagged=r["flagged"],
                    expected_arrivals=round(r["arrivals"], 1), arriving_gbp_m=round(r["exposure"], 1))

    return {
        "source": "writeup.py from deliver.figures(), which reads target/ only through solve.golden()",
        "call": {"caseload": F["call"], "expected_arrivals": round(F["expected"], 1)},
        "components": {"book_groups": F["N1"], "flagged_groups": F["F1"], "flagged_on_customer": F["D1"],
                       "rate_flagged_on_customer_pct": round(F["p_d"] * 100, 1),
                       "rate_flagged_only_elsewhere_pct": round(F["p_i"] * 100, 2),
                       "rate_not_flagged_pct": round(F["p_unflag"] * 100, 2)},
        "steps": {"cohort_flagged_on_customer": m["D"], "cohort_flagged_on_customer_reached": m["D_R"],
                  "cohort_flagged_only_elsewhere": m["I"], "cohort_flagged_only_elsewhere_reached": m["I_R"],
                  "cohort_not_flagged": m["U"], "cohort_not_flagged_reached": m["U_R"],
                  "backtest_largest_miss_split_pct": round(F["split"][1] * 100, 1),
                  "backtest_largest_miss_one_rate_pct": round(F["single"][1] * 100, 1),
                  "facilities_booked_twice": F["twice"]},
        "band_edges_gbp_m": [5, 15, 40, 100],
        # as block 4 prints them ("£499.9m"), for figures_check.py, whose tokeniser stops at the unit letter;
        # under parameters so a reader is scored on the numeric keys above and below, never on these
        "parameters": {"money_as_stated": [money(r[k]) for r in F["rows"] + [F["total"]]
                                           for k in ("committed", "exposure")],
                       "standard_sections_cited": ["1.3", "2.2", "3.2", "4.1", "4.2", "4.3", "5.3", "6.1", "6.2"]},
        "workbook": {"heading": F["call"], "bands": {k: row(r) for k, r in zip(BAND_KEYS, F["rows"])},
                     "total": row(F["total"])},
        "chart": {"bars": [round(r["arrivals"], 1) for r in F["rows"]], "caseload": F["call"],
                  "title": deliver.TITLE % (F["call"], F["N1"])},
    }


def write_figures(F):
    import json
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(figures_doc(F), fh, indent=1, ensure_ascii=False)
        fh.write("\n")


if __name__ == "__main__":
    main()
