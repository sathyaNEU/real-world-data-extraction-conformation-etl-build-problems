"""submission.md, written from figures.json (every figure emitted, none typed)."""
import golden as GD
import pack as K
import world as W

MONTHS = GD.MONTHS


def write(path, fig):
    c, a, b, lad = fig["call"], fig["ask_a"], fig["ask_b"], fig["ladder"]
    L = []
    L += ["## Tags", "",
          "> **Domain:** Education & Learning Sciences (item response theory and test equating).",
          "> **Analytical objective:** Data Extraction & Conformation (ETL).", ""]
    L += ["## 1. Final Recommendation", "",
          "**Set the pass mark on Harrowgate Testing's theory paper at %d out of 60.** It holds the standard of 65 on "
          "Brindle Assessment's scale under AP-3, read through the candidates who failed Brindle's paper and sat "
          "Harrowgate's next, against Brindle's own resits matched on the first score. Not %d, the mark that carries "
          "the 2025 first-time pass rate onto the 2026 first-time candidates, a stronger cohort." % (
              c["pass_mark"], lad["same months a year earlier"]), ""]
    L += ["## 2. Critical Components", "",
          "1. The candidates measured on both papers are the %s who failed their one Brindle sitting and sat "
          "Harrowgate's paper next; a second sitting reads higher than a first on any paper." % "{:,}".format(c["n_cross_switch"]),
          "2. Brindle's resits of first-sitting fails in 2021 to 2025, matched on the first score, put **%.1f per "
          "cent** of those candidates at 65 or more on a second Brindle sitting." % (100 * c["p_equivalent"]),
          "3. On Harrowgate's paper %.1f per cent of them reach %d and %.1f per cent reach %d, so **%d** is the "
          "lowest raw mark no larger share reaches." % (100 * c["share_below_mark"], c["pass_mark"] - 1,
                                                       100 * c["share_at_mark"], c["pass_mark"], c["pass_mark"]),
          ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Tied every sitting to a person through %s (Brindle and Harrowgate candidate numbers to board numbers; "
          "board numbers sharing surname, initials and date of birth as one person), kept Brindle's SAT rows and "
          "Harrowgate's cleared and released marks once per sitting_ref, dated by the UK local date." % K.FILES["register"],
          "2. Took the candidates whose only Brindle sitting was a fail (under 65) and whose next sitting was "
          "Harrowgate's paper, with their first scaled score and their raw mark.",
          "3. Took every Brindle fail at a first sitting from 2021 to 2025 followed by a second Brindle sitting, and "
          "for each first score the share scoring 65 or more at the second.",
          "4. Averaged that share over the cross-switch candidates' first scores (AP-3 section 2's equivalent group): "
          "%.1f per cent." % (100 * c["p_equivalent"]),
          "5. Set the pass mark at the lowest raw mark the cross-switch candidates reach in no larger share: %d." % c["pass_mark"],
          "6. Counted, on the same people, each 2026 month's first-time and resitting candidates and each year's "
          "first sittings of Brindle's paper with their passes (a person's first sat sitting on either paper).",
          "7. Recommended %d out of 60." % c["pass_mark"], ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % GD.PDF, "",
          "1. Recommendation: set the pass mark on Harrowgate's theory paper at %d out of 60." % c["pass_mark"],
          "2. Chart: the share of the candidates who sat Harrowgate's paper reaching each raw mark, with the pass "
          "mark of %d drawn on it." % c["pass_mark"],
          "3. Candidates sitting the theory paper for the first time, and candidates resitting it, in each month of "
          "2026 to September, whole numbers:"]
    for i in range(9):
        k = "2026-%02d" % (i + 1)
        L.append("   - %s 2026: %s first time, %s resitting" % (MONTHS[i], "{:,}".format(a[k]["first_time"]),
                                                                  "{:,}".format(a[k]["resitting"])))
    L.append("4. Candidates who first sat Brindle's paper in each year from 2021 to 2025, and how many of them "
             "passed at that sitting, whole numbers:")
    for y, v in b.items():
        L.append("   - %s: %s first sat, %s passed" % (y, "{:,}".format(v["first_time"]), "{:,}".format(v["passed"])))
    L += ["", "### %s" % GD.CSV, "",
          "1. Every 2026 sitting of the theory paper to 30 September, one row each: the person's board number, the "
          "board number at the sitting, the UK date, the provider, the scale, the mark, the attempt, whether it was "
          "the first sitting and the result (65 on Brindle's scale, %d on Harrowgate's)." % c["pass_mark"], ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
