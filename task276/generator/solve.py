"""Solve the shipped pack: the drivers each shortlisted cab fails (the golden and every rung below it) and the fleet
figures the asks grade. Reads only files under target/, plus the document constants the generator wrote into them
(verify.py reads those constants back out of the documents on its own path)."""
import csv
import datetime as dt
import math
import os

import pandas as pd

import pack as PK
import params as P
import world as Wd

D = dt.timedelta
KG_PER_LB = 0.45359237


def _read_csv(root, key):
    with open(os.path.join(root, PK.FILES[key]), encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _xlsx(root, key):
    return pd.read_excel(os.path.join(root, PK.FILES[key]))


def _d(x):
    if x is None or (not isinstance(x, str) and pd.isna(x)):
        return None
    if isinstance(x, (dt.datetime, pd.Timestamp)):
        return x.date() if hasattr(x, "date") else x
    if x is None or (isinstance(x, float) and math.isnan(x)) or x == "":
        return None
    s = str(x)
    if "/" in s:
        p = s.split("/")
        y = int(p[2]) + (2000 if len(p[2]) == 2 else 0)
        return dt.date(y, int(p[1]), int(p[0]))
    return dt.date.fromisoformat(s[:10])


# ----------------------------------------------------------------------------------------------- drivers
def drivers(root, which="latest", population="roster", crosswalk=True, lb=KG_PER_LB):
    roster = _read_csv(root, "roster")
    cw = _xlsx(root, "crosswalk")
    to_new = dict(zip(cw["Former Vennerley staff number"].astype(str), cw["Service staff number"].astype(str)))
    m = _xlsx(root, "measure")
    recs = {}
    for r in m.itertuples(index=False):
        key = str(r[1])
        if crosswalk and key in to_new:
            key = to_new[key]
        if r.Form == "Vennerley paper form":
            stature = (12 * r[6] + r[7]) * 25.4
            seh = r[9] * 25.4
            weight = (14 * r[11] + r[12]) * lb
        else:
            stature, seh, weight = float(r[5]), float(r[8]), float(r[10])
        recs.setdefault(key, []).append((_d(r[2]), r[0], stature, weight, seh))
    out = []
    pool = [(row["Staff number"], row["Sex"]) for row in roster]
    if population == "measured":
        sexes = {row["Staff number"]: row["Sex"] for row in roster}
        pool = [(k, sexes.get(k, "?")) for k in recs]
    for staff, sex in pool:
        rs = sorted(recs.get(staff, []))
        if not rs:
            continue
        r = rs[-1] if which == "latest" else (rs[0] if which == "first" else None)
        if which == "mean":
            r = (None, None, sum(x[2] for x in rs) / len(rs), sum(x[3] for x in rs) / len(rs), sum(x[4] for x in rs) / len(rs))
        out.append({"staff": staff, "sex": sex, "stature": r[2], "weight": r[3], "seh": r[4], "n": len(rs)})
    return out


def rung(cab, a, name):
    if name == "R1":
        return a["in_travel"]
    if name == "R2":
        return a["in_travel"] and a["vision"]
    if name == "R2r":
        return a["in_travel"] and a["vision"] and a["recline_ok"]
    if name == "G":
        return Wd.fits(a)
    if name == "R1c":
        return a["in_travel"] and a["clear"]
    raise ValueError(name)


def fit_table(dr, name="G"):
    out = {}
    for cab in P.CABS:
        fails = [d for d in dr if not rung(cab, Wd.assess(cab, d["stature"], d["weight"], d["seh"]), name)]
        out[cab["id"]] = {"fail": len(fails), "women": sum(1 for d in fails if d["sex"] == "F")}
    return out


def r0(dr):
    """the percentile check: the 5th to 95th percentile hip point against each cab's stated travel (shortfall, mm)"""
    out = {}
    for cab in P.CABS:
        xs = sorted(Wd.assess(cab, d["stature"], d["weight"], d["seh"])["xh"] for d in dr)
        p5, p95 = xs[int(0.05 * (len(xs) - 1))], xs[int(0.95 * (len(xs) - 1))]
        t0, t1 = cab["travel"]
        out[cab["id"]] = max(0.0, t0 - p5) + max(0.0, p95 - t1)
    return out


def call(table):
    order = sorted(table, key=lambda k: table[k]["fail"])
    return order[0], order[1], table[order[1]]["fail"] - table[order[0]]["fail"]


# ----------------------------------------------------------------------------------------------- fleet
def vehicles(root, in_service="true"):
    reg = _xlsx(root, "register")
    dis = _xlsx(root, "disposals")
    al = _xlsx(root, "assets")
    true_legacy = {str(r.Vehicle): _d(r[3]) for r in al.itertuples(index=False)}
    out = []
    for r in reg.itertuples(index=False):
        former = "" if (isinstance(r[1], float) and math.isnan(r[1])) else str(r[1])
        held = _d(r[5])
        start = true_legacy.get(former, held) if (former and in_service == "true") else held
        out.append({"key": "R:" + str(r[0]), "fleet": str(r[0]), "former": former, "chassis": r[2], "converter": r[3],
                    "start": start, "end": None})
    for r in dis.itertuples(index=False):
        former = "" if (isinstance(r[1], float) and math.isnan(r[1])) else str(r[1])
        held = _d(r[4])
        start = true_legacy.get(former, held) if (former and in_service == "true") else held
        out.append({"key": "D:%s:%s" % (r[0], _d(r[5])), "fleet": str(r[0]), "former": former, "chassis": r[2],
                    "converter": r[3], "start": start, "end": _d(r[5])})
    return out


def _owner(vs, label, day, how="asof"):
    """the vehicle a record on this fleet number (or former number) on this date belongs to"""
    c = [v for v in vs if v["fleet"] == label or v["former"] == label]
    if not c:
        return None
    if how == "register":
        reg = [v for v in c if v["end"] is None]
        return (reg or c)[0]
    live = [v for v in c if v["end"] is None or day < v["end"]]
    if len(live) > 1:
        live = [v for v in live if v["end"] is not None] or live
    return live[0] if live else c[0]


def job_records(root, vs, join="asof", transferred="first", legacy_map=True):
    merged = _read_csv(root, "jobs")
    legacy = _read_csv(root, "legacy_jobs")
    cmap = _xlsx(root, "codemap")
    to_code = dict(zip(cmap["Vennerley defect code"], cmap["Fleet job code"]))
    recs = []
    open_legacy = []
    for r in legacy:
        day = _d(r["Date in"])
        v = _owner(vs, r["Vehicle"], day, join) if legacy_map else None
        code = to_code.get(r["Defect code"], r["Defect code"])
        rec = {"veh": v, "raised": day, "code": code, "off": r["Off road"] == "Y", "from": day,
               "to": _d(r["Date out"]), "src": "legacy", "status": r["Status"], "label": r["Vehicle"]}
        if r["Status"] == "TRANSFERRED":
            open_legacy.append(rec)
        recs.append(rec)
    for r in merged:
        day = _d(r["raised"])
        v = _owner(vs, r["fleet_no"], day, join)
        recs.append({"veh": v, "raised": day, "code": r["job_code"], "off": r["off_road"] == "Y",
                     "from": _d(r["off_road_from"]), "to": _d(r["back_on_road"]), "src": "merged", "status": "",
                     "label": r["fleet_no"]})
    # a job open in the Vennerley system at its closure continues as the job raised for it on 1 July 2025
    for lg in open_legacy:
        twin = [m for m in recs if m["src"] == "merged" and m["raised"] == P.WORKSHOP_CUTOVER and m["veh"] is lg["veh"]
                and m["code"] == lg["code"] and not m.get("twin")]
        if twin and lg["veh"] is not None:
            m = twin[0]
            m["twin"] = lg
            lg["twin"] = m
            if lg["off"]:
                lg["to"] = P.WORKSHOP_CUTOVER
            if transferred == "first":
                m["count"] = False
            elif transferred == "merged":
                lg["count"] = False
    for r in recs:
        r.setdefault("count", True)
        if r["src"] == "legacy" and r["status"] == "TRANSFERRED" and r["off"] and r["to"] is None:
            r["to"] = P.FY[1] + D(days=1)
    return recs


def _q(day):
    for i, (_, a, b) in enumerate(P.QUARTERS):
        if a <= day <= b:
            return i
    return None


def miles(root, vs, how="window", join="asof"):
    units = _xlsx(root, "units")
    by_unit = {}
    with open(os.path.join(root, PK.FILES["odometer"]), encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            by_unit.setdefault(r["unit_id"], []).append((dt.date.fromisoformat(r["reading_date"]), float(r["odometer_miles"])))
    fy0, fy1 = P.FY
    tot = {}
    for u in units.itertuples(index=False):
        uid, label, fitted, removed, entered = str(u[0]), str(u[1]), _d(u[2]), _d(u[3]), u[4]
        v = _owner(vs, label, fitted if fitted >= fy0 else fy0, join)
        if v is None:
            continue
        rd = sorted(by_unit.get(uid, []))
        if not rd:
            continue
        if how == "unit_span":
            inside = [x for x in rd if fy0 - D(days=1) <= x[0] <= fy1]
            if len(inside) >= 2:
                tot[v["key"]] = tot.get(v["key"], 0.0) + inside[-1][1] - inside[0][1]
            continue
        start = max(fitted, fy0)
        stop = min(removed, fy1 + D(days=1)) if removed else fy1 + D(days=1)
        inside = [x for x in rd if start <= x[0] < stop]
        if not inside:
            continue
        if fitted >= fy0 and how == "window_first":
            base = inside[0][1]
        elif fitted >= fy0:
            base = float(entered)
        else:
            prior = [x for x in rd if x[0] < start]
            base = prior[-1][1]
        tot[v["key"]] = tot.get(v["key"], 0.0) + inside[-1][1] - base
    return tot


def fleet_figures(root, join="asof", transferred="first", legacy_map=True, miles_how="window", in_service="true",
                  vor="union"):
    vs = vehicles(root, in_service)
    recs = job_records(root, vs, join, transferred, legacy_map)
    fy0, fy1 = P.FY
    conv = {}
    for r in recs:
        if not r["count"] or r["veh"] is None or r["code"] not in ("B12", "B30"):
            continue
        q = _q(r["raised"])
        if q is None:
            continue
        conv.setdefault(r["veh"]["converter"], [0, 0, 0, 0])[q] += 1
    mi = miles(root, vs, miles_how, join)
    conv_miles = {}
    for v in vs:
        conv_miles[v["converter"]] = conv_miles.get(v["converter"], 0.0) + mi.get(v["key"], 0.0)
    # days off the road
    days = {}
    spells = {}
    for r in recs:
        if not r["off"] or r["veh"] is None or r["from"] is None:
            continue
        a, b = r["from"], r["to"] or (fy1 + D(days=1))
        spells.setdefault(r["veh"]["key"], []).append((a, b))
    for v in vs:
        ch = days.setdefault(v["chassis"], [0, 0, 0, 0])
        if vor == "union":
            seen = set()
            for a, b in spells.get(v["key"], []):
                d = a
                while d < b:
                    seen.add(d)
                    d += D(days=1)
            for d in seen:
                q = _q(d)
                if q is not None:
                    ch[q] += 1
        else:
            for a, b in spells.get(v["key"], []):
                d = a
                while d < b:
                    q = _q(d)
                    if q is not None:
                        ch[q] += 1
                    d += D(days=1)
    vy = {}
    for v in vs:
        a = max(v["start"], fy0)
        b = min(v["end"] or fy1 + D(days=1), fy1 + D(days=1))
        vy[v["chassis"]] = vy.get(v["chassis"], 0) + max(0, (b - a).days)
    out = {"converters": {}, "chassis": {}}
    for c in ("Pennick Coachbuild", "Ostrel Vehicle Conversions"):
        jobs = conv.get(c, [0, 0, 0, 0])
        out["converters"][c] = {"jobs": jobs, "miles": conv_miles.get(c, 0.0),
                                "rate": sum(jobs) / conv_miles[c] * 100000.0 if conv_miles.get(c) else None}
    for c in ("FD35", "RD43"):
        out["chassis"][c] = {"days": days.get(c, [0, 0, 0, 0]), "vehicle_years": vy.get(c, 0) / 365.0,
                             "rate": sum(days.get(c, [0, 0, 0, 0])) / (vy[c] / 365.0)}
    out["_vehicles"] = vs
    return out


def solve(root, variants=False):
    dr = drivers(root)
    S = {"drivers": len(dr), "fit": fit_table(dr, "G"), "rungs": {n: fit_table(dr, n) for n in ("R1", "R2", "R2r", "R1c")},
         "r0": r0(dr)}
    S["call"] = call(S["fit"])
    S["default_call"] = call(S["rungs"]["R2"])
    S["fleet"] = fleet_figures(root)
    if variants:
        S["variants"] = {
            "first": fit_table(drivers(root, which="first")), "mean": fit_table(drivers(root, which="mean")),
            "measured": fit_table(drivers(root, population="measured")),
            "no_crosswalk": fit_table(drivers(root, crosswalk=False)),
            "lb_rounded": fit_table(drivers(root, lb=0.4536)),
        }
    return S
