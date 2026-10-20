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


def record(target, shift=0, optime=True):
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
            o["load"].append(round(float(r["GLOAD_MW"]) * (float(r["OP_TIME"]) if optime else 1.0), 4))
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
    """Each unit's plant's NOx per MMBtu in the first measured hour after an air loss, pooled over the plant's units;
    and the fleet's mean measured NOx in hours 1 to 3 after a start, pooled over every unit (rec["pooled"])."""
    pooled = {}
    for k in (1, 2, 3):
        v = [n for w in out for n, s in zip(out[w]["nox"], out[w]["since"]) if s == k and n is not None]
        pooled[k] = float(np.mean(v)) if v else 0.0
    for u in out:
        out[u]["pooled"] = pooled
        v = [b_[3] for w in out if w.split("-")[0] == u.split("-")[0] for b_ in out[w]["blocks"] if b_[3] is not None]
        out[u]["plant_after"] = float(np.mean(v)) if v else None
    return out


def _standard(t):
    a, b = dt.datetime(2026, 3, 8, 3), dt.datetime(2026, 11, 1, 2)
    return t - dt.timedelta(hours=1) if a <= t < b else t


def _local(t):
    a, b = dt.datetime(2026, 3, 8, 2), dt.datetime(2026, 11, 1, 1)
    return t + dt.timedelta(hours=1) if a <= t < b else t


def prices(target, route="next"):
    """{(delivery point, gas day): $/Dth}. A gas day with no invoice line at a delivery point is priced, by route:
    "next" at the point's next invoice line (a line covers the gas days since the point's previous line, its quantity
    their total burn); "prev" at the point's previous line; "interp" between the two; "skip" left unpriced."""
    rows = {}
    for r in _rows(find(target, "gas_supply_daily_invoices")):
        rows.setdefault(r["delivery_point"], []).append((r["gas_day"], float(r["price_usd_per_dth"])))
    out = {}
    for p, ls in rows.items():
        ls.sort()
        for (d, v) in ls:
            out[(p, d)] = v
        if route == "skip":
            continue
        for (d0, v0), (d1, v1) in zip(ls, ls[1:]):
            a_, b_ = dt.date.fromisoformat(d0), dt.date.fromisoformat(d1)
            n = (b_ - a_).days
            for k in range(1, n):
                d = (a_ + dt.timedelta(days=k)).isoformat()
                out[(p, d)] = {"next": v1, "prev": v0}.get(route, round(v0 + (v1 - v0) * k / n, 4))
    return out


def _outage_terms(target, route="golden"):
    """Each combined-cycle unit's IEEE 762 terms over the ozone season, every hour local time from 1 May to
    30 September: FOH (hours in a full forced outage, U1 to U3, a later report replacing an earlier full outage it
    overlaps on the unit), the number of forced outages, SH (operating time), RSH (hours neither operating nor in a
    full outage, the part of a part hour not operating included), the actual starts, EFDH (each D1 or D2 hour outside
    a full outage at derate_mw over nameplate MW) and EFDHRS (the part of EFDH falling in reserve shutdown).
    Routes for the checks: "rows" counts operating rows for SH; "noresolve" keeps every full outage report;
    "standard" reads the events on the DAHS clock; "service" counts derates in service only."""
    a, b = dt.datetime(2026, 5, 1), dt.datetime(2026, 10, 1)
    cap = {}
    ws = load_workbook(find(target, "generating_unit_register"), read_only=True).active
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r and r[0]:
            cap[r[0]] = float(r[3])
    op, prev_on, starts = {}, {}, {}
    for r in _rows(find(target, "dahs_hourly_export")):
        u = r["UNIT_ID"]
        t = dt.datetime.combine(dt.date.fromisoformat(r["OP_DATE"]), dt.time(int(r["OP_HOUR"])))
        loc = t if route == "standard" else _local(t)
        f = float(r["OP_TIME"] or 0)
        if a <= loc < b:
            op[(u, loc)] = f
            if f > 0 and not prev_on.get(u, False):
                starts[u] = starts.get(u, 0) + 1
        prev_on[u] = f > 0
    evs, der = {}, {}
    for r in _rows(find(target, "gads_event_report")):
        s0 = dt.datetime.strptime(r["start_local"], "%Y-%m-%d %H:%M")
        e0 = dt.datetime.strptime(r["end_local"], "%Y-%m-%d %H:%M")
        if r["event_type"] in ("U1", "U2", "U3"):
            evs.setdefault(r["unit"], []).append((s0, e0, r["date_reported"], int(r["event_no"])))
        elif r["event_type"] in ("D1", "D2"):
            der.setdefault(r["unit"], []).append((s0, e0, float(r["derate_mw"])))
    out = {}
    hours = {}
    for (w, t) in op:
        hours.setdefault(w, []).append(t)
    for u in cc_units(target):
        keep = []
        if route == "noresolve":
            keep = evs.get(u, [])
        else:
            for e in sorted(evs.get(u, []), key=lambda e: (e[2], e[3]), reverse=True):
                if not any(e[0] < k[1] and k[0] < e[1] for k in keep):
                    keep.append(e)
        keep = [e for e in keep if e[0] < b and a < e[1]]
        fo = set()
        foh = 0
        for s0, e0, *_ in keep:
            t = max(a, s0)
            while t < min(b, e0):
                foh += 1 if route == "noresolve" or t not in fo else 0
                fo.add(t)
                t += dt.timedelta(hours=1)
        hs = hours.get(u, [])
        sh = sum(1 for t in hs if op[(u, t)] > 0) if route == "rows" else sum(op[(u, t)] for t in hs)
        rsh = sum(1 - op[(u, t)] for t in hs if t not in fo)
        efdh = efdhrs = 0.0
        for s0, e0, mw in der.get(u, []):
            t = max(a, s0)
            while t < min(b, e0):
                if t not in fo:
                    f = op.get((u, t), 0.0)
                    efdh += mw / cap[u] * (f if route == "service" else 1.0)
                    efdhrs += mw / cap[u] * (1 - f)
                t += dt.timedelta(hours=1)
        out[u] = dict(foh=foh, n_fo=len(keep), sh=sh, rsh=rsh, starts=starts.get(u, 0), efdh=efdh, efdhrs=efdhrs)
    return out


def ask_b(target, route="golden"):
    """Each unit's ozone-season equivalent forced outage rate (IEEE 762), per cent: 100 (FOH + EFDH) / (FOH + SH +
    EFDHRS). "nors" leaves EFDHRS out of the denominator; other routes as _outage_terms."""
    out = {}
    for u, x in _outage_terms(target, route).items():
        rs = 0.0 if route == "nors" else x["efdhrs"]
        out[u] = 100.0 * (x["foh"] + x["efdh"]) / (x["foh"] + x["sh"] + rs)
    return out


def ask_a(target, route="golden"):
    """Each unit's ozone-season demand equivalent forced outage rate (IEEE 762, EFORd), per cent:
    100 (f FOH + fp EFDH) / (SH + f FOH), with f = (1/r + 1/T) / (1/r + 1/T + 1/D), r = FOH over the number of forced
    outages, T = RSH over the attempted starts, D = SH over the actual starts, fp = SH / AH and AH = SH + RSH.
    "plain" is the plain rate with f and fp at one; "nofp" leaves fp at one; other routes as _outage_terms."""
    out = {}
    for u, x in _outage_terms(target, route).items():
        r = x["foh"] / x["n_fo"] if x["n_fo"] else float("inf")
        T = x["rsh"] / x["starts"] if x["starts"] else float("inf")
        D = x["sh"] / x["starts"] if x["starts"] else float("inf")
        inv = lambda v: 0.0 if v == float("inf") or v == 0 else 1.0 / v
        f = (inv(r) + inv(T)) / (inv(r) + inv(T) + inv(D)) if route != "plain" else 1.0
        fp = x["sh"] / (x["sh"] + x["rsh"]) if route not in ("plain", "nofp") else 1.0
        out[u] = 100.0 * (f * x["foh"] + fp * x["efdh"]) / (x["sh"] + f * x["foh"])
    return out


def season_totals(target):
    rec = record(target)
    return {u: (sum(o["load"]), len(o["load"])) for u, o in rec.items()}
