"""Every figure the write-up and the goldens state, computed forward from the world, written to figures.json."""
import json

import params as P
import world as Wd


def r100(v):
    return int(round(v / 100.0) * 100)


def compute(W, gate_truth, repay_truth):
    S, info = Wd.rungs(W)
    st = {c: S[c]["R2"] for c in S}
    order = sorted(st, key=lambda c: -st[c])
    pick, ru = order[0], order[1]
    same = {c: S[c]["R1"] for c in S}
    sorder = sorted(same, key=lambda c: -same[c])
    fig = {
        "stations": {c: round(st[c], 1) for c in st},
        "stations_r100": {c: r100(st[c]) for c in st},
        "pick": pick,
        "pick_saving": r100(st[pick]),
        "runner_up": ru,
        "runner_up_saving": r100(st[ru]),
        "gap": r100(st[pick] - st[ru]),
        "gap_raw": round(st[pick] - st[ru], 1),
        "same_train": {c: round(same[c], 1) for c in same},
        "same_train_r100": {c: r100(same[c]) for c in same},
        "default_pick": sorder[0],
        "default_saving": r100(same[sorder[0]]),
        "pellingham_same_train": r100(same["Pellingham"]),
        "pellingham_knock_on": r100(st["Pellingham"] - same["Pellingham"]),
        "rungs": {c: {k: round(v, 1) for k, v in S[c].items()} for c in S},
        "reactionary": {"network": round(info["net"], 4), "line": {k: round(v, 4) for k, v in info["line"].items()}},
        "base_passenger_lateness": int(round(info["base_full"])),
        "weekdays": len(W["days"]),
        "team_share": P.TEAM_SHARE,
        "min_turnround_minutes": P.MIN_TURN / P.HM,
        "gates": gate_truth,
        "repay": {"%s|%s" % k: v for k, v in repay_truth.items()},
        "repay_gbp": {"%s|%s" % k: int(round(v)) for k, v in repay_truth.items()},
        "constants": {"counter_wrap": P.COUNTER_WRAP, "band_bounds": [15, 29, 30, 59, 60],
                      "team_hours": ["06:30", "19:30"],
                      "rounding_passenger_minutes": 100, "census_day": "13 October 2026",
                      "record": ["7 September 2026", "27 November 2026"], "section": 3},
    }
    return fig


def write(fig, path):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True, default=str)
        fh.write("\n")
