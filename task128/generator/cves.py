"""Vulnerability identifiers, their daily exploit scores and the scanner's exploit flag.

A CVE belongs to one upstream package. Its score runs in two phases: a level before its changeover
date and a final level after it. Every changeover falls on or before 21 September 2026, and every
final level sits outside 0.07 to 0.14, so in the last 30 days of the history no score is inside
that band (the C1 convergence of the November reading). No score at any date sits within 0.005 of
the 0.10 line.
"""
import datetime as dt
import math

from params import SCORE_FIRST, SCORE_LAST, CONVERGE_FROM

KINDS = ("X", "N", "XN", "NX")   # final exploitable, final not, crossing down, crossing up


class Cve:
    __slots__ = ("id", "package", "published", "cvss", "flag", "kind", "pre", "final", "change")

    def score_on(self, d, jit):
        lvl = self.pre if d < self.change else self.final
        return round(lvl * jit, 5)


class Registry:
    def __init__(self, rng):
        self.rng = rng
        self.by_id = {}
        self.pool = {}          # (package, kind, yyyymm) -> list of ids already created
        self.used_numbers = set()

    def _new_id(self, year):
        while True:
            n = self.rng.randint(1100, 58999)
            if (year, n) not in self.used_numbers:
                self.used_numbers.add((year, n))
                return f"CVE-{year}-{n}"

    def _levels(self, kind):
        r = self.rng
        lo = lambda a, b: math.exp(r.uniform(math.log(a), math.log(b)))
        if kind == "X":
            pre, final = lo(0.115, 0.85), lo(0.16, 0.94)
        elif kind == "N":
            pre = lo(0.0004, 0.092) if r.random() < 0.8 else r.uniform(0.05, 0.092)
            final = lo(0.0004, 0.064)
        elif kind == "XN":
            pre, final = lo(0.115, 0.42), lo(0.004, 0.062)
        else:
            pre, final = r.uniform(0.02, 0.092), lo(0.16, 0.7)
        return pre, final

    def make(self, package, kind, published, change=None):
        c = Cve()
        c.id = self._new_id(published.year)
        c.package = package
        c.published = published
        c.kind = kind
        c.pre, c.final = self._levels(kind)
        if change is None:
            # non-crossing CVEs drift once, somewhere between publication and 21 September
            a = max(published, SCORE_FIRST)
            b = CONVERGE_FROM - dt.timedelta(days=2)
            span = (b - a).days
            change = a + dt.timedelta(days=self.rng.randint(0, span)) if span > 0 else a
        c.change = change
        r = self.rng
        if kind in ("X", "NX"):
            c.cvss = round(r.uniform(6.5, 9.8), 1)
            c.flag = r.random() < 0.90
        else:
            c.cvss = round(min(9.8, max(3.1, r.gauss(6.4, 1.4))), 1)
            c.flag = r.random() < 0.04
        if kind == "XN":
            c.flag = r.random() < 0.6
        self.by_id[c.id] = c
        return c

    def get(self, package, kind, published, reuse=True, change=None):
        """A CVE of this package and kind published in the same month, reused across estates when one
        exists and is not yet used by the caller, else a new one."""
        key = (package, kind, published.strftime("%Y%m"))
        if reuse and change is None and self.pool.get(key) and self.rng.random() < 0.55:
            return self.by_id[self.rng.choice(self.pool[key])]
        c = self.make(package, kind, published, change)
        self.pool.setdefault(key, []).append(c.id)
        return c


def jitter_series(rng, n):
    """Multiplicative day-to-day jitter, within +-2.5 per cent, as a list of n factors."""
    out, x = [], 1.0
    for _ in range(n):
        x = 0.7 * x + 0.3 * (1.0 + rng.uniform(-0.025, 0.025))
        out.append(x)
    return out


def score_rows(reg, rng):
    """Daily score rows (cve, date, score) from max(published, 1 May) to 22 October."""
    rows = {}
    for cid in sorted(reg.by_id):
        c = reg.by_id[cid]
        d0 = max(c.published, SCORE_FIRST)
        n = (SCORE_LAST - d0).days + 1
        if n <= 0:
            continue
        jit = jitter_series(rng, n)
        series = []
        for k in range(n):
            d = d0 + dt.timedelta(days=k)
            s = c.score_on(d, jit[k])
            # keep clear of the line and of the band, whatever the jitter did
            if c.pre >= 0.10 and d < c.change:
                s = max(s, 0.10501)
            if c.pre < 0.10 and d < c.change:
                s = min(s, 0.09499)
            if d >= c.change:
                if c.final >= 0.10:
                    s = max(s, 0.14101)
                else:
                    s = min(s, 0.06899)
            series.append((d, max(s, 0.00010)))
        rows[cid] = series
    return rows
