"""Design-time: move each provider's effect so its full-population outcome sits on its target."""
import json, re, numpy as np, pandas as pd, importlib
import common, world
TARGET = {40117: 15.08, 40152: 15.93, 40188: 12.88, 41206: 15.12, 41231: 17.06, 41274: 13.91, 41309: 13.04,
          41355: 15.04, 41388: 13.95, 41402: 12.97}

def golden_scores():
    importlib.reload(world)
    w = world.build_world()
    w = w[w.fy.isin(["2023-24", "2024-25"])].copy()
    w["pre_obs"] = (np.round(w.pre_true / 2) * 2).clip(0, 100)
    w["post_obs"] = (np.round(w.post_true / 2) * 2).clip(0, 100)
    w["chg"] = w.pre_obs - w.post_obs
    C = common.CASEMIX
    w["E"] = (C["intercept"] + C["pre_odi_minus_45"] * (w.pre_obs - 45) + C["age_minus_55"] * (w.age.astype(int) - 55)
              + C["female"] * w.female + C["smoker"] * w.smoker + C["previous_lumbar_surgery"] * w.prev
              + C["symptoms_over_12_months"] * w.symp12 + C["disc_herniation"] * w.disc)
    el = w[w.pre_done & ~w.died_12m].copy()
    el["d"] = el.chg - el.E
    el["f90"] = el.emerg.apply(lambda ev: any(t <= 90 for k, t in ev))
    netE = el.E.mean()
    out = {}
    for k in TARGET:
        m = el[el.prov == k]
        tot = 0.0
        for c in (False, True):
            cell = m[m.f90 == c]
            tot += cell[cell.resp_12m].d.sum() + cell[cell.resp_12m].d.mean() * (~cell.resp_12m).sum()
        out[k] = netE + tot / len(m)
    return out

for it in range(4):
    g = golden_scores()
    for p in common.PROVIDERS:
        p["u"] = round(p["u"] + (TARGET[p["key"]] - g[p["key"]]), 3)
    print(it, {k: round(g[k], 3) for k in g})
print({p["key"]: p["u"] for p in common.PROVIDERS})
import json; json.dump({p['key']: p['u'] for p in common.PROVIDERS}, open('/tmp/claude-0/-home-user-real-world-data-extraction-conformation-etl-build-problems/ecc55210-d8ca-5df7-bc82-5621272de73c/scratchpad/t264/u.json','w'))
