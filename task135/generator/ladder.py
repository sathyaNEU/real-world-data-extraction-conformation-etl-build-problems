"""The ladder and the Layer 1 grid on the pack's own returns."""
import numpy as np

import estimators as E
import callcalc as CC
import world as W

SLIPS = ["flows left in", "distributions left out", "post-holiday days dropped", "common trading days kept",
         "permanent endowment only", "expendable endowment only", "mandate cash left out", "accrued income left out",
         "demerger uncarried", "accumulation units", "250 days a year", "260 days a year"]
# the deliberate stale-day filter, in its two forms: a lower rung that investment policy 4.3 refuses (the periods it
# leaves are not of equal length), accepted at stage 3 with its figures recorded rather than held off 60
ACCEPTED = ("post-holiday days dropped", "common trading days kept")


def pack_matrix(F, **kw):
    return CC.matrix(F["val"], F["moves"], F["events"], F["kest"], **kw)


def merged(X, d, drop):
    """the dates in `drop` taken out of the price series, so the next kept date's return runs across them"""
    rows, dates, carry = [], [], np.ones(X.shape[1])
    for k in range(len(d)):
        carry = carry * (1 + X[k])
        if k in drop and k + 1 < len(d):
            continue
        rows.append(carry - 1)
        dates.append(d[k])
        carry = np.ones(X.shape[1])
    return np.array(rows), dates


def slip_matrix(F, slip):
    if slip == "flows left in":
        return pack_matrix(F, flows_in=True)
    if slip == "distributions left out":
        return pack_matrix(F, dist_out=True)
    if slip == "post-holiday days dropped":
        # the days the North American or Japan fund carries no new close of its market
        X, d = pack_matrix(F)
        return merged(X, d, set(CC.post_holiday_rows(F["cal"], d)))
    if slip == "common trading days kept":
        # only the calendars' days on which London, New York and Tokyo are all open
        X, d = pack_matrix(F)
        return merged(X, d, set(CC.non_common_rows(F["cal"], d)))
    if slip == "permanent endowment only":
        return pack_matrix(F, sub="WRX-PE01")
    if slip == "expendable endowment only":
        return pack_matrix(F, sub="WRX-EX02")
    if slip == "mandate cash left out":
        return pack_matrix(F, cash=False)
    if slip == "accrued income left out":
        return pack_matrix(F, accrued=False)
    if slip == "demerger uncarried":
        return pack_matrix(F, carry=False)
    if slip == "accumulation units":
        return pack_matrix(F, unit="acc")
    return pack_matrix(F)


def calls_on(X, dates, per_year=None):
    """the default's call and every golden member's call"""
    T = E.table(X, dates)
    if per_year:
        f = np.sqrt(per_year / 252.0)
        T = {n: {s: (v * f if not ("five-day blocks" in n or "calendar" in n) else v) for s, v in t.items()} for n, t in T.items()}
    return {n: E.call(t) for n, t in T.items()}, T


def slip_grid(F):
    out = {}
    for s in SLIPS:
        py = 250 if s == "250 days a year" else 260 if s == "260 days a year" else None
        X, d = slip_matrix(F, s)
        calls, T = calls_on(X, d, py)
        gold = sorted({c for n, c in calls.items() if E.GOLDEN(n)}, key=lambda x: (x is None, x))
        outlier = float(np.max(np.abs(X[:, 0] - np.median(X[:, 0]))) / np.std(X[:, 0]))
        out[s] = dict(default=calls["R0 daily"], golden=gold, outlier=outlier, maxabs=float(np.max(np.abs(X))))
    return out


def slip_ok(g):
    """no slip lands the default on 60; no slip moves the golden family off 60 unless it is gross (50 or below on every
    member, with a one-day return of ten per cent or more that a solver sees); the accepted stale-day filter is recorded
    instead (checks.py asserts its refusal by policy 4.3)"""
    bad = []
    for s, r in g.items():
        if s in ACCEPTED:
            continue
        if r["default"] == 60:
            bad.append((s, "default on 60"))
        if r["golden"] != [60]:
            gross = all(x is None or x <= 50 for x in r["golden"])
            if not (gross and r["maxabs"] > 0.10):
                bad.append((s, "golden %s" % r["golden"]))
    return bad
