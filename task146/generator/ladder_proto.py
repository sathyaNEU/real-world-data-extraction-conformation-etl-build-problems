"""Stage 2 measurement, kept for the resume: the golden's defensible constructions and the rivals on the published
view of the world (world.py), the rate's precision and how far the history rejects the rivals. Folded into calc.py at
stage 3, where every figure is recomputed from the shipped files instead of the simulation.

    python3 task146/generator/ladder_proto.py"""
import os, sys, datetime as dt, math
import numpy as np, pandas as pd
import statsmodels.api as sm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as K
import world as WD

T = WD.simulate()
S = T.sundays
A = K.ASOF_LAST_SUNDAY
ai = T.idx[A]
ti = T.idx[K.TARGET_SUNDAY]
# the published series: revised for every week but the latest, advance for the latest
pub = np.array([T.nat_revised[i] for i in range(ai + 1)], dtype=float)
pub[ai] = T.nat_advance[ai]
adv = np.array([T.nat_advance[i] for i in range(ai + 1)], dtype=float)
weeks = pd.DataFrame({"sun": S[:ai + 1], "rev": pub, "adv": adv})
weeks["q"] = [K.quarter_of(s) for s in weeks["sun"]]
weeks["kq"] = T.kq[:ai + 1]
# the program statistics: ineligible determinations by claims-week month, quarters by sum
pool = {}
for q in sorted(set(weeks["q"])):
    idx = [i for i in range(ai + 1) if T.quarter[i] == q]
    if len(idx) and T.quarter[ai] != q or q == T.quarter[ai]:
        pool[q] = float(sum(T.nat_inelig[i] for i in idx))
P = pool[(2026, 3)]
truth = T.target_expected_revised * (1 - T.target_late_share)
print("pool 2026Q3 %.0f  truth(expected advance) %.0f  realised advance %d" % (P, truth, T.nat_advance[ti]))

rows = []
for i in range(3, ai + 1):
    if T.kq[i] != 0:
        continue
    q = T.quarter[i]; pq = K.prev_quarter(q)
    if pq not in pool or pq == (2013, 4):
        continue
    rows.append(dict(q=q, qq=q[1], y=q[0], nq=pub[i], nqa=adv[i], p1=pub[i - 1], p2=pub[i - 2], p3=pub[i - 3],
                     n1=pub[i + 1] if i + 1 <= ai else np.nan, pool=pool[pq],
                     pqc=sum(pub[j] for j in range(ai + 1) if T.quarter[j] == pq)))
R = pd.DataFrame(rows)
p1, p2, p3 = pub[ai], pub[ai - 1], pub[ai - 2]
def D(df): return pd.get_dummies(df["qq"].astype(str), prefix="q", dtype=float)
out = {}
X = D(R); X["pool"] = R["pool"]; f = sm.OLS(R["nq"] - R["p1"], X).fit(); out["Ga prev+q-int"] = p1 + f.params["q_4"] + f.params["pool"] * P; ga_slope = f.params["pool"]
R4 = R[R.qq == 4]; f = sm.OLS(R4["nq"] - R4["p1"], sm.add_constant(R4["pool"])).fit(); out["Gb Q4 only"] = p1 + f.params["const"] + f.params["pool"] * P
X = D(R); X["pool"] = R["pool"]; f = sm.OLS(R["nq"] - (R["p1"] + R["p2"] + R["p3"]) / 3, X).fit(); out["Gc mean3"] = (p1 + p2 + p3) / 3 + f.params["q_4"] + f.params["pool"] * P
X = D(R); X["pr"] = R["pool"] / R["p1"]; f = sm.OLS(R["nq"] / R["p1"] - 1, X).fit(); out["Gd ratio"] = p1 * (1 + f.params["q_4"]) + f.params["pr"] * P
Rn = R[R.qq != 1]; X = D(Rn); X["pool"] = Rn["pool"]; f = sm.OLS(Rn["nq"] - Rn["p1"], X).fit(); out["Ge no Q1"] = p1 + f.params["q_4"] + f.params["pool"] * P
Rx = R[~R.y.isin([2020, 2021])]; X = D(Rx); X["pool"] = Rx["pool"]; f = sm.OLS(Rx["nq"] - Rx["p1"], X).fit(); out["Gf excl 20-21"] = p1 + f.params["q_4"] + f.params["pool"] * P
Rx = R[R.y >= 2019]; X = D(Rx); X["pool"] = Rx["pool"]; f = sm.OLS(Rx["nq"] - Rx["p1"], X).fit(); out["Gg since 2019"] = p1 + f.params["q_4"] + f.params["pool"] * P
Rx = R[R.y >= 2022]; X = D(Rx); X["pool"] = Rx["pool"]; f = sm.OLS(Rx["nq"] - Rx["p1"], X).fit(); out["Gh since 2022"] = p1 + f.params["q_4"] + f.params["pool"] * P
# excess over the mean of the week before and the fourth week (the refiling over by then)
Rk = R.dropna(subset=["n1"]).copy()
# advance-based
X = D(R); X["pool"] = R["pool"]; f = sm.OLS(R["nqa"] - R["p1"], X).fit(); out["Gi adv target"] = p1 + f.params["q_4"] + f.params["pool"] * P
# robust (Huber)
X = D(R); X["pool"] = R["pool"]; f = sm.RLM(R["nq"] - R["p1"], X, M=sm.robust.norms.HuberT()).fit(); out["Gj huber"] = p1 + f.params["q_4"] + f.params["pool"] * P
print("slope (first week per pool member) %.4f true %.4f" % (ga_slope, WD.R_TURN[0]))
# rivals
w = weeks.copy()
w["ma"] = w["rev"].rolling(52, center=True).mean(); w["ratio"] = w["rev"] / w["ma"]
w["yr"] = [s.year for s in w["sun"]]
w2 = w[(w["sun"] >= dt.date(2022, 1, 2)) & (w["sun"] <= dt.date(2025, 12, 28))]
fac_q = w2.groupby(["kq", w2["q"].map(lambda x: x[1])])["ratio"].mean()
lvl = np.mean([pub[ai - j] / fac_q[(T.kq[ai - j], T.quarter[ai - j][1])] for j in range(4)])
out["R0 default (quarter-week factors x level4)"] = lvl * fac_q[(0, 4)]
w2 = w2.copy(); w2["iso"] = [ (s + dt.timedelta(days=6)).isocalendar()[1] for s in w2["sun"]]
fac_i = w2.groupby("iso")["ratio"].mean()
isos = [(S[ai - j] + dt.timedelta(days=6)).isocalendar()[1] for j in range(4)]
lvl_i = np.mean([pub[ai - j] / fac_i[isos[j]] for j in range(4)])
out["R0b iso-week factors x level4"] = lvl_i * fac_i[(K.TARGET_SUNDAY + dt.timedelta(days=6)).isocalendar()[1]]
ly = T.idx[dt.date(2025, 10, 5)]
g8 = pub[ai - 7:ai + 1].sum() / np.array([T.nat_revised[j] for j in range(ly - 8, ly)]).sum()
out["R1 yoy"] = T.nat_revised[ly] * g8
X = D(R); f = sm.OLS(R["nq"] - R["p1"], X).fit(); out["R2 q-dummy"] = p1 + f.params["q_4"]
X = D(R); X["pqc"] = R["pqc"]; f = sm.OLS(R["nq"] - R["p1"], X).fit(); pqc26 = sum(pub[j] for j in range(ai + 1) if T.quarter[j] == (2026, 3)); out["R3 level-driven"] = p1 + f.params["q_4"] + f.params["pqc"] * pqc26
X = D(R); f = sm.OLS(R["nq"] / R["p1"] - 1, X).fit(); out["R4 ratio dummy"] = p1 * (1 + f.params["q_4"])
# a regression of weekly claims on lags and a quarter-start term, logs
w3 = w.dropna().copy()
gold = out["Ga prev+q-int"]
for k, v in out.items():
    print("%-44s %8.0f  r=%6d  d=%+6.0f  clr=%.2f" % (k, v, K.round_to(v, 1000), v - gold, K.bin_clearance(v, 1000)))
gv = [v for k, v in out.items() if k.startswith("G")]
print("golden spread %.0f..%.0f (%.0f)" % (min(gv), max(gv), max(gv) - min(gv)))



# ---- precision, rejection margins and twin pairs
X = D(R); X["pool"] = R["pool"]; f = sm.OLS(R["nq"] - R["p1"], X).fit()
print("Ga slope %.4f se %.4f  r2 %.3f  resid sd %.0f  n %d" % (f.params["pool"], f.bse["pool"], f.rsquared, np.sqrt(f.scale), len(R)))
print("one sigma on the slope moves the call by %.0f" % (f.bse["pool"] * P))
X0 = D(R); f0 = sm.OLS(R["nq"] - R["p1"], X0).fit()
print("dummy-only r2 %.3f resid sd %.0f" % (f0.rsquared, np.sqrt(f0.scale)))
X3 = D(R); X3["pqc"] = R["pqc"]; f3 = sm.OLS(R["nq"] - R["p1"], X3).fit()
print("level-driven r2 %.3f resid sd %.0f" % (f3.rsquared, np.sqrt(f3.scale)))
# errors at the turns after the highest-pool quarters (excluding 2020): leave-one-out errors of each model
R = R.reset_index(drop=True)
def loo(cols):
    errs = []
    for k in range(len(R)):
        tr = R.drop(index=k)
        Xt = D(tr)
        for c in cols: Xt[c] = tr[c]
        ft = sm.OLS(tr["nq"] - tr["p1"], Xt).fit()
        xk = D(R).iloc[[k]]
        for c in cols: xk[c] = R.loc[[k], c]
        xk = xk.reindex(columns=Xt.columns, fill_value=0.0)
        errs.append(float((R.loc[k, "nq"] - R.loc[k, "p1"]) - ft.predict(xk).iloc[0]))
    return np.array(errs)
e_pool, e_dum, e_lvl = loo(["pool"]), loo([]), loo(["pqc"])
hi = R["pool"] >= R["pool"].quantile(0.8)
print("LOO RMSE all turns: pool %.0f dummy %.0f level %.0f" % (np.sqrt((e_pool**2).mean()), np.sqrt((e_dum**2).mean()), np.sqrt((e_lvl**2).mean())))
print("LOO mean abs error, the fifth of turns after the largest pools: pool %.0f dummy %.0f level %.0f (n=%d)" % (np.abs(e_pool[hi]).mean(), np.abs(e_dum[hi]).mean(), np.abs(e_lvl[hi]).mean(), hi.sum()))
print(R.loc[hi, ["q", "pool", "pqc"]].to_string())
# twin search: Q2-Q4 turns with prior-quarter claims within 3 per cent and pools at least 1.8x apart
cand = R[R.qq != 1].reset_index(drop=True)
best = None
for a in range(len(cand)):
    for b in range(a + 1, len(cand)):
        ra, rb = cand.loc[a], cand.loc[b]
        if abs(ra.pqc / rb.pqc - 1) < 0.03 and max(ra.pool, rb.pool) / min(ra.pool, rb.pool) > 1.8:
            ex_a, ex_b = ra.nq - ra.p1, rb.nq - rb.p1
            print("twin", ra.q, rb.q, int(ra.pqc), int(rb.pqc), int(ra.pool), int(rb.pool), int(ex_a), int(ex_b))
