"""task122 generator: the archive of nine home-carousel A/B tests (March 2023 to May 2026).

For each test: the logging window that preceded it at session grain (cell, arm, propensity, renders,
in-session orders), and the realised lift of the online test, measured as the charter defines lift.
The logged sessions are generated from each test's true per-cell effect; the generator then nudges
single orders until the estimators land where the test's record puts them (session weights within
0.21 of the realised lift on every test, render weights off on the three tests whose gain sat in long
sessions, replay off on the six whose logger allocation varied by cell). Every estimate is then
recomputed from the written sheet by checks.py and the verifier.

Hidden from the pack: each archived session's watched-listing orders and its orders over the 21
days after the session. They exist so the build can assert that the archive is blind to borrowed
orders for a reason (no archived ranker put a watched listing ahead of others) and that the kept
construction would also reproduce all nine tests.
"""
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P

# test_id, family, inputs, logger, logging window, test window, traffic, days, cells, uniform?,
# mean renders, realised, interval half-width, targets (session, render weights, replay rows)
TESTS = [
    ("T1", "Two-tower personaliser", "Buyer and listing embeddings from views, orders and searches", "v2",
     date(2023, 2, 6), date(2023, 2, 19), date(2023, 3, 6), date(2023, 4, 2), 10, 28, "all", True, 2.60, 7.9, 1.7,
     7.78, 8.03, None),
    ("T2", "Recency boost", "Listing age; category", "v2",
     date(2023, 7, 10), date(2023, 7, 23), date(2023, 8, 7), date(2023, 9, 3), 10, 28, "all", False, 2.70, 4.1, 1.6,
     4.29, 4.94, 5.21),
    ("T3", "Sequence model", "In-session sequence of listing views", "v3",
     date(2024, 1, 8), date(2024, 1, 21), date(2024, 2, 5), date(2024, 3, 3), 10, 28, "all", False, 1.90, 5.6, 1.6,
     5.52, 5.75, 6.31),
    ("T4", "Two-tower personaliser", "Buyer and listing embeddings from views, orders and searches", "v3",
     date(2024, 4, 15), date(2024, 4, 28), date(2024, 5, 13), date(2024, 6, 9), 10, 28, "all", False, 2.50, 7.1, 1.7,
     7.02, 7.27, 7.71),
    ("T5", "Seller-diversity cap", "Seller id", "v3",
     date(2024, 8, 26), date(2024, 9, 8), date(2024, 9, 23), date(2024, 10, 13), 5, 21, "app", True, 2.40, 3.6, 2.1,
     3.68, 3.74, None),
    ("T6", "Trending boost", "Category order velocity by size; buyer sizes", "v3",
     date(2024, 10, 21), date(2024, 11, 3), date(2024, 11, 18), date(2024, 12, 15), 10, 28, "all", True, 2.80, 4.4, 1.6,
     4.37, 4.52, None),
    ("T7", "Sequence model", "In-session sequence of listing views", "v3",
     date(2025, 11, 16), date(2025, 11, 29), date(2025, 12, 8), date(2026, 1, 4), 10, 28, "all", False, 6.80, 2.5, 1.6,
     2.61, 5.12, 6.31),
    ("T8", "Two-tower personaliser", "Buyer and listing embeddings from views, orders and searches", "v4",
     date(2026, 1, 19), date(2026, 2, 1), date(2026, 2, 16), date(2026, 3, 15), 10, 28, "all", False, 2.60, 6.8, 1.7,
     6.71, 6.98, 8.12),
    ("T9", "Local pickup radius", "Buyer region; seller pickup settings", "v4",
     date(2026, 3, 30), date(2026, 4, 12), date(2026, 4, 27), date(2026, 5, 24), 10, 28, "app", False, 2.50, 3.2, 1.9,
     3.41, 4.27, 5.12),
]
TEST_COLS = ["test_id", "family", "inputs", "logger", "log_from", "log_to", "test_from", "test_to", "traffic",
             "days", "cells", "uniform", "renders", "realised", "half", "t_sess", "t_rend", "t_rep"]

ARCH_N = 11000
SHARES = P.N_CELL / P.N_CELL.sum()


def cells_of(scope):
    return list(range(4)) if scope == "app" else list(range(8))


def alloc(t, cells, hi):
    """Test-arm propensity per cell: one value when the logger allocated uniformly, otherwise a
    higher share in the app cells with established buyers (where the base rate is highest)."""
    if t["uniform"]:
        v = {"T1": 0.40, "T5": 0.35, "T6": 0.40}[t["test_id"]]
        return {c: v for c in cells}
    lo = 0.30
    return {c: (hi if c in (2, 3) else lo) for c in cells}


def arch_render_dist(c, mean_all):
    scale = mean_all / 2.693
    return P.render_dist(max(1.05, P.NBAR[c] * scale))


def counts_for(t, cells):
    w = np.array([SHARES[c] for c in cells])
    w = w / w.sum()
    raw = w * ARCH_N
    out = np.maximum(100, np.round(raw / 100).astype(int) * 100)
    return {c: int(v) for c, v in zip(cells, out)}


def expected(t, cells, Nc, pi, L, b, f=1.0):
    """Expected (session IPS, render-weighted IPS, replay rows, replay sessions) lifts."""
    num = {k: {"T": 0.0, "C": 0.0} for k in ("s", "rw_n", "rw_d", "rp_n", "rp_d", "rs_n", "rs_d")}
    Ntot = sum(Nc.values())
    S = 0.0
    rw = {"T": [0.0, 0.0], "C": [0.0, 0.0]}
    rp = {"T": [0.0, 0.0], "C": [0.0, 0.0]}
    rs = {"T": [0.0, 0.0], "C": [0.0, 0.0]}
    for c in cells:
        H = arch_render_dist(c, t["renders"])
        n = np.arange(1, P.NMAX + 1)
        nb = (H * n).sum()
        base = P.KAPPA[c] * f * (P.ALPHA + (1 - P.ALPHA) * n / nb)
        d = L + b * (n - nb)
        for arm, p in (("T", pi[c]), ("C", 1 - pi[c])):
            y = base + (d if arm == "T" else 0)
            m = Nc[c] * p
            if arm == "T":
                S += Nc[c] / Ntot * (H * y).sum()
            else:
                S -= Nc[c] / Ntot * (H * y).sum()
            rw[arm][0] += Nc[c] * (H * n * y).sum()
            rw[arm][1] += Nc[c] * (H * n).sum()
            rp[arm][0] += m * (H * n * y).sum()
            rp[arm][1] += m * (H * n).sum()
            rs[arm][0] += m * (H * y).sum()
            rs[arm][1] += m
    f2 = lambda d: d["T"][0] / d["T"][1] - d["C"][0] / d["C"][1]
    return S, f2(rw), f2(rp), f2(rs)


def solve_test(t):
    cells = cells_of(t["cells"])
    Nc = counts_for(t, cells)
    # slope for the render-weighted target, level for the session target, allocation for replay
    best = None
    his = [None] if t["uniform"] else list(np.round(np.arange(0.31, 0.71, 0.01), 2))
    for hi in his:
        pi = alloc(t, cells, hi if hi is not None else 0.0)
        # linear in L and b: solve the 2x2 for session and render targets
        s0, r0, _, _ = expected(t, cells, Nc, pi, 0.0, 0.0)
        s1, r1, _, _ = expected(t, cells, Nc, pi, 1.0, 0.0)
        s2, r2, _, _ = expected(t, cells, Nc, pi, 0.0, 1.0)
        A = np.array([[s1 - s0, s2 - s0], [r1 - r0, r2 - r0]])
        L, b = np.linalg.solve(A, np.array([t["t_sess"] - s0, t["t_rend"] - r0]))
        s, r, rp, rs = expected(t, cells, Nc, pi, L, b)
        err = 0.0 if t["t_rep"] is None else abs(rp - t["t_rep"])
        if best is None or err < best[0]:
            best = (err, pi, L, b, s, r, rp, rs)
    return cells, Nc, best


def build_archive():
    tests = [dict(zip(TEST_COLS, row)) for row in TESTS]
    sessions = []
    meta = []
    for ti, t in enumerate(tests):
        cells, Nc, (err, pi, L, b, s, r, rp, rs) = solve_test(t)
        rng = P.stream(f"archive-{t['test_id']}")
        rows = []
        for c in cells:
            H = arch_render_dist(c, t["renders"])
            n_vals = np.arange(1, P.NMAX + 1)
            nb = (H * n_vals).sum()
            for arm, p in (("test", pi[c]), ("control", round(1 - pi[c], 2))):
                m = int(round(Nc[c] * p))
                cnt = np.zeros(P.NMAX + 1, int)
                cnt[1:] = _lr(H, m)
                carry = 0.0
                for n in range(P.NMAX, 0, -1):
                    if cnt[n] == 0:
                        continue
                    base = P.KAPPA[c] * (P.ALPHA + (1 - P.ALPHA) * n / nb)
                    mu = base + ((L + b * (n - nb)) if arm == "test" else 0.0)
                    tgt = max(0.0, mu) * cnt[n] / 1000 + carry
                    k = int(np.floor(tgt + 0.5))
                    carry = tgt - k
                    y = np.zeros(cnt[n], int)
                    y[rng.choice(cnt[n], size=min(k, cnt[n]), replace=False)] = 1
                    for v in y:
                        rows.append((t["test_id"], c, arm, p, n, int(v)))
        df = pd.DataFrame(rows, columns=["test_id", "cell", "arm", "p", "n", "y"])
        df = tune_test(df, t, rng)
        sessions.append(df)
        meta.append(dict(t, pi=pi, L=L, b=b))
    A = pd.concat(sessions, ignore_index=True)
    return tests, meta, A


def _lr(w, total):
    w = np.asarray(w, float)
    raw = w / w.sum() * total
    out = np.floor(raw).astype(int)
    rem = int(total - out.sum())
    order = np.argsort(-(raw - out), kind="stable")
    out[order[:rem]] += 1
    return out


def arch_estimates(df):
    """(session IPS, render-weighted IPS, replay rows, replay sessions) lift per 1,000 sessions."""
    N = len(df)
    T = df[df.arm == "test"]
    C = df[df.arm == "control"]
    s = ((T.y / T.p).sum() - (C.y / C.p).sum()) / N * 1000
    rw = ((T.n * T.y / T.p).sum() / (T.n / T.p).sum() - (C.n * C.y / C.p).sum() / (C.n / C.p).sum()) * 1000
    rp = ((T.n * T.y).sum() / T.n.sum() - (C.n * C.y).sum() / C.n.sum()) * 1000
    rs = (T.y.mean() - C.y.mean()) * 1000
    return s, rw, rp, rs


RENDER_MISS = {"T2", "T7", "T9"}
TWINS = ("T3", "T7")


BOXES = {  # (session weights, render weights, replay over render rows); None = free
    "T1": ((7.70, 7.90), (7.92, 8.10), None),
    "T2": ((4.18, 4.31), (4.84, 5.04), (5.10, 5.32)),
    "T3": ((5.42, 5.62), (5.62, 5.80), (6.265, 6.335)),
    "T4": ((6.92, 7.10), (7.16, 7.30), (7.64, 7.80)),
    "T5": ((3.58, 3.78), (3.64, 3.80), None),
    "T6": ((4.28, 4.48), (4.44, 4.60), None),
    "T7": ((2.52, 2.70), (5.00, 5.24), (6.265, 6.335)),
    "T8": ((6.62, 6.80), (6.86, 7.00), (8.04, 8.20)),
    "T9": ((3.30, 3.41), (4.17, 4.37), (5.02, 5.22)),
}


def intervals(t):
    """Where each estimate has to land for this test: session weights within 0.21 of the realised
    lift on every test; render weights within 0.20 on six tests and 0.84 to 2.72 above on the three
    whose gain sat in long sessions (T2, T7, T9); replay over render rows (the published offline
    estimate) 0.56 to 3.83 above on the six cell-allocated tests, inside 6.27 to 6.33 for the twin
    pair (T3, T7) so both publish 6.3."""
    b = BOXES[t["test_id"]]
    return np.array([b[0], b[1], b[2] if b[2] is not None else (-1e9, 1e9)], float)


def _effects(df):
    N = len(df)
    T = (df.arm == "test").to_numpy()
    p = df.p.to_numpy()
    n = df.n.to_numpy().astype(float)
    sw_T, sw_C = (n[T] / p[T]).sum(), (n[~T] / p[~T]).sum()
    nT, nC = n[T].sum(), n[~T].sum()
    return np.vstack([np.where(T, 1.0, -1.0) / p / N * 1000,
                      np.where(T, n / p / sw_T, -n / p / sw_C) * 1000,
                      np.where(T, n / nT, -n / nC) * 1000])


def tune_test(df, t, rng):
    """Move the three estimates inside the test's intervals by flipping session outcomes (0 <-> 1):
    a bounded least-squares solve over flip types (arm, cell, renders, current outcome) aimed at a
    point inside every interval, rounded, then single flips until every estimate is inside."""
    from scipy.optimize import lsq_linear
    box = intervals(t)
    width = box[:, 1] - box[:, 0]
    free = width > 1e6
    aim = np.where(width < 1.0, box.mean(axis=1), box[:, 0] + 0.15)
    wt = np.where(free, 0.0, 1.0)
    y = df.y.to_numpy().astype(int).copy()
    d = _effects(df)
    key = df.arm.astype(str) + "|" + df.cell.astype(str) + "|" + df.n.astype(str) + "|"
    df.y = y
    est = np.array(arch_estimates(df)[:3])
    for attempt in range(10):
        types = (key + pd.Series(y, index=df.index).astype(str)).to_numpy()
        uniq, inv = np.unique(types, return_inverse=True)
        dy = np.where(y == 0, 1.0, -1.0)
        V = np.zeros((3, len(uniq)))
        avail = np.bincount(inv, minlength=len(uniq)).astype(float)
        first = np.zeros(len(uniq), int)
        first[inv[::-1]] = np.arange(len(inv))[::-1]
        V = d[:, first] * dy[first]
        gap = (aim - est) * wt
        Aw = V * wt[:, None]
        sol = lsq_linear(np.vstack([Aw, 0.02 * np.eye(len(uniq))]), np.concatenate([gap, np.zeros(len(uniq))]),
                         bounds=(np.zeros(len(uniq)), avail))
        x = np.floor(sol.x + rng.random(len(uniq))).astype(int)
        x = np.minimum(x, avail.astype(int))
        for j in np.flatnonzero(x):
            idx = np.flatnonzero(inv == j)
            pick = rng.choice(idx, size=x[j], replace=False)
            y[pick] += dy[pick].astype(int)
        df.y = y
        est = np.array(arch_estimates(df)[:3])
        # single-flip repair
        for it in range(400):
            inside = ((est >= box[:, 0]) & (est <= box[:, 1])).all()
            if inside:
                break
            dy = np.where(y == 0, 1.0, -1.0)
            cand = est[:, None] + d * dy[None, :]
            lo = np.maximum(0, box[:, 0][:, None] - cand)
            hi = np.maximum(0, cand - box[:, 1][:, None])
            sc = ((lo + hi) ** 2).sum(axis=0) + 1e-4 * (wt[:, None] * (cand - aim[:, None]) ** 2).sum(axis=0)
            cur = (np.maximum(0, box[:, 0] - est) + np.maximum(0, est - box[:, 1])) ** 2
            cur = cur.sum() + 1e-4 * (wt * (est - aim) ** 2).sum()
            i = int(np.argmin(sc))
            if sc[i] < cur:
                y[i] += int(dy[i])
                est = cand[:, i]
                continue
            # no single flip helps: the best pair among the 300 best single flips
            top = np.argsort(sc)[:300]
            pair = est[:, None, None] + (d[:, top] * dy[top])[:, :, None] + (d[:, top] * dy[top])[:, None, :]
            lo2 = np.maximum(0, box[:, 0][:, None, None] - pair)
            hi2 = np.maximum(0, pair - box[:, 1][:, None, None])
            s2 = ((lo2 + hi2) ** 2).sum(axis=0) + 1e-4 * (wt[:, None, None] * (pair - aim[:, None, None]) ** 2).sum(axis=0)
            np.fill_diagonal(s2, np.inf)
            a, b = np.unravel_index(int(np.argmin(s2)), s2.shape)
            if s2[a, b] >= cur:
                break
            for k in (top[a], top[b]):
                y[k] += int(dy[k])
            est = pair[:, a, b]
        if ((est >= box[:, 0]) & (est <= box[:, 1])).all():
            break
    df.y = y
    est = np.array(arch_estimates(df)[:3])
    assert ((est >= box[:, 0] - 1e-9) & (est <= box[:, 1] + 1e-9)).all(), (t["test_id"], est, box)
    return df


def hidden_layers(A):
    """Watched-listing in-session orders and follow-up orders over 21 days for each archived session,
    at exactly the same per-session rate in both arms of every cell: no archived ranker put a buyer's
    watched listing ahead of others, so in-session orders and orders over the test agree. Each cell
    holds a multiple of 100 sessions and each arm a whole number of hundredths of it, so a per-unit
    allotment makes the two arms' rates equal to the order."""
    rng = P.stream("archive-hidden")
    A = A.copy()
    A["watched_orders"] = 0
    A["followup_orders"] = 0
    for (tid, c), g in A.groupby(["test_id", "cell"]):
        unit = len(g) // 100
        rate_w = 0.0        # no archived ranker showed a buyer's watched listing
        rate_f = P.BG_RATE[c] * 21 + P.WATCH_LAMBDA[c] * P.ANYWAY_NUM / P.ANYWAY_DEN
        jw = int(round(rate_w * unit))
        jf = int(round(rate_f * unit))
        for arm, ga in g.groupby("arm"):
            m = len(ga)
            assert m % unit == 0, (tid, c, arm, m, unit)
            units = m // unit
            kw, kf = jw * units, jf * units
            A.loc[rng.choice(ga.index.to_numpy(), size=kw, replace=False), "watched_orders"] = 1
            base, rem = divmod(kf, m)
            per = np.full(m, base, int)
            per[rng.choice(m, size=rem, replace=False)] += 1
            A.loc[ga.index, "followup_orders"] = per
    return A
