"""Scales each group's base cost (world.GROUPS) until the golden cost per member-month lands at world.DESIRED, then
prints every route.     python3 tune.py [iterations]"""
import importlib
import re
import sys

import numpy as np

import sources as S
import world as W


def main(it):
    for _ in range(it):
        ms = S.members(np.random.default_rng(W.SEED))
        g = S.pmpm(ms, "golden")
        src = open(W.__file__).read()
        for k, (name, county, n0, base, *rest) in W.GROUPS.items():
            nb = round(base * W.DESIRED[k] / g[k], 2)
            src = re.sub(r'("%s": \("[^"]+", "[^"]+", %d, )[0-9.]+' % (k, n0), r"\g<1>%s" % nb, src)
        open(W.__file__, "w").write(src)
        importlib.reload(W)
        importlib.reload(S)
    ms = S.members(np.random.default_rng(W.SEED))
    r = {k: S.pmpm(ms, k) for k in ("golden", "roster", "retro", "orphan")}
    for k in W.GROUPS:
        print(k, " ".join("%s %.2f" % (x, r[x][k]) for x in r))
    for x in r:
        print(x, sorted(k for k in r[x] if r[x][k] >= W.BENCHMARK))


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 4)
