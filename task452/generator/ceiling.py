"""Pair ceiling on the cut pack: scores the cracker (on the call) and the mirror (off it, on the stack-test route)
against the golden figures, each ask figure scored by what that response's own handling computes from target/.

Rubric model (supplemental-stumping Part 0): 38 for the call and its components, 7 for instruction-following,
55 spread evenly over the ask figures; a figure is kept when the response's value rounds to the golden's.

    python3 task452/generator/ceiling.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A        # noqa: E402

TGT = os.path.join(os.path.dirname(HERE), "target")


def rh(x):
    return int(math.floor(x + 0.5))


def ask_values(route):
    """The ask figures a response computes on its own route."""
    out = {}
    if route == "journal_feed_events":
        # the careful route through the journal: start-of-log states, mill TRIP as a stop, the clock change handled,
        # the kiln's state followed through its FEED ON and FEED OFF lines
        a1 = A.ask1(TGT, burner_trip_stops_feed=False)
        fe = A.ask_feed(TGT, burner_trip_stops_feed=False)
        d = {k: a1[k]["quarters"] for k in a1}
    elif route == "historian":
        d = A.ask1_historian(TGT)
        fe = A.ask_feed_historian(TGT)
    else:   # the full includer: every device found and handled
        a1 = A.ask1(TGT)
        d = {k: a1[k]["quarters"] for k in a1}
        fe = A.ask_feed(TGT)
    for k in ("K1", "K2"):
        for q in range(4):
            out["direct_h_%s_Q%d" % (k, q + 1)] = rh(d[k][q])
            out["feed_h_%s_Q%d" % (k, q + 1)] = "{:,}".format(rh(fe[k][q]))
    if route == "full":
        nox = A.ask2(TGT)
    else:
        # the logger found for the May hole and read on the historian's 10 per cent oxygen basis
        nox = A.ask2(TGT, logger_converted_again=True)
    for k in ("K1", "K2"):
        out["nox_t_%s" % k] = rh(nox[k]["total"])
    return out


def score(figs, call_right, route):
    vals = ask_values(route)
    keys = sorted(vals)
    kept = [k for k in keys if vals[k] == figs[k]]
    ask_w = 55.0 * len(kept) / len(keys)
    call_w = 38.0 if call_right else 0.0
    return call_w + 7.0 + ask_w, len(kept), len(keys), kept


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    hg = A.mercury(TGT)
    dflt = A.default_route(TGT)
    call_cracker = rh(hg["K1"]["release"]) == figs["hg_K1_kg"]
    call_mirror = rh(dflt["K1"]["r0"]) == figs["hg_K1_kg"]
    rows = []
    for name, call, route in (("cracker (balance, journal route)", call_cracker, "journal_feed_events"),
                              ("mirror (stack tests, journal route)", call_mirror, "journal_feed_events"),
                              ("cracker (balance, historian route)", call_cracker, "historian"),
                              ("mirror (stack tests, historian route)", call_mirror, "historian"),
                              ("full includer (balance, every device handled)", call_cracker, "full")):
        s, n, N, kept = score(figs, call, route)
        rows.append((name, s, n, N, kept))
        print("%-48s %5.1f  asks kept %d of %d %s" % (name, s, n, N, kept))
    pair_j = (rows[0][1] + rows[1][1]) / 2
    pair_h = (rows[2][1] + rows[3][1]) / 2
    print("pair ceiling, journal route %.1f; historian route %.1f" % (pair_j, pair_h))
    print("mirror leakage, journal route %.1f per cent; historian route %.1f per cent"
          % (100.0 * rows[1][2] / rows[1][3], 100.0 * rows[3][2] / rows[3][3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
