"""The routes from the conformed quarterly record to each industry's 2021 to 2025 growth in pay per job, and the slate.

rec: {sector: {(year, quarter): (wages paid, (month1 jobs, month2 jobs, month3 jobs))}}, as published (latest release).
Every route takes the same record; they differ only in how wages paid become pay for the work done."""
import numpy as np

import sources as S
import world as W

QD = 365.25 / 4 / 14         # the biweekly pay dates in an average quarter


def shifted_counts(key, shift=True):
    if shift:
        return S.counts(key)
    c = {}
    for d, _ in S.paydays(key):
        c[S.qof(d)] = c.get(S.qof(d), 0) + 1
    return c


def annual_jobs(rec_s, y):
    return sum(sum(rec_s[(y, q)][1]) for q in range(1, 5)) / 12


def annual_paid(rec_s, y):
    return sum(rec_s[(y, q)][0] for q in range(1, 5))


def exposures(rec_s, keys=("FA", "FB", "TA", "TB"), form="yfe", shift=True, years=None, per_job=True, log=True):
    """Each phase's share of the payroll, from how the quarter's wages move with the pay dates it holds."""
    years = years or list(range(W.Y0, W.Y1 + 1))
    cnt = {k: shifted_counts(k, shift) for k in keys}
    X, Y = [], []
    for y in years:
        for q in range(1, 5):
            w, jm = rec_s[(y, q)]
            v = w / (sum(jm) / 3) if per_job else w
            r = []
            if form == "yfe":
                r += [1.0 if y == yy else 0.0 for yy in years]
            else:
                t = y + (q - 1) / 4 - 2019
                r += [1.0, t, t * t, t ** 3] + [1.0 if (y, q) == c else 0.0 for c in ((2020, 2), (2020, 3), (2020, 4))]
            r += [1.0 if q == qq else 0.0 for qq in (2, 3, 4)]
            r += [cnt[k].get((y, q), 0) for k in keys]
            X.append(r)
            Y.append(np.log(v) if log else v)
    X, Y = np.array(X), np.array(Y)
    b = np.linalg.lstsq(X, Y, rcond=None)[0]
    beta = b[-len(keys):]
    if not log:
        beta = beta / np.mean(Y)
    return {k: float(beta[i] * QD) for i, k in enumerate(keys)}


def ratio(e, y, shift=True):
    """Wages paid in year y over the pay for the work done in it, for a payroll with phase exposures e."""
    r = 1.0
    for k, s in e.items():
        n = sum(shifted_counts(k, shift).get((y, q), 0) for q in range(1, 5))
        r += s * (n * 14 / S.ydays(y) - 1)
    return r


def growth(rec_s, e=None, shift=True):
    e = e or {}
    a = annual_paid(rec_s, W.BASE) / ratio(e, W.BASE, shift) / annual_jobs(rec_s, W.BASE)
    b = annual_paid(rec_s, W.LATEST) / ratio(e, W.LATEST, shift) / annual_jobs(rec_s, W.LATEST)
    return b / a - 1


def eligible(rec):
    return sorted(s for s in rec if s != "99" and annual_jobs(rec[s], W.LATEST) >= W.MIN_JOBS)


def route(rec, name):
    """{sector: growth} for every eligible sector under a named route."""
    out = {}
    tot = None
    if name == "total":
        keys = list(rec[eligible(rec)[0]].keys())
        tot = {k: (sum(rec[s][k][0] for s in rec), tuple(sum(rec[s][k][1][i] for s in rec) for i in range(3)))
               for k in keys}
        et = exposures(tot)
    for s in eligible(rec):
        r = rec[s]
        if name == "paid":
            out[s] = growth(r)
        elif name == "friday":
            out[s] = growth(r, exposures(r, keys=("FA", "FB")))
        elif name == "noshift":
            out[s] = growth(r, exposures(r, shift=False), shift=False)
        elif name == "total":
            out[s] = growth(r, et)
        elif name == "golden":
            out[s] = growth(r, exposures(r))
        elif name == "trend":
            out[s] = growth(r, exposures(r, form="trend"))
        elif name == "levels":
            out[s] = growth(r, exposures(r, log=False))
        elif name == "wages":
            out[s] = growth(r, exposures(r, per_job=False))
        elif name == "since2016":
            out[s] = growth(r, exposures(r, years=list(range(2016, W.Y1 + 1))))
        elif name == "no2020":
            out[s] = growth(r, exposures(r, years=[y for y in range(W.Y0, W.Y1 + 1) if y != 2020]))
        elif name == "weekly":
            out[s] = growth(r, exposures(r, keys=("FA", "FB", "TA", "TB")))
        else:
            raise KeyError(name)
    return out


FAMILY = ["golden", "trend", "levels", "wages", "since2016", "no2020"]
WRONG = ["paid", "friday", "noshift", "total"]


def slate(g):
    order = sorted(g, key=lambda s: -g[s])
    return order[:W.SLATE], order[W.SLATE]
