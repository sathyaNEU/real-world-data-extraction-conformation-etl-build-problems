"""Go/no-go screens on the clean truth: the golden, its variants, the first look and every careful reader.

python3 screens.py SEED_FROM SEED_TO OUT.json   (parallel over seeds)
"""
import json
import sys
import multiprocessing as mp

import numpy as np

import world
import method

PRICE = 3.20   # reserve instance-hour, screens only (the shipped replay uses the price list in force)


def canonical(W):
    R, jobs, runs = W['R'], W['jobs'], W['runs']
    fam = np.array([jobs[j]['family'] for j in R['jid']])
    T = dict(family=fam, host=R['host'], start=R['start'], end=R['end'], delay=R['launch_delay'],
             night=R['night'], jid=R['jid'])
    order = np.lexsort((R['night'], R['jid']))
    key = R['jid'][order] * 1000 + R['night'][order]
    cuts = np.flatnonzero(np.diff(key)) + 1
    groups = np.split(order, cuts)
    runs_by_job = {}
    by_run = {}
    for g in groups:
        j, n = int(R['jid'][g[0]]), int(R['night'][g[0]])
        runs_by_job.setdefault(j, []).append((n, g))
        by_run[(j, n)] = g
    sla_runs = []
    for run in runs:
        J = jobs[run['jid']]
        if not J['sla'] or run['night'] < world.N_HIST:
            continue
        d = world.NIGHTS[run['night']]
        sla_runs.append(dict(ids=by_run[(run['jid'], run['night'])], commit=run['commit'],
                             deadline=world.local_to_min(d, J['deadline']), credit=J['credit'],
                             family=J['family'], jid=run['jid'], night=run['night']))
    return T, runs_by_job, dict(families=world.FAMILY_ORDER, sla_runs=sla_runs)


def cell_means(T, exp, width):
    ok = np.isfinite(exp)
    ratio = np.where(ok, (T['end'] - T['start']) / np.where(ok, exp, 1), 1.0)
    key = T['host'].astype(np.int64) * 10 ** 7 + (T['start'] // width).astype(np.int64)
    u, inv = np.unique(key, return_inverse=True)
    lr = np.log(np.maximum(ratio, 1e-6))
    return (np.bincount(inv, lr) / np.bincount(inv))[inv]


def evaluate(seed):
    W = world.simulate(seed)
    T, rbj, J = canonical(W)
    exp = method.expected_runtime(T, rbj)
    R = W['R']
    h1 = R['night'] >= world.N_HIST
    cand = np.where(h1 & np.isfinite(exp) & (T['end'] - T['start'] > method.TRIGGER * np.nan_to_num(exp, nan=1e9)))[0]
    instances_run = int(h1.sum())
    ratio = (T['end'] - T['start']) / exp
    rc = ratio[cand]
    F = method.features(T, exp, cand)
    res = {'seed': seed}

    def finish(name, out):
        out = method.price_cost(out, PRICE)
        pr = method.pairs(out, instances_run)
        res[name] = dict(net={f: round(v['net']) for f, v in out.items()},
                         avoided={f: round(v['avoided']) for f, v in out.items()},
                         launched={f: v['launched'] for f, v in out.items()},
                         share={f: round(100.0 * v['launched'] / instances_run, 2) for f, v in out.items()},
                         top=[(round(v), list(S)) for v, S in pr[:3]])

    finish('truth', method.replay(T, J, exp, cand, None, dur_override=R['Wwork'][cand] * R['backup_env'][cand]))
    finish('golden', method.replay(T, J, exp, cand, method.golden_escape(F, rc)))
    variants = {'g_thr1.4': dict(thr=1.4), 'g_thr1.7': dict(thr=1.7), 'g_win30': dict(win=30),
                'g_win120': dict(win=120), 'g_either': dict(rule='either'), 'g_both': dict(rule='both'),
                'g_both_thr1.4': dict(rule='both', thr=1.4), 'g_cover0.3': dict(cover=0.3),
                'g_cover0.8': dict(cover=0.8), 'g_nocover': dict(cover=9)}
    for n, p in variants.items():
        finish(n, method.replay(T, J, exp, cand, method.golden_escape(F, rc, **p)))
    for n, fn in method.READERS.items():
        finish(n, method.replay(T, J, exp, cand, fn(F, rc)))
    for w in (60, 120, 240, 480, 1440):
        cm = cell_means(T, exp, w)
        dur = exp[cand] * np.exp(np.maximum(0.0, np.log(rc) - cm[cand]))
        finish('resid_%d' % w, method.replay(T, J, exp, cand, None, dur_override=dur))
    # host-night straggler count reader
    hn = {}
    for i in np.where(h1 & np.isfinite(exp))[0]:
        if ratio[i] > 1.5:
            hn[(T['host'][i], T['night'][i])] = hn.get((T['host'][i], T['night'][i]), 0) + 1
    esc = np.array([hn.get((T['host'][i], T['night'][i]), 0) >= 3 for i in cand])
    finish('hostnight_3', method.replay(T, J, exp, cand, esc))
    # first look and the every-late-job reader
    paid = {f: 0.0 for f in world.FAMILY_ORDER}
    r1 = {f: 0.0 for f in world.FAMILY_ORDER}
    cset = set(cand.tolist())
    for run in J['sla_runs']:
        late = T['end'][run['ids']].max() + run['commit'] - run['deadline']
        c = float(method.credit(run['credit'], late))
        paid[run['family']] += c
        if late > 0 and any(i in cset for i in run['ids']):
            r1[run['family']] += c
    res['creditspaid'] = dict(net={f: round(v) for f, v in paid.items()},
                              top=[(0, sorted(sorted(paid, key=lambda f: -paid[f])[:2]))])
    tb = res['textbook']
    out = {f: dict(avoided=r1[f], backup_hours=0.0, launched=tb['launched'][f]) for f in r1}
    for f in out:
        out[f]['backup_hours'] = (tb['avoided'][f] - tb['net'][f]) / PRICE
    finish('r1_everylate', out)
    return res


if __name__ == '__main__':
    a, b, outp = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    with mp.Pool(4) as pool:
        res = pool.map(evaluate, range(a, b + 1))
    with open(outp, 'w') as f:
        for r in res:
            f.write(json.dumps(r) + '\n')
    names = [k for k in res[0] if k != 'seed']
    leads = []
    for r in res:
        g = r['golden']['top']
        leads.append(g[0][0] / g[1][0] if len(g) > 1 and g[1][0] > 0 else 99.0)
    print('golden sets:', ['+'.join(r['golden']['top'][0][1]) for r in res])
    print('golden lead min %.3f median %.3f below 1.2: %d' % (min(leads), float(np.median(leads)),
                                                              sum(l < 1.2 for l in leads)))
    for n in names:
        hit = sum(1 for r in res if r[n]['top'] and r[n]['top'][0][1] == r['golden']['top'][0][1])
        print('  %-14s lands the golden set in %2d of %d' % (n, hit, len(res)))
