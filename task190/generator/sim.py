"""The arisings population, the survey sample, and the design-based estimates the call rests on.

The arisings of a waste stream are a variable every enterprise in the frame carries (zero where it
produces none), so a stream is a domain of the variable rather than a subpopulation of enterprises,
and the design variance of its estimated total runs over every sampled unit in each stratum.
"""
import math

import numpy as np

import world as W


def population(rng):
    """Arisings in tonnes for every enterprise in the frame, by stream and stratum."""
    pop = {}
    for key, _name, pis, mus, cvs in W.STREAMS:
        cols = []
        for h, (_code, _label, N, _r) in enumerate(W.STRATA):
            k = 1.0 / cvs[h] ** 2
            x = rng.gamma(k, mus[h] / k, size=N) * (rng.random(N) < pis[h])
            cols.append(np.round(x, 3))
        pop[key] = cols
    return pop


def draw(pop, rng):
    """Responding sample: r_h of the N_h in each stratum, E1 complete."""
    idx = {}
    for h, (_code, _label, N, r) in enumerate(W.STRATA):
        idx[h] = np.sort(rng.choice(N, size=r, replace=False))
    samp = {k: [pop[k][h][idx[h]] for h in range(len(W.STRATA))] for k in pop}
    return samp, idx


def weights():
    return [N / float(r) for _c, _l, N, r in W.STRATA]


def est_total(samp, key):
    w = weights()
    return float(sum(w[h] * samp[key][h].sum() for h in range(len(W.STRATA))))


def var_design(samp, key):
    """CORRECT: stratified design variance with each stratum's finite-population correction, over
    every sampled unit in the stratum (the zeros included). A completely enumerated stratum has
    f = 1 and contributes nothing."""
    V = 0.0
    for h, (_c, _l, N, r) in enumerate(W.STRATA):
        if r >= N:
            continue
        s2 = float(samp[key][h].var(ddof=1))
        V += N * N * (1.0 - r / float(N)) * s2 / r
    return V


def var_jackknife(samp, key):
    """Delete-one jackknife within strata, the take-all stratum excluded. Converges on var_design."""
    base = est_total(samp, key)
    w = weights()
    V = 0.0
    for h, (_c, _l, N, r) in enumerate(W.STRATA):
        if r >= N:
            continue
        x = samp[key][h]
        tot_h = w[h] * x.sum()
        wj = N / (r - 1.0)
        reps = base - tot_h + wj * (x.sum() - x)
        V += (1.0 - r / float(N)) * (r - 1.0) / r * float(((reps - reps.mean()) ** 2).sum())
    return V


def var_no_fpc(samp, key):
    """Rung 2: strata declared, the finite-population correction omitted."""
    V = 0.0
    for h, (_c, _l, N, r) in enumerate(W.STRATA):
        s2 = float(samp[key][h].var(ddof=1))
        V += N * N * s2 / r
    return V


def var_with_replacement(samp, key):
    """Rung 2b: Hansen-Hurwitz on the weights, no strata, no correction."""
    w = weights()
    vals, ws = [], []
    for h in range(len(W.STRATA)):
        vals.extend(samp[key][h].tolist())
        ws.extend([w[h]] * len(samp[key][h]))
    v = np.array(vals) * np.array(ws)
    n = len(v)
    return float(n / (n - 1.0) * ((v - v.mean()) ** 2).sum())


def var_srs_pooled(samp, key):
    """Rung 2c: the sample pooled as a simple random sample of the whole frame."""
    vals = np.concatenate([samp[key][h] for h in range(len(W.STRATA))])
    N = sum(N for _c, _l, N, _r in W.STRATA)
    n = len(vals)
    return float(N * N * (1.0 - n / float(N)) * vals.var(ddof=1) / n)


def var_reporting_only(samp, key):
    """Rung 3: the client's named shortcut, subset then estimate (non-reporting units dropped)."""
    V = 0.0
    for h, (_c, _l, N, r) in enumerate(W.STRATA):
        if r >= N:
            continue
        x = samp[key][h]
        nz = x[x > 0]
        if len(nz) < 2:
            continue
        V += N * N * (1.0 - r / float(N)) * float(nz.var(ddof=1)) / r
    return V


def reporting_count(samp, key):
    return int(sum(int((samp[key][h] > 0).sum()) for h in range(len(W.STRATA))))


def national_cv(samp):
    """The design CV of the 2026 national arisings estimate, which the release's methodology note
    publishes. Correct for what it measures, and what rung 1 misuses."""
    w = weights()
    tot = sum(est_total(samp, k) for k, _n, _p, _m, _c in W.STREAMS)
    V = 0.0
    for h, (_c, _l, N, r) in enumerate(W.STRATA):
        if r >= N:
            continue
        rows = np.sum([samp[k][h] for k, _n, _p, _m, _c in W.STREAMS], axis=0)
        V += N * N * (1.0 - r / float(N)) * float(rows.var(ddof=1)) / r
    return math.sqrt(V) / tot, tot


def attainment(samp):
    """Everything the call needs, per stream: the estimate, the register total, the rate, its
    standard error under every route, the plan target and the verdict."""
    out = {}
    for key, _n, _p, _m, _c in W.STREAMS:
        X = est_total(samp, key)
        rec = int(round(W.PRINTED_RATE[key] / 100.0 * X))
        rate = rec / X
        cv = math.sqrt(var_design(samp, key)) / X
        tgt = round(rate * (1.0 + W.Z_DESIGN[key] * cv) * 100.0, 1) / 100.0
        se = rate * cv
        z = (tgt - rate) / se
        out[key] = {"arisings": X, "recovered_t": rec, "rate": rate, "cv": cv, "se": se,
                    "target": tgt, "shortfall": tgt - rate, "z": z,
                    "lo": rate - W.BAR * se, "hi": rate + W.BAR * se,
                    "established": bool(z > W.BAR), "reporting": reporting_count(samp, key)}
    return out


def build_sample(seed=None):
    rng = np.random.default_rng(W.SEED if seed is None else seed)
    pop = population(rng)
    samp, idx = draw(pop, rng)
    return pop, samp, idx
