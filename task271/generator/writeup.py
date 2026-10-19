"""submission.md from figures.json: every figure the write-up states is one the generator wrote."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402


def money(x):
    return "{:,}".format(x)


def write(task):
    f = json.load(open(os.path.join(HERE, "figures.json")))
    names = [K.NAME[h] for h in K.ELIGIBLE]
    order = sorted(names, key=lambda n: f["ratio_unrounded"][n])
    ald, bra, far = K.NAME["A"], K.NAME["B"], K.NAME["C"]
    net, fer, elm = K.NAME["E"], K.NAME["G"], K.NAME["H"]
    centres = f["call"]["centres"]
    first = lambda n: n.split()[0]
    others = [v for k, v in f["earlier_share"].items() if k not in (ald, bra)]
    cl = f["filed"]["clauses"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Healthcare Delivery & Health Economics (provider quality and risk adjustment).  ")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Name %s, %s and %s as the 2027 Pancreatic Surgery Centres.**" % tuple(centres))
    L.append("Their ratios of observed to expected deaths within %d days are %.1f, %.1f and %.1f, the three lowest of the "
             "eight, Aldermoor at %.3f unrounded. Not %s (%.1f, %.3f unrounded), which reaches the three only when the "
             "expected deaths leave out the earlier operation on the pancreas or bile ducts that %.1f per cent of "
             "Aldermoor's patients bring (Aldermoor %.2f on the operation's own record). Not %s (%.1f) or %s (%.1f), above "
             "the line on either model.\n"
             % (f["filed"]["follow_up_days"], f["ratio"][centres[0]], f["ratio"][centres[1]], f["ratio"][centres[2]],
                f["ratio_unrounded"][ald], far, f["ratio"][far], f["ratio_unrounded"][far], f["earlier_share"][ald],
                f["rival"]["own_record_ratio"][ald], elm, f["ratio"][elm], bra, f["ratio"][bra]))
    L.append("## 2. Critical Components\n")
    L.append("1. Operations: **%s** pancreatic resections at the eight hospitals in 2023 to 2025, **%d** deaths within %d "
             "days." % (money(f["totals"]["operations"]), f["totals"]["deaths"], f["filed"]["follow_up_days"]))
    L.append("2. An earlier operation on the pancreas or bile ducts, from the patients' earlier admissions since 2016: "
             "**%.1f** per cent of Aldermoor's patients and **%.1f** per cent of Brackwell's, **%.1f** to **%.1f** per "
             "cent elsewhere; coefficient **%.2f** in the pooled model."
             % (f["earlier_share"][ald], f["earlier_share"][bra], min(others), max(others), f["earlier_coefficient"]))
    L.append("3. Expected deaths: " + ", ".join("%s **%.1f**" % (first(n), f["expected"][n]) for n in order) + ".")
    L.append("4. Ratios: " + ", ".join("%s **%.1f**" % (first(n), f["ratio"][n]) for n in order) + ".\n")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took every Appendix A resection on an adult at the eight hospitals with an operation date in 2023 to 2025 "
             "from %s, hospital IDs through %s: %s operations." % (K.FILES["d2023_2025"], K.FILES["hospitals"],
                                                                   money(f["totals"]["operations"])))
    L.append("2. Linked each patient's death through the person key in %s: %d deaths within %d days of the operation "
             "date (criteria %s)." % (K.FILES["deaths"], f["totals"]["deaths"], f["filed"]["follow_up_days"],
                                      cl["deaths"]))
    L.append("3. Read each patient's earlier admissions in every discharge file from 2016 through the person key and "
             "flagged an earlier operation on the pancreas or bile ducts (the pancreas and bile duct operations in %s): "
             "%.1f per cent of Aldermoor's patients." % (K.FILES["codes"], f["earlier_share"][ald]))
    L.append("4. Fitted one logistic model of death within %d days on the eight hospitals' operations together, on age, "
             "sex, a malignant diagnosis, the operation, the urgency, the seven conditions present on admission and the "
             "earlier operation (%.2f), and summed each hospital's predicted risks: Aldermoor %.1f expected deaths."
             % (f["filed"]["follow_up_days"], f["earlier_coefficient"], f["expected"][ald]))
    L.append("5. Divided each hospital's deaths by its expected deaths (criteria %s) and compared the ratios unrounded "
             "(%s): Aldermoor %.3f against Farrowmere %.3f." % (cl["expected"], cl["comparison"],
                                                              f["ratio_unrounded"][ald], f["ratio_unrounded"][far]))
    L.append("6. Counted each hospital's resections discharged January to June 2026 in %s, two records of one person at "
             "one hospital whose stays overlap counted as one operation: Aldermoor %d." % (K.FILES["revised"],
                                                                                         f["ask_a"][ald]))
    L.append("7. Followed each claim in %s through original_claim_id to the claim first received, took each chain's "
             "latest version, left out voided claims and their voids, added a stay's interim claims and averaged per "
             "stay: Aldermoor %s dollars." % (K.FILES["claims"], money(f["ask_b"][ald])))
    L.append("8. Named the three lowest ratios as the 2027 centres: %s, %s and %s.\n" % tuple(centres))
    L.append("## 4. Deliverable Answers\n")
    L.append("### pancreatic_centres_2027.xlsx\n")
    L.append("1. Ratio of observed to expected deaths within %d days, 2023 to 2025 resections, one decimal:"
             % f["filed"]["follow_up_days"])
    for n in order:
        L.append("   - %s: %.1f" % (n, f["ratio"][n]))
    L.append("2. The 2027 centres: %s, %s and %s." % tuple(centres))
    L.append("3. Pancreatic resections discharged January to June 2026:")
    for n in names:
        L.append("   - %s: %d" % (n, f["ask_a"][n]))
    L.append("4. Average amount allowed per stay for the cooperative's members' pancreatic resection stays discharged "
             "2023 to 2025, whole dollars:")
    for n in names:
        L.append("   - %s: $%s" % (n, money(f["ask_b"][n])))
    L.append("\n### pancreatic_centres_2027.png\n")
    L.append("1. Dot chart of the eight ratios from lowest to highest, the three centres in plum and the other five in "
             "grey, each dot labelled with its ratio, a dashed line at 1.0.")
    with open(os.path.join(task, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    write(os.path.dirname(HERE))
