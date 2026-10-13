"""The analysis, read from the shipped files only: each tributary's total phosphorus samples (both organisations,
routine and accepted, one unit), each station's daily mean discharge (approved records, local days, drainage-area
ratio), every route's water-year 2026 load, the slate each route funds, and the two asks."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

import pack as P
import world as W

K = W.CFS_DAY_KG
WY26 = [W.WY26_START + dt.timedelta(days=i) for i in range((W.WY_END - W.WY26_START).days + 1)]


def load(target):
    f = lambda k: os.path.join(target, P.FILES[k])
    import openpyxl
    wq = pd.read_csv(f("wq"), dtype=str)
    uv = pd.read_csv(f("uv"), comment="#", dtype={"gage_id": str, "qualifiers": str})
    dv = pd.read_csv(f("dv"), comment="#", dtype={"gage_id": str, "qualifiers": str})
    wb = openpyxl.load_workbook(f("register"), read_only=True)
    st = [r for r in wb["Stations"].iter_rows(min_row=5, values_only=True) if r[0]]
    streams = [r for r in wb["Streams"].iter_rows(min_row=4, values_only=True) if r[0]]
    fac = [r for r in wb["Facilities"].iter_rows(min_row=4, values_only=True) if r[0]]
    dmr = pd.read_csv(f("dmr"), dtype=str)
    con = pd.read_csv(f("contracts"), dtype=str, comment="#")
    fld = pd.read_csv(f("fields"), dtype=str)
    return dict(wq=wq, uv=uv, dv=dv, stations=st, streams=streams, facilities=fac, dmr=dmr, contracts=con, fields=fld)


def register(L):
    """tributary name -> (commission station, college station, gage, drainage-area ratio, station river km)"""
    out = {}
    for r in L["stations"]:
        name, st, lab, gage, da_s, da_g, rkm = r[:7]
        out[name] = dict(st=st, lab=lab, gage=str(gage), ratio=float(da_s) / float(da_g), rkm=float(rkm))
    return out


# ---------------------------------------------------------------------------------------------- the samples
def tp_samples(L, accepted_only=True, routine_only=True):
    """each tributary's total phosphorus results in mg/L by local sample date"""
    reg = register(L)
    by_station = {}
    for name, r in reg.items():
        by_station[r["st"]] = name
        by_station[r["lab"]] = name
    w = L["wq"]
    tp = w[w["CharacteristicName"].isin(["Phosphorus", "Total Phosphorus, mixed forms"]) & w["ResultSampleFractionText"].eq("Total")]
    if routine_only:
        tp = tp[tp["ActivityTypeCode"].eq("Sample-Routine")]
    if accepted_only:
        tp = tp[tp["ResultStatusIdentifier"].eq("Accepted")]
    v = pd.to_numeric(tp["ResultMeasureValue"], errors="coerce")
    unit = tp["ResultMeasure/MeasureUnitCode"]
    mgl = np.where(unit.eq("ug/L"), v / 1000.0, v)
    out = {n: [] for n in reg}
    for loc, d, c in zip(tp["MonitoringLocationIdentifier"], tp["ActivityStartDate"], mgl):
        if loc in by_station and np.isfinite(c):
            out[by_station[loc]].append((dt.date.fromisoformat(d), float(c)))
    return {k: sorted(v) for k, v in out.items()}


# ---------------------------------------------------------------------------------------------- the flows
def daily_q(L, local=True, ratio=True, uv=None):
    """each tributary's daily mean discharge at its compliance station (cfs), water years 2024 to 2026: the approved
    daily values, then the approved 15-minute values averaged over local days"""
    reg = register(L)
    uv = L["uv"] if uv is None else uv
    t = pd.to_datetime(uv["datetime_utc"])
    if local:
        off = pd.Series(5, index=t.index)
        for a, b in W.DST:          # daylight time from 07:00 UTC on the start date to 06:00 UTC on the end date
            off[(t >= pd.Timestamp(a.year, a.month, a.day, 7)) & (t < pd.Timestamp(b.year, b.month, b.day, 6))] = 4
        loc = (t - pd.to_timedelta(off, unit="h")).dt.date
    else:
        loc = t.dt.date
    g = uv.assign(day=loc).groupby(["gage_id", "day"])["discharge_cfs"].mean()
    dv = L["dv"]
    out = {}
    for name, r in reg.items():
        q = {dt.date.fromisoformat(d): float(v) for d, v in zip(dv.loc[dv["gage_id"].eq(r["gage"]), "date"],
                                                                 dv.loc[dv["gage_id"].eq(r["gage"]), "discharge_cfs"])}
        for d, v in g.loc[r["gage"]].items():
            if W.WY26_START <= d <= W.WY_END:
                q[d] = float(v)
        f = r["ratio"] if ratio else 1.0
        out[name] = {d: v * f for d, v in q.items()}
    return out


def doy(d):
    return d.timetuple().tm_yday


# ---------------------------------------------------------------------------------------------- the routes
def rating(samples, q, days, season=True, corr="smear", quad=False, fit=None):
    """a rating curve of log concentration on log discharge (with seasonal terms), applied to every day"""
    s = [(d, c) for d, c in samples if d in q and (fit is None or fit[0] <= d <= fit[1])]
    lq = np.log([q[d] for d, c in s])
    y = np.log([c for d, c in s])
    def X(lqv, dd):
        cols = [np.ones(len(lqv)), lqv]
        if quad:
            cols.append(lqv ** 2)
        if season:
            a = np.array([2 * np.pi * doy(d) / 365.25 for d in dd])
            cols += [np.sin(a), np.cos(a)]
        return np.column_stack(cols)
    A = X(lq, [d for d, c in s])
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    r = y - A @ beta
    qd = np.array([q[d] for d in days])
    pred = np.exp(X(np.log(qd), days) @ beta)
    s2 = float(np.sum(r ** 2) / (len(y) - A.shape[1]))
    f = {"none": 1.0, "smear": float(np.mean(np.exp(r))), "mle": float(np.exp(s2 / 2))}[corr]
    return float(np.sum(pred * qd) * K * f), dict(beta=beta, s2=s2, n=len(y), smear=float(np.mean(np.exp(r))))


def interp(samples, q, days):
    """the default: each day's concentration interpolated between the water year's samples"""
    s = [(d, c) for d, c in samples if W.WY26_START <= d <= W.WY_END]
    x = np.array([d.toordinal() for d, c in s])
    y = np.array([c for d, c in s])
    xd = np.array([d.toordinal() for d in days])
    qd = np.array([q[d] for d in days])
    return float(np.sum(np.interp(xd, x, y) * qd) * K)


def averaging(samples, q, days, weight="time"):
    s = [(d, c) for d, c in samples if W.WY26_START <= d <= W.WY_END]
    vol = float(np.sum([q[d] for d in days]) * K)
    c = np.array([c for d, c in s])
    if weight == "time":
        return float(np.mean(c)) * vol
    w = np.array([q[d] for d, c in s])
    return float(np.sum(c * w) / np.sum(w)) * vol


def monthly(samples, q, days):
    """each month's samples (mean) times the month's discharge"""
    s = [(d, c) for d, c in samples if W.WY26_START <= d <= W.WY_END]
    tot = 0.0
    for m in sorted({(d.year, d.month) for d in days}):
        cs = [c for d, c in s if (d.year, d.month) == m]
        if not cs:
            continue
        tot += float(np.mean(cs)) * float(np.sum([q[d] for d in days if (d.year, d.month) == m]) * K)
    return tot


ROUTES = ("G1 rating curve, seasonal, smearing", "G2 rating curve, seasonal, normal-theory correction",
          "G3 rating curve, no seasonal terms, smearing", "G4 rating curve, quadratic in discharge, smearing",
          "G5 rating curve, no retransformation correction", "G6 rating curve, water years 2025 and 2026",
          "G7 rating curve, water year 2026 only",
          "R0 interpolation (default)", "R2 sample mean times volume", "R3 flow-weighted sample mean times volume",
          "R4 monthly sample times monthly volume")
GOLDEN = ROUTES[:7]
GOLD = ROUTES[0]
DEFAULT = "R0 interpolation (default)"


def route_loads(L, samples=None, q=None):
    samples = samples or tp_samples(L)
    q = q or daily_q(L)
    out = {nm: {} for nm in ROUTES}
    info = {}
    for name in samples:
        s, qq = samples[name], q[name]
        out[ROUTES[0]][name], info[name] = rating(s, qq, WY26)
        out[ROUTES[1]][name], _ = rating(s, qq, WY26, corr="mle")
        out[ROUTES[2]][name], _ = rating(s, qq, WY26, season=False)
        out[ROUTES[3]][name], _ = rating(s, qq, WY26, quad=True)
        out[ROUTES[4]][name], _ = rating(s, qq, WY26, corr="none")
        out[ROUTES[5]][name], _ = rating(s, qq, WY26, fit=(dt.date(2024, 10, 1), W.WY_END))
        out[ROUTES[6]][name], _ = rating(s, qq, WY26, fit=(W.WY26_START, W.WY_END))
        out[ROUTES[7]][name] = interp(s, qq, WY26)
        out[ROUTES[8]][name] = averaging(s, qq, WY26)
        out[ROUTES[9]][name] = averaging(s, qq, WY26, weight="flow")
        out[ROUTES[10]][name] = monthly(s, qq, WY26)
    return out, info


def slate(loads, alloc, n=3):
    ex = {k: loads[k] - alloc[k] for k in loads}
    top = sorted((k for k in ex if ex[k] > 0), key=lambda k: -ex[k])[:n]
    return top, ex


# ------------------------------------------------------------------------------------------------- the asks
def stream_to_tributary(L):
    """each stream's tributary and the river km on the tributary where it joins (a tributary maps to itself)"""
    names = {r[0] for r in L["stations"]}
    m = {r[0]: (r[1], float(r[2])) for r in L["streams"]}
    def walk(s):
        if s in names:
            return s, None
        into, rkm = m[s]
        t, _ = walk(into)
        return t, rkm
    return walk


def ask_wastewater(L, how="network", days="period"):
    """each tributary's water-year 2026 phosphorus from permitted facilities upstream of its compliance station (kg):
    the latest submission for each reporting period, its monthly average concentration times its monthly average flow
    (or its monthly average mass) for each day it covers; outfalls placed on the stream network by river km and service
    dates. how="name" joins a facility to the tributary its receiving water is named for; days="month" multiplies a
    report by the days in its end month"""
    reg = register(L)
    walk = stream_to_tributary(L)
    d = L["dmr"].copy()
    d["start"] = pd.to_datetime(d["MONITORING_PERIOD_START_DATE"]).dt.date
    d["end"] = pd.to_datetime(d["MONITORING_PERIOD_END_DATE"]).dt.date
    d["recv"] = d["RECEIVED_DATE"]
    d = d[d["STATISTICAL_BASE"].eq("MO AVG")]
    d = d.sort_values("recv").groupby(["PERMIT_ID", "OUTFALL", "end", "PARAMETER_DESC"]).tail(1)     # the latest submission
    out = {n: 0.0 for n in reg}
    outfalls = {}
    for r in L["facilities"]:
        pid, fname, of, rw, rkm, a, b = r[:7]
        outfalls[(pid, of)] = (rw, float(rkm), a, b)
    for (pid, of, start, end), g in d.groupby(["PERMIT_ID", "OUTFALL", "start", "end"]):
        rw, rkm, a, b = outfalls[(pid, of)]
        n_days = (end - start).days + 1 if days == "period" else end.day
        tpr = g[g["PARAMETER_DESC"].str.startswith("Phosphorus")].tail(1)
        flw = g[g["PARAMETER_DESC"].str.startswith("Flow")].tail(1)
        kg = 0.0
        for (_, t), (_, f) in zip(tpr.iterrows(), flw.iterrows()):
            if t["DMR_UNIT"] == "lb/d":
                kg += float(t["DMR_VALUE"]) * W.LB_KG * n_days
            else:
                kg += float(t["DMR_VALUE"]) * float(f["DMR_VALUE"]) * W.GAL_L * n_days
        if how == "network":
            trib, join = walk(rw)
            pos = rkm if join is None else join
            if pos <= reg[trib]["rkm"]:
                continue
            out[trib] += kg
        else:
            if rw in out:
                out[rw] += kg
    return out


def ask_cover(L, how="split"):
    """each watershed's 2026 cover crop acres: the contracts in force for crop year 2026 at their latest amendment, each
    enrolled field's acres shared among the watersheds it lies in by the program's overlay. The wrong reads:
    how="split_contract" shares each line's contracted acres (the contract's) by the overlay; "label_latest" puts each
    line's contracted acres under the line's watershed; "label_field" puts each field's own acres under the line's
    watershed; "label_all" puts each line's contracted acres under its watershed over every line of every amendment"""
    c = L["contracts"].copy()
    c["amendment_no"] = c["amendment_no"].astype(int)
    if how != "label_all":
        c = c[c["amendment_no"].eq(c.groupby("contract_id")["amendment_no"].transform("max"))]
    c = c[(c["first_crop_year"].astype(int) <= W.WY) & (c["last_crop_year"].astype(int) >= W.WY)]
    reg = register(L)
    out = {n: 0.0 for n in reg}
    f = L["fields"]
    share, field_acres = {}, {}
    for fid, fa, ws, sh in zip(f["field_id"], f["field_acres"], f["watershed"], f["share_of_field"]):
        share.setdefault(fid, []).append((ws, float(sh)))
        field_acres[fid] = float(fa)
    for fid, ca, ws in zip(c["field_id"], c["contracted_acres"].astype(float), c["watershed"]):
        if how == "split":
            for w_, sh in share[fid]:
                out[w_] += field_acres[fid] * sh
        elif how == "split_contract":
            for w_, sh in share[fid]:
                out[w_] += ca * sh
        elif how == "label_field":
            out[ws] += field_acres[fid]
        else:
            out[ws] += ca
    return out
