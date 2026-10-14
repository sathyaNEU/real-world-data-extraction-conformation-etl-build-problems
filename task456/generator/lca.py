"""Estimating each region's share of full hospital-days from the three feeds, and the routes that miss it.

The latent class model: each hospital-day is full or not; given its state the three feeds flag it independently,
each feed with its own chance of flagging a full day (s) and an ordinary day (f), the same everywhere; the share of
full days is free in each region. Maximum likelihood by EM; a day with no census report enters through the two
feeds that did report it.
"""
import itertools

import numpy as np

PATTERNS = list(itertools.product([0, 1], repeat=3))


def _lik(Y, s, f):
    """likelihood of each row's flags under full (l1) and ordinary (l0); NaN flags drop out"""
    obs = ~np.isnan(Y)
    Yz = np.nan_to_num(Y)
    l1 = np.prod(np.where(obs, np.where(Yz == 1, s, 1 - s), 1.0), axis=1)
    l0 = np.prod(np.where(obs, np.where(Yz == 1, f, 1 - f), 1.0), axis=1)
    return l1, l0


def fit(Y, group, groups, by_group=True, iters=20000, tol=1e-12, s0=(0.5, 0.8, 0.4), f0=(0.05, 0.2, 0.05)):
    """EM for the two-class model. Y: n x 3 array of 0, 1 or NaN; group: n labels. Returns the share by group,
    the feeds' s and f, and each row's posterior probability of a full day."""
    Y = np.asarray(Y, dtype=float)
    group = np.asarray(group)
    idx = {g: np.where(group == g)[0] for g in groups}
    pi = {g: 0.3 for g in groups}
    s, f = np.array(s0, dtype=float), np.array(f0, dtype=float)
    obs = ~np.isnan(Y)
    Yz = np.nan_to_num(Y)
    last = None
    for _ in range(iters):
        l1, l0 = _lik(Y, s, f)
        pr = np.empty(len(Y))
        for g in groups:
            pr[idx[g]] = pi[g]
        w = pr * l1 / (pr * l1 + (1 - pr) * l0)
        if by_group:
            pi = {g: float(w[idx[g]].mean()) for g in groups}
        else:
            m = float(w.mean())
            pi = {g: m for g in groups}
        s = np.array([(w * Yz[:, j] * obs[:, j]).sum() / (w * obs[:, j]).sum() for j in range(3)])
        f = np.array([((1 - w) * Yz[:, j] * obs[:, j]).sum() / ((1 - w) * obs[:, j]).sum() for j in range(3)])
        ll = float(np.log(pr * l1 + (1 - pr) * l0).sum())
        if last is not None and abs(ll - last) < tol:
            break
        last = ll
    l1, l0 = _lik(Y, s, f)
    pr = np.array([pi[g] for g in group])
    w = pr * l1 / (pr * l1 + (1 - pr) * l0)
    return {"share": pi, "s": s, "f": f, "post": w, "loglik": last}


def monotone_rules():
    """every non-trivial rule that settles a day as full from its three flags and never un-flags a day when a
    feed adds a flag: a set of flag patterns closed upwards (eighteen of them)"""
    out = []
    for m in range(1, 256):
        S = [PATTERNS[k] for k in range(8) if m >> k & 1]
        if (0, 0, 0) in S:
            continue
        if all(all(q in S for q in PATTERNS if all(q[i] >= p[i] for i in range(3))) for p in S):
            out.append(tuple(S))
    return out


def rule_share(Y, group, groups, rule, missing_as=0):
    """each region's share of hospital-days the rule calls full (a missing census report read as no flag)"""
    Yr = np.where(np.isnan(Y), missing_as, Y).astype(int)
    hit = np.array([tuple(r) in rule for r in Yr], dtype=float)
    group = np.asarray(group)
    return {g: float(hit[group == g].mean()) for g in groups}


def rule_name(rule):
    names = {((0, 0, 1), (0, 1, 0), (0, 1, 1), (1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)): "any feed",
             ((0, 1, 1), (1, 0, 1), (1, 1, 0), (1, 1, 1)): "two of three"}
    return names.get(tuple(sorted(rule)), "+".join("".join("ABC"[i] for i in range(3) if p[i]) for p in
                                                       sorted(rule)))
