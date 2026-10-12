"""Binomial GLM on grouped counts (logit, probit or identity link), fitted by Newton iterations, numpy only."""
import math

import numpy as np
from scipy.special import expit, ndtr
from scipy.stats import norm


def fit(X, y, n, link="logit", iters=100, ridge=1e-8, offset=None, b0=None):
    X = np.asarray(X, float)
    y = np.asarray(y, float)
    n = np.asarray(n, float)
    k = X.shape[1]
    off = np.zeros(len(y)) if offset is None else np.asarray(offset, float)
    b = np.zeros(k)
    p0 = min(max(y.sum() / n.sum(), 1e-4), 1 - 1e-4)
    if link == "logit":
        b[0] = math.log(p0 / (1 - p0))
    elif link == "probit":
        b[0] = norm.ppf(p0)
    else:
        b[0] = p0
    if b0 is not None:
        b = np.asarray(b0, float).copy()
    for _ in range(iters):
        eta = X @ b + off
        if link == "logit":
            mu = expit(eta)
            dmu = mu * (1 - mu)
        elif link == "probit":
            mu = ndtr(eta)
            dmu = norm.pdf(eta)
        else:
            mu = np.clip(eta, 1e-6, 1 - 1e-6)
            dmu = np.ones_like(eta)
        var = np.maximum(mu * (1 - mu), 1e-12)
        w = n * dmu * dmu / var
        zres = (y - n * mu) * dmu / var
        H = (X * w[:, None]).T @ X + ridge * np.eye(k)
        g = X.T @ zres
        step = np.linalg.solve(H, g)
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    eta = X @ b + off
    mu = expit(eta) if link == "logit" else (ndtr(eta) if link == "probit" else np.clip(eta, 1e-6, 1 - 1e-6))
    ll = float(np.sum(y * np.log(np.maximum(mu, 1e-300)) + (n - y) * np.log(np.maximum(1 - mu, 1e-300))))
    cov = np.linalg.inv(H)
    return dict(b=b, cov=cov, se=np.sqrt(np.diag(cov)), ll=ll, k=k, aic=2 * k - 2 * ll, link=link)


def predict(model, X, offset=None):
    eta = np.asarray(X, float) @ model["b"] + (0 if offset is None else np.asarray(offset, float))
    if model["link"] == "logit":
        return expit(eta)
    if model["link"] == "probit":
        return ndtr(eta)
    return np.clip(eta, 1e-6, 1 - 1e-6)


def design(df, terms, levels=None):
    """columns: intercept, then each term; a term is a numeric column name, ('cat', col) one-hot with the
    first level dropped, or ('num', col, fn). levels pins the category levels (for prediction frames)."""
    cols = [np.ones(len(df))]
    names = ["const"]
    levels = dict(levels or {})
    for t in terms:
        if isinstance(t, str):
            cols.append(df[t].values.astype(float))
            names.append(t)
        elif t[0] == "cat":
            col = t[1]
            lv = levels.get(col)
            if lv is None:
                lv = sorted(df[col].unique().tolist())
                levels[col] = lv
            v = df[col].values
            for l in lv[1:]:
                cols.append((v == l).astype(float))
                names.append(f"{col}={l}")
        else:
            raise ValueError(t)
    return np.column_stack(cols), names, levels
