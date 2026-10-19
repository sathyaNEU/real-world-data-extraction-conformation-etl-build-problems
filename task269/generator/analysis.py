"""task269's analysis: the generalizability study of the 2026 marks and the decision study for 2027, the golden
and every rung of the ladder, computed from station marks (candidates x stations x the station's two examiners)."""
import math
import numpy as np

import common as K


def gstudy(y):
    """Variance components of one examiner's station mark from the balanced p x (r:s) design, by expected mean
    squares: candidate, station, candidate by station, examiner within station, and the residual (the examiner's
    reading of the encounter, confounded with the candidate by examiner interaction)."""
    n_p, n_s, n_r = y.shape
    g = y.mean()
    yp = y.mean(axis=(1, 2))
    ys = y.mean(axis=(0, 2))
    yps = y.mean(axis=2)
    yrs = y.mean(axis=0)
    ss_p = n_s * n_r * ((yp - g) ** 2).sum()
    ss_s = n_p * n_r * ((ys - g) ** 2).sum()
    ss_rs = n_p * ((yrs - ys[:, None]) ** 2).sum()
    ss_ps = n_r * ((yps - yp[:, None] - ys[None, :] + g) ** 2).sum()
    res = y - yps[:, :, None] - yrs[None, :, :] + ys[None, :, None]
    ss_e = (res ** 2).sum()
    ms = {"p": ss_p / (n_p - 1), "s": ss_s / (n_s - 1), "rs": ss_rs / (n_s * (n_r - 1)),
          "ps": ss_ps / ((n_p - 1) * (n_s - 1)), "e": ss_e / ((n_p - 1) * n_s * (n_r - 1))}
    v = {"e": ms["e"], "ps": (ms["ps"] - ms["e"]) / n_r, "p": (ms["p"] - ms["ps"]) / (n_s * n_r),
         "rs": (ms["rs"] - ms["e"]) / n_p, "s": (ms["s"] - ms["ps"] - ms["rs"] + ms["e"]) / (n_p * n_r)}
    return v, ms


def rel_2027(v, n):
    """The 2027 total mark's reliability for ranking candidates at n stations, one examiner a station and the
    examiners differing between candidates (three circuits, examiners from the register): the examiner's
    stringency is error alongside the case specificity and the residual."""
    return v["p"] / (v["p"] + (v["ps"] + v["rs"] + v["e"]) / n)


def need(v_err, v_p, bar=K.STANDARD):
    """The unrounded number of stations at which p / (p + err / n) reaches the bar."""
    return bar / (1 - bar) * v_err / v_p


def alpha(x):
    k = x.shape[1]
    return k / (k - 1) * (1 - x.var(axis=0, ddof=1).sum() / x.sum(axis=1).var(ddof=1))


def sb_need(rel, k, bar=K.STANDARD):
    """Spearman-Brown: the number of stations a coefficient rel at k stations needs to reach the bar."""
    return k * (bar / (1 - bar)) / (rel / (1 - rel))


def sb(rel, k, n):
    f = n / k
    return f * rel / (1 + (f - 1) * rel)


def ladder(y, seed=0):
    v, ms = gstudy(y)
    n_s = y.shape[1]
    out = {"v": v, "ms": ms}
    # R0: the 2026 sitting as it ran, alpha on the two examiners' mean mark, stepped by Spearman-Brown
    a0 = alpha(y.mean(axis=2))
    out["R0"] = {"alpha12": a0, "need": sb_need(a0, n_s), "at": {n: sb(a0, n_s, n) for n in K.SETTINGS}}
    # R1: single-examiner marks, alpha on each examiner's marks (lead, second), stepped by Spearman-Brown;
    # the same as a G-study that keeps each station's examiner crossed with the candidates
    a1 = alpha(y[:, :, 0])
    a2 = alpha(y[:, :, 1])
    cross = v["p"] / (v["p"] + (v["ps"] + v["e"]) / n_s)
    out["R1"] = {"alpha_lead": a1, "alpha_second": a2, "g_crossed12": cross,
                 "need_lead": sb_need(a1, n_s), "need_second": sb_need(a2, n_s),
                 "need_crossed": need(v["ps"] + v["e"], v["p"]),
                 "at": {n: v["p"] / (v["p"] + (v["ps"] + v["e"]) / n) for n in K.SETTINGS}}
    # R2: single examining simulated by taking one of the two examiners' marks at random for each encounter
    rng = np.random.default_rng([seed, 99])
    pick = rng.integers(0, 2, y.shape[:2])
    yp = np.take_along_axis(y, pick[:, :, None], 2)[:, :, 0]
    a3 = alpha(yp)
    out["R2"] = {"alpha": a3, "need": sb_need(a3, n_s), "half": need(v["ps"] + v["rs"] / 2 + v["e"], v["p"])}
    # R3: the absolute coefficient, station difficulty counted as error too
    err_abs = v["s"] + v["ps"] + v["rs"] + v["e"]
    out["R3"] = {"need": need(err_abs, v["p"]), "at": {n: v["p"] / (v["p"] + err_abs / n) for n in K.SETTINGS}}
    # golden
    nstar = need(v["ps"] + v["rs"] + v["e"], v["p"])
    out["golden"] = {"need": nstar, "stations": int(math.ceil(nstar)),
                     "at": {n: rel_2027(v, n) for n in K.SETTINGS}}
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
