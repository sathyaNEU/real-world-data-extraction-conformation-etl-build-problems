"""How the bank's cases come to exist, and when anyone first sees them."""
import datetime as dt
import math
import random

import world as W


def months_between(a, b):
    return (b.year - a.year) * 12 + (b.month - a.month)


def month_start(d):
    return dt.date(d.year, d.month, 1)


def add_months(d, n):
    y, m = divmod((d.year * 12 + d.month - 1) + n, 12)
    return dt.date(y, m + 1, min(d.day, 28))


def delay_months(rng, mean):
    """months a case goes unseen: a bounded spread around the line's own mean.

    The spread is capped at W.DELAY_CAP months, which is the longest any case in the bank's record has
    gone unseen, so onset cohorts older than that are resolved as a matter of the record rather than
    of anybody's say-so.
    """
    if rng.random() < 0.014:
        # now and then a case surfaces years after it began, on any line
        x = rng.gammavariate(2.2, 1.0 / 2.2) * (3.0 + 9.0 * rng.random())
    else:
        x = rng.gammavariate(2.2, 1.0 / 2.2)
    return max(0, min(W.DELAY_CAP, int(round(mean * x))))


SEASON = [1.04, 0.92, 1.06, 1.01, 0.97, 0.95, 1.0, 1.03, 1.08, 1.05, 0.98, 0.91]


def poisson(rng, mu):
    """Knuth's method: the month's case count, drawn rather than rounded"""
    if mu <= 0:
        return 0
    k, p, lim = 0, 1.0, math.exp(-mu)
    while True:
        p *= rng.random()
        if p <= lim:
            return k
        k += 1
        if k > 400:
            return k


def pick_typology(rng, code):
    """the typologies the line actually sees, in the mix it sees them in"""
    w = [x + 1.5 for x in W.TYPOLOGY_MIX[code]]
    x = rng.random() * sum(w)
    run = 0.0
    for t, wt in zip(W.TYPOLOGIES, w):
        run += wt
        if x <= run:
            return t
    return W.TYPOLOGIES[-1]


def cases(line):
    """every case the line generates over the register's span, with its onset and its delay"""
    name, code, lam, cust, wbar, backlog = line
    rng = random.Random(W.SEED * 31 + sum(ord(c) for c in code))
    span = months_between(W.SPAN_FROM, W.REVIEW_FROM) + 1
    per_month = lam / 3.0
    out = []
    n = 0
    for m in range(span):
        onset_month = add_months(W.SPAN_FROM, m)
        mu = per_month * W.YEAR_FACTOR[code][onset_month.year] * SEASON[onset_month.month - 1]
        for _ in range(poisson(rng, mu)):
            n += 1
            day = 1 + rng.randrange(0, 27)
            onset = dt.date(onset_month.year, onset_month.month, day)
            d = delay_months(rng, wbar)
            out.append({"line": name, "code": code, "n": n, "onset": onset, "delay": d,
                        "detected": add_months(onset, d),
                        "typology": pick_typology(rng, code)})
    return out


def calibrate(line, target_lam, target_w, rounds=40):
    """nudge the draw so the line's closed-window arrival rate and mean delay hit their targets"""
    name, code, lam, cust, wbar, backlog = line
    lo_w, hi_w = 0.2 * target_w, 3.0 * target_w
    for _ in range(rounds):
        mid = (lo_w + hi_w) / 2.0
        rows = cases((name, code, lam, cust, mid, backlog))
        closed = [r for r in rows if W.CLOSED_FROM <= r["onset"] <= W.CLOSED_TO]
        got = sum(r["delay"] for r in closed) / len(closed)
        if got < target_w:
            lo_w = mid
        else:
            hi_w = mid
    return (lo_w + hi_w) / 2.0
