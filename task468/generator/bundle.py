"""Read the shipped pack as a solver would: both AVL exports conformed to one table of stop events in local time (each
stop by its public code, each bus by its fleet number, each event on its service day; Quinnell's repeated file-head
rows and the two systems' overlap on the evening of 31 March removed), Service Quality's review log, the two GTFS
feeds, the fleet roster and the ridership report."""
import csv
import datetime as dt
import io
import os
import zipfile

import numpy as np
import pandas as pd

import world as W

CODE_OF_KEY = {k: v[0] for k, v in W.STOPS.items()}
KEY_OF_CODE = {v[0]: k for k, v in W.STOPS.items()}


def path(target, key):
    return os.path.join(target, W.FILES[key])


def gtfs_table(target, key, name):
    with zipfile.ZipFile(path(target, key)) as z:
        return pd.read_csv(io.BytesIO(z.read(name)), dtype=str, keep_default_na=False)


def stop_codes(target):
    """GTFS stop_id to public stop code, both feeds."""
    out = {}
    for key in ("gtfs_jan", "gtfs_apr"):
        st = gtfs_table(target, key, "stops.txt")
        out.update(dict(zip(st["stop_id"], st["stop_code"])))
    return out


def roster(target):
    return pd.read_csv(path(target, "fleet"), dtype=str, keep_default_na=False)


def svc_minutes(s):
    h, m, sec = (int(v) for v in s.split(":"))
    return h * 60 + m + sec / 60.0


def arbor(target):
    a = pd.read_csv(path(target, "avl_q1"), dtype=str, keep_default_na=False)
    codes = stop_codes(target)
    out = pd.DataFrame({
        "source": "Arbor", "event": a["event_id"], "bus": a["veh_no"], "code": a["stop_id"].map(codes),
        "service_day": pd.to_datetime(a["svc_date"]).dt.date, "dep": pd.to_datetime(a["dep_time"]),
        "arr": pd.to_datetime(a["arr_time"]), "route": a["route"], "trip": a["trip_id"],
        "attributed": a["trip_id"] != "",
        "sched": [svc_minutes(s) if s else np.nan for s in a["sched_dep"]],
        "deviation_s": np.nan})
    return out


def quinnell(target, repeats=False):
    q = pd.read_csv(path(target, "avl_q2"), dtype=str, keep_default_na=False)
    tag = dict(zip(roster(target)["asset_tag"], roster(target)["fleet_no"]))
    utc = pd.to_datetime(q["ActualDepartureUTC"], utc=True)
    dep = utc.dt.tz_convert(W.TZ).dt.tz_localize(None)
    sched = [svc_minutes(s) if s else np.nan for s in q["ScheduledDeparture"]]
    out = pd.DataFrame({
        "source": "Quinnell", "event": q["EventID"], "bus": q["VehicleID"].map(tag), "code": q["StopCode"],
        "dep": dep, "arr": pd.NaT, "route": q["Route"], "trip": q["TripID"], "attributed": q["MatchStatus"] == "MATCHED",
        "sched": sched, "deviation_s": pd.to_numeric(q["DeviationSec"], errors="coerce")})
    out["service_day"] = service_day(out)
    if not repeats:
        out = out[~out.duplicated(["bus", "code", "dep"], keep="first")]
    return out


def candidates(target):
    """Planning's candidate routes and the designated stop code each would name."""
    c = pd.read_csv(path(target, "candidates"), dtype=str, keep_default_na=False)
    return dict(zip(c["route"], c["designated_stop_code"]))


def secs(s):
    h, m, x = (int(v) for v in s.split(":"))
    return h * 3600 + m * 60 + x


def timetable(target):
    """The feeds' scheduled departures: each candidate trip's departure from its designated stop (seconds after the
    service day's midnight), and the frequency blocks (route, start, end) of the trips that run by headway."""
    stop_of = candidates(target)
    dep, blocks = {}, []
    for key in ("gtfs_jan", "gtfs_apr"):
        code = dict(zip(*(gtfs_table(target, key, "stops.txt")[c] for c in ("stop_id", "stop_code"))))
        route = dict(zip(*(gtfs_table(target, key, "trips.txt")[c] for c in ("trip_id", "route_id"))))
        st = gtfs_table(target, key, "stop_times.txt")
        for t, sid, d in zip(st["trip_id"], st["stop_id"], st["departure_time"]):
            if route[t] in stop_of and code[sid] == stop_of[route[t]]:
                dep[t] = secs(d)
        fq = gtfs_table(target, key, "frequencies.txt")
        blocks += [(route[t], secs(a), secs(b)) for t, a, b in zip(fq["trip_id"], fq["start_time"], fq["end_time"])]
    return dep, blocks


def published(t, target):
    """Each candidate's tied departure's scheduled departure in the feeds, minutes after the service day's midnight: the
    trip's own stop time, or for a trip run by headway, its minute in the frequency block that covers it."""
    dep, blocks = timetable(target)
    cand = candidates(target)
    out = np.full(len(t), np.nan)
    for j, (r, trip, sch, att) in enumerate(zip(t["route"], t["trip"], t["sched"], t["attributed"])):
        if not att or r not in cand:
            continue
        if trip in dep:
            out[j] = dep[trip] / 60.0
            continue
        m = int(np.floor(sch + 1e-9))
        cover = [a for rr, a, b in blocks if rr == r and a // 60 <= m and m * 60 < b]
        assert cover, (r, trip, sch)
        out[j] = m + (cover[0] % 60) / 60.0
    return out


def service_day(t):
    """A stop event's service day: a scheduled trip's own (the day whose midnight plus the scheduled time, past 24:00
    after midnight, lies nearest the departure); an event with no trip before 3 a.m. belongs to the day before."""
    dep = t["dep"]
    sched = t["sched"].to_numpy(dtype=float)
    has = ~np.isnan(sched)
    base = dep - pd.to_timedelta(np.where(has, sched, 0.0), unit="m")
    by_trip = (base + pd.Timedelta(hours=12)).dt.normalize()
    mins = (dep - dep.dt.normalize()).dt.total_seconds().to_numpy() / 60.0
    by_clock = dep.dt.normalize() - pd.to_timedelta((mins < 180).astype(int), unit="D")
    return pd.Series(np.where(has, by_trip, by_clock), index=t.index).dt.date


def events(target):
    """One table of stop events at the five stops: Arbor to the end of 31 March's service, Quinnell after."""
    a = arbor(target)
    q = quinnell(target)
    q = q[q["service_day"] >= dt.date(2026, 4, 1)]
    t = pd.concat([a, q], ignore_index=True)
    t["stop"] = t["code"].map(KEY_OF_CODE)
    t["hour"] = t["dep"].dt.hour
    t["month"] = pd.to_datetime(t["service_day"]).dt.month
    t["pub"] = published(t, target)
    return t


def review(target):
    return pd.read_csv(path(target, "review"), dtype=str, keep_default_na=False)


def ridership(target):
    from openpyxl import load_workbook
    ws = load_workbook(path(target, "ridership"), data_only=True)["Weekday average"]
    out = {}
    for row in ws.iter_rows(min_row=1, values_only=True):
        if row and row[0] is not None and str(row[0]).strip().isdigit() and isinstance(row[-1], (int, float)):
            out[str(row[0]).strip()] = float(row[-1])
    return out
