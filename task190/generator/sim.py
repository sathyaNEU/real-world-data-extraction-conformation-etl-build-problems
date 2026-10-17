"""The capital programme payment population, and the monetary-unit selection run on it.

Every line amount is strictly positive and the cumulative book value is monotone, asserted: three
classes summing above a programme's non-certificate value once made it otherwise, and the lattice
was then reading an impossible record.
"""
import bisect
import datetime as dt
import math

import world as W


def shash(text):
    """A deterministic string hash: Python's own is salted per process."""
    h = 2166136261
    for ch in text:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h


class Rng(object):
    def __init__(self, seed):
        self.s = (seed * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)

    def next(self):
        self.s = (self.s * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return (self.s >> 11) & ((1 << 53) - 1)

    def u(self):
        return self.next() / float(1 << 53)

    def below(self, n):
        return self.next() % n if n else 0

    def pick(self, seq):
        return seq[self.below(len(seq))]


def dates(lo, hi):
    a = dt.date(*[int(v) for v in lo.split("-")])
    b = dt.date(*[int(v) for v in hi.split("-")])
    out = []
    while a <= b:
        if a.weekday() < 5:
            out.append(a)
        a += dt.timedelta(days=1)
    return out


def population(year=W.YEAR, seed=190003, scale=1.0):
    """One row per payment line: programme, amount, class, tainting fraction."""
    rng = Rng(seed if year == W.YEAR else seed + 7717)
    vol = 1.0 if year == W.YEAR else 0.86
    lines = []
    for code, name, value, certs in W.PROGRAMMES:
        value = value * vol
        certs = [c * vol for c in certs]
        rest = value - sum(certs)
        assert rest > 0, code
        dwv, intv = rest * W.DW_SHARE, rest * W.INT_SHARE
        sunv = rest - dwv - intv
        dwmean = W.DAYWORK_MEAN[code]
        ndw = max(20, int(round(dwv / dwmean)))
        dw = [dwmean * (0.42 + 1.35 * rng.u() ** 0.8) for _ in range(ndw)]
        dw = [x * dwv / sum(dw) for x in dw]
        nint = max(5, int(round(intv / W.INTERIM_MEAN)))
        ints = [W.INTERIM_MEAN * (0.52 + 1.1 * rng.u() ** 0.75) for _ in range(nint)]
        ints = [x * intv / sum(ints) for x in ints]
        nsun = max(50, int(W.LINES[code] * vol) - len(certs) - ndw - nint)
        raw = [(1.0 - rng.u()) ** (-1.0 / 2.3) for _ in range(nsun)]
        cap = W.INTERVAL - 2500.0
        raw = [min(x * sunv / sum(raw), cap) for x in raw]
        raw = [x * sunv / sum(raw) for x in raw]
        for a in certs:
            lines.append([code, round(float(a), 2), "certificate", 0.0])
        for a in dw:
            lines.append([code, round(a, 2), "daywork", 0.0])
        for a in ints:
            lines.append([code, round(min(a, cap), 2), "interim", 0.0])
        for a in raw:
            lines.append([code, round(max(a, 15.0), 2), "sundry", 0.0])
    # the defect: a wrong day-work labour rate on a run of small variation invoices
    byprog = {}
    for L in lines:
        if L[2] == "daywork":
            byprog.setdefault(L[0], []).append(L)
    for code, (cnt, tf) in sorted(W.DEFECT.items()):
        cnt = max(4, int(round(cnt * scale * (1.0 if year == W.YEAR else 0.72))))
        cand = sorted(byprog[code], key=lambda L: (L[1], L[0]))
        step = max(1, len(cand) // cnt)
        taken = 0
        for i in range(0, len(cand), step):
            if taken >= cnt:
                break
            f = (tf + 0.24 * (rng.u() - 0.5)) * W.TAINT_MUL
            cand[i][3] = round(min(1.0, max(0.14, f)), 4)
            taken += 1
    # the ledger's own sequence, which is the order the selection ran on
    rng2 = Rng(770119 if year == W.YEAR else 770119 + 13)
    order = sorted((rng2.next(), i) for i in range(len(lines)))
    out = [lines[i] for _, i in order]
    assert all(x[1] > 0 for x in out), "a line amount went non-positive"
    cum = 0.0
    for x in out:
        cum += x[1]
    assert cum > 0
    return out


def cumulative(lines):
    c = [0.0]
    for L in lines:
        c.append(c[-1] + L[1])
    return c


def select(lines, interval=W.INTERVAL, start=W.RANDOM_START):
    """Monetary-unit selection: the line holding each start + j*interval of cumulated value."""
    cum = cumulative(lines)
    total = cum[-1]
    counts = {}
    j = 0
    while True:
        t = start + j * interval
        if t >= total:
            break
        counts[bisect.bisect_right(cum, t) - 1] = \
            counts.get(bisect.bisect_right(cum, t) - 1, 0) + 1
        j += 1
    return sorted(counts.items()), total, j
