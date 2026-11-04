"""task401 generator checks on the cut pack and the clean truth. Exit 1 on any failure.

    python3 task401/generator/checks.py            checks on target/ and 20 redraws of the world
"""
import json, os, sys, zipfile, re
from collections import defaultdict
from datetime import date, datetime, timedelta
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import golden as G
import world as W

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
FAILS = []


def ok(name, cond, detail=''):
    print('%s  %s %s' % ('PASS' if cond else 'FAIL', name, detail))
    if not cond:
        FAILS.append(name)


def edge(v, u):
    return u / 2 - abs(v - round(v / u) * u)


fig = json.load(open(os.path.join(HERE, 'figures.json')))

# ------------------------------------------------------------------ main call on the shipped pack
days = G.monitor_days(T)
days_f = G.monitor_days(T, use_flagged=True)
for lo, hi, key in (G.WIN + ('exc_window',), G.PRIOR + ('exc_prior',)):
    a, b = G.exceedances(days, lo, hi), G.exceedances(days_f, lo, hi)
    ok('SF1 the flagged maintenance readings never move an exceedance day (%s)' % key, a == b and len(a) == fig[key], '%d %d' % (len(a), len(b)))
near = [d for d, m in days.items() if 0.53 < m < 0.67]
ok('SF2 no day mean within 0.07 of the standard, so every validity reading files the same days', not near, str(near[:3]))
short = [d for d in W.DAYS if d not in days]
ok('SF3 every day carries 72 or more valid readings', not short, str(short[:3]))
exc = G.exceedances(days, *G.WIN)
forms = {}
for name, kw, lags in [('large 1-2', {}, (1, 2)), ('large 1-3', {}, (1, 2, 3)), ('large 1-4', {}, (1, 2, 3, 4)),
                       ('large 1-5', {}, (1, 2, 3, 4, 5)), ('large 0-3', {}, (0, 1, 2, 3)),
                       ('any night 1-3', dict(ph_max=6.7, flow_min=0.0, hours=(0, 24)), (1, 2, 3)),
                       ('any night 0-5', dict(ph_max=6.7, flow_min=0.0, hours=(0, 24)), (0, 1, 2, 3, 4, 5)),
                       ('ph<6.3 flow>8 1-2', dict(ph_max=6.3, flow_min=8.0), (1, 2))]:
    ev = G.dairy_events(T, **kw)
    forms[name] = len(G.reach(exc, ev, lags))
fe = G.historian_fe(T)
ev = G.dairy_events(T)
episode = 0
for d in exc:
    j = d
    while (j - timedelta(days=1)) in fe and fe[j - timedelta(days=1)] > 3.0:
        j -= timedelta(days=1)
    if (j - timedelta(days=1)) in ev or j in ev:
        episode += 1
forms['episode'] = episode
ok('SF4 every reach form (windows, large or any discharge, episode-based) files the same days on the pack',
   len(set(forms.values())) == 1 and fig['dairy_reach'] == fig['exc_window'], str(forms))
ok('the upgrade and the control reach no exceedance day under any form', fig['other_reach'] == 0)
ev_all = G.dairy_events(T)
for lo, hi, nm in ((date(2025, 12, 1), date(2026, 2, 28), 'December to February'), (date(2025, 10, 1), date(2026, 3, 31), 'October to March')):
    e2 = G.exceedances(days, lo, hi)
    ok('SF6 a reader who takes "this winter" as %s files the same call: every exceedance day reached' % nm,
       len(G.reach(e2, ev_all)) == len(e2) and len(e2) > 0, '%d of %d' % (len(G.reach(e2, ev_all)), len(e2)))
prior_wide = G.exceedances(days, date(2024, 10, 1), date(2025, 3, 31))
ok('SF7 a reader who compares with the whole of the previous October to March files the same contrast',
   len(prior_wide) <= 6 and len(exc) >= 4 * len(prior_wide), '%d against %d' % (len(exc), len(prior_wide)))
ok('SF8 no exceedance day in either winter lacks a dairy discharge on the two evenings before it, so no other candidate '
   'reaches one', len(G.reach(exc, ev_all)) == len(exc) and len(G.reach(G.exceedances(days, *G.PRIOR), ev_all)) == fig['exc_prior'])
acc_u = defaultdict(list)
for r in G.rows(T, 'allery_d_s_coldmere_wq_monitor_2024-10_2026-03.csv'):
    if not r['qc_flag']:
        acc_u[datetime.strptime(r['datetime_utc'], '%Y-%m-%dT%H:%M:%SZ').date()].append(float(r['ammonium_mg_l_as_n']))
days_u = {d: sum(v) / len(v) for d, v in acc_u.items() if len(v) >= 72}
for lo, hi, key in (G.WIN + ('exc_window',), G.PRIOR + ('exc_prior',)):
    ok('SF5 a reader who keeps the monitor\'s UTC days files the same exceedance days (%s)' % key,
       G.exceedances(days_u, lo, hi) == G.exceedances(days, lo, hi))
dairy_rows = G.rows(T, 'thornlea_dairy_discharge_monitor_15min.csv')
ok('the dairy\'s record carries no alarm, flag or status column', list(dairy_rows[0].keys()) == ['logger_time', 'flow_m3', 'ph', 'temperature_c'])
phs = [float(r['ph']) for r in dairy_rows]
ok('the dairy\'s pH never leaves its consent\'s 6 to 11, so no limit is visibly breached', 6.0 <= min(phs) and max(phs) <= 11.0,
   '%.2f to %.2f' % (min(phs), max(phs)))
dc = [float(r['result']) for r in G.rows(T, 'lims_trade_effluent_results_2025-01_2026-04.csv')
      if r['sample_point'] == 'TH-SC1' and r['determinand'] == 'COD settled']
cc = [x[1] for x in G.composites(T, 'TH-SC1')]
ok('the dairy\'s weekly composites read normal (no bottle above the consent\'s 6,000 mg/l, no composite above twice '
   'their mean)', max(dc) < 6000 and max(cc) < 2 * sum(cc) / len(cc),
   '%.0f bottle max, %.0f composite max, %.0f composite mean' % (max(dc), max(cc), sum(cc) / len(cc)))
hist_cols = G.rows(T, 'coldmere_wrc_historian_hourly_2024-10_2026-03.csv')[0].keys()
ok('the works\' historian carries no inlet pH or inhibition tag', not any('PH' in c.upper() or 'TOX' in c.upper() for c in hist_cols))
not_after = [d for d in days if G.WIN[0] <= d <= G.WIN[1] and d not in exc]
ok('no slug-free day in either winter exceeds', all(days[d] <= G.STANDARD for d in not_after))

# the default path's rungs on the pack: process model on temperature, load and the control (no discharge record)
win_days = [W.DAYS[i] for i in range(W.N) if W.PRIOR[0] <= W.DAYS[i] <= W.WIN[1]]
P = W.daily_process()
y = np.array([1.0 if days.get(d, 0) > G.STANDARD else 0.0 for d in win_days])
temp = np.array([P['temp'][W.idx(d)] for d in win_days])
ctrl = np.array([1.0 if d >= W.AER_GO_LIVE else 0.0 for d in win_days])
load = np.array([P['load'][W.idx(d)] for d in win_days])
X = np.column_stack([np.ones(len(y)), np.clip(14 - temp, 0, None), load, ctrl])
b = np.linalg.lstsq(X, y, rcond=None)[0]
wmask = np.array([G.WIN[0] <= d <= G.WIN[1] for d in win_days])
ctrl_days = b[3] * ctrl[wmask].sum()
ok('rung 1: the process model books most of the window to the aeration control', ctrl_days > 0.6 * fig['exc_window'],
   '%.1f of %d' % (ctrl_days, fig['exc_window']))
Xf = np.column_stack([X, (temp < 8).astype(float), (temp < 10).astype(float), np.clip(14 - temp, 0, None) * ctrl, load * ctrl])
bf = np.linalg.lstsq(Xf, y, rcond=None)[0]
flex = bf[3] * ctrl[wmask].sum() + bf[6] * (np.clip(14 - temp, 0, None) * ctrl)[wmask].sum() + bf[7] * (load * ctrl)[wmask].sum()
ok('rung 2: the flexible default still books most of the window to the control', flex > 0.6 * fig['exc_window'], '%.1f' % flex)
dairy_kg = 0.0

# literal executions of the filed WHAT
lit_dated = 'control'   # a dated before-and-after cannot part 27 October from 3 November with daily data a week apart
ok('literal: a dated before-and-after names the control (control 27 Oct, new line 3 Nov, both before the first exceedance)',
   min(exc) > W.NEW_LINE and min(exc) > W.AER_GO_LIVE, str(min(exc)))

# ------------------------------------------------------------------ 20 redraws of the world (clean truth)
inv = []
for k in range(20):
    s = 9100 + k
    Pk = W.daily_process(s); W.dairy_15min(Pk, s)
    fk = W.reach_forms(Pk, *W.WIN)
    nk = len(W.exceedance_days(Pk, *W.WIN))
    big = {x['day'] for x in Pk['slugs']}
    nearw = {x + timedelta(days=L) for x in big for L in (1, 2)}
    oth = [Pk['river'][W.idx(d)] for d in W.DAYS if d not in nearw and (W.WIN[0] <= d <= W.WIN[1] or W.PRIOR[0] <= d <= W.PRIOR[1])]
    inv.append((len(set(fk.values())) == 1 and fk['1-2'] == nk, max(oth), nk))
ok('SF4 over 20 redraws: every reach form equal to the window count, every redraw',
   all(x[0] for x in inv), '%d of 20; window %d to %d; slug-free max %.3f' % (sum(x[0] for x in inv), min(x[2] for x in inv),
                                                                            max(x[2] for x in inv), max(x[1] for x in inv)))

# ------------------------------------------------------------------ the shock's footprint in the works and the week
from collections import Counter
wd = Counter(d.weekday() for d in exc)
ok('no weekly pattern a tabulation finds: no weekday above three tenths of the exceedance days, at most one empty',
   max(wd.values()) <= 0.3 * len(exc) and sum(1 for k in range(7) if wd.get(k, 0) == 0) <= 1, str(sorted(wd.items())))
hist = [(datetime.strptime(r['timestamp'], '%d/%m/%Y %H:%M'), float(r['AL1_DO'] or r['AB1_DO_AIT110']))
        for r in G.rows(T, 'coldmere_wrc_historian_hourly_2024-10_2026-03.csv')]
for lim, hours, morning in ((1.0, 3, False), (0.8, 6, False), (0.6, 4, True), (1.0, 8, True)):
    sag = defaultdict(int)
    for t, v in hist:
        if v < lim and (t.hour < 12 or not morning):
            sag[t.date()] += 1
    sag_days = {d for d, n in sag.items() if n >= hours and G.WIN[0] <= d <= G.WIN[1]}
    hit = len(sag_days & set(exc))
    ok('the oxygen sags are no one-query signal (DO under %.1f for %d hours%s): under half the sag days are exceedance days'
       % (lim, hours, ', mornings' if morning else ''), hit < 0.5 * len(sag_days), '%d sag days, %d exceedance' % (len(sag_days), hit))

# ------------------------------------------------------------------ the Wednesday: the strained line's cleaning day
wed, other = [], []
for r in dairy_rows:
    t = datetime.strptime(r['logger_time'], '%Y-%m-%d %H:%M')
    if t.date() >= W.NEW_LINE and t.weekday() in (0, 1, 2, 3, 4) and 9 <= t.hour < 17:
        (wed if t.weekday() == 2 else other).append(float(r['flow_m3']))
ok('from 3 November the chamber record shows the strained line standing on Wednesdays (lower daytime flow)',
   sum(wed) / len(wed) < 0.9 * sum(other) / len(other), '%.2f against %.2f m3 a quarter-hour' % (sum(wed) / len(wed), sum(other) / len(other)))
ok('no whey evening falls on a Wednesday', not any(e.weekday() == 2 for e in G.dairy_events(T) if e >= W.NEW_LINE))

# ------------------------------------------------------------------ the ask: literal executor and devices
A = fig['ask_a']
cons = {c['discharger']: c for c in G.consents(T)}
for name, v in A.items():
    for key in ('volume', 'ot', 'st'):
        ok('Ask A mid-bin %s %s' % (key, name), edge(v[key + '_raw'], 1.0) >= 0.07, '%.3f' % edge(v[key + '_raw'], 1.0))
for name in ('Wyecote Brewery', 'Pellow Meats'):
    dv = abs(G.chargeable_volume(T, cons[name], exchanges=False) - A[name]['volume_raw'])
    ok('Ask A P1, the 1 April reads differenced across the exchange, moves %s by many bins' % name, dv > 500, '%.0f m3' % dv)
for name in A:
    if name not in ('Wyecote Brewery', 'Pellow Meats'):
        ok('Ask A no exchange at %s' % name, abs(G.chargeable_volume(T, cons[name], exchanges=False) - A[name]['volume_raw']) < 1e-6)
c1 = dict(cons['Kestry Linen Services']); c1['register_multiplier'] = 1
ok('Ask A hazard: the consent\'s ten-unit register moves the laundry by many bins',
   abs(G.chargeable_volume(T, c1) - A['Kestry Linen Services']['volume_raw']) > 1000)
# the three wrong readings of a two-bottle composite, each against every strength at every site (in mg/l bins)
for sf, merge, what in (('SF9', 'each', 'each bottle counted as its own composite'),
                        ('SF10', 'plain', 'a plain mean of the two bottles'),
                        ('SF11', 'drop2', 'the second bottle dropped')):
    moves = []
    for name, v in A.items():
        ot2, st2, n2 = G.strengths(T, cons[name], merge=merge)
        moves += [abs(round(ot2) - v['ot']), abs(round(st2) - v['st'])]
    ok('%s %s moves every one of the ten strengths by 2 bins or more' % (sf, what), min(moves) >= 2,
       'smallest %d, largest %d bins' % (min(moves), max(moves)))
# the bottle join at face value: the round sheet's bottle number against the sampler download log's
dl = G.rows(T, 'te_sampler_downloads_2025-01_2026-04.csv')
keys = [(r['sampling_point'], r['run_end'], r['bottle']) for r in dl]
ok('Ask A join: each sampler run and bottle appears once in the download log', len(keys) == len(set(keys)))
runs = defaultdict(list)
for r in dl:
    runs[r['sampling_point']].append((datetime.strptime(r['run_start'], '%d/%m/%Y %H:%M'),
                                      datetime.strptime(r['run_end'], '%d/%m/%Y %H:%M')))
overlap = 0
for pt, rr in runs.items():
    rr = sorted(set(rr))
    overlap += sum(1 for (s0, e0), (s1, e1) in zip(rr, rr[1:]) if s1 < e0)
ok('Ask A join: no logged run overlaps another at the same point, so point and time pick one run', overlap == 0)
sheet_keys = {(r['sampling_point'], r['collected_at'], r['bottle']) for r in G.rows(T, 'te_sampling_rounds_2025-01_2026-04.csv')}
ok('Ask A join: every bottle on the round sheets has its run and bottle in the log, and the reverse', sheet_keys == set(keys))
# the literal executor: the ten strengths rebuilt from the filed fields and nothing else
vol = {(r['sampling_point'], r['run_end'], r['bottle']): float(r['volume_ml']) for r in dl}
lab = defaultdict(dict)
for r in G.rows(T, 'lims_trade_effluent_results_2025-01_2026-04.csv'):
    lab[r['client_ref']][r['determinand']] = float(r['result'])
comp = defaultdict(list)
for r in G.rows(T, 'te_sampling_rounds_2025-01_2026-04.csv'):
    comp[(r['sampling_point'], r['collected_at'])].append(r)
lit = defaultdict(lambda: [[], []])
for (pt, when), bottles in comp.items():
    taken = datetime.strptime(when, '%d/%m/%Y %H:%M').date()
    if not (date(2025, 4, 1) <= taken <= date(2026, 3, 31)):
        continue
    w = [vol[(pt, when, b['bottle'])] for b in bottles]
    for k, det in enumerate(('COD settled', 'Suspended solids')):
        lit[pt][k].append(sum(wi * lab[b['bottle_ref']][det] for wi, b in zip(w, bottles)) / sum(w))
for name, v in A.items():
    pt = cons[name]['sampling_point']
    ok('Ask A literal executor rebuilds %s settled COD and suspended solids from the filed fields' % name,
       round(sum(lit[pt][0]) / len(lit[pt][0])) == v['ot'] and round(sum(lit[pt][1]) / len(lit[pt][1])) == v['st'])
codes = defaultdict(set)
for r in G.rows(T, 'lims_trade_effluent_results_2025-01_2026-04.csv'):
    codes[r['sample_point']].add(r['customer_code'])
ok('Ask A hazard: one sampling point carries two customer codes (the bottler before the laboratory migration)',
   sorted(len(v) for v in codes.values()) == [1, 1, 1, 1, 2], str(dict(codes)))

# ------------------------------------------------------------------ separation line and realism
main_files = ['allery_d_s_coldmere_wq_monitor_2024-10_2026-03.csv', 'coldmere_wrc_historian_hourly_2024-10_2026-03.csv',
              'thornlea_dairy_discharge_monitor_15min.csv', 'coldmere_ammonia_investigation_terms.docx']
ask_files = ['te_meter_reads_2025-26.csv', 'lims_trade_effluent_results_2025-01_2026-04.csv',
             'te_sampling_rounds_2025-01_2026-04.csv', 'te_sampler_downloads_2025-01_2026-04.csv',
             'trade_effluent_consents_register.xlsx', 'wendmoor_trade_effluent_charges_scheme_2025-26.pdf']
ok('separation: no ask device sits in a main-call file', not (set(main_files) & set(ask_files)))
files = sorted(os.listdir(T))
ok('input gate: 10 or more files', len(files) >= 10, str(len(files)))
ok('input gate: 3 or more formats', len({f.rsplit('.', 1)[1] for f in files}) >= 3)
big = max(sum(1 for _ in open(os.path.join(T, f), encoding='utf-8')) for f in files if f.endswith('.csv'))
ok('input gate: a file of 25,000 rows or more', big >= 25000, str(big))
pqp = os.path.join(T, 'coldmere_site_meters_halfhourly.parquet')
raw = open(pqp, 'rb').read()
flen = int.from_bytes(raw[-8:-4], 'little')
foot = raw[-8 - flen:-8]
ok('scrub: the parquet footer names a release writer and carries no arrow schema',
   b'parquet-mr version' in foot and b'ARROW:schema' not in foot and b'parquet-cpp' not in foot)
for f in files:
    if f.endswith(('.docx', '.xlsx')):
        z = zipfile.ZipFile(os.path.join(T, f))
        core = z.read('docProps/core.xml').decode()
        ok('scrub: %s carries an office author and no generator' % f, 'python' not in core.lower() and 'openpyxl' not in core.lower())
    if f.endswith('.pdf'):
        b2 = open(os.path.join(T, f), 'rb').read()
        ok('scrub: %s names Word, not reportlab' % f, b'ReportLab' not in b2 and b'reportlab' not in b2)
mon = G.rows(T, 'allery_d_s_coldmere_wq_monitor_2024-10_2026-03.csv')
ok('realism: the monitor file spans October 2024 to March 2026 as named',
   mon[0]['datetime_utc'].startswith('2024-09-30T23') and mon[-1]['datetime_utc'].startswith('2026-03-31T22'))
print('\n%d failures' % len(FAILS))
sys.exit(1 if FAILS else 0)
