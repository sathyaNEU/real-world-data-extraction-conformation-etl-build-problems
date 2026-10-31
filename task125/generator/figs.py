"""Every graded figure, computed from the cut pack the way the golden reads it, with the ladder's rungs and the asks'
wrong handlings beside it."""
import csv
import datetime as dt
import os
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

import pack as P
import world as W

CONV = 0.0864
EC_ALERT = 1500.0
WET_MONTHS = [(2025, 11), (2025, 12), (2026, 1), (2026, 2), (2026, 3), (2026, 4)]
QUARTERS = {"Q1": [(2025, 10), (2025, 11), (2025, 12)], "Q2": [(2026, 1), (2026, 2), (2026, 3)],
            "Q3": [(2026, 4), (2026, 5), (2026, 6)], "Q4": [(2026, 7), (2026, 8), (2026, 9)]}


def _rows(target, key):
    with open(os.path.join(target, P.FILES[key]), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load(target):
    wb = load_workbook(os.path.join(target, P.FILES["register"]), read_only=True)
    sites = list(wb["Sites"].iter_rows(values_only=True))[1:]
    weirs = list(wb["Weirs"].iter_rows(values_only=True))[1:]
    units = list(wb["Resource units"].iter_rows(values_only=True))[1:]
    boundary = {s[3]: s[0] for s in sites if str(s[7]).startswith("boundary monitor")}
    station = {w[0]: w[1] for w in weirs}
    ru = [(u[0], u[3], [x.strip() for x in (u[5] or "").split(",") if x.strip()]) for u in units]
    so4 = {}
    best = {}
    for r in _rows(target, "lab"):
        if r["analyte"] != "SO4":
            continue
        key = (r["site_code"], r["sample_date"])
        rank = (r["lab_sample_id"].endswith("-R"), r["analysed_date"])
        if key not in best or rank > best[key]:
            best[key] = rank
            so4[key] = float(r["result"].lstrip("<"))
    flow = {(r["station"], r["date"]): float(r["mean_flow_m3s"]) for r in _rows(target, "gauges")}
    runs = sorted({dt.date.fromisoformat(k[1]) for k in so4})
    return dict(boundary=boundary, station=station, ru=ru, so4=so4, flow=flow, runs=runs)


def dry_runs(D):
    return [d for d in D["runs"] if W.DRY0 <= d <= W.DRY1]


def point_load(D, code, d):
    """the boundary monitor's sulfate on the run times the boundary weir's mean flow that day, t/d"""
    weir = [u for u in D["ru"] if u[0] == code][0][1]
    c = D["so4"][(D["boundary"][code], d.isoformat())]
    q = D["flow"][(D["station"][weir], d.isoformat())]
    return c * q * CONV


def conserved_load(D, code, d, memo=None):
    """the sulfate the unit's water carries past its boundary: what its inflows carry in, each source unit measured
    at its own boundary, where its water is mixed (sulfate is conservative over these reaches)"""
    memo = {} if memo is None else memo
    if (code, d) in memo:
        return memo[(code, d)]
    inflows = [u for u in D["ru"] if u[0] == code][0][2]
    v = point_load(D, code, d) if not inflows else sum(conserved_load(D, i, d, memo) for i in inflows)
    memo[(code, d)] = v
    return v


def season_loads(D, method="golden"):
    runs = dry_runs(D)
    out = {}
    for code, weir, inflows in D["ru"]:
        if method == "golden":
            vals = [conserved_load(D, code, d) for d in runs]
        elif method == "point":
            vals = [point_load(D, code, d) for d in runs]
        elif method == "downstream":
            # the next mixed monitor below carries the same water: the unit's load read there, less what joins between
            vals = [conserved_load(D, code, d) for d in runs]
        else:
            raise ValueError(method)
        out[code] = float(np.mean(vals))
    return out


def ratio_loads(D):
    """the flow-weighted ratio estimator on the boundary samples: the runs' load over the runs' flow, times the
    season's mean flow"""
    runs = dry_runs(D)
    days = [W.DRY0 + dt.timedelta(days=i) for i in range((W.DRY1 - W.DRY0).days + 1)]
    out = {}
    for code, weir, inflows in D["ru"]:
        st = D["station"][weir]
        lq = np.mean([point_load(D, code, d) for d in runs])
        qr = np.mean([D["flow"][(st, d.isoformat())] for d in runs])
        qs = np.mean([D["flow"][(st, d.isoformat())] for d in days])
        out[code] = float(lq / qr * qs)
    return out


def ec_loads(target, D):
    """the loggers' daily EC turned into sulfate through each site's own sample pairs, times the day's flow, over
    every dry-season day; units without a logger read on their samples"""
    ec = defaultdict(list)
    for r in _rows(target, "ec"):
        t = dt.datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=2)
        ec[(r["site_code"], t.date())].append(float(r["ec_uS_cm"]))
    lab_ec = {}
    for r in _rows(target, "lab"):
        if r["analyte"] == "EC":
            lab_ec[(r["site_code"], r["sample_date"])] = float(r["result"]) * 10.0
    days = [W.DRY0 + dt.timedelta(days=i) for i in range((W.DRY1 - W.DRY0).days + 1)]
    pts = season_loads(D, "point")
    out = dict(pts)
    for lid, site in P.LOGGERS:
        code = [c for c, s in D["boundary"].items() if s == site][0]
        weir = [u for u in D["ru"] if u[0] == code][0][1]
        xs = [lab_ec[k] for k in sorted(lab_ec) if k[0] == site and (site, k[1]) in D["so4"]]
        ys = [D["so4"][k] for k in sorted(lab_ec) if k[0] == site and k in D["so4"]]
        b, a = np.polyfit(xs, ys, 1)
        vals = []
        for d in days:
            e = float(np.mean(ec[(site, d)]))
            vals.append((a + b * e) * D["flow"][(D["station"][weir], d.isoformat())] * CONV)
        out[code] = float(np.mean(vals))
    return out


def verdicts(loads):
    alloc = {r[0]: r[5] for r in W.RU}
    return {c: loads[c] > alloc[c] for c in loads}


def over_set(loads):
    return sorted(c for c, v in verdicts(loads).items() if v)


# ------------------------------------------------------------------ ask A: what each licensed discharge discharged
def ask_a(target, as_s="convert", meter="inspection", resub="latest"):
    rows = _rows(target, "returns")
    best = {}
    for r in rows:
        key = (r["discharge_point"], r["month"])
        if resub == "latest":
            if key not in best or r["submitted_on"] > best[key]["submitted_on"]:
                best[key] = r
        else:
            if key not in best or r["submitted_on"] < best[key]["submitted_on"]:
                best[key] = r
    insp = _rows(target, "inspections")
    swaps = {}
    for r in insp:
        f = r["findings"]
        if "final reading" in f:
            import re
            old = float(re.search(r"final reading ([0-9]+)", f).group(1))
            swaps[r["discharge_point"]] = (r["date"][:7], old)
    pts = sorted({k[0] for k in best})
    months = sorted({k[1] for k in best})
    out = {}
    for pt in pts:
        prev = None
        monthly = {}
        for m in months:
            r = best[(pt, m)]
            tot = float(r["totaliser_m3"])
            if prev is None:
                vol = None
            elif pt in swaps and swaps[pt][0] == m and meter == "inspection":
                vol = (swaps[pt][1] - prev) + tot
            elif tot < prev:
                vol = tot if meter == "restart" else 0.0
            else:
                vol = tot - prev
            prev = tot
            so4 = float(r["sulphate_mg_l"])
            holder = pt.split("-")[0]
            if as_s == "convert" and holder in W.LAB_AS_S_MINES and m >= W.LAB_AS_S_FROM.strftime("%Y-%m"):
                so4 *= W.S_TO_SO4
            monthly[m] = (vol, so4)
        for q, ms in QUARTERS.items():
            tons = 0.0
            for (y, mo) in ms:
                key = "%04d-%02d" % (y, mo)
                vol, so4 = monthly[key]
                tons += vol * so4 / 1e6
            out[(pt, q)] = tons
    return out


# ------------------------------------------------------------------ ask B: hours each logger read the water over 1,500
def ask_b(target, drift="linear", clock="sast", memory=True):
    visits = defaultdict(list)
    for r in _rows(target, "service"):
        t = dt.datetime.strptime(r["visit_local"], "%Y-%m-%d %H:%M")
        before, after = r["reading_before_clean_uS_cm"], r["reading_after_clean_uS_cm"]
        visits[r["logger_id"]].append((t, float(before) - float(after) if before and after else 0.0))
    for k in visits:
        visits[k].sort()
    out = defaultdict(int)
    readings = []
    for r in _rows(target, "ec"):
        t = dt.datetime.strptime(r["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
        readings.append((r["logger_id"], t + dt.timedelta(hours=2) if clock == "sast" else t, float(r["ec_uS_cm"])))
    if memory:
        have = {(a, b) for a, b, c in readings}
        for r in _rows(target, "memory"):
            t = dt.datetime.strptime(r["reading_local"], "%Y-%m-%d %H:%M")
            if (r["logger_id"], t) not in have:
                readings.append((r["logger_id"], t, float(r["ec_uS_cm"])))
    for lid, local, v in readings:
        if drift == "linear":
            vs = visits[lid]
            nxt = [x for x in vs if x[0] > local]
            prv = [x for x in vs if x[0] <= local]
            if nxt and prv:
                t1, d1 = nxt[0]
                t0 = prv[-1][0]
                v -= d1 * (local - t0).total_seconds() / (t1 - t0).total_seconds()
        if (local.year, local.month) in WET_MONTHS and v > P.TRIGGERS[lid]:
            out[(lid, "%04d-%02d" % (local.year, local.month))] += 1
    return {(lid, "%04d-%02d" % ym): out.get((lid, "%04d-%02d" % ym), 0) for lid, _ in P.LOGGERS for ym in WET_MONTHS}
