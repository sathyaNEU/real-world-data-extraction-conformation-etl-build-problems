"""task248 estimators shared by the simulator's aim, the checks and the write-up: the dashboard's weekly levels, its
episodes, and the shed-load restoration."""
import datetime as dt

import numpy as np

import params as P

LOG10E = np.log10(np.e)


def monday(d):
    return d - dt.timedelta(days=d.weekday())


def percentile_inc(x, q):
    """a spreadsheet's PERCENTILE.INC: linear between the order statistics"""
    x = np.sort(np.asarray(x, dtype=float))
    h = (len(x) - 1) * q
    lo = int(np.floor(h))
    return float(x[lo] + (h - lo) * (x[min(lo + 1, len(x) - 1)] - x[lo]))


def weekly(dates, vals):
    """{monday: mean of the week's composite values}"""
    acc = {}
    for d, v in zip(dates, vals):
        if v is None or (isinstance(v, float) and np.isnan(v)):
            continue
        acc.setdefault(monday(d), []).append(v)
    return {w: float(np.mean(v)) for w, v in acc.items()}


def levels(dates, vals, ref=P.REF):
    wk = weekly(dates, vals)
    base = percentile_inc([v for w, v in wk.items() if ref[0] <= w <= ref[1]], 0.10)
    return {w: v - base for w, v in sorted(wk.items())}, base


def episodes(lev, window=P.WINTER):
    """an episode opens in the first week at High or above and closes in the first week back at Low; counted when it
    opens in the window"""
    n, on, opened = 0, False, []
    for w in sorted(lev):
        x = lev[w]
        if not on and x >= P.HIGH:
            on = True
            if window[0] <= w <= window[1]:
                n += 1
                opened.append(w)
        elif on and x < P.LOW:
            on = False
    return n, opened
