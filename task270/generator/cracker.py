"""task270 ask-layer arithmetic measured on the cut pack: the figures the cracker (lands the call, runs the hygiene
battery, executes every filed rule) and the mirror (stops at the station replay) keep on each ask, and the pair ceiling.

The battery merges each firefighter's overlapping bookings into one spell (consecutive and overlapping spells merged)
and dates roles by the role changes sheet (an effective-dated map). On the incident records it drops exact duplicates
(there are none) or, the stricter reflex, keeps one false alarm per premises a day. Both crackers are scored; the gate
takes the worse. The asks read none of the call's construction, so the mirror's ask readings are the cracker's.

    python3 task270/generator/cracker.py <target>"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402

ASK_WEIGHT, REC_WEIGHT, IF_WEIGHT, REC_KEPT_OFF_CALL = 55.0, 38.0, 7.0, 5.0


def kept(target):
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    P = C.Pack(target)
    a_union = C.ask_a(target, P, how="union", roles="dated")
    out = {}
    for name, dedupe in (("cracker, every record", "none"), ("cracker, one alarm a premises a day", "day")):
        c = C.ask_c(target, P, dedupe=dedupe)
        ka = sum(C.hm(a_union[s][0]) == F["ask_a"][s]["off_run_4plus"] for s in C.RURAL_STATIONS) + \
            sum(C.hm(a_union[s][1]) == F["ask_a"][s]["no_oic"] for s in C.RURAL_STATIONS)
        kc = sum(str(c[d][0]) == F["ask_c"][d]["actuations"] for d in K.DISTRICTS) + \
            sum("%.1f" % K.round_half_up(c[d][1], 1) == F["ask_c"][d]["per_100"] for d in K.DISTRICTS)
        out[name] = (ka, kc)
    return out, 2 * len(C.RURAL_STATIONS), 2 * len(K.DISTRICTS)


def main(target):
    k, na, nc = kept(target)
    n = float(na + nc)
    worst = max(sum(v) for v in k.values())
    for name, (ka, kc) in k.items():
        print("%-38s Ask A %d of %d, Ask C %d of %d" % (name, ka, na, kc, nc))
    c = REC_WEIGHT + IF_WEIGHT + ASK_WEIGHT * worst / n
    s = REC_KEPT_OFF_CALL + IF_WEIGHT + ASK_WEIGHT * worst / n
    both = REC_WEIGHT + IF_WEIGHT + ASK_WEIGHT * worst / n
    print("cracker %.1f  mirror %.1f  pair %.1f  (both on the call %.1f)" % (c, s, (c + s) / 2, both))
    print("mirror leakage %.1f per cent of ask weight" % (100.0 * worst / n))
    return 0 if (c + s) / 2 <= 60.0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
