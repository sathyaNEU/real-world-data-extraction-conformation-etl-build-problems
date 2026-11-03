"""The ladder on the clean truth: the hybrid's yield effect under each route a solver takes.

    python3 task401/generator/ladder.py [seed ...]
"""
import sys

import numpy as np

import world as WD


def fit(rows, feats, fe):
    keys = list(feats(rows[0]).keys())
    if fe == "farm+year":
        a = sorted({d["yard"] for d in rows}); b = sorted({d["season"] for d in rows})[1:]
        def dum(d):
            return [1.0 * (d["yard"] == x) for x in a] + [1.0 * (d["season"] == x) for x in b]
    else:
        g = sorted({(d["yard"], d["season"]) for d in rows}); ix = {x: i for i, x in enumerate(g)}
        def dum(d):
            v = [0.0] * len(g); v[ix[(d["yard"], d["season"])]] = 1.0; return v
    X = np.array([[feats(d)[k] for k in keys] + dum(d) for d in rows])
    beta, *_ = np.linalg.lstsq(X, np.log([d["yield_bu"] for d in rows]), rcond=None)
    return float(np.expm1(beta[keys.index("hybrid")]))


def routes(T):
    W, rows = T["weather"], T["rows"]
    def w(d):
        return W[(d["season"], d["station"])]
    def season(d):
        x = w(d); y = d["season"]
        a, b = WD.doy(y, 5, 1) - 1, WD.doy(y, 8, 31)
        tm = (x["tmax"][a:b] + x["tmin"][a:b]) / 2
        return dict(hybrid=d["hybrid"], gdd=float(np.maximum(tm - 5, 0).sum()) / 100,
                    edd=float(np.maximum(x["tmax"][a:b] - 29.5, 0).sum()), ljun=float(np.log(max(d["june_mm"], 5))))
    def flower(thr=29.5, days=18, tt=520.0):
        def f(d):
            x = w(d); fl = WD.first_flower(x, d["seed_doy"], tt)
            return dict(hybrid=d["hybrid"], heat=WD.heat_in_flower(x, fl, days, thr), ljun=float(np.log(max(d["june_mm"], 5))))
        return f
    o = {}
    h = [d["yield_bu"] for d in rows if d["season"] == 2026 and d["hybrid"]]
    i = [d["yield_bu"] for d in rows if d["season"] == 2026 and not d["hybrid"]]
    o["raw_2026"] = np.mean(h) / np.mean(i) - 1
    o["season_panel"] = fit(rows, season, "farm+year")
    o["farm_by_year"] = fit(rows, lambda d: dict(hybrid=d["hybrid"]), "farmxyear")
    o["season_plus_seed_lin"] = fit(rows, lambda d: dict(season(d), sd=d["seed_doy"]), "farm+year")
    o["farmyear_plus_seed_lin"] = fit(rows, lambda d: dict(hybrid=d["hybrid"], sd=d["seed_doy"]), "farmxyear")
    o["golden"] = fit(rows, flower(), "farm+year")
    for nm, kw in (("thr28", dict(thr=28.0)), ("thr31", dict(thr=31.0)), ("days14", dict(days=14)), ("days22", dict(days=22)),
                   ("tt490", dict(tt=490.0)), ("tt550", dict(tt=550.0))):
        o["g_" + nm] = fit(rows, flower(**kw), "farm+year")
    o["g_farmxyear"] = fit(rows, lambda d: dict(flower()(d)), "farmxyear")
    def wk(d):
        return (d["seed_doy"] - WD.doy(d["season"], 5, 1)) // 7
    weeks = sorted({(d["season"], wk(d)) for d in rows})[1:]
    o["season_plus_seed_weeks"] = fit(rows, lambda d: dict(season(d), **{"w%d_%d" % k: 1.0 * ((d["season"], wk(d)) == k) for k in weeks}), "farm+year")
    def spl(d):
        z = (d["seed_doy"] - WD.doy(d["season"], 5, 1)) / 10.0
        v = dict(hybrid=d["hybrid"])
        for yy in sorted({e["season"] for e in rows}):
            on = 1.0 * (d["season"] == yy)
            v.update({"s1_%d" % yy: on * z, "s2_%d" % yy: on * z * z, "s3_%d" % yy: on * z ** 3})
        return v
    o["seed_spline_by_season"] = fit(rows, spl, "farm+year")
    # flowering overlap with the heat wave under the window variants, 2026
    h0 = WD.doy(*WD.HEAT_WAVE_START); h1 = h0 + WD.HEAT_WAVE_DAYS
    r26 = [d for d in rows if d["season"] == 2026]
    for nm, base, tt, days in (("b5_520_18", 5, 520, 18), ("b5_480_14", 5, 480, 14), ("b5_600_24", 5, 600, 24), ("b0_900_18", 0, 900, 18)):
        ov = {0: [], 1: []}
        for d in r26:
            x = w(d); tm = (x["tmax"] + x["tmin"]) / 2; g = np.maximum(tm - base, 0)
            c = np.cumsum(g[d["seed_doy"]:]); fl = d["seed_doy"] + 1 + int(np.searchsorted(c, tt))
            ov[d["hybrid"]].append(max(0, min(fl + days, h1) - max(fl, h0)))
        o["ovl_" + nm] = "inc%.1f/hyb%.1f" % (np.mean(ov[0]), np.mean(ov[1]))
    cells = {}
    for d in rows:
        if d["season"] == 2026:
            cells.setdefault((d["yard"], d["seed_doy"] // 3), [[], []])[d["hybrid"]].append(d["yield_bu"])
    num = den = 0
    for inc, hy in cells.values():
        if inc and hy:
            num += len(hy) * (np.mean(hy) / np.mean(inc) - 1); den += len(hy)
    o["match_same_days"] = num / den if den else float("nan")
    o["n_match_hybrid"] = den
    r26 = [d for d in rows if d["season"] == 2026]
    o["n_canola_2026"] = len(r26); o["n_hybrid_2026"] = sum(d["hybrid"] for d in r26)
    o["seed_gap_days"] = float(np.median([d["seed_doy"] for d in r26 if d["hybrid"]]) - np.median([d["seed_doy"] for d in r26 if not d["hybrid"]]))
    return o


if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [WD.SEED]
    for s in seeds:
        o = routes(WD.build(s))
        print(s, " ".join("%s=%s" % (k, ("%.3f" % v) if isinstance(v, float) else v) for k, v in o.items()))
