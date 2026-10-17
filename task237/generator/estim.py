"""task237 estimators, read only from the pack: each version's valid pilot completes under TAS-4 s.4, the item scores
under s.5, each version's reliability under s.6 the golden way (the trait's share of the total score's variance from a
model giving the negatively worded items a wording factor of their own) and the other ways of estimating it, the
routes a solver reaches for instead, the release decisions, and the two asks (valid completes, pilot mean score)."""
import os
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd
from scipy.optimize import minimize

CODES = ["BCS%02d" % i for i in range(1, 13)]
POS = [0, 2, 4, 6, 8, 10]
NEG = [1, 3, 5, 7, 9, 11]
RELEASE, HOLD = 0.80, 0.70
ORDER = ["pa", "zh-Hans", "yue", "tl", "ar", "es", "ur", "vi", "fa", "ko"]
MISSING = {9, -8, -9}


def load(target, files):
    rd = lambda k: pd.read_csv(os.path.join(target, files[k]), dtype=str, keep_default_na=False)
    D = dict(online=rd("online"), ledger=rd("ledger"), capi=rd("capi"), bc=rd("bc"), para=rd("para"))
    D["reg"] = pd.read_excel(os.path.join(target, files["reg"]), sheet_name="Register", dtype=str)
    return D


def round_half(x, places=1):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_UP))


# ------------------------------------------------------------------ TAS-4 s.4: valid completes
def eastern_date(utc):
    t = pd.to_datetime(utc.str.replace("Z", "", regex=False))
    return (t - pd.Timedelta(hours=5)).dt.strftime("%Y-%m-%d")


def surviving_member(ledger):
    """each panel account mapped to the account it was finally merged into (itself when never merged)"""
    m = ledger[ledger.outcome == "merged"].set_index("panel_member_id").merged_into.to_dict()

    def root(a):
        seen = set()
        while a in m and a not in seen:
            seen.add(a)
            a = m[a]
        return a
    return root


def online_completes(D, status_only=False, utc_dates=False, no_window=False, merges_ignored=False, retakes=False,
                     switchers=False, inside=False):
    o = D["online"].copy()
    lang = {v.upper(): v for v in ORDER}
    o["version"] = o.survey_code.str.replace("CCS6-BCS-", "", regex=False).map(lang)
    keep = o.status == "complete" if status_only else o.status.isin(["complete", "partial"])
    if not inside:                                           # the module reached its end (no item left blank)
        keep &= (o[CODES] != "").all(axis=1)
    o = o[keep & (o.age.astype(int) >= 18)]
    if not no_window:
        reg = D["reg"].set_index("version")
        d = o.start_utc.str[:10] if utc_dates else eastern_date(o.start_utc)
        o = o[(d >= o.version.map(reg.pilot_start)) & (d <= o.version.map(reg.pilot_end))]
    if not switchers:
        o = o[o.ui_language_at_end == o.version]
    if not retakes:
        led = D["ledger"][D["ledger"].respondent_id != ""].set_index("respondent_id").panel_member_id
        root = (lambda a: a) if merges_ignored else surviving_member(D["ledger"])
        o = o.assign(member=o.respondent_id.map(led).map(root), t=o.end_utc.where(o.end_utc != "", o.start_utc))
        o = o.sort_values(["version", "member", "t"]).drop_duplicates(["version", "member"], keep="first")
    out = o[["respondent_id", "version"] + CODES].rename(columns={"respondent_id": "id"})
    for c in CODES:
        out[c] = pd.to_numeric(out[c].replace("", np.nan))
    return out


def capi_interviews(D):
    c = D["capi"]
    return c.pivot_table(index=["case_id", "version", "interviewer_id", "interview_date"], columns="variable",
                         values="value", aggfunc="first").reset_index()


def capi_completes(D, result_only=False, case_join=False, pretest=False, unconfirmed=False, not_reached=True,
                   inside=False):
    w = capi_interviews(D)
    if result_only:
        w = w[w.RESULT == "1"]
    if not inside:                                           # the module reached its end (every item has a row)
        w = w[w[CODES].notna().all(axis=1)]
    if not pretest:
        reg = D["reg"].set_index("version")
        w = w[(w.interview_date >= w.version.map(reg.pilot_start)) & (w.interview_date <= w.version.map(reg.pilot_end))]
    bc = D["bc"]
    if case_join:
        out = w.case_id.map(bc.drop_duplicates("case_id").set_index("case_id").outcome).fillna("")
    else:
        key = bc.case_id + "|" + bc.interviewer_id
        out = (w.case_id + "|" + w.interviewer_id).map(pd.Series(bc.outcome.values, index=key)).fillna("")
    if not unconfirmed:
        w = w[out.reindex(w.index) != "not confirmed"]
    if not not_reached:
        w = w[out.reindex(w.index) != "not reached"]
    w = w[w.AGE.astype(int) >= 18]
    res = w[["case_id", "version"] + CODES].rename(columns={"case_id": "id"})
    for col in CODES:
        res[col] = pd.to_numeric(res[col])
    return res


ONLINE = ("status_only", "utc_dates", "no_window", "merges_ignored", "retakes", "switchers", "inside")
CAPI = ("result_only", "case_join", "pretest", "unconfirmed", "not_reached", "inside")


def completes(D, **kw):
    on = {k: v for k, v in kw.items() if k in ONLINE}
    ca = {k: v for k, v in kw.items() if k in CAPI}
    return pd.concat([online_completes(D, **on), capi_completes(D, **ca)], ignore_index=True)


# ------------------------------------------------------------------ TAS-4 s.5: item scores
def item_scores(df, missing_as_values=False):
    X = df[CODES].to_numpy(dtype=float)
    if not missing_as_values:
        X[np.isin(X, list(MISSING))] = np.nan
    X[:, NEG] = 6 - X[:, NEG]
    return X


def total_scores(X, prorate=True):
    answered = (~np.isnan(X)).sum(axis=1)
    s = np.nanmean(X, axis=1) * 12
    if prorate:
        s[answered < 10] = np.nan
    else:
        s[answered < 12] = np.nan
    return s


# ------------------------------------------------------------------ s.6: reliability, the model the data supports
def fit(S, mask, resid_pairs=()):
    """maximum likelihood factor model on a covariance matrix: unit-variance orthogonal factors with the free loadings in
    mask, unique variances, and free residual covariances for the listed item pairs"""
    p, k = mask.shape
    idx = np.argwhere(mask)
    nl, npair = len(idx), len(resid_pairs)

    def unpack(x):
        L = np.zeros((p, k)); L[idx[:, 0], idx[:, 1]] = x[:nl]
        Th = np.diag(np.exp(x[nl:nl + p]))
        for (i, j), v in zip(resid_pairs, x[nl + p:]):
            Th[i, j] = Th[j, i] = v
        return L, Th

    def f(x):
        L, Th = unpack(x)
        Sig = L @ L.T + Th
        sign, logdet = np.linalg.slogdet(Sig)
        if sign <= 0:
            return 1e10
        return logdet + np.trace(np.linalg.solve(Sig, S))

    d = np.sqrt(np.diag(S))
    x0 = np.concatenate([0.5 * d[idx[:, 0]], np.log(0.5 * np.diag(S)), np.zeros(npair)])
    r = minimize(f, x0, method="L-BFGS-B", options={"maxiter": 20000, "maxfun": 200000})
    L, Th = unpack(r.x)
    for j in range(k):
        if L[:, j].sum() < 0:
            L[:, j] *= -1
    return L, Th, r.fun


def trait_share(S):
    """the general factor's share of the total score's variance in a model with a wording factor on the negatively
    worded items (orthogonal to the general factor)"""
    m = np.zeros((12, 2), bool); m[:, 0] = True; m[NEG, 1] = True
    L, Th, _ = fit(S, m)
    g, w = L[:, 0].sum(), L[:, 1].sum()
    var = g ** 2 + w ** 2 + Th.sum()
    return dict(share=g ** 2 / var, common=(g ** 2 + w ** 2) / var, g=g, w=w, L=L, Th=Th)


def trait_share_cu(S):
    """the same share from a single factor with the negatively worded items' residuals free to covary"""
    pairs = [(NEG[a], NEG[b]) for a in range(6) for b in range(a + 1, 6)]
    L, Th, _ = fit(S, np.ones((12, 1), bool), pairs)
    g = L[:, 0].sum()
    return g ** 2 / (g ** 2 + Th.sum())


def trait_share_moments(S):
    """the trait's loadings on the positively worded items from their own single factor, the negatively worded items'
    from their covariance with the positively worded ones, over the observed variance of the total"""
    Lp, Thp, _ = fit(S[np.ix_(POS, POS)], np.ones((6, 1), bool))
    lp = Lp[:, 0].sum()
    ln = S[np.ix_(POS, NEG)].sum() / lp
    return (lp + ln) ** 2 / S.sum()


def alpha(S):
    p = S.shape[0]
    return p / (p - 1) * (1 - np.trace(S) / S.sum())


def one_factor(S):
    L, Th, _ = fit(S, np.ones((S.shape[0], 1), bool))
    g = L[:, 0].sum()
    return g ** 2 / (g ** 2 + Th.sum())


def band(v):
    return "release" if v >= RELEASE else "hold" if v >= HOLD else "rework"


def full_answer_cov(Xv):
    Xc = Xv[~np.isnan(Xv).any(axis=1)]
    return np.cov(Xc, rowvar=False), len(Xc)


def reliability(df):
    """every estimate for every version on its valid completes who answered all twelve items"""
    out = {}
    for v in ORDER:
        X = item_scores(df[df.version == v])
        S, n = full_answer_cov(X)
        ts = trait_share(S)
        out[v] = dict(n=n, golden=ts["share"], common=ts["common"], cu=trait_share_cu(S), moments=trait_share_moments(S),
                      alpha=alpha(S), one_factor=one_factor(S), positive_only=one_factor(S[np.ix_(POS, POS)]),
                      wording_sum=ts["w"], trait_sum=ts["g"])
    return out


def model_fit(S, n, mask):
    """the model's chi-square against the saturated model and its RMSEA (maximum likelihood)"""
    p = S.shape[0]
    _, _, f = fit(S, mask)
    chi = (n - 1) * (f - np.linalg.slogdet(S)[1] - p)
    df = p * (p + 1) // 2 - int(mask.sum()) - p
    return chi, df, float(np.sqrt(max(chi - df, 0) / (df * (n - 1))))


def wording_test(df):
    """for each version: a single factor against a single factor plus a wording factor on the negatively worded items"""
    from scipy.stats import chi2
    out = {}
    for v in ORDER:
        S, n = full_answer_cov(item_scores(df[df.version == v]))
        one = np.ones((12, 1), bool)
        two = np.zeros((12, 2), bool); two[:, 0] = True; two[NEG, 1] = True
        c1, d1, r1 = model_fit(S, n, one)
        c2, d2, r2 = model_fit(S, n, two)
        out[v] = dict(rmsea_one=r1, rmsea_two=r2, diff=c1 - c2, p=float(chi2.sf(c1 - c2, d1 - d2)))
    return out


def ordinal_share(df):
    """the same share on polychoric correlations of the answers (a reliability of the latent responses)"""
    import poly
    out = {}
    for v in ORDER:
        X = item_scores(df[df.version == v])
        Xc = X[~np.isnan(X).any(axis=1)].astype(int)
        out[v] = trait_share(poly.poly_matrix(Xc))["share"]
    return out


# ------------------------------------------------------------------ the asks
def valid_counts(df):
    return {v: int((df.version == v).sum()) for v in ORDER}


def mean_scores(df, prorate=True, missing_as_values=False, raw=False):
    out = {}
    for v in ORDER:
        s = total_scores(item_scores(df[df.version == v], missing_as_values), prorate)
        m = float(np.nanmean(s))
        out[v] = m if raw else round_half(m, 2)
    return out


STOPS = {
    "partials past the module dropped (vendor status)": dict(status_only=True, result_only=True),
    "back-check joined by case": dict(case_join=True),
    "merged accounts kept apart": dict(merges_ignored=True),
    "online dates read in UTC": dict(utc_dates=True),
    "no window for the online pilots": dict(no_window=True),
    "retakes counted": dict(retakes=True),
    "switchers counted": dict(switchers=True),
    "partials inside the module counted": dict(inside=True),
    "pretest interviews counted": dict(pretest=True),
    "unconfirmed interviews counted": dict(unconfirmed=True),
    "unreached back-checks dropped": dict(not_reached=False),
}


def ask_stops(D):
    base = completes(D)
    gA, gB = valid_counts(base), mean_scores(base)
    runs = {k: completes(D, **kw) for k, kw in STOPS.items()}
    A = {k: valid_counts(v) for k, v in runs.items()}
    B = {k: mean_scores(v) for k, v in runs.items()}
    B["no prorating"] = mean_scores(base, prorate=False)
    B["missing codes read as answers"] = mean_scores(base, missing_as_values=True)
    B["one decimal"] = {v: round_half(x, 1) for v, x in mean_scores(base, raw=True).items()}
    return gA, gB, A, B


# ------------------------------------------------------------------ everything the goldens and the write-up owe
def solve(target, files):
    D = load(target, files)
    df = completes(D)
    rel = reliability(df)
    calls = {v: band(rel[v]["golden"]) for v in ORDER}
    reg = D["reg"].set_index("version")
    return dict(D=D, df=df, rel=rel, calls=calls, counts=valid_counts(df), means=mean_scores(df),
                means_raw=mean_scores(df, raw=True), language=reg.language.to_dict(), mode=reg["mode"].to_dict(),
                vendor=reg.vendor.to_dict(), wording=wording_test(df), entries=len(D["online"]),
                interviews=len(capi_interviews(D)))
