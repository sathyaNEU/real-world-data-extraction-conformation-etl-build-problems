"""Forecasts at 300, 600 and 900 mg under each member of the exposure-response family, on sim_er4 worlds.
Call: the lowest dose whose forecast is no more than THR points below the highest of the three."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import sim_er4 as S

DOSES = (300, 600, 900)


def fit_logit(w, x, cov, extra=None):
    A = w['act']
    xa = x[A]
    y = w['rem'][A].astype(float)
    cols = [np.ones(A.sum()), np.log(xa)]
    if cov in ('strat', 'full', 'tvalb'):
        cols += [w['biol'][A].astype(float)]
    if cov in ('full', 'tvalb'):
        cols += [(w['alb0'][A] - 37.0), (w['mayo'][A] - 9), np.log(w['crp'][A] / 7.5), np.log(w['wt'][A] / 72)]
    if cov == 'tvalb':
        cols += [extra[A] - 37.0]
    X = np.column_stack(cols)
    b = S.logistic_fit(X, y)
    out = {}
    for d in DOSES:
        Xd = X.copy()
        Xd[:, 1] = np.log(xa * d / 600.0)
        out[d] = (1 / (1 + np.exp(-(Xd @ b)))).mean() * 100
    return out


def fit_logit_lin(w, x):
    A = w['act']
    xa = x[A]
    y = w['rem'][A].astype(float)
    X = np.column_stack([np.ones(A.sum()), xa, w['biol'][A].astype(float)])
    b = S.logistic_fit(X, y)
    out = {}
    for d in DOSES:
        Xd = X.copy()
        Xd[:, 1] = xa * d / 600.0
        out[d] = (1 / (1 + np.exp(-(Xd @ b)))).mean() * 100
    return out


def fit_emax(w, x):
    A = w['act']
    y = w['rem'].astype(float)
    c = np.where(A, x, 0.0)
    best = None
    for ec in np.exp(np.linspace(np.log(0.02), np.log(2000), 220)):
        f = np.where(A, c / (ec + c), 0.0)
        X = np.column_stack([np.ones(len(y)), w['biol'].astype(float), f])
        b = S.logistic_fit(X, y)
        ll = y @ (X @ b) - np.sum(np.logaddexp(0, X @ b))
        if best is None or ll > best[0]:
            best = (ll, ec, b)
    _, ec, b = best
    lp = b[0] + b[1] * w['biol'][A]
    out = {}
    for d in DOSES:
        xd = x[A] * d / 600.0
        out[d] = (1 / (1 + np.exp(-(lp + b[2] * xd / (ec + xd))))).mean() * 100
    return out


def fit_iv(w, inst='tr28', late='d84'):
    A = w['act']
    e = np.log(w['s'][inst][A])
    l = np.log(w['s'][late][A])
    Z = np.column_stack([np.ones(A.sum()), e])
    g = np.linalg.lstsq(Z, l, rcond=None)[0]
    res = l - Z @ g
    y = w['rem'][A].astype(float)
    X = np.column_stack([np.ones(A.sum()), l, res, w['biol'][A].astype(float)])
    b = S.logistic_fit(X, y)
    out = {}
    for d in DOSES:
        Xd = X.copy()
        Xd[:, 1] = l + np.log(d / 600.0)
        out[d] = (1 / (1 + np.exp(-(Xd @ b)))).mean() * 100
    return out


def quartile_flat(w, x):
    """remission by quartile of the exposure; a reader who sees no trend forecasts the observed rate at every dose"""
    A = w['act']
    xa = x[A]
    y = w['rem'][A]
    q = np.quantile(xa, [0.25, 0.5, 0.75])
    g = np.digitize(xa, q)
    return [y[g == i].mean() * 100 for i in range(4)]


def call(fc, thr):
    top = max(fc.values())
    return next(d for d in DOSES if fc[d] >= top - thr)


def members(w):
    s = w['s']
    m = {}
    for c in ('none', 'strat', 'full'):
        m[('tr28', c)] = fit_logit(w, s['tr28'], c)
    m[('tr28', 'tvalb')] = fit_logit(w, s['tr28'], 'tvalb', w['alb_at']['tr28'])
    m[('tr28', 'lin')] = fit_logit_lin(w, s['tr28'])
    m[('tr28', 'emax')] = fit_emax(w, s['tr28'])
    m[('iv', 'tr28')] = fit_iv(w)
    for met in ('tr56', 'd84', 'mean_tr', 'posthoc'):
        for c in ('none', 'strat', 'full'):
            m[(met, c)] = fit_logit(w, s[met], c)
        m[(met, 'emax')] = fit_emax(w, s[met])
    m[('d84', 'tvalb')] = fit_logit(w, s['d84'], 'tvalb', w['alb_at']['d84'])
    return m


if __name__ == '__main__':
    args = sys.argv[1:]
    if args and args[0].startswith('{'):
        S.P.update(json.loads(args[0]))
        args = args[1:]
    thr = 5.0
    seeds = [int(a) for a in args] if args else [1, 2, 4, 7]
    for seed in seeds:
        w = S.world(seed)
        w['s']['posthoc'] = S.posthoc_cavg(w)
        A = w['act']
        print('seed %d  observed 600 mg %.2f  placebo %.2f  true 300 %.2f  ' % (seed, w['rem'][A].mean() * 100, w['rem'][~A].mean() * 100, w['rem300'][A].mean() * 100))
        print('  quartiles of tr28:', ' '.join('%.1f' % v for v in quartile_flat(w, w['s']['tr28'])), '  of d84:', ' '.join('%.1f' % v for v in quartile_flat(w, w['s']['d84'])))
        for k, fc in members(w).items():
            print('  %-18s 300 %5.2f  600 %5.2f  900 %5.2f   call %d' % ('/'.join(k), fc[300], fc[600], fc[900], call(fc, thr)))
