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
    rc = f["reflex_counts"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Sociology & Demography (income and poverty measurement).  ")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The FY2027 budget should carry %d Decision Coaching Grants, $%s, for %s.**" % (
        n, money(f["budget_usd"]), ", ".join(q[:-1]) + " and " + q[-1]))
    L.append("At each of these hospitals at least six percent of the 2025 applications from households within the "
             "free-care limit on their income over the twelve months before applying left the household owing more "
             "than half its balance; at no other hospital did. Not the 2025 policy's yearly figure read as that "
             "income, which finds %d hospitals because a household whose work follows a harvest, fishing or resort "
             "season was assessed on its best or its worst quarter. Not one calendar for each kind of work or for "
             "each region, which finds %s because one kind of work keeps different months in different regions and "
             "one region's kinds of work keep different months.\n"
             % (rc["policy_quarter"], ("%d either way" % rc["kind_calendar"]) if rc["kind_calendar"] ==
                rc["region_calendar"] else ("%d or %d" % (rc["kind_calendar"], rc["region_calendar"]))))
    L.append("## 2. Critical Components\n")
    L.append("1. The counsellors' 2025 first-review decisions: **%s** across the 31 hospitals" %
             money(f["first_reviews_total"]))
    L.append("2. Of them, applications from households within the free-care limit on their twelve-month income, each "
             "household's quarter put on a yearly basis by its region's calendar for its kind of work: **%s**, of "
             "which **%s** left the household owing more than half its balance" % (money(f["eligible_total"]),
                                                                                 money(f["owing_total"])))
    L.append("3. Hospitals at six percent or more: **%d** (%s)" % (n, ", ".join(q)))
    L.append("4. FY2027 budget line: **%d** grants at **$%s**, **$%s**\n" % (n, money(f["grant_usd"]),
                                                                             money(f["budget_usd"])))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Conformed the three hub extracts by the data guide's codes, put the Columbia extract's UTC times on "
             "Pacific time, joined H23's rows across both hubs, and kept each hospital's 2025 first-review decisions, "
             "without reconsiderations, pends, withdrawals or the presumptive screening (criteria 2.2): %s decisions."
             % money(f["first_reviews_total"]))
    L.append("2. Put every application's income on the 2025 policy's yearly basis, the three full months before the "
             "month of application times four (the Puget three-month total times four, the Willamette yearly figure, "
             "the Columbia monthly average times twelve).")
    L.append("3. For each region in %s and each kind of work, averaged that yearly figure, as a share of the guideline for "
             "the household's size, over every first-review decision of 2024 and 2025 by month of application, set "
             "each month against the twelve months' average, and divided each application's figure by its month's "
             "factor: its income over the twelve months before it applied (criteria 2.3)." % K.FILES["hospitals"])
    L.append("4. Kept the applications from households at or below 200 percent of the 2025 guideline for their size "
             "(section 3), %s, and counted those denied or approved at 25 percent (criteria 2.4), %s." % (
                 money(f["eligible_total"]), money(f["owing_total"])))
    L.append("5. Compared each hospital's share with six percent unrounded (criteria 2.1 and 2.5): %d hospitals "
             "qualify, at $%s each (criteria 1.2), $%s." % (n, money(f["grant_usd"]), money(f["budget_usd"])))
    L.append("6. For the assistance, took each write-off once (the adjustments extract repeats it on every account "
             "the approval covers, so a line can exceed its own account's balance in %s), credited it to the "
             "household's approval decided last before it posted (an approval on a later application for the same "
             "bill posts under the number the household's first application carried), kept the counsellors' 2025 "
             "approvals, subtracted each reversal posted through 31 March 2026 from the approval whose write-off it "
             "reverses, and counted the Willamette hub's twice-loaded December 2025 lines once: $%s thousand in all."
             % (K.FILES["accounts"], format(f["ask_a_total"], ",.1f")))
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
    L.append("1. Horizontal bar chart of the 31 hospitals' shares against the six-percent line, the %d qualifying "
             "hospitals highlighted." % n)
    text = "\n".join(L) + "\n"
    assert "—" not in text
    open(os.path.join(TASK, "submission.md"), "w").write(text)
    return text


if __name__ == "__main__":
    print(write())
