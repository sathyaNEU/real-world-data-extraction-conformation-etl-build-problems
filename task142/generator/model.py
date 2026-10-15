"""The quarter's visit distribution and the booking, on plain arrays (used by world.py to place the capacity return
and by calc.py on the shipped bundle). A member's requirement for 1 January to 31 March 2027 is the visits its
admitted HITH patients receive on the quarter's days; admissions arrive at random at the plan's daily rates and each
stays for a length drawn from the stream's stays on file, so the quarter's total is a compound Poisson count whose
distribution is computed exactly (FFT of the generating function) on the integer visits."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K


def window_visits(stream, off, L, W):
    """Visits inside day 0..W of the window for a stay of L home days admitted at offset off (days from the window's
    first day; negative before it). Vectorised over off and L."""
    off = np.asarray(off)
    L = np.asarray(L)
    lo = np.maximum(off, 0)
    hi = np.minimum(off + L - 1, W)
    nd = np.clip(hi - lo + 1, 0, None)
    if stream == "H06":
        # visits on days k = 0, 2, 4 ... of the stay, k = t - off
        first = np.where((lo - off) % 2 == 0, lo, lo + 1)
        return np.where(hi >= first, (hi - first) // 2 + 1, 0)
    if stream == "H08":
        # two visits on stay days 0 and 1
        extra = np.clip(np.minimum(off + 1, hi) - np.maximum(off, lo) + 1, 0, None)
        return np.where(nd > 0, nd + extra, 0)
    return nd


def stream_mix(stream, rates, offs, pool, W, kmax):
    """Expected count of admissions with k window visits, k = 0..kmax, for one stream: sum over admission days of the
    day's rate times the share of the pool's stays giving k visits."""
    pool = np.asarray(pool)
    out = np.zeros(kmax + 1)
    if len(pool) == 0:
        return out
    vals, cnt = np.unique(pool, return_counts=True)
    p = cnt / cnt.sum()
    for lam, o in zip(rates, offs):
        if lam <= 0:
            continue
        v = window_visits(stream, np.full(len(vals), o), vals, W)
        np.add.at(out, v, lam * p)
    return out


def compound(mix, size=1 << 13):
    """The pmf of a compound Poisson total whose admissions with k visits arrive at expected count mix[k]."""
    lam = mix.sum()
    f = np.zeros(size)
    f[:len(mix)] = mix
    F = np.fft.rfft(f)
    G = np.exp(F - lam)
    g = np.fft.irfft(G, n=size)
    g = np.clip(g, 0, None)
    return g / g.sum()


def quantile(pmf, q=0.9):
    c = np.cumsum(pmf)
    return int(np.searchsorted(c, q - 1e-12))


def daily_rates(adm_month, a, b):
    """Daily admission rates from a to b (both included), flat within each month at the month's admissions over its
    days; adm_month maps a month's first day to its admissions."""
    out = []
    for d in K.days(a, b):
        m0 = d.replace(day=1)
        n = adm_month.get(m0, 0.0)
        out.append(n / K.month_end(d).day)
    return np.array(out)


def quarter_mix(plan_adm, pools, start=dt.date(2026, 10, 1), window=(K.Q0, K.Q1), kmax=200, fixed=None):
    """The window-visit mix of every stream of one member. plan_adm[stream] maps month starts to admissions; pools
    maps a stream to its stays (home days)."""
    W = (window[1] - window[0]).days
    dd = K.days(start, window[1])
    offs = np.array([(d - window[0]).days for d in dd])
    mix = np.zeros(kmax + 1)
    mean = 0.0
    for s in K.STREAMS:
        if s not in plan_adm:
            continue
        r = daily_rates(plan_adm[s], start, window[1])
        if r.sum() == 0:
            continue
        m = stream_mix(s, r, offs, pools[s], W, kmax)
        mix += m
        mean += (np.arange(kmax + 1) * m).sum()
    return mix, mean


def requirement(plan_adm, pools, plan_visits, start=dt.date(2026, 10, 1), recentre=True):
    """The 90th percentile of the quarter's requirement: exact compound distribution, recentred on the plan's visits
    (Schedule 2 clause 2.5) unless recentre is False. Returns (requirement, p90, mean, sd)."""
    mix, mean = quarter_mix(plan_adm, pools, start=start)
    pmf = compound(mix)
    x = np.arange(len(pmf))
    m = (x * pmf).sum()
    sd = math.sqrt(((x - m) ** 2 * pmf).sum())
    p90 = quantile(pmf)
    req = p90 + (plan_visits - m) if recentre else float(p90)
    return req, p90, m, sd


def book(reqs, capacity, order=None, block=K.BLOCK):
    """Schedule 2 clauses 2.6 and 2.7: each member's lots, taken in order until the block is used."""
    order = order or K.MEMBERS
    left = block // K.LOT
    need, got = {}, {}
    for m in order:
        n = K.lots_for(reqs[m] - capacity[m])
        need[m] = n
        take = min(n, left)
        got[m] = take
        left -= take
    return {m: got[m] * K.LOT for m in order}, need, left * K.LOT
