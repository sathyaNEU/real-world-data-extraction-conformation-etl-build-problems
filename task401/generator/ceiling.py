"""task401 ask-layer ceiling, measured on the cut pack. Shares no code with the generator.

Four responses, each scored on every ask figure (a hit is within half a unit of the stated rounding of the golden):
  cracker   lands the call, runs the hygiene battery and executes every filed convention: the cutover plan's scope
            (accounts not closed, meter points dropped on a completed loss), quantities in force on 1 November with day
            and night together, UK-time weeks with each account once in the week its last load completed (one per
            legacy reference), switches one per registration with withdrawn registrations out. Finds no device.
  mirror    stops at the most attractive wrong rung: live accounts and each meter point's latest quantity, loads by
            their UTC week, every registration row by its start month.
  full      the full includer, every device it can find handled: the switching flows replayed to 1 November (withdrawn
            losses, completed losses, erroneous transfers returned), each register's own quantity in force summed; the
            reload chain walked back to its first legacy reference, each account once in its last load's UK week with
            that load's fuels, and (the plan files that a moved account is one the new platform was billing when phase 1
            closed) every loaded account found live on the legacy prepayment extract left out as never moved; one switch
            per accepted quote, withdrawn registrations out, the quote's channel. The silent second device on each ask
            is left: a meter whose registers changed at an exchange, a loaded account the legacy platform took back
            only after phase 1 closed, a registration re-pointed at a later quote.
  norepair  every row taken as it stands: every extract row an account, each meter point's last row, every load row
            in its UTC week, every registration row in its start month under the quote it names.
    python3 ceiling.py <target dir> <figures.json>
"""
import csv, json, sys
from collections import defaultdict
from datetime import date, datetime, timedelta

ASOF = date(2026, 11, 1)


def rows(path):
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def uk(ts):
    t = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%SZ')
    def ls(m):
        d = date(t.year, m + 1, 1) - timedelta(days=1)
        return d - timedelta(days=(d.weekday() + 1) % 7)
    on = datetime.combine(ls(3), datetime.min.time()) + timedelta(hours=1)
    off = datetime.combine(ls(10), datetime.min.time()) + timedelta(hours=1)
    return t + timedelta(hours=1 if on <= t < off else 0)


def week(d):
    return (d - date(2025, 9, 1)).days // 7 + 1


def quantity_table(T):
    import pyarrow.parquet as pq
    t = pq.read_table(T + '/meter_point_annual_quantities.parquet').to_pydict()
    return list(zip(t['meter_point'], t['register'], t['annual_quantity_kwh'], t['effective_from']))


def per_register_in_force(q):
    best = {}
    for mp, reg, kwh, d in q:
        if d <= ASOF and ((mp, reg) not in best or d >= best[(mp, reg)][1]):
            best[(mp, reg)] = (kwh, d)
    out = defaultdict(float)
    for (mp, reg), (kwh, d) in best.items():
        out[mp] += kwh
    return out


def last_row(q):
    best = {}
    for mp, reg, kwh, d in q:
        if mp not in best or d >= best[mp][1]:
            best[mp] = (kwh, d)
    return {mp: v[0] for mp, v in best.items()}


def ask_a(T, mode):
    acc = rows(T + '/legacy_accounts_extract_2026-10-31.csv'); fl = rows(T + '/switching_flows_2026-05-01_2026-11-05.csv')
    q = quantity_table(T)
    if mode in ('cracker', 'full'):
        qmap = per_register_in_force(q)
    else:
        qmap = last_row(q)
    if mode == 'cracker':
        lost = {f['meter_point'] for f in fl if f['flow'] == 'Loss completed' and date.fromisoformat(f['effective_date']) <= ASOF}
    elif mode == 'full':
        rank = {'Loss notified': 0, 'Loss withdrawn': 1, 'Loss completed': 2, 'Erroneous transfer returned': 3}
        ev = sorted((f['meter_point'], f['flow_date'], rank[f['flow']], f['flow']) for f in fl if date.fromisoformat(f['flow_date']) <= ASOF)
        state = {}
        for mp, d, r, flow in ev:
            state[mp] = flow
        lost = {mp for mp, s in state.items() if s == 'Loss completed'}
    else:
        lost = set()
    counts, e, g, seen = defaultdict(int), 0.0, 0.0, set()
    for a in acc:
        if mode != 'norepair':
            if a['account_number'] in seen:
                continue
            seen.add(a['account_number'])
        if mode in ('cracker', 'full') and a['account_status'] == 'Closed':
            continue
        if mode == 'mirror' and a['account_status'] != 'Live':
            continue
        mps = [('E', a['mpan'])] + ([('G', a['mprn'])] if a['mprn'] else [])
        live = [(f, m) for f, m in mps if m not in lost]
        if not live:
            continue
        counts[a['region']] += 1
        for f, m in live:
            if f == 'E':
                e += qmap.get(m, 0)
            else:
                g += qmap.get(m, 0)
    return dict(counts), e / 1e6, g / 1e6


def ask_b(T, mode):
    out = defaultdict(int)
    with open(T + '/phase1_migration_loads.jsonl', encoding='utf-8') as f:
        recs = [json.loads(l) for l in f]
    if mode in ('mirror', 'norepair'):
        for r in recs:
            w = week(datetime.strptime(r['completed_utc'], '%Y-%m-%dT%H:%M:%SZ').date())
            if 1 <= w <= 9:
                out[(w, r['fuel_profile'])] += 1
        return dict(out)
    src = {r['platform_account_no']: r['legacy_account_ref'] for r in recs}
    def root(k):
        n = 0
        while mode in ('full', 'dated') and k in src and n < 20:
            k = src[k]; n += 1
        return k
    last = {}
    for r in recs:
        t = uk(r['completed_utc']); k = root(r['legacy_account_ref'])
        if k not in last or t >= last[k][0]:
            last[k] = (t, r['fuel_profile'])
    on_legacy = set()
    if mode == 'full':
        on_legacy = {a['account_number'] for a in rows(T + '/legacy_accounts_extract_2026-10-31.csv')}
    elif mode == 'dated':      # stress: the full includer that also dates each legacy return against the close
        on_legacy = {a['account_number'] for a in rows(T + '/legacy_accounts_extract_2026-10-31.csv') if a['status_date'] <= '2025-11-02'}
    for k, (t, fp) in last.items():
        w = week(t.date())
        if 1 <= w <= 9 and k not in on_legacy:
            out[(w, fp)] += 1
    return dict(out)


def ask_c(T, mode):
    rg = rows(T + '/supply_registrations_2024-05_2025-12.csv'); qt = {r['quote_ref']: r['channel'] for r in rows(T + '/quote_log_2024-05_2025-12.csv')}
    out = defaultdict(int)
    if mode in ('mirror', 'norepair'):
        for r in rg:
            if r['event'] == 'Registration':
                d = date.fromisoformat(r['supply_start_date'])
                if date(2025, 7, 1) <= d <= date(2025, 12, 31):
                    out[(qt.get(r['quote_ref'], '?'), d.month)] += 1
        return dict(out)
    wd = {r['registration_ref'] for r in rg if r['event'] == 'Withdrawal'}
    first = {}
    for r in rg:
        if r['event'] != 'Registration' or r['registration_ref'] in wd:
            continue
        d = date.fromisoformat(r['supply_start_date'])
        k = r['registration_ref'] if mode == 'cracker' else r['quote_ref']
        if k not in first or d < first[k][0]:
            first[k] = (d, r['quote_ref'])
    for k, (d, qref) in first.items():
        if date(2025, 7, 1) <= d <= date(2025, 12, 31):
            out[(qt[qref], d.month)] += 1
    return dict(out)


def score(T, F, mode):
    per = {}
    ma = 'full' if mode == 'dated' else mode       # the stress response is the full includer on Asks A and C
    a_counts, a_e, a_g = ask_a(T, ma)
    g = F['ask_a']; h = sum(1 for r, v in g['counts'].items() if a_counts.get(r, -1) == v)
    he, hg = int(abs(a_e - g['elec_gwh']) < 0.05), int(abs(a_g - g['gas_gwh']) < 0.05)
    per['A'] = (h + he + hg, len(g['counts']) + 2, 'counts %d of %d, elec %s, gas %s' % (h, len(g['counts']), 'hit' if he else 'miss', 'hit' if hg else 'miss'))
    b = ask_b(T, mode); gb = F['ask_b']
    hb = {fp: sum(1 for k, v in gb.items() if k.endswith(fp) and b.get((int(k.split('|')[0]), fp), -1) == v) for fp in ('ELEC', 'DUAL')}
    per['B'] = (sum(hb.values()), len(gb), 'electricity-only %d of 9, dual fuel %d of 9' % (hb['ELEC'], hb['DUAL']))
    c = ask_c(T, ma); gc = F['ask_c']
    hc = defaultdict(int)
    for k, v in gc.items():
        ch, m = k.split('|')
        hc[ch] += int(c.get((ch, int(m)), -1) == v)
    per['C'] = (sum(hc.values()), len(gc), ', '.join('%s %d of 6' % (ch, hc[ch]) for ch in sorted(hc)))
    hits = sum(v[0] for v in per.values()); n = sum(v[1] for v in per.values())
    return hits / n, per


if __name__ == '__main__':
    T, F = sys.argv[1], json.load(open(sys.argv[2]))
    res = {m: score(T, F, m) for m in ('cracker', 'mirror', 'full', 'norepair')}
    for m, (k, per) in res.items():
        print('%-9s keeps %.3f of ask weight: %s' % (m, k, '; '.join('%s %d of %d (%s)' % (a, v[0], v[1], v[2]) for a, v in sorted(per.items()))))
    on = lambda k: 38 + 7 + 55 * k
    off = lambda k: 5 + 7 + 55 * k
    pairs = {'cracker on the call, mirror off': (on(res['cracker'][0]) + off(res['mirror'][0])) / 2,
             'full includer on the call, mirror off': (on(res['full'][0]) + off(res['mirror'][0])) / 2,
             'full includer on the call, no-repair off': (on(res['full'][0]) + off(res['norepair'][0])) / 2,
             'cracker on the call, no-repair off': (on(res['cracker'][0]) + off(res['norepair'][0])) / 2,
             'full includer and cracker, both on the call': (on(res['full'][0]) + on(res['cracker'][0])) / 2,
             'two full includers on the call (stress)': on(res['full'][0])}
    for k, v in pairs.items():
        print('pair, %s: %.1f' % (k, v))
    one_off = {k: v for k, v in pairs.items() if 'off' in k}
    print('pair ceiling %.1f (one response off the call, the worst of four); both on the call %.1f; mirror leakage %.1f per cent'
          % (max(one_off.values()), pairs['full includer and cracker, both on the call'], 100 * res['mirror'][0]))
    # stress, outside the four: the full includer that also dates every legacy return against the close of phase 1
    k, per = score(T, F, 'dated')
    print('stress: date-testing includer keeps %.3f of ask weight (%s); with the mirror off %.1f, with the cracker on the call %.1f'
          % (k, '; '.join('%s %d of %d' % (a, v[0], v[1]) for a, v in sorted(per.items())), (on(k) + off(res['mirror'][0])) / 2,
             (on(k) + on(res['cracker'][0])) / 2))
