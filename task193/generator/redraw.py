"""Structural redraw screen, design evidence and not part of the build (build.py does not run it): rebuild the world
under 20 other seeds, each with its own placements, and count how often every route files the golden set of that
world. Run from the generator directory: python3 redraw.py"""
import collections
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import routes as RT
import world as W


def main(n=20):
    hits, sizes, fails = collections.Counter(), [], 0
    for i in range(n):
        W.SEED = 50000 + 17 * i
        import sim
        importlib.reload(sim)
        try:
            S = sim.run()
        except AssertionError:
            fails += 1
            continue
        oc = {(w, k): S["cmp"][(w, W.EVAL, k)] for w in W.COMPLIANCE for k in W.INDICATORS}
        sets = {r: RT.designate(S["limits"][r], oc) for r in S["limits"]}
        g = sets[RT.GOLDEN]
        sizes.append(len(g))
        for r, s in sets.items():
            hits[r] += (s == g)
    print("worlds built %d of %d (placement failed in %d)" % (n - fails, n, fails))
    for r in sorted(hits):
        print("  %-44s lands the golden set %2d" % (r, hits[r]))
    print("golden set sizes", sizes)


if __name__ == "__main__":
    main()
