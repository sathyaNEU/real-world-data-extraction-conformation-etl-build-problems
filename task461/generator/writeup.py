"""Write task461/submission.md from generator/figures.json."""
import calendar
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W   # noqa: E402

MONTHS = [calendar.month_name[m] for m in range(1, 11)]


def write(fig_path, out_path):
    F = json.load(open(fig_path))
    call, below = F["call"], F["below"]
    E = F["exp"]
    R = F["rungs"]
    r0 = R["R0 the node's own record"]
    r1 = R["R1 the hub plus the node's average spread premium"]
    hub = R["Rx the hub's record alone"]
    full = R["G full years 2019 to 2025"]
    hm, fl = F["hub_mean_by_year"], F["hub_flat_share_by_year"]
    ordinary = [fl[str(y)] for y in (2019, 2021, 2022, 2023, 2024, 2025)]
    means = [hm[str(y)] for y in range(2019, 2026)]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** General Statistics & Data Science (data integration: the battery node's short day-ahead price "
             "record extended over the North Hub's eight-year record through their overlap).")
    L.append("**Analytical objective:** Data Extraction & Conformation (ETL).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Load a 2027 cycling threshold of $%d per MWh into Redrock Draw's trading system.**" % call)
    L.append("At $%d the battery is expected to cycle on %d days of 2027, within the warranty's %d Full Cycles; at $%d, "
             "the next setting down, it would cycle on %d. The node's own %d days since MPI first priced it are one "
             "windy stretch: their average spread is ordinary, but %d per cent of the hub's 2026 days had a spread under "
             "$8 against %d to %d per cent in an ordinary year, so the node's own days set $%d (%d expected days), too "
             "low for 2027. The North Hub's record from 2019, carried to the node at the ratio its %d overlapping days "
             "show (the node's spread %.2f times the hub's), gives the expected days at each setting. Not $%d, the hub's "
             "record taken for the node's, and not $%d, the hub plus the node's average spread premium ($%.2f), which "
             "lifts every flat day by the same amount.\n" % (
                 call, E[str(call)], F["limit"], below, E[str(below)], F["node_days"], fl["2026"], min(ordinary),
                 max(ordinary), r0["call"], r0["exp"][str(r0["call"])], F["overlap_days"], F["k"], hub["call"],
                 r1["call"], F["premium"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Expected 2027 cycling days at $%d: **%d**, within the %d limit." % (call, E[str(call)], F["limit"]))
    L.append("2. At $%d, the next setting down: **%d** expected cycling days, over the limit." % (below, E[str(below)]))
    L.append("3. The node's daily spread is **%.2f** times the hub's over the **%d** days MPI priced it at its own "
             "settlement point." % (F["k"], F["overlap_days"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Read %s (dates MM/DD/YYYY and hours 01:00 to 24:00 to 2021, ISO dates and hours 1 to 24 from 2022) and "
             "%s, joining %s and %s through %s, each operating day on Central prevailing time with its 23 or 25 hours "
             "as they are." % (W.FILES["hub"], W.FILES["node"], W.NODE_OLD, W.NODE, W.FILES["points"]))
    L.append("2. Computed each operating day's spread as the policy defines it (the average of the four highest hourly "
             "day-ahead prices less the average of the four lowest): %s hub days and %d node days." % (
                 format(F["record_days"], ","), F["node_days"]))
    L.append("3. Set aside the node's first %d days, which MPI priced at the hub's prices, and took the ratio of the node's "
             "total spread to the hub's over the %d days left: %.2f, the relationship running through the origin." % (
                 F["hub_priced_days"], F["overlap_days"], F["k"]))
    L.append("4. Compared the hub's years: its 2026 average spread ($%.2f) sits inside the 2019 to 2025 range ($%.2f to "
             "$%.2f), but %d per cent of its 2026 days were under $8 against %d to %d per cent in 2019 and 2021 to 2025 "
             "(%d in 2020, falling back to %d in 2021): the node's own days are a windy stretch, not an ordinary year." % (
                 hm["2026"], min(means), max(means), fl["2026"], min(ordinary), max(ordinary), fl["2020"], fl["2021"]))
    L.append("5. Extended the node's record over the hub's %s days (the node's own spread where MPI priced it, %.2f times "
             "the hub's on every other day) and took the expected 2027 cycling days at each setting as 365 times the "
             "share of days at or above it; the extension's other estimators agree on the call (the full years 2019 to "
             "2025 alone give %d days at $%d and %d at $%d)." % (
                 format(F["record_days"], ","), F["k"], full["exp"][str(call)], call, full["exp"][str(below)], below))
    L.append("6. Picked the lowest setting within %d: $%d (%d days); $%d gives %d." % (
        F["limit"], call, E[str(call)], below, E[str(below)]))
    L.append("7. Counted 2026's Full Cycles as warranty Schedule 4 does: the BMS's DC discharge for each hour in contract "
             "months on Central prevailing time; for the %d hours (in %d runs) in which the meter recorded the battery "
             "discharging while the BMS export shows zero energy with its last state held, the meter's delivered energy "
             "over 0.975, as the warranty's data clause has it; both capacity tests left out (%s, logged TEST, and %s, logged MAINT after the "
             "June firmware update)." % (F["lost_hours"], F["lost_spans"], F["tests"][0], F["tests"][1]))
    L.append("8. Took the day-ahead net from the latest statement line for each hour and charge type (a final statement "
             "restates the day; 20 and 21 July were repriced between initial and final), reversed MPI's sign and "
             "counted the administrative fee once per operating day, the export carrying the day's fee on every hour "
             "line.")
    L.append("9. Divided the January to October net by the Full Cycles: $%s per cycle.\n" % format(F["per_cycle"], ","))
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % W.GOLDEN["workbook"])
    L.append("1. Threshold for 2027: $%d per MWh; the next setting down, $%d, is over the limit." % (call, below))
    L.append("2. Expected 2027 cycling days at each setting:")
    for s in sorted(E, key=int):
        L.append("   - $%s: %d" % (s, E[s]))
    L.append("3. Full Cycles the warranty counts in each month of 2026:")
    for m, name in zip(range(1, 11), MONTHS):
        L.append("   - %s: %.2f" % (name, F["cycles"][str(m)]))
    L.append("   - January to October: %.2f" % F["cycles_total"])
    L.append("4. Day-ahead net after MPI's fees in each month of 2026, thousands of dollars:")
    for m, name in zip(range(1, 11), MONTHS):
        L.append("   - %s: %s" % (name, format(F["net_k"][str(m)], ",.1f")))
    L.append("   - January to October: %s" % format(F["net_total_k"], ",.1f"))
    L.append("5. Day-ahead net per Full Cycle, January to October: $%s." % format(F["per_cycle"], ","))
    L.append("6. Chart: the cumulative 2026 Full Cycles at each month's end (%.2f at the end of October) against the pace "
             "to 300 by 31 December, on the Cycle chart sheet.\n" % F["cum_cycles"]["10"])
    L.append("### %s\n" % W.GOLDEN["daily"])
    L.append("1. %s rows, one per settlement point and operating day: the North Hub from 2019-01-01 and the node, under "
             "%s, from 2025-12-02, both to 2026-11-02, with the hours in the day, the spread in dollars per MWh and "
             "whether MPI set the node's price at the hub's." % (format(F["csv_rows"], ","), W.NODE))
    with open(out_path, "w") as f:
        f.write("\n".join(L) + "\n")
