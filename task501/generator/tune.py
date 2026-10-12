"""Tuning harness on the simulated world (in memory): the main call's ladder and golden family, before any file is
written. The shipped figures are always recomputed from target/ by solve.py; this file only steers the world."""
import math
import sys
from datetime import date

import numpy as np

import world as W
import sim

PLAN_I = W.month_index(2026, 12)
WIN = list(range(PLAN_I + 1, PLAN_I + 13))


def monthly(funds, fx):
    """Per fund: calls by value-date month (CHF at the plan-date rate), first call month, IP end month, commitment (CHF)."""
    out = []
    for f in funds:
        r = fx.rate(W.PLAN_DATE, f.ccy)
        m = {}
        first = None
        for n in f.notices:
            if n["type"] != "CAPITAL_CALL" or n["status"] != "ISSUED":
                continue
            vi = W.month_index(n["value_date"].year, n["value_date"].month)
            m[vi] = m.get(vi, 0.0) + sum(l[3] for l in n["lines"]) * r
            first = vi if first is None else min(first, vi)
        fc = W.month_index(f.first_close.year, f.first_close.month)
        out.append(dict(code=f.code, s=f.strategy, C=f.commitment * r, calls=m, first=first, fc=fc,
                        ip=W.month_index(f.ip_end.year, f.ip_end.month), ip_date=f.ip_end, f=f))
    return out


def called_to(d, upto):
    return sum(v for k, v in d["calls"].items() if k <= upto)


def bkey(d, i, key, band, age_from):
    a0 = d["first"] if age_from == "first_call" else d["fc"]
    if key == "age":
        return (i - a0) // band
    if key == "toip":
        return (d["ip"] - i) // band if i <= d["ip"] else -1 - (i - d["ip"]) // band
    if key == "ipstatus":
        return ((i - a0) // band, i > d["ip"])


def rates(fs, plan_i=PLAN_I, est0=0, band=12, key="age", by_strat=False, age_from="first_call", weight="sum"):
    num, den, per = {}, {}, {}
    for d in fs:
        if d["first"] is None or d["first"] > plan_i:
            continue
        cum = 0.0
        for i in range(d["first"], plan_i + 1):
            unf = d["C"] - cum
            c = d["calls"].get(i, 0.0)
            if i >= est0 and unf > 1.0:
                b = bkey(d, i, key, band, age_from)
                if by_strat:
                    b = (d["s"], b)
                num[b] = num.get(b, 0.0) + c
                den[b] = den.get(b, 0.0) + unf
                per.setdefault(b, []).append(c / unf)
            cum += c
    if weight == "mean":
        return {b: float(np.mean(v)) for b, v in per.items()}
    return {b: num[b] / den[b] for b in num if den[b] > 0}


def _n(k, by_strat):
    x = k[1] if by_strat else k
    return x[0] if isinstance(x, tuple) else x


def lookup(R, b, by_strat, s):
    k = (s, b) if by_strat else b
    if k in R:
        return R[k]
    cands = [kk for kk in R if (kk[0] == s if by_strat else True)]
    if isinstance(b, tuple):
        cands = [kk for kk in cands if (kk[1] if by_strat else kk)[1] == b[1]] or cands
    bb = b[0] if isinstance(b, tuple) else b
    lower = [kk for kk in cands if _n(kk, by_strat) <= bb]
    if lower:
        return R[max(lower, key=lambda kk: _n(kk, by_strat))]
    return R[min(cands, key=lambda kk: _n(kk, by_strat))] if cands else 0.0


def ta(d, R, months, unf0, band=12, key="age", by_strat=False, age_from="first_call"):
    unf, s = unf0, 0.0
    for i in months:
        r = lookup(R, bkey(d, i, key, band, age_from), by_strat, d["s"])
        c = min(unf, r * unf)
        unf -= c
        s += c
    return s


def closed_shares(fs, plan_i=PLAN_I, by="value"):
    out = {}
    for d in fs:
        if d["ip"] <= plan_i and d["ip_date"] <= W.PLAN_DATE:
            f = d["f"]
            r = d["C"] / f.commitment
            tot = sum(sum(l[3] for l in n["lines"]) for n in f.notices if n["type"] == "CAPITAL_CALL" and n["status"] == "ISSUED"
                      and (n["value_date"] if by == "value" else n["notice_date"]) <= f.ip_end) * r
            out[d["code"]] = tot / d["C"]
    return out


def forecast(fs, method="golden", plan_i=PLAN_I, tau=None, band=12, by_strat=False, age_from="first_call", est0=0, key="age",
             weight="sum"):
    R = rates(fs, plan_i, est0, band, key, by_strat, age_from, weight)
    sh = closed_shares(fs, plan_i)
    tau_v = float(np.mean(list(sh.values()))) if tau is None else tau
    smean = {}
    for st in ("BO", "GR", "PC", "IN"):
        v = [x for d in fs for c, x in sh.items() if c == d["code"] and d["s"] == st]
        smean[st] = float(np.mean(v)) if v else tau_v
    win = list(range(plan_i + 1, plan_i + 13))
    tot = grp = 0.0
    for d in fs:
        if d["first"] is None or d["first"] > plan_i:
            continue
        called = called_to(d, plan_i)
        unf = d["C"] - called
        in_win = win[0] <= d["ip"] <= win[-1]
        if method == "golden" and in_win:
            t = smean[d["s"]] if tau == "strategy" else (tau_v if not callable(tau) else tau(d))
            need = max(0.0, t * d["C"] - called)
            post_months = [i for i in win if i > d["ip"]]
            post = ta(d, R, post_months, max(0.0, unf - need), band, key, by_strat, age_from) if post_months else 0.0
            s = need + post
            grp += s
        else:
            s = ta(d, R, win, unf, band, key, by_strat, age_from)
            if in_win:
                grp += s
        tot += s
    return tot, grp


def req(E):
    return (1 + W.MARGIN) * E - W.RESERVE


def amount(E):
    r = req(E)
    for a in W.MENU:
        if a * 1e6 >= r:
            return a
    return None


def report(funds, fx_rows):
    fx = sim.FX(fx_rows)
    fs = monthly(funds, fx)
    sh = closed_shares(fs)
    v = np.array(list(sh.values()))
    t12 = sum(d["calls"].get(i, 0.0) for d in fs for i in range(PLAN_I - 11, PLAN_I + 1))
    cells = {"R0 2026 run rate": (t12, None)}
    for nm, kw in [("R1 age12 pooled", {}), ("R1 age6", dict(band=6)), ("R1 strat", dict(by_strat=True)), ("R1 fc", dict(age_from="first_close")),
                   ("R1b ipstatus", dict(key="ipstatus")), ("R2 toip12", dict(key="toip")), ("R2 toip6", dict(key="toip", band=6)),
                   ("R2 toip3", dict(key="toip", band=3)), ("R2 toip6 strat", dict(key="toip", band=6, by_strat=True)),
                   ("R1 mean", dict(weight="mean")), ("R1 win2019", dict(est0=W.month_index(2019, 1))), ("R1 win2021", dict(est0=W.month_index(2021, 1)))]:
        cells[nm] = forecast(fs, "ta", **kw)
    for nm, kw in [("G", {}), ("G age6", dict(band=6)), ("G strat", dict(by_strat=True)), ("G fc", dict(age_from="first_close")),
                   ("G median", dict(tau=float(np.median(v)))), ("G tau-strat", dict(tau="strategy")), ("G win2019", dict(est0=W.month_index(2019, 1))),
                   ("G win2021", dict(est0=W.month_index(2021, 1))), ("G strat6", dict(by_strat=True, band=6)), ("G mean-rate", dict(weight="mean")),
                   ("X tau=1", dict(tau=1.0)), ("X tau=min", dict(tau=float(v.min()))), ("X tau=max", dict(tau=float(v.max())))]:
        cells[nm] = forecast(fs, "golden", **kw)
    truth = sim.world_calls_2027(funds, fx)
    g = req(cells["G"][0])
    ga = amount(cells["G"][0])
    print("closed funds %d, drawn share at the IP end: mean %.4f median %.4f sd %.4f range %.3f-%.3f" % (len(v), v.mean(), np.median(v), v.std(), v.min(), v.max()))
    print("golden requirement %.1f -> %d (edges %.1f / %.1f); world's own 2027 calls %.1f" % (g / 1e6, ga, g / 1e6 - (ga - 25), ga - g / 1e6, truth / 1e6))
    for k, (E, grp) in cells.items():
        a = amount(E)
        print("  %-18s E %6.1f  group %6s  req %6.1f -> %4d %s" % (k, E / 1e6, "%.1f" % (grp / 1e6) if grp is not None else "-", req(E) / 1e6, a, "<== golden" if a == ga else ""))
    for yr in (2024, 2025, 2026):
        bi = W.month_index(yr - 1, 12)
        fl = [d for d in fs if d["first"] is not None and d["first"] <= bi]
        R = rates(fs, plan_i=bi)
        fc_ = sum(ta(d, R, list(range(bi + 1, bi + 13)), d["C"] - called_to(d, bi)) for d in fl)
        real = sum(d["calls"].get(i, 0.0) for d in fl for i in range(bi + 1, bi + 13))
        print("  back-test %d: R1 %.1f realised %.1f (%+.1f%%)" % (yr, fc_ / 1e6, real / 1e6, 100 * (fc_ / real - 1)))
    for d in fs:
        if WIN[0] - 3 <= d["ip"] <= WIN[-1] + 9:
            print("    %-9s %s C %6.1f called %.3f ip_end %s" % (d["code"], d["s"], d["C"] / 1e6, called_to(d, PLAN_I) / d["C"], d["ip_date"]))
    return cells


if __name__ == "__main__":
    funds, fx_rows = sim.simulate()
    report(funds, fx_rows)
