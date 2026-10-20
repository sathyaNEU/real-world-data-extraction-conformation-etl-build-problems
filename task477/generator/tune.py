"""Moves world.ADJ (each Tallis sector's growth target) until the golden on the cut record lands at world.DESIRED, and
reports the slate margins, every family member's slate and each graded growth's distance to its rounding edge.

    python3 task477/generator/tune.py [iterations]
"""
import importlib
import re
import sys

import methods as M
import pack as P
import sources as S
import world as W


def record():
    P.everything.cache_clear()
    x = P.everything()
    cl = P.cells(x)
    rec = {}
    for (fips, own, ind, agg, y, q), c in cl.items():
        if fips == W.COUNTY_FIPS and own == "5" and agg == "74" and c["disclosed"]:
            rec.setdefault(ind, {})[(y, q)] = (float(c["wages"]), tuple(c["m"]))
    return {k: v for k, v in rec.items() if len(v) == 52}


def report(rec):
    R = {n: M.route(rec, n) for n in M.FAMILY + M.WRONG}
    g = R["golden"]
    for n in M.FAMILY + M.WRONG:
        sl, ru = M.slate(R[n])
        o = sorted(R[n], key=lambda s: -R[n][s])
        print("%-9s %s next %s gap %.2f" % (n, sl, ru, 100 * (R[n][o[3]] - R[n][o[4]])))
    spread = {s: 100 * (max(R[n][s] for n in M.FAMILY) - min(R[n][s] for n in M.FAMILY)) for s in g}
    edge = {s: .5 - abs(100 * g[s] - round(100 * g[s])) for s in g}
    for s in sorted(g):
        print("%-6s golden %6.2f spread %.2f edge %.2f paid %6.2f" % (s, 100 * g[s], spread[s], edge[s], 100 * R["paid"][s]))
    return R


def main(it):
    for _ in range(it):
        rec = record()
        g = M.route(rec, "golden")
        adj = dict(W.ADJ)
        for s, d in W.DESIRED.items():
            adj[s] = round(adj.get(s, 0.0) + (d / 100 - g[s]) * 1.0, 5)
        src = open(W.__file__).read()
        src = re.sub(r"ADJ = \{.*?\}", "ADJ = %r" % dict(sorted(adj.items())), src, flags=re.S)
        open(W.__file__, "w").write(src)
        importlib.reload(W)
        for mod in (S, M, P):
            importlib.reload(mod)
    report(record())


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
