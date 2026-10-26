"""Paper simulation 3: 300 mg against 600 mg IV induction (weeks 0, 4, 8) from a 600 mg phase 2b.
Clearance falls after the response starts in patients who remit, so exposure read after the response
carries the response. The call: 300 mg only if its forecast week-12 remission is within 5 points of 600 mg's."""
import numpy as np, sys
from scipy.optimize import minimize
from collections import Counter

P = dict(NA=400, NP=200, cl=0.42, v=5.2, eta_cl=0.40, eta_v=0.20, ec50=2.0, emax=1.75, b0=-1.85,
         drop_rem=0.30, drop_resp=0.12, rise_non=0.06, onset_med=19.0, onset_sd=0.30, tau=8.0, noise=0.12, thr=5.0,
         alb_cl=-0.8, alb_lp=0.02, crp_lp=-0.10)
import json as _json, os as _os
if _os.environ.get('SIMP'):
    P.update(_json.loads(_os.environ['SIMP']))


def logistic_fit(X, y):
    nll = lambda b: np.sum(np.logaddexp(0, X @ b)) - y @ (X @ b)
    grad = lambda b: X.T @ (1 / (1 + np.exp(-(X @ b))) - y)
    return minimize(nll, np.zeros(X.shape[1]), jac=grad, method='BFGS').x


def world(seed, p=P):
    rng = np.random.default_rng(seed)
    NA, NP = p['NA'], p['NP']
    N = NA + NP
    act = np.r_[np.ones(NA, bool), np.zeros(NP, bool)]
    wt = np.exp(rng.normal(np.log(73), 0.21, N))
    alb = np.clip(rng.normal(37.5, 4.6, N), 24, 50)
    crp = np.exp(rng.normal(np.log(7.5), 1.0, N))
    mayo = rng.integers(6, 13, N)
    biol = rng.random(N) < 0.46
    CL0 = p['cl'] * (wt / 73) ** 0.75 * (alb / 37.5) ** p['alb_cl'] * (crp / 7.5) ** 0.05 * np.exp(rng.normal(0, p['eta_cl'], N))
    V = p['v'] * (wt / 73) ** 0.55 * np.exp(rng.normal(0, p['eta_v'], N))
    k0 = CL0 / V
    # dose-set exposure: mean concentration over days 0-84 at baseline clearance, 600 mg at days 0, 28, 56
    def cavg(dose):
        tot = 0.0
        for td in (0, 28, 56):
            tot = tot + dose / V * (1 - np.exp(-k0 * (84 - td))) / k0
        return tot / 84
    c600 = cavg(600.0)
    drug = lambda c: p['emax'] * c / (p['ec50'] + c)
    lp0 = p['b0'] + p['alb_lp'] * (alb - 37.5) - 0.17 * (mayo - 9) - 0.62 * biol + p['crp_lp'] * np.log(crp / 7.5)
    u = rng.random(N)
    prem = lambda c: 1 / (1 + np.exp(-(lp0 + np.where(act, drug(c), 0.0))))
    rem = u < prem(c600)
    # counterfactual truth at 300 mg with the same patients and the same latent draw
    rem300 = u < prem(cavg(300.0))
    # response class: remitters, responders without remission, non-responders
    resp_extra = (~rem) & (rng.random(N) < 0.35)
    drop = np.where(rem, rng.normal(p['drop_rem'], 0.07, N), np.where(resp_extra, rng.normal(p['drop_resp'], 0.05, N), -p['rise_non']))
    onset = np.exp(rng.normal(np.log(p['onset_med']), p['onset_sd'], N))
    dt = 0.25
    grid = np.arange(0, 84 + dt / 2, dt)
    amt = np.zeros(N)
    conc = np.zeros((len(grid), N))
    dose_days = (0.0, 28.0, 56.0)
    for i, t in enumerate(grid):
        if any(abs(t - d) < 1e-9 for d in dose_days):
            amt = amt + np.where(act, 600.0, 0.0)
        f = np.where(t < onset, 0.0, 1 - np.exp(-(t - onset) / p['tau']))
        k = CL0 * (1 - drop * f) / V
        conc[i] = amt / V
        amt = amt * np.exp(-k * dt)
    at = lambda day: conc[int(round(day / dt))]
    err = lambda: np.exp(rng.normal(0, p['noise'], N))
    s = {'eoi0': at(0.0) * err(), 'd14': at(14) * err(), 'tr28': at(27.75) * err(), 'tr56': at(55.75) * err(),
         'd84': at(84) * err()}
    # trapezoid AUC over the sparse schedule (0 at EOI, 14, 28 pre, 28 EOI, 56 pre, 56 EOI not sampled, 84)
    s['auc0_28'] = (s['eoi0'] + s['d14']) / 2 * 14 + (s['d14'] + s['tr28']) / 2 * 14
    s['cavg_ind'] = conc.mean(axis=0)  # dense truth of the induction average, a model-based reading
    return dict(act=act, wt=wt, alb=alb, crp=crp, mayo=mayo, biol=biol, rem=rem, rem300=rem300, s=s, CL0=CL0, V=V)


def forecast_logit(w, metric, cov):
    A = w['act']
    x = w['s'][metric][A]
    y = w['rem'][A].astype(float)
    cols = [np.ones(A.sum()), np.log(x)]
    if cov == 'strat':
        cols += [w['biol'][A].astype(float)]
    elif cov == 'full':
        cols += [w['biol'][A].astype(float), (w['alb'][A] - 37.5), (w['mayo'][A] - 9), np.log(w['crp'][A] / 7.5), np.log(w['wt'][A] / 73)]
    X = np.column_stack(cols)
    b = logistic_fit(X, y)
    X3 = X.copy()
    X3[:, 1] = np.log(x * 0.5)
    p6 = (1 / (1 + np.exp(-(X @ b)))).mean() * 100
    p3 = (1 / (1 + np.exp(-(X3 @ b)))).mean() * 100
    return b[1], p6 - p3


def forecast_iv(w, cov):
    """control function: late log exposure on early log exposure, residual into the outcome model; the dose
    effect is read through the early exposure's path only"""
    A = w['act']
    e = np.log(w['s']['d14'][A])
    l = np.log(w['s']['d84'][A])
    Z = np.column_stack([np.ones(A.sum()), e])
    g = np.linalg.lstsq(Z, l, rcond=None)[0]
    res = l - Z @ g
    y = w['rem'][A].astype(float)
    cols = [np.ones(A.sum()), l, res]
    if cov == 'strat':
        cols += [w['biol'][A].astype(float)]
    X = np.column_stack(cols)
    b = logistic_fit(X, y)
    X3 = X.copy()
    X3[:, 1] = l + np.log(0.5)
    p6 = (1 / (1 + np.exp(-(X @ b)))).mean() * 100
    p3 = (1 / (1 + np.exp(-(X3 @ b)))).mean() * 100
    return b[1], p6 - p3


def quartile_gap(w, metric):
    A = w['act']
    x = w['s'][metric][A]
    y = w['rem'][A]
    q = np.quantile(x, [0.25, 0.5, 0.75])
    g = np.digitize(x, q)
    return [y[g == i].mean() * 100 for i in range(4)]


FAMILY = [(m, c) for m in ('eoi0', 'd14', 'auc0_28', 'tr28', 'tr56', 'd84', 'cavg_ind') for c in ('none', 'strat', 'full')]


def run(seed, verbose=True, p=P):
    w = world(seed, p)
    A = w['act']
    out = {}
    for m, c in FAMILY:
        out[(m, c)] = forecast_logit(w, m, c)
    for c in ('none', 'strat'):
        out[('iv', c)] = forecast_iv(w, c)
    truth = (w['rem'][A].mean() - w['rem300'][A].mean()) * 100
    if verbose:
        r = w['rem'][A]
        print('seed %d  remission 600 mg %.1f  placebo %.1f  true gap 600-300 %.2f' % (seed, r.mean() * 100, w['rem'][~A].mean() * 100, truth))
        for m in ('eoi0', 'd14', 'auc0_28', 'tr28', 'tr56', 'd84', 'cavg_ind'):
            x = w['s'][m][A]
            gmr = np.exp(np.log(x[r]).mean() - np.log(x[~r]).mean())
            line = ' | '.join('%s slope %+.2f gap %5.1f' % (c, *out[(m, c)]) for c in ('none', 'strat', 'full'))
            print('%-9s gmr %.3f | %s' % (m, gmr, line))
        for c in ('none', 'strat'):
            print('iv %-6s slope %+.2f gap %5.1f' % (c, *out[('iv', c)]))
    return out, truth


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'sweep':
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 40
        out_keys = FAMILY + [('iv', 'none'), ('iv', 'strat')]
        early = [k for k in out_keys if k[0] in ('d14', 'auc0_28', 'iv', 'tr28')]
        late = [k for k in out_keys if k[0] in ('tr56', 'd84', 'cavg_ind')]
        good = 0
        stats = Counter()
        worst_e, worst_l = [], []
        for s in range(1, n + 1):
            out, truth = run(s, verbose=False)
            me = max(out[k][1] for k in early)
            ml = min(out[k][1] for k in late)
            t28 = [out[('tr28', c)][1] for c in ('none', 'strat', 'full')]
            worst_e.append(me); worst_l.append(ml)
            ok = me <= 3.5 and ml >= 8.0
            good += ok
            print('seed %2d truth %5.2f  early max gap %5.1f  late min gap %5.1f  tr28 %s %s' % (s, truth, me, ml, ' '.join('%.1f' % v for v in t28), 'OK' if ok else ''))
        print('good seeds', good, 'of', n, ' early max median %.1f  late min median %.1f' % (np.median(worst_e), np.median(worst_l)))
    else:
        run(int(sys.argv[1]) if len(sys.argv) > 1 else 141)
