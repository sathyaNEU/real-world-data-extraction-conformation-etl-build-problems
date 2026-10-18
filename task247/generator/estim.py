"""task247 estimators: HotSpots, degree heating weeks, the maximum monthly mean, the refill of cloud gaps and the
routes that correct the near-real-time record by its mean error."""
import numpy as np

import params as P


def mmm_of(clim_monthly):
    """the maximum of a site's twelve monthly mean climatologies"""
    return max(clim_monthly)


def dhw(sst, mmm):
    """daily degree heating weeks: the HotSpots of a degree or more above the maximum monthly mean over the last 84
    days (the day itself included), divided by 7"""
    hs = np.asarray(sst, float) - mmm
    hs = np.where(hs >= P.HS_MIN, hs, 0.0)
    c = np.concatenate([[0.0], np.cumsum(hs)])
    n = len(hs)
    lo = np.maximum(0, np.arange(n) - (P.WINDOW - 1))
    return (c[1:] - c[lo]) / 7.0


def season_max(sst, mmm, in_season):
    return float(dhw(sst, mmm)[in_season].max())


def level(x):
    return "Alert Level 2" if x >= P.AL2 else ("Alert Level 1" if x >= P.AL1 else "below Alert Level 1")


def refill(sst, observed, clim, bias, mode="anomaly"):
    """take the clear-sky bias out of the observed days and fill every other day by straight-line interpolation of the
    anomaly between the observed days either side (mode 'anomaly'); variants interpolate the temperature itself,
    carry the last observed anomaly forward, or take the nearer observed day's anomaly"""
    sst = np.asarray(sst, float)
    obs = np.asarray(observed, bool)
    idx = np.arange(len(sst))
    an = sst - bias - clim
    if mode == "anomaly":
        return clim + np.where(obs, an, np.interp(idx, idx[obs], an[obs]))
    if mode == "pchip":
        from scipy.interpolate import PchipInterpolator
        return clim + np.where(obs, an, PchipInterpolator(idx[obs], an[obs])(idx))
    if mode == "temperature":
        v = sst - bias
        return np.where(obs, v, np.interp(idx, idx[obs], v[obs]))
    o = idx[obs]
    if mode == "carry":
        k = np.clip(np.searchsorted(o, idx, side="right") - 1, 0, len(o) - 1)
        return clim + np.where(obs, an, an[o[k]])
    if mode == "nearest":
        hi = np.clip(np.searchsorted(o, idx), 0, len(o) - 1)
        lo = np.clip(hi - 1, 0, len(o) - 1)
        pick = np.where(np.abs(idx - o[lo]) <= np.abs(o[hi] - idx), o[lo], o[hi])
        return clim + np.where(obs, an, an[pick])
    raise ValueError(mode)
