"""submission.md, emitted from generator/figures.json so every figure it states is one the build computed."""
import json
import os

import common as K

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def money(x):
    return format(x, ",")


def write():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    q = f["call"]["qualify"]
    n = f["call"]["count"]
    names = ["%s %s" % (c, K.NAME[c]) for c in q]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science (resampling and simulation).  ")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The FY2027 budget should carry %d Decision Coaching Grants, $%s, for %s.**" % (
        n, money(f["budget_usd"]), ", ".join(q[:-1]) + " and " + q[-1]))
    L.append("At each of these hospitals the counsellors are six points or more less likely to approve right after "
             "an approval than right after a denial, once each working day is measured against its own "
             "determinations in any order; at no other hospital are they. Not holding each counsellor-day fixed, which puts most "
             "hospitals over the line because a short working day shows a drop after an approval with no counsellor "
             "swayed. Not pooling consecutive determinations, which clears nearly every hospital because days of "
             "easier applications string approvals together.\n")
    L.append("## 2. Critical Components\n")
    L.append("1. The counsellors' 2025 approvals and denials, by counsellor and local working day: **%s** "
             "determinations across the 31 hospitals" % money(f["determinations_total"]))
    L.append("2. Hospitals at six points or more against their own working days' determinations in any order: "
             "**%d** (%s)" % (n, ", ".join(q)))
    L.append("3. FY2027 budget line: **%d** grants at **$%s**, **$%s**\n" % (n, money(f["grant_usd"]),
                                                                             money(f["budget_usd"])))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Conformed the three hub extracts by the data guide's codes, put the Columbia extract's UTC times on "
             "Pacific time, and kept each hospital's counsellors' 2025 approvals and denials, first and on "
             "reconsideration, without pends, withdrawals or the presumptive screening (criteria 2.2): %s "
             "determinations." % money(f["determinations_total"]))
    L.append("2. Ordered each counsellor's determinations within each local working day by the recorded time and "
             "paired each with the one before it that day (criteria 2.3).")
    L.append("3. For each hospital, pooled over its counsellor-days, took the share approved right after a denial "
             "less the share approved right after an approval, and subtracted that contrast's expectation with each "
             "working day's determinations in every order and its approvals held (a day with k approvals among n "
             "gives k(k-1)/n approval-approval pairs in expectation), which measures the counsellors within their "
             "own day's applications (criteria 2.4).")
    L.append("4. Compared each measure with six points unrounded (criteria 2.1 and 2.6): %d hospitals qualify, "
             "%s." % (n, ", ".join(q)))
    L.append("5. Priced the grants at $%s each (criteria 1.2): $%s." % (money(f["grant_usd"]), money(f["budget_usd"])))
    L.append("6. For the assistance, took each counsellor-approved 2025 application's write-off once (the adjustments "
             "extract carries an approval's whole write-off on every account it covers, which is why a line can "
             "exceed its own account's balance in %s), subtracted the reversals posted through 31 March 2026 and "
             "counted the Willamette hub's twice-loaded December 2025 lines once: $%s thousand in all." % (
                 K.FILES["accounts"], format(f["ask_a_total"], ",.1f")))
    L.append("7. For the denials, counted the counsellors' 2025 denials for documents not received, reading code 2 "
             "before 1 July 2025 and code 1 from 1 July, when the reason list was renumbered (the denials that "
             "reconsiderations reopen carry code 2 to 30 June and code 1 after): %s in all." % money(f["ask_b_total"]))
    L.append("8. Recommendation: %d grants, $%s.\n" % (n, money(f["budget_usd"])))
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % K.DELIVERABLES[0])
    L.append("1. Number of grants: %d, the FY2027 budget line $%s" % (n, money(f["budget_usd"])))
    L.append("2. Whether each hospital qualifies, 31 hospitals in code order:")
    for c in K.CODES:
        L.append("   - %s %s: %s" % (c, K.NAME[c], f["verdict"][c]))
    L.append("3. Assistance written off on the counsellors' 2025 approvals, net of reversals posted by 31 March 2026, "
             "thousands of dollars to one decimal:")
    for c in K.CODES:
        L.append("   - %s: %s" % (c, format(f["ask_a"][c], ",.1f")))
    L.append("4. Counsellor denials in 2025 for documents not received, whole counts:")
    for c in K.CODES:
        L.append("   - %s: %s" % (c, money(f["ask_b"][c])))
    L.append("")
    L.append("### %s\n" % K.DELIVERABLES[1])
    L.append("1. Horizontal bar chart of the 31 hospitals' measures against the six-point line, the %d qualifying "
             "hospitals highlighted." % n)
    text = "\n".join(L) + "\n"
    assert "—" not in text
    open(os.path.join(TASK, "submission.md"), "w").write(text)
    return text


if __name__ == "__main__":
    print(write())
