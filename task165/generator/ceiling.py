"""task165 architecture 2: the cracker, the mirror and the full includer, run on the cut pack; the pair ceiling and
the mirror's leakage on the asks.

    cracker        lands the call (Alternative C) and is as careful on the asks as the battery and the filed
                   documents take it: exact duplicate tips dropped; each cal-check visit's tips removed over the
                   arrival-to-departure window the field log gives, read against the tips' own stamps; every tip at
                   the inventory's 0.01 in; the Northside returns from the pumps' run states at the O&M station curve,
                   or (its second try, the better of the two kept) from the level falls through Table 4-1.
    mirror         stops at the default path (Alternative B, the pumps' rating) and takes the cracker's ask paths.
    full includer  finds every device the asks carry: the TipLink loggers' UTC, the pours by their steady run, the
                   0.2 mm mechanism, the re-mounted transducer.
Scoring on supplemental-stumping Part 0: the call and its components 38, the instructions 7, the asks 55 shared
equally over the 53 ask figures (48 rainfall cells, 5 returned volumes). A cell is kept when it matches the golden
at the asked rounding.

    python3 ceiling.py [target]"""
import csv
import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G  # noqa: E402

TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
W_CALL, W_IF, W_ASK = 38.0, 7.0, 55.0
R_OFF = 5.0           # what a response off the call keeps of the call's 38 (the alternatives' table half right)
CURVE = {1: 4.0, 2: 7.4, 3: 10.2}


def pump_route(target):
    tot = {y: 0.0 for y in range(2021, 2026)}
    with open(os.path.join(target, "northside_tank_scada_2020-2025.csv"), newline="") as f:
        for r in csv.DictReader(f):
            y = int(r["Timestamp"][:4])
            n = int(r["NT_P1_RUN"]) + int(r["NT_P2_RUN"]) + int(r["NT_P3_RUN"])
            if n and y in tot:
                tot[y] += CURVE[n] / 96.0
    return tot


def keep1(a, gold):
    return sum(int(round(a[g][m] + 1e-9, 2) == round(gold[g][m] + 1e-9, 2)) for g in gold for m in range(12))


def keep2(a, gold):
    return sum(int(round(a[y] + 1e-9) == round(gold[y] + 1e-9)) for y in gold)


def main():
    gold1 = G.ask1(TARGET)
    gold2 = G.ask2(TARGET)[0]
    paths = {
        "cracker/mirror": (G.ask1(TARGET, handle_clock=False, pours="window", bucket=False),
                           max((pump_route(TARGET), G.ask2(TARGET, offset=False)[0]), key=lambda a: keep2(a, gold2))),
        "cracker, pours by steady run": (G.ask1(TARGET, handle_clock=False, pours="steady", bucket=False),
                                         G.ask2(TARGET, offset=False)[0]),
        "cracker, clocks found": (G.ask1(TARGET, handle_clock=True, pours="window", bucket=False),
                                  G.ask2(TARGET, offset=False)[0]),
        "cracker, pours kept": (G.ask1(TARGET, handle_clock=False, pours="keep", bucket=False),
                                pump_route(TARGET)),
        "full includer": (gold1, gold2),
    }
    n = 48 + 5
    rows = {}
    for name, (a1, a2) in paths.items():
        k1, k2 = keep1(a1, gold1), keep2(a2, gold2)
        rows[name] = (k1, k2, (k1 + k2) / n)
        print("%-32s rainfall %2d/48  returns %d/5  ask keep %.3f" % (name, k1, k2, (k1 + k2) / n))
    L = rows["cracker/mirror"][2]
    on = W_CALL + W_IF + W_ASK * L
    off = R_OFF + W_IF + W_ASK * L
    pair = (on + off) / 2
    print("cracker on the call %.1f; mirror off the call %.1f; pair %.1f; mirror leakage %.1f per cent of ask weight"
          % (on, off, pair, 100 * L))
    json.dump(dict(rows={k: list(v) for k, v in rows.items()}, pair=round(pair, 1), mirror_leak=round(100 * L, 1)),
              open(os.path.join(HERE, "ceiling.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
