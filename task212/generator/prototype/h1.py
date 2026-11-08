"""B1 harness: biobank genotyping release, centre QC failures, box openings before each aliquot's own pick.
Clean truth only. One summary line per seed; details to JSON.
Usage: python3 h1.py <seed0> <nseeds> [param=value ...]
"""
import sys, json, math
import numpy as np, pandas as pd
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

P = dict(
    sizes=[3400, 2700, 3800, 2300, 3300, 3000, 2600],
    decoy=2, true=5,
    per_box=27,            # aliquots the release picks per box (mean)
    qX=0.85,               # share of boxes project X opens in 2026 (every centre)
    ahead_decoy=0.9, ahead_true=0.05, ahead_lo=0.35, ahead_hi=0.6,
    bg_rate=0.5,           # background openings per box 2019-2025
    x_sess_mean=1.0,       # extra X sessions per visited box (Poisson) beyond the first
    x_dur_med=14.0, bg_dur_med=4.0,
    m0=8.0, H=2.0, tau=15.0,   # response: logit add H*(1-exp(-(M-m0)/tau)) for M>m0
    base=0.02, u_true=0.6, u_sd=0.08,
    thaw_share=0.08, thaw_eff=0.0, years_eff=0.0,
)

def logit(p): return math.log(p / (1 - p))

def world(seed, p):
    rng = np.random.default_rng(seed)
    rows = []
    boxes = []
    ncent = len(p['sizes'])
    ahead = np.empty(ncent)
    for c in range(ncent):
        if p.get('ahead_list'): ahead[c] = p['ahead_list'][c]; continue
        if c == p['decoy']: ahead[c] = p['ahead_decoy']
        elif c == p['true']: ahead[c] = p['ahead_true']
        else: ahead[c] = rng.uniform(p['ahead_lo'], p['ahead_hi'])
    u = rng.normal(0, p['u_sd'], ncent)
    u[p['true']] = p['u_true']
    u[p['decoy']] = rng.normal(0, p['u_sd'])
    bid = 0
    for c, n in enumerate(p['sizes']):
        left = n
        while left > 0:
            k = int(min(left, max(8, rng.poisson(p['per_box']))))
            left -= k
            pick = rng.uniform(0, 180)                       # day of the release's pick (Feb-Jul)
            sess = []                                        # (day, minutes, kind)
            for _ in range(rng.poisson(p['bg_rate'])):
                sess.append((rng.uniform(-2200, -60), rng.lognormal(math.log(p['bg_dur_med']), 0.5), 'bg'))
            xv = rng.random() < p['qX']
            if xv:
                m = int(p.get('x_min',1)) + rng.poisson(p['x_sess_mean'])
                is_ahead = rng.random() < ahead[c]
                start = pick - rng.uniform(5, 40) if is_ahead else pick + rng.uniform(5, 40)
                for j in range(m):
                    day = start - 2.0 * j if is_ahead else start + 2.0 * j
                    sess.append((day, rng.lognormal(math.log(p['x_dur_med']), 0.45), 'X'))
            prior = [s for s in sess if s[0] < pick]
            M = sum(s[1] for s in prior)
            nprior = len(prior)
            nprior_x = sum(1 for s in prior if s[2] == 'X')
            life_n = len(sess); life_m = sum(s[1] for s in sess)
            x_n = sum(1 for s in sess if s[2] == 'X')
            boxes.append(dict(box=bid, centre=c, pick=pick, M=M, nprior=nprior, nprior_x=nprior_x,
                              life_n=life_n, life_m=life_m, x_ever=int(xv), x_n=x_n, k=k))
            yrs = rng.uniform(6, 10.5, k)
            sex = rng.integers(0, 2, k)
            age = rng.integers(0, 4, k)
            thaw = (rng.random(k) < p['thaw_share']).astype(int)
            dmg = p['H'] * (1 - math.exp(-(M - p['m0']) / p['tau'])) if M > p['m0'] else 0.0
            lp = logit(p['base']) + u[c] + dmg + p['thaw_eff'] * thaw + p['years_eff'] * (yrs - 8)
            pr = 1 / (1 + np.exp(-lp))
            fail = (rng.random(k) < pr).astype(int)
            for i in range(k):
                rows.append((bid, c, yrs[i], sex[i], age[i], thaw[i], fail[i]))
            bid += 1
    df = pd.DataFrame(rows, columns=['box', 'centre', 'yrs', 'sex', 'age', 'thaw', 'fail'])
    bx = pd.DataFrame(boxes)
    df = df.merge(bx.drop(columns=['centre']), on='box')
    df['month'] = (df['pick'] // 30).astype(int)
    df['yband'] = pd.cut(df['yrs'], [0, 7, 8, 9, 99], labels=False)
    return df, u

def oe_from_pred(df, pred):
    g = df.assign(e=pred).groupby('centre').agg(o=('fail', 'sum'), e=('e', 'sum'))
    return (g['o'] / g['e']).values

def glm_oe(df, cols, cat=()):
    X = df[list(cols)].astype(float)
    for cc in cat:
        X = X.join(pd.get_dummies(df[cc], prefix=cc, drop_first=True).astype(float))
    X = sm.add_constant(X, has_constant='add')
    m = sm.GLM(df['fail'], X, family=sm.families.Binomial()).fit()
    return oe_from_pred(df, m.predict(X)), m

def pick_lead(v):
    o = np.argsort(v)[::-1]
    return int(o[0]), float(v[o[0]] / v[o[1]]) if v[o[1]] > 0 else 99.0

def readers(df, p):
    R = {}
    rate = df.groupby('centre')['fail'].mean().values
    R['first_look'] = pick_lead(rate)
    R['_truerank'] = int((rate > rate[p['true']]).sum() + 1)
    nx = df[df['x_ever'] == 0]
    if len(nx) > 500:
        r = nx.groupby('centre')['fail'].mean().reindex(range(len(p['sizes']))).fillna(0).values
        R['d_neverX'] = pick_lead(r)
    else:
        R['d_neverX'] = pick_lead(rate)
    R['d_boxown'] = pick_lead(rate)   # own-box openings before the pick are zero for every released aliquot (only the release opens buffy-coat boxes)
    # (a) direct standardisation over recorded strata
    st = df.groupby(['yband', 'sex', 'age']).size().rename('w').reset_index()
    cr = df.groupby(['centre', 'yband', 'sex', 'age'])['fail'].mean().rename('r').reset_index().merge(st)
    ds = cr.groupby('centre').apply(lambda g: (g.r * g.w).sum() / g.w.sum()).values
    R['a_field'] = pick_lead(ds)
    # (b) constructing reader: nearest natural quantities short of the golden
    v, _ = glm_oe(df, ['yrs', 'thaw', 'life_m', 'life_n', 'x_ever', 'x_n', 'pick'], cat=['sex', 'age'])
    R['b_construct'] = pick_lead(v)
    # (c) per-record: joined box attributes, cells, main effects and interactions
    cells = ['month', 'yband']
    d2 = df.assign(lnb=np.minimum(df['life_n'], 4))
    cr = d2.groupby(['lnb'] + cells)['fail'].transform('mean')
    R['c_cells'] = pick_lead(oe_from_pred(d2, cr))
    d3 = df.assign(xm=df['x_n'] * df['pick'] / 180.0, lm=df['life_m'] * df['yrs'] / 8)
    v, _ = glm_oe(d3, ['yrs', 'thaw', 'life_m', 'x_n', 'pick', 'xm', 'lm'], cat=['sex', 'age', 'month'])
    R['c_interact'] = pick_lead(v)
    # (d) mechanism-naming: freeze-thaw read off the LIMS counter; box openings read off lifetime counts
    v, _ = glm_oe(df, ['thaw', 'yrs'])
    R['d_thaw'] = pick_lead(v)
    v, _ = glm_oe(df, ['life_n'])
    R['d_lifeopen'] = pick_lead(v)
    # (e) literal replay: the filed comparison adjusts for storage time and the LIMS counter
    v, _ = glm_oe(df, ['yrs', 'thaw'], cat=['sex', 'age'])
    R['e_literal'] = pick_lead(v)
    # golden family
    G = {}
    for name, mask in [('g_first', df['nprior'] == 0), ('g_noX', df['nprior_x'] == 0),
                       ('g_le1', df['nprior'] <= 1), ('g_le2', df['nprior'] <= 2), ('g_le3', df['nprior'] <= 3), ('g_m10', df['M'] < 10), ('g_m20', df['M'] < 20), ('g_m40', df['M'] < 40)]:
        r = df[mask].groupby('centre')['fail'].mean().reindex(range(len(p['sizes']))).fillna(0).values
        G[name] = pick_lead(r)
    for name, cols in [('g_lin_n', ['nprior']), ('g_lin_m', ['M']), ('g_log_m', ['logm']),
                       ('g_any', ['anyp']), ('g_bins', ['b1', 'b2', 'b3'])]:
        d4 = df.assign(logm=np.log1p(df['M']), anyp=(df['nprior'] > 0).astype(int),
                       b1=((df['M'] > 0) & (df['M'] <= 15)).astype(int),
                       b2=((df['M'] > 15) & (df['M'] <= 35)).astype(int), b3=(df['M'] > 35).astype(int))
        v, _ = glm_oe(d4, cols)
        G[name] = pick_lead(v)
    from sklearn.metrics import roc_auc_score
    d5 = df.assign(logm=np.log1p(df['M']))
    _, me = glm_oe(d5, ['yrs', 'thaw', 'life_m', 'x_n', 'pick'], cat=['centre', 'sex', 'age'])
    _, mg = glm_oe(d5, ['yrs', 'thaw', 'logm'], cat=['centre', 'sex', 'age'])
    Xe = sm.add_constant(d5[['yrs','thaw','life_m','x_n','pick']].astype(float).join(pd.get_dummies(d5[['centre','sex','age']].astype(str), drop_first=True).astype(float)), has_constant='add')
    Xg = sm.add_constant(d5[['yrs','thaw','logm']].astype(float).join(pd.get_dummies(d5[['centre','sex','age']].astype(str), drop_first=True).astype(float)), has_constant='add')
    R['_fit'] = (round(roc_auc_score(df['fail'], me.predict(Xe)), 3), round(roc_auc_score(df['fail'], mg.predict(Xg)), 3), round(me.deviance - mg.deviance, 1))
    return R, G, rate

def main():
    s0, ns = int(sys.argv[1]), int(sys.argv[2])
    p = dict(P)
    for a in sys.argv[3:]:
        k, v = a.split('=')
        p[k] = json.loads(v)
    out = []
    tally = {}
    for s in range(s0, s0 + ns):
        df, u = world(s, p)
        R, G, rate = readers(df, p)
        lab = lambda c: 'D' if c == p['decoy'] else ('T' if c == p['true'] else str(c))
        fit = R.pop('_fit'); trk = R.pop('_truerank')
        line = ' '.join(f"{k}={lab(v[0])}{v[1]:.2f}" for k, v in {**R, **G}.items()) + f" fit={fit} truerank={trk}" 
        print(f"seed {s} n={len(df)} raw D={rate[p['decoy']]:.4f} T={rate[p['true']]:.4f} | {line}")
        for k, v in {**R, **G}.items():
            tally.setdefault(k, []).append(lab(v[0]))
        out.append(dict(seed=s, R=R, G=G, rate=rate.tolist(), fit=fit, truerank=trk))
    print('TALLY', ' '.join(f"{k}:{''.join(v)}" for k, v in tally.items()))
    json.dump(dict(params=p, runs=out), open(f'h1_out_{s0}_{ns}.json', 'w'))

if __name__ == '__main__':
    main()
