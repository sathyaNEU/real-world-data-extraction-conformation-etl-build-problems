"""The estimates the review turns on, and the wrong routes beside them. A turn's need is seen in full only when the turn
held its departure (need = time available + the minutes it was not ready); a turn ready in time is known only to have
needed no more than the time it had. The share of turns needing longer than a ground time g is therefore read where it
is fully observed (turns that had less than g), or with the product-limit estimator for left-censored times, or with a
lognormal fitted to the exact and censored turns; the three agree on every verdict and every shortest ground time."""
import numpy as np
from scipy import optimize, stats

import world as W


def cond(t, g, strict=True):
    """Share needing longer than g among the turns that had less than g on the ground (strict) or no more than g:
    every one of those turns shows whether it needed longer than g."""
    m = (t["B"] < g) if strict else (t["B"] <= g)
    if m.sum() == 0:
        return np.nan
    return float((t["exact"] & (t["need"] > g) & m).sum() / m.sum())


def km(t, g):
    """Product-limit estimate for left-censored needs (time reversed): exact needs are events, a ready-in-time turn is
    censored at the time it had."""
    ex = t["exact"].to_numpy()
    y = np.where(ex, t["need"].to_numpy(), t["B"].to_numpy()).astype(float)
    F = 1.0
    for v in np.unique(y[ex & (y > g)]):
        d = ((y == v) & ex).sum()
        r = (y <= v).sum()
        F *= 1 - d / r
    return float(1 - F)


def lognormal(t, g):
    """Lognormal fitted by maximum likelihood to the exact needs and the left-censored ones."""
    ex = t["exact"].to_numpy()
    y = np.log(np.where(ex, t["need"].to_numpy(), np.maximum(t["B"].to_numpy(), 1)).astype(float))

    def nll(p):
        mu, ls = p
        s = np.exp(ls)
        return -(stats.norm.logpdf(y[ex], mu, s).sum() + stats.norm.logcdf(y[~ex], mu, s).sum())
    r = optimize.minimize(nll, [np.log(30), np.log(0.2)], method="Nelder-Mead", options=dict(xatol=1e-7, fatol=1e-9))
    mu, s = r.x[0], np.exp(r.x[1])
    return float(stats.norm.sf((np.log(g) - mu) / s))


ESTIMATORS = {"cond": cond, "cond_le": lambda t, g: cond(t, g, strict=False), "km": km, "lognormal": lognormal}


def gstar(t, f):
    for g in W.GRID:
        v = f(t, g)
        if v == v and v <= W.STANDARD:
            return g
    return None


def review(pop, filings, f=cond, key="seg"):
    """Each relationship's share needing longer than its filing, the verdict and the shortest acceptable time."""
    out = {}
    for seg in W.ORDER:
        t = pop[pop[key] == seg]
        g = filings[seg]
        share = f(t, g)
        out[seg] = dict(turns=len(t), filed=g, share=share, send_back=share > W.STANDARD, shortest=gstar(t, f))
    return out


# ---------------------------------------------------------------- the wrong routes
def r0_visible(t, g):
    """The overruns the records show, over every turn: a ready-in-time turn counted as not needing longer."""
    return float((t["exact"] & (t["need"] > g)).mean())


def r1_ground(t, g):
    """The stand log's ground time less the minutes a ready aircraft was held, read as the need."""
    return float(((t["off"] - t["on"] - t["held"]) > g).mean())


def r2_like(t, g):
    """The turns scheduled with no more than g on the ground in 2026, and the share of them that held the departure."""
    m = t["sched_gt"].notna() & (t["sched_gt"] <= g)
    if m.sum() == 0:
        return np.nan
    return float((t["exact"] & m).sum() / m.sum())


def r5_whole_delay(t, g):
    """Every late minute read as the turn's, held minutes included, then read where fully observed."""
    late = (t["nr"] + t["held"]) > 0
    need = np.where(late, t["B"] + t["nr"] + t["held"], np.nan)
    m = t["B"] < g
    return float(((need > g) & late & m).sum() / m.sum())


POOL = {"S1": "PMV-E75", "S4": "PMV-E75", "S3": "SBC-DH4", "S5": "SBC-DH4", "S2": "GYA-AT7", "S6": "GYA-AT7"}


def r4_pooled(pop, filings):
    """One operator's turns of one type pooled across the brands it flies for, read where fully observed."""
    p = pop.assign(pool=pop["seg"].map(POOL))
    out = {}
    for seg in W.ORDER:
        t = p[p["pool"] == POOL[seg]]
        g = filings[seg]
        s = cond(t, g)
        out[seg] = dict(share=s, send_back=s > W.STANDARD, shortest=gstar(t, cond))
    return out


def rung_verdicts(pop, filings):
    """Each route's set of relationships sent back, and its shortest ground times."""
    rungs = {"R0 visible overruns": r0_visible, "R1 ground time as need": r1_ground,
             "R2 like-for-like 2026 turns": r2_like, "R5 whole delay as need": r5_whole_delay}
    out = {}
    for k, f in rungs.items():
        rv = review(pop, filings, f)
        out[k] = rv
    out["R4 operator pooled"] = r4_pooled(pop, filings)
    return out
