"""Reads the cut pack back: the combined-cycle units from the register, their ozone-season operating hours from the
DAHS export as the routes in methods.py take them, and the two asks."""
import csv
import datetime as dt
import os

from openpyxl import load_workbook

import world as W


def find(folder, stem):
    for fn in sorted(os.listdir(folder)):
        if fn.startswith(stem):
            return os.path.join(folder, fn)
    raise FileNotFoundError(stem)


def _rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def cc_units(target):
    ws = load_workbook(find(target, "generating_unit_register"), read_only=True).active
    out = []
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r and r[0] and str(r[2]).lower().startswith("combined cycle"):
            out.append(r[0])
    return sorted(out)


def season_hour(d, h):
    return W.SEASON[0] <= d <= W.SEASON[1]


def record(target):
    """{unit: dict(load, nox, since, heat, stamps)} over each combined-cycle unit's operating hours in the season;
    hours since start counted along the whole year's record."""
    cc = set(cc_units(target))
    out = {u: dict(load=[], nox=[], since=[], heat=[], stamps=[]) for u in cc}
    run = {u: 0 for u in cc}
    for r in _rows(find(target, "dahs_hourly_export")):
        u = r["UNIT_ID"]
        if u not in cc:
            continue
        on = float(r["OP_TIME"] or 0) > 0
        run[u] = run[u] + 1 if on else 0
        d = dt.date.fromisoformat(r["OP_DATE"])
        if on and season_hour(d, int(r["OP_HOUR"])):
            o = out[u]
            o["load"].append(float(r["GLOAD_MW"]))
            o["heat"].append(float(r["HEAT_INPUT_MMBTU"]))
            o["nox"].append(float(r["NOX_MASS_LB"]) if r["NOX_MASS_LB"] else None)
            o["since"].append(run[u])
            o["stamps"].append(dt.datetime.combine(d, dt.time(int(r["OP_HOUR"]))))
    return out


def _local(t):
    a, b = dt.datetime(2026, 3, 8, 2), dt.datetime(2026, 11, 1, 1)
    return t + dt.timedelta(hours=1) if a <= t < b else t


def ask_a(target, route="gasday"):
    """Each unit's ozone-season fuel cost: each operating hour's heat input at the invoice price of its gas day."""
    fac = {}
    for r in _rows(find(target, "dahs_hourly_export")):
        fac[r["UNIT_ID"]] = r["FACILITY_NAME"]
    price = {}
    for r in _rows(find(target, "gas_supply_daily_invoices")):
        price[(r["delivery_point"], r["gas_day"])] = float(r["price_usd_per_dth"])
    rec = record(target)
    out = {}
    for u, o in rec.items():
        tot = 0.0
        for t, q in zip(o["stamps"], o["heat"]):
            if route == "gasday":
                gd = (_local(t) - dt.timedelta(hours=9)).date()
            elif route == "standard9":
                gd = (t - dt.timedelta(hours=9)).date()
            else:
                gd = t.date()
            k = (fac[u], gd.isoformat())
            while k not in price:
                gd -= dt.timedelta(days=1)
                k = (fac[u], gd.isoformat())
            tot += q * price[k]
        out[u] = tot
    return out


def ask_b(target, union=True):
    """Each unit's ozone-season forced outage hours: hours inside any U1, U2 or U3 event, local time, each once."""
    a, b = dt.datetime(2026, 5, 1), dt.datetime(2026, 10, 1)
    out = {}
    hrs = {}
    for r in _rows(find(target, "gads_event_report")):
        if r["event_type"] not in ("U1", "U2", "U3"):
            continue
        s = max(a, dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M"))
        e = min(b, dt.datetime.strptime(r["end_local"], "%Y-%m-%d %H:%M"))
        if e <= s:
            out.setdefault(r["unit"], 0)
            continue
        if union:
            st = hrs.setdefault(r["unit"], set())
            t = s
            while t < e:
                st.add(t)
                t += dt.timedelta(hours=1)
        else:
            out[r["unit"]] = out.get(r["unit"], 0) + (e - s).total_seconds() / 3600
    if union:
        for u, st in hrs.items():
            out[u] = len(st)
    return out


def season_totals(target):
    rec = record(target)
    return {u: (sum(o["load"]), len(o["load"])) for u, o in rec.items()}
