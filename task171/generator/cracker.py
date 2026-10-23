"""The cracker and the mirror on the cut pack, and the pair ceiling on supplemental-stumping Part 0's weights
(the call and its components 38, instructions 7, asks 55 over the 22 ask figures; a response off the call keeps 5).

The cracker lands the call (it matures the in-state invoices on each plate's registration expiry), runs the hygiene
battery and executes every filed rule: it nets returned payments, counts a vehicle read twice in the express lanes
within a second once, applies each payment to the invoice it names, toll first, and cuts the payments at 31 October
2026. The mirror stops off the call (it matures invoices by their age) and takes the violation lines and payments at
face value."""
from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import solve         # noqa: E402

T = os.path.join(C.TASK, "target")


def ask_a(F, V, careful):
    keep = ~V.straddle if careful else np.ones(len(V), bool)
    ok = V[keep]
    ok = ok[(ok.crossed_at >= "2026-01-01") & (ok.crossed_at < "2026-10-01")]
    g = ok.groupby(ok.crossed_at.dt.month).agg(n=("toll", "size"), toll=("toll", "sum"))
    return {int(mo): (int(r.n), round(float(r.toll), 2)) for mo, r in g.iterrows()}


def ask_b(F, V, careful):
    IV = F["IV"]
    owed = V[~V.straddle].groupby("invoice_no").toll.sum() if careful else V.groupby("invoice_no").toll.sum()
    tp = solve.toll_paid(F, whole_account=False)
    d = IV.assign(owed=IV.invoice_no.map(owed).fillna(0.0), tp=tp)
    d["got"] = np.minimum(d.tp, d.owed)
    d = d[(d.invoice_type == "VIOLATION") & (d.plate_state != C.HOME)]
    out = {}
    for q, a, b in solve.QUARTERS:
        s = d[(d.issued_on >= a) & (d.issued_on < b)]
        out[q] = int(round(float(s.got.sum() / s.owed.sum()) * 100))
    return out


def score(fig, A, B):
    hits = 0
    for mo in range(1, 10):
        n, t = A.get(mo, (None, None))
        hits += int(n == fig["a_2026_%02d_crossings" % mo])
        hits += int(t is not None and abs(t - fig["a_2026_%02d_toll_owed_usd" % mo]) < 0.005)
    for q, v in B.items():
        hits += int(v == fig["b_%s_collected_pct" % q.lower()])
    return hits


def main(quiet=False):
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    F = solve.frames(T)
    V = solve.straddle_and_phantom(F)
    n_ask = 22
    ca, cb = ask_a(F, V, True), ask_b(F, V, True)
    ma, mb = ask_a(F, V, False), ask_b(F, V, False)
    ch, mh = score(fig, ca, cb), score(fig, ma, mb)
    cracker = 38 + 7 + 55 * ch / n_ask
    mirror = 5 + 7 + 55 * mh / n_ask
    out = dict(cracker_hits=ch, mirror_hits=mh, cracker=round(cracker, 1), mirror=round(mirror, 1),
               pair=round((cracker + mirror) / 2, 1), mirror_leakage_pct=round(100 * mh / n_ask, 1),
               cracker_A=ca, cracker_B=cb, mirror_B=mb)
    if not quiet:
        print(json.dumps(out, indent=1, default=str))
    return out


if __name__ == "__main__":
    main()
