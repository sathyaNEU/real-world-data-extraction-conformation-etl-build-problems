"""task246 estimators. A zone's wasting figure is read from a normal distribution (section 6 of the protocol): the
children with oedema counted directly, the share of the rest below 125 mm read from the normal distribution with a
mean and standard deviation. The bulletin's figure uses the readings' own mean and spread; the figure from the
children's own arm circumference needs each reading's departure from the round's standard taken out, and the rungs
below differ only in how that is done. REFERENCE names the golden; VARIANTS are the standard ways of computing the same
thing, which have to agree on every note."""
import numpy as np
from scipy.stats import norm

import params as P


def figure(mean, var, n_rest, n_oed):
    """the zone's prevalence in per cent: oedema counted directly, the rest read from the normal distribution"""
    p = norm.cdf((P.CUT - mean) / np.sqrt(var))
    return 100.0 * (n_oed + n_rest * p) / (n_oed + n_rest)


def test_stats(test):
    """test: rows of (measurer, session, child, r1, r2, ref). Each measurer's offset (mean single-reading departure
    from the reference), field error variance (variance of the single-reading departures about the offset), repeat
    error (technical error of measurement squared), mean squared departure, and per-session offsets"""
    out = {}
    for a in sorted({t[0] for t in test}):
        rows = [t for t in test if t[0] == a]
        r = np.array([[t[3], t[4]] for t in rows], float)
        ref = np.array([t[5] for t in rows], float)
        d = (r - ref[:, None]).ravel()
        dm = r.mean(1) - ref
        tem2 = float(np.mean((r[:, 0] - r[:, 1]) ** 2) / 2.0)
        ses = {}
        for s in sorted({t[1] for t in rows}):
            ii = [i for i, t in enumerate(rows) if t[1] == s]
            ses[s] = float((r[ii] - ref[ii][:, None]).mean())
        out[a] = dict(b=float(d.mean()), fe=float(d.var(ddof=1)), fe0=float(d.var(ddof=0)), tem2=tem2,
                      mse=float(np.mean(d ** 2)), fem=float(dm.var(ddof=1) + tem2 / 2.0), ses=ses,
                      seb=float(np.sqrt(dm.var(ddof=1) / len(dm))), n=len(rows))
    return out


def supervisor_tem2(sup):
    """sup: rows of (session, child, r1, r2)"""
    r = np.array([[s[2], s[3]] for s in sup], float)
    return float(np.mean((r[:, 0] - r[:, 1]) ** 2) / 2.0)


def zone_figures(x, meas, sess, oed, T, sup_tem2=0.0):
    """x: the zone's MUAC readings in mm (children without oedema); meas: the anthropometrist of each reading; sess:
    the standardisation session in force on the reading's day (1 before the refresher, 2 from it); oed: the number of
    children with oedema; T: test_stats. Returns the readings' figure and every rung's figure from the children's own
    arm circumference."""
    x = np.asarray(x, float)
    n = len(x)
    m, s2 = x.mean(), x.var(ddof=1)
    g = lambda k: np.array([T[a][k] for a in meas])
    F = lambda mean, var: figure(mean, var, n, oed)
    b = g("b")
    y = x - b
    out = {"readings": F(m, s2)}
    out["R0_repeat"] = F(m, s2 - g("tem2").mean())
    out["R1_field"] = F(m, s2 - g("fe").mean())
    out["R1_mse"] = F(m, s2 - g("mse").mean())
    out["R2_offset_repeat"] = F(y.mean(), y.var(ddof=1) - g("tem2").mean())
    out["R3"] = F(y.mean(), y.var(ddof=1) - g("fe").mean())
    out["R5_offset_mse"] = F(y.mean(), y.var(ddof=1) - g("mse").mean())
    # the standard variants of R3
    w = {a: np.mean(np.asarray(meas) == a) for a in set(meas)}
    bb = sum(w[a] * T[a]["b"] for a in w)
    vb = sum(w[a] * (T[a]["b"] - bb) ** 2 for a in w)
    out["V_zone_level"] = F(m - bb, s2 - vb - sum(w[a] * T[a]["fe"] for a in w))
    out["V_means_route"] = F(y.mean(), y.var(ddof=1) - g("fem").mean())
    out["V_ddof0"] = F(y.mean(), y.var(ddof=0) - g("fe0").mean())
    out["V_reference_error"] = F(y.mean(), y.var(ddof=1) - g("fe").mean() + sup_tem2 / 2.0)
    bs = np.array([T[a]["ses"].get(s, T[a]["b"]) for a, s in zip(meas, sess)])
    ys = x - bs
    out["V_session_offsets"] = F(ys.mean(), ys.var(ddof=1) - g("fe").mean())
    shrink = np.array([T[a]["b"] if abs(T[a]["b"]) >= 2 * T[a]["seb"] else 0.0 for a in meas])
    yk = x - shrink
    out["V_significant_offsets"] = F(yk.mean(), yk.var(ddof=1) - g("fe").mean())
    out["own_mean"], out["own_sd"] = float(y.mean()), float(np.sqrt(y.var(ddof=1) - g("fe").mean()))
    out["read_mean"], out["read_sd"] = float(m), float(np.sqrt(s2))
    out["n"], out["oed"] = n, oed
    return out


RUNGS = ["R0_repeat", "R1_field", "R1_mse", "R2_offset_repeat", "R5_offset_mse"]
REFERENCE = "R3"
VARIANTS = ["R3", "V_zone_level", "V_means_route", "V_ddof0", "V_reference_error", "V_session_offsets",
            "V_significant_offsets"]


def points(Z, key):
    """the measurement points: the readings' figure less the figure from the children's own arm circumference, both
    to one decimal place as the bulletin prints them"""
    return round(round(Z["readings"], 1) - round(Z[key], 1), 1)


def noted(ZF, key):
    """the zones whose two figures differ by the note's points or more, either way"""
    return [z for z in P.ZCODES if abs(points(ZF[z], key)) >= P.NOTE_POINTS - 1e-9]
