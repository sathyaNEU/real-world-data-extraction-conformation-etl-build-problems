"""Tuning report (run by hand): every candidate 2020 tract's rates and z under each route, each neighbourhood's count
and the designated set per route.

    python3 tune.py"""
import acs as A
import geo as G
import methods as M
import world as W


def evaluate():
    ts = G.tracts()
    bge = A.bg_estimates(ts)
    tre = A.tract_estimates(ts, bge)
    rows = []
    for t in ts:
        if t.nbhd is None:
            continue
        tr18 = {t.code10: tre[(1, t.code10)]}
        par2 = tre[(1, t.code10)]
        split = len(t.children) > 1
        # the parent tested as a whole: 2019-23 children summed
        p2whole = M.proportion(*M.summed([tre[(2, c)] for c, _ in t.children]))
        p1whole = M.proportion(par2.x, par2.mx, par2.u, par2.mu)
        zwhole = M.z(*p1whole, *p2whole)
        for code, bgs in t.children:
            cur = tre[(2, code)]
            c = M.proportion(cur.x, cur.mx, cur.u, cur.mu)
            share = sum(b.u1 for b in bgs) / sum(b.u1 for b in t.bgs)
            r = dict(nb=t.nbhd, code=code, split=split, cur=c)
            for route in ("golden", "parent"):
                for ratio in (False, True):
                    e = M.earlier(route, code, [(t.code10, share)], [bge[(1, b.geoid10)] for b in bgs], tr18, ratio)
                    cc = M.proportion(cur.x, cur.mx, cur.u, cur.mu, ratio=ratio)
                    r[(route, ratio)] = (e, M.z(*e, *cc))
            # both periods from the block groups
            e = M.proportion(*M.summed([bge[(1, b.geoid10)] for b in bgs]))
            c2 = M.proportion(*M.summed([bge[(2, b.geoid20)] for b in bgs]))
            r["bgboth"] = (e, M.z(*e, *c2), c2)
            r["whole"] = zwhole
            rows.append(r)
    return rows


def verdicts(rows, key):
    out = {}
    for r in rows:
        if key == "whole":
            zz, cur = (r["whole"] if r["split"] else r[("parent", False)][1]), r["cur"][0]
        elif key == "drop":
            zz, cur = (-9 if r["split"] else r[("parent", False)][1]), r["cur"][0]
        elif key == "bgboth":
            zz, cur = r["bgboth"][1], r["bgboth"][2][0]
        elif key == "point":
            zz, cur = (9 if r["cur"][0] > r[("parent", False)][0][0] else -9), r["cur"][0]
        else:
            zz, cur = r[key][1], r["cur"][0]
        out[r["code"]] = cur >= W.THRESHOLD and zz > M.Z
    return out


def designated(rows, key):
    v = verdicts(rows, key)
    n = {}
    for r in rows:
        n[r["nb"]] = n.get(r["nb"], 0) + v[r["code"]]
    return sorted(k for k, c in n.items() if c >= W.MIN_TRACTS), n


if __name__ == "__main__":
    rows = evaluate()
    for r in rows:
        g, gz = r[("golden", False)]
        p, pz = r[("parent", False)]
        print("%-16s %s %s cur %.3f±%.3f  gold %.3f±%.3f z %5.2f (ratio %5.2f, bg %5.2f)  parent %.3f±%.3f z %5.2f  whole %5.2f" % (
            r["nb"], r["code"], "S" if r["split"] else " ", r["cur"][0], r["cur"][1], g[0], g[1], gz,
            r[("golden", True)][1], r["bgboth"][1], p[0], p[1], pz, r["whole"]))
    for key in (("golden", False), ("golden", True), "bgboth", ("parent", False), ("parent", True), "whole", "drop", "point"):
        s, n = designated(rows, key)
        print(key, s, n)
