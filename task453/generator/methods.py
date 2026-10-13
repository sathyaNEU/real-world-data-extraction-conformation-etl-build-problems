"""Seasonal adjustment of a region's monthly payroll jobs, January 2021 to March 2027, and the trigger's test: the
seasonally adjusted average of January to March 2027 against the unadjusted average of the twelve months of 2026.

The step-aware family estimates the seasonal pattern with the January 2026 change of placement removed as a level
shift (or the history restated to the new placement, or the pattern taken from the months before the change); the
default family estimates it across the change."""
import numpy as np
import pandas as pd

from stl import stl

BREAK = "2026-01"


class Frame:
    def __init__(self, months):
        self.months = list(months)
        self.n = len(self.months)
        self.t = np.arange(self.n)
        self.mo = np.array([int(m[5:7]) for m in self.months])
        self.yr = np.array([int(m[:4]) for m in self.months])
        self.brk = self.months.index(BREAK) if BREAK in self.months else self.n
        self.q1 = self.yr == 2027
        self.y26 = self.yr == 2026
        self.q1_26 = (self.yr == 2026) & (self.mo <= 3)


def pct(F, sa, y):
    """per cent: the quarter's seasonally adjusted average against 2026's unadjusted average"""
    return 100.0 * (sa[F.q1].mean() / y[F.y26].mean() - 1.0)


def classical(F, lv, mult=True):
    """the classical decomposition: a centred 2x12 moving average, each month's mean ratio (or difference) to it,
    normalised; returned as log factors (mult) or level factors"""
    y = np.exp(lv) if mult else lv
    s = pd.Series(y)
    tr = (0.5 * s.shift(6) + sum(s.shift(k) for k in range(-5, 6)) + 0.5 * s.shift(-6)) / 12.0
    d = (s / tr) if mult else (s - tr)
    pos = np.arange(F.n) % 12
    f = d.groupby(pos).mean().reindex(range(12)).values
    f = f / f.mean() if mult else f - f.mean()
    return np.log(f[pos]) if mult else f[pos]


def regression(F, lv, knots_every=12, start=0):
    """log jobs on month effects, a trend with a knot every `knots_every` months and a level shift from January 2026;
    returns the centred month effects for every month and the level shift"""
    M = np.zeros((F.n, 12))
    M[F.t, F.mo - 1] = 1.0
    knots = [np.maximum(0, F.t - k) for k in range(knots_every, F.n, knots_every)]
    X = np.column_stack([M, F.t, (F.t >= F.brk).astype(float)] + knots)
    use = F.t >= start
    b, *_ = np.linalg.lstsq(X[use], lv[use], rcond=None)
    eff = b[:12] - b[:12].mean()
    return eff[F.mo - 1], b[13]


def pre_factors(F, se_pre):
    """the last year's factors before the change, carried to every month"""
    pre = F.t < F.brk
    f = np.zeros(12)
    f[F.mo[pre][-12:] - 1] = se_pre[-12:]
    return f[F.mo - 1]


GOLDEN = ("reg12", "reg24", "reg12_2023", "ls_stl", "ls_stl13", "ls_classical", "pre_stl", "pre_classical",
          "splice_stl", "annual_ratio_stl", "q1_ratio_stl", "ls_stl_robust")
DEFAULT = ("stl", "stl_levels", "classical", "classical_additive")
OTHER = ("stl13", "stl_robust", "yoy")


def all_methods(F, y):
    """every route's per cent for one region's series y (jobs, unrounded or whole)"""
    y = np.asarray(y, dtype=float)
    lv = np.log(y)
    r = {}
    sf, ls = regression(F, lv)
    lk = lv + np.where(F.t < F.brk, ls, 0.0)
    pre = F.t < F.brk
    r["reg12"] = pct(F, np.exp(lv - sf), y)
    r["reg24"] = pct(F, np.exp(lv - regression(F, lv, 24)[0]), y)
    r["reg12_2023"] = pct(F, np.exp(lv - regression(F, lv, 12, start=24)[0]), y)
    r["ls_stl"] = pct(F, np.exp(lv - stl(lk)[0]), y)
    r["ls_stl13"] = pct(F, np.exp(lv - stl(lk, seasonal=13)[0]), y)
    r["ls_classical"] = pct(F, np.exp(lv - classical(F, lk)), y)
    r["pre_stl"] = pct(F, np.exp(lv - pre_factors(F, stl(lv[pre])[0])), y)
    r["pre_classical"] = pct(F, np.exp(lv - pre_factors(F, _classical_pre(F, lv))), y)
    sp = lv[F.brk] - lv[F.brk - 1]
    r["splice_stl"] = pct(F, np.exp(lv - stl(lv + np.where(pre, sp, 0.0))[0]), y)
    ar = np.log(y[F.yr == 2026].mean() / y[F.yr == 2025].mean())
    r["annual_ratio_stl"] = pct(F, np.exp(lv - stl(lv + np.where(pre, ar, 0.0))[0]), y)
    q = np.log(y[(F.yr == 2026) & (F.mo <= 3)].mean() / y[(F.yr == 2025) & (F.mo <= 3)].mean())
    r["q1_ratio_stl"] = pct(F, np.exp(lv - stl(lv + np.where(pre, q, 0.0))[0]), y)
    r["ls_stl_robust"] = pct(F, np.exp(lv - stl(lk, robust=True)[0]), y)
    r["stl"] = pct(F, np.exp(lv - stl(lv)[0]), y)
    r["stl_levels"] = pct(F, y - stl(y)[0], y)
    r["classical"] = pct(F, np.exp(lv - classical(F, lv)), y)
    r["classical_additive"] = pct(F, y - classical(F, y, mult=False), y)
    r["stl13"] = pct(F, np.exp(lv - stl(lv, seasonal=13)[0]), y)
    r["stl_robust"] = pct(F, np.exp(lv - stl(lv, robust=True)[0]), y)
    r["yoy"] = 100.0 * (np.mean(y[F.q1] / y[F.q1_26]) - 1.0)
    r["level_shift"] = 100.0 * (np.exp(ls) - 1.0)
    return r


def _classical_pre(F, lv):
    """the classical factors estimated on the months before the change"""
    pre = F.t < F.brk
    G = Frame(F.months[:F.brk])
    return classical(G, lv[pre])
