"""The equating methods and the ladder's routes, on plain arrays: X and VX for the new form's first-attempt
candidates, Y and VY for the base form's. Linear methods (Tucker and Levine observed-score at three synthetic weights,
chained linear) and chained equipercentile with continuized percentile ranks; a route's cut is the smallest new-form
raw score whose equated score rounds to the base form's passing raw score."""
import numpy as np

import world as W

MAXX = W.MAX_RAW
VMAX = W.N_SHARED + W.WA_WEIGHT * 8


def chained_linear(X, VX, Y, VY, vshift=0.0):
    mvx = VX.mean() + vshift
    return lambda x: Y.mean() + Y.std() / VY.std() * (mvx + VX.std() / X.std() * (x - X.mean()) - VY.mean())


def _synthetic(X, VX, Y, VY, g1, g2, w1, vshift):
    w2 = 1 - w1
    dmu = VX.mean() + vshift - VY.mean()
    dvar = VX.var() - VY.var()
    mux = X.mean() - w2 * g1 * dmu
    muy = Y.mean() + w1 * g2 * dmu
    vx = X.var() - w2 * g1 ** 2 * dvar + w1 * w2 * g1 ** 2 * dmu ** 2
    vy = Y.var() + w1 * g2 ** 2 * dvar + w1 * w2 * g2 ** 2 * dmu ** 2
    return lambda x: muy + np.sqrt(vy / vx) * (x - mux)


def tucker(X, VX, Y, VY, w1=None, vshift=0.0):
    w1 = len(X) / (len(X) + len(Y)) if w1 is None else w1
    return _synthetic(X, VX, Y, VY, np.cov(X, VX)[0, 1] / VX.var(), np.cov(Y, VY)[0, 1] / VY.var(), w1, vshift)


def levine(X, VX, Y, VY, w1=None, vshift=0.0):
    w1 = len(X) / (len(X) + len(Y)) if w1 is None else w1
    return _synthetic(X, VX, Y, VY, X.var() / np.cov(X, VX)[0, 1], Y.var() / np.cov(Y, VY)[0, 1], w1, vshift)


def _cdf(s, top):
    return np.cumsum(np.bincount(np.asarray(np.round(s), int), minlength=top + 1)[: top + 1] / len(s))


def _prk(F, x):
    top = len(F) - 1
    if x < -0.5:
        return 0.0
    if x >= top + 0.5:
        return 1.0
    xs = int(np.floor(x + 0.5))
    lo = F[xs - 1] if xs >= 1 else 0.0
    return lo + (x - xs + 0.5) * (F[xs] - lo)


def _iprk(F, pr):
    top = len(F) - 1
    xp = np.concatenate([[-0.5], np.arange(top + 1) + 0.5])
    fp = np.concatenate([[0.0], F])
    keep = np.concatenate([[True], np.diff(fp) > 1e-12])
    return float(np.interp(pr, fp[keep], xp[keep]))


def chained_equipercentile(X, VX, Y, VY, vshift=0.0):
    FX, FVX, FY, FVY = _cdf(X, MAXX), _cdf(VX, VMAX), _cdf(Y, MAXX), _cdf(VY, VMAX)
    return lambda x: _iprk(FY, _prk(FVY, _iprk(FVX, _prk(FX, x)) + vshift))


def family(X, VX, Y, VY, vshift=0.0):
    """every method the golden must agree under: Tucker and Levine at the sample weight, equal weights and the new
    form's population, chained linear and chained equipercentile"""
    out = {"chained linear": chained_linear(X, VX, Y, VY, vshift),
           "chained equipercentile": chained_equipercentile(X, VX, Y, VY, vshift)}
    for nm, w in (("sample", None), ("equal", 0.5), ("new form", 1.0)):
        out["Tucker (%s weights)" % nm] = tucker(X, VX, Y, VY, w, vshift)
        out["Levine (%s weights)" % nm] = levine(X, VX, Y, VY, w, vshift)
    return out


def cut(e, target=W.PASS_RAW_25A):
    for x in range(MAXX + 1):
        if e(x) >= target - 0.5:
            return x, float(e(x)), float(e(x - 1))
    return None


def validity_shift(papers, reads, wa="WA2", per_paper=False):
    """mean (2026 read minus consensus) on the assignment's validity papers; the anchor's shift for that assignment is
    minus twice it (two reads) times the assignment's weight"""
    if per_paper:
        by = {}
        for pi, v in reads:
            if papers[pi]["wa"] == wa:
                by.setdefault(pi, []).append(v - papers[pi]["consensus"])
        return float(np.mean([np.mean(v) for v in by.values()]))
    d = [v - papers[pi]["consensus"] for pi, v in reads if papers[pi]["wa"] == wa]
    return float(np.mean(d))


def routes(X, VX, VXmc, Y, VY, VYmc, bias_wa2, bias_pooled):
    """the ladder: every route's cut under every method"""
    shift = -2 * bias_wa2 * W.WA_WEIGHT
    shift_pooled = -2 * bias_pooled * W.WA_WEIGHT
    out = {"R0 the 2025 raw passing score": {"none": cut(lambda x: x)},
           "R0p raters adjusted, no equating": {"none": cut(lambda x: x - 2 * bias_wa2 * W.WA_WEIGHT * W.N_WA)}}
    out["R1 anchor as scored"] = {k: cut(e) for k, e in family(X, VX, Y, VY).items()}
    out["R1p anchor adjusted by every assignment's papers"] = {k: cut(e) for k, e in
                                                               family(X, VX, Y, VY, shift_pooled).items()}
    out["R2 multiple-choice anchor"] = {k: cut(e) for k, e in family(X, VXmc, Y, VYmc).items()}
    out["G anchor on the 2025 standard"] = {k: cut(e) for k, e in family(X, VX, Y, VY, shift).items()}
    return out, shift


def pass_rates(rows, scored, cut26):
    """each program's 2025-26 completers with a first attempt: a June 2025 first attempt passes at raw 56 on 25A, a
    June 2026 first attempt at the 2026 cut"""
    res = {}
    for yr, c in ((2025, W.PASS_RAW_25A), (2026, cut26)):
        s = scored[yr]
        for j, i in enumerate(s["idx"]):
            x = rows[i]
            if x["group"] == "completer" and x["first"] == yr:
                res.setdefault(x["program"], []).append(bool(s["raw"][j] >= c))
    return {k: (sum(v), len(v)) for k, v in res.items()}
