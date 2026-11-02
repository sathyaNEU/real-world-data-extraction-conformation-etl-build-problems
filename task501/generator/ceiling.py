"""task501 ask layer against the careful solver's routes, on the cut pack, read against the prompt as filed.

    python3 task501/generator/ceiling.py [target] [--figures PATH]

The asks: for each pipe diameter the 2025-26 flushing programme flushed, the water it used per 100 m of main flushed in
2025 and in 2026 (10 figures); for each district whose supply the relining re-routes, the water used from November 2025
to October 2026 by the non-household customers it supplies (7 figures). Three devices on disjoint blocks:
- A-run (75, 100 and 150 mm, 6 figures): crew C14 books its standpipe meter's running display as each section's
  volume_m3 on nights from 1 December 2025; read plainly, every later section used 1.3 or more times what its hydrant
  passed at the gauge flow for the flush's minutes.
- A-twin (225 and 300 mm, 4 figures): crew C22 flushes those mains through two hydrants run together and writes one row
  per hydrant, each carrying the section's full length; read plainly, the section's metres are flushed twice in the
  same minutes.
- B-supply (7 figures): four large users are recorded in the DMA their premises sit in and supplied from the
  neighbouring DMA; read plainly, each uses more water in some hours than its recorded DMA's whole inflow.
The cracker lands the call, reads every field by its plain meaning (volume_m3 as the section's water,
section_length_m as the metres flushed, DMA as the district that supplies the premises), executes every filed rule
and runs the hygiene battery: re-sent rows dropped, both date layouts read, flushes past midnight timed across it,
months filtered to the window, the autumn repeated hour kept as a real hour, near-duplicate hydrant rows kept as
written (dropping either is printed as its own route and also misses). The mirror is the best response off the call
(the normal arrangement, six mains), scored at its strongest: every battery handling and at most one device cracked
beyond it, chosen against the answers. The full includer handles all three devices and must reproduce figures.json.
Pair on the sheet's weights: 38 recommendation and components, 7 instruction following, 55 for the 17 ask figures; a
wrong call keeps r = 19 (the six works peaks, the two flags it gets right and part of the chart), and each response
keeps 8 per cent of the ask weight it misses as method credit."""
import argparse
import hashlib
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S      # noqa: E402
import world as W      # noqa: E402

R_OFF = 19
CREDIT = 0.08


def r1(x):
    return "%.1f" % (np.floor(x * 10 + 0.5) / 10.0)


def score(figs, a, b):
    hits = {}
    for (dn, yr), v in a.items():
        hits["A %d mm %d" % (dn, yr)] = r1(v) == figs["flushing_water_m3_per_100m"]["%d mm %d" % (dn, yr)]
    for d in W.REROUTED:
        k = "%s %s" % (W.DCODE[d], W.DISTRICTS[d][1])
        hits["B " + k] = r1(b[W.DCODE[d]]) == figs["nonhousehold_water_ml"][k]
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default=os.path.join(os.path.dirname(HERE), "target"))
    ap.add_argument("--figures", default=os.path.join(HERE, "figures.json"))
    a = ap.parse_args()
    figs = json.load(open(a.figures, encoding="utf-8"))
    rer = [W.DCODE[d] for d in W.REROUTED]
    A = {h: S.ask_a(a.target, h)[0] for h in ("golden", "plain", "dedup", "running_only", "twin_only")}
    Bv = {h: S.ask_b(a.target, h, rer)[0] for h in ("golden", "plain", "corr")}
    n = 10 + 7
    rows = {
        "cracker (on the call, plain reading)": score(figs, A["plain"], Bv["plain"]),
        "cracker, near-duplicate hydrant rows dropped": score(figs, A["dedup"], Bv["plain"]),
        "mirror, A-run cracked": score(figs, A["running_only"], Bv["plain"]),
        "mirror, A-twin cracked": score(figs, A["twin_only"], Bv["plain"]),
        "mirror, B-supply cracked": score(figs, A["plain"], Bv["golden"]),
        "full includer (every device handled)": score(figs, A["golden"], Bv["golden"]),
    }
    for k, v in rows.items():
        print("%-46s %2d of %d ask figures" % (k, sum(v.values()), n))
    crack = max(sum(rows[k].values()) for k in rows if k.startswith("cracker")) / n
    mirror = max(sum(rows[k].values()) for k in rows if k.startswith("mirror")) / n
    full = sum(rows["full includer (every device handled)"].values())
    C = 38 + 7 + 55 * (crack + CREDIT * (1 - crack))
    Sx = R_OFF + 7 + 55 * (mirror + CREDIT * (1 - mirror))
    digest = hashlib.md5(b"".join(open(os.path.join(a.target, f), "rb").read()
                                  for f in sorted(os.listdir(a.target)))).hexdigest()
    print("pack digest %s" % digest)
    print("Cracker keep: %.1f per cent of ask weight" % (100 * crack))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * mirror))
    print("Pair ceiling: %.1f (C %.1f on the call, S %.1f off it)" % ((C + Sx) / 2, C, Sx))
    if crack > 0 or full != n:
        print("FAIL: the cracker keeps a figure or the full includer misses one")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
