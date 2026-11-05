"""The golden figures, computed on the clean truth: the Q3 sweep (every ring, the holdback, the notice figure, one
line per ring) and the three asks (disputes, on-chain withdrawals, merchant-group cashback)."""
import numpy as np, pandas as pd
from collections import defaultdict
from core import Q, DAY
from screens import golden_set


def holdback(R, susp):
    """Expunged and held counts under the playbook's 3.3, which applies to every account, suspended or not."""
    exp = R[R.rater.isin(susp)]
    rs = R[R.role_ratee == 'seller'].groupby('ratee').size()
    es = exp[exp.role_ratee == 'seller'].groupby('ratee').size()
    held = (es - rs.reindex(es.index) // 2).clip(lower=0)
    return exp, held[held > 0]


def rings_of(d, gs):
    """Connected components of the loop accounts: each buyer, the account it passed coins to, and the seller."""
    from screens import forwards
    M = forwards(d, 60, False)
    X = d['X']
    C = X.rename(columns={'src': 'x', 'dst': 'h', 'amt': 'ca', 't': 'ct'})
    L = M.merge(C, on=['x', 'h']).drop_duplicates('pid')
    par = {}
    def f(a):
        while par.get(a, a) != a:
            par[a] = par.get(par[a], par[a]); a = par[a]
        return a
    for h, s, x in zip(L.h, L.s, L.x):
        for b in (s, x):
            ra, rb = f(h), f(b)
            if ra != rb: par[ra] = rb
    comp = defaultdict(set)
    for a in gs: comp[f(a)].add(a)
    return list(comp.values())


def main_call(d, x, handle_now):
    R = d['R'][d['R'].t < Q]
    gs = golden_set(d)
    exp, held = holdback(R, gs)
    rings = rings_of(d, gs)
    T = d['T']
    # a held rating belongs to the ring whose accounts gave the ratings on that seller (one ring per seller, asserted)
    ring_ix = {a: i for i, r in enumerate(rings) for a in r}
    held_ring = {}
    for s, hn in held.items():
        rs_ = {ring_ix[r] for r in exp[(exp.ratee == s) & (exp.role_ratee == 'seller')].rater}
        assert len(rs_) == 1, (s, rs_)
        held_ring[s] = rs_.pop()
    lines = []
    for i, ring in enumerate(rings):
        e = exp[exp.rater.isin(ring)]
        h_ = int(sum(int(hn) for s, hn in held.items() if held_ring[s] == i))
        # every held rating sits on a seller inside the same ring (asserted in checks.py)
        sells = T[T.seller.isin(ring)].groupby('seller').size().sort_values(ascending=False)
        top = sells.index[0]
        lines.append(dict(ring=handle_now[top], accounts=len(ring), given=int(len(e)), held=h_, expunged=int(len(e) - h_),
                          members=sorted(int(a) for a in ring)))
    lines.sort(key=lambda r: -r['expunged'])
    total_given = int(len(exp)); total_held = int(held.sum()); total = total_given - total_held
    return dict(ring_set=gs, lines=lines, given=total_given, held=total_held, expunged=total,
                notice=int(round(total, -2)), accounts=len(gs), held_on_outside=int(held[~held.index.isin(gs)].sum()))


def ask_disputes(x):
    C = x['cases']
    mk = x['A'].market.to_dict()
    T = x['T']; ret = x['ret']
    seller = dict(zip(T.tid, T.seller)); seller.update(dict(zip(ret.tid, ret.seller)))
    def outcome(g):
        r = g.iloc[0]
        if r.code == 'W': return 'W'
        return 'B' if (r.role == 'buyer') == (r.code == 'U') else 'S'
    o = C.groupby('true_tid').apply(outcome, include_groups=False)
    m = pd.Series({t: mk[seller[t]] for t in o.index})
    out = {}
    for k in ('NG', 'GH', 'KE', 'GB'):
        sel = m[m == k].index
        out[k] = dict(disputed=int(len(sel)), for_buyer=int((o[sel] == 'B').sum()))
    return out


def ask_onchain(x):
    C = x['chain']
    C = C[(C.kind == 'withdrawal') & (C.block < Q)]
    mo = pd.cut(C.block, [0, 31 * DAY, 62 * DAY, Q], right=False, labels=['Jul', 'Aug', 'Sep'])
    g = C.groupby(mo, observed=False).agg(amt=('amt', 'sum'), fee=('fee', 'sum'))
    return {k: dict(withdrawn=float(g.loc[k, 'amt']), fees=float(g.loc[k, 'fee'])) for k in ('Jul', 'Aug', 'Sep')}


def ask_cashback(d, x):
    X = x['X']
    treas = {gw: mk for gw, desks, mk in d['groups']}
    for r in x['repl']:
        treas[r['new_gw']] = r['market']
    desks = {dk for gw, ds, mk in d['groups'] for dk in ds}
    cb = X[X.src.isin(treas) & ~X.dst.isin(desks) & ~X.dst.isin(treas) & (X.t >= 0) & (X.t < Q)]
    cb = cb.assign(mk=cb.src.map(treas))
    out = {}
    for k in ('NG', 'GH', 'KE', 'GB'):
        s = cb[cb.mk == k]
        out[k] = dict(cashback=float(s.amt.sum()), buyers=int(s.dst.nunique()))
    return out, cb


def edge(v, unit):
    """Distance from a value to the nearest edge of its printed bin."""
    return unit / 2 - abs(v - round(v / unit) * unit)
