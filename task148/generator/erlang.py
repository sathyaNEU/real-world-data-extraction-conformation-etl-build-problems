"""Queueing formulas: Erlang C (M/M/c) and Erlang A (M/M/c+M, exponential patience) service levels.

For Erlang A the tagged caller's phase-type waiting process depends on (c, mu, theta) only: from k callers ahead the
queue advances at rate c*mu + k*theta, from the head of the queue the caller is served at rate c*mu, and the caller
abandons at rate theta throughout. Those matrices are computed once per (c, mu, theta) and reused for every arrival
rate; the arrival rate only sets the stationary distribution seen on arrival (PASTA)."""
from __future__ import annotations

import math

import numpy as np
from scipy.linalg import expm

KMAX = 90            # waiting places modelled; the tail beyond is negligible at the loads used
_TAG = {}


def _tagged(c, mu, th, t, tex):
    key = (c, round(mu, 10), round(th, 10), round(t, 10), round(tex, 10))
    if key in _TAG:
        return _TAG[key]
    K = KMAX
    S, AB = K, K + 1
    Q = np.zeros((K + 2, K + 2))
    for k in range(K):
        if k == 0:
            Q[k, S] = c * mu
        else:
            Q[k, k - 1] = c * mu + k * th
        Q[k, AB] = th
        Q[k, k] = -Q[k].sum()
    Pt = expm(Q * t)
    Pex = expm(Q * tex)
    T = Q[:K, :K]
    a = np.full(K, th)
    M1 = np.linalg.solve(-T, a)                 # P(abandon) from k ahead
    M2 = np.linalg.solve(-T, M1)                # E[time x 1{abandon}] from k ahead
    W1 = np.linalg.solve(-T, np.ones(K))        # E[wait] from k ahead
    out = (Pt[:K, S].copy(), Pex[:K, AB].copy(), M1, M2, W1)
    _TAG[key] = out
    return out


def stationary(lam, mu, th, c):
    N = c + KMAX
    p = np.empty(N)
    p[0] = 1.0
    for n in range(1, N):
        p[n] = p[n - 1] * lam / (min(n, c) * mu + max(n - c, 0) * th)
    return p / p.sum()


def erlang_a(lam, mu, th, c, t=15.0 / 3600, tex=5.0 / 3600):
    """Rates per hour. Returns (P(answered within t), P(abandoned within tex), P(abandon), E[wait | abandoned] in
    hours, E[wait] in hours) for a Poisson arrival."""
    St, ABx, M1, M2, W1 = _tagged(c, mu, th, t, tex)
    p = stationary(lam, mu, th, c)
    q = p[c:]
    st = float(p[:c].sum() + q @ St)
    ab5 = float(q @ ABx)
    pab = float(q @ M1)
    wab = float((q @ M2) / pab) if pab > 0 else float("nan")
    return st, ab5, pab, wab, float(q @ W1)


def erlang_c(lam, mu, c, t=15.0 / 3600):
    """P(answered within t) for M/M/c with no abandonment (every caller waits)."""
    a = lam / mu
    if a >= c:
        return 0.0
    s = sum(a ** k / math.factorial(k) for k in range(c))
    pc = (a ** c / math.factorial(c)) * (c / (c - a))
    pw = pc / (s + pc)
    return 1.0 - pw * math.exp(-(c * mu - lam) * t)
