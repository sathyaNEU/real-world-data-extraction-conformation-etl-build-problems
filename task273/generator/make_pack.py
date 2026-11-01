"""Builds target/ from the world: the plan first (last summer's takes per bore, PB9 at its tested rate), then
every file in its system's own form, then the file dates."""
import datetime as dt
import math
import os

import numpy as np
import pandas as pd

import docs as D
import pack as PK
import params as P
import world as W

STAMP = (2026, 11, 2, 8, 40, 0)
PLAN_STEP = 0.05


def base_plan(w):
    """The plan carries each existing bore at its 2025-26 average take for the month, in the operations' 0.05 ML/d
    step, and PB9 at the rate it held through its constant-rate test."""
    tk = w["takes"]
    plan = {}
    for m in P.SUMMER_MONTHS:
        y = 2025 if m == 12 else 2026
        sel = tk[(tk.index.year == y) & (tk.index.month == m)]
        plan[m] = {i: round(round(sel[i].mean() / PLAN_STEP) * PLAN_STEP, 2) for i in W.IDS}
        plan[m]["PB9"] = 4.40
    return plan


def truth_levels(w, plan):
    """Lowest level (m bmp) per existing bore and month under the plan, from the world's own coefficients."""
    bt, a, mb = w["bt"], w["a"], w["mb"]
    out = {}
    for m in P.SUMMER_MONTHS:
        y = P.DROUGHT_YEAR if m == 12 else P.DROUGHT_YEAR + 1
        lo = float(mb[(mb.index.year == y) & (mb.index.month == m)].min())
        q = plan[m]
        for i in W.IDS:
            nb = sum(a.at[i, j] * q[j] for j in W.ALL if j != i)
            rl = lo + P.MB_DATUM_OFFSET + bt.at[i, "offset"] - bt.at[i, "own"] * q[i] - nb
            out[(i, m)] = bt.at[i, "mp_rl"] - rl
    return out


def edge_distance(v):
    r = v / P.GRADE_STEP
    return abs(r - math.floor(r) - 0.5) * P.GRADE_STEP


def tune_plan(w, plan):
    """Nudge each existing bore's monthly take by whole 0.05 ML/d steps (at most 0.30 either way) until every
    lowest level sits at least BIN_FLOOR inside its reporting bin."""
    plan = {m: dict(v) for m, v in plan.items()}
    for _ in range(40):
        lev = truth_levels(w, plan)
        bad = [(k, v) for k, v in lev.items() if edge_distance(v) < P.BIN_FLOOR]
        if not bad:
            break
        (i, m), v = min(bad, key=lambda kv: edge_distance(kv[1]))
        base = plan[m][i]
        best = None
        for s in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5, 6, -6):
            trial = {mm: dict(vv) for mm, vv in plan.items()}
            trial[m][i] = round(base + s * PLAN_STEP, 2)
            tl = truth_levels(w, trial)
            score = min(edge_distance(x) for (ii, mm), x in tl.items() if mm == m)
            if best is None or score > best[0] + 1e-9:
                best = (score, trial)
            if score >= P.BIN_FLOOR:
                break
        plan = best[1]
    return plan


def tune_load(w, utc, local, frac, target, path):
    """Each pump's load factor is set within its maker's band (0.86 to 0.97) in 0.002 steps, one value per
    switchboard, so every electricity-per-ML figure sits at least 0.15 kWh/ML inside its whole-number bin."""
    import analysis as A
    PK.write_icp(w, utc, local, PK.pump_energy(w, utc, frac), path)
    boards = [["PB1"], ["PB2"], ["PB3"], ["PB4"], ["PB5", "PB6"], ["PB7", "PB8"]]
    P = A.Pack(target)
    meters = A.ask_meters(P)
    for b in boards:
        base = PK.LOAD[b[0]]
        for k in range(60):
            step = (k // 2 + 1) * 0.002 * (1 if k % 2 == 0 else -1) if k else 0.0
            for i in b:
                PK.LOAD[i] = round(base + step, 3)
            PK.write_icp(w, utc, local, PK.pump_energy(w, utc, frac), path)
            e = A.ask_energy(P, meters=meters)
            if all(abs((e[(i, q)] % 1) - 0.5) >= 0.15 for i in b for q in range(1, 5)):
                break
    return PK.pump_energy(w, utc, frac)


def build(target, plan=None, w=None):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    w = w or W.simulate()
    plan = plan or tune_plan(w, base_plan(w))
    f = lambda k: os.path.join(target, PK.FILES[k])
    n = {}
    n["daily"] = PK.write_daily(w, f("daily"))
    n["mb1"] = PK.write_mb1(w, f("mb1"))
    PK.write_register(w, f("register"))
    n["test"] = PK.write_test(w, f("test"))
    PK.write_plan(plan, f("plan"))
    D.standard(f("standard"))
    D.permit(f("permit"))
    utc, local, frac = PK.pump_halfhours(w)
    n["telemetry"], meter_truth, q_utc = PK.write_telemetry(w, utc, frac, f("telemetry"))
    PK.write_icp_register(f("icp_reg"))
    energy = tune_load(w, utc, local, frac, target, f("icp"))
    n["icp"] = PK.write_icp(w, utc, local, energy, f("icp"))
    n["nitrate"] = PK.write_nitrate(f("nitrate"))
    n["rain"] = PK.write_rain(w, f("rain"))
    t = dt.datetime(*STAMP).timestamp()
    for k in PK.FILES:
        os.utime(f(k), (t, t))
    truth = {"utc": utc, "local": local, "frac": frac, "energy": energy, "meter": meter_truth, "q_utc": q_utc}
    return w, plan, n, truth
