"""The search that fixed world.SEED, world.TARGET and world.LEAK (run by hand; the build uses the constants):
the main call's acceptance criteria, then the asks' (the share mid-bin, the sub-metered read leaving every month's
loss positive and plausible).

    python3 task120/generator/tune.py <first seed> <last seed>
"""
import sys

import numpy as np

import asks as A
import world as WD


def asks_ok(W):
    final = A.meters(W)
    F = A.figures(W, final)
    edge = abs((F["share"] * 10) % 1 - 0.5) / 10            # distance to the x.x5 rounding edge, points
    nat = F["stops"][(True, True, True, True, "used")]["lost"]
    return edge >= 0.02 and nat.min() >= 2.5e6, F, edge, nat.min()


def main(a, b):
    for sd in range(a, b):
        for tg in [4_470_300.0 + 230.0 * k for k in range(8)]:
            W = WD.build(sd, tg)
            s = WD.summary(W)
            if not WD.acceptable(s):
                continue
            ok, F, edge, natmin = asks_ok(W)
            print(sd, tg, "gap %.3f r1 %.1f r2 %.1f r3 %.1f rank %d share %.3f edge %.3f natmin %.0f"
                  % (s["gap"], s["r1"], s["r2"], s["r3"], s["gold_prod_rank"], F["share"], edge, natmin), ok)
            if ok:
                return sd, tg
            break
    return None


if __name__ == "__main__":
    print(main(int(sys.argv[1]), int(sys.argv[2])))
