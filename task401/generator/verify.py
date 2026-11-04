"""Independent verifier: recomputes from target/ alone (its own code, pandas group-bys rather than golden.py's arrays)
the four changes' membership-year costs and the call, every admissions figure and every fees figure, and compares them with
generator/figures.json. Exit 1 on any mismatch.

    python3 verify.py
"""
import os, sys, glob, json, re
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), 'target')
F = json.load(open(os.path.join(HERE, 'figures.json')))
OUT = []


def check(name, cond, detail=''):
    OUT.append((bool(cond), name, detail))


def main_call():
    reg = pd.read_csv(os.path.join(T, 'membership_register_2026-03-16.csv'), dtype=str)
    reg['joined'] = pd.to_datetime(reg.joined)
    rq = pd.read_csv(glob.glob(os.path.join(T, 'cancellation_requests_*.csv'))[0], dtype=str)
    rq['received'] = pd.to_datetime(rq.received).dt.normalize()
    first = rq.groupby('membership_no').received.min()
    reg['first'] = reg.membership_no.map(first)
    v = pd.read_parquet(glob.glob(os.path.join(T, 'access_weekly_usage_*.parquet'))[0])
    v['wc'] = pd.to_datetime(v.week_commencing)
    bk = pd.read_parquet(glob.glob(os.path.join(T, 'class_bookings_*.parquet'))[0])
    bk['st'] = pd.to_datetime(bk.session_start)
    day = bk[(bk.st.dt.weekday < 5) & (bk.st.dt.hour < 17)]
    acct = pd.to_datetime(reg.rewards_account_opened)
    def booked(a, b):
        x = day[(day.st >= a) & (day.st < pd.Timestamp(b) + pd.Timedelta(days=1))].membership_no.unique()
        return reg.membership_no.isin(x)
    yr = pd.Timedelta(days=364)
    R26 = {'A': acct <= '2026-01-31', 'D': reg.tariff_code.str.startswith('L-'),
           'C': booked(pd.Timestamp('2025-10-13'), pd.Timestamp('2026-01-11')), 'E': reg.home_centre.isin(['Northgate', 'Westcroft'])}
    R25 = {'A': acct <= pd.Timestamp('2026-01-31') - yr, 'D': R26['D'],
           'C': booked(pd.Timestamp('2025-10-13') - yr, pd.Timestamp('2026-01-11') - yr), 'E': R26['E']}
    start = {'A': '2026-02-02', 'D': '2026-02-02', 'C': '2026-01-12', 'E': '2026-02-09'}
    ext = pd.Timestamp('2026-03-16')
    def books(d): return (reg.joined < d) & (reg['first'].isna() | (reg['first'] >= d))
    def notvisiting(d):
        seen = v[(v.wc >= d - pd.Timedelta(days=28)) & (v.wc < d)].membership_no.unique()
        return books(d) & ~reg.membership_no.isin(seen)
    def left(m, a, b): return (m & reg['first'].notna() & (reg['first'] >= a) & (reg['first'] < b)).sum()
    nv1, nv0 = notvisiting(ext), notvisiting(ext - yr)
    costs = {}
    for k in 'ADCE':
        d = pd.Timestamp(start[k])
        a1, a0 = R26[k] & books(d), R25[k] & books(d - yr)
        so = (left(a1, d, ext) / a1.sum() - left(a0, d - yr, ext - yr) / a0.sum()) * a1.sum()
        b1, b0 = R26[k] & books(ext), R25[k] & books(ext - yr)
        ex = ((nv1 & R26[k]).sum() / b1.sum() - (nv0 & R25[k]).sum() / b0.sum()) * b1.sum()
        coh = nv0 & R25[k]
        conv = left(coh, ext - yr, pd.Timestamp('2026-02-02')) / coh.sum()
        costs[k] = so + ex * conv
        check('cost of %s recomputes' % k, int(round(costs[k], -1)) == F['cost'][k], '%.1f against %d' % (costs[k], F['cost'][k]))
    check('the call recomputes', max(costs, key=costs.get) == F['call_key'], max(costs, key=costs.get))


def admissions():
    pl = pd.read_excel(os.path.join(T, 'price_list_2025-26.xlsx'), sheet_name='Pay as you go')
    size = {round(p, 2): sum(int(x) for x in re.findall(r'(\d+) (?:adult|child)', a)) or 1 for p, a in zip(pl.price, pl.admits)}
    o = pd.read_csv(os.path.join(T, 'till_sales_old_system_2025-10-01_to_2025-11-30.csv'))
    o = o[o.price != 0].copy()
    o['n'] = np.where(o['product'] == 'Family Swim', o.price.abs().round(2).map(size), 1) * np.sign(o.price)
    o['m'] = pd.to_datetime(o.sold, format='%d/%m/%Y %H:%M').dt.strftime('%Y-%m')
    o['g'] = np.where(o.site.isin(['Northgate', 'Westcroft']), 'NW', 'other')
    import docx
    tbl = docx.Document(os.path.join(T, 'epos_go_live_notice_2025-10.docx')).tables[0]
    codes = {r.cells[1].text: r.cells[0].text for r in tbl.rows[1:]}
    e = pd.read_csv(glob.glob(os.path.join(T, 'epos_sales_*.csv'))[0])
    e['t'] = pd.to_datetime(e.timestamp); e['site'] = e.site_code.map(codes)
    e['half'] = (e.amount.abs() == 4.70) & e['item'].isin(['POOL-ADULT', 'GYM-ADULT'])
    tx = e.groupby('transaction').agg(t=('t', 'first'), site=('site', 'first'), lines=('item', 'size'), neg=('amount', lambda a: (a < 0).all()),
                                      pool_half=('half', lambda h: h[e.loc[h.index, 'item'] == 'POOL-ADULT'].sum()),
                                      gym_half=('half', lambda h: h[e.loc[h.index, 'item'] == 'GYM-ADULT'].sum()))
    tx['people'] = tx.lines - np.minimum(tx.pool_half, tx.gym_half)
    pc = pd.read_csv(glob.glob(os.path.join(T, 'pool_closures_*.csv'))[0])
    pc['a'] = pd.to_datetime(pc.date + ' ' + pc.closed_at); pc['b'] = pd.to_datetime(pc.date + ' ' + pc.reopened_at)
    def in_closure(r):
        z = pc[pc.site == r.site]; return ((z.a <= r.t) & (r.t <= z.b)).any()
    neg = tx[tx.neg].copy(); neg['closure'] = [in_closure(r) for r in neg.itertuples()]
    tx['n'] = np.where(~tx.neg, tx.people, 0)
    tx.loc[neg.index[~neg.closure], 'n'] = -neg.people[~neg.closure]
    tx['m'] = tx.t.dt.strftime('%Y-%m'); tx['g'] = np.where(tx.site.isin(['Northgate', 'Westcroft']), 'NW', 'other')
    tot = pd.concat([o.groupby(['m', 'g']).n.sum(), tx.groupby(['m', 'g']).n.sum()]).groupby(level=[0, 1]).sum()
    for key, val in F['admissions'].items():
        m, g = key.split()
        check('admissions %s recomputes' % key, int(round(tot.get((m, g), 0), -1)) == val, '%s against %s' % (tot.get((m, g), 0), val))


def fees():
    reg = pd.read_csv(os.path.join(T, 'membership_register_2026-03-16.csv'), dtype=str)
    fee = pd.read_excel(os.path.join(T, 'price_list_2025-26.xlsx'), sheet_name='Memberships').set_index('tariff_code').monthly_fee
    hol = {date(2025, 12, 25), date(2025, 12, 26), date(2026, 1, 1)}
    def nxt(d):
        d += timedelta(days=1)
        while d.weekday() > 4 or d in hol: d += timedelta(days=1)
        return d
    payer = {m: (p if isinstance(p, str) else m) for m, p in zip(reg.membership_no, reg.paid_by_membership_no)}
    day = {m: int(cd) for m, cd in zip(reg.membership_no, reg.collection_day)}
    joined = {m: date.fromisoformat(j) for m, j in zip(reg.membership_no, reg.joined)}
    ends = {m: (date.fromisoformat(x) if isinstance(x, str) else date(2099, 1, 1)) for m, x in zip(reg.membership_no, reg.membership_ends)}
    a = pd.read_csv(glob.glob(os.path.join(T, 'dd_bureau_A_submissions_*.csv'))[0], dtype=str)
    b = pd.read_csv(glob.glob(os.path.join(T, 'dd_collections_*.csv'))[0], dtype=str)
    md = pd.read_csv(os.path.join(T, 'dd_mandates_2026-03-16.csv'), dtype=str).set_index('mandate_reference').membership_no
    rt = pd.read_csv(glob.glob(os.path.join(T, 'bacs_returns_*.csv'))[0], dtype=str)
    returned = set(zip(rt.reference, rt.original_date))
    members = {}
    for m, p in payer.items(): members.setdefault(p, []).append(m)
    ev = {}
    for r in a.itertuples():
        pdte = datetime.strptime(r.processing_date, '%d/%m/%Y').date(); m = r.payer_reference.split('/')[1]
        ev.setdefault(m, []).append((nxt(pdte), r.transaction_code, (r.payer_reference, pdte.isoformat()) not in returned))
    for r in b.itertuples():
        cd = date.fromisoformat(r.collection_date)
        for m in members.get(md[r.mandate_reference], []):
            if joined[m] <= cd < ends[m]:
                ev.setdefault(m, []).append((cd, 'FIRST' if r.type == 'FIRST' else 'B', (r.mandate_reference, r.collection_date) not in returned))
    tot = {}
    for m, es in ev.items():
        owed, pend = [], None
        for cd, kind, good in sorted(es):
            if kind == '18':
                cover, pend = pend or [], None
            else:
                mo = (joined[m].year, joined[m].month) if kind in ('01', 'FIRST') else (
                    (cd.year, cd.month) if cd.day >= day[payer[m]] else ((cd.year - 1, 12) if cd.month == 1 else (cd.year, cd.month - 1)))
                cover, owed = owed + [mo], []
            if good:
                for mo in cover:
                    k = ('%d-%02d' % mo, 'legacy' if reg.set_index('membership_no').tariff_code.get(m, 'L-').startswith('L-') else '2023') if False else ('%d-%02d' % mo, m)
                    tot[k] = tot.get(k, 0) + 1
            elif kind in ('01', '17'):
                pend = cover
            else:
                owed = cover
    tar = dict(zip(reg.membership_no, reg.tariff_code))
    sums = {}
    for (mo, m), cnt in tot.items():
        g = 'legacy' if tar[m].startswith('L-') else '2023'
        sums[(mo, g)] = sums.get((mo, g), 0) + cnt * float(fee[tar[m]])
    for key, val in F['fees'].items():
        mo, g = key.split()
        check('fees %s recomputes' % key, int(round(sums.get((mo, g), 0), -2)) == val, '%.2f against %s' % (sums.get((mo, g), 0), val))


if __name__ == '__main__':
    main_call(); admissions(); fees()
    bad = [x for x in OUT if not x[0]]
    for good, name, detail in OUT:
        print('%s  %s  [%s]' % ('PASS' if good else 'FAIL', name, detail))
    print('%d of %d' % (len(OUT) - len(bad), len(OUT)))
    raise SystemExit(1 if bad else 0)
