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


def truth_record(x):
    """The routes' record built from the clean truth, as bundle.record builds it from the cut pack."""
    m = x["on"] & S.IN_SEASON
    idx = np.where(m)[0]
    pos = {h: i for i, h in enumerate(idx)}
    nox = np.where(x["out"], np.nan, x["lb"])
    rt = lambda h: None if h < 0 or h >= S.NH or not x["on"][h] or np.isnan(nox[h]) else float(nox[h] / x["heat"][h])
    blocks, h = [], 0
    a = x["air"] & m
    while h < S.NH:
        if a[h]:
            k = h
            while k + 1 < S.NH and a[k + 1]:
                k += 1
            blocks.append((pos[h], pos[k], rt(h - 1), rt(k + 1)))
            h = k
        h += 1
    return dict(load=list(x["load"][m]), nox=[None if np.isnan(v) else float(v) for v in nox[m]],
                since=list(x["since"][m]), heat=list(x["heat"][m]), air=list(a[m]), blocks=blocks)


def record():
    f = S.fleet(np.random.default_rng(W.SEED))
    return {u: truth_record(f[u]) for u in W.CC}, f


def main(it):
    for _ in range(it):
        rec, _f = record()
        adj = dict(W.ADJ)
        for u, d in W.DESIRED.items():
            g = M.rate(rec[u], "golden")
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
