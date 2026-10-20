"""Scales world.ADJ (each unit's start NOx) until the golden on the cut record lands at world.DESIRED, then reports
every route's rate and the margins against the target.

    python3 task474/generator/tune.py [iterations]
"""
import importlib
import re
import sys

import numpy as np

import methods as M
import sources as S
import world as W


def record():
    f = S.fleet(np.random.default_rng(W.SEED))
    rec = {}
    for u in W.CC:
        x = f[u]
        m = x["on"] & S.IN_SEASON
        rec[u] = dict(load=list(x["load"][m]), nox=[None if o else float(v) for o, v in zip(x["out"][m], x["lb"][m])],
                      since=list(x["since"][m]))
    return rec, f


def main(it):
    for _ in range(it):
        rec, _f = record()
        adj = dict(W.ADJ)
        for u, d in W.DESIRED.items():
            g = M.rate(rec[u], "golden")
            base = M.rate(dict(rec[u], nox=[v for v in rec[u]["nox"]]), "golden")
            a = adj.get(u, 1.0)
            # the start NOx carries roughly the part of the rate above the steady rate (about 0.04)
            adj[u] = round(float(max(.2, a * (d - .04) / max(1e-6, g - .04))), 5)
        src = open(W.__file__).read()
        src = re.sub(r"ADJ = \{.*?\}", "ADJ = %r" % dict(sorted(adj.items())), src, flags=re.S)
        open(W.__file__, "w").write(src)
        importlib.reload(W)
        importlib.reload(S)
        importlib.reload(M)
    rec, _f = record()
    print("unit   " + " ".join(r[:9].rjust(9) for r in M.FAMILY + M.WRONG))
    for u in rec:
        v = [M.rate(rec[u], r) for r in M.FAMILY + M.WRONG]
        print(u.ljust(6), " ".join("%9.4f" % x for x in v), " spread %.4f" % (max(v[:4]) - min(v[:4])))
    for r in M.FAMILY + M.WRONG:
        print(r.ljust(10), M.designated(rec, r))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
