"""submission.md from generator/figures.json (written by golden.py from the pack): the five blocks, every figure
emitted, never typed."""
import json

ORDER = ["Ore Dock", "Pine Neck", "Gannet Point", "Halyard", "Saltworks", "Millrace"]


def write(fig_path, path):
    f = json.load(open(fig_path, encoding="utf-8"))
    c = f["components"]
    saved = c["berth_hours_saved"]
    call, ru, gap = f["call"]["terminal"], c["runner_up"], c["gap_hours"]
    by = sorted(saved, key=lambda k: -saved[k])
    a, b = f["a_breakdown_hours"], f["b_labor_hours"]
    i = f["inputs"]
    n = c["total_large_vessel_calls"]
    fmt = lambda d: "; ".join("%s %s" % (k, "{:,}".format(d[k])) for k in ORDER)
    out = []
    out.append("## Tags\n")
    out.append("**Domain:** Supply Chain & Logistics (ports and container terminals, data integration and record "
               "linkage: two terminal operating systems, the pilot station's sailings, the Salt Point tide predictions "
               "and the vessel register linked into a fiscal year's large-vessel calls, each call's sailing "
               "re-allocated under the port's access rules from an earlier ready-to-sail time).")
    out.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Ternmouth should place the six 2027 replacement cranes at %s.**" % call)
    out.append("Its fiscal year 2026 large-vessel calls would have been %d berth hours shorter with the new cranes, %d "
               "more than %s's %d. Not Saltworks, which logged the most cargo work, because its deep-draft ships "
               "finish ahead of their tide at Salt Point and a faster finish only lengthens their wait (%d hours). Not "
               "Pine Neck or Ore Dock, whose largest ships are worked to sail at first light and gain nothing from "
               "finishing earlier in the night (%d and %d hours).\n"
               % (saved[call], gap, ru, saved[ru], saved["Saltworks"], saved["Pine Neck"], saved["Ore Dock"]))
    out.append("## 2. Critical Components\n")
    out.append("1. Fiscal year 2026 large-vessel calls (ships of %s TEU and over, first container move in the year): "
               "**%d**" % ("{:,}".format(i["teu_line"]), n))
    out.append("2. %s's berth hours saved: **%d**" % (call, saved[call]))
    out.append("3. The runner-up, %s: **%d**; %s's lead: **%d** berth hours\n" % (ru, saved[ru], call, gap))
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Linked each visit in tos_vessel_visits_2026.csv and the Calls sheet of srt_tos_export_fy2026.xlsx to "
        "vessel_register_extract_2026-10-05.json by IMO number and kept ships of %s TEU and over whose first "
        "container move fell in fiscal year 2026, Eastern time (rules %s and %s): %d calls."
        % ("{:,}".format(i["teu_line"]), i["rules"][0], i["rules"][1], n),
        "Took each call's cargo work, first container move to last, from tos_crane_activity_2026.csv and the QC "
        "Hours sheet (UTC, converted), and matched each call to its sailing in pilot_station_sailings_fy2026.csv by "
        "the ship's name at the time (current or former) or call sign, at the call's berth after its last move.",
        "Read when a ship may sail from harbor_masters_general_directions_2025.pdf: a draft of %d feet or more passes "
        "Salt Point from %s before to %s after high water (%s), on the passage times in %s, with high waters from "
        "salt_point_tide_predictions_2025_2026.txt (standard time, an hour added in daylight saving time); a ship of "
        "%s feet or more unberths in the harbor only from %s to %s (%s); every sailing in the record is the first "
        "such time an hour or more after its notice."
        % (i["deep_draft_ft"], i["window_before"], i["window_after"], i["rules"][4], i["rules"][5],
           "{:,}".format(i["long_ft"]), i["daylight"][0], i["daylight"][1], i["rules"][3]),
        "For each call, brought its ready-to-sail notice forward by a fifth of its cargo work, gave it the first "
        "permitted sailing an hour or more after that, and took the difference from its actual sailing as its berth "
        "hours saved (rule %s); summed by terminal (rule %s): %s."
        % (i["rules"][2], i["rules"][6], "; ".join("%s %d" % (k, saved[k]) for k in by)),
        "Ask A: took the out-of-service periods in cmms_asset_status_history_fy2026.csv on orders whose type at the "
        "pull is BD (each period of a reopened order) and the BRKDN jobs in srt_maintenance_jobs_2025-26.xlsx, "
        "counted February 2026's river stops held in both systems once, placed each stop at the terminal whose calls "
        "its crane was working at the time in the TOS crane hours (three cranes moved along the common rail during "
        "the year, which the crane register does not show), and summed fiscal year hours: %s." % fmt(a),
        "Ask B: summed cmms_labor_transactions_fy2026.csv on crane orders, the SRT job hours not also in the "
        "Authority's system, and the days in crane_maker_service_timesheets_fy2026.xlsx not already keyed into the "
        "ledger as CONTRACT on the same order, day and hours, each at the terminal where the crane was working that "
        "day, yard equipment left out: %s." % fmt(b),
        "Placed the cranes at the terminal with the most berth hours saved: %s, %d hours ahead of %s." % (call, gap, ru),
    ]
    for k, s in enumerate(steps, 1):
        out.append("%d. %s" % (k, s))
    out.append("")
    out.append("## 4. Deliverable Answers\n")
    out.append("### ternmouth_2027_crane_placement.xlsx\n")
    out.append("1. Recommended terminal: %s." % call)
    out.append("2. Berth hours the new cranes would have saved on fiscal year 2026 large-vessel calls, whole hours:")
    for k in by:
        out.append("   - %s: %d" % (k, saved[k]))
    out.append("3. Runner-up: %s; %s leads by %d berth hours." % (ru, call, gap))
    out.append("4. Bar chart of the six terminals' berth hours saved on the Berth hours saved sheet, largest first, "
               "%s highlighted." % call)
    out.append("5. Hours ship-to-shore cranes stood out of service for breakdowns at each terminal over fiscal year "
               "2026, whole hours:")
    for k in ORDER:
        out.append("   - %s: %s" % (k, "{:,}".format(a[k])))
    out.append("6. Maintenance labor hours spent on ship-to-shore cranes at each terminal over fiscal year 2026, the "
               "Authority's own staff and contractors alike, whole hours:")
    for k in ORDER:
        out.append("   - %s: %s" % (k, "{:,}".format(b[k])))
    out.append("")
    out.append("### ternmouth_fy2026_large_vessel_calls.csv\n")
    out.append("1. The conformed table of the %d fiscal year 2026 large-vessel calls, one row per call: terminal, "
               "visit, ship, IMO number, first and last container move (Eastern time) and berth hours saved to two "
               "decimals." % n)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out) + "\n")
