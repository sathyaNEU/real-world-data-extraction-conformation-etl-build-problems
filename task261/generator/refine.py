import multiprocessing as mp, sys
import numpy as np
from search2 import evaluate
best = dict(seed=312, ryp=0.796, gap=3.218, csd=0.892, s34=0.32, k3=1.052, k4=1.09, k5=1.142, sd5=0.56)
r = np.random.default_rng(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
cfgs = [best]
for _ in range(int(sys.argv[2]) if len(sys.argv) > 2 else 400):
    c = dict(best)
    for k in ("ryp", "gap", "csd", "s34", "k3", "k4", "k5", "sd5"):
        c[k] = float(best[k] * np.exp(r.normal(0, 0.06)))
    c["ryp"] = min(c["ryp"], 0.85)
    cfgs.append(c)
if __name__ == "__main__":
    with mp.Pool(4) as pool:
        res = pool.map(evaluate, cfgs)
    res.sort(key=lambda x: -x[0])
    for sc, cfg, m, z in res[:5]:
        print("%.3f" % sc, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in cfg.items()}, m)
        print("     ", z)
