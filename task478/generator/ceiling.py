"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call (each burner's tests carried to each 2026 month's heat content), runs the hygiene battery
(keys unique, exact and same-value repeats across one account's meters, every line and log row joined) and executes
every filed rule it is pointed at: plan 4.2's billed usage as the dictionary names it (USAGE_THERMS, the usage billed
for the period), each combined account's repeated usage taken once, spread over its read days; guidance 6's time run as
the logs record it at each engine's permitted rating and tier. The mirror stops at the default path (each burner's
latest test) and reads every ask the same way. Two reader-calibrated rows price what a response that reconciles the
billed usage against the plan units' fuel, and the logs against the hour meters, keeps. A hit is a figure inside half a
unit of its stated rounding.

    python3 task478/generator/ceiling.py [target]
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import bundle as B   # noqa: E402

W_REC, W_IF, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(target, call, gas, eng):
    I = B.Inputs(target)
    t = B.facility_tons(I, call)
    out = {"call": tuple(B.five(t))}
    g = B.gas_2026(target, gas)
    e = B.engine_lb(target, eng)
    for n in B.ORDER:
        out["tons|" + n] = B.hround(t[n])
        out["A|" + n] = B.hround(g[n])
        out["B|" + n] = B.hround(e[n])
    return out


def score(gold, resp):
    asks = [k for k in gold if k[:2] in ("A|", "B|")]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    sh = sum(1 for n in B.ORDER if resp["tons|" + n] == gold["tons|" + n])
    rec = W_REC if call and sh == len(B.ORDER) else R_WRONG if not call else W_REC * (0.4 + 0.6 * sh / len(B.ORDER))
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, sh


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    gold = figures(target, "golden", "golden", "golden")
    rows = {"cracker": figures(target, "golden", "as_labelled_dedupe", "naive"),
            "mirror": figures(target, "latest", "as_labelled_dedupe", "naive"),
            "validating cracker (usage against the units' fuel, logs against the meters)":
                figures(target, "golden", "golden", "no_bank"),
            "validating mirror": figures(target, "latest", "golden", "no_bank")}
    out = {}
    for name, resp in rows.items():
        sc, kept, asks, call, sh = score(gold, resp)
        out[name] = (sc, kept, asks)
        ka = sum(1 for k in kept if k.startswith("A|"))
        kb = sum(1 for k in kept if k.startswith("B|"))
        print("%-76s call %-5s tons %2d/14  ask A %2d/14  ask B %2d/14  score %.1f" % (name, call, sh, ka, kb, sc))
    sc, sm = out["cracker"][0], out["mirror"][0]
    vc = out["validating cracker (usage against the units' fuel, logs against the meters)"][0]
    vm = out["validating mirror"][0]
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(out["mirror"][1]) / len(out["mirror"][2])))
    print("Validating pair (one on the call): %.1f" % ((vc + vm) / 2))
    return (sc + sm) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
