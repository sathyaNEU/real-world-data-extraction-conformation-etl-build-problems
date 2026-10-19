"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W


def lst(items):
    items = list(items)
    return ", ".join(items[:-1]) + " and " + items[-1] if len(items) > 1 else items[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    ph, sp, cl, rb, rv = f["call"]["pharmacists"], f["spend_m"], f["caseload"], f["rebates_k"], f["rivals"]
    name = {c: W.CLASSES[c]["name"] for c in W.CANDIDATES}
    staffing = "; ".join("%s %d" % (name[c], ph[c]) for c in W.CANDIDATES)
    lines = [
        "## Tags",
        "",
        "**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics: two pharmacy "
        "benefit managers' specialty claim files conformed into one repriced record of fills, from which each class's "
        "program-year spend for the members now on therapy is projected).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**Staff the Specialty Clinical Pharmacy Program with %d clinical pharmacists for July 2026 to June 2027: %s.**"
        % (f["call"]["total"], staffing),
        "Each class's managed spend is its members on therapy on June 30, 2026 carried forward by the class's own spend "
        "and continuation at each month of an episode of therapy, starting each member at the months their current "
        "episode has run; a member back on a drug after a lapse of more than %d days starts a new episode. Not the same "
        "projection counted from each member's first fill in the class, which gives weight management %d, severe asthma "
        "%d and migraine prevention %d (%d in all), because the members who came back to those drugs in 2026 after the "
        "step therapy change would be projected like the long-standing members who never stopped; not last year's "
        "on-therapy members' following-year spend applied to this June's members, which gives weight management %d; not "
        "the trailing year, which gives hepatitis C %d (its courses end within twelve weeks)." % (
            f["episode_gap_days"], rv["first_fill"]["GLP"], rv["first_fill"]["AST"], rv["first_fill"]["CGR"],
            sum(rv["first_fill"].values()), rv["analog"]["GLP"], rv["trailing"]["HCV"]),
        "",
        "## 2. Critical Components",
        "",
        "1. Members on therapy on June 30, 2026 (the caseloads): %s." % "; ".join(
            "%s {:,}".format(cl[c]) % c for c in W.CANDIDATES),
        "2. Projected managed spend for the program year, $ million at the 2026 schedule: %s; total %d." % (
            "; ".join("%s %d" % (c, sp[c]) for c in W.CANDIDATES), f["spend_total_m"]),
        "3. Pharmacists at one per $1.5 million of managed spend or part: %s; total %d." % (
            "; ".join("%s %d" % (c, ph[c]) for c in W.CANDIDATES), f["call"]["total"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Conformed %s and %s into one record of fills: reversed claims removed with the claims they reverse "
        "(Orrin's REVERSAL lines, Tallis's R status), members linked to plan IDs through %s, Orrin's 10-digit NDCs "
        "padded to 11 digits, each NDC's class from %s." % (W.FILES["orrin"], W.FILES["tallis"], W.FILES["crosswalk"],
                                                           W.FILES["drugs"]),
        "2. Priced every fill at %s: units times the unit price plus the dispensing fee (charter 2.2)." % W.FILES["prices"],
        "3. Took each class's caseload: members with a fill whose days' supply reaches June 30, 2026 (charter 2.1).",
        "4. Split each member's fills in a class into episodes of therapy, a new episode starting at a fill more than "
        "%d days after every earlier supply had run out, and dated each member's months on therapy from the start of "
        "the episode; a member already filling in the first quarter of 2019 has an unseen start and sits in the "
        "longest-duration cell." % f["episode_gap_days"],
        "5. For each class and each month of an episode, averaged the spend over the following twelve months of the "
        "members on therapy at a month end at that month, over every month end from January 2019 whose twelve months "
        "are in the record (months from 36 on pooled).",
        "6. Projected each caseload member at the month of the episode they had reached on June 30, 2026, summed by "
        "class, and staffed one pharmacist per $1.5 million or part (charter 3.1).",
        "7. For the rebates, took %s's contract quarters 2025-Q1 to 2025-Q4 (a contract year runs February to "
        "January, the only calendar on which its units tie to the claims), each product's quarterly rebate once "
        "although the statement repeats it on each channel line, plus January 2025's units at contract quarter "
        "2024-Q4's rebate per unit." % W.FILES["rebates"],
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["workbook"],
        "",
        "1. Clinical pharmacists by class:",
    ]
    for c in W.CANDIDATES:
        lines.append("   - %s: %d" % (name[c], ph[c]))
    lines.append("2. Total: %d pharmacists." % f["call"]["total"])
    lines.append("3. Managed spend for July 2026 to June 2027, $ million:")
    for c in W.CANDIDATES:
        lines.append("   - %s: %d" % (name[c], sp[c]))
    lines.append("4. Manufacturer rebates on fills dispensed in 2025, $ thousand:")
    for c in W.CANDIDATES:
        lines.append("   - %s: {:,}".format(rb[c]) % name[c])
    lines.append("5. Bar chart of the pharmacists by class, on the Staffing sheet.")
    lines.append("")
    open(out_path, "w", encoding="utf-8").write("\n".join(lines))
