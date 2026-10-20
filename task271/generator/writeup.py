"""submission.md from figures.json: every figure the write-up states is one the generator wrote."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402


def n(x):
    return format(x, ",")


def write(task):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    four = fig["call"]["regions"]
    below = fig["call"]["first_below"]
    sh = fig["share"]
    ar = fig["answer_rate"]
    oc = fig["outcomes"]
    rv = fig["rivals"]
    a, b = fig["ask_a"], fig["ask_b"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement error "
             "adjustment).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Trevanna should put the 2027 Community Engagement Support navigator teams in %s, %s, %s and %s.**\n"
             % tuple(four))
    L.append("Estimated over every member the survey sampled, reached or not, these four have the smallest shares of "
             "expansion members who worked 80 hours or more in March 2026 (%s, %s, %s and %s per cent). Not %s, which "
             "the interviewed members' own answers put among the four: members in work rarely answer a weekday daytime "
             "call, so the members never reached are mostly members in work, and %s's calls went out mostly by day "
             "from the Member Services Center. Not those answers reweighted to each region's age and sex, or the "
             "members reached late carried to the members never reached, which leave that gap in place and name %s "
             "again."
             % (sh[four[0]], sh[four[1]], sh[four[2]], sh[four[3]], " and ".join(rv["respondents_not_golden"]),
                " and ".join(rv["respondents_not_golden"]), " and ".join(rv["cells_not_golden"])))
    L.append("\n## 2. Critical Components\n")
    L.append("1. **%s** of the 15,000 sampled members were never reached, and the survey's answer is known for **%s** "
             "(%s completed interviews and %s members who declined but answered the key question)."
             % (n(oc["not_reached"]), n(oc["completed"] + oc["declined_key_answered"]), n(oc["completed"]),
                n(oc["declined_key_answered"])))
    L.append("2. Across all 15,000 sampled members the estimated share who worked 80 hours or more is **%s per cent**, "
             "against **%s per cent** of the members interviewed." % (fig["overall"]["estimated"],
                                                                   fig["overall"]["interviewed"]))
    L.append("\n## 3. Step-by-Step Solution\n")
    L.append("1. Took the 15,000 sampled cases in %s and their survey calls: Kestrelby's from %s (the February pilot's "
             "MW26P cases and the TEST calls left out) and the Member Services Center's MWIS outbound calls from %s, "
             "joined on member ID, each call placed in its window by Pacific time (weekday day, weekday evening, "
             "Saturday)." % (K.FILES["sample"], K.FILES["dialer"], K.FILES["crm"]))
    L.append("2. Read each case's calls in time order to the first that reached the member (dialer 1100 or 2110, CRM "
             "Spoke to member): %s completed, %s declined, %s never reached."
             % (n(oc["completed"]), n(oc["declined"]), n(oc["not_reached"])))
    L.append("3. Took the class from %s, total March hours of 80 or more for a completed interview and the key "
             "question's answer for a member who declined (TEST rows left out), known for %s members."
             % (K.FILES["interviews"], n(oc["completed"] + oc["declined_key_answered"])))
    L.append("4. Fitted a latent class callback model by EM to every sampled member's calls: each class's chance that "
             "a call in each window reaches the member, the same in every region; a reached member's chance of "
             "declining the same in either class; each region's share of the class; members of unknown class "
             "weighted by their posterior.")
    L.append("5. Averaged each region's 1,500 members (known class or posterior) and ranked the regions unrounded "
             "(criteria 2.1 to 2.4): %s." % ", ".join("%s %s" % (r, sh[r]) for r in fig["call"]["order"][:4]))
    L.append("6. Members covered on 1 October 2026 (criteria 3.1 and 3.2): the roster's members whose enrollment began "
             "by 1 October and had not ended, with members the change log terminated on or after 1 October restored "
             "(including those enrolled again later in October) and each member at the county before any move logged "
             "after 1 October, aged 19 to 64 on that day, by the county's region in %s." % K.FILES["regions"])
    L.append("7. Parents and caretakers (criteria 3.3): of those members, case heads, spouses and caretaker relatives "
             "in %s whose case had a child under 14 on 1 October 2026, from the children's birth dates and days in "
             "the case, each person counted once." % K.FILES["cases"])
    L.append("8. Named %s, %s, %s and %s for the track." % tuple(four))
    L.append("\n## 4. Deliverable Answers\n")
    L.append("### %s\n" % K.DELIVERABLES[0])
    L.append("1. Track regions, with each one's estimated share of expansion members aged 19 to 64 who worked 80 hours "
             "or more in March 2026, to the whole percent:")
    for r in four:
        L.append("   - %s: %s per cent" % (r, sh[r]))
    L.append("2. Members covered on 1 October 2026, aged 19 to 64, by region:")
    for c in K.CODES:
        L.append("   - %s: %s" % (K.NAME[c], n(a[K.NAME[c]])))
    L.append("3. Parents and caretaker relatives of a child under 14 on 1 October 2026, by region:")
    for c in K.CODES:
        L.append("   - %s: %s" % (K.NAME[c], n(b[K.NAME[c]])))
    L.append("\n### %s\n" % K.DELIVERABLES[1])
    L.append("1. Bar chart of the ten regions' estimated shares, smallest at the top, %s, %s, %s and %s highlighted "
             "above a line marking the four navigator teams, each region's whole percent beside its bar." % tuple(four))
    open(os.path.join(task, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    write(os.path.dirname(HERE))
