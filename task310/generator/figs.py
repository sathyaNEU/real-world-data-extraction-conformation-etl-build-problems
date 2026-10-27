"""Every owed figure from the cut pack, as the write-up and the goldens state them, written to figures.json.

    python3 task310/generator/figs.py <target dir>
"""
import json
import math
import os

import params as P
import solve as S

HERE = os.path.dirname(os.path.abspath(__file__))
INV = {v: k for k, v in P.REGIONS.items()}


def rnd(v, u):
    """Half up to the unit, the way the brief prints it."""
    return math.floor(v / u + 0.5) * u


def compute(target):
    pk, res = S.solve(target)
    g, d = res["golden"], res["recorded"]
    order, dorder = S.order(g), S.order(d)
    name = lambda r: P.REGIONS[r]
    f = {
        "call": name(order[0]),
        "runner_up": name(order[1]),
        "schedule": {name(r): P.ROUND_YEARS[i] for i, r in enumerate(order)},
        "kwh_per_battery": {name(r): int(rnd(g[r], 50)) for r in P.REGION_ORDER},
        "round_mwh": {name(r): int(rnd(P.ROUND_BATTERIES * g[r] / 1000.0, 100)) for r in P.REGION_ORDER},
        "kwh_raw": {name(r): round(g[r], 1) for r in P.REGION_ORDER},
        "default_schedule": {name(r): P.ROUND_YEARS[i] for i, r in enumerate(dorder)},
        "default_kwh_per_battery": {name(r): int(rnd(d[r], 50)) for r in P.REGION_ORDER},
        "default_round_mwh": {name(r): int(rnd(P.ROUND_BATTERIES * d[r] / 1000.0, 100)) for r in P.REGION_ORDER},
        "limited_homes": {name(r): int(((pk.region == r) & pk.limited).sum()) for r in P.REGION_ORDER},
        "constants": {"round_batteries": P.ROUND_BATTERIES, "usable_kwh": P.BAT_USABLE_KWH, "power_kw": P.BAT_POWER_KW,
                      "charge_eff": P.BAT_CHARGE_EFF, "discharge_eff": P.BAT_DISCHARGE_EFF, "homes_per_region": 40,
                      "census": "2026-09-30", "solar_by": "2025-09-30", "export_limit_kw": {"MEG-CZ05": 0.5, "MEG-L15": 1.5},
                      "efficiency_pct": 95, "straddling_postcodes": [2716, 2905], "round_kwh_to": 50, "round_mwh_to": 100},
    }
    a = S.ask_eligible(target)
    f["ask_a"] = {n: int(a.get(n, 0)) for n in P.REGIONS.values()}
    b = S.ask_pilot(target)
    f["ask_b"] = {"Q%d 2025" % (i + 1): round(rnd(v, 0.1), 1) for i, v in enumerate(b)}
    f["ask_b_raw"] = [round(v, 4) for v in b]
    c = S.ask_installs(target)
    f["ask_c"] = {n: int(c.get(n, 0)) for n in P.REGIONS.values()}
    return f, (pk, res)


def write(target, path=os.path.join(HERE, "figures.json")):
    f, r = compute(target)
    with open(path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return f, r


if __name__ == "__main__":
    import sys
    print(json.dumps(write(sys.argv[1])[0], indent=1))
