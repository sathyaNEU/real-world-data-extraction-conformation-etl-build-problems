"""task401 ask-layer ceiling, measured on the cut pack. Shares no code with the generator.

The cracker lands the call, runs the hygiene battery and executes every filed convention (the cutover plan's scope,
UK-time weeks, each account once in the week its last load completed; the asking sentences' one switch per customer
in the month its first supply started, withdrawn switches out). The mirror stops at the most attractive wrong rung.
Each ask figure is a hit when it is within half a unit of the stated rounding of the golden.
    python3 ceiling.py <target dir> <figures.json>
"""
import csv, json, sys
from collections import defaultdict
from datetime import date, datetime, timedelta


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


def quantities(T):
    import pyarrow.parquet as pq
    t = pq.read_table(T + '/meter_point_annual_quantities.parquet').to_pydict()
    return list(zip(t['meter_point'], t['annual_quantity_kwh'], t['effective_from']))


def ask_a(T, mode):
    acc = rows(T + '/legacy_accounts_extract_2026-10-31.csv'); fl = rows(T + '/switching_flows_2026-05_2026-10.csv')
    asof = date(2026, 11, 1)
    q = quantities(T); inforce, latest = {}, {}
    for mp, kwh, d in q:
        if d <= asof and (mp not in inforce or d >= inforce[mp][1]):
            inforce[mp] = (kwh, d)
        if mp not in latest or d >= latest[mp][1]:
            latest[mp] = (kwh, d)
    lost = {f['meter_point'] for f in fl if f['flow'] == 'Loss completed' and date.fromisoformat(f['effective_date']) <= asof}
    counts, e, g, seen = defaultdict(int), 0.0, 0.0, set()
    for a in acc:
        if a['account_number'] in seen:
            continue
        seen.add(a['account_number'])
        if mode == 'cracker':
            if a['account_status'] == 'Closed':
                continue
            mps = [('E', a['mpan'])] + ([('G', a['mprn'])] if a['mprn'] else [])
            live = [(f, m) for f, m in mps if m not in lost]
            src = inforce
        else:
            if a['account_status'] != 'Live':
                continue
            live = [('E', a['mpan'])] + ([('G', a['mprn'])] if a['mprn'] else [])
            src = latest
        if not live:
            continue
        counts[a['region']] += 1
        for f, m in live:
            if f == 'E':
                e += src[m][0]
            else:
                g += src[m][0]
    return dict(counts), e / 1e6, g / 1e6


def ask_b(T, mode):
    out = defaultdict(int); last = {}
    with open(T + '/phase1_migration_loads.jsonl', encoding='utf-8') as f:
        recs = [json.loads(l) for l in f]
    if mode == 'mirror':
        for r in recs:
            t = datetime.strptime(r['completed_utc'], '%Y-%m-%dT%H:%M:%SZ')
            w = (t.date() - date(2025, 9, 1)).days // 7 + 1
            if 1 <= w <= 9:
                out[(w, r['fuel_profile'])] += 1
        return dict(out)
    for r in recs:
        t = uk(r['completed_utc'])
        k = r['legacy_account_ref']
        if k not in last or t >= last[k][0]:
            last[k] = (t, r['fuel_profile'])
    for k, (t, fp) in last.items():
        w = (t.date() - date(2025, 9, 1)).days // 7 + 1
        if 1 <= w <= 9:
            out[(w, fp)] += 1
    return dict(out)


def ask_c(T, mode):
    rg = rows(T + '/supply_registrations_2024-07_2025-12.csv'); qt = {r['quote_ref']: r['channel'] for r in rows(T + '/quote_log_2024-06_2025-12.csv')}
    out = defaultdict(int)
    if mode == 'mirror':
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
        d = date.fromisoformat(r['supply_start_date']); k = r['registration_ref']
        if k not in first or d < first[k][0]:
            first[k] = (d, r['quote_ref'])
    for k, (d, qref) in first.items():
        if date(2025, 7, 1) <= d <= date(2025, 12, 31):
            out[(qt[qref], d.month)] += 1
    return dict(out)


def score(T, F, mode):
    hits, n, per = 0, 0, {}
    a_counts, a_e, a_g = ask_a(T, mode)
    g = F['ask_a']; h = sum(1 for r, v in g['counts'].items() if a_counts.get(r, -1) == v)
    h += int(abs(a_e - g['elec_gwh']) < 0.05) + int(abs(a_g - g['gas_gwh']) < 0.05)
    per['A'] = (h, len(g['counts']) + 2); hits += h; n += len(g['counts']) + 2
    b = ask_b(T, mode); gb = F['ask_b']
    h = sum(1 for k, v in gb.items() if b.get((int(k.split('|')[0]), k.split('|')[1]), -1) == v)
    per['B'] = (h, len(gb)); hits += h; n += len(gb)
    c = ask_c(T, mode); gc = F['ask_c']
    h = sum(1 for k, v in gc.items() if c.get((k.split('|')[0], int(k.split('|')[1])), -1) == v)
    per['C'] = (h, len(gc)); hits += h; n += len(gc)
    return hits / n, per


if __name__ == '__main__':
    T, F = sys.argv[1], json.load(open(sys.argv[2]))
    lc, pc = score(T, F, 'cracker'); lm, pm = score(T, F, 'mirror')
    C = 38 + 7 + 55 * lc; S = 5 + 7 + 55 * lm
    print('cracker (lands the call, every filed convention, the hygiene battery): ask weight kept %.3f %s' % (lc, pc))
    print('mirror (stops at the most attractive wrong rung): ask weight kept %.3f %s' % (lm, pm))
    print('pair ceiling %.1f (cracker %.1f, mirror %.1f); mirror leakage %.1f per cent' % ((C + S) / 2, C, S, 100 * lm))
