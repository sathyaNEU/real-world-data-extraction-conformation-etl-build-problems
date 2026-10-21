"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(fig_path, out):
    f = json.load(open(fig_path))
    n = f["call"]["raised"]
    e = f["expected_pmpm"]
    rate = f["claims_component"]
    dp = f["default_path"]
    missed = [d for d in n if d not in dp["raised"]]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Raise the contributions of %s from 1 January 2027.**" % _and(n))
    w("Their expected plan year 2026 plan-paid claims are $%s per member per month against claims components of $%s; "
      "every other district is under its claims component. %s moved from plan MVA ($500 deductible) to plan MVC "
      "($3,000) in 2026, and a plan MVC year carries less of its claims in January to June, so their first half "
      "is completed by the factor of the districts that ran plan MVC through 2025; completed by their own 2025 on plan "
      "MVA they read $%s and look covered." % (
          _and(str(e[d]) for d in n), _and(rate[d] for d in n), _and(missed),
          _and(str(dp["expected_pmpm"][d]) for d in missed)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Districts raised from 1 January 2027: %s" % ", ".join("**%s**" % d for d in n))
    w("2. Expected plan year 2026 plan-paid claims PMPM, to the nearest $10: %s" % ", ".join(
        "%s **%d**" % (d, e[d]) for d in sorted(e)))
    w("3. Claims components of the 2026 contribution rates: %s" % ", ".join("%s %s" % (d, rate[d]) for d in sorted(rate)))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Joined the two claims lag reports by district, month of service, paid month and category, the May 2026 "
      "cells both platforms sent counted once, cents in dollars.")
    w("2. Counted each district's member months from the eligibility file, 2025 and January to June 2026.")
    w("3. Took each district's plan in 2025 and 2026 from the benefit designs PDF.")
    w("4. For each plan, pooled the districts that ran it through 2025: plan year 2025 PMPM over January to June 2025 "
      "PMPM.")
    w("5. Multiplied each district's January to June 2026 PMPM by the factor of its 2026 plan, so the four districts "
      "that moved to plan MVC are completed on plan MVC's year, not their own 2025.")
    w("6. Compared with the 2026 claims component: %s over." % ", ".join(n))
    w("7. Ask A: July to September 2026 eligibility counted once per person a month (members reissued new ids when "
      "their district moved payroll matched on district, birth date, sex and relationship).")
    w("8. Ask B: each member's latest 2026 advisory, the district through the 2026 policy schedule, a claimant file "
      "reopened under a member's new id joined to the member's earlier one.")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### mvshc_january_2027_contribution_review.xlsx")
    w("")
    w("1. Expected plan year 2026 plan-paid claims PMPM (nearest $10) against the 2026 claims component, and the call:")
    for d in sorted(e):
        w("   - %s: %d against %s, %s" % (d, e[d], rate[d], "raised" if d in n else "not raised"))
    w("2. Chart of each district's expected PMPM beside its claims component, the raised districts marked.")
    w("3. July to September 2026 member months:")
    for d in sorted(f["ask_a"]):
        w("   - %s: %s" % (d, "{:,}".format(f["ask_a"][d])))
    w("4. 2026 specific advisories: members on advisory and their incurred claims to date as last reported (whole "
      "dollars):")
    for d in sorted(f["ask_b"]):
        b = f["ask_b"][d]
        w("   - %s: %d, $%s" % (d, b["members"], "{:,}".format(b["claims_to_date"])))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
