"""Calibration: evaluate a world's ladder (every route's cut under every method, the golden family's margins, the
generating truth) and the program sets each route designates; search seeds for a world that passes."""
import sys

import numpy as np

import methods as M
import sim as S
import world as W


def arrays(w):
    s25, s26 = w["scored"][2025], w["scored"][2026]
    f25, f26 = s25["first"], s26["first"]
    Y, VY, VYmc = s25["raw"][f25], s25["anchor"][f25], s25["mc"][f25][:, :W.N_SHARED].sum(1)
    X, VX, VXmc = s26["raw"][f26], s26["anchor"][f26], s26["mc"][f26][:, :W.N_SHARED].sum(1)
    return X.astype(float), VX.astype(float), VXmc.astype(float), Y.astype(float), VY.astype(float), VYmc.astype(float)


def truth(w):
    """the 2025 first-attempt candidates sitting Form 26A under the 2026 scoring: single-group equipercentile"""
    r = S.rng(w["seed"], 9)
    s25 = w["scored"][2025]
    idx = s25["idx"][s25["first"]]
    t1 = np.array([w["rows"][i]["t1"] for i in idx])
    t2 = np.array([w["rows"][i]["t2"] for i in idx])
    mc = S.mc_scores(t1, w["f26"]["mc"], r)
    wa = S.wa_reads(t2, w["f26"]["wa"], w["p"]["sev"][2026], r)[3]
    YX = (mc.sum(1) + W.WA_WEIGHT * wa.sum(1)).astype(float)
    Y = s25["raw"][s25["first"]].astype(float)
    FYX, FY = M._cdf(YX, M.MAXX), M._cdf(Y, M.MAXX)
    return M.cut(lambda x: M._iprk(FY, M._prk(FYX, x)))


def evaluate(w, verbose=False):
    X, VX, VXmc, Y, VY, VYmc = arrays(w)
    b2 = M.validity_shift(w["papers"], w["vreads"], "WA2")
    pooled = float(np.mean([v - w["papers"][pi]["consensus"] for pi, v in w["vreads"]]))
    rts, shift = M.routes(X, VX, VXmc, Y, VY, VYmc, b2, pooled)
    g = rts["G anchor on the 2025 standard"]
    gcuts = {v[0] for v in g.values()}
    res = dict(bias=b2, pooled=pooled, shift=shift, gcuts=gcuts)
    if len(gcuts) == 1:
        c = gcuts.pop()
        res["g"] = c
        res["lo"] = min(v[1] - (W.PASS_RAW_25A - 0.5) for v in g.values())
        res["hi"] = min((W.PASS_RAW_25A - 0.5) - v[2] for v in g.values())
    res["cuts"] = {k: sorted({v[0] for v in d.values()}) for k, d in rts.items()}
    res["truth"] = truth(w)[0]
    res["p25"] = float((Y >= W.PASS_RAW_25A).mean())
    sets = {}
    for k, cs in res["cuts"].items():
        for c in cs:
            pr = M.pass_rates(w["rows"], w["scored"], c)
            sets[(k, c)] = (frozenset(p for p, (a, n) in pr.items() if a / n < W.REVIEW_LINE), pr)
    res["sets"] = sets
    if verbose:
        print("validity bias WA2 %.3f, pooled %.3f, anchor shift %.3f" % (b2, pooled, shift))
        for k, d in rts.items():
            print("  %-48s %s" % (k, "  ".join("%s %d (%.2f/%.2f)" % (m.split(" (")[0][:7] + ("" if "(" not in m else m[m.index("(") + 1:m.index("(") + 4]), v[0], v[1], v[2]) for m, v in d.items())))
        print("  truth", res["truth"], " 2025 pass %.3f" % res["p25"])
    return res


def judge(res, need_margin=0.25):
    if "g" not in res:
        return False, "golden family split %s" % res["gcuts"]
    g = res["g"]
    c = res["cuts"]
    probs = []
    if min(res["lo"], res["hi"]) < need_margin:
        probs.append("margin %.2f/%.2f" % (res["lo"], res["hi"]))
    if abs(res["truth"] - g) > 1:
        probs.append("truth %d" % res["truth"])
    if min(c["R1 anchor as scored"]) < g + 2:
        probs.append("R1 %s" % c["R1 anchor as scored"])
    if max(c["R2 multiple-choice anchor"]) > g - 2:
        probs.append("R2 %s" % c["R2 multiple-choice anchor"])
    if c["R0 the 2025 raw passing score"][0] < g + 3:
        probs.append("R0 %s" % c["R0 the 2025 raw passing score"])
    if abs(c["R0p raters adjusted, no equating"][0] - g) < 2:
        probs.append("R0p %s" % c["R0p raters adjusted, no equating"])
    if g in c["R1p anchor adjusted by every assignment's papers"]:
        probs.append("R1p touches G")
    gset = res["sets"][("G anchor on the 2025 standard", g)][0]
    for (k, cc), (st, _) in res["sets"].items():
        if not k.startswith("G") and st == gset:
            probs.append("set of %s at %d equals G's" % (k[:3], cc))
    if not (3 <= len(gset) <= 7):
        probs.append("G set size %d" % len(gset))
    pr = res["sets"][("G anchor on the 2025 standard", g)][1]
    near = min(abs(a - W.REVIEW_LINE * n) for a, n in pr.values())
    if near < 1.5:
        probs.append("a program within %.1f candidates of the line" % near)
    if not (0.74 <= res["p25"] <= 0.84):
        probs.append("p25 %.3f" % res["p25"])
    return not probs, "; ".join(probs)


if __name__ == "__main__":
    seeds = range(int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else [W.SEED]
    for sd in seeds:
        w = S.world(sd)
        res = evaluate(w, verbose=len(seeds) == 1)
        ok, why = judge(res)
        print(sd, "PASS" if ok else "fail", res.get("g"), "%.2f/%.2f" % (res.get("lo", 0), res.get("hi", 0)), why)


# ----------------------------------------------------------------------------------------------- program placement
TARGETS = [0.90, 0.875, 0.85, 0.83, 0.81, 0.79, 0.77, 0.752, 0.737, 0.721, 0.678, 0.655, 0.628, 0.598, 0.565, 0.535]


def program_rate(w, k, off, g):
    """program k's first-attempt pass rate at cut g with its completers' abilities moved by off (same draws)"""
    hits = n = 0
    for yr, c, form in ((2025, W.PASS_RAW_25A, w["f25"]), (2026, g, w["f26"])):
        s = w["scored"][yr]
        js = [j for j, i in enumerate(s["idx"]) if w["rows"][i]["group"] == "completer" and w["rows"][i]["program"] == k
              and w["rows"][i]["first"] == yr]
        if not js:
            continue
        js = np.array(js)
        t1 = np.array([w["rows"][s["idx"][j]]["t1"] for j in js]) + off
        t2 = np.array([w["rows"][s["idx"][j]]["t2"] for j in js]) + off
        raw = S.raw_of(form, yr, t1, t2, s["U"][js], tuple(z[js] for z in s["Z"]), w["p"]["sev"][yr])
        hits += int((raw >= c).sum())
        n += len(js)
    return hits / n


def place(seed, order=None, rounds=6, **kw):
    """solve each program's ability offset so its first-attempt pass rate at the golden cut sits at its target,
    repeating until the golden cut stops moving"""
    order = order or list(range(len(W.PROGRAMS)))
    base = list(W.PROGRAMS)
    off = np.zeros(len(base))
    last = None
    try:
        for _ in range(rounds):
            W.PROGRAMS[:] = [(p[0], p[1], p[2], p[3], p[4] + off[k], p[5] + off[k], p[6], p[7]) for k, p in enumerate(base)]
            w = S.world(seed, **kw)
            res = evaluate(w)
            if "g" in res:
                g = res["g"]
            else:   # the family split this round: place on the Tucker cut and judge only the final world
                g = int(np.median(res["cuts"]["G anchor on the 2025 standard"]))
            if g == last and "g" in res:
                break
            last = g
            for k in range(len(base)):
                tgt = TARGETS[order.index(k)]
                lo, hi = -1.5, 1.5
                for _ in range(24):
                    mid = (lo + hi) / 2
                    if program_rate(w, k, mid, g) < tgt:
                        lo = mid
                    else:
                        hi = mid
                off[k] += hi
        W.PROGRAMS[:] = [(p[0], p[1], p[2], p[3], round(p[4] + off[k], 4), round(p[5] + off[k], 4), p[6], p[7])
                         for k, p in enumerate(base)]
        w = S.world(seed, **kw)
        res = evaluate(w)
        return list(W.PROGRAMS), res
    finally:
        W.PROGRAMS[:] = base
