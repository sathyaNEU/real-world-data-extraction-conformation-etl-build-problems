"""Every owed figure, computed from the pack by solve.py and written to figures.json for figures_check.py."""
import json

import numpy as np

import params as P
import solve as SV

QUARTER_LABEL = {"2025Q4": "October to December 2025", "2026Q1": "January to March 2026",
                 "2026Q2": "April to June 2026", "2026Q3": "July to September 2026"}


def tenth(x):
    return float(np.floor(x * 10.0 + 0.5) / 10.0)


def compute(target):
    R = SV.call(target)
    g = R["routes"]["golden"]
    duties = {}
    for code, name in SV.NAMES.items():
        x, m = g[code], R["fits"][(code, "adl10")]
        duties[code] = dict(
            name=name,
            beta=round(float(m["beta"]), 3), lam=round(float(m["lam"]), 3),
            eps=[round(float(e), 3) for e in x["eps"]],
            litres_k=round(float(np.sum(x["q0"])) / 1000.0, 1),
            shelf=round(float(x["p0"]), 2), producer=round(float(x["c"]), 2),
            rate27=round(float(x["d27"]), 4), cut=round(float(x["cut"]), 4),
            new_rate=round(float(x["d27"] - x["cut"]), 4),
            rate27_2dp=round(float(x["d27"]), 2), new_rate_2dp=round(float(x["d27"] - x["cut"]), 2),
            cut_1dp=round(float(x["cut"]), 1),
            wedge_share=round(float(x["wedge_share"]), 3),
            extra_litres_k=round(float(np.sum(x["q1"] - x["q0"])) / 1000.0, 1),
            eb_k=int(round(x["gain"] / 1000.0)), eb_m=tenth(x["gain"] / 1e6), eb=float(x["gain"]))
    w, r = R["winner"], R["runner"]
    A = SV.asks(target)
    asks = {c: {q: SV.thousand(A[c][q]) for q in P.ASK_QUARTERS} for c in SV.NAMES}
    routes = {k: {c: round(v[c]["gain"] / 1e6, 3) for c in SV.NAMES} for k, v in R["routes"].items()}
    F = dict(winner=w, winner_name=SV.NAMES[w], runner=r, runner_name=SV.NAMES[r],
             winner_m=tenth(g[w]["gain"] / 1e6), runner_m=tenth(g[r]["gain"] / 1e6),
             order=R["order"], duties=duties, envelope_m=P.ENVELOPE / 1e6, gst_pct=int(round(P.GST * 100)),
             uprate_pct=int(round((P.UPRATE_2027 - 1) * 100)),
             asks_k=asks, asks_exact=A, routes=routes,
             first_quarter=SV.series(target)[w]["quarters"][0], quarters=len(SV.series(target)[w]["quarters"]),
             codes=[4071, 6171, 7171])
    return F


def write(F, path):
    keep = {k: v for k, v in F.items() if k != "asks_exact"}
    keep["asks_exact"] = {c: {q: round(v, 2) for q, v in d.items()} for c, d in F["asks_exact"].items()}
    with open(path, "w") as fh:
        json.dump(keep, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
