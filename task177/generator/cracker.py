"""task177 cracker: the ask layer's two measured responses on the cut pack, scored against figures.json.

    python3 task177/generator/cracker.py [<target>]

The cracker lands the call, runs the hygiene battery and executes every filed rule it points at: it counts each
conversation once (conversation_id, the dictionary's grain), in the month of its first session as the export
records it, employers by the employer channel, our own use by the console and the accounts typed staff. The mirror
stops on a wrong rung of the call and handles the asks the same way. Pair ceiling on supplemental-stumping Part 0's
weights (38 recommendation and components for a landed call, about 5 kept by a wrong one, 7 instruction-following,
55 asks)."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K   # noqa: E402

MONTHS = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December")


def score(e, o, fig):
    ge = [fig["ask_employers"][m] for m in MONTHS]
    go = [fig["ask_own"][m] for m in MONTHS]
    return sum(a == b for a, b in zip(e, ge)), sum(a == b for a, b in zip(o, go))


def main(target):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    D = K.load(target)
    fi = K.filed_inputs(target)
    total = 24
    paths = {
        "cracker (on the call; every filed rule, conversation grain, recorded month, channel and per-session type)":
            dict(own_bn=False, employer_utc=False, retyped=False),
        "mirror (off the call; the same handling of the asks)": dict(own_bn=False, employer_utc=False, retyped=False),
    }
    kept = {}
    for name, f in paths.items():
        e, o = K.ask_counts(D, bn=fi["bn"], **f)
        he, ho = score(e, o, fig)
        kept[name] = (he + ho) / total
        print("%-100s employers %2d of 12, own use %2d of 12" % (name, he, ho))
    print("one device found (for the record; neither measured response finds one):")
    for label, f in (("the own business number", dict(own_bn=True, employer_utc=False, retyped=False)),
                     ("the widget's UTC", dict(own_bn=False, employer_utc=True, retyped=False)),
                     ("the re-typed accounts", dict(own_bn=False, employer_utc=False, retyped=True)),
                     ("business number and UTC", dict(own_bn=True, employer_utc=True, retyped=False)),
                     ("business number and re-typed", dict(own_bn=True, employer_utc=False, retyped=True))):
        e, o = K.ask_counts(D, bn=fi["bn"], **f)
        he, ho = score(e, o, fig)
        print("   %-34s employers %2d of 12, own use %2d of 12" % (label, he, ho))
    lc = list(kept.values())[0]
    ls = list(kept.values())[1]
    c = 38 + 7 + 55 * lc
    s = 5 + 7 + 55 * ls
    print("Pair ceiling: %.1f (cracker %.1f, mirror %.1f)" % ((c + s) / 2, c, s))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
