"""task238 household model: the issued addresses of the 2027 contact strategy test, who is eligible, who completes,
by which mode, and each household's answers under both modes (the counterfactual the generator alone sees)."""
import numpy as np

import params as P


def _logit(x):
    return 1.0 / (1.0 + np.exp(-x))


class World:
    pass


def make(seed=P.SEED):
    rng = np.random.default_rng(seed)
    W = World()
    n = P.ISSUED * len(P.QUARTERS)
    W.n = n
    W.quarter = np.repeat(np.arange(len(P.QUARTERS)), P.ISSUED)
    W.region = rng.choice([r[0] for r in P.REGIONS], n, p=[r[2] for r in P.REGIONS])
    # letters allocated at random within quarter and region, half to each
    W.letter_a = np.zeros(n, dtype=bool)
    for q in range(len(P.QUARTERS)):
        for r, _, _ in P.REGIONS:
            idx = np.flatnonzero((W.quarter == q) & (W.region == r))
            pick = rng.permutation(idx)[: len(idx) // 2 + (rng.random() < 0.5 if len(idx) % 2 else 0)]
            W.letter_a[pick] = True
    # eligibility
    u = rng.random(n)
    W.elig = np.full(n, "", dtype=object)
    cut = 0.0
    for code, p in P.ELIGIBILITY:
        W.elig[(u >= cut) & (u < cut + p)] = code
        cut += p
    W.eligible = W.elig == ""
    # the selected adult
    W.age = np.clip(np.round(rng.normal(49, 17.5, n)), 18, 94).astype(int)
    W.female = rng.random(n) < 0.52
    e = rng.random(n)
    W.post = (e >= 0.37) & (e < 0.73)
    W.deg = e >= 0.73
    W.emp = rng.random(n) < np.clip(0.80 - 0.016 * np.maximum(W.age - 55, 0), 0.06, 0.9)
    W.rent = rng.random(n) < np.clip(0.50 - 0.006 * (W.age - 30), 0.08, 0.7)
    W.hh = np.clip(rng.poisson(1.4, n) + 1 + (W.age < 45) * rng.integers(0, 2, n), 1, 8)
    W.away = rng.standard_normal(n) + 0.30 * W.emp - 0.010 * (W.age - 49)
    W.online = rng.standard_normal(n) - 0.012 * (W.age - 49)
    a10 = (W.age - 49) / 10.0
    # response, the letter playing no part
    r = P.RESP
    pr = _logit(r["base"] + r["age"] * a10 + r["post"] * W.post + r["deg"] * W.deg + r["emp"] * W.emp
                + r["rent"] * W.rent + r["away"] * W.away + r["online"] * W.online)
    W.complete = W.eligible & (rng.random(n) < pr)
    m = P.MODE
    pw = _logit(m["base"] + m["letter_a"] * W.letter_a + m["age"] * a10 + m["post"] * W.post + m["deg"] * W.deg
                + m["emp"] * W.emp + m["rent"] * W.rent + m["away"] * W.away + m["online"] * W.online)
    W.web = W.complete & (rng.random(n) < pw)
    # answers under both modes
    W.ans = {}
    reg_i = W.region - 1
    for code, name, item, kind, tol, theta in P.INDEXES:
        c = P.OUT[code]
        base = (c[0] + c[1] * a10 + c[2] * W.female + c[3] * W.post + c[4] * W.deg + c[5] * W.emp + c[6] * W.rent
                + c[7] * (W.hh - 2.4) + c[8] * W.away + c[9] * W.online
                + np.asarray(P.REGION_SHIFT[kind])[reg_i])
        if kind == "score":
            lat = base + rng.normal(0, c[10], n)
            ph = np.clip(np.round(lat), 0, 10).astype(int)
            wb = np.clip(np.round(lat + theta), 0, 10).astype(int)
        else:
            p0 = np.clip(base, 0.01, 0.97)
            uu = rng.random(n)
            ph = (uu < p0).astype(int)
            wb = (uu < np.clip(p0 + theta / 100.0, 0, 1)).astype(int)
        W.ans[code] = (ph, wb)
    return W
