"""The rivers: 15-minute discharge, turbidity and true suspended-sediment concentration at each station over 2025 to
2027, and the field team's depth-integrated samples. Sand is entrained only while the river is rising, so the
concentration a unit of turbidity carries is higher on rising water; the glacier rivers rise every summer morning with
the melt and the rain rivers rise at the head of each flood."""
import numpy as np
from scipy.signal import lfilter

import params as P

DT = 0.25                      # hours per step
YRS = 3
N = int(YRS * 365 * 24 / DT)   # 105,120 steps, 1 January 2025 00:00 UTC to 31 December 2027 23:45 UTC
H = np.arange(N) * DT
DOY = (H / 24) % 365
HOD = H % 24
Y27 = slice(int(2 * 365 * 24 / DT), N)
RISE = 0.015                   # the rate of rise (per hour, smoothed over an hour) above which sand moves


def storms(seed=249, per_year=(10, 14)):
    """the regional storm calendar: autumn and summer rain over inner Sogn, shared by every river"""
    rng = np.random.default_rng(seed)
    out = []
    for y in range(YRS):
        n = int(rng.integers(*per_year))
        # storms favour late summer and autumn
        days = np.sort(rng.choice(np.arange(365), n, replace=False, p=_season_weights()))
        for d_ in days:
            out.append(int((y * 365 + d_) * 24 / DT + rng.integers(0, int(24 / DT))))
    out = np.array([t for t in out if 300 <= t < N - 3000])
    return out


def _season_weights():
    doy = np.arange(365)
    w = 0.35 + np.exp(-((doy - 255) / 45.0) ** 2) + 0.5 * np.exp(-((doy - 200) / 30.0) ** 2)
    return w / w.sum()


def station(seed, kind, sand, crew_lag, crew_sd, n_callouts, routine_hour=11.0, winter_routine=True,
            rounds_per_month=1, area=40.0, calendar=None):
    rng = np.random.default_rng(seed)
    base = area * rng.uniform(0.06, 0.10)
    melt_amp = rng.uniform(1.7, 2.3)
    q = np.full(N, base) * (1 + 1.4 * np.exp(-((DOY - 165) / 32) ** 2))
    if kind == "glacier":
        melt = np.clip(np.sin(np.pi * (DOY - 145) / 125), 0, None)
        diel = 0.5 * (1 + np.cos(2 * np.pi * (HOD - 17.0) / 24))
        q = q * (1 + melt_amp * melt * (0.25 + 0.75 * diel))
    starts = []
    for t0 in calendar:
        if rng.uniform() > 0.88:
            continue
        t0 = int(t0 + rng.integers(0, int(3 / DT)))
        pk = base * rng.uniform(3, 15) * (0.6 if kind == "lake" else 1.0)
        r = int(rng.uniform(5, 16) / DT) * (3 if kind == "lake" else 1)
        f = int(rng.uniform(30, 80) / DT) * (2 if kind == "lake" else 1)
        seg = np.r_[pk * np.linspace(0, 1, r) ** 1.6, pk * np.exp(-np.linspace(0, 4, f))]
        q[t0:t0 + len(seg)] += seg[:N - t0]
        starts.append(t0)
    starts = np.array(starts)
    q = q * np.exp(np.convolve(rng.normal(0, 0.004, N), np.ones(8) / 8, "same"))
    rate = np.gradient(q) / DT / q
    rate_s = np.convolve(rate, np.ones(4) / 4, "same")
    rising = rate_s > RISE
    ar = lfilter([1.0], [1.0, -0.92], rng.normal(0, 0.10 * np.sqrt(1 - 0.92 ** 2), N))
    T = 2.0 * (q / base) ** 1.1 * np.exp(ar + rng.normal(0, 0.03, N))
    ssc = 1.5 * (1 + sand * rising) * T
    idx, src, trip = [], [], []
    for m in range(YRS * 12):
        mon = m % 12
        if not winter_routine and mon in (11, 0, 1, 2):
            continue
        for j in range(rounds_per_month):
            lo = 2 + j * 28 / rounds_per_month
            k = int((int(m * 30.42 + rng.uniform(lo, lo + 24 / rounds_per_month)) * 24 + routine_hour
                     + rng.normal(0, 1.4)) / DT)
            if 0 <= k < N:
                idx.append(k); src.append("routine"); trip.append(-1)
    for t0 in starts[rng.permutation(len(starts))[:n_callouts * YRS]]:
        k = t0 + int(max(0.5, rng.normal(crew_lag, crew_sd)) / DT)
        for extra in (0.0, rng.uniform(1.5, 3.0)):
            kk = k + int(extra / DT)
            if 0 <= kk < N:
                idx.append(kk); src.append("callout"); trip.append(int(t0))
    idx = np.array(idx); src = np.array(src); trip = np.array(trip)
    o = np.argsort(idx)
    idx, src, trip = idx[o], src[o], trip[o]
    s = ssc[idx] * rng.lognormal(0, 0.06, len(idx))
    return dict(q=q, T=T, ssc=ssc, rate_s=rate_s, rising=rising, idx=idx, src=src, trip=trip, s=s, base=base,
                starts=starts)


def published_discharge(q):
    """the hydrometry system publishes discharge to three significant figures"""
    ex = np.floor(np.log10(q)) - 2
    return np.round(q / 10 ** ex) * 10 ** ex


def world():
    W = {}
    cal = storms()
    for key in P.KEYS:
        kind, sand, lag, sd, nco, hour, winter, extra = P.SPEC[key]
        d = station(P.SEED[key], kind, sand, lag, sd, nco, routine_hour=hour, winter_routine=winter,
                    area=P.AREA[key], calendar=cal, **extra)
        c = P.TSCALE[key] / 2.0
        d["T"] = d["T"] * c
        d["ssc"] = d["ssc"] * c
        d["s"] = d["s"] * c
        d["qp"] = published_discharge(d["q"])
        d["kind"], d["sand"] = kind, sand
        W[key] = d
    return W
