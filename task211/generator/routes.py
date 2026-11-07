"""The ladder, computed from target/ alone: each rung is a complete pipeline a competent analyst files, run on the
shipped files, and the set of stations (with dates) it ends on.

  R0  the operating procedure's own screen: every period of investigation-level values (reference level plus 30
      nSv/h on the alarm configuration), cleared as natural when the nearest valley rain gauge tipped within an hour
      of it; the rest notified (the default path)
  R1  R0, also clearing a dry period when a neighbouring station within 18 km was elevated at the same time
  R2  R1, keeping only the dry, lonely periods that begin at night (radiography's working hours)
  R3  the golden: the excursions whose excess falls by more than half in one ten-minute step and stays down
"""
import csv
import datetime as dt
import json
import os

import numpy as np
from openpyxl import load_workbook

import golden as G
import pack
import world as W

PAD = 6            # ten-minute intervals either side of a period searched for rain


def register(tgt):
    wb = load_workbook(os.path.join(tgt, pack.FILES["register"]), read_only=True)
    rows = list(wb["Stations"].iter_rows(values_only=True))
    wb.close()
    return {r[0]: dict(name=r[1], e=float(r[3]), n=float(r[4]), alt=float(r[5])) for r in rows[1:]}


def gauges(tgt):
    sites = {}
    with open(os.path.join(tgt, pack.FILES["gauge_sites"]), newline="") as f:
        for r in list(csv.reader(f))[1:]:
            sites[r[0]] = (float(r[2]), float(r[3]))
    series = {g: np.zeros(W.N10) for g in sites}
    with open(os.path.join(tgt, pack.FILES["gauges"]), newline="") as f:
        rd = csv.reader(f); next(rd)
        for g, stamp, mm in rd:
            t = dt.datetime.strptime(stamp, "%d/%m/%Y %H:%M") - W.BST
            k = int((t - W.Q_START).total_seconds() // 600)
            if 0 <= k < W.N10 and float(mm) > 0:
                series[g][k:k + 2] += float(mm)
    return sites, series


def references(tgt):
    cfg = json.load(open(os.path.join(tgt, pack.FILES["alarm"])))
    return {s["siteId"]: float(s["referenceLevel"]) for s in cfg["sites"]}


def periods(mask):
    out = []
    t = 0
    n = len(mask)
    while t < n:
        if mask[t]:
            s = t
            while t < n and mask[t]:
                t += 1
            out.append((s, t))
        else:
            t += 1
    return out


def ladder(g, tgt):
    vals, stat = g["vals"], g["stat"]
    reg = register(tgt)
    sites, rain = gauges(tgt)
    ref = references(tgt)
    near = {}
    for c, s in reg.items():
        near[c] = min(sites, key=lambda k: (sites[k][0] - s["e"]) ** 2 + (sites[k][1] - s["n"]) ** 2)
    nb = {c: [k for k in reg if k != c and np.hypot(reg[k]["e"] - reg[c]["e"], reg[k]["n"] - reg[c]["n"]) < 18000]
          for c in reg}
    ex = {}
    for c, v in vals.items():
        x = v.copy(); x[stat[c] != "V"] = np.nan
        ex[c] = x - G.rolling_median(x)
    out = dict(R0={}, R1={}, R2={}, inv_counts={}, near=near)
    for c in sorted(vals):
        x = vals[c].copy(); x[stat[c] != "V"] = np.nan
        inv = np.nan_to_num(x, nan=-1) >= ref[c] + 30
        out["inv_counts"][c] = int(inv.sum())
        for s, e in periods(inv):
            a, b = max(0, s - PAD), min(W.N10, e + PAD)
            dry = rain[near[c]][a:b].sum() == 0
            if not dry:
                continue
            day = (W.Q_START + dt.timedelta(minutes=10 * s)).date()
            out["R0"].setdefault(c, set()).add(day)
            lonely = not any((np.nan_to_num(ex[k][s:e], nan=-99) > 10).any() for k in nb[c])
            if not lonely:
                continue
            out["R1"].setdefault(c, set()).add(day)
            hour = (s % 144) / 6.0
            if hour >= 19 or hour < 6:
                out["R2"].setdefault(c, set()).add(day)
    out["R3"] = {c: set(v["dates"]) for c, v in g["call"].items()}
    wet = set()
    for c, v in g["call"].items():
        for s, e, f in v["episodes"]:
            if rain[near[c]][max(0, s - PAD):min(W.N10, e + PAD)].sum() > 0:
                wet.add((c, (W.Q_START + dt.timedelta(minutes=10 * s)).date()))
    out["wet_days"] = len(wet)
    out["wet_detection_days"] = sorted(wet)
    for k in ("R0", "R1", "R2", "R3"):
        out[k + "_codes"] = sorted(out[k])
    return out
