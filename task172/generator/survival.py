"""Survival machinery shared by the golden, the checks, the verifier and the seed screen: the stratified log-rank
test with ties, the stratified Cox hazard ratio (Efron ties), interval hazards, the B-value conditional power,
and the patient-level projection of the trial to its final event count."""
import math

import numpy as np
from scipy.stats import norm

Z_ALPHA = norm.ppf(0.975)


def logrank(time, event, arm, stratum):
    """Stratified log-rank: returns (z, U, V) with U = expected minus observed on arm 1, so z > 0 favours arm 1."""
    U = V = 0.0
    for s in np.unique(stratum):
        m = stratum == s
        t, e, a = time[m], event[m].astype(float), arm[m].astype(float)
        ut, inv = np.unique(t, return_inverse=True)
        d = np.bincount(inv, weights=e, minlength=len(ut))
        d1 = np.bincount(inv, weights=e * a, minlength=len(ut))
        cnt = np.bincount(inv, minlength=len(ut)).astype(float)
        cnt1 = np.bincount(inv, weights=a, minlength=len(ut))
        n = np.cumsum(cnt[::-1])[::-1]
        n1 = np.cumsum(cnt1[::-1])[::-1]
        k = d > 0
        d, d1, n, n1 = d[k], d1[k], n[k], n1[k]
        U += np.sum(d * n1 / n - d1)
        with np.errstate(invalid="ignore", divide="ignore"):
            v = d * (n1 / n) * (1 - n1 / n) * np.where(n > 1, (n - d) / (n - 1), 0.0)
        V += np.nansum(v)
    return U / math.sqrt(V), U, V


def cox_hr(time, event, arm, stratum, iters=50):
    """Stratified Cox model, one binary covariate, Efron ties: (hr, se of log hr)."""
    beta = 0.0
    for _ in range(iters):
        g = h = 0.0
        for s in np.unique(stratum):
            m = stratum == s
            t, e, a = time[m], event[m].astype(bool), arm[m].astype(float)
            r = np.exp(beta * a)
            for tt in np.unique(t[e]):
                at = t >= tt
                dm = (t == tt) & e
                dcount = dm.sum()
                s0, s1 = np.sum(r[at]), np.sum((r * a)[at])
                s0d, s1d = np.sum(r[dm]), np.sum((r * a)[dm])
                g += np.sum(a[dm])
                for l in range(dcount):
                    f = l / dcount
                    a0 = s0 - f * s0d
                    a1 = s1 - f * s1d
                    g -= a1 / a0
                    h += a1 / a0 - (a1 / a0) ** 2
        step = g / h
        beta += step
        if abs(step) < 1e-10:
            break
    return math.exp(beta), 1 / math.sqrt(h)


def interval_rates(time, event, arm, cuts):
    """Events and exposure by arm in [cuts[i], cuts[i+1]): rows of (lo, hi, d0, pt0, d1, pt1)."""
    rows = []
    for lo, hi in zip(cuts[:-1], cuts[1:]):
        r = [lo, hi]
        for a in (0, 1):
            m = arm == a
            pt = np.clip(np.minimum(time[m], hi) - lo, 0, None).sum()
            d = int(np.sum(event[m] & (time[m] >= lo) & (time[m] < hi)))
            r += [d, float(pt)]
        rows.append(r)
    return rows


def cp_bvalue(z, frac, theta_full):
    """Conditional power from the B-value: z at information fraction frac, drift theta_full at full information."""
    b = z * math.sqrt(frac)
    return 1 - norm.cdf((Z_ALPHA - b - theta_full * (1 - frac)) / math.sqrt(1 - frac))


def weibull_fit(time, event):
    """Weibull MLE (shape k, scale lam) by a profile search on k."""
    t = np.maximum(time, 0.5)
    d = event.sum()
    best = None
    for k in np.linspace(0.3, 3.0, 541):
        lam = (np.sum(t ** k) / d) ** (1 / k)
        ll = d * math.log(k) - d * k * math.log(lam) + (k - 1) * np.sum(np.log(t[event])) - np.sum((t / lam) ** k)
        if best is None or ll > best[0]:
            best = (ll, k, lam)
    return best[1], best[2]


class Hazard:
    """Per-arm hazards for the projection: kind 'pw' (piecewise constant on breaks), 'ph' (control piecewise with a
    constant hazard ratio), or 'weibull'."""

    def __init__(self, kind, time, event, arm, breaks=(), hr=None):
        self.kind = kind
        if kind in ("pw", "ph"):
            self.cuts = [0.0] + list(breaks) + [1e9]
            rows = interval_rates(time, event, arm, self.cuts)
            self.rate = np.array([[r[2] / r[3], r[4] / r[5]] for r in rows])
            if kind == "ph":
                self.rate[:, 1] = self.rate[:, 0] * hr
        else:
            self.wb = [weibull_fit(time[arm == a], event[arm == a].astype(bool)) for a in (0, 1)]

    def draw(self, rng, arm, start):
        u = rng.exponential(1.0, len(arm))
        if self.kind == "weibull":
            out = np.empty(len(arm))
            for a in (0, 1):
                m = arm == a
                k, lam = self.wb[a]
                h0 = (start[m] / lam) ** k
                out[m] = lam * (h0 + u[m]) ** (1 / k)
            return out
        out = np.full(len(arm), np.nan)
        rem = u.copy()
        pos = start.astype(float).copy()
        done = np.zeros(len(arm), bool)
        for j in range(len(self.cuts) - 1):
            lo, hi = self.cuts[j], self.cuts[j + 1]
            rate = self.rate[j][arm]
            act = (~done) & (pos < hi)
            span = np.where(act, hi - np.maximum(pos, lo), 0.0)
            cap = rate * span
            hit = act & (rem < cap)
            out[hit] = np.maximum(pos[hit], lo) + rem[hit] / rate[hit]
            done |= hit
            rem = np.where(act & ~hit, rem - cap, rem)
            pos = np.where(act & ~hit, hi, pos)
        return out


def project_cp(pfs, hz, nsim, seed, n_target, final_events, enrol_rate, drop_rate, strata_mix, stratified=True):
    """Conditional power by simulating every patient still at risk at the cut and every patient still to be
    randomised, under hazards hz, to the calendar day of the final event count; the final analysis is the
    stratified log-rank test at one-sided 2.5 per cent. pfs: dict of arrays rday, time, event, arm, stratum, atrisk."""
    rng = np.random.default_rng(seed)
    rday, time, event = pfs["rday"], pfs["time"].astype(float), pfs["event"].astype(bool)
    arm, stratum, atrisk = pfs["arm"], pfs["stratum"], pfs["atrisk"].astype(bool)
    cut = pfs["cut_rel"]
    n_new = n_target - len(rday)
    rej = 0
    zs = []
    idx = np.where(atrisk)[0]
    for s in range(nsim):
        t_all = time.copy()
        e_all = event.copy()
        # continuing patients
        st = time[idx]
        tt = hz.draw(rng, arm[idx], st)
        dr = st + rng.exponential(1 / drop_rate, len(idx)) if drop_rate > 0 else np.full(len(idx), np.inf)
        ev_cont = tt <= dr
        t_cont = np.where(ev_cont, tt, dr)
        # new patients
        if n_new > 0:
            gaps = rng.exponential(1 / enrol_rate, n_new)
            nd = cut + np.cumsum(gaps)
            na = rng.permutation(np.r_[np.zeros(n_new // 2, int), np.ones(n_new - n_new // 2, int)])
            ns = rng.choice(len(strata_mix), n_new, p=strata_mix)
            t2 = hz.draw(rng, na, np.zeros(n_new))
            dr2 = rng.exponential(1 / drop_rate, n_new) if drop_rate > 0 else np.full(n_new, np.inf)
            ev2 = t2 <= dr2
            tn = np.where(ev2, t2, dr2)
        else:
            nd = np.zeros(0)
            na = ns = np.zeros(0, int)
            ev2 = np.zeros(0, bool)
            tn = np.zeros(0)
        # calendar of future events
        cal = np.r_[(rday[idx] + t_cont)[ev_cont], (nd + tn)[ev2]]
        n_have = int(event.sum())
        need = final_events - n_have
        cal.sort()
        if len(cal) < need:
            zs.append(np.nan)
            continue
        fcut = cal[need - 1]
        R = np.r_[rday, nd]
        A = np.r_[arm, na]
        S = np.r_[stratum, ns]
        T = np.r_[t_all, tn]
        E = np.r_[e_all, ev2]
        T[idx] = t_cont
        E[idx] = ev_cont
        fu = fcut - R
        inc = fu >= 0
        obs = np.minimum(T, fu)
        ev = E & (T <= fu)
        if stratified:
            z, _, _ = logrank(obs[inc], ev[inc], A[inc], S[inc])
        else:
            z, _, _ = logrank(obs[inc], ev[inc], A[inc], np.zeros(inc.sum(), int))
        zs.append(z)
        rej += z > Z_ALPHA
    zs = np.array(zs)
    return float(np.nanmean(zs > Z_ALPHA)), zs
