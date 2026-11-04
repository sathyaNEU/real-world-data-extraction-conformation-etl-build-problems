"""Independent verifier: reads every shipped file back in its own format, recomputes the call with its own code
(no generator import), and checks the golden deliverables against figures.json. Exit 1 on any failure."""
import csv
import io
import json
import math
import os
import re
import sys
import zipfile
import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT, GLD = os.path.join(TASK, 'target'), os.path.join(TASK, 'golden')
fails = []


def ok(label, cond, detail=''):
    print('%s  %s%s' % ('PASS' if cond else 'FAIL', label, ('  [%s]' % detail) if detail else ''))
    if not cond:
        fails.append(label)


def path(prefix, d=TGT):
    return os.path.join(d, [f for f in sorted(os.listdir(d)) if f.startswith(prefix)][0])


# every file opens in its own format
for f in sorted(os.listdir(TGT)):
    p = os.path.join(TGT, f)
    ext = os.path.splitext(f)[1]
    try:
        if ext == '.csv':
            n = sum(1 for _ in open(p))
        elif ext == '.parquet':
            n = pq.read_metadata(p).num_rows
        elif ext == '.geojson':
            n = len(json.load(open(p))['features'])
        elif ext == '.pdf':
            n = len(PdfReader(p).pages)
        elif ext == '.xlsx':
            n = sum(len(v) for v in pd.read_excel(p, sheet_name=None).values())
        elif ext == '.docx':
            n = len(zipfile.ZipFile(p).read('word/document.xml'))
        else:
            n = -1
        ok('opens: %s' % f, n > 0, '%d' % n)
    except Exception as ex:
        ok('opens: %s' % f, False, repr(ex))

# the call, recomputed: loaded runs from the fixes, face and tip by nearest surveyed point, hourly energy per route
sv = json.load(open(path('ravensby_topographic')))
pts = {}
for ft in sv['features']:
    g = ft['geometry']
    if g['type'] == 'Point':
        pts[ft['properties']['name']] = g['coordinates'][:2]
    elif ft['properties']['name'] == 'Run-of-mine stockpile':
        pts['Run-of-mine stockpile'] = list(np.array(g['coordinates'][0])[:-1, :2].mean(axis=0))
faces = {k: v for k, v in pts.items() if k.endswith('face')}
t = pq.read_table(path('adt_telematics')).to_pandas().sort_values(['unit_id', 'fix_utc']).reset_index(drop=True)
t['fix_utc'] = pd.to_datetime(t['fix_utc'], utc=True)
c = math.cos(math.radians(54.3))
def near(lon, lat, cands):
    return min(cands, key=lambda k: ((cands[k][0] - lon) * c) ** 2 + (cands[k][1] - lat) ** 2)
rows = []
for u, g in t.groupby('unit_id'):
    st = g['payload_state'].to_numpy(); lon = g['lon'].to_numpy(); lat = g['lat'].to_numpy(); tm = g['fix_utc'].to_numpy()
    for i in range(1, len(st)):
        if st[i] == 'LOADED' and st[i - 1] == 'EMPTY':
            j = i
            while j < len(st) and st[j] == 'LOADED':
                j += 1
            if j < len(st):
                fc = near(lon[i - 1], lat[i - 1], faces)
                tip = near(lon[j], lat[j], {'hopper': pts['Primary crusher feed hopper'], 'stock': pts['Run-of-mine stockpile']})
                rows.append((fc, tip, pd.Timestamp(tm[j])))
tr = pd.DataFrame(rows, columns=['face', 'tip', 't'])
raw = open(path('mp1_')).read().splitlines()
k = [i for i, l in enumerate(raw) if l.startswith('Period end')][0]
m = pd.read_csv(io.StringIO('\n'.join(raw[k:])))
m.columns = ['end', 'LAeq', 'LA90', 'LA10', 'LAFmax']
m['s'] = pd.to_datetime(m['end']).dt.tz_localize('UTC') - pd.Timedelta(minutes=15)
m['loc'] = m['s'].dt.tz_convert('Europe/London')
m = m[(m['loc'].dt.weekday < 5) & (m['loc'].dt.hour >= 7) & (m['loc'].dt.hour < 17)]
m = m[m['loc'].dt.date.isin(set(tr['t'].dt.tz_convert('Europe/London').dt.date))]
m['h'] = m['s'].dt.floor('h')
Hh = m.groupby('h').agg(E=('LAeq', lambda x: (10 ** (x / 10) * 900).sum()), n=('LAeq', 'size'))
Hh = Hh[Hh['n'] == 4]
tr['h'] = tr['t'].dt.floor('h')
X = [np.ones(len(Hh))]
keys = sorted(set(zip(tr['face'], tr['tip'])))
for key in keys:
    X.append(tr[(tr['face'] == key[0]) & (tr['tip'] == key[1])]['h'].value_counts().reindex(Hh.index).fillna(0).to_numpy())
b = np.linalg.lstsq(np.array(X).T, Hh['E'].to_numpy(), rcond=None)[0]
e = b[1 + keys.index(('North face', 'hopper'))]
nmax = 10 ** 4.4 * 3600 / e
call = int(math.floor(nmax / 4.5))
fig = json.load(open(os.path.join(HERE, 'figures.json')))
ok('the call recomputes independently', call == fig['call_adts'], '%d trucks (%.2f movements an hour at the share)' % (call, nmax))
# the noise plan's residual, read with this verifier's own extractor, and the call with the baseline fixed at it
nmp = ' '.join(' '.join(pg.extract_text().split()) for pg in PdfReader(path('ravensby_noise_management_plan')).pages)
mr = re.search(r'residual sound level of (\d+\.\d) dB', nmp)
ok('NMP 5.2 files the residual measured with the site stopped', mr is not None, mr.group(0) if mr else 'missing')
if mr:
    base = 3600.0 * (10 ** 3.75 + 10 ** (float(mr.group(1)) / 10))
    bf = np.linalg.lstsq(np.array(X[1:]).T, Hh['E'].to_numpy() - base, rcond=None)[0]
    nf = 10 ** 4.4 * 3600 / bf[keys.index(('North face', 'hopper'))]
    ok('the call recomputes with the baseline fixed at the plant and the filed residual', int(math.floor(nf / 4.5)) == fig['call_adts'],
       '%.2f movements an hour' % nf)
# the note's geometry sentence: the Phase 4 haul road against Haul road 2, from the survey alone
lines = {ft['properties']['name']: ft['geometry']['coordinates'] for ft in sv['features'] if ft['geometry']['type'] == 'LineString'}
mp = pts['MP1 Ulverthorpe Lane']
def loc(cs):
    return [((c[0] - mp[0]) * 111320.0 * math.cos(math.radians(mp[1])), (c[1] - mp[1]) * 111132.0) for c in cs]
def walk(cs, n=300):
    p = loc(cs); seg = [math.dist(p[i], p[i + 1]) for i in range(len(p) - 1)]; L = sum(seg); out = []
    for j in range(n + 1):
        s, i = L * j / n, 0
        while i < len(seg) - 1 and s > seg[i]:
            s -= seg[i]; i += 1
        f = min(1.0, s / seg[i]); out.append(math.hypot(p[i][0] + f * (p[i + 1][0] - p[i][0]), p[i][1] + f * (p[i + 1][1] - p[i][1])))
    return L, out
L2, r2 = walk(lines['Haul road 2']); L4, r4 = walk(lines['Phase 4 haul road'])
ok('the Phase 4 haul road is Haul road 2\'s length within a metre and its distance from MP1 within a metre all along it',
   abs(L2 - L4) < 1.0 and max(abs(a - b) for a, b in zip(r2, r4)) < 1.0,
   'lengths %.1f and %.1f m, largest distance gap %.2f m, %.0f to %.0f m from MP1' % (L2, L4, max(abs(a - b) for a, b in zip(r2, r4)), r2[0], r2[-1]))
ok('the belt scale export states interval-start stamps on the site clock',
   open(path('primary_belt_scale')).read(200).count('Interval start,Tonnes') == 1)

# the golden deliverables carry the graded figures
with open(os.path.join(GLD, 'extension_haul_dial.csv')) as fh:
    dial = list(csv.DictReader(fh))
ok('dial: twelve settings', len(dial) == 12)
ok('dial: verdicts match figures.json', all(r['within_44_0_dB_haulage_share'] == fig['dial_%02d_within_share' % int(r['adts_on_phase4_haul_road'])] for r in dial))
ok('dial: the last setting within the share is the call', max(int(r['adts_on_phase4_haul_road']) for r in dial if r['within_44_0_dB_haulage_share'] == 'yes') == fig['call_adts'])
txt = '\n'.join(p.extract_text() for p in PdfReader(os.path.join(GLD, 'extension_scheme_note.pdf')).pages)
for kf, v in fig.items():
    if kf.startswith('t_per_'):
        ok('note carries %s' % kf, ('%.1f' % v) in txt, '%.1f' % v)
    elif kf.startswith('jan2026_'):
        ok('note carries %s' % kf, '{:,}'.format(v) in txt, '{:,}'.format(v))
ok('note names the allocation', re.search(r'\bThree articulated dump trucks\b', txt) is not None)
meta = PdfReader(os.path.join(GLD, 'extension_scheme_note.pdf')).metadata
ok('note metadata scrubbed', 'ReportLab' not in str(meta) and 'reportlab' not in open(os.path.join(GLD, 'extension_scheme_note.pdf'), 'rb').read().decode('latin1').lower(), str(meta))
print('\n%d failed' % len(fails))
sys.exit(1 if fails else 0)
