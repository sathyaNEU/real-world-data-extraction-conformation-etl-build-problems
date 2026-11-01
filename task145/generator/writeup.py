"""task145 architecture 2: submission.md and metadata.json, every figure from figures.json."""
import json

import params as P

SCHOOL_LONG = P.SCHOOL_NAME
MONTHS = ["August", "September", "October", "November", "December"]
SPRING_YEAR = {"2023-24": "2024", "2024-25": "2025", "2025-26": "2026"}


def submission(fig, S, path):
    c = fig["call"]
    hl, cf = fig["hist_leavers"], fig["chronic_fall"]
    L = []
    w = L.append
    w("## Tags\n")
    w("> **Domain:** Education & Learning Sciences (learning analytics and early-warning models: a charter high school "
      "network's spring leavers forecast student by student from its student information system's attendance, course "
      "and enrolment exports).")
    w("> **Analytical objective:** Forecasting & Predictive Modeling.\n")
    w("## 1. Final Recommendation\n")
    w("**Fund %s of the Pathwise Bridge schedule for spring 2027 (%d seats, USD %s).** About %d of the %s students on "
      "roll for 5 January 2027 are expected to leave the network without completing by 30 June 2027, above Tier 1's %d "
      "seats and within %s's %d. The students who leave are the ones who were away for a week or more at a stretch in "
      "the fall, and those runs rose this fall while the family texts cut the scattered absences the chronic absence "
      "rate counts, so the early-warning indicators file the first tier.\n"
      % (c["tier"], c["seats"], "{:,}".format(c["price"]), c["expected"], "{:,}".format(fig["on_roll"]),
         P.TIERS[0][1], c["tier"], c["seats"]))
    w("## 2. Critical Components\n")
    w("1. Each student's chance of leaving is read off the fall's unbroken runs of instructional days missed (five or "
      "more in a row, rebuilt from the absence rows on each school's own calendar), not off the share of days missed.")
    w("2. Expected spring 2027 leavers: **%d**, above Tier 1's **%d** seats and within %s's **%d**."
      % (c["expected"], P.TIERS[0][1], c["tier"], c["seats"]))
    w("3. Leavers under Policy JF-7 among the students on roll on each spring's first day: **%d** in 2024, **%d** in "
      "2025 and **%d** in 2026." % (hl["2023-24"], hl["2024-25"], hl["2025-26"]))
    w("4. Students on roll for 5 January 2027: **%s**." % "{:,}".format(fig["on_roll"]))
    w("5. The network's fall chronic absence rate: **%.1f%%** in fall 2025 and **%.1f%%** in fall 2026.\n"
      % (cf["2025-26"], cf[P.CUR]))
    w("## 3. Step-by-Step Solution\n")
    steps = [
        "Read enrollment_records_2023-24_to_2026-27.csv as one student per state id, a record opened without one "
        "linked to the same student's earlier record by name and date of birth; where a student's exit from one of "
        "the network's schools was entered after their entry at the next, the earlier record ends the day before.",
        "Counted leavers per section 3 of board_policy_JF-7_bridge_program.pdf among the students on roll on each "
        "spring's first instructional day: exits coded DO, GE or EX (W3, W5 or W9 before July 2024, "
        "sis_code_reference.csv), and transfers (TI, TO, TU; W1, W2, WT) with no request in "
        "registrar_records_requests_2023-2026.csv within 45 days: %d, %d and %d." % (hl["2023-24"], hl["2024-25"],
                                                                                    hl["2025-26"]),
        "Read each fall day absent per section 1 of attendance_regulation_JH-R_2026-27.pdf on the minutes in "
        "attendance_absences_2023-24.csv and the portions or Mesa Vista periods in "
        "attendance_absences_2024-25_to_2026-27.csv against bell_schedules_2026-27.pdf, a day missed only where the "
        "student was absent at every school enrolled that day.",
        "Rebuilt each student's fall runs of five or more consecutive instructional days missed on each school's "
        "calendar in instructional_calendars_2023-24_to_2026-27.xlsx (weekends, holidays, non-student days and the "
        "October 2026 weather closure do not break a run): in springs 2024 to 2026, %.1f%% of students with no run "
        "left, %.1f%% with one and %.1f%% with two or more." % (fig["rate_no_run"], fig["rate_one_run"],
                                                             fig["rate_two_runs"]),
        "Priced each of the %s students on roll for 5 January 2027 at the 2024 to 2026 spring leaving rate of "
        "students with the same runs (none, one, two or more) and fall F grades in course_grades_2023-24_to_2026-27.csv "
        "(none, one, two or more): %.1f expected leavers." % ("{:,}".format(fig["on_roll"]), fig["expected_unrounded"]),
        "Took the smallest tier of pathwise_schedule_B_spring_2027.pdf with at least that many seats, per section 4 of "
        "JF-7: %s, %d seats, USD %s." % (c["tier"], c["seats"], "{:,}".format(c["price"])),
        "Ask A: each school's fall 2026 students enrolled ten or more instructional days there, one school a day, "
        "chronically absent on a tenth or more of them per JH-R section 3, each out-of-school suspension's days from "
        "behavior_incidents_2023-24_to_2026-27.csv counted absent beside the attendance rows.",
        "Ask B: each out-of-school suspension once per student and start date, the last-entered row standing (a "
        "hearing officer's reduction is a new row, often under another behaviour code), its days on the school's "
        "instructional days from the start while enrolled there, in the month each day falls.",
    ]
    for i, s in enumerate(steps, 1):
        w("%d. %s" % (i, s))
    w("")
    w("## 4. Deliverable Answers\n")
    w("### bridge_2027_board_paper.pdf\n")
    w("1. Tier to fund for spring 2027: %s (%d seats, USD %s)." % (c["tier"], c["seats"], "{:,}".format(c["price"])))
    w("2. Expected spring 2027 leavers: %d." % c["expected"])
    w("3. Chart: each tier's seats as a bar with the expected leavers marked against them.\n")
    w("### attendance_figures_2026.xlsx\n")
    w("1. Fall 2026 chronic absence rate, per cent to one decimal:")
    for s in P.SCHOOLS:
        for g in P.GRADES:
            w("   - %s, grade %d: %.1f" % (SCHOOL_LONG[s], g, fig["ask_a"]["%s %d" % (s, g)]))
    w("2. Out-of-school suspension days served in fall 2026, whole days:")
    for s in P.SCHOOLS:
        for m in MONTHS:
            w("   - %s, %s: %d" % (SCHOOL_LONG[s], m, fig["ask_b"]["%s %s" % (s, m)]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


FILES = {
    "enrollment_records_2023-24_to_2026-27.csv": "the network student information system's enrolment records, one "
    "row per student and school enrolment, 2023-24 to the December 2026 extract",
    "attendance_absences_2023-24.csv": "the legacy student information system's 2023-24 absence export, minutes "
    "absent by student and day",
    "attendance_absences_2024-25_to_2026-27.csv": "the current student information system's absence export from "
    "July 2024, one row per student, school and day absent, by session or period",
    "course_grades_2023-24_to_2026-27.csv": "semester course grades and credits by student and course section",
    "behavior_incidents_2023-24_to_2026-27.csv": "the behaviour system's incident and consequence log",
    "registrar_records_requests_2023-2026.csv": "the registrar's log of other schools' requests for students' records",
    "instructional_calendars_2023-24_to_2026-27.xlsx": "each school's board-approved calendar, one sheet a school year",
    "sis_code_reference.csv": "the student information system's code tables, with the legacy codes retired in 2024",
    "board_policy_JF-7_bridge_program.pdf": "the board's Bridge program policy (who it is sized for, leaving, the tier)",
    "attendance_regulation_JH-R_2026-27.pdf": "the network's attendance regulation for 2026-27",
    "bell_schedules_2026-27.pdf": "the schools' bell schedules and instructional minutes",
    "pathwise_schedule_B_spring_2027.pdf": "the Bridge provider's spring 2027 seat schedule",
    "bridge_seats_for_spring.eml": "the director of student services' request to the data office",
    "family_texts_fall_2026.csv": "the family-texting platform's message log for fall 2026",
    "transportation_routes_2026-27.csv": "the 2026-27 bus routes and stops by school",
    "school_climate_survey_spring_2026.xlsx": "the spring 2026 school climate survey summary by school",
}
DISTRACTORS = {
    "family_texts_fall_2026.csv": "the texts follow each unexcused absence and show when families were reached, but "
    "they record contact, not whether a student missed a day or left; every day missed is in the absence exports",
    "transportation_routes_2026-27.csv": "bus routes bear on getting to school, but no route or rider count is tied to "
    "a student, so nothing in it prices a student's chance of leaving",
    "school_climate_survey_spring_2026.xlsx": "belonging and safety bear on leaving, but the survey is a school-level "
    "summary from spring 2026 with no student detail, so it cannot price the students on roll",
}


def metadata(path):
    m = dict(task="task145", architecture=2,
             files={f: dict(role="distractor" if f in DISTRACTORS else "evidence",
                            source="synthetic, generated by task145/generator (seeded)", describes=d,
                            date=P.AS_OF.isoformat(), license="CC0-1.0") for f, d in FILES.items()},
             distractors=sorted(DISTRACTORS), distractor_reasons=DISTRACTORS, stated_inputs=["30 June 2027"],
             deliverables=["bridge_2027_board_paper.pdf", "attendance_figures_2026.xlsx"])
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1)
        fh.write("\n")
