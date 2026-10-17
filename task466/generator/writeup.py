"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    c, k, sc, fl = f["call"], f["components"], f["scenarios"], f["flip"]
    rv = f["rivals"]
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
    blocks = words.get(c["blocks"], str(c["blocks"]))
    lines = [
        "## Tags",
        "",
        "**Domain:** General Statistics & Data Science (data integration: a river gauge's record and a water works' "
        "reports, kept under different observation mechanisms, combined in one maximum-likelihood fit).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**Reserve %s MGD (%s blocks) of firm capacity on the Castlewick interconnect for 2027.**" % (c["block_mgd"], blocks),
        "At the Varrow River's 50-year 7-day low flow of %s cfs the permit allows %s MGD, %s MGD short of the 2027 "
        "Stage 2 demand of %s MGD, and %s blocks cover it. Not %s MGD, from a fit to the gauge's years and the %d "
        "report years with a measured flow alone (%s cfs), which drops the %d report years without a stoppage as if "
        "they held no record; not %s MGD, from the gauge alone (%s cfs), which leaves out the reports the guidance "
        "requires." % (k["design_flow_cfs"], k["withdrawal_mgd"], k["shortfall_mgd"], k["stage2_demand_mgd"], blocks,
                       rv["R1"]["block_mgd"], k["measured_years"], rv["R1"]["design_flow_cfs"], k["silent_years"],
                       rv["R0"]["block_mgd"], rv["R0"]["design_flow_cfs"]),
        "",
        "## 2. Critical Components",
        "",
        "1. The 50-year 7-day low flow at the intake: **%s cfs**." % k["design_flow_cfs"],
        "2. The withdrawal the permit allows at it: **%s MGD**; the Stage 2 shortfall: **%s MGD**." % (
            k["withdrawal_mgd"], k["shortfall_mgd"]),
        "3. The record fitted: **%d** gauged climatic years, **%d** report years with a measured flow and **%d** report "
        "years without a stoppage, each entered as a 7-day low flow above **%s** cfs." % (
            k["gauged_years"], k["measured_years"], k["silent_years"], k["suspension_flow_cfs"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Took each complete climatic year's 7-day low flow (April to March, the lowest mean of seven consecutive "
        "daily means) from the approved daily values in %s: %d years, 1951 to 2024 (climatic year 2025 left out: its "
        "winter is provisional)." % (W.FILES["gauge"], k["gauged_years"]),
        "2. Took each report year from %s: %d seasons the pumps stopped, with the lowest seven-day flow converted to "
        "cfs (gallons a day before 1921, second-feet after), %d years with no stoppage, %d reports not found and left "
        "out." % (W.FILES["reports"], k["measured_years"], k["silent_years"], k["missing_reports"]),
        "3. Read a year with no stoppage, under the 1893 agreement the transcription quotes, as a 7-day low flow above "
        "two million gallons a day (%s cfs)." % k["suspension_flow_cfs"],
        "4. Fitted the log-Pearson Type III of %s with the regional skew of -0.30 by maximum likelihood to all of it: "
        "the measured years at their flows, the years without a stoppage above %s cfs." % (W.FILES["guidance"],
                                                                                           k["suspension_flow_cfs"]),
        "5. Read the 50-year 7-day low flow, %s cfs, and the 10-, 25- and 100-year flows from the fit." % k["design_flow_cfs"],
        "6. Applied %s (the flow above the 0.50 cfs passby) and %s (2027 Stage 2 demand %s MGD, the smallest 0.1 MGD "
        "block covering the shortfall): %s MGD short, %s MGD reserved." % (W.FILES["permit"], W.FILES["plan"],
                                                                            k["stage2_demand_mgd"], k["shortfall_mgd"],
                                                                            c["block_mgd"]),
        "7. For each Stage 2 period in %s, summed each day's finished water from %s less Elm Hollow's water from %s, "
        "plus the Hollow Road wells (the historian's total until the telemetry failed on 2023-06-14, the operator's "
        "readings in %s after), and took the period's average and highest day." % (
            W.FILES["notices"], W.FILES["scada"], W.FILES["elmhollow"], W.FILES["welllog"]),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["memo"],
        "",
        "1. The recommended block: %s MGD (%s blocks of 0.1 MGD)." % (c["block_mgd"], blocks),
        "2. The 10-, 25-, 50- and 100-year 7-day low flows at the intake, the withdrawal the permit allows and the Stage "
        "2 shortfall at each:",
    ]
    for t in ("10", "25", "50", "100"):
        s = sc[t]
        short = ("%s MGD" % s["shortfall_mgd"]) if float(s["shortfall_mgd"]) > 0 else "none"
        lines.append("   - %s years: %s cfs, withdrawal %s MGD, shortfall %s" % (t, s["flow_cfs"], s["withdrawal_mgd"], short))
    lines += [
        "3. The recommended block stops covering the Stage 2 shortfall beyond the %s-year 7-day low flow (%s cfs)." % (
            fl["years"], fl["flow_cfs"]),
        "4. A chart of the annual 7-day low flows against recurrence interval: the fitted curve, the %d gauged years, the "
        "%d measured report years, and the 50-year flow of %s cfs marked with dashed lines." % (
            k["gauged_years"], k["measured_years"], k["design_flow_cfs"]),
        "5. For each Stage 2 period the Select Board declared since 2012, the average and the highest daily water "
        "supplied to the town's own distribution system:",
    ]
    for a in f["ask"]:
        lines.append("   - %s to %s: average %s MGD, highest %s MGD" % (a["start"], a["end"], a["average_mgd"],
                                                                     a["highest_mgd"]))
    lines += [
        "",
        "### %s" % W.GOLDEN["table"],
        "",
        "1. One row for each climatic year from 1894 to 2024 (%d rows): the year, its source, what the record shows and "
        "its 7-day low flow where the record gives one." % f["conformed_rows"],
        "2. %d gauged years and %d measured report years carry a flow; %d report years without a stoppage and %d "
        "reports not found carry none." % (k["gauged_years"], k["measured_years"], k["silent_years"], k["missing_reports"]),
        "",
    ]
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
