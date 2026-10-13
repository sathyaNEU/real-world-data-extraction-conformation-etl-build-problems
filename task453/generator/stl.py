"""STL (Cleveland, Cleveland, McRae and Terpenning 1990) in numpy, following the reference Fortran with the
statsmodels defaults (seasonal 7, trend and low-pass windows from the period, every jump 1, degree 1 throughout,
five inner passes plain, two inner passes and fifteen robustness passes robust)."""
import math
import numpy as np


def _est(y, n, ln, deg, xs, nleft, nright, userw, rw):
    rng = float(n) - 1.0
    h = max(xs - float(nleft), float(nright) - xs)
    if ln > n:
        h += float((ln - n) // 2)
    h9, h1 = 0.999 * h, 0.001 * h
    j = np.arange(nleft, nright + 1, dtype=float)
    r = np.abs(j - xs)
    w = np.zeros_like(j)
    inside = r <= h9
    w[inside] = np.where(r[inside] <= h1, 1.0, (1.0 - (r[inside] / h) ** 3) ** 3) if h > 0 else 1.0
    if userw:
        w = w * rw[nleft - 1:nright]
    a = w.sum()
    if a <= 0:
        return None
    w = w / a
    if h > 0 and deg > 0:
        a = (w * j).sum()
        b = xs - a
        c = (w * (j - a) ** 2).sum()
        if math.sqrt(c) > 0.001 * rng:
            b = b / c
            w = w * (b * (j - a) + 1.0)
    return float((w * y[nleft - 1:nright]).sum())


def _ess(y, n, ln, deg, jump, userw, rw):
    ys = np.zeros(n)
    if n < 2:
        ys[0] = y[0]
        return ys
    newnj = min(jump, n - 1)
    if ln >= n:
        nleft, nright = 1, n
        for i in range(1, n + 1, newnj):
            v = _est(y, n, ln, deg, float(i), nleft, nright, userw, rw)
            ys[i - 1] = y[i - 1] if v is None else v
    elif newnj == 1:
        nsh = (ln + 1) // 2
        nleft, nright = 1, ln
        for i in range(1, n + 1):
            if i > nsh and nright != n:
                nleft += 1
                nright += 1
            v = _est(y, n, ln, deg, float(i), nleft, nright, userw, rw)
            ys[i - 1] = y[i - 1] if v is None else v
    else:
        nsh = (ln + 1) // 2
        for i in range(1, n + 1, newnj):
            if i < nsh:
                nleft, nright = 1, ln
            elif i >= n - nsh + 1:
                nleft, nright = n - ln + 1, n
            else:
                nleft, nright = i - nsh + 1, ln + i - nsh
            v = _est(y, n, ln, deg, float(i), nleft, nright, userw, rw)
            ys[i - 1] = y[i - 1] if v is None else v
    if newnj != 1:
        for i in range(1, n - newnj + 1, newnj):
            delta = (ys[i + newnj - 1] - ys[i - 1]) / newnj
            for jj in range(i + 1, i + newnj):
                ys[jj - 1] = ys[i - 1] + delta * (jj - i)
        k = ((n - 1) // newnj) * newnj + 1
        if k != n:
            v = _est(y, n, ln, deg, float(n), nleft, nright, userw, rw)
            ys[n - 1] = y[n - 1] if v is None else v
            if k != n - 1:
                delta = (ys[n - 1] - ys[k - 1]) / (n - k)
                for jj in range(k + 1, n):
                    ys[jj - 1] = ys[k - 1] + delta * (jj - k)
    return ys


def _ss(y, n, np_, ns, deg, jump, userw, rw):
    season = np.zeros(n + 2 * np_)
    for j in range(1, np_ + 1):
        k = (n - j) // np_ + 1
        w1 = y[j - 1::np_][:k].astype(float)
        w3 = rw[j - 1::np_][:k] if userw else np.ones(k)
        w2 = np.zeros(k + 2)
        w2[1:k + 1] = _ess(w1, k, ns, deg, jump, userw, w3)
        nright = min(ns, k)
        v = _est(w1, k, ns, deg, 0.0, 1, nright, userw, w3)
        w2[0] = w2[1] if v is None else v
        nleft = max(1, k - ns + 1)
        v = _est(w1, k, ns, deg, float(k + 1), nleft, k, userw, w3)
        w2[k + 1] = w2[k] if v is None else v
        for m in range(1, k + 3):
            season[(m - 1) * np_ + j - 1] = w2[m - 1]
    return season


def _ma(x, ln):
    c = np.concatenate([[0.0], np.cumsum(x)])
    return (c[ln:] - c[:-ln]) / ln


def _fts(x, np_):
    return _ma(_ma(_ma(x, np_), np_), 3)


def _rwts(y, fit):
    r = np.abs(y - fit)
    n = len(y)
    s = np.sort(r)
    m1 = n // 2 + 1
    m2 = n - m1 + 1
    cmad = 3.0 * (s[m1 - 1] + s[m2 - 1])
    c9, c1 = 0.999 * cmad, 0.001 * cmad
    rw = np.where(r <= c1, 1.0, np.where(r <= c9, (1.0 - (r / cmad) ** 2) ** 2, 0.0))
    return rw


def stl(y, period=12, seasonal=7, trend=None, low_pass=None, robust=False, inner=None, outer=None):
    y = np.asarray(y, dtype=float)
    n = len(y)
    if trend is None:
        trend = int(math.ceil(1.5 * period / (1.0 - 1.5 / seasonal)))
        trend += (trend % 2) == 0
    if low_pass is None:
        low_pass = period + 1
        low_pass += (low_pass % 2) == 0
    inner = inner if inner is not None else (2 if robust else 5)
    outer = outer if outer is not None else (15 if robust else 0)
    tr = np.zeros(n)
    se = np.zeros(n)
    rw = np.ones(n)
    userw = False
    k = 0
    while True:
        for _ in range(inner):
            w = y - tr
            c = _ss(w, n, period, seasonal, 1, 1, userw, rw)
            lp = _ess(_fts(c, period), n, low_pass, 1, 1, False, rw)
            se = c[period:period + n] - lp
            tr = _ess(y - se, n, trend, 1, 1, userw, rw)
        k += 1
        if k > outer:
            break
        rw = _rwts(y, tr + se)
        userw = True
    return se, tr, y - se - tr
