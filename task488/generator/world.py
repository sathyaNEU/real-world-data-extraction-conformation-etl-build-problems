"""The world before any export: each grade's bank (the 2021 calibrated items and the 2024 and 2025 workshop items
with the writing panel's ratings), the students, and the adaptive engine run over the three 2025-26 windows. The
engine selects and scores with the bank's operational values: the calibrated value, or for a workshop item the
panel's provisional rating."""
from __future__ import annotations

import numpy as np

import params as P

GRID = np.linspace(-5.0, 5.0, 121)
PRIOR = np.exp(-GRID ** 2 / 2)
PRIOR /= PRIOR.sum()


def p_correct(t, b):
    return 1.0 / (1.0 + np.exp(-np.clip(t - b, -30, 30)))


def theta_of(qss):
    return (np.asarray(qss, float) - P.SCALE_A) / P.SCALE_B


def bank(grade, rng):
    cut = theta_of(P.CUT_QSS[grade])
    nk = int(rng.integers(330, 372))
    bk = rng.normal(0.28, 0.85, nk * 2)
    bk = bk[np.abs(bk - cut) > 0.09][:nk]                      # no calibrated item within 3.6 points of the cut
    bk = np.round(P.SCALE_A + P.SCALE_B * bk, 1)                # the bank stores the 2021 value to a tenth
    groups = {"right": int(rng.integers(30, 41)), "low_mis": int(rng.integers(15, 25)),
              "high_mis": int(rng.integers(13, 23)), "mid_ok": int(rng.integers(7, 12))}
    true, rating, grp = [], [], []
    b = rng.uniform(-2.3, -1.3, groups["right"]); true += list(b); rating += list(b - 0.08 + rng.normal(0, 0.14, b.size))
    grp += ["right"] * b.size
    b = np.clip(rng.normal(cut - 0.82, 0.06, groups["low_mis"]), cut - 0.95, cut - 0.7); true += list(b)
    rating += list(rng.normal(-2.5, 0.15, b.size)); grp += ["low_mis"] * b.size
    b = np.clip(rng.normal(cut + 0.62, 0.07, groups["high_mis"]), cut + 0.5, cut + 0.78); true += list(b)
    rating += list(rng.normal(-2.25, 0.15, b.size)); grp += ["high_mis"] * b.size
    b = rng.normal(0.35, 0.35, groups["mid_ok"]); b = np.where(b < cut + 0.35, cut + 0.35 + rng.uniform(0, 0.3, b.size), b)
    true += list(b); rating += list(b + rng.normal(0, 0.15, b.size)); grp += ["mid_ok"] * b.size
    rating = np.round(P.SCALE_A + P.SCALE_B * np.array(rating))     # the panel rated to whole points
    retired = rng.random(bk.size) < 0.035                       # retired in the 2024 review, out of the pool
    return dict(grade=grade, calibrated_qss=bk, prov_true=np.array(true), prov_rating_qss=rating,
                prov_group=np.array(grp), cut=cut, retired=retired)


def run_grade(grade, B, rng):
    """Three windows of the adaptive test. Returns per-event and per-response arrays."""
    nk = B["calibrated_qss"].size
    b_true = np.r_[theta_of(B["calibrated_qss"]) + rng.normal(0, 0.03, nk), B["prov_true"]]
    b_op = np.r_[theta_of(B["calibrated_qss"]), theta_of(B["prov_rating_qss"])]
    ni = b_true.size
    out_of_pool = np.r_[B["retired"], np.zeros(B["prov_true"].size, bool)] * 999.0
    ns = P.STUDENTS[grade]
    base = rng.normal(0, 1, ns)
    growth = [0.0, 0.28 + rng.normal(0, 0.12, ns), 0.49 + rng.normal(0, 0.16, ns)]
    prior_est = np.clip(base + P.WINDOWS[0][3] + rng.normal(0, 0.55, ns), -3, 3)   # last spring's score, roughly
    ev = []    # (student, window, theta_true, rep_eap, rep_sd, n_items, status, resumed_at)
    rs_e, rs_i, rs_x, rs_seq = [], [], [], []
    start = prior_est.copy()
    eid = 0
    for w, (wname, d0, d1, shift) in enumerate(P.WINDOWS):
        th = base + shift + growth[w] - (growth[0] if w == 0 else 0)
        present = rng.random(ns) > P.ABSENT_SHARE
        idx = np.where(present)[0]
        n = idx.size
        tt = th[idx]
        h = start[idx].copy()
        seen = np.zeros((n, ni), bool)
        logL = np.zeros((n, GRID.size))
        length = np.full(n, P.TEST_LENGTH)
        stop = rng.random(n) < P.INCOMPLETE_SHARE
        length[stop] = rng.integers(14, 37, int(stop.sum()))
        for s in range(P.TEST_LENGTH):
            act = length > s
            d = np.abs(b_op[None, :] - h[:, None]) + seen * 99.0 + out_of_pool[None, :]
            cand = np.argpartition(d, P.EXPOSURE_K, axis=1)[:, :P.EXPOSURE_K]
            k = cand[np.arange(n), rng.integers(0, P.EXPOSURE_K, n)]
            x = (rng.random(n) < p_correct(tt, b_true[k])).astype(np.int8)
            seen[np.arange(n)[act], k[act]] = True
            pg = p_correct(GRID[None, :], b_op[k][:, None])
            add = np.where(x[:, None] == 1, np.log(pg), np.log(1 - pg))
            logL[act] += add[act]
            post = np.exp(logL - logL.max(1, keepdims=True)) * PRIOR
            post /= post.sum(1, keepdims=True)
            h = np.where(act, (post * GRID).sum(1), h)
            rs_e.append(eid + np.where(act)[0]); rs_i.append(k[act]); rs_x.append(x[act]); rs_seq.append(np.full(int(act.sum()), s + 1))
        post = np.exp(logL - logL.max(1, keepdims=True)) * PRIOR
        post /= post.sum(1, keepdims=True)
        sd = np.sqrt((post * (GRID[None, :] - h[:, None]) ** 2).sum(1))
        status = np.where(stop, "incomplete", "complete").astype(object)
        inval = rng.random(n) < P.INVALIDATED_SHARE
        status[inval] = "invalidated"
        for j in range(n):
            ev.append((int(idx[j]), w, float(tt[j]), float(h[j]), float(sd[j]), int(length[j]), status[j]))
        start[idx] = h
        eid += n
    E = np.concatenate(rs_e); I = np.concatenate(rs_i); X = np.concatenate(rs_x); SQ = np.concatenate(rs_seq)
    return dict(events=ev, resp_event=E, resp_item=I, resp_score=X, resp_seq=SQ, b_true=b_true, b_op=b_op, nk=nk)


def simulate():
    rb = np.random.default_rng(P.SEED_BANK)
    rc = np.random.default_rng(P.SEED_CAT)
    out = {}
    for g in P.GRADES:
        B = bank(g, rb)
        R = run_grade(g, B, rc)
        out[g] = dict(bank=B, run=R)
    return out
