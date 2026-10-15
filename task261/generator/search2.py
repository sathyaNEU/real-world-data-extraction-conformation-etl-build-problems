"""Random design search across the core's free parameters (stream-preserving) and the tuning factors, scored on the
ladder's constraints with margins: the golden only on the older partner with the difference on the replicates."""
from __future__ import annotations

import multiprocessing as mp
import sys

import numpy as np

import common as K
import tune as T
from search import light


def evaluate(cfg):
    design = dict(seed=cfg["seed"], ref_younger_p=cfg["ryp"], gap_mean=cfg["gap"], common_sd=cfg["csd"],
                  specific_sd=np.array([0.5, 0.5, 0.5, cfg["s34"], cfg["s34"], 0.5]))
    k = (1, 1, 1, cfg["k3"], cfg["k4"], cfg["k5"])
    o = T.routes(light(k, (0.0, cfg["sd5"]), design), nboot=80)
    c, q, s, b = o["older"]["zc"], o["older"]["zq"], o["older"]["zs"], o["older"]["zb"]
    rc, rq, rs = o["ref"]["zc"], o["ref"]["zq"], o["ref"]["zs"]
    m = dict(gold_apart=min(c[:4]) - 2.3, gold_merge=1.65 - abs(c[4]), def_q3=1.65 - q[3], def_q4=1.65 - abs(q[4]),
             def_young=min(q[:3]) - 2.1,
             srs=min(max(1.7 - s[3], abs(s[4]) - 2.3), max(1.7 - b[3], abs(b[4]) - 2.3)),
             refc=max(abs(rc[4]) - 2.3, 1.7 - rc[3], 1.7 - rc[2]),
             refq=max(1.7 - rq[3], 1.7 - rq[2], abs(rq[4]) - 2.3))
    return min(m.values()), cfg, {kk: round(v, 2) for kk, v in m.items()}, dict(c=np.round(c, 2), q=np.round(q, 2),
                                                                                s=np.round(s, 2), b=np.round(b, 2),
                                                                                rc=np.round(rc, 2), rq=np.round(rq, 2))


if __name__ == "__main__":
    r = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    cfgs = []
    for _ in range(n):
        cfgs.append(dict(seed=int(r.integers(1, 400)), ryp=float(r.uniform(0.6, 0.85)),
                         gap=float(r.uniform(3.0, 4.8)), csd=float(r.uniform(0.6, 0.95)),
                         s34=float(r.uniform(0.1, 0.5)), k3=float(r.uniform(0.95, 1.1)), k4=float(r.uniform(1.05, 1.3)),
                         k5=float(r.uniform(1.0, 1.3)), sd5=float(r.uniform(0.0, 0.8))))
    with mp.Pool(4) as pool:
        res = pool.map(evaluate, cfgs)
    res.sort(key=lambda x: -x[0])
    for sc, cfg, m, z in res[:6]:
        print("%.3f" % sc, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in cfg.items()}, m)
        print("     ", z)
