"""The ask ceiling, measured on the cut pack: every persona's route through each ask block, scored against the golden.

Shares no code with the generator: its own readers over target/, and figures.json only for the golden values.
A figure is kept when the route's value rounds to the golden's value at the asked rounding."""
import datetime as dt
import io
import itertools
import json
import math
import os
import re
import sys
import numpy as np
import pandas as pd
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), 'target')
MONTHS = ['2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10']


def f(prefix):
    return os.path.join(TGT, [x for x in sorted(os.listdir(TGT)) if x.startswith(prefix)][0])


def table(prefix, head):
    raw = open(f(prefix)).read().splitlines()
    k = [i for i, l in enumerate(raw) if l.startswith(head)][0]
    return pd.read_csv(io.StringIO('\n'.join(raw[k:])), keep_default_na=False)


# ------------------------------------------------------------------------------------------- plant block readers

def hopper_loads():
    """Loaded runs that end at the primary hopper, by local month of the tip."""
    sv = json.load(open(f('ravensby_topographic')))
    pts = {ft['properties']['name']: ft['geometry']['coordinates'] for ft in sv['features'] if ft['geometry']['type'] == 'Point'}
    hop = pts['Primary crusher feed hopper']
    stk = [ft for ft in sv['features'] if ft['properties']['name'] == 'Run-of-mine stockpile'][0]
    sk = np.array(stk['geometry']['coordinates'][0])[:-1, :2].mean(axis=0)
    t = pq.read_table(f('adt_telematics')).to_pandas().sort_values(['unit_id', 'fix_utc'])
    lat0 = math.radians(hop[1])
    t['dh'] = np.hypot((t['lon'] - hop[0]) * math.cos(lat0), t['lat'] - hop[1])
    t['ds'] = np.hypot((t['lon'] - sk[0]) * math.cos(lat0), t['lat'] - sk[1])
    prev = t.groupby('unit_id')['payload_state'].shift(1)
    tips = t[(t['payload_state'] == 'EMPTY') & (prev == 'LOADED')]
    tips = tips[tips['dh'] < tips['ds']]
    tl = pd.to_datetime(tips['fix_utc'])
    tl = (tl.dt.tz_localize('UTC') if tl.dt.tz is None else tl).dt.tz_convert('Europe/London')
    return tl


def plant_routes():
    belt = table('primary_belt_scale', 'Interval start')
    belt['t'] = pd.to_datetime(belt['Interval start'], format='%d/%m/%Y %H:%M')
    belt['Tonnes'] = belt['Tonnes'].astype(float)
    flow = belt.set_index('t')['Tonnes']
    L = table('wheel_loader', 'Date,Time')
    L['t'] = pd.to_datetime(L['Date'] + ' ' + L['Time'], format='%d/%m/%Y %H:%M:%S')
    L['w'] = L['Bucket t'].astype(float)
    blank = L[L['Order'] == ''].copy()
    blank['bin'] = blank['t'].dt.floor('15min')
    plc = pd.read_csv(f('primary_crusher_plc'))
    plc = plc[plc['event'].str.startswith('CRUSHER')].copy()
    plc['t'] = pd.to_datetime(plc['event_time_local'])
    plc = plc.sort_values('t').reset_index(drop=True)
    from pypdf import PdfReader
    txt = '\n'.join(p.extract_text() for p in PdfReader(f('northfell')).pages)
    cuts = []
    for m in re.finditer(r'(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})\s+(\d{2}:\d{2})', txt):
        d = dt.datetime.strptime(m.group(1), '%d/%m/%Y')
        cuts.append(d + pd.Timedelta(m.group(2) + ':00'))
    # running intervals three ways
    naive, dropped, dno, beltclose = [], [], [], []
    ev = list(zip(plc['t'], plc['event']))
    for i, (t0, e) in enumerate(ev):
        if e != 'CRUSHER START':
            continue
        nxt = ev[i + 1] if i + 1 < len(ev) else None
        if nxt and nxt[1] == 'CRUSHER STOP':
            naive.append((t0, nxt[0]))
            c = [x for x in cuts if t0 < x < nxt[0]]
            dno.append((t0, min(c) if c else nxt[0]))
            continue
        stop = next((t for (t, e2) in ev[i + 1:] if e2 == 'CRUSHER STOP'), None)
        if stop is not None:
            naive.append((t0, stop))
        end = nxt[0] if nxt else t0 + pd.Timedelta(hours=12)
        c = [x for x in cuts if t0 < x < end]
        if c:
            dno.append((t0, min(c)))
        else:
            dno.append((t0, stop if stop is not None else end))
        fl = flow[(flow.index >= t0.floor('15min')) & (flow.index < end) & (flow > 0)]
        if len(fl):
            beltclose.append((t0, fl.index.max() + pd.Timedelta(minutes=15)))
    def hours(runs):
        h = {}
        for a, b in runs:
            h[a.strftime('%Y-%m')] = h.get(a.strftime('%Y-%m'), 0.0) + (b - a).total_seconds() / 3600
        return h
    def inside(ts, runs):
        arr = np.zeros(len(ts), bool)
        for a, b in runs:
            arr |= (ts >= a).to_numpy() & (ts < b).to_numpy()
        return arr
    loads = hopper_loads().dt.strftime('%Y-%m').value_counts()
    bm = belt.assign(m=belt['t'].dt.strftime('%Y-%m')).groupby('m')['Tonnes'].sum()
    blank['m'] = blank['t'].dt.strftime('%Y-%m')
    sub = {
        'none': blank.iloc[0:0],
        'all_blank': blank,
        'blank_plc_naive': blank[inside(blank['t'], naive)],
        'blank_plc_dno': blank[inside(blank['t'], dno)],
        'blank_belt_bins': blank[blank['bin'].map(lambda b: flow.get(b, 0.0) > 0)],
    }
    out = {}
    for name, s in sub.items():
        rc = s.groupby('m')['w'].sum()
        out['P1:' + name] = {m: (bm[m] - rc.get(m, 0.0)) / loads[m] for m in MONTHS}
    for name, runs in (('plc_as_logged', naive), ('dno', dno)):
        h = hours(runs)
        out['P2:' + name] = {m: bm[m] / h[m] for m in MONTHS}
    return out


# ------------------------------------------------------------------------------------------- sales block readers

def sales_routes():
    tk = pd.read_excel(f('weighbridge_tickets'))
    od = pd.read_excel(f('sales_orders'))
    pl = pd.read_csv(f('product_list'), dtype={'Code': str})
    pt = pd.read_csv(f('axle_weigher'), skiprows=1)
    tk['when'] = pd.to_datetime(tk['Date/time'], format='%d/%m/%Y %H:%M')
    tk['code'] = tk['Product'].astype(str)
    tk['ordered'] = tk['Order no'].map(dict(zip(od['Order no'], od['Product'])))
    tk['current'] = tk['code'].map(dict(zip(pl['Code'], pl['Description'])))
    maj = tk.groupby('code')['ordered'].agg(lambda s: s.value_counts().index[0])
    tk['majority'] = tk['code'].map(maj)
    pt['w'] = pd.to_datetime(pt['Date'] + ' ' + pt['Time'], format='%d/%m/%Y %H:%M')
    pt['n'] = (pt['Net kg'] / 1000).round(2)
    one = {(r['Vehicle'], r['n']): r['w'] for _, r in pt.iterrows()}
    tk['d_naive'] = tk['when']
    tk['d_one2one'] = [one.get((v, round(n, 2)), w) if w.weekday() == 0 else w for v, n, w in zip(tk['Vehicle'], tk['Net (t)'], tk['when'])]
    sub = []
    used = set()
    for i, r in tk.iterrows():
        w = r['when']
        if w.weekday() == 0:
            c = pt[(pt['Vehicle'] == r['Vehicle']) & (pt['w'] < w) & (pt['w'] > w - pd.Timedelta(days=7))]
            hit = None
            for day, g in c.groupby(c['w'].dt.date):
                for k in (1, 2, 3):
                    for s in itertools.combinations([j for j in g.index if j not in used], k):
                        if hit is None and abs(pt.loc[list(s), 'n'].sum() - r['Net (t)']) < 0.005:
                            hit = s
            if hit:
                used |= set(hit); w = pt.loc[list(hit), 'w'].min()
        sub.append(w)
    tk['d_subset'] = sub
    def prod(col, dcol='d_subset'):
        j = tk[(tk[dcol] >= '2026-01-01') & (tk[dcol] < '2026-02-01')]
        return j.groupby(col)['Net (t)'].sum().to_dict()
    def weeks(dcol):
        out = {}
        for lab, a, b in (('2025-12-29', '2026-01-01', '2026-01-05'), ('2026-01-05', '2026-01-05', '2026-01-12'),
                          ('2026-01-12', '2026-01-12', '2026-01-19'), ('2026-01-19', '2026-01-19', '2026-01-26'),
                          ('2026-01-26', '2026-01-26', '2026-02-01')):
            out[lab] = tk[(tk[dcol] >= a) & (tk[dcol] < b)]['Net (t)'].sum()
        return out
    return {'Q1:current_list': prod('current'), 'Q1:order_book': prod('ordered'), 'Q1:code_majority': prod('majority'),
            'Q2:ticket_date': weeks('d_naive'), 'Q2:one_to_one': weeks('d_one2one'), 'Q2:subset_sum': weeks('d_subset')}


# ----------------------------------------------------------------------------------------------------- score

PERSONAS = {  # the route each persona takes through each block
    'first_look':    {'P1': 'none', 'P2': 'plc_as_logged', 'Q1': 'current_list', 'Q2': 'ticket_date'},
    'mirror':        {'P1': 'all_blank', 'P2': 'plc_as_logged', 'Q1': 'order_book', 'Q2': 'ticket_date'},
    'cracker':       {'P1': 'blank_plc_naive', 'P2': 'plc_as_logged', 'Q1': 'order_book', 'Q2': 'one_to_one'},
    'full_includer': {'P1': 'blank_plc_dno', 'P2': 'dno', 'Q1': 'order_book', 'Q2': 'one_to_one'},
}


def score():
    fig = json.load(open(os.path.join(HERE, 'figures.json')))
    R = plant_routes(); R.update(sales_routes())
    gold = {'P1': {m: fig['t_per_load_%s' % m] for m in MONTHS}, 'P2': {m: fig['t_per_running_hour_%s' % m] for m in MONTHS},
            'Q1': {k[len('jan2026_t_'):]: v for k, v in fig.items() if k.startswith('jan2026_t_')},
            'Q2': {k[len('jan2026_week_'):-2]: v for k, v in fig.items() if k.startswith('jan2026_week_')}}
    rnd = {'P1': 1, 'P2': 1, 'Q1': 0, 'Q2': 0}
    def keep(block, route):
        vals = R['%s:%s' % (block, route)]
        hits = 0
        for k, g in gold[block].items():
            key = k if block != 'Q1' else [p for p in vals if p.replace(' ', '_').replace('-', '_') == k]
            v = vals[key[0]] if block == 'Q1' and key else (vals.get(k) if block != 'Q1' else None)
            if v is not None and round(v, rnd[block]) == g:
                hits += 1
        return hits, len(gold[block])
    table_ = {}
    for name in sorted(R):
        b, r = name.split(':')
        table_[name] = keep(b, r)
    n_all = sum(len(v) for v in gold.values())
    per = {}
    for p, route in PERSONAS.items():
        per[p] = sum(table_['%s:%s' % (b, r)][0] for b, r in route.items()) / n_all
    # the response on the call takes the better of the cracker's and the full includer's keep
    on = 38 + 7 + 55 * max(per['cracker'], per['full_includer'])
    pair = (on + (5 + 7 + 55 * per['mirror'])) / 2
    per['_pair_both_on'] = on   # both top responses land the call and keep the best persona's asks
    return table_, per, pair, n_all, R, gold


if __name__ == '__main__':
    t, per, pair, n, R, gold = score()
    for k, v in t.items():
        print('%-28s keeps %d of %d' % (k, v[0], v[1]))
    print('persona keep:', {k: round(v, 3) for k, v in per.items() if not k.startswith('_')}, 'of', n,
          'figures; pair ceiling %.1f (one on the call, one off); both on the call %.1f' % (pair, per['_pair_both_on']))
    if '-v' in sys.argv:
        for k, v in R.items():
            print(k, {a: round(b, 1) for a, b in v.items()})
