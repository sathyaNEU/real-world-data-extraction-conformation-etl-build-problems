"""The golden and every rung, computed from the world (design time) and, in verify.py, again from the shipped files.
Here the inputs are the world's own tables; calc_from_pack in verify.py reads only the bundle."""
from __future__ import annotations

import math

import numpy as np

import common as K


def placement(E, est=None, bar=K.STANDARD_LOAD, posts=K.NEW_POSTS):
    """BRK-STD-03: one post at a time to the gateway whose load (forecast monthly formal entries over its posts,
    the posts already placed counted) is highest, while that load exceeds the standard; the rest held."""
    est = dict(est or K.ESTABLISHMENT)
    placed = {g: 0 for g in E}
    order = []
    for _ in range(posts):
        load = {g: E[g] / (est[g] + placed[g]) for g in E}
        g = max(load, key=lambda x: (load[x], x))
        if load[g] > bar:
            placed[g] += 1
            order.append((g, load[g]))
        else:
            break
    held = posts - sum(placed.values())
    final = {g: E[g] / (est[g] + placed[g]) for g in E}
    return placed, held, final, order


def base_shipments(W, g):
    return sum(W.volume[(g, y, m)] for (y, m) in K.BASE_MONTHS)


def plan_shipments_k(W):
    """The 2027 network plan: each gateway's base-year month times the plan's growth, in thousands to one decimal."""
    out = {}
    for g in K.GATEWAYS:
        for (y, m) in K.BASE_MONTHS:
            out[(g, m)] = K.round_dp(W.volume[(g, y, m)] * (1 + K.PLAN_GROWTH[g]) / 1000.0, 1)
    return out


def plan_ratio(W, g, plan_k=None):
    plan_k = plan_k or plan_shipments_k(W)
    return sum(plan_k[(g, m)] for m in range(1, 13)) * 1000.0 / base_shipments(W, g)


def formal_at(W, g, rate_of, ogd_kept=True):
    """Base-year shipments at gateway g routed with the rate given by rate_of(shipment)."""
    n = 0
    for s in W.ships:
        if s.gw != g:
            continue
        if s.ogd and ogd_kept:
            n += 1
        elif s.ogd and not ogd_kept:
            n += int(s.value * rate_of(s) > K.LINE_CAD)
        else:
            n += int(K.round_dp(s.value * rate_of(s), 2) > K.LINE_CAD)
    return n


def golden_E(W):
    return {g: formal_at(W, g, lambda s: K.PLAN_RATE[s.cur]) * plan_ratio(W, g) / 12.0 for g in K.GATEWAYS}


def default_E(W):
    return {g: sum(W.formal_hist[(g, y, m)] for (y, m) in K.BASE_MONTHS) * plan_ratio(W, g) / 12.0
            for g in K.GATEWAYS}


# ---------------------------------------------------------------------------------------------------- the rungs
def monthly_series(W, g):
    return np.array([W.formal_hist[(g, y, m)] for (y, m) in K.HIST_MONTHS], float), \
        np.array([W.volume[(g, y, m)] for (y, m) in K.HIST_MONTHS], float)


def trend_E(W, g):
    """R0b: a log-linear trend with month-of-year effects on the gateway's monthly formal entries since January 2021,
    carried to 2027 (the shortcut that never looks at a value)."""
    f, _ = monthly_series(W, g)
    t = np.arange(len(f))
    mo = np.array([m for (_, m) in K.HIST_MONTHS])
    X = np.column_stack([np.ones(len(f)), t] + [(mo == k).astype(float) for k in range(2, 13)])
    b, *_ = np.linalg.lstsq(X, np.log(f), rcond=None)
    tf = np.arange(len(f) + 3, len(f) + 15)          # January to December 2027
    Xf = np.column_stack([np.ones(12), tf] + [(np.arange(1, 13) == k).astype(float) for k in range(2, 13)])
    return float(np.exp(Xf @ b).mean())


def holt_winters_E(W, g):
    """R0c: additive-trend, multiplicative-season exponential smoothing on the monthly formal entries."""
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    f, _ = monthly_series(W, g)
    fit = ExponentialSmoothing(f, trend="add", seasonal="mul", seasonal_periods=12,
                               initialization_method="estimated").fit()
    fc = fit.forecast(15)[3:]
    return float(np.mean(fc))


def share_regression_E(W, g):
    """R1: the formal share of shipments regressed on the month's US dollar and euro rates (month-of-year effects),
    evaluated at the plan's rates and carried on the plan's shipments."""
    f, v = monthly_series(W, g)
    share = f / v
    mo = np.array([m for (_, m) in K.HIST_MONTHS])
    usd = np.array([K.monthly_rate("USD", i) for i in range(len(f))])
    eur = np.array([K.monthly_rate("EUR", i) for i in range(len(f))])
    X = np.column_stack([np.ones(len(f)), usd, eur] + [(mo == k).astype(float) for k in range(2, 13)])
    b, *_ = np.linalg.lstsq(X, share, rcond=None)
    sh = []
    for k in range(1, 13):
        row = [1.0, K.PLAN_RATE["USD"], K.PLAN_RATE["EUR"]] + [1.0 if k == j else 0.0 for j in range(2, 13)]
        sh.append(float(np.dot(b, row)))
    plan_k = plan_shipments_k(W)
    return sum(sh[k - 1] * plan_k[(g, k)] * 1000.0 for k in range(1, 13)) / 12.0


def usd_only_E(W):
    """R2: every foreign-currency shipment re-routed with its CAD value moved by the US dollar's change alone."""
    out = {}
    for g in K.GATEWAYS:
        n = formal_at(W, g, lambda s: s.rate * (K.PLAN_RATE["USD"] / W.rates["USD"][s.local.date()])
                      if s.cur != "CAD" else 1.0)
        out[g] = n * plan_ratio(W, g) / 12.0
    return out


def eur_only_E(W):
    """R2b: only the euro shipments re-routed at the plan's euro rate, the rest kept as routed."""
    out = {}
    for g in K.GATEWAYS:
        n = formal_at(W, g, lambda s: K.PLAN_RATE["EUR"] if s.cur == "EUR" else s.rate)
        out[g] = n * plan_ratio(W, g) / 12.0
    return out


def value_only_E(W):
    """R2c: every shipment re-routed at the plan's rate on its value alone, the OGD program ignored."""
    return {g: formal_at(W, g, lambda s: K.PLAN_RATE[s.cur], ogd_kept=False) * plan_ratio(W, g) / 12.0
            for g in K.GATEWAYS}


def latest_quarter_E(W, g):
    """R0d: the formal share of the last three months, carried on the plan."""
    last = K.BASE_MONTHS[-3:]
    f = sum(W.formal_hist[(g, y, m)] for (y, m) in last)
    v = sum(W.volume[(g, y, m)] for (y, m) in last)
    plan_k = plan_shipments_k(W)
    return f / v * sum(plan_k[(g, k)] for k in range(1, 13)) * 1000.0 / 12.0


def pooled_E(W):
    """R0e: the network's formal share of the base year carried on each gateway's plan."""
    f = sum(W.formal_hist[(g, y, m)] for g in K.GATEWAYS for (y, m) in K.BASE_MONTHS)
    v = sum(W.volume[(g, y, m)] for g in K.GATEWAYS for (y, m) in K.BASE_MONTHS)
    plan_k = plan_shipments_k(W)
    return {g: f / v * sum(plan_k[(g, k)] for k in range(1, 13)) * 1000.0 / 12.0 for g in K.GATEWAYS}


def spot_E(W):
    """A rival rate basis: the shipments re-routed at the last rate on file (30 September 2026) instead of the plan's."""
    last = {c: W.rates[c][K.HIST_END] for c in K.CURRENCIES}
    return {g: formal_at(W, g, lambda s: last[s.cur]) * plan_ratio(W, g) / 12.0 for g in K.GATEWAYS}


def inflated_E(W, f):
    """The corridor: invoice values moved by a factor f before the plan's rates are applied."""
    return {g: formal_at(W, g, lambda s: K.PLAN_RATE[s.cur] * f) * plan_ratio(W, g) / 12.0 for g in K.GATEWAYS}


# ---------------------------------------------------------------------------------------------------- the asks
OT_CODES = ("OT15", "OT20")


def ask_a(staff, lines, mode="golden"):
    """Overtime hours worked at each desk in each fiscal quarter of 2025-26.
    golden: OT lines at their hours, call-backs at the time between punches, the October overlap once, each line on
    the desk the employee was assigned to on the work date.
    s1: the line's home cost centre as the export stamped it; s2: call-backs at paid hours; s3: the migration week
    twice; cracker: all three; s5: the HR staff file's current desk for every line."""
    import field as FD
    by_k = {s.k: s for s in staff}
    out = {(g, q): 0.0 for g in K.GATEWAYS for q in (1, 2, 3, 4)}
    for ln in lines:
        if not (K.FY_START <= ln.day <= K.FY_END):
            continue
        if ln.code not in OT_CODES + ("CB",):
            continue
        s = by_k[ln.emp]
        if mode in ("s1", "cracker"):
            if ln.day <= FD.TA_LEGACY_END:
                desk = s.desk_on(FD.TA_LEGACY_PULL) if (s.left is None or s.left > FD.TA_LEGACY_PULL) else s.desk_on(s.left)
            else:
                desk = s.desk_on(FD.TA_NEW_PULL) if (s.left is None or s.left > FD.TA_NEW_PULL) else s.desk_on(s.left)
        elif mode == "s5":
            desk = s.desk_on(FD.HR_PULL) if s.left is None else s.desk_on(s.left)
        else:
            desk = s.desk_on(ln.day)
        if ln.code == "CB":
            h = ln.hours if mode in ("s2", "cracker") else ln.worked
        else:
            h = ln.hours
        mult = 2 if (mode in ("s3", "cracker") and FD.TA_NEW_FROM <= ln.day <= FD.TA_LEGACY_END) else 1
        out[(desk, K.fiscal_quarter(ln.day))] += h * mult
    return out


def ask_b(stmts, mode="golden"):
    """What Brandmoor charged before tax for the entries it transmitted for each desk in each fiscal quarter.
    golden: each statement's net (its entry charges and minimum adjustment once) on its transmissions' month, the
    re-issue in place of the original. s1 (cracker): the AP register by posting date, both statements of the dispute;
    s2: the statements by their titled month (the re-issue in place); s3: the portal by transmission date, the
    minimum adjustment on every line, March 2026 absent; s4: the portal by transmission date, the adjustment once,
    March 2026 absent; s5: the statements on their transmissions' month, the disputed original kept beside its
    re-issue."""
    out = {(g, q): 0.0 for g in K.GATEWAYS for q in (1, 2, 3, 4)}
    replaced = {s.reissue_of for s in stmts if s.reissue_of}
    for st in stmts:
        tm = st.month
        im = (st.issued.year, st.issued.month)
        if mode == "golden":
            if st.number in replaced:
                continue
            d = dt_date(*tm)
            if K.FY_START <= d <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(d))] += st.net
        elif mode == "s1":
            post = st.issued       # posted within days of issue, same month (asserted in checks)
            if K.FY_START <= post <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(post))] += st.net
            if st.credit_memo and K.FY_START <= st.credit_memo[1] <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(st.credit_memo[1]))] -= st.net
        elif mode == "s5":
            d = dt_date(*tm)
            if K.FY_START <= d <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(d))] += st.net
        elif mode == "s2":
            if st.number in replaced:
                continue
            lab = dt_date(st.month[0] + (st.month[1] == 12), st.month[1] % 12 + 1)
            if K.FY_START <= lab <= K.FY_END:
                out[(st.gw, K.fiscal_quarter(lab))] += st.net
        elif mode in ("s3", "s4"):
            if st.number in replaced:
                continue
            lab = dt_date(st.month[0] + (st.month[1] == 12), st.month[1] % 12 + 1)
            if not (dt_date(2025, 4, 1) <= lab <= dt_date(2026, 3, 1)):
                continue
            std_r, ogd_r, rush_r = st.portal_rates
            for e in st.entries:
                d = e.t.date()
                if not (K.FY_START <= d <= K.FY_END):
                    continue
                fee = std_r if e.service == "STD" else ogd_r
                v = fee + (rush_r if e.rush else 0.0)
                if mode == "s3":
                    v += st.minimum_adj
                out[(st.gw, K.fiscal_quarter(d))] += v
            if mode == "s4":
                d = dt_date(*tm)
                if K.FY_START <= d <= K.FY_END:
                    out[(st.gw, K.fiscal_quarter(d))] += st.minimum_adj
    return out


def dt_date(y, m, d=1):
    import datetime as _dt
    return _dt.date(y, m, d)
