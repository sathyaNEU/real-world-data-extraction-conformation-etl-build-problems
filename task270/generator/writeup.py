"""task270 submission.md, written from figures.json so every number in it is one the generator computed."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C        # noqa: E402
import common as K      # noqa: E402

NAMES = {c: n for d, lst in K.OC_STATIONS.items() for c, n in lst}


def write(task_dir, F):
    cov = F["cover"]
    named = F["call"]
    rural = [d for d in K.RURAL]
    near = F["nearest_above"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Urban & Regional Science (network analysis).")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**The 2027 to 2031 plan should name %s, the only districts whose 2026 cover fell below the 75 per cent "
             "line.**" % " and ".join(named))
    L.append("%s's cover was %s per cent and %s's %s per cent. Not %s, at %s and %s per cent: cover read from each "
             "engine's own station leaves out the Calderstow engines that stood by at their on-call stations. Not %s, "
             "the nearest above the line at %s per cent." % (named[0], cov[named[0]], named[1], cov[named[1]],
                                                            " and ".join(rural), cov[rural[0]], cov[rural[1]], near,
                                                            cov[near]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. %s's 2026 cover is **%s per cent**" % (named[0], cov[named[0]]))
    L.append("2. %s's 2026 cover is **%s per cent**" % (named[1], cov[named[1]]))
    L.append("3. %s's and %s's 2026 cover are **%s per cent** and **%s per cent**" % (rural[0], rural[1], cov[rural[0]],
                                                                                    cov[rural[1]]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Took the homes as the addresses classed RD in address_register_extract.csv, each in the district of its "
             "output area per output_area_lookup.xlsx, and placed each at its nearest node of routing_network_nodes.csv.")
    L.append("2. Timed drives over routing_network_links.csv (drive_time_s, one-way links one way only) and added two "
             "minutes' turnout for wholetime-crewed and five for on-call-crewed engines per fleet_and_stations_2026.xlsx.")
    L.append("3. Read each engine free at the start of a minute when its latest Status row in "
             "mobilising_resource_log_2026.csv at or before that minute had code 1 (Available).")
    L.append("4. Placed each engine each minute at its station unless the same log had it out of base, after a Left "
             "base row and before the next Arrived base row; then at the node nearest its latest location row.")
    L.append("5. Counted a home covered when a free engine's turnout and drive to it took ten minutes or less, and "
             "averaged each district's covered share over the 525,600 minutes of 2026: %s." %
             ", ".join("%s %s per cent" % (d, cov[d]) for d in K.DISTRICTS))
    L.append("6. For each on-call station in Altmoor and Skirwold, counted the minutes its engine was at status 8 while "
             "four or more of its firefighters were booked in oncall_availability_bookings_2026.csv, a later-entered "
             "booking replacing the same firefighter's earlier booking it overlaps, and of those the minutes with no "
             "crew or watch commander booked, by role on the day per oncall_crew_register_2026.xlsx.")
    L.append("7. Counted incidents in incident_records_2022_2026.csv classified A01 or FAA at addresses classed C, a "
             "record whose call came before the closing time of an earlier record at the same premises being the same "
             "actuation, by district of the address, and per 100 addresses classed C.")
    L.append("8. Named the districts below 75 per cent on unrounded cover: %s." % " and ".join(named))
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### district_fire_cover_2026.xlsx")
    L.append("")
    L.append("1. Each district's 2026 cover and whether it is named, whole per cent:")
    for d in K.DISTRICTS:
        L.append("   - %s: %s per cent, %s" % (d, cov[d], "named" if d in named else "not named"))
    L.append("2. Each on-call station in Altmoor and Skirwold, time in 2026 off the run with four or more firefighters "
             "booked, and of that time with no crew commander or watch commander booked, in hours and minutes:")
    for s in C.RURAL_STATIONS:
        a = F["ask_a"][s]
        L.append("   - %s: %s; %s" % (NAMES[s], a["off_run_4plus"], a["no_oic"]))
    L.append("3. Each district's actuations of fire alarm apparatus at non-domestic premises that brought engines out "
             "to a false alarm, 2022 to 2026, and per 100 non-domestic premises, one decimal:")
    for d in K.DISTRICTS:
        c = F["ask_c"][d]
        L.append("   - %s: %s actuations, %s per 100 premises" % (d, c["actuations"], c["per_100"]))
    L.append("")
    L.append("### district_fire_cover_2026.png")
    L.append("")
    L.append("1. A dot for each district's 2026 cover in whole per cent against a marked 75 per cent line, %s "
             "highlighted as named." % " and ".join(named))
    L.append("")
    with open(os.path.join(task_dir, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    task = sys.argv[1]
    F = json.load(open(os.path.join(task, "generator", "figures.json"), encoding="utf-8"))
    write(task, F)
