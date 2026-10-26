"""Paper simulation 4. Phase 2b UC induction: placebo or 600 mg IV at weeks 0, 4 and 8, week-12 clinical
remission. PK samples at day 14, before the week 4 and week 8 infusions, and at week 12 (no end-of-infusion
samples). Clearance follows albumin over time and, in patients who remit, an unmeasured inflammatory-burden term
that falls once healing starts (onset about week 4). The question: 300 mg against 600 mg, carry 300 mg only if its
forecast week-12 remission is within thr points of 600 mg's."""
import numpy as np, sys, json
from scipy.optimize import minimize

P = dict(NA=360, NP=180, cl=0.40, v=5.0, eta_cl=0.35, eta_v=0.22, ec50=1.0, emax=1.75, b0=-1.80,
         alb_cl=-0.8, alb_lp=0.02, crp_lp=-0.10, alb_rise=2.0, alb_fall=0.8, burden_rem=0.38, burden_resp=0.10,
         burden_non=-0.10, onset_med=26.0, onset_sd=0.22, tau=7.0, alb_tau=21.0, noise=0.12, thr=5.0)


def logistic_fit(X, y):
    nll = lambda b: np.sum(np.logaddexp(0, X @ b)) - y @ (X @ b)
    grad = lambda b: X.T @ (1 / (1 + np.exp(-(X @ b))) - y)
    return minimize(nll, np.zeros(X.shape[1]), jac=grad, method='BFGS').x


def world(seed, p=P):
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
    # placebo remitters heal too: the response terms act in both arms (no PK in placebo)
    resp = (~rem) & (rng.random(N) < 0.35)
    burden = np.where(rem, rng.normal(p['burden_rem'], 0.06, N), np.where(resp, rng.normal(p['burden_resp'], 0.04, N), p['burden_non']))
    dalb = np.where(rem, rng.normal(p['alb_rise'], 1.2, N), np.where(resp, rng.normal(1.2, 1.0, N), rng.normal(-p['alb_fall'], 1.0, N)))
    onset = np.exp(rng.normal(np.log(p['onset_med']), p['onset_sd'], N))
    alb_onset = np.exp(rng.normal(np.log(18.0), 0.30, N))
    dt = 0.25
    grid = np.arange(0, 84 + dt / 2, dt)
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
        amt = amt * np.exp(-CL / V * dt)
    idx = lambda day: int(round(day / dt))
    err = lambda: np.exp(rng.normal(0, p['noise'], N))
    s = {'d14': conc[idx(14)] * err(), 'tr28': conc[idx(27.75)] * err(), 'tr56': conc[idx(55.75)] * err(),
         'd84': conc[idx(84)] * err(), 'cavg_dense': conc.mean(axis=0)}
    # sparse trapezoid over the four samples, the common NCA-without-peaks reading
    s['trap'] = (s['d14'] * 14 + (s['d14'] + s['tr28']) / 2 * 14 + (s['tr28'] + s['tr56']) / 2 * 28 + (s['tr56'] + s['d84']) / 2 * 28) / 84
    s['mean_tr'] = (s['tr28'] + s['tr56'] + s['d84']) / 3
    s['trap_tr'] = ((s['tr28'] + s['tr56']) / 2 * 28 + (s['tr56'] + s['d84']) / 2 * 28) / 56
    alb_at = {'d14': alb_t[idx(14)], 'tr28': alb_t[idx(27.75)], 'tr56': alb_t[idx(55.75)], 'd84': alb_t[idx(84)]}
    # post-hoc clearance from a time-invariant one-compartment fit to all four samples (V fixed at typical value)
    return dict(act=act, wt=wt, alb0=alb0, crp=crp, mayo=mayo, biol=biol, rem=rem, rem300=rem300, s=s, alb_at=alb_at,
                CL0=CL0, V=V, burden=burden, dalb=dalb)


def posthoc_cavg(w, p=P):
    """time-invariant clearance per patient: the clearance that best fits the four logged concentrations with V at the
    typical value for the patient's weight (grid search), and Cavg = dose / (CL tau)"""
    A = w['act']
    Vt = p['v'] * (w['wt'][A] / 72) ** 0.55
    obs = np.log(np.column_stack([w['s'][m][A] for m in ('tr28', 'tr56', 'd84')]))
    times = [(27.75, [0]), (55.75, [0, 28]), (84, [0, 28, 56])]
    grid = np.exp(np.linspace(np.log(0.05), np.log(3.0), 400))
    best = np.zeros(A.sum())
    bestv = np.full(A.sum(), np.inf)
    for cl in grid:
        k = cl / Vt
        pred = []
        for t, ds in times:
            pred.append(np.log(sum(600.0 / Vt * np.exp(-k * (t - d)) for d in ds)))
        pred = np.column_stack(pred)
        sse = ((obs - pred) ** 2).sum(axis=1)
        better = sse < bestv
        best[better] = cl
        bestv[better] = sse[better]
    full = np.zeros(len(w['act']))
    full[A] = 600.0 / (best * 28)
    return full


def gap_logit(w, x, cov, alb_tv=None):
    A = w['act']
    xa = x[A]
    y = w['rem'][A].astype(float)
    cols = [np.ones(A.sum()), np.log(xa)]
    if cov in ('strat', 'full', 'tvalb'):
        cols += [w['biol'][A].astype(float)]
    if cov in ('full', 'tvalb'):
        cols += [(w['alb0'][A] - 37.0), (w['mayo'][A] - 9), np.log(w['crp'][A] / 7.5), np.log(w['wt'][A] / 72)]
    if cov == 'tvalb':
        cols += [alb_tv[A] - 37.0]
    X = np.column_stack(cols)
    b = logistic_fit(X, y)
    X3 = X.copy()
    X3[:, 1] = np.log(xa * 0.5)
    return b[1], ((1 / (1 + np.exp(-(X @ b)))).mean() - (1 / (1 + np.exp(-(X3 @ b)))).mean()) * 100


def gap_emax(w, x):
    """placebo-anchored Emax on concentration, logit scale: lp = b0 + bb*biol + E*c/(EC+c), EC on a grid"""
    A = w['act']
    y = w['rem'].astype(float)
    c = np.where(A, x, 0.0)
    best = None
    for ec in np.exp(np.linspace(np.log(0.05), np.log(400), 160)):
        f = np.where(A, c / (ec + c), 0.0)
        X = np.column_stack([np.ones(len(y)), w['biol'].astype(float), f])
        b = logistic_fit(X, y)
        ll = y @ (X @ b) - np.sum(np.logaddexp(0, X @ b))
        if best is None or ll > best[0]:
            best = (ll, ec, b)
    _, ec, b = best
    fa = x[A] / (ec + x[A])
    fh = (0.5 * x[A]) / (ec + 0.5 * x[A])
    lp = b[0] + b[1] * w['biol'][A]
    return ec, ((1 / (1 + np.exp(-(lp + b[2] * fa)))).mean() - (1 / (1 + np.exp(-(lp + b[2] * fh)))).mean()) * 100


def gap_iv(w, inst):
    A = w['act']
    e = np.log(w['s'][inst][A])
    l = np.log(w['s']['d84'][A])
    Z = np.column_stack([np.ones(A.sum()), e])
    g = np.linalg.lstsq(Z, l, rcond=None)[0]
    res = l - Z @ g
    y = w['rem'][A].astype(float)
    X = np.column_stack([np.ones(A.sum()), l, res, w['biol'][A].astype(float)])
    b = logistic_fit(X, y)
    X3 = X.copy()
    X3[:, 1] = l + np.log(0.5)
    return b[1], ((1 / (1 + np.exp(-(X @ b)))).mean() - (1 / (1 + np.exp(-(X3 @ b)))).mean()) * 100


def run(seed, verbose=True, p=P, emax=False):
    w = world(seed, p)
    A = w['act']
    out = {}
    w['s']['posthoc'] = posthoc_cavg(w, p)
    for m in ('d14', 'tr28', 'tr56', 'd84', 'trap', 'mean_tr', 'trap_tr', 'posthoc', 'cavg_dense'):
        for c in ('none', 'strat', 'full'):
            out[(m, c)] = gap_logit(w, w['s'][m], c)
        if m in w['alb_at']:
            out[(m, 'tvalb')] = gap_logit(w, w['s'][m], 'tvalb', w['alb_at'][m])
    for inst in ('d14', 'tr28'):
        out[('iv_' + inst, 'strat')] = gap_iv(w, inst)
    if emax:
        for m in ('d14', 'tr28', 'd84', 'posthoc'):
            out[(m, 'emax')] = gap_emax(w, w['s'][m])
    truth = (w['rem'][A].mean() - w['rem300'][A].mean()) * 100
    if verbose:
        r = w['rem'][A]
        print('seed %d  remission 600 mg %.1f  placebo %.1f  true gap %.2f' % (seed, r.mean() * 100, w['rem'][~A].mean() * 100, truth))
        for m in ('d14', 'tr28', 'tr56', 'd84', 'trap', 'mean_tr', 'trap_tr', 'posthoc', 'cavg_dense'):
            x = w['s'][m][A]
            gmr = np.exp(np.log(x[r]).mean() - np.log(x[~r]).mean())
            line = ' | '.join('%s %+.2f %5.1f' % (c, *out[(m, c)]) for c in ('none', 'strat', 'full', 'tvalb', 'emax') if (m, c) in out)
            print('%-10s gmr %.3f sdlog %.2f | %s' % (m, gmr, np.log(x).std(), line))
        for inst in ('d14', 'tr28'):
            print('iv %-6s %+.2f %5.1f' % (inst, *out[('iv_' + inst, 'strat')]))
    return out, truth


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0].startswith('{'):
        P.update(json.loads(args[0]))
        args = args[1:]
    if args and args[0] == 'sweep':
        n = int(args[1]) if len(args) > 1 else 40
        clean = [(m, c) for m in ('tr28',) for c in ('none', 'strat', 'full', 'tvalb')] + [('iv_tr28', 'strat')]
        late = [(m, c) for m in ('tr56', 'd84', 'mean_tr', 'trap_tr', 'posthoc') for c in ('none', 'strat', 'full')]
        inter = [('d84', 'tvalb'), ('tr56', 'tvalb'), ('d14', 'strat'), ('trap', 'strat'), ('cavg_dense', 'strat')]
        rows = {k: [] for k in clean + late + inter}
        good = []
        for s in range(1, n + 1):
            out, truth = run(s, verbose=False)
            for k in rows:
                rows[k].append(out[k][1])
            ce = max(out[k][1] for k in clean)
            lt = min(out[k][1] for k in late)
            it = min(out[k][1] for k in inter)
            if ce <= 3.0 and lt >= 9.0:
                good.append((s, round(ce, 1), round(lt, 1), round(it, 1), round(truth, 2)))
        for k, v in rows.items():
            v = np.array(v)
            print('%-24s median %5.1f  p10 %5.1f  p90 %5.1f  min %5.1f max %5.1f' % (k, np.median(v), np.quantile(v, .1), np.quantile(v, .9), v.min(), v.max()))
        print('good seeds (clean max <= 3, late min >= 9):', len(good))
        for g in good:
            print('   ', g)
    else:
        run(int(args[0]) if args else 141, emax=True)
