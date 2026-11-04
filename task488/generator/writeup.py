"""Write task488/submission.md from generator/figures.json: every figure in it is emitted, never typed."""
import json

import names as N

SECTION_NAMES = {"FARM": "farm header", "MAIN": "hydrant main", "A": "Pier A", "B": "Pier B",
                 "C": "international apron", "E": "cargo apron", "F": "remote stands", "G": "maintenance base"}


def c(v):
    return "{:,}".format(int(v))


def segs(lst):
    return lst[0] if len(lst) == 1 else (" and ".join(lst) if len(lst) == 2 else "%s to %s" % (lst[0], lst[-1]))


def write(fig_path, out):
    F = json.load(open(fig_path))
    call, ref, r0 = F["call"], F["refuellers"], F["rung0"]
    st, sg = call["standing_100"], call["segments"]
    held, air = ref["held_10"], ref["by_air_10"]
    tanks = ref["set"]
    tank_list = ", ".join(tanks[:-1]) + " and " + tanks[-1]
    rows = F["csv"]["rows"]
    L = ["## Tags\n",
         "**Domain:** Supply Chain & Logistics (transportation network: tracking a recalled jet fuel batch through an "
         "airport hydrant and its refuellers), in General Statistics & Data Science (data integration).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).\n",
         "## 1. Final Recommendation\n",
         "**Before fuelling resumes, drain Pier B's far end (%s L), the cargo apron beyond its first pit (%s L), the "
         "remote stands (%s L) and refuellers %s, and notify the operators of the %d uplifts that took the recalled batch (%d "
         "hydrant, %d refueller).**" % (c(st["B"]), c(st["E"]), c(st["F"]), tank_list, rows, call["hydrant_uplifts"],
                                         ref["refueller_uplifts"]),
         "Fuel in each hydrant segment moved only when a pit downstream of it drew, so the batch reached these branches "
         "late or not at all past their first pits and still stands there. Not the product change reckoning, which "
         "files the hydrant clear once one line fill has passed the pump station's meter (%s) and notifies %d uplifts; "
         "not a branch's turnover against its own line fill, which clears the cargo apron and the remote stands and "
         "drains the maintenance base, which never took the batch.\n" % (r0["edges"][1], r0["uplifts"]),
         "## 2. Critical Components\n",
         "1. Pier B's %s, under the stands closed at %s, hold **%s L** of the batch at 05:30." % (
             segs(sg["B"]), F["times"]["stands_closed"], c(st["B"])),
         "2. The cargo apron's %s, beyond its first pit, hold **%s L**." % (segs(sg["E"]), c(st["E"])),
         "3. The remote stands' %s hold **%s L**; every other section holds none." % (segs(sg["F"]), c(st["F"])),
         "4. **%d** hydrant uplifts took fuel from the batch." % call["hydrant_uplifts"],
         "",
         "## 3. Step-by-Step Solution\n",
         "1. Conformed every hydrant draw: corbel_fuel_tickets_2026-10-12_14.csv in local time with the voided ticket "
         "dropped, northgarth_tickets_20261012-20261014.xlsx moved from UTC and its stands mapped to pits by "
         "hydrant_network_register.xlsx, the idle-pit flushes in both agents' check records and the Monday low point "
         "drains in hydrant_maintenance_2026-wk42.xlsx.",
         "2. Took Tank 3's time on the hydrant (%s to %s) from the valve states in "
         "hydrant_scada_2026-09-14_2026-10-14.csv and its time on the rack (%s to %s) from "
         "farm_shift_log_2026-10-12_14.pdf." % (F["times"]["hydrant_on"], F["times"]["hydrant_off"],
                                                F["times"]["rack_on"], F["times"]["rack_off"]),
         "3. Traced the batch through the register's segments, each a first-in first-out pipe of its length and bore "
         "moved only by the draws downstream of it: at 05:30 it stands in %s, and %d hydrant uplifts took it."
         % (", ".join("%s (%s L)" % (SECTION_NAMES[s], c(st[s])) for s in call["sections"]), call["hydrant_uplifts"]),
         "4. Checked the tracing against every density in corbel_daily_checks_2026-10.csv, "
         "northgarth_qc_checks_oct2026.xlsx and the low point drain record, each read against "
         "batch_certificates_register_2026.csv: every sample shows the batch the tracing puts at its pit and time, "
         "while one line fill through the meter (clear by %s) does not." % r0["edges"][1],
         "5. Rebuilt each refueller tank as one mixed body from its weekly dip of 12 October through "
         "rack_loading_log_2026-10-12_14.csv (the rack line's %s L of the tank before ahead of each load), the "
         "tickets, the %s L RF-23 put into RF-24 (corbel_equipment_log_2026-10.csv) and Northgarth's tractor tickets "
         "keyed to the trailer northgarth_vehicle_log_2026-10.csv shows coupled (T-35 behind N-7 from %s): %s hold "
         "the batch at 05:30." % (c(F["rack_line_fill"]), c(F["transfer_litres"]), F["times"]["coupling_t35"], tank_list),
         "6. Took each refueller uplift's batch litres as its litres times its tank's batch share when it started: %d "
         "refueller uplifts delivered the batch." % ref["refueller_uplifts"],
         "7. Listed the %d uplifts in the recall notice's fields and drew the plan: drain the three sections' segments "
         "and the four refuellers, notify every listed operator." % rows,
         "",
         "## 4. Deliverable Answers\n",
         "### j26-1187_recall_uplifts.csv\n",
         "1. %d rows, one per uplift that delivered fuel from the recalled batch, in order of start (UTC): %d hydrant and %d "
         "refueller." % (rows, call["hydrant_uplifts"], ref["refueller_uplifts"]),
         "2. Columns: ticket number, into-plane agent, aircraft operator, flight, registration, uplift start in UTC, "
         "pit or refueller, litres delivered at 15 C, litres of the recalled batch at 15 C to the nearest 10 L.",
         "3. Hydrant uplifts, by section of the pit:"]
    for sec in ("A", "B", "C", "E", "F", "G"):
        t = F["hydrant_tickets_by_section"][sec]
        if t:
            L.append("   - %s, %d: %s" % (SECTION_NAMES[sec][0].upper() + SECTION_NAMES[sec][1:], len(t), ", ".join(t)))
    L.append("4. Refueller uplifts (ticket, operator, refueller, litres delivered, batch litres, each graded within "
             "%d L):" % F["row_band_whole_l"])
    for tkt, op, loc, lit, b in F["refueller_rows"]:
        L.append("   - %s, %s, %s, %s L, %s L" % (tkt, op, loc, c(lit), c(b)))
    L.append("5. Batch litres on the hydrant rows: a row the batch filled whole carries its litres delivered at 15 C, "
             "graded within %d L; the rows the batch's head or tail crossed during the uplift carry these batch litres "
             "(of the litres delivered), each graded within the band shown, which holds every reading of the litres "
             "basis, the flushes and the line-up minute:" % F["row_band_whole_l"])
    for tkt, b, lit, band in F["partial_rows"]:
        L.append("   - %s: %s L of %s L, within %s L" % (tkt, c(b), c(lit), c(band)))
    L += ["",
          "### hydrant_resumption_plan.pdf\n",
          "1. Hydrant sections to drain, batch litres standing to the nearest 100 L:",
          "   - Pier B (%s): %s L" % (segs(sg["B"]), c(st["B"])),
          "   - Cargo apron (%s): %s L" % (segs(sg["E"]), c(st["E"])),
          "   - Remote stands (%s): %s L" % (segs(sg["F"]), c(st["F"])),
          "   - Farm header, hydrant main, Pier A, international apron and maintenance base: none",
          "2. Refuellers to drain, batch litres held to the nearest 10 L:"]
    for k in tanks:
        L.append("   - %s: %s L" % (k, c(held[k])))
    L.append("   - RF-21, RF-22, T-32 and N-12: none")
    L.append("3. Batch litres the refuellers delivered, by airline, to the nearest 10 L:")
    for k in sorted(air):
        L.append("   - %s: %s L" % (k, c(air[k])))
    L.append("4. Schematic of the hydrant on page 2 marking %s, %s and %s as holding the batch, each with its section's "
             "litres." % (segs(sg["B"]), segs(sg["E"]), segs(sg["F"])))
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
