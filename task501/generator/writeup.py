"""Write submission.md from figures.json: every figure in it is one the generator emitted."""
import json
import os

import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    m = f["mains"]
    pk = lambda k: m[k]["highest_hourly_flow_during_works_l_s"]
    rf = lambda k: m[k]["highest_hourly_flow_carried_nov2025_oct2026_l_s"]
    keep = ["TM104", "TM109", "TM110", "IC03"]
    aw = f["flushing_water_m3_per_100m"]
    bw = f["nonhousehold_water_ml"]
    mv = f["moved_supply_points"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Energy Systems & Utilities (asset condition and maintenance: water distribution trunk mains).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**%s**" % f["call"])
    L.append("TM112 will carry %d l/s during the works against at most %d l/s in November 2025 to October 2026, and IC05 "
             "%d l/s against none. Not TM104, TM109, TM110 or IC03: the relining loads them to %d, %d, %d and %d l/s, "
             "below the %d, %d, %d and %d l/s they carried in the June and July 2026 Mill Road jobs. Not all six mains "
             "the relining loads, which is what flows read through the register's normal valve positions give."
             % (pk("TM112"), rf("TM112"), pk("IC05"), pk("TM104"), pk("TM109"), pk("TM110"), pk("IC03"), rf("TM104"),
                rf("TM109"), rf("TM110"), rf("IC03")))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. The relining arrangement sends more water through six trunk mains in every hour: TM104, TM109, TM110, "
             "TM112, IC03 and IC05.")
    L.append("2. Highest hourly flow during the works: TM104 **%d**, TM109 **%d**, TM110 **%d**, TM112 **%d**, IC03 **%d** "
             "and IC05 **%d** l/s." % (pk("TM104"), pk("TM109"), pk("TM110"), pk("TM112"), pk("IC03"), pk("IC05")))
    L.append("3. Highest hourly flow carried in November 2025 to October 2026, through the valve positions in force each "
             "hour: TM104 **%d**, TM109 **%d**, TM110 **%d**, TM112 **%d**, IC03 **%d** and IC05 **%d** l/s."
             % (rf("TM104"), rf("TM109"), rf("TM110"), rf("TM112"), rf("IC03"), rf("IC05")))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Read nos12_planned_supply_route_changes_issue3.pdf (section 4) and tm107_ferrars_lane_relining_outage_plan_"
             "v1.pdf: the reference is November 2025 to October 2026, works flows are judged on the districts' inflows for "
             "15 March to 15 September 2026, and the plan opens the IC05 and IC03 boundary valves and shuts TM115 and "
             "TM107.")
    L.append("2. Built the network from trunk_mains_register_2026-11.xlsx (mains by junction, valves by main, districts by "
             "inlet junction) and read dma_inlet_flows_2025-11_2026-10.csv on UTC hours, re-sent rows dropped and "
             "blank hours left out.")
    L.append("3. Routed the 15 March to 15 September 2026 inflows through the plan's valve positions: six mains carry more "
             "than in normal running in every hour, peaking at %d (TM104), %d (TM109), %d (TM110), %d (TM112), %d (IC03) "
             "and %d (IC05) l/s." % (pk("TM104"), pk("TM109"), pk("TM110"), pk("TM112"), pk("IC03"), pk("IC05")))
    L.append("4. Applied every OPEN and CLOSE on a register valve in control_room_valve_log_2025-11_2026-10.csv (local "
             "time to UTC) to get the positions in force each hour, among them TM105 out from 13 April to 19 June with "
             "Brook End fed through IC02, TM108 out from 24 to 27 June with Mill Bridge and Sallowby fed through IC03 and "
             "TM115, and TM108 out from 20 to 22 July with Mill Bridge fed through IC08.")
    L.append("5. Routed every hour's inflows through that hour's positions: the highest hourly flow carried was %d "
             "(TM104), %d (TM109), %d (TM110), %d (TM112), %d (IC03) and %d (IC05) l/s."
             % (rf("TM104"), rf("TM109"), rf("TM110"), rf("TM112"), rf("IC03"), rf("IC05")))
    L.append("6. Flushing water: from mains_flushing_job_sheets_2025-26.csv, dropped re-sent rows, differenced crew C14's "
             "volume_m3 within each night from 1 December 2025 (a running meter reading, each later figure well above "
             "that row's gauge flow times its minutes), added the two hydrants of a twin-hydrant flush and counted its "
             "section length once, then divided water by length by diameter and year of night_of.")
    L.append("7. Non-household water: summed nonhousehold_monthly_consumption_2025-04_2026-10.csv for 2025-11 to "
             "2026-10 by SPID; the logged supply points %s use more in some hours than their recorded DMA's whole inflow "
             "(amr_large_users_hourly_2025-11_2026-10.csv against the inlet meters) and were placed in the neighbouring "
             "DMA whose inflow carries their load steps (%s)." % (
                 ", ".join(x["logger"] for x in mv),
                 "; ".join("%s from %s to %s" % (x["logger"], x["recorded"], x["supplied"]) for x in mv)))
    L.append("8. Compared each main's works peak with its highest hourly flow carried (NOS 12 section 4): only TM112 and IC05 "
             "pass it, so those two are flushed and the other four are not.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### ferrars_lane_flushing_2027.xlsx")
    L.append("")
    L.append("1. %s" % f["call"])
    L.append("2. Trunk mains the relining arrangement sends more water through, highest hourly flow during the works "
             "(l/s) and whether to flush:")
    for k in sorted(m):
        L.append("   - %s %s: %d l/s, %s" % (k, m[k]["name"], pk(k), "flush" if m[k]["flush"] == "Yes" else "no flush"))
    L.append("3. Water used per 100 m of main flushed, 2025-26 flushing programme (m3 per 100 m):")
    for dn in W.DIAMETERS:
        L.append("   - %d mm: %s in 2025, %s in 2026" % (dn, aw["%d mm 2025" % dn], aw["%d mm 2026" % dn]))
    L.append("4. Water used from November 2025 to October 2026 by the non-household customers each re-routed district "
             "supplies (Ml):")
    for k, v in bw.items():
        L.append("   - %s: %s" % (k, v))
    L.append("")
    L.append("### ferrars_lane_flushing_note.pdf")
    L.append("")
    L.append("1. One page that leads with the call and charts each of the six mains' highest hourly flow during the "
             "works as a bar (TM112 and IC05 in orange, the others in blue), each with a marker at the highest hourly flow it carried in "
             "November 2025 to October 2026.")
    with open(os.path.join(TASK, "submission.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
