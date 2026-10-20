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


def gates(target):
    """{terminal: {date: (trucks in, trucks out)}}."""
    out = {}
    for r in _rows(find(target, "terminal_daily_gate_report")):
        out.setdefault(r["terminal"], {})[_date(r["report_date"])] = (int(r["trucks_in"]), int(r["trucks_out"]))
    return out


def access_roads(target):
    ws = load_workbook(find(target, "port_roadway_links"), read_only=True).active
    names = {v[0]: k for k, v in W.TERMINALS.items()}
    return {r[0]: names[r[6]] for r in ws.iter_rows(min_row=4, values_only=True) if r and r[0] and r[6]}


def estimate(target, route="golden", **kw):
    """{link: {class: AADT}}. golden: the classifying stations' class factors, the access roads' combination trucks by
    their terminal's gate activity; classes: class factors on every link (the textbook); every other route as
    methods.estimate."""
    gk = {k: kw.pop(k) for k in ("gate_how", "gate_col") if k in kw}
    base = "golden" if route in ("golden", "classes") else route
    est = M.estimate(stations(target), register(target), counts(target), base, **kw)
    if route == "golden":
        est = M.access(est, counts(target), gates(target), access_roads(target), gk.get("gate_how", "mean_ratio"),
                       gk.get("gate_col", "in"))
    return est


def nox(target, route="golden", **kw):
    est = estimate(target, route, **kw)
    ef = rates(target)
    return {k: sum(v[c] * len(W.DAYS) * ef[c] for c in W.CLASSES) / 1e6 for k, v in est.items()}


# the asks: the drayage truck registry
def registry(target):
    return _rows(find(target, "drayage_truck_registry"))


def certs(target):
    ws = load_workbook(find(target, "heavy_duty_engine_certifications"), read_only=True).active
    return {r[0]: int(r[2]) for r in ws.iter_rows(min_row=2, values_only=True) if r and r[0]}


def fleet_asks(target, route="golden"):
    """({quarter: (trucks, of which engine model year 2009 or older)}, {carrier: (trucks, of which 2009 or older)} at
    30 September 2026). golden: a truck is its VIN (O and I, which a VIN never holds, read as 0 and 1), counted once
    under its latest registration, its engine's model year read from its engine family in the certification list;
    ids: trucks by truck_id; vin: trucks by the VIN as written; modelyear: the registry's model_year for the engine,
    the certification list only where it is blank."""
    regs = registry(target)
    fam = certs(target)
    norm = lambda v: v.replace("O", "0").replace("I", "1")
    out = {}
    for q, (a, b) in W.QUARTERS.items():
        d = _date(b)
        live = {}
        for r in regs:
            if _date(r["registered_from"]) <= d and (not r["registered_to"] or d <= _date(r["registered_to"])):
                key = r["truck_id"] if route == "ids" else (r["vin"] if route == "vin" else norm(r["vin"]))
                if key not in live or r["registered_from"] > live[key]["registered_from"]:
                    live[key] = r
        out[q] = live

    def year(r):
        if route in ("modelyear", "ids", "vin") and r["model_year"]:
            return int(r["model_year"])
        return fam[r["engine_family"]]
    old = lambda r: year(r) <= 2009
    quarters = {q: (len(v), sum(1 for r in v.values() if old(r))) for q, v in out.items()}
    carriers = {}
    for r in out[4].values():
        c = carriers.setdefault(r["motor_carrier"], [0, 0])
        c[0] += 1
        c[1] += old(r)
    return quarters, {k: tuple(v) for k, v in sorted(carriers.items())}


def _dst(d):
    import records as R
    return R.us_eastern_dst(d)
