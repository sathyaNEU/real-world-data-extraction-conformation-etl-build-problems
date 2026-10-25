"""The family for the graded 2028 export of the winner and the runner-up: the bases a competent solver takes for the
fleet's measured performance and the first-year age, every member on the one call."""
import datetime as dt
import sys

import numpy as np
import pandas as pd

import solve as SV


def members(K):
    out = {}
    pr_kp = SV.site_pr(K, "Knowle Park")
    d_fit = SV.bifacial_degradation(K)
    age_kp = SV.mean_age(K, "Knowle Park")
    # daily-level degradation: each bifacial farm's daily ratio, log-linear in age, a level for each farm and month
    rows = []
    for s in ["Ivy Cross", "Furzedown", "Jessop's Farm", "Knowle Park"]:
        x = K.ex[K.ex.site == s].merge(K.w[K.w.site == s], on=["date", "site"])
        x["lpr"] = np.log(x.export_mwh / (K.dc[s] * x.poa_irradiation_kwh_m2))
        x["age"] = (x.date - K.comm[s]).dt.days / 365.25
        x["s"] = s
        x["m"] = x.date.dt.month
        rows.append(x[np.isfinite(x.lpr)])
    df = pd.concat(rows, ignore_index=True)
    X = pd.get_dummies(df[["s"]].astype(str)).astype(float).join(pd.get_dummies(df.m.astype(str), prefix="m", drop_first=True).astype(float))
    X["age"] = df.age
    b = np.linalg.lstsq(X.values, df.lpr.values, rcond=None)[0]
    d_daily = float(1 - np.exp(b[-1]))
    # outage days out
    ev = K.om[K.om.site == "Knowle Park"]
    x = K.ex[K.ex.site == "Knowle Park"].merge(K.w[K.w.site == "Knowle Park"], on=["date", "site"])
    x = x[~x.date.isin(ev.date)]
    pr_kp_noout = x.export_mwh.sum() / (12.0 * x.poa_irradiation_kwh_m2.sum())
    # the bifacial farms' mean ratio, each carried to Knowle Park's age at the fitted rate
    prs = []
    for s in ["Ivy Cross", "Furzedown", "Jessop's Farm", "Knowle Park"]:
        prs.append(SV.site_pr(K, s) * (1 - d_fit) ** (age_kp - SV.mean_age(K, s)))
    pr_bif = float(np.mean(prs))
    for name, pr, d in [("KP, annual fit", pr_kp, d_fit), ("KP, daily fit", pr_kp, d_daily), ("KP, datasheet 0.45", pr_kp, 0.0045),
                        ("KP outage days out, annual fit", pr_kp_noout, d_fit), ("bifacial mean, annual fit", pr_bif, d_fit),
                        ("bifacial mean, daily fit", pr_bif, d_daily), ("KP, 2025 only, annual fit", SV.site_pr(K, "Knowle Park", (2025, 2025)), None)]:
        if d is None:
            age25 = SV.mean_age(K, "Knowle Park", dt.date(2025, 1, 1), dt.date(2025, 12, 31))
            f = lambda c: 11.0 * SV.avg_year_poa(K, c) * pr * (1 - d_fit) ** (SV.age_2028(c) - age25)
        else:
            f = lambda c, pr=pr, d=d: 11.0 * SV.avg_year_poa(K, c) * pr * (1 - d) ** (SV.age_2028(c) - age_kp)
        out[name] = {c: f(c) for c in ["Kingsley Fields", "Larkhill Common"]}
    return out, d_fit, d_daily


if __name__ == "__main__":
    K = SV.Pack(sys.argv[1])
    m, d1, d2 = members(K)
    print("degradation: annual fit %.4f, daily fit %.4f" % (d1, d2))
    for k, v in m.items():
        print("%-34s Kingsley %7.0f  Larkhill %7.0f  lead %.2f%%" % (k, v["Kingsley Fields"], v["Larkhill Common"], 100 * (v["Kingsley Fields"] / v["Larkhill Common"] - 1)))
