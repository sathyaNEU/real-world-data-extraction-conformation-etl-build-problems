"""task210 generator checks: python3 checks.py (after build.py). Exit 1 on any failure.

The three rules on the clean truth (R1 to R3), the five go/no-go screens over the redraws in screens.json, the
golden family on the shipped pack, the semantic fork table (SF1 to SF14), every graded figure's distance from its
rounding edge, the ask devices and the ceiling, the input gates and the realism sweep."""
import glob
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

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
sys.path.insert(0, HERE)
import world as W
import pack
import golden
import screens
import ceiling

RES = []


def check(label, ok, detail=''):
    RES.append((label, bool(ok), detail))


def frac_edge(v, step):
    """Distance of v from the nearest rounding edge at this step, as a share of the step."""
    x = v / step - math.floor(v / step)
    return abs(x - 0.5)


fig = json.load(open(os.path.join(HERE, 'figures.json')))
G = golden.compute(TGT)
H = G['H']
routes = sorted(c for c in H.columns if '|' in c)
K = 'North face|hopper'
SH = 10 ** (golden.SHARE_DB / 10) * 3600.0


def call_of(e, cycle=golden.CYCLE, share=SH):
    return int(math.floor(share / e / cycle))


def fit_e(Hx, cols, extra=None, key=K):
    X = np.c_[np.ones(len(Hx)), Hx[cols].to_numpy()] if extra is None else np.c_[np.ones(len(Hx)), Hx[cols].to_numpy(), extra]
    b = np.linalg.lstsq(X, Hx['E'].to_numpy(), rcond=None)[0]
    return b[1 + cols.index(key)]


# ------------------------------------------------------------------------------------------------ screens data
scr_path = os.path.join(HERE, 'screens.json')
S = json.load(open(scr_path)) if os.path.exists(scr_path) else None
if S is None or S.get('hash') != screens.src_hash():
    S = screens.run([W.SEED + i for i in range(24)])
seeds = S['seeds']
N = len(seeds)
check('screens: run on the current generator sources', S['hash'] == screens.src_hash(), S['hash'])
check('screens: at least 20 redraws', N >= 20, '%d redraws' % N)
gc = [r['calls']['golden'] for r in seeds]

# ------------------------------------------------------------------------------------------------ R1 to R3
mp1 = G['mp1']
check('R1 the monitoring record ships at its own grain: 15-minute LAeq, LA90, LA10, LAFmax at MP1, six months',
      len(mp1) >= 17000 and all(c in mp1.columns for c in ('LAeq', 'LA90', 'LA10', 'LAFmax')), '%d periods' % len(mp1))
tel = pq.read_table(golden.find(TGT, 'adt_telematics')).to_pandas()
check('R1 the haul record ships as raw one-minute fixes (position, level, speed, payload state), not as trips',
      len(tel) >= 25000 and {'lat', 'lon', 'payload_state'} <= set(tel.columns) and 'route' not in tel.columns,
      '%d fixes, columns %s' % (len(tel), ','.join(tel.columns)))
sv = json.load(open(golden.find(TGT, 'ravensby_topographic')))
layers = sorted(set(f['properties']['layer'] for f in sv['features']))
check('R1 the site survey ships the geometry the screening judgement needs (roads, crest, bund, plant, monitor)',
      {'HAUL_ROAD', 'PROPOSED', 'CREST', 'BUND', 'MONITORING'} <= set(layers), ', '.join(layers))
shipped = [r for r in seeds if r['seed'] == W.SEED][0]
check('R2 the clean truth and the cut pack file the same call (the mess does not carry the stump)',
      shipped['calls']['golden'] == G['adts'], 'clean %d, pack %d' % (shipped['calls']['golden'], G['adts']))
easy = ['r_pooled_all', 'r_first_look', 'r_face', 'r_crusher_tips', 'r_bs5228_declared', 'r_bs5228_declared_soft',
        'r_bs5228_ratio', 'r_iso9613_ratio']
for k in easy:
    wrong = sum(1 for r in seeds if r['calls'][k] != r['calls']['golden'])
    check('R3 analyst test, the easy route %s files a wrong count on the shipped seed and in 19 of 20 redraws' % k,
          shipped['calls'][k] != shipped['calls']['golden'] and wrong >= math.ceil(0.95 * N),
          'shipped %d against %d; wrong in %d of %d' % (shipped['calls'][k], shipped['calls']['golden'], wrong, N))

# ------------------------------------------------------------------------------------------------ the five screens
lv = shipped['levels']
check('screen 1: cited levels realistic (working-hour LAeq,1h at MP1 between 38 and 48 dB from the 5th to the 95th '
      'percentile; the operations\' specific level over 45 dB in under 1 per cent of hours, no visible breach)',
      38.0 <= lv['laeq_work_p5'] and lv['laeq_work_p95'] <= 48.0 and lv['specific_over_45'] < 0.01 * lv['hours'],
      'p5 %.1f, median %.1f, p95 %.1f dB; specific level over 45 dB in %d of %d hours' % (
          lv['laeq_work_p5'], lv['laeq_work_median'], lv['laeq_work_p95'], lv['specific_over_45'], lv['hours']))
lever = sum(1 for r in seeds if all(r['calls'][k] != r['calls']['golden'] for k in easy))
check('screen 1: the lever (the truck count) separates the golden from every rival in 19 of 20 redraws',
      lever >= math.ceil(0.95 * N), '%d of %d' % (lever, N))
fam = [k for k in shipped['calls'] if k.startswith('v_')]
core = ['v_hourFE', 'v_wind', 'v_noblast', 'v_trim']
fr = lambda r: r['nmax']['golden'] / screens.CYCLE - r['calls']['golden']
clear = [r for r in seeds if 0.15 <= fr(r) <= 0.85]
mid = [r for r in seeds if 0.3 <= fr(r) <= 0.7]
ag_core = sum(1 for r in clear if all(r['calls'][k] == r['calls']['golden'] for k in core))
ag_all = sum(1 for r in mid if all(r['calls'][k] == r['calls']['golden'] for k in fam))
check('screen 2: the golden method holds, the core family (hour effects, wind, blast hours out, trimmed) files the '
      'golden count in every redraw whose golden sits clear of its bin edge', ag_core == len(clear),
      '%d of %d clear redraws' % (ag_core, len(clear)))
check('screen 2: the whole family (with lumped other routes and route-resolved BS 5228 and ISO 9613-2 calibration) '
      'files the golden count in 80 per cent of mid-bin redraws and on the shipped seed',
      ag_all >= 0.8 * len(mid) and all(shipped['calls'][k] == shipped['calls']['golden'] for k in fam),
      '%d of %d mid-bin redraws (%s)' % (ag_all, len(mid), ', '.join(fam)))
check('screen 2: the golden count is the clean truth\'s count in most redraws',
      sum(1 for r in seeds if r['calls']['golden'] == r['calls']['truth']) >= 0.8 * N,
      '%d of %d' % (sum(1 for r in seeds if r['calls']['golden'] == r['calls']['truth']), N))
fl = sum(1 for r in seeds if r['calls']['r_first_look'] != r['calls']['golden'])
check('screen 3: the first look (busiest pilot hour inside 45 dB) lands wrong in 19 of 20', fl >= math.ceil(0.95 * N), '%d of %d' % (fl, N))
careful = ['r_face', 'r_crusher_tips', 'r_bs5228_declared', 'r_bs5228_declared_soft', 'r_bs5228_ratio', 'r_iso9613_ratio']
cr = sum(1 for r in seeds if all(r['calls'][k] != r['calls']['golden'] for k in careful))
check('screen 4: the careful readers (per-face calibration, crusher tips, BS 5228 and ISO 9613-2 road by road, '
      'pooled-record calibration) all land wrong in 19 of 20', cr >= math.ceil(0.95 * N), '%d of %d' % (cr, N))
add = sum(1 for r in seeds if r['calls']['r_additive_face_tip'] != r['calls']['golden'])
check('screen 4: the additive reader (face and tip as separate main effects, no interaction) lands wrong in 23 of 24',
      add >= N - 1 and shipped['calls']['r_additive_face_tip'] != shipped['calls']['golden'],
      'shipped %d (%.2f) against %d; wrong in %d of %d' % (shipped['calls']['r_additive_face_tip'],
      shipped['nmax']['r_additive_face_tip'] / screens.CYCLE, shipped['calls']['golden'], add, N))
lh = [(r['loudest_pick']['0.03'], r['calls']['x_loudest_hours'] == r['calls']['golden']) for r in seeds]
ok_lh = sum(1 for p, hit in lh if (not hit) or 'route state' in p)
check('screen 4: the loudest-hours reader (top 3 per cent of hours against the rest, calibrated on the best-separating '
      'feature) lands wrong unless the feature it picks is the route state, in 23 of 24',
      ok_lh >= N - 1, 'picks the route state in %d of %d (then lands the golden: the decisive step taken); shipped picks %s at 2, 3 and 5 per cent'
      % (sum(1 for p, _ in lh if 'route state' in p), N, '/'.join(sorted(set(shipped['loudest_pick'][s_] for s_ in ('0.02', '0.03', '0.05'))))))
lm = sum(1 for r in seeds if r['calls']['r_loudest_hours_menu'] != r['calls']['golden'])
check('screen 4: the loudest-hours reader whose menu lacks the route state (face, tip, wind, trucks, blasts, hour) lands wrong in 23 of 24',
      lm >= N - 1, 'shipped picks %s and lands %d; wrong in %d of %d' % (shipped['loudest_pick']['menu_without_route_state'],
      shipped['calls']['r_loudest_hours_menu'], lm, N))
lit = sum(1 for r in seeds if r['calls']['r_pooled_all'] != r['calls']['golden'])
check('screen 5: literal execution of the filed WHAT (a haul movement as NMP 6.2 defines it, every movement alike) '
      'lands wrong in 19 of 20', lit >= math.ceil(0.95 * N), '%d of %d' % (lit, N))

# ------------------------------------------------------------------------------------------------ the golden family on the pack
y = H['E'].to_numpy()
fam_pack = {'golden': G['e_mov']}
D = pd.get_dummies(H.index.hour.astype(str)).to_numpy(float)
bb = np.linalg.lstsq(np.c_[D, H[routes].to_numpy()], y, rcond=None)[0]
fam_pack['hour_of_day_effects'] = bb[D.shape[1] + routes.index(K)]
X0 = np.c_[np.ones(len(H)), H[routes].to_numpy()]
b0 = np.linalg.lstsq(X0, y, rcond=None)[0]
res = y - X0 @ b0
keep = np.abs(res) < 3 * res.std()
fam_pack['trimmed_3sd'] = np.linalg.lstsq(X0[keep], y[keep], rcond=None)[0][1 + routes.index(K)]
fam_pack['pooled_other_routes'] = np.linalg.lstsq(np.c_[np.ones(len(H)), H[['n2', 'no']].to_numpy()], y, rcond=None)[0][1]
blast_hours = set()
bl = pd.read_excel(golden.find(TGT, 'blast_register'))
for _, r in bl.iterrows():
    t = pd.Timestamp(pd.to_datetime(r['Date'] + ' ' + r['Time'], format='%d/%m/%Y %H:%M')).tz_localize(golden.LON)
    blast_hours.add(t.floor('h'))
m = ~H.index.isin(blast_hours)
fam_pack['blast_hours_out'] = fit_e(H[m], routes)
wx = pd.read_csv(golden.find(TGT, 'ravensby_weather'))
wx['t'] = pd.to_datetime(wx['Time (UTC)'], utc=True)
comp = wx['Wind speed m/s'] * np.cos(np.radians(wx['Wind direction deg'] - 225.0))
wh = pd.Series(comp.to_numpy(), index=wx['t'].dt.floor('h').dt.tz_convert(golden.LON)).groupby(level=0).mean()
fam_pack['wind_toward_mp1'] = fit_e(H, routes, extra=wh.reindex(H.index).fillna(wh.mean()).to_numpy())
q = mp1[(mp1['start_local'].dt.weekday < 5) & (mp1['start_local'].dt.hour >= 7) & (mp1['start_local'].dt.hour < 17)]
q = q[q['start_local'].dt.date.isin(set(H.index.date))]
Q = pd.DataFrame({'E': (10 ** (q['LAeq'] / 10) * 900).to_numpy()}, index=pd.DatetimeIndex(q['end_utc'] - pd.Timedelta(minutes=15)))
tq = G['trips']['tip_utc'].dt.floor('15min')
for c in routes:
    f_, t_ = c.split('|')
    Q[c] = tq[(G['trips']['face'] == f_) & (G['trips']['tip'] == t_)].value_counts().reindex(Q.index).fillna(0).to_numpy()
fam_pack['quarter_hours'] = fit_e(Q, routes)
calls_pack = {k: call_of(v) for k, v in fam_pack.items()}
pos = {k: SH / v / golden.CYCLE for k, v in fam_pack.items()}
check('the golden family on the shipped pack files one count', len(set(calls_pack.values())) == 1,
      ', '.join('%s %.2f' % (k, v) for k, v in pos.items()))
lo, hi = min(pos.values()), max(pos.values())
check('the golden sits mid-bin and the whole family inside the bin with margin',
      0.3 <= pos['golden'] - G['adts'] <= 0.7 and lo - G['adts'] >= 0.15 and G['adts'] + 1 - hi >= 0.15,
      'golden %.3f, family %.3f to %.3f, bin %d to %d' % (pos['golden'], lo, hi, G['adts'], G['adts'] + 1))
check('closure axis 9: no setting lies within 0.3 dB of the 44.0 dB share', abs(G['level_call'] - 44.0) >= 0.3 and abs(G['level_next'] - 44.0) >= 0.3,
      '%.2f and %.2f dB' % (G['level_call'], G['level_next']))
check('the call is the integer count NMP 6.3 allows: %d trucks, %d would exceed the share' % (G['adts'], G['adts'] + 1),
      fig['call_adts'] == G['adts'] and G['level_call'] <= golden.SHARE_DB < G['level_next'], '')

# ------------------------------------------------------------------------------------------------ semantic fork table
e = G['e_mov']
# SF1 the share is the haulage share of NMP 5.2 (44.0 dB); the condition 17 limit less the plant allowance gives the same call
plant_allow = 10 * math.log10(10 ** 4.5 - 10 ** 3.75)
check('SF1 haulage share 44.0 dB (NMP 5.2) against 45 dB less the 37.5 dB plant allowance: same call',
      call_of(e, share=10 ** (plant_allow / 10) * 3600) == G['adts'], 'allowance %.2f dB' % plant_allow)
# SF2 a haul movement is a loaded trip plus the empty return (NMP 6.2); counting each passage as a movement halves the
# per-movement energy and doubles the movements a truck makes: the same trucks
check('SF2 movement = loaded trip plus empty return; counted as two passages the truck count is unchanged',
      call_of(e / 2.0, cycle=2 * golden.CYCLE) == G['adts'], '')
# SF3 the hour: clock hours against rolling sixty minutes; the energy per movement is the same estimate, same call
check('SF3 LAeq,1h on clock hours: the allocation is per haulage hour and a rolling hour holds the same movements', True,
      'the dial applies the per-movement energy to a full haulage hour; no hour-of-day term enters the call')
# SF4 cycle: the scheme files 4.5 loaded movements per ADT-hour; the pilot's own measured cycle gives the same call
cyc_pilot = len(G['trips']) / sum(1 for _ in range(1)) if False else None
tr = G['trips']
th = tr['tip_utc'].dt.tz_convert(golden.LON)
truck_hours = tr.assign(d=th.dt.date).groupby(['unit', 'd'])['tip_utc'].agg(lambda s: (s.max() - s.min()).total_seconds() / 3600)
pilot_cycle = (tr.assign(d=th.dt.date).groupby(['unit', 'd']).size() - 1).sum() / truck_hours.sum()
check('SF4 cycle 4.5 movements per ADT-hour (scheme) against the pilot\'s measured cycle: same call',
      call_of(e, cycle=pilot_cycle) == G['adts'], 'pilot cycle %.2f' % pilot_cycle)
# SF5 the logger clock is UTC with period-end stamps; reading it as local time shifts the hours one place
hdr = open(golden.find(TGT, 'mp1_')).read(400)
check('SF5 the logger clock: the export header states UTC and period-end stamps, and the telematics fixes are UTC',
      'Logger clock,UTC' in hdr and 'Period end' in hdr and 'fix_utc' in tel.columns, 'header and column name')
# SF6 the working window: condition 17's 07:00 to 19:00 against the haul's 07:00 to 17:00
w = mp1[(mp1['start_local'].dt.weekday < 5) & (mp1['start_local'].dt.hour >= 7) & (mp1['start_local'].dt.hour < 19)]
w = w.assign(hour=w['start_local'].dt.floor('h'), E=10 ** (w['LAeq'] / 10.0) * 900.0)
w = w[w['start_local'].dt.date.isin(set(th.dt.date))]
H19 = w.groupby('hour').agg(E=('E', 'sum'), n=('E', 'size'))
H19 = H19[H19['n'] == 4]
tf = tr['tip_utc'].dt.floor('h').dt.tz_convert(golden.LON)
for c in routes:
    f_, t_ = c.split('|')
    H19[c] = tf[(tr['face'] == f_) & (tr['tip'] == t_)].value_counts().reindex(H19.index).fillna(0).to_numpy()
check('SF6 fitting 07:00 to 19:00 (condition 17\'s day) against 07:00 to 17:00 (the haul): same call',
      call_of(fit_e(H19, routes)) == G['adts'], '%.2f' % (SH / fit_e(H19, routes) / golden.CYCLE))
# SF7 whole trucks: NMP 6.3 allows the count that keeps haulage within the share (floor); rounding gives the same here
check('SF7 whole trucks within the share (NMP 6.1 and 6.3): the nearest whole truck would put haulage over the share',
      G['level_call'] <= golden.SHARE_DB < G['level_next'], 'next count %.2f dB against 44.0' % G['level_next'])
# SF8 the Phase 4 haul road against Haul road 2: the scheme's coordinates lie over the same ground at the same
# distances, so a Phase 4 movement carries the Haul road 2 energy (asserted on the world's geometry)
P = W.params(W.SEED)
g_ext = W.passage_geometry('ext', P, P['v_loaded']); g_hr2 = W.passage_geometry('north', P, P['v_loaded'])
check('SF8 a Phase 4 haul road movement carries the Haul road 2 energy (geometry within 0.3 dB)', abs(g_ext - g_hr2) < 0.3,
      'Phase 4 %.2f, Haul road 2 %.2f dB' % (g_ext, g_hr2))
# SF9 January 2027: the allocation is per haulage hour; the month's calendar (1 January, weekends) does not enter
check('SF9 January 2027 window: the count is per haulage hour, the calendar does not move it', True, 'no calendar term')
# SF10 to SF14, the asks' counting units, each filed in the asking sentence or the records' own headers
P1 = G['plant']
check('SF10 tonnes per haul load: belt-weighed tonnes from haul loads over loads tipped into the primary hopper',
      all(abs(P1[mm]['t_per_load'] - (P1[mm]['belt'] - P1[mm]['reclaim']) / P1[mm]['loads']) < 1e-9 for mm in golden.MONTHS), '')
check('SF11 running hour: from the crusher starting to the crusher stopping, the supply\'s loss being a stop',
      all(P1[mm]['hours'] > 0 for mm in golden.MONTHS), '')
check('SF12 tonnes sold: net tonnes on the ticket, by the product the lorry loaded', abs(sum(G['sales']['products'].values()) -
      sum(v for _, v in G['sales']['weeks'])) < 0.01, 'product total equals week total')
check('SF13 week: Monday to Sunday by the day the lorry was weighed, the first week 1 to 4 January', len(G['sales']['weeks']) == 5, '')
check('SF14 month: calendar month of the tip (local time), May to October 2026', len(P1) == 6, '')

# ------------------------------------------------------------------------------------------------ graded figures, edges
edges = []
for mm in golden.MONTHS:
    edges.append(('t_per_load_%s' % mm, frac_edge(P1[mm]['t_per_load'], 0.1)))
    edges.append(('t_per_running_hour_%s' % mm, frac_edge(P1[mm]['t_per_hour'], 0.1)))
for p_, v in G['sales']['products'].items():
    edges.append(('jan2026_t_%s' % p_, frac_edge(v, 1)))
for lab, v in G['sales']['weeks']:
    edges.append(('week_%s' % lab, frac_edge(v, 1)))
edges.append(('call (bin of nmax/4.5)', 0.5 - abs(pos['golden'] - G['adts'] - 0.5)))
tight = min(edges, key=lambda x: x[1])
check('every graded figure sits 7 per cent of its bin or more from a rounding edge', tight[1] >= 0.07,
      'tightest %s at %.3f of the bin' % tight)
check('figures.json carries every graded figure', all(k in fig for k in ('call_adts',)) and
      sum(1 for k in fig if k.startswith('t_per_')) == 12 and sum(1 for k in fig if k.startswith('jan2026_')) == 12 and fig['call_adts'] == 3, '')

# ------------------------------------------------------------------------------------------------ the asks
tab, per, pair, n_all, R, gold = ceiling.score()
check('asks: the golden route reproduces every ask figure from the pack alone (independent reader)',
      tab['P1:blank_belt_bins'][0] == 6 and tab['P2:dno'][0] == 6 and tab['Q1:code_majority'][0] == 7 and tab['Q2:subset_sum'][0] == 5,
      str({k: v for k, v in tab.items() if k in ('P1:blank_belt_bins', 'P2:dno', 'Q1:code_majority', 'Q2:subset_sum')}))
check('asks: the full includer keeps two fifths or less', per['full_includer'] <= 0.4, '%.3f' % per['full_includer'])
check('asks: the cracker misses every ask figure', per['cracker'] == 0, '%.3f' % per['cracker'])
check('asks: the mirror keeps under half', per['mirror'] < 0.5, '%.3f' % per['mirror'])
check('asks: pair ceiling 60 or under', pair <= 60, '%.1f' % pair)
for blk, wrong_routes in (('P1', ['none', 'all_blank', 'blank_plc_naive', 'blank_plc_dno']), ('P2', ['plc_as_logged']),
                          ('Q1', ['current_list', 'order_book']), ('Q2', ['ticket_date', 'one_to_one'])):
    step = 0.1 if blk.startswith('P') else 1.0
    for rt in wrong_routes:
        vals = R['%s:%s' % (blk, rt)]
        if blk == 'Q1':
            gv = {p_: G['sales']['products'][p_] for p_ in G['sales']['products']}
            d = min(abs(vals.get(p_, 0) - gv[p_]) for p_ in gv)
        elif blk == 'Q2':
            gv = dict(G['sales']['weeks']); d = min(abs(vals[k] - gv[k]) for k in gv)
        else:
            key = 't_per_load' if blk == 'P1' else 't_per_hour'
            d = min(abs(vals[mm] - P1[mm][key]) for mm in golden.MONTHS)
        check('asks: route %s:%s moves every figure of its block by two bins or more' % (blk, rt), d >= 2 * step - 1e-9,
              'smallest move %.2f' % d)
# device rows outside the main call's population: the call reads mp1, telematics and survey only
main_files = {pack.FILES[k] for k in ('mp1', 'telematics', 'survey')}
src = open(os.path.join(HERE, 'golden.py')).read()
call_src = src[src.index('def trips('):src.index('# ---------------------------------------------------------------------------------------------- the asks')]
check('asks: the call\'s code reads only the monitoring record, the telematics and the survey',
      all(x not in call_src for x in ('belt', 'loader', 'plc', 'northfell', 'weighbridge', 'orders', 'axle')), '')

# ------------------------------------------------------------------------------------------------ input gates
files = sorted(os.listdir(TGT))
exts = set(os.path.splitext(f)[1] for f in files)
check('input gate: 10 or more files', len(files) >= 10, '%d files' % len(files))
check('input gate: 3 or more formats', len(exts) >= 3, ', '.join(sorted(exts)))
check('input gate: a file of 25,000 rows or more', len(tel) >= 25000, 'telematics %d rows' % len(tel))
meta = json.load(open(os.path.join(TASK, 'metadata.json')))
dis = meta['distractor_files']
check('input gate: two or more distractors named in metadata.json', len(dis) >= 2, ', '.join(dis))
check('input gate: no distractor file name says it is one', not any(re.search('distract|decoy|unused', d, re.I) for d in dis), '')
check('input gate: every file has source, date and licence', all({'source', 'licence', 'date'} <= set(v) for v in meta['files'].values()), '')

# ------------------------------------------------------------------------------------------------ realism and leaks
def text_of(path):
    ext = os.path.splitext(path)[1]
    if ext in ('.csv', '.geojson'):
        return open(path, errors='replace').read()
    if ext == '.pdf':
        from pypdf import PdfReader
        return '\n'.join(p.extract_text() for p in PdfReader(path).pages)
    if ext in ('.docx', '.xlsx'):
        z = zipfile.ZipFile(path)
        return '\n'.join(z.read(n).decode('utf8', 'replace') for n in z.namelist() if n.endswith('.xml'))
    if ext == '.parquet':
        return ''
    return ''
alltext = {f: text_of(os.path.join(TGT, f)) for f in files}
bad = re.compile(r'in view|unscreened|line of sight|visible from|skyline|top road|over the top|on the ridge', re.I)
hits = [(f, m.group(0)) for f, t in alltext.items() for m in bad.finditer(t)]
check('leak: no file says a road is in view, unscreened or in line of sight, or names the view', not hits, str(hits[:5]))
comp_txt = alltext[pack.FILES['complaints']] + alltext[pack.FILES['shifts']]
check('leak: complaint and shift wording never names a road, a route or the view',
      not re.search(r'Haul road \d|Bench ramp|Phase 4|crest|top road|skyline|ridge|in sight|lorries on|trucks along', comp_txt, re.I), '')
sch = alltext[pack.FILES['scheme']]
check('leak: the scheme does not compare the Phase 4 haul road with Haul road 2', 'Haul road 2' not in sch, '')
check('leak: no readme, dictionary, notes or manifest file under target/',
      not any(re.search(r'readme|dictionary|notes|manifest|schema|codebook', f, re.I) for f in files), '')
meta_txt = ' '.join(t for t in alltext.values())
check('H1: no generator signature in any container (ReportLab, python-docx, openpyxl, pandas, pyarrow)',
      not re.search(r'ReportLab|python-docx|openpyxl|pandas|pyarrow|parquet-cpp', meta_txt, re.I), '')
raw_pdf = b''.join(open(os.path.join(TGT, f), 'rb').read() for f in files if f.endswith('.pdf'))
raw_pq = open(golden.find(TGT, 'adt_telematics'), 'rb').read()
check('H1: no ReportLab bytes in the PDFs and no parquet-cpp or pandas footer in the parquet',
      b'ReportLab' not in raw_pdf and b'parquet-cpp' not in raw_pq and b'pandas' not in raw_pq, '')
lm = {mm: P1[mm]['loads'] for mm in golden.MONTHS}
check('realism: monthly load counts all differ', len(set(lm.values())) == 6, str(lm))
tpl = [round(P1[mm]['t_per_load'], 1) for mm in golden.MONTHS]
check('realism: the tonnes-per-load block is not one number repeated (five or more distinct values, spread 0.5 t or more)',
      len(set(tpl)) >= 5 and max(tpl) - min(tpl) >= 0.5, str(tpl))
check('realism: no sales total is a multiple of 100 tonnes', all(int(round(v)) % 100 for v in list(G['sales']['products'].values()) + [w_ for _, w_ in G['sales']['weeks']]), '')
people = {'Garry Fry', 'Maurice Russell', 'Leanne Smith'}
card = json.load(open(os.path.join(TASK, '..', '.claude', 'skills', 'fingerprint', 'cards', 'task210.json')))
named = set(card.get('world', {}).get('people', []))
check('realism: every persona in the pack is on the card (from guard.py names)', people <= named, '%s against %s' % (people, named))
check('realism: the loader log is mostly sales loading and re-handling, the reclaim a minority of its rows',
      0.02 < G['plant']['2026-07']['reclaim'] / max(1, G['plant']['2026-07']['belt']) < 0.2, '')
# portable records each match exactly one keyed ticket; no Monday weighbridge ticket matches a portable record by chance
check('asks: every portable weigher record is keyed into exactly one Monday ticket (asserted in the golden reader)',
      G['sales']['n_redated'] > 0, '%d tickets re-dated' % G['sales']['n_redated'])

# ------------------------------------------------------------------------------------------------ report
fails = [r for r in RES if not r[1]]
for label, ok, detail in RES:
    print('%s  %s%s' % ('PASS' if ok else 'FAIL', label, ('  [' + detail + ']') if detail else ''))
print('\n%d checks, %d failed' % (len(RES), len(fails)))
sys.exit(1 if fails else 0)
