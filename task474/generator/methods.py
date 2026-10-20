"""The routes from the conformed hourly record to each combined-cycle unit's ozone-season NOx per gross MWh.

rec: {unit: dict(load, nox, since)} over the season's operating hours, nox None where the analyzers were out.
Every route takes the same record; they differ only in how an hour without a measurement is filled."""
import numpy as np

import world as W


def _arr(r):
    load = np.array(r["load"], float)
    nox = np.array([np.nan if v is None else v for v in r["nox"]], float)
    s = np.array(r["since"], int)
    return load, nox, s


def _fit(x, y, cols):
    X = np.column_stack(cols)
    return np.linalg.lstsq(X, y, rcond=None)[0]


def fill(r, route):
    load, nox, s = _arr(r)
    m = ~np.isnan(nox)
    miss = ~m
    tot = nox[m].sum()
    if route == "record":
        return tot
    if route == "share":
        return tot / load[m].sum() * load.sum()
    if route == "load":
        b = _fit(None, nox[m], [np.ones(m.sum()), load[m], load[m] ** 2])
        return tot + (b[0] + b[1] * load[miss] + b[2] * load[miss] ** 2).sum()
    if route == "rate":
        return tot + (nox[m].sum() / load[m].sum()) * load[miss].sum()
    if route in ("golden", "state_rate", "state4"):
        top = 4 if route == "state4" else 3
        add = 0.0
        for k in range(1, top + 1):
            mk, mi = m & (s == k), miss & (s == k)
            if mi.any():
                if route == "state_rate":
                    add += nox[mk].sum() / load[mk].sum() * load[mi].sum()
                else:
                    add += mi.sum() * nox[mk].mean()
        ms, mis = m & (s > top), miss & (s > top)
        b = _fit(None, nox[ms], [np.ones(ms.sum()), load[ms], load[ms] ** 2])
        return tot + add + (b[0] + b[1] * load[mis] + b[2] * load[mis] ** 2).sum()
    if route == "state_reg":
        d = [(s == k).astype(float) for k in (1, 2, 3)]
        b = _fit(None, nox[m], [np.ones(m.sum()), load[m], load[m] ** 2] + [x[m] for x in d])
        pred = b[0] + b[1] * load + b[2] * load ** 2 + sum(b[3 + i] * d[i] for i in range(3))
        return tot + pred[miss].sum()
    raise KeyError(route)


def rate(r, route):
    return fill(r, route) / np.array(r["load"], float).sum()


FAMILY = ["golden", "state_rate", "state4", "state_reg"]
WRONG = ["record", "share", "load", "rate"]


def designated(rec, route):
    return sorted(u for u in rec if rate(rec[u], route) >= W.TARGET)
