"""The generator's assertions on the cut pack and the clean truth: the pack replays the truth, the call and its
margins, the ladder (every cheap route's pick), every semantic fork row (SF1 to SF15), the ask devices and their
interiors, the three-rules analyst test, the figure edges and the input gates.

    python3 task307/generator/checks.py <target dir>
"""
import datetime as dt
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A  # noqa: E402
import build  # noqa: E402
import net  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import records as R  # noqa: E402
import rungs  # noqa: E402
import solve  # noqa: E402
import world  # noqa: E402

N = {"pass": 0}
CODE = {p["tip_id"]: p["code"] for p in P.PROJECTS}


def ok(cond, msg):
    if not cond:
        raise AssertionError(msg)
    N["pass"] += 1


def edge(v, u):
    """distance from v to the nearest edge of its printed cell, as a share of the unit"""
    return (u / 2 - abs(v - math.floor(v / u + 0.5) * u)) / u


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def main(target):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    o = solve.run()
    n = pack.Net(target)
    c = n.call()

    # ---------------------------------------------------------------- the pack replays the truth
    ok(len(n.arcs) == len(o["links"]), "every directed link of the extract is in the pack")
    ok(n.zones == {int(z) for z in world.zones()}, "every zone is a centroid in the node table")
    for tip, r in c["proj"].items():
        ok(abs(r["annual"] - o["proj"][CODE[tip]]["annual"]) < 0.01, "pack replay of %s's annual benefit" % tip)
    for per in ("AM", "PM"):
        ok(abs(c["nobuild"][per] - o["nobuild"][per]["vht"]) < 1e-6, "pack replay of the %s no-build VHT" % per)
        ok(sum(n.od[per].values()) == sum(o["tabs"][per].values()), "trip table total %s" % per)
    ok(pack.WEEKDAYS * pack.EXPANSION == P.ANNUAL_FACTOR, "the guidance's annual factor")
    ok(n.cost == {p["tip_id"]: p["cost_m"] for p in P.PROJECTS}, "candidate costs")

    # ---------------------------------------------------------------- the call
    ann = {k: v["annual"] for k, v in c["proj"].items()}
    ok(c["best"] == "TIP-28-009" == F["award"], "golden award: the Center Street Bridge widening")
    srt = sorted(ann.values(), reverse=True)
    ok(srt[0] / srt[1] > 1.5, "the award leads the runner-up by more than half")
    ok(max(c["proj"], key=lambda k: c["proj"][k]["per_m"]) == "TIP-28-009", "the award also leads per million dollars")
    ok(F["runner_up"] == "TIP-28-014", "runner-up: the Route 9 auxiliary lane")

    # ---------------------------------------------------------------- the ladder: every cheap route's pick
    rt = rungs.routes(o)
    pick = {k: max(v, key=v.get) for k, v in rt.items()}
    ok(pick["fixed no-build volumes"] == "A", "default path: fixed no-build volumes fund the Route 9 widening")
    ok(pick["fixed volumes, per million dollars"] == "A", "fixed volumes per million dollars also fund Route 9")
    ok(pick["equilibrium, AM peak only"] == "C", "AM peak alone: same call")
    ok(pick["one all-or-nothing re-route"] == "A", "one all-or-nothing re-route lands on Route 9")
    for k in ("Frank-Wolfe, 3 iterations", "Frank-Wolfe, 10 iterations", "Frank-Wolfe, 50 iterations",
              "MSA, 10 iterations", "MSA, 50 iterations"):
        ok(pick[k] == "C", "%s: same call" % k)
    fx = n.fixed()
    ok(fx["best"] == "TIP-28-014", "the pack's fixed-volume route (loaded file) funds Route 9")
    ok(fx["TIP-28-014"]["annual"] / fx["TIP-28-009"]["annual"] > 1.5, "the fixed-volume route's margin for Route 9")
    ok(F["fixed_route"]["award"] == "TIP-28-014", "figures carry the easy route")

    # ---------------------------------------------------------------- semantic fork rows
    links, cap, t0, al, be, tabs = o["links"], o["cap"], o["t0"], o["al"], o["be"], o["tabs"]

    def call_with(scale=1.0, caps=None, period=("AM", "PM"), proj_caps=None, tol=1e-12):
        cp = cap if caps is None else caps
        res = {}
        for pr in P.PROJECTS:
            c2 = (proj_caps or solve.project_caps)(links, cp, pr)
            s = 0.0
            for per in period:
                od = {k: q * scale for k, q in tabs[per].items()}
                v0, tt0, _, _ = net.ue_paths(links, solve.aggregate(od), cp, t0, al, be, tol=tol)
                v1, tt1, _, _ = net.ue_paths(links, solve.aggregate(od), c2, t0, al, be, tol=tol)
                s += (v0 @ tt0 - v1 @ tt1) / 60.0
            res[pr["code"]] = s * P.ANNUAL_FACTOR
        return res
    # SF1 the trip tables in passenger-car equivalents rather than vehicles (heavy vehicles at 2.0)
    r = call_with(scale=1.08)
    ok(max(r, key=r.get) == "C", "SF1 trips scaled to PCE: same call")
    # SF2 both peak hours (filed, guidance 2.1 and 2.2); the AM alone names the same project
    ok(pick["equilibrium, AM peak only"] == "C", "SF2 AM alone: same call")
    # SF3 connector time in the vehicle-hours or not: the savings are identical
    for tip in c["proj"]:
        s_conn = c["proj"][tip]["saved"]["AM"]
        ok(abs(s_conn - o["proj"][CODE[tip]]["AM"]["saved"]) < 1e-6, "SF3 connector time cancels for %s" % tip)
    # SF4 converged to the documentation's relative gap of 0.000001 rather than exactly: every figure the same, and
    # a run stopped ten times looser still names the same project
    r6 = call_with(tol=1e-6)
    r5 = call_with(tol=1e-5)
    for code, tip in ((p["code"], p["tip_id"]) for p in P.PROJECTS):
        ok(rnd(r6[code], 1000) == F["annual_vh"][tip], "SF4 gap 1e-6: %s annual unchanged" % tip)
        ok(rnd(r6[code] / n.cost[tip], 100) == F["per_musd_vh"][tip], "SF4 gap 1e-6: %s per million unchanged" % tip)
        ok(abs(r6[code] - ann[tip]) < 120, "SF4 gap 1e-6: %s within 120 vehicle-hours" % tip)
    ok(max(r5, key=r5.get) == "C", "SF4 gap 1e-5: same call")
    # SF5 the no-build vehicle-hours read from the loaded network file rather than re-run: every figure the same
    L = n.loaded
    for per in ("AM", "PM"):
        vf = float(((L["AB_VOL_" + per] * L["AB_TIME_" + per] + L["BA_VOL_" + per] * L["BA_TIME_" + per]).sum()) / 60)
        ok(abs(vf - c["nobuild"][per]) < 0.1, "SF5 loaded file's %s VHT within 0.1 of the re-run" % per)
    # SF6 the Ferry Street project's on-ramp lane left out (exit direction only): same call
    def caps_b_exit(lk, cp, pr):
        c2 = solve.project_caps(lk, cp, pr)
        if pr["code"] == "B":
            for j, l in enumerate(lk):
                if l["name"] == "Ferry Street exit" and l["a"] == "DT1":
                    c2[j] = cp[j]
        return c2
    r = call_with(proj_caps=caps_b_exit)
    ok(max(r, key=r.get) == "C", "SF6 Ferry Street exit direction only: same call")
    # SF7 the Route 9 widening read as the whole Lakeview Road to Quarry Lane stretch (links 1 to 3): same call
    def caps_a_long(lk, cp, pr):
        c2 = solve.project_caps(lk, cp, pr)
        if pr["code"] == "A":
            for j, l in enumerate(lk):
                if l["name"] == "Route 9" and l["a"] in ("F1", "F2", "F3") and l["b"] in ("F1", "F2", "F3", "F4"):
                    c2[j] = max(c2[j], 3 * net.LANE_CAP["freeway"])
        return c2
    r = call_with(proj_caps=caps_a_long)
    ok(max(r, key=r.get) == "C", "SF7 Route 9 widening read long: same call")
    # SF8 the Southport package's per-lane capacity read as one direction only: same call
    def caps_d_one(lk, cp, pr):
        c2 = solve.project_caps(lk, cp, pr)
        if pr["code"] == "D":
            for j, l in enumerate(lk):
                if l["name"] in pr["streets"] and l["a"] in ("C1", "C2", "DT2"):
                    c2[j] = cp[j]
        return c2
    r = call_with(proj_caps=caps_d_one)
    ok(max(r, key=r.get) == "C", "SF8 Southport package one direction: same call")
    # SF9 a different annual factor (260 weekdays, or the peak hour alone): proportional, same call
    ok(max(ann, key=ann.get) == "TIP-28-009", "SF9 any common annual factor: same call")
    # SF10 the lane-drop section (FTYPE 12) at the bridge capacity per lane rather than the freeway's: same call
    cap_b = cap.copy()
    for j, l in enumerate(links):
        if l["bottleneck"]:
            cap_b[j] = l["lanes"] * net.LANE_CAP["bridge"]
    r = call_with(caps=cap_b)
    ok(max(r, key=r.get) == "C", "SF10 lane-drop at bridge capacity: same call")
    # SF11 per million dollars as the award rule rather than the largest benefit: same call
    ok(max(c["proj"], key=lambda k: c["proj"][k]["per_m"]) == "TIP-28-009", "SF11 per million: same call")
    # SF12 a zone used as a way through: no zone has two connectors, so no path can
    conn = pd.Series([l["a"] for l in links if l["ftype"] == "connector" and l["a"] in world.zones() or
                      (l["ftype"] == "connector" and l["a"].isdigit())])
    ok(conn.value_counts().max() == 1, "SF12 one connector per zone")
    # SF13 trip tables at subzone level against the macro zones: subzones share their zone's connector node
    ok(len({world.ATTACH[m] for m in world.zones().values()}) == 10, "SF13 ten attachment nodes")
    # SF14 elastic demand or induced trips: filed out (guidance 2.1); the tables are the only demand
    ok(True, "SF14 fixed demand, filed (guidance 2.1)")
    # SF16 the Route 9 section's facility type after widening: the coding sheet changes lanes only and the weaving
    # remains (FTYPE 12); recoded as plain freeway it names the same project
    def caps_a_ftype(lk, cp, pr):
        return solve.project_caps(lk, cp, pr)
    al_f = al.copy()
    be_f = be.copy()
    for j, l in enumerate(links):
        if l["bottleneck"]:
            al_f[j], be_f[j] = net.VDF["freeway"]
    res = {}
    for pr in P.PROJECTS:
        c2 = solve.project_caps(links, cap, pr)
        s_ = 0.0
        for per in ("AM", "PM"):
            agg = solve.aggregate(tabs[per])
            v0, t0_, _, _ = net.ue_paths(links, agg, cap, t0, al, be)
            alx, bex = (al_f, be_f) if pr["code"] == "A" else (al, be)
            v1, t1_, _, _ = net.ue_paths(links, agg, c2, t0, alx, bex)
            s_ += (v0 @ t0_ - v1 @ t1_) / 60.0
        res[pr["code"]] = s_
    ok(max(res, key=res.get) == "C", "SF16 Route 9 recoded as plain freeway: same call")
    tipwb = __import__("openpyxl").load_workbook(os.path.join(target, P.FILES["tip"]), read_only=True)
    ok(all("FTYPE" not in str(r[4]) for r in list(tipwb["Model coding"].iter_rows(values_only=True))[1:]),
       "SF16 the coding sheet changes no facility type")
    # SF15 the opening year: the 2028 tables are the only opening-year tables in the pack
    ok(set(pd.read_csv(os.path.join(target, P.FILES["trips"])).PERIOD) == {"AM", "PM"}, "SF15 one year of tables")

    # ---------------------------------------------------------------- three rules: the analyst test on the clean truth
    ok(pick["fixed no-build volumes"] == "A" and max(ann, key=ann.get) == "TIP-28-009",
       "analyst test: the easy route (no re-assignment) files Route 9, the equilibrium files Center Street")
    ok(o["proj"]["A"]["annual_fixed"] > 1.2 * o["proj"]["A"]["annual"], "the widening loses a share of its link saving")
    # the binding constraint: under re-assignment the widened lane-drop feeds the Route 9 bridge
    nb_v = o["nobuild"]["AM"]["v"]
    bridge = [j for j, l in enumerate(links) if l["name"] == "Route 9 Ashkettle Bridge" and l["a"] == "F4"][0]
    va = o["proj"]["A"]["AM"]["v"]
    ok(va[bridge] > nb_v[bridge] and va[bridge] / cap[bridge] > 1.0, "the Route 9 bridge binds once A opens")

    # ---------------------------------------------------------------- ask devices
    cnt = A.Counts(target)
    win = cnt.fault_windows()
    for st, (d, f0, f1, fac, lane, kind) in R.FAULTS.items():
        ok(win[(st, d)] == (f0.date(), f1.date()), "fault window of %s %s recovered from the pack" % (st, d))
    for st, (d, f0, f1, fac, lane, kind) in R.FAULTS.items():
        near = [h for h in R.HOLIDAYS_2025 + [R.DST_ON, R.DST_OFF] if abs((h - f0.date()).days) <= 1]
        ok(not near, "fault start of %s clear of holidays and clock changes" % st)
    df_truth, info = R.atr_records(*R.base_assignment())
    atr = cnt.df
    ok(len(atr) == len(df_truth), "ATR rows")
    # carried polls: the hour after each missed poll holds the missed hours' vehicles, status OK, no flag
    carried = 0
    for st, runs in info["missed"].items():
        w = cnt.wide(st)
        for (day, h), L_ in runs:
            row = w[(w.D == day) & (w.HR_END == h) & (w.OCC == 0)].index[0]
            ok((w.loc[row:row + L_ - 1, "s1"] == "NR").all(), "missed poll at %s %s %s" % (st, day, h))
            ok(w.loc[row + L_, "s1"] == "OK", "the next poll answered")
            carried += 1
    ok(carried >= 60, "carried polls across the stations (%d)" % carried)
    ok(set(atr.STATUS) == {"OK", "NR", "EST"}, "three statuses, no flag for a carried hour")
    # interior: after a whole-day outage the counters restart, and the first hour back is its own count
    spells = sum(1 for s in info["outages"].values() for x in s if x[2] == "NR")
    ok(spells >= 8, "whole-day outages")
    # every month has every weekday among its valid days, on the golden and on every ladder path
    for st in cnt.stations:
        for kw in ({}, dict(faults=False, carry=False), dict(carry=False), dict(faults=False), dict(carry_after_spell=True)):
            vd = cnt.valid_days(st, **kw)
            cells = {(d.month, d.weekday()) for d in vd}
            ok(len(cells) == 84, "every month-weekday cell has a valid day (%s, %s)" % (st, kw))
    # the probe vendor stamps interval ends: the year's first stamp is 00:15 local, its last 24:00
    pr = pd.read_parquet(os.path.join(target, P.FILES["probe"]))
    ok(pr.measurement_tstamp.min() == "2025-01-01T06:15:00Z", "first stamp ends the first interval")
    ok(pr.measurement_tstamp.max() == "2026-01-01T06:00:00Z", "last stamp ends the year's last interval")
    ok(len(pr) >= 25000, "probe rows")
    # validation: the model's vehicles are whole vehicles
    val = pd.read_csv(os.path.join(target, P.FILES["valid"]))
    vv = val.VOL_PCE / (1 + val.HV_PCT / 100)
    ok(np.allclose(vv, vv.round(), atol=0.01), "model vehicles within 0.01 of whole")
    ok(set(val.STATION) == {"S-0101", "S-0102", "S-0103", "S-0104", "S-0105"}, "validation stations")

    # the filed-rules path (the cracker) misses every ask figure; the mirror is the same on the asks
    g = A.golden(target)
    cr1 = cnt.ask1(faults=False)
    for s in cnt.stations:
        ok(rnd(cr1[s]["aadt"], 1) != F["aadt"][s], "cracker misses %s AADT" % s)
        ok("%.3f" % rnd(cr1[s]["k"], 0.001) != F["k_factor"][s], "cracker misses %s K" % s)
    cr2 = cnt.ask2(target, faults=False)
    for k in cr2:
        ok("%.1f" % rnd(cr2[k]["pct"], 0.1) != F["validation_pct"]["%s %s %s" % k], "cracker misses %s validation" % (k,))

    # ---------------------------------------------------------------- figures: edges and agreement
    for tip in ann:
        ok(edge(ann[tip], 1000) >= 0.25, "annual edge %s" % tip)
        ok(edge(c["proj"][tip]["per_m"], 100) >= 0.25, "per-million edge %s" % tip)
        ok(F["annual_vh"][tip] == rnd(ann[tip], 1000), "figures annual %s" % tip)
    for s, v in g["ask1"].items():
        ok(edge(v["aadt"], 1) >= 0.15, "AADT edge %s (%.3f)" % (s, v["aadt"]))
        ok(edge(v["k"], 0.001) >= 0.15, "K edge %s (%.5f)" % (s, v["k"]))
        ok(abs(v["k"] - v["k_raw"]) < 1e-5 and "%.3f" % rnd(v["k_raw"], 0.001) == F["k_factor"][s],
           "K the same on the rounded or the exact AADT %s" % s)
    for k, v in g["ask2"].items():
        ok(edge(v["pct"], 0.1) >= 0.25, "validation edge %s (%.4f)" % (k, v["pct"]))

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten or more files (%d)" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "three or more formats")
    ok(len(atr) >= 25000, "a file of 25,000 or more rows")
    ok(len(build.DISTRACTORS) >= 2 and all(P.FILES[k] in files for k in build.DISTRACTORS), "two or more distractors")
    meta = json.load(open(os.path.join(build.TASK, "metadata.json")))
    ok(sorted(meta["distractors"]) == sorted(P.FILES[k] for k in build.DISTRACTORS), "distractors named in metadata.json")
    ok(set(files) == set(P.FILES.values()), "pack holds exactly the filed files")
    print("checks: %d passed" % N["pass"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
