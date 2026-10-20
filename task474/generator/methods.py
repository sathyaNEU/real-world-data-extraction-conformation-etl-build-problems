"""The routes from the conformed hourly record to each combined-cycle unit's ozone-season NOx per gross MWh.

rec: {unit: dict(load, nox, since, heat, air, blocks)} over the season's operating hours, nox None where the analyzers
were out; air marks the hours inside a plant instrument air loss and blocks lists each such run of hours with the NOx
per MMBtu measured in the operating hour before it and the one after it (None where that hour was not measured).
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
    if route == "state":
        route = "golden"
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


def _without_air(r):
    keep = [not a for a in r["air"]]
    return dict(load=[v for v, k in zip(r["load"], keep) if k], nox=[v for v, k in zip(r["nox"], keep) if k],
                since=[v for v, k in zip(r["since"], keep) if k])


def after_rate(r):
    """The unit's NOx per MMBtu in the first measured hour after its air losses, averaged over them (a unit with none
    measured takes its plant's, rec["plant_after"])."""
    v = [b[3] for b in r["blocks"] if b[3] is not None]
    return float(np.mean(v)) if v else None


def fill_air(r, route):
    """The state fill on every other gap, and the hours of each air loss filled by the route."""
    base = {"golden": "golden", "g_event": "golden", "g_state4": "state4", "g_reg": "state_reg", "interp": "golden",
            "air_load": "golden"}[route]
    tot = fill(_without_air(r), base)
    heat = np.array(r["heat"], float)
    if route == "air_load":
        load, nox = np.array(r["load"], float), np.array([np.nan if v is None else v for v in r["nox"]], float)
        m, a = ~np.isnan(nox), np.array(r["air"], bool)
        b = _fit(None, nox[m], [np.ones(m.sum()), load[m], load[m] ** 2])
        return tot + (b[0] + b[1] * load[a] + b[2] * load[a] ** 2).sum()
    u = after_rate(r)
    u = u if u is not None else r.get("plant_after")
    for i0, i1, before, after in r["blocks"]:
        q = heat[i0:i1 + 1].sum()
        if route == "interp":
            v = [x for x in (before, after) if x is not None]
            tot += float(np.mean(v)) * q if v else 0.0
        elif route == "g_event" and after is not None:
            tot += after * q
        else:
            tot += (u or 0.0) * q
    return tot


def rate(r, route):
    if route in AIR_ROUTES:
        return fill_air(r, route) / np.array(r["load"], float).sum()
    return fill(r, route) / np.array(r["load"], float).sum()


AIR_ROUTES = ["golden", "g_event", "g_state4", "g_reg", "interp", "air_load"]
FAMILY = ["golden", "g_event", "g_state4", "g_reg"]
WRONG = ["state", "interp", "air_load", "load", "record", "share", "rate"]


def designated(rec, route):
    return sorted(u for u in rec if rate(rec[u], route) >= W.TARGET)
