"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task281/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ORDER = ["HRC", "ACF", "TWC", "PCN", "PCS", "FFH", "OXG", "KPG"]
TITLES = [("CO", "Correctional Officer"), ("PCO", "Police Communications Operator"), ("FSA", "Forensic Security Aide"),
          ("HMW", "Highway Maintenance Worker")]
WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    u = f["units"]
    p = f["call"]["positions"]
    ev = f["evidence"]
    rt = f["route_totals"]
    nm = lambda k: u[k]["name"]
    placed = ", ".join("%s %d" % (nm(k), p[k]) for k in ORDER)
    out = ["## Tags", "",
           "**Domain:** General Statistics & Data Science (exploratory data analysis and distribution assessment).",
           "**Analytical objective:** Descriptive & Distribution Analysis.", "",
           "## 1. Final Recommendation", "",
           "**Place %d of the 60 relief positions (%s) and return %s to the Governor's reserve.**"
           % (f["call"]["total"], placed, WORD[f["call"]["returned_to_reserve"]]),
           "The positions are filled from the July 2027 entry classes, whose holders will be in their first year on "
           "post through FY2028, and the July 2025 classes were off post %.1f per cent of their scheduled hours in "
           "that year against %.1f per cent for the units' holders. Not the title's average holder, which leaves a "
           "relief position %.1f to %.1f hours on post a week and needs %d positions, %s short; not FY2026's weeks "
           "as they stood with its separations' vacant lines, %d; not the annual relief factor the standard "
           "replaced, %d."
           % (ev["july2025_off_post_pct"], ev["units_off_post_pct"], ev["title_average_hours_range"][0],
              ev["title_average_hours_range"][1], ev["default_path_total"], WORD[ev["default_path_short_by"]],
              rt["R1"], rt["mean"]),
           "",
           "## 2. Critical Components", "",
           "1. The FY2028 need carries the **%d** lines the position control holds vacant on 1 July 2027, in full "
           "until their first shifts on post (fiscal weeks **%d** to **%d**)." % (ev["vacant_lines_fy2028"],
                                                                                 ev["fill_weeks"][0],
                                                                                 ev["fill_weeks"][1]),
           "2. FY2026's **%s** hours of vacant line-shifts, lines vacated by separation, stay out of the FY2028 need "
           "(Budget Instruction 2024-07, 2.4)." % format(ev["fy2026_vacant_line_hours"], ","),
           "3. A relief position's holder is read as an entry-class graduate in the first year on post: the July "
           "2025 classes were off post **%.1f** per cent of their FY2026 scheduled hours, the units' holders **%.1f** "
           "per cent." % (ev["july2025_off_post_pct"], ev["units_off_post_pct"]),
           "",
           "## 3. Step-by-Step Solution", "",
           "1. Took Budget Instruction 2024-07 (2.1 to 3.4) with the Director's memo: each unit's complement is the "
           "smallest whole number of relief positions whose hours on post in an average FY2028 week reach its "
           "fifth-heaviest FY2028 week of backfill need, the positions filled from the July 2027 entry classes.",
           "2. Summed each unit's off-post hours by fiscal week of FY2026 from merrimont_shift_rosters_fy2026.csv "
           "(the latest export of each line and date, both systems' codes through timekeeping_status_codes.csv, "
           "training off post), leaving out the %s hours of vacant line-shifts (2.4)."
           % format(ev["fy2026_vacant_line_hours"], ","),
           "3. Added the %d lines position_control_fy2028_round_the_clock_units.csv carries vacant: eight hours on each "
           "scheduled day (days_off left out) before first_shift_on_post, and from it the new holder's off-post share "
           "of those hours."
           % ev["vacant_lines_fy2028"],
           "4. Rated a relief position at 40 hours less the off-post share of the July 2025 classes over FY2026 "
           "(academy_class in hr_employee_extract_2026-10-01.csv), by title: %.1f per cent off post overall."
           % ev["july2025_off_post_pct"],
           "5. For overtime worked, summed the OT lines' hours and the CTE and CTS lines' credited hours over their credit "
           "(1.5 and 1.0, payroll_earnings_codes.csv; MOU 14.2) for FY2026 work dates, each piece once (a later check "
           "paying the same employee, work date, start_time and hours again is a second payment), at the post_unit of "
           "the accepted offer in overtime_offer_log_fy2026.csv with the same employee_id, post_date and start_time, "
           "else the employee's own unit (MOU 14.3), the line's home_timekeeper (SL-0410 is Thornmere); OTN and OTR "
           "lines carry pay only.",
           "6. For people at each unit, counted once everyone with an OT, CTE or CTS piece dated in FY2026 placed at the unit "
           "as in step 5, joining each employee whose seniority_date precedes the hire_date to the separated record "
           "with the same seniority_date and title.",
           "7. For people over 600 hours, summed overtime worked as in step 5 over each joined person and counted those "
           "over 600 hours under the title held in FY2026.",
           "8. Cut each unit's %d weekly needs at the fifth-heaviest and divided by its title's relief hours, "
           "rounding up: %s, %d of the 60, %s returned to the reserve."
           % (ev["weeks"], placed, f["call"]["total"], WORD[f["call"]["returned_to_reserve"]]),
           "",
           "## 4. Deliverable Answers", "",
           "### fy2028_relief_positions_by_unit.xlsx", "",
           "1. Relief positions placed for FY2028 (whole positions):"]
    for k in ORDER:
        out.append("   - %s: %d" % (nm(k), p[k]))
    out.append("   - All units: %d of the 60; %d returned to the Governor's reserve" % (f["call"]["total"],
                                                                                   f["call"]["returned_to_reserve"]))
    out.append("2. Overtime hours worked at each unit in FY2026 (nearest hour):")
    for k in ORDER:
        out.append("   - %s: %s" % (nm(k), format(f["ask_a_overtime_hours_by_unit"][k], ",")))
    out.append("3. People who worked overtime at each unit in FY2026:")
    for k in ORDER:
        out.append("   - %s: %d" % (nm(k), f["ask_b_people_by_unit"][k]))
    out.append("4. People who worked more than 600 hours of overtime in FY2026, by the title they held that year:")
    for t, tn in TITLES:
        out.append("   - %s: %d" % (tn, f["ask_c_people_over_600_hours"][t]))
    out += ["", "### fy2028_weekly_backfill_need.png", "",
            "1. Eight panels, one a unit, of the FY2028 weekly backfill need against the hours the unit's relief "
            "positions work on post a week, the weeks above that line (four at most a unit) highlighted."]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
