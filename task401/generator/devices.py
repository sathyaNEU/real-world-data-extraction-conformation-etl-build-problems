"""task401: the asks' second devices and the export realism pass, applied after pack.cut().

Every draw here comes from its own generator, so the main stream that cut() consumes (and with it every row of
the main call's population) is exactly what it was before this pass. Files touched here are rewritten whole.
  - phase 1 load log: validation failures fell on gas meter point data, so every reload chain is a dual fuel
    account; a few hundred electricity-only smart prepayment accounts, carried as credit on the legacy platform,
    were loaded in the nine batches and returned to the legacy platform days later (their legacy status was reset).
  - registrations: a gas registration raised again under its own reference only happens where the meter point was
    looked up from the address (web and comparison-site sales); broker sales are confirmed on a call by the phone
    team, which re-quotes when the customer changes tariff, and the pending registration is re-pointed at the new
    quote.
  - meter point annual quantities: held per register; two-rate meters on the prepayment book carry a day and a
    night register, and meters exchanged during 2026 for a single-rate smart meter carry a standard register from
    the exchange date while the old registers simply stop.
  - the 2026 survey export: version 4 response ids and completion times to the second.
"""
import csv, datetime as dt, io, json, os, uuid
import numpy as np
import pyarrow as pa, pyarrow.parquet as pq
import world as W

D = dt.date
SEED_B, SEED_C, SEED_A, SEED_T, SEED_O = 4011, 4012, 4013, 4014, 4015
N_ROLLED = {'Electricity': 300, 'Dual fuel': 110}
P_REPOINT = {3: 0.10, 0: 0.025, 1: 0.025}   # broker, direct web, comparison site
N_COT = 420
P_E7, P_EXCH = 0.22, 0.12
CREATED_BY = b'parquet-cpp version 1.5.1-SNAPSHOT'


def bst(d):
    def last_sun(y, m):
        x = D(y, m + 1, 1) - dt.timedelta(days=1)
        return x - dt.timedelta(days=(x.weekday() + 1) % 7)
    return 1 if last_sun(d.year, 3) <= d < last_sun(d.year, 10) else 0


def write_csv(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(header); w.writerows(rows)


class _Ids:
    """Fresh identifiers from a private generator, unique against everything the pack already issued."""
    def __init__(self, used, rng):
        self.used, self.rng = used, rng

    def draw(self, f):
        while True:
            v = f()
            if v not in self.used:
                self.used.add(v); return v

    def platform(self):
        return self.draw(lambda: '72%08d' % self.rng.integers(0, 10 ** 8))

    def quote(self):
        a = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        return self.draw(lambda: 'Q' + ''.join(a[k] for k in self.rng.integers(0, len(a), 9)))


# ---------------------------------------------------------------- Ask B: the phase 1 load log
def loads(out, U):
    rng = np.random.default_rng(W.SEED + SEED_B)
    ids = _Ids(U['ids'].used, rng)
    L = U['loads']
    # (1) reload chains belong to dual fuel accounts: a failure on the gas meter point's data
    chain_roots = {r['root'] for r in L if 'root' in r}
    for r in L:
        if r['legacy'] in chain_roots or r.get('root') in chain_roots:
            r['dual'] = True
    # (2) electricity-only smart prepayment accounts carried as credit: loaded, then returned to legacy
    accts = U['phase2_accts']
    lost_mp = {f[1] for f in U['flows']}
    pick, cand = [], []
    for fuel, n in sorted(N_ROLLED.items()):
        c = [k for k, a in enumerate(accts) if a[3] == fuel and a[4] == 'Live' and a[8] < '2025-06-01'
             and a[6] not in lost_mp and a[7] not in lost_mp and a[0] not in U['cot_old']]
        pick += [c[j] for j in sorted(rng.choice(len(c), n, replace=False))]
    cand = list(range(len(accts)))
    weeks = [W.PHASE1_START + dt.timedelta(days=7 * k) for k in range(9)]
    wshare = np.array([.06, .09, .12, .13, .12, .13, .12, .12, .11]); wshare /= wshare.sum()
    rolled = []
    for j in pick:
        a = accts[cand[j]]
        w = int(rng.choice(9, p=wshare))
        day = weeks[w] + dt.timedelta(days=int(rng.integers(0, 7)))
        hh = int(rng.choice([22, 23, 0, 1, 2, 3, 4], p=[.12, .2, .22, .18, .14, .09, .05]))
        local = dt.datetime.combine(day, dt.time(hh, int(rng.integers(0, 60)), int(rng.integers(0, 60))))
        if hh < 12:
            local += dt.timedelta(days=1)
        utc = local - dt.timedelta(hours=bst(local.date()))
        L.append(dict(load_id='', legacy=a[0], platform=ids.platform(), utc=utc, dual=a[3] == 'Dual fuel',
                      batch='P1-W%02d' % (w + 1)))
        back = local.date() + dt.timedelta(days=int(rng.integers(1, 7)))
        a[5] = back.isoformat()                          # the legacy record set live again on its return
        rolled.append(a[0])
    U['rolled_back'] = rolled
    # (3) the platform numbers its loads as they complete
    L.sort(key=lambda r: (r['utc'], r['legacy'], r['platform']))
    base_id = 208113
    for k, r in enumerate(L):
        r['load_id'] = 'L%07d' % (base_id + k * 3 + int(rng.integers(0, 3)))
    with open(os.path.join(out, 'phase1_migration_loads.jsonl'), 'w', encoding='utf-8') as f:
        for r in L:
            f.write(json.dumps({'load_id': r['load_id'], 'batch': r['batch'], 'legacy_account_ref': r['legacy'],
                                'platform_account_no': r['platform'], 'fuel_profile': 'DUAL' if r['dual'] else 'ELEC',
                                'completed_utc': r['utc'].strftime('%Y-%m-%dT%H:%M:%SZ')}, separators=(',', ':')) + '\n')
    U['phase2_accts'].sort(key=lambda r: r[0])
    write_csv(os.path.join(out, 'legacy_accounts_extract_2026-10-31.csv'),
              ['account_number', 'region', 'payment_method', 'fuel', 'account_status', 'status_date', 'mpan', 'mprn',
               'supply_start_date'], U['phase2_accts'])


# ---------------------------------------------------------------- Ask C: quotes and registrations
def sales(out, U):
    rng = np.random.default_rng(W.SEED + SEED_C)
    ids = _Ids(U['ids'].used, rng)
    J, table = U['J'], U['table']
    qrows, rrows = U['qrows'], U['rrows']
    qch = {r[0]: r[2] for r in qrows}
    live = {}
    wd = {r[0] for r in rrows if r[5] == 'Withdrawal'}
    for r in rrows:
        if r[5] == 'Registration' and r[0] not in wd:
            live.setdefault(r[4], []).append(r)
    # (1) a gas registration raised again under its own reference only follows an address lookup (web, comparison site)
    unsplit = 0
    for qref, rows in live.items():
        refs = sorted({r[0] for r in rows})
        if len(refs) > 1 and qch.get(qref) in ('Broker', 'Phone'):
            e = [r for r in rows if r[3] == 'Electricity'][0]
            for r in rows:
                if r[3] == 'Gas':
                    r[0], r[6] = e[0], e[6]
            unsplit += 1
    U['unsplit'] = unsplit
    # (2) broker sales re-quoted on the phone team's confirmation call; the pending registration follows the new quote
    idx = {q: i for i, q in enumerate(J['quote_ref'])}
    by_quote = {}
    for r in rrows:
        by_quote.setdefault(r[4], []).append(r)
    repointed = []
    order = sorted(live)
    for qref in order:
        i = idx.get(qref)
        if i is None or J['resp'][i] or int(J['t'][i]) != 1 or int(J['channel'][i]) not in P_REPOINT or U['rereg'][i]:
            continue
        rows = live[qref]
        if len({r[0] for r in rows}) > 1 or rng.random() >= P_REPOINT[int(J['channel'][i])]:
            continue
        reg_day = min(D.fromisoformat(r[6]) for r in rows)
        start = J['start'][i]
        hi = (start - reg_day).days - 3
        if hi < 3:
            continue
        q2day = reg_day + dt.timedelta(days=int(rng.integers(2, min(hi, 11))))
        if J['tariff'][i] == 'SVT':
            launch = max(l for l in W.FIX_LAUNCH if l <= q2day)
            t2 = 'FIX12-%s' % launch.strftime('%y%m')
        else:
            t2 = 'SVT'
        r2 = W.rates_for(table, t2, int(J['region'][i]), q2day)
        cost = W.cost_gbp(J['qe'][i], J['qg'][i], J['dual'][i], r2)
        q2 = ids.quote()
        qrows.append([q2, q2day.isoformat(), 'Phone', W.REGIONS[int(J['region'][i])][0], t2,
                      'Dual fuel' if J['dual'][i] else 'Electricity', int(J['qe'][i]),
                      int(J['qg'][i]) if J['dual'][i] else '', '%.2f' % cost, J['prospect'][i]])
        for r in by_quote[qref]:
            r[4] = q2
        repointed.append((qref, q2))
    U['repointed'] = repointed
    qrows.sort(key=lambda r: (r[1], r[0])); rrows.sort(key=lambda r: (r[6], r[0], r[3], r[5]))
    write_csv(os.path.join(out, 'quote_log_2024-06_2025-12.csv'),
              ['quote_ref', 'quote_date', 'channel', 'region', 'tariff_code', 'fuel', 'annual_kwh_electricity',
               'annual_kwh_gas', 'projected_annual_cost_gbp', 'prospect_ref'], qrows)
    write_csv(os.path.join(out, 'supply_registrations_2024-07_2025-12.csv'),
              ['registration_ref', 'account_number', 'meter_point', 'fuel', 'quote_ref', 'event', 'event_date',
               'supply_start_date'], rrows)


# ---------------------------------------------------------------- Ask A: register-level annual quantities
def scrub_parquet(path):
    """Replace the writer's signature in the footer with the warehouse export's own."""
    b = open(path, 'rb').read()
    flen = int.from_bytes(b[-8:-4], 'little'); start = len(b) - 8 - flen
    foot = b[start:-8]
    old = pq.read_metadata(path).created_by.encode()
    def varint(n):
        o = b''
        while True:
            x = n & 0x7f; n >>= 7
            if n:
                o += bytes([x | 0x80])
            else:
                return o + bytes([x])
    k = foot.find(varint(len(old)) + old)
    assert k >= 0 and foot.count(old) == 1
    foot = foot[:k] + varint(len(CREATED_BY)) + CREATED_BY + foot[k + len(varint(len(old))) + len(old):]
    open(path, 'wb').write(b[:start] + foot + len(foot).to_bytes(4, 'little') + b'PAR1')


def quantities(out, U):
    rng = np.random.default_rng(W.SEED + SEED_A)
    qty = U['qty_rows']
    e_mps = sorted({mp for _, _, _, mps in U['phase2_truth'] for f, mp in mps if f == 'E'})
    e7 = set(np.array(e_mps)[rng.random(len(e_mps)) < P_E7].tolist())
    byq = {}
    for r in qty:
        byq.setdefault(r[0], []).append(r)
    rows, exch = [], []
    asof_limit = D(2026, 10, 29)
    for mp in sorted(byq):
        rs = sorted(byq[mp], key=lambda r: r[3])
        if rs[0][1] == 'G':
            rows += [(m, 'G', None, q, d, s) for m, f, q, d, s in rs]
            continue
        if mp not in e7:
            rows += [(m, 'E', 'Standard', q, d, s) for m, f, q, d, s in rs]
            continue
        up = float(rng.lognormal(np.log(1.6), 0.12)); night = float(rng.uniform(0.55, 0.70))
        pre = [r for r in rs if r[3] <= D(2026, 10, 31)]
        x_day = None
        if pre and rng.random() < P_EXCH:
            cand = pre[-1][3] + dt.timedelta(days=int(rng.integers(20, 111)))
            if cand <= asof_limit:
                x_day = cand
        for m, f, q, d, s in rs:
            tot = q * up
            if x_day is not None and d >= x_day:
                rows.append((m, 'E', 'Standard', int(round(tot)), d, s))
            else:
                rows.append((m, 'E', 'Day', int(round(tot * (1 - night))), d, s))
                rows.append((m, 'E', 'Night', int(round(tot * night)), d, s))
        if x_day is not None:
            tot = pre[-1][2] * up * float(rng.lognormal(0, 0.05))
            rows.append((mp, 'E', 'Standard', int(round(tot)), x_day, 'Revision'))
            exch.append(mp)
    rk = {'Day': 0, 'Night': 1, 'Standard': 2, None: 3}
    rows.sort(key=lambda r: (r[0], r[4], rk[r[2]]))
    U['qty_reg_rows'], U['e7'], U['exchanged'] = rows, sorted(e7), exch
    tbl = pa.table({'meter_point': [r[0] for r in rows], 'fuel': [r[1] for r in rows],
                    'register': pa.array([r[2] for r in rows], pa.string()),
                    'annual_quantity_kwh': pa.array([r[3] for r in rows], pa.int32()),
                    'effective_from': pa.array([r[4] for r in rows], pa.date32()), 'source': [r[5] for r in rows]})
    path = os.path.join(out, 'meter_point_annual_quantities.parquet')
    pq.write_table(tbl, path, compression='snappy', store_schema=False)
    scrub_parquet(path)


# ---------------------------------------------------------------- the 2026 survey export
def survey_2026(out, U):
    rng = np.random.default_rng(W.SEED + SEED_T)
    rows = U['rows26']                                   # in the export's order: time, then the old id
    groups = {}
    for k, r in enumerate(rows):
        groups.setdefault((r[1], r[2]), []).append(k)
    for (acct, ts), ks in sorted(groups.items()):
        # an account that answered twice in the same minute keeps its answers in the order the export had them
        secs = sorted(rng.choice(60, len(ks), replace=False).tolist()) if len(ks) > 1 else [int(rng.integers(0, 60))]
        for k, sec in zip(ks, secs):
            r = rows[k]
            t = dt.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')
            if r[3] == '' and t.minute == 5:              # partial responses: minute and second
                t = t.replace(minute=int(rng.integers(0, 60)))
            r[2] = t.replace(second=sec).strftime('%Y-%m-%dT%H:%M:%SZ')
    for r in rows:
        r[0] = str(uuid.UUID(bytes=bytes(rng.integers(0, 256, 16, dtype=np.uint8).tolist()), version=4))
    rows.sort(key=lambda r: (r[2], r[0]))
    write_csv(os.path.join(out, 'survey_export_6m_2026-01-01_2026-06-30.csv'),
              ['response_id', 'account_number', 'completed_at', 'overall_satisfaction', 'bill_accuracy', 'bill_clarity',
               'value_for_money', 'ease_of_contact', 'resolution', 'app_experience', 'contacted_last_3_months',
               'likelihood_to_recommend'], rows)


def occupiers(U):
    """Recent changes of occupier on the prepayment book: the leaving occupier's account waits for its final bill while
    the new occupier is set up on the legacy platform (prepayment stays there until phase 2) on the same meter points."""
    rng = np.random.default_rng(W.SEED + SEED_O)
    accts = U['phase2_accts']
    lost_mp = {f[1] for f in U['flows']}
    shared = {}
    for a in accts:
        shared[a[6]] = shared.get(a[6], 0) + 1
    cand = [k for k, a in enumerate(accts) if a[4] == 'Live' and a[8] < '2026-06-01' and a[6] not in lost_mp
            and a[7] not in lost_mp and shared[a[6]] == 1]
    old = set()
    for j in sorted(rng.choice(len(cand), N_COT, replace=False)):
        a = accts[cand[j]]
        move = D(2026, 9, 1) + dt.timedelta(days=int(rng.integers(0, 58)))
        new = U['ids'].draw(lambda: '4%07d' % rng.integers(0, 10 ** 7))
        accts.append([new, a[1], 'Prepayment', a[3], 'Live', move.isoformat(), a[6], a[7], move.isoformat()])
        a[4], a[5] = 'Final bill pending', move.isoformat()
        old.add(a[0])
    U['cot_old'] = old


def apply(out, U):
    occupiers(U); loads(out, U); sales(out, U); quantities(out, U); survey_2026(out, U)
