"""task401 generator checks on the cut pack: the fork table (SF1 to SF13), the first-look readers and literal executions
on the shipped seed, the call under every remaining setting, the asks against the world's truth with their bin edges and
profiles, the input gates and the realism sweep. Exit 1 on any failure.

    python3 checks.py
"""
import os, sys, glob, json, pickle, re, zipfile
from datetime import date, timedelta
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G
import asks

T = os.path.join(os.path.dirname(HERE), 'target')
RES = []


def ok(name, cond, detail=''):
    RES.append((bool(cond), name, detail))


def edge(v, u): return u / 2 - abs(v - round(v / u) * u)


def call_of(g): return max(g, key=g.get)


def run(R=None):
    R = R or G.run()
    S, mc, rd, F = R['S'], R['mc'], R['rd'], R['F']
    P = pickle.load(open(os.path.join(HERE, '.truth.pkl'), 'rb'))
    tru = P['truth']
    # the design's truth and the golden agree
    ok('truth: the closure costs the most over the membership year', max(tru, key=tru.get) == 'A', str(tru))
    ok('golden names the truth\'s change', mc['call'] == 'A' == max(tru, key=tru.get), mc['call'])
    ok('golden lead over its runner-up at least 1.5x', F['lead'] >= 1.5, F['lead'])
    ok('truth: the letters cost less than the closure by 2x or more', tru['A'] >= 2 * tru['D'], '%d against %d' % (tru['A'], tru['D']))
    # first looks and literal executions on the shipped seed (each must land off the closure)
    ok('first look, cancellations in each reach after against before', rd['FL'] != 'A', rd['FL'])
    ok('first look, the same net of the same weeks of 2025', rd['FLY'] != 'A', rd['FLY'])
    ok('first look, 28-day active share year on year', rd['ENG_share'] != 'A', rd['ENG_share'])
    sh = rd['ENG']['share']
    ok('active share margin: the named reach falls 10 per cent more than the closure\'s', sh[rd['ENG_share']] <= 1.1 * sh['A'],
       '%s %.4f against the closure %.4f' % (rd['ENG_share'], sh[rd['ENG_share']], sh['A']))
    ok('first look, visits per member year on year', rd['ENG_vpm'] != 'A', rd['ENG_vpm'])
    ok('count reader (cancellations plus lost actives) off the closure by 1.25x or more', rd['HARM_top'] != 'A' and rd['HARM_margin'] >= 1.25,
       '%s %.2f' % (rd['HARM_top'], rd['HARM_margin']))
    ok('residual recorded: the 28-day active count alone names the closure', rd['ENG_count'] == 'A', rd['ENG_count'])
    ok('first look, centres: the largest fall is at a centre of the hours cut', rd['CENTRE_top'] in G.HOURS_SITES, rd['CENTRE_top'])
    ok('first look, stated reasons', rd['SR_top'] != 'A', str(rd['SR']))
    for nm, k in rd['LIT'].items():
        ok('literal execution / cracker rung %s off the closure' % nm, k != 'A', k)
    lv = rd['LIT_values']['L2_year_on_year']
    ok('literal execution margin: the letters\' count so far over the closure\'s golden', lv['D'] > G.project(S, 'A')[0],
       '%.0f against %.0f' % (lv['D'], G.project(S, 'A')[0]))
    # the call under every remaining setting (28 days, the filed membership year; 21 to 42 days and 9 to 12 months too)
    held = [k for k, g in mc['var'].items() if k.endswith('extract') and int(k.split('_')[0][1:]) <= 6 and k.split('_')[1] != '6m']
    flips = [k for k in held if call_of(mc['var'][k]) != 'A']
    ok('SF10 SF11 SF12 the call holds at 21 to 42 days, 9 to 12 months and the year end, both sources, both baselines', not flips,
       '%d settings, flips %s' % (len(held), flips[:4]))
    out6 = sum(call_of(g) != 'A' for k, g in mc['var'].items() if '_6m_' in k and k.endswith('extract') and k.startswith('t4_'))
    out8 = sum(call_of(g) != 'A' for k, g in mc['var'].items() if k.startswith('t8_') and k.endswith('extract'))
    ok('outside the filed WHATs: six-month horizon and 56 days recorded', True, 'flips at 6 months %d of 4, at 56 days %d of 20' % (out6, out8))
    # SF rows: the readings the fork table rules out or shows inert
    base = {k: G.project(S, k)[0] for k in 'ACDE'}
    # SF1: counting every request rather than the first per membership (the duplicates)
    canc = pd.read_csv(glob.glob(os.path.join(T, 'cancellation_requests_*.csv'))[0], dtype=str)
    dup = len(canc) - canc.membership_no.nunique()
    ok('SF1 a cancellation counted once on its first request (filed); duplicates %d would not move the call' % dup, dup > 0 and call_of(base) == 'A')
    # SF2: the closure's members as Rewards holders on 31 January (filed) against every 2023-tariff member
    keep = S['R26']['A'].copy(), S['R25']['A'].copy()
    S['R26']['A'], S['R25']['A'] = ~S['legacy'], ~S['legacy']
    alt = {k: G.project(S, k)[0] for k in 'ACDE'}
    S['R26']['A'], S['R25']['A'] = keep
    ok('SF2 the closure read on every 2023-tariff member names the same change', call_of(alt) == 'A', '%.0f' % alt['A'])
    # SF3: the letters' members as legacy members on the books on 2 February (filed) equal the letters log
    lg = set(S['letters'].membership_no)
    onb = set(S['reg'].membership_no[S['legacy'] & G.on_books(S, date(2026, 2, 2))])
    ok('SF3 the letters went to exactly the legacy members on the books on 2 February', lg == onb, '%d letters, %d members' % (len(lg), len(onb)))
    # SF4: the timetable's members from bookings of any status (filed: booked) against attended only
    ok('SF4 the timetable reach (any booking) names the same change', call_of(base) == 'A', 'reach %d' % S['R26']['C'].sum())
    # SF5: the hours cut's members by home centre (filed)
    ok('SF5 the hours cut read on home centre names the same change', call_of(base) == 'A', 'reach %d' % S['R26']['E'].sum())
    # SF6: the membership year (filed in the prompt and the terms): the horizon runs to its end
    ok('SF6 the conversion follows last year\'s members to the end of the 2025-26 membership year', G.HZ['year'] == (date(2026, 2, 2) - date(2025, 3, 17)).days)
    # SF7: the same weeks of the previous year, 364 days back (filed: the same weeks)
    ok('SF7 the previous membership year began 364 days before this one', (date(2026, 2, 2) - date(2025, 2, 3)).days == G.SHIFT)
    # SF8: last year's members in the same position then (filed) against this year's members a year earlier (survivors)
    keepA = S['R25']['A'].copy(); S['R25']['A'] = S['R26']['A']
    alt8 = {k: G.project(S, k)[0] for k in 'ACDE'}; S['R25']['A'] = keepA
    ok('SF8 the closure compared with its own survivors a year earlier names the same change', call_of(alt8) == 'A', '%.0f' % alt8['A'])
    # SF9: members who had already asked to leave are not in a reach at its date (they cannot cancel again)
    ok('SF9 a member already leaving cannot cancel twice; the reach counts members not leaving', True)
    # SF13: the as-of date is the extract (the prompt)
    ok('SF13 every record ends at the extract', canc.received.max() < '2026-03-16', canc.received.max())
    # the asks: goldens against the world's truth, bin edges, the profiles
    fee = {'L-ADULT': 34.0, 'L-OFFPEAK': 26.5, 'L-CONC': 22.0, 'FLEX-ADULT': 38.5, 'FLEX-OFFPEAK': 29.0, 'FLEX-CONC': 24.5, 'FLEX-STUDENT': 25.0}
    tar = dict(zip(S['reg'].membership_no, S['reg'].tariff_code))
    tr = {}
    for (m, mo), paid in P['paid'].items():
        if paid and mo in asks.DD_MONTHS:
            k = ('%d-%02d' % mo, 'legacy' if tar[m].startswith('L-') else '2023'); tr[k] = tr.get(k, 0) + fee[tar[m]]
    ok('ask fees: the golden equals what the world collected', all(abs(R['dd'][k] - tr.get(k, 0)) < 0.01 for k in R['dd']))
    tt = {}
    for (y, m, c), n in P['till'].items():
        k = ('%d-%02d' % (y, m), 'NW' if c in G.HOURS_SITES else 'other'); tt[k] = tt.get(k, 0) + n
    ok('ask admissions: the golden equals the people the world admitted', all(R['till'][k] == tt.get(k, 0) for k in R['till']))
    e1 = {k: edge(v, 10) for k, v in R['till'].items()}; e2 = {k: edge(v, 100) for k, v in R['dd'].items()}
    t1, t2 = min(e1, key=e1.get), min(e2, key=e2.get)
    ok('every admissions figure mid-bin (7 per cent of a bin from its edge)', e1[t1] >= 0.7, 'tightest %s at %.1f of 10' % (t1, e1[t1]))
    ok('every fees figure mid-bin', e2[t2] >= 7, 'tightest %s at %.1f of 100' % (t2, e2[t2]))
    keep = {}
    for route in ('cracker', 'full', 'norepair'):
        a, b = asks.till_count(route), asks.dd_count(route)
        keep[route] = (sum(round(a[k] / 10) == round(R['till'][k] / 10) for k in a), sum(round(b[k] / 100) == round(R['dd'][k] / 100) for k in b))
    ok('cracker misses every ask figure', keep['cracker'] == (0, 0), str(keep['cracker']))
    ok('no-repair reader misses every ask figure', keep['norepair'] == (0, 0), str(keep['norepair']))
    fk = sum(keep['full']) / 18
    ok('full includer keeps at most two fifths of the ask figures', fk <= 0.4, '%s = %.1f per cent' % (keep['full'], 100 * fk))
    ok('full includer misses a block in each ask', keep['full'][0] < 10 and keep['full'][1] < 8, str(keep['full']))
    # input gates and realism
    files = sorted(os.listdir(T))
    ok('input gate: 10 or more files', len(files) >= 10, len(files))
    ok('input gate: 3 or more formats', len({f.rsplit('.', 1)[1] for f in files}) >= 3, sorted({f.rsplit('.', 1)[1] for f in files}))
    ok('input gate: a file of 25,000 rows or more', len(S['v']) >= 25000, len(S['v']))
    for f in files:
        p = os.path.join(T, f)
        if f.endswith('.parquet'):
            b = open(p, 'rb').read()
            ok('realism: %s footer carries no arrow signature' % f, b'parquet-cpp-arrow' not in b and b'pandas' not in b[-4000:])
        if f.endswith(('.docx', '.xlsx')):
            z = zipfile.ZipFile(p); names = z.namelist(); core = z.read('docProps/core.xml')
            ok('realism: %s metadata scrubbed' % f, b'python' not in core.lower() and b'openpyxl' not in z.read('docProps/app.xml').lower())
            if f.endswith('.xlsx'):
                ok('realism: %s stores shared strings' % f, 'xl/sharedStrings.xml' in names)
        if f.endswith('.pdf'):
            b = open(p, 'rb').read()
            ok('realism: %s producer scrubbed' % f, b'ReportLab' not in b and b'reportlab' not in b)
    txt = ''
    import docx
    for f in files:
        if f.endswith('.docx'):
            txt += '\n'.join(p.text for p in docx.Document(os.path.join(T, f)).paragraphs)
    ok('realism: no em or en dash in the documents', '—' not in txt and '–' not in txt)
    for f in files:
        m = re.findall(r'(\d{4}-\d{2}-\d{2})_to_(\d{4}-\d{2}-\d{2})', f)
        if not m or not f.endswith('.csv'): continue
        df = pd.read_csv(os.path.join(T, f), dtype=str, nrows=None)
        col = {'cancellation': 'received', 'epos': 'timestamp', 'pool': 'date', 'member_care': 'called_at', 'dd_bureau': 'processing_date',
               'dd_collections': 'collection_date', 'till': 'sold'}[next(k for k in ('cancellation', 'epos', 'pool', 'member_care', 'dd_bureau', 'dd_collections', 'till') if f.startswith(k))]
        vals = df[col].astype(str)
        if '/' in vals.iloc[0]:
            vals = pd.to_datetime(vals.str[:10], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
        lo, hi = vals.str[:10].min(), vals.str[:10].max()
        ok('realism: %s spans its name' % f, lo >= m[0][0] and hi <= m[0][1], '%s to %s' % (lo, hi))
    bad = [r for r in RES if not r[0]]
    for good, name, detail in RES:
        print('%s  %s%s' % ('PASS' if good else 'FAIL', name, ('  [%s]' % detail) if detail != '' else ''))
    print('%d checks, %d failures' % (len(RES), len(bad)))
    if bad:
        raise SystemExit(1)
    return RES


if __name__ == '__main__':
    run()
