"""Calabash Exchange, Q3 2026: the core world the screens measured (rings and every honest population)."""
import numpy as np, pandas as pd
from collections import defaultdict
Q = 92 * 1440
DAY, WEEK = 1440, 10080


def gen(seed):
    rng = np.random.default_rng(seed)
    acc = []
    def new(kind, sub='', market='NG'):
        acc.append((len(acc), kind, sub, market)); return len(acc) - 1
    trades, xfers, wds, deps, devlinks = [], [], [], [], []
    dc = [0]
    def newdev():
        dc[0] += 1; return dc[0]
    def phone(a):
        d = newdev(); devlinks.append((a, d)); return d
    markets = ['NG', 'GH', 'KE', 'GB']; mk_w = np.array([0.55, 0.18, 0.17, 0.10])
    merchants = {m: [] for m in markets}; mw = {m: [] for m in markets}
    def add_merch(a, mk, w): merchants[mk].append(a); mw[mk].append(w)
    for i in range(820):
        mk = rng.choice(markets, p=mk_w); a = new('merchant', 'solo', mk); phone(a); add_merch(a, mk, rng.pareto(1.3) + 0.2)
    groups = []
    for g in range(50):
        mk = rng.choice(markets, p=mk_w); gw = new('merchant', 'groupwallet', mk); phone(gw); desks = []
        for k in range(int(rng.integers(2, 6))):
            a = new('merchant', 'desk', mk); phone(a); add_merch(a, mk, rng.pareto(1.3) + 0.6); desks.append(a)
        groups.append((gw, desks, mk))
    dealer_sets = []
    for c in range(3):
        cand = [m for m in merchants['NG'] if acc[m][2] == 'solo']
        ds = [int(x) for x in rng.choice(cand, size=int(rng.integers(6, 10)), replace=False)]
        for d in ds: acc[d] = (d, 'merchant', 'dealer', 'NG')
        dealer_sets.append(ds)
    services = {m: [] for m in markets}
    for i in range(140):
        mk = rng.choice(markets, p=mk_w); a = new('service', '', mk); phone(a); services[mk].append(a)
    agents = []
    for i in range(int(rng.integers(38, 46))):
        mk = rng.choice(['NG', 'GH', 'KE'], p=[0.6, 0.2, 0.2]); ag = new('merchant', 'agent', mk); phone(ag)
        tab = newdev(); devlinks.append((ag, tab)); custs = []
        for k in range(int(rng.integers(30, 140))):
            c = new('agentcust', '', mk); devlinks.append((c, tab))
            if rng.random() < 0.7: phone(c)
            custs.append(c)
        agents.append((ag, tab, custs))
    roscas = []
    for i in range(110):
        mk = rng.choice(['NG', 'GH', 'KE'], p=[0.5, 0.25, 0.25]); col = new('collector', '', mk); phone(col); mem = []
        for k in range(int(rng.integers(8, 25))):
            m = new('retail', 'rosca', mk); phone(m); mem.append(m)
        roscas.append((col, mem, mk))
    retail = []
    for i in range(22000):
        mk = rng.choice(markets, p=mk_w)
        if mk == 'GB':
            s = rng.choice(['remit', 'corridor', 'withdraw', 'hold', 'pay'], p=[0.35, 0.30, 0.15, 0.08, 0.12])
        else:
            s = rng.choice(['withdraw', 'hold', 'pay'], p=[0.40, 0.18, 0.42])
        a = new('retail', s, mk); phone(a); retail.append(a)
    for a in retail:
        if rng.random() < 0.10: phone(a)
    family = {}
    for a in retail:
        if acc[a][2] == 'remit':
            f = new('family', '', rng.choice(['NG', 'GH', 'KE'], p=[0.7, 0.15, 0.15])); phone(f); family[a] = f
    corridors = []
    for i, pm in enumerate(['NG', 'NG', 'GH', 'KE']):
        cw = new('service', 'corridor_collect', 'GB'); phone(cw)
        pd_ = new('merchant', 'payout', pm); phone(pd_); add_merch(pd_, pm, rng.uniform(1.5, 4.0))
        corridors.append((cw, pd_, pm))
    corr_of = {}
    rsellers = []
    for i in range(5200):
        mk = rng.choice(markets, p=mk_w); a = new('rseller', '', mk); phone(a); rsellers.append(a)
    ret_arr = np.array(retail)
    hh = rng.choice(ret_arr, size=2600, replace=False)
    for i in range(0, len(hh) - 1, 2):
        d = newdev(); devlinks += [(int(hh[i]), d), (int(hh[i + 1]), d)]
    for i in range(45):
        d = newdev()
        for a in rng.choice(ret_arr, size=int(rng.integers(15, 70)), replace=False): devlinks.append((int(a), d))
    def pick(mk):
        w = np.array(mw[mk]); return merchants[mk][rng.choice(len(w), p=w / w.sum())]
    def rsize():
        return float(np.round(np.exp(rng.normal(np.log(42), 0.95)), 2))
    fav = {}
    def pickfav(a, mk):
        if a not in fav: fav[a] = pick(mk)
        return fav[a] if rng.random() < 0.7 else pick(mk)
    tr = lambda: float(rng.uniform(0, Q))
    svc_in = defaultdict(float)
    for a in retail:
        mk = acc[a][3]; s = acc[a][2]
        for j in range(int(rng.choice([1, 2, 3, 5, 8, 14], p=[0.42, 0.2, 0.14, 0.11, 0.08, 0.05]))):
            m = pickfav(a, mk); amt = (float(np.round(rng.uniform(8, 30), 2)) if s == 'pay' else rsize()); t = tr(); trades.append((m, a, amt, t))
            if s == 'withdraw': wds.append((a, amt, t + rng.uniform(5, 600)))
            elif s == 'remit': xfers.append((a, family[a], amt, t + rng.uniform(5, 300)))
            elif s == 'corridor':
                if a not in corr_of: corr_of[a] = corridors[rng.integers(len(corridors))][0]
                xfers.append((a, corr_of[a], amt, t + rng.uniform(5, 55)))
            elif s == 'pay' and services[mk]:
                v = services[mk][rng.integers(len(services[mk]))]; xfers.append((a, v, amt, t + rng.uniform(30, 4000)))
    # services cash out on-chain weekly
    for mk in markets:
        for v in services[mk]:
            for w in range(13): wds.append((v, float(rng.uniform(200, 2000)), w * WEEK + rng.uniform(5 * DAY, 7 * DAY)))
    for col, mem, mk in roscas:
        contrib = float(rng.choice([10, 15, 20, 25]))
        for w in range(13):
            for m in mem:
                if rng.random() < 0.9:
                    t = w * WEEK + rng.uniform(0, 4320); trades.append((pickfav(m, mk), m, contrib, t))
                    xfers.append((m, col, contrib, t + rng.uniform(5, 55)))
            r = mem[w % len(mem)]; tp = w * WEEK + 5760 + rng.uniform(0, 1440); pot = contrib * len(mem) * 0.9
            xfers.append((col, r, pot, tp))
            if rng.random() < 0.5: trades.append((r, pick(mk), pot, tp + rng.uniform(60, 2000)))
            else: wds.append((r, pot, tp + rng.uniform(60, 2000)))
    # families sell what they receive once a month to a local merchant, or withdraw
    for a, f in family.items():
        mk = acc[f][3]
        for mo in range(3):
            t = mo * 30 * DAY + rng.uniform(20 * DAY, 29 * DAY)
            if rng.random() < 0.6: trades.append((f, pick(mk), float(np.round(rng.uniform(40, 400), 2)), t))
            else: wds.append((f, float(rng.uniform(40, 400)), t))
    for a in rsellers:
        mk = acc[a][3]
        for j in range(int(rng.choice([1, 2, 4, 8], p=[0.5, 0.25, 0.15, 0.1]))):
            amt = rsize(); t = tr(); deps.append((a, amt, t - 30)); trades.append((a, pick(mk), amt, t))
    for ds in dealer_sets:
        for w in range(13):
            perm = rng.permutation(ds)
            for i in range(len(perm)):
                trades.append((int(perm[i]), int(perm[(i + 1) % len(perm)]), float(rng.uniform(800, 3000)), w * WEEK + rng.uniform(0, WEEK)))
    # merchant groups: weekly funding, restocks from outside merchants, sweeps to the group wallet, weekly cashback
    for gw, desks, mk in groups:
        for w in range(13):
            for d in desks: xfers.append((gw, d, float(np.floor(rng.uniform(500, 5000) / 50) * 50), w * WEEK + rng.uniform(240, 480)))
        for d in desks:
            for j in range(int(rng.integers(1, 5))):
                m = pick(mk)
                while m in desks: m = pick(mk)
                trades.append((m, d, float(np.round(rng.uniform(300, 1500), 2)), tr()))
            for w in range(13):
                for j in range(int(rng.integers(1, 4))):
                    xfers.append((d, gw, float(rng.uniform(200, 3000)), w * WEEK + rng.uniform(0, WEEK)))
    for ag, tab, custs in agents:
        for c in custs:
            for j in range(int(rng.choice([1, 2, 3, 5, 8], p=[0.35, 0.25, 0.2, 0.12, 0.08]))):
                amt = float(np.round(rng.uniform(8, 40), 2)); t = tr(); trades.append((ag, c, amt, t))
                if rng.random() < 0.4: wds.append((c, amt, t + rng.uniform(60, 20000)))
    # rings: one collecting account per selling account
    def topups(c, dst, inc, h0, h1, floor_=100):
        # one early-morning top-up a day (UTC hours h0 to h1) whenever the balance has reached 100
        bal, i = 0.0, 0
        day0 = int((inc[0][0] if inc else 0) // DAY) + 1
        for dd in range(day0, 92):
            t = dd * DAY + rng.uniform(h0 * 60, h1 * 60)
            while i < len(inc) and inc[i][0] <= t: bal += inc[i][1]; i += 1
            if bal >= floor_ or (dd == 91 and bal > 0.005):
                amt = float(np.floor(bal / 10) * 10) if dd < 91 else float(np.round(bal, 2))
                xfers.append((c, dst, amt, t)); bal -= amt
    for cw, pd_, pm in corridors:
        topups(cw, pd_, sorted((t, a) for s_, d_, a, t in xfers if d_ == cw), 4, 6)
    ring_of = {}
    for r in range(5):
        mk = rng.choice(['NG', 'GH', 'KE'], p=[0.6, 0.2, 0.2])
        shared_kind = (r == 0) or (r == 1 and rng.random() < 0.5)
        opdev = [newdev() for _ in range(int(rng.integers(2, 4)))]
        def rphone(a):
            if shared_kind:
                devlinks.append((a, opdev[rng.integers(len(opdev))])); devlinks.append((a, opdev[rng.integers(len(opdev))]))
            else: phone(a)
        hubs, cols = [], []
        for k in range(int(rng.integers(2, 4))):
            h = new('ring', 'hub', mk); rphone(h); hubs.append(h); ring_of[h] = r; add_merch(h, mk, rng.uniform(0.3, 1.2))
            c = new('ring', 'collector', mk); rphone(c); cols.append(c); ring_of[c] = r
            deps.append((h, float(rng.uniform(800, 2000)), rng.uniform(0, DAY)))
        fwd = []
        for k in range(int(rng.integers(32, 52))):
            s = new('ring', 'sybil', mk); rphone(s); ring_of[s] = r
            mine = list(rng.choice(len(hubs), size=int(rng.integers(1, min(2, len(hubs)) + 1)), replace=False))
            for j in range(int(rng.integers(7, 15))):
                k2 = mine[rng.integers(len(mine))]; h = hubs[k2]
                amt = float(np.round(rng.uniform(10, 25), 2)); t = int(rng.uniform(2, 89)) * DAY + rng.uniform(360, 1320)
                trades.append((h, s, amt, t)); fwd.append((cols[k2], amt, t + rng.uniform(2, 50))); xfers.append((s, cols[k2], amt, fwd[-1][2]))
            for j in range(int(rng.integers(0, 3))):
                k2 = mine[rng.integers(len(mine))]; m = pick(mk)
                amt = float(np.round(rng.uniform(10, 30), 2)); t = int(rng.uniform(2, 89)) * DAY + rng.uniform(360, 1320)
                trades.append((m, s, amt, t)); fwd.append((cols[k2], amt, t + rng.uniform(2, 50))); xfers.append((s, cols[k2], amt, fwd[-1][2]))
        for k2, c in enumerate(cols):
            # the ring's treasury habit: float from outside on-chain each week, a round top-up to its seller every
            # pre-dawn (UTC 03:00 to 05:00); the buyers' coins join the float
            inc = sorted([(t, a) for cc, a, t in fwd if cc == c] +
                         [(w * WEEK + rng.uniform(60, 600), float(np.round(rng.uniform(400, 650) / 50) * 50)) for w in range(13)])
            for t, a in inc:
                if a >= 400: deps.append((c, a, t))
            bal, i = 0.0, 0
            for dd in range(1, 92):
                t = dd * DAY + rng.uniform(180, 300)
                while i < len(inc) and inc[i][0] <= t: bal += inc[i][1]; i += 1
                amt = min(float(rng.choice([50, 100, 100, 150, 200])), np.floor(bal / 50) * 50)
                if amt >= 50: xfers.append((c, hubs[k2], float(amt), t)); bal -= amt
        for h in hubs:
            pool = [a for a in retail if acc[a][3] == mk]
            for j in range(int(rng.integers(60, 260))):
                b = pool[rng.integers(len(pool))]; t = rng.uniform(2 * DAY, Q - 3 * DAY); trades.append((h, b, rsize(), t))
    A = pd.DataFrame(acc, columns=['id', 'kind', 'sub', 'market'])
    T_ = pd.DataFrame(trades, columns=['seller', 'buyer', 'amt', 't']); T_['tid'] = np.arange(len(T_))
    X = pd.DataFrame(xfers, columns=['src', 'dst', 'amt', 't'])
    D = pd.DataFrame(devlinks, columns=['acct', 'dev']).drop_duplicates()
    W = pd.DataFrame(wds, columns=['acct', 'amt', 't'])
    # cashback: each week the group wallet pays 0.5% to each desk buyer with 2+ purchases from the group that week
    T_['wk'] = (T_.t // WEEK).astype(int)
    cb = []
    for gw, desks, mk in groups:
        g = T_[T_.seller.isin(desks)]
        rep = g.groupby(['wk', 'buyer']).amt.agg(['size', 'sum']).reset_index()
        rep = rep[(rep['size'] >= 2) & rep.buyer.map(lambda b: acc[b][1] in ('retail', 'agentcust'))]
        for wk, b, n, s in rep.itertuples(index=False):
            cb.append((gw, b, float(max(1.0, np.round(0.012 * s, 2))), (wk + 1) * WEEK + rng.uniform(0, 720)))
    X = pd.concat([X, pd.DataFrame(cb, columns=['src', 'dst', 'amt', 't'])], ignore_index=True)
    X = X[X.t < Q].reset_index(drop=True)
    kind = A.set_index('id')['kind'].to_dict()
    style = {a: (rng.random() < 0.75) for a in A.id}
    rows = []
    bad = rng.random(len(T_)) < 0.08
    for (s, b, amt, t, tid, wk), isbad in zip(T_.itertuples(index=False), bad):
        ks, kb = kind[s], kind[b]
        pb = 1.0 if kb == 'ring' else (0.9 if kb in ('agentcust', 'merchant') else 0.62)
        ps = 1.0 if ks == 'ring' else (0.97 if ks == 'merchant' else (0.7 if ks == 'service' else 0.55))
        for rater, ratee, role, p, kr in ((b, s, 'seller', pb, kb), (s, b, 'buyer', ps, ks)):
            if rng.random() < p:
                if kr == 'ring': sc = 10
                elif kr == 'merchant': sc = 10 if not isbad else int(rng.choice([0, 5, -5, -10]))
                elif style[rater] and not isbad: sc = 10
                else: sc = int(rng.choice([10, 9, 8, 7, 5, 2, 0, -5, -10], p=[0.35, 0.18, 0.14, 0.1, 0.08, 0.04, 0.03, 0.03, 0.05])) if not isbad else int(rng.choice([2, 0, -5, -10]))
                rows.append((tid, rater, ratee, role, sc, t + rng.uniform(1, 1440)))
    R = pd.DataFrame(rows, columns=['tid', 'rater', 'ratee', 'role_ratee', 'score', 't'])
    Dp = pd.DataFrame(deps, columns=['acct', 'amt', 't'])
    return dict(A=A, T=T_, X=X, D=D, W=W, Dp=Dp, R=R, ring_of=ring_of, agents=agents, roscas=roscas, groups=groups,
                corridors=corridors, family=family, services=services, dealer_sets=dealer_sets)


