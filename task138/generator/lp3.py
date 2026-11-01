"""The district standard's frequency method (OLDD-LS-02 section 4): a log-Pearson Type III distribution fitted by
the method of moments on base-10 logarithms of annual peak discharges, the station skew weighted with the regional
skew by their mean square errors. Used by analysis.py; verify.py carries its own implementation."""
import math

import numpy as np
from scipy import stats


def station_skew(y):
    y = np.asarray(y, float)
    n = len(y)
    m = y.mean()
    s = y.std(ddof=1)
    return n * np.sum((y - m) ** 3) / ((n - 1) * (n - 2) * s ** 3)


def mse_station_skew(g, n):
    ag = abs(g)
    a = -0.33 + 0.08 * ag if ag <= 0.90 else -0.52 + 0.30 * ag
    b = 0.94 - 0.26 * ag if ag <= 1.50 else 0.55
    return 10 ** (a - b * math.log10(n / 10.0))


def weighted_skew(g, n, gr, mse_r):
    mg = mse_station_skew(g, n)
    return (mse_r * g + mg * gr) / (mse_r + mg)


def fit(q, gr, mse_r):
    y = np.log10(np.asarray(q, float))
    n = len(y)
    m, s = y.mean(), y.std(ddof=1)
    g = station_skew(y)
    gw = weighted_skew(g, n, gr, mse_r)
    return {"n": n, "mean": m, "sd": s, "g": g, "gw": gw}


def quantile(f, aep):
    k = stats.pearson3.ppf(1.0 - aep, f["gw"])
    return 10 ** (f["mean"] + k * f["sd"])


def exceedance(f, q):
    """Annual chance a peak exceeds q under the fitted distribution."""
    z = (math.log10(q) - f["mean"]) / f["sd"]
    return float(stats.pearson3.sf(z, f["gw"]))
