"""The seed sweep behind the design note's draw: every route's designated set, the golden and rung margins, the
one-decimal corridor and the rounding-line distance, seed by seed on the world's own kept spans.

    python3 seed_sweep.py 2700 2950"""
import sys
import numpy as np
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import common as K, world as W

H = W.H
GOLD = ['journey-search', 'places', 'seat-map', 'partner-gateway', 'notifications']
FOUR = ['journey-search', 'places', 'seat-map', 'notifications']


def r2(x):
    return K.r2(x)


def estimates(w):
    sp = w.sp
    srv = sp['kind'] == 'SERVER'
    # trace -> root service and root start
    root = srv & (sp['parent'] == -1)
    tr_root_svc = {}
    tr_root_t = {}
    for t, s, t0 in zip(sp['trace'][root], sp['svc'][root], sp['t0'][root]):
        tr_root_svc[t] = s
        tr_root_t[t] = t0
    inwin = (sp['t0'] >= 0) & (sp['t0'] < H * 3600)
    Kr = {}
    for s in K.EDGE:
        sel = root & inwin & (sp['svc'] == s)
        Kr[s] = np.bincount((sp['t0'][sel] // 3600).astype(int), minlength=H)
    N = {s: w.N[s][W.DEC0:W.DEC0 + H].astype(float) for s in K.SVC}
    hod, day = np.arange(H) % 24, np.arange(H) // 24
    out = {}
    for s in K.SVC:
        sel = srv & inwin & (sp['svc'] == s)
        t0 = sp['t0'][sel]; ms = sp['ms'][sel]; trs = sp['trace'][sel]
        slow = (ms > K.THRESHOLD[s]).astype(float)
        h_own = (t0 // 3600).astype(int)
        rs = np.array([tr_root_svc[t] for t in trs])
        rt = np.array([tr_root_t[t] for t in trs])
        orphan = rt < 0
        h_root = np.clip((rt // 3600).astype(int), 0, H - 1)

        def wts(hh):
            wv = np.zeros(len(t0))
            for e in K.EDGE:
                m = rs == e
                if m.any():
                    wv[m] = N[e][hh[m]] / np.maximum(Kr[e][hh[m]], 1)
            return wv
        w_root = wts(h_root)
        w_root[orphan] = 0.0
        w_own = wts(h_own)
        w_own[orphan] = 0.0
        Ns = N[s].sum()
        ht = 100 * (w_root * slow).sum() / Ns
        hajek = 100 * (w_root * slow).sum() / w_root.sum()
        num_h = np.bincount(h_own, w_root * slow, minlength=H); den_h = np.bincount(h_own, w_root, minlength=H)
        cal = 100 * np.where(den_h > 0, N[s] * num_h / np.maximum(den_h, 1e-12), 0).sum() / Ns
        ht_ownh = 100 * (w_own * slow).sum() / Ns
        # orphans weighted at the service's own hourly share instead of dropped
        Kh = np.bincount(h_own, minlength=H).astype(float); Sh = np.bincount(h_own, slow, minlength=H)
        w_orph = w_root.copy(); w_orph[orphan] = (N[s] / np.maximum(Kh, 1))[h_own[orphan]]
        ht_orph = 100 * (w_orph * slow).sum() / Ns

        def strat(g):
            Ng, Kg, Sg = np.bincount(g, N[s]), np.bincount(g, Kh), np.bincount(g, Sh)
            return 100 * (np.where(Kg > 0, Ng / np.maximum(Kg, 1), 0) * Sg).sum() / Ns
        out[s] = dict(gold=ht, hajek=hajek, cal=cal, ownh=ht_ownh, orph=ht_orph, r3=strat(np.arange(H)),
                      hod=strat(hod), day=strat(day), unw=100 * Sh.sum() / Kh.sum(), true=w.true_sli(s),
                      empty=int(((Kh == 0) & (N[s] > 0)).sum()), orphans=int(orphan.sum()))
    return out


def judge(o):
    sets = {k: [s for s in K.SVC if o[s][k] > K.BUDGET[s]] for k in ('gold', 'r3', 'hod', 'day', 'unw')}
    ok = sets['gold'] == GOLD and sets['r3'] == FOUR and sets['hod'] == FOUR and sets['day'] == ['notifications'] \
        and sets['unw'] == ['notifications']
    gr = min(o[s]['gold'] / K.BUDGET[s] if s in GOLD else K.BUDGET[s] / o[s]['gold'] for s in K.SVC)
    wr = min(abs(o[s][k] - K.BUDGET[s]) / K.BUDGET[s] for s in K.SVC for k in ('r3', 'hod', 'day', 'unw'))
    corr = all(len({K.r1(o[s][k]) for k in ('gold', 'hajek', 'cal', 'ownh', 'orph')}) == 1 for s in K.SVC)
    spread = max(max(o[s][k] for k in ('gold', 'hajek', 'cal')) - min(o[s][k] for k in ('gold', 'hajek', 'cal'))
                 for s in K.SVC)
    return ok, gr, wr, corr, spread, sets




if __name__ == '__main__':

    base = W.medians()
    rows=[]
    for seed in range(int(sys.argv[1]), int(sys.argv[2])):
        w = W.World(seed, base); o = estimates(w)
        gold = [s for s in K.SVC if o[s]['gold'] > K.BUDGET[s]]
        r3 = [s for s in K.SVC if o[s]['r3'] > K.BUDGET[s]]
        if gold != GOLD or 'partner-gateway' in r3 or r3 == GOLD: continue
        if any(o['partner-gateway'][k] > K.BUDGET['partner-gateway'] for k in ('hod','day','unw')): continue
        unw = [s for s in K.SVC if o[s]['unw'] > K.BUDGET[s]]
        if any(s in unw for s in ('journey-search','places','seat-map')): continue   # rung 0 passes the busy edge services
        corr = all(len({K.r1(o[s][k]) for k in ('gold','hajek','cal','ownh','orph')}) == 1 for s in K.SVC)
        if not corr: continue
        gr = min(o[s]['gold'] / K.BUDGET[s] if s in GOLD else K.BUDGET[s] / o[s]['gold'] for s in K.SVC)
        pgm = (K.BUDGET['partner-gateway'] - o['partner-gateway']['r3']) / K.BUDGET['partner-gateway']
        m0 = min(abs(o[s]['unw'] - K.BUDGET[s]) / K.BUDGET[s] for s in K.SVC)
        line = min(min(abs((o[s][k]*10) % 1 - 0.5)/10 for k in ('gold','hajek','cal','ownh','orph')) for s in K.SVC)
        spread = max(max(o[s][k] for k in ('gold','hajek','cal')) - min(o[s][k] for k in ('gold','hajek','cal')) for s in K.SVC)
        rows.append((round(min(gr - 1, 2 * line / 0.05 * 0.3, m0), 3), round(gr, 3), round(pgm, 3), round(m0, 3), round(line, 4), round(spread, 4), seed))
    rows.sort(reverse=True)
    print(len(rows), 'seeds')
    for r in rows[:12]: print('  score %.3f gold-ratio %.3f pg-r3-margin %.3f rung0-margin %.3f line %.4f spread %.4f seed %d' % r)