"""Write task464/submission.md from generator/figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402


def _and(names):
    return ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]


def n(v):
    return "{:,}".format(int(v))


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    c = F["call"]
    nm = F["names"]
    sh = {d: W.short_name(d) for d in W.APPLICANTS}
    lv = F["level1"]
    br = F["bridge"]
    reg = F["regression"]
    k1 = F["boundaries"][0]
    F_ = W.FILES
    cut = F["cuts"]["grade8"][0]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Education & Learning Sciences (test equating and linking: a retiring state reading test's "
             "grade 8 scores placed on the new test's scale through a single-group bridge study).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Fund %s.**" % _and(["%s (%s)" % (nm[d], n(lv[d])) for d in c["funded"]]))
    L.append("Each count is the applicant's grade 9 and 10 students on the October 1, 2026 roll whose latest grade 8 "
             "result is at Level 1, with the 2025 retiring-test scores placed on the new scale by a concordance that "
             "matches the two tests' score distributions in the bridge study (retiring scores of %d and below at Level "
             "1). %s, the first left out at %s, trails %s by %d. Not the slate that places each 2025 score at its "
             "regression prediction (%d and below), which funds %s in %s's place: the regression line is flatter than "
             "the line linking the scales, so it puts %.1f per cent of the bridge students at Level 1 against %.1f per "
             "cent on the new test itself.\n" % (
                 k1, sh[c["first_out"]], n(lv[c["first_out"]]), sh[c["sixth"]], c["gap"], reg["boundary"],
                 sh[[d for d in reg["funded"] if d not in c["funded"]][0]], sh[[d for d in c["funded"]
                                                                              if d not in reg["funded"]][0]],
                 br["share_reg_l1"], br["share_new_l1"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Retiring-test grade 8 scores placed at Level 1 on the new scale: **%d and below** (the new test's "
             "Level 2 begins at %d)." % (k1, cut))
    L.append("2. Students at Level 1 in %s, the sixth: **%s**; in %s, the first left out: **%s**; the gap: **%d**." % (
        sh[c["sixth"]], n(lv[c["sixth"]]), sh[c["first_out"]], n(lv[c["first_out"]]), c["gap"]))
    L.append("3. Bridge students at Level 1 on the new test: **%.1f** per cent; placed by the regression: **%.1f** per "
             "cent." % (br["share_new_l1"], br["share_reg_l1"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took the spells in %s covering October 1, 2026 (entry on or before it, exit blank or on or after "
             "it) in grades 9 and 10 of the fourteen applicants in %s." % (F_["enrollment"], F_["rules"]))
    L.append("2. Took every grade 8 session with a score from %s (SCR rows, make-ups included, blank state "
             "identifiers filled from %s) and %s (Scored rows), and kept each student's latest." % (
                 F_["glra"], F_["crosswalk"], F_["slm"]))
    L.append("3. Linked the two scales with the %s pairs of %s by equipercentile matching of the two score "
             "distributions; linear linking and every percentile convention give the same placement: retiring scores "
             "of %d and below at Level 1 (new-test scores below %d)." % (n(br["n"]), F_["bridge"], k1, cut))
    L.append("4. Counted each applicant's students at Level 1 and ranked them; %s is sixth with %s and %s first left "
             "out with %s." % (sh[c["sixth"]], n(lv[c["sixth"]]), sh[c["first_out"]], n(lv[c["first_out"]])))
    L.append("5. Rejected the regression of the new score on the retiring score: placed by it only %.1f per cent of the "
             "bridge students reach Level 1 against %.1f per cent on the new test, and it funds %s." % (
                 br["share_reg_l1"], br["share_new_l1"], sh[[d for d in reg["funded"] if d not in c["funded"]][0]]))
    L.append("6. For grade 7, took each applicant's own middle schools from %s (rows from nonpublic schools in %s left "
             "out), the Scored grade 7 rows of %s, and Level 1 below the grade 7 cut of %d adopted in %s, not the "
             "file's performance level, reported before the Board set the grade 7 cuts." % (F_["directory"], F_["nonpublic"], F_["slm"], F["cuts"]["grade7_level2"],
                                         F_["resolution"]))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % W.GOLDEN["workbook"])
    L.append("1. The six districts funded: %s." % _and([nm[d] for d in c["funded"]]))
    L.append("2. Each applicant's grade 9 and 10 students on the October 1, 2026 roll at Level 1:")
    for d in sorted(W.APPLICANTS, key=lambda d: (-lv[d], d)):
        L.append("   - %s: %s" % (nm[d], n(lv[d])))
    L.append("3. The first district left out: %s, %s students, %d below %s." % (
        nm[c["first_out"]], n(lv[c["first_out"]]), c["gap"], nm[c["sixth"]]))
    L.append("4. Each applicant's grade 7 students at Level 1 in spring 2026 and their share of its grade 7 students "
             "with a score:")
    for d in sorted(W.APPLICANTS, key=lambda d: (-lv[d], d)):
        L.append("   - %s: %s students, %.1f per cent" % (nm[d], n(F["grade7_level1"][d]), F["grade7_share"][d]))
    L.append("5. A horizontal bar chart of the fourteen applicants' students at Level 1 on the Chart sheet, the six "
             "funded in dark green and the rest in grey, a dashed line under %s labelled with the sixth's %s and the "
             "first left out's %s." % (sh[c["sixth"]], n(lv[c["sixth"]]), n(lv[c["first_out"]])))
    L.append("")
    L.append("### %s\n" % W.GOLDEN["table"])
    L.append("1. One row for each of the %s counted students (grade 9 or 10 on an applicant's October 1, 2026 roll with "
             "a grade 8 result): the state identifier, district, school, grade, the test and year of the latest grade 8 "
             "result, its scale score and its level on the new scale." % n(F["conformed_rows"]))
    L.append("2. Students at each level: Level 1 %s, Level 2 %s, Level 3 %s, Level 4 %s." % tuple(
        n(F["conformed_levels"][str(k)]) for k in (1, 2, 3, 4)))
    txt = "\n".join(L) + "\n"
    assert "—" not in txt and "–" not in txt
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return txt
