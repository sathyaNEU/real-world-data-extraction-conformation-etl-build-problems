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
            eq = A.ask_energy(P, split="hours_kw_quarter", meters=meters) if len(b) > 1 else e
            if all(abs((e[(i, q)] % 1) - 0.5) >= 0.15 and round(e[(i, q)]) == round(eq[(i, q)])
                   for i in b for q in range(1, 5)):
                break
    return PK.pump_energy(w, utc, frac)


def tune_meters(w, utc, frac):
    """Each council meter reads within its verified plus or minus 5 per cent; its error is set in 0.001 steps so every
    whole-ML quarterly volume sits at least 0.1 ML inside its bin whether a quarter-hour belongs to the local day it
    starts in or the day its reading is stamped on."""
    bt = w["bt"]
    q_utc = pd.date_range(utc[0], utc[-1] + pd.Timedelta(minutes=15), freq="15min")
    local = PK.utc_to_local_index(q_utc)
    end = local + pd.Timedelta(minutes=15)
    qs = [(pd.Timestamp(a), pd.Timestamp(b) + pd.Timedelta(days=1)) for a, b in
          [("2025-07-01", "2025-09-30"), ("2025-10-01", "2025-12-31"), ("2026-01-01", "2026-03-31"),
           ("2026-04-01", "2026-06-30")]]
    endday = end.normalize()
    for i in W.IDS:
        rate = 0.97 * bt.at[i, "cap"] * 1000 / 48.0
        v = np.repeat(frac[i] * rate / 2.0, 2)
        new = np.asarray((q_utc + pd.Timedelta(hours=12, minutes=15) > PK.PB4_SWAP) & (i == "PB4"))
        base = PK.METER_BIAS[i]
        for k in range(80):
            step = (k // 2 + 1) * 0.001 * (1 if k % 2 == 0 else -1) if k else 0.0
            bias = round(base + step, 3)
            vol = v * np.where(new, PK.PB4_NEW_BIAS, bias)
            good = True
            for a, b in qs:
                va = vol[np.asarray((local >= a) & (local < b))].sum() / 1000
                vb = vol[np.asarray((endday >= a) & (endday < b))].sum() / 1000
                if abs((va % 1) - 0.5) < 0.1 or round(va) != round(vb):
                    good = False
            if good:
                PK.METER_BIAS[i] = bias
                break


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
    tune_meters(w, utc, frac)
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
