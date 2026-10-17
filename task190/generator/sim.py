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

    The spread is capped at W.DELAY_CAP months, so every case with an onset in the closed window has
    been seen by the extract date and clause 6.3's closure is exact rather than approximate.
    """
    x = rng.gammavariate(2.2, 1.0 / 2.2)
    return max(0, min(W.DELAY_CAP, int(round(mean * x))))


def cases(line):
    """every case the line generates from 2022 to the review date, with its onset and its delay"""
    name, code, lam, cust, wbar, backlog = line
    rng = random.Random(W.SEED * 31 + sum(ord(c) for c in code))
    span = months_between(W.SPAN_FROM, W.REVIEW_FROM) + 1
    per_month = lam / 3.0
    out = []
    n = 0
    for m in range(span):
        onset_month = add_months(W.SPAN_FROM, m)
        k = int(per_month) + (1 if rng.random() < (per_month - int(per_month)) else 0)
        for _ in range(k):
            n += 1
            day = 1 + rng.randrange(0, 27)
            onset = dt.date(onset_month.year, onset_month.month, day)
            d = delay_months(rng, wbar)
            out.append({"line": name, "code": code, "n": n, "onset": onset, "delay": d,
                        "detected": add_months(onset, d),
                        "typology": W.TYPOLOGIES[(n + sum(ord(c) for c in code)) % len(W.TYPOLOGIES)]})
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
