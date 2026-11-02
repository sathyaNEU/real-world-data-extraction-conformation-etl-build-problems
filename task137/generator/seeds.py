"""Seed screen: simulate the world for a range of seeds and print every route's 2027 figure, so the shipped seed is one
whose standing family sits inside one cell of the graded rounding while every easy route sits outside it.

    python3 task137/generator/seeds.py 1 20
"""
import datetime as dt
import json
import sys

import numpy as np

import analysis as AN
import astro as A
import params as P
import world as WO


def frames(W):
    runs = [(r["date"], r["depot"], r["journeys"][0][0], r["journeys"][0][1], r["journeys"][0][2]) for r in W["runs"]
            if r["date"] <= P.REC_END]
    claims = [(c["date"], c["depot"], c["time_h"]) for c in W["claims"] if c["date"] <= P.REC_END]
    plan = []
    for d in WO.plan_2027():
        for r in W["routes"]:
            plan.append((d, r["depot"], r["plan"], r["plan"] + r["dur"], float(r["km"])))
    E = AN.exposure(runs, A.TABLE, A.row_of, A.bst_offset)
    C = AN.claim_frame(claims, A.TABLE, A.row_of, A.bst_offset)
    F = AN.exposure(plan, A.TABLE, A.row_of, A.bst_offset)
    return E, C, F


def routes(E, C, F):
    out = {}
    for name, cols in list(AN.MODELS_EASY.items()) + list(AN.MODELS_LIGHT.items()):
        if "year" in cols:
            continue
        q, y, _ = AN.forecast(E, C, F, cols)
        out[name] = {"year": round(y, 1), "q": [round(float(q.get(i, 0)), 1) for i in (1, 2, 3, 4)]}
    q, y = AN.cell_forecast(E, C, F, ["month", "band"], ["band"])
    out["month by band cells, band where empty"] = {"year": round(y, 1), "q": [round(float(q.get(i, 0)), 1) for i in (1, 2, 3, 4)]}
    q, y = AN.cell_forecast(E, C, F, ["band", "dark"], ["band"])
    out["band by light cells"] = {"year": round(y, 1), "q": [round(float(q.get(i, 0)), 1) for i in (1, 2, 3, 4)]}
    return out


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    for s in range(a, b + 1):
        W = WO.simulate(s)
        E, C, F = frames(W)
        R = routes(E, C, F)
        easy = [v["year"] for k, v in R.items() if "light" not in k]
        fam = [v["year"] for k, v in R.items() if "light" in k]
        print(json.dumps({"seed": s, "claims": len(C), "dark_share_rec": round(float(E[E.dark == 1].km.sum() / E.km.sum()), 3),
                          "dark_share_2027": round(float(F[F.dark == 1].km.sum() / F.km.sum()), 3),
                          "easy": [min(easy), max(easy)], "family": [min(fam), max(fam)],
                          "golden": R["clock band and light (golden)"],
                          "fam_q_min": [min(R[k]["q"][i] for k in R if "light" in k) for i in range(4)],
                          "fam_q_max": [max(R[k]["q"][i] for k in R if "light" in k) for i in range(4)],
                          "routes": {k: v["year"] for k, v in R.items()}}))
        sys.stdout.flush()
