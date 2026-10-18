"""The forecast methods, the golden family and the routes a solver takes, on two-way hourly arrays.

Inputs are plain arrays so that checks.py can run them on the clean truth and verify.py on what it reads back
from the bundle: flows[code][year] -> days x 24 (NaN where the counter recorded nothing), days[year] -> dates,
weather (dict date -> (tmax, rain_mm)), caps[code], cycleways {cw: [codes]}.
"""
import math

import numpy as np

H_WINDOW = list(range(6, 22))
WET_MM = 1.0                     # a wet day: 1.0 mm of rain or more
YEARS = [2024, 2025, 2026]


def daygroup(d, dt, scheme):
    if scheme == "wkwe":
        return "we" if dt == "we" else "wk"
    if scheme == "dt3":
        return dt
    if scheme == "all":
        return "all"
    if scheme == "dow":
        return "we" if dt == "we" else ("d%d" % d.weekday())
    if scheme == "dow_term":
        return "we" if dt == "we" else ("d%d_%s" % (d.weekday(), dt))
    raise ValueError(scheme)


PERIODS = {"early": [6], "am": [7, 8, 9], "mid": [10, 11, 12, 13, 14, 15], "pm": [16, 17, 18], "eve": [19, 20, 21],
           "night": [0, 1, 2, 3, 4, 5, 22, 23]}


def _design(tmax, rain, spec):
    wet = 1.0 if rain >= WET_MM else 0.0
    if spec == "flagT":
        return [wet, tmax - 20.0]
    if spec == "flagTband":
        return [wet, float(tmax < 17), float(17 <= tmax < 20), float(23 <= tmax < 26), float(tmax >= 26)]
    if spec == "flagT2":
        return [wet, tmax - 20.0, (tmax - 20.0) ** 2]
    if spec == "mmT":
        return [min(rain, 25.0), tmax - 20.0]
    if spec == "anyT":
        return [1.0 if rain > 0 else 0.0, tmax - 20.0]
    if spec == "wetonly":
        return [wet]
    if spec == "Tonly":
        return [tmax - 20.0]
    if spec == "mmonly":
        return [min(rain, 25.0)]
    if spec == "logmmT":
        return [math.log1p(rain), tmax - 20.0]
    if spec == "flagTwetT":
        return [wet, tmax - 20.0, wet * (tmax - 20.0)]
    if spec == "none":
        return []
    raise ValueError(spec)


def fit_growth(series, spec, estimator="ols"):
    """series: list of (year, tmax, rain, value). Returns the annual growth factor exp(beta_year)."""
    X, y = [], []
    for yr, tmax, rain, v in series:
        if v is None or not np.isfinite(v) or v <= 0 or tmax is None:
            continue
        X.append([1.0, yr - 2026] + _design(tmax, rain, spec))
        y.append(v)
    if len(y) < 15:
        return 1.0
    X = np.array(X)
    y = np.array(y, float)
    b, *_ = np.linalg.lstsq(X, np.log(y), rcond=None)
    if estimator == "poisson":
        for _ in range(30):
            mu = np.exp(X @ b)
            z = X @ b + (y - mu) / mu
            XtW = X.T * mu
            b = np.linalg.solve(XtW @ X, XtW @ z)
    return math.exp(b[1])


def _fit(X, y, estimator):
    if len(y) < 15:
        return 1.0
    b, *_ = np.linalg.lstsq(X, np.log(y), rcond=None)
    if estimator == "poisson":
        for _ in range(30):
            mu = np.exp(X @ b)
            z = X @ b + (y - mu) / mu
            XtW = X.T * mu
            b = np.linalg.solve(XtW @ X, XtW @ z)
    return math.exp(b[1])


def cell_growth(flows, days, dts, weather, scheme="wkwe", cells="hour", spec="flagT", estimator="ols", years=YEARS):
    """growth per counter per (day group, hour): dict code -> dict (group, hour) -> factor. A cell's series is every
    day of its group with weather on record and every hour of the cell recorded; the fit is log riders on year and the
    weather terms (fit_growth's model, vectorised over counters)."""
    if cells == "hour":
        hsets = [[h] for h in range(24)]
    elif cells == "period":
        hsets = list(PERIODS.values())
    elif cells == "day":
        hsets = [list(range(24))]
    else:
        raise ValueError(cells)
    lab, Xrows = [], []
    index = []
    for y in years:
        for i, (d, t) in enumerate(zip(days[y], dts[y])):
            w = weather.get(d)
            if w is None or w[0] is None:
                continue
            lab.append(daygroup(d, t, scheme))
            Xrows.append([1.0, y - 2026] + _design(w[0], w[1], spec))
            index.append((y, i))
    lab = np.array(lab)
    Xall = np.array(Xrows)
    groups = sorted(set(lab.tolist()))
    G = {}
    for code, per in flows.items():
        A = np.vstack([per[y][i] for y, i in index])
        G[code] = {}
        for g in groups:
            sel = lab == g
            Xg, Ag = Xall[sel], A[sel]
            for hs in hsets:
                v = Ag[:, hs]
                ok = ~np.isnan(v).any(axis=1)
                tot = v.sum(axis=1)
                ok &= np.nan_to_num(tot, nan=0.0) > 0
                gr = _fit(Xg[ok], tot[ok], estimator)
                for h in hs:
                    G[code][(g, h)] = gr
    return G


def scale_cells(flows, days, dts, G, scheme):
    out = {}
    labs = {y: [daygroup(d, t, scheme) for d, t in zip(days[y], dts[y])] for y in YEARS}
    for code, per in flows.items():
        out[code] = {}
        for y in YEARS:
            fac = np.array([[G[code][(g, h)] for h in range(24)] for g in labs[y]]) ** (2027 - y)
            out[code][y] = per[y] * fac
    return out


def scale_uniform(flows, factor):
    """factor: dict code -> growth, or a float"""
    out = {}
    for code, per in flows.items():
        g = factor[code] if isinstance(factor, dict) else factor
        out[code] = {y: per[y] * g ** (2027 - y) for y in YEARS}
    return out


def crowded_days(scaled, caps, cycleways, years=YEARS):
    """mean over the given summers of the days any counted segment carries more than its capacity in a window hour"""
    out = {}
    for cw, codes in cycleways.items():
        tot = 0
        for y in years:
            c = None
            for code in codes:
                a = scaled[code][y][:, H_WINDOW]
                hit = np.nan_to_num(a, nan=-1.0) > caps[code]
                hit = hit.any(axis=1)
                c = hit if c is None else (c | hit)
            tot += int(c.sum())
        out[cw] = tot / len(years)
    return out


def crowded_by_counter(scaled, caps, codes, y):
    return {code: int((np.nan_to_num(scaled[code][y][:, H_WINDOW], nan=-1.0) > caps[code]).any(axis=1).sum())
            for code in codes}


def total_growth(flows, kind, days=None, dts=None, weather=None, spec="flagT"):
    out = {}
    for code, per in flows.items():
        tot = {y: np.nansum(per[y]) for y in YEARS}
        if kind == "yoy":
            out[code] = tot[2026] / tot[2025]
        elif kind == "cagr":
            out[code] = (tot[2026] / tot[2024]) ** 0.5
        else:
            raise ValueError(kind)
    return out


def golden(flows, days, dts, weather, caps, cycleways, scheme="wkwe", cells="hour", spec="flagT", estimator="ols", years=YEARS):
    G = cell_growth(flows, days, dts, weather, scheme, cells, spec, estimator, years)
    sc = scale_cells(flows, days, dts, G, scheme)
    return crowded_days(sc, caps, cycleways), G, sc


FAMILY = [("wkwe", "hour", "flagT", "ols"), ("wkwe", "hour", "flagT", "poisson"), ("wkwe", "hour", "flagTband", "ols"),
          ("wkwe", "hour", "flagT2", "ols"), ("wkwe", "hour", "mmT", "ols"), ("wkwe", "hour", "anyT", "ols"),
          ("wkwe", "period", "flagT", "ols"), ("wkwe", "period", "flagTband", "ols"),
          ("dt3", "hour", "flagT", "ols"), ("dt3", "hour", "flagT", "poisson"), ("dt3", "hour", "flagTband", "ols"),
          ("dt3", "hour", "flagT2", "ols"), ("dt3", "period", "flagT", "ols"), ("dt3", "period", "flagTband", "ols")]


def routes(flows, days, dts, weather, caps, cycleways):
    """every natural route a solver takes; name -> crowded days by cycleway"""
    R = {}
    G = cell_growth(flows, days, dts, weather, "wkwe", "hour", "flagT", years=[2025, 2026])
    R["golden variant: hour cells, weather, 2025-26 only"] = crowded_days(scale_cells(flows, days, dts, G, "wkwe"), caps, cycleways)
    for name, sch, cells, spec in [("weekday/weekend daily growth, weather-adjusted", "wkwe", "day", "flagT"),
                                   ("term/holiday/weekend daily growth, weather-adjusted", "dt3", "day", "flagT"),
                                   ("each counter's total growth, weather-adjusted", "all", "day", "flagT"),
                                   ("hour cells growth, no weather", "wkwe", "hour", "none"),
                                   ("period cells growth, no weather", "wkwe", "period", "none"),
                                   ("each counter's total growth by regression, no weather", "all", "day", "none")]:
        G = cell_growth(flows, days, dts, weather, sch, cells, spec)
        R[name] = crowded_days(scale_cells(flows, days, dts, G, sch), caps, cycleways)
    yoy = total_growth(flows, "yoy")
    cagr = total_growth(flows, "cagr")
    R["default: 2026 replayed at each counter's 2025-26 total growth"] = crowded_days(scale_uniform(flows, yoy), caps, cycleways, years=[2026])
    R["three summers at each counter's 2025-26 total growth"] = crowded_days(scale_uniform(flows, yoy), caps, cycleways)
    R["three summers at each counter's 2024-26 compound growth"] = crowded_days(scale_uniform(flows, cagr), caps, cycleways)
    head = {}
    for cw, codes in cycleways.items():
        for c in codes:
            head[c] = yoy[codes[0]]
    R["three summers at the headline counter's 2025-26 growth"] = crowded_days(scale_uniform(flows, head), caps, cycleways)
    for u in (1.00, 1.02, 1.03, 1.05, 1.08, 1.10, 1.12, 1.15, 1.18):
        R["three summers at a flat %+.0f%% a year" % ((u - 1) * 100)] = crowded_days(scale_uniform(flows, u), caps, cycleways)
    R["2026 replayed as recorded"] = crowded_days(scale_uniform(flows, 1.0), caps, cycleways, years=[2026])
    G = cell_growth(flows, days, dts, weather, "wkwe", "hour", "flagT")
    R["golden growth, 2026 weather only"] = crowded_days(scale_cells(flows, days, dts, G, "wkwe"), caps, cycleways, years=[2026])
    # peak-hour growth: growth of each day's busiest window hour, by weekday/weekend, with and without weather
    for name, spec in [("daily busiest-hour growth, weather-adjusted", "flagT"), ("daily busiest-hour growth, no weather", "none")]:
        Gp = {}
        for code, per in flows.items():
            Gp[code] = {}
            for g in ("wk", "we"):
                series = []
                for y in YEARS:
                    for i, (d, t) in enumerate(zip(days[y], dts[y])):
                        if daygroup(d, t, "wkwe") != g:
                            continue
                        v = per[y][i, H_WINDOW]
                        if np.isnan(v).any() or d not in weather:
                            continue
                        series.append((y, weather[d][0], weather[d][1], float(v.max())))
                gr = fit_growth(series, spec)
                for h in range(24):
                    Gp[code][(g, h)] = gr
        R[name] = crowded_days(scale_cells(flows, days, dts, Gp, "wkwe"), caps, cycleways)
    # crowded days in the record, carried on a straight line
    rec = {y: crowded_days(scale_uniform(flows, 1.0), caps, cycleways, years=[y]) for y in YEARS}
    R["record's crowded days on a straight line"] = {cw: rec[2026][cw] + (rec[2026][cw] - rec[2024][cw]) / 2.0 for cw in cycleways}
    R["record's crowded days, mean of three summers"] = {cw: np.mean([rec[y][cw] for y in YEARS]) for cw in cycleways}
    return R
