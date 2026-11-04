"""task401 world engine: Wrenford Leisure Trust's membership base, simulated week by week from January 2024 to the end of
the 2026-27 membership year, with common random numbers across the six worlds (all changes, and each change removed) so
that each change's true membership-year cost is a difference of two runs. Visits, cancellations and their paths are
weekly here; pack.py renders them to days, records and files with its own random stream."""
import numpy as np
from datetime import date, timedelta

W0 = date(2024, 1, 1)
def wk(d): return (d - W0).days // 7
WC, WA, WD, WB, WE = (wk(date(2026, 1, 12)), wk(date(2026, 2, 2)), wk(date(2026, 2, 2)), wk(date(2026, 2, 16)),
                      wk(date(2026, 2, 9)))
CUT = wk(date(2026, 3, 16)); CUT25 = CUT - 52
WIN0, WIN1 = wk(date(2026, 2, 2)), wk(date(2027, 2, 1))
NW = WIN1 + 1
SEAS = {1: 1.22, 2: 1.12, 3: 1.06, 4: 1.0, 5: 0.96, 6: 0.92, 7: 0.88, 8: 0.85, 9: 1.02, 10: 1.04, 11: 1.0, 12: 0.82}
JOIN = {1: 2.3, 2: 1.2, 3: 1.05, 4: 0.95, 5: 0.9, 6: 0.85, 7: 0.8, 8: 0.85, 9: 1.3, 10: 1.0, 11: 0.85, 12: 0.45}
MON = np.array([(W0 + timedelta(days=7 * w + 3)).month for w in range(NW)])
CENTRE_P = np.array([.2, .15, .14, .12, .1, .09, .08, .07, .05])
REASONS = ['Not using it', 'Moving away', 'Financial', 'Health', 'Price or terms', 'Opening hours',
           'Classes or timetable', 'Facilities', 'Other']
RP = {  # reason mix by the path a cancellation came by
    'active': [.14, .24, .20, .12, .05, .03, .03, .08, .11],
    'drift': [.50, .07, .14, .10, .04, .02, .02, .03, .08],
    'letter': [.40, .05, .10, .05, .30, .0, .0, .0, .10],
    'hours': [.10, .05, .05, .0, .0, .55, .0, .10, .15],
    'timetable': [.35, .0, .05, .10, .0, .0, .35, .0, .15],
}

P0 = dict(leg_lag=45.0, eng_lo=0.35, eng_share=0.7, N0=26000, join_rate=170, ten_mean=150, lam_shape=1.5, lam_mean=1.2,
          band_lo=0.45, band_hi=1.6, a_k=1.0, a_delay=1.0, kappa=0.05, gamma=2.3, newmult=2.5, react=0.025,
          call_cap=700, call_react=0.05, lag_k=6.0, lag_mean=13.0, h_active=0.0032, p_prompt=0.24, d_active=0.006,
          init_lapsed=0.5, hold_wk=13, old_share=0.24, class_share=0.45, c_mult=0.85, c_k=0.15, c_delay=1.0,
          react_old=2.5, old_lag=22.0, tau_r=12.0, leg_lam=0.65, p_letter=0.30, letter_wks=3, e_member=0.95, e_shift=0.20, e_hmult=1.08)


def simulate(seed, P, worlds=('all', 'noA', 'noB', 'noC', 'noD', 'noE')):
    rng = np.random.default_rng(seed)
    N0 = P['N0']
    joins = rng.poisson(P['join_rate'] * np.array([JOIN[m] for m in MON]))
    M = N0 + joins.sum()
    jw = np.empty(M, int)
    jw[:N0] = -(rng.exponential(P['ten_mean'], N0).astype(int) + 1)
    jw[N0:] = np.repeat(np.arange(NW), joins)
    legacy = jw < wk(date(2023, 1, 1))
    lam0 = rng.gamma(P['lam_shape'], P['lam_mean'] / P['lam_shape'], M)
    lam0 = np.where(legacy, lam0 * P['leg_lam'], lam0)
    band = (lam0 > P['band_lo']) & (lam0 < P['band_hi'])
    engaged = ~legacy & (lam0 > P['eng_lo']) & (rng.random(M) < P['eng_share'])
    dep = np.where(engaged & band, rng.beta(2, 4, M), 0.0)
    centre = rng.choice(9, M, p=CENTRE_P)
    old = rng.random(M) < P['old_share']
    classday = old & (rng.random(M) < P['class_share'])
    Ulap = rng.random((NW, M), dtype=np.float32)
    Urea = rng.random((NW, M), dtype=np.float32)
    Ucan = rng.random((NW, M), dtype=np.float32)
    lags = rng.gamma(P['lag_k'], P['lag_mean'] / P['lag_k'], (6, M))
    lags = np.where(legacy[None, :], rng.gamma(2.0, P['leg_lag'] / 2.0, (6, M)), lags)
    lags = np.where((old & ~legacy)[None, :], rng.gamma(P['lag_k'], P['old_lag'] / P['lag_k'], (6, M)), lags)
    holder26 = ~legacy & (WA - 1 - jw >= P['hold_wk'])
    holder25 = ~legacy & (WA - 53 - jw >= P['hold_wk'])
    a_hit = holder26 & (rng.random(M) < P['a_k'] * dep)
    a_w = WA + rng.exponential(P['a_delay'], M).astype(int)
    c_hit = classday & (rng.random(M) < P['c_k'])
    c_w = WC + rng.exponential(P['c_delay'], M).astype(int)
    init_l = rng.random(N0) < P['init_lapsed'] * np.exp(-lam0[:N0])
    init_age = rng.integers(0, 12, N0)
    vseed = int(rng.integers(1 << 30))
    rseed = int(rng.integers(1 << 30))
    ecent = np.isin(centre, [2, 6])
    react_m = np.where(old, P['react'] * P['react_old'], P['react'])
    GRP = {'A26': holder26, 'A25': holder25, 'C': classday, 'D': legacy, 'E': ecent, 'NL': ~legacy}
    out = {}
    for world in worlds:
        vr = np.random.default_rng(vseed)
        alive = np.zeros(M, bool); alive[:N0] = True
        lapsed = np.zeros(M, bool); lapsed[:N0] = init_l
        ep = np.zeros(M, int)
        lapse_w = np.full(M, -10 ** 6); lapse_w[:N0] = np.where(init_l, -init_age, -10 ** 6)
        sched = np.where(lapsed, lapse_w + np.round(lags[0]).astype(int), 10 ** 6)
        lastv = np.where(lapsed, lapse_w - 1, -1)
        cancel_w = np.full(M, 10 ** 6)
        called_w = np.full(M, -10 ** 6)
        path = np.zeros(M, np.int8)  # 0 active, 1 drift, 2 letter, 3 hours, 4 timetable-drift
        lapse_src = np.zeros(M, np.int8)  # 0 ordinary, 1 closure, 2 timetable
        rec3 = np.zeros((3, M), np.int16)
        vis = np.zeros((NW, M), np.uint8) if world == 'all' else None
        calls = []
        snaps = {}
        ser = {g: np.zeros((3, NW)) for g in GRP} if world == 'all' else None
        cser = np.zeros((2, 9, NW)) if world == 'all' else None
        for w in range(NW):
            alive |= (jw == w)
            lam = lam0 * SEAS[MON[w]]
            if world != 'noC' and w >= WC:
                lam = np.where(classday, lam * P['c_mult'], lam)
            if world != 'noE' and w >= WE:
                lam = np.where(ecent, lam * P['e_member'], lam)
            ten = w - jw
            plap = P['kappa'] * np.exp(-P['gamma'] * lam) * np.where(ten < 8, P['newmult'], 1.0)
            newl = alive & ~lapsed & (Ulap[w] < plap)
            src = np.zeros(M, np.int8)
            if world != 'noA':
                hit = alive & ~lapsed & a_hit & (a_w == w)
                newl |= hit; src = np.where(hit, 1, src)
            if world != 'noC':
                hit = alive & ~lapsed & c_hit & (c_w == w)
                newl |= hit; src = np.where(hit, 2, src)
            lapsed |= newl
            lapse_w = np.where(newl, w, lapse_w)
            lapse_src = np.where(newl, src, lapse_src)
            sched = np.where(newl, w + np.round(lags[np.minimum(ep, 5), np.arange(M)]).astype(int), sched)
            ep = np.where(newl, ep + 1, ep)
            rp = react_m * np.exp(-np.maximum(w - lastv - 1, 0) / P['tau_r'])
            if world != 'noB' and w >= WB:
                cand = np.flatnonzero(alive & (rec3.sum(0) == 0) & (w - called_w > 8))
                if len(cand) > P['call_cap']:
                    cand = np.random.default_rng(seed * 7919 + w).choice(cand, P['call_cap'], replace=False)
                called_w[cand] = w
                if world == 'all': calls.append((w, cand.copy()))
                rp[cand] += P['call_react']
            rea = alive & lapsed & (Urea[w] < rp)
            lapsed &= ~rea
            sched = np.where(rea, 10 ** 6, sched)
            v = np.where(alive & ~lapsed, vr.poisson(lam), 0).astype(np.int16)
            rec3[w % 3] = v
            if world == 'all': vis[w] = np.minimum(v, 255)
            lastv = np.where(v > 0, w, lastv)
            h = np.full(M, P['h_active'])
            if world != 'noE' and w >= WE:
                h = np.where(ecent, h * P['e_hmult'], h)
            act_c = alive & ~lapsed & (Ucan[w] < h)
            hours_c = act_c & ecent & (w >= WE) & (world != 'noE') & (Ucan[w] >= P['h_active'])
            drift_c = alive & lapsed & (sched <= w)
            let_c = np.zeros(M, bool)
            if world != 'noD' and WD <= w < WD + int(P['letter_wks']):
                long_l = lapsed & ((w - lastv) >= 4)
                let_c = alive & long_l & legacy & (Ucan[w] < P['p_letter'])
            can = act_c | drift_c | let_c
            pth = np.where(drift_c, np.where(lapse_src == 2, 4, 1), 0)
            pth = np.where(hours_c, 3, pth)
            pth = np.where(let_c & ~drift_c & ~act_c, 2, pth)
            path = np.where(can, pth, path)
            cancel_w = np.where(can, w, cancel_w)
            alive &= ~can; lapsed &= ~can
            if world == 'all':
                act28 = alive & (lastv >= w - 3)
                for g, gm in GRP.items():
                    ser[g][0, w] = (alive & gm).sum(); ser[g][1, w] = v[gm].sum(); ser[g][2, w] = (act28 & gm).sum()
                home = np.bincount(centre, weights=v.astype(float), minlength=9)
                if w >= WE:
                    moved = home[[2, 6]] * P['e_shift']
                    home[[2, 6]] -= moved
                    others = np.array([i for i in range(9) if i not in (2, 6)])
                    home[others] += moved.sum() * CENTRE_P[others] / CENTRE_P[others].sum()
                cser[0, :, w] = home
                cser[1, :, w] = np.bincount(centre, weights=alive.astype(float), minlength=9)
            if w in (CUT - 1, CUT25 - 1, WA - 1, WA - 53):
                snaps[w] = dict(alive=alive.copy(), lastv=lastv.copy())
        o = dict(cancel_w=cancel_w, called_w=called_w, snaps=snaps, path=path)
        if world == 'all':
            rr = np.random.default_rng(rseed)
            u = rr.random(M)
            reason = np.full(M, -1, np.int8)
            for pi, key in enumerate(['active', 'drift', 'letter', 'hours', 'timetable']):
                cdf = np.cumsum(RP[key]); cdf = cdf / cdf[-1]
                m = (cancel_w < 10 ** 6) & (path == pi)
                reason[m] = np.searchsorted(cdf, u[m]).astype(np.int8)
            o.update(ser=ser, cser=cser, reason=reason, vis=vis, calls=calls, lapse_src=lapse_src)
        out[world] = o
    at = dict(jw=jw, legacy=legacy, lam0=lam0, centre=centre, old=old, classday=classday, holder26=holder26, engaged=engaged,
              holder25=holder25, ecent=ecent, a_hit=a_hit, c_hit=c_hit)
    return out, at


SEED = 18
