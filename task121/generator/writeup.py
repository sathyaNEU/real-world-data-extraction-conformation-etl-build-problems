"""submission.md, drafted from generator/figures.json so every figure it states is one the generator computed.

    python3 task121/generator/writeup.py"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
GROUPS = [("MAIN", "Marlvale Main Line"), ("VALE", "Hollin Vale"), ("COAST", "Coastway"), ("BRANCH", "Pellow Branch"),
          ("LINK", "Corrington Link")]
LABEL = {"crowding": "Crowding", "punctuality": "Punctuality", "on-board staffing": "On-board staffing", "fares": "Fares"}


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c, s, b, ev, rt = f["call"], f["shares"], f["bridge_points"], f["evidence"], f["routes"]
    cs, ef = ev["condition_share_pct"], ev["effect_points_if_met"]
    out = ["## Tags", "",
           "**Domain:** Marketing & Consumer Research (customer satisfaction driver analysis).",
           "**Analytical objective:** Root-Cause Analysis.", "",
           "## 1. Final Recommendation", "",
           "**Crowding accounts for most of the fall: %d of the %.1f points by which the share of passengers "
           "satisfied overall fell, from %.1f%% in spring 2025 to %.1f%% in spring 2026. Fund the crowding remedy.**"
           % (c["points"], s["fall_points"], s["spring_2025"], s["spring_2026"]),
           "Measured on the conditions each surveyed passenger's own train ran under, journeys on a train carrying "
           "more passengers than seats rose from %.1f%% to %.1f%% and such a journey ends satisfied %.1f points less "
           "often. Not on-board staffing, which the tracker's attribute ratings put first (%d points by derived "
           "importance) because passengers on a crowded train mark every aspect down; not %d point with the ratings "
           "held as controls."
           % (cs["crowded"]["2025"], cs["crowded"]["2026"], ef["crowded"], ev["default_path"]["points"],
              rt["R1_points"]),
           "",
           "## 2. Critical Components", "",
           "1. Every questionnaire is linked through its batch to the train it was handed out on and the passenger's "
           "own stations, so each of the four drivers is the Schedule 7 (3.1) condition of that passenger's trip.",
           "2. Crowding: **%.1f%%** of journeys in spring 2025, **%.1f%%** in spring 2026, **%.1f** points less "
           "likely satisfied when met, **%d** points of the fall." % (cs["crowded"]["2025"], cs["crowded"]["2026"],
                                                                   ef["crowded"], b["crowding"]),
           "3. On-board staffing **%d**, punctuality **%d**, fares **%d** points: trains without staff rose from "
           "**%.1f%%** to **%.1f%%** of journeys but cost **%.1f** points when met; late arrivals rose from **%.1f%%** "
           "to **%.1f%%**." % (b["on-board staffing"], b["punctuality"], b["fares"], cs["unstaffed"]["2025"],
                               cs["unstaffed"]["2026"], ef["unstaffed"], cs["late"]["2025"], cs["late"]["2026"]),
           "",
           "## 3. Step-by-Step Solution", "",
           "1. Took the Partnership's letter (a) with Schedule 7 Part 3: a driver's points are those by which the "
           "tracker's weighted share satisfied (codes 4 and 5) would have fallen less had its condition met "
           "passengers as in spring 2025, the other three as they were.",
           "2. Linked each response's batch_id to the fieldwork log's train and the working timetable in force that "
           "day (Dec24 before 14 December 2025, Dec25 after; bank holidays on the SUN schedules), and coded the "
           "written-in stations to station codes.",
           "3. Crowded: the load-weigh passengers of the train's units (class 166 vehicles summed) on departure from "
           "any station of the passenger's trip above the standard seats of the units formed that day; late: "
           "arrival at the passenger's station five minutes or more after the timetable; unstaffed: no as-worked crew "
           "row for the train; fares: the flow's change for the ticket type in spring 2026.",
           "4. Fitted a weighted linear model of being satisfied on the four conditions and a spring 2026 term over "
           "both waves; each driver's points are minus its effect times the change in its weighted share of "
           "journeys.",
           "5. On time: the Dec25 trains timetabled each day of the four weeks ending 19 September 2026 (31 August on "
           "the SUN schedules), on time when arriving at the final destination less than five minutes late, an arrival "
           "after midnight timed against the evening's schedule, a train with no arrival there not on time.",
           "6. Staffed: of the trains with any movement row, those whose turn was Rostered or covered by an "
           "amendment, an amendment logged in the evening covering the next day's turn (its original_staff_ref).",
           "7. Standing: weekday trains due at Marlvale Central from 07:00 to 09:59 (31 August left out, the same "
           "either way), each formed unit's load-weigh rows at the station before matched by unit and the minute the "
           "train left (a class 166's three vehicle rows, each carrying the unit's figure since the May 2026 system "
           "move, read once), less the standard seats (the refreshed units at their seats after return), summed "
           "where positive.",
           "8. Crowding %d points, on-board staffing %d, punctuality %d, fares %d; crowding accounts for most of the "
           "fall." % (b["crowding"], b["on-board staffing"], b["punctuality"], b["fares"]),
           "",
           "## 4. Deliverable Answers", "",
           "### satisfaction_fall_spring2026.xlsx", "",
           "1. Driver accounting for most of the fall: crowding",
           "2. Points of the fall it accounts for: %d" % c["points"],
           "3. Share of passengers satisfied overall: spring 2025 %.1f%%; spring 2026 %.1f%%"
           % (s["spring_2025"], s["spring_2026"]),
           "4. Trains on time at their final destination, four weeks ending 19 September 2026 (per cent):"]
    for g, n in GROUPS:
        out.append("   - %s: %.1f" % (n, f["ask_on_time_pct"][g]))
    out.append("5. Trains that ran with on-board staff, same weeks (per cent):")
    for g, n in GROUPS:
        out.append("   - %s: %.1f" % (n, f["ask_staffed_pct"][g]))
    out.append("6. Passengers standing on weekday arrivals at Marlvale Central from 07:00 to 09:59, same weeks:")
    for g, n in GROUPS:
        if g != "BRANCH":
            out.append("   - %s: %s" % (n, format(f["ask_standing"][g], ",")))
    out += ["", "### satisfaction_bridge_spring2026.png", "",
            "1. The fall in the share satisfied by driver (points): crowding %d, on-board staffing %d, punctuality "
            "%d, fares %d, not explained by the four %d; the fall %.1f."
            % (b["crowding"], b["on-board staffing"], b["punctuality"], b["fares"], b["other"], s["fall_points"])]
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
