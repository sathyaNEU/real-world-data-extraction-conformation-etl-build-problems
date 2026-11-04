"""task401 asks, from the shipped files: pay-as-you-go admissions by month at Northgate and Westcroft together and at the
other seven centres together (October 2025 to February 2026), and membership fees by the month they pay for on the
legacy and the 2023 tariffs (November 2025 to February 2026). Each ask has a golden and the profiles ceiling.py scores:
the cracker (the hygiene battery, every line read as it stands), the full includer (every device noticed and handled
the natural way) and the no-repair reader (every row as it stands)."""
import os, glob, re
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), 'target')
HOURS_SITES = ('Northgate', 'Westcroft')
TILL_MONTHS = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2)]
DD_MONTHS = [(2025, 11), (2025, 12), (2026, 1), (2026, 2)]
HOLIDAYS = {date(2025, 8, 25), date(2025, 12, 25), date(2025, 12, 26), date(2026, 1, 1), date(2026, 4, 3)}


def working(d): return d.weekday() < 5 and d not in HOLIDAYS
def next_working(d):
    d += timedelta(days=1)
    while not working(d): d += timedelta(days=1)
    return d


def till_load():
    pl = pd.read_excel(os.path.join(T, 'price_list_2025-26.xlsx'), sheet_name='Pay as you go')
    party = {}
    for _, r in pl.iterrows():
        nums = [int(x) for x in re.findall(r'(\d+) (?:adult|child)', r.admits)]
        party[round(float(r.price), 2)] = sum(nums) if nums else 1
    old = pd.read_csv(os.path.join(T, 'till_sales_old_system_2025-10-01_to_2025-11-30.csv'))
    old['t'] = pd.to_datetime(old.sold, format='%d/%m/%Y %H:%M')
    new = pd.read_csv(glob.glob(os.path.join(T, 'epos_sales_*.csv'))[0])
    new['t'] = pd.to_datetime(new.timestamp)
    import docx
    d = docx.Document(os.path.join(T, 'epos_go_live_notice_2025-10.docx'))
    code = {row.cells[1].text: row.cells[0].text for row in d.tables[0].rows[1:]}
    new['site'] = new.site_code.map(code)
    pc = pd.read_csv(glob.glob(os.path.join(T, 'pool_closures_*.csv'))[0])
    pc['a'] = pd.to_datetime(pc.date + ' ' + pc.closed_at); pc['b'] = pd.to_datetime(pc.date + ' ' + pc.reopened_at)
    return party, old, new, pc


def till_count(route):
    party, old, new, pc = till_load()
    grp = lambda s: 'NW' if s in HOURS_SITES else 'other'
    res = {}
    def add(t, site, n):
        k = (t.year, t.month, grp(site)); res[k] = res.get(k, 0) + n
    # old till
    for r in old.itertuples():
        if r.price == 0: continue
        if route == 'golden' or route == 'full':
            n = party.get(round(abs(r.price), 2), 1) if r.product == 'Family Swim' else 1
        else:
            n = 1
        if r.price < 0:
            if route == 'norepair': continue
            n = -n
        add(r.t, r.site, n)
    # new EPOS: one transaction at a time
    inwin = {}
    for c in pc.itertuples():
        inwin.setdefault(c.site, []).append((c.a, c.b))
    for tx, g in new.groupby('transaction', sort=False):
        t = g.t.iloc[0]; site = g.site.iloc[0]
        neg = (g.amount < 0).all()
        if route in ('golden', 'full'):
            pairs = min(((g.item == 'POOL-ADULT') & (g.amount.abs() == 4.70)).sum(), ((g.item == 'GYM-ADULT') & (g.amount.abs() == 4.70)).sum())
            n = len(g) - pairs
        else:
            n = len(g)
        if neg:
            if route == 'norepair':
                continue
            if route == 'golden':
                closure = any(a <= t <= b for (a, b) in inwin.get(site, []))
                if closure:
                    continue          # refunded after the pool closed: these people had been admitted
            n = -n
        add(t, site, n)
    return {('%d-%02d' % (y, m), g): res.get((y, m, g), 0) for (y, m) in TILL_MONTHS for g in ('NW', 'other')}


def dd_load():
    reg = pd.read_csv(os.path.join(T, 'membership_register_2026-03-16.csv'), dtype=str)
    fees = pd.read_excel(os.path.join(T, 'price_list_2025-26.xlsx'), sheet_name='Memberships')
    fee = dict(zip(fees.tariff_code, fees.monthly_fee.astype(float)))
    admin = float(pd.read_excel(os.path.join(T, 'price_list_2025-26.xlsx'), sheet_name='Charges').query("charge.str.startswith('Failed')").amount.iloc[0])
    A = pd.read_csv(glob.glob(os.path.join(T, 'dd_bureau_A_submissions_*.csv'))[0], dtype=str)
    A['pdate'] = [datetime.strptime(x, '%d/%m/%Y').date() for x in A.processing_date]
    A['amount'] = A.amount_pence.astype(int) / 100
    A['membership_no'] = A.payer_reference.str.split('/').str[1]
    B = pd.read_csv(glob.glob(os.path.join(T, 'dd_collections_*.csv'))[0], dtype=str)
    B['cdate'] = [date.fromisoformat(x) for x in B.collection_date]; B['amount'] = B.amount.astype(float)
    MD = pd.read_csv(os.path.join(T, 'dd_mandates_2026-03-16.csv'), dtype=str)
    RT = pd.read_csv(glob.glob(os.path.join(T, 'bacs_returns_*.csv'))[0], dtype=str)
    RT['odate'] = [date.fromisoformat(x) for x in RT.original_date]
    return reg, fee, admin, A, B, MD, RT


def dd_count(route):
    """Membership fees by the month they pay for. golden: a fee counts for its month once any collection that carries it
    clears, across both bureaux; full: the same, but a returned collection's months are looked for only in the next
    collection on the same reference, and an amount nothing explains is kept in the month it came in; cracker: returned
    lines out, every line whole in its own date's month and the payer's tariff group; norepair: every line as it stands."""
    reg, fee, admin, A, B, MD, RT = dd_load()
    grp = {m: ('legacy' if t.startswith('L-') else '2023') for m, t in zip(reg.membership_no, reg.tariff_code)}
    mfee = {m: fee[t] for m, t in zip(reg.membership_no, reg.tariff_code)}
    payer = {m: (p if isinstance(p, str) else m) for m, p in zip(reg.membership_no, reg.paid_by_membership_no)}
    cday = dict(zip(reg.membership_no, reg.collection_day.astype(int)))
    house = {}
    for m, p in payer.items(): house.setdefault(p, []).append(m)
    m_of = dict(zip(MD.mandate_reference, MD.membership_no))
    retA = {(r.reference, r.odate) for r in RT[RT.bureau == 'A'].itertuples()}
    retB = {(r.reference, r.odate) for r in RT[RT.bureau == 'B'].itertuples()}
    joined = {m: date.fromisoformat(j) for m, j in zip(reg.membership_no, reg.joined)}
    ends = {m: (date.fromisoformat(e) if isinstance(e, str) else date(2099, 1, 1)) for m, e in zip(reg.membership_no, reg.membership_ends)}
    def month_for(m, cd):
        day = cday[payer[m]]
        if cd.day >= day: return (cd.year, cd.month)
        return (cd.year - (cd.month == 1), 12 if cd.month == 1 else cd.month - 1)
    res = {}
    def add(mo, m, x):
        k = (mo, grp[m]); res[k] = res.get(k, 0.0) + x
    events = []
    for r in A.itertuples():
        cd = next_working(r.pdate) if route in ('golden', 'full') else r.pdate
        first = r.transaction_code == '01'
        events.append((cd, 'A', [r.membership_no], r.amount, (r.payer_reference, r.pdate) not in retA, r.transaction_code == '18', r.payer_reference, first))
    for r in B.itertuples():
        p = m_of[r.mandate_reference]
        due = [m for m in house.get(p, [p]) if joined[m] <= r.cdate < ends[m]]
        events.append((r.cdate, 'B', due if route in ('golden', 'full') else [p], r.amount, (r.mandate_reference, r.cdate) not in retB, False,
                       r.mandate_reference, r.type == 'FIRST'))
    events.sort(key=lambda e: (e[0], e[1], e[6]))
    out = lambda: {('%d-%02d' % mo, g): round(res.get((mo, g), 0.0), 2) for mo in DD_MONTHS for g in ('legacy', '2023')}
    if route == 'norepair':
        for cd, kind, mem, amt, ok, rep, ref, first in events:
            add((cd.year, cd.month), mem[0], amt)
        return out()
    if route == 'cracker':
        for cd, kind, mem, amt, ok, rep, ref, first in events:
            if ok: add((cd.year, cd.month), mem[0], amt)
        return out()
    unpaid, last_fail, pending = {}, {}, {}
    for cd, kind, mem, amt, ok, rep, ref, first in events:
        if kind == 'A' and rep:
            cover = pending.pop(ref, [])
        else:
            cover = []
            for m in mem:
                owed = unpaid.pop(m, []) if route == 'golden' else last_fail.pop((ref, m), [])
                mo = (joined[m].year, joined[m].month) if first else month_for(m, cd)
                cover += [(m, x) for x in owed] + [(m, mo)]
        if ok:
            for (m, mo) in cover:
                add(mo, m, mfee[m])
            if route == 'full' and not (kind == 'A' and rep):
                cur = {(m, mo) for (m, mo) in cover if mo == month_for(m, cd) or first}
                extra = amt - sum(mfee[m] for (m, _) in cover) - admin * (len(cover) > len(cur))
                if extra > 0.005 and len(cover) == len(cur):
                    add(month_for(mem[0], cd), mem[0], extra)
        elif kind == 'A' and not rep:
            pending[ref] = cover
        else:
            for (m, mo) in cover:
                if route == 'golden':
                    unpaid.setdefault(m, []).append(mo)
                else:
                    last_fail.setdefault((ref, m), []).append(mo)
    return out()
