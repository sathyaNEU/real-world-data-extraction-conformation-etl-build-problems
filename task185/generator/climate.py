"""The weather the instruments saw, and what each instrument recorded.

A day's true maximum is a seasonal cycle (southern hemisphere, hottest late January), a slow warming and an anomaly
that persists from day to day and runs hotter on its hot side. The glass maximum thermometer in the large wooden
screen read it to the half degree. The electronic probe in the small plastic shield reads the same on ordinary days
and warmer on hot ones, because the small shield heats on still, sunny afternoons: the difference is a function of
the day's maximum, flat on cool days and rising through the hot range. Every site the network compared carries the
same instrument pair, so the same function, plus each instrument's own reading error."""
import datetime as dt

import numpy as np

import world as W


def delta(t):
    """probe minus glass, by the day's true maximum (C)"""
    x = np.asarray(t, float)
    lo, hi = 31.0, 34.5
    s = np.clip((x - lo) / (hi - lo), 0.0, 1.0)
    ramp = 0.05 + 0.65 * (3 * s ** 2 - 2 * s ** 3)
    return np.where(x <= hi, ramp, 0.70 + 0.25 * (x - hi))


def rng(*key):
    return np.random.default_rng([W.SEED] + [int(k) for k in key])


def days_between(d0, d1):
    return [d0 + dt.timedelta(k) for k in range((d1 - d0).days + 1)]


# site: (code, name, station number, mean max, seasonal amplitude, anomaly spread, warming C a year,
#        comparison period start and end)
SITES = [
    ("MF", W.STATION, W.NEW_ID, 21.4, 7.6, 3.3, 0.012, W.CHANGE, W.CHECK_END),
    ("BR", "Barrow Downs", "041318", 23.6, 8.4, 3.6, 0.011, dt.date(1993, 9, 1), dt.date(1998, 8, 31)),
    ("CW", "Coolwater Siding", "042205", 24.9, 8.9, 3.7, 0.012, dt.date(1994, 2, 1), dt.date(1999, 1, 31)),
    ("HG", "Hallgate", "040977", 20.6, 7.2, 3.1, 0.010, dt.date(1994, 6, 1), dt.date(1997, 5, 31)),
    ("PN", "Pinnaroo East", "043112", 25.8, 9.2, 3.8, 0.013, dt.date(1995, 3, 1), dt.date(2000, 2, 29)),
    ("TB", "Tolbin Hill", "041455", 22.3, 7.9, 3.4, 0.012, dt.date(1994, 10, 1), dt.date(1997, 9, 30)),
    ("WK", "Warrick Plains", "042640", 24.2, 8.7, 3.6, 0.011, dt.date(1993, 11, 1), dt.date(1998, 10, 31)),
]


def true_max(site_idx, days):
    _, _, _, mean, amp, spread, warm, _, _ = SITES[site_idx]
    g = rng(1, site_idx)
    n = len(days)
    doy = np.array([d.timetuple().tm_yday for d in days])
    yr = np.array([d.year + (doy_ - 1) / 365.25 for d, doy_ in zip(days, doy)])
    clim = mean + amp * np.cos(2 * np.pi * (doy - 25) / 365.25)
    sd = spread + 1.4 * np.cos(2 * np.pi * (doy - 20) / 365.25)
    e = g.standard_normal(n)
    z = np.empty(n)
    z[0] = e[0]
    phi = 0.62
    for i in range(1, n):
        z[i] = phi * z[i - 1] + np.sqrt(1 - phi ** 2) * e[i]
    skew = np.where(z > 0, 1.18, 0.86)
    return clim + warm * (yr - 1994.0) + sd * z * skew


def glass(site_idx, t):
    g = rng(2, site_idx)
    return np.round((t + 0.12 * g.standard_normal(len(t))) * 2) / 2


def probe(site_idx, t):
    g = rng(3, site_idx)
    return np.round(t + delta(t) + 0.08 * g.standard_normal(len(t)), 1)


def merrin_flat():
    """Merrin Flat's days from the start of the record to the as-of date: true maximum, glass reading (to the end of
    the check readings), probe reading (from the change), minimum temperature."""
    days = days_between(W.RECORD_START, W.RECORD_END)
    t = true_max(0, days)
    gl = glass(0, t)
    pr = probe(0, t)
    g = rng(4, 0)
    tmin = np.round(t - (11.5 + 1.5 * g.standard_normal(len(t))) - 1.8 * np.cos(2 * np.pi * (np.arange(len(t)) % 365) / 365), 1)
    return {"days": days, "true": t, "glass": gl, "probe": pr, "tmin": tmin}


def comparison():
    """Every comparison site's paired days: (site code, date, glass reading, probe reading)."""
    out = []
    for i, site in enumerate(SITES):
        d0, d1 = site[7], site[8]
        days = days_between(dt.date(1964, 7, 1), d1)
        t = true_max(i, days)
        gl, pr = glass(i, t), probe(i, t)
        for k, d in enumerate(days):
            if d0 <= d <= d1:
                out.append((site[0], d, float(gl[k]), float(pr[k])))
    return out
