"""Recompute every graded figure from target/ alone (no generator state) and compare with figures.json.

    python3 task313/generator/verify.py [target_dir]

The functions take options so checks.py and ceiling.py can run the same path with one handling changed; the
defaults are the golden's handling.
"""
import csv
import datetime as dt
import json
import math
import os
import sys
from zoneinfo import ZoneInfo
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), 'target')
LONDON = ZoneInfo('Europe/London')
UTC = dt.timezone.utc
PLAN_A, PLAN_Z = dt.datetime(2025, 10, 1), dt.datetime(2026, 10, 1)
HV_MIN, TEL_MIN = 20, 3       # any cut inside the gap between failed and completed contacts gives the same counts
UNPLANNED = ('21', '22', '28', '81')
FIVE = ['Ravensby Royal Infirmary', 'Kellingworth University Hospital', 'Sedgefold Hospital', "St Aldric's Hospital",
        'Wennby Community Hospital']
CODE = dict(zip(FIVE, ['RRI', 'KUH', 'SDH', 'SAH', 'WCH']))
REASONS = ['LPT', 'BFP', 'EDC', 'WTL', 'VJD', 'SPH']
DAY28 = dt.timedelta(days=28)
_CACHE = {}


def rd(name, tgt):
    with open(os.path.join(tgt, name), encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def nhs_ok(n):
    if len(n) != 10 or not n.isdigit():
        return False
    s = sum(int(n[i]) * (10 - i) for i in range(9))
    c = 11 - s % 11
    c = 0 if c == 11 else c
    return c != 10 and c == int(n[9])


def raw(tgt):
    """Every shipped file parsed once, in its own form."""
    if tgt in _CACHE:
        return _CACHE[tgt]
    sites = rd('site_codes.csv', tgt)
    a_code = {r['maternity_system_code']: r['site'] for r in sites if r['maternity_system_code']}
    b_name = {r['maternity_system_name']: r['site'] for r in sites if r['maternity_system_name']}
    label_code = {r['label']: r['code'] for r in rd('newborn_risk_reasons.csv', tgt)}
    babies = []
    for r in rd('rk_maternity_postnatal_discharges_2024-04_2026-10.csv', tgt):
        babies.append(dict(site=a_code[r['SITE']], hosp=r['MRN'], nhs=r['NHS_NUMBER'], mother=r['MOTHER_NHS_NUMBER'],
                           disch=dt.datetime.strptime(r['DISCHARGE_DTTM'], '%d/%m/%Y %H:%M'),
                           birth=dt.datetime.strptime(r['BABY_DOB_DTTM'], '%d/%m/%Y %H:%M'),
                           flag=r['NB_RISK_FLAG'] == 'Y', multiple=r['MULTIPLE_BIRTH'] == 'Y',
                           reasons=[x for x in r['NB_RISK_CODES'].split(';') if x]))
    wb = openpyxl.load_workbook(os.path.join(tgt, 'sw_maternity_postnatal_discharges.xlsx'), read_only=True)
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        hdr = list(next(it))
        ix = {h: i for i, h in enumerate(hdr)}
        for row in it:
            if row[0] is None:
                continue
            if 'Discharged' in ix:
                d = row[ix['Discharged']]
                flag = row[ix['Newborn risk flag']] == 'Y'
                rs = row[ix['Newborn risk reasons']] or ''
            else:
                dd, tt = row[ix['Discharge date']], row[ix['Discharge time']]
                h, m = map(int, tt.split(':'))
                d = dt.datetime(dd.year, dd.month, dd.day, h, m)
                flag = row[ix['Feeding/jaundice risk']] == 'Yes'
                rs = row[ix['Risk reasons']] or ''
            bd, bt = row[ix['Date of birth']], row[ix['Time of birth']]
            h, m = map(int, bt.split(':'))
            babies.append(dict(site=b_name[row[ix['Hospital']]], hosp=row[ix['Hospital No']],
                               nhs=(row[ix['NHS No']] or '').replace(' ', ''), mother=(row[ix['Mother NHS No']] or '').replace(' ', ''),
                               disch=d, birth=dt.datetime(bd.year, bd.month, bd.day, h, m), flag=flag,
                               multiple=bool(row[ix['Multiple birth']]),
                               reasons=[label_code[x.strip()] for x in rs.split(';') if x.strip()]))
    mpi = {(r['trust'], r['hospital_number']): r['nhs_number'] for r in rd('mpi_baby_hospital_numbers.csv', tgt)}
    notes = rd('community_midwifery_notifications_2024-04_2026-10.csv', tgt)
    adm = rd('neonatal_paediatric_admissions_2024-04_2026-10.csv', tgt)
    contacts = rd('copperfield_outreach_contacts.csv', tgt)
    wb = openpyxl.load_workbook(os.path.join(tgt, 'copperfield_trial_randomisation_final.xlsx'), read_only=True)
    it = wb.active.iter_rows(values_only=True)
    hdr = list(next(it))
    ix = {h: i for i, h in enumerate(hdr)}
    final = [dict(nhs=str(r[ix['NHS No']]), hosp=r[ix['Hospital No']], arm=r[ix['Arm']], primary=r[ix['Primary risk reason']])
             for r in it if r[0] is not None]
    _CACHE[tgt] = dict(babies=babies, mpi=mpi, notes=notes, adm=adm, contacts=contacts, final=final,
                       label_code=label_code)
    return _CACHE[tgt]


def landmark(t, rule='rule'):
    """The earliest the outreach line could reach the family once the office holds the notification."""
    if t is None:
        return None
    if rule == 'recv':
        return t
    if rule == 'recv1h':
        return t + dt.timedelta(hours=1)
    lo, hi, lag = 8, 19, dt.timedelta(0)
    if rule == 'open0900':
        lo = 9
    elif rule == 'last2000':
        hi = 20
    elif rule == 'rule2h':
        lag = dt.timedelta(hours=2)
    if lo <= t.hour < hi:
        return t + lag
    d = t.date() if t.hour < lo else t.date() + dt.timedelta(days=1)
    return dt.datetime(d.year, d.month, d.day, lo, 0) + lag


def link(tgt, utc_local=False, hosp_fallback=True, amended=False, use_mpi=True, mother_map=True,
         methods=UNPLANNED, window=DAY28, per_admission=False):
    """Each baby with its first notification receipt and its unplanned admissions in the window."""
    R = raw(tgt)
    babies = [dict(b) for b in R['babies']]
    mpi = R['mpi']
    for b in babies:
        if not b['nhs']:
            b['nhs'] = mpi.get(('RK' if b['hosp'].startswith('RK') else 'SW', b['hosp']), '')
    by_nhs = {b['nhs']: b for b in babies if b['nhs']}
    by_hosp = {b['hosp']: b for b in babies}
    first, seen = {}, set()
    kinds = ('Discharge home', 'Amended') if amended else ('Discharge home',)
    for r in R['notes']:
        if r['office_ref'] in seen or r['notification'] not in kinds:
            continue
        seen.add(r['office_ref'])
        b = by_nhs.get(r['nhs_number']) if nhs_ok(r['nhs_number']) else None
        if b is None and hosp_fallback:
            b = by_hosp.get(r['hospital_number'])
        if b is None:
            continue
        t = dt.datetime.strptime(r['received_utc'], '%Y-%m-%dT%H:%M:%SZ')
        if not utc_local:
            t = t.replace(tzinfo=UTC).astimezone(LONDON).replace(tzinfo=None)
        if amended:
            if b['hosp'] not in first or t > first[b['hosp']]:
                first[b['hosp']] = t
        elif b['hosp'] not in first or t < first[b['hosp']]:
            first[b['hosp']] = t
    for b in babies:
        b['recv'] = first.get(b['hosp'])
    mothers = {}
    for b in babies:
        if b['mother']:
            mothers.setdefault(b['mother'], []).append(b)
    adm = {}
    for r in R['adm']:
        if r['admission_method'] not in methods:
            continue
        n = r['nhs_number'] or (mpi.get((r['pas_trust'], r['hospital_number']), '') if use_mpi else '')
        if not n:
            continue
        t = dt.datetime.strptime(r['admitted'], '%Y-%m-%d %H:%M')
        if n not in by_nhs:
            # a row under a mother's NHS number (a baby back on a postnatal ward with its mother) belongs to her
            # baby discharged home in the 28 days before
            if mother_map and n in mothers:
                for k in mothers[n]:
                    if k['nhs'] and k['disch'] < t <= k['disch'] + DAY28:
                        adm.setdefault(k['nhs'], []).append(t)
            continue
        adm.setdefault(n, []).append(t)
    for b in babies:
        ts = sorted(t for t in adm.get(b['nhs'], []) if b['disch'] < t and (window is None or t <= b['disch'] + window))
        b['readm'] = ts[0] if ts else None
        b['n_adm'] = len(ts) if per_admission else (1 if ts else 0)
    return babies, by_nhs


def largest_remainder(v, total=30):
    q = [total * x / sum(v) for x in v]
    fl = [int(math.floor(x)) for x in q]
    order = sorted(range(len(v)), key=lambda i: (-(q[i] - fl[i]), i))
    for i in order[:total - sum(fl)]:
        fl[i] += 1
    return fl


def theta(tgt, babies, by_nhs, rule='rule', source='final', estimator='rr', window_days=28):
    """The trial's cut in readmission after the earliest contact (risk ratio, or incidence rate ratio on the
    days at risk), arms as randomised, from the final list."""
    R = raw(tgt)
    lst = R['final']
    rate = {}
    for arm in ('Outreach', 'Usual care'):
        A = [by_nhs[x['nhs']] for x in lst if x['arm'] == arm and x['nhs'] in by_nhs]
        if rule is not None:
            A = [b for b in A if not (b['readm'] is not None and b['recv'] is not None and b['readm'] <= landmark(b['recv'], rule))]
        r = sum(1 for b in A if b['readm'] is not None)
        if estimator == 'rr':
            rate[arm] = r / len(A)
        else:
            days = 0.0
            for b in A:
                start = landmark(b['recv'], rule) if rule is not None and b['recv'] is not None else b['disch']
                start = max(start, b['disch'])
                end = b['readm'] if b['readm'] is not None else b['disch'] + dt.timedelta(days=window_days)
                days += max((end - start).total_seconds() / 86400.0, 0.0)
            rate[arm] = r / days
    return 1 - rate['Outreach'] / rate['Usual care']


def call(tgt=None, rule='rule', theta_rule='rule', theta_source='final', estimator='rr', twins=True,
         window_on='disch', reached_only=True, **link_opts):
    tgt = tgt or TGT
    babies, by_nhs = link(tgt, **link_opts)
    plan = {}
    for s in FIVE:
        P = [b for b in babies if b['site'] == s and b['flag'] and (twins or not b['multiple'])]
        key = 'disch' if window_on == 'disch' else 'birth'
        plan[s] = [b for b in P if PLAN_A <= b[key] < PLAN_Z]
    if reached_only:
        counted = [sum(b['n_adm'] for b in plan[s] if b['readm'] is not None and b['recv'] is not None
                       and b['readm'] > landmark(b['recv'], rule)) for s in FIVE]
    else:
        counted = [sum(b['n_adm'] for b in plan[s] if b['readm'] is not None) for s in FIVE]
    th = theta(tgt, babies, by_nhs, rule=theta_rule, source=theta_source, estimator=estimator)
    total = th * sum(counted)
    return dict(posts=dict(zip([CODE[s] for s in FIVE], largest_remainder(counted))), counted=counted, theta=th,
                total=total, total_rounded=int(math.floor(total / 25 + 0.5) * 25),
                eligible=[len(plan[s]) for s in FIVE])


def ask_a(tgt=None, reasons_from='discharge', **link_opts):
    """By risk reason: the usual-care readmission rate (per cent, one decimal) and the risk ratio (two decimals)."""
    tgt = tgt or TGT
    babies, by_nhs = link(tgt, **link_opts)
    R = raw(tgt)
    lc = R['label_code']
    out = {}
    for r in REASONS:
        grp = {}
        for arm in ('Outreach', 'Usual care'):
            if reasons_from == 'discharge':
                A = [by_nhs[x['nhs']] for x in R['final'] if x['arm'] == arm and r in by_nhs[x['nhs']]['reasons']]
            else:
                A = [by_nhs[x['nhs']] for x in R['final'] if x['arm'] == arm and lc[x['primary']] == r]
            grp[arm] = (sum(1 for b in A if b['readm'] is not None), len(A))
        (ro, no), (rc, nc) = grp['Outreach'], grp['Usual care']
        out[r] = {'usual_care_rate_pct': round(100.0 * rc / nc, 1) if nc else float('nan'),
                  'risk_ratio': round((ro / no) / (rc / nc), 2) if (no and rc) else float('nan'),
                  'counts': (no, ro, nc, rc)}
    return out


def ask_b(tgt=None, call_mother_map=True, split_pre_update=True, dedupe=True, window=True, reasons_from='discharge'):
    tgt = tgt or TGT
    babies, by_nhs = link(tgt)
    R = raw(tgt)
    lc = R['label_code']
    out_b = {x['nhs']: by_nhs[x['nhs']] for x in R['final'] if x['arm'] == 'Outreach'}
    prim = {x['nhs']: lc[x['primary']] for x in R['final'] if x['arm'] == 'Outreach'}
    mother = {b['mother']: n for n, b in out_b.items()}
    hv, tel, seen = {}, {}, set()
    for c in R['contacts']:
        if dedupe and c['contact_id'] in seen:
            continue
        seen.add(c['contact_id'])
        n = c['nhs_number'] if c['nhs_number'] in out_b else (mother.get(c['nhs_number']) if call_mother_map else None)
        if n is None:
            continue
        t = dt.datetime.strptime(c['contact_datetime'], '%Y-%m-%d %H:%M')
        b = out_b[n]
        if window and not (b['disch'] < t <= b['disch'] + DAY28):
            continue
        # NA and TNA are failed attempts; before those codes came into use (6 January 2025) a failed attempt was
        # filed as HV or TEL with the few minutes it took, a cluster far below any completed visit or call
        m = int(c['minutes'])
        if c['contact_type'] == 'HV' and (m >= HV_MIN or not split_pre_update):
            hv[n] = hv.get(n, 0) + 1
        elif c['contact_type'] == 'TEL' and (m >= TEL_MIN or not split_pre_update):
            tel[n] = tel.get(n, 0) + 1
    out = {}
    for r in REASONS:
        if reasons_from == 'discharge':
            ns = [n for n, b in out_b.items() if r in b['reasons']]
        else:
            ns = [n for n in out_b if prim[n] == r]
        out[r] = {'home_visits': round(sum(hv.get(n, 0) for n in ns) / len(ns), 2),
                  'calls': round(sum(tel.get(n, 0) for n in ns) / len(ns), 2)}
    return out


def main():
    tgt = sys.argv[1] if len(sys.argv) > 1 else TGT
    V = call(tgt)
    A = ask_a(tgt)
    Bk = ask_b(tgt)
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    bad = []
    if V['posts'] != F['call']['posts']:
        bad.append('posts %s vs %s' % (V['posts'], F['call']['posts']))
    if V['total_rounded'] != F['call']['readmissions_avoided_2027_28']:
        bad.append('total %s vs %s' % (V['total_rounded'], F['call']['readmissions_avoided_2027_28']))
    if V['eligible'] != [F['eligible'][u] for u in ['RRI', 'KUH', 'SDH', 'SAH', 'WCH']]:
        bad.append('eligible %s vs %s' % (V['eligible'], F['eligible']))
    for k, v in A.items():
        for kk in ('usual_care_rate_pct', 'risk_ratio'):
            if abs(v[kk] - F['ask_a'][k][kk]) > 1e-9:
                bad.append('ask_a %s %s %s vs %s' % (k, kk, v[kk], F['ask_a'][k][kk]))
        f = F['ask_a'][k]
        if v['counts'] != (f['outreach_babies'], f['outreach_readmitted'], f['usual_care_babies'], f['usual_care_readmitted']):
            bad.append('ask_a %s counts %s' % (k, v['counts']))
    for k, v in Bk.items():
        for kk in ('home_visits', 'calls'):
            if abs(v[kk] - F['ask_b'][k][kk]) > 1e-9:
                bad.append('ask_b %s %s %s vs %s' % (k, kk, v[kk], F['ask_b'][k][kk]))
    print('verify: posts %s total %.1f -> %d theta %.4f reached %s' % (V['posts'], V['total'], V['total_rounded'], V['theta'], V['counted']))
    if bad:
        print('VERIFY FAIL')
        for b in bad:
            print('  ' + b)
        sys.exit(1)
    print('VERIFY PASS: every graded figure recomputed from target/ alone')


if __name__ == '__main__':
    main()
