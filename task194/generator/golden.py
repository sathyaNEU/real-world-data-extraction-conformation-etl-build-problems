"""Every graded figure, computed from the shipped bundle alone (no generator state)."""
import csv
import datetime as dt
import json
import os

import numpy as np
import openpyxl

BST_END = dt.datetime(2026, 10, 25, 1, 0)
BASE = (dt.date(2026, 9, 7), dt.date(2026, 10, 4))
COMP = (dt.date(2026, 10, 12), dt.date(2026, 11, 1))
HH_NU, NHH_NU, N1 = 1.7, 6.0, 1.15
F = {
    "flows": "historian_inlet_flows_20260801_20261102.csv", "pressure": "aznp_pressure_hourly_2026.csv",
    "register": "dma_register_2026-09.xlsx", "amr": "amr_large_user_reads_hourly.csv",
    "accounts": "large_user_accounts.xlsx", "billing": "billing_account_events_extract.csv",
    "works": "works_orders_aug_oct_2026.xlsx", "assets": "mains_asset_list.csv",
    "valves": "gis_boundary_valves.geojson",
}


def loc(t):
    return t + dt.timedelta(hours=1) if t < BST_END else t


def parse(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


def register(target):
    wb = openpyxl.load_workbook(os.path.join(target, F["register"]), read_only=True)
    ws = wb["Areas"]
    areas = {}
    hdr = None
    for row in ws.iter_rows(values_only=True):
        if row and row[0] == "Area code":
            hdr = row
            continue
        if hdr and row and row[0]:
            areas[row[0]] = dict(name=row[1], tags=[t.strip() for t in str(row[2]).split(";")], hh=int(row[3]),
                                 nhh=int(row[4]), km=float(row[5]), logger=row[6], prev=row[8] or "")
    sp = {r[0]: r[1] for r in wb["Supply points"].iter_rows(min_row=2, values_only=True) if r[0]}
    units = {r[0]: r[1] for r in wb["Instrument units"].iter_rows(min_row=2, values_only=True) if r[0]}
    return areas, sp, units


def flows(target, units):
    """{tag: {utc datetime: m3/h}}"""
    out = {}
    with open(os.path.join(target, F["flows"])) as f:
        r = csv.reader(f)
        next(r)
        for tag, ts, v, q in r:
            x = float(v) * (3.6 if units[tag] == "l/s" else 1.0)
            out.setdefault(tag, {})[parse(ts)] = x
    return out


def night_mean(series, per):
    by = {}
    for t, v in series.items():
        lt = loc(t)
        if lt.hour == 3 and per[0] <= lt.date() <= per[1]:
            by.setdefault(lt.date(), []).append(v)
    nights = [np.mean(v) for v in by.values()]
    return float(np.mean(nights)), len(nights)


def area_flow(fl, tags):
    keys = set(fl[tags[0]])
    for t in tags[1:]:
        keys &= set(fl[t])
    return {k: sum(fl[t][k] for t in tags) for k in keys}


def pressure(target):
    out = {}
    with open(os.path.join(target, F["pressure"])) as f:
        r = csv.reader(f)
        next(r)
        for lg, ts, v, u in r:
            m = float(v) / 0.0980665 if u == "bar" else float(v)
            out.setdefault(lg, {})[parse(ts)] = m
    return out


def amr(target):
    """Per meter serial: sorted [(utc, register)]."""
    out = {}
    with open(os.path.join(target, F["amr"])) as f:
        r = csv.reader(f)
        next(r)
        for s, ts, v in r:
            out.setdefault(s, []).append((parse(ts), float(v)))
    for s in out:
        out[s].sort()
    return out


def advances(reads):
    """Hourly register advances within one meter: a fall is a five-digit register rolling over."""
    adv = []
    for (t0, r0), (t1, r1) in zip(reads, reads[1:]):
        d = r1 - r0
        if d < 0:
            d += 100000.0
        adv.append((t0, t1, d))
    return adv


def accounts(target):
    wb = openpyxl.load_workbook(os.path.join(target, F["accounts"]), read_only=True)
    rows = list(wb.active.iter_rows(min_row=2, values_only=True))
    return [dict(acc=r[0], name=r[1], area=r[2], serial=r[3], sp=r[4]) for r in rows if r[0]]


def revenue_meters(target):
    """The meters that measure each supply point's draw: the register's revenue meter, a meter the same account
    fitted in its place, or the meter of a supply point connected after the register issue. {serial: area}"""
    areas, sp, _ = register(target)
    wb = openpyxl.load_workbook(os.path.join(target, F["register"]), read_only=True)
    rev = {r[0]: r[3] for r in wb["Supply points"].iter_rows(min_row=2, values_only=True) if r[0]}
    old = {a["prev"]: c for c, a in areas.items() if a["prev"]}
    acc = accounts(target)
    owner = {a["serial"]: a["acc"] for a in acc}
    out = {}
    for a in acc:
        if a["sp"] in sp:
            if a["serial"] == rev[a["sp"]] or owner.get(rev[a["sp"]]) == a["acc"]:
                out[a["serial"]] = sp[a["sp"]]
        else:
            out[a["serial"]] = old.get(a["area"], a["area"])
    return out


def lu_night(target, sp=None, meters=None):
    """Logged large users' night-hour consumption per area and period, metered at each supply point."""
    reads = amr(target)
    meters = meters if meters is not None else revenue_meters(target)
    out = {}
    for serial, area in meters.items():
        a = {"serial": serial}
        for per in ("base", "comp"):
            pr = BASE if per == "base" else COMP
            byn = {}
            for t0, t1, d in advances(reads.get(a["serial"], [])):
                l0 = loc(t0)
                if l0.hour == 3 and pr[0] <= l0.date() <= pr[1] and (t1 - t0) == dt.timedelta(hours=1):
                    byn[l0.date()] = d
            out.setdefault(area, {}).setdefault(per, {})
            for k, v in byn.items():
                out[area][per][k] = out[area][per].get(k, 0.0) + v
    res = {}
    for area, d in out.items():
        res[area] = {}
        for per in ("base", "comp"):
            pr = BASE if per == "base" else COMP
            ndays = (pr[1] - pr[0]).days + 1
            res[area][per] = sum(d.get(per, {}).values()) / ndays
    return res


def aznp(press, logger, per):
    vals = [v for t, v in press[logger].items() if loc(t).hour == 3 and per[0] <= loc(t).date() <= per[1]]
    return float(np.mean(vals))


def valves(target):
    gj = json.load(open(os.path.join(target, F["valves"])))
    return [(f["properties"]["asset_id"], f["properties"]["dma_1"], f["properties"]["dma_2"]) for f in gj["features"]]


def profile(series, per):
    """Mean flow by local quarter-hour slot over the days of a set of nights."""
    by = {}
    for t, v in series.items():
        lt = loc(t)
        if per[0] <= lt.date() <= per[1]:
            by.setdefault(lt.hour * 4 + lt.minute // 15, []).append(v)
    return np.array([np.mean(by[s]) for s in range(96)])


def main_call(target):
    areas, sp, units = register(target)
    fl = flows(target, units)
    press = pressure(target)
    lu = lu_night(target, sp)
    R = {}
    series = {}
    for code, a in areas.items():
        s = area_flow(fl, a["tags"])
        series[code] = s
        mb, nb = night_mean(s, BASE)
        mc, nc = night_mean(s, COMP)
        nu = (a["hh"] * HH_NU + a["nhh"] * NHH_NU) / 1000.0
        lb = mb - nu - lu.get(code, {}).get("base", 0.0)
        lc = mc - nu - lu.get(code, {}).get("comp", 0.0)
        pb, pc = aznp(press, a["logger"], BASE), aznp(press, a["logger"], COMP)
        fac = (pb / pc) ** N1
        R[code] = dict(name=a["name"], km=a["km"], hh=a["hh"], mnf_b=mb, mnf_c=mc, nights=(nb, nc),
                       r0=mc - mb, r1=lc - lb, r2=lc * fac - lb, pb=pb, pc=pc, fac=fac, lb=lb, lc=lc)
    # boundary test: each valve pair's whole-day increments against each other
    pairs = []
    for vid, a, b in valves(target):
        da = profile(series[a], COMP) - profile(series[a], BASE)
        db = profile(series[b], COMP) - profile(series[b], BASE)
        c = float(np.corrcoef(da, -db)[0, 1])
        pairs.append(dict(valve=vid, a=a, b=b, corr=c, da_night=float(da[12:16].mean()), db_night=float(db[12:16].mean()),
                          da_day=float(da.mean()), db_day=float(db.mean())))
    # a pair whose whole-day volumes moved by equal and opposite amounts is water crossing the boundary
    open_pairs = [p for p in pairs if abs(p["da_day"]) > 2.0 and 0.85 <= -p["db_day"] / p["da_day"] <= 1.15]
    for code in R:
        R[code]["own"] = R[code]["r2"]
        R[code]["transfer_night"] = 0.0
    for p in open_pairs:
        rise, fall = (p["a"], p["b"]) if p["da_day"] > 0 else (p["b"], p["a"])
        dn_r = p["da_night"] if rise == p["a"] else p["db_night"]
        dn_f = p["db_night"] if rise == p["a"] else p["da_night"]
        T = (dn_r - dn_f) / 2.0
        R[rise]["own"] = R[rise]["r2"] - T * R[rise]["fac"]
        R[fall]["own"] = R[fall]["r2"] + T * R[fall]["fac"]
        R[rise]["transfer_night"], R[fall]["transfer_night"] = T, -T
        p["transfer_night"] = T
    return R, pairs, open_pairs


# ------------------------------------------------------------------ asks
def ask_lu_october(target):
    """Each area's logged large users' metered consumption in October 2026 (local month), by supply point."""
    areas, sp, _ = register(target)
    reads = amr(target)
    out = {c: 0.0 for c in areas}
    lo, hi = dt.datetime(2026, 9, 30, 23, 0), dt.datetime(2026, 11, 1, 0, 0)
    for serial, area in revenue_meters(target).items():
        for t0, t1, d in advances(reads.get(serial, [])):
            if lo <= t0 and t1 <= hi:
                out[area] += d
    return out


def ask_occupied(target):
    """Occupied household properties per area at the end of 31 October 2026, from effective-dated events."""
    areas, _, _ = register(target)
    old = {a["prev"]: c for c, a in areas.items() if a["prev"]}
    events = {}
    with open(os.path.join(target, F["billing"])) as f:
        r = csv.DictReader(f)
        for e in r:
            eff = dt.datetime.strptime(e["effective_date"], "%d/%m/%Y").date()
            if eff > dt.date(2026, 10, 31):
                continue
            events.setdefault(e["property_ref"], []).append((eff, e["posted"], e["account_no"], e["event"], e["property_class"],
                                                             old.get(e["area_code"], e["area_code"])))
    out = {c: 0 for c in areas}
    for pref, ev in events.items():
        ev.sort()
        acc_state, cls, area = {}, None, None
        for eff, posted, acc, kind, pc, ac in ev:
            area = ac
            if kind == "OCC":
                acc_state[acc] = True
                cls = cls or pc
            elif kind == "VAC":
                acc_state[acc] = False
            elif kind == "CONV":
                cls = pc
        if cls is None:
            cls = ev[-1][4]
        if any(acc_state.values()) and cls == "HH":
            out[area] += 1
    return out


def ask_repairs(target):
    """Mains repairs per area whose repair task was completed between 1 August and 31 October 2026."""
    amap = {}
    with open(os.path.join(target, F["assets"])) as f:
        for r in csv.DictReader(f):
            amap[r["asset_id"]] = r["dma"]
    wb = openpyxl.load_workbook(os.path.join(target, F["works"]), read_only=True)
    rows = list(wb.active.iter_rows(min_row=2, values_only=True))
    job_asset = {}
    for job, task, ttype, asset, raised, done, closed in rows:
        a = str(asset)
        if not a.startswith("W26-"):
            job_asset.setdefault(job, a if a.startswith("WM-") else "WM-%06d" % int(a.split("/")[0]))
    jobs = {}
    for job, task, ttype, asset, raised, done, closed in rows:
        if ttype != "REPAIR MAIN" or done is None:
            continue
        if dt.datetime(2026, 8, 1) <= done < dt.datetime(2026, 11, 1):
            a = str(asset)
            aid = job_asset[a] if a.startswith("W26-") else job_asset[job]   # a contractor's job carries the job it took over
            jobs[job] = amap[aid]
    areas, _, _ = register(target)
    out = {c: 0 for c in areas}
    for job, area in jobs.items():
        out[area] += 1
    return out


def compute(target):
    R, pairs, open_pairs = main_call(target)
    order = sorted(R, key=lambda c: -R[c]["own"])
    return dict(R=R, pairs=pairs, open_pairs=open_pairs, order=order,
                lu_oct=ask_lu_october(target), occupied=ask_occupied(target), repairs=ask_repairs(target))
