"""The statistics the plan files and the routes a competent analyst could take to a background, shared by the
simulation (to place the deciding October results), the golden and the checks. The verifier has its own copy of
the plan's formula and does not import this module."""
import math

import numpy as np
from scipy import stats

import world as W


def upl(values, alpha=W.ALPHA):
    """The plan's upper prediction limit: exp(m + t s sqrt(1 + 1/n)) on natural logarithms, t at 1 - alpha."""
    y = np.log(np.asarray(values, float))
    n = len(y)
    t = stats.t.ppf(1 - alpha, n - 1)
    return math.exp(y.mean() + t * y.std(ddof=1) * math.sqrt(1 + 1.0 / n))


def rosner_keep(y, alpha=0.05, kmax=10):
    """Generalised ESD (Rosner) on y; returns a keep mask."""
    y = np.asarray(y, float)
    n = len(y)
    kmax = min(kmax, n - 3)
    work = list(range(n))
    removed, R, lam = [], [], []
    for i in range(1, kmax + 1):
        vals = y[work]
        m, s = vals.mean(), vals.std(ddof=1)
        dev = np.abs(vals - m)
        j = int(np.argmax(dev))
        R.append(dev[j] / s)
        removed.append(work[j])
        nn = n - i + 1
        t = stats.t.ppf(1 - alpha / (2 * nn), nn - 2)
        lam.append((nn - 1) * t / math.sqrt((nn - 2 + t * t) * nn))
        work.pop(j)
    nout = 0
    for i in range(kmax):
        if R[i] > lam[i]:
            nout = i + 1
    keep = np.ones(n, bool)
    keep[removed[:nout]] = False
    return keep


def background_limits(bg, rev, events, dry=None, head_diff=None):
    """bg: {(well, event_index, indicator): value} for the background window; rev: {(well, event_index): bool}
    reversed at the boundary on that event's gauging; events: list of event labels. Returns {route: {ind: limit}},
    {route: {ind: n}}."""
    E = sorted({e for (_, e, _) in bg})
    out, cnt = {}, {}

    def build(name, keep):
        out[name], cnt[name] = {}, {}
        for k in W.INDICATORS:
            v = [bg[(w, e, k)] for e in E for w in W.BACKGROUND if (w, e, k) in bg and keep(w, e)]
            out[name][k] = upl(v)
            cnt[name][k] = len(v)

    build("R0 every background result", lambda w, e: True)
    # Rosner screen on the pooled logarithms
    out["R1 pooled Rosner screen"], cnt["R1 pooled Rosner screen"] = {}, {}
    for k in W.INDICATORS:
        v = np.array([bg[(w, e, k)] for e in E for w in W.BACKGROUND if (w, e, k) in bg])
        keep = rosner_keep(np.log(v))
        out["R1 pooled Rosner screen"][k] = upl(v[keep])
        cnt["R1 pooled Rosner screen"][k] = int(keep.sum())
    out["R1w per-well Rosner screen"], cnt["R1w per-well Rosner screen"] = {}, {}
    for k in W.INDICATORS:
        kept = []
        for w in W.BACKGROUND:
            v = np.array([bg[(w, e, k)] for e in E if (w, e, k) in bg])
            keep = rosner_keep(np.log(v), kmax=5)
            kept += list(v[keep])
        out["R1w per-well Rosner screen"][k] = upl(kept)
        cnt["R1w per-well Rosner screen"][k] = len(kept)
    build("R2a background without MW-1", lambda w, e: w != "MW-1")
    build("R2b April results only", lambda w, e: events[e].endswith("APR"))
    build("R2d first eight events", lambda w, e: e < 8)
    build("R2e last eight events", lambda w, e: e >= max(E) - 7)
    build("R2h MW-3 alone", lambda w, e: w == "MW-3")
    if dry is not None:
        build("R2j dry seasons dropped", lambda w, e: events[e] not in dry)
    out["R2c per-well cut at median plus two MAD"], cnt["R2c per-well cut at median plus two MAD"] = {}, {}
    for k in W.INDICATORS:
        kept = []
        for w in W.BACKGROUND:
            v = np.array([bg[(w, e, k)] for e in E if (w, e, k) in bg])
            med = np.median(v)
            mad = 1.4826 * np.median(np.abs(v - med))
            kept += list(v[v <= med + 2 * mad])
        out["R2c per-well cut at median plus two MAD"][k] = upl(kept)
        cnt["R2c per-well cut at median plus two MAD"][k] = len(kept)
    out["R2k per-well Tukey fences"], cnt["R2k per-well Tukey fences"] = {}, {}
    for k in W.INDICATORS:
        kept = []
        for w in W.BACKGROUND:
            v = np.array([bg[(w, e, k)] for e in E if (w, e, k) in bg])
            y = np.log(v)
            q1, q3 = np.percentile(y, 25), np.percentile(y, 75)
            iqr = q3 - q1
            kept += list(v[(y >= q1 - 1.5 * iqr) & (y <= q3 + 1.5 * iqr)])
        out["R2k per-well Tukey fences"][k] = upl(kept)
        cnt["R2k per-well Tukey fences"][k] = len(kept)
    out["R2g nonparametric maximum"] = {k: max(bg[(w, e, k)] for e in E for w in W.BACKGROUND if (w, e, k) in bg)
                                        for k in W.INDICATORS}
    cnt["R2g nonparametric maximum"] = dict(cnt["R0 every background result"])
    build("R3 heads at each sampling event", lambda w, e: not rev[(w, e)])
    revents = {e for (w, e), r in rev.items() if r}
    build("R3e whole reversed events dropped", lambda w, e: e not in revents)
    nxt = {e + 1 for e in revents}
    build("R3n reversed and following events dropped", lambda w, e: not rev[(w, e)] and not (w != "MW-3" and e in nxt))
    for tol in (0.15, 0.25):
        name = "R3t heads with a %.2f ft tolerance" % tol
        out[name], cnt[name] = {}, {}
        for k in W.INDICATORS:
            v = [bg[(w, e, k)] for e in E for w in W.BACKGROUND if (w, e, k) in bg and not (head_diff or {}).get((w, e), 1.0) < tol]
            out[name][k] = upl(v)
            cnt[name][k] = len(v)
    out["R3r heads then Rosner"], cnt["R3r heads then Rosner"] = {}, {}
    for k in W.INDICATORS:
        v = np.array([bg[(w, e, k)] for e in E for w in W.BACKGROUND if (w, e, k) in bg and not rev[(w, e)]])
        keep = rosner_keep(np.log(v))
        out["R3r heads then Rosner"][k] = upl(v[keep])
        cnt["R3r heads then Rosner"][k] = int(keep.sum())
    return out, cnt


GOLDEN = "R3 heads at each sampling event"
LICENSED = ["R3 heads at each sampling event", "R3r heads then Rosner"]
VARIANTS = ["R3e whole reversed events dropped", "R3n reversed and following events dropped"]
CHEAP_HIGH = ["R0 every background result", "R1 pooled Rosner screen", "R1w per-well Rosner screen",
              "R2a background without MW-1", "R2b April results only", "R2d first eight events",
              "R2e last eight events", "R2g nonparametric maximum", "R2j dry seasons dropped",
              "R2c per-well cut at median plus two MAD", "R2k per-well Tukey fences"]
CHEAP_LOW = ["R2h MW-3 alone"]


def designate(limits, october):
    """october: {(well, indicator): result}. The wells with any result above its indicator's limit."""
    return sorted({w for (w, k), v in october.items() if v > limits[k]}, key=lambda w: W.COMPLIANCE.index(w))


def intrawell(history, october):
    """Each compliance well against its own record before the evaluated event (the guidance's alternative)."""
    s = set()
    for (w, k), v in october.items():
        h = history.get((w, k), [])
        if len(h) >= 8 and v > upl(h):
            s.add(w)
    return sorted(s, key=lambda w: W.COMPLIANCE.index(w))
