"""Reads the pack and computes the call, the routes and the ask from the shipped files only."""
import collections
import datetime as dt
import os
import statistics

import numpy as np
import openpyxl
import pandas as pd

import world as W

F = W.FILES


def ndc11(ten):
    """a ten-digit hyphenated NDC to the eleven-digit 5-4-2 form, by its configuration"""
    a, b, c = ten.split("-")
    if len(a) == 4:
        a = "0" + a
    elif len(b) == 3:
        b = "0" + b
    elif len(c) == 1:
        c = "0" + c
    return a + b + c


def claims(target):
    df = pd.read_csv(os.path.join(target, F["claims"]), dtype=str, keep_default_na=False)
    for c in ("quantity_dispensed", "ingredient_cost_paid", "dispensing_fee_paid"):
        df[c] = df[c].astype(float)
    df["fill"] = pd.to_datetime(df.fill_date).dt.date
    df["month"] = df.fill.map(lambda d: dt.date(d.year, d.month, 1))
    return df


def rates(target):
    df = pd.read_csv(os.path.join(target, F["aac"]), dtype=str, keep_default_na=False)
    df["rate"] = df.aac_per_unit.astype(float)
    df["eff"] = pd.to_datetime(df.effective_date).dt.date
    df["end"] = df.end_date.map(lambda x: dt.date.fromisoformat(x) if x else dt.date(2099, 12, 31))
    return df


def drugs(target):
    wb = openpyxl.load_workbook(os.path.join(target, F["drugs"]), read_only=True)
    ws = wb["Drug file"]
    rows = list(ws.iter_rows(values_only=True))
    df = pd.DataFrame(rows[1:], columns=rows[0])
    df["ndc"] = df.NDC.map(ndc11)
    up = df["Package description"].str.upper()
    df["pkg"] = np.where(up.str.contains("UNIT-DOSE") | up.str.contains("BLISTER"), "U", "B")
    return df


def classes(target):
    wb = openpyxl.load_workbook(os.path.join(target, F["classes"]), read_only=True)
    c = list(wb["Classes"].iter_rows(values_only=True))
    hdr = [i for i, r in enumerate(c) if r and r[0] == "Class code"][0]
    names = {r[0]: r[1] for r in c[hdr + 1:] if r and r[0]}
    p = list(wb["Products"].iter_rows(values_only=True))
    return {r[0]: names[r[4]] for r in p[1:] if r and r[0]}


def summary(target):
    wb = openpyxl.load_workbook(os.path.join(target, F["summary"]), read_only=True)
    rows = list(wb["Utilization"].iter_rows(values_only=True))
    return pd.DataFrame(rows[1:], columns=rows[0])


def frame(target):
    """the claims joined to product, package and current class"""
    cl, dr, cls = claims(target), drugs(target), classes(target)
    m = dr.set_index("ndc")
    cl["gpc"] = cl.ndc.map(m.GPC)
    cl["pkg"] = cl.ndc.map(m.pkg)
    cl["cls"] = cl.gpc.map(cls)
    return cl, dr, cls


def months_list():
    out, y, mo = [], 2026, 4
    while (y, mo) <= (2027, 3):
        out.append(dt.date(y, mo, 1))
        y, mo = (y + 1, 1) if mo == 12 else (y, mo + 1)
    return out


def in_effect(rt, dr):
    """{(ndc, month): rate} and {(gpc, pkg, month): [rates of priced NDCs]}"""
    gpc = dr.set_index("ndc").GPC
    pkg = dr.set_index("ndc").pkg
    by_ndc, by_grp = {}, collections.defaultdict(list)
    for r in rt.itertuples():
        for m in months_list():
            if r.eff <= m <= r.end:
                by_ndc[(r.ndc, m)] = r.rate
                by_grp[(gpc[r.ndc], pkg[r.ndc], m)].append(r.rate)
    return by_ndc, by_grp


def premium(by_grp, cls_of_gpc, pooled=False):
    rs = collections.defaultdict(list)
    for (g, k, m), xs in by_grp.items():
        if k == "U" and (g, "B", m) in by_grp:
            rs[cls_of_gpc.get(g)].append(statistics.median(xs) / statistics.median(by_grp[(g, "B", m)]))
    allr = [x for v in rs.values() for x in v]
    if pooled:
        return collections.defaultdict(lambda: statistics.median(allr))
    out = collections.defaultdict(lambda: statistics.median(allr))
    for k, v in rs.items():
        out[k] = statistics.median(v)
    return out


ROUTES = ("golden", "golden_mean", "golden_class", "golden_pooled", "default", "default_mean", "lowest", "highest",
          "complete_case")
GOLDEN = ("golden", "golden_mean", "golden_class", "golden_pooled")
DEFAULT = ("default", "default_mean", "lowest")


def unit_cost(route, g, k, m, by_grp, prem, cls):
    same = by_grp.get((g, k, m))
    b = by_grp.get((g, "B", m))
    allx = (by_grp.get((g, "B", m)) or []) + (by_grp.get((g, "U", m)) or [])
    if route == "golden":
        if same:
            return statistics.median(same)
        return statistics.median(b) * prem[cls] if (b and k == "U") else None
    if route == "golden_mean":
        if same:
            return float(np.mean(same))
        return float(np.mean(b)) * prem[cls] if (b and k == "U") else None
    if route in ("golden_class", "golden_pooled"):
        if k == "U" and b:
            return statistics.median(b) * prem[cls]
        return statistics.median(same) if same else None
    if not allx:
        return None
    if route == "default":
        return statistics.median(allx)
    if route == "default_mean":
        return float(np.mean(allx))
    if route == "lowest":
        return min(allx)
    if route == "highest":
        return max(allx)
    raise ValueError(route)


def spreads(target, route="golden", cl=None, dr=None, cls=None, latest=False):
    """each class's ingredient spread: the claims' ingredient cost less the units' acquisition cost, the State AAC
    rate in effect for the NDC on the fill date where there is one, the route's estimate where there is none"""
    if cl is None:
        cl, dr, cls = frame(target)
    rt = rates(target)
    by_ndc, by_grp = in_effect(rt, dr)
    if latest:
        last = months_list()[-1]
        lat = {}
        for r in rt.sort_values("eff").itertuples():
            lat[r.ndc] = r.rate
        by_ndc = {(n, m): lat[n] for (n, m) in by_ndc}
    prem = premium(by_grp, cls, pooled=(route == "golden_pooled"))
    out = collections.Counter()
    missing = 0
    cache = {}
    for r in cl.itertuples():
        rate = by_ndc.get((r.ndc, r.month))
        if rate is None:
            if route == "complete_case":
                continue
            key = (r.gpc, r.pkg, r.month)
            if key not in cache:
                cache[key] = unit_cost(route, r.gpc, r.pkg, r.month, by_grp, prem, r.cls)
            rate = cache[key]
            if rate is None:
                missing += 1
                continue
        out[r.cls] += r.ingredient_cost_paid - rate * r.quantity_dispensed
    return {c: out[c] for c in W.SHORTLIST_NAMES}, missing


def ranking(sp):
    return sorted(W.SHORTLIST_NAMES, key=lambda c: -sp[c])


def ask(target, by_label=False):
    """each shortlisted class's FY2026 claims, units and ingredient cost paid, classes as the current list defines
    them (or, by_label, as the summary's stored label reads)"""
    sm, dr, cls = summary(target), drugs(target), classes(target)
    if by_label:
        sm["cls"] = sm["Drug class"]
    else:
        gpc = dr.set_index("ndc").GPC
        sm["cls"] = sm.NDC.map(gpc).map(cls)
    g = sm.groupby("cls")[["Claims", "Units", "Ingredient cost paid"]].sum()
    return {c: (int(g.loc[c, "Claims"]), float(g.loc[c, "Units"]), float(g.loc[c, "Ingredient cost paid"]))
            for c in W.SHORTLIST_NAMES}
