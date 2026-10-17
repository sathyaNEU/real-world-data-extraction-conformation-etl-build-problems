"""The data files as Larkhaven Transit's systems export them: Arbor Fleetware's stop events for the first quarter (local
time, GTFS stop ids, fleet numbers), Quinnell Transit Systems' stop events from its go-live (UTC, public stop codes,
asset tags, concatenated from its daily export files), Service Quality's trip-matching review log, the fleet roster,
the ridership report and the farebox workbook."""
import csv
import datetime as dt

import numpy as np
import pandas as pd

import gtfs as G
import world as W

UTC = dt.timezone.utc
GO_LIVE_LOCAL = W.GO_LIVE_UTC.astimezone(W.TZ).replace(tzinfo=None)      # 2026-03-31 19:00


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def gtfs_time(m):
    return "%02d:%02d:00" % (m // 60, m % 60)


def detail(x):
    """Each event's dwell, the arrival it implies, and Quinnell's clock offset (its units read a few seconds later)."""
    if "detail" in x:
        return x["detail"]
    ev = x["ev"]
    r = np.random.default_rng([W.SEED, 31])
    late = (ev["sec"].to_numpy() / 60.0 - ev["sched_min"].to_numpy())
    route = ev["route"].to_numpy()
    rev = ev["revenue"].to_numpy()
    dwell = np.zeros(len(ev))
    sched_dwell = np.zeros(len(ev))
    for i in range(len(ev)):
        if not rev[i]:
            dwell[i] = 8 + r.integers(0, 35)
            continue
        rt = route[i]
        if rt in W.LAYOVER:                 # the trip starts here: the bus waits at the terminal
            sd = W.LAYOVER[rt]
            sched_dwell[i] = 0.0
        else:
            sd = W.DWELL.get(rt, 1)
            sched_dwell[i] = sd
        lost = max(0.0, late[i])
        dwell[i] = max(0.35, sd - lost * 0.8) * 60 + r.normal(0, 18)
        dwell[i] = max(15.0, dwell[i])
    x["detail"] = dict(dwell=np.round(dwell).astype(int), sched_dwell=sched_dwell,
                       q_offset=r.integers(1, 9, len(ev)))
    return x["detail"]


# ---------------------------------------------------------------- Arbor Fleetware, January to March
ARBOR_COLS = ["event_id", "svc_date", "veh_no", "stop_id", "arr_time", "dep_time", "route", "trip_id", "sched_dep",
              "adherence_min"]


def arbor_rows(x):
    ev, dd = x["ev"], detail(x)
    sel = np.where(pd.to_datetime(ev["day"]).to_numpy() <= np.datetime64("2026-03-31"))[0]
    jan_id = {k: v[1] for k, v in W.STOPS.items()}
    rows = []
    for i in sel:
        e = ev.iloc[i]
        dep = e["time"].to_pydatetime()
        arr = dep - dt.timedelta(seconds=int(dd["dwell"][i]))
        m = bool(e["matched"])
        rows.append([int(e["event_id"]), e["day"].isoformat(), e["vehicle"], jan_id[e["stop"]],
                     arr.strftime("%Y-%m-%d %H:%M:%S"), dep.strftime("%Y-%m-%d %H:%M:%S"),
                     e["route"] if m else "", e["trip"] if m else "", gtfs_time(int(e["sched_min"])) if m else "",
                     "%.1f" % ((e["sec"] - e["sched_min"] * 60) / 60.0) if m else ""])
    return rows


# ---------------------------------------------------------------- Quinnell Transit Systems, from go-live
QUINNELL_COLS = ["EventID", "VehicleID", "StopCode", "ActualDepartureUTC", "ScheduledDeparture", "TripID", "Route",
                 "MatchStatus", "DeviationSec"]


def quinnell_events(x):
    """Quinnell's record of every event from its go-live: (index into ev, UTC departure)."""
    ev, dd = x["ev"], detail(x)
    t = ev["time"].to_numpy()
    sel = np.where(t >= np.datetime64(GO_LIVE_LOCAL))[0]
    out = []
    for i in sel:
        loc = ev["time"].iloc[i].to_pydatetime() + dt.timedelta(seconds=int(dd["q_offset"][i]))
        out.append((i, loc.replace(tzinfo=W.TZ).astimezone(UTC)))
    return out


def quinnell_rows(x):
    """The daily export files, concatenated: each file holds the events from 04:50 UTC to 05:00 UTC the next day, so
    the ten minutes before each file's start are written again at its head with the next EventIDs."""
    ev, dd = x["ev"], detail(x)
    evs = sorted(quinnell_events(x), key=lambda p: (p[1], ev["stop"].iloc[p[0]]))
    times = [u for _, u in evs]
    first = dt.datetime(2026, 4, 1, 0, 0, tzinfo=UTC)
    cut = dt.datetime(2026, 4, 1, 5, 0, tzinfo=UTC)
    files = [(first, cut)]
    while cut <= times[-1]:
        files.append((cut - dt.timedelta(minutes=W.FILE_OVERLAP_MIN), cut + dt.timedelta(days=1)))
        cut = cut + dt.timedelta(days=1)
    code = {k: v[0] for k, v in W.STOPS.items()}
    rows, n = [], 410_000_001
    import bisect
    for lo, hi in files:
        for i, u in evs[bisect.bisect_left(times, lo):bisect.bisect_left(times, hi)]:
            if True:
                e = ev.iloc[i]
                m = bool(e["matched"])
                if m:
                    pub = int(e["sched_min"]) * 60 + W.pub_sec(e["route"], int(e["sched_min"]))
                    dev = str(int(e["sec"]) + int(dd["q_offset"][i]) - pub)
                else:
                    pub, dev = None, ""
                rows.append([n, W.ASSET[e["vehicle"]], code[e["stop"]], u.strftime("%Y-%m-%dT%H:%M:%SZ"),
                             G.gtfs_hms(pub) if m else "", e["trip"] if m else "",
                             e["route"] if m else "", "MATCHED" if m else "NO TRIP", dev])
                n += 1
    return rows


# ---------------------------------------------------------------- Service Quality's review log
REVIEW_COLS = ["review_id", "review_month", "service_date", "bus", "stop_code", "event_time", "source_system",
               "source_event_id", "route_operated", "finding", "minutes_late", "reviewed_by"]


def review_rows(x):
    ev, rv = x["ev"], x["review"]
    q = {i: u for i, u in quinnell_events(x)}
    qid = first_quinnell_ids(x)
    code = {k: v[0] for k, v in W.STOPS.items()}
    idx = {int(e): i for i, e in enumerate(ev["event_id"].to_numpy())}
    who = np.random.default_rng([W.SEED, 61]).choice(W.REVIEWERS, size=len(rv), p=[0.5, 0.3, 0.2])
    rows = []
    for mth, g in rv.groupby(pd.to_datetime(rv["day"]).dt.month):
        for j, (_, e) in enumerate(g.iterrows()):
            i = idx[int(e["event_id"])]
            in_q = i in q and e["day"] >= dt.date(2026, 4, 1)
            if in_q:
                t = q[i].astimezone(W.TZ).strftime("%H:%M:%S")
                src, sid = "Quinnell", str(qid[i])
            else:
                t = e["time"].strftime("%H:%M:%S")
                src, sid = "Arbor", str(int(e["event_id"]))
            if not e["revenue"]:
                rt, fnd, ml = "Not in service", "Out of service", ""
            elif e["fault"]:
                rt, fnd, ml = e["route"], "Logon fault", ""
            else:
                lt = (e["sec"] - e["sched_min"] * 60) / 60.0
                rt, fnd, ml = e["route"], "Late beyond window" if lt > 0 else "Early beyond window", "%.1f" % lt
            rows.append(["SQ-2026%02d-%03d" % (mth, j + 1), "2026-%02d" % mth, e["day"].isoformat(), e["vehicle"],
                         code[e["stop"]], t, src, sid, rt, fnd, ml, who[len(rows)]])
    return rows


def first_quinnell_ids(x):
    if "qid" in x:
        return x["qid"]
    ev = x["ev"]
    t = ev["time"].to_numpy()
    sel = np.where(t >= np.datetime64(GO_LIVE_LOCAL))[0]
    q = quinnell_events(x)
    rows = x.get("qrows") or quinnell_rows(x)
    x["qrows"] = rows
    key = {}
    for i, u in q:
        key[(W.ASSET[ev["vehicle"].iloc[i]], {k: v[0] for k, v in W.STOPS.items()}[ev["stop"].iloc[i]],
             u.strftime("%Y-%m-%dT%H:%M:%SZ"))] = i
    out = {}
    for r in rows:
        i = key[(r[1], r[2], r[3])]
        out.setdefault(i, r[0])
    x["qid"] = out
    assert len(out) == len(sel)
    return out


def review_frame(x):
    """Bus-days listed, drawn and reviewed each month (Service Quality's own tally)."""
    ev, rv = x["ev"], x["review"]
    un = ev[~ev["matched"]]
    out = []
    for mth in range(1, 7):
        g = un[pd.to_datetime(un["day"]).dt.month == mth]
        listed = g.groupby(["vehicle", "day"]).size().shape[0]
        drawn = int((pd.to_datetime(rv["day"]).dt.month == mth).sum())
        out.append((mth, listed, drawn))
    return out


# ---------------------------------------------------------------- the fleet roster
FLEET_COLS = ["fleet_no", "asset_tag", "make_model", "model_year", "length_ft", "propulsion", "garage", "in_service"]


def fleet_rows():
    out = []
    for b in W.FLEET:
        n = int(b)
        if n < 1230:
            mm, yr, ln, pr = "Gillig Low Floor", 2014 + (n - 1201) // 8, 40, "Diesel"
        elif n < 1243:
            mm, yr, ln, pr = "Gillig Low Floor Plus", 2019, 40, "Diesel-electric hybrid"
        else:
            mm, yr, ln, pr = "New Flyer Xcelsior", 2023 + (n - 1601) // 15, 35 if n <= 1606 else 40, "Diesel"
        garage = "Kessler Yard" if n % 3 else "Westgate Yard"
        out.append([b, W.ASSET[b], mm, yr, ln, pr, garage, "%d-%02d-%02d" % (yr, 3 + n % 8, 1 + n % 27)])
    return out


# ---------------------------------------------------------------- the candidate list for the application
CANDIDATE_COLS = ["route", "route_name", "designated_stop_code", "designated_stop_name", "direction"]


def candidate_rows():
    """Planning's list of the routes the department is assessing, each with the designated stop it would name."""
    out = []
    for r in sorted(W.CANDIDATES, key=int):
        k = W.STOP_OF[r]
        out.append([r, W.ROUTE_NAMES[r], W.STOPS[k][0], W.STOPS[k][3], "Outbound, to " + G.pattern_stops(r)[-1][0]])
    return out


# ---------------------------------------------------------------- ridership and farebox workbooks
def ridership_table():
    """Average weekday boardings by route and month (APC, expanded), and the period average the report ranks by."""
    r = np.random.default_rng([W.SEED, 41])
    rows = []
    for rt in sorted(W.RIDERSHIP, key=int):
        base = W.RIDERSHIP[rt]
        months = [base * f for f in (0.95, 0.99, 1.02, 1.03, 1.02, 0.99)]
        months = [int(round(v * (1 + r.normal(0, 0.012)))) for v in months]
        shift = base * 6 - sum(months)
        months[3] += shift
        sat = int(round(base * 0.52 * (1 + r.normal(0, 0.03))))
        sun = int(round(base * 0.36 * (1 + r.normal(0, 0.03))))
        rows.append((rt, W.ROUTE_NAMES[rt], months, base, sat, sun))
    return rows


def farebox_table():
    r = np.random.default_rng([W.SEED, 42])
    out = []
    for rt in sorted(W.RIDERSHIP, key=int):
        b = W.RIDERSHIP[rt]
        out.append((rt, W.ROUTE_NAMES[rt], [round(b * 21.3 * 0.71 * (1 + r.normal(0, 0.04)), 2) for _ in range(6)]))
    return out
