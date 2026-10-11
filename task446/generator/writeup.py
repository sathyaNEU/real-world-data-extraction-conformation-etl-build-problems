"""Write submission.md from the golden path (solve.py over target/), so every figure is computed once."""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve
from deliver import SHORT, m1

QL = ["30 Sep 2025", "31 Dec 2025", "31 Mar 2026", "30 Jun 2026", "30 Sep 2026"]


def f1(x):
    return "%.1f" % x


def main():
    pack = solve.Pack()
    res = sorted(solve.run(pack, "restated"), key=lambda r: -r["utilisation"])
    x = [r for r in res if r["item"] == "B1"][0]
    pit = [r for r in solve.run(pack, "pit") if r["item"] == "B1"][0]
    names = {r["item"]: pack.l1[solve.PROJ][r["top"]]["Entity.LegalName"] for r in res}
    L = []
    L.append("# task446 submission")
    L.append("")
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Banking, Credit & Financial Risk (obligor-group credit concentration and house-limit monitoring).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).")
    L.append("**Axis 2:** Explore/Discover, Hypothesize, Analyze/Validate, Synthesize, Recommend/Communicate.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Credit committee should approve GBP %sm of Kelderby Facilities Ltd's GBP %sm term loan.**" % (
        f1(x["approvable"]), f1(x["request"])))
    L.append("")
    L.append("Kelderby's projected 31 December 2026 exposure is GBP %sm against its GBP %sm house limit. "
             "Not GBP %sm, which builds each past quarter on the group as it stood then, so the Tarrant "
             "Hydraulics purchase reads as growth. Not the full GBP %sm, which would take Kelderby over its limit." % (
                 f1(m1(x["projected"])), f1(x["limit"]), f1(pit["approvable"]), f1(x["request"])))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. At 30 September 2026 the Kelderby group includes Tarrant Hydraulics Ltd and no longer includes Norbeck Coatings Ltd")
    L.append("2. Kelderby's quarter-end exposures on that membership are **%s** (GBP m, 30 Sep 2025 to 30 Sep 2026)" % (
        ", ".join(f1(m1(v)) for v in x["series"])))
    L.append("3. Kelderby's projected 31 December 2026 exposure is **GBP %sm**, utilisation **%s%%** of the GBP %sm limit" % (
        f1(m1(x["projected"])), f1(round(x["utilisation"] * 100, 1)), f1(x["limit"])))
    L.append("4. The approvable term loan is **GBP %sm**" % f1(x["approvable"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    steps = [
        "Took the six Part B requests and borrower LEIs from credit_committee_agenda_20261104.docx and each group's limit from house_limit_register_20260930.xlsx.",
        "Resolved every LEI to its Obligor Group on the 30 September 2026 GLEIF archive under Policy section 2 (consolidation chains, branches to head office, managed funds alone, lapsed records kept, merged LEIs to successors): Tarrant Hydraulics is Kelderby's, Norbeck Coatings is Meridale's.",
        "Measured each quarter-end's exposure under Policy section 3 from the loan extracts (the late Dublin file included, migrated facilities once), the treasury positions (ISIN file for blank issuer LEIs), the R2 rerun for the 30 Sep 2026 netting sets in GBP thousands less cash CSA collateral, all converted at Treasury rates.",
        "Assigned all five quarter-ends to the groups as constituted at 30 September 2026 (LMS-03 2.3): Kelderby runs %s." % ", ".join(f1(m1(v)) for v in x["series"]),
        "Projected 31 December 2026 as the 30 September exposure plus the least-squares slope (LMS-03 2.2): Kelderby GBP %sm, %s%% of GBP %sm." % (
            f1(m1(x["projected"])), f1(round(x["utilisation"] * 100, 1)), f1(x["limit"])),
        "Applied LMS-03 3.1 and 3.2 (term 100%, revolver 50%, GBP 0.1m steps, capped at the request) to every request.",
        "Recommendation: approve GBP %sm of Kelderby's GBP %sm term loan." % (f1(x["approvable"]), f1(x["request"])),
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### limit_check_2026-11-04.xlsx")
    L.append("1. Kelderby: approve GBP %sm of the GBP %sm term loan" % (f1(x["approvable"]), f1(x["request"])))
    L.append("2. One row per request, highest projected utilisation first, GBP m to one decimal:")
    for r in res:
        b = r["books"]
        L.append("   - %s %s (%s): drawn loans %s, undrawn commitments %s, securities %s, derivatives %s; "
                 "quarter-end exposures %s; projected 31 Dec 2026 %s; utilisation %s%%; approvable %s of %s requested" % (
                     r["item"], r["borrower"], names[r["item"]], f1(m1(b.get("loans_drawn", 0))),
                     f1(m1(b.get("undrawn", 0))), f1(m1(b.get("securities", 0))), f1(m1(b.get("derivatives", 0))),
                     ", ".join("%s %s" % (q, f1(m1(v))) for q, v in zip(QL, r["series"])),
                     f1(m1(r["projected"])), f1(round(r["utilisation"] * 100, 1)), f1(r["approvable"]), f1(r["request"])))
    L.append("")
    L.append("### projected_utilisation_2026Q4.png")
    L.append("1. Horizontal bars of projected utilisation per group in the workbook's order (%s), the house limit line marked at 100%%, "
             "Kelderby's bar annotated \"Approve GBP %sm of GBP %sm\", titled \"Kelderby can take GBP %sm of its GBP %sm term loan\"." % (
                 ", ".join("%s %s%%" % (SHORT[r["item"]], f1(round(r["utilisation"] * 100, 1))) for r in res),
                 f1(x["approvable"]), f1(x["request"]), f1(x["approvable"]), f1(x["request"])))
    txt = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "..", "submission.md"), "w") as fh:
        fh.write(txt)


if __name__ == "__main__":
    main()
