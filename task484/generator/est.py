"""The estimators every rung and the golden use, on plain arrays (no file I/O).

Shared by world.py (which tunes the count days on the values it is about to write) and analysis.py (which
reads them back from target/). Days are indexed 0..364 for 2025.
"""
import datetime as dt

import numpy as np

YEAR = 2025
DAYS = [dt.date(YEAR, 1, 1) + dt.timedelta(i) for i in range(365)]


def mean_valid(x):
    x = np.asarray(x, dtype=float)
    return float(np.nanmean(x))


# ----- the textbook expansion from the permanent counters (the default and the golden off the detectors) -----
def tmg_sameday_ratio_of_sums(c12, di, atcs):
    """atcs: list of (q24 array, q12 array). Ratio of the group's annual means to its counted-day 12 hours."""
    num = sum(mean_valid(a[0]) for a in atcs)
    den = sum(float(a[1][di]) for a in atcs)
    return c12 * num / den


def tmg_sameday_mean_of_ratios(c12, di, atcs):
    return c12 * float(np.mean([mean_valid(a[0]) / float(a[1][di]) for a in atcs]))


def tmg_average_factor(c12, di, atcs, holidays=()):
    """Average factor: the group's annual mean over its mean 12 hours on the same weekday in the same month."""
    d = DAYS[di]
    idx = [i for i, x in enumerate(DAYS) if x.month == d.month and x.weekday() == d.weekday() and x not in holidays]
    num = sum(mean_valid(a[0]) for a in atcs)
    den = sum(float(np.nanmean(np.asarray(a[1], dtype=float)[idx])) for a in atcs)
    return c12 * num / den


def tmg_split_factor(c12, di, atcs, holidays=()):
    """Separate factors: the group's 24/12 ratio over the year, times its annual mean over the counted
    weekday's mean 24 hours in that month (the month-and-weekday factor table)."""
    d = DAYS[di]
    q24 = [np.asarray(a[0], dtype=float) for a in atcs]
    q12 = [np.asarray(a[1], dtype=float) for a in atcs]
    r = sum(np.nansum(x) for x in q24) / sum(np.nansum(x) for x in q12)
    idx = [i for i, x in enumerate(DAYS) if x.month == d.month and x.weekday() == d.weekday() and x not in holidays]
    seas = sum(mean_valid(x) for x in q24) / sum(float(np.nanmean(x[idx])) for x in q24)
    return c12 * r * seas


TMG = {"T1 same-day, ratio of sums": tmg_sameday_ratio_of_sums,
       "T2 same-day, mean of ratios": tmg_sameday_mean_of_ratios,
       "T3 month-and-weekday 12-hour factor": tmg_average_factor,
       "T4 24/12 ratio times month-and-weekday factor": tmg_split_factor}


# ----- the section's own record: a detector on one approach lane of the section -----
def own_exact_day(c12, di, d24, d12, avail):
    """Golden form: the counted 12 hours times the detector's annual mean day over its own counted-day
    12 hours, the annual mean taken over the days it recorded in full."""
    d24 = np.asarray(d24, dtype=float)
    a = np.asarray(avail, dtype=float)
    full = a >= 100
    return c12 * float(np.nanmean(d24[full])) / float(d12[di])


def own_scaled_partial(c12, di, d24, d12, avail):
    d24 = np.asarray(d24, dtype=float)
    a = np.asarray(avail, dtype=float)
    ok = a > 0
    return c12 * float(np.nanmean(d24[ok] * 100.0 / a[ok])) / float(d12[di])


def own_all_recorded(c12, di, d24, d12, avail):
    d24 = np.asarray(d24, dtype=float)
    a = np.asarray(avail, dtype=float)
    ok = a > 0
    return c12 * float(np.nanmean(d24[ok])) / float(d12[di])


def own_month_weekday(c12, di, d24, d12, avail, holidays=()):
    d = DAYS[di]
    d24 = np.asarray(d24, dtype=float)
    d12 = np.asarray(d12, dtype=float)
    a = np.asarray(avail, dtype=float)
    full = a >= 100
    idx = [i for i, x in enumerate(DAYS) if x.month == d.month and x.weekday() == d.weekday()
           and full[i] and x not in holidays]
    return c12 * float(np.nanmean(d24[full])) / float(np.mean(d12[idx]))


OWN = {"G1 counted day, full days": own_exact_day,
       "G2 counted day, partial days scaled up": own_scaled_partial,
       "G3 counted day, every recorded day as recorded": own_all_recorded,
       "G4 month-and-weekday mean of its 12 hours": own_month_weekday}


def own_group_2412(c12, di, d24, d12, avail, atcs):
    """A rung, not a licensed form: the count taken to 24 hours with the counters' 24/12 ratio and to the
    year with the detector's own 24-hour days, so another road's 12-hour share stands in for the section's."""
    q24 = [np.asarray(a[0], dtype=float) for a in atcs]
    q12 = [np.asarray(a[1], dtype=float) for a in atcs]
    r = sum(np.nansum(x) for x in q24) / sum(np.nansum(x) for x in q12)
    d24 = np.asarray(d24, dtype=float)
    a = np.asarray(avail, dtype=float)
    full = a >= 100
    return c12 * r * float(np.nanmean(d24[full])) / float(d24[di])


def bin01(aadf):
    """Annual traffic in millions of vehicles, unrounded."""
    return aadf * 365.0 / 1e6


def edge(v, unit=0.1):
    """Distance of v from the nearest rounding edge at this unit (positive inside the bin)."""
    return unit / 2.0 - abs(v - round(v / unit) * unit)
