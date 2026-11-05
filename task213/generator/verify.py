"""task213 independent verifier: reads only target/ (and figures.json to compare), shares no code with the generator,
and recomputes the call, every ring line and every ask figure from the shipped files at face value, reading back every
format the pack ships (CSV, parquet, XLSX, PDF text with positive controls). Exit 1 on any mismatch."""
import json, re, sys
from collections import defaultdict
from pathlib import Path
import numpy as np, pandas as pd
from pypdf import PdfReader

TASK = Path(__file__).resolve().parent.parent
TG = TASK / 'target'
F = json.loads((TASK / 'generator' / 'figures.json').read_text())
Q0, Q1 = pd.Timestamp('2026-07-01', tz='UTC'), pd.Timestamp('2026-10-01', tz='UTC')
MK = {'NGN': 'NG', 'GHS': 'GH', 'KES': 'KE', 'GBP': 'GB'}
OUT, BAD = [], []


def ok(name, cond, detail=''):
    OUT.append('%s  %s  %s' % ('PASS' if cond else 'FAIL', name, detail))
    if not cond:
        BAD.append(name)


def pdf_text(name):
    t = ' '.join((p.extract_text() or '') for p in PdfReader(str(TG / name)).pages)
    return re.sub(r'\s+', ' ', t)


def main():
    # documents: every filed sentence the answer leans on, read back through one extractor, positive control first
    pb = pdf_text('moderation_playbook_v4.2.pdf')
    ok('pdf read-back control: playbook title', 'Moderation Playbook' in pb, '%d characters' % len(pb))
    ok('playbook 3.3 covers suspended accounts', 'including an account the sweep suspends' in pb)
    ok('playbook 1.2 latest version and first-given quarter', 'in its latest version' in pb and 'first given' in pb)
    sd = pdf_text('support_desk_procedure_sd04.pdf')
    ok('pdf read-back control: SD-04 title', 'Escrow Disputes Procedure' in sd, '%d characters' % len(sd))
    ok('SD-04 1.2 files which order a case is about', 'A case is about the order whose coins the escrow is holding when the case is opened' in sd)
    mp = pdf_text('merchant_programme_terms_mp2.pdf')
    ok('MP-2 1.2 defines the treasury wallet', 'wallet from which the group funds its desks and pays its cashback' in mp)
    tr = pdf_text('transparency_report_2026q2.pdf')
    ok('transparency report states its basis and the Q3 sample date', 'given by an account in a rating ring' in tr and 'January 2027' in tr)
    nt = pdf_text('integrity_notices_2026.pdf')
    ok('notices carry their own quarters', '9,800' in nt and '181,400' in nt)
    ok('the playbook names no wallet, transfer, forward or loop', not re.search(r'\b(wallet|transfers?|forward\w*|loops?)\b', pb, re.I), '')

    # keys: handles as at the order, wallet numbers to accounts through the register
    acc = pd.read_csv(TG / 'accounts.csv', dtype=str, keep_default_na=False)
    hc = pd.read_csv(TG / 'handle_changes.csv', dtype=str)
    hc['t'] = pd.to_datetime(hc.changed_at, utc=True)
    cur = dict(zip(acc.handle, acc.account_id))
    prev = defaultdict(list)
    for a, h, t in zip(hc.account_id, hc.previous_handle, hc.t): prev[h].append((t, a))
    def who(h, t):
        for tt, a in sorted(prev.get(h, ())):
            if t < tt: return a
        return cur.get(h)
    wal = {w: a for a, w in zip(acc.account_id, acc.wallet_no) if w}
    handle_now = dict(zip(acc.account_id, acc.handle))

    es = []
    for m in (7, 8, 9):
        e = pd.read_csv(TG / ('escrow_orders_2026-%02d.csv' % m), dtype=str, keep_default_na=False)
        es.append(e.rename(columns={'settled_at': 'released_at'}))
    E = pd.concat(es, ignore_index=True)
    ok('escrow exports read back', len(E) > 25000 and E.order_no.is_unique, '%d orders' % len(E))
    E['c'] = pd.to_datetime(E.created_at, utc=True); E['z'] = pd.to_datetime(E.closed_at, utc=True)
    E['sa'] = [who(h, t) for h, t in zip(E.seller, E.c)]; E['ba'] = [who(h, t) for h, t in zip(E.buyer, E.c)]
    rel = E[E.status == 'released'].copy()
    rel['r'] = pd.to_datetime(rel.released_at, utc=True)

    L = pd.read_parquet(TG / 'wallet_ledger_2026q3.parquet')
    L['t'] = L.posted_at.dt.tz_localize('Africa/Lagos').dt.tz_convert('UTC')
    X = L[L.entry_type == 'transfer'].copy()
    X['src'] = X.wallet_no.astype('int64').astype(str); X['dst'] = X.counterparty_wallet_no.astype('Int64').astype(str)
    walletof = dict(zip(acc.account_id, acc.wallet_no))

    # the loop: the buyer's transfer within the hour after the release, to an account that transfers to that seller
    P = rel[['order_no', 'sa', 'ba', 'r']].copy()
    P['bw'] = P.ba.map(walletof); P['sw'] = P.sa.map(walletof)
    M = P.merge(X[['src', 'dst', 't']], left_on='bw', right_on='src')
    M = M[(M.t >= M.r) & (M.t <= M.r + pd.Timedelta(minutes=60))]
    funds = set(zip(X.src, X.dst))
    M = M[[(d, s) in funds and d != s for d, s in zip(M.dst, M.sw)]].drop_duplicates('order_no')
    ring = set(M.sa) | set(M.ba) | set(M.dst.map(wal))
    ok('every loop account resolves through the register', None not in ring and np.nan not in ring, '%d accounts' % len(ring))
    par = {}
    def f(a):
        while par.get(a, a) != a: a = par[a]
        return a
    for s, b, x in zip(M.sa, M.ba, M.dst.map(wal)):
        for o in (b, x):
            ra, rb = f(s), f(o)
            if ra != rb: par[ra] = rb
    comp = defaultdict(set)
    for a in ring: comp[f(a)].add(a)

    R = pd.read_parquet(TG / 'ratings_2026q3.parquet')
    first = R.groupby('rating_id').recorded_at.min()
    R = R.sort_values(['rating_id', 'version']).drop_duplicates('rating_id', keep='last')
    R = R[R.rating_id.map(first).between(Q0, Q1, inclusive='left')]
    exp = R[R.rater_account.isin(ring)]
    rs = R[R.ratee_role == 'seller'].groupby('ratee_account').size()
    es_ = exp[exp.ratee_role == 'seller'].groupby('ratee_account').size()
    held = (es_ - rs.reindex(es_.index) // 2).clip(lower=0)
    held = held[held > 0]
    total = len(exp) - int(held.sum())
    c = F['call']
    ok('ring accounts', len(ring) == c['accounts_suspended'], '%d' % len(ring))
    ok('rings', len(comp) == c['rings'], '%d' % len(comp))
    ok('ratings given', len(exp) == c['ratings_given'], '%d' % len(exp))
    ok('held', int(held.sum()) == c['held'], '%d' % int(held.sum()))
    ok('expunged', total == c['expunged_exact'], '%d' % total)
    ok('notice figure', int(round(total, -2)) == c['notice'], '%d' % int(round(total, -2)))
    ringof = {a: k for k, s in comp.items() for a in s}
    sells = rel.groupby('sa').size()
    lines = {}
    for k, s in comp.items():
        e = exp[exp.rater_account.isin(s)]
        hk = 0
        for sl, hn in held.items():
            rr = {ringof[r] for r in exp[(exp.ratee_account == sl) & (exp.ratee_role == 'seller')].rater_account}
            if rr == {k}: hk += int(hn)
        top = sells.reindex(list(s)).fillna(0).sort_values(ascending=False).index[0]
        lines[handle_now[top]] = (len(s), len(e), hk, len(e) - hk)
    for r in F['rings']:
        ok('ring line %s' % r['ring'], lines.get(r['ring']) == (r['accounts'], r['given'], r['held'], r['expunged']), str(lines.get(r['ring'])))

    # ask 1: each case on the order the escrow held when it opened (SD-04 1.2)
    cs = pd.read_excel(TG / 'support_cases_2026q3.xlsx', sheet_name='Cases', dtype=str)
    codes = pd.read_excel(TG / 'support_cases_2026q3.xlsx', sheet_name='Outcome codes', dtype=str)
    ok('desk code sheet read back', set(codes.code) == {'U', 'R', 'W'}, '')
    cs['o'] = pd.to_datetime(cs.opened_wat).dt.tz_localize('Africa/Lagos').dt.tz_convert('UTC')
    em = E.set_index('order_no')
    pair = {k: g for k, g in E.groupby(['sa', 'ba'])}
    refs = []
    for ref, o in zip(cs.order_ref, cs.o):
        if ref in em.index and em.at[ref, 'c'] <= o <= em.at[ref, 'z']:
            refs.append(ref); continue
        s, b = (em.at[ref, 'sa'], em.at[ref, 'ba']) if ref in em.index else (None, None)
        g = pair.get((s, b))
        cand = g[(g.c <= o) & (g.z >= o)] if g is not None else g
        refs.append(cand.order_no.iloc[0] if cand is not None and len(cand) == 1 else None)
    cs['true'] = refs
    ok('every case names one order held when it opened', cs.true.notna().all(), '%d cases' % len(cs))
    cs['mk'] = cs.true.map(em.fiat_currency).map(MK)
    cs['fb'] = (cs.category.eq('coins not released') & cs.outcome.eq('U')) | (cs.category.eq('payment not received') & cs.outcome.eq('R'))
    per = cs.groupby(['mk', 'true']).fb.max().reset_index()
    for k in ('NG', 'GH', 'KE', 'GB'):
        s = per[per.mk == k]
        ok('ask 1 %s' % k, (len(s), int(s.fb.sum())) == (F['disputes'][k]['disputed'], F['disputes'][k]['for_buyer']), '%d, %d' % (len(s), int(s.fb.sum())))

    # ask 2: custodian transfers to outside addresses, sweeps of deposit addresses left out, by UTC month confirmed
    cu = pd.read_parquet(TG / 'custodian_outbound_2026q3.parquet')
    dep = set(L[L.entry_type == 'deposit'].chain_address.dropna())
    hot = set(cu.from_address) - dep
    w = cu[~cu.from_address.isin(dep) & ~cu.to_address.isin(hot)]
    g = w.groupby(w.confirmed_at.dt.month).agg(a=('amount_usdt', 'sum'), f=('network_fee_usdt', 'sum'))
    for m, k in ((7, 'Jul'), (8, 'Aug'), (9, 'Sep')):
        ok('ask 2 %s' % k, (int(round(g.loc[m, 'a'])), int(round(g.loc[m, 'f']))) == (F['onchain'][k]['withdrawn'], F['onchain'][k]['fees']),
           '%d, %d' % (round(g.loc[m, 'a']), round(g.loc[m, 'f'])))

    # ask 3: a group's treasury is every wallet that funded its desks (MP-2 1.2); its transfers to buyers are cashback
    gr = pd.read_excel(TG / 'merchant_programme_2026-09-30.xlsx', sheet_name='Groups', dtype=str)
    dk = pd.read_excel(TG / 'merchant_programme_2026-09-30.xlsx', sheet_name='Desks', dtype=str)
    dk['w'] = dk.desk_handle.map(cur).map(walletof)
    desks_w = set(dk.w)
    tre = {}
    for gc, mk_ in zip(gr.group_code, gr.market):
        dw = set(dk[dk.group_code == gc].w)
        for s in set(X[X.dst.isin(dw)].src) - desks_w:
            tre[s] = mk_
    cb = X[X.src.isin(tre) & ~X.dst.isin(desks_w) & ~X.dst.isin(tre) & (X.t >= Q0) & (X.t < Q1)]
    for k in ('NG', 'GH', 'KE', 'GB'):
        s = cb[cb.src.map(tre) == k]
        ok('ask 3 %s' % k, (int(round(s.amount_micro.sum() / 1e6)), s.dst.nunique()) == (F['cashback'][k]['cashback'], F['cashback'][k]['buyers']),
           '%d, %d' % (round(s.amount_micro.sum() / 1e6), s.dst.nunique()))

    # the golden workbook carries the same figures
    wb = pd.read_excel(TASK / 'golden' / 'q3_ratings_sweep.xlsx', sheet_name='Q3 sweep', header=None)
    ok('golden workbook carries the notice figure', (wb == c['notice']).any().any(), '')
    print('\n'.join(OUT))
    print('%s: %d checks, %d failed' % ('PASS' if not BAD else 'FAIL', len(OUT), len(BAD)))
    return 1 if BAD else 0


if __name__ == '__main__':
    sys.exit(main())
