"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call (every logger record carried through the lag fitted on the pilot overlaps) and every
store's hours, runs the hygiene battery (keys unique, exact repeats, every line joined, each quantity in its unit)
and executes every filed rule it is pointed at: section 8.2's balance over calendar 2026 with the counts as the year's
ends, every document that shows doses leaving the stock taken off (the write-offs as logged, Meridale's return
credits), and section 9.2's spend as each invoice once with its amount as exported, a route's amount to each of its
stores. The mirror stops at the default path (each logger's readings as the vaccine's temperature) and reads every
ask the same way. A hit is a figure inside half a unit of its stated rounding.

    python3 task482/generator/ceiling.py [target]
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
warnings.filterwarnings("ignore")

import bundle as B   # noqa: E402

W_REC, W_IF, W_ASK, R_WRONG = 38.0, 7.0, 55.0, 5.0


def figures(I, hours, a_kw, b_kw):
    out = {"call": tuple(B.covered(hours)), "near": B.nearest_below(hours)[0]}
    a = B.unaccounted(I, **a_kw)
    b = B.service(I, **b_kw)
    for no in I.order:
        out["h|%d" % no] = B.hround(hours[no])
        out["A|%d" % no] = int(a[no])
        out["B|%d" % no] = B.hround(b[no])
    return out


def score(gold, resp, order):
    asks = [k for k in gold if k[:2] in ("A|", "B|")]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    sh = sum(1 for no in order if resp["h|%d" % no] == gold["h|%d" % no])
    rec = W_REC if call and sh == len(order) else R_WRONG if not call else W_REC * (0.4 + 0.6 * sh / len(order))
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, sh


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    I = B.Inputs(target)
    g = B.golden_hours(I, B.taus(I))
    r0 = B.rung_hours(I, "R0")
    gold = figures(I, g, {}, {})
    ca, cb = dict(cut=False, vials=False, credits=True), dict(tax=False, split=False)
    rows = {"cracker": figures(I, g, ca, cb),
            "mirror": figures(I, r0, ca, cb),
            "cracker who reads the counts' times": figures(I, g, dict(ca, cut=True), cb),
            "cracker who reads the counts' times and the credits": figures(I, g, dict(cut=True, vials=False), cb),
            "cracker who finds the tax switch": figures(I, g, ca, dict(split=False)),
            "cracker who finds the tax switch and the routes": figures(I, g, ca, {})}
    out = {}
    for name, resp in rows.items():
        sc, kept, asks, call, sh = score(gold, resp, I.order)
        out[name] = (sc, kept, asks)
        ka = sum(1 for k in kept if k.startswith("A|"))
        kb = sum(1 for k in kept if k.startswith("B|"))
        print("%-52s call %-5s hours %2d/30  ask A %2d/30  ask B %2d/30  score %.1f" % (name, call, sh, ka, kb, sc))
    sc, sm = out["cracker"][0], out["mirror"][0]
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(out["mirror"][1]) / len(out["mirror"][2])))
    return (sc + sm) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
