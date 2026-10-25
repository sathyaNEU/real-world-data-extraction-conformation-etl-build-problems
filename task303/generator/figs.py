"""figures.json: every figure the write-up and the goldens state, computed from the shipped pack by solve.py."""
import json
import os
import re

from docx import Document

import solve as S


def rnd(x, unit):
    if unit >= 1:
        return int(round(x / unit)) * unit
    return round(round(x / unit) * unit, 1)


def compute(target):
    pk = S.Pack(target)
    g = pk.call(True)
    d = pk.call(False)
    order = sorted(S.CAND, key=lambda f: -g[f])
    win = order[0]
    n_shared, cmi_shared = pk.shared_counts()
    storm, taps = pk.storm(), pk.taps()
    inv = pk.inv
    plan = " ".join(p.text for p in Document(os.path.join(target, S.FILES["plan"])).paragraphs)
    rate = float(re.search(r"earns USD ([0-9.]+) for each customer-minute", plan).group(1))
    assert abs(rate - S.INCENTIVE) < 1e-9
    dec = [t for t in pk.tickets if t["sys"] == "legacy" and "." in t["raw"]]
    ex = next(t for t in dec if t["feeder"] in S.CAND and t["device"] == "Fuse" and int(t["raw"].split(".")[0]) >= 2
              and int(t["raw"].split(".")[1]) >= 10)
    fig = {
        "rate": rate,
        "fdr_example": 112,
        "hmm_example": {"text": ex["raw"], "minutes": ex["minutes"]},
        "hmm_max_after_point": max(int(t["raw"].split(".")[1]) for t in dec),
        "call": {"feeder": win, "substation": inv[win]["Substation"], "figure_exact": round(g[win], 2),
                 "figure": rnd(g[win], 100), "value_exact": round(g[win] * S.INCENTIVE, 2),
                 "value": rnd(g[win] * S.INCENTIVE, 1000), "runner_up": order[1], "runner_up_figure": rnd(g[order[1]], 100)},
        "candidates": {f: {"substation": inv[f]["Substation"], "exact": round(g[f], 2), "figure": rnd(g[f], 100),
                           "rank": order.index(f) + 1, "backbone_miles": inv[f]["Three-phase backbone (miles)"],
                           "cost_musd": round(inv[f]["Three-phase backbone (miles)"] * 0.42, 1)} for f in S.CAND},
        "default": {f: {"exact": round(d[f], 2), "figure": rnd(d[f], 100)} for f in S.CAND},
        "default_pick": max(S.CAND, key=lambda f: d[f]),
        "shared": {f: {"tickets": n_shared.get(f, 0),
                       "addressed_cmi_a_year": rnd(S.PREVENTED * cmi_shared.get(f, 0) / S.YEARS_N, 100)}
                   for f in S.CAND},
        "storm": {f: {"cmi": rnd(storm[f]["cmi"], 1000), "cmi_exact": storm[f]["cmi"], "ci": storm[f]["ci"],
                      "per": rnd(storm[f]["per"], 0.1), "per_exact": round(storm[f]["per"], 4)} for f in S.CAND},
        "taps": {f: {"year": rnd(taps[f]["year"], 10), "year_exact": round(taps[f]["year"], 2),
                     "per": rnd(taps[f]["per"], 0.1), "per_exact": round(taps[f]["per"], 4)} for f in S.CAND},
    }
    return fig


def write(fig, path):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
