"""Emits task459's submission.md and generator/figures.json from the golden results (every figure computed, none typed)."""
import json

MEDICAL = "med_claims_svc2025_paid_thru_20260630.csv"


def fmt(n):
    return "{:,}".format(n)


def submission(res):
    rg, ag = res["regions"], res["agencies"]
    al = res["alloc"]
    call = ", ".join("%s USD %s" % (a, fmt(al[r])) for r, a in zip(rg[:-1], ag[:-1])) + \
        " and %s USD %s" % (ag[-1], fmt(al[rg[-1]]))
    counts = ", ".join("%s **%s**" % (r, fmt(res["counts"][r])) for r in rg)
    lines = [
        "## Tags", "",
        "**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics.",
        "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
        "## 1. Final Recommendation", "",
        "**Pay the 2027 in-home support budget of USD %s as %s.**" % (fmt(res["budget"]), call),
        "Each amount is the budget's share of the %s Covered Members counted in the agency's region, where the plan's "
        "2025 claims place each member on the most days. Not the address on file or the assigned primary care practice, "
        "which stay at the high-country homes that members who winter in the low desert leave from October to May. Not "
        "a count of claims or of days with a claim, which weights the summer months those members spend at home with "
        "their regular doctors." % fmt(res["covered"]), "",
        "## 2. Critical Components", "",
        "1. Covered Members (enrolled on every day of 2025, aged 75 or over on 31 December 2025): **%s**" % fmt(res["covered"]),
        "2. Covered Members by 2025 region: %s" % counts, "",
        "## 3. Step-by-Step Solution", "",
        "1. Kept the members in sc_member_extract_20260102.csv whose spans in sc_enrollment_spans_20260102.csv cover every "
        "day of 2025 and who were 75 or over on 31 December 2025 (Schedule B, B.3): %s Covered Members." % fmt(res["covered"]),
        "2. Placed each 2025 line in %s at the rendering practice's county on the date of service (provider_directory_20261001.xlsx, "
        "with provider_location_changes_2025.csv for practices that moved) and that county's region under B.1, leaving out "
        "place of service 81 (the reference laboratory bills from Phoenix) and telehealth (02 and 10)." % MEDICAL,
        "3. Added each paid fill in pbm_claims_2025_PVHP.txt (cardholder PV plus the member number) at its Arizona "
        "pharmacy's region in pharmacy_network_2025.csv, mail-order and specialty pharmacies being out of state, and each "
        "visit in ihs_visit_claims_2025.csv at its agency's region.",
        "4. Gave every day of 2025 the region of the member's nearest dated place and counted each Covered Member in the "
        "region holding the most days (B.4): the counts in block 2.",
        "5. Multiplied USD %s by each region's share of Covered Members, rounded to the nearest dollar (B.5): the "
        "allocations in block 1." % fmt(res["budget"]),
        "6. For members aged 65 to 74 on 31 December 2025, applied replacements and voids in ihs_visit_claims_2025.csv, "
        "chained claims for the same member, agency and date where one period starts as the previous ends into one Visit "
        "(B.7), and counted Visits by agency (AGENCY_NAME in the provider directory) and quarter, with their average "
        "minutes: block 4.",
        "7. For the same members, summed PAID_AMT in %s net of replacements and voids by the region of the rendering "
        "practice on the date of service: block 4." % MEDICAL,
        "8. Recommend the allocations in block 1 for the 2027 agreements.", "",
        "## 4. Deliverable Answers", "",
        "### member_regions_2025.csv", "",
        "1. One row per Covered Member, %s rows, each with its 2025 region and its 2027 agency; region counts as in "
        "block 2." % fmt(res["covered"]), "",
        "### home_care_allocation_2027.pdf", "",
        "1. 2027 allocations to the nearest dollar, with the Covered Members behind each:",
    ]
    for r, a in zip(rg, ag):
        lines.append("   - %s (%s): USD %s, %s Covered Members" % (a, r, fmt(al[r]), fmt(res["counts"][r])))
    lines.append("2. 2025 Visits by members aged 65 to 74, by calendar quarter:")
    for a in ag:
        v = res["visits"]
        lines.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % (a, fmt(v[(a, 1)]), fmt(v[(a, 2)]), fmt(v[(a, 3)]), fmt(v[(a, 4)])))
    lines.append("3. Average Visit length for those members, minutes to one decimal:")
    for a in ag:
        lines.append("   - %s: %.1f" % (a, res["minutes"][a]))
    lines.append("4. Plan-paid 2025 medical spend for those members by the region of the rendering practice on the date of "
                 "service, USD thousands to one decimal:")
    for r in rg:
        lines.append("   - %s: %s" % (r, "{:,.1f}".format(res["spend_k"][r])))
    lines.append("5. Bar chart of the 2027 allocation by agency with the Covered Members counted in each region (Figure 1).")
    return "\n".join(lines) + "\n"


def figures(res):
    rg, ag = res["regions"], res["agencies"]
    return {
        "budget": fmt(res["budget"]),
        "covered_members": fmt(res["covered"]),
        "allocation": {a: fmt(res["alloc"][r]) for r, a in zip(rg, ag)},
        "covered_by_region": {r: fmt(res["counts"][r]) for r in rg},
        "visits_by_quarter": {"%s Q%d" % (a, q): fmt(res["visits"][(a, q)]) for a in ag for q in (1, 2, 3, 4)},
        "visits_2025": {a: fmt(res["visits_total"][a]) for a in ag},
        "average_visit_minutes": {a: "%.1f" % res["minutes"][a] for a in ag},
        "medical_spend_usd_thousands": {r: "{:,.1f}".format(res["spend_k"][r]) for r in rg},
        "filed_constants": ["65", "74", "75", "81", "02", "10"],
    }


def write(res, sub_path, fig_path):
    with open(sub_path, "w", encoding="utf-8") as f:
        f.write(submission(res))
    with open(fig_path, "w", encoding="utf-8") as f:
        json.dump(figures(res), f, indent=1, sort_keys=False)
        f.write("\n")
