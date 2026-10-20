"""Calibration (run by hand, never by the build): set each hospital's true mortality relative to expected so that its
golden ratio sits at its target, mid-bin at one decimal, and print every route and reading so the ladder's sets and
margins can be read. Prints the theta values to carry into world.HOSPITALS.

    python3 task468/generator/calibrate.py
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import methods as M   # noqa: E402
import sim as S       # noqa: E402
import world as W     # noqa: E402


def golden_ratios(theta):
    x = S.simulate(theta)
    f = M.frame_from_truth(x)
    return M.ratios(f, M.deaths(f)), x, f


def main(rounds=24, start=None):
    theta = start or {h[0]: h[7] for h in W.HOSPITALS}
    best = (9.0, dict(theta))
    for k in range(rounds):
        g, x, f = golden_ratios(theta)
        dist = {h: abs(g[h] - W.TARGET[h]) for h in W.CANDIDATES}
        worst = max(dist.values())
        if worst < best[0]:
            best = (worst, dict(theta))
        print("round %d: worst distance from target %.4f (%s)" % (k, worst, max(dist, key=dist.get)))
        if worst < 0.006:
            break
        step = 0.6 if k < 6 else 0.35
        for h in W.CANDIDATES:
            if dist[h] > 0.004:
                theta[h] = round(theta[h] * (W.TARGET[h] / g[h]) ** step, 4)
    print("best %.4f" % best[0])
    print(json.dumps(best[1]))
    return best[1]


if __name__ == "__main__":
    main(start=json.loads(sys.argv[1]) if len(sys.argv) > 1 else None)
