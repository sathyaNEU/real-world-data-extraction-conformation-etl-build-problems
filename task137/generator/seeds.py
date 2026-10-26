"""Seed screen for the shipped world, run on the generator's clean world (no pack): the staffing seed stays at SEED, so
the e-roster's sickness is unchanged, and the demand stream's seed and the deterrence's strength are screened for the
margins of every route that bears on the call: the golden family (the window the fit picks, weekly distributed lags,
weekly totals), the geometric decay at the cell's top edge, the round 2 Opus reader's ten daily lags and its variants,
twenty and thirty daily lags, the default, and the practices with a clinic against those without.

    python3 task137/generator/seeds.py task137/generator WEEKS K SEED0 SEED1
"""
import datetime as dt
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")
sys.path.insert(0, sys.argv[1])
import params as P
import world as W

G = 1.035 ** 2
LO, HI = 43750, 46250


def frame(w):
    n = sum(1 for d in w["days"] if d <= P.REC_END)
    D = pd.DataFrame({"d": w["days"][:n], "wk": w["wk"][:n], "ro": w["ro"][:n].astype(int), "pbh": w["pbh"][:n].astype(int),
                      "t": w["t"][:n], "AP": w["A"]["P"][:n], "AN": w["A"]["N"][:n], "AH": w["A"]["H"][:n]})
    D["AG"] = D.AP + D.AN
    D["wd"] = [x.weekday() for x in D.d]
    D["mo"] = [x.month for x in D.d]
    D["fy"] = [W.fy(x) for x in D.d]
    wk = D.groupby("wk").ro.agg(["sum", "size"])
    sh = (wk["sum"] / wk["size"]).to_dict()
    for j in range(1, 27):
        D["w%d" % j] = [sh.get(x - dt.timedelta(7 * j), 0.0) for x in D.wk]
    return D


def calX(D, extra=(), month=True, fyd=False, trend=True, pbh=True):
    Z = pd.get_dummies(D[["wd", "mo"] if month else ["wd"]].astype(str), drop_first=True).astype(float)
    if fyd:
        Z = pd.concat([Z, pd.get_dummies(D[["fy"]].astype(str), drop_first=True).astype(float)], axis=1)
    if trend:
        Z["t"] = D.t.values
    if pbh:
        Z["pbh"] = D.pbh.values
    for c in extra:
        Z[c] = D[c].values
    return sm.add_constant(Z, has_constant="add")


def undo(D, x):
    Q = D.assign(x=x)
    m = sm.GLM(Q.AG, calX(Q, ["x"]), family=sm.families.Poisson()).fit()
    fy = (Q.fy == 2025).values
    return float((Q.AG.values[fy] * np.exp(-m.params["x"] * x[fy])).sum()) * G, m.aic


def kernel(D, w):
    w = np.asarray(w, float) / np.sum(w)
    return sum(w[j - 1] * D["w%d" % j].values for j in range(1, len(w) + 1))


def lags(D, n=10, month=True, hosp=False, poisson=False):
    Q = D.copy()
    f = Q.ro.values
    cols = []
    for j in range(1, n + 1):
        Q["l%d" % j] = np.r_[np.zeros(j), f[:-j]]
        cols.append("l%d" % j)
    X = calX(Q, cols + (["AH"] if hosp else []), month=month, fyd=True, trend=False, pbh=False)
    op = f == 0
    m = (sm.GLM(Q.AG[op], X[op], family=sm.families.Poisson()) if poisson else sm.OLS(Q.AG[op], X[op])).fit()
    X0 = X.copy()
    X0[cols] = 0
    return float(m.predict(X0)[(Q.fy == 2025).values].sum()) * G


def screen(L, K, s0, s1):
    for ds in range(s0, s1):
        w = W.simulate(seed=P.SEED, K=K, dseed=ds, weeks=L)
        D = frame(w)
        fy = (D.fy == 2025).values
        fits = {l: undo(D, kernel(D, np.ones(l))) for l in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12)}
        best = min(fits, key=lambda l: fits[l][1])
        gold = fits[best][0]
        X = calX(D, ["w%d" % j for j in range(1, 11)])
        m = sm.GLM(D.AG, X, family=sm.families.Poisson()).fit()
        eta = sum(m.params["w%d" % j] * D["w%d" % j].values for j in range(1, 11))
        dl = float((D.AG.values[fy] * np.exp(-eta[fy])).sum()) * G
        geo = min((undo(D, kernel(D, [r ** (j - 1) for j in range(1, 27)])) for r in np.arange(0.70, 0.965, 0.02)), key=lambda z: z[1])[0]
        F = [lags(D), lags(D, month=False), lags(D, hosp=True), lags(D, poisson=True)]
        default = float(D.AG[fy].sum()) * G
        print("L%d K%.2f ds %2d | best %d gold %.0f distlag %.0f geo %.0f (top margin %.0f) | ten lags max %.0f (%.0f below), 20 lags %.0f, 30 lags %.0f | default %.0f"
              % (L, K, ds, best, gold, dl, geo, HI - geo, max(F), LO - max(F), lags(D, n=20), lags(D, n=30), default), flush=True)


if __name__ == "__main__":
    screen(int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
