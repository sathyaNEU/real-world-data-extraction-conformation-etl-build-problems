"""The MAT-R item bank and the item administrations behind every 2028 attempt (the exposure log).

The bank is a 2PL bank of 340 items in three content areas, dense in the middle and thin above about +1 logit.
Administrations follow the adaptive selection: the next item is drawn from the five unused items of the due content
area whose difficulty sits nearest the running estimate, and the running estimate closes on the attempt's final
estimate as items accrue. No response is logged here; the platform's sittings export holds the scores."""
import numpy as np

AREAS = ("NUM", "VER", "ABS")


def bank(rng):
    n = 340
    core = rng.normal(-0.45, 0.85, 300)
    tail = rng.uniform(1.15, 2.6, 40)
    b = np.concatenate([core, tail])
    order = rng.permutation(n)
    b = b[order]
    a = np.round(np.exp(rng.normal(0.18, 0.22, n)), 2)
    area = np.array([AREAS[i % 3] for i in range(n)])[rng.permutation(n)]
    ids = np.array(["R%04d" % i for i in rng.choice(np.arange(1000, 9999), n, replace=False)])
    intro = rng.choice(np.array(["2025-06-30", "2026-06-29", "2027-06-28", "2028-06-26"]), n, p=[0.42, 0.27, 0.2, 0.11])
    return dict(id=ids, b=np.round(b, 3), a=a, area=area, intro=intro)


def administer_all(rng, final_est, n_items, bk, start):
    """item indices shown in each attempt (attempts x 16, -1 past the attempt's last item), vectorised over attempts"""
    m = len(final_est)
    b = bk["b"]
    used = np.zeros((m, len(b)), bool)
    out = np.full((m, 16), -1, int)
    est = np.asarray(start, float).copy()
    area_idx = {a: np.where(bk["area"] == a)[0] for a in AREAS}
    for k in range(16):
        live = n_items > k
        if not live.any():
            break
        cols = area_idx[AREAS[k % 3]]
        d = np.abs(b[cols][None, :] - est[:, None])
        d[used[:, cols]] = np.inf
        near = np.argpartition(d, 5, axis=1)[:, :5]
        pick = near[np.arange(m), rng.integers(0, 5, m)]
        j = cols[pick]
        out[live, k] = j[live]
        used[np.arange(m)[live], j[live]] = True
        w = 1.0 - np.exp(-(k + 1) / 4.0)
        est = w * final_est + (1 - w) * start + rng.normal(0, 0.35 * (1 - w) + 0.05, m)
    return out
