"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call (each station's weights put on the static basis through its loaded steer axles), runs the
hygiene battery (exact duplicates dropped) and executes every filed rule it is pointed at: local weekdays from the
stamps the dictionary gives as UTC, the plaza list by its dates with the 2025 schedule, violation code G, and each
citation at the tag's last toll entry before the stop (program 6.2).
The mirror stops at the default path (the gross as recorded) and reads every ask the same natural way. A hit is a
figure inside half a unit of its stated rounding.

    python3 task478/generator/ceiling.py [target]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import bundle as B   # noqa: E402

W_REC, W_IF, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(target, route):
    df = B.class9(B.read_wim(target))
    out = {}
    if route in ("golden", "cracker"):
        sh = B.shares(df, B.factors(df, B.read_tickets(target), "loaded"))
    else:
        sh = B.shares(df)
    out["call"] = tuple(B.five(sh))
    for c in B.CODES:
        out["share_%s" % c] = B.hround(sh[c])
    if route == "golden":
        wk = B.weekday_entries(target)
        ci = B.citations_by_section(target)
    else:
        # the battery's exact duplicates dropped, every stamp read as UTC as the dictionary gives the current host's,
        # each citation placed at its tag's last entry before the stop as program 6.2 says
        wk = B.weekday_entries(target, dedup="exact", clock="utc")
        ci = B.citations_by_section(target, "trip", dedup="exact", clock="utc")
    for c in B.CODES:
        out["A_cit_%s" % c] = ci[c]
        out["B_wk_%s" % c] = B.hround(wk[c])
    return out


def score(gold, resp):
    asks = [k for k in gold if k[:2] in ("A_", "B_")]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    sh = sum(1 for c in B.CODES if resp["share_%s" % c] == gold["share_%s" % c])
    rec = W_REC if call and sh == len(B.CODES) else R_WRONG if not call else W_REC * (0.4 + 0.6 * sh / len(B.CODES))
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, sh


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    gold = figures(target, "golden")
    cr = figures(target, "cracker")
    mi = figures(target, "mirror")
    sc, kept_c, asks, call_c, sh_c = score(gold, cr)
    sm, kept_m, _, call_m, sh_m = score(gold, mi)
    print("ask figures: %d (A %d, B %d)" % (len(asks), sum(1 for k in asks if k[:2] == "A_"),
                                            sum(1 for k in asks if k[:2] == "B_")))
    for name, kept in (("cracker", kept_c), ("mirror", kept_m)):
        for ask in ("A", "B"):
            ks = [k for k in asks if k.startswith(ask + "_")]
            hit = [k for k in ks if k in kept]
            print("%-8s ask %s: %d of %d kept %s" % (name, ask, len(hit), len(ks), " ".join(hit)))
    print("cracker: call %s, %d of 12 shares, score %.1f" % (call_c, sh_c, sc))
    print("mirror:  call %s, %d of 12 shares, score %.1f" % (call_m, sh_m, sm))
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(kept_m) / len(asks)))
    return (sc + sm) / 2, 100.0 * len(kept_m) / len(asks), kept_c, kept_m


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
