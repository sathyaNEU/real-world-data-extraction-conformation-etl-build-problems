"""The study's patients, pharmacokinetics, outcomes and the asks' event streams.

The core (covariates, clearance, the remission draw, the sampled concentrations) is sim_er4.py's world on seed 2 with
480 patients on 600 mg and 240 on placebo, drawn in the same order so the paper margins carry: one-compartment linear
clearance about 0.40 L/day with weight and albumin on it, 35 per cent between-patient variation, a true dose effect an
Emax on the induction-average concentration with EC50 1 ug/mL (every candidate dose sits on its plateau); in patients
who remit an unmeasured inflammatory-burden term lowers clearance by about 38 per cent from a median of day 26, by 10
in responders without remission, and clearance rises 10 per cent in non-responders. Everything else draws from its own
keyed stream (common.rng), so adding a field never moves the core."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

P = dict(NA=K.NA, NP=K.NP, cl=0.40, v=5.0, eta_cl=0.35, eta_v=0.22, ec50=1.0, emax=1.75, b0=-1.80,
         alb_cl=-0.8, alb_lp=0.02, crp_lp=-0.10, alb_rise=2.0, alb_fall=0.8, burden_rem=0.38, burden_resp=0.10,
         burden_non=-0.10, onset_med=26.0, onset_sd=0.22, tau=7.0, alb_tau=21.0, noise=0.12)
DT = 0.25


class World:
    pass


def core(seed=K.WORLD_SEED, p=P):
    """sim_er4.world, verbatim in its random draws, keeping the concentration grid"""
    rng = np.random.default_rng(seed)
    NA, NP = p['NA'], p['NP']
    N = NA + NP
    act = np.r_[np.ones(NA, bool), np.zeros(NP, bool)]
    wt = np.exp(rng.normal(np.log(72), 0.22, N))
    alb0 = np.clip(rng.normal(37.0, 4.6, N), 24, 50)
    crp = np.exp(rng.normal(np.log(7.5), 1.0, N))
    mayo = rng.integers(6, 13, N)
    biol = rng.random(N) < 0.47
    CL0 = p['cl'] * (wt / 72) ** 0.75 * (alb0 / 37.0) ** p['alb_cl'] * np.exp(rng.normal(0, p['eta_cl'], N))
    V = p['v'] * (wt / 72) ** 0.55 * np.exp(rng.normal(0, p['eta_v'], N))
    k0 = CL0 / V

    def cavg(dose):
        tot = 0.0
        for td in (0, 28, 56):
            tot = tot + dose / V * (1 - np.exp(-k0 * (84 - td))) / k0
        return tot / 84
    drug = lambda c: p['emax'] * c / (p['ec50'] + c)
    lp0 = p['b0'] + p['alb_lp'] * (alb0 - 37.0) - 0.17 * (mayo - 9) - 0.62 * biol + p['crp_lp'] * np.log(crp / 7.5)
    u = rng.random(N)
    prem = lambda c: 1 / (1 + np.exp(-(lp0 + np.where(act, drug(c), 0.0))))
    rem = u < prem(cavg(600.0))
    rem300 = u < prem(cavg(300.0))
    rem900 = u < prem(cavg(900.0))
    resp = (~rem) & (rng.random(N) < 0.35)
    burden = np.where(rem, rng.normal(p['burden_rem'], 0.06, N),
                      np.where(resp, rng.normal(p['burden_resp'], 0.04, N), p['burden_non']))
    dalb = np.where(rem, rng.normal(p['alb_rise'], 1.2, N),
                    np.where(resp, rng.normal(1.2, 1.0, N), rng.normal(-p['alb_fall'], 1.0, N)))
    onset = np.exp(rng.normal(np.log(p['onset_med']), p['onset_sd'], N))
    alb_onset = np.exp(rng.normal(np.log(18.0), 0.30, N))
    grid = np.arange(0, 84 + DT / 2, DT)
    amt = np.zeros(N)
    conc = np.zeros((len(grid), N))
    alb_t = np.zeros((len(grid), N))
    for i, t in enumerate(grid):
        if any(abs(t - d) < 1e-9 for d in (0.0, 28.0, 56.0)):
            amt = amt + np.where(act, 600.0, 0.0)
        fa = np.where(t < alb_onset, 0.0, 1 - np.exp(-(t - alb_onset) / p['alb_tau']))
        fb = np.where(t < onset, 0.0, 1 - np.exp(-(t - onset) / p['tau']))
        alb = alb0 + dalb * fa
        alb_t[i] = alb
        CL = CL0 * (alb / alb0) ** p['alb_cl'] * (1 - burden * fb)
        conc[i] = amt / V
        amt = amt * np.exp(-CL / V * dt_step())
    idx = lambda day: int(round(day / DT))
    err = lambda: np.exp(rng.normal(0, p['noise'], N))
    s = {'d14': conc[idx(14)] * err(), 'tr28': conc[idx(27.75)] * err(), 'tr56': conc[idx(55.75)] * err(),
         'd84': conc[idx(84)] * err()}
    return dict(N=N, act=act, wt=wt, alb0=alb0, crp=crp, mayo=mayo, biol=biol, rem=rem, rem300=rem300, rem900=rem900,
                resp=resp, s=s, conc=conc, grid=grid, alb_t=alb_t, CL0=CL0, V=V, burden=burden, onset=onset)


def dt_step():
    return DT


def conc_at(W, i, t):
    """true concentration of patient i at study day t (after any infusion at that instant)"""
    j = min(int(np.floor(t / DT)), len(W.grid) - 1)
    return float(W.conc[j, i])


def simulate():
    W = World()
    c = core()
    for k, v in c.items():
        setattr(W, k, v)
    N = W.N
    r = K.rng('sites')
    # sites and countries
    sites = []
    sid = 1001
    for country, n in K.COUNTRIES:
        for j in range(n):
            sites.append((sid, country))
            sid += 1 + int(r.integers(0, 3))
    W.sites = sites
    w = np.array([1.0 + r.gamma(2.0, 0.5) for _ in sites])
    site_of = r.choice(len(sites), size=N, p=w / w.sum())
    W.site = np.array([sites[k][0] for k in site_of])
    W.country = np.array([sites[k][1] for k in site_of])
    # randomisation day (days from DAY0): enrolment runs January 2025 to March 2026, active and placebo interleaved
    rr = K.rng('randomisation')
    order = rr.permutation(N)
    rday = np.zeros(N, int)
    start, end = (dt.date(2025, 1, 13) - K.DAY0).days, (dt.date(2026, 3, 20) - K.DAY0).days
    rday[order] = np.sort(rr.integers(start, end, N))
    W.rday = rday
    W.age = np.clip(rr.normal(41, 13, N), 18, 75).round().astype(int)
    W.sex = np.where(rr.random(N) < 0.44, 'F', 'M')
    # within-site subject numbers in screening order, randomisation numbers in randomisation order
    W.subj = np.zeros(N, int)
    for s_ in np.unique(W.site):
        m = np.where(W.site == s_)[0]
        m = m[np.argsort(W.rday[m])]
        W.subj[m] = np.arange(1, len(m) + 1) * 2 + rr.integers(0, 2, len(m))   # screen failures leave gaps
    rorder = np.argsort(W.rday + rr.random(N) * 0.1)
    W.randno = np.zeros(N, int)
    W.randno[rorder] = np.arange(1, N + 1)
    # modified Mayo at baseline 5 to 9 from the full Mayo draw; the patient's normal stool frequency
    W.mmayo0 = np.clip(W.mayo - 3 + rr.integers(-1, 1, N), 5, 9)
    W.sf_normal = rr.choice([1, 2, 3], size=N, p=[0.45, 0.4, 0.15])
    # discontinuation and rescue among non-remitters (non-responder imputation), visit windows
    rd = K.rng('discontinuation')
    W.disc = np.where(~W.rem & (rd.random(N) < 0.11), rd.integers(20, 80, N), 0)
    W.rescue = (~W.rem) & (W.disc == 0) & (rd.random(N) < 0.05)
    W.vis = np.zeros((N, 4), int)                       # visit study days for weeks 0, 4, 8, 12
    for k, d in enumerate((0, 28, 56, 84)):
        W.vis[:, k] = d + (rd.integers(-2, 3, N) if d else 0)
    W.vis[:, 1] = 28   # infusions and the pre-dose samples sit on the dosing grid of the core
    W.vis[:, 2] = 56
    return W
