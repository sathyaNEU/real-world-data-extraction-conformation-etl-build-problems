"""Fast in-memory estimators (the golden's logic, vectorised) for screening seeds and variants.

    python3 tune.py N        # screen N seeds and print the margins of every graded figure
"""
import datetime as dt
import math
import sys
from collections import defaultdict

import numpy as np
import pandas as pd

import claims as CL
import simulate as SIM
import stores as ST
import world as W


def frame(rows):
    df = pd.DataFrame(rows, columns=["week", "store", "item", "units", "reg", "dp", "ref"])
    return df


def estimators(df, window=13, pool="pooled", depressed=True, gap=1, side="gain"):
    bags = {k: v["bags"] for k, v in W.LINE.items()}
    own = W.OWN
    key = df.set_index(["store", "week", "item"])
    regmap = key["reg"]
    unitmap = key["units"]
    num, den = defaultdict(float), defaultdict(float)
    per = defaultdict(list)
    oln = old = 0.0
    for code, start, item, kind, val, label in W.EVENTS:
        weeks = [start + dt.timedelta(days=7 * k) for k in range(3)]
        pre = [start - dt.timedelta(days=7 * k) for k in range(gap, gap + window)]
        sub = df[(df.item == item) & df.week.isin(pre) & df.dp.isna()]
        base = sub.groupby("store").units.mean()
        pair = own.get(bags[item])
        ev = df[(df.item == item) & df.week.isin(weeks) & df.dp.notna()].copy()
        ev = ev[ev.store.isin(base.index)]
        if pair:
            idx = list(zip(ev.store, ev.week, [pair] * len(ev)))
            olp = regmap.reindex(idx).values
            ev["cross"] = ev.dp.values <= olp + 1e-9
            obase = df[(df.item == pair) & df.week.isin(pre) & df.dp.isna()].groupby("store").units.mean()
            cr = ev[ev.cross]
            if len(cr):
                olu = unitmap.reindex(list(zip(cr.store, cr.week, [pair] * len(cr)))).values
                ob = obase.reindex(cr.store).values
                ok = ~np.isnan(ob)
                oln += float(np.nansum(olu[ok]))
                old += float(np.nansum(ob[ok]))
        else:
            ev["cross"] = False
        nc = ev[~ev.cross]
        if kind != "pct" or not len(nc):
            continue
        u = nc.units.sum()
        b = base.reindex(nc.store).sum()
        num[val] += u
        den[val] += b
        per[val].append(u / b - 1)
    if pool == "pooled":
        pure = {d: num[d] / den[d] - 1 for d in num}
    else:
        pure = {d: float(np.mean(v)) for d, v in per.items()}
    if side == "gain":
        return pure, gain_share(df, pure, window, gap)
    return pure, 1 - oln / old


def gain_share(df, pure, window=13, gap=1):
    """The switch measured on the deal line: its units over base x (1 + pure lift), per own-label base."""
    key = df.set_index(["store", "week", "item"])
    regmap = key["reg"]
    gn = gd = 0.0
    for code, start, item, kind, val, label in W.EVENTS:
        pair = W.OWN.get(W.LINE[item]["bags"])
        if not pair:
            continue
        weeks = [start + dt.timedelta(days=7 * k) for k in range(3)]
        pre = [start - dt.timedelta(days=7 * k) for k in range(gap, gap + window)]
        base = df[(df.item == item) & df.week.isin(pre) & df.dp.isna()].groupby("store").units.mean()
        obase = df[(df.item == pair) & df.week.isin(pre) & df.dp.isna()].groupby("store").units.mean()
        ev = df[(df.item == item) & df.week.isin(weeks) & df.dp.notna()].copy()
        olp = regmap.reindex(list(zip(ev.store, ev.week, [pair] * len(ev)))).values
        ev = ev[(ev.dp.values <= olp + 1e-9) & ev.store.isin(base.index) & ev.store.isin(obase.index)]
        if not len(ev):
            continue
        L = np.array([lift_at(pure, W.depth(r, kind, val)) for r in ev.reg])
        gn += float((ev.units.values - base.reindex(ev.store).values * (1 + L)).sum())
        gd += float(obase.reindex(ev.store).values.sum())
    return gn / gd


# the switch is measured on the deal line (its units over base x (1 + pure lift), per own-label base); the
# own-label loss read one for one ("l13") is the wrong path that lands on half price, and the 26-week window
# reads the previous crossing cycle's depressed own-label weeks into the base
VARIANTS = [("p13", {}), ("p8", {"window": 8}), ("r8", {"window": 8, "gap": 2}), ("p10", {"window": 10}),
            ("m13", {"pool": "mean"}), ("m8", {"window": 8, "pool": "mean"}), ("l13", {"side": "loss"}),
            ("p26", {"window": 26})]
REQUIRED = ["p13", "p8", "r8", "p10", "m13", "m8"]


def battery(df, stores, appb):
    """Every graded Ask A and Ask B figure under each estimator variant."""
    out = {}
    for name, kw in VARIANTS:
        pure, share = estimators(df, **kw)
        out[name] = figures(df, stores, appb, pure, share)
        out[name]["share"] = share
        out[name]["pure"] = pure
    return out


def cells(g):
    c = {}
    for n in ("third", "forty", "half", "off240"):
        c[("chain", n)] = g["chain"][n]
        for r in REGS:
            c[(r, n)] = g["region"][r][n]
    c[("chain", "packs")] = g["packs_forty"]
    for r in REGS:
        c[(r, "packs")] = g["packs_region"][r]
    return c


def report(bat, required=REQUIRED, show=True):
    """Per cell: golden value, its offset from the bin centre, and the worst margin over the required variants."""
    gold = cells(bat["p13"])
    worst = {}
    for k, x in gold.items():
        step = 1000.0 if k[1] == "packs" else 0.1
        cen = round(x / step) * step
        lo, hi = cen - step / 2, cen + step / 2
        vals = [cells(bat[v])[k] for v in required]
        m = min(min(v - lo, hi - v) for v in vals) / step
        p26 = cells(bat["p26"])[k]
        worst[k] = (x, (x - cen) / step, m, lo <= p26 < hi)
        if show:
            print("%-16s %10.4f  off %+.3f  margin %.3f  p26 %s" % ("%s %s" % k, x, (x - cen) / step, m,
                                                                    "in" if lo <= p26 < hi else "OUT"))
    return worst


def lift_at(pure, d):
    pts = sorted([(0.0, 0.0)] + list(pure.items()))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if d <= x1 + 1e-12:
            return y0 + (y1 - y0) * (d - x0) / (x1 - x0)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    return y1 + (y1 - y0) * (d - x1) / (x1 - x0)


def figures(df, stores, appb, pure, share, regmode="event", zero_fill=False, test="store", rrp=3.79):
    weeks = W.BASE_WEEKS
    sub = df[df.week.isin(weeks) & df.dp.isna() & df.item.isin([W.DEL160, W.OL160])]
    if zero_fill:     # a missing store-week read as a week of zero sales (deal weeks still left out)
        on_deal = df[df.week.isin(weeks) & df.dp.notna() & (df.item == W.DEL160)].week.unique()
        expect = len(weeks) - len(on_deal)
        g = sub.groupby(["store", "item"]).units.sum()
        g = g / g.index.get_level_values("item").map(lambda i: expect if i == W.DEL160 else len(weeks))
    else:
        g = sub.groupby(["store", "item"]).units.mean()
    b = g.xs(W.DEL160, level="item")
    o = g.xs(W.OL160, level="item")
    last = df.week.max()
    cur = df[df.week == last].set_index(["store", "item"]).reg
    regof = {}
    for s in stores:
        for w in weeks:
            sid = ST.scan_ids(s, w)
            if sid:
                regof[sid] = {"event": s["reg_event"], "may27": s["reg_may27"],
                              "jan": s["reg_jan"] if not s.get("reissued") else "WNW"}[regmode]
    res = {"chain": {}, "region": defaultdict(dict), "base_region": defaultdict(float), "packs_region": {}}
    rows = []
    for sid in b.index:
        if sid in appb:
            continue
        reg = float(cur[(sid, W.DEL160)])
        olp = float(cur[(sid, W.OL160)])
        r = {"sid": sid, "region": regof[sid], "base": float(b[sid]), "ol": float(o.get(sid, 0.0))}
        for name, kind, val, label in W.MENU:
            dp = W.deal_price(reg, kind, val)
            dpt = val if kind == "pct" else val / reg
            ref = olp if test == "store" else rrp
            r[name] = r["base"] * (1 + lift_at(pure, dpt)) + (share * r["ol"] if dp <= ref + 1e-9 else 0.0)
        rows.append(r)
    t = pd.DataFrame(rows)
    B = t.base.sum()
    res["base_chain"] = B
    for name, *_ in W.MENU:
        res["chain"][name] = t[name].sum() / B
        res["packs_" + name] = 3 * t[name].sum()
    for reg, gg in t.groupby("region"):
        res["base_region"][reg] = gg.base.sum()
        for name, *_ in W.MENU:
            res["region"][reg][name] = gg[name].sum() / gg.base.sum()
        res["packs_region"][reg] = 3 * gg["forty"].sum()
    return res


def margin1(x):      # distance of x from its one-decimal bin edge
    return abs(x * 10 - math.floor(x * 10 + 0.5) - 0.5) / 10 if False else min(
        abs(x - (math.floor(x * 10 - 0.5) + 0.5) / 10), abs(x - (math.floor(x * 10 - 0.5) + 1.5) / 10))


def edge_dist(x, step):
    """Distance from x to the nearest rounding boundary of a grid of width step."""
    k = x / step
    frac = k - math.floor(k)
    return abs(frac - 0.5) * step


def screen(seed_stores, seed_sim, verbose=False):
    stores = ST.build(seed_stores)
    rows, means, truth = SIM.simulate(stores, seed_sim)
    df = frame(rows)
    import build
    err, appb = build.choose_appendix_b(rows, stores, seed_sim)
    appb = set(appb)
    variants = {}
    for vname, kw in [("p13", {}), ("p8", {"window": 8}), ("m13", {"pool": "mean"})]:
        pure, share = estimators(df, **kw)
        variants[vname] = figures(df, stores, appb, pure, share)
    g = variants["p13"]
    worst = []
    for name in g["chain"]:
        vals = [v["chain"][name] for v in variants.values()]
        same = len({round(x + 1e-9, 1) for x in vals}) == 1
        worst.append(("chain " + name, min(edge_dist(x, 0.1) for x in vals), same))
    for reg in g["region"]:
        for name in g["region"][reg]:
            vals = [v["region"][reg][name] for v in variants.values()]
            same = len({round(x + 1e-9, 1) for x in vals}) == 1
            worst.append(("%s %s" % (reg, name), min(edge_dist(x, 0.1) for x in vals), same))
        worst.append(("base %s" % reg, edge_dist(g["base_region"][reg], 1.0), True))
        vals = [v["packs_region"][reg] for v in variants.values()]
        worst.append(("packs %s" % reg, min(edge_dist(x, 1000) for x in vals) / g["packs_region"][reg],
                      len({round(x / 1000) for x in vals}) == 1))
    worst.append(("base chain", edge_dist(g["base_chain"], 1.0), True))
    vals = [v["packs_forty"] for v in variants.values()]
    worst.append(("packs chain", min(edge_dist(x, 1000) for x in vals) / g["packs_forty"],
                  len({round(x / 1000) for x in vals}) == 1))
    if verbose:
        for w in worst:
            print("  %-40s %.4f %s" % w)
    return g, variants, worst, appb, err


def score(worst):
    bad = 0
    for name, m, same in worst:
        if not same:
            bad += 1
        elif name.startswith("packs"):
            bad += m < 0.015
        elif name.startswith("base"):
            bad += m < 0.12
        else:
            bad += m < 0.03
    return bad


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    best = None
    for k in range(n):
        s1, s2 = 115 + 1000 * k, 115 + 7 * k
        g, variants, worst, appb, err = screen(s1, s2)
        b = score(worst)
        fails = [w[0] for w in worst if (not w[2]) or (w[1] < (0.015 if w[0].startswith("packs") else 0.12 if w[0].startswith("base") else 0.03))]
        print(k, s1, s2, "bad", b, round(g["chain"]["forty"], 4), fails[:8])
        if best is None or b < best[0]:
            best = (b, s1, s2)
    print("best", best)


def solve(seed_stores=115, seed_sim=115, iters=8, verbose=True):
    """Centre the regional and chain figures by per-region multipliers on own label and Delahunt."""
    import importlib
    T = {"P": {}, "C": {}, "D": {}}
    hist = []
    for it in range(iters):
        stores = ST.build(seed_stores)
        rows, means, truth = SIM.simulate(stores, seed_sim, T)
        df = frame(rows)
        import build
        err, appb = build.choose_appendix_b(rows, stores, seed_sim)
        appb = set(appb)
        pure, share = estimators(df)
        g = figures(df, stores, appb, pure, share)
        L4, L5 = lift_at(pure, 0.40), lift_at(pure, 0.50)
        # current own-label sums by region and price file
        weeks = W.BASE_WEEKS
        sub = df[df.week.isin(weeks) & df.dp.isna() & df.item.isin([W.DEL160, W.OL160])]
        gm = sub.groupby(["store", "item"]).units.mean()
        pf, rg = {}, {}
        for s in stores:
            for w in weeks:
                sid = ST.scan_ids(s, w)
                if sid:
                    pf[sid], rg[sid] = s["pfile"], s["reg_event"]
        O = defaultdict(float)
        Bv = defaultdict(float)
        for (sid, item), v in gm.items():
            if sid in appb:
                continue
            if item == W.OL160:
                O[(rg[sid], pf[sid])] += v
            else:
                Bv[rg[sid]] += v
        worst_ok = True
        for r in ["DNE", "S", "WNW", "MSE"]:
            f = g["region"][r]["forty"]
            tf = round(f, 1)
            if abs(f - tf) > 0.012:
                worst_ok = False
                T["P"][r] = T["P"].get(r, 1.0) * (tf - 1 - L4) / (f - 1 - L4)
            h = g["region"][r]["half"]
            th = round(h, 1)
            if abs(h - th) > 0.012:
                worst_ok = False
                op_new = O[(r, "P")] * (tf - 1 - L4) / (f - 1 - L4) if abs(f - tf) > 0.012 else O[(r, "P")]
                need_c = (th - 1 - L5) / share * Bv[r] - op_new - O[(r, "V")]
                T["C"][r] = T["C"].get(r, 1.0) * max(0.5, need_c / O[(r, "C")])
            b = g["base_region"][r]
            if edge_dist(b, 1.0) < 0.15:
                worst_ok = False
                T["D"][r] = T["D"].get(r, 1.0) * (1 + 0.45 / b)
        hist.append((it, {k: round(v, 4) for k, v in g["chain"].items()}))
        if verbose:
            print(it, {k: round(v, 3) for k, v in g["chain"].items()},
                  {r: (round(g["region"][r]["forty"], 3), round(g["region"][r]["half"], 3),
                       round(g["base_region"][r], 2)) for r in ["DNE", "S", "WNW", "MSE"]})
        if worst_ok:
            break
    return T, g


REGS = ["DNE", "S", "WNW", "MSE"]


def state(T, seed_stores=115, seed_sim=115):
    stores = ST.build(seed_stores)
    rows, means, truth = SIM.simulate(stores, seed_sim, T)
    df = frame(rows)
    import build
    err, appb = build.choose_appendix_b(rows, stores, seed_sim)
    appb = set(appb)
    pure, share = estimators(df)
    g = figures(df, stores, appb, pure, share)
    return stores, rows, df, appb, pure, share, g


def solve2(targets_f, targets_h, packs_t, iters=14, T=None, verbose=True):
    """Hit regional Save 40% and half-price multiples and regional packs by per-region multipliers."""
    T = T or {"P": {}, "C": {}, "D": {}}
    for it in range(iters):
        stores, rows, df, appb, pure, share, g = state(T)
        L4, L5 = lift_at(pure, 0.40), lift_at(pure, 0.50)
        done = True
        for r in REGS:
            f, h, B = g["region"][r]["forty"], g["region"][r]["half"], g["base_region"][r]
            p = g["packs_region"][r]
            # base: move B so packs hit target at the target multiple
            Bt = packs_t[r] / (3 * targets_f[r])
            if abs(p - packs_t[r]) > 120:
                done = False
                T["D"][r] = T["D"].get(r, 1.0) * Bt / B
            if abs(f - targets_f[r]) > 0.004:
                done = False
                T["P"][r] = T["P"].get(r, 1.0) * (targets_f[r] - 1 - L4) / (f - 1 - L4)
            if abs(h - targets_h[r]) > 0.004:
                done = False
                T["C"][r] = T["C"].get(r, 1.0) * (1 + ((targets_h[r] - h) / share * B) /
                                                   max(1.0, sum(v for (sid, it2), v in []) or 1.0) * 0)
                # own-label in Core stores needed: share * dO_C / B = (target - h)
                sub = df[df.week.isin(W.BASE_WEEKS) & df.dp.isna() & (df.item == W.OL160)]
                gm = sub.groupby("store").units.mean()
                pfm = {}
                for s in stores:
                    for w in W.BASE_WEEKS:
                        sid = ST.scan_ids(s, w)
                        if sid:
                            pfm[sid] = (s["pfile"], s["reg_event"])
                oc = sum(v for sid, v in gm.items() if sid not in appb and pfm[sid] == ("C", r))
                need = oc + (targets_h[r] - h) / share * B
                T["C"][r] = T["C"].get(r, 1.0) * max(0.3, need / oc)
        if verbose:
            print(it, "chain", {k: round(v, 4) for k, v in g["chain"].items()}, "packs", round(g["packs_forty"]),
                  "B", round(g["base_chain"], 2))
            print("   ", {r: (round(g["region"][r]["forty"], 4), round(g["region"][r]["half"], 4),
                          round(g["base_region"][r], 2), round(g["packs_region"][r])) for r in REGS})
        if done:
            break
    return T, g


def state_fixed(T, appb, seed_stores=115, seed_sim=115):
    stores = ST.build(seed_stores)
    rows, means, truth = SIM.simulate(stores, seed_sim, T)
    df = frame(rows)
    pure, share = estimators(df)
    g = figures(df, stores, appb, pure, share)
    return stores, rows, df, pure, share, g


def ol_sum(df, stores, appb, pfile, region):
    sub = df[df.week.isin(W.BASE_WEEKS) & df.dp.isna() & (df.item == W.OL160)]
    gm = sub.groupby("store").units.mean()
    pfm = {}
    for s in stores:
        for w in W.BASE_WEEKS:
            sid = ST.scan_ids(s, w)
            if sid:
                pfm[sid] = (s["pfile"], s["reg_event"])
    return sum(v for sid, v in gm.items() if sid not in appb and pfm[sid] == (pfile, region))


def solve3(targets_f, targets_h, packs_t, appb, iters=30, T=None, damp=0.7, verbose=False):
    T = T or {"P": {}, "C": {}, "D": {}}
    for it in range(iters):
        stores, rows, df, pure, share, g = state_fixed(T, appb)
        L4, L5 = lift_at(pure, 0.40), lift_at(pure, 0.50)
        done = True
        for r in REGS:
            f, h, B = g["region"][r]["forty"], g["region"][r]["half"], g["base_region"][r]
            p = g["packs_region"][r]
            if abs(p - packs_t[r]) > 100:
                done = False
                T["D"][r] = T["D"].get(r, 1.0) * (packs_t[r] / p) ** damp
            if abs(f - targets_f[r]) > 0.003:
                done = False
                T["P"][r] = T["P"].get(r, 1.0) * ((targets_f[r] - 1 - L4) / (f - 1 - L4)) ** damp
            if abs(h - targets_h[r]) > 0.003:
                done = False
                oc = ol_sum(df, stores, appb, "C", r)
                need = oc + (targets_h[r] - h) / share * B
                T["C"][r] = T["C"].get(r, 1.0) * max(0.3, need / oc) ** damp
        if verbose or done or it == iters - 1:
            print(it, "chain", {k: round(v, 4) for k, v in g["chain"].items()}, "packs", round(g["packs_forty"]),
                  "B", round(g["base_chain"], 2))
            print("   ", {r: (round(g["region"][r]["forty"], 4), round(g["region"][r]["half"], 4),
                          round(g["base_region"][r], 2), round(g["packs_region"][r])) for r in REGS})
        if done:
            break
    return T, g
