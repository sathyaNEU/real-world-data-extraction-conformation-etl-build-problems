"""The main call's arithmetic on plain inputs, shared by the build's analysis (inputs read from the shipped pack) and
the seed search (inputs from the simulation): the golden, every rung and rival route, and the fork grid.

Inputs
  claims  list of dicts: cls, lag (days from incident to the Claim's first making), cost (trended, 2027 level),
          year (incident year), ent (entity where the care was given), parts / parts3 (each claim number apart)
  E       FTE-years of covered clinicians in the experience, by class (a basis: every entity, or some of them)
  Ee      FTE-years by (entity, class); Eem the mature years 2017 to 2020; Ee20 the 2020 code set only
  plan    {(entity, class): [12 monthly FTE]}
  trans   {entity: transition date}

The golden prices every entity's window on the experience of the Early Resolution Program's hospitals (Tolliver
Falls and Alderwick): from its Transition Date every entity's patients come to the Trust through the Program, and only
those hospitals' claims and exposure were generated under it."""
from __future__ import annotations

import datetime as dt

import numpy as np

YEAR = 2027
END = dt.date(YEAR, 12, 31)
NDAYS = 365
PROGRAM = ("TFH", "AMC")


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
    """The window construction: for each entity and class, the sum over the window's days of the day's FTE-years
    times the experience's cost (and count) per FTE-year of Claims made within the days then left in 2027. A class
    with no exposure on the basis carries nothing."""
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
            if E.get(k, 0.0) <= 0:
                out[(e, k)] = dict(cost=0.0, count=0.0, fte_years=float(w.sum()))
                continue
            out[(e, k)] = dict(cost=float(np.dot(w, G[left]) / E[k]), count=float(np.dot(w, N[left]) / E[k]),
                               fte_years=float(w.sum()))
    return out


def tot(g):
    return sum(v["cost"] for v in g.values())


def by_ent(g, e):
    return sum(v["cost"] for (ee, k), v in g.items() if ee == e)


def window_parts(claims, E, plan, trans, classes, entities):
    """L0: every claim number its own claim, made on its own date, at its own cost."""
    flat = [dict(cls=c["cls"], lag=L, cost=cost) for c in claims for (L, cost) in c["parts"]]
    return window(flat, E, plan, trans, classes, entities)


def by_month(claims, E, plan, trans, classes, entities):
    """Expected cost of the window's Claims by the month of 2027 they are made in, by entity."""
    out = {e: np.zeros(12) for e in entities}
    day_month = np.array([(dt.date(YEAR, 1, 1) + dt.timedelta(days=i)).month - 1 for i in range(NDAYS)])
    for k in classes:
        if E.get(k, 0.0) <= 0:
            continue
        ck = [c for c in claims if c["cls"] == k and c["lag"] <= NDAYS - 1]
        for e in entities:
            row = plan.get((e, k))
            if row is None:
                continue
            w = day_weights(row, trans[e])
            for c in ck:
                L = c["lag"]
                src = w[: NDAYS - L]
                np.add.at(out[e], day_month[L:], src * c["cost"] / E[k])
    return out


def fte_years(plan, trans, entities, classes):
    return {(e, k): float(day_weights(plan[(e, k)], trans[e]).sum()) for e in entities for k in classes
            if (e, k) in plan}


def basis(Ee, ents, classes):
    """FTE-years by class over the given entities."""
    return {k: sum(v for (e, kk), v in Ee.items() if kk == k and e in ents) for k in classes}


def program(claims):
    return [c for c in claims if c["ent"] in PROGRAM]


def classic(claims, E, E_mature, plan, trans, classes, entities):
    """Each classic rung on one basis (unrounded dollars): the window itself, a mature year per FTE-year (R0, and R0m
    on 2017 to 2020), the share made within twelve months (R1a), the window's count at the average cost (R1), a full
    year's in-year share prorated (R2), the same-calendar-year share (R2b), escalations apart (L0), a first-year
    claims-made step factor of 30 per cent (step30)."""
    X = fte_years(plan, trans, entities, classes)
    win = window(claims, E, plan, trans, classes, entities)
    r = {"window": tot(win)}
    div = lambda a, b: a / b if b > 0 else 0.0
    A = {k: div(sum(c["cost"] for c in claims if c["cls"] == k), E.get(k, 0.0)) for k in classes}
    n = {k: sum(1 for c in claims if c["cls"] == k) for k in classes}
    avg = {k: div(sum(c["cost"] for c in claims if c["cls"] == k), n[k]) for k in classes}
    mat = [c for c in claims if c["year"] <= 2020]
    Am = {k: div(sum(c["cost"] for c in mat if c["cls"] == k), E_mature.get(k, 0.0)) for k in classes}
    s12 = {k: div(sum(1 for c in mat if c["cls"] == k and c["lag"] <= 365), sum(1 for c in mat if c["cls"] == k))
           for k in classes}
    full = {k: div(sum(c["cost"] * max(0, 365 - c["lag"]) / 365.0 for c in claims if c["cls"] == k), E.get(k, 0.0))
            for k in classes}
    cal = {k: div(sum(c["cost"] for c in claims if c["cls"] == k and c["same_year"]), E.get(k, 0.0)) for k in classes}
    r["R0"] = sum(A[k] * X[(e, k)] for (e, k) in X)
    r["R0m"] = sum(Am[k] * X[(e, k)] for (e, k) in X)
    r["R1a"] = sum(s12[k] * Am[k] * X[(e, k)] for (e, k) in X)
    r["R1"] = sum(win[(e, k)]["count"] * avg[k] for (e, k) in win)
    r["R2"] = sum(full[k] * X[(e, k)] for (e, k) in X)
    r["R2b"] = sum(cal[k] * X[(e, k)] for (e, k) in X)
    r["L0"] = tot(window_parts(claims, E, plan, trans, classes, entities))
    r["step30"] = 0.30 * r["R0m"]
    return r, win


def rivals(ex, Ee, Eem, plan, trans, classes, entities):
    """The golden and every rival route the ladder and the audit name (unrounded dollars)."""
    allents = sorted({e for (e, k) in Ee})
    P = list(PROGRAM)
    S = [e for e in allents if e not in PROGRAM]
    exP = program(ex)
    exS = [c for c in ex if c["ent"] not in PROGRAM]
    EP, EPm = basis(Ee, P, classes), basis(Eem, P, classes)
    EA, EAm = basis(Ee, allents, classes), basis(Eem, allents, classes)
    out = {}
    rG, gold = classic(exP, EP, EPm, plan, trans, classes, entities)
    rA, pooled = classic(ex, EA, EAm, plan, trans, classes, entities)
    out["golden"] = rG["window"]
    out["pooled"] = rA["window"]
    for key in ("R0", "R0m", "R1a", "R1", "R2", "R2b", "L0", "step30"):
        out["pooled_" + key] = rA[key]
        out["program_" + key] = rG[key]
    own = {}
    for e in entities:
        exe = [c for c in ex if c["ent"] == e]
        own[e] = by_ent(window(exe, basis(Ee, [e], classes), plan, trans, classes, [e]), e)
    out["by_entity"] = sum(own.values())
    stone = window(exS, basis(Ee, S, classes), plan, trans, classes, [e for e in entities if e not in PROGRAM])
    out["by_carrier"] = sum(by_ent(gold, e) for e in P) + tot(stone)
    out["h1_own_program_hospitals"] = sum(own[e] for e in P) + sum(by_ent(gold, e) for e in entities if e not in P)
    out["h3_program_for_stoneleigh_only"] = sum(by_ent(pooled, e) for e in P) + \
        sum(by_ent(gold, e) for e in entities if e not in P)
    out["program_claims_over_all_fte"] = tot(window(exP, EA, plan, trans, classes, entities))
    # the Program's effect read as a relativity on a full year's cost per FTE-year by class (the Program hospitals'
    # against the System's), applied to the pooled window: the effect measured at full development points the other way
    rate = lambda cl, E, k: (sum(c["cost"] for c in cl if c["cls"] == k) / E[k]) if E.get(k, 0.0) > 0 else 0.0
    rel = {k: (rate(exP, EP, k) / rate(ex, EA, k)) if rate(ex, EA, k) > 0 else 1.0 for k in classes}
    out["pooled_window_by_full_year_relativity"] = sum(v["cost"] * rel[k] for (e, k), v in pooled.items())
    out["stoneleigh_for_all"] = tot(window(exS, basis(Ee, S, classes), plan, trans, classes, entities))
    # the quick claims (made within 330 days, the Program's reach) from the Program hospitals, the rest pooled
    quickP = [c for c in exP if c["lag"] <= 330]
    slowA = [c for c in ex if c["lag"] > 330]
    out["h4_quick_program_slow_pooled"] = tot(window(quickP, EP, plan, trans, classes, entities)) + \
        tot(window(slowA, EA, plan, trans, classes, entities))
    return out, gold, pooled, own


def grid(claims, E, plan, trans, classes, entities):
    """The 16 cells on one basis: window (mature, twelve months, full year prorated, by day) x weight (count at the
    average cost, each claim's cost) x escalations (merged, apart)."""
    X = fte_years(plan, trans, entities, classes)
    div = lambda a, b: a / b if b > 0 else 0.0
    cells = {}
    for esc in ("merged", "apart"):
        cl = claims if esc == "merged" else [dict(cls=c["cls"], lag=L, cost=cost, year=c["year"], same_year=sy)
                                               for c in claims for (L, cost, sy) in c["parts3"]]
        n = {k: sum(1 for c in cl if c["cls"] == k) for k in classes}
        avg = {k: div(sum(c["cost"] for c in cl if c["cls"] == k), n[k]) for k in classes}
        for win in ("mature", "twelve", "fullyear", "byday"):
            for wt in ("count", "cost"):
                if win == "byday":
                    g = window(cl, E, plan, trans, classes, entities)
                    v = tot(g) if wt == "cost" else sum(g[(e, k)]["count"] * avg[k] for (e, k) in g)
                else:
                    f = {"mature": lambda L: 1.0, "twelve": lambda L: 1.0 if L <= 365 else 0.0,
                         "fullyear": lambda L: max(0, 365 - L) / 365.0}[win]
                    v = 0.0
                    for k in classes:
                        ck = [c for c in cl if c["cls"] == k]
                        if wt == "cost":
                            per = div(sum(c["cost"] * f(c["lag"]) for c in ck), E.get(k, 0.0))
                        else:
                            per = div(sum(f(c["lag"]) for c in ck) * avg[k], E.get(k, 0.0))
                        v += per * sum(X[(e, kk)] for (e, kk) in X if kk == k)
                cells[(win, wt, esc)] = v
    return cells
