"""Every figure the write-up and the goldens state, computed once from the pack and written to figures.json.

    python3 task307/generator/figs.py <target dir>
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import asks as A  # noqa: E402
import pack  # noqa: E402

ORDER = ["TIP-28-014", "TIP-28-021", "TIP-28-009", "TIP-28-030"]


def r(v, u):
    """half-up rounding to a unit"""
    return math.floor(v / u + 0.5) * u


def compute(target):
    n = pack.Net(target)
    c = n.call()
    fx = n.fixed()
    c1 = A.Counts(target)
    g = dict(ask1=c1.ask1(), ask2=c1.ask2(target), windows=c1.fault_windows())
    ranked = sorted(ORDER, key=lambda k: -c["proj"][k]["annual"])
    F = {
        "award": c["best"],
        "award_name": n.names[c["best"]],
        "runner_up": ranked[1],
        "runner_up_name": n.names[ranked[1]],
        "ranking": ranked,
        "names": {k: n.names[k] for k in ORDER},
        "cost_musd": {k: n.cost[k] for k in ORDER},
        "annual_vh": {k: int(r(c["proj"][k]["annual"], 1000)) for k in ORDER},
        "annual_exact": {k: round(c["proj"][k]["annual"], 1) for k in ORDER},
        "per_musd_vh": {k: int(r(c["proj"][k]["per_m"], 100)) for k in ORDER},
        "per_musd_exact": {k: round(c["proj"][k]["per_m"], 2) for k in ORDER},
        "peak_hour_saved_vh": {k: {p: round(c["proj"][k]["saved"][p], 1) for p in ("AM", "PM")} for k in ORDER},
        "nobuild_vht": {p: round(v, 1) for p, v in c["nobuild"].items()},
        "fixed_route": {"award": fx["best"], "annual_vh": {k: int(r(fx[k]["annual"], 1000)) for k in ORDER}},
        "annual_factor": pack.WEEKDAYS * pack.EXPANSION,
        "aadt": {s: int(r(v["aadt"], 1)) for s, v in g["ask1"].items()},
        "aadt_exact": {s: round(v["aadt"], 3) for s, v in g["ask1"].items()},
        "k_factor": {s: "%.3f" % r(v["k"], 0.001) for s, v in g["ask1"].items()},
        "k_exact": {s: round(v["k"], 5) for s, v in g["ask1"].items()},
        "h30": {s: int(v["h30"]) for s, v in g["ask1"].items()},
        "validation_pct": {"%s %s %s" % k: "%.1f" % r(v["pct"], 0.1) for k, v in g["ask2"].items()},
        "validation_exact": {"%s %s %s" % k: round(v["pct"], 4) for k, v in g["ask2"].items()},
        "validation_model_veh": {"%s %s %s" % k: round(v["model"], 1) for k, v in g["ask2"].items()},
        "validation_count_veh": {"%s %s %s" % k: round(v["count"], 1) for k, v in g["ask2"].items()},
        "validation_days": {"%s %s %s" % k: v["days"] for k, v in g["ask2"].items()},
        "fault_windows": {"%s %s" % k: [str(a), str(b)] for k, (a, b) in g["windows"].items()},
        "filed": {"weekdays": pack.WEEKDAYS, "peak_expansion": pack.EXPANSION, "relative_gap": 0.000001,
                  "rounding_annual": 1000, "rounding_per_million": 100,
                  "sections": [4.1, 4.2, 4.3, 6.1, 6.3, 6.4, 3.1]},
    }
    return F


def main(target):
    F = compute(target)
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True)
    return F


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")), indent=1))
