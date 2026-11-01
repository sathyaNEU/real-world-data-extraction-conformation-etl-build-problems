"""The pair ceiling measured on the cut pack: the cracker (lands the call, runs the hygiene battery, executes every
filed rule; misses the master sample's pre-review region codes and the calls a tablet wrote twice) and the mirror
(the strong analyst's default path, final weights held fixed) priced against generator/figures.json.

    python3 task240/generator/ceiling.py [target]

Weights 38 / 7 / 55: the call side 38 (the warned set, the 48 coefficients of variation and their warnings),
instructions 7, the ask layer 55 over its 24 figures (each health region's response rate and calls to its addresses
with a full interview). A figure is kept when it prints in the golden's cell at the ask's rounding. A response off the
call keeps 8 of the call side (the cells its warnings share with the golden where the rubric grades them)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build as B   # noqa: E402
import estim as E   # noqa: E402

TASK = os.path.dirname(HERE)
CALL, INSTR, ASKS, OFF_CALL = 38.0, 7.0, 55.0, 8.0


def main(target=None):
    target = target or os.path.join(TASK, "target")
    X = E.solve(target, B.FILES)
    gold, g_rr, g_calls = X["warned"], X["rr"], X["calls"]
    hh, iss, out, cr = X["hh"], X["iss"], X["out"], X["cr"]
    n_fig = len(g_rr) + len(g_calls)
    paths = {
        "cracker": ("golden", dict(region="code", dedup=False)),
        "mirror (fixed weights)": ("fixed", dict(region="code", dedup=False)),
        "natural read (fixed weights)": ("fixed", dict(region="code", unworked=False, late=False, dedup=False)),
    }
    scores = {}
    for label, (route, kw) in paths.items():
        landed = X["routes"][route] == gold
        rr, calls = E.ask_files(hh, iss, out, cr, **kw)
        k = sum(round(rr[r], 1) == round(g_rr[r], 1) for r in g_rr) + sum(calls[r] == g_calls[r] for r in g_calls)
        s = (CALL if landed else OFF_CALL) + INSTR + ASKS * k / n_fig
        scores[label] = s
        print("%-30s call %-5s (%2d warned)  ask figures kept %2d of %d  ask share %4.1f%%  score %5.1f"
              % (label, landed, len(X["routes"][route]), k, n_fig, 100.0 * k / n_fig, s))
    pair = (scores["cracker"] + scores["mirror (fixed weights)"]) / 2
    print("pair ceiling %.1f" % pair)
    return pair


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
