"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
QN = {"Q1": "January to March", "Q2": "April to June", "Q3": "July to September", "Q4": "October to December"}


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c, i, ci, po, py = f["cost"], f["increase"], f["continuance_increase"], f["put_off"], f["plan_year"]
    my, A, B = f["member_year"], f["ask_a"], f["ask_b"]
    call = f["call"]["maximum"]
    out = ["## Tags", "",
           "**Domain:** Healthcare Delivery & Health Economics, payment, claims and health plan analytics (a self-insured "
           "employer dental plan's 2027 annual maximum costed for collective bargaining, conformed from its claims "
           "administrator's two adjudication platforms, predetermination logs, eligibility spans, member crosswalk and "
           "network fee schedules).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**Agree a %s dollar annual maximum for 2027, not the union's 3,000.**" % call,
           "Costed under Finance Policy F-17, the %s dollar maximum adds USD %s per covered person month (USD %s against "
           "USD %s at the current 1,500), inside Board Resolution 2026-31's USD %s, and 3,000 dollars adds USD %s, over "
           "it. The 2025 claims alone put 3,000 dollars at USD %s, because %d members whose predetermination showed the "
           "1,500 dollar maximum reducing the plan's payment had that work done only after the plan year began again on "
           "1 January 2026; at a higher maximum the work falls in the plan year, USD %s of plan share at the 2027 fees, "
           "and 3,000 dollars no longer fits." % (
               call, i["2,000"], c["2,000"], c["1,500"], f["constants"]["limit"], i["3,000"], ci["3,000"], po["members"],
               po["amount"]), "",
           "## 2. Critical Components", "",
           "1. 2027 cost per covered person month under F-17 (the 2025 plan year at the 2027 fees): 1,500 dollars "
           "**USD %s**, 2,000 dollars **USD %s**, 3,000 dollars **USD %s**." % (c["1,500"], c["2,000"], c["3,000"]),
           "2. Increase over the current 1,500 dollar design against the mandate's USD %s: 2,000 dollars **USD %s**, "
           "3,000 dollars **USD %s**." % (f["constants"]["limit"], i["2,000"], i["3,000"]),
           "3. Predetermined work put off past 31 December 2025 and costed in the plan year: **%d** members, **USD %s** "
           "of plan share at the 2027 fees." % (po["members"], po["amount"]),
           "4. The 2025 plan year: **%s** covered persons, **%s** covered person months." % (
               "{:,}".format(py["persons"]), "{:,}".format(py["months"])), "",
           "## 3. Step-by-Step Solution", "",
           "1. Conformed Ridgeline's two platforms: Classic voided originals out and replacements in, Nexus superseded "
           "lines out, a Classic claim restated on Nexus taken from the restatement, every member through the July 2025 "
           "crosswalk.",
           "2. Took 2025's covered persons and covered person months from both eligibility files (Classic spans to 30 "
           "June 2025, its open end written 12/31/9999; Nexus spans from 1 July 2025, an open end blank).",
           "3. Priced each 2025 service line at the 2027 fee sheet with the deductible the plan applied to it and its "
           "class's coinsurance, frequency-denied lines out and the lines the maximum cut at their full share.",
           "4. Marked the 2025 predetermination requests whose estimated plan payment the maximum reduced (Nexus stamps "
           "read in Central time).",
           "5. Added to each person the estimated procedures of those requests not claimed for the same person, "
           "procedure and tooth in 2025 and claimed after 1 January 2026 within the estimate's 12 months, at the 2027 "
           "fee and coinsurance.",
           "6. Costed each maximum as the sum over 2025's covered persons of the lesser of the person's amount (with "
           "that work at a higher maximum) and the maximum, per covered person month, each increase against 1,500 at "
           "the same fees.",
           "7. Counted Schedule C requests by quarter of receipt (after 5:00 p.m. Central or on a non-business day, the "
           "next business day; a Nexus request every estimate for one member and dentist at one receipt time, answered "
           "at its last estimate) and those answered within five business days.",
           "8. Followed each child's orthodontic treatment across a change of orthodontist through the crosswalk, its "
           "year from the first banding, and summed the unpaid benefit of children in treatment and covered on 30 "
           "September 2026.", "",
           "## 4. Deliverable Answers", "",
           "### pembrook_dental_member_year_2025.csv", "",
           "1. One row per 2025 covered person: **%s** rows, **%s** covered person months." % (
               "{:,}".format(my["rows"]), "{:,}".format(my["months"])),
           "2. Column totals in dollars: put-off work at the 2027 fees **USD %s**; cost at 1,500 **USD %s**, at 2,000 "
           "**USD %s**, at 3,000 **USD %s**." % (my["put"], my["cost"]["1,500"], my["cost"]["2,000"],
                                                my["cost"]["3,000"]), "",
           "### pembrook_dental_maximum_2027.pdf", "",
           "1. Recommendation: agree a %s dollar maximum from 1 January 2027." % call,
           "2. Cost per covered person month: USD %s (1,500), USD %s (2,000), USD %s (3,000); increases USD %s and USD "
           "%s against the USD %s limit." % (c["1,500"], c["2,000"], c["3,000"], i["2,000"], i["3,000"],
                                            f["constants"]["limit"]),
           "3. Predetermination requests by quarter of receipt, received and answered within five business days:"]
    for q in sorted(A):
        out.append("   - %s (%s %s): %s received, %s answered within five business days" % (
            q, QN[q[-2:]], q[:4], "{:,}".format(A[q][0]), "{:,}".format(A[q][1])))
    out.append("4. Orthodontic treatment by the year it began, children still in treatment on 30 September 2026 and the "
               "plan's payments still owed for them:")
    for y in sorted(B):
        out.append("   - %s: %d %s, USD %s" % (y, B[y]["children"], "child" if B[y]["children"] == 1 else "children",
                                             B[y]["owed"]))
    out += ["", "### pembrook_dental_maximum_2027.svg", "",
            "1. Bar chart of each option's increase per covered person month, USD %s at 2,000 dollars and USD %s at "
            "3,000 dollars, against a dashed line at the mandate's USD %s: the 2,000 bar falls under the line and the "
            "3,000 bar rises over it." % (i["2,000"], i["3,000"], f["constants"]["limit"])]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
