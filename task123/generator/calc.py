"""The rungs and the golden, computed from the simulated records (the generator's side; verify.py recomputes
the golden from the shipped files alone on its own code path).

Every method splits a bill's therms across the gas days it covers, (start, end], and sums each premise's
January share by county. They differ only in the weight a gas day gets:
  R0 billed month   a bill read in January counts whole, any other not at all
  R1 days           every gas day the same
  R2 month shape    each gas day the mean AMI use of its calendar month
  R3 scale-up       the AMI premises' mean January therms times the county's premises with January service
  R4 daily shape    each gas day the mean AMI use that day (the golden)
"""
from collections import defaultdict
from datetime import timedelta

import numpy as np

import world as W

TD = timedelta


def shape_from_mdms(mdms, stat="mean", pids=None):
    """Per gas day, the mean (or median) CCF over the AMI meters reporting that day."""
    rows = [(d0, ccf) for pid, (d0, ccf, q) in mdms.items() if pids is None or pid in pids]
    if stat == "mean":
        tot = np.zeros(W.NDAY)
        cnt = np.zeros(W.NDAY)
        for d0, ccf in rows:
            ok = np.isfinite(ccf)
            tot[d0:d0 + len(ccf)] += np.where(ok, ccf, 0.0)
            cnt[d0:d0 + len(ccf)] += ok
        w = np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan)
    else:
        M = np.full((len(rows), W.NDAY), np.nan)
        for k, (d0, ccf) in enumerate(rows):
            M[k, d0:d0 + len(ccf)] = ccf
        w = np.nanmedian(M, axis=0)
    return w


def month_shape(w):
    out = np.array(w, dtype=float)
    for y, m in W.MONTHS:
        idx = [i for i, d in enumerate(W.DAYS) if (d.year, d.month) == (y, m)]
        vals = w[idx]
        if np.isfinite(vals).any():
            out[idx] = np.nanmean(vals)
    return out


def jan_share(weights, a, b):
    """Share of the gas days (a, b] that falls in January 2026 under per-day weights."""
    ia, ib = W.IDX[a] + 1, W.IDX[b] + 1
    seg = weights[ia:ib]
    j = W.JAN[ia:ib]
    tot = seg.sum()
    return float(seg[j].sum() / tot) if tot > 0 else 0.0


def touches_jan(bl):
    return bl.end >= W.D(2026, 1, 1) and bl.start < W.D(2026, 1, 31)


def county_jan(bills, w, method):
    """County January therms under one method (R0, R1, R2, R4); every txn line is split like its bill, so
    cancels net their originals."""
    out = defaultdict(float)
    days = np.ones(W.NDAY)
    ms = month_shape(w) if method == "R2" else None
    for bl in bills:
        if method == "R0":
            if bl.end.year == 2026 and bl.end.month == 1:
                out[bl.county] += bl.therms
            continue
        if not touches_jan(bl):
            continue
        wt = {"R1": days, "R2": ms, "R4": w}[method]
        out[bl.county] += bl.therms * jan_share(wt, bl.start, bl.end)
    return dict(out)


def span_jan(bills, w):
    """The golden by another route: each account's bills from its first read on or after 1 November to its
    last read on or before 31 March merged into one span and split by the daily shape."""
    by = defaultdict(list)
    for bl in bills:
        by[(bl.pid, bl.account)].append(bl)
    out = defaultdict(float)
    for (pid, acct), bs in by.items():
        bs = [b for b in bs if b.start >= W.D(2025, 11, 1) and b.end <= W.D(2026, 3, 31)]
        if not bs:
            continue
        a = min(b.start for b in bs)
        e = max(b.end for b in bs)
        tot = sum(b.therms for b in bs)
        if e < W.D(2026, 1, 1) or a >= W.D(2026, 1, 31):
            continue
        out[bs[0].county] += tot * jan_share(w, a, e)
    return dict(out)


def scale_up(bills, prem):
    """R3: the AMI premises' mean January therms times each county's premises with January service."""
    ami_jan = defaultdict(float)
    for bl in bills:
        if bl.basis == "CALENDAR" and bl.end.year == 2026 and bl.end.month == 1:
            ami_jan[bl.pid] += bl.therms
    mean = float(np.mean(list(ami_jan.values())))
    n = defaultdict(int)
    for p in prem:
        n[p.county] += 1
    return {c: mean * n[c] for c in n}, mean


def awards(totals, grant=W.GRANT):
    t = sum(totals.values())
    return {c: grant * totals[c] / t for c in totals}


def rounded(a):
    return {c: int(round(v / 1000.0)) * 1000 for c, v in a.items()}
