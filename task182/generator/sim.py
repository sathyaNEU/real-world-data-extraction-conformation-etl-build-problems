"""The simulation behind the pack (never shipped): gridded-style daily climate for the mine's coordinates, the
metered take by source, and each bore's true water level as its response to rainfall less evaporation, less
its response to the take, plus AR(1) noise."""
import datetime as dt
import math

import numpy as np

import world as W

T0 = W.SPINUP
T_END = dt.date(2026, 10, 9)
N = (T_END - T0).days + 1
DATES = np.array([T0 + dt.timedelta(days=i) for i in range(N)])
MONTH = np.array([x.month for x in DATES])
YEAR = np.array([x.year for x in DATES])
WY = np.where(MONTH >= 10, YEAR + 1, YEAR)


def idx(day):
    return (day - T0).days


# ------------------------------------------------------------------ climate

def climate():
    """Daily rainfall and Morton areal potential evapotranspiration (mm), seeded, summer-dominant, each water
    year scaled to its rainfall factor."""
    r = W.rng("climate")
    pre = W.rng("climate-pre-1990")
    factors = {}
    for wy in range(T0.year, T_END.year + 2):
        factors[wy] = W.RAIN_YEAR.get(wy, float(np.clip(pre.normal(1.0, 0.2), 0.55, 1.6)))
    f = np.array([factors[w] for w in WY])
    ndays = np.array([31, 28.25, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
    p_wet = np.array([W.WET_DAYS[m] / ndays[m - 1] for m in MONTH])
    mean_wet = np.array([W.RAIN_MONTH[m] / W.WET_DAYS[m] for m in MONTH])
    wet_season = np.isin(MONTH, [12, 1, 2, 3])
    mf = np.clip(np.where(wet_season, 1 + (f - 1) * 1.25, 1 + (f - 1) * 0.55), 0.15, None)
    u = r.random(N)
    amt = r.gamma(0.75, 1.0 / 0.75, N)
    pw = np.clip(p_wet * np.sqrt(mf), 0, 0.9)
    rain = np.where(u < pw, amt * mean_wet * np.sqrt(mf), 0.0)
    for w in np.unique(WY):
        sel = WY == w
        tot = rain[sel].sum()
        if tot > 0:
            rain[sel] *= f[sel][0] * 580.0 * sel.sum() / 365.25 / tot
    rain = np.round(rain, 1)
    noise = r.normal(0, 1, N).clip(-2.5, 2.5)
    pet = np.array([W.APET_MONTH[m] / ndays[m - 1] for m in MONTH])
    pet = pet * (1 + 0.02 * (1 - f)) * (1 + 0.1 * noise)
    pet = np.where(rain >= 2.0, pet * 0.78, pet)
    pet = np.round(np.clip(pet, 0.5, None), 1)
    tmax = np.array([[0, 33.6, 32.8, 31.6, 29.2, 25.9, 23.1, 22.9, 25.1, 28.6, 31.6, 33.4, 34.1][m] for m in MONTH])
    tmin = np.array([[0, 21.8, 21.4, 19.9, 16.3, 12.4, 9.6, 8.1, 9.4, 12.8, 16.6, 19.3, 20.9][m] for m in MONTH])
    tmax = np.round(tmax + 2.2 * r.normal(0, 1, N) - np.where(rain >= 5, 2.5, 0) + 0.8 * (1 - f), 1)
    tmin = np.round(tmin + 2.0 * r.normal(0, 1, N) + np.where(rain >= 5, 1.0, 0), 1)
    return dict(rain=rain, pet=pet, tmax=tmax, tmin=np.minimum(tmin, tmax - 3.0))


# ------------------------------------------------------------------ the take

def take():
    """Daily metered take by source, ML/day, rising as the pit deepens; {source id: array over DATES}."""
    r = W.rng("take")
    out = {}
    t = np.arange(N)
    for sid, _, start in W.SOURCES:
        s0 = idx(dt.date.fromisoformat(start))
        on = t >= s0
        yrs = np.clip((t - s0) / 365.25, 0, None)
        if sid.startswith("PS"):
            base = (1.9 if sid == "PS1" else 1.2) + 0.55 * yrs
        else:
            base = {"AD01": 0.95, "AD02": 0.85, "AD03": 1.05, "AD04": 0.9}[sid] + 0.12 * yrs
        q = base * (1 + 0.08 * r.normal(0, 1, N))
        down = r.random(N) < (0.03 if sid.startswith("AD") else 0.015)
        q = np.where(down, q * r.uniform(0.0, 0.4, N), q)
        q = np.where(on, np.clip(q, 0, None), 0.0)
        out[sid] = np.round(q, 3)
    return out


# ------------------------------------------------------------------ responses

def gamma_kernel(n, mean_d, length=None):
    a = mean_d / n
    if length is None:
        length = int(min(N - 1, mean_d * 4 + 3000))
    tt = np.arange(length) + 0.5
    k = np.exp((n - 1) * np.log(tt) - tt / a - math.lgamma(n) - n * np.log(a))
    return k / k.sum()


def conv(x, k):
    n = len(x) + len(k)
    m = 1 << (n - 1).bit_length()
    return np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(k, m), m)[:len(x)]


_XG = np.linspace(-14.0, 6.0, 8001)


def hantush_W(u, beta):
    """The leaky-aquifer well function W(u, beta) by quadrature in log space."""
    y = np.exp(_XG)
    integrand = np.exp(-y - beta * beta / (4.0 * y))
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(_XG))])
    tail = cum[-1] - cum          # integral from x to the top of the grid
    x = np.log(np.clip(u, np.exp(_XG[0]), np.exp(_XG[-1])))
    return np.interp(x, _XG, tail)


def take_response(lag_d, leak, total):
    """Unit-normalised Hantush step response (time scale lag_d days, leakage r/B) convolved with the changes in
    the take: drawdown per ML/day of steady take, as a function of time."""
    t = np.arange(1, N + 1, dtype=float)
    steady = hantush_W(np.array([1e-12]), leak)[0]
    step = hantush_W(lag_d / t, leak) / steady
    dq = np.diff(np.concatenate([[0.0], total]))
    return conv(dq, step)


def heads(clim=None, q=None, which=None):
    """True daily water level (m AHD) at every bore, the climate part and the take part separately."""
    clim = clim or climate()
    q = q or take()
    total = sum(q.values())
    sep = slice(idx(dt.date(2026, 9, 1)), idx(dt.date(2026, 9, 30)) + 1)
    out = {}
    for b in W.BORES:
        if which and b["label"] not in which:
            continue
        R = clim["rain"] - b["f"] * clim["pet"]
        c = conv(R - R[:idx(W.CLIMATE_START)].mean(), gamma_kernel(b["n"], b["mean_d"]))
        ref = c[idx(b["base"])] if b["base"] else c[idx(dt.date(2022, 4, 1)):idx(dt.date(2022, 6, 30)) + 1].mean()
        gain = b["clim"] / (ref - c[sep].mean())
        climate_part = gain * c
        if b["dd"] > 0:
            s = take_response(b["lag_d"], b["leak"], total)
            dd = b["dd"] / s[sep].mean() * s
        else:
            dd = np.zeros(N)
        r = W.rng("noise-" + b["label"])
        e = np.empty(N)
        z = r.normal(0, b["sigma"] * math.sqrt(1 - b["phi"] ** 2), N)
        e[0] = r.normal(0, b["sigma"])
        for i in range(1, N):
            e[i] = b["phi"] * e[i - 1] + z[i]
        h0 = climate_part - dd + e
        anchor = idx(b["base"]) if b["base"] else idx(dt.date(2022, 5, 1))
        level = b["gl"] - W.SWL_BGL[b["label"]] + W.SHIFT.get(b["label"], 0.0)
        h = h0 + (level - h0[anchor])
        out[b["label"]] = dict(h=h, climate=climate_part + (level - h0[anchor]), dd=dd, noise=e, gain=gain)
    return out
