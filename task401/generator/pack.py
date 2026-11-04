"""task401 pack: renders the world (world.py) into Wrenford Leisure Trust's own records under target/, with its own
random stream (the world's weekly states are never re-drawn). Called by build.py."""
import os, uuid, calendar
from datetime import date, datetime, timedelta
import numpy as np
import pandas as pd
import pyarrow as pa, pyarrow.parquet as pq
import world as W
import docs

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
EXTRACT = date(2026, 3, 16)
CENTRES = ['Central', 'Ashgrove', 'Northgate', 'Brookvale', 'Cottam Road', 'Elmstead', 'Westcroft', 'Glenmoor', 'Hatherley']
HOURS_CENTRES = (CENTRES[2], CENTRES[6])
FEES = {'L-ADULT': 34.00, 'L-OFFPEAK': 26.50, 'L-CONC': 22.00,
        'FLEX-ADULT': 38.50, 'FLEX-OFFPEAK': 29.00, 'FLEX-CONC': 24.50, 'FLEX-STUDENT': 25.00}
ADMIN_CHARGE = 5.00
CASUAL = {'Adult Swim': 5.20, 'Junior Swim': 3.10, 'Senior Swim': 3.60, 'Gym Pass': 7.50, 'Swim & Gym': 9.40,
          'Family Swim 1+2': 9.90, 'Family Swim 1+3': 12.20, 'Family Swim 2+2': 14.50, 'Family Swim 2+3': 16.80}
PARTY = {'Family Swim 1+2': 3, 'Family Swim 1+3': 4, 'Family Swim 2+2': 4, 'Family Swim 2+3': 5}
BUREAU_SWITCH = date(2025, 12, 1)
EPOS_LIVE = {c: (date(2025, 11, 1) if c in HOURS_CENTRES else date(2025, 12, 1)) for c in CENTRES}
HOLIDAYS = {date(2025, 8, 25), date(2025, 12, 25), date(2025, 12, 26), date(2026, 1, 1), date(2026, 4, 3)}
DD_SEED, TILL_SEED = 10, 0       # the asks' own random streams (searched for mid-bin figures)
ASK_MONTHS = [(2025, 10), (2025, 11), (2025, 12), (2026, 1), (2026, 2)]
DD_MONTHS = [(2025, 11), (2025, 12), (2026, 1), (2026, 2)]


def wdate(w): return W.W0 + timedelta(days=7 * int(w))
def working(d): return d.weekday() < 5 and d not in HOLIDAYS
def next_working(d):
    while not working(d): d += timedelta(days=1)
    return d
def prev_working(d):
    d -= timedelta(days=1)
    while not working(d): d -= timedelta(days=1)
    return d
def add_working(d, n):
    for _ in range(n):
        d += timedelta(days=1)
        while not working(d): d += timedelta(days=1)
    return d
def plus_month(d):
    y, m = (d.year + (d.month == 12), d.month % 12 + 1)
    return date(y, m, min(d.day, calendar.monthrange(y, m)[1]))
def uid(rng): return str(uuid.UUID(bytes=rng.integers(0, 256, 16, dtype=np.uint8).tobytes(), version=4))


def write_parquet(df, path):
    tbl = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(tbl, path, compression='snappy', version='2.6')
    b = open(path, 'rb').read()
    flen = int.from_bytes(b[-8:-4], 'little'); foot = b[-8 - flen:-8]
    i = foot.find(b'parquet-cpp-arrow version')
    new = b'parquet-mr version 1.12.3 (build f8dced182c4c1fbdec6ccb3185537b5a01e6ed6b)'
    foot2 = foot[:i - 1] + bytes([len(new)]) + new + foot[i + foot[i - 1]:]
    open(path, 'wb').write(b[:-8 - flen] + foot2 + len(foot2).to_bytes(4, 'little') + b'PAR1')


def members(out, at, rng, faker):
    """The membership register: every membership on the books at any time from 1 January 2024 to the extract."""
    M = len(at['jw']); cw = out['all']['cancel_w']
    keep = np.flatnonzero(at['jw'] <= W.CUT - 1)
    jday = rng.integers(0, 7, M)
    joined = {int(i): wdate(at['jw'][i]) + timedelta(days=int(jday[i])) for i in keep}
    order = sorted(keep, key=lambda i: (joined[int(i)], int(i)))
    num, n = {}, 3125
    for i in order:
        n += 1 + int(rng.random() < 0.03); num[int(i)] = '%06d' % n
    rows = []
    for i in order:
        i = int(i); u = rng.random()
        if at['legacy'][i]:
            tariff = 'L-CONC' if (at['old'][i] and u < 0.7) else ('L-ADULT' if u < 0.72 else 'L-OFFPEAK')
        elif at['old'][i] and u < 0.7:
            tariff = 'FLEX-CONC'
        else:
            tariff = 'FLEX-ADULT' if u < 0.62 else ('FLEX-OFFPEAK' if u < 0.82 else 'FLEX-STUDENT')
        sex = 'F' if rng.random() < 0.54 else 'M'
        first = faker.first_name_female() if sex == 'F' else faker.first_name_male()
        age = int(rng.integers(65, 86)) if at['old'][i] else (int(rng.integers(18, 24)) if tariff == 'FLEX-STUDENT' else int(rng.integers(24, 65)))
        dob = date(2026 - age, 1, 1) + timedelta(days=int(rng.integers(0, 365)))
        acct = ''
        if not at['legacy'][i] and at['jw'][i] + 13 <= W.WA - 1 and cw[i] >= at['jw'][i] + 13:
            acct = (wdate(at['jw'][i] + 13) + timedelta(days=int(rng.integers(0, 3)))).isoformat()
        rows.append(dict(idx=i, membership_no=num[i], first_name=first, surname=faker.last_name(), date_of_birth=dob.isoformat(),
                         joined=joined[i].isoformat(), tariff_code=tariff, home_centre=CENTRES[at['centre'][i]],
                         collection_day=min(joined[i].day, 28), rewards_account_opened=acct))
    return pd.DataFrame(rows), num, joined


def cancellations(out, at, reg, rng):
    """Requests received to the extract: three channels, a reason from the form's list, and some members asking twice."""
    cw = out['all']['cancel_w']; reason = out['all']['reason']; path = out['all']['path']
    num = dict(zip(reg.idx, reg.membership_no))
    rows, seq = [], {}
    for i in reg.idx:
        if cw[i] > W.CUT - 1: continue
        d = wdate(cw[i]) + timedelta(days=int(rng.choice(7, p=[.2, .18, .17, .16, .14, .1, .05])))
        if d >= EXTRACT: d = EXTRACT - timedelta(days=1)
        ch = rng.choice(['Online form', 'Front desk', 'Telephone'], p=[.52, .27, .21] if path[i] != 2 else [.58, .12, .30])
        if ch == 'Front desk' and d.weekday() == 6: ch = 'Online form'
        hh = int(rng.integers(7, 23)) if ch == 'Online form' else int(rng.integers(9, 20))
        t = datetime(d.year, d.month, d.day, hh, int(rng.integers(0, 60)), int(rng.integers(0, 60)))
        r = W.REASONS[reason[i]] if reason[i] >= 0 else 'Other'
        yr = t.year % 100; seq[yr] = seq.get(yr, 0) + 1 + int(rng.random() < 0.02)
        rows.append(dict(request_ref='CR%02d-%05d' % (yr, seq[yr]), membership_no=num[i], received=t, channel=ch, reason=r,
                         membership_ends=plus_month(t.date()).isoformat()))
        if rng.random() < 0.06:
            t2 = t + timedelta(days=int(rng.integers(1, 6)), hours=int(rng.integers(0, 8)), minutes=int(rng.integers(0, 60)))
            if t2.date() < EXTRACT:
                ch2 = 'Telephone' if ch != 'Telephone' else 'Online form'
                yr2 = t2.year % 100; seq[yr2] = seq.get(yr2, 0) + 1
                rows.append(dict(request_ref='CR%02d-%05d' % (yr2, seq[yr2]), membership_no=num[i], received=t2, channel=ch2,
                                 reason=r if rng.random() < 0.8 else 'Other', membership_ends=plus_month(t.date()).isoformat()))
    df = pd.DataFrame(rows).sort_values(['received', 'request_ref']).reset_index(drop=True)
    df['received'] = df.received.dt.strftime('%Y-%m-%d %H:%M:%S')
    return df


def visits(out, at, reg, rng):
    """The access-control system's weekly usage export: one row per membership per week with any gate entry."""
    vis = out['all']['vis']
    idx = reg.idx.values
    num = np.empty(vis.shape[1], dtype=object); num[idx] = reg.membership_no.values
    sub = vis[:W.CUT, :][:, idx]
    ww, jj = np.nonzero(sub)
    v = sub[ww, jj].astype(int)
    m = idx[jj]
    entries = v + rng.binomial(v, 0.06)
    home = at['centre'][m]
    away = (np.isin(home, [2, 6]) & (ww >= W.WE) & (rng.random(len(m)) < W.P0['e_shift'] * 1.6)) | (rng.random(len(m)) < 0.04)
    cen = np.where(away, rng.choice(9, len(m), p=W.CENTRE_P), home)
    cen = np.where(away & (cen == home), (home + 1 + rng.integers(0, 8, len(m))) % 9, cen)
    df = pd.DataFrame({'membership_no': num[m], 'week_commencing': pd.to_datetime([wdate(w) for w in range(W.CUT)]).values[ww],
                       'centre': np.array(CENTRES)[cen], 'gate_entries': entries.astype(np.int16)})
    outage = (df.week_commencing == pd.Timestamp(2024, 11, 18)) & (df.centre == 'Brookvale')
    df = df[~outage].sort_values(['week_commencing', 'membership_no']).reset_index(drop=True)
    df['week_commencing'] = df.week_commencing.dt.date
    return df


def letters(out, at, reg, rng):
    cw = out['all']['cancel_w']
    on = reg[[bool(at['legacy'][i]) and cw[i] >= W.WD for i in reg.idx]].copy()
    on = on.sort_values('membership_no').reset_index(drop=True)
    n = len(on); cuts = np.linspace(0, n, 6).astype(int)
    rows = []
    for b in range(5):
        for k in range(cuts[b], cuts[b + 1]):
            posted = date(2026, 2, 2) + timedelta(days=b)
            ret = ''
            if rng.random() < 0.028:
                ret = add_working(posted, int(rng.integers(3, 12))).isoformat()
            rows.append(dict(membership_no=on.membership_no[k], batch='LT-%d' % (b + 1), posted=posted.isoformat(),
                             returned_undelivered=ret))
    return pd.DataFrame(rows)


def calls(out, at, reg, rng):
    num = dict(zip(reg.idx, reg.membership_no)); rows = []
    for w, cand in out['all']['calls']:
        if w >= W.CUT: break
        for i in sorted(cand, key=lambda i: num.get(int(i), '')):
            i = int(i)
            if i not in num: continue
            d = wdate(w) + timedelta(days=int(rng.choice(5, p=[.24, .22, .2, .19, .15])))
            t = datetime(d.year, d.month, d.day, int(rng.integers(10, 19)), int(rng.integers(0, 60)), int(rng.integers(0, 60)))
            rows.append(dict(called_at=t.strftime('%d/%m/%Y %H:%M:%S'), member=str(int(num[i])),
                             outcome=rng.choice(['Answered', 'Voicemail', 'No answer', 'Number not recognised'], p=[.38, .32, .25, .05]),
                             agent=rng.choice(['KH', 'DM', 'RT', 'SB'], p=[.3, .28, .24, .18])))
    df = pd.DataFrame(rows)
    df['_t'] = pd.to_datetime(df.called_at, format='%d/%m/%Y %H:%M:%S')
    return df.sort_values('_t').drop(columns='_t').reset_index(drop=True)


DAY_CLASSES = ['Aqua Fit', 'Gentle Yoga', 'Pilates', 'Strength and Balance', 'Low Impact Aerobics', 'Chair Pilates']
EVE_CLASSES = ['Spin', 'Body Pump', 'HIIT', 'Zumba', 'Yoga Flow', 'Boxfit', 'Aqua Fit', 'Circuit Training']


def bookings(out, at, reg, rng):
    """The class booking system from 7 October 2024: weekday daytime classes are booked by the daytime class users only."""
    vis = out['all']['vis']; num = reg.set_index('idx').membership_no
    w0 = W.wk(date(2024, 10, 7))
    evening_users = (~at['classday']) & (rng.random(len(at['jw'])) < 0.3)
    rows = []
    for w in range(w0, W.CUT):
        act = np.flatnonzero(vis[w] > 0)
        act = act[np.isin(act, reg.idx.values)]
        for i in act:
            if at['classday'][i]:
                p = 0.88 if w < W.WC else 0.72
                if rng.random() < p:
                    day = int(rng.integers(0, 5)); hh = int(rng.choice([9, 10, 11, 13, 14])); mm = int(rng.choice([0, 15, 30]))
                    cen = at['centre'][i] if rng.random() < 0.9 else int(rng.integers(0, 9))
                    rows.append((i, cen, DAY_CLASSES[int(rng.integers(0, 6))], wdate(w) + timedelta(days=day), hh, mm))
            elif evening_users[i] and rng.random() < 0.45:
                day = int(rng.integers(0, 7))
                hh = int(rng.choice([17, 18, 19, 20])) if day < 5 else int(rng.choice([8, 9, 10, 11]))
                rows.append((i, at['centre'][i], EVE_CLASSES[int(rng.integers(0, 8))], wdate(w) + timedelta(days=day), hh,
                             int(rng.choice([0, 15, 30, 45]))))
    out_rows = []
    for k, (i, cen, cls, d, hh, mm) in enumerate(rows):
        st = rng.choice(['Attended', 'No-show', 'Cancelled'], p=[.84, .07, .09])
        out_rows.append(dict(booking_id=7310000 + 3 * k + int(rng.integers(0, 3)), membership_no=num.loc[i], centre=CENTRES[cen], class_name=cls,
                             session_start=datetime(d.year, d.month, d.day, hh, mm), status=st))
    df = pd.DataFrame(out_rows).sort_values(['session_start', 'centre', 'class_name', 'membership_no']).reset_index(drop=True)
    return df[df.session_start < pd.Timestamp(EXTRACT)].reset_index(drop=True)


def households(reg, cw, rng):
    """Memberships paid from another member's account, among members on the books from September 2025 to the extract
    with no request to leave; a quarter of the households mix a legacy and a 2023 tariff."""
    ok = reg[(pd.to_datetime(reg.joined) < pd.Timestamp(2025, 9, 1)) & np.array([cw[i] > W.CUT - 1 for i in reg.idx])]
    pool = ok.iloc[rng.permutation(len(ok))].reset_index(drop=True)
    grp = dict(zip(pool.membership_no, pool.tariff_code.str[:2]))
    leg = [m for m in pool.membership_no if grp[m] == 'L-'][:310]
    flex = [m for m in pool.membership_no if grp[m] == 'FL'][:310]
    pairs = [((a, b) if rng.random() < 0.6 else (b, a)) for a, b in zip(leg, flex)]
    used = set(leg) | set(flex)
    rest = [m for m in pool.membership_no if m not in used]
    k = 0
    while len(pairs) < 1240 and k + 1 < len(rest):
        a, b = rest[k], rest[k + 1]; k += 2
        if grp[a] == grp[b]: pairs.append((a, b))
    return {payee: payer for payer, payee in pairs}


def dd(reg, canc, house, rng):
    """Collections due from October 2025 to the extract. Bureau A to the end of November: one line per membership, dated
    by its BACS processing day, in pence; a returned collection is re-presented once, ten working days later. Bureau B from
    1 December: one line per mandate, a household's memberships in one collection, dated by the collection day. Whatever
    is still unpaid after a return (B) or a failed re-presentation (A) is added to the membership's next collection, with
    the administration charge for each failure, through whichever bureau takes it."""
    first_req = canc.groupby('membership_no').received.min()
    ends = {m: plus_month(datetime.strptime(t, '%Y-%m-%d %H:%M:%S').date()) for m, t in first_req.items()}
    R = reg.set_index('membership_no')
    payer_of = lambda m: house.get(m, m)
    sched = []
    for m, r in R.iterrows():
        j = date.fromisoformat(r.joined); fee = FEES[r.tariff_code]; end = ends.get(m, date(2026, 12, 31))
        day = int(R.loc[house[m]].collection_day) if m in house else int(r.collection_day)
        for (y, mo) in ASK_MONTHS + [(2026, 3)]:
            if (y, mo) < (j.year, j.month): continue
            first = (y, mo) == (j.year, j.month)
            cd = next_working(j) if first else next_working(date(y, mo, day))
            if cd >= end or cd >= EXTRACT or cd < date(2025, 10, 1): continue
            sched.append((m, (y, mo), cd, fee, first))
    payers = [m for m in sorted(R.index) if payer_of(m) == m]
    refs = rng.choice(np.arange(1000000, 9999999), size=len(payers), replace=False)
    mand = {m: 'WRF%07d' % int(x) for m, x in zip(payers, refs)}
    groups = {}
    for s in sched:
        key = payer_of(s[0]) if s[2] >= BUREAU_SWITCH else s[0]
        groups.setdefault((s[2], key), []).append(s)
    A_rows, B_rows, ret, paid = [], [], [], {}
    owed = {}     # membership -> list of ((membership, month), fee) still unpaid
    fails = {}    # membership -> failures not yet charged
    def code(): return '0'
    for (cd, key), items in sorted(groups.items()):
        if cd < BUREAU_SWITCH:
            for (m, mon, _, fee, first) in items:
                pdte = prev_working(cd); ref = 'WLT/%s' % m
                ow = owed.pop(m, []); fl = fails.pop(m, 0)
                amt = fee + sum(f for (_, f) in ow) + ADMIN_CHARGE * fl
                A_rows.append(dict(processing_date=pdte, payer_reference=ref, amount_pence=int(round(amt * 100)),
                                   transaction_code='01' if first else '17', _m=m))
                due = ow + [((m, mon), fee)]
                if rng.random() >= 0.025:
                    for (mm, _) in due: paid[mm] = True
                    continue
                c1 = code()
                ret.append(dict(bureau='A', reference=ref, amount=round(amt, 2), original_date=pdte, returned=add_working(cd, 2), reason_code=c1))
                if c1 != '0':
                    continue
                rp = add_working(pdte, 10)
                A_rows.append(dict(processing_date=rp, payer_reference=ref, amount_pence=int(round(amt * 100)), transaction_code='18', _m=m))
                if rng.random() < 0.85 and add_working(rp, 1) < EXTRACT:
                    for (mm, _) in due: paid[mm] = True
                else:
                    ret.append(dict(bureau='A', reference=ref, amount=round(amt, 2), original_date=rp, returned=add_working(rp, 3), reason_code='0'))
                    owed[m] = due; fails[m] = fl + 1
        else:
            ref = mand[key]
            due, fl, amt = [], 0, 0.0
            for (m, mon, _, fee, _) in items:
                ow = owed.pop(m, []); f0 = fails.pop(m, 0)
                due += ow + [((m, mon), fee)]; fl += f0
                amt += fee + sum(f for (_, f) in ow)
            amt += ADMIN_CHARGE * fl
            B_rows.append(dict(collection_date=cd, mandate_reference=ref, amount=round(amt, 2),
                               type='FIRST' if all(it[4] for it in items) else 'RECURRING'))
            if rng.random() < 0.025:
                c1 = code()
                ret.append(dict(bureau='B', reference=ref, amount=round(amt, 2), original_date=cd, returned=add_working(cd, 3), reason_code=c1))
                if c1 == '0':
                    for (m, mon, _, fee, _) in items:
                        owed[m] = [x for x in due if x[0][0] == m]
                    fails[items[0][0]] = fl + 1
            else:
                for (mm, _) in due: paid[mm] = True
    names = (R.first_name.str[0] + ' ' + R.surname).str.upper()
    A = pd.DataFrame(A_rows)
    A['payer_name'] = [names[payer_of(m)] for m in A._m]
    A = A.drop(columns='_m').sort_values(['processing_date', 'payer_reference', 'transaction_code']).reset_index(drop=True)
    A = A[['processing_date', 'payer_reference', 'payer_name', 'amount_pence', 'transaction_code']]
    B = pd.DataFrame(B_rows).sort_values(['collection_date', 'mandate_reference']).reset_index(drop=True)
    RT = pd.DataFrame(ret).sort_values(['returned', 'bureau', 'reference']).reset_index(drop=True)
    live = {payer_of(m) for (m, _, cd, _, _) in sched if cd >= BUREAU_SWITCH}
    MD = pd.DataFrame([dict(mandate_reference=mand[k], account_holder=(R.loc[k].first_name + ' ' + R.loc[k].surname).upper(),
                            membership_no=k, set_up=max(BUREAU_SWITCH, date.fromisoformat(R.loc[k].joined)).isoformat())
                       for k in sorted(live)]).sort_values('mandate_reference').reset_index(drop=True)
    return A, B, RT, MD, paid


def tills(rng):
    """Pay-as-you-go sales, 1 October 2025 to the extract. The old till: one line per ticket, a family ticket one line whose
    price is its party, a mis-keyed sale voided by a negative line, a pool closure's swimmers given a free-swim voucher
    (a zero line). The new EPOS (Northgate and Westcroft from 1 November, the other seven from 1 December): one line per
    person and area, a Swim and Gym ticket two half-price lines, voids the same way, and a pool closure's swimmers
    refunded to their cards in negative lines. Pool closures are logged by the duty managers."""
    base = W.CENTRE_P / W.CENTRE_P.max() * 88
    prods = list(CASUAL)
    pp = np.array([.37, .14, .10, .14, .12, .03, .02, .05, .03]); pp = pp / pp.sum()
    season = {10: 1.0, 11: 0.96, 12: 0.78, 1: 1.12, 2: 1.04, 3: 1.0}
    dow = [0.92, 0.95, 0.94, 0.97, 0.9, 1.25, 1.2]
    hp = np.array([2, 5, 6, 7, 8, 9, 9, 8, 7, 7, 8, 9, 7, 5, 3, 1], float); hp /= hp.sum()
    site = {'Central': 'CEN', 'Ashgrove': 'ASH', 'Northgate': 'NGT', 'Brookvale': 'BRV', 'Cottam Road': 'CTR',
            'Elmstead': 'ELM', 'Westcroft': 'WCR', 'Glenmoor': 'GLM', 'Hatherley': 'HAT'}
    item_of = {'Adult Swim': 'POOL-ADULT', 'Junior Swim': 'POOL-JUNIOR', 'Senior Swim': 'POOL-SENIOR', 'Gym Pass': 'GYM-ADULT'}
    old, new, closures, truth = [], [], [], {}
    tx = 4100000
    d = date(2025, 10, 1)
    while d < EXTRACT:
        for c, cen in enumerate(CENTRES):
            lam = base[c] * season[d.month] * dow[d.weekday()]
            if cen in HOURS_CENTRES and d >= date(2026, 2, 9): lam *= 0.78
            if d == date(2025, 12, 25): lam = 0
            epos = d >= EPOS_LIVE[cen]
            sales = []
            for _ in range(int(rng.poisson(lam))):
                p = prods[int(rng.choice(len(prods), p=pp))]
                hh = int(rng.choice(np.arange(6, 22), p=hp))
                sales.append((datetime(d.year, d.month, d.day, hh, int(rng.integers(0, 60)), int(rng.integers(0, 60))), p))
            sales.sort()
            clo = None
            if lam > 0 and rng.random() < 4.2 / 30:
                st = datetime(d.year, d.month, d.day, int(rng.integers(10, 19)), int(rng.choice([0, 10, 20, 30, 40, 50])))
                clo = (st, st + timedelta(minutes=int(rng.choice([60, 90, 120, 150, 180]))))
                closures.append(dict(site=cen, date=d.isoformat(), closed_at=clo[0].strftime('%H:%M'), reopened_at=clo[1].strftime('%H:%M'),
                                     reason=str(rng.choice(['Faecal fouling', 'Plant failure', 'Lifeguard shortage', 'Vomit'], p=[.45, .2, .2, .15]))))
            for (t, p) in sales:
                people = PARTY.get(p, 1)
                if clo is not None and p != 'Gym Pass' and clo[0] <= t < clo[1]:
                    continue
                void = rng.random() < 0.008 and not (clo is not None and clo[0] - timedelta(minutes=8) <= t < clo[1])
                if not void:
                    truth[(d.year, d.month, cen)] = truth.get((d.year, d.month, cen), 0) + people
                pool = p != 'Gym Pass'
                hit = clo is not None and pool and (clo[0] - timedelta(minutes=120)) <= t < clo[0] and not void
                if not epos:
                    name = 'Family Swim' if p.startswith('Family') else p
                    old.append(dict(sold=t, site=cen, product=name, price=CASUAL[p], tender='Card' if rng.random() < 0.83 else 'Cash'))
                    if void:
                        old.append(dict(sold=t + timedelta(minutes=int(rng.integers(1, 4))), site=cen, product=name, price=-CASUAL[p], tender='Card'))
                    if hit:
                        old.append(dict(sold=clo[0] + timedelta(minutes=int(rng.integers(2, 35))), site=cen, product='Free swim voucher', price=0.0, tender=''))
                    continue
                tx += 1 + int(rng.integers(0, 3))
                lines = []
                if p.startswith('Family'):
                    cents = int(round(CASUAL[p] * 100)); per = [cents // people + (1 if k < cents % people else 0) for k in range(people)]
                    lines = [('POOL-FAMILY', per[k] / 100) for k in range(people)]
                elif p == 'Swim & Gym':
                    lines = [('POOL-ADULT', 4.70), ('GYM-ADULT', 4.70)]
                else:
                    lines = [(item_of[p], CASUAL[p])]
                for k, (it, a) in enumerate(lines):
                    new.append(dict(transaction=tx, timestamp=t + timedelta(seconds=k), site_code=site[cen], item=it, amount=a))
                if void:
                    tx += 1
                    tv = t + timedelta(minutes=int(rng.integers(1, 4)), seconds=int(rng.integers(0, 60)))
                    for k, (it, a) in enumerate(lines):
                        new.append(dict(transaction=tx, timestamp=tv + timedelta(seconds=k), site_code=site[cen], item=it, amount=-a))
                if hit:
                    tx += 1
                    tr = clo[0] + timedelta(minutes=int(rng.integers(2, 35)), seconds=int(rng.integers(0, 60)))
                    for k, (it, a) in enumerate(lines):
                        if it.startswith('POOL'):
                            new.append(dict(transaction=tx, timestamp=tr + timedelta(seconds=k), site_code=site[cen], item=it, amount=-a))
        d += timedelta(days=1)
    O = pd.DataFrame(old).sort_values(['sold', 'site', 'price']).reset_index(drop=True)
    O['sold'] = O.sold.dt.strftime('%d/%m/%Y %H:%M')
    N = pd.DataFrame(new).sort_values(['timestamp', 'transaction']).reset_index(drop=True)
    N['timestamp'] = N.timestamp.dt.strftime('%Y-%m-%dT%H:%M:%S')
    PC = pd.DataFrame(closures).sort_values(['date', 'closed_at', 'site']).reset_index(drop=True)
    return O, N, PC, truth, site


def xlsx(path, sheets, author, created, modified, stamp):
    with pd.ExcelWriter(path, engine='openpyxl') as xw:
        for name, df in sheets:
            df.to_excel(xw, sheet_name=name, index=False)
            ws = xw.sheets[name]
            for col in ws.columns:
                ws.column_dimensions[col[0].column_letter].width = max(10, min(46, max(len(str(c.value or '')) for c in col[:200]) + 2))
    docs.scrub_xlsx(path, author, created, modified, stamp)


def price_list(path):
    mem = pd.DataFrame([dict(tariff_code=k, description=v, monthly_fee=FEES[k]) for k, v in [
        ('FLEX-ADULT', 'Flex adult, all centres, any time'), ('FLEX-OFFPEAK', 'Flex adult, weekdays before 4pm and weekends'),
        ('FLEX-CONC', 'Flex concession (60 and over, or Wrenford Leisure Card)'), ('FLEX-STUDENT', 'Flex student (full-time, with ID)'),
        ('L-ADULT', 'Legacy adult (closed to new members January 2023)'), ('L-OFFPEAK', 'Legacy off-peak (closed January 2023)'),
        ('L-CONC', 'Legacy concession (closed January 2023)')]])
    cas = pd.DataFrame([dict(ticket=k, price=v, admits=('1 adult and 2 children' if k.endswith('1+2') else '1 adult and 3 children'
                             if k.endswith('1+3') else '2 adults and 2 children' if k.endswith('2+2') else '2 adults and 3 children'
                             if k.endswith('2+3') else '1 person')) for k, v in CASUAL.items()])
    chg = pd.DataFrame([dict(charge='Failed Direct Debit administration charge', amount=ADMIN_CHARGE),
                        dict(charge='Replacement membership card', amount=5.00), dict(charge='Locker key not returned', amount=10.00)])
    xlsx(path, [('Memberships', mem), ('Pay as you go', cas), ('Charges', chg)], 'Finance', '2025-01-20T10:15:00Z',
         '2025-01-27T16:40:00Z', (2025, 1, 27, 16, 40, 0))


def survey(path, rng):
    n = 2214; rows = []
    d0 = date(2025, 10, 13)
    for k in range(n):
        cen = CENTRES[int(rng.choice(9, p=W.CENTRE_P))]
        g = 'Legacy' if rng.random() < 0.3 else '2023 tariff'
        sat = int(np.clip(round(rng.normal(7.4 if g == 'Legacy' else 7.0, 1.7)), 1, 10))
        rec = int(np.clip(round(sat + rng.normal(-0.4, 1.4)), 0, 10))
        rows.append(dict(response_id=uid(rng), completed=(d0 + timedelta(days=int(rng.integers(0, 28)))).isoformat(), centre=cen,
                         tariff_group=g, overall_satisfaction=sat, likely_to_recommend=rec,
                         cleanliness=int(np.clip(round(rng.normal(3.9, 0.8)), 1, 5)), staff=int(np.clip(round(rng.normal(4.2, 0.7)), 1, 5)),
                         value_for_money=int(np.clip(round(rng.normal(3.4 if g == 'Legacy' else 3.1, 0.9)), 1, 5))))
    df = pd.DataFrame(rows).sort_values(['completed', 'response_id']).reset_index(drop=True)
    xlsx(path, [('Responses', df)], 'Insight', '2025-11-14T09:00:00Z', '2025-11-17T12:25:00Z', (2025, 11, 17, 12, 25, 0))


def offers(path):
    df = pd.DataFrame([
        dict(month='2025-04', offer='Half-price first month on Flex adult', code='SPRING25', channel='Online and reception'),
        dict(month='2025-06', offer='Free guest pass with every new membership', code='SUMMERGUEST', channel='Online'),
        dict(month='2025-09', offer='No joining fee', code='SEPT0', channel='Online and reception'),
        dict(month='2025-11', offer='Student rate extended to apprentices', code='APPR25', channel='Reception'),
        dict(month='2026-01', offer='No joining fee and a free induction', code='NEWYEAR26', channel='Online and reception'),
        dict(month='2026-02', offer='Refer a friend: GBP 10 cafe credit each', code='FRIEND26', channel='Online')])
    xlsx(path, [('Offers', df)], 'Marketing', '2025-03-24T10:00:00Z', '2026-01-28T15:10:00Z', (2026, 1, 28, 15, 10, 0))


def write_all(out, at):
    from faker import Faker
    faker = Faker('en_GB'); faker.seed_instance(401018)
    rng = np.random.default_rng(401018)
    os.makedirs(T, exist_ok=True)
    for f in os.listdir(T):
        os.remove(os.path.join(T, f))
    reg, num, joined = members(out, at, rng, faker)
    cw = out['all']['cancel_w']
    canc = cancellations(out, at, reg, rng)
    rdd = np.random.default_rng(401018 * 3 + DD_SEED)
    house = households(reg, cw, rdd)
    reg['paid_by_membership_no'] = reg.membership_no.map(house).fillna('')
    first = canc.groupby('membership_no').received.min()
    ends = canc.groupby('membership_no').membership_ends.min()
    reg['status'] = ['Active' if m not in first.index else ('Notice given' if ends[m] >= EXTRACT.isoformat() else 'Ended') for m in reg.membership_no]
    reg['membership_ends'] = [ends.get(m, '') for m in reg.membership_no]
    files = {}
    R = reg.drop(columns='idx').sort_values('membership_no')
    R = R[['membership_no', 'first_name', 'surname', 'date_of_birth', 'joined', 'tariff_code', 'home_centre', 'collection_day',
           'paid_by_membership_no', 'rewards_account_opened', 'status', 'membership_ends']]
    files['membership_register_2026-03-16.csv'] = R
    R.to_csv(os.path.join(T, 'membership_register_2026-03-16.csv'), index=False)
    V = visits(out, at, reg, rng)
    write_parquet(V, os.path.join(T, 'access_weekly_usage_2024-01-01_to_2026-03-15.parquet'))
    canc.to_csv(os.path.join(T, 'cancellation_requests_2024-01-01_to_2026-03-15.csv'), index=False)
    L = letters(out, at, reg, rng)
    xlsx(os.path.join(T, 'legacy_terms_letters_2026-02.xlsx'), [('Letters', L)], 'Membership Services', '2026-02-02T08:30:00Z',
         '2026-02-27T15:05:00Z', (2026, 2, 27, 15, 5, 0))
    C = calls(out, at, reg, rng)
    C.to_csv(os.path.join(T, 'member_care_calls_2026-02-16_to_2026-03-13.csv'), index=False)
    BK = bookings(out, at, reg, rng)
    write_parquet(BK, os.path.join(T, 'class_bookings_2024-10-07_to_2026-03-15.parquet'))
    A, B, RT, MD, paid = dd(reg.drop(columns='idx'), canc, house, rdd)
    a0, a1 = A.processing_date.min(), A.processing_date.max()
    A2 = A.copy(); A2['processing_date'] = [d.strftime('%d/%m/%Y') for d in A2.processing_date]
    A2.to_csv(os.path.join(T, 'dd_bureau_A_submissions_%s_to_%s.csv' % (a0.isoformat(), a1.isoformat())), index=False)
    B2 = B.copy(); B2['collection_date'] = [d.isoformat() for d in B2.collection_date]
    B2.to_csv(os.path.join(T, 'dd_collections_%s_to_%s.csv' % (B.collection_date.min().isoformat(), B.collection_date.max().isoformat())), index=False)
    MD.to_csv(os.path.join(T, 'dd_mandates_2026-03-16.csv'), index=False)
    RT2 = RT.copy()
    for c in ('original_date', 'returned'): RT2[c] = [d.isoformat() for d in RT2[c]]
    RT2.to_csv(os.path.join(T, 'bacs_returns_%s_to_%s.csv' % (RT.returned.min().strftime('%Y-%m'), RT.returned.max().strftime('%Y-%m'))), index=False)
    O, N, PC, till_truth, site = tills(np.random.default_rng(401018 * 5 + TILL_SEED))
    O.to_csv(os.path.join(T, 'till_sales_old_system_2025-10-01_to_2025-11-30.csv'), index=False)
    PC.to_csv(os.path.join(T, 'pool_closures_2025-10-01_to_2026-03-15.csv'), index=False)
    N.to_csv(os.path.join(T, 'epos_sales_2025-11-01_to_2026-03-15.csv'), index=False)
    price_list(os.path.join(T, 'price_list_2025-26.xlsx'))
    docs.contract_schedule(os.path.join(T, 'operating_contract_schedule_4.pdf'))
    docs.savings_programme(os.path.join(T, 'savings_programme_2025-26.docx'))
    docs.membership_terms(os.path.join(T, 'membership_terms_2025-26.pdf'))
    docs.bureau_letter(os.path.join(T, 'direct_debit_bureau_change_2025-11.pdf'))
    docs.epos_notice(os.path.join(T, 'epos_go_live_notice_2025-10.docx'), site)
    survey(os.path.join(T, 'member_survey_autumn_2025.xlsx'), rng)
    offers(os.path.join(T, 'joining_offers_2025-26.xlsx'))
    return dict(reg=reg, house=house, paid=paid, till_truth=till_truth)
