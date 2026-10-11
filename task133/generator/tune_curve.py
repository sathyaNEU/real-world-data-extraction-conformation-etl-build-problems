"""Fit PLPD-2026.06's smoothing: from month on book 4 the log of each month's increment is a natural cubic spline (the
knots in world.py), fitted to the development sample's monthly default shares weighted by the defaults in each month,
with the final month (the defaults recorded after the last repayment date) left out of the fit. The coefficients are
then moved as little as the fit allows so that the allowance and both stage amounts come out as they do on the sample's
own shares, with the divisor read from the curve and read from the sample (closure row 6). Builds on the crude shares
(world.CURVE_FIT emptied for the run); paste the printed CURVE_FIT into world.py and rebuild."""
import os
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import extracts as X
import verify as V

P = ("PL36", "PL60")


def grid(target):
    """per product: the stage 1 and 2 loans' positions and the weights PD(k) multiplies (scalar, scenarios, LGD, EAD, DF)"""
    bk, cv, dev, hd, mult, conv = V.read_inputs(target)
    rep = pd.Timestamp(V.REP)
    fr = bk["first_repayment_date"]
    due = ((rep.year - fr.dt.year) * 12 + (rep.month - fr.dt.month) + (fr.dt.day <= rep.day).astype(int)).clip(lower=0)
    rem = (bk["term_months"] - due).where(bk["term_months"] - due > 0, 1)
    pos = (bk["term_months"] - rem).to_numpy()
    st = V.stages(bk, hd, conv, V.REP, bk["current_score_v4"])
    lgd = bk["product"].map({"PL36": 0.70, "PL60": 0.76}).to_numpy()
    out = {}
    for p in P:
        T = W.PRODUCTS[p]
        idx = np.where((bk["product"] == p).to_numpy() & (st < 3))[0]
        aa, rr = pos[idx], rem.to_numpy()[idx]
        H = np.where(st[idx] == 2, rr, np.minimum(12, rr))
        kk = np.arange(1, 61)[None, :]
        mask = kk <= H[:, None]
        m = np.minimum(aa[:, None] + kk, T)
        rate = bk["contract_rate"].to_numpy()[idx] / 12.0
        bal = bk["current_balance"].to_numpy()[idx]
        pmt = bal * rate / (1 - (1 + rate) ** (-rr.astype(float)))
        g = (1 + rate)[:, None] ** (kk - 1)
        ead = bal[:, None] * g - pmt[:, None] * (g - 1) / rate[:, None]
        wgt = np.where(mask, np.where(st[idx] == 2, 2.4, 1.0)[:, None] * mult * lgd[idx][:, None] * ead
                       * (1 + rate)[:, None] ** (-kk), 0.0)
        out[p] = dict(aa=aa, m=m, w=wgt, s2=st[idx] == 2)
    shares = {}
    for p, g in dev.groupby("product"):
        n, T = len(g), W.PRODUCTS[p]
        D = np.cumsum(np.bincount(g.loc[g["outcome"] == "default", "outcome_month_on_book"], minlength=T + 1)) / n
        Cl = np.cumsum(np.bincount(g.loc[g["outcome"] != "default", "outcome_month_on_book"], minlength=T + 1)) / n
        shares[p] = dict(D=D, Cl=Cl, n=n)
    return out, shares


def allowance(G, sh, C, divisor=None):
    """total, stage 1, stage 2; the divisor's default share from `divisor` (the curve itself when None)"""
    f = np.zeros(3)
    for p in P:
        q, c = G[p], C[p]
        dd = c if divisor is None else divisor[p]
        e = ((c[q["m"]] - c[q["m"] - 1]) / (1 - dd[q["aa"]] - sh[p]["Cl"][q["aa"]])[:, None] * q["w"]).sum(1)
        f += [e.sum(), e[~q["s2"]].sum(), e[q["s2"]].sum()]
    return f


def main():
    W.CURVE_FIT = {}
    tmp = tempfile.mkdtemp()
    import build as B
    B.build(tmp)
    G, sh = grid(tmp)
    D = {p: sh[p]["D"] for p in P}
    target = np.concatenate([allowance(G, sh, D)] * 2)
    beta0, info = {}, {}
    for p in P:
        T = W.PRODUCTS[p]
        m = np.arange(W.CURVE_FROM, T + 1, dtype=float)
        inc = np.diff(D[p])[W.CURVE_FROM - 1:]
        wts = inc * sh[p]["n"]                     # defaults in each month
        wts[-1] = 0.0                              # the final month is not fitted
        Bm = X.ns_basis(m, W.CURVE_KNOTS[p])
        A = Bm.T @ (wts[:, None] * Bm)
        beta0[p] = np.linalg.solve(A, Bm.T @ (wts * np.log(inc)))
        info[p] = A
    v0 = np.concatenate([beta0[p] for p in P])
    M = np.zeros((len(v0), len(v0)))
    i = 0
    for p in P:
        k = len(beta0[p])
        M[i:i + k, i:i + k] = info[p]
        i += k

    def unvec(v):
        out, i = {}, 0
        for p in P:
            k = len(beta0[p])
            out[p] = v[i:i + k]
            i += k
        return out

    def F(v):
        C = X.smooth_curve(D, unvec(v))
        return np.concatenate([allowance(G, sh, C), allowance(G, sh, C, D)])

    v = v0.copy()
    for it in range(12):
        f = F(v)
        J = np.zeros((6, len(v)))
        for j in range(len(v)):
            e = np.zeros(len(v))
            e[j] = 1e-6
            J[:, j] = (F(v + e) - F(v - e)) / 2e-6
        K = np.block([[2 * M, J.T], [J, np.zeros((6, 6))]])
        v = np.linalg.solve(K, np.concatenate([2 * M @ v0, target - f + J @ v]))[:len(v)]
    beta = unvec(v)
    C = {p: np.round(c, 6) for p, c in X.smooth_curve(D, beta).items()}
    print("targets  ", np.round(target[:3], 1))
    print("curve    ", np.round(allowance(G, sh, C), 1))
    print("sample S ", np.round(allowance(G, sh, C, D), 1))
    print("CURVE_FIT = {%s}" % ", ".join('"%s": [%s]' % (p, ", ".join(repr(float(x)) for x in beta[p])) for p in P))


if __name__ == "__main__":
    main()
