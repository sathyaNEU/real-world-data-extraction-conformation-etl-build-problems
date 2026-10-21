"""task178 world: the Port Tessaly gauge's water level as it happened, before any system records it.

The astronomical tide (harmonic constants for a Gulf of Maine harbour), the weather surge (seasonal storm climate with
named storms on the record's real storm dates), a surge-dependent advance of the tide (tide-surge interaction), mean
sea level rising 2.4 mm a year with year-to-year anomalies. Everything here is metres relative to the 1983-2001
epoch's mean sea level unless a name says ft."""
from __future__ import annotations

import datetime as dt
from functools import lru_cache

import numpy as np
from scipy.signal import lfilter

import common as C
from tide import predict

CONSTS = {'M2': (1.40, 104), 'S2': (0.22, 140), 'N2': (0.30, 76), 'K2': (0.059, 138), 'K1': (0.14, 200),
          'O1': (0.11, 175), 'P1': (0.045, 198), 'Q1': (0.02, 160), 'L2': (0.04, 120), 'nu2': (0.06, 80),
          'mu2': (0.03, 90), '2N2': (0.04, 48), 'T2': (0.012, 140), 'M4': (0.02, 30), 'MS4': (0.012, 80),
          'MN4': (0.01, 0), 'M6': (0.008, 40), 'Sa': (0.05, 300), 'Ssa': (0.02, 50)}
KAPPA = 0.6                     # hours of tidal advance per metre of surge
MO_SD = np.array([.090, .085, .075, .062, .052, .048, .048, .052, .062, .075, .085, .090])
MO_LAM = np.array([2.5, 2.2, 1.6, 1.0, 0.6, 0.4, 0.4, 0.5, 0.9, 1.6, 2.2, 2.5])
MO_BETA = np.array([.25, .24, .20, .15, .11, .10, .10, .11, .14, .19, .23, .25])
# the record's named storms: (UTC date, peak surge in metres, hours from the nearest predicted high water)
NAMED = [(dt.datetime(2018, 1, 4, 16), 0.741, 0.0),
         (dt.datetime(2018, 3, 2, 14), 0.674, -0.4),
         (dt.datetime(2022, 12, 23, 15), 0.716, 0.3),
         (dt.datetime(2024, 1, 10, 13), 0.560, 0.5),
         (dt.datetime(2024, 1, 13, 17), 0.830, 0.0),
         (dt.datetime(2019, 12, 2, 16), 0.500, 0.6),
         (dt.datetime(2020, 2, 7, 20), 0.470, -0.6),
         (dt.datetime(2021, 10, 27, 13), 0.520, 0.4),
         (dt.datetime(2017, 10, 30, 12), 0.450, 0.8),
         (dt.datetime(2026, 10, 28, 17), 0.920, -0.2)]

T_START = C.hours(dt.datetime(1994, 12, 1))
T_END = C.hours(dt.datetime(2028, 1, 1))


@lru_cache(None)
def datums():
    """tidal datums of the 1983-2001 epoch from the astronomical tide (metres relative to epoch MSL)"""
    t = np.arange(C.hours(dt.datetime(1983, 1, 1)), C.hours(dt.datetime(2002, 1, 1)), 0.1)
    z = predict(t, CONSTS)
    i = np.where((z[1:-1] > z[:-2]) & (z[1:-1] >= z[2:]))[0] + 1
    j = np.where((z[1:-1] < z[:-2]) & (z[1:-1] <= z[2:]))[0] + 1
    day = np.floor((t + 12 + 5) / 24).astype(int)   # local standard days
    hh = np.full(day.max() - day.min() + 1, -np.inf); np.maximum.at(hh, day[i] - day.min(), z[i])
    ll = np.full(day.max() - day.min() + 1, np.inf); np.minimum.at(ll, day[j] - day.min(), z[j])
    hh, ll = hh[np.isfinite(hh)], ll[np.isfinite(ll)]
    return dict(MHHW=float(hh.mean()), MHW=float(z[i].mean()), MSL=0.0, MLW=float(z[j].mean()), MLLW=float(ll.mean()))


def to_ft_mllw(m):
    return (np.asarray(m) - datums()['MLLW']) / C.FT


@lru_cache(None)
def predicted_hw():
    """every predicted high water 1994-12 to 2027: times (hours since J2000, UTC) and heights (metres)"""
    t = np.arange(T_START, T_END, 0.1)
    p = predict(t, CONSTS)
    k = np.where((p[1:-1] > p[:-2]) & (p[1:-1] >= p[2:]))[0] + 1
    y0, y1, y2 = p[k - 1], p[k], p[k + 1]
    off = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    hl_t = t[k] + off * 0.1
    hl_h = y1 - 0.25 * (y0 - y2) * off
    k2 = np.where((p[1:-1] < p[:-2]) & (p[1:-1] <= p[2:]))[0] + 1
    y0, y1, y2 = p[k2 - 1], p[k2], p[k2 + 1]
    off2 = 0.5 * (y0 - y2) / (y0 - 2 * y1 + y2)
    return hl_t, hl_h, t[k2] + off2 * 0.1, y1 - 0.25 * (y0 - y2) * off2


@lru_cache(None)
def surge_hourly():
    """hourly weather surge (metres), the storm climate plus the named storms"""
    rng = C.stream("surge")
    th = np.arange(T_START, T_END + 2, 1.0)
    base = np.datetime64('2000-01-01T12:00')
    d = base + (th * 3600).astype('timedelta64[s]')
    mo = d.astype('datetime64[M]').astype(int) % 12
    yr = d.astype('datetime64[Y]').astype(int) + 1970
    phi = np.exp(-1 / 12.0)
    e = rng.standard_normal(len(th)) * np.sqrt(1 - phi ** 2)
    s = lfilter([1.0], [1.0, -phi], e) * MO_SD[mo]
    years = np.unique(yr)
    mult = {int(y): float(np.exp(rng.normal(0, 0.3))) for y in years}
    ym = d.astype('datetime64[M]')
    for m in np.unique(ym):
        idx = np.where(ym == m)[0]
        mm = int(m.astype(int) % 12)
        k = rng.poisson(MO_LAM[mm] * mult[int(m.astype('datetime64[Y]').astype(int) + 1970)])
        for _ in range(k):
            c = th[idx[0]] + rng.uniform(0, len(idx))
            if rng.uniform() < 0.85:
                pk = 0.08 + rng.exponential(MO_BETA[mm])
                pk = min(pk, 0.48)          # the record's unnamed storms stay below the named ones
            else:
                pk = -(0.05 + rng.exponential(0.12))
            w = rng.uniform(5, 12)
            lo, hi = max(0, int(c - th[0] - 4 * w)), min(len(th), int(c - th[0] + 4 * w))
            s[lo:hi] += pk * np.exp(-0.5 * ((th[lo:hi] - c) / w) ** 2)
    hw_t, hw_h, _, _ = predicted_hw()
    for when, pk, lag in NAMED:
        h = C.hours(when)
        c = hw_t[np.argmin(np.abs(hw_t - h))] + lag
        w = 9.0
        lo, hi = int(c - th[0] - 4 * w), int(c - th[0] + 4 * w)
        # remove whatever the climate put there, then the storm
        s[lo:hi] = s[lo:hi] * 0.3 + pk * np.exp(-0.5 * ((th[lo:hi] - c) / w) ** 2)
    return th, s


@lru_cache(None)
def msl_anomaly():
    rng = C.stream("msl")
    Y = np.arange(1990, 2031)
    a = np.zeros(len(Y))
    for i in range(1, len(Y)):
        a[i] = 0.5 * a[i - 1] + rng.normal(0, 0.015)
    return Y, a


def msl(t):
    yrf = 2000.0 + (np.asarray(t) - 0.0) / (24 * 365.25) + 0.0
    Y, a = msl_anomaly()
    return C.SLR * (yrf - C.EPOCH_MID) + np.interp(yrf, Y + 0.5, a)


def surge(t):
    th, s = surge_hourly()
    return np.interp(t, th, s)


def level(t, noise=None):
    """the water level (metres, epoch MSL) at times t (hours since J2000, UTC)"""
    t = np.asarray(t, float)
    S = surge(t)
    out = predict(t + KAPPA * S, CONSTS) + S + msl(t)
    if noise is not None:
        out = out + noise
    return out


def grid(start, end, step_min):
    a, b = C.hours(start), C.hours(end)
    return np.arange(a, b - 1e-9, step_min / 60.0)


@lru_cache(None)
def true_15min():
    t = grid(C.REC_START, C.VER_END, 15)
    rng = C.stream("noise15")
    return t, level(t, rng.normal(0, 0.006, len(t)))


@lru_cache(None)
def true_6min():
    t = grid(C.TEL_START, C.TEL_END, 6)
    rng = C.stream("noise6")
    return t, level(t, rng.normal(0, 0.006, len(t)))


@lru_cache(None)
def true_hourly_board():
    t = grid(C.BOARD_START, C.TEL_END, 60)
    rng = C.stream("board")
    # the float well damps the level a little (a 6-minute lag)
    return t, level(t - 0.1, rng.normal(0, 0.006, len(t)))


def annual_msl_ft():
    """annual mean sea level at the gauge (ft MLLW) from the true 15-minute record, 1995-2025"""
    t, z = true_15min()
    base = np.datetime64('2000-01-01T12:00')
    yr = (base + (t * 3600).astype('timedelta64[s]')).astype('datetime64[Y]').astype(int) + 1970
    return {int(y): float(to_ft_mllw(z[yr == y].mean())) for y in range(1995, 2026)}
