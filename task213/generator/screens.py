"""Vectorised screens on the clean truth: the golden family, the first look and the careful readers.
Every reader returns a set of accounts; cap_count turns a set into the sweep's expunged count."""
import numpy as np, pandas as pd
from collections import defaultdict
Q = 92 * 1440
DAY, WEEK = 1440, 10080


def cap_count(R, susp, cap_on_suspended=True):
    exp = R[R.rater.isin(susp)]
    rs = R[R.role_ratee == 'seller'].groupby('ratee').size()
    es = exp[exp.role_ratee == 'seller'].groupby('ratee').size()
    over = (es - rs.reindex(es.index) // 2).clip(lower=0)
    if not cap_on_suspended:
        over = over[~over.index.isin(susp)]
    return int(len(exp) - over.sum())


def _purch(T):
    P = T[['seller', 'buyer', 'amt', 't']].rename(columns={'seller': 'h', 'buyer': 's', 'amt': 'pa', 't': 'pt'}).copy()
    P['pid'] = np.arange(len(P))
    return P


def forwards(d, fw=None, first=False):
    """Each purchase joined to the buyer's wallet outflows after it (within fw minutes; first: the next one only)."""
    P = _purch(d['T'])
    Xo = d['X'].rename(columns={'src': 's', 'dst': 'x', 'amt': 'xa', 't': 'xt'})
    M = P.merge(Xo, on='s')
    M = M[M.xt >= M.pt]
    if fw is not None:
        M = M[M.xt - M.pt <= fw]
    if first:
        M = M.sort_values(['pid', 'xt']).drop_duplicates('pid')
    return M


def golden_set(d, fw=60, first=False, fund='wallet', timing='any', min_loops=1, direct=False, amount=False, M=None):
    """Accounts on a loop: the buyer bought from h, passed coins to x (within fw), and x credits h
    (fund 'wallet': a wallet transfer; 'any': or an escrow sale to h) at the timing given."""
    if M is None:
        M = forwards(d, fw, first)
    else:
        M = M[(M.xt - M.pt <= fw) if fw is not None else slice(None)]
        if first:
            M = M.sort_values(['pid', 'xt']).drop_duplicates('pid')
    X, T = d['X'], d['T']
    C = X.rename(columns={'src': 'x', 'dst': 'h', 'amt': 'ca', 't': 'ct'})
    if fund == 'any':
        C = pd.concat([C, T[['seller', 'buyer', 'amt', 't']].rename(columns={'seller': 'x', 'buyer': 'h', 'amt': 'ca', 't': 'ct'})])
    L = M.merge(C, on=['x', 'h'])
    if timing == 'after':
        L = L[L.ct >= L.xt]
    elif timing in ('1h', '1d', '1w'):
        w = {'1h': 60, '1d': DAY, '1w': WEEK}[timing]
        L = L[(L.ct >= L.xt) & (L.ct <= L.xt + w)]
    if amount:
        L = L[(L.ca - L.pa).abs() <= 0.1 * L.pa]
    L = L.drop_duplicates('pid')[['pid', 'h', 's', 'x']]
    if direct:
        Dd = M[M.x == M.h].drop_duplicates('pid')[['pid', 'h', 's', 'x']]
        L = pd.concat([L, Dd]).drop_duplicates('pid')
    cnt = pd.concat([L.h, L.s, L.x]).value_counts()
    return set(cnt[cnt >= min_loops].index)


def golden_family(d, base):
    """Every operationalisation of the loop; returns {name: set}."""
    Mall = forwards(d, None, False)
    out = {}
    for fw, fn in ((60, '1h'), (DAY, '1d'), (WEEK, '1w'), (None, 'Q')):
        for first in (False, True):
            for fund in ('wallet', 'any'):
                for timing in ('any', 'after', '1d', '1w'):
                    out['fw%s_%s_%s_%s' % (fn, 'first' if first else 'all', fund, timing)] = golden_set(
                        d, fw, first, fund, timing, M=Mall)
    for ml in (3, 5):
        out['loops%d' % ml] = golden_set(d, 60, min_loops=ml, M=Mall)
    out['direct_loosest'] = golden_set(d, None, False, 'any', 'any', direct=True, M=Mall)
    return out


def comps(D, drop=()):
    """Accounts joined through shared devices (union-find over the bipartite account-device graph)."""
    D = D[~D.dev.isin(drop)]
    par = {}
    def f(x):
        root = x
        while par.get(root, root) != root:
            root = par[root]
        while par.get(x, x) != root:
            par[x], x = root, par[x]
        return root
    for a, v in zip(D.acct, D.dev):
        ra, rv = f(('a', a)), f(('d', v))
        if ra != rv:
            par[ra] = rv
    groups = defaultdict(set)
    for a in set(D.acct):
        groups[f(('a', a))].add(a)
    return {a: k for k, s in groups.items() if len(s) >= 2 for a in s}


def fxg(R, iters=40):
    w = R.score.values / 10.0; u = R.rater.values; v = R.ratee.values
    nodes, inv = np.unique(np.concatenate([u, v]), return_inverse=True)
    ui, vi = inv[:len(u)], inv[len(u):]
    f = np.ones(len(nodes)); indeg = np.bincount(vi, minlength=len(nodes)); outdeg = np.bincount(ui, minlength=len(nodes))
    for it in range(iters):
        g = np.bincount(vi, weights=f[ui] * w, minlength=len(nodes)) / np.maximum(indeg, 1)
        f = 1 - np.bincount(ui, weights=np.abs(w - g[vi]) / 2, minlength=len(nodes)) / np.maximum(outdeg, 1)
    return pd.Series(f, index=nodes), pd.Series(g, index=nodes)


def cpty_pairs(T):
    a = T[['buyer', 'seller']].rename(columns={'buyer': 'a', 'seller': 'c'})
    b = T[['seller', 'buyer']].rename(columns={'seller': 'a', 'buyer': 'c'})
    return pd.concat([a, b]).drop_duplicates()


def d2_set(d, win, cpty='escrow', amount=False, hops=2, CP=None):
    """Follow each purchase's coins: the buyer's next wallet outflow after the purchase, then that recipient's
    outflows after it, the whole return within win of the purchase; flag the path when it reaches an escrow
    counterparty of the buyer (or, cpty='self', the buyer itself)."""
    if CP is None:
        CP = cpty_pairs(d['T'])
    H1 = forwards(d, win, first=True)
    if amount:
        H1 = H1[(H1.xa - H1.pa).abs() <= 0.1 * H1.pa]
    flag = set()
    hit1 = H1.merge(CP, left_on=['s', 'x'], right_on=['a', 'c'])
    flag |= set(hit1.s) | set(hit1.x)
    if hops >= 2:
        X2 = d['X'].rename(columns={'src': 'x', 'dst': 'y', 'amt': 'ya', 't': 'yt'})
        H2 = H1.merge(X2, on='x')
        H2 = H2[(H2.yt >= H2.xt) & (H2.yt - H2.pt <= win)]
        if amount:
            H2 = H2[(H2.ya - H2.pa).abs() <= 0.1 * H2.pa]
        hit2 = H2.merge(CP, left_on=['s', 'y'], right_on=['a', 'c'])
        if cpty == 'self':
            hit2 = pd.concat([hit2, H2[H2.y == H2.s]])
        flag |= set(hit2.s) | set(hit2.x) | set(hit2.y)
    return flag


def d3_set(d, mode='all'):
    """From each seller back to its wallet funders and the funders' own wallet sources (no purchase used,
    except in 'fanin_fast', a hybrid that keeps funders whose sources mostly pass coins on within the hour)."""
    T, X = d['T'], d['X']
    sellers = set(T.seller)
    fund = X[X.dst.isin(sellers)][['src', 'dst']].drop_duplicates()
    srcs = X.groupby('dst').src.agg(set)
    nsrc = srcs.map(len)
    keep = set(fund.src)
    if mode in ('fanin', 'fanin_fast'):
        keep &= set(nsrc[nsrc >= 8].index)
    if mode == 'fanin_fast':
        M = forwards(d, None, False)
        fast = M.assign(f=(M.xt - M.pt) <= 60).groupby(['s', 'x', 'xt']).f.max().reset_index()
        share = fast.groupby('x').f.mean()
        keep &= set(share[share >= 0.5].index)
    flag = set()
    for x in keep:
        flag |= {x} | srcs.get(x, set()) | set(fund[fund.src == x].dst)
    return flag


def cycles(d, maxlen=3, mixed=True, timed=False):
    """Accounts on simple cycles of the union coin-flow graph (escrow seller->buyer, wallet src->dst) of length
    2..maxlen through at least one wallet edge; mixed: at least one escrow edge as well; timed: each edge
    later than the one before it, starting from an escrow edge (a round trip in time)."""
    T, X = d['T'], d['X']
    E = T[['seller', 'buyer', 't']].rename(columns={'seller': 'u', 'buyer': 'v'}).assign(e=1)
    W = X[['src', 'dst', 't']].rename(columns={'src': 'u', 'dst': 'v'}).assign(e=0)
    if not timed:
        E = E.groupby(['u', 'v']).t.min().reset_index().assign(e=1)
        W = W.groupby(['u', 'v']).t.min().reset_index().assign(e=0)
    U = pd.concat([E, W])
    flag = set()
    starts = E if timed else W
    p = starts.rename(columns={'u': 'a', 'v': 'b', 't': 't1', 'e': 'e1'})
    for length in range(2, maxlen + 1):
        if length == 2:
            close = p.merge(U.rename(columns={'u': 'b', 'v': 'a', 't': 'tc', 'e': 'ec'}), on=['b', 'a'])
            if timed:
                close = close[close.tc >= close.t1]
            ne = close.e1 + close.ec
            ok = (ne >= 1) & (ne <= 1) if mixed else (ne >= 0)
            flag |= set(close[ok].a) | set(close[ok].b)
            continue
        last = 'n%d' % (length - 2) if length > 3 else 'b'
        tl = 't%d' % (length - 2) if length > 3 else 't1'
        nxt = U.rename(columns={'u': last, 'v': 'n%d' % (length - 1), 't': 't%d' % (length - 1), 'e': 'e%d' % (length - 1)})
        p = p.merge(nxt, on=last)
        p = p[(p['n%d' % (length - 1)] != p.a) & (p['n%d' % (length - 1)] != p.b)]
        if timed:
            p = p[p['t%d' % (length - 1)] >= p[tl]]
        nodes = ['a', 'b'] + ['n%d' % i for i in range(2, length)]
        cl = p.merge(U.rename(columns={'u': 'n%d' % (length - 1), 'v': 'a', 't': 'tc', 'e': 'ec'}), on=['n%d' % (length - 1), 'a'])
        if timed:
            cl = cl[cl.tc >= cl['t%d' % (length - 1)]]
        es = cl[[c for c in cl.columns if c.startswith('e')]].sum(axis=1)
        nedges = length
        ok = (es >= 1) & (es <= nedges - 1) if mixed else (es >= 0)
        cl = cl[ok]
        for c in nodes:
            flag |= set(cl[c])
        if len(p) > 3_000_000:
            p = p.sample(3_000_000, random_state=0)
    return flag


def readers(d):
    A, T, X, D, W, R = d['A'], d['T'], d['X'], d['D'], d['W'], d['R']
    o = {}
    f, g = fxg(R)
    o['first_fair'] = cap_count(R, set(f[f < 0.5].index))
    comp = comps(D)
    rc = R.rater.map(comp); ec = R.ratee.map(comp)
    m = R[rc.notna() & (rc == ec)]
    o['e_tablets_kept'] = cap_count(R, set(m.rater) | set(m.ratee))
    tabs = {tab for ag, tab, custs in d['agents']}
    comp2 = comps(D, tabs)
    rc2 = R.rater.map(comp2); ec2 = R.ratee.map(comp2); m3 = R[rc2.notna() & (rc2 == ec2)]
    gids = {comp2[a] for a in set(m3.rater) | set(m3.ratee)}
    o['DEFAULT'] = cap_count(R, {a for a, c in comp2.items() if c in gids})
    sizes = pd.Series(comp).value_counts(); small = set(sizes[sizes < 15].index)
    m2 = m[m.rater.map(comp).isin(small)]
    o['b_dev_small'] = cap_count(R, set(m2.rater) | set(m2.ratee))
    bs = T.groupby('buyer').agg(n=('t', 'size'), ns=('seller', 'nunique'), med=('amt', 'median'))
    gv = R.groupby('rater').score.agg(['min', 'size'])
    fb = set(bs[(bs.ns <= 4) & (bs.med <= 30) & (bs.n >= 3)].index) & set(gv[gv['min'] == 10].index)
    sh = T.assign(fb=T.buyer.isin(fb)).groupby('seller').fb.mean()
    o['b_smallticket'] = cap_count(R, fb | set(sh[sh >= 0.3].index))
    xo = X.groupby('src').amt.sum(); bi = T.groupby('buyer').amt.sum(); wo = W.groupby('acct').amt.sum()
    fw = set(bi.index[(xo.reindex(bi.index, fill_value=0) >= 0.9 * bi) & (wo.reindex(bi.index, fill_value=0) == 0)])
    o['b_forwarders'] = cap_count(R, fw)
    nin = X.groupby('dst').src.nunique(); sellers = set(T.seller)
    outp = X[X.dst.isin(sellers)].groupby('src').dst.nunique()
    cols = set(nin[nin >= 8].index) & set(outp.index)
    nb = set(X[X.dst.isin(cols)].src) | set(X[X.src.isin(cols)].dst) | cols
    o['b_fanin_collectors'] = cap_count(R, nb)
    tin = X.groupby('dst').amt.sum(); so = T.groupby('seller').amt.sum()
    tf = set(so.index[tin.reindex(so.index, fill_value=0) >= 0.5 * so])
    o['b_tfund_fwdbuyers'] = cap_count(R, tf | set(T[T.seller.isin(tf) & T.buyer.isin(fw)].buyer))
    cell = set(bs[(bs.med <= 30)].index) & fw & set(gv[gv['min'] == 10].index)
    o['c_cell'] = cap_count(R, cell)
    sh3 = T.assign(fb=T.buyer.isin(cell)).groupby('seller').fb.mean()
    o['c_cell_sellers'] = cap_count(R, cell | set(sh3[sh3 >= 0.25].index))
    rec = set(X[X.src.isin(cell)].dst); fund = X[X.src.isin(rec) & X.dst.isin(sellers)]
    o['c_cell_recips_sellers'] = cap_count(R, cell | rec | set(fund.dst))
    rt = set(zip(T.seller, T.buyer)) & set(zip(X.dst, X.src))
    pairs = set(zip(T.seller, T.buyer))
    wash = {a for (a, b) in pairs if (b, a) in pairs} | {b for (a, b) in pairs if (b, a) in pairs}
    o['d_wash_pairrt'] = cap_count(R, wash | {a for p in rt for a in p})
    pos = R[R.score == 10]
    pe = set(zip(pos.rater, pos.ratee)); deg = defaultdict(int)
    for a, b in pe:
        if (b, a) in pe and a < b:
            deg[a] += 1; deg[b] += 1
    o['d_mutual_core'] = cap_count(R, {a for a, k in deg.items() if k >= 4})
    CP = cpty_pairs(T)
    for win, nm in ((60, '1h'), (DAY, '1d'), (WEEK, '1w'), (Q, 'Q')):
        o['d2_any_' + nm] = cap_count(R, d2_set(d, win, 'escrow', CP=CP))
        o['d2_self_' + nm] = cap_count(R, d2_set(d, win, 'self', CP=CP))
    o['d2_amount_1w'] = cap_count(R, d2_set(d, WEEK, 'escrow', amount=True, CP=CP))
    o['d2_direct_Q'] = cap_count(R, d2_set(d, Q, 'escrow', hops=1, CP=CP))
    o['d3_all'] = cap_count(R, d3_set(d, 'all'))
    o['d3_fanin'] = cap_count(R, d3_set(d, 'fanin'))
    o['d3_fanin_fast'] = cap_count(R, d3_set(d, 'fanin_fast'))
    o['cyc2'] = cap_count(R, cycles(d, 2, False))
    o['cyc3_mixed'] = cap_count(R, cycles(d, 3, True))
    o['cyc3_mixed_timed'] = cap_count(R, cycles(d, 3, True, True))
    o['cyc4_mixed'] = cap_count(R, cycles(d, 4, True))
    o['cyc3_escrow_only'] = cap_count(R, cycles_single(d, 'escrow'))
    o['cyc3_wallet_only'] = cap_count(R, cycles_single(d, 'wallet'))
    o['cyc3_any'] = cap_count(R, cycles(d, 3, False) | cycles_single(d, 'escrow'))
    ss = T[T.amt <= 25].groupby('seller').size() / T.groupby('seller').size()
    top = set(ss[ss >= ss.quantile(0.99)].index)
    o['a_decompose'] = cap_count(R, top | set(T[T.seller.isin(top) & (T.amt <= 25)].buyer))
    return o


def cycles_single(d, which):
    """Cycles of length 2 or 3 inside one ledger."""
    G = d['T'][['seller', 'buyer']].rename(columns={'seller': 'u', 'buyer': 'v'}) if which == 'escrow' else \
        d['X'][['src', 'dst']].rename(columns={'src': 'u', 'dst': 'v'})
    G = G.drop_duplicates()
    two = G.merge(G.rename(columns={'u': 'v', 'v': 'u'}), on=['u', 'v'])
    flag = set(two.u) | set(two.v)
    p = G.rename(columns={'u': 'a', 'v': 'b'}).merge(G.rename(columns={'u': 'b', 'v': 'c'}), on='b')
    p = p[(p.c != p.a)]
    cl = p.merge(G.rename(columns={'u': 'c', 'v': 'a'}), on=['c', 'a'])
    return flag | set(cl.a) | set(cl.b) | set(cl.c)


def readers_default(d, w):
    """The default path alone: shared-device groups with the Calabash Point tablets set aside, kept where members traded
    with and rated one another, every account in those groups suspended, the holdback applied."""
    R = d['R'][d['R'].t < Q]
    tabs = {tab for ag, tab, custs in w['agents']}
    comp2 = comps(d['D'], tabs)
    rc2 = R.rater.map(comp2); ec2 = R.ratee.map(comp2); m3 = R[rc2.notna() & (rc2 == ec2)]
    gids = {comp2[a] for a in set(m3.rater) | set(m3.ratee)}
    return cap_count(R, {a for a, c in comp2.items() if c in gids})
