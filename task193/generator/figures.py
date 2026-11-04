"""figures.json: every figure the write-up states, emitted from the golden computed on the cut pack."""
import math

import routes as RT
import world as W

EV = [e["label"] for e in W.EVENTS]


def s3(x):
    d = 3 - int(math.floor(math.log10(abs(x)))) - 1
    return ("%%.%df" % max(d, 0)) % round(x, d)


def figures(g, info):
    G = g["golden"]
    R0 = g["limits"]["R0 every background result"]
    rev_mw1 = sum(1 for (w, ei), r in g["rev"].items() if r and w == "MW-1" and ei in W.BG_EVENTS)
    rev_mw2 = sum(1 for (w, ei), r in g["rev"].items() if r and w == "MW-2" and ei in W.BG_EVENTS)
    rev_mw3 = sum(1 for (w, ei), r in g["rev"].items() if r and w == "MW-3" and ei in W.BG_EVENTS)
    window = {k: g["counts"]["R0 every background result"][k] for k in W.INDICATORS}
    f = {
        "call": g["resample"],
        "call_sentence": "Yes: the October 2026 event sends %s to verification resampling" % ", ".join(g["resample"]),
        "default_path_answer": g["sets"]["R0 every background result"],
        "limits": {k: s3(G[k]) for k in W.INDICATORS},
        "limits_unrounded": {k: round(G[k], 4) for k in W.INDICATORS},
        "background_n": dict(g["golden_n"]),
        "window_n": window,
        "reversed_events": {"MW-1": rev_mw1, "MW-2": rev_mw2, "MW-3": rev_mw3, "total": rev_mw1 + rev_mw2 + rev_mw3},
        "background_events": len(W.BG_EVENTS),
        "default_limits": {k: s3(R0[k]) for k in W.INDICATORS},
        "october": {"%s %s" % (w, k): s3(g["october"][(w, k)]) for w in W.COMPLIANCE for k in W.INDICATORS},
        "exceed": {w: [k for k in W.INDICATORS if g["exceed"][(w, k)]] for w in W.COMPLIANCE},
        "spc_25c": {w: int(round(v)) for w, v in g["spc"].items()},
        "purge_gal": {w: "%.1f" % round(v, 1) for w, v in g["purge"].items()},
        "temp_coef_pct": "1.91",
        "litres_per_gallon": "3.785",
        "alpha_percentile": 99,
        "resample_days": 60,
        "route_sets": {r: s for r, s in g["sets"].items()},
        "route_limits": {r: {k: s3(v) for k, v in lim.items()} for r, lim in g["limits"].items()},
        "low_route_extra": [w for w in g["sets"]["R2h MW-3 alone"] if w not in g["resample"]],
        "rows": {"edd_a": info["edd_a_rows"], "edd_b": info["edd_b_rows"], "gauging": info["gauging_rows"],
                 "purge": info["purge_rows"]},
    }
    # the deciding margins, written for the note and the checks
    f["deciding"] = {"MW-7 sodium": s3(g["october"][("MW-7", "sodium")]), "MW-9 boron": s3(g["october"][("MW-9", "boron")])}
    return f
