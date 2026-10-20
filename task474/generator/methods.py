"""The estimators, working on daily totals: {station: {class or 'ALL': {date: volume}}} for the stations (the
classifying ones carry every class) and {link: {class: {date: volume}}} for the two count days of each link.

golden   each class expanded with factors computed for that class at the classifying stations
textbook the count's total expanded with all-vehicle factors from every station, split by the counted class shares
raw      the count's daily mean times the year
month    all-vehicle monthly factors only, split by the counted shares
"""
import numpy as np

import world as W


def _factors(series, how="cell", aadt="mean"):
    """{(month, weekday): factor} from one station's {date: volume}: the station's AADT over the average volume of
    that month's days of that weekday."""
    days = sorted(series)
    vals = np.array([series[d] for d in days])
    if aadt == "aashto":
        cells = {}
        for d, v in zip(days, vals):
            cells.setdefault((d.month, d.weekday()), []).append(v)
        mean = np.mean([np.mean(v) for v in cells.values()])
    else:
        mean = vals.mean()
    out = {}
    if how == "cell":
        cells = {}
        for d, v in zip(days, vals):
            cells.setdefault((d.month, d.weekday()), []).append(v)
        for k, v in cells.items():
            out[k] = mean / np.mean(v)
    else:                                       # separate monthly and weekday factors, multiplied
        mo, wd = {}, {}
        for d, v in zip(days, vals):
            mo.setdefault(d.month, []).append(v)
            wd.setdefault(d.weekday(), []).append(v)
        for m in mo:
            for w in wd:
                out[(m, w)] = (mean / np.mean(mo[m])) * (mean / np.mean(wd[w]))
    return out


def group_factors(stations, key, how="cell", aadt="mean"):
    fs = [_factors(s[key], how, aadt) for s in stations]
    return {k: float(np.mean([f[k] for f in fs])) for k in fs[0]}


def _sep(stations, key):
    """({month: factor}, {weekday: factor}) averaged over the stations."""
    mo, wd = [], []
    for s in stations:
        ser = s[key]
        mean = np.mean(list(ser.values()))
        m, w = {}, {}
        for d, v in ser.items():
            m.setdefault(d.month, []).append(v)
            w.setdefault(d.weekday(), []).append(v)
        mo.append({k: mean / np.mean(v) for k, v in m.items()})
        wd.append({k: mean / np.mean(v) for k, v in w.items()})
    return ({k: float(np.mean([x[k] for x in mo])) for k in mo[0]}, {k: float(np.mean([x[k] for x in wd])) for k in wd[0]})


def estimate(stations, register, counts, route="golden", how="cell", aadt="mean", car_from="classifying",
             links_type=None):
    """{link: {class: AADT}}. links_type ({link: road type}) groups the stations by road type."""
    if links_type:
        out = {}
        for rt in sorted(set(links_type.values())):
            st = {k: v for k, v in stations.items() if register[k]["road"].lower() == rt}
            cn = {k: v for k, v in counts.items() if links_type[k] == rt}
            out.update(estimate(st, register, cn, route, how, aadt, car_from))
        return out
    cls = [stations[s] for s in sorted(stations) if register[s]["classifies"]]
    every = [{"ALL": s["ALL"]} for s in (stations[k] for k in sorted(stations))]
    out = {}
    if route in ("classdow", "classmonth"):
        am, aw = _sep(every, "ALL")
        for k, cnt in counts.items():
            out[k] = {}
            for c in W.CLASSES:
                cm, cw = _sep(cls, c)
                mf, wf = (am, cw) if route == "classdow" else (cm, aw)
                out[k][c] = float(np.mean([v * mf[d.month] * wf[d.weekday()] for d, v in cnt[c].items()]))
        return out
    if route == "golden":
        F = {c: group_factors(cls, c, how, aadt) for c in W.CLASSES}
        if car_from == "all":
            F["P"] = group_factors(every, "ALL", how, aadt)
        for k, cnt in counts.items():
            out[k] = {c: float(np.mean([v * F[c][(d.month, d.weekday())] for d, v in cnt[c].items()]))
                      for c in W.CLASSES}
        return out
    FA = group_factors(every, "ALL", how, aadt)
    for k, cnt in counts.items():
        tot = {d: sum(cnt[c][d] for c in W.CLASSES) for d in cnt["P"]}
        share = {c: sum(cnt[c].values()) / sum(tot.values()) for c in W.CLASSES}
        if route == "textbook":
            a = float(np.mean([v * FA[(d.month, d.weekday())] for d, v in tot.items()]))
        elif route == "raw":
            a = float(np.mean(list(tot.values())))
        elif route == "month":
            mo = {}
            for s in every:
                for d, v in s["ALL"].items():
                    mo.setdefault(d.month, []).append(v / np.mean(list(s["ALL"].values())))
            mf = {m: 1 / np.mean(v) for m, v in mo.items()}
            a = float(np.mean([v * mf[d.month] for d, v in tot.items()]))
        out[k] = {c: a * share[c] for c in W.CLASSES}
    return out


def nox(est):
    return {k: sum(v[c] * len(W.DAYS) * W.EF[c] for c in W.CLASSES) / 1e6 for k, v in est.items()}


def designated(rate):
    return sorted(k for k, v in rate.items() if v >= W.LINE)


def access(est, counts, gates, roads, how="mean_ratio", col="in"):
    """Replaces the combination trucks' AADT on the terminal access roads ({link: terminal}) with the count expanded
    by the terminal's own gate activity: each count day's combination trucks times the terminal's average daily
    visits over the year over its visits that day. gates is {terminal: {date: (in, out)}}."""
    out = {k: dict(v) for k, v in est.items()}
    pick = {"in": lambda p: p[0], "out": lambda p: p[1], "both": lambda p: (p[0] + p[1]) / 2}[col]
    for k, t in roads.items():
        g = {d: pick(p) for d, p in gates[t].items()}
        mean = float(np.mean(list(g.values())))
        days = sorted(counts[k]["CU"])
        if how == "mean_ratio":
            out[k]["CU"] = float(np.mean([counts[k]["CU"][d] * mean / g[d] for d in days]))
        else:
            out[k]["CU"] = sum(counts[k]["CU"][d] for d in days) * mean / sum(g[d] for d in days)
    return out
