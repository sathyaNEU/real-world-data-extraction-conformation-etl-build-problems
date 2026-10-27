#!/usr/bin/env python3
"""task464: generator/figures.json and submission.md, both emitted, never typed."""
import json
import os

import answers
import docs
import world

TAGS = ("**Domain:** Healthcare delivery and health economics (payment, claims and health plan "
        "analytics).\n**Analytical objective:** Data extraction and conformation (ETL).\n")


def figures(st):
    t = st["truth"]
    C, S, A, B, D = t["call"], t["sites"], t["ask_a"], t["ask_b"], t["ask_c"]
    comp = answers.components(st["sites"], st["by_area"], st["rows"])
    f = {
        "call": {
            "network_weekly_slots": C["network"],
            "areas_short": len(C["short"]),
            "nearest_short_area": world.AREA[C["nearest"]]["name"],
            "nearest_short_shortfall": C["nearest_shortfall"],
            "required_weekly_slots_network": comp["required_weekly_slots_network"],
        },
        "cc1": comp["deliverable_positions"],
        "cc2": comp["attested_stations"],
        "cc3": comp["projected_weekly_demand_2027"],
        "cc4": comp["required_weekly_slots_network"],
        "area": {a["code"]: {"slots": a["slots"], "required": a["required"],
                             "meets": "yes" if a["meets"] else "no",
                             "shortfall": a["shortfall"]} for a in C["areas"]},
        "site": {r["site"]: {"slots": r["slots"]} for r in S},
        "ask_a": {},
        "ask_b": {b["code"]: {"sites": b["sites"], "stations": b["stations"]} for b in B},
        "ask_c": {d["code"]: {"sites": d["sites"], "stations": d["stations"]} for d in D},
        "constants": {
            "sites_in_scope": len(st["sites"]),
            "service_areas": len(world.CODES),
            "cushion": world.CUSHION,
            "weeks_in_contract_year": world.WEEKS_IN_CONTRACT_YEAR,
            "record_months": 48,
            "encounter_rows": st["na"] + st["nb"],
            "agreement_capacity_clause": docs.CLAUSE_CAPACITY,
            "agreement_adequacy_clause": docs.CLAUSE_ADEQUACY,
        },
        "step": {
            "3_positions": comp["deliverable_positions"],
            "3_attested": comp["attested_stations"],
            "4_slots": C["network"],
            "5_projected": comp["projected_weekly_demand_2027"],
            "5_required": comp["required_weekly_slots_network"],
            "6_ask_a_figures": len(A),
            "7_ask_b_figures": len(B) * 2,
            "7_ask_c_figures": len(D) * 2,
            "8_areas_short": len(C["short"]),
        },
    }
    for a in A:
        f["ask_a"].setdefault(a["code"], {})[a["half"]] = {"treatments": a["treatments"],
                                                           "share": a["share"]}
    with open(os.path.join(st["task"], "generator", "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=2, sort_keys=True)
        fh.write("\n")
    return f


def submission(st, f):
    t = st["truth"]
    C, S, A, B, D = t["call"], t["sites"], t["ask_a"], t["ask_b"], t["ask_c"]
    n = "{:,}".format
    L = []
    L.append("## Tags\n")
    L.append(TAGS)
    L.append("\n## 1. Final Recommendation\n")
    L.append("**The 2027 outpatient dialysis and infusion network holds %s weekly treatment slots, and "
             "six of the twelve service areas sit below the adequacy standard.**\n"
             % n(C["network"]))
    L.append("Network slots are %s against %s required across the twelve areas, and %s is the nearest of "
             "the six to the standard, %s slots short. Not the stations the directory attests, which are "
             "%s positions against %s and put three of those six areas above the standard. Not the "
             "stations the state licence lists, which are higher again. Not each site's busiest week in "
             "the record, which measures demand and leaves %d of the twelve areas short.\n"
             % (n(C["network"]), n(f["cc4"]), f["call"]["nearest_short_area"],
                n(C["nearest_shortfall"]), n(f["cc2"]), n(f["cc1"]),
                len(st["truth"]["call"]["ladder"]["short"]["R2"])))
    L.append("\n## 2. Critical Components\n")
    L.append("1. Deliverable treatment positions across the forty sites in scope are **%s**, against "
             "**%s** attested stations\n" % (n(f["cc1"]), n(f["cc2"])))
    L.append("2. Projected 2027 weekly treatment demand across the twelve areas is **%s** treatments\n"
             % n(f["cc3"]))
    L.append("3. The weekly treatment slots the standard requires across the twelve areas are **%s**\n"
             % n(f["cc4"]))
    L.append("\n## 3. Step-by-Step Solution\n")
    steps = [
        "Took the sites carrying a 2027 contract intent on the attestation cycle current at the network "
        "position date in provider_directory_2027.csv: forty sites in twelve service areas.",
        "Counted the treatment sessions each site's roster staffs in a week from "
        "staffing_roster_2026q4.csv, and the treatments a position delivers in a session from Schedule 4 "
        "clause %s." % docs.CLAUSE_CAPACITY,
        "Rebuilt each treatment's service interval from both tables of treatment_encounters.db, the 2023 "
        "and 2024 table carrying a stop time and the 2025 and 2026 table a length in minutes, and took "
        "each site's deliverable treatment positions as the greatest number of its own treatments running "
        "at one time over the four-year record: %s positions against %s attested stations."
        % (n(f["cc1"]), n(f["cc2"])),
        "Multiplied each site's positions by its sessions a week and by its category figure, as Schedule 4 "
        "clause %s sets the unit: %s weekly treatment slots for the network."
        % (docs.CLAUSE_CAPACITY, n(C["network"])),
        "Took each area's 2026 contract year treatments a week from the same extract and grew them by the "
        "area's factor in enrolment_projection_2027.csv: %s treatments a week projected and %s weekly "
        "slots required." % (n(f["cc3"]), n(f["cc4"])),
        "Rebuilt the out-of-network half-year counts on service date from "
        "out_of_network_payments_2026.csv with out_of_network_payments_runout_2027q1.csv, placing each "
        "claim in the area of the site that treated rather than the member's residence area: %d figures "
        "on the Out of Network 2026 sheet." % len(A),
        "Took the state_licence_register.xlsx facility row covering the position date for each licence "
        "number, corporate rows excluded, for the licensed supply, and the row covering the 2026 filing's "
        "own position date to resolve each distinct site in state_adequacy_filing_2026.xlsx: %d and %d "
        "figures." % (len(B) * 2, len(D) * 2),
        "Compared each area's slots with its required figure: %d of the twelve areas sit below the "
        "standard and the network holds %s weekly treatment slots." % (len(C["short"]), n(C["network"])),
    ]
    for i, s in enumerate(steps, start=1):
        L.append("%d. %s\n" % (i, s))
    L.append("\n## 4. Deliverable Answers\n")
    L.append("\n### outpatient_capacity_2027.csv\n")
    L.append("1. Weekly treatment slots, forty rows in the file's order, whole slots:\n")
    for r in S:
        L.append("   - %s, %s: %s\n" % (r["site"], r["area_name"], n(r["slots"])))
    L.append("\n### area_capacity_2027.xlsx\n")
    L.append("2. Area Capacity, the twelve areas in the sheet's order, whole slots:\n")
    for a in C["areas"]:
        L.append("   - %s: %s slots, %s required, meets the standard %s%s\n"
                 % (a["name"], n(a["slots"]), n(a["required"]), "yes" if a["meets"] else "no",
                    "" if a["meets"] else ", %s slots short" % n(a["shortfall"])))
    L.append("3. Nearest the standard without meeting it: %s, %s slots short.\n"
             % (f["call"]["nearest_short_area"], n(C["nearest_shortfall"])))
    L.append("4. Out of Network 2026, twelve areas by half, whole treatments and shares to one decimal:\n")
    for a in A:
        L.append("   - %s, %s: %s treatments, %.1f per cent\n"
                 % (a["name"], a["half"], n(a["treatments"]), a["share"]))
    L.append("5. Licensed Supply, twelve areas, whole sites and stations:\n")
    for b in B:
        L.append("   - %s: %s sites, %s stations\n" % (b["name"], n(b["sites"]), n(b["stations"])))
    L.append("6. Sites Dropped, twelve areas, whole sites and stations:\n")
    for d in D:
        L.append("   - %s: %s sites, %s stations\n" % (d["name"], n(d["sites"]), n(d["stations"])))
    L.append("7. Bar chart of weekly treatment slots against the required figure on the Area Capacity "
             "sheet, the six areas below the standard carrying their shortfall in the sheet's own "
             "shortfall column.\n")
    with open(os.path.join(st["task"], "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(L))


def write(task_dir, st):
    f = figures(st)
    submission(st, f)
    return f
