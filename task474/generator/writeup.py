"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def fmt(n):
    return "{:,}".format(int(n))


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    regs = [r["region"] for r in f["regions"]]
    council = {r["region"]: r["council"] for r in f["regions"]}
    a, av, cells, asks = f["amounts"], f["average"], f["cells"], f["asks"]
    rel, snap, mid = f["rivals"]["release_shares"], f["rivals"]["snap_shares"], f["rivals"]["middle_year"]
    off = f["rivals_off"]
    moved = [g for g in regs if rel[g] != a[g]]
    g1, g2 = "Greater Ormsby", "Mill River Valley"
    lines = [
        "## Tags",
        "",
        "**Domain:** Survey Research & Official Statistics (official time-series production: an annual model-based "
        "poverty series rebuilt on new county-equivalents, its 2020 to 2022 years produced by temporal "
        "disaggregation with SNAP recipients benchmarked town by town to the survey's five-year level).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**Split the $%s as follows: %s.**" % (fmt(f["fund"]), _join(["%s $%s" % (council[g], fmt(a[g])) for g in regs])),
        "The split follows the nine regions' 2020-2024 average residents in poverty (together %s), with each former "
        "county's 2020, 2021 and 2022 estimate divided among its towns by their SNAP recipients that year scaled to "
        "each town's own 2020-2024 survey count. Not the split the five-year release's town shares give (%s $%s, "
        "%s $%s, %s of the nine amounts off), because that release is an average over 2020 to 2024 and carries the "
        "2021 relocations out of Ormsby and Wexport into 2020 and 2021; not the split the year's SNAP recipients "
        "give (%s $%s, %s off), because recipients per resident in poverty differ by town (the survey count runs "
        "from %.2f to %.2f times the recipients); not the release read as 2022 and moved by SNAP (%s $%s, %s off), "
        "because the release describes the whole 60 months." % (
            fmt(f["average_sum"]), g1, fmt(rel[g1]), g2, fmt(rel[g2]), WORD[off["release_shares"]],
            g1, fmt(snap[g1]), WORD[off["snap_shares"]], f["ratio_range"][0], f["ratio_range"][1],
            [g for g in regs if mid[g] != a[g]][0], fmt(mid[[g for g in regs if mid[g] != a[g]][0]]),
            WORD[off["middle_year"]]),
        "",
        "## 2. Critical Components",
        "",
        "1. Average residents in poverty, 2020-2024, nearest hundred: %s." % _join(
            ["%s **%s**" % (g, fmt(av[g])) for g in regs]),
        "2. The nine averages sum to **%s**." % fmt(f["average_sum"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Took each year's estimate as last published (rule %s): the former counties' 2020, 2021 and 2022 from "
        "Table 2 of %s, %s and %s, and the planning regions' 2023 (Table 2) and 2024 (Table 1) from %s; the former "
        "counties total %s, %s and %s." % (
            f["rule_sections"]["latest"], W.FILES["rel2022"], W.FILES["rel2023"], W.FILES["rel2024"],
            W.FILES["rel2025"], fmt(f["county_totals"]["2020"]), fmt(f["county_totals"]["2021"]),
            fmt(f["county_totals"]["2022"])),
        "2. Matched the towns in %s to %s (DSS writes them in capitals with abbreviations) and took each town's mean "
        "monthly RECIPIENTS in each calendar year 2020 to 2024, the year the methods note defines." % (
            W.FILES["snap"], W.FILES["codes"]),
        "3. Took each town's B17001_002 from %s through town_geoid_region_basis (the average over January 2020 to "
        "December 2024, per the table notes) and divided it by the town's mean recipients over 2020 to 2024: the "
        "ratio runs from %.2f to %.2f." % (W.FILES["acs"], f["ratio_range"][0], f["ratio_range"][1]),
        "4. Estimated each town's residents in poverty in 2020, 2021 and 2022 as its mean recipients that year times "
        "its ratio, divided each former county's estimate among its towns in proportion to those figures and summed "
        "the towns' parts into regions (rule %s), then averaged each region's five years with equal weight (rule "
        "%s): the averages sum to %s." % (f["rule_sections"]["division"], f["rule_sections"]["average"],
                                           fmt(f["average_sum"])),
        "5. Read %s counting Wexmoor's April 2026 upload once (the extract holds it twice), kept service dates from July 1, "
        "2025 to June 30, 2026, matched Corbin's pre-2026 client numbers to its new ones through %s, and placed each "
        "client in the town given by the town edits in %s for the service date (effective_date), since each row "
        "carries its record's town when the extract was cut; counted distinct people per agency and region and "
        "shared each agency's Unexpended balance in %s by those counts (rule %s): $%s in all." % (
            W.FILES["extract"], W.FILES["conversion"], W.FILES["audit"], W.FILES["closeout"],
            f["rule_sections"]["balances"], fmt(asks["unexpended_total"])),
        "6. Counted each energy assistance (EA) payment once per household_no and service_date, since the extract "
        "repeats it on the row of every household member, in the town the audit trail gives for the payment date "
        "(rule %s)." % f["rule_sections"]["energy"],
        "7. Split $%s in proportion to the unrounded averages and rounded each allocation to the nearest $%s (rule "
        "%s): %s." % (fmt(f["fund"]), fmt(f["rounding"]["amounts"]), f["rule_sections"]["allocation"],
                     _join(["%s $%s" % (g, fmt(a[g])) for g in regs])),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.DELIVERABLES[0],
        "",
        "1. Residents in poverty by planning region, nearest hundred, in the file's order:",
    ]
    for g in regs:
        c = cells[g]
        lines.append("   - %s: 2020 %s; 2021 %s; 2022 %s; 2020-2024 average %s" % (
            g, fmt(c["2020"]), fmt(c["2021"]), fmt(c["2022"]), fmt(av[g])))
    lines += ["", "### %s" % W.DELIVERABLES[1], "", "1. FY2027 allocations, nearest $%s:" % fmt(f["rounding"]["amounts"])]
    for g in regs:
        lines.append("   - %s: $%s" % (council[g], fmt(a[g])))
    lines += ["2. Bar chart of the nine FY2027 allocations, one bar per council with its amount, below the "
              "allocation table.",
              "3. Each council's share of the former county agencies' unexpended FY2026 balances, nearest $%s:" % (
                  fmt(f["rounding"]["dollars"]))]
    for g in regs:
        lines.append("   - %s: $%s" % (council[g], fmt(asks["carry"][g])))
    lines.append("4. People each share is counted on:")
    for g in regs:
        lines.append("   - %s: %s" % (council[g], fmt(asks["people"][g])))
    lines.append("5. Energy assistance the agencies paid in FY2026 to households in each council's towns, nearest $%s:"
                 % fmt(f["rounding"]["dollars"]))
    for g in regs:
        lines.append("   - %s: $%s" % (council[g], fmt(asks["energy"][g])))
    open(out_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")
