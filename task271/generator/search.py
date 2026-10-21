"""The world search: build the world for each seed, run every estimator and route on each group's mothers, sisters
and daughters, and keep the seeds where the estimator family names the same groups with every member at least four
points from 30 per cent, every easy route names another set, and the clean truth names the family's set.

    python3 search.py FIRST LAST [WORKERS]      prints one JSON line per seed"""
import os
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import json             # noqa: E402
import sys              # noqa: E402
import warnings         # noqa: E402
from multiprocessing import Pool   # noqa: E402

import numpy as np      # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K      # noqa: E402
import core as C        # noqa: E402
import models as M      # noqa: E402
import world as W       # noqa: E402

warnings.filterwarnings("ignore")
LINE = 0.30
MARGIN = 0.04


def evaluate(w, rates=None):
    rates = C.POP * 1e5 if rates is None else rates
    res = {}
    for code in K.CODES:
        a = W.fdr_female(w, code)
        t, ev, car, tested, alive = a.T
        pb = np.array([(int(np.floor(f["persons"][f["proband"]]["breast"])), 1) for f in w["families"]
                       if f["code"] == code], float)
        est = M.estimates(t, ev, np.where(tested == 1, car, 0), tested, alive, rates, pb[:, 0], pb[:, 1])
        est["truth"] = M.km(t[car == 1], ev[car == 1])
        res[code] = {k: float(v) for k, v in est.items()}
    return res


def verdicts(res, key):
    return frozenset(c for c in K.CODES if res[c][key] >= LINE)


def summary(seed):
    w = W.world(seed)
    res = evaluate(w)
    sets = {k: verdicts(res, k) for k in M.FAMILY + M.ROUTES + M.RECORDED + ("truth",)}
    gold = sets["kin"]
    fam_ok = all(sets[k] == gold for k in M.FAMILY) and sets["truth"] == gold
    worst = min((res[c][k] - LINE) if c in gold else (LINE - res[c][k]) for c in K.CODES for k in M.FAMILY)
    wrong_ok = all(sets[k] != gold for k in ("default", "naive", "relshare", "sloppy", "kin_testedneg"))
    return dict(seed=seed, gold=" ".join(sorted(gold)), fam_ok=fam_ok, worst=round(worst, 4), wrong_ok=wrong_ok,
                **{k: " ".join(sorted(sets[k])) for k in M.ROUTES + M.RECORDED},
                values={c: {k: round(res[c][k], 4) for k in M.FAMILY + M.ROUTES + M.RECORDED + ("truth",)} for c in K.CODES})


if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    with Pool(workers) as pool:
        for r in pool.imap(summary, range(lo, hi)):
            print(json.dumps(r), flush=True)
