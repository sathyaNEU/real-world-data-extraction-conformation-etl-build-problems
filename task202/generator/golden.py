"""Every graded figure, the ladder's rungs and the default path, computed from the cut pack itself."""
import csv
import datetime as dt
import math
import os
from collections import defaultdict

import numpy as np
import openpyxl

import world as W

SEASON_MONTHS = (6, 7, 8, 9)


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def parse_uk(s):
    return dt.datetime.strptime(s, "%d/%m/%Y %H:%M")


def bst(local):
    return W.uk_offset(local) == 1


def utc_of_local(local, seen):
    """Station rows are UK clock; the repeated 01:00 hour each October is BST first, then GMT."""
    key = local
    n = seen.get(key, 0)
    seen[key] = n + 1
    off = W.uk_offset(local)
    if local.month == 10 and local.hour == 1 and _last_sunday(local.year, 10) == local.date():
        off = 1 if n == 0 else 0
    return local - dt.timedelta(hours=off)


def _last_sunday(y, m):
    d = dt.date(y, m, 31)
    while d.weekday() != 6:
        d -= dt.timedelta(1)
    return d


# ----------------------------------------------------------------------------------------------- readers
def station_hourly(T):
    """UTC hour -> dict(temp, flow); validated rows stand where both releases hold an hour."""
    out = {}
    for fn, rank in (("lenning_foot_hourly_provisional.csv", 0), ("lenning_foot_hourly_validated.csv", 1)):
        seen = {}
        for r in read_csv(os.path.join(T, fn)):
            u = utc_of_local(parse_uk(r["Timestamp (UK)"]), seen)
            if u in out and out[u]["rank"] > rank:
                continue
            out[u] = dict(temp=float(r["Water temp (C)"]), flow=float(r["Flow (m3/s)"]), rank=rank)
    return out


def buoy_surface(T):
    """UTC day -> mean temperature of the 0.5 to 5 m sensors."""
    acc = defaultdict(list)
    for r in read_csv(os.path.join(T, "fellside_buoy_thermistor_daily.csv")):
        z = float(r["Depth (m)"])
        if z <= 5.0:
            acc[r["Date (UTC)"]].append(float(r["Water temperature (degC)"]))
    return {dt.date.fromisoformat(k): float(np.mean(v)) for k, v in acc.items()}


def buoy_profiles(T):
    prof = defaultdict(dict)
    for r in read_csv(os.path.join(T, "fellside_buoy_thermistor_daily.csv")):
        prof[dt.date.fromisoformat(r["Date (UTC)"])][float(r["Depth (m)"])] = float(r["Water temperature (degC)"])
    return prof


def returns(T):
    wb = openpyxl.load_workbook(os.path.join(T, "fellmoor_wwtw_monthly_returns.xlsx"), data_only=True)
    out = {}
    for ws in wb.worksheets:
        rows = list(ws.iter_rows(values_only=True))
        hdr = [str(h) for h in rows[2]]
        for row in rows[3:]:
            if not row or row[0] is None:
                continue
            d = dict(zip(hdr, row))
            if "Site" in d:
                name = d["Site"].replace(" WwTW", "")
                mon = dt.datetime.strptime(d["Month"], "%b-%y")
                rec = dict(vol=d["Final effluent volume (m3)"], tp=d["TP mean (mg/l)"], load=d["TP load (kg)"],
                           temp=d["Final effluent temperature (deg C)"])
            else:
                name = d["Works"].title()
                mon = dt.datetime.strptime(d["Period"], "%Y-%m")
                rec = dict(vol=d["FE volume m3"], tp=d["TP mean mg/l"], load=d["TP load kg"], temp=d["FE temp mean (C)"])
            out[(name, mon.year, mon.month)] = rec
    return out


def outfall_monthly(T):
    wb = openpyxl.load_workbook(os.path.join(T, "mill_beck_outfall_monitoring.xlsx"), data_only=True)
    ws = wb["Monthly loads"]
    out = {}
    for row in list(ws.iter_rows(values_only=True))[1:]:
        m = dt.datetime.strptime(row[0], "%b %Y")
        out[(m.year, m.month)] = float(row[3])
    return out


def appraisal(T):
    wb = openpyxl.load_workbook(os.path.join(T, "programme_appraisals_2027.xlsx"), data_only=True)
    ws = wb["Shortlist"]
    out = {}
    for row in list(ws.iter_rows(values_only=True))[1:]:
        out[row[0]] = dict(title=row[1], credit=row[6] / 100.0)
    return out


def sampler(T):
    rows = []
    for r in read_csv(os.path.join(T, "lenning_foot_sampler_results.csv")):
        rows.append(dict(kind=r["Programme"], first=parse_uk(r["First sub-sample (UK)"]),
                         last=parse_uk(r["Last sub-sample (UK)"]), n=int(r["Sub-samples"]), tp=float(r["TP (ug/l)"])))
    return rows


def regulator(T):
    """station name -> UTC hour -> mean flow."""
    out = defaultdict(dict)
    for r in read_csv(os.path.join(T, "regulator_gauged_flows_hourly.csv")):
        out[r["station_name"]][dt.datetime.strptime(r["datetime"], "%Y-%m-%dT%H:%M:%SZ")] = float(r["mean_flow_m3s"])
    return out


# ----------------------------------------------------------------------------------------------- the call
def river_daily_temp(st):
    acc = defaultdict(list)
    for u, v in st.items():
        acc[u.date()].append(v["temp"])
    return {d: float(np.mean(v)) for d, v in acc.items()}


def insertion(T, st=None):
    """Per season: the June-to-September days the Lenning's water was denser than the 0-5 m water at the buoy,
    the days compared, and the depth range at which the river's temperature meets the lake's profile."""
    st = st or station_hourly(T)
    tr = river_daily_temp(st)
    surf = buoy_surface(T)
    prof = buoy_profiles(T)
    out = {}
    for y in W.SEASONS:
        dense = n = 0
        zs = []
        d = dt.date(y, 6, 1)
        while d <= dt.date(y, 9, 30):
            if d in tr and d in surf:
                n += 1
                if W.density(tr[d]) > W.density(surf[d]):
                    dense += 1
                p = prof[d]
                z = [k for k in sorted(p) if p[k] <= tr[d]]
                zs.append(z[0] if z else 99.0)
            d += dt.timedelta(1)
        out[y] = dict(dense=dense, n=n, zmin=min(zs), zmax=max(zs))
    return out


def effluent_buoyancy(T, ret=None):
    ret = ret or returns(T)
    surf = buoy_surface(T)
    out = {}
    for y in W.SEASONS:
        for m in SEASON_MONTHS:
            days = [d for d in surf if d.year == y and d.month == m]
            s = float(np.mean([surf[d] for d in days]))
            out[(y, m)] = (ret[("Hollinsby", y, m)]["temp"], round(s, 2))
    return out


def season_figures(T):
    ret = returns(T)
    of = outfall_monthly(T)
    ap = appraisal(T)
    ins = insertion(T)
    res = {}
    for y in W.SEASONS:
        hol = sum(ret[("Hollinsby", y, m)]["load"] for m in SEASON_MONTHS)
        bra = sum(ret[("Brathwick", y, m)]["load"] for m in SEASON_MONTHS)
        out = sum(of[(y, m)] for m in SEASON_MONTHS)
        share = 0.0 if ins[y]["dense"] == ins[y]["n"] else (ins[y]["n"] - ins[y]["dense"]) / ins[y]["n"]
        res[y] = dict(C=ap["C"]["credit"] * hol, D=ap["D"]["credit"] * out, B=ap["B"]["credit"] * bra * share,
                      A=None, hol=hol, bra=bra, out=out)
    return res, ap, ins


def default_path(T):
    """The season's load apportionment: the Lenning's daily load from the day bottles and the station's daily
    flow, Brathwick's from its returns and the farms as the remainder; Hollinsby and Mill Beck from theirs."""
    st = station_hourly(T)
    flow = defaultdict(list)
    for u, v in st.items():
        flow[u.date()].append(v["flow"])
    dayb = {}
    for b in sampler(T):
        if b["kind"] == "DAY":
            dayb[b["first"].date()] = b["tp"]
    ret = returns(T)
    of = outfall_monthly(T)
    ap = appraisal(T)
    out = {}
    for y in W.SEASONS:
        lr = 0.0
        d = dt.date(y, 6, 1)
        while d <= dt.date(y, 9, 30):
            q = float(np.mean(flow[d]))
            c = dayb.get(d)
            if c is None:          # a missing day bottle: the neighbouring days' mean
                c = np.mean([dayb[x] for x in (d - dt.timedelta(1), d + dt.timedelta(1)) if x in dayb])
            lr += q * 86400 * c / 1e6
            d += dt.timedelta(1)
        bra = sum(ret[("Brathwick", y, m)]["load"] for m in SEASON_MONTHS)
        hol = sum(ret[("Hollinsby", y, m)]["load"] for m in SEASON_MONTHS)
        outl = sum(of[(y, m)] for m in SEASON_MONTHS)
        out[y] = dict(A=ap["A"]["credit"] * (lr - bra), B=ap["B"]["credit"] * bra, C=ap["C"]["credit"] * hol,
                      D=ap["D"]["credit"] * outl, river=lr)
    return out


def hourly_conc(T):
    """UTC hour -> TP of the bottle that took that hour's sub-sample: the storm programme's bottle where it sampled,
    the day bottle otherwise."""
    conc = {}
    bottles = sampler(T)
    for kind in ("DAY", "STORM"):
        for b in bottles:
            if b["kind"] != kind:
                continue
            u0 = b["first"] - dt.timedelta(hours=W.uk_offset(b["first"]))
            u1 = b["last"] - dt.timedelta(hours=W.uk_offset(b["last"]))
            t = u0
            while t <= u1:
                conc[t] = b["tp"]
                t += dt.timedelta(hours=1)
    return conc


def annual_path(T):
    """Rung 0, the annual inventory: each programme on its source's whole water year (October to September), the
    Lenning's load hour by hour from the station's flow and the sampler's bottles (a day the sampler lost takes the
    day before's bottle), the farms as the river's load less Brathwick's; the three years averaged."""
    st = station_hourly(T)
    conc = hourly_conc(T)
    ret = returns(T)
    of = outfall_monthly(T)
    ap = appraisal(T)
    out = {}
    for y in W.SEASONS:
        lr = 0.0
        t = dt.datetime(y - 1, 10, 1)
        z = dt.datetime(y, 10, 1)
        while t < z:
            c = conc.get(t)
            k = 1
            while c is None:
                c = conc.get(t - dt.timedelta(hours=24 * k))
                k += 1
            lr += st[t]["flow"] * 3600 * c / 1e6
            t += dt.timedelta(hours=1)
        mons = [(y - 1, m) for m in (10, 11, 12)] + [(y, m) for m in range(1, 10)]
        bra = sum(ret[("Brathwick",) + k]["load"] for k in mons)
        hol = sum(ret[("Hollinsby",) + k]["load"] for k in mons)
        outl = sum(of[k] for k in mons)
        out[y] = dict(A=ap["A"]["credit"] * (lr - bra), B=ap["B"]["credit"] * bra, C=ap["C"]["credit"] * hol,
                      D=ap["D"]["credit"] * outl, river=lr)
    return out


# ----------------------------------------------------------------------------------------------- asks
def winter_ask(T, st=None):
    """The Lenning's inflow to the lake and its phosphorus, 1 October to 30 April (UTC), each hour's flow at the
    concentration of the bottle that took that hour's sub-sample; before 1 June 2024 the station's flow is the
    Lenning Bridge feed and the Brankell Beck, which joins below that gauge, is added hour by hour from its gauge."""
    st = st or station_hourly(T)
    reg = regulator(T)
    brankell = reg["BRANKELL BECK AT HOWE"]
    conc = hourly_conc(T)
    res = {}
    for (y0, y1) in W.WINTERS:
        a = dt.datetime(y0, 10, 1) - dt.timedelta(hours=1)      # 1 October 00:00 BST
        z = dt.datetime(y1, 5, 1) - dt.timedelta(hours=1)       # 1 May 00:00 BST
        vol = load = 0.0
        t = a
        while t < z:
            q = st[t]["flow"]
            if t.date() < W.GAUGE_SWITCH:
                q = q + brankell[t]
            vol += q * 3600
            load += q * 3600 * conc[t] / 1e6
            t += dt.timedelta(hours=1)
        res[(y0, y1)] = dict(vol=vol / 1e6, load=load)
    return res


def survey_ask(T):
    reg = {r["UPRN"]: r for r in read_csv(os.path.join(T, "hollinsby_address_register_extract.csv"))}
    flats = defaultdict(list)
    for u, r in reg.items():
        if r["PARENT_UPRN"]:
            flats[r["PARENT_UPRN"]].append(u)
    found, fixed = set(), set()
    cutoff = dt.date(2026, 9, 30)
    for v in read_csv(os.path.join(T, "connect_right_visits_export.csv")):
        day = dt.datetime.strptime(v["Visit ref"].split("-")[1], "%y%m%d").date()
        dwell = flats.get(v["UPRN"]) or [v["UPRN"]]
        if v["Outcome"] == "MISCONNECTED":
            found.update(dwell)
        elif v["Outcome"] == "FIX CONFIRMED" and day <= cutoff:
            fixed.update(dwell)
    fixed &= found
    return dict(found=len(found), fixed=len(fixed), open=len(found - fixed))


def lab_ask(T):
    rows = read_csv(os.path.join(T, "fellside_lake_lab_results.csv"))
    res = {}
    for y in (2025, 2026):
        acc = defaultdict(list)
        for r in rows:
            d = dt.datetime.strptime(r["sampled"], "%d-%b-%Y").date()
            if d.year != y or not (6 <= d.month <= 9):
                continue
            north = (r["site"] == "NB" and d < dt.date(2025, 4, 1)) or r["site"] == "SWL01"
            if north and r["depth_m"] == "0-5":
                acc[r["determinand"]].append(float(r["result"]))
        res[y] = dict(tp=float(np.mean(acc["Total phosphorus"])), chl=float(np.mean(acc["Chlorophyll a"])))
    return res


def all_figures(T):
    seas, ap, ins = season_figures(T)
    F = {}
    for y in W.SEASONS:
        F["C_%d" % y] = seas[y]["C"]
        F["D_%d" % y] = seas[y]["D"]
        F["B_%d" % y] = seas[y]["B"]
    F["C_mean"] = float(np.mean([seas[y]["C"] for y in W.SEASONS]))
    F["D_mean"] = float(np.mean([seas[y]["D"] for y in W.SEASONS]))
    F["A_mean"] = 0.0
    F["B_mean"] = float(np.mean([seas[y]["B"] for y in W.SEASONS]))
    F["gap"] = F["C_mean"] - F["D_mean"]
    wa = winter_ask(T)
    F["inflow_2023_24"] = wa[(2023, 2024)]["vol"]
    for k, v in wa.items():
        F["load_%d_%02d" % (k[0], k[1] % 100)] = v["load"]
    sa = survey_ask(T)
    F.update({"dw_found": sa["found"], "dw_fixed": sa["fixed"], "dw_open": sa["open"]})
    la = lab_ask(T)
    for y, v in la.items():
        F["tp_%d" % y] = v["tp"]
        F["chl_%d" % y] = v["chl"]
    return F, seas, ins
