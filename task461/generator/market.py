"""The Midplains Power Market's day-ahead prices, operating day by operating day on Central prevailing time: the
North Hub from 2019 and Redrock Draw's own settlement point from its creation in December 2025. Each day has a level
and a swing (the evening peak over the midday solar trough and the night), set by the season and the day's weather. In a
windy stretch the swing varies more from day to day (more flat days and more sharp ones) while its average holds; the
level eases. The node's prices swing with the hub's, amplified by the congestion between them. Also the hub's
real-time prices and the day-ahead ancillary service clearing prices for 2026."""
import datetime as dt

import numpy as np

import world as W

FIRST = dt.date(2019, 1, 1)
LAST = W.ARCHIVE_PULL


def dst_bounds(year):
    """Second Sunday of March and first Sunday of November."""
    m = dt.date(year, 3, 1)
    spring = m + dt.timedelta(days=(6 - m.weekday()) % 7 + 7)
    n = dt.date(year, 11, 1)
    fall = n + dt.timedelta(days=(6 - n.weekday()) % 7)
    return spring, fall


def day_hours(d):
    """The operating day's hours as (hour ending, repeated flag, local clock hour beginning, UTC offset at the hour)."""
    spring, fall = dst_bounds(d.year)
    out = []
    if d == spring:                      # 2:00 to 3:00 does not exist; hour ending 03 is skipped
        for he in (1, 2):
            out.append((he, False, he - 1, -6))
        for he in range(4, 25):
            out.append((he, False, he - 1, -5))
    elif d == fall:                      # 1:00 to 2:00 happens twice; the second is hour ending 02 repeated
        out.append((1, False, 0, -5))
        out.append((2, False, 1, -5))
        out.append((2, True, 1, -6))
        for he in range(3, 25):
            out.append((he, False, he - 1, -6))
    else:
        off = -5 if spring <= d < fall else -6
        out = [(he, False, he - 1, off) for he in range(1, 25)]
    return out


def hour_start_utc(d, hr):
    """UTC start of an operating-day hour given as (hour ending, repeated, clock, offset)."""
    he, rep, clk, off = hr
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(hours=clk - off)


def ar1(rng, n, phi, sd):
    e = rng.normal(0, sd, n)
    x = np.zeros(n)
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def shape(clock):
    h = clock + 0.5
    return np.exp(-((h - 19.0) / 2.2) ** 2) - 0.6 * np.exp(-((h - 13.0) / 2.8) ** 2) - 0.35 * np.exp(-((h - 3.5) / 2.5) ** 2)


def windiness(d):
    """0 in an ordinary stretch, 1 inside a windy one, ramped over a month at each end."""
    w = 0.0
    for a, b in W.WINDY:
        if a <= d <= b:
            w = max(w, min(1.0, (d - a).days / 30.0, (b - d).days / 30.0))
    return w


def simulate(seed=W.SEED):
    """Per operating day: the hours (hour ending, repeated flag, clock, UTC offset), the hub's and the node's prices."""
    rng = np.random.default_rng(seed)
    days = [FIRST + dt.timedelta(days=k) for k in range((LAST - FIRST).days + 1)]
    nd = len(days)
    doy = np.array([d.timetuple().tm_yday for d in days])
    summ = np.clip(np.cos(2 * np.pi * (doy - 200) / 365), 0, None)
    wint = np.clip(np.cos(2 * np.pi * (doy - 20) / 365), 0, None)
    wd = np.array([windiness(d) for d in days])
    z = ar1(rng, nd, 0.6, 1.0) / 1.25
    g = rng.gamma(1.2, 1.0, nd)
    g = (g - g.mean()) / g.std()
    sig = W.SIG_ORDINARY + (W.SIG_WINDY - W.SIG_ORDINARY) * wd
    lw = sig * (np.sqrt(1 - W.SKEW_MIX) * z + np.sqrt(W.SKEW_MIX) * g)
    wx = np.exp(lw - 0.5 * sig ** 2)
    lvl = 32 + 10 * summ + 6 * wint + 4 * ar1(rng, nd, 0.8, 1.0) - W.LEVEL_WINDY * wd
    swing = 12 * W.SWING_SCALE * (0.7 + 0.8 * summ + 0.2 * wint) * wx
    hub_noise = rng.normal(0, 1.2, (nd, 25))
    node_noise = rng.normal(0, 0.4, (nd, 25))
    crng = np.random.default_rng(seed + 3)            # the congestion's own day-to-day variation
    gain = W.NODE_K * np.exp(crng.normal(0, W.NODE_K_SD, nd) - 0.5 * W.NODE_K_SD ** 2)
    extra = crng.normal(0, 0.9, (nd, 25))
    out = []
    for i, d in enumerate(days):
        hrs = day_hours(d)
        clk = np.array([c for _, _, c, _ in hrs], dtype=float)
        hub = lvl[i] + swing[i] * shape(clk) + hub_noise[i, :len(hrs)]
        node = (hub.mean() + W.NODE_BASIS + gain[i] * (hub - hub.mean()) + node_noise[i, :len(hrs)] +
                extra[i, :len(hrs)])
        out.append(dict(day=d, hours=hrs, hub=np.round(hub, 2), node=np.round(node, 2), windy=wd[i]))
    return out


def tb4(p):
    s = np.sort(np.asarray(p, dtype=float))
    return s[-4:].mean() - s[:4].mean()


def realtime(days, seed=W.SEED + 7):
    """The hub's 2026 real-time prices at fifteen-minute intervals: the day-ahead hour's price with real-time error,
    a few scarcity intervals and the occasional negative run."""
    rng = np.random.default_rng(seed)
    rows = []
    for x in days:
        if x["day"].year != 2026 or x["day"] >= W.ARCHIVE_PULL:   # real-time prices for complete operating days
            continue
        for hr, p in zip(x["hours"], x["hub"]):
            for q in range(4):
                e = rng.normal(0, 2.5 + 0.08 * abs(p))
                if rng.random() < 0.004:
                    e += rng.gamma(2.0, 45.0)
                if rng.random() < 0.006:
                    e -= rng.gamma(2.0, 12.0)
                rows.append((x["day"], hr, q + 1, round(float(p + e), 2)))
    return rows


def ancillary(days, seed=W.SEED + 9):
    """The 2026 day-ahead ancillary service clearing prices (regulation up and down, responsive and non-spinning
    reserve), hourly on the operating day."""
    rng = np.random.default_rng(seed)
    rows = []
    for x in days:
        if x["day"].year != 2026:
            continue
        sw = tb4(x["hub"])
        for hr, p in zip(x["hours"], x["hub"]):
            base = max(0.4, 0.06 * sw + 0.03 * max(p, 0))
            rows.append((x["day"], hr, round(float(base * rng.uniform(0.8, 1.3) + 1.1), 2),
                         round(float(0.6 * base * rng.uniform(0.7, 1.3) + 0.4), 2),
                         round(float(0.8 * base * rng.uniform(0.8, 1.2) + 0.9), 2),
                         round(float(0.35 * base * rng.uniform(0.6, 1.4) + 0.2), 2)))
    return rows
