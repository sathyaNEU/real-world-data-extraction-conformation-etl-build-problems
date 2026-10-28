"""task464 architecture 8: submission.md, drafted from figures.json so no figure in it is typed."""
import json, os
import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    f = json.load(open(os.path.join(BASE, "generator", "figures.json")))
    L = W.LABEL
    order = sorted(W.CODES, key=lambda c: -f["corrected_share_pct"][c])
    cents = sorted(f["ask2_started"])
    n = format(f["withdrawals_total"], ",")
    o = []
    o += ["## Tags",
          "**Domain:** Education & Learning Sciences (text analysis: learners' free-text exit comments coded against a manual).",
          "**Analytical objective:** Descriptive & Distribution Analysis.", ""]
    o += ["## 1. Final Recommendation",
          "**Our 2027 retention budget line should target caring responsibilities.**",
          "Caring responsibilities account for %.1f per cent of 2025/26 withdrawals against work hours clash at %.1f, "
          "a gap of %.1f points. Not work hours clash, which leads the coded counts at %.1f per cent only because "
          "%.1f per cent of the comments coded to it are about caring. Not other or not stated, which leads the "
          "moderation file's own mix only because every comment coded OT is moderated."
          % (f["call_share_pct"], f["runner_up_share_pct"], f["gap_points"], f["coded_share_pct"]["WH"],
             f["wh_coded_belonging_cr_pct"]), ""]
    o += ["## 2. Critical Components",
          "1. Coded shares of the %s withdrawals: work hours clash **%.1f** per cent, caring responsibilities **%.1f**"
          % (n, f["coded_share_pct"]["WH"], f["coded_share_pct"]["CR"]),
          "2. Of the moderated comments coded work hours clash, **%.1f** per cent belong to caring responsibilities"
          % f["wh_coded_belonging_cr_pct"],
          "3. Share of withdrawals that happened for caring responsibilities **%.1f** per cent, for work hours clash **%.1f**"
          % (f["call_share_pct"], f["runner_up_share_pct"]), ""]
    o += ["## 3. Step-by-Step Solution",
          "1. Stacked withdrawals_autumn_winter_2025.csv and withdrawals_spring_summer_2026.json on the spring export's "
          "term codes, kept one row per withdrawal reference (the late-keyed winter withdrawals sit in both) and "
          "normalised the typed reason codes: %s withdrawals." % n,
          "2. Counted the withdrawals by coded reason over the four terms: work hours clash %.1f per cent, caring "
          "responsibilities %.1f." % (f["coded_share_pct"]["WH"], f["coded_share_pct"]["CR"]),
          "3. Took, within each coded reason in coding_moderation_2025_26.csv, the split of the moderating coder's "
          "categories, the return being drawn by code as quality_assurance_procedure.pdf sets out: %.1f per cent of "
          "moderated work hours clash comments belong to caring responsibilities." % f["wh_coded_belonging_cr_pct"],
          "4. Carried each code's split onto that code's share of the year's withdrawals and summed by reason: caring "
          "responsibilities %.1f per cent, work hours clash %.1f." % (f["call_share_pct"], f["runner_up_share_pct"]),
          "5. Built learner-courses from enrolments_2025_26.csv at the five centres in site_directory.csv on the learner "
          "number and the course reference, linking each course that course_catalogue_2025_26.csv plans over winter "
          "and spring but which has no spring rows to the one spring course at the same centre whose learners are all "
          "its continuing learners (%d links), and summed each learner-course's planned hours once from the catalogue: "
          "six area totals." % f["cutover_links"],
          "6. Attributed each learner-course to the centre of its first term's row and counted it completed where any "
          "of its rows reads completed: five started counts and five completed shares.",
          "7. Named the reason with the largest share of withdrawals: caring responsibilities, %.1f points ahead of "
          "work hours clash." % f["gap_points"], ""]
    o += ["## 4. Deliverable Answers", "", "### withdrawal_reason_composition_2025_26.csv",
          "1. Share of 2025/26 withdrawals that happened for each reason, six rows, per cent to one decimal place:"]
    o += ["   - %s: %.1f" % (L[c], f["corrected_share_pct"][c]) for c in order]
    o += ["", "### retention_target_2027.xlsx",
          "1. Reason the 2027 retention budget line targets: caring responsibilities, %.1f per cent" % f["call_share_pct"],
          "2. Runner-up: work hours clash, %.1f per cent" % f["runner_up_share_pct"],
          "3. Gap between them: %.1f points" % f["gap_points"],
          "4. Bar chart of the six shares by reason on the Reason composition sheet, caring responsibilities picked out",
          "5. Planned guided hours of the learner-courses the five centres started in 2025/26, by curriculum area, whole hours:"]
    o += ["   - %s: %s" % (a, format(f["ask1_planned_hours"][a], ",")) for a in W.CURRICULUM]
    o += ["6. Learner-courses started in 2025/26 and the share of them that completed, by centre, per cent to one decimal place:"]
    o += ["   - %s: %s started, %.1f completed" % (c, format(f["ask2_started"][c], ","), f["ask2_completed_pct"][c])
          for c in cents]
    open(os.path.join(BASE, "submission.md"), "w").write("\n".join(o) + "\n")
    print("  submission.md")


if __name__ == "__main__":
    main()
