"""figures.json: every figure the write-up states, at the precision it states it, from solve.py on the cut pack."""
import json
import os

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))


def r1(x):
    return round(x + 1e-9, 1)


def r2(x):
    return round(x + 1e-9, 2)


def build(mc, A, Bq, I27):
    gold = mc["gold"]
    pick = max(P.REGIONS, key=lambda r: gold[r]["value"])
    second = max(gold[r]["value"] for r in P.REGIONS if r != pick)
    pen = gold["Pennine"]
    O = mc["O"]
    ex = O[(O.region == "Pennine") & (O.G - P.RETENTION / 1e6 >= P.LIMIT / 1e6)]
    fz = O[(O.region == "Pennine") & (O.peril == "freeze") & (O.year < 2021)]
    figs = {
        "call": {"region": pick, "value": r1(gold[pick]["value"]), "margin": r1(gold[pick]["value"] - second)},
        "values": {r: r1(gold[r]["value"]) for r in P.REGIONS},
        "cc": {"pennine_recoveries": r2(pen["recoveries"]), "pennine_reinstatement": r2(pen["rip"]),
               "pennine_premium": r2(P.PREMIUM["Pennine"] / 1e6), "pennine_exhausting": int(len(ex)),
               "layer_limit": P.LIMIT / 1e6},
        "steps": {"hours": [P.HOURS["windstorm"], P.HOURS["flood"]], "index_2027": round(I27, 1),
                  "fit_occurrences": int((O.n >= 150).sum()), "fit_min_claims": 150,
                  "fit_threshold": mc["fit"]["u0"], "fit_slope_pct": round(100 * mc["fit"]["k"], 1),
                  "pennine_freezes_then": [r1(fz.u_all.min()), r1(fz.u_all.max())],
                  "pennine_freezes_2027": [r1(fz.u27_all.min()), r1(fz.u27_all.max())],
                  "annual_cap": P.ANNUAL / 1e6},
        "askA": {r: {str(y): r2(A["golden"]["%s|%d" % (r, y)]) for y in (2023, 2024, 2025)} for r in P.REGIONS},
        "askB": {r: r1(Bq["golden"][r]["si_m"]) for r in P.REGIONS},
    }
    raw = {
        "values": {r: gold[r]["value"] for r in P.REGIONS},
        "recoveries": {r: gold[r]["recoveries"] for r in P.REGIONS},
        "rip": {r: gold[r]["rip"] for r in P.REGIONS},
        "default": {r: mc["default"][r]["value"] for r in P.REGIONS},
        "askA": A["golden"],
        "askB": {r: Bq["golden"][r] for r in P.REGIONS},
        "exhausting": [str(s) for s in ex.start],
        "fit": mc["fit"],
    }
    return figs, raw


def write(figs, path=os.path.join(HERE, "figures.json")):
    with open(path, "w") as fh:
        json.dump(figs, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
