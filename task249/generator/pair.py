"""The cracker and the mirror scored on the cut pack (supplemental-stumping Part 1.1): the cracker lands the call, runs
the hygiene battery and executes every filed rule; the mirror stops at the sign-in split and takes the asks the same
way (they do not turn on the call).  Each ask figure is a hit within half a unit of its rounding.  Weights 38 / 7 / 55 (Part 0)."""
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import params as P
import solve as S


def asks(tgt, nl_kw, sc_kw):
    nl = S.newsletter(tgt, B.FILES, **nl_kw)
    sc = S.sold_copies(tgt, B.FILES, **sc_kw).round()
    return {("nl", c): int(nl[c]) for c in P.CODES} | {("sc", c): int(sc[c]) for c in P.CODES}


def run(tgt, quiet=False):
    gold = asks(tgt, {}, {})
    paths = {
        "cracker (every hazard met, start dates and link additions as recorded)": ({"link_adds": None}, {"restore": None}),
        "mirror (off the call, the same asks)": ({"link_adds": None}, {"restore": None}),
        "over-cleaner (every link addition undone, the release's weeks moved)": ({"link_adds": "all"}, {"restore": "window"}),
        "lazy (the exports as they stand)": ({"groups_as_of": False, "status_as_of": False}, {"restore": None, "combi_addon": True}),
        "every device met": ({}, {}),
    }
    out = {}
    for name, (a, b) in paths.items():
        got = asks(tgt, a, b)
        hits = sum(abs(got[k] - gold[k]) <= 0.5 for k in gold)
        out[name] = hits
        if not quiet:
            print("%-72s keeps %2d of %d ask figures" % (name, hits, len(gold)))
    n = len(gold)
    c = 38 + 7 + 55 * out[list(paths)[0]] / n
    s = 5 + 7 + 55 * out[list(paths)[1]] / n
    pair = (c + s) / 2
    if not quiet:
        print("cracker %.1f, mirror %.1f, pair ceiling %.1f, mirror leakage %.1f per cent of ask weight" % (c, s, pair, 100 * out[list(paths)[1]] / n))
    return out, pair


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
