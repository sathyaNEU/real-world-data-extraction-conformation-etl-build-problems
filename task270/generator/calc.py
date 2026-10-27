"""task270 the call, computed from the cut pack: each team's assessed patients (their latest completed 2026 fortnight,
the team holding their care on its first day), each patient's negative affect at every answered prompt, and the
patient's emotional instability under each route a solver could take, then each team's share at 2.0 or more.

The golden reads each patient's change over the collaborative's three hours from the same-day ratings 2.5 to 3.5 hours
apart (route W). The standing family reads the same quantity other ways (W2, K2, E, ET); the wrong rungs read the trust
app's own spacing (R1 adjacent prompts, R2 successive answered prompts, R0 across the fortnight) or stretch the
adjacent change to three hours in proportion to the time between the ratings (R3)."""
from __future__ import annotations

import datetime as dt
import math
import os

import numpy as np
import pandas as pd

import common as K

ROUTES = ("R0", "R1", "R2", "R3", "W", "W2", "K2", "E", "ET")
FAMILY = ("W", "W2", "K2", "E", "ET")
TAUS = np.linspace(0.5, 15.0, 59)


def load(target=None, scale_v3=10.0, keep_resends=False, scheduled_clock=False, drop_second_codes=False):
    """Every answered prompt as (patient, local date, block, local answer time, negative affect), plus every sent
    prompt for the completion count."""
    target = target or K.TARGET
    v3 = pd.read_csv(os.path.join(target, K.F_V3), dtype=str, keep_default_na=False)
    v4 = pd.read_csv(os.path.join(target, K.F_V4), dtype=str, keep_default_na=False)
    en = pd.read_csv(os.path.join(target, K.F_ENROL), dtype=str, keep_default_na=False)
    code2pt = dict(zip(en.participant_code, en.patient_number))
    if drop_second_codes:
        reg = pd.read_excel(os.path.join(target, K.F_REGISTER), dtype=str)
        keep = set(reg["App code"])
        code2pt = {c: p for c, p in code2pt.items() if c in keep}
    a3 = v3.copy()
    a3["patient"] = a3.participant_id.map(code2pt)
    a3["sent"] = pd.to_datetime(a3.scheduled_local, format="%d/%m/%Y %H:%M")
    a3["answered"] = pd.to_datetime(a3.responded_local.replace("", None), format="%d/%m/%Y %H:%M:%S")
    a3["block"] = a3.beep.astype(int)
    items3 = ["na_down_vas", "na_anxious_vas", "na_irritable_vas", "na_ashamed_vas"]
    a3["na"] = a3[items3].replace("", np.nan).astype(float).mean(axis=1) / scale_v3
    if not keep_resends:
        v4 = v4.drop_duplicates()
    a4 = v4.copy()
    a4["patient"] = a4.participant.map(code2pt)
    su = pd.to_datetime(a4.sent_at_utc, format="%Y-%m-%dT%H:%M:%SZ")
    au = pd.to_datetime(a4.answered_at_utc.replace("", None), format="%Y-%m-%dT%H:%M:%SZ")
    bst_on = (su >= pd.Timestamp(K.BST_START)) & (su < pd.Timestamp(K.BST_END))
    a4["sent"] = su + pd.to_timedelta(bst_on.astype(int), unit="h")
    bst_a = (au >= pd.Timestamp(K.BST_START)) & (au < pd.Timestamp(K.BST_END))
    a4["answered"] = au + pd.to_timedelta(bst_a.fillna(False).astype(int), unit="h")
    a4["block"] = a4.block.astype(int)
    a4["na"] = a4[["down", "anxious", "irritable", "ashamed"]].replace("", np.nan).astype(float).mean(axis=1)
    cols = ["patient", "sent", "answered", "block", "na"]
    allp = pd.concat([a3[cols], a4[cols]], ignore_index=True)
    allp = allp[allp.patient.notna()]
    if scheduled_clock:
        allp["answered"] = allp["answered"].where(allp["answered"].isna(), allp["sent"])
    allp["day"] = allp.sent.dt.date
    return allp


def episodes(target=None):
    ep = pd.read_csv(os.path.join(target or K.TARGET, K.F_EPISODES), dtype=str, keep_default_na=False)
    out = {}
    for r in ep.itertuples(index=False):
        out.setdefault(r.patient_number, []).append(
            (r.team_code, dt.date.fromisoformat(r.episode_start),
             dt.date.fromisoformat(r.episode_end) if r.episode_end else None))
    return out


def team_on(eps, patient, day):
    for team, s, e in eps.get(patient, []):
        if s <= day and (e is None or e >= day):
            return team
    return None


def register(target=None):
    reg = pd.read_excel(os.path.join(target or K.TARGET, K.F_REGISTER), dtype={"Patient number": str, "App code": str})
    reg["First day"] = pd.to_datetime(reg["First day"]).dt.date
    reg["Last day"] = pd.to_datetime(reg["Last day"]).dt.date
    return reg


def population(allp, reg, eps, rule="latest", completion="answered", team_day="first"):
    """The assessed patients: (patient, first day, last day, team) for each counted fortnight."""
    ans = allp[allp.answered.notna()]
    grp = {}
    for pt, day in zip(ans.patient, ans.day):
        grp.setdefault(pt, []).append(day)
    rows = []
    for r in reg.itertuples(index=False):
        pt, code_, f, l, status = r[1], r[2], r[3], r[4], r[6]
        if not (K.YEAR0 <= f <= K.YEAR1):
            continue
        n_ans = sum(1 for d in grp.get(pt, []) if f <= d <= l)
        done = (n_ans >= K.COMPLETE) if completion == "answered" else (status == "Completed")
        if done:
            rows.append((pt, f, l))
    by = {}
    for pt, f, l in rows:
        by.setdefault(pt, []).append((f, l))
    out = []
    for pt, fs in by.items():
        fs.sort()
        chosen = fs if rule == "every" else ([fs[-1]] if rule == "latest" else [fs[0]])
        for f, l in chosen:
            day = {"first": f, "enrolled": f - dt.timedelta(days=3), "census": K.CENSUS}[team_day]
            team = team_on(eps, pt, day)
            if team is None:
                team = team_on(eps, pt, f)
            out.append((pt, f, l, K.CURRENT[team]))
    return out


def fit_exp(g, q, taus=TAUS):
    best = None
    for t in taus:
        X = np.c_[1 - np.exp(-g / t), np.ones_like(g)]
        c = np.linalg.lstsq(X, q, rcond=None)[0]
        r = ((X @ c - q) ** 2).sum()
        if best is None or r < best[0]:
            best = (r, t, c)
    return best


def pairs_of(df):
    """Same-day pairs of a patient fortnight's answered prompts: (block i, block j, gap hours, squared change,
    adjacent in answered order)."""
    out = []
    for day, g in df.groupby("day", sort=True):
        g = g.sort_values("answered")
        b = g.block.to_numpy()
        t = g.answered.to_numpy()
        y = g.na.to_numpy()
        n = len(g)
        for i in range(n):
            for j in range(i + 1, n):
                gap = (t[j] - t[i]) / np.timedelta64(1, "h")
                out.append((b[i], b[j], gap, (y[j] - y[i]) ** 2, j == i + 1))
    return out


def rmssd(vals):
    return math.sqrt(sum(vals) / len(vals)) if len(vals) else float("nan")


def instability(allp, pop, fits=True):
    """Each counted patient fortnight's instability under every route (fits=False: the curve fits E and ET left out)."""
    ans = allp[allp.answered.notna()]
    by_pt = {pt: g for pt, g in ans.groupby("patient")}
    res = []
    for pt, f, l, team in pop:
        g = by_pt[pt]
        g = g[(g.day >= f) & (g.day <= l)]
        P = pairs_of(g)
        o = {"patient": pt, "first": f, "team": team, "answered": len(g)}
        o["R1"] = rmssd([p[3] for p in P if p[1] == p[0] + 1])
        o["R2"] = rmssd([p[3] for p in P if p[4]])
        o["R3"] = rmssd([p[3] * 3.0 / p[2] for p in P if p[1] == p[0] + 1])
        o["W"] = rmssd([p[3] for p in P if 2.5 <= p[2] <= 3.5])
        o["W2"] = rmssd([p[3] for p in P if 2.75 <= p[2] <= 3.25])
        o["K2"] = rmssd([p[3] for p in P if p[1] == p[0] + 2])
        gg = g.sort_values("answered")
        y = gg.na.to_numpy()
        o["R0"] = rmssd(list(np.diff(y) ** 2))
        gap = np.array([p[2] for p in P])
        sq = np.array([p[3] for p in P])
        if fits:
            _r, t, c = fit_exp(gap, sq)
            o["E"] = math.sqrt(max(c[0] * (1 - math.exp(-3 / t)) + c[1], 0.0))
        o["_gap"], o["_sq"] = gap, sq
        res.append(o)
    if not fits:
        for o in res:
            del o["_gap"], o["_sq"]
        return res
    # one time constant per team, each patient's own level and noise
    for team in {o["team"] for o in res}:
        mine = [o for o in res if o["team"] == team]
        best = None
        for t in TAUS:
            tot = 0.0
            for o in mine:
                X = np.c_[1 - np.exp(-o["_gap"] / t), np.ones_like(o["_gap"])]
                c = np.linalg.lstsq(X, o["_sq"], rcond=None)[0]
                tot += ((X @ c - o["_sq"]) ** 2).sum()
            if best is None or tot < best[0]:
                best = (tot, t)
        t = best[1]
        for o in mine:
            X = np.c_[1 - np.exp(-o["_gap"] / t), np.ones_like(o["_gap"])]
            c = np.linalg.lstsq(X, o["_sq"], rcond=None)[0]
            o["ET"] = math.sqrt(max(c[0] * (1 - math.exp(-3 / t)) + c[1], 0.0))
    for o in res:
        del o["_gap"], o["_sq"]
    return res


def shares(res, route):
    out = {}
    for c, _n in K.TEAMS:
        mine = [o[route] for o in res if o["team"] == c]
        hi = sum(1 for v in mine if v >= K.HIGH)
        out[c] = {"n": len(mine), "high": hi, "share": hi / len(mine)}
    return out


def funded(sh):
    return sorted(c for c, v in sh.items() if 100 * v["share"] >= K.LINE)


def pooled_change(allp, pop, lo, hi):
    """The mean squared change in negative affect over every counted patient's same-day pairs lo to hi hours
    apart, and the number of pairs."""
    ans = allp[allp.answered.notna()]
    by_pt = {pt: g for pt, g in ans.groupby("patient")}
    vals = []
    for pt, f, l, team in pop:
        g = by_pt[pt]
        g = g[(g.day >= f) & (g.day <= l)]
        vals.extend(p[3] for p in pairs_of(g) if lo <= p[2] <= hi)
    return float(np.mean(vals)), len(vals)


def adjacent_gap_median(allp, pop):
    ans = allp[allp.answered.notna()]
    by_pt = {pt: g for pt, g in ans.groupby("patient")}
    gaps = []
    for pt, f, l, team in pop:
        g = by_pt[pt]
        g = g[(g.day >= f) & (g.day <= l)]
        gaps.extend(p[2] for p in pairs_of(g) if p[1] == p[0] + 1)
    return float(np.median(gaps)) * 60.0


def main_call(target=None):
    allp = load(target)
    reg = register(target)
    eps = episodes(target)
    pop = population(allp, reg, eps)
    res = instability(allp, pop)
    return allp, reg, eps, pop, res
