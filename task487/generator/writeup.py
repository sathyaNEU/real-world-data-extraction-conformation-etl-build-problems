"""submission.md from generator/figures.json: the five blocks, every figure taken from the generator's own output."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
ROUTES = ["R%02d" % i for i in range(1, 13)]


def t(x):
    return "{:,}".format(x)


def main():
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c = f["call"]
    out = ["## Tags", "",
           "**Domain:** Physical & Environmental Sciences, emissions inventory (an upstream oil producer's 2026 "
           "release-event methane return to its provincial energy board, conformed from two lease operator apps, an "
           "event register, a SCADA alarm journal, daily production and tank vapour analyses, with its fugitive "
           "emissions schedule from the leak survey log and tracker).",
           "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
           "## 1. Final Recommendation", "",
           "**Budget CAD %s for Vennholt Energy's 2027 release-event levy: its 2026 return falls in band %s, at %.1f t "
           "of release-event methane, CAD %s for each of its %s batteries.**" % (
               t(c["levy_cad"]), c["band"], f["methane_t"], t(c["rate_per_battery_cad"]), c["batteries"]),
           "The band rests on when the undated events began, read from all of the operator's 2026 windows between visits: "
           "open hatches turn up more often after long windows than after short ones, but far less than in proportion "
           "to the window, because a share of them is left open by the departing visit and vents the whole window. Not "
           "band B, which starting every undated event halfway through its window gives: it prices the hatches the "
           "departing visit left open at half their windows. Not band E, which starting every hatch at the previous "
           "departure gives: most hatches open between visits.", "",
           "## 2. Critical Components", "",
           "1. Release events found in 2026: **%s** (%s open thief hatches, %s combustor pilots out, %s relief valves "
           "not reseated, %s of them timed by a tank pressure alarm)." % (
               t(f["events.total"]), t(f["events.hatch"]), f["events.pilot"], f["events.relief"],
               f["events.relief_alarm_timed"]),
           "2. Release-event methane for 2026: **%.1f t** on the fit of all the year's windows, band %s." % (
               f["methane_t"], c["band"]), "",
           "## 3. Step-by-Step Solution", "",
           "1. Joined each event in release_event_register_2026.xlsx to the visit that found it in "
           "route_app_visits_20251215_20260630.csv or checkin_app_visits_20260615_20270112.jsonl (check-in app re-entries "
           "within ten minutes and the June visits logged in both apps taken once, BT-0907 read as BT-0907A): %s "
           "events, each with its window since the previous visit left." % t(f["events.total"]),
           "2. Started each relief valve that did not reseat at a telemetered battery at the first alarm of the last "
           "lift before its find in scada_alarm_journal_20251215_20270112.csv, on the RTU's clock: %d events." %
           f["events.relief_alarm_timed"],
           "3. Fitted, for each kind over all of the operator's 2026 windows, the chance that a window ends in an event "
           "of that kind as a share started as the previous visit left plus a rate an hour, by maximum likelihood, and "
           "took every other start at its expected value given its window (Directive 17 s.3.2), each hour at the "
           "battery's tank vapour methane that day (s.3.3) from battery_daily_production_20251215_20261231.csv and "
           "tank_vapour_analyses_2025_2026.xlsx: %.1f t, band %s." % (f["methane_t"], c["band"]),
           "4. Placed each tag in ldar_leak_tracker_20270112.xlsx at its battery's survey in ldar_surveys_2025_2026.csv, "
           "the last on or before the day it reached the tracker, reading a battery's surveys as the sessions that "
           "screened its points (the %d re-checks of a few repaired fittings are not surveys), and took a tag hung on a "
           "component whose earlier tag had not been repaired by that survey as the same leak found again (Directive 17 "
           "s.5.2)." % f["schedule_b.sessions"],
           "5. Took each leak's repair from the last leak repair in maintenance_work_orders_2026.csv that names its tag, "
           "a contract order's on its field ticket's day (the %d contract orders were completed when the foreman "
           "approved their tickets, on the 10th of the next month or the next working day): %d tags the tracker closed on a first repair were "
           "still leaking at a re-check, and their leaks run to the later work order." % (
               f["schedule_b.contract_orders"], f["schedule_b.rechecked_tags"]),
           "6. Vented each leak from its battery's last survey before it was first found to its repair, at the rate "
           "measured then, split at 1 July and kept inside 2026, and carried each half by the run that served the "
           "battery then: the route app's Route to 30 June and the check-in app's run from 1 July, not the 2027 runs "
           "in battery_register_20270108.csv (%d batteries changed run on 1 July 2026 and %d on 4 January 2027)." % (
               f["schedule_b.moved_jul"], f["schedule_b.moved_jan"]),
           "7. Recommended budgeting the band %s levy of CAD %s for 2027." % (c["band"], t(c["levy_cad"])), "",
           "## 4. Deliverable Answers", "",
           "### release_events_2026.csv", "",
           "1. One row per release event found in 2026 in the Board's schema, %s rows (%s HATCH, %s COMBUSTOR, %s "
           "RELIEF), each with its start, start basis (ALARM for %d, EXPECTED for the rest), find, closure, active hours "
           "and methane." % (t(f["events.total"]), t(f["events.hatch"]), f["events.pilot"], f["events.relief"],
                             f["events.relief_alarm_timed"]), "",
           "### release_levy_filing_2026.xlsx", "",
           "1. Release-event methane for 2026: %.1f t; band %s; 2027 levy CAD %s (CAD %s for each of %s batteries)." % (
               f["methane_t"], c["band"], t(c["levy_cad"]), t(c["rate_per_battery_cad"]), c["batteries"]),
           "2. Schedule B, fugitive methane by route, tonnes, January to June and July to December:"]
    for r in ROUTES:
        out.append("   - %s: %.1f and %.1f" % (r, f["schedule_b.%s.h1_t" % r], f["schedule_b.%s.h2_t" % r]))
    open(os.path.join(TASK, "submission.md"), "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
