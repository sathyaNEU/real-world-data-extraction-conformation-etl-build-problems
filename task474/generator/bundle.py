"""Reads the cut pack back: the combined-cycle units from the register, their ozone-season operating hours from the
DAHS export as the routes in methods.py take them, and the two asks."""
import csv
import datetime as dt
import os

import numpy as np
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


def air_windows(target):
    """{unit: [(start, end)]}: each maintenance ticket for the dilution probes' air supply that the plant's instrument
    air took down, opened and closed in local time and returned here in the DAHS's standard time."""
    out = {}
    for r in _rows(find(target, "cems_maintenance_tickets")):
        desc = r["description"].lower()
        if "instrument air" not in desc and "air compressor" not in desc:
            continue
        a = _standard(dt.datetime.strptime(r["opened_local"], "%m/%d/%Y %H:%M"))
        b = _standard(dt.datetime.strptime(r["closed_local"], "%m/%d/%Y %H:%M")) if r["closed_local"] else None
        out.setdefault(r["unit"], []).append((a, b))
    return out


def record(target, shift=0):
    """{unit: dict(load, nox, since, heat, stamps, air, blocks)} over each combined-cycle unit's operating hours in the
    season; hours since start counted along the whole year's record. air marks an unmeasured hour inside an instrument
    air ticket; blocks lists each run of such hours with the NOx per MMBtu in the operating hour before and after it.
    shift moves the tickets' clock by that many hours (a check that the clock is read right)."""
    cc = set(cc_units(target))
    win = air_windows(target)
    out = {u: dict(load=[], nox=[], since=[], heat=[], stamps=[], air=[], blocks=[]) for u in cc}
    seq = {u: [] for u in cc}
    run = {u: 0 for u in cc}
    for r in _rows(find(target, "dahs_hourly_export")):
        u = r["UNIT_ID"]
        if u not in cc:
            continue
        on = float(r["OP_TIME"] or 0) > 0
        run[u] = run[u] + 1 if on else 0
        d = dt.date.fromisoformat(r["OP_DATE"])
        t = dt.datetime.combine(d, dt.time(int(r["OP_HOUR"])))
        nox = float(r["NOX_MASS_LB"]) if on and r["NOX_MASS_LB"] else None
        heat = float(r["HEAT_INPUT_MMBTU"]) if on else 0.0
        a = on and nox is None and any(s + dt.timedelta(hours=shift) < t + dt.timedelta(hours=1) and
                                       (e is None or t < e + dt.timedelta(hours=shift)) for s, e in win.get(u, []))
        seq[u].append((t, on, nox, heat, a))
        if on and season_hour(d, int(r["OP_HOUR"])):
            o = out[u]
            o["load"].append(float(r["GLOAD_MW"]))
            o["heat"].append(heat)
            o["nox"].append(nox)
            o["since"].append(run[u])
            o["stamps"].append(t)
            o["air"].append(a)
    for u, rows in seq.items():
        pos = {t: i for i, t in enumerate(out[u]["stamps"])}
        rt = lambda i: None if i < 0 or i >= len(rows) or not rows[i][1] or rows[i][2] is None or not rows[i][3] \
            else rows[i][2] / rows[i][3]
        i = 0
        while i < len(rows):
            if rows[i][4] and rows[i][0] in pos:
                k = i
                while k + 1 < len(rows) and rows[k + 1][4]:
                    k += 1
                out[u]["blocks"].append((pos[rows[i][0]], pos[rows[k][0]], rt(i - 1), rt(k + 1)))
                i = k
            i += 1
    return _plant_after(out)


def _plant_after(out):
    """Each unit's plant's NOx per MMBtu in the first measured hour after an air loss, pooled over the plant's units."""
    for u in out:
        v = [b_[3] for w in out if w.split("-")[0] == u.split("-")[0] for b_ in out[w]["blocks"] if b_[3] is not None]
        out[u]["plant_after"] = float(np.mean(v)) if v else None
    return out


def _standard(t):
    a, b = dt.datetime(2026, 3, 8, 3), dt.datetime(2026, 11, 1, 2)
    return t - dt.timedelta(hours=1) if a <= t < b else t


def _local(t):
    a, b = dt.datetime(2026, 3, 8, 2), dt.datetime(2026, 11, 1, 1)
    return t + dt.timedelta(hours=1) if a <= t < b else t


def prices(target, route="sister"):
    """{(delivery point, gas day): $/Dth}; a gas day with no invoice line is rebuilt, when asked, from another delivery
    point's price that day plus the two points' price difference. "sister" takes the point whose difference from this
    one is the same on every day both are invoiced (the points on one transporter, whose charges move together);
    "first" the first other point invoiced that day with the pair's most common difference; "mean" the average
    difference over the days both are invoiced; "linear" a straight-line fit of one point's price on the other's;
    "prev" carries the point's last invoiced price forward."""
    price = {}
    for r in _rows(find(target, "gas_supply_daily_invoices")):
        price[(r["delivery_point"], r["gas_day"])] = float(r["price_usd_per_dth"])
    pts = sorted({k[0] for k in price})
    days = sorted({k[1] for k in price})
    out = dict(price)
    if route == "prev":
        for p in pts:
            last = None
            for d in days:
                if (p, d) in price:
                    last = price[(p, d)]
                elif last is not None:
                    out[(p, d)] = last
        return out
    fit, spread = {}, {}
    for a_ in pts:
        for b_ in pts:
            both = [d for d in days if (a_, d) in price and (b_, d) in price]
            if a_ == b_ or len(both) < 10:
                continue
            x = np.array([price[(b_, d)] for d in both])
            y = np.array([price[(a_, d)] for d in both])
            ds = [round(v, 4) for v in y - x]
            spread[(a_, b_)] = float(np.percentile(ds, 95) - np.percentile(ds, 5))
            if route == "linear":
                fit[(a_, b_)] = tuple(np.polyfit(x, y, 1)[::-1])
            elif route == "mean":
                fit[(a_, b_)] = (float(np.mean(ds)), 1.0)
            else:
                fit[(a_, b_)] = (max(set(ds), key=ds.count), 1.0)
    for p in pts:
        order = sorted((q for q in pts if (p, q) in fit), key=lambda q: spread[(p, q)]) if route == "sister" else \
            [q for q in pts if (p, q) in fit]
        for d in days:
            if (p, d) not in out:
                for q in order:
                    if (q, d) in price:
                        c0, c1 = fit[(p, q)]
                        out[(p, d)] = round(c0 + c1 * price[(q, d)], 4)
                        break
    return out


def ask_a(target, route="gasday"):
    """Each unit's ozone-season fuel cost: each operating hour's heat input at the invoice price of its gas day."""
    fac = {}
    for r in _rows(find(target, "dahs_hourly_export")):
        fac[r["UNIT_ID"]] = r["FACILITY_NAME"]
    price = prices(target, route if route in ("prev", "first", "mean", "linear") else "sister")
    rec = record(target)
    out = {}
    for u, o in rec.items():
        tot = 0.0
        for t, q in zip(o["stamps"], o["heat"]):
            if route in ("gasday", "prev", "first", "mean", "linear"):
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


def ask_b(target, route="golden"):
    """Each unit's ozone-season forced outage hours: hours inside a U1, U2 or U3 event, local time, where a later report
    of the same outage (overlapping it on the same unit) replaces the earlier one."""
    a, b = dt.datetime(2026, 5, 1), dt.datetime(2026, 10, 1)
    evs = {}
    for r in _rows(find(target, "gads_event_report")):
        if r["event_type"] not in ("U1", "U2", "U3"):
            continue
        evs.setdefault(r["unit"], []).append((dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M"),
                                              dt.datetime.strptime(r["end_local"], "%Y-%m-%d %H:%M"), r["date_reported"],
                                              int(r["event_no"]), r["cause_code"]))
    out = {}
    for u, es in evs.items():
        if route == "golden":
            # a full outage reported again a day earlier, at the same hours, with the same length and cause, in a later
            # filing is the same outage dated right; the earlier filing gives way to it
            es = [e for e in es if not any(f[3] != e[3] and f[2] > e[2] and f[4] == e[4] and f[1] - f[0] == e[1] - e[0]
                                           and e[0] - f[0] == dt.timedelta(days=1) for f in es)]
        keep = []
        if route in ("latest", "golden"):
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
