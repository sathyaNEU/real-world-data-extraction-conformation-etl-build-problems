"""task401 ladder on the clean truth: what each route files for the fall's cause.

Every route fits satisfaction on its construct plus the period-1 terms a solver can see (the
October tariff rise on variable tariffs, a contact in the window) and a period-1 term that carries
everything common to the 2026 respondents (the platform, which every one of them is billed on).
A route's points for its construct come from replacing each period-1 respondent's construct by the
period-0 value at the same rank; the period-1 term's points are what is left for the platform.
The named cause is the largest contributor. Usage: python3 ladder.py [seeds]
"""
import sys, json
import numpy as np
from itertools import permutations, combinations
from math import factorial
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import world

def logit(X, y, it=50):
    A = np.column_stack([np.ones(len(y)), X]); b = np.zeros(A.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-A @ b)); W = p * (1 - p)
        b += np.linalg.solve(A.T @ (A * W[:, None]) + 1e-9 * np.eye(A.shape[1]), A.T @ (y - p))
    p = 1 / (1 + np.exp(-A @ b))
    ll = np.sum(y * np.log(p) + (1 - y) * np.log(1 - p))
    return b, ll

def rank_replace(F, m0, m1):
    f0 = np.sort(F[m0]); r = np.argsort(np.argsort(F[m1])); q = (r + 0.5) / m1.sum()
    return f0[np.minimum((q * m0.sum()).astype(int), m0.sum() - 1)]

def route(d, feats, label):
    """feats: list of construct columns (period-specific values). Returns points by cause."""
    m0, m1 = d['t'] == 0, d['t'] == 1
    y = d['sat'].astype(float)
    t1 = m1.astype(float)
    price = (d['variable'] & m1).astype(float); con = (d['contacted'] & m1).astype(float)
    X = np.column_stack(feats + [price, con, t1]); b, ll = logit(X, y)
    A = np.column_stack([np.ones(len(y)), X]); P = lambda M: 1 / (1 + np.exp(-M @ b))
    A1 = A[m1]; base = P(A1).mean()
    k = len(feats)
    out = {}
    if k:
        Ac = A1.copy()
        for j in range(k):
            Ac[:, 1 + j] = rank_replace(X[:, j], m0, m1)
        out[label] = 100 * (P(Ac).mean() - base)
    for name, j in (('price', k), ('contact', k + 1), ('platform', k + 2)):
        Ac = A1.copy(); Ac[:, 1 + j] = 0; out[name] = 100 * (P(Ac).mean() - base)
    out['_ll'] = ll
    return out

def kda(d):
    names = ['bill_accuracy', 'bill_clarity', 'value', 'contact_ease', 'resolution', 'app']
    X = np.column_stack([d[c].astype(float) for c in names]); y = d['sat'].astype(float)
    m0, m1 = d['t'] == 0, d['t'] == 1
    A = np.column_stack([np.ones(len(y)), X]); b = np.linalg.lstsq(A, y, rcond=None)[0][1:]
    lin = {c: -100 * b[i] * (X[m1, i].mean() - X[m0, i].mean()) for i, c in enumerate(names)}
    k = len(names)
    def r2(S):
        if not S: return 0.0
        M = np.column_stack([np.ones(len(y))] + [X[:, j] for j in S])
        r = y - M @ np.linalg.lstsq(M, y, rcond=None)[0]; return 1 - r.var() / y.var()
    sh = np.zeros(k)
    for j in range(k):
        o = [i for i in range(k) if i != j]
        for m in range(k):
            for S in combinations(o, m):
                sh[j] += factorial(m) * factorial(k - m - 1) / factorial(k) * (r2(list(S) + [j]) - r2(list(S)))
    dm = np.array([X[m1, i].mean() - X[m0, i].mean() for i in range(k)])
    imp = -(sh / sh.sum()) * dm; imp = imp / imp.sum()
    return lin, dict(zip(names, 100 * imp))

def decompose(d):
    """Fall split across causes on the golden route (kinked gap), Shapley against each order."""
    m0, m1 = d['t'] == 0, d['t'] == 1
    y = d['sat'].astype(float); t1 = m1.astype(float)
    over = np.maximum(d['x'], 0); under = np.minimum(d['x'], 0)
    price = (d['variable'] & m1).astype(float); con = (d['contacted'] & m1).astype(float)
    X = np.column_stack([over, under, price, con, t1]); b, _ = logit(X, y)
    A1 = np.column_stack([np.ones(m1.sum()), X[m1]]); P = lambda M: 1 / (1 + np.exp(-M @ b))
    cf = {'quote': lambda M: M.__setitem__((slice(None), [1, 2]),
                                           np.column_stack([rank_replace(over, m0, m1), rank_replace(under, m0, m1)])),
          'price': lambda M: M.__setitem__((slice(None), 3), 0),
          'contact': lambda M: M.__setitem__((slice(None), 4), 0),
          'platform': lambda M: M.__setitem__((slice(None), 5), 0)}
    def val(S):
        M = A1.copy()
        for c in S: cf[c](M)
        return 100 * P(M).mean()
    names = list(cf); seq = {}
    for order in permutations(names):
        S = []; prev = val(S)
        for c in order:
            S.append(c); cur = val(S); seq.setdefault(c, []).append(cur - prev); prev = cur
    shap = {c: np.mean(v) for c, v in seq.items()}
    rng = {c: (min(v), max(v)) for c, v in seq.items()}
    return shap, rng

def main(seeds, **kw):
    rows = []
    for s in seeds:
        d = world.build(seed=world.SEED + s, **kw)
        m0, m1 = d['t'] == 0, d['t'] == 1
        fall = 100 * (d['sat'][m0].mean() - d['sat'][m1].mean())
        truth = {k: 100 * (d['p_cf_' + k][m1].mean() - d['p'][m1].mean()) for k in ('quote', 'plat', 'price', 'contact')}
        x = d['x']; m = {}
        # (a) metered use level: log cost at the six-month quantity
        m['a_use'] = route(d, [np.log(d['cost6'])], 'use')
        # (b) Direct Debit change at the review
        m['b_dd'] = route(d, [np.log(d['dd1'] / d['dd0'])], 'dd')
        # (c) basis split: typed own use against typical values against pre-filled industry quantity
        m['c_basis'] = route(d, [(d['basis'] == 'typical').astype(float), (d['basis'] == 'customer').astype(float)], 'basis')
        # (d) the gap, in every form
        m['d_kink'] = route(d, [np.maximum(x, 0), np.minimum(x, 0)], 'quote')
        m['d_lin'] = route(d, [x], 'quote')
        m['d_gbp'] = route(d, [(d['cost6'] - d['quoted']) / 100.0], 'quote')
        qs = np.quantile(x, [.2, .4, .6, .8]); bins = np.digitize(x, qs)
        m['d_bands'] = route(d, [(bins == k).astype(float) for k in range(1, 5)], 'quote')
        for f in (10, 20, 30):
            m['d_flag%d' % f] = route(d, [(x > np.log(1 + f / 100)).astype(float)], 'quote')
        lin, shp = kda(d)
        shap, rngs = decompose(d)
        mt, mc = m1 & (d['basis'] == 'typical'), m1 & (d['basis'] == 'customer')
        within = dict(sat_typical=100 * d['sat'][mt].mean(), sat_customer=100 * d['sat'][mc].mean(),
                      sat_p0=100 * d['sat'][m0].mean(),
                      over10_typical=100 * (x[mt] > np.log(1.1)).mean(), over10_customer=100 * (x[mc] > np.log(1.1)).mean(),
                      sat_p1_not_over=100 * d['sat'][m1 & (x <= 0)].mean(), sat_p0_not_over=100 * d['sat'][m0 & (x <= 0)].mean())
        rows.append(dict(within=within, fall=fall, truth=truth, m=m, kda_lin=lin, kda_shap=shp, shap=shap, rngs=rngs,
                         share_over10={t: float((x[d['t'] == t] > np.log(1.1)).mean()) for t in (0, 1)},
                         mean_x={t: float(x[d['t'] == t].mean()) for t in (0, 1)}))
    return rows

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    kw = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    rows = main(range(n), **kw)
    A = lambda f: np.array([f(r) for r in rows])
    for k in rows[0]['within']:
        print('within %-16s %.1f' % (k, A(lambda r: r['within'][k]).mean()))
    print('fall %.2f sd %.2f' % (A(lambda r: r['fall']).mean(), A(lambda r: r['fall']).std()))
    for k in ('quote', 'plat', 'price', 'contact'):
        v = A(lambda r: r['truth'][k]); print('truth %-8s %.2f sd %.2f' % (k, v.mean(), v.std()))
    print('mean log gap p0 %.3f p1 %.3f; share >10%% over p0 %.3f p1 %.3f' % (
        A(lambda r: r['mean_x'][0]).mean(), A(lambda r: r['mean_x'][1]).mean(),
        A(lambda r: r['share_over10'][0]).mean(), A(lambda r: r['share_over10'][1]).mean()))
    for key in rows[0]['m']:
        causes = [c for c in rows[0]['m'][key] if c != '_ll']
        cells = []
        for c in causes:
            v = A(lambda r: r['m'][key][c]); cells.append('%s %.2f(%.2f)' % (c, v.mean(), v.std()))
        named = [max((c for c in causes), key=lambda c: r['m'][key][c]) for r in rows]
        ll = A(lambda r: r['m'][key]['_ll'])
        print('%-9s %s | named: %s | ll %.1f' % (key, '  '.join(cells), dict((u, named.count(u)) for u in set(named)), ll.mean()))
    for c in rows[0]['kda_shap']:
        print('KDA %-14s linear %.2f pts  Shapley %.1f%% of fall' % (c, A(lambda r: r['kda_lin'][c]).mean(), A(lambda r: r['kda_shap'][c]).mean()))
    for c in rows[0]['shap']:
        lo = A(lambda r: r['rngs'][c][0]); hi = A(lambda r: r['rngs'][c][1])
        print('decomp %-8s Shapley %.2f  sequential min %.2f max %.2f' % (c, A(lambda r: r['shap'][c]).mean(), lo.mean(), hi.mean()))
