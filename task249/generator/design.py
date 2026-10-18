"""Scratch: a trial head design measured on the window, every estimator against the band."""
import numpy as np, params as P, sim, tune

def run(spans, offs, pts, seed=P.SEED, noise=2.5, show=False):
    rng = np.random.default_rng(seed)
    an = [(a[2], a[3]) for a in P.ANALYSERS]
    true = sim.field(an + pts, rng)
    i0, i1 = tune.window_idx()
    A = true[:4, i0:i1]; N = true[4:, i0:i1]
    pool = A.reshape(-1); m4 = A.mean(0)
    rows = []
    for j, (x, y) in enumerate(pts):
        d = [np.hypot(x - ax, y - ay) for ax, ay in an]; k = int(np.argmin(d))
        node = spans[j] * N[j] + offs[j] + noise * rng.standard_normal(N.shape[1])
        e = tune.estimators(node, A[k], pool)
        e["ols_m4"] = np.polyfit(m4, node, 1)[0]
        e["d"] = min(d)
        rows.append(e)
    return rows

def lists(rows, lo=P.BAND[0], hi=P.BAND[1]):
    out = {}
    for k in rows[0]:
        if k in ("d", "r"):
            continue
        out[k] = sorted(j for j, e in enumerate(rows) if not lo <= e[k] <= hi)
    return out
