"""Every figure the task grades, and every rung, computed from the shipped files alone."""
import datetime as dt
import math
import os

import numpy as np
import openpyxl
import pandas as pd

import world as W

F = dict(register="protection_asset_register_2026-09-30.csv", wo="eam_work_orders_protection_2021-01_2026-09.csv",
         subs="substations.csv", prog="protection_renewal_programme_2026.xlsx", stock="spares_stock_2026-09-30.csv")


def month_add(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return dt.date(y, m, 1)


def months(a, b):
    out, d = [], dt.date(a.year, a.month, 1)
    while d < b:
        out.append(d)
        d = month_add(d, 1)
    return out


def age_on(inst, first):
    return first.year - inst.year - ((first.month, 1) < (inst.month, inst.day))


def _d(x):
    if x is None or (isinstance(x, float) and math.isnan(x)) or x == "":
        return None
    return dt.date.fromisoformat(str(x)[:10])


def load(target):
    reg = pd.read_csv(os.path.join(target, F["register"]), dtype=str, keep_default_na=False)
    reg["install"] = reg["install_date"].map(_d)
    reg["retired"] = reg["retired_date"].map(_d)
    wo = pd.read_csv(os.path.join(target, F["wo"]), dtype=str, keep_default_na=False)
    wo["rep"] = wo["reported_date"].map(_d)
    subs = pd.read_csv(os.path.join(target, F["subs"]), dtype=str, keep_default_na=False)
    stock = pd.read_csv(os.path.join(target, F["stock"]))
    wb = openpyxl.load_workbook(os.path.join(target, F["prog"]), data_only=True)
    plan = {}
    for sheet in ("Approved 2026", "2025 plan (superseded)"):
        ws = wb[sheet]
        m = {}
        for row in ws.iter_rows(min_row=4, values_only=True):
            if not row or not row[1]:
                continue
            v = row[5]
            m[row[1]] = None if v == "Not in programme period" else dt.datetime.strptime(v, "%b %Y").date()
        plan[sheet] = m
    return reg, wo, subs, stock, plan


def fleet(reg):
    return reg[reg["model"] == "VPR-340"].copy()


def failures(wo, fl):
    ids = set(fl["asset_id"])
    f = wo[wo["asset_id"].isin(ids) & wo["work_type"].isin(["CM", "EM"]) & (wo["failed_component"] == "PSU")
           & wo["status"].isin(["COMP", "CLOSE"])].copy()
    inst = dict(zip(fl["asset_id"], fl["install"]))
    f["month"] = [dt.date(d.year, d.month, 1) for d in f["rep"]]
    f["age"] = [age_on(inst[a], m) for a, m in zip(f["asset_id"], f["month"])]
    f["band"] = [W.band_of(a) for a in f["age"]]
    return f


def exposure(fl, start):
    """relay-months by band, counting a relay for every month it is in service on the first day, from
    `start` (None: from installation) to the extract date"""
    e = np.zeros(len(W.BANDS))
    end_all = dt.date(2026, 10, 1)
    for inst, ret in zip(fl["install"], fl["retired"]):
        first = month_add(dt.date(inst.year, inst.month, 1), 1) if inst.day > 1 else dt.date(inst.year, inst.month, 1)
        if start is not None and first < start:
            first = start
        for m in months(first, ret or end_all):
            e[W.band_of(age_on(inst, m))] += 1
    return e


def support_end(sub, plan):
    if sub not in plan:
        return None                     # substation not in the programme list: relays already gone
    p = plan[sub]
    return p if p is not None else month_add(W.PROGRAMME_END, 1)


def forward(fl, plan, subs, start=W.HORIZON_START, until_programme_end=False):
    """relay-months by band over the support period; also by year and by current region"""
    region = dict(zip(subs["sub_code"], subs["region"]))
    nb = len(W.BANDS)
    tot = np.zeros(nb)
    by_year, by_region = {}, {}
    live = fl[fl["status"] == "IN SERVICE"]
    for inst, sub in zip(live["install"], live["sub_code"]):
        end = month_add(W.PROGRAMME_END, 1) if until_programme_end else support_end(sub, plan)
        if end is None:
            continue
        for m in months(start, end):
            b = W.band_of(age_on(inst, m))
            tot[b] += 1
            by_year.setdefault(m.year, np.zeros(nb))[b] += 1
            by_region.setdefault(region[sub], np.zeros(nb))[b] += 1
    return tot, by_year, by_region


def in_service_jan1(fl, plan):
    live = fl[fl["status"] == "IN SERVICE"]
    out = {}
    for y in range(2027, 2036):
        d = dt.date(y, 1, 1)
        out[y] = int(sum(1 for s in live["sub_code"] if (support_end(s, plan) or dt.date(1900, 1, 1)) > d))
    return out


def available(stock):
    s = stock[stock["item_code"] == "VPR340-PSU-02"]
    return int(s[s["stock_state"].isin(["SERVICEABLE", "AT REPAIR"])]["quantity"].sum())


def poisson_cdf(k, lam):
    """P(X <= k) for X ~ Poisson(lam), summed in log space so a large mean cannot underflow"""
    if k < 0:
        return 0.0
    logs = [i * math.log(lam) - lam - math.lgamma(i + 1) for i in range(k + 1)]
    top = max(logs)
    return math.exp(top) * sum(math.exp(x - top) for x in logs)


def lots_needed(lam, avail):
    n = 0
    while poisson_cdf(avail + n * W.LOT, lam) < W.COVER:
        n += 1
    return n


def rates(f, expo):
    cnt = np.bincount(f["band"], minlength=len(W.BANDS)).astype(float)
    return cnt / expo * 12.0, cnt


def solve(target):
    reg, wo, subs, stock, plan = load(target)
    fl = fleet(reg)
    f = failures(wo, fl)
    p26 = plan["Approved 2026"]
    expW = exposure(fl, W.MIGRATION)
    rW, cnt = rates(f, expW)
    tot, by_year, by_region = forward(fl, p26, subs)
    lam = float((rW * tot).sum() / 12.0)
    avail = available(stock)
    lots = lots_needed(lam, avail)
    psu = stock[stock["item_code"] == "VPR340-PSU-02"]
    st_n = {k: int(psu[psu["stock_state"] == k]["quantity"].sum()) for k in ("SERVICEABLE", "AT REPAIR", "QUARANTINE")}
    out = dict(serviceable=st_n["SERVICEABLE"], at_repair=st_n["AT REPAIR"], quarantine=st_n["QUARANTINE"],rates=rW, counts=cnt, exposure=expW, fwd=tot, lam=lam, avail=avail, lots=lots,
               modules=lots * W.LOT, cost=lots * W.LOT * W.UNIT_PRICE,
               cover=poisson_cdf(avail + lots * W.LOT, lam),
               by_year={y: float((rW * v).sum() / 12.0) for y, v in sorted(by_year.items())},
               by_region={r: float((rW * v).sum() / 12.0) for r, v in sorted(by_region.items())},
               in_service=in_service_jan1(fl, p26), n_fail=len(f),
               settings={n: dict(cover=poisson_cdf(avail + n * W.LOT, lam), cost=n * W.LOT * W.UNIT_PRICE)
                         for n in W.SETTINGS})
    return out


def rungs(target):
    """the ladder's wrong constructions, each as (expected failures, lots)"""
    reg, wo, subs, stock, plan = load(target)
    fl = fleet(reg)
    f = failures(wo, fl)
    p26, p25 = plan["Approved 2026"], plan["2025 plan (superseded)"]
    avail = available(stock)
    tot, _, _ = forward(fl, p26, subs)
    fwd_years = tot.sum() / 12.0
    expW, expI = exposure(fl, W.MIGRATION), exposure(fl, None)
    rW, cnt = rates(f, expW)
    rI, _ = rates(f, expI)
    out = {}
    live = (fl["status"] == "IN SERVICE").sum()
    last12 = int((f["month"] >= dt.date(2025, 10, 1)).sum())
    out["trailing_rate"] = last12 / live * fwd_years
    out["trailing_count_x_horizon"] = last12 * (len(months(W.HORIZON_START, month_add(W.PROGRAMME_END, 1))) / 12.0)
    out["pooled_window"] = cnt.sum() / expW.sum() * 12.0 * fwd_years
    out["pooled_install"] = cnt.sum() / expI.sum() * 12.0 * fwd_years
    out["banded_install"] = float((rI * tot).sum() / 12.0)
    tot25, _, _ = forward(fl, p25, subs)
    out["banded_window_2025_plan"] = float((rW * tot25).sum() / 12.0)
    totE, _, _ = forward(fl, p26, subs, until_programme_end=True)
    out["banded_window_no_programme"] = float((rW * totE).sum() / 12.0)
    # counting cancelled and logistics PSU work orders as failures
    ids = set(fl["asset_id"])
    g = wo[wo["asset_id"].isin(ids) & (wo["failed_component"] == "PSU")].copy()
    inst = dict(zip(fl["asset_id"], fl["install"]))
    g["band"] = [W.band_of(age_on(inst[a], dt.date(d.year, d.month, 1))) for a, d in zip(g["asset_id"], g["rep"])]
    rAll, _ = rates(g, expW)
    out["banded_window_all_psu_wos"] = float((rAll * tot).sum() / 12.0)
    rAllI, _ = rates(g, expI)
    out["banded_install_all_psu_wos"] = float((rAllI * tot).sum() / 12.0)
    out["ANSWER"] = float((rW * tot).sum() / 12.0)
    return {k: (v, lots_needed(v, avail)) for k, v in out.items()}, avail
