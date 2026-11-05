"""Render the pack's data files from the world, each in the producing system's own idiom."""
import datetime as dt
import numpy as np, pandas as pd
import pyarrow as pa, pyarrow.parquet as pq
from collections import defaultdict
from core import Q, DAY, WEEK

T0 = dt.datetime(2026, 7, 1, 0, 0, 0)
ALNUM = '23456789ABCDEFGHJKLMNPQRSTUVWXYZ'
CUR = {'NG': 'NGN', 'GH': 'GHS', 'KE': 'KES', 'GB': 'GBP'}
RATE = {'NG': (1532.0, 1611.0), 'GH': (15.18, 16.42), 'KE': (128.6, 130.4), 'GB': (0.7362, 0.7791)}


def utc(t):
    return (T0 + dt.timedelta(minutes=float(t))).strftime('%Y-%m-%dT%H:%M:%SZ')


def wat(t):
    return (T0 + dt.timedelta(minutes=float(t) + 60)).strftime('%Y-%m-%d %H:%M:%S')


def ms(t):
    return int(round((T0 - dt.datetime(1970, 1, 1)).total_seconds() * 1000 + float(t) * 60000))


def day_of(t):
    return (T0 + dt.timedelta(minutes=float(t))).date()


def write_parquet(df, path):
    tbl = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(tbl, path, compression='zstd', compression_level=9, write_statistics=False)


def ids(rng, n, lo, hi):
    out = set()
    while len(out) < n:
        out.update(int(x) for x in rng.integers(lo, hi, n - len(out)))
    return list(rng.permutation(sorted(out)))


def render(w, x, seed, target):
    """w: core world; x: extras. Returns the key maps the golden and checks need."""
    rng = np.random.default_rng(seed * 104729 + 5)
    A, T, X = x['A'], x['T'], x['X']
    kind, sub, market = A.kind.to_dict(), A['sub'].to_dict(), A.market.to_dict()
    acct_id = dict(zip(A.id, ['CXA%07d' % v for v in ids(rng, len(A), 1_000_000, 9_999_999)]))
    agents_tab = {ag: tab for ag, tab, custs in w['agents']}

    # --- escrow: one export per month of creation, pulled on the 3rd of the next month ---------------------------
    mt = [d for d in x['ret'].itertuples(index=False)]
    rows = []
    def method(s, b):
        mk = market[s]
        if sub.get(s) == 'agent': return 'cash_at_point'
        if mk == 'NG': return 'bank_transfer' if rng.random() < 0.7 else 'mobile_money'
        if mk == 'GH': return 'mobile_money' if rng.random() < 0.8 else 'bank_transfer'
        if mk == 'KE': return 'mobile_money' if rng.random() < 0.9 else 'bank_transfer'
        return 'faster_payments'
    onos = set()
    def ono():
        while True:
            o = 'CX' + ''.join(rng.choice(list(ALNUM), 8))
            if o not in onos:
                onos.add(o); return o
    order_of = {}
    ring = set(w['ring_of'])
    co = x['created_override']
    for tid, s, b, amt, t in zip(T.tid, T.seller, T.buyer, T.amt, T.t):
        lag = float(rng.uniform(5, 20)) if s in ring else float(rng.uniform(4, 48))
        rows.append((tid, s, b, amt, co.get(int(tid), t - lag), t, 'released'))
    for r in x['ret'].itertuples(index=False):
        rows.append((r.tid, r.seller, r.buyer, r.amt, r.created, r.t, 'returned'))
    for r in x['cnx'].itertuples(index=False):
        rows.append((r.tid, r.seller, r.buyer, r.amt, r.created, r.t, 'cancelled'))
    E = pd.DataFrame(rows, columns=['tid', 'seller', 'buyer', 'amt', 'created', 'closed', 'status']).sort_values('created', kind='stable')
    E['order_no'] = [ono() for _ in range(len(E))]
    order_of = dict(zip(E.tid, E.order_no))
    lo_hi = {mk: v for mk, v in RATE.items()}
    E['mk'] = E.seller.map(market)
    E['method'] = [method(s, b) for s, b in zip(E.seller, E.buyer)]
    r_ = rng.uniform(0, 1, len(E))
    rate = np.array([lo_hi[m][0] + (lo_hi[m][1] - lo_hi[m][0]) * (0.5 + 0.5 * np.sin(c / (9 * DAY))) for m, c in zip(E.mk, E.created)])
    E['fiat'] = np.round(E.amt.values * rate * (1.004 + 0.016 * r_), 2)
    E['fee'] = np.where(E.method == 'cash_at_point', 0.0, np.round(E.amt.values * 0.01, 6))
    E['seller_h'] = [x['handle_at'](s, c) for s, c in zip(E.seller, E.created)]
    E['buyer_h'] = [x['handle_at'](b, c) for b, c in zip(E.buyer, E.created)]
    E['month'] = [day_of(c).month if c >= 0 else 6 for c in E.created]
    for mo in (7, 8, 9):
        m = E[E.month == mo]
        rel = 'released_at' if mo == 7 else 'settled_at'
        out = pd.DataFrame({
            'order_no': m.order_no, 'created_at': [utc(c) for c in m.created],
            rel: [utc(c) if st == 'released' else '' for c, st in zip(m.closed, m.status)],
            'closed_at': [utc(c) for c in m.closed],
            'status': m.status, 'seller': m.seller_h, 'buyer': m.buyer_h,
            'amount_usdt': ['%.6f' % a for a in m.amt], 'fiat_currency': m.mk.map(CUR),
            'fiat_amount': ['%.2f' % f for f in m.fiat], 'payment_method': m.method,
            'seller_fee_usdt': ['%.6f' % f for f in m.fee]})
        out.to_csv(target / ('escrow_orders_2026-%02d.csv' % mo), index=False, lineterminator='\n')

    # --- ratings service: a row per version ---------------------------------------------------------------------
    R = w['R'][w['R'].t < Q].copy().reset_index(drop=True)
    R = R[R.tid.isin(order_of)].sort_values('t', kind='stable').copy()
    rid = ids(rng, len(R), 40_000_000, 99_000_000)
    R['rating_id'] = sorted(rid)
    rows = []
    ringr = R.rater.isin(ring).values
    for (tid, rater, ratee, role, sc, t, rr), isring in zip(R[['tid', 'rater', 'ratee', 'role_ratee', 'score', 't', 'rating_id']].itertuples(index=False), ringr):
        rows.append((rr, order_of[tid], acct_id[rater], acct_id[ratee], role, int(sc), 1, t))
        if not isring and rng.random() < 0.05:
            sc2 = int(np.clip(sc + rng.choice([-10, -5, -3, -2, 2, 3, 5]), -10, 10))
            t2 = t + float(rng.uniform(10, 72 * 60 - 30))
            rows.append((rr, order_of[tid], acct_id[rater], acct_id[ratee], role, sc2, 2, t2))
            if rng.random() < 0.1:
                rows.append((rr, order_of[tid], acct_id[rater], acct_id[ratee], role,
                             int(np.clip(sc2 + rng.choice([-2, 2, 5]), -10, 10)), 3, t2 + float(rng.uniform(5, 600))))
    RV = pd.DataFrame(rows, columns=['rating_id', 'order_no', 'rater_account', 'ratee_account', 'ratee_role', 'score',
                                     'version', 'recorded_at'])
    RV = RV.sort_values(['recorded_at', 'rating_id', 'version'], kind='stable').reset_index(drop=True)
    RV['recorded_at'] = pd.to_datetime([T0 + dt.timedelta(minutes=float(t)) for t in RV.recorded_at]).as_unit('ms').tz_localize('UTC')
    write_parquet(RV, target / 'ratings_2026q3.parquet')

    # --- wallet ledger: Lagos wall-clock time, integer micro-USDT ------------------------------------------------
    wallet = x['wallet']
    rows = []
    for s, d_, a, t in zip(X.src, X.dst, X.amt, X.t):
        if 0 <= t < Q:
            rows.append((t, 'transfer', int(wallet[s]), int(wallet[d_]), int(round(a * 1e6)), 0, None, None))
    for r in x['deps'].itertuples(index=False):
        rows.append((r.t, 'deposit', int(wallet[r.acct]), None, int(round(r.amt * 1e6)), 0, r.network, r.address))
    for r in x['wds'][x['wds'].t < Q].itertuples(index=False):
        rows.append((r.t, 'withdrawal', int(wallet[r.acct]), None, int(round(r.amt * 1e6)), int(round(r.ufee * 1e6)), r.network, r.address))
    L = pd.DataFrame(rows, columns=['t', 'entry_type', 'wallet_no', 'counterparty_wallet_no', 'amount_micro', 'fee_micro',
                                    'network', 'chain_address']).sort_values('t', kind='stable').reset_index(drop=True)
    L['counterparty_wallet_no'] = L['counterparty_wallet_no'].astype('Int64')
    L.insert(0, 'entry_id', sorted(ids(rng, len(L), 7_100_000_000, 7_999_999_999)))
    L.insert(1, 'posted_at', pd.to_datetime([T0 + dt.timedelta(minutes=float(t) + 60) for t in L.t]).as_unit('s'))
    L = L.drop(columns='t')
    write_parquet(L, target / 'wallet_ledger_2026q3.parquet')

    # --- identity service: device links, one row per account, device and app generation ---------------------------
    D = w['D']
    first, last = x['first'], x['last']
    fp1, fp2, upg = {}, {}, {}
    def fps(dev):
        if dev not in fp1:
            fp1[dev] = ''.join(rng.choice(list('0123456789abcdef'), 16))
            fp2[dev] = 'k2' + ''.join(rng.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'), 20))
            upg[dev] = 21 * DAY + float(rng.uniform(0, 45)) * DAY if rng.random() < 0.93 else Q + DAY
        return fp1[dev], fp2[dev], upg[dev]
    rows = []
    for a, dev in zip(D.acct, D.dev):
        if a not in first: continue
        lo = max(0.0, first[a] - float(rng.uniform(0, 3)) * DAY)
        hi = min(Q - 1, last[a] + float(rng.uniform(0, 5)) * DAY)
        if hi <= lo: hi = min(Q - 1, lo + 60)
        f1, f2, u = fps(dev)
        if lo < u:
            e = min(hi, u)
            rows.append((acct_id[a], f1, '4.%d' % rng.integers(6, 9), ms(lo), ms(e), max(1, int((e - lo) / DAY * rng.uniform(0.2, 0.7)))))
        if hi > u:
            s_ = max(lo, u)
            rows.append((acct_id[a], f2, '5.%d' % rng.integers(0, 3), ms(s_), ms(hi), max(1, int((hi - s_) / DAY * rng.uniform(0.2, 0.7)))))
    DL = pd.DataFrame(rows, columns=['account_id', 'device_fingerprint', 'app_version', 'first_seen_ms', 'last_seen_ms', 'active_days'])
    DL = DL.sort_values(['first_seen_ms', 'account_id'], kind='stable').reset_index(drop=True)
    write_parquet(DL, target / 'device_links_2026q3.parquet')

    # --- account register and handle changes ------------------------------------------------------------------
    opened, status, closed = x['opened'], x['status'], x['closed_at']
    reissued_from = {a for a, b, wn in x['reissue']}
    reg = pd.DataFrame({
        'account_id': [acct_id[a] for a in A.id], 'handle': [x['handle_now'][a] for a in A.id],
        'wallet_no': ['' if (status[a] == 'closed' and a in reissued_from) or status[a] == 'closed' else wallet[a] for a in A.id],
        'market': [market[a] for a in A.id], 'kyc_tier': [x['tier'][a] for a in A.id],
        'opened_on': [(T0 + dt.timedelta(minutes=float(opened[a]))).date().isoformat() for a in A.id],
        'status': [status[a] for a in A.id],
        'closed_on': [(T0 + dt.timedelta(minutes=float(closed[a]))).date().isoformat() if a in closed else '' for a in A.id]})
    reg = reg.sort_values('opened_on', kind='stable').reset_index(drop=True)
    reg.to_csv(target / 'accounts.csv', index=False, lineterminator='\n')
    hc = pd.DataFrame([(acct_id[a], old, new, utc(t)) for a, old, new, t in x['renames']],
                      columns=['account_id', 'previous_handle', 'new_handle', 'changed_at']).sort_values('changed_at')
    hc.to_csv(target / 'handle_changes.csv', index=False, lineterminator='\n')

    # --- Calabash Points register ------------------------------------------------------------------------------
    towns = {'NG': ['Mushin', 'Oshodi', 'Ikorodu', 'Agege', 'Ojo', 'Aba', 'Onitsha', 'Kano', 'Ibadan', 'Ilorin', 'Nnewi'],
             'GH': ['Kasoa', 'Madina', 'Kumasi', 'Tema', 'Ashaiman', 'Tamale'], 'KE': ['Kibera', 'Kawangware', 'Thika', 'Nakuru', 'Eldoret', 'Kisumu']}
    pts = []
    for i, (ag, tab, custs) in enumerate(w['agents']):
        mk = market[ag]; f1, f2, u = fps(tab)
        town = towns[mk][rng.integers(len(towns[mk]))]
        shape = rng.integers(5)
        owner = rng.choice(['Mama Bisi', 'Alhaji Musa', 'Grace', 'Iya Ruka', 'Kofi', 'Auntie Esi', 'Brother Joe', 'Wanjiku', 'Otieno', 'Blessing'])
        nm = ['%s %s' % (town, rng.choice(['Mart', 'Phones', 'Ventures', 'Stores'])), '%s %s' % (owner, rng.choice(['POS', 'Phones & Accessories', 'Provisions'])),
              'No. %d %s Road' % (rng.integers(2, 120), town), '%s Calabash Point %d' % (town, rng.integers(1, 4)),
              '%s & Sons Enterprises' % owner.split()[-1]][shape]
        pts.append(('CP-%s-%03d' % (mk, rng.integers(100, 999)), nm,
                    town, mk, acct_id[ag], f1, f2 if u < Q else '', (T0 - dt.timedelta(days=int(rng.integers(60, 500)))).date().isoformat()))
    PT = pd.DataFrame(pts, columns=['point_code', 'point_name', 'town', 'market', 'agent_account_id', 'tablet_fingerprint',
                                    'tablet_fingerprint_v5', 'joined_on']).sort_values('joined_on')
    PT.to_csv(target / 'calabash_points.csv', index=False, lineterminator='\n')

    return dict(acct_id=acct_id, order_of=order_of, E=E, RV=RV, L=L, DL=DL, reg=reg, PT=PT, fp1=fp1, fp2=fp2)
