"""Every owed figure, computed from the cut pack by solve.py, written to figures.json."""
import json

import numpy as np

import solve as S


def nearest(x, step):
    return int(step * round(float(x) / step))


def compute(target):
    price, free = S.paper_table(target)
    heavy, light, latest = S.kpi(target)
    g, c = S.golden_call(target)
    up1, free1, gone1 = S.response(target)
    rt, info = S.routes(target)
    order = np.argsort(-g)
    win, run = int(order[0]), int(order[1])
    dP, dF, fr = c["P1"] - c["P0"], c["F0"] - c["F1"], c["fr"]
    by_app = {}
    for i, a in enumerate(S.APPS):
        by_app[a] = {"over_three": int(heavy[i]), "three_or_fewer": int(light[i]),
                     "reaching_four_2027": int(round(light[i] * fr[:11].sum())),
                     "plus_price": float(price[i]), "free_revenue": float(free[i]),
                     "addition": int(round(g[i]))}
    fig = {
        "call": {"app": S.APPS[win], "addition": int(round(g[win])), "addition_rounded": nearest(g[win], 50000),
                 "runner_up": S.APPS[run], "runner_up_addition": int(round(g[run])), "margin": round(float(g[win] / g[run]), 3)},
        "by_app": by_app,
        "response": {"stops": int(c["n1"]), "unstopped_account_months": int(c["n0"]), "plus_next_month": round(float(up1), 4),
                     "free_next_month": round(float(free1), 4), "gone_next_month": round(float(gone1), 4),
                     "plus_months_gained": round(float(dP.sum()), 4), "free_months_lost": round(float(dF.sum()), 4),
                     "own_plus_12": round(float(info["U"]), 4), "own_gone_12": round(float(info["L"]), 4),
                     "stopped_plus": [round(float(x), 4) for x in c["P1"]], "stopped_free": [round(float(x), 4) for x in c["F1"]],
                     "unstopped_plus": [round(float(x), 4) for x in c["P0"]], "unstopped_free": [round(float(x), 4) for x in c["F0"]],
                     "reaching_four_by_month": [round(float(x), 5) for x in fr]},
        "shares_pct": {"plus_next_month": round(100 * float(up1), 1), "free_next_month": round(100 * float(free1), 1),
                       "gone_next_month": round(100 * float(gone1), 1), "own_plus_12": round(100 * float(info["U"]), 1)},
        "allowance_mib": 2048, "thresholds_mib": [2000, 1950, 2047], "rounding_gbp": 50000,
        "kpi_month": str(latest),
        "routes": {k: {a: int(round(v[i])) for i, a in enumerate(S.APPS)} for k, v in rt.items()},
        "standing": {k: {a: int(round(v[i])) for i, a in enumerate(S.APPS)}
                     for k, v in list(S.standing(target).items()) + list(S.adjusted(target).items())},
        "ask": S.bridge(target),
    }
    return fig


def write(fig, path):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
