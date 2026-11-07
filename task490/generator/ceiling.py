"""task490 ceiling: scores the cracker (lands the call, runs the hygiene battery, reads every remark and helper
document, executes every filed sentence) and the mirror (stops at rung 1, the chamber replayed boat by boat) on the
cut pack, ask figure by ask figure, at half a unit of the stated rounding. Weights 38 / 7 / 55."""
import csv
import json
import os
from datetime import datetime, timedelta

import world as W
import golden as G
import records as R

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), "target")
F = json.load(open(os.path.join(HERE, "figures.json")))


def hit(a, b, unit):
    return abs(a - b) < unit / 2 - 1e-9


# ------------------------------------------------------------------ the asks, as the cracker computes them
ret = G.load_returns(T)
cr = {}
for name in ("Upper Kelsby Reservoir", "Tilsey Reservoir"):
    # the remarks give each valve change its time, so the season's ends are cut exactly
    cr[name] = G.seg_volume(G.rate_segments(ret[name]), G.SEASON_A, G.SEASON_B)
# Lower Kelsby: the Released column summed over the season's water days (each line a day's figure)
cr["Lower Kelsby Reservoir"] = sum(l["rel"] for l in ret["Lower Kelsby Reservoir"]
                                   if W.SEASON_START <= l["d"] <= W.SEASON_END)
stored = 0.0
with open(os.path.join(T, R.F_COLD), newline="") as f:
    for row in csv.DictReader(f):
        t = datetime.strptime(row["period_end_utc"], "%Y-%m-%dT%H:%M:%SZ")
        if datetime(2026, 3, 31, 23, 0) < t <= datetime(2026, 11, 1, 0, 0):
            stored += float(row["flow_ls_mean"]) * 0.9 / 1000.0
cr["Coldmere Reservoir"] = stored
share_h = W.FOX_HARNOCK_B / (W.FOX_HARNOCK_B + W.FOX_TILSEY_B)
recv_c = {"Kelsby": cr["Lower Kelsby Reservoir"], "Harnock": stored * share_h,
          "Tilsey": cr["Tilsey Reservoir"] + stored * (1 - share_h)}
# abstraction: readings chained by abstraction point, a lower reading on one meter read as its dials rolling over,
# a new serial at the same point taken from its first reading
reads = {}
with open(os.path.join(T, R.F_READ), newline="") as f:
    for row in csv.DictReader(f):
        reads.setdefault(row["point_ref"], []).append(row)
abs_c = {}
for L in W.LICENCES:
    by = {}
    for r_ in reads[L["point"]]:
        by.setdefault(r_["meter_serial"], []).append(int(r_["reading_m3"]))
    abs_c[L["ref"]] = sum((y - x) % (10 ** L["digits"]) for v in by.values() for x, y in zip(v, v[1:]))
abs_tot_c = {s: sum(abs_c[L["ref"]] for L in W.LICENCES if L["summit"] == s) for s in W.SUMMITS}

rows = []
for k in W.RESERVOIRS:
    rows.append(("S", "release " + k, cr[k], F["reservoir_release_ml"][k], 0.1))
for s in W.SUMMITS:
    rows.append(("S", "received " + s, recv_c[s], F["summit_received_ml"][s], 0.1))
for L in W.LICENCES:
    rows.append(("A", "take " + L["ref"], abs_c[L["ref"]], F["abstraction_m3"][L["ref"]], 1))
for s in W.SUMMITS:
    rows.append(("A", "total " + s, abs_tot_c[s], F["abstraction_summit_m3"][s], 1))
kept = [r_ for r_ in rows if hit(r_[2], r_[3], r_[4])]
L_ask = len(kept) / len(rows)

# ----------------------------------------------------------- the call side: the cracker lands it, the mirror is at rung 1
mirror_call_hits = 2          # the two counts of records left out are Layer 1 and the mirror cleans as well as the cracker
call_items = 14               # call, runner-up, gap, 3 summit figures, 6 lock waters, 2 record counts
cracker = 38 + 7 + 55 * L_ask
mirror = 38 * mirror_call_hits / call_items + 7 + 55 * L_ask
pair = (cracker + mirror) / 2

if __name__ == "__main__":
    print("| Ask figure | Cracker | Golden | Cracker |")
    print("|---|---|---|---|")
    for a, lab, c, g, u in rows:
        print("| %s: %s | %s | %s | %s |" % (a, lab, ("%.1f" % c) if u < 1 else "%d" % c, ("%.1f" % g) if u < 1 else
                                             "%d" % g, "hit" if hit(c, g, u) else "miss"))
    for ask in ("S", "A"):
        n = [r_ for r_ in rows if r_[0] == ask]
        k = [r_ for r_ in n if hit(r_[2], r_[3], r_[4])]
        print("ask %s: the cracker keeps %d of %d" % (ask, len(k), len(n)))
    print("Pair ceiling: %.1f (cracker %.1f, mirror %.1f)" % (pair, cracker, mirror))
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * L_ask))
