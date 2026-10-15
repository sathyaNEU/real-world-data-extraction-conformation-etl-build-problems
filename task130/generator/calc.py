"""The main call's arithmetic on plain inputs, shared by the build's analysis (inputs read from the shipped pack) and
the seed search (inputs from the simulation): the golden, every route a solver can take to the contribution, the
conventions the fork table closes, and the golden's sampling error.

Inputs
  claims  list of dicts, one per experience Claim: cls, lag (days from incident to the Claim's first making), cost
          (trended, 2027 level), year (incident year), same_year, parts (lag, cost) per claim number, mtype, alleg
  E       FTE-years of covered clinicians in the experience, by class (each payroll month one twelfth of an FTE-year)
  plan    {(entity, class): [12 monthly FTE]}
  trans   {entity: Transition Date}"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

YEAR = 2027
END = dt.date(YEAR, 12, 31)
NDAYS = 365
BIN = 250_000


def _dim(m):
    return (dt.date(YEAR + (m == 12), m % 12 + 1, 1) - dt.date(YEAR, m, 1)).days


def day_weights(plan_row, start):
    """Each day's FTE-years from the Transition Date: a month's plan FTE is one twelfth of an FTE-year, as a payroll
    month is in the experience, held through the month's days. Index 0 is 1 January."""
    w = np.zeros(NDAYS)
    d = dt.date(YEAR, 1, 1)
    for i in range(NDAYS):
        if d >= start:
            w[i] = plan_row[d.month - 1] / 12.0 / _dim(d.month)
        d += dt.timedelta(days=1)
    return w


def fte_years(plan, trans, entities, classes):
    return {(e, k): float(day_weights(plan[(e, k)], trans[e]).sum()) for e in entities for k in classes
            if (e, k) in plan}


def _cum(w):
    return np.concatenate([[0.0], np.cumsum(w)])


def lag_weights(plan, trans, E, classes, entities, end_shift=0):
    """a[k][L], L = 0 .. 365: the 2027 FTE-years of class k, each entity from its Transition Date, with at least L days
    left to 31 December 2027, per experience FTE-year of the class. An experience Claim of class k made L days after
    its incident is expected a[k][L] times among the Claims made in the window; a[k][365] = 0."""
    a = {}
    for k in classes:
        acc = np.zeros(NDAYS + 1)
        for e in entities:
            if (e, k) not in plan:
                continue
            pre = _cum(day_weights(plan[(e, k)], trans[e]))
            for L in range(NDAYS):
                acc[L] += pre[min(NDAYS, max(0, NDAYS - L + end_shift))]
        a[k] = acc / E[k]
    return a


def entity_lag_weights(plan, trans, E, classes, entities):
    out = {}
    for k in classes:
        for e in entities:
            if (e, k) not in plan:
                continue
            pre = _cum(day_weights(plan[(e, k)], trans[e]))
            acc = np.zeros(NDAYS + 1)
            for L in range(NDAYS):
                acc[L] = pre[NDAYS - L]
            out[(e, k)] = acc / E[k]
    return out


def golden(claims, a):
    return float(sum(c["cost"] * a[c["cls"]][c["lag"]] for c in claims if c["lag"] < NDAYS))


def count(claims, a, k=None):
    return float(sum(a[c["cls"]][c["lag"]] for c in claims if c["lag"] < NDAYS and (k is None or c["cls"] == k)))


def poisson_sd(claims, a):
    """The golden's standard error, each experience Claim a Poisson draw of its own kind."""
    return math.sqrt(sum((c["cost"] * a[c["cls"]][c["lag"]]) ** 2 for c in claims if c["lag"] < NDAYS))


def bootstrap_sd(claims, a, reps=400, seed=20261012):
    rng = np.random.default_rng(seed)
    x = np.array([c["cost"] * a[c["cls"]][c["lag"]] if c["lag"] < NDAYS else 0.0 for c in claims])
    return float(np.std([float((x * rng.poisson(1.0, len(x))).sum()) for _ in range(reps)]))


def by_entity_class(claims, plan, trans, E, classes, entities):
    """Expected cost and count of the window's Claims by entity and class."""
    out = {}
    for (e, k), ak in entity_lag_weights(plan, trans, E, classes, entities).items():
        ck = [c for c in claims if c["cls"] == k and c["lag"] < NDAYS]
        out[(e, k)] = dict(cost=float(sum(c["cost"] * ak[c["lag"]] for c in ck)),
                           count=float(sum(ak[c["lag"]] for c in ck)),
                           fte_years=float(day_weights(plan[(e, k)], trans[e]).sum()))
    return out


# ------------------------------------------------------------------------------------------------ fitted curves
def _ols_curve(cl, xf):
    pos = [c for c in cl if c["cost"] > 0]
    x = np.array([xf(c["lag"]) for c in pos])
    y = np.log([c["cost"] for c in pos])
    A = np.vstack([np.ones_like(x), x]).T
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    smear = float(np.mean(np.exp(y - A @ beta)))
    p_pos = len(pos) / len(cl)
    return lambda L: p_pos * smear * math.exp(beta[0] + beta[1] * xf(L))


def _gamma_irls(X, y, beta0=None, iters=300):
    beta = np.zeros(X.shape[1]) if beta0 is None else beta0.copy()
    if beta0 is None:
        beta[0] = math.log(y.mean())
    for _ in range(iters):
        eta = np.clip(X @ beta, -50, 50)
        mu = np.exp(eta)
        z = eta + (y - mu) / mu
        nb = np.linalg.lstsq(X, z, rcond=None)[0]
        if np.max(np.abs(nb - beta)) < 1e-10:
            return nb
        beta = 0.5 * beta + 0.5 * nb
    return beta


def _spline_basis(L):
    x = math.log(max(L, 1))
    return [1.0, x] + [max(0.0, x - kk) for kk in (math.log(30), math.log(90), math.log(365))]


def routes(claims, E, plan, trans, classes, entities):
    """Every route to the contribution, unrounded. golden is the claim-by-claim construction; the rest are the routes a
    solver takes instead (each named in the design note's ladder and closure table)."""
    a = lag_weights(plan, trans, E, classes, entities)
    X = fte_years(plan, trans, entities, classes)
    Xk = {k: sum(v for (e, kk), v in X.items() if kk == k) for k in classes}
    byk = {k: [c for c in claims if c["cls"] == k] for k in classes}
    win = {k: count(claims, a, k) for k in classes}
    mean = lambda cl: float(np.mean([c["cost"] for c in cl]))
    out = {"golden": golden(claims, a)}

    # the frequency-severity family: the expected count of Claims made in the window, at a severity
    out["R1_count_x_class_average"] = sum(win[k] * mean(byk[k]) for k in classes)
    out["R1m_count_x_mature_average"] = sum(win[k] * mean([c for c in byk[k] if c["year"] <= 2020]) for k in classes)
    lnm = {}
    for k in classes:
        x = np.array([c["cost"] for c in byk[k] if c["cost"] > 0])
        mu, sd = float(np.log(x).mean()), float(np.log(x).std())
        lnm[k] = len(x) / len(byk[k]) * math.exp(mu + sd * sd / 2)
    out["R1g_count_x_lognormal_mean"] = sum(win[k] * lnm[k] for k in classes)
    out["R1p_count_x_pooled_average"] = count(claims, a) * mean(claims)
    out["R1y_count_x_average_made_within_year"] = sum(win[k] * mean([c for c in byk[k] if c["lag"] < NDAYS])
                                                      for k in classes)
    out["R1c_count_x_average_same_year"] = sum(win[k] * mean([c for c in byk[k] if c["same_year"]]) for k in classes)
    # each entity's window count at the average cost of its class's Claims made within the entity's window length
    t = 0.0
    for (e, k), ak in entity_lag_weights(plan, trans, E, classes, entities).items():
        span = (END - trans[e]).days + 1
        inside = [c for c in byk[k] if c["lag"] < span]
        if inside:
            t += sum(ak[c["lag"]] for c in byk[k] if c["lag"] < NDAYS) * mean(inside)
    out["R1w_count_x_average_within_entity_window"] = t

    def strat(key):
        tot = 0.0
        for k in classes:
            groups = {}
            for c in byk[k]:
                groups.setdefault(c[key], []).append(c)
            for name in sorted(groups):
                cl = groups[name]
                tot += mean(cl) * sum(a[k][c["lag"]] for c in cl if c["lag"] < NDAYS)
        return tot
    out["R1t_count_x_average_by_matter_type"] = strat("mtype")
    out["R1a_count_x_average_by_allegation"] = strat("alleg")

    # fitted severity curves
    def curve_route(fk):
        return float(sum(a[c["cls"]][c["lag"]] * fk[c["cls"]](c["lag"]) for c in claims if c["lag"] < NDAYS))
    out["F1_loglog_by_class"] = curve_route({k: _ols_curve(byk[k], lambda L: math.log(L)) for k in classes})
    out["F2_loglinear_by_class"] = curve_route({k: _ols_curve(byk[k], lambda L: L / 365.0) for k in classes})
    f = _ols_curve(claims, lambda L: math.log(L))
    out["F3_loglog_pooled"] = curve_route({k: f for k in classes})

    def gamma_classes(xf):
        Xm = np.array([[1.0 if c["cls"] == k else 0.0 for k in classes] + [xf(c["lag"])] for c in claims])
        y = np.array([max(c["cost"], 1.0) for c in claims])
        b0 = np.zeros(Xm.shape[1])
        b0[:len(classes)] = math.log(y.mean())
        beta = _gamma_irls(Xm, y, b0)
        tot = 0.0
        for c in claims:
            if c["lag"] < NDAYS:
                row = np.array([1.0 if c["cls"] == k else 0.0 for k in classes] + [xf(c["lag"])])
                tot += a[c["cls"]][c["lag"]] * math.exp(min(50.0, float(row @ beta)))
        return tot
    out["F4_gamma_loglag_class_factors"] = gamma_classes(lambda L: math.log(L))
    out["F5_gamma_lag_class_factors"] = gamma_classes(lambda L: L / 365.0)

    def per_class_gamma(basis):
        tot = 0.0
        for k in classes:
            cl = byk[k]
            Xm = np.array([basis(c["lag"]) for c in cl])
            beta = _gamma_irls(Xm, np.array([max(c["cost"], 1.0) for c in cl]))
            tot += sum(a[k][c["lag"]] * math.exp(float(np.clip(np.array(basis(c["lag"])) @ beta, -50, 50)))
                       for c in cl if c["lag"] < NDAYS)
        return float(tot)
    out["F6_gamma_quadratic_by_class"] = per_class_gamma(lambda L: [1.0, L / 365.0, (L / 365.0) ** 2])
    out["S1_gamma_spline_by_class"] = per_class_gamma(_spline_basis)
    tot = 0.0
    for k in classes:
        cl = byk[k]
        xs = np.array([c["lag"] / 365.0 for c in cl])
        ys = np.log([max(c["cost"], 1.0) for c in cl])
        A = np.vstack([np.ones_like(xs), xs, xs ** 2]).T
        b, *_ = np.linalg.lstsq(A, ys, rcond=None)
        sm = float(np.mean(np.exp(ys - A @ b)))
        tot += sum(a[k][c["lag"]] * sm * math.exp(b[0] + b[1] * c["lag"] / 365 + b[2] * (c["lag"] / 365) ** 2)
                   for c in cl if c["lag"] < NDAYS)
    out["S2_quadratic_log_ols_by_class"] = float(tot)

    # severity by lag band within class, each band's average cost on its own window count
    def bands(bs):
        t = 0.0
        for k in classes:
            for lo, hi in zip(bs[:-1], bs[1:]):
                cl = [c for c in byk[k] if lo <= c["lag"] < hi]
                if cl:
                    t += mean(cl) * sum(a[k][c["lag"]] for c in cl)
        return t
    out["B1_half_year_bands"] = bands([0, 183, 365])
    out["E1_30_day_bands"] = bands(list(range(0, 361, 30)) + [365])
    out["E2_bands_30_90_180_365"] = bands([0, 31, 91, 181, 365])
    out["E3_bands_90_180_365"] = bands([0, 91, 181, 365])
    out["E4_quarter_bands"] = bands([0, 92, 183, 275, 365])
    out["E5_bands_120_365"] = bands([0, 121, 365])

    # the classes pooled (the funding policy pools within each class)
    tot_cost = sum(c["cost"] for c in claims)
    share = np.zeros(NDAYS + 1)
    for c in claims:
        if c["lag"] < NDAYS:
            share[c["lag"]] += c["cost"] / tot_cost
    out["P1_pooled_lag_share_x_class_rate"] = float(sum(sum(c["cost"] for c in byk[k]) * float(np.dot(share, a[k]))
                                                        for k in classes))
    Etot = sum(E[k] for k in classes)
    a_all = sum(a[k] * E[k] for k in classes) / Etot
    out["P2_all_classes_pooled"] = float(sum(c["cost"] * a_all[c["lag"]] for c in claims if c["lag"] < NDAYS))
    t = 0.0
    edges = list(range(0, 361, 30)) + [365]
    for lo, hi in zip(edges[:-1], edges[1:]):
        cl = [c for c in claims if lo <= c["lag"] < hi]
        if cl:
            t += mean(cl) * sum(a[c["cls"]][c["lag"]] for c in cl)
    out["P3_pooled_band_severity_x_class_counts"] = t

    # no lag truncation, or a calendar shortcut for it
    out["R0_mature_year"] = sum(sum(c["cost"] for c in byk[k]) / E[k] * Xk[k] for k in classes)
    out["R2_full_year_share_prorated"] = sum(sum(c["cost"] * max(0, NDAYS - c["lag"]) / NDAYS for c in byk[k]) / E[k]
                                             * Xk[k] for k in classes)
    out["R2b_same_year_prorated"] = sum(sum(c["cost"] for c in byk[k] if c["same_year"]) / E[k] * Xk[k]
                                        for k in classes)
    t = 0.0
    for (e, k), fy in X.items():
        L = (END - trans[e]).days + 1
        t += sum(c["cost"] for c in byk[k] if c["lag"] < L) / E[k] * fy
    out["R3_window_length_filter"] = t
    return out, a


def conventions(claims, E, plan, trans, classes, entities):
    """The golden under each convention the fork table closes."""
    a = lag_weights(plan, trans, E, classes, entities)
    out = {"golden": golden(claims, a)}
    out["lag_plus_1"] = golden([dict(c, lag=c["lag"] + 1) for c in claims], a)
    out["lag_minus_1"] = golden([dict(c, lag=max(0, c["lag"] - 1)) for c in claims], a)
    for name, d in (("transition_plus_1", 1), ("transition_minus_1", -1)):
        tr2 = {e: trans[e] + dt.timedelta(days=d) for e in trans}
        if d < 0:
            # a day before 1 January 2027 is outside the Plan Year: Tolliver Falls keeps its start
            tr2["TFH"] = trans["TFH"]
        out[name] = golden(claims, lag_weights(plan, tr2, E, classes, entities))
    out["window_end_plus_1"] = golden(claims, lag_weights(plan, trans, E, classes, entities, end_shift=1))

    def month_point(day):
        tot = 0.0
        for k in classes:
            ck = [c for c in claims if c["cls"] == k]
            for e in entities:
                if (e, k) not in plan:
                    continue
                for mth in range(trans[e].month, 13):
                    dd = min(day, _dim(mth))
                    left = (END - dt.date(YEAR, mth, dd)).days
                    w = plan[(e, k)][mth - 1] / 12.0 / E[k]
                    tot += w * sum(c["cost"] for c in ck if c["lag"] <= left)
        return tot
    out["month_mid"] = month_point(15)
    out["month_start"] = month_point(1)
    out["month_end"] = month_point(31)
    # each day one 365th of the month's FTE-year share (calendar-day exposure)
    tot = 0.0
    for k in classes:
        ck = [c for c in claims if c["cls"] == k and c["lag"] < NDAYS]
        for e in entities:
            if (e, k) not in plan:
                continue
            w = np.zeros(NDAYS)
            d = dt.date(YEAR, 1, 1)
            for i in range(NDAYS):
                if d >= trans[e]:
                    w[i] = plan[(e, k)][d.month - 1] / NDAYS
                d += dt.timedelta(days=1)
            pre = _cum(w)
            tot += sum(c["cost"] * pre[NDAYS - c["lag"]] for c in ck) / E[k]
    out["calendar_day_exposure"] = tot
    return out


def rounded(x):
    return int(math.floor(x / BIN + 0.5) * BIN)
