"""The call and every rung beside it, computed from result records, the bridging run and the accuracy check.

The golden: each 2025 result is divided by the bias of the calibration it was measured under. A calibration's shift
against the December bridging run is the mean, over the bridging pairs whose first result it measured, of the log of
the first result over the bridging result; the October check fixes the bias of the calibration it ran under, so the
bridging run's own bias is the check's less that calibration's shift, and every other calibration's is the bridging
run's plus its own shift. Each county's share is the exam-weighted share of its adults whose result so divided is
below 20 ng/mL, and the counties above 30 per cent open first.

Every function takes plain records so the same code runs on the world (generator) and on the pack (verify.py):
  R      list of dicts: seqn, county, w, value, analyzer, lot, cal, month
  pairs  dict seqn -> bridging result
  chk    dict: mean (the provider's mean percent difference), lab, targets, cal, lot, analyzer"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np

CUTOFF = 20.0
LINE = 0.30
NC = 8


def shares(R, logbias):
    """Exam-weighted share below the cut-off by county, each result divided by exp(logbias[i])."""
    num = np.zeros(NC)
    den = np.zeros(NC)
    for r, b in zip(R, logbias):
        den[r["county"]] += r["w"]
        if r["value"] / math.exp(b) < CUTOFF:
            num[r["county"]] += r["w"]
    return num / den


def designated(sh):
    return tuple(int(i) for i in np.where(np.asarray(sh) > LINE)[0])


def anchor(chk, how="provider"):
    """The check's bias on the log scale: the provider's recorded mean percent difference (golden), the mean of the
    five log ratios, or the ratio of the summed results to the summed targets."""
    if how == "provider":
        return math.log1p(chk["mean"] / 100.0)
    if how == "meanlog":
        return float(np.mean([math.log(x / t) for x, t in zip(chk["lab"], chk["targets"])]))
    if how == "sums":
        return math.log(sum(chk["lab"]) / sum(chk["targets"]))
    raise ValueError(how)


def pair_logs(R, pairs):
    out = []
    for r in R:
        if r["seqn"] in pairs:
            out.append((r, math.log(r["value"] / pairs[r["seqn"]])))
    return out


def group_shift(PL, key, est="mean"):
    g = defaultdict(list)
    for r, y in PL:
        g[key(r)].append(y)
    f = {"mean": np.mean, "median": np.median, "ratio": lambda v: math.log(np.mean(np.exp(v)))}[est]
    return {k: float(f(v)) for k, v in g.items()}, {k: len(v) for k, v in g.items()}


def golden(R, pairs, chk, est="mean", how="provider"):
    """Per calibration, anchored at the check's own calibration."""
    PL = pair_logs(R, pairs)
    s, n = group_shift(PL, lambda r: r["cal"], est)
    a = anchor(chk, how)
    if chk["cal"] not in s:
        raise ValueError("no bridging pair measured under the check's calibration")
    lb = [a + s[r["cal"]] - s[chk["cal"]] for r in R]
    return shares(R, lb), dict(shift=s, n=n, anchor=a, bridge_bias=a - s[chk["cal"]])


def routes(R, pairs, chk):
    """The rungs a competent analyst can stop on, each a complete pipeline."""
    a = anchor(chk)
    PL = pair_logs(R, pairs)
    out = {}
    out["R0_reported"] = shares(R, [0.0] * len(R))
    out["R1_check_on_all"] = shares(R, [a] * len(R))
    ys = [y for _, y in PL]
    # one overall shift: every result reads mean(y) above the bridging run, and the bridging run reads like the check
    out["R2_overall_shift"] = shares(R, [a + float(np.mean(ys))] * len(R))
    cell, _ = group_shift(PL, lambda r: (r["lot"], r["analyzer"]))
    ck = (chk["lot"], chk["analyzer"])
    out["R3_lot_analyzer"] = shares(R, [a + cell[(r["lot"], r["analyzer"])] - cell[ck] for r in R])
    # the bridging run on the check's lot and analyzer taken to read like the check
    out["R3b_lot_analyzer_bridge_as_check"] = shares(R, [a + cell[(r["lot"], r["analyzer"])] for r in R])
    lot, _ = group_shift(PL, lambda r: r["lot"])
    out["R3c_lot_only"] = shares(R, [a + lot[r["lot"]] - lot[chk["lot"]] for r in R])
    # additive lot and analyzer effects by least squares
    lots = sorted({r["lot"] for r, _ in PL})
    X = np.array([[1.0 if r["lot"] == L else 0.0 for L in lots] + [float(r["analyzer"])] for r, _ in PL])
    beta, *_ = np.linalg.lstsq(X, np.array(ys), rcond=None)
    eff = {L: beta[i] for i, L in enumerate(lots)}
    out["R3d_lot_plus_analyzer"] = shares(
        R, [a + eff[r["lot"]] + beta[-1] * r["analyzer"] - eff[chk["lot"]] - beta[-1] * chk["analyzer"] for r in R])
    # per calibration, the bridging run taken to read like the check
    cal, _ = group_shift(PL, lambda r: r["cal"])
    out["R4_calibration_bridge_as_check"] = shares(R, [a + cal[r["cal"]] for r in R])
    # time windows instead of calibrations: the month of the run on each analyzer
    mon, _ = group_shift(PL, lambda r: (r["month"], r["analyzer"]))
    cm = (chk["month"], chk["analyzer"])
    out["R5_month_analyzer"] = shares(R, [a + mon[(r["month"], r["analyzer"])] - mon[cm] for r in R])
    return out


def family(R, pairs, chk):
    """The constructions that read each result at its own calibration: three estimators of a calibration's shift
    and three readings of the check's bias."""
    out = {}
    for est in ("mean", "median", "ratio"):
        for how in ("provider", "meanlog", "sums"):
            out["G_%s_%s" % (est, how)] = golden(R, pairs, chk, est, how)[0]
    return out


def margin(sh):
    return float(np.min(np.abs(np.asarray(sh) - LINE)))
