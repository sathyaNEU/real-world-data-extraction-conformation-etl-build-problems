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


def prices(target, rebuild=True):
    """{(delivery point, gas day): $/Dth}; a gas day with no invoice line is rebuilt, when asked, from another delivery
    point's price that day plus the constant difference between the two points' prices (the Daily Index is common to
    every point and each point carries its own adder)."""
    price = {}
    for r in _rows(find(target, "gas_supply_daily_invoices")):
        price[(r["delivery_point"], r["gas_day"])] = float(r["price_usd_per_dth"])
    if not rebuild:
        return price
    pts = sorted({k[0] for k in price})
    diff = {}
    for a_ in pts:
        for b_ in pts:
            ds = [round(price[(a_, d)] - price[(b_, d)], 4) for (p, d) in price if p == a_ and (b_, d) in price]
            if ds:
                diff[(a_, b_)] = max(set(ds), key=ds.count)
    days = sorted({k[1] for k in price})
    out = dict(price)
    for p in pts:
        for d in days:
            if (p, d) not in out:
                for q in pts:
                    if (q, d) in price and (p, q) in diff:
                        out[(p, d)] = round(price[(q, d)] + diff[(p, q)], 4)
                        break
    return out


def ask_a(target, route="gasday"):
    """Each unit's ozone-season fuel cost: each operating hour's heat input at the invoice price of its gas day."""
    fac = {}
    for r in _rows(find(target, "dahs_hourly_export")):
        fac[r["UNIT_ID"]] = r["FACILITY_NAME"]
    price = prices(target, rebuild=route != "prev")
    rec = record(target)
    out = {}
    for u, o in rec.items():
        tot = 0.0
        for t, q in zip(o["stamps"], o["heat"]):
            if route in ("gasday", "prev"):
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


def ask_b(target, route="latest"):
    """Each unit's ozone-season forced outage hours: hours inside a U1, U2 or U3 event, local time, where a later report
    of the same outage (overlapping it on the same unit) replaces the earlier one."""
    a, b = dt.datetime(2026, 5, 1), dt.datetime(2026, 10, 1)
    evs = {}
    for r in _rows(find(target, "gads_event_report")):
        if r["event_type"] not in ("U1", "U2", "U3"):
            continue
        evs.setdefault(r["unit"], []).append((dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M"),
                                              dt.datetime.strptime(r["end_local"], "%Y-%m-%d %H:%M"), r["date_reported"],
                                              int(r["event_no"])))
    out = {}
    for u, es in evs.items():
        keep = []
        if route == "latest":
            for e in sorted(es, key=lambda e: (e[2], e[3]), reverse=True):
                if not any(e[0] < k[1] and k[0] < e[1] for k in keep):
                    keep.append(e)
        elif route == "samestart":
            best = {}
            for e in es:
                if e[0] not in best or (e[2], e[3]) > (best[e[0]][2], best[e[0]][3]):
                    best[e[0]] = e
            keep = list(best.values())
        else:
            keep = es
        if route == "union":
            st = set()
            for s, e, *_ in keep:
                t = max(a, s)
                while t < min(b, e):
                    st.add(t)
                    t += dt.timedelta(hours=1)
            out[u] = len(st)
        else:
            out[u] = int(sum(max(0, (min(b, e) - max(a, s)).total_seconds()) / 3600 for s, e, *_ in keep))
    return out


def season_totals(target):
    rec = record(target)
    return {u: (sum(o["load"]), len(o["load"])) for u, o in rec.items()}
