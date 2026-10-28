"""The policy's arithmetic on a start date: the excess fall admissions a current user would run over the days a
patient who stops is off the drug, from months since the patient first started a hypnotic."""
import calendar
import datetime as dt

import params as P


def add_months(d, m):
    y, mo = divmod(d.month - 1 + m, 12)
    y, mo = d.year + y, mo + 1
    return dt.date(y, mo, min(d.day, calendar.monthrange(y, mo)[1]))


def excess_years(start, window=(P.OFF_FROM, P.OFF_TO), months=add_months):
    """sum over the off-drug window of (rate ratio - 1), in years (days over 365)"""
    lo, hi = window[0], window[1] + dt.timedelta(days=1)
    edges, prev = [], start
    for m, rr in P.RR:
        end = months(start, m) if m is not None else dt.date(9999, 1, 1)
        edges.append((prev, end, rr))
        prev = end
    tot = 0.0
    for a, b, rr in edges:
        days = (min(b, hi) - max(a, lo)).days
        if days > 0:
            tot += days * (rr - 1.0)
    return tot / 365.0


def avoided(starts):
    """the admissions a team avoids: the stop share of the users' excess over the window, at the policy's base rate"""
    return P.STOP * P.BASE / 100.0 * sum(excess_years(s) for s in starts)
