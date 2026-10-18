"""The regional ozone field (ppb) at the analysers and the node sites, hourly UTC."""
import datetime as dt
import math
import numpy as np
import params as P

HOURS = int((P.END - P.START).total_seconds() // 3600) + 1


def hour(i):
    return P.START + dt.timedelta(hours=int(i))


def index(t):
    return int((t - P.START).total_seconds() // 3600)


def field(sites, seed=P.SEED, exposure=None):
    """True ozone (ppb) at each (x, y) km site, one row per site, one column per UTC hour. exposure: per site, the
    share of the night's surface-layer loss the site escapes (0 on the plain, about 0.7 on a hill above it)."""
    rng = np.random.default_rng(seed)
    n = len(sites)
    t = np.arange(HOURS)
    doy = (t / 24.0) % 365.25
    level = 33.0 + 13.0 * np.sin(2 * np.pi * (doy - 105) / 365.25)
    season = np.clip(np.sin(2 * np.pi * (doy - 75) / 365.25), 0, None)
    amp = 7.0 + 15.0 * season
    nd = HOURS // 24 + 2
    dayf = np.zeros(nd)
    z = rng.standard_normal(nd)
    for d in range(1, nd):
        dayf[d] = 0.6 * dayf[d - 1] + 0.8 * z[d]
    dayfac = np.exp(0.22 * dayf)[t // 24]
    shape = np.sin(2 * np.pi * (((t + 1) % 24) - 9) / 24.0)
    shape = np.where(shape > 0, shape, 0.55 * shape)
    a = math.exp(-1.0 / P.SYN_TAU_H)
    syn = np.zeros(HOURS)
    zz = rng.standard_normal(HOURS)
    for h in range(1, HOURS):
        syn[h] = a * syn[h - 1] + math.sqrt(1 - a * a) * zz[h]
    regional = level + amp * dayfac * shape + 6.5 * syn
    xy = np.array(sites, float)
    d = np.sqrt(((xy[:, None, :] - xy[None, :, :]) ** 2).sum(-1))
    resid = np.zeros((n, HOURS))
    for sd, L, phi in P.RESID:
        Lc = np.linalg.cholesky(np.exp(-d / L) + 1e-9 * np.eye(n))
        e = np.zeros((n, HOURS))
        w = rng.standard_normal((n, HOURS))
        s = math.sqrt(1 - phi ** 2)
        for h in range(1, HOURS):
            e[:, h] = phi * e[:, h - 1] + s * (Lc @ w[:, h])
        mixed = np.clip(np.sin(2 * np.pi * (((t + 1) % 24) - 9) / 24.0), 0, None)   # the convective afternoon
        resid += (sd * (0.75 + 0.45 * season) * (1.2 - 0.75 * mixed))[None, :] * e
    # the night's surface layer: ozone lost to deposition and titration under the inversion, deepest on clear calm nights
    nz = rng.standard_normal(nd)
    calm = np.clip(1.0 + 0.65 * nz, 0.05, 2.6)[t // 24]
    night = np.clip(-np.sin(2 * np.pi * (((t + 1) % 24) - 9) / 24.0), 0, None) ** 0.8
    loss = (9.0 + 9.0 * season) * calm * night
    ex = np.zeros(n) if exposure is None else np.asarray(exposure, float)
    return np.clip(regional[None, :] + resid - (1.0 - ex)[:, None] * loss[None, :], 0.5, None)
