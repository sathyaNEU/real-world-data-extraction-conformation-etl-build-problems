"""Design-time ladder on the clean truth (never shipped)."""
import numpy as np, pandas as pd
from common import PROVIDERS
from world import build_all
from truth import golden_truth, place, cell_impute, KEYS

A = build_all()
g, el, netE = golden_truth(A)
names = {p["key"]: p["name"].split()[0][:5] for p in PROVIDERS}


def show(lab, s):
    aw = place(s)
    print(f"{lab:10s}", " ".join(f"{names[k]}:{s[k]:5.2f}" for k in KEYS), "|",
          " ".join(f"{names[k][:4]}{aw[k]}" for k in KEYS if aw[k] > 0))


res = {}
res["R0raw"] = {k: el[(el.prov == k) & el.resp].chg.mean() for k in KEYS}
nE_r = el[el.resp].E.mean()
res["R1resp"] = {k: nE_r + el[(el.prov == k) & el.resp].d.mean() for k in KEYS}
res["R1b"] = {k: netE + el[(el.prov == k) & el.resp].d.mean() for k in KEYS}
X = ["pre_obs", "age", "female", "smoker", "prev", "symp12", "disc"]


def regimp(m, cols):
    rr = m[m.resp]
    Am = np.column_stack([np.ones(len(rr))] + [rr[c].astype(float) for c in cols])
    beta, *_ = np.linalg.lstsq(Am, rr.d.values, rcond=None)
    nn = m[~m.resp]
    B = np.column_stack([np.ones(len(nn))] + [nn[c].astype(float) for c in cols])
    return (rr.d.sum() + (B @ beta).sum()) / len(m)


res["R2cmix"] = {k: netE + regimp(el[el.prov == k], X) for k in KEYS}
res["AtExp"] = {k: netE + np.where(el[el.prov == k].resp, el[el.prov == k].d, 0).mean() for k in KEYS}
res["BOCF"] = {k: netE + (np.where(el[el.prov == k].resp, el[el.prov == k].chg, 0) - el[el.prov == k].E).mean() for k in KEYS}
res["GOLD"] = g
for lab, s in res.items():
    show(lab, s)
fam = {}
for fl in ["f30", "f90", "f365"]:
    fam["cell_" + fl] = cell_impute(el, fl, netE)
    fam["reg_" + fl] = {k: netE + regimp(el[el.prov == k], [fl] + X) for k in KEYS}
for lab, s in fam.items():
    show(lab, s)
print("netE", round(netE, 3), "eligible", len(el), "resp", round(el.resp.mean(), 3))
print("max spread vs GOLD", {names[k]: round(max(abs(fam[f][k] - g[k]) for f in fam), 3) for k in KEYS})
print("bin dist", {names[k]: round(min(abs(fam[f][k] - np.floor(fam[f][k]) - 0.5) for f in list(fam) + []), 2) for k in KEYS})
print("resp by flag", el.groupby("f90").resp.mean().round(3).to_dict(), "d by flag(resp)", el[el.resp].groupby("f90").d.mean().round(2).to_dict())
