"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W

TAGS = ("**Domain:** Healthcare Delivery & Health Economics (payment, claims and health plan analytics: a Medicaid "
        "managed care plan's paid medical cost per member-month by primary care group).\n"
        "**Analytical objective:** Data Extraction & Conformation (ETL).")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve"}


def fmt(n):
    return "{:,}".format(int(n))


def _join(xs):
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else xs[0]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    F = W.FILES
    des, sec, mm, a = f["call"], f["sections"], f["member_months"], f["asks"]
    L = ["## Tags", "", TAGS, "",
         "## 1. Final Recommendation", "",
         "**Designate %s of the %s primary care groups for the 2027 Cost Performance Program: %s.**" % (
             WORDS[f["n_call"]], WORDS[f["n_groups"]], _join(des)),
         "Each group's paid medical cost per member-month for January to June 2026 is $%s or more once the "
         "member-months are the months its members were covered rather than the months the roster lists. The roster "
         "is the state's enrollment as processed by the 5th of each month: members who lost coverage at renewal and "
         "were reinstated back to the lapse are missing from the months they were later covered for, and members who "
         "died stay on it for months the state later took its capitation back for. The member-level lines of the "
         "state's capitation remittance record both. Counted on the roster alone, the groups with the most renewal "
         "churn look costlier and the groups with the most deaths look cheaper, and the designation would be %s." % (
             f["benchmark"], _join(f["roster_route"])),
         "",
         "## 2. Critical Components", "",
         "1. Groups at or above $%s per member-month: **%d** of %d." % (f["benchmark"], f["n_call"], f["n_groups"]),
         "2. Member-months: **%s** covered, against **%s** on the roster; **%s** member-months added from the "
         "remittance's reinstatement lines and **%s** roster member-months removed for recoupments." % (
             fmt(mm["golden"]), fmt(mm["roster"]), fmt(mm["added"]), fmt(mm["removed"])),
         "",
         "## 3. Step-by-Step Solution", "",
         "1. Took every group in %s (rule %s) and each member's group from pcp_group_id in %s, roster_month 2026-01 "
         "to 2026-06." % (F["groups"], sec["groups"], F["roster"]),
         "2. Took the lines of %s with a medicaid_id and a coverage_month from 2026-01 to 2026-06, mapped each "
         "medicaid_id to its member_id through the roster, and summed member_count per member and coverage month "
         "(a rate cell correction's two lines net to zero)." % F["remit"],
         "3. Covered member-months: the roster's member-months, plus each member and month netting above zero that "
         "the roster does not list, less each roster member-month netting below zero (rule %s)." % sec["rate"],
         "4. Summed paid_amount in %s over claims with service_from from 2026-01-01 to 2026-06-30 and paid_date by "
         "2026-10-31, by the member's group." % F["claims"],
         "5. Divided each group's paid cost by its covered member-months and designated every group at $%s or more "
         "(rule %s): %s." % (f["benchmark"], sec["designation"], _join(des)),
         "6. For the pharmacy summary (rule %s), took each claim_number in %s at its line with the latest "
         "processed_at, kept those whose fill_date falls from 2026-01-01 to 2026-06-30, classed each by its ndc in "
         "%s, summed paid_amount by class and counted the claims whose latest line paid more than zero as fills." % (
             sec["pharmacy"], F["rx"], F["classes"]),
         "",
         "## 4. Deliverable Answers", "",
         "### %s" % W.GOLDEN["workbook"], "",
         "1. Every primary care group, designated or not:"]
    for g in f["groups"]:
        L.append("   - %s: %s" % (g, "designated" if g in des else "not designated"))
    L.append("2. Every drug class, paid pharmacy cost (dollars, nearest dollar) and fills, January to June 2026:")
    for c in sorted(a["paid"]):
        L.append("   - %s: $%s; %s fills" % (c, fmt(a["paid"][c]), fmt(a["fills"][c])))
    L += ["", "### %s" % W.GOLDEN["memo"], "",
          "1. The designated groups: %s." % _join(des),
          "2. Bar chart of every group's paid medical cost per member-month, January to June 2026, against the "
          "$%s benchmark line, the designated groups' bars in orange." % f["benchmark"]]
    open(out_path, "w", encoding="utf-8").write("\n".join(L) + "\n")
