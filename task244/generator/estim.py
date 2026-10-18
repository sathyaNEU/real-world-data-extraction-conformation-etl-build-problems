"""task244 estimators on arrays: the share of a published flow's counted moves that are not real moves, read through the
reinterview's classification error at both quarters (the golden), and the routes the ladder is built against."""
import numpy as np

import params as P

S = P.STATUS
CELLS = [("U", "E"), ("E", "U")]
FLOWNAME = {("U", "E"): "job-finding", ("E", "U"): "job-loss"}


def misread(C):
    """P(recorded status | true status) from a true x recorded table of reinterviewed persons"""
    return C / C.sum(1, keepdims=True)


def true_flows(O, M):
    """the true flows behind a recorded flows table: O = M' F M with independent readings in the two quarters"""
    Mi = np.linalg.inv(M)
    return Mi.T @ (O / O.sum()) @ Mi


def not_real(O, M, a, b):
    """the share of the persons a flow counts as moving from a to b whose true statuses in the two quarters were not
    a then b: one less (true a-to-b flow read correctly at both ends) over the counted flow"""
    i, j = S.index(a), S.index(b)
    F = true_flows(O, M)
    Os = O / O.sum()
    return 1.0 - F[i, j] * M[i, i] * M[j, j] / Os[i, j]


def true_rate(O, M, a, b):
    i, j = S.index(a), S.index(b)
    F = true_flows(O, M)
    return F[i, j] / F[i].sum()


def published_rate(O, a, b):
    i, j = S.index(a), S.index(b)
    return O[i, j] / O[i].sum()


# ------------------------------------------------------------------ the ladder's other routes
def ppv(C):
    """P(true status | recorded status) from the reinterview table (rows true, columns recorded)"""
    return np.diag(C) / C.sum(0)


def not_real_ppv(C, a, b):
    """R1: the two ends' predictive values multiplied, as if a counted move's two readings were independent draws from
    the recorded stocks"""
    v = ppv(C)
    return 1.0 - v[S.index(a)] * v[S.index(b)]


def not_real_both_right(M, a, b):
    """R1': one less the chance both readings are right, the correct-reading rates of the two statuses multiplied"""
    return 1.0 - M[S.index(a), S.index(a)] * M[S.index(b), S.index(b)]


def not_real_net(O, M, a, b):
    """the published rate's overstatement of the true rate as a share of the published rate (a net reading)"""
    pr = published_rate(O / O.sum(), a, b)
    return (pr - true_rate(O, M, a, b)) / pr


def not_real_flow_net(O, M, a, b):
    """the counted flow's excess over the true flow as a share of the counted flow (a net reading at the flow)"""
    i, j = S.index(a), S.index(b)
    return 1.0 - true_flows(O, M)[i, j] / (O / O.sum())[i, j]


def stocks_ppv(F, M):
    """the predictive values of the recorded statuses in a population whose true joint flows are F, pooled over the
    two quarters of the pair"""
    pi = 0.5 * (F.sum(1) + F.sum(0))
    rec = pi @ M
    return pi * np.diag(M) / rec


def warned(shares):
    return sorted(k for k, v in shares.items() if v >= P.WARN_SHARE - 1e-12)


# ------------------------------------------------------------------ variants the checks assert against
def table(true_idx, rec_idx, w=None):
    """a true x recorded table from index arrays, optionally weighted"""
    C = np.zeros((3, 3))
    np.add.at(C, (np.asarray(true_idx), np.asarray(rec_idx)), 1.0 if w is None else np.asarray(w, float))
    return C
