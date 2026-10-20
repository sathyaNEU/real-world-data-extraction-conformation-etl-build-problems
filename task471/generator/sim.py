"""The simulation: each county's private domestic wells (on the permit list, the parcel list or both), their nitrate,
the survey's draws from each list (a household that declines or cannot be reached is replaced by the next draw, a
household drawn from both lists is tested once), the first tests and the confirmation retests."""
import numpy as np

import world as W


def rng(seed, *parts):
    return np.random.default_rng([seed, *parts])


def exceed_share(median, sigma):
    """share of wells above the standard for a lognormal nitrate with this median and log-spread"""
    from math import erf, log, sqrt
    z = (log(W.STANDARD_N) - log(median)) / sigma
    return 0.5 * (1 - erf(z / sqrt(2)))


def county(seed, k, p):
    """p: dict(N, po, qo, mPo, mQo, mB, sigma, nP, nQ, accept, retest, phone, tries)"""
    r = rng(seed, 10, k, p.get("tries", 0))
    N = p["N"]
    grp = r.choice(3, N, p=[p["po"], p["qo"], 1 - p["po"] - p["qo"]])      # 0 permit-only, 1 parcel-only, 2 both
    med = np.array([p["mPo"], p["mQo"], p["mB"]])[grp]
    nitrate = med * np.exp(p["sigma"] * r.normal(0, 1, N))
    accept = r.random(N) < p["accept"]
    onP, onQ = grp != 1, grp != 0
    iP, iQ = np.flatnonzero(onP), np.flatnonzero(onQ)
    orderP, orderQ = r.permutation(iP), r.permutation(iQ)
    tested = np.zeros(N, bool)
    from_list = {}                       # well -> set of lists it was drawn from and counted for
    draws = []                           # (list, well, outcome)
    for lst, order, n in (("P", orderP, p["nP"]), ("Q", orderQ, p["nQ"])):
        got = 0
        for i in order:
            if got >= n:
                break
            if tested[i]:
                draws.append((lst, i, "TESTED_EARLIER"))
                from_list.setdefault(i, set()).add(lst)
                got += 1
            elif accept[i]:
                tested[i] = True
                draws.append((lst, i, "TESTED"))
                from_list.setdefault(i, set()).add(lst)
                got += 1
            else:
                draws.append((lst, i, "DECLINED" if r.random() < 0.7 else "NO_RESPONSE"))
    # first test: lab measurement around the well's nitrate
    measured = np.where(tested, nitrate * np.exp(r.normal(0, 0.04, N)), np.nan)
    # confirmation retests of first tests above the standard
    above = tested & (measured > W.STANDARD_N)
    ret = above & (r.random(N) < p["retest"])
    phone = ret & (r.random(N) < p["phone"])
    remeas = np.where(ret, nitrate * r.uniform(0.82, 1.02, N) * np.exp(r.normal(0, 0.04, N)), np.nan)
    return dict(k=k, N=N, grp=grp, nitrate=nitrate, accept=accept, onP=onP, onQ=onQ, tested=tested,
                from_list=from_list, draws=draws, measured=measured, retested=ret, phone=phone, remeasured=remeas,
                nP=p["nP"], nQ=p["nQ"], NP=int(onP.sum()), NQ=int(onQ.sum()))


def estimates(c):
    """every route the ladder names, from the simulated county (no files involved)"""
    fP, fQ = c["nP"] / c["NP"], c["nQ"] / c["NQ"]
    t = c["tested"]
    y = np.where(t, c["measured"] > W.STANDARD_N, False)
    onP, onQ = c["onP"], c["onQ"]
    inP = np.zeros(c["N"], bool)
    inQ = np.zeros(c["N"], bool)
    for i, s in c["from_list"].items():
        inP[i] = "P" in s
        inQ[i] = "Q" in s
    pi = 1 - (1 - fP * onP) * (1 - fQ * onQ)
    out = {}
    out["KA"] = float((y[t] / pi[t]).sum())
    m = onP.astype(int) + onQ.astype(int)
    out["multiplicity"] = float((y[inP] / (fP * m[inP])).sum() + (y[inQ] / (fQ * m[inQ])).sum())
    dom = c["grp"]
    est = 0.0
    for g in (0, 1, 2):
        sel = t & (dom == g)
        est += (dom == g).sum() * (y[sel].mean() if sel.any() else 0.0)
    out["domain means"] = float(est)
    out["pooled"] = float(y[t].mean() * c["N"])
    out["lists added"] = float((y[inP] / fP).sum() + (y[inQ] / fQ).sum())
    w = np.where(inP, 1 / fP, 1 / fQ)
    out["drawn list's rate"] = float((y[t] * w[t]).sum())
    out["permit list alone"] = float((y[inP] / fP).sum())
    out["parcel list alone"] = float((y[inQ] / fQ).sum())
    out["parcel share x wells"] = float(y[inQ].mean() * c["N"])
    for th in (0.0, 1.0):
        g = c["grp"]
        out["hartley %g" % th] = float((y[inP & (g == 0)] / fP).sum() + (y[inQ & (g == 1)] / fQ).sum()
                                       + th * (y[inP & (g == 2)] / fP).sum() + (1 - th) * (y[inQ & (g == 2)] / fQ).sum())
    out["tested above"] = int(y.sum())
    return out
