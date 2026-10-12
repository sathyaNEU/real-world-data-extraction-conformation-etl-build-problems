"""The three annex measures for each plant and quarter of 2026 to date, computed from the shipped files, with the
paths a careful solver takes that land elsewhere: the injected volume (the operators' reports), the earthquakes the
automatic system located (its origin table), and the hours each network had fewer than four stations recording
(the inventory's epochs and the availability log)."""
import datetime as dt
import json
import os
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd

import models as M
import records as R
import world as W

QS = [(2026, 1), (2026, 2), (2026, 3)]


def qbounds():
    return {(y, q): tuple(int(x.timestamp()) for x in W.quarter_bounds(y, q)) for y, q in QS}


def plant_register(target):
    with open(os.path.join(target, R.PLANT_REG), encoding="utf-8") as fh:
        return json.load(fh)


# ------------------------------------------------------------------------------------------------- ask 1
def report_frame(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, R.REPORTS), read_only=True, data_only=True)
    rows = []
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        head = next(it)
        for r in it:
            if r[0] is None:
                continue
            rows.append(dict(zip(head, r), sheet=ws.title))
    wb.close()
    return pd.DataFrame(rows)


def _shift(label, k):
    y, m = int(label[:4]), int(label[5:7])
    m += k
    while m < 1:
        y, m = y - 1, m + 12
    while m > 12:
        y, m = y + 1, m - 12
    return y, m


def volumes(target, how="golden"):
    """Injected volume per plant and 2026 quarter (m3, unrounded) from the operators' reports. golden: the 2026
    sheet's month is the month a report was submitted, so each row reports the month before; as_labelled: the
    month read as the month reported; no_october: shifted, but the October 2026 submissions left out as outside
    the record; register_only: as labelled, wells mapped to plants through the register's current ids alone."""
    df = report_frame(target)
    reg = plant_register(target)
    op_plant = {p["operator"]: p["plant"] for p in reg["plants"]}
    wells = pd.read_csv(os.path.join(target, R.WELL_REG))
    well_plant = dict(zip(wells["well_id"], wells["plant"]))
    d = df[(df["sheet"] == "2026") & (df["function"] == "injection")].copy()
    if how == "register_only":
        d["plant"] = d["well"].map(well_plant)
        d = d[d["plant"].notna()]
    else:
        d["plant"] = d["operator"].map(op_plant)
    k = -1 if how in ("golden", "no_october") else 0
    if how == "no_october":
        d = d[d["month"] != "2026-10"]
    ym = [_shift(x, k) for x in d["month"]]
    d["y"] = [a for a, _ in ym]
    d["q"] = [(b - 1) // 3 + 1 for _, b in ym]
    out = {p: {qq: 0.0 for qq in QS} for p in W.PLANTS}
    for (p, y, q), v in d.groupby(["plant", "y", "q"])["volume_m3"].sum().items():
        if (int(y), int(q)) in out[p]:
            out[p][(int(y), int(q))] = float(v)
    return out


def round100(v):
    return int(np.floor(v / 100.0 + 0.5)) * 100


# ------------------------------------------------------------------------------------------------- ask 2
def origin_frame(target):
    a = pd.read_csv(os.path.join(target, R.AUTO))
    a["t"] = M.epoch(a["origin_time_utc"])
    a["c"] = M.epoch(a["creation_time_utc"])
    return a


def cluster(a, window_s=3.0, dist_km=5.0):
    """Group origins into events: in origin-time order, an origin joins the open event whose latest origin is
    within window_s seconds and dist_km kilometres of it, else it opens a new one. Returns an event index per row."""
    a = a.sort_values(["t", "c"]).reset_index()
    t, lat, lon = a["t"].to_numpy(), a["latitude"].to_numpy(), a["longitude"].to_numpy()
    ev = np.empty(len(a), int)
    open_ = []                       # (event, last t, lat, lon)
    n = 0
    for i in range(len(a)):
        open_ = [o for o in open_ if t[i] - o[1] <= window_s]
        hit = None
        for j, o in enumerate(open_):
            dkm = np.hypot((lon[i] - o[3]) * 74.6, (lat[i] - o[2]) * 110.6)
            if dkm <= dist_km:
                hit = j
                break
        if hit is None:
            ev[i] = n
            open_.append((n, t[i], lat[i], lon[i]))
            n += 1
        else:
            e = open_[hit][0]
            ev[i] = e
            open_[hit] = (e, t[i], lat[i], lon[i])
    out = pd.Series(ev, index=a["index"]).sort_index()
    return out.to_numpy()


def automatic_counts(target, how="golden", window_s=3.0, dist_km=5.0):
    """Earthquakes of ML 1.0 or more within 5 km that the automatic system located, per plant and 2026 quarter.
    golden: the real-time system's origins (author scautoloc), one per event at its final origin (the latest it
    created); rows: every automatic origin counted; first: each event at its first origin; wide: events grouped
    within a minute; all_latest: every origin in the table grouped into events, each at its latest origin (the
    analyst's, where the event was reviewed); all_rows: every origin in the table counted."""
    a = origin_frame(target)
    if how not in ("all_latest", "all_rows"):
        a = a[a["author"] == "scautoloc@lgrt1"].reset_index(drop=True)
    hm = M.holes(pd.read_csv(os.path.join(target, R.WELL_REG)))
    if how in ("rows", "all_rows"):
        sel = a
    else:
        a["ev"] = cluster(a, 60.0 if how == "wide" else window_s, dist_km)
        a = a.sort_values(["ev", "c"])
        sel = a.groupby("ev").tail(1) if how in ("golden", "wide", "all_latest") else a.groupby("ev").head(1)
    sel = sel[sel["ml"] >= W.COUNT_ML].copy()
    sel["plant"], _ = M.zone(sel["latitude"], sel["longitude"], hm)
    sel = sel[sel["plant"] != ""]
    y, q, _ = M.local_parts(sel["t"].to_numpy())
    sel["y"], sel["q"] = y, q
    out = {p: {qq: 0 for qq in QS} for p in W.PLANTS}
    for (p, yy, qq), n in sel.groupby(["plant", "y", "q"]).size().items():
        if (int(yy), int(qq)) in out[p]:
            out[p][(int(yy), int(qq))] = int(n)
    return out


# ------------------------------------------------------------------------------------------------- ask 3
NS = "{http://www.fdsn.org/xml/station/1}"


def epochs(target, channel="HHZ"):
    """{station: [(start, end)]} for the channel's epochs, UTC seconds (end None while open)."""
    root = ET.parse(os.path.join(target, R.INVENTORY)).getroot()
    out = {}
    for st in root.iter(NS + "Station"):
        for ch in st.iter(NS + "Channel"):
            if ch.get("code") != channel:
                continue
            s = pd.Timestamp(ch.get("startDate")).timestamp()
            e = pd.Timestamp(ch.get("endDate")).timestamp() if ch.get("endDate") else None
            out.setdefault(st.get("code"), []).append((s, e, ch.get("locationCode")))
    return out


def gap_frame(target):
    g = pd.read_csv(os.path.join(target, R.GAPS), dtype={"loc": str})
    g["s"] = M.epoch(g["gap_start"])
    g["e"] = M.epoch(g["gap_end"])
    return g


def visit_frame(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, R.VISITS), read_only=True, data_only=True)
    ws = wb.worksheets[0]
    it = ws.iter_rows(values_only=True)
    head = next(it)
    rows = [dict(zip(head, r)) for r in it if r[0] is not None]
    wb.close()
    return pd.DataFrame(rows)


def _minus(intervals, holes_):
    """Intervals minus holes (both lists of (a, b))."""
    out = []
    holes_ = sorted(holes_)
    for a, b in intervals:
        cur = a
        for h0, h1 in holes_:
            if h1 <= cur or h0 >= b:
                continue
            if h0 > cur:
                out.append((cur, h0))
            cur = max(cur, h1)
            if cur >= b:
                break
        if cur < b:
            out.append((cur, b))
    return out


def _under(per_station, a, b, need=4):
    """Seconds in [a, b) with fewer than need stations recording."""
    ev = []
    for iv in per_station.values():
        for s, e in iv:
            s, e = max(s, a), min(e, b)
            if e > s:
                ev.append((s, 1))
                ev.append((e, -1))
    ev.sort()
    n, last, under = 0, a, 0.0
    for x, k in ev:
        if n < need:
            under += x - last
        n += k
        last = x
    if n < need:
        under += b - last
    return under


def network_hours(target, how="golden"):
    """Hours each plant's network had fewer than four stations recording, per 2026 quarter. golden: a station
    records within its channel epochs outside its vertical-channel gaps; gaps_only: every network station taken as
    recording outside its vertical gaps, epochs not read; current_epoch: only each station's current epoch;
    visits_utc / visits_local: gaps_only with the crew's visits added as downtime, read as UTC or converted from
    local time; any_channel: epochs with gaps on any channel."""
    reg = plant_register(target)
    ep = epochs(target)
    g = gap_frame(target)
    if how != "any_channel":
        g = g[g["cha"] == "HHZ"]
    a0, z0 = int(W.YEAR_START_2026.timestamp()), int(W.RECORD_END.timestamp())
    vis = visit_frame(target) if how.startswith("visits") else None
    out = {}
    for p in reg["plants"]:
        per = {}
        for sta in p["monitoring_network"]:
            if how in ("gaps_only", "visits_utc", "visits_local"):
                live = [(a0, z0)]
            elif how == "current_epoch":
                s, e, _ = sorted(ep[sta])[-1]
                live = [(s, e if e else z0)]
            else:
                live = [(s, e if e else z0) for s, e, _ in ep[sta]]
            gg = g[g["sta"] == sta]
            holes_ = list(zip(gg["s"], gg["e"]))
            if vis is not None:
                for v in vis[vis["station"] == sta].itertuples():
                    d0 = v.date if isinstance(v.date, dt.date) else pd.Timestamp(v.date).date()
                    t0 = dt.datetime.combine(d0, dt.time(*map(int, v.arrival.split(":"))))
                    t1 = dt.datetime.combine(d0, dt.time(*map(int, v.departure.split(":"))))
                    if how == "visits_utc":
                        holes_.append((t0.replace(tzinfo=dt.timezone.utc).timestamp(),
                                       t1.replace(tzinfo=dt.timezone.utc).timestamp()))
                    else:
                        holes_.append((t0.replace(tzinfo=W.LOCAL).timestamp(), t1.replace(tzinfo=W.LOCAL).timestamp()))
            per[sta] = _minus(sorted(live), holes_)
        out[p["plant"]] = {k: _under(per, a, b) / 3600.0 for k, (a, b) in qbounds().items()}
    return out


def round1(h):
    return float(np.floor(h * 10 + 0.5) / 10)


def golden(target):
    vol = volumes(target)
    auto = automatic_counts(target)
    hrs = network_hours(target)
    return {p: {k: dict(volume_m3=round100(vol[p][k]), automatic=auto[p][k], hours_under_four=round1(hrs[p][k]),
                         volume_raw=vol[p][k], hours_raw=hrs[p][k]) for k in QS} for p in W.PLANTS}
