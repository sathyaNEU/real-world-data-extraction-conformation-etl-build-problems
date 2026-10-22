"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call, runs the hygiene battery and executes every filed rule it is pointed at: it sums each
line's pounds (no rule says a line can carry its order's total). The mirror stops at the default path (one linking
distance, 200 feet, for every detection as Kerbline placed it) and reads every ask the natural way. A hit is a figure
inside half a unit of its stated rounding.

    python3 task478/generator/ceiling.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import methods as M   # noqa: E402

ORDER = [403, 407, 411, 402, 409, 405, 412, 414, 401, 406, 413, 404, 408, 410]
DEFAULT_FT = 200
W_REC, W_IF, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(p, route):
    """Every graded figure under one route: the call, the fourteen whole-number figures and the 28 ask figures."""
    g = M.golden(p)
    out = {}
    if route == "golden" or route == "cracker":
        est, call = g["est"], g["set"]
    else:
        est = M.single(p, DEFAULT_FT, g["road"])
        call = M.designated(est)
    out["call"] = tuple(call)
    for s in ORDER:
        out["est_%d" % s] = int(est[s] + 0.5)
    if route == "golden":
        a = M.ask_pounds(p)
    elif route == "cracker":
        a = M.ask_pounds(p, pounds="lines")
    else:
        a = M.ask_pounds(p, pounds="lines")
    for s in ORDER:
        out["A_lb_%d" % s] = a.get(s, 0)
    return out


def score(gold, resp):
    asks = [k for k in gold if k[:2] in ("A_", "B_")]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    ests = sum(1 for s in ORDER if resp["est_%d" % s] == gold["est_%d" % s])
    rec = W_REC if call and ests == len(ORDER) else R_WRONG if not call else W_REC * (0.4 + 0.6 * ests / len(ORDER))
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, ests


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    p = M.load(target)
    gold = figures(p, "golden")
    cr = figures(p, "cracker")
    mi = figures(p, "mirror")
    sc, kept_c, asks, call_c, est_c = score(gold, cr)
    sm, kept_m, _, call_m, est_m = score(gold, mi)
    print("ask figures: %d (A %d)" % (len(asks), sum(1 for k in asks if k[:2] == "A_")))
    for name, kept in (("cracker", kept_c), ("mirror", kept_m)):
        for ask in ("A",):
            ks = [k for k in asks if k.startswith(ask + "_")]
            hit = [k for k in ks if k in kept]
            print("%-8s ask %s: %d of %d kept %s" % (name, ask, len(hit), len(ks), " ".join(hit)))
    print("cracker: call %s, %d of 14 estimates, score %.1f" % (call_c, est_c, sc))
    print("mirror whole numbers kept: %d of 14" % est_m)
    print("mirror:  call %s, %d of 14 estimates, score %.1f" % (call_m, est_m, sm))
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(kept_m) / len(asks)))
    return (sc + sm) / 2, 100.0 * len(kept_m) / len(asks), kept_c, kept_m


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
