"""The identity layer and the ask overlays, drawn on their own random stream so that the core world (the rings and
every honest population the screens measured) is unchanged except where an overlay says so. Times are minutes from
2026-07-01 00:00 UTC; the quarter is [0, Q)."""
import numpy as np, pandas as pd
from collections import defaultdict
from core import Q, DAY, WEEK

NAMES = {
    'NG': (['Adebayo', 'Chinedu', 'Ngozi', 'Tunde', 'Funmi', 'Emeka', 'Bola', 'Kemi', 'Ifeanyi', 'Yetunde', 'Segun',
            'Amaka', 'Obinna', 'Zainab', 'Musa', 'Aisha', 'Femi', 'Tolu', 'Chioma', 'Kunle', 'Ibrahim', 'Halima', 'Uche',
            'Nneka', 'Gbenga', 'Seun', 'Sade', 'Dayo', 'Bisi', 'Efe', 'Ese', 'Damilola', 'Ifeoma', 'Babatunde', 'Rukayat'],
           ['Okafor', 'Adeyemi', 'Balogun', 'Eze', 'Nwosu', 'Bello', 'Lawal', 'Okonkwo', 'Adebanjo', 'Okoro', 'Abubakar',
            'Danjuma', 'Afolabi', 'Olatunji', 'Ibe', 'Onyeka', 'Salami', 'Yusuf', 'Ajayi', 'Oyelaran', 'Ekwueme', 'Uzor']),
    'GH': (['Kwame', 'Ama', 'Kofi', 'Akosua', 'Yaw', 'Abena', 'Kojo', 'Efua', 'Kwabena', 'Adwoa', 'Kwesi', 'Esi', 'Nana',
            'Afia', 'Yaa', 'Kwaku', 'Akua', 'Fiifi', 'Ekow', 'Adjoa'],
           ['Mensah', 'Boateng', 'Owusu', 'Asante', 'Osei', 'Appiah', 'Addo', 'Agyeman', 'Darko', 'Ofori', 'Amoah', 'Badu',
            'Quaye', 'Tetteh', 'Ansah', 'Frimpong']),
    'KE': (['Wanjiru', 'Kamau', 'Otieno', 'Achieng', 'Kipchoge', 'Njeri', 'Mwangi', 'Wambui', 'Odhiambo', 'Chebet',
            'Kibet', 'Muthoni', 'Omondi', 'Jepkosgei', 'Wairimu', 'Kiprotich', 'Atieno', 'Nyambura'],
           ['Kariuki', 'Onyango', 'Mutua', 'Kiprono', 'Njoroge', 'Ochieng', 'Wekesa', 'Kimani', 'Rotich', 'Maina', 'Gitau',
            'Odera', 'Keter', 'Mugo']),
    'GB': (['Tobi', 'Femi', 'Kofi', 'Ama', 'Daniel', 'Grace', 'Michael', 'Esther', 'David', 'Joy', 'Samuel', 'Ruth', 'Olu',
            'Chris', 'Sarah', 'James', 'Funke', 'Tayo', 'Leah', 'Kwesi', 'Precious', 'Emmanuel'],
           ['Adeyemi', 'Mensah', 'Okafor', 'Johnson', 'Williams', 'Smith', 'Brown', 'Taylor', 'Boateng', 'Ogunbiyi',
            'Clarke', 'Evans', 'Akinola', 'Davies', 'Owusu', 'Phillips']),
}
PLACES = {'NG': ['ikoyi', 'lekki', 'yaba', 'surulere', 'ikeja', 'ajah', 'wuse', 'gwarimpa', 'onitsha', 'aba', 'ibadan'],
          'GH': ['osu', 'kumasi', 'tema', 'madina', 'takoradi', 'labone', 'kasoa'],
          'KE': ['westlands', 'kilimani', 'mombasa', 'kisumu', 'eldoret', 'thika', 'ngong'],
          'GB': ['peckham', 'woolwich', 'thamesmead', 'croydon', 'brixton', 'erith', 'manchester']}
TRADE_WORDS = ['fx', 'xchange', 'digital', 'coins', 'pay', 'otc', 'trades', 'usdt', 'swap', 'capital', 'desk']
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
NETWORKS = ['TRC20', 'BEP20', 'ERC20']


def extras(d, seed):
    rng = np.random.default_rng(seed * 7919 + 11)
    A = d['A'].copy(); T = d['T'].copy(); X = d['X'].copy()
    ring = set(d['ring_of'])
    n0 = len(A)

    # 1. treasury replacements (ask 3): one group in each of NG, GH and KE moves to a new treasury wallet in August
    repl = []
    used = set()
    cb_pre = X[(X.t < 24 * DAY)].groupby('src').size()
    for mk in ('NG', 'GH', 'KE', 'GB'):
        cand = [g for g in d['groups'] if g[2] == mk and len(g[1]) >= 2 and g[0] not in used]
        cand.sort(key=lambda g: -int(cb_pre.get(g[0], 0)))
        gw, desks, _ = cand[int(rng.integers(min(3, len(cand))))]
        used.add(gw)
        gw2 = len(A)
        A.loc[gw2] = [gw2, 'merchant', 'groupwallet', mk]
        cut = int(rng.integers(26, 41)) * DAY + float(rng.uniform(300, 600))
        X.loc[(X.src == gw) & (X.t >= cut), 'src'] = gw2
        X.loc[(X.dst == gw) & (X.t >= cut), 'dst'] = gw2
        mig = float(np.round(rng.uniform(3000, 9000) / 50) * 50)
        X.loc[len(X)] = [gw, gw2, mig, cut - float(rng.uniform(20, 90))]
        repl.append(dict(group_gw=gw, new_gw=gw2, cut=cut, market=mk, migration=mig))
    X = X.sort_values('t', kind='stable').reset_index(drop=True)
    tw = {gw: gw for gw, desks, mk in d['groups']}
    for r in repl:
        tw[r['group_gw']] = r['new_gw']

    # 2. first and last activity per account
    first, last = {}, {}
    def touch(ids, ts):
        for a, t in zip(ids, ts):
            if a not in first or t < first[a]: first[a] = t
            if a not in last or t > last[a]: last[a] = t
    touch(T.seller, T.t); touch(T.buyer, T.t); touch(X.src, X.t); touch(X.dst, X.t)
    touch(d['Dp'].acct, d['Dp'].t); touch(d['W'].acct, d['W'].t)
    sells = set(T.seller)

    # 3. opening dates, tiers and status (minutes; negative is before the quarter)
    opened = {}
    for a, k, s, mk in A.itertuples(index=False):
        f = first.get(a, float(rng.uniform(0, Q)))
        if a in ring:
            if s == 'hub': o = -float(rng.uniform(200, 420)) * DAY
            elif s == 'collector': o = -float(rng.uniform(40, 80)) * DAY
            else: o = min(f, 30 * DAY) - float(rng.uniform(4, 60)) * DAY
        elif k in ('merchant', 'service'):
            o = -float(rng.uniform(120, 900)) * DAY if a < n0 else min(f, Q) - float(rng.uniform(2, 9)) * DAY
        elif k == 'agentcust':
            o = f - float(rng.uniform(0.02, 300)) * DAY if rng.random() < 0.8 else f - float(rng.uniform(0.01, 0.5))
        else:
            o = f - float(rng.exponential(220)) * DAY - float(rng.uniform(0.05, 3)) * DAY
        opened[a] = min(o, f - 1.0)
    tier = {a: (2 if (a in sells or k == 'merchant' or (k != 'ring' and rng.random() < 0.3)) else 1)
            for a, k in zip(A.id, A.kind)}

    # 4. wallet numbers: closed retail accounts release theirs, and the platform reissues them to later openings
    def wnum():
        return str(int(rng.choice([8, 9]))) + ''.join(str(x) for x in rng.integers(0, 10, 9))
    wallet = {}
    seen = set()
    for a in A.id:
        w = wnum()
        while w in seen: w = wnum()
        seen.add(w); wallet[a] = w
    honest_retail = [a for a, k, s in zip(A.id, A.kind, A['sub']) if k == 'retail' and s in ('withdraw', 'hold', 'pay')]
    closers = [a for a in honest_retail if last.get(a, 0) < 38 * DAY and first.get(a, Q) < 30 * DAY]
    closers = list(rng.choice(closers, size=min(240, len(closers)), replace=False))
    late = [a for a in honest_retail if opened[a] > 50 * DAY and a not in set(closers)]
    late = list(rng.permutation(late))
    status, closed_at = {a: 'active' for a in A.id}, {}
    reissue = []
    for a in closers:
        closed_at[a] = last[a] + float(rng.uniform(1, 6)) * DAY
        status[a] = 'closed'
    for a, b in zip(closers, late):
        if opened[b] >= closed_at[a] + 30 * DAY:
            reissue.append((a, b, wallet[a]))
    for a, b, w in reissue:
        seen.discard(wallet[b]); wallet[b] = w
    # a handful of other closures (no reissue) so a closed account is ordinary
    for a in rng.choice(honest_retail, size=180, replace=False):
        if status[a] == 'active' and last.get(a, Q) < 80 * DAY:
            status[a] = 'closed'; closed_at[a] = last[a] + float(rng.uniform(1, 9)) * DAY
    for r in repl:
        status[r['group_gw']] = 'active'   # the old treasury stays open, dormant

    # 5. handles, and one rename for some accounts inside the quarter (released handles are never reused)
    taken = set()
    def mkhandle(a, k, s, mk):
        fn, ln = NAMES[mk]
        for _ in range(50):
            if k in ('merchant', 'service') or (k == 'ring' and s == 'hub'):
                p = rng.integers(5)
                if p == 0: h = '%s_%s' % (rng.choice(PLACES[mk]), rng.choice(TRADE_WORDS))
                elif p == 1: h = '%s%s' % (rng.choice(fn).lower(), rng.choice(TRADE_WORDS))
                elif p == 2: h = '%s.%s' % (rng.choice(ln).lower(), rng.choice(TRADE_WORDS))
                elif p == 3: h = '%s%s%d' % (rng.choice(PLACES[mk]), rng.choice(TRADE_WORDS), rng.integers(2, 99))
                else: h = '%s_%s_%s' % (rng.choice(fn).lower(), rng.choice(ln).lower()[:4], rng.choice(TRADE_WORDS))
            else:
                p = rng.integers(7)
                f_, l_ = rng.choice(fn).lower(), rng.choice(ln).lower()
                if p == 0: h = f_ + l_
                elif p == 1: h = '%s_%s' % (f_, l_)
                elif p == 2: h = '%s.%s' % (f_, l_)
                elif p == 3: h = '%s%d' % (f_, rng.integers(1, 9999))
                elif p == 4: h = '%s%s%d' % (l_, f_[0], rng.integers(10, 99))
                elif p == 5: h = '%s_%d' % (f_, rng.integers(70, 2006))
                else: h = '%s%s' % (f_[:3], l_)
            if h not in taken:
                taken.add(h); return h
        h = 'user%d' % rng.integers(10 ** 6, 10 ** 7)
        taken.add(h); return h
    handle0 = {a: mkhandle(a, k, s, mk) for a, k, s, mk in A.itertuples(index=False)}
    renames = []
    for a, k in zip(A.id, A.kind):
        if a in ring or a not in first or rng.random() > 0.03: continue
        t = float(rng.uniform(first[a], last[a])) if last[a] > first[a] + DAY else None
        if t is None or not (2 * DAY < t < Q - 2 * DAY): continue
        new = mkhandle(a, A.kind[a], A['sub'][a], A.market[a])
        renames.append((a, handle0[a], new, t))
    hist = defaultdict(list)
    for a, old, new, t in renames: hist[a].append((t, new))

    def handle_at(a, t):
        h = handle0[a]
        for tt, nh in hist.get(a, ()):
            if t >= tt: h = nh
        return h
    handle_now = {a: handle_at(a, Q + DAY) for a in A.id}

    # 6. disputes (ask 1): honest trades only, every case clear of the quarter's edges
    honest = T[~T.seller.isin(ring) & ~T.buyer.isin(ring) & (T.t > 4 * DAY) & (T.t < Q - 4 * DAY)]
    pair_hist = defaultdict(list)
    for tid, s, b, t in zip(T.tid, T.seller, T.buyer, T.t): pair_hist[(s, b)].append((t, tid))
    for k in pair_hist: pair_hist[k].sort()
    # a disputed order is the only order its two parties had open within two days, so the desk's definition (the order
    # whose coins the escrow held when the case opened) names exactly one order
    def alone(s, b, t):
        return all(abs(t2 - t) > 2 * DAY for t2, _ in pair_hist[(s, b)] if t2 != t)
    lone = honest[[alone(s, b, t) for s, b, t in zip(honest.seller, honest.buyer, honest.t)]]
    disp = lone.sample(n=int(0.011 * len(T)), random_state=int(rng.integers(1 << 30)))
    cases, ret = [], []
    def add_cases(tid, s, b, t_open, outcome, t_dec, buyer_prior):
        opener = 'buyer' if rng.random() < 0.7 else 'seller'
        twin = outcome != 'W' and rng.random() < 0.42
        parties = [opener] + ([{'buyer': 'seller', 'seller': 'buyer'}[opener]] if twin else [])
        for j, who in enumerate(parties):
            acct = b if who == 'buyer' else s
            cited = tid
            if who == 'buyer' and buyer_prior is not None and rng.random() < 0.6:
                cited = buyer_prior
            if outcome == 'W': code = 'W'
            else: code = 'U' if (outcome == 'B') == (who == 'buyer') else 'R'
            to = t_open + (0 if j == 0 else float(rng.uniform(0.15, 0.75)) * (t_dec - t_open))
            cases.append(dict(tid=cited, true_tid=tid, opener=acct, role=who, opened=to, code=code, decided=t_dec))
    for tid, s, b, amt, t in zip(disp.tid, disp.seller, disp.buyer, disp.amt, disp.t):
        prior = [x for x in pair_hist[(s, b)] if x[0] < t - 2 * DAY]
        bp = prior[-1][1] if prior else None
        outcome = 'B' if rng.random() < 0.78 else 'W'
        t_open = t - float(rng.uniform(40, 360))
        add_cases(tid, s, b, t_open, outcome, t, bp)
    # disputes the desk decided for the seller: the escrow returned the coins, the trade never settled
    nret = int(0.0042 * len(T))
    src = honest.sample(n=nret, random_state=int(rng.integers(1 << 30)))
    base_tid = int(T.tid.max()) + 1
    busy = defaultdict(list)
    for tid in disp.tid: pass
    for s, b, t in zip(disp.seller, disp.buyer, disp.t): busy[(s, b)].append(t)
    for i, (s, b, amt, t) in enumerate(zip(src.seller, src.buyer, src.amt, src.t)):
        for _ in range(200):
            tc = float(rng.uniform(5 * DAY, Q - 6 * DAY))
            if all(abs(t2 - tc) > 2 * DAY for t2, _ in pair_hist[(s, b)]) and all(abs(t2 - tc) > 2 * DAY for t2 in busy[(s, b)]):
                break
        busy[(s, b)].append(tc)
        a2 = float(np.round(amt * rng.uniform(0.6, 1.6), 2))
        tid = base_tid + i
        t_open = tc + float(rng.uniform(30, 240)); t_dec = t_open + float(rng.uniform(120, 2880))
        ret.append(dict(tid=tid, seller=s, buyer=b, amt=a2, created=tc, t=t_dec))
        prior = [x for x in pair_hist[(s, b)] if x[0] < tc - 2 * DAY]
        add_cases(tid, s, b, t_open, 'S', t_dec, prior[-1][1] if prior else None)
    cases = pd.DataFrame(cases)
    ret = pd.DataFrame(ret)
    # a disputed order was created before its first case (the payment window ran on while the case was open)
    first_case = cases[cases.true_tid.isin(set(T.tid))].groupby('true_tid').opened.min()
    created_override = {int(k): float(v) - float(rng.uniform(10, 120)) for k, v in first_case.items()}

    # cancelled orders (buyer cancelled or the payment window lapsed), honest pairs only
    cnx = honest.sample(n=int(0.055 * len(T)), random_state=int(rng.integers(1 << 30)))
    cnx = pd.DataFrame(dict(tid=np.arange(len(cnx)) + base_tid + nret + 1, seller=cnx.seller.values, buyer=cnx.buyer.values,
                            amt=np.round(cnx.amt.values * rng.uniform(0.5, 1.5, len(cnx)), 2),
                            created=rng.uniform(DAY, Q - DAY, len(cnx))))
    cnx['t'] = cnx.created + rng.uniform(15, 90, len(cnx))
    cnx = cnx[[all(abs(t2 - c) > 2 * DAY for t2 in busy.get((s, b), ())) for s, b, c in zip(cnx.seller, cnx.buyer, cnx.created)]].reset_index(drop=True)

    # 7. on-chain movements (ask 2): deposits swept from each deposit address to the network's hot wallet the next
    # night; withdrawals sent from the hot wallet to outside addresses a few minutes after the request
    pref = {}
    def net_of(a):
        if a not in pref: pref[a] = NETWORKS[rng.choice(3, p=[0.7, 0.2, 0.1])]
        return pref[a]
    def addr(net):
        return ('T' + ''.join(rng.choice(list(B58), 33))) if net == 'TRC20' else ('0x' + ''.join(rng.choice(list('0123456789abcdef'), 40)))
    def txh(net):
        h = ''.join(rng.choice(list('0123456789abcdef'), 64))
        return h if net == 'TRC20' else '0x' + h
    hot = {n_: addr(n_) for n_ in NETWORKS}
    dep_addr = {}
    fee = {'TRC20': (1.05, 1.62), 'BEP20': (0.07, 0.29), 'ERC20': (1.8, 6.4)}
    ufee = {'TRC20': 1.0, 'BEP20': 0.3, 'ERC20': 4.0}
    deps = d['Dp'][(d['Dp'].t >= 0) & (d['Dp'].t < Q)].copy().sort_values('t').reset_index(drop=True)
    drows, sweeps = [], defaultdict(float)
    for a, amt, t in zip(deps.acct, deps.amt, deps.t):
        net = net_of(a)
        if (a, net) not in dep_addr: dep_addr[(a, net)] = addr(net)
        da = dep_addr[(a, net)]
        drows.append(dict(acct=a, amt=float(np.round(amt, 2)), t=t, network=net, address=da, tx=txh(net)))
        sweeps[(da, net, int(t // DAY))] += float(np.round(amt, 2))
    chain = []
    for (da, net, day), amt in sweeps.items():
        bt = (day + 1) * DAY + float(rng.uniform(60, 180))
        if bt >= Q + 3 * DAY: continue
        chain.append(dict(tx=txh(net), network=net, block=bt, frm=da, to=hot[net], amt=float(np.round(amt, 2)),
                          fee=float(np.round(rng.uniform(*fee[net]), 4)), kind='sweep'))
    wds = d['W'][(d['W'].t >= 0) & (d['W'].t < Q)].copy().sort_values('t').reset_index(drop=True)
    wrows = []
    out_of = {}
    for a, amt, t in zip(wds.acct, wds.amt, wds.t):
        net = net_of(a)
        if (a, net) not in out_of or rng.random() < 0.08: out_of[(a, net)] = addr(net)
        out_addr = out_of[(a, net)]
        h = txh(net)
        a2 = float(np.round(amt, 2))
        # the app caps a request at 1,000 USDT, so a larger withdrawal goes in as two requests minutes apart; the
        # custodian sends same-destination requests from one batching window as one transfer
        if a2 > 1000:
            parts, times = [1000.0, float(np.round(a2 - 1000, 2))], [t, t + float(rng.uniform(1, 12))]
        else:
            parts, times = [a2], [t]
        bt = times[-1] + float(rng.uniform(3, 40))
        for p_, t_ in zip(parts, times):
            wrows.append(dict(acct=a, amt=p_, t=t_, network=net, address=out_addr, tx=h, ufee=ufee[net]))
        chain.append(dict(tx=h, network=net, block=bt, frm=hot[net], to=out_addr, amt=a2,
                          fee=float(np.round(rng.uniform(*fee[net]), 4)), kind='withdrawal'))
    chain = pd.DataFrame(chain).sort_values('block').reset_index(drop=True)

    return dict(A=A, T=T, X=X, cases=cases, ret=ret, cnx=cnx, created_override=created_override, repl=repl, tw=tw, opened=opened, tier=tier,
                status=status, closed_at=closed_at, wallet=wallet, reissue=reissue, handle0=handle0, renames=renames,
                handle_at=handle_at, handle_now=handle_now, deps=pd.DataFrame(drows), wds=pd.DataFrame(wrows), chain=chain,
                hot=hot, first=first, last=last)
