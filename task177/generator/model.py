"""task177 model: the reinforcement-learning model of each jobseeker's channel choices, fitted by maximum likelihood
to their contact-by-contact record, and its simulation forward through the assistant-first weeks and the window.

One value per channel, moved after each contact towards its outcome (1 resolved, 0 not) by a learning rate; the
assistant chosen with probability logistic(beta * (Q_assistant - Q_phone) + bias + kappa * last), last being +1 when
the jobseeker's previous choice was the assistant and -1 when it was the phone. The rate a contact moves its channel's
value by is a_free for a contact the jobseeker chose and a_forced for an overflow transfer; the specifications differ in
how a_forced is tied (to a_free, to nothing, or free) and in the perseveration and starting values."""
from __future__ import annotations

import numpy as np
from scipy.optimize import minimize


def sigm(x):
    return 1.0 / (1.0 + np.exp(-x))


class Seq:
    """per-claimant sequences, padded and ordered longest first so each position is a leading slice"""

    def __init__(self, cid, choice, red, res, extra=None):
        cid = np.asarray(cid)
        n_by = {}
        order = np.argsort(cid, kind="stable")
        cid_s = cid[order]
        uniq, start, cnt = np.unique(cid_s, return_index=True, return_counts=True)
        rank = np.argsort(-cnt, kind="stable")
        self.ids = uniq[rank]
        self.n = cnt[rank]
        N, L = len(self.ids), int(self.n.max())
        self.N, self.L = N, L
        self.valid = np.arange(L)[None, :] < self.n[:, None]
        self.choice = np.zeros((N, L), bool)
        self.red = np.zeros((N, L), bool)
        self.res = np.zeros((N, L), float)
        for row, (s, c) in enumerate(zip(start[rank], cnt[rank])):
            sel = order[s:s + c]
            self.choice[row, :c] = np.asarray(choice)[sel]
            self.red[row, :c] = np.asarray(red)[sel]
            self.res[row, :c] = np.asarray(res)[sel]
        self.m_t = (self.n[None, :] > np.arange(L)[:, None]).sum(1)
        self.index = {k: i for i, k in enumerate(self.ids)}


SPECS = {
    # the field's textbook route: one learning rate for every contact
    "one_rate": dict(split="same", persev="choice", q0="fixed"),
    # the decisive judgment: contacts the jobseeker did not choose learned at their own rate
    "split": dict(split="free", persev="choice", q0="fixed"),
    "split_no_persev": dict(split="free", persev="none", q0="fixed"),
    "split_persev_exp": dict(split="free", persev="experienced", q0="fixed"),
    "split_q0": dict(split="free", persev="choice", q0="est"),
    "teach_nothing": dict(split="zero", persev="choice", q0="fixed"),
    "one_rate_no_persev": dict(split="same", persev="none", q0="fixed"),
    "one_rate_q0": dict(split="same", persev="choice", q0="est"),
    # readings of how a transfer moves the phone's value too (the model class left open; the record rejects both)
    "split_tp_free": dict(split="free", persev="choice", q0="fixed", transfer_phone="free"),
    "split_tp_forced": dict(split="free", persev="choice", q0="fixed", transfer_phone="forced"),
    # an outsider's other readings of the same class: the transferred calls' choice left out of the likelihood, and
    # the values started at 0 or at 1 rather than halfway
    "split_lik_out": dict(split="free", persev="choice", q0="fixed", lik_transfers=False),
    "split_q0_zero": dict(split="free", persev="choice", q0="zero"),
    "split_q0_one": dict(split="free", persev="choice", q0="one"),
}


def n_params(spec):
    return 3 + (spec["split"] == "free") + (spec["persev"] != "none") + 2 * (spec["q0"] == "est")


def unpack(x, spec):
    i = 0
    P = {}
    P["a_free"] = sigm(x[i]); i += 1
    if spec["split"] == "free":
        P["a_forced"] = sigm(x[i]); i += 1
    elif spec["split"] == "zero":
        P["a_forced"] = 0.0
    else:
        P["a_forced"] = P["a_free"]
    P["beta"] = np.exp(x[i]); i += 1
    P["bias"] = x[i]; i += 1
    P["kappa"] = 0.0
    if spec["persev"] != "none":
        P["kappa"] = x[i]; i += 1
    P["q0b"] = P["q0p"] = {"zero": 0.0, "one": 1.0}.get(spec["q0"], 0.5)
    if spec["q0"] == "est":
        P["q0b"] = sigm(x[i]); P["q0p"] = sigm(x[i + 1]); i += 2
    return P


def x0_for(spec, k):
    base = [dict(a=-0.5, f=-1.5, b=1.5, c=-0.5, k=0.3, q=0.0), dict(a=0.3, f=-0.5, b=1.2, c=0.0, k=0.0, q=0.3)][k]
    x = [base["a"]]
    if spec["split"] == "free":
        x.append(base["f"])
    x += [base["b"], base["c"]]
    if spec["persev"] != "none":
        x.append(base["k"])
    if spec["q0"] == "est":
        x += [base["q"], base["q"]]
    return np.array(x, float)


def run(P, S, spec, want_ll=True, mask=None):
    """the log-likelihood of every choice (or of the choices where mask is set) and the end state; with a mask,
    also the predicted and observed assistant choices over the masked contacts"""
    N = S.N
    qb = np.full(N, P["q0b"])
    qp = np.full(N, P["q0p"])
    last = np.zeros(N)
    ll = 0.0
    pred = obs = cnt = 0.0
    af, ao, be, bi, ka = P["a_free"], P["a_forced"], P["beta"], P["bias"], P["kappa"]
    exp_persev = spec["persev"] == "experienced"
    tp = {"free": af, "forced": ao}.get(spec.get("transfer_phone", "none"))
    for t in range(S.L):
        m = S.m_t[t]
        if m == 0:
            break
        c = S.choice[:m, t]
        rd = S.red[:m, t]
        r = S.res[:m, t]
        QB = qb[:m]
        QP = qp[:m]
        if want_ll:
            x = be * (QB - QP) + bi + ka * last[:m]
            terms = np.where(c, -np.logaddexp(0.0, -x), -np.logaddexp(0.0, x))
            if spec.get("lik_transfers", True) is False:
                terms = np.where(rd, 0.0, terms)
            if mask is None:
                ll += float(np.sum(terms))
            else:
                mk = mask[:m, t]
                ll += float(np.sum(terms[mk]))
                pred += float(np.sum(sigm(x[mk])))
                obs += float(np.sum(c[mk]))
                cnt += float(mk.sum())
        gb = c | rd
        a = np.where(rd, ao, af)
        QB += np.where(gb, a * (r - QB), 0.0)
        QP += np.where(~gb, af * (r - QP), 0.0)
        if tp is not None:
            QP += np.where(rd, tp * (r - QP), 0.0)
        last[:m] = np.where(gb if exp_persev else c, 1.0, -1.0)
    out = dict(qb=qb, qp=qp, last=last)
    if mask is not None:
        out.update(pred=pred, obs=obs, n=cnt)
    return ll, out


def fit(S, spec, starts=(0, 1)):
    best = None
    for k in starts:
        f = lambda x: -run(unpack(x, spec), S, spec)[0]
        r = minimize(f, x0_for(spec, k), method="L-BFGS-B", options={"maxiter": 400, "eps": 1e-6})
        if best is None or r.fun < best.fun:
            best = r
    P = unpack(best.x, spec)
    return P, -best.fun, best.x


def simulate(P, spec, qb, qp, last, rate_day, af_days, free_days, p_new, p_phone, p_over, reps=60, seed=1,
             life=None, sched_af=None, sched_free=None, p_chat=None, p_sent_free=None, denom="all",
             num="chosen", af_last="chosen"):
    """the expected share of the population's own contacts started in the assistant over the free days, after the
    assistant-first days (every phone choice met by the upgraded assistant). Each claimant makes sched_af and
    sched_free scheduled contacts in the two phases (none when not given) and further contacts at rate_day a day;
    p_over is the share of free-day calls the overflow transfers; life (optional) each claimant's days left. p_chat
    and p_sent_free (optional, the semantic-fork rows only) resolve the conversations a claimant opens, and the
    free days' transfers, at another rate than p_new. denom "no_transfers" leaves the free days' transferred calls out
    of the denominator, num "with_transfers" counts them as assistant starts (both semantic-fork rows only)"""
    rng = np.random.default_rng(seed)
    exp_persev = spec["persev"] == "experienced"
    tp_rate = {"free": P["a_free"], "forced": P["a_forced"]}.get(spec.get("transfer_phone", "none"))
    tb = tt = 0.0
    tb_af = tt_af = 0.0
    n = qb.size
    z = np.zeros(n, int)
    for k in range(reps):
        b = qb.copy()
        p = qp.copy()
        la = last.copy()
        for phase, ndays, sch in (("af", af_days, sched_af), ("free", free_days, sched_free)):
            if life is None:
                nk = rng.poisson(rate_day * ndays) + (z if sch is None else sch)
            else:
                start = 0 if phase == "af" else af_days
                open_frac = np.clip(life - start, 0, ndays) / ndays
                nk = rng.poisson(rate_day * ndays * open_frac) + \
                    (z if sch is None else rng.binomial(sch, open_frac))
            for t in range(int(nk.max()) if n else 0):
                ii = np.flatnonzero(nk > t)
                x = P["beta"] * (b[ii] - p[ii]) + P["bias"] + P["kappa"] * la[ii]
                cb = rng.random(ii.size) < sigm(x)
                if phase == "af":
                    rd = ~cb
                else:
                    rd = (~cb) & (rng.random(ii.size) < p_over)
                gb = cb | rd
                u1 = rng.random(ii.size)
                u2 = rng.random(ii.size)
                thr = p_new
                if p_chat is not None or (p_sent_free is not None and phase == "free"):
                    thr = np.full(ii.size, p_new)
                    if p_chat is not None:
                        thr = np.where(cb, p_chat, thr)
                    if p_sent_free is not None and phase == "free":
                        thr = np.where(rd, p_sent_free, thr)
                r = np.where(gb, u1 < thr, u2 < p_phone).astype(float)
                a = np.where(rd, P["a_forced"], P["a_free"])
                b[ii] = np.where(gb, b[ii] + a * (r - b[ii]), b[ii])
                p[ii] = np.where(~gb, p[ii] + P["a_free"] * (r - p[ii]), p[ii])
                if tp_rate is not None:
                    p[ii] = np.where(rd, p[ii] + tp_rate * (r - p[ii]), p[ii])
                la[ii] = np.where(gb if (exp_persev or (af_last == "met" and phase == "af")) else cb, 1.0, -1.0)
                if phase == "free":
                    tb += cb.sum() + (rd.sum() if num == "with_transfers" else 0)
                    tt += ii.size - (rd.sum() if denom == "no_transfers" else 0)
                else:
                    tb_af += cb.sum(); tt_af += ii.size
    return dict(share=tb / tt, share_af=tb_af / tt_af)
