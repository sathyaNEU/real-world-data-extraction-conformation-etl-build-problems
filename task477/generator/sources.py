"""The clean truth: every county's industries, month by month jobs and quarter by quarter pay for the work done, and
the wages each payroll schedule pays out in each quarter under the calendar (the record counts wages in the quarter
they are paid). Nothing here knows about files or mess."""
import datetime as dt
import functools

import numpy as np

import world as W

QUARTERS = [(y, q) for y in range(W.Y0, W.Y1 + 1) for q in range(1, 5)]
KEYS = ["FA", "FB", "TA", "TB"]           # the effective biweekly phases a weekly payroll splits into


def holidays(y):
    """Federal holidays observed in year y (a Saturday holiday on the Friday before, a Sunday one on the Monday after)."""
    def nth(month, weekday, n):
        d = dt.date(y, month, 1)
        d += dt.timedelta((weekday - d.weekday()) % 7)
        return d + dt.timedelta(7 * (n - 1))

    def last(month, weekday):
        d = dt.date(y, month + 1, 1) - dt.timedelta(1)
        return d - dt.timedelta((d.weekday() - weekday) % 7)
    fixed = [(1, 1), (7, 4), (11, 11), (12, 25)] + ([(6, 19)] if y >= 2021 else [])
    out = set()
    for m, d in fixed:
        x = dt.date(y, m, d)
        out.add(x - dt.timedelta(1) if x.weekday() == 5 else x + dt.timedelta(1) if x.weekday() == 6 else x)
    out |= {nth(1, 0, 3), nth(2, 0, 3), last(5, 0), nth(9, 0, 1), nth(10, 0, 2), nth(11, 3, 4)}
    return out


@functools.lru_cache(None)
def _hol():
    s = set()
    for y in range(W.Y0 - 1, W.Y1 + 3):
        s |= holidays(y)
    return frozenset(s)


def paid_on(d):
    """A pay date on a weekend or holiday is paid on the business day before."""
    h = _hol()
    while d.weekday() >= 5 or d in h:
        d -= dt.timedelta(1)
    return d


def qof(d):
    return (d.year, (d.month - 1) // 3 + 1)


@functools.lru_cache(None)
def paydays(key):
    """Every scheduled pay date of a schedule from late 2011 to early 2027 with the date it is actually paid."""
    kind, wd, anchor = W.SCHEDULES[key]
    out = []
    if kind in ("weekly", "biweekly"):
        step = 7 if kind == "weekly" else 14
        d = anchor or (dt.date(2021, 1, 1) + dt.timedelta((wd - 4) % 7))
        while d > dt.date(W.Y0 - 1, 11, 1):
            d -= dt.timedelta(step)
        while d < dt.date(W.Y1 + 1, 3, 1):
            out.append((d, paid_on(d)))
            d += dt.timedelta(step)
    else:
        for y in range(W.Y0 - 1, W.Y1 + 2):
            for m in range(1, 13):
                end = (dt.date(y, m + 1, 1) if m < 12 else dt.date(y + 1, 1, 1)) - dt.timedelta(1)
                for d in ([dt.date(y, m, 15), end] if kind == "semimonthly" else [end]):
                    out.append((d, paid_on(d)))
    return tuple(out)


@functools.lru_cache(None)
def counts(key):
    """Pay dates actually paid in each quarter."""
    c = {}
    for _, p in paydays(key):
        c[qof(p)] = c.get(qof(p), 0) + 1
    return c


def days(y, q):
    a = dt.date(y, 3 * q - 2, 1)
    b = dt.date(y, 3 * q + 1, 1) if q < 4 else dt.date(y + 1, 1, 1)
    return (b - a).days


def ydays(y):
    return (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days


# what one pay date pays, in days of work
PERIOD = {"weekly": 7, "biweekly": 14, "semimonthly": 365.25 / 24, "monthly": 365.25 / 12}


def paid_factor(sched_mix, y, q):
    """Wages paid in the quarter over the quarter's pay for the work done, for a payroll with this schedule mix."""
    f = 0.0
    for k, s in sched_mix.items():
        kind = W.SCHEDULES[k][0]
        f += s * counts(k).get((y, q), 0) * PERIOD[kind] / days(y, q)
    return f


def effective(sched_mix):
    """The schedule mix as shares on the four biweekly phases (a weekly payroll is half on each phase of its weekday)."""
    e = dict.fromkeys(KEYS, 0.0)
    for k, s in sched_mix.items():
        if k == "WF":
            e["FA"] += s / 2
            e["FB"] += s / 2
        elif k == "WT":
            e["TA"] += s / 2
            e["TB"] += s / 2
        elif k in e:
            e[k] += s
    return e


def series(rng, fips, scale, profile):
    """One county's industries: {child: dict(sector, mix, jobs {(y,m)}, earned {(y,q)}, paid {(y,q)}, estabs {(y,q)})}."""
    out = {}
    for sec, (title, jobs, wage, g, eg, kids) in profile.items():
        sec_noise = rng.normal(0, 1)
        for code, share, rel, smix in kids:
            j0 = jobs * share * scale * float(np.exp(rng.normal(0, .08)))
            if j0 < 4:
                continue
            w0 = wage * rel * float(np.exp(rng.normal(0, .03)))
            gg = np.log1p(g + W.ADJ.get(sec, 0.0) if fips == W.COUNTY_FIPS else g) / 4 + rng.normal(0, .0025)
            eseas = rng.normal(0, .025, 12)
            pseas = rng.normal(0, .012, 4)
            covid = {(2020, 4): -.14, (2020, 5): -.11, (2020, 6): -.07, (2020, 7): -.05, (2020, 8): -.04,
                     (2020, 9): -.03, (2020, 10): -.025, (2020, 11): -.02, (2020, 12): -.02}
            hit = abs(rng.normal(1.0, .35)) * (1.8 if sec in ("72", "71", "81", "44-45", "56") else .7)
            jobs_m = {}
            for y in range(W.Y0, W.Y1 + 1):
                for m in range(1, 13):
                    t = (y - W.BASE) + (m - .5) / 12
                    v = j0 * np.exp(eg * (t - 4.5) + eseas[m - 1] + hit * covid.get((y, m), 0) + rng.normal(0, .006))
                    jobs_m[(y, m)] = max(1, int(round(v)))
            earned, paid = {}, {}
            ar = 0.0
            for (y, q) in QUARTERS:
                t = (y - W.BASE) + (q - .5) / 4
                ar = .5 * ar + rng.normal(0, .007)
                comp = .05 * hit if (y, q) in ((2020, 2), (2020, 3)) else (.02 * hit if (y, q) == (2020, 4) else 0)
                wk = w0 * np.exp(gg * t + pseas[q - 1] + ar + comp + .002 * sec_noise)
                jq = sum(jobs_m[(y, m)] for m in range(3 * q - 2, 3 * q + 1)) / 3
                e = jq * wk * days(y, q) / 7
                earned[(y, q)] = e
                paid[(y, q)] = e * paid_factor(smix, y, q)
            est = max(1, int(round(j0 / rng.uniform(6, 30))))
            estabs = {k: max(1, est + int(rng.integers(-1, 2)) + int((k[0] - W.Y0) * rng.uniform(0, .6)))
                      for k in QUARTERS}
            out[code] = dict(sector=sec, mix=smix, jobs=jobs_m, earned=earned, paid=paid, estabs=estabs)
    return out


def tallis(rng):
    return series(rng, W.COUNTY_FIPS, 1.0, W.SECTORS)


def other_profile(rng):
    """Another county draws its own schedule mixes and growth around the state's industry structure."""
    prof = {}
    opts = [W.SECTORS[s][5][0][3] for s in W.SECTORS] + [{"FA": .5, "FB": .5}, {"SM": .6, "FB": .4},
                                                          {"WF": .5, "FA": .5}, {"TA": .4, "FB": .6}]
    for sec, (title, jobs, wage, g, eg, kids) in W.SECTORS.items():
        nk = []
        for code, share, rel, smix in kids:
            pick = opts[int(rng.integers(0, len(opts)))] if rng.random() < .5 else smix
            nk.append((code, share, rel, pick))
        prof[sec] = (title, jobs, wage * float(np.exp(rng.normal(-.05, .08))), g + rng.normal(0, .02),
                     eg + rng.normal(0, .006), nk)
    return prof
