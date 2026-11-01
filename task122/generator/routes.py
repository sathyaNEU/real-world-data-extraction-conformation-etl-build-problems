"""The ladder and the standing family, each route computed from target/ on the cleaned records (the golden's Layer 1
handling), plus the Layer 1 readings the fork table prices.

    python3 task122/generator/routes.py [target]
"""
import os
import sys
import warnings

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import figs as F      # noqa: E402
import params as P    # noqa: E402

warnings.filterwarnings("ignore")


def mh(df, keys):
    g = F.strata_table(df, keys)
    tt = g.ex_on + g.ex_off
    ok = tt > 0
    return float((g.al_on * g.ex_off / tt)[ok].sum() / (g.al_off * g.ex_on / tt)[ok].sum())


def poisson(df, formula, min_n=0):
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    G = df.groupby(["sector", "n", "T", "on"]).agg(al=("al", "sum"), ex=("m", "size")).reset_index()
    G = G[(G.ex > 0) & (G.n >= min_n)].copy()
    G["onf"] = G.on.astype(int)
    G["lp"] = np.log(np.maximum(G.n * (G.n - 1) / 2.0, 0.5))
    f = smf.glm(formula, data=G, family=sm.families.Poisson(), offset=np.log(G.ex)).fit()
    return float(np.exp(f.params["onf"]))


def ladder(df):
    """Each route's ratio of the activation rate with the probe running to the rate without; share = 1 - ratio."""
    on, off = df[df.on], df[~df.on]
    r = {}
    r["R0 per flight hour"] = (on.al.sum() / on.n.sum()) / (off.al.sum() / off.n.sum())
    d = df.copy()
    d["hour"] = (d.m // 60)
    d["hod"] = ((d.m + 13 * 60) // 60) % 24
    d["hn"] = np.round(d.groupby(["sector", "hour"]).n.transform("mean")).astype(int)
    r["R1 hourly traffic"] = mh(d, ["sector", "hod", "hn"])
    r["R1b same sector-hour"] = mh(d, ["sector", "hour"])
    r["R2 like occupancy"] = mh(d, ["sector", "n"])
    r["R2 like occupancy and hour of day"] = mh(d, ["sector", "n", "hod"])
    pairs_on = (on.n * (on.n - 1) / 2.0).sum()
    pairs_off = (off.n * (off.n - 1) / 2.0).sum()
    r["R2b per aircraft pair"] = (on.al.sum() / pairs_on) / (off.al.sum() / pairs_off)
    r["R2c per climbing or descending aircraft"] = (on.al.sum() / on["T"].sum()) / (off.al.sum() / off["T"].sum())
    O, E, _ = F.observed_expected(df)
    r["R3 observed against expected (sector, n, T)"] = O / E
    r["R3 Mantel-Haenszel (sector, n, T)"] = mh(d, ["sector", "n", "T"])
    r["R3 strata with hour of day"] = mh(d, ["sector", "n", "T", "hod"])
    r["R3 Poisson, sector, count and climbing count as factors"] = poisson(df, "al ~ onf + C(sector) + C(n) + C(T)")
    r["R3 Poisson, count factors, climbing count linear"] = poisson(df, "al ~ onf + C(sector) + C(n) + T")
    r["R3 Poisson, log aircraft pairs and climbing count"] = poisson(df, "al ~ onf + C(sector) + lp + T", min_n=2)
    return r


def standing(r):
    return {k: v for k, v in r.items() if k.startswith("R3")}


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else F.TARGET
    D = F.load(t)
    df = F.frame(F.panel(D))
    for k, v in ladder(df).items():
        print("%-58s %.3f  prevented %5.1f%%" % (k, v, 100 * (1 - v)))
