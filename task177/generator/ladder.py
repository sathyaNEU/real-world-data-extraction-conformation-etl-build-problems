"""task177 ladder: every route to the call, run on the shipped pack. The routes without the bill-timing step (the
default path and its reflexes), the routes with it (the golden's family, an outsider's choices), and the routes that
build the days to the bill wrongly. checks.py asserts each one's printed share; the design note quotes them."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression

import calc as K
import common as C


def X(df, asof, with_d=False):
    start = pd.to_datetime(df.started_on)
    out = pd.DataFrame({"ten": (pd.Timestamp(asof) - start).dt.days.values / 30.44,
                        "arts": np.log1p(df.articles_read_28d.astype(int).values),
                        "news": df.newsletters.astype(int).values, "supp": df.support_contacts_90d.astype(int).values})
    out["lten"] = np.log(np.maximum(out.ten, 0.5))
    for col, vals in (("plan", C.PLANS), ("most_used_on", ("web", "ios", "android", "mixed")),
                      ("payment_method", ("card", "direct debit", "paypal"))):
        for v in vals:
            out["%s_%s" % (col, v)] = (df[col].values == v).astype(float)
    if with_d:
        out["d"] = df.d.values.astype(float)
    return out


LR = lambda: LogisticRegression(max_iter=4000)
HGB = lambda: HistGradientBoostingClassifier(max_iter=250, learning_rate=0.05, random_state=7)
HGBR = lambda: HistGradientBoostingRegressor(max_iter=250, learning_rate=0.05, random_state=7)


def _t_learner(ly, ty, mk, with_d):
    t = ly["T"].values == 1
    A, B = X(ly, C.LY_LIST, with_d), X(ty, C.TY_LIST, with_d)
    m1, m0 = mk().fit(A[t], ly.Y[t]), mk().fit(A[~t], ly.Y[~t])
    return 100 * (m1.predict_proba(B)[:, 1] - m0.predict_proba(B)[:, 1]).mean()


def _s_learner(ly, ty, with_d):
    A = X(ly, C.LY_LIST, with_d)
    A["T"] = ly["T"].values
    m = HGB().fit(A, ly.Y)
    B = X(ty, C.TY_LIST, with_d)
    b1, b0 = B.copy(), B.copy()
    b1["T"], b0["T"] = 1, 0
    return 100 * (m.predict_proba(b1)[:, 1] - m.predict_proba(b0)[:, 1]).mean()


def _transformed(ly, ty, with_d):
    p = ly["T"].mean()
    z = ly.Y.values * (ly["T"].values / p - (1 - ly["T"].values) / (1 - p))
    g = HGBR().fit(X(ly, C.LY_LIST, with_d), z)
    return 100 * g.predict(X(ty, C.TY_LIST, with_d)).mean()


def _x_learner(ly, ty):
    t = ly["T"].values == 1
    A, B = X(ly, C.LY_LIST, True), X(ty, C.TY_LIST, True)
    m1, m0 = HGB().fit(A[t], ly.Y[t]), HGB().fit(A[~t], ly.Y[~t])
    d1 = ly.Y.values[t] - m0.predict_proba(A[t])[:, 1]
    d0 = m1.predict_proba(A[~t])[:, 1] - ly.Y.values[~t]
    g1, g0 = HGBR().fit(A[t], d1), HGBR().fit(A[~t], d0)
    e = t.mean()
    return 100 * ((1 - e) * g1.predict(B) + e * g0.predict(B)).mean()


def _glm(ly, ty, knots):
    D = X(ly, C.LY_LIST).copy()
    D["T"] = ly["T"].values
    D["dd"] = ly.d.values.astype(float)
    for k in knots:
        D["h%d" % k] = np.maximum(ly.d.values - k, 0).astype(float)
    terms = ["dd"] + ["h%d" % k for k in knots]
    for c in terms:
        D["T_" + c] = D["T"] * D[c]
    D = sm.add_constant(D, has_constant="add")
    m = sm.GLM(ly.Y.values, D, family=sm.families.Binomial()).fit()
    E = X(ty, C.TY_LIST).copy()
    E["dd"] = ty.d.values.astype(float)
    for k in knots:
        E["h%d" % k] = np.maximum(ty.d.values - k, 0).astype(float)
    E1, E0 = E.copy(), E.copy()
    E1["T"], E0["T"] = 1, 0
    for c in terms:
        E1["T_" + c], E0["T_" + c] = E1[c], 0.0
    E1 = sm.add_constant(E1, has_constant="add")[D.columns]
    E0 = sm.add_constant(E0, has_constant="add")[D.columns]
    return 100 * (m.predict(E1) - m.predict(E0)).mean()


def _local_linear(ly, d0, h):
    w = np.maximum(1 - np.abs(ly.d.values - d0) / h, 0)
    k = w > 0
    T = ly["T"].values[k].astype(float)
    x = ly.d.values[k].astype(float) - d0
    A = np.column_stack([np.ones(k.sum()), T, x, T * x])
    s = np.sqrt(w[k])
    beta, *_ = np.linalg.lstsq(A * s[:, None], ly.Y.values[k] * s, rcond=None)
    return 100 * beta[1]


def routes(P, c=None, ly=None, ty=None):
    if ly is None:
        c, ly, ty = K.call(P)
    t = ly["T"] == 1
    out = {}
    # ---- without the step
    out["pooled difference of the arms"] = K.diff(ly)
    out["two-model logistic on the features"] = _t_learner(ly, ty, LR, False)
    out["two-model gradient boosting on the features"] = _t_learner(ly, ty, HGB, False)
    out["one-model gradient boosting with treatment"] = _s_learner(ly, ty, False)
    out["transformed outcome, gradient boosting"] = _transformed(ly, ty, False)
    for col in ("plan", "region", "most_used_on", "risk_band"):
        tot = 0.0
        for v, g in ly.groupby(col):
            tot += K.diff(g) * (ty[col] == v).sum()
        out["strata by %s" % col.replace("_", " ")] = tot / len(ty)
    acc_subs = set(P.lbs[P.lbs.applied_ref.isin(set(P.offers.acceptance_ref))].subscription_ref)
    acc = ly.subscription_ref.isin(acc_subs)
    opened = ly.customer_no.isin(set(P.email[P.email.event == "opened"].customer_no))
    itt = K.diff(ly)
    out["difference over the open rate"] = itt / opened[t].mean()
    out["difference over the acceptance rate"] = itt / acc[t].mean()
    out["accepters against the holdout"] = 100 * (ly.Y[acc].mean() - ly.Y[~t].mean())
    out["openers against the holdout"] = 100 * (ly.Y[opened].mean() - ly.Y[~t].mean())
    # ---- with the step (the golden's family)
    for lo, hi in ((1, 14), (1, 7), (1, 10), (3, 9), (4, 8), (5, 7), (6, 6), (2, 12)):
        out["days %d to %d before the bill" % (lo, hi)] = K.diff(ly, (ly.d >= lo) & (ly.d <= hi))
    for h in (3, 5, 8):
        out["local linear at day 6, bandwidth %d" % h] = _local_linear(ly, 6, h)
    out["two-model gradient boosting with the days"] = _t_learner(ly, ty, HGB, True)
    out["two-model logistic with the days"] = _t_learner(ly, ty, LR, True)
    out["one-model gradient boosting with the days"] = _s_learner(ly, ty, True)
    out["transformed outcome with the days"] = _transformed(ly, ty, True)
    out["X-learner with the days"] = _x_learner(ly, ty)
    out["logistic, treatment by days (linear)"] = _glm(ly, ty, [])
    out["logistic, treatment by days (knots 10, 14, 18)"] = _glm(ly, ty, [10, 14, 18])
    # ---- the days built wrongly, or a window past the fortnight
    obs = P.lbs[(P.lbs.line_type == "SUB") & (P.lbs.date > "2026-01-31")].groupby("subscription_ref").date.min()
    dobs = (ly.subscription_ref.map(obs) - pd.Timestamp(C.LY_LIST)).dt.days
    m = dobs.notna() & (dobs >= 1) & (dobs <= 14)
    out["days to the next bill seen (leavers have none)"] = K.diff(ly, m)
    sd = pd.to_datetime(ly.started_on).dt.day
    dan = np.array([(C.month_day(2026, 2, int(k)) - C.LY_LIST).days for k in sd])
    out["days from the start date's day"] = K.diff(ly, (dan >= 1) & (dan <= 14))
    for lo, hi in ((1, 16), (1, 21)):
        out["days %d to %d before the bill" % (lo, hi)] = K.diff(ly, (ly.d >= lo) & (ly.d <= hi))
    return out


STEP = ("days 1 to 14", "days 1 to 7", "days 1 to 10", "days 3 to 9", "days 4 to 8", "days 5 to 7", "days 6 to 6",
        "days 2 to 12", "local linear", "with the days", "treatment by days")
WRONG_DAYS = ("next bill seen", "start date", "days 1 to 16", "days 1 to 21")


def group(name):
    if any(w in name for w in WRONG_DAYS):
        return "days built wrongly"
    if any(s in name for s in STEP):
        return "with the step"
    return "without the step"
