"""Ladder on the clean truth (design-time tuning only; never shipped)."""
import numpy as np, pandas as pd, sys
from common import PROVIDERS, CASEMIX, VOLUME_2027, FLOOR
from world import build_world

w = build_world()
w = w[w.fy.isin(["2023-24", "2024-25"])].copy()
w["pre_obs"] = (np.round(w.pre_true / 2) * 2).clip(0, 100)
w["post_obs"] = (np.round(w.post_true / 2) * 2).clip(0, 100)
w["chg"] = w.pre_obs - w.post_obs
E = (CASEMIX["intercept"] + CASEMIX["pre_odi_minus_45"] * (w.pre_obs - 45) + CASEMIX["age_minus_55"] * (w.age.astype(int) - 55)
     + CASEMIX["female"] * w.female + CASEMIX["smoker"] * w.smoker + CASEMIX["previous_lumbar_surgery"] * w.prev
     + CASEMIX["symptoms_over_12_months"] * w.symp12 + CASEMIX["disc_herniation"] * w.disc)
w["E"] = E
el = w[w.pre_done & ~w.died_12m].copy()
el["d"] = el.chg - el.E
netE = el.E.mean()
names = {p["key"]: p["name"].split()[0] for p in PROVIDERS}
cap = {p["key"]: p["cap"] for p in PROVIDERS}
keys = [p["key"] for p in PROVIDERS]


def place(s):
    order = sorted([k for k in keys if s[k] >= FLOOR], key=lambda k: -s[k])
    left, aw = VOLUME_2027, {}
    for k in order:
        a = min(cap[k], left); aw[k] = a; left -= a
        if left <= 0: break
    return {k: aw.get(k, 0) for k in keys}


def show(lab, s):
    aw = place(s)
    print(f"{lab:9s}", " ".join(f"{names[k][:5]}:{s[k]:5.2f}" for k in keys), "|",
          " ".join(f"{names[k][:4]}{aw[k]}" for k in keys if aw[k] > 0))
    return s

res = {}
res["TRUE"] = {k: netE + el[el.prov == k].d.mean() for k in keys}
res["R0raw"] = {k: el[(el.prov == k) & el.resp_12m].chg.mean() for k in keys}
res["R1resp"] = {k: netE + el[(el.prov == k) & el.resp_12m].d.mean() for k in keys}
res["BOCF"] = {k: netE + (np.where(el[el.prov == k].resp_12m, el[el.prov == k].chg, 0) - el[el.prov == k].E).mean() for k in keys}
res["AtExp"] = {k: netE + np.where(el[el.prov == k].resp_12m, el[el.prov == k].d, 0).mean() for k in keys}
g = {}
for k in keys:
    m = el[el.prov == k]
    tot = 0.0
    for c in (False, True):
        cell = m[m.comp == c]
        mu = cell[cell.resp_12m].d.mean()
        tot += cell[cell.resp_12m].d.sum() + mu * (~cell.resp_12m).sum()
    g[k] = netE + tot / len(m)
res["GOLD"] = g
for lab, s in res.items():
    show(lab, s)
print("netE", round(netE, 3), "eligible", len(el), "resp", round(el.resp_12m.mean(), 3))
print("comp", {names[k][:5]: round(el[el.prov == k].comp.mean(), 3) for k in keys})
print("resp", {names[k][:5]: round(el[el.prov == k].resp_12m.mean(), 3) for k in keys})
print("gold-R1", {names[k][:5]: round(g[k] - res['R1resp'][k], 2) for k in keys})
