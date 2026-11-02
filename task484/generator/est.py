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


def own_family(c12, di, lanes, holidays=()):
    """Every licensed treatment of the section's own approach detectors, and the zero-filled readings the
    semantic fork table rules out. lanes: list of (d24, d12, avail) arrays, one per lane detector. The approach is
    the lanes summed (a day counts as recorded when every lane recorded it, in full when every lane is at 100), and
    on a two-lane approach each lane alone is read the same ways. Bases: the annual mean over full days, over
    every recorded day as recorded, or over every recorded day scaled up by its availability. Denominators: the
    detectors' own 07:00-19:00 flow on the counted day, or their mean on the same weekday in the same month."""
    d = DAYS[di]
    sets = [("", lanes)]
    if len(lanes) == 2:
        sets += [("lane 1 alone: ", [lanes[0]]), ("lane 2 alone: ", [lanes[1]])]
    forms, zero = {}, {}
    for tag, ls in sets:
        av = np.min([np.asarray(x[2], dtype=float) for x in ls], axis=0)
        d24 = np.sum([np.asarray(x[0], dtype=float) for x in ls], axis=0)
        d12 = np.sum([np.asarray(x[1], dtype=float) for x in ls], axis=0)
        full, rec = av >= 100, av > 0
        bases = {"full days": float(np.mean(d24[full])), "every recorded day as recorded": float(np.mean(d24[rec])),
                 "partial days scaled up": float(np.mean(d24[rec] * 100.0 / av[rec]))}
        idx = [i for i, x in enumerate(DAYS) if x.month == d.month and x.weekday() == d.weekday() and full[i] and x not in holidays]
        dens = {"counted day": float(d12[di]), "month-and-weekday mean": float(np.mean(d12[idx]))}
        for bk, bv in bases.items():
            for dk, dv in dens.items():
                forms["%s%s, %s" % (tag, dk, bk)] = c12 * bv / dv
        zb = float(np.sum(np.where(rec, d24, 0.0)) / len(DAYS))
        for dk, dv in dens.items():
            zero["%szero-filled blanks, %s" % (tag, dk)] = c12 * zb / dv
    named = {"G1 counted day, full days": forms["counted day, full days"],
             "G2 counted day, partial days scaled up": forms["counted day, partial days scaled up"],
             "G3 counted day, every recorded day as recorded": forms["counted day, every recorded day as recorded"],
             "G4 month-and-weekday mean of its 12 hours": forms["month-and-weekday mean, full days"]}
    for k, v in forms.items():
        if k not in ("counted day, full days", "counted day, partial days scaled up",
                     "counted day, every recorded day as recorded", "month-and-weekday mean, full days"):
            named["G" + ("6 " if k.startswith("lane") else "4 ") + k] = v
    return named, zero
