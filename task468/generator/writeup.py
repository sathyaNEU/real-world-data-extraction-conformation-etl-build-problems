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
        "and continuation at each month on therapy, starting each member at the months they have already completed. "
        "Not last year's on-therapy members' following-year spend applied to this June's members, which gives weight "
        "management %d, severe asthma %d and migraine prevention %d (their 2026 members are new starters after the "
        "step therapy change, most of whom stop within months); not the class's spend from first fill, which gives oral "
        "oncology %d (its members on therapy have already passed the early discontinuation); not the trailing year "
        "or the June run-rate, which give hepatitis C %d (its courses end within twelve weeks)." % (
            rv["analog"]["GLP"], rv["analog"]["AST"], rv["analog"]["CGR"], rv["from_start"]["ONC"],
            rv["trailing"]["HCV"]),
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
        "4. Dated each member's therapy from the first fill in the class; members already filling in the first quarter "
        "of 2019 have an unseen start and sit in the longest-duration cell.",
        "5. For each class and each month on therapy, averaged the spend over the following twelve months of the "
        "members on therapy at a month end at that duration, over every month end from January 2019 whose twelve "
        "months are in the record (durations from 36 months pooled).",
        "6. Projected each caseload member at the duration they had reached on June 30, 2026, summed by class, and "
        "staffed one pharmacist per $1.5 million or part (charter 3.1).",
        "7. For the rebates, summed %s's lines with a 2025 utilization quarter, each product's rebate for a quarter "
        "counted once although the statement repeats it on each channel line." % W.FILES["rebates"],
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
    lines.append("4. Manufacturer rebates on 2025 utilization, $ thousand:")
    for c in W.CANDIDATES:
        lines.append("   - %s: {:,}".format(rb[c]) % name[c])
    lines.append("5. Bar chart of the pharmacists by class, on the Staffing sheet.")
    lines.append("")
    open(out_path, "w", encoding="utf-8").write("\n".join(lines))
