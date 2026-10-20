"""Reads the cut pack back: the estimators' inputs (stations' daily totals, the register, each link's two count days
by class from its programme's file) and the terminals' visits under each route."""
import csv
import datetime as dt
import os

from openpyxl import load_workbook

import methods as M
import world as W


def find(folder, stem):
    for fn in sorted(os.listdir(folder)):
        if fn.startswith(stem):
            return os.path.join(folder, fn)
    raise FileNotFoundError(stem)


def _rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def _date(s):
    return dt.date.fromisoformat(s)


def register(target):
    ws = load_workbook(find(target, "count_station_register"), read_only=True).active
    return {r[0]: {"classifies": r[3] == "Yes", "road": r[2]} for r in ws.iter_rows(min_row=5, values_only=True)
            if r and r[0]}


CODE = {"1-3": "P", "4-7": "SU", "8-13": "CU"}


def stations(target):
    """{station: {class or 'ALL': {date: daily volume}}}."""
    out = {}
    for r in _rows(find(target, "ccs_hourly")):
        s = out.setdefault(r["station_id"], {})
        d = _date(r["date"])
        v = int(r["volume"])
        keys = ["ALL"] if r["vehicle_class"] == "ALL" else [CODE[r["vehicle_class"]], "ALL"]
        for k in keys:
            s.setdefault(k, {})
            s[k][d] = s[k].get(d, 0) + v
    return out


def links(target):
    ws = load_workbook(find(target, "port_roadway_links"), read_only=True).active
    return {r[0]: {"site": r[5], "programme": r[4], "length": r[3]} for r in ws.iter_rows(min_row=4, values_only=True)
            if r and r[0]}


def counts(target):
    """{link: {class: {date: volume}}}, both directions, from whichever programme counted the link."""
    site = {v["site"]: k for k, v in links(target).items()}
    out = {}

    def add(k, c, d, v):
        out.setdefault(k, {cc: {} for cc in W.CLASSES})
        out[k][c][d] = out[k][c].get(d, 0) + v
    for r in _rows(find(target, "dot_short_counts")):
        for c, col in zip(W.CLASSES, ("class_1_3", "class_4_7", "class_8_13")):
            add(site[r["site_id"]], c, _date(r["count_date"]), int(r[col]))
    for r in _rows(find(target, "terminal_access_counts")):
        add(site[r["site_code"]], r["class_code"], _date(r["interval_start"][:10]), int(r["volume"]))
    wb = load_workbook(find(target, "county_traffic_counts"), read_only=True)
    for ws in wb.worksheets:
        for r in ws.iter_rows(min_row=6, values_only=True):
            if not r or not r[0]:
                continue
            m, dd, y = r[0].split("/")
            d = dt.date(int(y), int(m), int(dd))
            for j, c in enumerate(W.CLASSES):
                add(site[ws.title], c, d, int(r[2 + j]) + int(r[5 + j]))
    return out


def rates(target):
    return {r["class_group"]: float(r["nox_g_per_mile"]) for r in _rows(find(target, "onroad_nox_emission_rates"))}


def nox(target, route="golden", **kw):
    est = M.estimate(stations(target), register(target), counts(target), route, **kw)
    ef = rates(target)
    return {k: sum(v[c] * len(W.DAYS) * ef[c] for c in W.CLASSES) / 1e6 for k, v in est.items()}


# the asks: terminal visits
def _dst(d):
    import records as R
    return R.us_eastern_dst(d)


def gate_rows(target, full=False):
    f = "%Y-%m-%d %H:%M:%S"
    out = []
    for r in _rows(find(target, "terminal_gate_transactions")):
        row = (r["terminal"], r["truck_tag"], dt.datetime.strptime(r["gate_in"], f), dt.datetime.strptime(r["gate_out"], f))
        out.append(row + ((int(r["transaction_id"]), r["in_lane"], r["out_lane"], r["container_no"]) if full else ()))
    return out


def _merge(rows):
    out = []
    by = {}
    for t, tag, a, b in rows:
        by.setdefault((t, tag), []).append((a, b))
    for (t, tag), iv in sorted(by.items()):
        iv.sort()
        ca, cb = iv[0]
        for a, b in iv[1:]:
            if a <= cb:
                cb = max(cb, b)
            else:
                out.append((t, ca, cb))
                ca, cb = a, b
        out.append((t, ca, cb))
    return out


def visits(target, route="golden"):
    """[(terminal, gate-in, gate-out)]. golden: Berth 20's in-gate brought from standard to local time in the daylight
    months, Pacific Gateway's voided transactions (a container and gate-in shared with a later transaction under
    another tag) dropped, Berth 40's legs through the rail ramp gate joined into one stay, then each truck's
    overlapping transactions at a terminal merged into one stay; merged: the stays merged as recorded; rows: every
    transaction a visit; intime: transactions sharing a truck and gate-in time merged."""
    full = gate_rows(target, True)
    if route == "rows":
        return [(t, a, b) for t, tag, a, b, *_ in full]
    if route == "intime":
        seen = {}
        for t, tag, a, b, *_ in full:
            seen.setdefault((t, tag, a), (t, a, b))
        return list(seen.values())
    if route == "merged":
        return _merge([(t, tag, a, b) for t, tag, a, b, *_ in full])
    later = {}
    for t, tag, a, b, tid, il, ol, cn in full:
        later.setdefault((t, cn, a), []).append(tid)
    rows = []
    legs = {}
    for t, tag, a, b, tid, il, ol, cn in full:
        if t == "B30" and tid < max(later[(t, cn, a)]) and route != "keep-voids":
            continue
        if t == "B20" and _dst(a.date()) and route != "b20-as-recorded":
            a = a + dt.timedelta(hours=1)
        if route == "ramp-legs":
            rows.append((t, tag, a, b))
            continue
        if ol == "RG1":
            legs[(t, tag)] = a
            continue
        if il == "RG1":
            a = legs.pop((t, tag))
        rows.append((t, tag, a, b))
    return _merge(rows)


PARTIAL = ("b20-as-recorded", "keep-voids", "ramp-legs")


def quarter(d):
    return (d.month - 10) % 12 // 3 + 1


def gate_asks(target, route="golden"):
    """{(terminal, quarter): (visits, mean turn minutes)}."""
    acc = {}
    for t, a, b in visits(target, route):
        k = (t, quarter(a.date()))
        o = acc.setdefault(k, [0, 0.0])
        o[0] += 1
        o[1] += (b - a).total_seconds() / 60
    return {k: (o[0], o[1] / o[0]) for k, o in sorted(acc.items())}
