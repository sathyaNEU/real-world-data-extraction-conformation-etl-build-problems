"""Every figure the task grades, and every rung, computed from the shipped files alone."""
import datetime as dt
import math
import os
import re

import numpy as np
import openpyxl
import pandas as pd

import world as W

F = dict(register="protection_asset_register_2026-09-30.csv", wo="eam_work_orders_protection_2021-01_2026-09.csv",
         hist="psu_rotating_item_history_2021-01_2026-09.csv", subs="substations.csv",
         prog="protection_renewal_programme_2026.xlsx", stock="spares_stock_2026-09-30.csv")
SHEETS = ("Approved 2026", "2025 plan (superseded)")
END_HIST = dt.date(2026, 10, 1)


def month_add(d, n):
    y, m = d.year + (d.month - 1 + n) // 12, (d.month - 1 + n) % 12 + 1
    return dt.date(y, m, 1)


def months(a, b):
    out, d = [], dt.date(a.year, a.month, 1)
    while d < b:
        out.append(d)
        d = month_add(d, 1)
    return out


def age_on(fitted, first):
    return first.year - fitted.year - ((first.month, 1) < (fitted.month, fitted.day))


def first_month(d):
    m = dt.date(d.year, d.month, 1)
    return m if d.day == 1 else month_add(m, 1)


def _d(x):
    if x is None or (isinstance(x, float) and math.isnan(x)) or x == "":
        return None
    return dt.date.fromisoformat(str(x)[:10])


def _bays(txt):
    m = re.fullmatch(r"F(\d+)-F(\d+)", str(txt).strip())
    return (int(m.group(1)), int(m.group(2))) if m else None


def load(target):
    reg = pd.read_csv(os.path.join(target, F["register"]), dtype=str, keep_default_na=False)
    reg["install"] = reg["install_date"].map(_d)
    reg["retired"] = reg["retired_date"].map(_d)
    wo = pd.read_csv(os.path.join(target, F["wo"]), dtype=str, keep_default_na=False)
    wo["rep"] = wo["reported_date"].map(_d)
    hist = pd.read_csv(os.path.join(target, F["hist"]), dtype=str, keep_default_na=False)
    hist["fitted"] = hist["fitted_date"].map(_d)
    hist["removed"] = hist["removed_date"].map(_d)
    subs = pd.read_csv(os.path.join(target, F["subs"]), dtype=str, keep_default_na=False)
    stock = pd.read_csv(os.path.join(target, F["stock"]), dtype={"item_no": str})
    wb = openpyxl.load_workbook(os.path.join(target, F["prog"]), data_only=True)
    plan = {}
    for sheet in SHEETS:
        rows = {}
        for row in wb[sheet].iter_rows(min_row=4, values_only=True):
            if not row or not row[2]:
                continue
            rng = _bays(row[5])
            if rng is None:
                continue
            v = row[7]
            if isinstance(v, dt.datetime):
                when = dt.date(v.year, v.month, 1)
            elif isinstance(v, dt.date):
                when = dt.date(v.year, v.month, 1)
            elif str(v).strip() == "Not in programme period":
                when = None
            else:
                when = dt.datetime.strptime(str(v).strip(), "%b %Y").date()
            rows.setdefault(row[2], []).append((rng, when))
        plan[sheet] = rows
    return reg, wo, hist, subs, stock, plan


def fleet(reg):
    return reg[reg["model"] == "VPR-340"].copy()


def failures(wo, fl, hist):
    """AM-PC-014 4.1 failures, each with the module it took out (the rotating item removed under the work order)"""
    ids = set(fl["asset_id"])
    f = wo[wo["asset_id"].isin(ids) & wo["work_type"].isin(["CM", "EM"]) & (wo["failed_component"] == "PSU")
           & wo["status"].isin(["COMP", "CLOSE"])].copy()
    fit = dict(zip(hist["removal_wo"], hist["fitted"]))
    f["fitted"] = [fit[w] for w in f["wo_number"]]
    f["month"] = [dt.date(d.year, d.month, 1) for d in f["rep"]]
    f["age"] = [age_on(a, m) for a, m in zip(f["fitted"], f["month"])]
    f["band"] = [W.band_of(a) for a in f["age"]]
    return f


def spell_months(fitted, removed, start=None, stop=END_HIST):
    """months a module counts (in service on the first day), from `start` (None: from fitting)"""
    a = first_month(fitted)
    if start is not None and a < start:
        a = start
    b = stop if removed is None else min(stop, first_month(removed))
    return months(a, b)


def exposure(hist, start):
    """module-months by band over the rotating-item history, from `start` (None: from each module's fitting)"""
    e = np.zeros(len(W.BANDS))
    for fitted, removed in zip(hist["fitted"], hist["removed"]):
        for m in spell_months(fitted, removed, start):
            e[W.band_of(age_on(fitted, m))] += 1
    return e


def rates(f, expo):
    cnt = np.bincount(f["band"], minlength=len(W.BANDS)).astype(float)
    return cnt / expo * 12.0, cnt


def support_end(sub, bay, plan):
    """first month the relay in this bay is no longer supported; None when its station is not in the programme"""
    if sub not in plan:
        return None
    b = int(bay[1:])
    for (lo, hi), when in plan[sub]:
        if lo <= b <= hi:
            return when if when is not None else month_add(W.PROGRAMME_END, 1)
    return None


def current_modules(fl, hist):
    live = fl[fl["status"] == "IN SERVICE"]
    cur = hist[hist["removed"].isna()]
    fit = dict(zip(cur["asset_id"], cur["fitted"]))
    return [(a, s, b, fit[a]) for a, s, b in zip(live["asset_id"], live["sub_code"], live["bay"])]


def forward(fl, hist, plan, subs, r, renew=True, hold=False, end_fn=None, age_from=None):
    """expected failures from the count to each relay's support end: the module in service each month is today's
    module while it survives, and a new module (0-9 band) from the month after a failure"""
    region = dict(zip(subs["sub_code"], subs["region"]))
    q0 = r[0] / 12.0
    tot, by_year, by_region = 0.0, {}, {}
    for aid, sub, bay, fitted in current_modules(fl, hist):
        end = end_fn(sub, bay) if end_fn else support_end(sub, bay, plan)
        if end is None:
            continue
        base = age_from[aid] if age_from else fitted
        surv = 1.0
        for m in months(W.HORIZON_START, end):
            a = age_on(base, W.HORIZON_START if hold else m)
            q = r[W.band_of(a)] / 12.0
            e = surv * q + (1.0 - surv) * q0 if renew else q
            surv *= (1.0 - q)
            tot += e
            by_year[m.year] = by_year.get(m.year, 0.0) + e
            by_region[region[sub]] = by_region.get(region[sub], 0.0) + e
    return tot, by_year, by_region


def occupancy(fl, hist, plan, r):
    """expected module-months in each band to the end of support: today's module while it survives, a new module
    (0-9 band) after a failure"""
    occ = np.zeros(len(W.BANDS))
    q0 = r[0] / 12.0
    for aid, sub, bay, fitted in current_modules(fl, hist):
        end = support_end(sub, bay, plan)
        if end is None:
            continue
        surv = 1.0
        for m in months(W.HORIZON_START, end):
            b = W.band_of(age_on(fitted, m))
            occ[b] += surv
            occ[0] += 1.0 - surv
            surv *= 1.0 - r[b] / 12.0
    return occ


def in_service_jan1(fl, plan):
    live = fl[fl["status"] == "IN SERVICE"]
    out = {}
    for y in range(2027, 2036):
        d = dt.date(y, 1, 1)
        out[y] = int(sum(1 for s, b in zip(live["sub_code"], live["bay"]) if (support_end(s, b, plan) or dt.date(1900, 1, 1)) > d))
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


def solve(target):
    reg, wo, hist, subs, stock, plan = load(target)
    fl = fleet(reg)
    f = failures(wo, fl, hist)
    p26 = plan["Approved 2026"]
    expW = exposure(hist, W.MIGRATION)
    rW, cnt = rates(f, expW)
    lam, by_year, by_region = forward(fl, hist, p26, subs, rW)
    avail = available(stock)
    lots = lots_needed(lam, avail)
    psu = stock[stock["item_code"] == "VPR340-PSU-02"]
    st_n = {k: int(psu[psu["stock_state"] == k]["quantity"].sum()) for k in ("SERVICEABLE", "AT REPAIR", "QUARANTINE")}
    naive, _, _ = forward(fl, hist, p26, subs, rW, renew=False)
    occ = occupancy(fl, hist, p26, rW)
    return dict(serviceable=st_n["SERVICEABLE"], at_repair=st_n["AT REPAIR"], quarantine=st_n["QUARANTINE"],
                rates=rW, counts=cnt, exposure=expW, lam=lam, avail=avail, lots=lots,
                modules=lots * W.LOT, cost=lots * W.LOT * W.UNIT_PRICE, cover=poisson_cdf(avail + lots * W.LOT, lam),
                by_year=dict(sorted(by_year.items())), by_region=dict(sorted(by_region.items())),
                in_service=in_service_jan1(fl, p26), n_fail=len(f), naive=naive, occupancy=occ,
                n_live=len(current_modules(fl, hist)),
                settings={n: dict(cover=poisson_cdf(avail + n * W.LOT, lam), cost=n * W.LOT * W.UNIT_PRICE)
                          for n in W.SETTINGS})


def rungs(target):
    """the ladder's wrong constructions, each as (expected failures, lots)"""
    reg, wo, hist, subs, stock, plan = load(target)
    fl = fleet(reg)
    f = failures(wo, fl, hist)
    p26, p25 = plan[SHEETS[0]], plan[SHEETS[1]]
    avail = available(stock)
    expW, expI = exposure(hist, W.MIGRATION), exposure(hist, None)
    rW, cnt = rates(f, expW)
    rI, _ = rates(f, expI)
    out = {}
    out["ANSWER"] = forward(fl, hist, p26, subs, rW)[0]
    out["window_no_renewal"] = forward(fl, hist, p26, subs, rW, renew=False)[0]
    out["install_renewal"] = forward(fl, hist, p26, subs, rI)[0]
    out["install_no_renewal"] = forward(fl, hist, p26, subs, rI, renew=False)[0]
    out["window_hold_band_no_renewal"] = forward(fl, hist, p26, subs, rW, renew=False, hold=True)[0]
    out["window_hold_band_renewal"] = forward(fl, hist, p26, subs, rW, hold=True)[0]
    # relay age in place of module age (the register's installation date), window exposure, no renewal
    inst = dict(zip(fl["asset_id"], fl["install"]))
    rl = fl.copy()
    rl_hist = pd.DataFrame(dict(asset_id=rl["asset_id"], fitted=rl["install"], removed=rl["retired"]))
    fr = f.copy()
    fr["band"] = [W.band_of(age_on(inst[a], m)) for a, m in zip(fr["asset_id"], fr["month"])]
    rR, _ = rates(fr, exposure(rl_hist, W.MIGRATION))
    out["relay_age_window_no_renewal"] = forward(fl, hist, p26, subs, rR, renew=False, age_from=inst)[0]
    # module-age rates but each relay aged from its installation date
    out["module_rates_relay_ageing_no_renewal"] = forward(fl, hist, p26, subs, rW, renew=False, age_from=inst)[0]
    # staged schemes read as one month for the whole station
    def stage_one(s, b):
        if s not in p26:
            return None
        ws = [w for _, w in p26[s]]
        return min((w or month_add(W.PROGRAMME_END, 1)) for w in ws)
    def stage_last(s, b):
        if s not in p26:
            return None
        ws = [w for _, w in p26[s]]
        return max((w or month_add(W.PROGRAMME_END, 1)) for w in ws)
    out["station_first_stage"] = forward(fl, hist, p26, subs, rW, end_fn=stage_one)[0]
    out["station_last_stage"] = forward(fl, hist, p26, subs, rW, end_fn=stage_last)[0]
    out["plan_2025"] = forward(fl, hist, p25, subs, rW)[0]
    out["no_programme"] = forward(fl, hist, p26, subs, rW, end_fn=lambda s, b: month_add(W.PROGRAMME_END, 1) if s in p26 else None)[0]
    # every PSU work order on a VPR-340 counted (cancelled and logistics included)
    ids = set(fl["asset_id"])
    g = wo[wo["asset_id"].isin(ids) & (wo["failed_component"] == "PSU")].copy()
    rows = []
    for a, d in zip(g["asset_id"], g["rep"]):
        m = dt.date(d.year, d.month, 1)
        h = hist[(hist["asset_id"] == a) & (hist["fitted"].map(first_month) <= m)]
        rows.append(W.band_of(age_on(h["fitted"].max(), m)))
    g["band"] = rows
    rAll, _ = rates(g, expW)
    out["all_psu_wos"] = forward(fl, hist, p26, subs, rAll)[0]
    # trailing twelve months per in-service relay over the forward relay-years
    live_n = len(current_modules(fl, hist))
    last12 = int((f["month"] >= dt.date(2025, 10, 1)).sum())
    fwd_years = sum(len(months(W.HORIZON_START, support_end(s, b, p26))) for _, s, b, _ in current_modules(fl, hist)
                    if support_end(s, b, p26)) / 12.0
    out["trailing_rate"] = last12 / live_n * fwd_years
    out["pooled_window"] = cnt.sum() / expW.sum() * 12.0 * fwd_years
    return {k: (v, lots_needed(v, avail)) for k, v in out.items()}, avail
