"""submission.md, emitted from figures.json so that no figure is typed."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def f1(x):
    return "%.1f" % x


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    d = F["default"]
    names = sorted(F["own_change"])
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Energy Systems & Utilities, grid reliability and outage analysis (district metered area burst detection on a water distribution network).  ")
    L.append("**Analytical objective:** Anomaly Detection & Diagnostics.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Send the leak detection crew to %s in week 46, whose own leakage rose by %s l/s, %s l/s more than %s.** "
             "Not %s, whose normalised night flow rose %s l/s only because boundary valve %s passes %s's supply through its inlet meter; "
             "not %s, whose rise is the higher pressure its PRV now holds; not %s, whose rise is a new depot's metered night use."
             % (F["call"], f1(F["call_change"]), f1(F["gap"]), F["runner_up"], d["r2_pick"], f1(d["r2_pick_change"]),
                F["open_valve"], F["donor"], d["r1_pick"], d["r0_pick"]))
    L.append("\n## 2. Critical Components\n")
    L.append("1. %s's normalised net night flow rose **%s l/s** while %s's fell by the same amount, hour for hour across the whole day, so the area boundary on %s is open." % (F["receiver"], f1(d["r2_pick_change"]), F["donor"], F["open_valve"]))
    L.append("2. The supply crossing %s at night is **%s l/s**, and netting it leaves %s and %s with an own leakage change of **%s l/s** each." % (F["open_valve"], f1(F["transfer_night"]), F["receiver"], F["donor"], f1(F["own_change"][F["receiver"]])))
    L.append("3. %s's own leakage rose **%s l/s**, matched by no neighbour's fall; the runner-up %s rose **%s l/s**." % (F["call"], f1(F["call_change"]), F["runner_up"], f1(F["runner_up_change"])))
    L.append("\n## 3. Step-by-Step Solution\n")
    L.append("1. Took each area's inlet tags from dma_register_2026-09.xlsx, converted l/s tags to m3/h by its Instrument units sheet, summed two-meter areas and averaged the 03:00 to 04:00 local readings of historian_inlet_flows_20260801_20261102.csv over each night set in LP04 Appendix B.")
    L.append("2. Took off household and unlogged non-household night use at LP04 4.2 and 4.3 and the logged large users' 03:00 hour consumption from amr_large_user_reads_hourly.csv, metered at the register's supply points: %s's rise falls to nothing." % d["r0_pick"])
    L.append("3. Normalised each night set to its baseline AZNP pressure from aznp_pressure_hourly_2026.csv with N1 of 1.15 (LP04 5.1, bar converted to metres): %s's rise falls to nothing and %s leads at %s l/s." % (d["r1_pick"], d["r2_pick"], f1(d["r2_pick_change"])))
    L.append("4. Compared every valve pair in gis_boundary_valves.geojson on its two areas' whole-day volume change: only %s shows an equal and opposite move, %s up and %s down by the same profile." % (F["open_valve"], F["receiver"], F["donor"]))
    L.append("5. Took the night crossing as the mean of %s's night rise and %s's night fall, %s l/s, and netted it out of both areas' normalised changes." % (F["receiver"], F["donor"], f1(F["transfer_night"])))
    L.append("6. For the large users, summed hourly register advances per meter (adding 100,000 m3 where a five-digit register rolls over) over October local time for the register's revenue meter at each supply point, the same account's replacement meter and supply points connected since the register issue, leaving out tenants' check meters on bulk supplies.")
    L.append("7. For households, ordered billing_account_events_extract.csv by effective date to 31 October and counted properties with an occupied account whose class, after any CONV event, is HH; for repairs, counted jobs in works_orders_aug_oct_2026.xlsx with a REPAIR MAIN task completed from 1 August to 31 October, a contractor's TC job placed through the job number in its Asset field, areas from mains_asset_list.csv.")
    L.append("8. Ranked the areas on own leakage change: %s first at %s l/s, %s second at %s l/s." % (F["call"], f1(F["call_change"]), F["runner_up"], f1(F["runner_up_change"])))
    L.append("\n## 4. Deliverable Answers\n")
    L.append("### crew_allocation_week46.xlsx\n")
    L.append("1. Crew area: %s, %s l/s." % (F["call"], f1(F["call_change"])))
    L.append("2. Runner-up: %s, %s l/s; gap %s l/s." % (F["runner_up"], f1(F["runner_up_change"]), f1(F["gap"])))
    L.append("3. Change in own leakage by area, l/s, one decimal:")
    for n in names:
        L.append("   - %s: %s" % (n, f1(F["own_change"][n])))
    L.append("4. Metered consumption of logged large users, October 2026, whole m3:")
    for n in names:
        L.append("   - %s: %s" % (n, "{:,}".format(F["lu_oct"][n])))
    L.append("5. Occupied household properties at the end of 31 October 2026:")
    for n in names:
        L.append("   - %s: %s" % (n, "{:,}".format(F["occupied"][n])))
    L.append("6. Mains repairs completed August to October 2026:")
    for n in names:
        L.append("   - %s: %s" % (n, F["repairs"][n]))
    L.append("\n### night_flow_changes.pdf\n")
    L.append("1. One bar per area of the change in own leakage in l/s, %s's bar marked as the crew's area." % F["call"])
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
