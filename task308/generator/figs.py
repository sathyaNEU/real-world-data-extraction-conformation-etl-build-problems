"""Every figure the write-up and the goldens state, computed once from the pack and written to figures.json."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import params as P  # noqa: E402
import solve as S  # noqa: E402


def r100(v):
    return int(round(v / 100.0) * 100)


def money(v):
    return int(round(v))


def compute(target):
    pk = S.Pack(target, build.FILES)
    g = pk.call("golden")
    easy = pk.call("rated")
    facts = pk.shortfall_facts()
    m = S.Meter(target, build.FILES)
    energy = m.energy()
    cp, peaks = m.cp12()
    pay = {o: P.annual_payment(o) for o in P.OFFERS}
    by_year = {}
    import numpy as np
    yrs = pk.tb.weather_year.values
    for y in P.YEARS:
        by_year[str(y)] = r100(float(np.clip(pk.short[yrs == y], 0, None).sum()))
    F = {
        "award": g["best"],
        "base_eue_mwh": r100(g["base"]),
        "base_eue_exact": round(g["base"], 1),
        "shortfall_hours": facts["hours"],
        "shortfall_hours_per_year": round(facts["hours_per_year"], 1),
        "share_in_fuel_outage_hours_pct": int(round(100 * facts["share_in_allout"])),
        "removed_mwh": {o: r100(v) for o, v in g["removed"].items()},
        "removed_exact": {o: round(v, 1) for o, v in g["removed"].items()},
        "value_musd": {o: money(g["removed"][o] * P.VOLL / 1e6) for o in P.OFFERS},
        "payment_musd": {o: round(pay[o] / 1e6, 1) for o in P.OFFERS},
        "net_musd": {o: money(v) for o, v in g["net"].items()},
        "net_exact": {o: round(v, 3) for o, v in g["net"].items()},
        "offer_mw": {o: int(P.OFFER_MW[o]) for o in P.OFFERS},
        "voll": int(P.VOLL),
        "easy_route": {"award": easy["best"], "peaker_removed_mwh": r100(easy["removed"]["Ketchum Ridge"]),
                       "peaker_net_musd": money(easy["net"]["Ketchum Ridge"])},
        "class_forced_rate_pct": round(100 * pk.ct_rate(), 1),
        "rated_eford_pct": 4.5,
        "eue_by_weather_year": by_year,
        "ask_a_mwh": {k: int(round(v)) for k, v in energy.items()},
        "ask_b_mw": {k: round(float(v), 1) for k, v in cp.items()},
        "cp_hours": [str(t.tz_convert(P.TZ)) for t in peaks],
        "kw_year": pk.kw_years,
        "fuel_cause_code": 9130,
        "existing_import_mw": int(P.IMPORT_EX_MW),
    }
    return F


def main(target):
    F = compute(target)
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(F, fh, indent=1, sort_keys=True)
    return F


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(build.TASK, "target")), indent=1))
