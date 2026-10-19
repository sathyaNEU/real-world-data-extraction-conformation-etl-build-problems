"""task269's analysis: the generalizability study of the 2026 marks and the decision study for 2027, the golden
and every rung of the ladder, computed from station marks (candidates x stations x the station's two examiners).

The blueprint (policy 4.2) draws the same number of stations from each of the four domains every year, the
remainder in the policy's order, so the domains are fixed in every form: a candidate's strength in a domain recurs
in every form and is part of the universe score, while the case specificity within a domain, the examiner's
stringency and the residual are error once each candidate meets one examiner a station in three circuits."""
import math
import numpy as np

import common as K

DOM_OF = [K.DOMAINS.index(st[3]) for st in K.STATIONS26]


def by_domain(y):
    """The station marks regrouped candidates x domain x station within domain x examiner, in the blueprint's
    domain order and each domain's stations in circuit order."""
    idx = [[si for si, d in enumerate(DOM_OF) if d == k] for k in range(len(K.DOMAINS))]
    return np.stack([y[:, ix, :] for ix in idx], axis=1)


def gstudy(y):
    """Variance components of one examiner's station mark from the balanced p x (r:s:d) design, by expected mean
    squares: candidate, candidate by domain, case specificity within domain (candidate by station), examiner within
    station, residual (the examiner's reading of the encounter), and the stations' and domains' own difficulty."""
    z = by_domain(y)
    n_p, n_d, n_s, n_r = z.shape
    g = z.mean()
    m_p = z.mean(axis=(1, 2, 3))
    m_d = z.mean(axis=(0, 2, 3))
    m_pd = z.mean(axis=(2, 3))
    m_sd = z.mean(axis=(0, 3))
    m_psd = z.mean(axis=3)
    m_rsd = z.mean(axis=0)
    ss = {"p": n_d * n_s * n_r * ((m_p - g) ** 2).sum(),
          "d": n_p * n_s * n_r * ((m_d - g) ** 2).sum(),
          "pd": n_s * n_r * ((m_pd - m_p[:, None] - m_d[None, :] + g) ** 2).sum(),
          "sd": n_p * n_r * ((m_sd - m_d[:, None]) ** 2).sum(),
          "psd": n_r * ((m_psd - m_pd[:, :, None] - m_sd[None] + m_d[None, :, None]) ** 2).sum(),
          "rsd": n_p * ((m_rsd - m_sd[:, :, None]) ** 2).sum()}
    res = z - m_psd[..., None] - m_rsd[None] + m_sd[None, :, :, None]
    ss["e"] = (res ** 2).sum()
    df = {"p": n_p - 1, "d": n_d - 1, "pd": (n_p - 1) * (n_d - 1), "sd": n_d * (n_s - 1),
          "psd": (n_p - 1) * n_d * (n_s - 1), "rsd": n_d * n_s * (n_r - 1), "e": (n_p - 1) * n_d * n_s * (n_r - 1)}
    ms = {k: ss[k] / df[k] for k in ss}
    v = {"e": ms["e"], "rs": (ms["rsd"] - ms["e"]) / n_p, "ps": (ms["psd"] - ms["e"]) / n_r,
         "pd": (ms["pd"] - ms["psd"]) / (n_s * n_r), "p": (ms["p"] - ms["pd"]) / (n_d * n_s * n_r),
         "s": (ms["sd"] - ms["psd"] - ms["rsd"] + ms["e"]) / (n_p * n_r),
         "d": (ms["d"] - ms["pd"] - ms["sd"] + ms["psd"]) / (n_p * n_s * n_r)}
    return v, ms


def gstudy_pooled(y):
    """The same marks decomposed with the stations taken as one undivided set (p x (r:s)): candidate, station,
    candidate by station, examiner within station and residual."""
    n_p, n_s, n_r = y.shape
    g = y.mean()
    yp, ys, yps, yrs = y.mean(axis=(1, 2)), y.mean(axis=(0, 2)), y.mean(axis=2), y.mean(axis=0)
    ms = {"p": n_s * n_r * ((yp - g) ** 2).sum() / (n_p - 1), "s": n_p * n_r * ((ys - g) ** 2).sum() / (n_s - 1),
          "rs": n_p * ((yrs - ys[:, None]) ** 2).sum() / (n_s * (n_r - 1)),
          "ps": n_r * ((yps - yp[:, None] - ys[None, :] + g) ** 2).sum() / ((n_p - 1) * (n_s - 1))}
    res = y - yps[:, :, None] - yrs[None, :, :] + ys[None, :, None]
    ms["e"] = (res ** 2).sum() / ((n_p - 1) * n_s * (n_r - 1))
    return {"e": ms["e"], "ps": (ms["ps"] - ms["e"]) / n_r, "p": (ms["p"] - ms["ps"]) / (n_s * n_r),
            "rs": (ms["rs"] - ms["e"]) / n_p, "s": (ms["s"] - ms["ps"] - ms["rs"] + ms["e"]) / (n_p * n_r)}


def blueprint(n):
    """Policy 4.2: the same number of stations from each domain, the remainder from the domains in the policy's
    order (history taking, physical examination, communication, procedural skills)."""
    q, r = divmod(n, len(K.DOMAINS))
    return [q + (1 if k < r else 0) for k in range(len(K.DOMAINS))]


def rel_2027(v, n, examiner_share=1.0):
    """The 2027 total mark's reliability for ranking candidates at n stations on the blueprint, one examiner a
    station: universe score candidate + candidate by domain weighted by the blueprint's shares, error the case
    specificity, the examiner's stringency and the residual over n stations."""
    S = sum((k / n) ** 2 for k in blueprint(n))
    tau = v["p"] + S * v["pd"]
    return tau / (tau + (v["ps"] + examiner_share * v["rs"] + v["e"]) / n)


def rel_multivariate(y, n):
    """The same coefficient from a separate p x (r:s) study in each domain: the domain composite's universe
    covariance (each domain's candidate variance on the diagonal, the domain means' covariances off it) and each
    domain's own error, weighted by the blueprint's stations."""
    z = by_domain(y)
    nd = blueprint(n)
    w = np.array(nd) / n
    comps = [gstudy_pooled(z[:, k]) for k in range(z.shape[1])]
    U = np.cov(z.mean(axis=(2, 3)).T)
    for k in range(z.shape[1]):
        U[k, k] = comps[k]["p"]
    tau = float(w @ U @ w)
    err = sum(w[k] ** 2 * (comps[k]["ps"] + comps[k]["rs"] + comps[k]["e"]) / nd[k] for k in range(len(nd)))
    return tau / (tau + err)


def smallest(f, bar=K.STANDARD, top=60):
    for n in range(4, top):
        if f(n) >= bar:
            return n
    return None


def alpha(x):
    k = x.shape[1]
    return k / (k - 1) * (1 - x.var(axis=0, ddof=1).sum() / x.sum(axis=1).var(ddof=1))


def sb(rel, k, n):
    f = n / k
    return f * rel / (1 + (f - 1) * rel)


def ladder(y, seed=0):
    v, ms = gstudy(y)
    vp = gstudy_pooled(y)
    n_s = y.shape[1]
    out = {"v": v, "ms": ms, "vp": vp}
    # R0: the 2026 sitting as it ran, alpha on the two examiners' mean mark, stepped by Spearman-Brown
    a0 = alpha(y.mean(axis=2))
    out["R0"] = {"alpha12": a0, "stations": smallest(lambda n: sb(a0, n_s, n))}
    # R1: single-examiner marks, alpha on each examiner's marks, stepped by Spearman-Brown, or the pooled study
    # keeping each station's examiner crossed with the candidates
    a1, a2 = alpha(y[:, :, 0]), alpha(y[:, :, 1])
    cross = lambda n: vp["p"] / (vp["p"] + (vp["ps"] + vp["e"]) / n)
    out["R1"] = {"alpha_lead": a1, "alpha_second": a2, "crossed12": cross(n_s),
                 "stations": max(smallest(lambda n: sb(a1, n_s, n)), smallest(lambda n: sb(a2, n_s, n)),
                                 smallest(cross))}
    # R2: single examining simulated by one of the two examiners' marks taken at random for each encounter
    rng = np.random.default_rng([seed, 99])
    pick = rng.integers(0, 2, y.shape[:2])
    yp = np.take_along_axis(y, pick[:, :, None], 2)[:, :, 0]
    a3 = alpha(yp)
    half = lambda n: vp["p"] / (vp["p"] + (vp["ps"] + vp["rs"] / 2 + vp["e"]) / n)
    out["R2"] = {"alpha": a3, "stations": smallest(lambda n: sb(a3, n_s, n)), "half_stations": smallest(half)}
    # R3: the textbook decision study, stations and examiners random from one undivided bank, the stringency error
    flat = lambda n: vp["p"] / (vp["p"] + (vp["ps"] + vp["rs"] + vp["e"]) / n)
    out["R3"] = {"stations": smallest(flat), "at": {n: flat(n) for n in K.SETTINGS}}
    # the blueprint's domains counted but the examiner left crossed (stratified, no stringency)
    strat_x = lambda n: rel_2027(v, n, examiner_share=0.0)
    out["R1s"] = {"stations": smallest(strat_x), "at12": strat_x(n_s)}
    # the absolute coefficient on the pooled study (station difficulty error too)
    absf = lambda n: vp["p"] / (vp["p"] + (vp["s"] + vp["ps"] + vp["rs"] + vp["e"]) / n)
    out["abs"] = {"stations": smallest(absf)}
    # golden and its estimator family
    gold = lambda n: rel_2027(v, n)
    out["golden"] = {"stations": smallest(gold), "at": {n: gold(n) for n in K.SETTINGS},
                     "multivariate": {n: rel_multivariate(y, n) for n in K.SETTINGS},
                     "shared_eleven_twelfths": {n: rel_2027(v, n, 11 / 12) for n in K.SETTINGS}}
    return out


def pass_fail(w, y):
    """The board's 2026 results: each station's pass mark by borderline regression of its examiners' station
    marks on their global grades (1 clear fail to 5 excellent), read at the borderline grade (2); a candidate passes
    when their total mark (the mean of the two examiners at each station, summed) reaches the sum of the stations'
    pass marks and they pass at least eight of the twelve stations."""
    n, S = y.shape[0], y.shape[1]
    cut = np.zeros(S)
    for si, st in enumerate(K.STATIONS26):
        xs, ys = [], []
        for i in range(n):
            for ro in (0, 1):
                xs.append(w["global"][(i, st[0], ro)] + 1)
                ys.append(y[i, si, ro])
        b, a = np.polyfit(xs, ys, 1)
        cut[si] = a + 2 * b
    m = y.mean(axis=2)
    ok = (m.sum(axis=1) >= cut.sum()) & ((m >= cut[None, :]).sum(axis=1) >= 8)
    return int(ok.sum()), int(n - ok.sum()), cut
