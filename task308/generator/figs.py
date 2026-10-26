"""Compute every figure the goldens and the write-up state, from the pack alone, and write figures.json."""
import json

import numpy as np

import solve as SV

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def compute(target):
    G = SV.solve(target)
    pl, nr = G["pilot"], G["net"]
    best = G["best"]
    others = sorted((n for n in SV.NETS if n != best), key=lambda n: -nr[n]["net"])
    dflt = max(SV.NETS, key=lambda n: nr[n]["default"])
    U, R = nr[best]["turned_away"], nr[best]["requests"]
    fig = {
        "recommended_network": best,
        "net_revenue": {n: SV.r25(nr[n]["net"]) for n in SV.NETS},
        "net_revenue_exact": {n: round(nr[n]["net"], 0) for n in SV.NETS},
        "runner_up": others[0],
        "rides_2025": {n: nr[n]["rides"] for n in SV.NETS},
        "turned_away": {n: int(round(nr[n]["turned_away"], -2)) for n in SV.NETS},
        "turned_away_exact": {n: round(nr[n]["turned_away"], 1) for n in SV.NETS},
        "requests": {n: int(round(nr[n]["requests"], -2)) for n in SV.NETS},
        "turned_away_share": {n: round(100 * nr[n]["turned_away"] / nr[n]["requests"], 1) for n in SV.NETS},
        "fare_classic": {n: round(nr[n]["fare_classic"], 2) for n in SV.NETS},
        "recorded_route": {n: SV.r25(nr[n]["default"]) for n in SV.NETS},
        "recorded_route_exact": {n: round(nr[n]["default"], 0) for n in SV.NETS},
        "recorded_route_pick": dflt,
        "pilot": {"ebike_share": round(100 * pl["X"], 1), "uplift": round(100 * pl["i"], 1),
                  "fare_ebike": round(pl["f_e"], 2), "fare_classic": round(pl["f_c_pilot"], 2),
                  "premium": round(pl["delta"], 2), "rides_pilot": pl["rides_pilot"],
                  "rides_comparison": pl["rides_comparison"], "ebike_rides": pl["ebike_rides_pilot"],
                  "stations_pilot": len(pl["pilot"]), "stations_comparison": len(pl["comparison"])},
        "people": {n: int(G["people"].get(n, 0)) for n in SV.NETS},
        "energy_kwh": {MONTHS[m - 1]: int(round(G["energy"][m])) for m in range(1, 13)},
        "energy_kwh_exact": {MONTHS[m - 1]: round(G["energy"][m], 3) for m in range(1, 13)},
        "workshop_per_10000": {("E-bike" if t == "ebike" else "Classic") + " Q%d" % q: round(v[2], 1)
                               for (t, q), v in G["workshop"].items()},
        "workshop_jobs": {("E-bike" if t == "ebike" else "Classic") + " Q%d" % q: v[0] for (t, q), v in G["workshop"].items()},
        "workshop_rides": {("E-bike" if t == "ebike" else "Classic") + " Q%d" % q: v[1] for (t, q), v in G["workshop"].items()},
        "university_turned_away_share": round(100 * U / R, 1),
        "constants": {"ebikes": 300, "per_rides": 10000, "rounding_usd": 25000, "false_start_seconds": 60,
                      "energy_year_kwh": int(round(sum(G["energy"].values())))},
    }
    return fig, G


def write(fig, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True, default=lambda x: int(x) if isinstance(x, np.integer) else float(x))
        fh.write("\n")
