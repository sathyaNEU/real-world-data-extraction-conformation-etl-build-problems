"""The scan that fixed the shipped world: which draw of the eight provinces' award levels the pack
carries, and the standard award level that puts clause 9's ceiling on the committed figure.

Scaling the standard award level scales every award, every cell average and the ceiling together and
leaves the scale-free award shape untouched, so the scan measures one simulated world per seed and
rescales it, then the shipped build re-runs the simulation at the chosen level and re-measures.

    python3 task202/generator/tune.py 202 203 204 ...
"""
import sys

import numpy as np

import params as P
import sim
import solve


def scaled(W, f):
    """The same world with every peso amount multiplied by f. The shape is unchanged."""
    out = dict(W)
    out["mean"] = {k: v * f for k, v in W["mean"].items()}
    out["porwin"] = [dict(a, amount=a["amount"] * f) for a in W["porwin"]]
    return out


def find_scale(W, target=7800):
    g1 = solve.lowest(lambda C: solve.share_cells(C, W["mean"], W["cnt"], W["shape"]))
    f = target / float(g1)
    for _ in range(40):
        Ws = scaled(W, f)
        g = solve.lowest(lambda C: solve.share_cells(C, Ws["mean"], Ws["cnt"], Ws["shape"]))
        if g == target:
            return f, g
        f *= (1.0 + 0.45 * (target - g) / target)
    return f, g


def clearance(W, C):
    """How far clause 9's share sits below the cap at the chosen ceiling, and above it one step down,
    as a fraction of the step the last PHP 100 of ceiling buys."""
    s0 = solve.share_cells(C, W["mean"], W["cnt"], W["shape"])
    s1 = solve.share_cells(C - P.ROUND_TO, W["mean"], W["cnt"], W["shape"])
    step = s1 - s0
    return (P.COMMITTED_SHARE - s0) / step, (s1 - P.COMMITTED_SHARE) / step, s0, s1, step


def transport(W, cap=None):
    """The ceiling each subset of the portal's own awards would produce (SF4's measurement)."""
    mean, cnt, shape = W["mean"], W["cnt"], W["shape"]
    pw = W["porwin"]
    band = np.array([a["band"] for a in pw])
    part = np.array([a["partner"] for a in pw])
    subs = []
    for b in P.BANDS:
        sel = band == b
        if sel.sum() > 400:
            subs.append(solve.lowest(lambda C: solve.share_cells(C, mean, cnt, shape[sel]), cap))
    lv = {p: float(np.mean([mean[(p, bb)] for bb in P.BANDS if (p, bb) in mean]))
          for p in sorted(set(part.tolist()))}
    ter = np.quantile(list(lv.values()), [1 / 3, 2 / 3])
    for lo, hi in [(-1e18, ter[0]), (ter[0], ter[1]), (ter[1], 1e18)]:
        sel = np.isin(part, [p for p, L in lv.items() if lo < L <= hi])
        if sel.sum() > 400:
            subs.append(solve.lowest(lambda C: solve.share_cells(C, mean, cnt, shape[sel]), cap))
    return (max(subs) - min(subs)) / 100.0, subs


def edge(v, unit):
    """Distance from the printed cell's nearest edge, in the figure's own unit."""
    c = round(v / unit) * unit
    return unit / 2.0 - abs(v - c)


def grade_edges(F):
    """Every graded figure's distance to its printed cell edge, as the asking sentences round them."""
    out = []
    for b in P.BANDS:
        d = F["bands"][b]
        out.append(("band %d referred share" % b, d["referred_share"], 0.1, edge(d["referred_share"], 0.1)))
        out.append(("band %d referred value share" % b, d["referred_value_share"], 0.1,
                    edge(d["referred_value_share"], 0.1)))
    out.append(("referred awards", F["referred"], 1.0, edge(F["referred"], 1.0)))
    out.append(("shape CV", F["cv"], 0.01, edge(F["cv"], 0.01)))
    return out


def report(seed):
    P.SEED = seed
    W = sim.make()
    f, g = find_scale(W)
    Ws = scaled(W, f)
    L = solve.ladder(Ws)
    F = solve.figures_for(L["R6"], Ws)
    cl, ex, s0, s1, step = clearance(Ws, L["R6"])
    tr, subs = transport(Ws)
    seps = {r: (L[r] - L["R6"]) / 100.0 for r in solve.ROUTES}
    ed = grade_edges(F)
    worst = min(abs(v) for v in seps.values())
    tight = min(ed, key=lambda x: x[3] / x[2])
    print("seed %d  BASE %.1f  golden %d  mix %+.0f" % (seed, P.BASE * f, L["R6"], L["Rmix"] - L["R6"]))
    print("   %s | worst %4.1f pu" % (" ".join("%s %+6.1f" % (r, seps[r]) for r in solve.ROUTES), worst))
    print("   share %.4f%% (cap 6.0) clearance %.2f of step | at -100 %.4f%% excess %.2f | step %.4f pp"
          % (100 * s0, cl, 100 * s1, ex, 100 * step))
    print("   transport %.1f pu %s | cv %.4f | tightest figure %s %.4f edge %.4f of %.3f"
          % (tr, subs, L["_cv"], tight[0], tight[1], tight[3], tight[2] / 2))
    return dict(seed=seed, f=f, L=L, worst=worst, cl=cl, ex=ex, tr=tr,
                min_edge=min(x[3] / (x[2] / 2) for x in ed))


if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [P.SEED]
    rs = [report(s) for s in seeds]
    print()
    print("ranked by the worst thing about each draw:")
    for r in sorted(rs, key=lambda r: -min(r["worst"] / 3.0, r["cl"] / 0.25, r["ex"] / 0.25, r["min_edge"] / 0.3)):
        print("  seed %d worst %4.1f pu | clearance %.2f | excess %.2f | min edge %.2f of half-cell | transport %.1f"
              % (r["seed"], r["worst"], r["cl"], r["ex"], r["min_edge"], r["tr"]))
