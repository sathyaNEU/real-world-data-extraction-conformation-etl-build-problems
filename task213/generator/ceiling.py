"""task213 ask ceiling, measured on the cut pack. Reads target/ and figures.json only and shares no code with the
generator. Three responses are scored ask figure by ask figure against the golden:
  cracker        on the call; runs the hygiene battery and every filed rule; takes each ask's system of record as it
                 stands (the desk's cited order, the custodian's outbound list, the register's treasury wallets);
  full includer  on the call; as the cracker, and also reconciles the wallet's withdrawal requests to the custodian
                 by destination address and amount, the habit of tying an input to another system's total;
  mirror         off the call (the phone-linkage default path); asks as the cracker.
A figure is kept when it equals the golden at the asking sentence's precision. Weights: 38 recommendation and
critical components plus 7 instruction-following on the call, 5 plus 7 off it, 55 shared equally by the ask figures."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd

TASK = Path(__file__).resolve().parent.parent
TG = TASK / 'target'
MK = {'NGN': 'NG', 'GHS': 'GH', 'KES': 'KE', 'GBP': 'GB'}
MONTHS = {7: 'Jul', 8: 'Aug', 9: 'Sep'}


def escrow():
    fs = []
    for m in (7, 8, 9):
        e = pd.read_csv(TG / ('escrow_orders_2026-%02d.csv' % m), dtype=str, keep_default_na=False)
        e = e.rename(columns={'settled_at': 'released_at'})
        fs.append(e)
    return pd.concat(fs, ignore_index=True).drop_duplicates('order_no')


def resolve_cases(cs, esc):
    """The desk's own definition: a case is about the order whose coins the escrow held when it was opened. Keep the
    cited order when it was open then; otherwise take the same two parties' order open at that moment."""
    acc = pd.read_csv(TG / 'accounts.csv', dtype=str, keep_default_na=False)
    hc = pd.read_csv(TG / 'handle_changes.csv', dtype=str)
    hc['t'] = pd.to_datetime(hc.changed_at, utc=True)
    cur = dict(zip(acc.handle, acc.account_id))
    old = {}
    for a, p, t in zip(hc.account_id, hc.previous_handle, hc.t): old.setdefault(p, []).append((t, a))
    def who(h, t):
        for tt, a in old.get(h, ()):
            if t < tt: return a
        return cur.get(h, h)
    e = esc.copy()
    e['c'] = pd.to_datetime(e.created_at, utc=True)
    e['z'] = pd.to_datetime(e.closed_at, utc=True)
    e['sa'] = [who(h, t) for h, t in zip(e.seller, e.c)]
    e['ba'] = [who(h, t) for h, t in zip(e.buyer, e.c)]
    cs = cs.copy()
    cs['o'] = pd.to_datetime(cs.opened_wat).dt.tz_localize('Africa/Lagos').dt.tz_convert('UTC')
    m = cs.merge(e[['order_no', 'sa', 'ba', 'c', 'z']], left_on='order_ref', right_on='order_no', how='left')
    good = (m.c <= m.o) & (m.z >= m.o)
    byp = {k: g for k, g in e.groupby(['sa', 'ba'])}
    refs = []
    for ok_, ref, s, b, o in zip(good, m.order_ref, m.sa, m.ba, m.o):
        if ok_ or not isinstance(s, str):
            refs.append(ref); continue
        g = byp.get((s, b))
        cand = g[(g.c <= o) & (g.z >= o)] if g is not None else []
        refs.append(cand.order_no.iloc[0] if len(cand) == 1 else ref)
    cs['order_ref'] = refs
    return cs


def ask1(esc, validate=False):
    cs = pd.read_excel(TG / 'support_cases_2026q3.xlsx', sheet_name='Cases', dtype=str)
    if validate:
        cs = resolve_cases(cs, esc)
    m = cs.merge(esc[['order_no', 'fiat_currency']], left_on='order_ref', right_on='order_no', how='inner')
    m['mk'] = m.fiat_currency.map(MK)
    m['buyer_case'] = m.category.eq('coins not released')
    m['for_buyer'] = (m.buyer_case & m.outcome.eq('U')) | (~m.buyer_case & m.outcome.eq('R'))
    per = m.groupby(['mk', 'order_ref']).for_buyer.max().reset_index()
    out = {}
    for k in ('NG', 'GH', 'KE', 'GB'):
        s = per[per.mk == k]
        out[k] = dict(disputed=int(len(s)), for_buyer=int(s.for_buyer.sum()))
    return out


def ask2(route):
    cu = pd.read_parquet(TG / 'custodian_outbound_2026q3.parquet')
    cu['mo'] = cu.confirmed_at.dt.month.map(MONTHS)
    if route == 'custodian':
        g = cu.groupby('mo').agg(w=('amount_usdt', 'sum'), f=('network_fee_usdt', 'sum'))
    else:
        wl = pd.read_parquet(TG / 'wallet_ledger_2026q3.parquet')
        wd = wl[wl.entry_type == 'withdrawal'].copy()
        wd['amt'] = (wd.amount_micro / 1e6).round(2)
        j = wd.merge(cu, left_on=['chain_address', 'amt'], right_on=['to_address', 'amount_usdt'], how='inner')
        j = j.drop_duplicates('tx_hash')
        g = j.groupby('mo').agg(w=('amount_usdt', 'sum'), f=('network_fee_usdt', 'sum'))
    return {k: dict(withdrawn=int(round(g.loc[k, 'w'])), fees=int(round(g.loc[k, 'f']))) for k in ('Jul', 'Aug', 'Sep')}


def ask3():
    gr = pd.read_excel(TG / 'merchant_programme_2026-09-30.xlsx', sheet_name='Groups', dtype=str)
    dk = pd.read_excel(TG / 'merchant_programme_2026-09-30.xlsx', sheet_name='Desks', dtype=str)
    acc = pd.read_csv(TG / 'accounts.csv', dtype=str, keep_default_na=False)
    wl = pd.read_parquet(TG / 'wallet_ledger_2026q3.parquet')
    desk_w = set(acc[acc.handle.isin(set(dk.desk_handle))].wallet_no.astype(str))
    tre = dict(zip(gr.treasury_wallet_no.astype(str), gr.market))
    tr = wl[wl.entry_type == 'transfer'].copy()
    tr['src'] = tr.wallet_no.astype('int64').astype(str); tr['dst'] = tr.counterparty_wallet_no.astype('Int64').astype(str)
    cb = tr[tr.src.isin(tre) & ~tr.dst.isin(desk_w) & ~tr.dst.isin(tre)].copy()
    cb['mk'] = cb.src.map(tre)
    out = {}
    for k in ('NG', 'GH', 'KE', 'GB'):
        s = cb[cb.mk == k]
        out[k] = dict(cashback=int(round(s.amount_micro.sum() / 1e6)), buyers=int(s.dst.nunique()))
    return out


def flat(a1, a2, a3):
    v = []
    for k in ('NG', 'GH', 'KE', 'GB'): v += [('disputes %s disputed' % k, a1[k]['disputed']), ('disputes %s for buyer' % k, a1[k]['for_buyer'])]
    for k in ('Jul', 'Aug', 'Sep'): v += [('on-chain %s withdrawn' % k, a2[k]['withdrawn']), ('on-chain %s fees' % k, a2[k]['fees'])]
    for k in ('NG', 'GH', 'KE', 'GB'): v += [('cashback %s USDT' % k, a3[k]['cashback']), ('cashback %s buyers' % k, a3[k]['buyers'])]
    return v


def main():
    F = json.loads((TASK / 'generator' / 'figures.json').read_text())
    gold = flat(F['disputes'], F['onchain'], F['cashback'])
    esc = escrow()
    a1 = ask1(esc); a1v = ask1(esc, validate=True); a3 = ask3()
    rows = {'cracker': (45, flat(a1, ask2('custodian'), a3)),
            'full includer': (45, flat(a1v, ask2('reconcile'), a3)),
            'mirror': (12, flat(a1, ask2('custodian'), a3)),
            'mirror includer': (12, flat(a1v, ask2('reconcile'), a3))}
    n = len(gold)
    score, keep = {}, {}
    print('%-28s %12s %12s %12s %12s %12s' % ('figure', 'golden', 'cracker', 'includer', 'mirror', 'mirror-incl'))
    for i, (name, g) in enumerate(gold):
        print('%-28s %12s %12s %12s %12s %12s' % (name, g, rows['cracker'][1][i][1], rows['full includer'][1][i][1], rows['mirror'][1][i][1], rows['mirror includer'][1][i][1]))
    for r, (bank, v) in rows.items():
        k = sum(1 for (nm, g), (nm2, x) in zip(gold, v) if abs(x - g) < 0.5)
        keep[r] = k; score[r] = bank + 55.0 * k / n
    asks = [('ask 1 disputes', 0, 8), ('ask 2 on-chain', 8, 14), ('ask 3 cashback', 14, 22)]
    print()
    print('| ask | figures | cracker keeps | full includer keeps | mirror keeps | cracker |')
    print('|---|---|---|---|---|---|')
    for nm, a, b in asks:
        kc = sum(1 for i in range(a, b) if abs(rows['cracker'][1][i][1] - gold[i][1]) < 0.5)
        kf = sum(1 for i in range(a, b) if abs(rows['full includer'][1][i][1] - gold[i][1]) < 0.5)
        km = sum(1 for i in range(a, b) if abs(rows['mirror'][1][i][1] - gold[i][1]) < 0.5)
        print('| %s | %d | %d | %d | %d | %s |' % (nm, b - a, kc, kf, km, 'miss' if kc < b - a else 'KEPT'))
    pair = max((score['full includer'] + score['mirror']) / 2, (score['cracker'] + score['mirror includer']) / 2,
               (score['full includer'] + score['mirror includer']) / 2)
    pair2 = (score['cracker'] + score['full includer']) / 2
    print()
    print('kept of %d: cracker %d, full includer %d, mirror %d, mirror includer %d' % (n, keep['cracker'], keep['full includer'], keep['mirror'], keep['mirror includer']))
    print('scores: cracker %.1f, full includer %.1f, mirror %.1f, mirror includer %.1f' % (score['cracker'], score['full includer'], score['mirror'], score['mirror includer']))
    print('Pair ceiling (worst pairing of one on the call and one off): %.1f' % pair)
    print('Pair with two on the call (cracker, full includer): %.1f' % pair2)
    print('Mirror leakage: %.1f per cent of ask weight (worst mirror)' % (100.0 * max(keep['mirror'], keep['mirror includer']) / n))
    return 0 if pair <= 60 else 1


if __name__ == '__main__':
    sys.exit(main())
