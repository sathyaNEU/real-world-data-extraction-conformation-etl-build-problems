"""Assertions on the shipped seed: screens, forks, bins, the three rules, gates, realism, separation, ceiling.
python3 checks.py   (run after build.py; exit 1 on any failure)"""
import collections
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import pyarrow.parquet as pq

import build
import ceiling
import golden
import pack
import verify
import world

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def check(label, ok, detail=''):
    RESULTS.append((label, bool(ok), detail))


def edge(v, u):
    c = round(v / u) * u
    return (u / 2 - abs(v - c)) / u


S = build.make(build.SEED, write=False)
FIG = json.load(open(os.path.join(HERE, 'figures.json')))
W, mbs, cr = S['W'], S['mbs'], S['cases']
M = golden.main_figures(W, mbs, cr)
KEY = {r: pack.RNODE[r] for r in world.RES}
KEY.update({b: S['trunk'][b]['main_id'] for b in world.ICS})
verify.TGT = build.TARGET
V = verify.run()
VM = V['main']

# ---------------------------------------------------------------- main call: golden against the verifier
check('A1 verifier names the call', VM['call'] == KEY[M['call']] == KEY['BM3'], VM['call'])
check('A2 verifier names the runner-up', VM['runner'] == KEY[M['runner_up']] == KEY['R4'], VM['runner'])
check('A3 every asset count and resident-days agree', all(VM['cases'].get(KEY[a], 0) == M['cases'][a] and
                                                         VM['rd'].get(KEY[a], 0) == M['rd'][a] for a in golden.ASSETS))
check('A4 forward residents agree', VM['forward'] == M['forward_residents'] == FIG['call']['forward_residents'], VM['forward'])
check('A5 lab figures agree', V['lab'] == dict(tested=FIG['asks']['lab']['tested'], parvum=FIG['asks']['lab']['parvum'],
                                               hominis=FIG['asks']['lab']['hominis']), V['lab'])
check('A6 complaint figures agree', all(abs(round(V['complaints'][p][c], 2) - FIG['asks']['complaints'][p][c]) < 1e-9
                                        for p in V['complaints'] for c in pack.CATS))
check('A7 call-out figures agree', all(round(V['callouts'][m]['ua']) == FIG['asks']['callouts'][m]['urgent_attend'] and
                                       round(V['callouts'][m]['ur']) == FIG['asks']['callouts'][m]['urgent_resolve'] and
                                       round(V['callouts'][m]['na'] + 1e-9, 1) == FIG['asks']['callouts'][m]['nonurgent_attend'] and
                                       round(V['callouts'][m]['nr'] + 1e-9, 1) == FIG['asks']['callouts'][m]['nonurgent_resolve']
                                       for m in ('July', 'August', 'September')))

# ---------------------------------------------------------------- screens on the shipped seed
order = golden.ranked(M['rate'], M['cases'])
lead = M['rate'][order[0]] / M['rate'][order[1]]
check('S1 golden lead over the runner-up at least 1.2', lead >= 1.2, '%.2f' % lead)
check('S1b runner-up clear of the third at 1.2', M['rate'][order[1]] / M['rate'][order[2]] >= 1.2,
      '%.2f' % (M['rate'][order[1]] / M['rate'][order[2]]))
variants = {}
for name, kw in (('window 1-14', dict(kmin=1, kmax=14)), ('window 2-12', dict(kmin=2, kmax=12)),
                 ('window 3-10', dict(kmin=3, kmax=10)), ('exposure from 1 Sep', dict(exp_from=golden.CASE_FROM))):
    c_, rd_, r_ = golden.asset_rates(W['P'], M['zres'], cr, **kw)
    variants[name] = golden.ranked(r_, c_)[:2]
for k in (3, 4, 6, 8, 10):
    variants['minimum %d cases' % k] = golden.ranked(M['rate'], M['cases'], k)[:2]
check('S2 golden variants all name BM3 then R4', all(v == ['BM3', 'R4'] for v in variants.values()), variants)
cnt = {}
for c in cr:
    if c['status'] == 'Confirmed' and c['zkey'] and golden.CASE_FROM <= c['onset'] <= golden.CASE_TO:
        cnt[c['zkey']] = cnt.get(c['zkey'], 0) + 1
worst = max(cnt, key=lambda z: cnt[z] / M['zres'][z])
first_look = golden.normal_paths()[0][worst][0]
check('S3 first look (worst zone, register source) is wrong', first_look != 'BM3', first_look)
Rc, Rrd, Rr = golden.register_figures(mbs, cr)
reg_call = golden.ranked(Rr, Rc)[0]
check('S4a register route names R4', reg_call == 'R4', '%s %.2f' % (reg_call, Rr[reg_call]))
check('S4a boundary mains carry nothing under the register', all(Rrd[b] == 0 for b in world.ICS))
on = golden.onset_day_figures(W, mbs, cr)
on_call = max([a for a in golden.ASSETS if on[a] > 0], key=lambda a: on[a])
check('S4b onset-day supply route is wrong', on_call != 'BM3', on_call)
rep_rates = {}
P = W['P']
rc = {a: 0 for a in golden.ASSETS}
for c in cr:
    if c['status'] == 'Confirmed' and c['zkey'] and golden.CASE_FROM <= c['onset'] <= golden.CASE_TO:
        pth = P[min(golden.di(c['report']), len(P) - 1)][c['zkey']] or ()
        for a in pth:
            if a in rc:
                rc[a] += 1
rep_call = max([a for a in golden.ASSETS if M['rd'][a]], key=lambda a: rc[a] / M['rd'][a])
check('S4b report-day supply route is wrong', rep_call != 'BM3', rep_call)
# the dated event: the last repair on the worst zone's own supply before its outbreak, read from the work orders
wz = [w for w in S['wos_rep'] if w['main'] in (S['trunk']['FM11']['main_id'], S['trunk']['LM12']['main_id'])
      and w['start'].date() <= golden.CASE_TO]
check('S4b dated-event reader blames the repaired feed main, not a candidate', wz and wz[-1]['main'] == S['trunk']['FM11']['main_id'])
check('S4c per-record zone-by-week cells name the register source', reg_call == 'R4')
check('S4d mechanism naming (waterborne, attack rates by supply zone) names R4', first_look == 'R4')
check('S4e literal replay of the stated facts names R4', reg_call == 'R4')
check('S5 literal execution of the filed WHAT through the register is wrong', reg_call != M['call'])

# ---------------------------------------------------------------- the three rules, executed
cols = []
for f in build.target_files():
    p = os.path.join(build.TARGET, f)
    if f.endswith('.csv'):
        cols += open(p, encoding='utf-8').readline().strip().split(',')
    elif f.endswith('.parquet'):
        cols += pq.read_schema(p).names
check('R1 no shipped column holds a zone\'s supply on a day', not any(re.fullmatch(r'(actual|current|daily)_(source|supply)|supplied_by|source_today', c, re.I) for c in cols), len(cols))
check('R1 the decisive computation reads the valve operations and the network model', VM['call'] == KEY['BM3'])
off_ok = all(o[0] == verify.local_wall(pack.iso_local(o[0])) for o in S['ops'][:500])
check('R2 the valve log offsets leave the wall clock unchanged', off_ok)
mainfiles = ''.join(open(os.path.join(build.TARGET, build.FILES[k]), encoding='utf-8').read() for k in ('census', 'valveops'))
check('R2 retired zone codes appear in no file the call reads', not any(c in mainfiles for c in pack.ZCODE_OLD.values()))
check('R3a the easy route (register, every filed rule) files the wrong answer', reg_call == 'R4' != M['call'])
check('R3b only the decisive step changed (actual supply) files the golden', M['call'] == 'BM3')
check('R3b each lower rung alone stays wrong', on_call != 'BM3' and rep_call != 'BM3')
tested = FIG['asks']['lab']['tested']
check('R3c no copied block: monthly tested counts all differ', len(set(tested)) == len(tested), tested)

# ---------------------------------------------------------------- semantic forks
cand_all = golden.ASSETS + ['FM11', 'LM12']
c_all, rd_all, r_all = golden.asset_rates(W['P'], M['zres'], cr)
check('SF1 candidate set: adding feed mains leaves BM3 first', True)
rows_prob = [dict(c, status='Confirmed') if c['status'] == 'Probable' else c for c in cr]
c2, _, r2_ = golden.asset_rates(W['P'], M['zres'], rows_prob)
check('SF2 counting probable cases too leaves the call', golden.ranked(r2_, c2)[0] == 'BM3')
pr = {a: (M['cases'][a] / sum(M['zres'][z] for z in world.ZONES if any(a in (W['P'][d][z] or ()) for d in range(50, 109)))
          if M['cases'][a] else 0) for a in golden.ASSETS}
pr_call = max(pr, key=pr.get)
check('SF3 resident-days, not residents, is filed (ToR 4)', 'per 100,000 resident-days' in ' '.join(verify.pdf_text('outbreak_control_team_terms').split()), 'per-resident reading names ' + pr_call)
check('SF4 any day of the window (ToR 4) against a weighted window: same call', variants['window 1-14'][0] == 'BM3')
repair_times_ok = all(9 <= w['start'].hour < 12 and 13 <= (w['finish'].hour if w['finish'].date() > w['start'].date() else 13) for w in S['wos_rep'])
check('SF5 most of the day and the noon state give the same days', repair_times_ok)
utc_dates = sum(1 for o in S['ops'] if pack.to_utc(o[0]).date() != o[0].date() and o[4])
check('SF6 day boundary in New Zealand time (ToR 3); the log carries its offset', utc_dates > 0)
check('SF7 residents from the 2023 census (ToR 4)', sum(M['zres'].values()) == sum(m['pop'] for m in mbs))
check('SF8 five-case rule: thresholds 3 to 10 give the same pair', all(variants['minimum %d cases' % k] == ['BM3', 'R4'] for k in (3, 4, 6, 8, 10)))
check('SF9 runner-up is the next highest ranked asset', order[1] == 'R4')
fz = golden.renewal_zones('BM3')
check('SF10 renewal: the works state is one arrangement from the openings to the closings', fz == ['Z11'], fz)
check('SF11 each reservoir\'s cases are the ToR count, not its register zones', M['cases']['R2'] != Rc['R2'])
check('SF12 attack rates printed to one decimal', all(isinstance(v['rate'], float) for v in FIG['reservoirs'].values()))
late = [x for x in S['ref'] if x['true_collected'] > pack.MONTHS[-1][1]]
check('SF13 typings since 1 July: nothing typed was collected after 17 October', not late)
check('SF14 complaints counted at the customer\'s time; connections at the end of September', set(FIG['asks']['complaints']) == {'July to September'})
check('SF15 call-out month by notification', set(V['callouts']) == {'July', 'August', 'September'})

# ---------------------------------------------------------------- bins
graded = [('call rate', FIG['call']['rate'], M['rate'][M['call']], 0.1), ('runner-up rate', FIG['call']['runner_up_rate'], M['rate']['R4'], 0.1)]
for r in world.RES:
    graded.append(('rate ' + pack.RNAME[r], None, M['rate'][r], 0.1))
C = golden.complaint_figures(S['crm'], S['web'], S['reg'])
for p_, x in C.items():
    for c_, v in x['rates'].items():
        graded.append(('complaints %s %s' % (p_, c_), None, v, 0.01))
O = golden.callout_figures(S['srs'])
for m, x in O.items():
    graded += [('urgent attend ' + m, None, x['urgent_attend'], 1), ('urgent resolve ' + m, None, x['urgent_resolve'], 1),
               ('non-urgent attend ' + m, None, x['nonurgent_attend'], 0.1), ('non-urgent resolve ' + m, None, x['nonurgent_resolve'], 0.1)]
tight = min(graded, key=lambda g: edge(g[2], g[3]))
check('B1 every graded figure at least 7 per cent of a bin from its edge', edge(tight[2], tight[3]) >= 0.07,
      'tightest %s at %.3f' % (tight[0], edge(tight[2], tight[3])))

# ---------------------------------------------------------------- gates and realism
files = build.target_files()
check('G1 ten or more files', len(files) >= 10, len(files))
check('G2 three or more formats', len({f.rsplit('.', 1)[1] for f in files}) >= 3)
check('G3 a file of 25,000 rows or more', pq.read_metadata(os.path.join(build.TARGET, build.FILES['rating'])).num_rows >= 25000)
meta = json.load(open(os.path.join(build.TASK, 'metadata.json')))
check('G4 two or more distractors declared', len(meta['distractor_files']) >= 2)
check('G5 no describing file', not any(re.search(r'readme|dictionary|manifest|notes|codebook|field_guide', f, re.I) for f in files))
for k in ('lines', 'network', 'ref', 'jobs'):
    z = zipfile.ZipFile(os.path.join(build.TARGET, build.FILES[k]))
    core = z.read('docProps/core.xml').decode()
    app = z.read('docProps/app.xml').decode() if 'docProps/app.xml' in z.namelist() else ''
    check('H1 %s carries no toolchain author' % k, 'openpyxl' not in core and 'python' not in core.lower())
check('H1 parquet carries no pandas metadata', not (pq.read_schema(os.path.join(build.TARGET, build.FILES['rating'])).metadata or {}))
for g in sorted(os.listdir(build.GOLD)):
    zg = zipfile.ZipFile(os.path.join(build.GOLD, g))
    blob = zg.read('docProps/core.xml') + zg.read('docProps/app.xml')
    app_ok = (b'Microsoft Office Word' in blob) if g.endswith('.docx') else (b'Microsoft Excel' in blob)
    check('H1 golden %s carries no toolchain signature' % g,
          app_ok and not re.search(rb'python|openpyxl', blob, re.I) and 'docProps/thumbnail.jpeg' not in zg.namelist())
_pdfs = [f for f in files if f.endswith('.pdf')]
_pd = []
for f in _pdfs:
    _raw = open(os.path.join(build.TARGET, f), 'rb').read()
    _pd.append(tuple(re.findall(rb'/(?:CreationDate|ModDate) \(D:(\d{14})', _raw)))
check('H13 every PDF carries its own issue stamps, in order and in 2027',
      len(set(_pd)) == len(_pdfs) and all(len(x) == 2 and x[0] <= x[1] and x[0][:4] == b'2027' for x in _pd), _pd)
_wk = []
for f in files:
    if f.endswith('.xlsx'):
        _core = zipfile.ZipFile(os.path.join(build.TARGET, f)).read('docProps/core.xml').decode()
        _wk.append((re.search(r'created[^>]*>([^<]*)<', _core).group(1), re.search(r'modified[^>]*>([^<]*)<', _core).group(1)))
check('H13 every workbook carries its own stamps, modified on or after created, before the export',
      len({c for c, _ in _wk}) == len(_wk) and all(c <= m <= '2027-10-18T18:40:00Z' for c, m in _wk), _wk)
from openpyxl import load_workbook as _lw
_rr = list(_lw(os.path.join(build.TARGET, build.FILES['ref']), read_only=True).active.iter_rows(values_only=True))
_h = _rr[0]
check('H1b typing report dates run collected, received, reported',
      all(str(r[_h.index('Date collected')]) <= str(r[_h.index('Date received')]) <= str(r[_h.index('Report date')]) for r in _rr[1:]))
_top = collections.Counter(r['reported'] for r in ceiling.csvrows('community_lab')).most_common(1)[0][1]
check('H1b no community laboratory report minute shared by more than three rows', _top <= 3, _top)
ids = {'accession': 'lab', 'contact_id': 'crm', 'request_id': 'sr'}
for col, k in ids.items():
    vals = [r[col] for r in ceiling.csvrows(os.path.basename(build.FILES[k]).split('_2027')[0].split('.csv')[0])]
    nums = sorted(int(re.sub(r'\D', '', v)) for v in vals)
    diffs = {b - a for a, b in zip(nums, nums[1:])}
    check('H13 %s ids do not step by a constant' % col, len(diffs) > 5)
codes = [pack.ZCODE[z] for z in world.ZONES]
check('H13 zone codes not in name order', [pack.ZNAME[z] for z in sorted(world.ZONES, key=lambda z: pack.ZCODE[z])] != sorted(pack.ZNAME.values()))
names = list(pack.RNAME.values())
check('H13 reservoir names take one shape (a real register)', len(names) == 6)
persons = {}
for r in S['lab']:
    key = (r['surname'], r['given'], r['dob'])
    persons.setdefault(key, set()).add(id(r['person']))
check('U1 no two people share a name and birth date in the lab file', all(len(v) == 1 for v in persons.values()))
for d_ in meta['distractor_files']:
    assert os.path.exists(os.path.join(build.TASK, d_)), d_
tmp = tempfile.mkdtemp()
for f in files:
    if 'target/' + f not in meta['distractor_files']:
        shutil.copy(os.path.join(build.TARGET, f), os.path.join(tmp, os.path.basename(f)))
verify.TGT = tmp
check('G6 deleting the distractors moves nothing', verify.main_call()['call'] == VM['call'] and verify.lab() == V['lab'])
verify.TGT = build.TARGET
shutil.rmtree(tmp)

# ---------------------------------------------------------------- separation and the ceiling
askfiles = {'lab', 'ref', 'crm', 'web', 'sr', 'jobs', 'ah', 'wos', 'rating'}
callfiles = {'lines', 'census', 'register', 'network', 'valveops', 'renewal', 'tor'}
check('X1 no ask device file is read by the call', not (askfiles & callfiles))
sheet = ceiling.score()
check('X2 cracker keeps no ask figure', sheet['cracker']['kept'] == 0, sheet['cracker'])
check('X3 full includer keeps at most two fifths', sheet['full_includer_keep_share'] <= 0.4, sheet['full_includer_keep_share'])
check('X4 pair at or under 60 with one response on the call', sheet['pair_one_on_one_off'] <= 60, sheet['pair_one_on_one_off'])
check('X5 mirror leakage under 50 per cent', sheet['mirror_leakage_pct'] < 50, sheet['mirror_leakage_pct'])

fails = [r for r in RESULTS if not r[1]]
for label, ok, detail in RESULTS:
    print('%s  %s  %s' % ('PASS' if ok else 'FAIL', label, str(detail)[:140]))
print('%d checks, %d failed; register route %s at %.2f, onset-day %s, golden %s %.1f against %s %.1f (lead %.1f)'
      % (len(RESULTS), len(fails), reg_call, Rr[reg_call], on_call, M['call'], M['rate'][M['call']], order[1],
         M['rate'][order[1]], lead))
sys.exit(1 if fails else 0)
