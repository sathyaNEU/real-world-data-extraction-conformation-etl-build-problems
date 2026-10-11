"""Climate-response models fitted bore by bore with numpy alone: the five families of the answer grid and the
single-window rainfall regression of the naive rung. Used by golden.py (on the shipped files) and by the tuning
scratch (on simulated readings); it reads no file itself.

Time is a day number from 1 January 1990. A bore's readings are (day, level) pairs: static manual dips, or
logger daily means where the bore has a logger."""
import datetime as dt
import math

import numpy as np

D0 = dt.date(1990, 1, 1)
SEP26 = (dt.date(2026, 9, 1), dt.date(2026, 9, 30))
CAL_END = dt.date(2022, 7, 3)
MAY15 = dt.date(2015, 5, 1)

GAMMA_N = (1.0, 1.5, 2.0, 3.0, 4.0, 6.0, 8.0, 12.0, 16.0, 20.0)
MEANS = np.geomspace(20.0, 12.0 * 365.25, 40)
EXP_A = np.geomspace(20.0, 12.0 * 365.25, 30)
EXP_DELAY_Y = (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0)
CRD_W_Y = tuple(range(1, 11))
CRD_LAG_M = tuple(range(0, 73, 6))
MA_Y = (1, 3, 5, 8)
TAKE_N = (1.0, 2.0, 3.0)
TAKE_MEANS = np.geomspace(15.0, 1500.0, 15)
F_GRID = np.round(np.arange(0.0, 1.0001, 0.025), 3)


def dnum(day):
    return (day - D0).days


def month_index(day):
    return (day.year - 1990) * 12 + day.month - 1


def conv(x, k):
    n = len(x) + len(k)
    m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(k, m), m)[:len(x)]


def gamma_pdf_bins(n, mean, edges):
    """The gamma(n, mean/n) probability mass in each [edges[i], edges[i+1]) bin (days), by fine quadrature."""
    a = mean / n
    hi = edges[-1]
    t = np.linspace(0.0, hi, int(hi * 4) + 2)[1:]
    pdf = np.exp((n - 1) * np.log(t) - t / a - math.lgamma(n) - n * np.log(a))
    cdf = np.concatenate([[0.0], np.cumsum(pdf) * (t[1] - t[0])])
    tt = np.concatenate([[0.0], t])
    return np.diff(np.interp(edges, tt, cdf))


class Climate:
    """Daily and monthly climate with the regressors each family needs, built once and shared by every bore."""

    def __init__(self, rain, pet, take=None):
        self.rain = np.asarray(rain, float)
        self.pet = np.asarray(pet, float)
        self.nd = len(self.rain)
        days = [D0 + dt.timedelta(days=i) for i in range(self.nd)]
        self.mi = np.array([month_index(x) for x in days])
        self.nm = self.mi[-1] + 1
        self.rain_m = np.bincount(self.mi, self.rain, self.nm)
        self.pet_m = np.bincount(self.mi, self.pet, self.nm)
        self.take = None if take is None else np.asarray(take, float)
        self.take_m = None if take is None else np.bincount(self.mi, self.take, self.nm)
        self._cache = {}
        # a month's model value is set at its middle; daily day numbers of the month starts
        self.month_start = np.array([dnum(dt.date(1990 + m // 12, m % 12 + 1, 1)) for m in range(self.nm)])

    # ---------------------------------------------------------------- kernels
    def kernels(self, family, step):
        key = (family, step)
        if key in self._cache:
            return self._cache[key]
        if step == "daily":
            L = self.nd
            edges_unit = 1.0
        else:
            L = self.nm
            edges_unit = 365.25 / 12.0
        ks, meta = [], []
        if family == "gamma":
            for n in GAMMA_N:
                for m in MEANS:
                    length = int(min(L, (m * 5 + 1500) / edges_unit + 2))
                    edges = np.arange(length + 1) * edges_unit
                    ks.append(gamma_pdf_bins(n, m, edges))
                    meta.append((n, float(m)))
        elif family == "exp":
            for dly in EXP_DELAY_Y:
                for a in EXP_A:
                    length = int(min(L, (dly * 365.25 + a * 6 + 400) / edges_unit + 2))
                    edges = np.arange(length + 1) * edges_unit - dly * 365.25
                    e0 = np.clip(edges, 0, None)
                    ks.append(np.diff(1.0 - np.exp(-e0 / a)))
                    meta.append((dly, float(a)))
        elif family == "take":
            for n in TAKE_N:
                for m in TAKE_MEANS:
                    length = int(min(L, (m * 6 + 200) / edges_unit + 2))
                    edges = np.arange(length + 1) * edges_unit
                    ks.append(gamma_pdf_bins(n, m, edges))
                    meta.append((n, float(m)))
        self._cache[key] = (ks, meta)
        return ks, meta

    def regressors(self, family, step):
        """Convolutions of rainfall and evaporation (or the take) with every kernel of a family:
        arrays (n_kernels, n_times)."""
        key = ("X", family, step)
        if key in self._cache:
            return self._cache[key]
        ks, meta = self.kernels(family, step)
        if family == "take":
            q = self.take if step == "daily" else self.take_m
            X = np.array([conv(q, k) for k in ks], dtype=np.float64)
            out = (X, None, meta)
        else:
            p = self.rain if step == "daily" else self.rain_m
            e = self.pet if step == "daily" else self.pet_m
            pm, em = p.mean(), e.mean()
            XP = np.array([conv(p - pm, k) for k in ks], dtype=np.float64)
            XE = np.array([conv(e - em, k) for k in ks], dtype=np.float64)
            out = (XP, XE, meta)
        self._cache[key] = out
        return out

    def crd(self, step, cal_mean_end):
        """Rainfall departure summed over a window ending a lag before each time: (n_windows, n_times)."""
        key = ("crd", step, cal_mean_end)
        if key in self._cache:
            return self._cache[key]
        if step == "daily":
            p = self.rain
            unit = 365.25 / 12.0
            pbar = p[:cal_mean_end].mean()
        else:
            p = self.rain_m
            unit = 1.0
            pbar = p[:month_index(D0 + dt.timedelta(days=cal_mean_end))].mean()
        c = np.concatenate([[0.0], np.cumsum(p - pbar)])
        T = len(p)
        rows, meta = [], []
        t = np.arange(T)
        for w in CRD_W_Y:
            for lag in CRD_LAG_M:
                hi = t + 1 - int(round(lag * unit))
                lo = hi - int(round(w * 12 * unit))
                ok = lo >= 0
                v = np.where(ok, c[np.clip(hi, 0, T)] - c[np.clip(lo, 0, T)], np.nan)
                rows.append(v)
                meta.append((w, lag))
        out = (np.array(rows), meta)
        self._cache[key] = out
        return out

    def moving_means(self, step):
        key = ("ma", step)
        if key in self._cache:
            return self._cache[key]
        p = self.rain if step == "daily" else self.rain_m
        unit = 365.25 if step == "daily" else 12.0
        c = np.concatenate([[0.0], np.cumsum(p)])
        T = len(p)
        t = np.arange(T)
        rows = []
        for y in MA_Y:
            w = int(round(y * unit))
            lo = t + 1 - w
            ok = lo >= 0
            rows.append(np.where(ok, (c[t + 1] - c[np.clip(lo, 0, T)]) / y, np.nan))   # mm a year
        out = np.array(rows)
        self._cache[key] = out
        return out


# ------------------------------------------------------------------ observations at the model's time step

def at_step(cl, days, levels, step):
    """(time indices, values) for the fit: every reading at its day (daily), or monthly means (monthly)."""
    days = np.asarray(days)
    levels = np.asarray(levels, float)
    if step == "daily":
        return days.astype(int), levels
    mi = np.array([month_index(D0 + dt.timedelta(days=int(x))) for x in days])
    u, inv = np.unique(mi, return_inverse=True)
    vals = np.bincount(inv, levels) / np.bincount(inv)
    return u, vals


def sep_times(cl, step):
    if step == "daily":
        return np.arange(dnum(SEP26[0]), dnum(SEP26[1]) + 1)
    return np.array([month_index(SEP26[0])])


# ------------------------------------------------------------------ fits

def _best_simple(XP, XE, ti, y, f_grid=F_GRID):
    """For every kernel and every evaporation factor, y = c + g (XP - f XE); the least-squares best with g > 0.
    Returns (kernel index, f, g, c, sse)."""
    P = XP[:, ti]
    E = XE[:, ti]
    n = len(y)
    Sy, Syy = y.sum(), (y * y).sum()
    SP, SE = P.sum(1), E.sum(1)
    SPP, SPE, SEE = (P * P).sum(1), (P * E).sum(1), (E * E).sum(1)
    SPy, SEy = P @ y, E @ y
    f = f_grid[None, :]
    Sz = SP[:, None] - f * SE[:, None]
    Szz = SPP[:, None] - 2 * f * SPE[:, None] + f * f * SEE[:, None]
    Szy = SPy[:, None] - f * SEy[:, None]
    vz = Szz - Sz * Sz / n
    cv = Szy - Sz * Sy / n
    g = cv / vz
    sse = (Syy - Sy * Sy / n) - cv * cv / vz
    sse = np.where(g > 0, sse, np.inf)
    k, j = np.unravel_index(np.argmin(sse), sse.shape)
    gg = g[k, j]
    cc = (Sy - gg * Sz[k, j]) / n
    return int(k), float(f_grid[j]), float(gg), float(cc), float(sse[k, j])


def fit_response(cl, family, step, days, levels):
    """Gamma or delayed-exponential response to rainfall less f times evaporation, fitted on the readings given.
    Returns the fitted model's value at every time and the chosen parameters."""
    XP, XE, meta = cl.regressors(family, step)
    ti, y = at_step(cl, days, levels, step)
    k, f, g, c, sse = _best_simple(XP, XE, ti, y)
    model = c + g * (XP[k] - f * XE[k])
    rmse = math.sqrt(sse / len(y))
    return model, dict(kernel=meta[k], f=f, gain=g, rmse=rmse, n_obs=len(y))


def fit_crd(cl, step, days, levels, cal_end_day):
    X, meta = cl.crd(step, cal_end_day)
    ti, y = at_step(cl, days, levels, step)
    best = None
    for k in range(len(meta)):
        x = X[k, ti]
        ok = ~np.isnan(x)
        if ok.sum() < 8:
            continue
        xx, yy = x[ok], y[ok]
        A = np.vstack([np.ones_like(xx), xx]).T
        coef, *_ = np.linalg.lstsq(A, yy, rcond=None)
        if coef[1] <= 0:
            continue
        sse = float(((yy - A @ coef) ** 2).sum()) / ok.sum() * len(y)
        if best is None or sse < best[0]:
            best = (sse, k, coef)
    sse, k, coef = best
    return coef[0] + coef[1] * X[k], dict(window=meta[k], rmse=math.sqrt(sse / len(y)))


def fit_crd_fixed(cl, step, days, levels, cal_end_day, window_y):
    """The single-window rainfall regression (no lag) used for every bore alike. A level cannot fall because more
    rain fell, so a fitted slope below zero is read as no response on that window: the model is then the bore's
    mean level over the readings."""
    X, meta = cl.crd(step, cal_end_day)
    k = meta.index((window_y, 0))
    ti, y = at_step(cl, days, levels, step)
    x = X[k, ti]
    ok = ~np.isnan(x)
    A = np.vstack([np.ones(ok.sum()), x[ok]]).T
    coef, *_ = np.linalg.lstsq(A, y[ok], rcond=None)
    if coef[1] <= 0:
        return np.full(X.shape[1], float(y[ok].mean())), dict(window=(window_y, 0), slope=0.0, raw_slope=float(coef[1]))
    return coef[0] + coef[1] * X[k], dict(window=(window_y, 0), slope=float(coef[1]), raw_slope=float(coef[1]))


def fit_ma(cl, step, days, levels):
    X = cl.moving_means(step)
    ti, y = at_step(cl, days, levels, step)
    x = X[:, ti]
    ok = ~np.isnan(x).any(0)
    A = np.vstack([np.ones(ok.sum())] + [x[i, ok] for i in range(len(MA_Y))]).T
    coef, *_ = np.linalg.lstsq(A, y[ok], rcond=None)
    model = coef[0] + coef[1:] @ X
    rmse = math.sqrt(float(((y[ok] - A @ coef) ** 2).mean()))
    return model, dict(coef=[float(c) for c in coef], rmse=rmse)


def fit_full(cl, step, days, levels, f_grid=F_GRID[::2]):
    """Full record (to September 2026) with the take as a second stress: y = c + g (XP - f XE) - h (S q).
    Returns the climate-and-constant part, the take term and the parameters."""
    XP, XE, meta = cl.regressors("gamma", step)
    S, _, tmeta = cl.regressors("take", step)
    ti, y = at_step(cl, days, levels, step)
    P, E, Q = XP[:, ti], XE[:, ti], S[:, ti]
    n = len(y)
    best = (np.inf, None)
    SP, SE, SQ, Sy = P.sum(1), E.sum(1), Q.sum(1), y.sum()
    PP, PE, EE = (P * P).sum(1), (P * E).sum(1), (E * E).sum(1)
    PQ, EQ, QQ = P @ Q.T, E @ Q.T, (Q * Q).sum(1)
    Py, Ey, Qy, yy = P @ y, E @ y, Q @ y, (y * y).sum()
    for f in f_grid:
        Sz = SP - f * SE
        zz = PP - 2 * f * PE + f * f * EE
        zq = PQ - f * EQ                      # (kernels, take kernels)
        zy = Py - f * Ey
        # centred normal equations for [z, q]
        a = zz[:, None] - Sz[:, None] ** 2 / n
        b = zq - Sz[:, None] * SQ[None, :] / n
        cq = QQ[None, :] - SQ[None, :] ** 2 / n
        ry = zy[:, None] - Sz[:, None] * Sy / n
        rq = Qy[None, :] - SQ[None, :] * Sy / n
        det = a * cq - b * b
        g = (ry * cq - b * rq) / det
        h = (a * rq - b * ry) / det
        sse = (yy - Sy * Sy / n) - (g * ry + h * rq)
        sse = np.where((g > 0) & (h < 0), sse, np.inf)
        k, j = np.unravel_index(np.argmin(sse), sse.shape)
        if sse[k, j] < best[0]:
            c0 = (Sy - g[k, j] * Sz[k] - h[k, j] * SQ[j]) / n
            best = (float(sse[k, j]), (k, j, float(f), float(g[k, j]), float(h[k, j]), float(c0)))
    sse, (k, j, f, g, h, c0) = best
    clim = c0 + g * (XP[k] - f * XE[k])
    take_term = -h * S[j]
    return clim, take_term, dict(kernel=meta[k], take_kernel=tmeta[j], f=f, rmse=math.sqrt(sse / n))


def sep_value(cl, series, step):
    return float(np.mean(series[sep_times(cl, step)]))
