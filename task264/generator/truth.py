"""The policy's quantities computed on the clean truth (the generator's own path, used for tuning and
for checks.py's comparison with analysis.py, which reads only target/)."""
import datetime as dt
import numpy as np
import pandas as pd
from common import PROVIDERS, CASEMIX, CALL_FROM, CALL_TO, VOLUME_2027, FLOOR, MIN_SECTIONS, WINDOW_PRE_DAYS

KEYS = [p["key"] for p in PROVIDERS]
CAP = {p["key"]: p["cap"] for p in PROVIDERS}
D = dt.timedelta


def eligible_frame(A):
    w = A["ops"]
    m = w[(w.op_date >= CALL_FROM) & (w.op_date <= CALL_TO)].copy()
    pre_ok = m.pre_done & (m.n_pre >= MIN_SECTIONS) & (m.pre_c <= m.op_date) & \
        ((m.op_date - m.pre_c).apply(lambda x: x.days) <= WINDOW_PRE_DAYS - 1)
    dead = set(A["deaths"].loc[:, "pseudo"]) if len(A["deaths"]) else set()
    dd = dict(zip(A["deaths"].pseudo, A["deaths"].dod))
    alive = m.apply(lambda r: not (r.pseudo in dd and dd[r.pseudo] <= r.op_date + D(days=365)), axis=1)
    el = m[pre_ok & alive].copy()
    days = (el.m12_c - el.op_date).apply(lambda x: x.days)
    el["resp"] = el.resp_12m & ~el.died_12m & (el.n_m12 >= MIN_SECTIONS) & (days >= 7 * 48) & (days <= 7 * 64) & \
        (el.m12_c <= dt.date(2026, 9, 30))
    el["pre_obs"] = el.pre_score
    el["post_obs"] = el.post_score
    el["chg"] = el.pre_obs - el.post_obs
    el["E"] = (CASEMIX["intercept"] + CASEMIX["pre_odi_minus_45"] * (el.pre_obs - 45)
               + CASEMIX["age_minus_55"] * (el.age.astype(int) - 55) + CASEMIX["female"] * el.female
               + CASEMIX["smoker"] * el.smoker + CASEMIX["previous_lumbar_surgery"] * el.prev
               + CASEMIX["symptoms_over_12_months"] * el.symp12 + CASEMIX["disc_herniation"] * el.disc)
    el["d"] = el.chg - el.E
    return el


def flags(A, el):
    """Later emergency admissions per eligible operation (the truth's own record of them)."""
    s = A["spells"]
    s = s[s.version == 1]
    em = s[s.meth.isin(["21", "22", "23", "24", "28"])]
    idx = s[s.kind == "index"][["pid", "dis"]].rename(columns={"dis": "idis"})
    em = em.merge(idx, on="pid")
    out = {}
    for lab, lo_from, days in [("f30", "dis", 30), ("f90", "dis", 90), ("f365", "op", 365)]:
        out[lab] = set()
    ops = el.set_index("pid")
    for r in em.itertuples():
        if r.pid not in ops.index:
            continue
        op = ops.loc[r.pid, "op_date"]
        if r.idis is not None and r.adm > r.idis and (r.adm - r.idis).days <= 30:
            out["f30"].add(r.pid)
        if r.idis is not None and r.adm > r.idis and (r.adm - r.idis).days <= 90:
            out["f90"].add(r.pid)
        if r.adm > op and (r.adm - op).days <= 365:
            out["f365"].add(r.pid)
    for lab in out:
        el[lab] = el.pid.isin(out[lab])
    return el


def place(score):
    order = sorted([k for k in KEYS if score[k] >= FLOOR], key=lambda k: -score[k])
    left, aw = VOLUME_2027, {}
    for k in order:
        a = min(CAP[k], left)
        aw[k] = a
        left -= a
        if left <= 0:
            break
    return {k: aw.get(k, 0) for k in KEYS}


def cell_impute(el, flag, netE):
    out = {}
    for k in KEYS:
        m = el[el.prov == k]
        tot = 0.0
        for c in (False, True):
            cell = m[m[flag] == c]
            mu = cell[cell.resp].d.mean()
            tot += cell[cell.resp].d.sum() + mu * (~cell.resp).sum()
        out[k] = netE + tot / len(m)
    return out


def golden_truth(A, flag="f90"):
    el = flags(A, eligible_frame(A))
    netE = el.E.mean()
    return cell_impute(el, flag, netE), el, netE
