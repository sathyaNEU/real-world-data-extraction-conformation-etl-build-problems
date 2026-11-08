"""The rungs and the golden on a table of interviews (one row per completed household interview), each estimating
every interviewer's roster effect in persons per 100 households against the interviewers as a body.

Columns used: iv, unit (the household: dwelling and household number), psu, q (quarter label), size (persons
rostered as resident), dtype, beds, urban, county, reissue (the interview completed a reissued case)."""
import numpy as np
import pandas as pd

TOL = 12.0   # persons per 100 households, FQ-3 section 3


def body(effect, n):
    """Effects against the interviewers as a body: the interview-weighted mean effect is zero; per 100 households."""
    keys = sorted(effect)
    w = np.array([n[k] for k in keys], dtype=float)
    v = np.array([effect[k] for k in keys])
    m = float((w * v).sum() / w.sum())
    return {k: 100.0 * (effect[k] - m) for k in keys}


def counts(df):
    return df.groupby("iv").size().to_dict()


def fit(df, absorb=None, covariates=None):
    """Least squares of size on interviewer dummies, quarter dummies and any covariates, with one factor absorbed
    exactly by demeaning within its levels (None: an intercept only). Returns the interviewer coefficients."""
    ivs = sorted(df["iv"].unique())
    X = [pd.get_dummies(df["iv"]).reindex(columns=ivs).astype(float)]
    X.append(pd.get_dummies(df["q"], drop_first=True).astype(float))
    if covariates is not None:
        X.append(covariates.astype(float))
    X = pd.concat(X, axis=1).values
    y = df["size"].values.astype(float)
    if absorb is not None:
        g = df[absorb].values
        codes, inv = np.unique(g, return_inverse=True)
        cnt = np.bincount(inv).astype(float)
        ym = np.bincount(inv, weights=y) / cnt
        y = y - ym[inv]
        Xm = np.zeros((len(codes), X.shape[1]))
        for j in range(X.shape[1]):
            Xm[:, j] = np.bincount(inv, weights=X[:, j]) / cnt
        X = X - Xm[inv]
        keep = cnt[inv] > 1          # a level seen once carries no within information
        X, y = X[keep], y[keep]
    else:
        pass
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    return {k: float(beta[i]) for i, k in enumerate(ivs)}


def frame_covariates(df):
    cov = pd.get_dummies(df[["dtype"]].astype(str), drop_first=True).astype(float)
    cov["beds"] = df["beds"].astype(float)
    cov["urban"] = df["urban"].astype(float)
    return cov


def r0_means(df):
    """The interviewer's mean household size against the body (no adjustment)."""
    m = df.groupby("iv")["size"].mean().to_dict()
    return body(m, counts(df))


def r1_frame(df):
    """Interviewer effects adjusted for the frame's dwelling covariates and the quarter (the survey methods
    standard for interviewer effects on one sample's records)."""
    return body(fit(df, None, frame_covariates(df)), counts(df))


def r2_area(df, drop_reissues=False):
    """Interviewer effects within small areas (PSU effects absorbed), the frame covariates held."""
    d = df[~df["reissue"].astype(bool)] if drop_reissues else df
    cov = frame_covariates(d).drop(columns=["urban"])
    return body(fit(d, "psu", cov), counts(d))


def golden(df):
    """Interviewer effects within households (each household's own size absorbed), quarters held: the effect rests
    on the households interviewed by more than one interviewer."""
    return body(fit(df, "unit"), counts(df))


def referred(eff, pool):
    """FQ-3 section 3: an interviewer whose rosters count 12 or more persons per 100 households above the body."""
    return sorted(k for k in pool if k in eff and eff[k] >= TOL)


def dwelling_fe(df):
    """The golden family's variant: the dwelling's own size absorbed (a change of occupant left in)."""
    return body(fit(df, "dwelling"), counts(df))


def segment_fe(df):
    """The golden family's variant: the rotation group's segment absorbed (the same dwellings across waves)."""
    return body(fit(df, "segment", frame_covariates(df).drop(columns=["urban"])), counts(df))
