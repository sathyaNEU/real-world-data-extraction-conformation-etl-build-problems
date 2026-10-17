"""submission.md, drafted from generator/figures.json: every figure the write-up states comes from there."""
import json

import world as W



def routes(rs):
    rs = list(rs)
    return ", ".join(rs[:-1]) + " and " + rs[-1]


def write(fig_path, out_path):
    f = json.load(open(fig_path, encoding="utf-8"))
    c, k, v, rv = f["call"], f["components"], f["verdicts"], f["rivals"]
    meets = [r for r in W.CANDIDATES if v[r]["meets"]]
    fails = [r for r in W.CANDIDATES if not v[r]["meets"]]
    lines = [
        "## Tags",
        "",
        "**Domain:** General Statistics & Data Science (data integration, record linkage and entity resolution: two "
        "AVL systems' stop events linked to the timetable's trips, the links the matchers missed propagated into each "
        "route's departures through the department's clerical review).",
        "**Analytical objective:** Data Extraction & Conformation (ETL).",
        "",
        "## 1. Final Recommendation",
        "",
        "**Nominate Routes %s to the Frequent Transit Corridors Program for FY2027.**" % routes(c["five"]),
        "Seven candidates meet the standard once each stop's departures without a trip are shared by Service Quality's "
        "review weighted by its own design: Route 17 is %d per cent of the Transit Mall's departures without a trip, "
        "its lowest hour averages %.1f departures, and it ranks fourth of the seven by boardings, leaving Route %s as "
        "the first qualifying route left out. Not Routes %s, which share by the review's unweighted mix (Route 17 at "
        "%d per cent) and leave Route 17 short at %.1f; not Routes %s, which share in proportion to the departures the "
        "matchers tied to trips and give the short-handed Route 9 Oak Street's late buses." % (
            k["mall_share_17_weighted_pct"], v["17"]["lowest"], c["first_left_out"], routes(rv["raw_review"]["five"]),
            k["mall_share_17_raw_pct"], rv["raw_review"]["route17_lowest"], routes(rv["proportional"]["five"])),
        "",
        "## 2. Critical Components",
        "",
        "1. Counting days: **%d** (weekdays of January to June 2026, the four state holidays out)." % k["counting_days"],
        "2. Departures in the counting hours that the AVL records tie to no trip: **{:,}** of {:,}.".format(
            k["no_trip_in_hours"], k["events_in_hours"]),
        "3. Route 17's share of the Transit Mall's departures without a trip, each reviewed event weighted by its "
        "bus-day's departures without a trip: **%d per cent** (unweighted, %d)." % (k["mall_share_17_weighted_pct"],
                                                                                   k["mall_share_17_raw_pct"]),
        "4. Route 17's lowest hourly average: **%.1f** departures, at least four in each of the thirteen hours." % (
            v["17"]["lowest"]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Conformed %s and %s into one table of departures in Central time at the five designated stops: Arbor's stop "
        "ids to stop codes through the January feed's stops.txt, Quinnell's UTC to Central time and its asset tags to "
        "fleet numbers through %s, each event to its service day, Quinnell's rows repeated at the head of each daily "
        "file (same bus, stop and second) dropped, and March 31's service taken from Arbor's export." % (
            W.FILES["avl_q1"], W.FILES["avl_q2"], W.FILES["fleet"]),
        "2. Kept the %d counting days and the thirteen clock hours from 6 a.m. (guidance 3.3 and 3.4): {:,} "
        "departures, {:,} with no trip.".format(k["events_in_hours"], k["no_trip_in_hours"]) % k["counting_days"],
        "3. Weighted each of the {:,} events in %s by the departures without a trip its bus-day had at the five stops "
        "(the review draws one from each of %d bus-days a month) and by its month's bus-days listed over drawn: Route "
        "17 is %d per cent of the Transit Mall's departures without a trip.".format(f["review"]["events_reviewed"]) % (
            W.FILES["review"], f["review"]["bus_days_drawn_month"], k["mall_share_17_weighted_pct"]),
        "4. Shared each stop's departures without a trip in each hour among its routes by the weighted mix, buses out "
        "of service left out, added the departures tied to each route's trips, and averaged over the counting days.",
        "5. Took each candidate's lowest hour: Routes %s meet four in every hour; Routes %s do not." % (
            routes(meets), routes(fails)),
        "6. Ranked the qualifying routes by average weekday boardings in %s (guidance 5.1): Routes %s, with Route %s "
        "the first qualifying route left out." % (W.FILES["ridership"], routes(c["five"]), c["first_left_out"]),
        "7. Timed each departure tied to a trip against the trip's scheduled departure from the designated stop in "
        "the feed in effect that day (%s to April 4, %s from April 5; guidance 4.2), not the minute-rounded schedule "
        "time in Arbor's export, for the on-time shares." % (W.FILES["gtfs_jan"], W.FILES["gtfs_apr"]),
        "8. Recommended nominating Routes %s." % routes(c["five"]),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % W.GOLDEN["workbook"],
        "",
        "1. Verdicts on the program's standard:",
    ]
    for r in sorted(W.CANDIDATES, key=int):
        lines.append("   - Route %s %s: %s" % (r, W.ROUTE_NAMES[r], "meets" if v[r]["meets"] else "does not meet"))
    lines += [
        "2. Nominated: Routes %s." % routes(c["five"]),
        "3. First qualifying route left out: Route %s." % c["first_left_out"],
        "4. Share of the departures tied to a trip that left no more than one minute early or five minutes late:",
    ]
    for r in sorted(W.CANDIDATES, key=int):
        lines.append("   - Route %s: %d%%" % (r, f["on_time_pct"][r]))
    lines += [
        "5. Bar chart of each candidate's lowest hourly average against the standard of four, on the Nominations sheet.",
        "",
    ]
    open(out_path, "w", encoding="utf-8").write("\n".join(lines))
