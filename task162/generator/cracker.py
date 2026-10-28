"""task162 ask-layer arithmetic measured on the cut pack: the figures the cracker (lands the call, runs the hygiene
battery, executes every filed rule) and the mirror (stops at the default rung) keep on each ask, and the pair ceiling.

The battery finds supply point references repeated in the property extract and identical lines in the billing
extract, and repairs both by reflex: each supply point counted once (the cracker), or every property record counted
(the mirror, which never checks the key), and identical bill lines dropped (both). Every filed rule is executed: the
certificate, the code history, NZ-TM, bills apportioned by days, the open boundary's days, NZ04's two inlets.

    python3 task162/generator/cracker.py <target>"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import world as W           # noqa: E402

ASK_WEIGHT, REC_WEIGHT, IF_WEIGHT, REC_KEPT_OFF_CALL = 55.0, 38.0, 7.0, 5.0
ROUTES = {"cracker": ("supply_points", "dedupe"), "mirror": ("rows", "dedupe")}


def kept(target):
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))["answers"]
    P = C.Pack(target, C.read_n1(target), C.read_settings(target))
    out = {}
    for who, (dwell, bills) in ROUTES.items():
        a = C.ask_a(P, W.NEAR, dwell)
        b = C.ask_b(target, bills)
        ka = sum("%.3f" % K.round_half_up(a[c], 3) == figs["ask_a"][c] for c in W.NEAR)
        kb = sum("%.2f" % K.round_half_up(b[k], 2) == figs["ask_b"][j]
                 for k, j in (("siv", "system_input"), ("unmeasured", "billed_unmetered"), ("real", "real_losses")))
        out[who] = {"A": ka, "B": kb}
    return out


def pair(k, both_on_call=False):
    n = 15.0
    c = REC_WEIGHT + IF_WEIGHT + ASK_WEIGHT * sum(k["cracker"].values()) / n
    s = (REC_WEIGHT if both_on_call else REC_KEPT_OFF_CALL) + IF_WEIGHT + ASK_WEIGHT * sum(k["mirror"].values()) / n
    return c, s, (c + s) / 2.0


def main(target):
    k = kept(target)
    c, s, p = pair(k)
    _, _, p2 = pair(k, both_on_call=True)
    print("cracker keeps A %d of 12, B %d of 3; mirror keeps A %d of 12, B %d of 3"
          % (k["cracker"]["A"], k["cracker"]["B"], k["mirror"]["A"], k["mirror"]["B"]))
    print("cracker %.1f  mirror %.1f  pair %.1f  (both on the call %.1f)" % (c, s, p, p2))
    print("mirror leakage %.1f per cent of ask weight" % (100.0 * sum(k["mirror"].values()) / 15.0))
    return 0 if p <= 60.0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
