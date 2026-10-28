"""submission.md, drafted from figures.json only."""
import params as P

SB_TITLE = {b[0]: b[2] for b in P.SKILL_BUILDERS}


def n(x):
    return "{:,}".format(int(x))


def write(path, F):
    L, T = F["chosen"], F["total"]
    lines = []
    a = lines.append
    a("## Tags")
    a("")
    a("**Domain:** Education and learning sciences (learning analytics and early-warning models).")
    a("**Analytical objective:** Forecasting and predictive modelling.")
    a("")
    a("## 1. Final Recommendation")
    a("")
    a("**Set the spring in-class skill builders at %d problems before the five-problem check.**" % L)
    a("At %d problems Units 4 to 7 are expected to produce about %s failed checks against the %s funded reteach places; "
      "6 problems would produce about %s, over the places, and 10 problems about %s, longer than the places need. "
      "Not the homework record replayed, where students stopped at three right in a row and finished over several "
      "evenings, which puts even 6 problems inside the places. Not a learning curve fitted across sittings, which "
      "reads the loss between evenings as slow learning and puts every length over the places."
      % (L, n(T[str(L)]), n(F["places"]), n(T["6"]), n(T["10"])))
    a("")
    a("## 2. Critical Components")
    a("")
    a("1. Expected failed checks at 6 problems: **%s**" % n(T["6"]))
    a("2. Expected failed checks at 8 problems: **%s**" % n(T["8"]))
    a("3. Expected failed checks at 10 problems: **%s**" % n(T["10"]))
    a("")
    a("## 3. Step-by-Step Solution")
    a("")
    a("1. Stacked pellmore_problem_log_2025-26_aug_dec.csv (Eastern local time) with "
      "pellmore_problem_log_2026_jan_jun.csv and pellmore_problem_log_2026-27_to_2026-10-23.csv (UTC put on Eastern "
      "time), mapped accounts to students through pellmore_student_link.csv (staff test "
      "accounts have no link and drop out) and each assignment to its skill builder through "
      "pellmore_assignments_2025-2027.csv.")
    a("2. Ordered each student's first attempts on each skill builder and split them into sittings, a new sitting "
      "starting after a break of more than three hours; for every problem, counted the student's earlier problems in "
      "the same sitting and in earlier sittings.")
    a("3. Fitted first-attempt correctness on a normal random intercept per student (spread by Laplace maximum "
      "likelihood), an easiness per skill builder and, per skill builder, one slope on each of the two counts.")
    a("4. For each of the %s seventh graders on roll on 23 October 2026 (grade7_roster_2026-10-23.xlsx) and each of "
      "skill builders 4 to 7, computed the chance of fewer than 3 of 5 check problems right after a set of 6, 8 or "
      "10 problems in one sitting (no earlier-sitting problems), averaged over the student's ability given their fall "
      "practice, and summed: about %s, %s and %s failed checks." % (n(F["on_roll"]), n(T["6"]), n(T["8"]), n(T["10"])))
    a("5. Applied spring_2027_grade7_math_plan.docx: the shortest length whose expected failed checks fit the %s "
      "places is %d problems." % (n(F["places"]), L))
    a("6. Counted the problems on skill builders 4 to 7 in pellmore_problem_log_2026_jan_jun.csv by students "
      "in pellmore_student_link.csv, by skill builder, at the school sis_archive/enrollment_history_2025-26.csv shows "
      "them attending on the Eastern-time day each problem was started (the log's school_code is each account's school "
      "when the export ran on 19 October 2026, and problems started between two enrollments count for no school).")
    a("")
    a("## 4. Deliverable Answers")
    a("")
    a("### spring_practice_set_length.xlsx")
    a("")
    a("1. Expected failed checks by set length, Units 4 to 7, nearest 250:")
    for Lx in F["lengths"]:
        a("   - %d problems: %s" % (Lx, n(T[str(Lx)])))
    a("2. Recommended set length: %d problems" % L)
    a("3. Expected failed checks at %d problems by spring unit, nearest 250:" % L)
    for sb in P.SPRING:
        a("   - Unit %s (%s): %s" % (sb, SB_TITLE[sb], n(F["unit"][sb])))
    a("4. 2025-26 skill-builder problems on each of Units 4 to 7 by the school the student attended that day, whole "
      "problems:")
    for code in sorted(F["problems"]):
        u = F["problems"][code]
        a("   - %s %s: Unit 4 %s, Unit 5 %s, Unit 6 %s, Unit 7 %s" % (code, F["school_names"][code], n(u["4"]), n(u["5"]),
                                                                    n(u["6"]), n(u["7"])))
    a("")
    a("### spring_reteach_memo.docx")
    a("")
    a("1. Recommends %d-problem sets, with about %s expected failed checks against the %s places, and gives 6 and 10 "
      "problems at about %s and %s." % (L, n(T[str(L)]), n(F["places"]), n(T["6"]), n(T["10"])))
    a("2. Explains why the homework record is not carried over: the run-of-three stop and the loss between evenings.")
    a("")
    a("### spring_reteach_forecast.png")
    a("")
    a("1. Stacked bars of expected failed checks by unit at 6, 8 and 10 problems, each labelled with its total (about "
      "%s, %s and %s), the %s places as a dashed line, and the %d-problem bar outlined as the recommendation."
      % (n(T["6"]), n(T["8"]), n(T["10"]), n(F["places"]), L))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
