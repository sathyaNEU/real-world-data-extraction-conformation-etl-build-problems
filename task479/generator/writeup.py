"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def write(fig_path, out):
    f = json.load(open(fig_path))
    n = f["call"]["notices"]
    r = f["retained_pmpm"]
    rate = f["rates"]
    dp = f["default_path"]
    extra = [g for g in dp["notices"] if g not in n]
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Send 2027 funding true-up notices to %s and %s only.**" % (", ".join(n[:-1]), n[-1]))
    w("Their expected 2027 retained claims are $%s per member per month against claims components of $%s; every "
      "other group is under its rate. Not the %d groups (%s) that trending 2025 retained claims also puts over: "
      "their 2025 experience carries members at or near the $250,000 specific deductible, who cost the plan no more "
      "than $250,000 in 2027 whatever the trend, so the trend on their claims lands with Arbor Ridge." % (
          ", ".join(r[g] for g in n[:-1]) + " and " + r[n[-1]], ", ".join(rate[g] for g in n[:-1]) + " and " +
          rate[n[-1]], len(extra), ", ".join(extra)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Groups with a notice: %s" % ", ".join("**%s**" % g for g in n))
    w("2. Expected 2027 retained claims PMPM, whole dollars: %s" % ", ".join("%s **%s**" % (g, r[g]) for g in sorted(r)))
    w("3. Claims components elected for 2027, whole dollars: %s" % ", ".join("%s %s" % (g, rate[g]) for g in sorted(rate)))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. From the two claims lag reports took each group's claims incurred in 2025 and paid through 31 March 2026, "
      "medical and pharmacy, the May 2026 cells the new platform re-sent counted once, cents in dollars.")
    w("2. Counted each group's 2025 member months from the enrollment file.")
    w("3. From Arbor Ridge's 2025 large claimant report took each claimant's 2025 claims, the group through the 2025 "
      "policy schedule.")
    w("4. Trended the group's 2025 claims two years at 7.5 per cent, and took off each large claimant's trended claims "
      "above $250,000: the specific deductible applies to 2027 claims, so each member's claims are trended before it.")
    w("5. Divided by the 2025 member months and compared with the claims component of the elected 2027 rate: %s over."
      % ", ".join(n))
    w("6. Ask A: 2026 enrollment counted once per person a month (members reissued new ids at a payroll vendor change "
      "matched on group, birth date, sex and relationship); 2026 incurred claims January to August paid through "
      "September 2026 over those member months.")
    w("7. Ask B: each claimant's latest 2026 advisory, the group through the 2026 policy schedule, a claimant file "
      "reopened under a member's new id joined to the member's earlier one.")
    w("8. Recommended notices to %s." % ", ".join(n))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### mba_2027_funding_true_up.xlsx")
    w("")
    w("1. Expected 2027 retained claims PMPM against the 2027 claims component, whole dollars, and the notice:")
    for g in sorted(r):
        w("   - %s: %s against %s, %s" % (g, r[g], rate[g], "notice" if g in n else "no notice"))
    w("2. Chart of each group's expected 2027 retained PMPM beside its claims component.")
    w("3. January to August 2026 member months and paid claims PMPM (dollars to the cent):")
    for g in sorted(f["ask_a"]):
        a = f["ask_a"][g]
        w("   - %s: %s, $%s" % (g, "{:,}".format(a["member_months"]), a["paid_pmpm"]))
    w("4. 2026 specific advisories: members flagged and their claims to date as last reported (whole dollars):")
    for g in sorted(f["ask_b"]):
        b = f["ask_b"][g]
        w("   - %s: %d, $%s" % (g, b["members"], "{:,}".format(b["claims_to_date"])))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
