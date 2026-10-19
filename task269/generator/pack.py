"""Read the shipped pack into the analysis tables, using nothing but the files in target/: the vendor's revised
departures (a trip's later record where it has two at a timing point), the timetable in force each day from the two
feeds, each trip's branch from its headsign, the corridor workbook, the stop changes log for the relocated stop, and
the ticketing journeys."""
import csv
import datetime as dt
import io
import os
import zipfile

import openpyxl
import pandas as pd

import common as K


def _rows(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _minutes(stamp):
    t = dt.datetime.fromisoformat(stamp)
    return t.hour * 60 + t.minute + t.second / 60


def _hms(x):
    h, m, s = (int(v) for v in x.split(":"))
    return h * 60 + m + s / 60


def feed(path):
    z = zipfile.ZipFile(path)
    rd = lambda n: list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8")))
    cal = rd("calendar.txt")[0]
    trips = {t["trip_id"]: t for t in rd("trips.txt")}
    st = rd("stop_times.txt")
    stops = {s["stop_id"]: s for s in rd("stops.txt")}
    return dict(start=dt.datetime.strptime(cal["start_date"], "%Y%m%d").date(),
                end=dt.datetime.strptime(cal["end_date"], "%Y%m%d").date(), trips=trips, stop_times=st, stops=stops)


def load(target, avl="avl_rev", doubles="later", one_feed=None, map_moved=True):
    """avl, doubles, one_feed and map_moved choose the Layer 1 handlings: the release ('avl_rev' or 'avl_first'),
    a doubled record ('later', 'earlier' or 'both'), one feed for the whole fortnight (None, 0 or 1) and whether the
    relocated stop's new number is mapped through the stop changes log."""
    p = lambda k: os.path.join(target, K.FILES[k])
    feeds = [feed(p("gtfs1")), feed(p("gtfs2"))]
    moved = {}
    for r in _rows(p("stops_log")):
        if r["new_stop_number"] and map_moved:
            moved[int(r["new_stop_number"])] = int(r["stop_number"])
    canon = lambda s: moved.get(int(s), int(s))
    # each trip's route, direction and branch: the feed's shape for the trip names its branch on branched routes
    trip_info = {}
    for f in feeds:
        for tid, t in f["trips"].items():
            rt = t["route_id"]
            d = "out" if t["direction_id"] == "0" else "in"
            shape = t["shape_id"]
            v = shape[-1] if rt in K.BRANCHED else ""
            trip_info[tid] = [rt, d, v]
    pats = {}
    for f in feeds:
        seq = {}
        for r in f["stop_times"]:
            seq.setdefault(r["trip_id"], []).append((int(r["stop_sequence"]), canon(r["stop_id"])))
        for tid, lst in seq.items():
            lst.sort()
            rt, d, v = trip_info[tid]
            pats.setdefault((rt, d, v), [s for _, s in lst])
    cor_wb = openpyxl.load_workbook(p("corridors"), read_only=True)
    corridor, tp = {}, {}
    for row in list(cor_wb["Corridor stops"].iter_rows(values_only=True))[1:]:
        rt, _, d, seq, stop, name, is_tp = row
        corridor.setdefault((str(rt), "out" if d == "Outbound" else "in"), []).append((seq, int(stop)))
        tp[int(stop)] = is_tp == "Yes"
    corridor = {k: [s for _, s in sorted(v)] for k, v in corridor.items()}
    # timing points beyond the corridor, from the feed's timepoint flags
    for f in feeds:
        for r in f["stop_times"]:
            if r["timepoint"] == "1":
                tp.setdefault(canon(r["stop_id"]), True)
    patterns = pats
    # scheduled times by day
    def feed_for(day):
        for f in feeds:
            if f["start"] <= day <= f["end"]:
                return f
        raise ValueError(day)
    sched = {}
    for i, f in enumerate(feeds):
        for r in f["stop_times"]:
            sched[(i, r["trip_id"], canon(r["stop_id"]))] = _hms(r["departure_time"])
    # departures: the revised release, a trip's later record where a timing point has two
    dep = {}
    for r in _rows(p(avl)):
        day = dt.date.fromisoformat(r["service_date"])
        key = (day, r["trip_id"], canon(r["timing_point"]))
        m = _minutes(r["departure_time"])
        if doubles == "both":
            dep.setdefault(key, []).append(m)
        elif key not in dep or (m > dep[key][0] if doubles == "later" else m < dep[key][0]):
            dep[key] = [m]
    rows = []
    for (day, tid, stop), ms in dep.items():
        fi = 0 if feeds[0]["start"] <= day <= feeds[0]["end"] else 1
        if one_feed is not None:
            fi = one_feed
        rt, d, v = trip_info[tid]
        s = sched.get((fi, tid, stop), sched.get((1 - fi, tid, stop)))
        for m in ms:
            rows.append((day, rt, d, tid, v, stop, s, m))
    deps = pd.DataFrame(rows, columns=["day", "route", "direction", "trip", "variant", "stop", "sched", "actual"])
    deps = deps.sort_values(["day", "route", "direction", "stop", "actual"]).reset_index(drop=True)
    jr = []
    for r in _rows(p("journeys")):
        tid = r["trip_id"]
        rt, d, v = trip_info[tid]
        day = dt.date.fromisoformat(r["tag_on_time"][:10])
        jr.append((day, rt, d, tid, v, canon(r["tag_on_stop"]),
                   canon(r["tag_off_stop"]) if r["tag_off_stop"] else None, _minutes(r["tag_on_time"])))
    jour = pd.DataFrame(jr, columns=["day", "route", "direction", "trip", "variant", "board", "alight", "on"])
    return dict(deps=deps, jour=jour, corridor=corridor, patterns=patterns, tp=tp, trip_info=trip_info,
                feeds=feeds, canon=canon)


# ------------------------------------------------------------------------------------------------- the pilot asks
PLAN_POSTS = {"HP03": ("3", "Dunstan Road Shops"), "HP07": ("7", "Hollins Road Shops"), "HP09": ("9", "Tolland Hospital"),
              "HP14": ("14", "Corran Hospital"), "HP22": ("22", "Mardale Institute"),
              "HP31": ("31", "Ellery Road Shops"), "HP40": ("40", "Wexcombe Shops"),
              "HP52": ("52", "Barrow Road Shops")}


def pilot_shifts(target, how="golden"):
    """Each shift worked at a pilot post, once. golden: the two systems' rows matched on the person (the staff list
    joins employee number and app user), the route (the plan joins post code and post location), the day (payroll
    dates day first) and the peak; cancelled and depot rows out. Other handlings for the cracker and the mirror:
    rows: every pilot-post row counted (cancelled out); monthfirst: matched with payroll dates read month first where
    they can be; routeday: matched on route, day and peak alone (a relieved peak's second supervisor dropped).
    Returns {(route, month): count}."""
    p = lambda k: os.path.join(target, K.FILES[k])
    staff = _rows(p("staff"))
    by_app = {s["roster_app_user"]: s["employee_number"] for s in staff}
    loc = {(rt, place): rt for rt, place in PLAN_POSTS.values()}
    seen, count = set(), {}
    for r in _rows(p("timesheets")):
        if r["source_system"] == "Payroll":
            if r["post_code"] not in PLAN_POSTS:
                continue
            rt = PLAN_POSTS[r["post_code"]][0]
            dd, mm, yy = (int(x) for x in r["work_date"].split("/"))
            if how == "monthfirst" and dd <= 12:
                dd, mm = mm, dd
            day = dt.date(yy, mm, dd)
            who = r["employee_number"]
            peak = r["shift"]
            start = None
        else:
            if r["status"] != "Worked" or (r["route"], r["location"]) not in loc:
                continue
            rt = r["route"]
            st = dt.datetime.fromisoformat(r["shift_start"])
            day = st.date()
            who = by_app.get(r["app_user"], r["app_user"])
            peak = "AM" if st.hour < 12 else "PM"
            start = st.strftime("%H:%M")
        if how == "rows":
            count[(rt, day.month)] = count.get((rt, day.month), 0) + 1
            continue
        key = (rt, day, peak) if how == "routeday" else (who, rt, day, peak)
        if key in seen:
            continue
        seen.add(key)
        count[(rt, day.month)] = count.get((rt, day.month), 0) + 1
    return count


def pilot_cost(target, shifts, how="golden"):
    """Each route's pilot cost: the operator's post charges on the route's cost centre, the 30 June journal out
    (reversed on 1 July at the central cost centre, the June invoices posted in July), plus each month's coordination
    fee shared by the month's shifts worked. Other handlings: lines (every supervision line on the route's cost
    centre, the central pilot lines shared by shifts); fy26 (the 2025-26 year's lines only)."""
    p = lambda k: os.path.join(target, K.FILES[k])
    rows = _rows(p("ledger"))
    rev = [r for r in rows if r["narration"].startswith("Reverse 30 June journal")]
    reversed_docs = {r["narration"].split()[-1] for r in rev}
    cost = {rt: 0.0 for rt in K.ROUTES}
    central = {}
    for r in rows:
        amt = float(r["amount"])
        day = dt.date.fromisoformat(r["posting_date"])
        if how == "fy26" and day >= dt.date(2026, 7, 1):
            continue
        if r["account"] == "6421" and r["cost_centre"] != "NP00":
            if how == "golden" and r["document"] in reversed_docs:
                continue
            cost[str(int(r["cost_centre"][2:]))] += amt
        elif r["account"] == "6422" or (r["account"] == "6421" and r["cost_centre"] == "NP00"):
            if how == "golden" and r["account"] == "6421":
                continue
            m = _month(r["narration"]) if r["account"] == "6422" else None
            central.setdefault(m, 0.0)
            central[m] += amt
    by_month = {}
    for (rt, m), n in shifts.items():
        by_month.setdefault(m, {})[rt] = n
    tot_all = sum(shifts.values())
    for m, amt in central.items():
        if m is None:
            for rt in K.ROUTES:
                cost[rt] += amt * sum(n for (r2, _), n in shifts.items() if r2 == rt) / tot_all
            continue
        tot = sum(by_month.get(m, {}).values())
        for rt, n in by_month.get(m, {}).items():
            cost[rt] += amt * n / tot
    return cost


def _month(narr):
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, n in enumerate(names, 1):
        if " %s-26" % n in narr:
            return i
    return None
