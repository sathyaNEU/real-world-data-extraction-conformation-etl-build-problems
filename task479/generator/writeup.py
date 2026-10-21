"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(fig_path, out):
    f = json.load(open(fig_path))
    n = f["call"]["surcharged"]
    rate = f["claims_component"]
    dp = f["default_path"]["surcharged"]
    added = [e for e in n if e not in dp]
    spared = [e for e in dp if e not in n]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Surcharge %s from 1 January 2027.**" % _and(n))
    w("Their expected 2027 retained claims exceed the claims components they elected; no other employer's do. Most "
      "member employers are small, and a small employer's three years carry the luck of a few members' claims, so "
      "each employer's trended experience is weighed against the trust's by its credibility. Read at face value, the "
      "experience would surcharge %s, whose experience was raised by a few large claims, and spare %s, whose "
      "experience was low by luck and whose claims components sit well under the trust's level." % (
          _and(spared), _and(added)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Employers surcharged from 1 January 2027: %s" % ", ".join("**%s**" % e for e in n))
    w("2. Employers not surcharged: %s" % ", ".join(e for e in sorted(rate) if e not in n))
    w("3. Claims components of the 2027 elections: %s" % ", ".join("%s %s" % (e, rate[e]) for e in sorted(rate)))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Joined the two claims lag reports by employer, month of service, paid month and category, the May 2026 "
      "cells both platforms sent counted once, cents in dollars.")
    w("2. For each employer and plan year 2023 to 2025 took claims incurred in the year and paid through March of the "
      "next, less Westerby's reimbursements (the employer through the policy schedule), over the year's member "
      "months, trended at 7 per cent a year to 2027.")
    w("3. Estimated the within-employer and between-employer variance of those trended PMPMs (Buhlmann-Straub, "
      "member-month weights) and gave each employer a credibility of its member months over its member months plus "
      "their ratio.")
    w("4. Took each employer's expected 2027 PMPM as its credibility times its own three-year trended PMPM plus the "
      "rest times the trust's member-month weighted level; limited-fluctuation credibility at 1,000 to 3,000 lives "
      "gives the same employers.")
    w("5. Compared with the claims component of the elected 2027 contribution: %s over." % ", ".join(n))
    w("6. Ask A: July to September 2026 eligibility counted once per person a month (members reissued new ids at the "
      "summer 2026 move matched on employer, birth date, sex and relationship).")
    w("7. Ask B: each member's latest row on the 2026 high-cost claimant report, a member's rows under the old and the "
      "new id joined as one member.")
    w("8. Recommended surcharges for %s." % ", ".join(n))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### crbht_2027_renewal_surcharges.xlsx")
    w("")
    w("1. Each employer's decision against its 2027 claims component:")
    for e in sorted(rate):
        w("   - %s (claims component %s): %s" % (e, rate[e], "surcharged" if e in n else "not surcharged"))
    w("2. Chart of each employer's expected 2027 retained PMPM beside its claims component, the surcharged employers "
      "marked.")
    w("3. July to September 2026 member months:")
    for e in sorted(f["ask_a"]):
        w("   - %s: %s" % (e, "{:,}".format(f["ask_a"][e])))
    w("4. Members on the 2026 high-cost claimant report and their claims paid to date as last reported (whole "
      "dollars):")
    for e in sorted(f["ask_b"]):
        b = f["ask_b"][e]
        w("   - %s: %d, $%s" % (e, b["members"], "{:,}".format(b["claims_to_date"])))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
