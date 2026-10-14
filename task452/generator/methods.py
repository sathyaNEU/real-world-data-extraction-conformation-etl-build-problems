"""Every route from the reference sample (and the change map) to the deforested area, and the emission reductions
built on it.

The design-implied route: the sample was drawn by stratified random sampling on the preliminary map's three
classes, so each point stands for its stratum's area over the stratum's sample size, whatever class the final map
later gave it; the deforested area is the sum of those weights over the points the reference data show as
deforestation 2024-2025."""
import math

import numpy as np

import world as W


def weights(points, Ah):
    n = {}
    for p in points:
        n[p["stratum"]] = n.get(p["stratum"], 0) + 1
    return np.array([Ah[p["stratum"]] / n[p["stratum"]] for p in points])


def ydef(points):
    return np.array([1.0 if p["ref"] == "D" else 0.0 for p in points])


def design_area(points, Ah):
    """the stratified estimator on the sampling strata"""
    return float((weights(points, Ah) * ydef(points)).sum())


def design_se(points, Ah):
    """its standard error, the stratified random sampling variance"""
    y = ydef(points)
    v = 0.0
    for s in Ah:
        m = np.array([p["stratum"] == s for p in points])
        n = m.sum()
        ph = y[m].mean()
        v += Ah[s] ** 2 * ph * (1 - ph) / (n - 1)
    return math.sqrt(v)


def design_by_district(points, Ah):
    w, y = weights(points, Ah), ydef(points)
    out = {c: 0.0 for c in W.DCODE}
    for i, p in enumerate(points):
        out[p["district"]] += w[i] * y[i]
    return out


def textbook_area(points, Af):
    """the error-matrix estimator on the final map's classes: each final class's mapped area times the share of its
    points that are deforestation (the strata taken to be the final map's classes)"""
    y = ydef(points)
    tot = 0.0
    for f, a in Af.items():
        m = np.array([p["final"] == f for p in points])
        tot += a * y[m].mean()
    return float(tot)


def poststratified_area(points, Ah, Af):
    """design weights, post-stratified to the final map's class areas"""
    w, y = weights(points, Ah), ydef(points)
    tot = 0.0
    for f, a in Af.items():
        m = np.array([p["final"] == f for p in points])
        tot += a * (w[m] * y[m]).sum() / w[m].sum()
    return float(tot)


def map_area(Af):
    return float(Af["FD"])


def map_user_accuracy(points, Af):
    """the final map's deforestation area times the share of its deforestation points that are deforestation"""
    y = ydef(points)
    m = np.array([p["final"] == "FD" for p in points])
    return float(Af["FD"] * y[m].mean())


def raw_share(points):
    """the share of all reference points that are deforestation, times the accounting area"""
    return float(ydef(points).mean() * sum(d[2] for d in W.DISTRICTS))


def reported(area):
    """the area of deforestation as the monitoring report states it: to the nearest hundred hectares"""
    return int(W.AREA_ROUND * math.floor(area / W.AREA_ROUND + 0.5))


def emission_reductions(area):
    """from the deforested area (unrounded) to the reductions and the payment, as the payment agreement sets them"""
    a = reported(area)
    rl = W.YEARS * W.RL_HA_YEAR * W.EF
    monitored = a * W.EF
    er = rl - monitored
    offered = max(0, math.floor(er * (1 - W.BUFFER)))
    return {"area_ha": a, "rl_t": rl, "monitored_t": monitored, "er_t": er, "buffer_t": er - offered if er > 0 else 0,
            "offered_t": offered, "payment_usd": round(offered * W.PRICE, 2)}
