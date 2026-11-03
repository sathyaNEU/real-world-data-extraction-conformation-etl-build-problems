"""Independent recomputation of task307's golden from the shipped files in target/ only (no generator imports).

    python3 task307/generator/verify.py          exit 0 when every graded figure matches figures.json

The functions are shared with ceiling.py, which runs the cracker's and the mirror's handlings on the same pack.
"""
import datetime as dt
import itertools
import json
import os
import re
import sys
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), 'target')
OSLO = ZoneInfo('Europe/Oslo')
T0 = pd.Timestamp(dt.datetime(2016, 1, 1, tzinfo=OSLO)).tz_convert('UTC')
T1 = pd.Timestamp(dt.datetime(2027, 1, 1, tzinfo=OSLO)).tz_convert('UTC')
NH = int((T1 - T0) / pd.Timedelta(hours=1))
STATION_OF = {'Øvre Sørdal': 'OSD', 'Sørdal': 'SDL', 'Nesvik': 'NSV'}


def hidx(d, h=0):
    """Hour index of local midnight (or hour h) of a date."""
    return int((pd.Timestamp(dt.datetime(d.year, d.month, d.day, h, tzinfo=OSLO)).tz_convert('UTC') - T0) / pd.Timedelta(hours=1))


def num(x):
    if isinstance(x, (int, float)):
        return float(x)
    return float(str(x).replace(',', '.'))


def load():
    D = {}
    old = pd.read_csv(os.path.join(TGT, 'historian_export_2016_2023.csv'), sep=';', decimal=',')
    D['old'] = old
    D['new'] = pd.read_csv(os.path.join(TGT, 'historian_export_2023_2026.csv'))
    D['map'] = pd.read_csv(os.path.join(TGT, 'historian_tag_map_2023.csv'))
    D['mh'] = pd.read_csv(os.path.join(TGT, 'maintenance_history.csv'), dtype=str).fillna('')
    reg = pd.read_excel(os.path.join(TGT, 'unit_register.xlsx'), sheet_name=None)
    D['units'] = reg['Aggregater']
    rng = reg['Driftsområder']
    row = rng[rng['Område'] == 'Begrenset'].iloc[0]
    D['band'] = (num(str(row.iloc[1]).strip(' %')) / 100, num(str(row.iloc[2]).strip(' %')) / 100)
    D['log'] = pd.read_csv(os.path.join(TGT, 'protection_log_2016_2026.csv'))
    D['insp'] = pd.read_excel(os.path.join(TGT, 'runner_inspections.xlsx'), dtype=str)
    import pdfplumber
    with pdfplumber.open(os.path.join(TGT, 'runner_refurbishment_quote_2027.pdf')) as pdf:
        text = '\n'.join(p.extract_text() for p in pdf.pages)
    D['quote'] = {m.group(1): float(m.group(2).replace(',', '')) / 1e6
                  for m in re.finditer(r'^(\w{3}-G\d) R-\d+ shop refurbishment ([\d,]+) ', text, re.M)}
    return D


def old_hour_index(D, dst='infer'):
    """UTC hour index of each old-historian row (local wall-clock labels)."""
    ts = pd.to_datetime(D['old']['Tidspunkt'], format='%d.%m.%Y %H:%M')
    if dst == 'infer':
        loc = ts.dt.tz_localize(OSLO, ambiguous='infer')
        return ((loc.dt.tz_convert('UTC') - T0) / pd.Timedelta(hours=1)).astype(int).to_numpy(), np.ones(len(ts), bool)
    # dedupe on the local label first, as a stacked export with the overlap removed by timestamp would
    keep = ~ts.duplicated(keep='first').to_numpy()
    loc = ts[keep].dt.tz_localize(OSLO, ambiguous=True)
    idx = np.full(len(ts), -1)
    idx[keep] = ((loc.dt.tz_convert('UTC') - T0) / pd.Timedelta(hours=1)).astype(int).to_numpy()
    return idx, keep


def outages(D):
    """Logged out-of-service spans per unit: (start hour, end hour)."""
    mh = D['mh']
    spans = {}
    for kind in ('overhaul', 'annual maintenance'):
        s = mh[mh['event'] == kind + ' start']
        e = mh[mh['event'] == kind + ' end']
        for u in s['unit'].unique():
            a = sorted(s[s['unit'] == u]['date'])
            b = sorted(e[e['unit'] == u]['date'])
            for x, y in zip(a, b):
                spans.setdefault(u, []).append((hidx(dt.date.fromisoformat(x)), hidx(dt.date.fromisoformat(y))))
    return spans


def rtu_dates(D):
    mh = D['mh']
    out = {}
    for _, r in mh[mh['event'] == 'control system'].iterrows():
        for name in ('Øvre Sørdal', 'Nesvik', 'Sørdal'):
            if r['detail'].startswith(name + ' station'):
                out[STATION_OF[name]] = hidx(dt.date.fromisoformat(r['date']))
                break
    return out


def series(D, swap='golden', overlap='once', dst='infer'):
    """Hourly MW per unit over the record. swap: 'golden' re-assigns the old slots before each RTU replacement from the
    logged outages, 'map' takes the 2023 tag map as given; overlap: 'once' or 'twice'; dst: 'infer' or 'label'."""
    tagmap = {r['old_tag']: r['new_tag'].replace('.P', '') for _, r in D['map'].iterrows()}
    units = list(D['units']['Aggregat'])
    idx, keep = old_hour_index(D, dst)
    old = {t: np.zeros(NH) for t in tagmap}
    for t in tagmap:
        v = D['old'][t].to_numpy(dtype=float)
        ok = keep & (idx >= 0) & (idx < NH)
        old[t][idx[ok]] = v[ok]
    new_t = pd.to_datetime(D['new']['time_utc'], utc=True)
    nidx = ((new_t - T0) / pd.Timedelta(hours=1)).astype(int).to_numpy()
    new_start = nidx.min()
    old_last = idx[keep].max()
    S = {u: np.zeros(NH) for u in units}
    assign = {}
    if swap == 'golden':
        spans = outages(D)
        rtu = rtu_dates(D)
        for st in ('OSD', 'SDL', 'NSV'):
            tags = [t for t in tagmap if tagmap[t].startswith(st)]
            us = [tagmap[t] for t in tags]
            end = rtu[st]
            best = None
            for perm in itertools.permutations(us):
                score = 0
                for t, u in zip(tags, perm):
                    for (a, b) in spans.get(u, []):
                        a, b = max(a, 0), min(b, end)
                        if a < b:
                            score += int((old[t][a:b] == 0).sum()) - int((old[t][a:b] > 0).sum())
                key = (score, tuple(perm) == tuple(us))
                if best is None or key > best[0]:
                    best = (key, perm)
            assign[st] = (dict(zip(tags, best[1])), end)
    for t, u in tagmap.items():
        S[u][:min(old_last + 1, NH)] += 0.0
    for t in tagmap:
        src = old[t]
        st = tagmap[t][:3]
        if swap == 'golden':
            perm, end = assign[st]
            S[perm[t]][:end] += src[:end]
            S[tagmap[t]][end:new_start] += src[end:new_start]
        else:
            S[tagmap[t]][:new_start] += src[:new_start]
        if overlap == 'twice':
            S[tagmap[t]][new_start:old_last + 1] += src[new_start:old_last + 1]
    for u in units:
        v = D['new'][u + '.P'].to_numpy(dtype=float)
        S[u][nidx] += v
    return S, assign


def ratings(D):
    return {r['Aggregat']: float(r['Ytelse (MW)']) for _, r in D['units'].iterrows()}


def in_band(S, D):
    lo, hi = D['band']
    R = ratings(D)
    out = {}
    for u, v in S.items():
        c = np.round(v * 100).astype(np.int64)
        out[u] = (c >= int(round(lo * R[u] * 100))) & (c < int(round(hi * R[u] * 100)))
    return out


def inspections(D):
    rows = []
    for _, r in D['insp'].iterrows():
        d = dt.datetime.strptime(r['Dato'], '%d.%m.%Y').date()
        rep = num(r['Etter reparasjon (cm²)']) if r['Reparert'] == 'Ja' else None
        rows.append({'runner': r['Løpehjul'], 'date': d, 'unit': r['Aggregat'], 'found': num(r['Funn totalt (cm²)']),
                     'rep': rep})
    rows.sort(key=lambda r: (r['date'], r['runner']))
    return rows


def call(D, S, mode='rz', peaker_out=True):
    """mode 'rz': pitting per hour in the restricted band (golden); 'run': per running hour, the peaker set aside."""
    R = ratings(D)
    band = in_band(S, D)
    count = {u: (band[u] if mode == 'rz' else S[u] > 0) for u in S}
    ins = [r for r in inspections(D) if r['date'] >= dt.date(2016, 1, 1)]
    num_, den = 0.0, 0
    for rn in sorted({r['runner'] for r in ins}):
        mine = [r for r in ins if r['runner'] == rn]
        for a, b in zip(mine, mine[1:]):
            if a['unit'] != b['unit']:
                continue
            if mode == 'run' and peaker_out and a['unit'] == 'SDL-G3':
                continue
            start = a['rep'] if a['rep'] is not None else a['found']
            num_ += b['found'] - start
            den += int(count[a['unit']][hidx(a['date']):hidx(b['date'])].sum())
    rate = num_ / den
    cur = {r['Aggregat']: r['Løpehjul'] for _, r in D['units'].iterrows()}
    rows = {}
    for u in S:
        rn = cur[u]
        last = [r for r in ins if r['runner'] == rn][-1]
        p0 = last['rep'] if last['rep'] is not None else last['found']
        now = p0 + rate * int(count[u][hidx(last['date']):NH].sum())
        q26 = int(count[u][hidx(dt.date(2026, 1, 1)):NH].sum())
        cross, p = None, now
        for y in range(2027, 2032):
            p += rate * q26
            if p >= 2400 and cross is None:
                cross = y
        if now >= 2400:
            cross = 2027
        gen = 0.0
        if cross is not None:
            tot = 0.0
            for y in range(2021, 2026):
                a = hidx(dt.date(y, 12, 1))
                b = hidx(dt.date(y, 12, 1) + dt.timedelta(weeks=14))
                tot += S[u][a:b].sum()
            gen = tot / 5
        rows[u] = {'runner': rn, 'last_date': last['date'], 'last_pitting': p0, 'now': now, 'cross': cross, 'gen': gen,
                   'per_mnok': gen / D['quote'][u], 'rate': rate}
    order = sorted(rows, key=lambda u: -rows[u]['per_mnok'])
    return rows, order


def log_events(D):
    """Breaker operations from the protection log as (object, station, hour index, kind) with kind 'open' or 'close'."""
    lg = D['log']
    t = pd.to_datetime(lg['time_utc'], utc=True)
    h = ((t - T0) / pd.Timedelta(hours=1)).astype(float).to_numpy()
    out = []
    for k, r in enumerate(lg.itertuples(index=False)):
        if r.event in ('breaker open', 'breaker closed'):
            out.append((r.object, r.station, int(np.floor(h[k])), 'open' if r.event == 'breaker open' else 'close'))
    return out


def asks(S, D=None, starts_mode='golden', trips_mode='golden'):
    """starts_mode: 'golden' every start from standstill (the hourly record's starts plus the restarts after a trip
    that the hourly record cannot see), 'hourly' the hourly record's alone, 'all' the hourly starts plus every unit trip;
    trips_mode: 'golden' each unit's own breaker trips and every line trip that caught it generating, 'unit_rows' the
    unit's own breaker trips alone, 'operated_rows' every protection-operated row on the unit, 'station_all' line trips
    on every unit of the station."""
    gen = {u: float(v.sum()) for u, v in S.items()}
    starts = {u: int(((v[1:] > 0) & (v[:-1] == 0)).sum()) for u, v in S.items()}
    if D is None:
        return gen, starts
    ev = log_events(D)
    station = {r['Aggregat']: r['Stasjon'] for _, r in D['units'].iterrows()}
    units = list(S)
    trips = {u: 0 for u in units}
    for k, (obj, st, h, kind) in enumerate(ev):
        if kind != 'open':
            continue
        if obj in S:
            trips[obj] += 1
            nxt = [e for e in ev[k + 1:] if e[0] == obj and e[3] == 'close'][0]
            invisible = bool((S[obj][h:nxt[2] + 1] > 0).all())
            if starts_mode == 'all' or (starts_mode == 'golden' and invisible):
                starts[obj] += 1
        else:
            for u in units:
                if station[u] == st and (trips_mode == 'station_all' or S[u][h] > 0):
                    trips[u] += 1
    if trips_mode == 'unit_rows':
        trips = {u: sum(1 for (obj, st, h, kind) in ev if obj == u and kind == 'open') for u in units}
    elif trips_mode == 'operated_rows':
        lg = D['log']
        trips = {u: int(((lg['object'] == u) & (lg['event'] == 'protection operated')).sum()) for u in units}
    return gen, starts, trips


def rnd(x, step):
    return int(np.floor(x / step + 0.5) * step)


def main():
    D = load()
    S, assign = series(D)
    rows, order = call(D, S)
    gen, starts, trips = asks(S, D)
    F = json.load(open(os.path.join(HERE, 'figures.json'), encoding='utf-8'))
    bad = []

    def chk(name, got, want):
        if got != want:
            bad.append('%s: got %r, figures.json %r' % (name, got, want))
    chk('chosen', order[0], F['call']['chosen'])
    chk('runner_up', order[1], F['call']['runner_up'])
    chk('chosen_gen', rnd(rows[order[0]]['gen'], 100), F['call']['chosen_gen_mwh'])
    chk('gap', rnd(rows[order[0]]['per_mnok'], 10) - rnd(rows[order[1]]['per_mnok'], 10), F['call']['gap_per_mnok'])
    for u, f in F['units'].items():
        r = rows[u]
        chk(u + ' runner', r['runner'], f['runner'])
        chk(u + ' last', rnd(r['last_pitting'], 10), f['last_pitting_cm2'])
        chk(u + ' now', rnd(r['now'], 10), f['now_cm2'])
        chk(u + ' cross', r['cross'], f['cross_year'])
        chk(u + ' gen', rnd(r['gen'], 100), f['gen_mwh'])
        chk(u + ' quote', D['quote'][u], f['quote_mnok'])
        chk(u + ' per_mnok', rnd(r['per_mnok'], 10), f['per_mnok'])
        chk(u + ' ask gen', rnd(gen[u], 100), F['asks']['generation_2016_2026_mwh'][u])
        chk(u + ' ask starts', starts[u], F['asks']['starts_2016_2026'][u])
        chk(u + ' ask trips', trips[u], F['asks']['trips_2016_2026'][u])
    for st, (perm, end) in assign.items():
        print('slots before the %s RTU replacement:' % st, ', '.join('%s carried %s' % kv for kv in sorted(perm.items())))
    if bad:
        print('VERIFY FAIL')
        print('\n'.join(bad))
        sys.exit(1)
    print('VERIFY PASS: call %s over %s, %d graded figures recomputed from target/' % (order[0], order[1], 4 + 10 * len(F['units'])))


if __name__ == '__main__':
    main()
