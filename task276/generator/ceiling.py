"""The cracker and mirror sheets, run on the cut pack: what the strongest response off and on the call keeps of the
rubric, the pair ceiling, and each device's lift. The cracker lands the call, runs the hygiene battery (former numbers,
code map, disposals, a carried job deduplicated to the record the fleet system holds), executes the filed definitions
(a unit's fitted window, 365-day vehicle-years), takes each unit's distance from its first reading in the window, adds
each job's off-road days, and joins on the numbers the current register and the disposals carry as they stand. The mirror takes the default path's call with the same ask handling.

    python3 task276/generator/ceiling.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G
import solve as SV

MAIN, IF, ASK = 38.0, 7.0, 55.0
CRACKER = dict(join="register", transferred="merged", miles_how="window_first", in_service="held", vor="sum")
GOLDEN = dict(join="asof", transferred="first", miles_how="window", in_service="true", vor="union")


def ask_figures(F):
    out = {}
    for c in G.CONVERTERS:
        f = F["converters"][c]
        k = c.split()[0]
        for i, q in enumerate(f["jobs"]):
            out[("A jobs by quarter", "%s Q%d" % (k, i + 1))] = q
        out[("A miles", k)] = int(round(f["miles"] / 100.0)) * 100
        out[("A rate", k)] = round(f["rate"] + 1e-9, 2)
    for c in G.CHASSIS:
        f = F["chassis"][c]
        for i, q in enumerate(f["days"]):
            out[("B days by quarter", "%s Q%d" % (c, i + 1))] = q
        out[("B vehicle-years", c)] = round(f["vehicle_years"] + 1e-9, 1)
        out[("B rate", c)] = round(f["rate"] + 1e-9, 1)
    return out


def kept(gold, resp):
    hits = [k for k in gold if gold[k] == resp.get(k)]
    return len(hits) / float(len(gold)), hits


def main_share(S, on_call):
    fit = S["fit"]
    if on_call:
        return MAIN
    r2 = S["rungs"]["R2"]
    same = [k for k in fit if fit[k] == r2[k]]
    return 12.0 * len(same) / 5 + 6.0 * len(same) / 5 + 2.0


def run(T):
    S = SV.solve(T)
    gold = ask_figures(SV.fleet_figures(T, **GOLDEN))
    crack = ask_figures(SV.fleet_figures(T, **CRACKER))
    lc, hits_c = kept(gold, crack)
    ls, hits_m = lc, hits_c
    C = MAIN + IF + ASK * lc
    M = main_share(S, False) + IF + ASK * ls
    pair = (C + M) / 2.0
    rows = {}
    for k in gold:
        rows.setdefault(k[0], [0, 0])
        rows[k[0]][1] += 1
        if k in hits_c:
            rows[k[0]][0] += 1
    lifts = {}
    for name, change in (("D7 reused numbers held on the record's date", {"join": "asof"}),
                         ("D2 renumbered vehicles from their original dates", {"in_service": "true"}),
                         ("carried Vennerley job at its first raise", {"transferred": "first"}),
                         ("a unit's distance from the odometer entered at fitting", {"miles_how": "window"}),
                         ("a vehicle's days off the road counted once", {"vor": "union"})):
        cfg = dict(CRACKER, **change)
        l2, _ = kept(gold, ask_figures(SV.fleet_figures(T, **cfg)))
        lifts[name] = ASK * (l2 - lc)
    return {"cracker_total": C, "mirror_total": M, "pair": pair, "cracker_ask_share": lc, "mirror_ask_share": ls,
            "rows": rows, "lifts": lifts, "mirror_main": main_share(S, False)}


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    R = run(os.path.join(task, "target"))
    print("cracker: main %.1f + IF %.1f + asks %.1f of %.0f = %.1f" % (MAIN, IF, ASK * R["cracker_ask_share"], ASK, R["cracker_total"]))
    print("mirror:  main %.1f + IF %.1f + asks %.1f of %.0f = %.1f" % (R["mirror_main"], IF, ASK * R["mirror_ask_share"], ASK,
                                                                      R["mirror_total"]))
    print("pair ceiling %.1f; mirror keeps %.1f per cent of the ask weight" % (R["pair"], 100 * R["mirror_ask_share"]))
    for k, (h, n) in R["rows"].items():
        print("  %-20s cracker hits %d of %d  %s" % (k, h, n, "miss" if h == 0 else "HIT"))
    for k, v in R["lifts"].items():
        print("  lift %-50s %.1f points (cap %.1f)" % (k, v, ASK / 3))
    assert R["pair"] <= 60.0, R["pair"]
    assert R["mirror_ask_share"] < 0.5
    assert all(v <= ASK / 3 for v in R["lifts"].values()), R["lifts"]
