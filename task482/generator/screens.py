"""task482 architecture 17: the six go/no-go screens over 20 redraws. The pool and the drafts stay fixed; each redraw
re-draws the schools' terms, sequences and sitting days, the candidates and their responses, and re-runs the
bank, the golden, its variants and every rival route. Writes screens.json, which checks.py reads."""
import json
import os
import sys

import numpy as np

import core as C
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = list(range(9000, 9020))


def main():
    pl = W.pool()
    dr = C.compose(pl)
    res = {}
    for sd in SEEDS:
        w = W.world(seed=sd, pl=pl, light=True)
        bb, _ = C.bank_run(w)
        rv = C.rivals(w, bb, dr)
        for k, v in rv.items():
            res.setdefault(k, {"picks": "", "marks": []})
            res[k]["picks"] += C.pick(v)
            res[k]["marks"].append([round(v[d], 3) for d in "ABC"])
    out = {}
    for k, v in res.items():
        mk = np.array(v["marks"])
        out[k] = {"picks": v["picks"], "mean": [round(float(x), 2) for x in mk.mean(0)],
                  "sd": [round(float(x), 2) for x in mk.std(0)]}
        print(k.ljust(18), v["picks"], out[k]["mean"])
    with open(os.path.join(HERE, "screens.json"), "w") as fh:
        json.dump({"seeds": SEEDS, "routes": out}, fh, indent=1, sort_keys=True)
        fh.write("\n")


if __name__ == "__main__":
    sys.exit(main())
