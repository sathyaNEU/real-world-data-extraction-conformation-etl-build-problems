"""task304 architecture 5: every figure the write-up and the goldens state, computed from target/ by analysis.py and
written to generator/figures.json."""
import json

import analysis as AN

QNAME = {1: "January to March", 2: "April to June", 3: "July to September"}
SNAME = {1: "Fatal", 2: "Serious", 3: "Slight"}


def r1(x):
    return float("%.1f" % (x + 1e-9))


def compute(target):
    pk, figs, lad = AN.golden(target)
    order = sorted(figs.values(), key=lambda r: r["name"])
    best = lad["golden"][2][0]
    second = lad["golden"][2][1]
    m = pk.spf()
    a = pk.ask_a()
    b = pk.ask_b()
    F = {
        "junctions": [r["name"] for r in order],
        "nodes": {r["name"]: r["node"] for r in order},
        "layout": {r["name"]: r["layout"] for r in order},
        "cmf": {r["name"]: r["cmf"] for r in order},
        "benefit": {r["name"]: r1(r["benefit"]) for r in order},
        "expected": {r["name"]: r1(r["expected"]) for r in order},
        "observed_2021_2025": {r["name"]: int(r["obs"]) for r in order},
        "call": best["name"],
        "call_benefit": r1(best["benefit"]),
        "call_expected": r1(best["expected"]),
        "call_observed": int(best["obs"]),
        "runner_up": second["name"],
        "runner_up_benefit": r1(second["benefit"]),
        "observed_route": lad["observed"][0],
        "observed_route_benefit": r1(lad["observed"][2][0]["obs_benefit"]),
        "model_route": lad["model_only"][0],
        "model_route_benefit": r1(lad["model_only"][2][0]["spf_benefit"]),
        "rate_route": lad["rate"][0],
        "reference_junctions": len(pk.reference()),
        "overdispersion": round(m["a"], 2),
        "screen_minimum": 12,
        "window": "2021 to 2025",
        "present": 2026,
        "ask_a": {"Q%d" % q: {SNAME[s]: a[(q, s)] for s in (1, 2, 3)} for q in (1, 2, 3)},
        "ask_b": {"Q%d" % q: {g: b[(q, g)] for g in AN.GROUPS} for q in (1, 2, 3)},
        "quarters": QNAME,
    }
    return F, pk, figs, lad


def write(target, path):
    F, pk, figs, lad = compute(target)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(F, f, indent=1, sort_keys=True)
    return F
