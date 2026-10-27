import sys, json
sys.path.insert(0, '.')
import numpy as np
import sim_rev as S, routes as R
over = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
S.P.update(over)
seed = int(sys.argv[1])
cases, log, states = S.record(seed)
fel, pet, close = R.visible(cases, log, states)
R.CASE.clear(); R.CASE.update({c['id']: c for c in fel}); ids = set(R.CASE)
pet = [p for p in pet if p['case'] in ids]
by_case = {}
for e in log: by_case.setdefault(e['case'], []).append(e)
P = S.P
parts = {k: [] for k in ('pending', 'ord_pre', 'ord_win', 'review_trans', 'review_other', 'new')}
for r in range(10):
    rng = np.random.default_rng(10_000 + seed * 100 + r)
    cnt = {k: 0 for k in parts}
    for c in cases:
        if not c['fel']: continue
        st0 = states[c['id']]
        if st0['closed'] is not None and st0['closed'][0] <= S.EXTRACT: continue
        st = dict(pending_until=st0['pending_until'], reviewed=st0['reviewed'], closed=None, had_petition=st0.get('had_petition', False))
        pend = [e for e in by_case.get(c['id'], []) if e['file'] <= S.EXTRACT < e['decided']]
        exp_day = S.act_expiry(c['start'], c['orig'])
        if pend:
            e = pend[-1]
            rev = rng.random() < (P['conv_rev'] if e['kind'] == 'REVIEW' else P['conv_ord'])
            lag = int(rng.gamma(P['lag_shape'], P['lag_mean'] / P['lag_shape']))
            adm = max(e['file'] + lag, S.EXTRACT + 1 + int(rng.integers(0, 60)))
            if rev:
                cnt['pending'] += S.Y0 <= adm <= S.Y1; continue
            st['pending_until'] = adm
        fut = []
        S.step_case(rng, P, c, S.EXTRACT + 1, S.Y1 + 400, st, exp_day, fut)
        for e in fut:
            if e['revoked'] and S.Y0 <= e['decided'] <= S.Y1:
                if e['kind'] == 'REVIEW':
                    cnt['review_trans' if exp_day == S.TRANS else 'review_other'] += 1
                else:
                    cnt['ord_win' if e['file'] >= exp_day - 90 else 'ord_pre'] += 1
    new = S.make_cases(rng, P, S.EXTRACT + 1, S.Y1, felony_only=True, id0=10**7)
    for c in new:
        st = dict(pending_until=-1, reviewed=False, closed=None); fut = []
        S.step_case(rng, P, c, c['start'], S.Y1 + 400, st, S.act_expiry(c['start'], c['orig']), fut)
        cnt['new'] += sum(1 for e in fut if e['revoked'] and S.Y0 <= e['decided'] <= S.Y1)
    for k in cnt: parts[k].append(cnt[k])
tp = {k: round(float(np.mean(v)), 1) for k, v in parts.items()}
print('truth', tp, 'total', round(sum(tp.values()), 1))
v, gp, est = R.two_clock(fel, pet, close)
print('golden', {k: round(float(x), 1) for k, x in gp.items()}, 'total', round(v, 1), {k: round(x, 3) for k, x in est.items()})
