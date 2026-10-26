"""The estimator family the directive's expected start leaves open, run on the cut pack: the golden's fit at other
groupings, other forms for the chance a window ends in an event (Weibull, the isotonic fit, a straight line), and the
placements that skip the fit. checks.py asserts where each one files."""
import numpy as np
from scipy.optimize import minimize

import golden as G


def _arrays(win, kind):
    w = np.array([x["w"] for x in win])
    y = np.array([1.0 if x["kind"] == kind else 0.0 for x in win])
    m = {"TH": np.ones(len(win), bool), "CP": np.array([x["comb"] for x in win]),
         "PV": ~np.array([x["tel"] for x in win])}[kind]
    return w[m], y[m]


def weibull(win, kind):
    w, y = _arrays(win, kind)

    def nll(x):
        c, k = np.exp(x)
        F = 1 - np.exp(-c * w ** k)
        return -(y * np.log(np.clip(F, 1e-300, 1)) + (1 - y) * np.log(np.clip(1 - F, 1e-300, 1))).sum()
    r = minimize(nll, [np.log(5e-4), 0.0], method="Nelder-Mead", options=dict(xatol=1e-11, fatol=1e-11, maxiter=20000))
    c, k = np.exp(r.x)

    def hours(W):
        s = np.linspace(0, W, 800)
        f = c * k * np.maximum(s, 1e-9) ** (k - 1) * np.exp(-c * s ** k)
        return W - np.trapezoid(s * f, s) / (1 - np.exp(-c * W ** k))
    return hours, dict(c=float(c), k=float(k), nll=float(r.fun))


def isotonic(win, kind):
    """the nonparametric fit: the chance by window length, monotone; each rise spread evenly over its interval and the
    mass below the shortest window placed at the departure"""
    w, y = _arrays(win, kind)
    o = np.argsort(w, kind="stable")
    y, w = y[o], w[o]
    st = []
    for i in range(len(y)):
        st.append([y[i], 1.0, i])
        while len(st) > 1 and st[-2][0] > st[-1][0]:
            a = st.pop()
            b = st.pop()
            st.append([(a[0] * a[1] + b[0] * b[1]) / (a[1] + b[1]), a[1] + b[1], b[2]])
    xs = np.array([w[s[2]] for s in st])
    Fs = np.array([s[0] for s in st])

    def hours(W):
        j = np.searchsorted(xs, W, side="right") - 1
        num, den = 0.0, Fs[0]
        for q in range(1, j + 1):
            inc = Fs[q] - Fs[q - 1]
            num += inc * (xs[q - 1] + xs[q]) / 2
            den += inc
        return W - (num / den if den > 0 else W / 2)
    return hours


def line(win, kind):
    """a straight line for the chance against the window, by least squares"""
    w, y = _arrays(win, kind)
    X = np.c_[np.ones(len(w)), w]
    a, b = np.linalg.lstsq(X, y, rcond=None)[0]
    a, b = max(a, 0.0), max(b, 1e-12)
    return lambda W: (a * W + b * W * W / 2) / (a + b * W)


def total(p, g, hours_by_kind):
    """the year's methane with the undated starts placed by another estimator"""
    o = g["opts"]
    rt = G.rates(p, o)
    s = 0.0
    for r in g["rows"]:
        if r["basis"] == "ALARM":
            s += r["kg"]
            continue
        h = hours_by_kind[r["kind"]](r["arr"] - r["dep"])
        s += G.methane(rt, r["bat"], r["arr"] - float(h), r["closed"])
    return s / 1000


def forms(p, g):
    win = g["windows"]
    out = {}
    wb = {k: weibull(win, k)[0] for k in ("TH", "CP", "PV")}
    out["weibull"] = total(p, g, wb)
    out["isotonic"] = total(p, g, {k: isotonic(win, k) for k in ("TH", "CP", "PV")})
    out["line"] = total(p, g, {k: line(win, k) for k in ("TH", "CP", "PV")})
    return out


def jump_vs_weibull(g):
    """2 log-likelihood of the golden's form over Weibull's for hatches (both two parameters)"""
    win = g["windows"]
    w, y = _arrays(win, "TH")
    f = g["fits"]["TH"]
    F = 1 - (1 - f["p"]) * np.exp(-f["b"] * w)
    nll_j = -(y * np.log(F) + (1 - y) * np.log(1 - F)).sum()
    return 2 * (weibull(win, "TH")[1]["nll"] - nll_j)


def standing(p, g):
    """the year's release-event methane under each fit the windows support: the golden's share and rate pooled by kind,
    the same fitted by route, by visit schedule and by battery, and the other forms"""
    out = {"pooled": g["total"]}
    for grp in ("route", "cls", "bat"):
        out["group_" + grp] = G.compute(p, fit_group=grp)["total"]
    out.update(forms(p, g))
    return out
