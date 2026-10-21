"""submission.md, drafted from generator/figures.json: every figure in blocks 1 to 4 is one the generator wrote."""
import json


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def write(fig_path, out):
    f = json.load(open(fig_path))
    aw = f["call"]["awarded"]
    dp = f["default_path"]["awarded"]
    sa = f["per_fte_standalone"]
    branches = sorted(f["ask_a"])
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality).")
    w("**Analytical objective:** Data Extraction & Conformation (ETL).")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**Award the 2027-28 instructional investment grant to %s.**" % _and(aw))
    w("They have the lowest fiscal 2026 instruction expense per FTE student. %s are branch campuses whose instruction "
      "sits inside their parents' returns: each parent's instruction is split among the parent and its branches by the "
      "cost of the credit hours each taught, at the cost per credit hour by level the sixteen campuses that report "
      "alone show, and the branches teach mostly lower-division hours. Split by FTE students instead, the branches "
      "carry their systems' averages and the five would be %s." % (
          _and([u for u in aw if u not in sa]), _and(dp)))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. Awarded: %s" % ", ".join("**%s**" % u for u in aw))
    w("2. Not awarded: every other reporting unit, %d campuses" % (26 - len(aw)))
    w("3. Instruction expense per FTE of the campuses reporting alone, whole dollars: %s" % ", ".join(
        "%s %s" % (u, "{:,}".format(sa[u])) for u in sorted(sa)))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took fiscal 2026 instruction (F1C011) from the finance return and 2025-26 FTE (FTEUG plus FTEGD) from the "
      "12-month return; the branches carry PRCH_F 2 and zero, their parents PRCH_F 1.")
    w("2. Summed the board's credit hour file by campus and level, campus codes to UNITID through the code list; it "
      "ties to the 12-month return's credit hours.")
    w("3. Fitted instruction expense on lower-division, upper-division and graduate credit hours across the sixteen "
      "campuses that report alone (least squares, no intercept).")
    w("4. Split each parent's reported instruction among the parent and its branches in proportion to the fitted cost "
      "of the credit hours each taught, keeping the parent's total.")
    w("5. Divided by each campus's FTE and took the five lowest: %s." % ", ".join(aw))
    w("6. Ask A: the branches' fall 2026 census rows, a student's course counted once (a cross-listed course carries "
      "the student under both course numbers at one meeting), undergraduate hours over 15 plus graduate over 12.")
    w("7. Ask B: each student counted once per branch, the rows under the old and the new student id joined by birth "
      "date, sex, home ZIP code and first term (birth date, sex and ZIP alone are shared by different students, "
      "and the new systems recoded some majors).")
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### lhecb_2027-28_instructional_investment_awards.xlsx")
    w("")
    w("1. The five awards: %s." % ", ".join(aw))
    w("2. Chart of every reporting unit's instruction expense per FTE, lowest first, the awards marked.")
    w("3. Fall 2026 FTE students at each branch campus (one decimal):")
    for u in branches:
        w("   - %s: %s" % (u, f["ask_a"][u]))
    w("4. Unduplicated fall 2026 headcount at each branch campus:")
    for u in branches:
        w("   - %s: %s" % (u, "{:,}".format(f["ask_b"][u])))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
