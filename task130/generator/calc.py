"""The main call's arithmetic on plain inputs, shared by the build's analysis (inputs read from the shipped pack) and
the seed search (inputs from the simulation): the golden, each rung of the ladder and the fork grid.

Inputs
  claims  list of dicts: cls, lag (days from incident to the Claim's first making), cost (trended, 2027 level),
          year (incident year), parts (list of (lag, cost) for each claim number apart, for the L0 rung)
  E       FTE-years of covered clinicians in the experience, by class
  plan    {(entity, class): [12 monthly FTE]}
  trans   {entity: transition date}"""
from __future__ import annotations

import datetime as dt

import numpy as np

YEAR = 2027
END = dt.date(YEAR, 12, 31)
NDAYS = 365


def day_weights(plan_row, start):
    """Each day's FTE-years from the transition date: each month's FTE is one twelfth of an FTE-year, earned
    evenly over the days of the month. Index 0 is 1 January."""
    w = np.zeros(NDAYS)
    d = dt.date(YEAR, 1, 1)
    for i in range(NDAYS):
        if d >= start:
            dim = (dt.date(YEAR + (d.month == 12), d.month % 12 + 1, 1) - dt.date(YEAR, d.month, 1)).days
            w[i] = plan_row[d.month - 1] / 12.0 / dim
        d += dt.timedelta(days=1)
    return w


def days_left():
    """(31 December 2027 - day).days for each day of 2027."""
    return np.arange(NDAYS - 1, -1, -1)


def cum_by_lag(lags, weights):
    """G[t] = sum of weights with lag <= t, t = 0 .. 364."""
    g = np.zeros(NDAYS)
    for L, c in zip(lags, weights):
        if L <= NDAYS - 1:
            g[L:] += c
    return g


def window(claims, E, plan, trans, classes, entities, lag_key="lag", cost_key="cost"):
    """The golden construction: for each entity and class, the sum over the window's days of the day's FTE-years
    times the experience's cost (and count) per FTE-year of Claims made within the days then left in 2027."""
    left = days_left()
    out = {}
    for k in classes:
        ck = [c for c in claims if c["cls"] == k]
        G = cum_by_lag([c[lag_key] for c in ck], [c[cost_key] for c in ck])
        N = cum_by_lag([c[lag_key] for c in ck], [1.0] * len(ck))
        for e in entities:
            row = plan.get((e, k))
            if row is None:
                continue
            w = day_weights(row, trans[e])
            out[(e, k)] = dict(cost=float(np.dot(w, G[left]) / E[k]), count=float(np.dot(w, N[left]) / E[k]),
                               fte_years=float(w.sum()))
    return out


def window_parts(claims, E, plan, trans, classes, entities):
    """L0: every claim number its own claim, made on its own date, at its own cost."""
    flat = [dict(cls=c["cls"], lag=L, cost=cost) for c in claims for (L, cost) in c["parts"]]
    return window(flat, E, plan, trans, classes, entities)


def by_month(claims, E, plan, trans, classes, entities):
    """Expected cost of the window's Claims by the month of 2027 they are made in, by entity."""
    out = {e: np.zeros(12) for e in entities}
    day_month = np.array([(dt.date(YEAR, 1, 1) + dt.timedelta(days=i)).month - 1 for i in range(NDAYS)])
    for k in classes:
        ck = [c for c in claims if c["cls"] == k and c["lag"] <= NDAYS - 1]
        for e in entities:
            row = plan.get((e, k))
            if row is None:
                continue
            w = day_weights(row, trans[e])
            for c in ck:
                L = c["lag"]
                # incidents on day i are made on day i + L, inside the year when i + L <= 364
                src = w[: NDAYS - L]
                np.add.at(out[e], day_month[L:], src * c["cost"] / E[k])
    return out


def fte_years(plan, trans, entities, classes):
    return {(e, k): float(day_weights(plan[(e, k)], trans[e]).sum()) for e in entities for k in classes
            if (e, k) in plan}


def rungs(claims, E, E_mature, plan, trans, classes, entities, E_2020only=None):
    """Every rung's contribution (unrounded dollars)."""
    X = fte_years(plan, trans, entities, classes)
    gold = window(claims, E, plan, trans, classes, entities)
    tot = lambda d: sum(v["cost"] for v in d.values())
    r = {"golden": tot(gold)}
    A = {k: sum(c["cost"] for c in claims if c["cls"] == k) / E[k] for k in classes}
    n = {k: sum(1 for c in claims if c["cls"] == k) for k in classes}
    avg = {k: sum(c["cost"] for c in claims if c["cls"] == k) / max(1, n[k]) for k in classes}
    mat = [c for c in claims if c["year"] <= 2020]
    Am = {k: sum(c["cost"] for c in mat if c["cls"] == k) / E_mature[k] for k in classes}
    s12 = {k: (sum(1 for c in mat if c["cls"] == k and c["lag"] <= 365) / max(1, sum(1 for c in mat if c["cls"] == k)))
           for k in classes}
    full = {k: sum(c["cost"] * max(0, 365 - c["lag"]) / 365.0 for c in claims if c["cls"] == k) / E[k] for k in classes}
    cal = {k: sum(c["cost"] for c in claims if c["cls"] == k and c["same_year"]) / E[k] for k in classes}
    r["R0"] = sum(A[k] * X[(e, k)] for (e, k) in X)
    r["R0m"] = sum(Am[k] * X[(e, k)] for (e, k) in X)
    r["R1a"] = sum(s12[k] * Am[k] * X[(e, k)] for (e, k) in X)
    r["R1"] = sum(gold[(e, k)]["count"] * avg[k] for (e, k) in gold)
    r["R2"] = sum(full[k] * X[(e, k)] for (e, k) in X)
    r["R2b"] = sum(cal[k] * X[(e, k)] for (e, k) in X)
    r["L0"] = tot(window_parts(claims, E, plan, trans, classes, entities))
    r["step30"] = 0.30 * r["R0m"]
    if E_2020only is not None:
        r["base2020"] = tot(window(claims, E_2020only, plan, trans, classes, entities))
    return r, gold


def grid(claims, E, E_2020, plan, trans, classes, entities):
    """The 32 cells: window (mature, twelve months, full year prorated, by day) x weight (count at the average cost,
    each claim's cost) x escalations (merged, apart) x base FTE (both code sets, 2020 codes only)."""
    X = fte_years(plan, trans, entities, classes)
    cells = {}
    for esc in ("merged", "apart"):
        cl = claims if esc == "merged" else [dict(cls=c["cls"], lag=L, cost=cost, year=c["year"], same_year=sy)
                                               for c in claims for (L, cost, sy) in c["parts3"]]
        for base in ("both", "2020"):
            EE = E if base == "both" else E_2020
            n = {k: sum(1 for c in cl if c["cls"] == k) for k in classes}
            avg = {k: sum(c["cost"] for c in cl if c["cls"] == k) / max(1, n[k]) for k in classes}
            for win in ("mature", "twelve", "fullyear", "byday"):
                for wt in ("count", "cost"):
                    if win == "byday":
                        g = window(cl, EE, plan, trans, classes, entities)
                        if wt == "cost":
                            v = sum(x["cost"] for x in g.values())
                        else:
                            v = sum(g[(e, k)]["count"] * avg[k] for (e, k) in g)
                    else:
                        f = {"mature": lambda L: 1.0, "twelve": lambda L: 1.0 if L <= 365 else 0.0,
                             "fullyear": lambda L: max(0, 365 - L) / 365.0}[win]
                        v = 0.0
                        for k in classes:
                            ck = [c for c in cl if c["cls"] == k]
                            if wt == "cost":
                                per = sum(c["cost"] * f(c["lag"]) for c in ck) / EE[k]
                            else:
                                per = sum(f(c["lag"]) for c in ck) * avg[k] / EE[k]
                            v += per * sum(X[(e, kk)] for (e, kk) in X if kk == k)
                    cells[(win, wt, esc, base)] = v
    return cells
