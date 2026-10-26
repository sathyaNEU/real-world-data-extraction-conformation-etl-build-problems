"""The main call from the shipped pack, read the way an analyst reads it: the registry's population under the
standard's 2.4, the scorecards' latest computation of each metric under its current key, each change's effect on the
five candidates and on retained_m6, and each candidate's correlation with retention across the changes.

The golden takes each change's sampling error out of the cross-change moments: the variance of each effect (the arms'
variances over their users) and, because both effects are measured on the same users, the covariance between the two
effects' errors (the 2025 holdout's user-level correlation between the candidate and retention, times the arms'
standard deviations, over their users). Every other rung is the same code with one argument changed."""
import os

import numpy as np
import pandas as pd

import common as K

FILES = dict(K.FILES, dictionary="data_dictionary.csv")


def load(target):
    p = lambda k: os.path.join(target, FILES[k])
    d = {}
    d["scorecards"] = pd.read_csv(p("scorecards"), dtype={"experiment_id": str, "arm": str, "metric": str})
    d["registry"] = pd.read_csv(p("registry"), dtype=str, keep_default_na=False)
    d["holdout"] = pd.read_csv(p("holdout"))
    d["cohorts"] = pd.read_csv(p("cohorts"))
    d["calendar"] = pd.read_csv(p("calendar"))
    d["forecast"] = pd.read_csv(p("forecast"))
    return d


def former_keys(target):
    """the catalogue's former key of each metric"""
    out, key = {}, None
    for line in open(os.path.join(target, FILES["catalogue"]), encoding="utf-8"):
        s = line.strip()
        if s.startswith("- key:"):
            key = s.split(":", 1)[1].strip()
        elif s.startswith("former_key:"):
            out[s.split(":", 1)[1].split("#")[0].strip()] = key
    return out


def scorecards(d, target, latest=True, rename=True):
    """latest=True keeps each arm and metric's latest computation (the export notes); "first" its earliest"""
    s = d["scorecards"].copy()
    if rename:
        s["metric"] = s["metric"].replace(former_keys(target))
    if latest:
        s = s.sort_values("computed_at").drop_duplicates(["experiment_id", "arm", "metric"],
                                                         keep="first" if latest == "first" else "last")
    return s


def changes(d, target, srm_out=True, latest=True, rename=True, stopped=True, closed_by=K.PULL, keep_all_versions=False,
            first_arm_only=False):
    """one row per change: users, means and standard deviations of the five candidates and retained_m6 in the
    treatment arm and in its control"""
    reg = d["registry"]
    reg = reg[(reg["six_month_read_closes"] != "") & (reg["six_month_read_closes"] <= closed_by.isoformat())]
    reg = reg[reg["status"].isin(["completed", "stopped_early"] if stopped else ["completed"])]
    if srm_out:
        reg = reg[reg["srm_check"] == "pass"]
    s = scorecards(d, target, latest=latest and not keep_all_versions, rename=rename)
    s = s[s["metric"].isin(K.CAND + [K.RET])]
    if keep_all_versions:
        # every computation read as its own scorecard: two-week metrics by computation, retention its own
        two = s[s["metric"] != K.RET]
        ret = s[s["metric"] == K.RET].sort_values("computed_at").drop_duplicates(["experiment_id", "arm"], keep="last")
        versions = [(eid, c) for eid, c in two[["experiment_id", "computed_at"]].drop_duplicates().itertuples(index=False)]
    rows = []
    for _, r in reg.iterrows():
        eid = r["experiment_id"]
        arms = r["arms"].split(";")
        ctrl = r["control_arm"]
        treats = [a for a in arms if a != ctrl][: 1 if first_arm_only else None]
        if keep_all_versions:
            vs = [c for e, c in versions if e == eid]
            frames = [pd.concat([two[(two["experiment_id"] == eid) & (two["computed_at"] == c)],
                                 ret[ret["experiment_id"] == eid]]) for c in vs]
        else:
            frames = [s[s["experiment_id"] == eid]]
        for g in frames:
            if not len(g):
                continue
            tab = {(a, m): (u, mu, sd) for a, m, u, mu, sd in g[["arm", "metric", "users", "mean", "std_dev"]]
                   .itertuples(index=False)}
            if any((a, m) not in tab for a in [ctrl] + treats for m in K.CAND + [K.RET]):
                continue
            for t in treats:
                row = dict(experiment_id=eid, arm=t, nt=tab[(t, K.RET)][0], nc=tab[(ctrl, K.RET)][0])
                for m in K.CAND + [K.RET]:
                    row["mt_" + m], row["st_" + m] = tab[(t, m)][1], tab[(t, m)][2]
                    row["mc_" + m], row["sc_" + m] = tab[(ctrl, m)][1], tab[(ctrl, m)][2]
                    row["nt_" + m], row["nc_" + m] = tab[(t, m)][0], tab[(ctrl, m)][0]
                rows.append(row)
    return pd.DataFrame(rows)


def holdout_moments(d):
    h = d["holdout"]
    X = h[K.CAND].to_numpy(float)
    y = h[K.RET].to_numpy(float)
    rho = np.array([np.corrcoef(X[:, k], y)[0, 1] for k in range(5)])
    cov = np.array([np.cov(X[:, k], y)[0, 1] for k in range(5)])
    return dict(rho=rho, cov=cov, sd=X.std(0, ddof=1), sdy=y.std(ddof=1), n=len(h))


def effects(c):
    out = {}
    for m in K.CAND + [K.RET]:
        out[m] = (c["mt_" + m] - c["mc_" + m]).to_numpy()
        out["v_" + m] = (c["st_" + m] ** 2 / c["nt_" + m] + c["sc_" + m] ** 2 / c["nc_" + m]).to_numpy()
    return out


def correlations(c, hm, method="golden", ddof=1, cov_from="rho", weights=None):
    """each candidate's correlation with retained_m6 across the changes under one construction:
    raw: the correlation of the effects as measured
    disattenuated: raw over the square root of each effect's reliability (its sampling variance taken out)
    golden: the sampling variances and the sampling covariance taken out of the cross-change moments"""
    e = effects(c)
    y, vy = e[K.RET], e["v_" + K.RET]
    n = len(y)
    w = np.ones(n) / n if weights is None else weights / weights.sum()
    f = 1 / (1 - (w ** 2).sum()) if ddof == 1 else 1.0
    out = []
    for k, m in enumerate(K.CAND):
        x, vx = e[m], e["v_" + m]
        mx, my = (w * x).sum(), (w * y).sum()
        cxy = f * (w * (x - mx) * (y - my)).sum()
        vxx = f * (w * (x - mx) ** 2).sum()
        vyy = f * (w * (y - my) ** 2).sum()
        if method == "raw":
            out.append(cxy / np.sqrt(vxx * vyy))
            continue
        if cov_from == "rho":
            s12 = hm["rho"][k] * (c["st_" + m] * c["st_" + K.RET] / c["nt_" + K.RET] +
                                 c["sc_" + m] * c["sc_" + K.RET] / c["nc_" + K.RET]).to_numpy()
        elif cov_from == "holdout":
            s12 = hm["cov"][k] * (1 / c["nt_" + K.RET] + 1 / c["nc_" + K.RET]).to_numpy()
            vx = hm["sd"][k] ** 2 * (1 / c["nt_" + m] + 1 / c["nc_" + m]).to_numpy()
            vy = hm["sdy"] ** 2 * (1 / c["nt_" + K.RET] + 1 / c["nc_" + K.RET]).to_numpy()
        elif cov_from == "pooled":
            nt, nc = c["nt_" + m].to_numpy(), c["nc_" + m].to_numpy()
            sp = np.sqrt(((nt - 1) * c["st_" + m] ** 2 + (nc - 1) * c["sc_" + m] ** 2) / (nt + nc - 2)).to_numpy()
            sq = np.sqrt(((nt - 1) * c["st_" + K.RET] ** 2 + (nc - 1) * c["sc_" + K.RET] ** 2) / (nt + nc - 2)).to_numpy()
            s12 = hm["rho"][k] * sp * sq * (1 / nt + 1 / nc)
            vx = sp ** 2 * (1 / nt + 1 / nc)
            vy = sq ** 2 * (1 / nt + 1 / nc)
        else:
            raise ValueError(cov_from)
        a = vxx - (w * vx).sum()
        b = vyy - (w * vy).sum()
        if method == "disattenuated":
            out.append(cxy / np.sqrt(a * b))
        elif method == "golden":
            out.append((cxy - (w * s12).sum()) / np.sqrt(a * b))
        elif method == "half":
            out.append((cxy - 0.5 * (w * s12).sum()) / np.sqrt(a * b))
        else:
            raise ValueError(method)
    return np.array(out)


def bivariate_reml(c, hm, ml=False):
    """the precision-weighted bivariate random-effects fit with each change's sampling covariance: not the standard's
    estimand (each change counts once), kept to show it names the same proxy"""
    from scipy.optimize import minimize
    e = effects(c)
    y, vy = e[K.RET], e["v_" + K.RET]
    out = []
    for k, m in enumerate(K.CAND):
        x, vx = e[m], e["v_" + m]
        s12 = hm["rho"][k] * (c["st_" + m] * c["st_" + K.RET] / c["nt_" + K.RET] +
                             c["sc_" + m] * c["sc_" + K.RET] / c["nc_" + K.RET]).to_numpy()
        D = np.column_stack([x, y])

        def nll(p):
            T = np.array([[np.exp(p[0]), 0], [p[1], np.exp(p[2])]])
            T = T @ T.T
            V = np.empty((len(x), 2, 2))
            V[:, 0, 0], V[:, 1, 1] = T[0, 0] + vx, T[1, 1] + vy
            V[:, 0, 1] = V[:, 1, 0] = T[0, 1] + s12
            Vi = np.linalg.inv(V)
            A = Vi.sum(0)
            mu = np.linalg.solve(A, np.einsum("eij,ej->i", Vi, D))
            R = D - mu
            v = 0.5 * (np.linalg.slogdet(V)[1].sum() + np.einsum("ei,eij,ej->", R, Vi, R))
            return v + (0 if ml else 0.5 * np.linalg.slogdet(A)[1])
        sx = np.sqrt(max(x.var() - vx.mean(), 1e-8))
        sy = np.sqrt(max(y.var() - vy.mean(), 1e-10))
        r = minimize(nll, [np.log(sx), 0.0, np.log(sy)], method="Nelder-Mead",
                     options=dict(xatol=1e-10, fatol=1e-12, maxiter=20000))
        T = np.array([[np.exp(r.x[0]), 0], [r.x[1], np.exp(r.x[2])]])
        T = T @ T.T
        out.append(T[0, 1] / np.sqrt(T[0, 0] * T[1, 1]))
    return np.array(out)


def spearman(c):
    e = effects(c)
    y = pd.Series(e[K.RET]).rank().to_numpy()
    return np.array([np.corrcoef(pd.Series(e[m]).rank().to_numpy(), y)[0, 1] for m in K.CAND])


def user_level(d):
    return holdout_moments(d)["rho"]


def pick(v):
    return K.CAND[int(np.argmax(v))]


def main_call(target):
    d = load(target)
    c = changes(d, target)
    hm = holdout_moments(d)
    gold = correlations(c, hm)
    order = list(np.argsort(-gold))
    res = dict(
        n_changes=len(c), n_experiments=int(c["experiment_id"].nunique()),
        golden=gold, proxy=K.CAND[order[0]], runner_up=K.CAND[order[1]],
        raw=correlations(c, hm, "raw"), disattenuated=correlations(c, hm, "disattenuated"),
        half=correlations(c, hm, "half"), spearman=spearman(c), user=hm["rho"],
        family=dict(mom=gold, mom_n=correlations(c, hm, ddof=0), holdout=correlations(c, hm, cov_from="holdout"),
                    pooled=correlations(c, hm, cov_from="pooled")),
        hm=hm, changes=c, data=d)
    return res
