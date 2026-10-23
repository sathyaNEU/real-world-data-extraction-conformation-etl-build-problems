"""The pair ceiling on the cut pack (supplemental-stumping Part 0, on its 38, 7 and 55 weights).

The cracker lands the call (each production day's outlet from the tests' relation at the day's inlet), runs the hygiene
battery (keys unique, exact repeats, every line joined, each weight read in its unit column) and executes every filed
rule it is pointed at: section 18-4-5(b) on the safety data sheet master's VOC for each cleaning material, the parts
washer tickets as the service record; the received inks, coatings and adhesives by ship date, each statement item on
Haldane's catalog, pounds by density. The mirror stops at the default path (each plant's latest test efficiency) and
reads every ask the same way. A hit is a figure inside half a unit of its stated rounding.

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


def figures(I, call, a_kw, b_kw):
    t = B.press_tons(I, "golden") if call == "golden" else B.rung_tons(I, call)
    out = {"call": tuple(B.covered(t))}
    a = B.cleaning_tons(I, **a_kw)
    b = B.unaccounted_gal(I, **b_kw)
    for n in I.order:
        v = t[n]["emitted"] if isinstance(t[n], dict) else t[n]
        out["tons|" + n] = B.hround(v)
        out["A|" + n] = B.round1(a[n])
        out["B|" + n] = B.hround(b[n])
    return out


def score(gold, resp, order):
    asks = [k for k in gold if k[:2] in ("A|", "B|")]
    kept = [k for k in asks if resp[k] == gold[k]]
    call = resp["call"] == gold["call"]
    sh = sum(1 for n in order if resp["tons|" + n] == gold["tons|" + n])
    rec = W_REC if call and sh == len(order) else R_WRONG if not call else W_REC * (0.4 + 0.6 * sh / len(order))
    return rec + W_IF + W_ASK * len(kept) / len(asks), kept, asks, call, sh


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    I = B.Inputs(target)
    gold = figures(I, "golden", {}, {})
    crack_a, crack_b = dict(vintage=False, stellar=False), dict(chain=False)
    rows = {"cracker": figures(I, "golden", crack_a, crack_b),
            "mirror": figures(I, "R0", crack_a, crack_b),
            "cracker who reads the revision log": figures(I, "golden", dict(stellar=False), crack_b),
            "cracker who reads the revision log and the payment lines": figures(I, "golden", {}, crack_b),
            "cracker who walks the replaces column": figures(I, "golden", crack_a, {})}
    out = {}
    for name, resp in rows.items():
        sc, kept, asks, call, sh = score(gold, resp, I.order)
        out[name] = (sc, kept, asks)
        ka = sum(1 for k in kept if k.startswith("A|"))
        kb = sum(1 for k in kept if k.startswith("B|"))
        print("%-58s call %-5s tons %2d/14  ask A %2d/14  ask B %2d/14  score %.1f" % (name, call, sh, ka, kb, sc))
    sc, sm = out["cracker"][0], out["mirror"][0]
    print("Pair ceiling: %.1f" % ((sc + sm) / 2))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * len(out["mirror"][1]) / len(out["mirror"][2])))
    return (sc + sm) / 2


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
