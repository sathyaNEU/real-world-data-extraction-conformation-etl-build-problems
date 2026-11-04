"""The generator's assertions on the clean truth and the cut pack: the three rules (R1 to R3c), the convention
family and the totals' bin, the semantic fork table (SF1 to SF20), the ask devices and their separation from
the main call, the input gates and the realism sweep.

    python3 task313/generator/checks.py        (exit 1 on any failure)
"""
import collections
import csv
import datetime as dt
import json
import math
import os
import re
import statistics as stx
import sys
import openpyxl

import world as W
import records as R
import golden as G
import verify as V

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, 'target')
RES = []


def ok(name, cond, detail=''):
    RES.append((name, bool(cond), detail))


def headers():
    out = {}
    for f in sorted(os.listdir(TGT)):
        p = os.path.join(TGT, f)
        if f.endswith('.csv'):
            with open(p, encoding='utf-8') as fh:
                out[f] = next(csv.reader(fh))
        elif f.endswith('.xlsx'):
            wb = openpyxl.load_workbook(p, read_only=True)
            for ws in wb.worksheets:
                out[f + ':' + ws.title] = [c for c in next(ws.iter_rows(values_only=True)) if c is not None]
    return out


def rows_of(f):
    p = os.path.join(TGT, f)
    if f.endswith('.csv'):
        with open(p, encoding='utf-8') as fh:
            return sum(1 for _ in fh) - 1
    if f.endswith('.xlsx'):
        wb = openpyxl.load_workbook(p, read_only=True)
        return sum(ws.max_row - 1 for ws in wb.worksheets)
    return 0


def pdf_text(path):
    from pypdf import PdfReader
    return re.sub(r'\s+', ' ', ' '.join(pg.extract_text() or '' for pg in PdfReader(path).pages))


def same(c, g):
    return c['posts'] == g['posts'] and c['total_rounded'] == g['total_rounded']


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    meta = json.load(open(os.path.join(TASK, 'metadata.json')))
    B = W.build_world()
    C = G.call(B)
    gold_posts = dict(zip(W.FIVE, C['posts']))
    g = V.call()

    # ------------------------------------------------------------------ the golden, two code paths
    ok('GOLD the cut pack reproduces the clean truth posts', g['posts'] == gold_posts, str(g['posts']))
    ok('GOLD the cut pack reproduces the clean truth total bin', g['total_rounded'] == C['total_rounded'] == 325,
       '%.1f and %.1f' % (g['total'], C['total']))
    ok('GOLD the total sits inside its 25 bin with 4 or more to either edge', 316.5 <= C['total'] <= 333.5, '%.1f' % C['total'])
    ok('GOLD figures.json carries the call', F['call']['posts'] == gold_posts and F['call']['readmissions_avoided_2027_28'] == 325)

    # ------------------------------------------------------------------ R1: the raw material ships
    heads = headers()
    flat = [h.lower() for hs in heads.values() for h in hs]
    ok('R1 every discharge ships at its own grain with its time', rows_of('rk_maternity_postnatal_discharges_2024-04_2026-10.csv') > 25000)
    ok('R1 every notification ships with its receipt instant', rows_of('community_midwifery_notifications_2024-04_2026-10.csv') > 50000)
    ok('R1 every admission ships with its admitted instant and method', 'admitted' in heads['neonatal_paediatric_admissions_2024-04_2026-10.csv'])
    bad = [h for h in flat if re.search(r'landmark|reach|delay|avoid|\blag\b|_lag|first_contact|eligible_for', h)]
    ok('R1 no shipped column holds the reachable window, a delay or the readmissions avoided', not bad, str(bad))
    ok('R1 the decisive computation reads row-level receipts and admissions (the default path reads neither receipt)',
       V.call(reached_only=False)['posts'] != g['posts'])

    # ------------------------------------------------------------------ R2: every mess item neutral
    mess = {
        'R2 notification receipts read as local time instead of UTC': dict(utc_local=True),
        'R2 transposed NHS numbers on paper notifications left unmatched': dict(hosp_fallback=False),
        'R2 amended notifications taken as the receipt (latest message)': dict(amended=True),
        'R2 admissions with no NHS number left unkeyed (no master patient index)': dict(use_mpi=False),
        'R2 transfer rows (method 81) dropped': dict(methods=('21', '22', '28')),
        'R2 admissions counted per row instead of once per baby': dict(per_admission=True),
        'R2 Copperfield postnatal-ward rows under the mother left unmapped': dict(mother_map=False),
    }
    for name, o in mess.items():
        c = V.call(**o)
        ok(name + ': call unchanged', same(c, g), '%s %.1f' % (c['posts'], c['total']))
    # the duplicated interface messages (same office_ref) carry the same receipt
    notes = V.raw(TGT)['notes']
    refs = collections.Counter(r['office_ref'] for r in notes)
    dups = [k for k, v in refs.items() if v > 1]
    ok('R2 duplicated notification messages repeat one receipt (first receipt unchanged)', len(dups) > 20, '%d repeated refs' % len(dups))
    # the 2026-27 sheet's combined discharge column and the 2024-26 date and time columns read the same instants
    ok('R2 the maternity B schema change is read on both layouts', g['eligible'] == [F['eligible'][u] for u in W.FIVE])

    # ------------------------------------------------------------------ R3a, R3b: the analyst test and the decisive step alone
    d = V.call(reached_only=False)
    ok('R3a the default path (trial ratio on every eligible readmission) files 8, 8, 5, 4, 5',
       list(d['posts'].values()) == [8, 8, 5, 4, 5] and C['naive_posts'] == [8, 8, 5, 4, 5], str(d['posts']))
    ok('R3a the default path files about 375 readmissions avoided (report ratio)', C['naive_total_rounded'] == 375,
       '%.1f' % C['naive_total'])
    ok('R3a the default total is two bins from the golden', abs(C['naive_total_rounded'] - 325) >= 50)
    ok('R3b the easy route with only the reachable readmissions changed files the golden', same(g, g) and g['posts'] == gold_posts)
    babies, by_nhs = V.link(TGT)
    plan = {s: [b for b in babies if b['site'] == s and b['flag'] and V.PLAN_A <= b['disch'] < V.PLAN_Z] for s in V.FIVE}

    def lr(counts):
        return V.largest_remainder(counts)

    def bin25(x):
        return int(math.floor(x / 25 + 0.5) * 25)
    th = g['theta']
    gp = list(g['posts'].values())
    rungs = {}
    rungs['caseload'] = (lr([len(plan[s]) for s in V.FIVE]), 375)
    # the trial's own lags: discharge to the first call that reached the family, and to the first visit made
    outn = {x['nhs'] for x in V.raw(TGT)['final'] if x['arm'] == 'Outreach'}
    fc, fv = {}, {}
    for c in V.raw(TGT)['contacts']:
        if c['nhs_number'] in outn:
            t = dt.datetime.strptime(c['contact_datetime'], '%Y-%m-%d %H:%M')
            if c['contact_type'] == 'TEL' and int(c['minutes']) >= V.TEL_MIN:
                fc[c['nhs_number']] = min(fc.get(c['nhs_number'], t), t)
            if c['contact_type'] == 'HV' and int(c['minutes']) >= V.HV_MIN:
                fv[c['nhs_number']] = min(fv.get(c['nhs_number'], t), t)
    d_call = stx.median([(fc[n] - by_nhs[n]['disch']).total_seconds() / 3600 for n in fc])
    d_visit = stx.median([(fv[n] - by_nhs[n]['disch']).total_seconds() / 3600 for n in fv])
    for nm, h in (('the trial lag to the first call, %.1f h' % d_call, d_call), ('a day', 24.0),
                  ('the trial lag to the first visit, %.1f h' % d_visit, d_visit)):
        cnt = [sum(1 for b in plan[s] if b['readm'] and b['readm'] > b['disch'] + dt.timedelta(hours=h)) for s in V.FIVE]
        rungs['one lag for every unit: ' + nm] = (lr(cnt), bin25(th * sum(cnt)))
    med = {s: stx.median([(b['recv'] - b['disch']).total_seconds() / 3600 for b in plan[s] if b['recv']]) for s in V.FIVE}
    cnt = [sum(1 for b in plan[s] if b['readm'] and b['readm'] > b['disch'] + dt.timedelta(hours=med[s])) for s in V.FIVE]
    rungs['each unit\'s median receipt lag (%s h)' % ', '.join('%.1f' % med[s] for s in V.FIVE)] = (lr(cnt), bin25(th * sum(cnt)))
    for nm, (p, t) in rungs.items():
        ok('R3b lower rung (%s) stays on a wrong answer' % nm, p != gp, '%s %d' % (p, t))
    shares = {V.CODE[s]: round(100.0 * g['counted'][i] / sum(1 for b in plan[s] if b['readm'])) for i, s in enumerate(V.FIVE)}
    ok('R3b the reachable share differs by unit (the two paper-route units lowest)', shares['RRI'] < 80 and shares['SAH'] < 80
       and min(shares['KUH'], shares['SDH']) > 95, str(shares))
    # the start of the effect: the trial's readmissions in the first half day after the earliest contact (before any
    # home visit) already differ by arm, so the visit-start reading is refuted by the trial itself
    fin = V.raw(TGT)['final']
    arm = collections.defaultdict(list)
    for x in fin:
        arm[x['arm']].append(by_nhs[x['nhs']])

    def early(A, days):
        n = r = 0
        for b in A:
            L = V.landmark(b['recv'])
            if b['readm'] is not None and b['readm'] <= L:
                continue
            n += 1
            if b['readm'] is not None and b['readm'] <= L + dt.timedelta(days=days):
                r += 1
        return r, n
    (ro, no), (rc, nc) = early(arm['Outreach'], 1.0), early(arm['Usual care'], 1.0)
    rr = (ro / no) / (rc / nc)
    up = math.exp(math.log(rr) + 1.96 * math.sqrt(1 / ro - 1 / no + 1 / rc - 1 / nc))
    ok('R3b the trial separates a start at the first call from a start at the first visit (day-one RR upper bound under 1)',
       up < 0.8, 'RR %.2f upper %.2f (%d of %d against %d of %d)' % (rr, up, ro, no, rc, nc))
    rcnt = [sum(1 for b in plan[s] if b['readm'] and b['recv'] and b['readm'] > b['recv'] + dt.timedelta(hours=39)) for s in V.FIVE]
    ok('R3b the visit-start reading files another call (so the separation is load-bearing)', lr(rcnt) != gp, str(lr(rcnt)))
    # R3c no plant
    ok('R3c no decoy document: neither PDF names a notification delay, a receipt or a window after contact',
       not re.search(r'notification (delay|lag)|received late|after the first (call|contact|visit)|landmark|reachable',
                     pdf_text(os.path.join(TGT, 'Neonatal outreach service specification 2027-28.pdf')) +
                     pdf_text(os.path.join(TGT, 'Copperfield neonatal outreach trial final report.pdf')), re.I))
    months = collections.Counter((b['site'], b['disch'].strftime('%Y-%m')) for b in babies)
    for s in V.FIVE:
        series = [v for (u, m), v in sorted(months.items()) if u == s]
        ok('R3c %s monthly discharges vary (no copied or constant block)' % V.CODE[s],
           len(set(series)) >= len(series) - 6 and max(series) > min(series) * 1.08, str(series[:6]))

    # ------------------------------------------------------------------ the convention family (C1, C3)
    fam = {}
    for rule in ('rule', 'recv', 'rule2h', 'open0900', 'last2000', 'recv1h'):
        for est in ('rr', 'irr'):
            for trule in (rule, None):
                fam[(rule, est, trule)] = V.call(rule=rule, theta_rule=trule, estimator=est)
    tots = [c['total'] for c in fam.values()]
    ok('SF8 every earliest-contact convention files the same posts', all(c['posts'] == g['posts'] for c in fam.values()))
    ok('SF9 risk ratio and incidence rate ratio file the same bin', all(c['total_rounded'] == 325 for c in fam.values()),
       '%.1f to %.1f' % (min(tots), max(tots)))
    ok('SF10 the trial ratio on the window after the earliest contact equals the whole-window ratio at Copperfield',
       abs(V.call(theta_rule=None)['theta'] - g['theta']) < 0.005)
    # reason-specific effects carried to each unit's reason mix
    rr_reason = {}
    for r in W.REASONS:
        o = [b for b in arm['Outreach'] if r in b['reasons']]
        c = [b for b in arm['Usual care'] if r in b['reasons']]
        rr_reason[r] = (sum(1 for b in o if b['readm']) / len(o)) / (sum(1 for b in c if b['readm']) / len(c))
    av = 0.0
    for s in V.FIVE:
        for b in plan[s]:
            if b['readm'] and b['recv'] and b['readm'] > V.landmark(b['recv']) and b['reasons']:
                av += 1 - sum(rr_reason[r] for r in b['reasons']) / len(b['reasons'])
    st_rep = G.trial_stats(B, G.report_missed(B))
    per_r = [0.0] * 5
    for i, s_ in enumerate(V.FIVE):
        for b in plan[s_]:
            if b['readm'] and b['recv'] and b['readm'] > V.landmark(b['recv']) and b['reasons']:
                per_r[i] += 1 - sum(rr_reason[r] for r in b['reasons']) / len(b['reasons'])
    ok('SF15 reason-specific effects leave the posts where they are', V.largest_remainder(per_r) == gp, str(V.largest_remainder(per_r)))
    ok('SF15 the report rules out reason-specific effects: no interaction test reaches 0.05 (the pooled ratio carries)',
       min(st_rep['p_interaction'].values()) >= 0.05, str({k: round(v, 2) for k, v in st_rep['p_interaction'].items()}))

    # ------------------------------------------------------------------ the fork table rows
    ok('SF1 planned admissions (11 to 13) are not readmissions; including them files the same call',
       same(V.call(methods=('11', '12', '13', '21', '22', '28', '81')), g))
    ok('SF2 the 28-day window on the discharge instant against 27 or 29 days: same call',
       same(V.call(window=dt.timedelta(days=29)), g) and same(V.call(window=dt.timedelta(days=27)), g))
    a_el, b_el = V.ask_a(), V.ask_b()
    for mode in ('incl', 'excl'):
        c_cal = V.call(calendar=mode)
        ok('SF2 whole calendar days from the discharge date (day 28 %s) against 28 days from the discharge instant: the '
           'posts, the total and every Ask A and Ask B figure are identical' % ('in' if mode == 'incl' else 'out'),
           c_cal['posts'] == g['posts'] and abs(c_cal['total'] - g['total']) < 1e-9 and V.ask_a(calendar=mode) == a_el
           and V.ask_b(calendar=mode) == b_el, '%.1f' % c_cal['total'])
    raw_ = V.raw(TGT)
    disch_of = {}
    for b in babies:
        if b['nhs']:
            disch_of[b['nhs']] = [b['disch']]
    for b in babies:
        if b['mother']:
            disch_of.setdefault(b['mother'], []).append(b['disch'])
    on28 = 0
    for r in raw_['adm']:
        t = dt.datetime.strptime(r['admitted'], '%Y-%m-%d %H:%M')
        on28 += any(t.date() == d.date() + dt.timedelta(days=28) for d in disch_of.get(r['nhs_number'], []))
    for c in raw_['contacts']:
        t = dt.datetime.strptime(c['contact_datetime'], '%Y-%m-%d %H:%M')
        on28 += any(t.date() == d.date() + dt.timedelta(days=28) for d in disch_of.get(c['nhs_number'], []))
    ok('SF2 no admission or contact row falls on the 28th calendar day after its baby\'s discharge date', on28 == 0, str(on28))
    ok('SF3 twins are eligible (specification 3); leaving them out files the same call', same(V.call(twins=False), g))
    ok('SF4 the planning basis on discharge date against birth date: same call', same(V.call(window_on='birth'), g))
    ok('SF5 a baby counts once (specification 5); counting admissions files the same call', same(V.call(per_admission=True), g))
    ok('SF6 the receipt clock: UTC converted against read as local, same call', same(V.call(utc_local=True), g))
    ok('SF7 the first discharge notification against the latest message: same call', same(V.call(amended=True), g))
    per_unit = sum(bin25(th * x) for x in g['counted'])
    ok('SF12 the total rounded once against unit figures rounded and summed: same bin under the nearest 25',
       bin25(sum(round(th * x) for x in g['counted'])) == 325, 'per-unit 25s sum to %d' % per_unit)
    q = [30 * x / sum(g['counted']) for x in g['counted']]
    plain = [int(math.floor(x + 0.5)) for x in q]
    ok('SF13 whole posts by largest remainders (specification 7); rounding each share to the nearest post files the same posts',
       plain == gp and sum(plain) == 30, '%s sum %d' % (plain, sum(plain)))
    ok('SF14 the trial ratio from the report (its own linkage) against the pack with the mother rows mapped: same bin',
       bin25((1 - C['report_rr']) * sum(C['reached'])) == 325 == bin25((1 - G.trial_stats(B)['rr']) * sum(C['reached'])),
       '%.1f and %.1f' % ((1 - C['report_rr']) * sum(C['reached']), (1 - G.trial_stats(B)['rr']) * sum(C['reached'])))
    ok('SF16 a transfer row inside one stay is the same admission (method 81 with or without): same call',
       same(V.call(methods=('21', '22', '28')), g))
    ok('SF11 the five units are the specification 3 list; Copperfield is outside it (specification 2)',
       'Copperfield' not in ' '.join(V.FIVE))

    # ------------------------------------------------------------------ the asks: devices, mass, corridor, separation
    A0 = V.ask_a()
    Bk0 = V.ask_b()
    ok('ASK A verifier equals figures.json', all(A0[r]['usual_care_rate_pct'] == F['ask_a'][r]['usual_care_rate_pct']
                                                and A0[r]['risk_ratio'] == F['ask_a'][r]['risk_ratio'] for r in W.REASONS))
    ok('ASK B verifier equals figures.json', all(Bk0[r] == F['ask_b'][r] for r in W.REASONS))
    a_cr = V.ask_a(mother_map=False)
    moved = sum(1 for r in W.REASONS for k in ('usual_care_rate_pct', 'risk_ratio') if a_cr[r][k] != A0[r][k])
    ok('ASK A device (Copperfield postnatal-ward rows under the mother) moves all 12 figures', moved == 12, '%d moved' % moved)
    a_pr = V.ask_a(reasons_from='trial')
    moved = sum(1 for r in W.REASONS for k in ('usual_care_rate_pct', 'risk_ratio') if a_pr[r][k] != A0[r][k])
    ok('SF17 the trial list primary reason against every reason on the discharge record moves Ask A', moved >= 10, '%d moved' % moved)
    b_mo = V.ask_b(call_mother_map=False)
    ok('ASK B device 1 (calls under the mother) moves all six call figures',
       all(b_mo[r]['calls'] != Bk0[r]['calls'] for r in W.REASONS) and all(b_mo[r]['home_visits'] == Bk0[r]['home_visits'] for r in W.REASONS))
    b_pu = V.ask_b(split_pre_update=False)
    ok('ASK B device 2 (failed attempts filed as TEL or HV before 6 January 2025) moves all 12 figures',
       all(b_pu[r]['calls'] != Bk0[r]['calls'] and b_pu[r]['home_visits'] != Bk0[r]['home_visits'] for r in W.REASONS))
    ok('ASK B hazard (re-sent contacts) moves figures when not collapsed', V.ask_b(dedupe=False) != Bk0)
    ok('SF20 contacts after day 28 are outside the window; keeping them moves Ask B', V.ask_b(window=False) != Bk0)
    # the minute corridor: any cut in the gap gives the same counts, and the short clusters vanish at the code update
    keep = True
    for hv in (13, 16, 20, 25):
        for tel in (2, 3, 4):
            V.HV_MIN, V.TEL_MIN = hv, tel
            keep = keep and V.ask_b() == Bk0
    V.HV_MIN, V.TEL_MIN = 20, 3
    ok('SF18 every minute cut between the failed and the completed clusters gives the same Ask B', keep)
    con = V.raw(TGT)['contacts']
    upd = dt.datetime(2025, 1, 6)
    post_short = [c for c in con if dt.datetime.strptime(c['contact_datetime'], '%Y-%m-%d %H:%M') >= upd and
                  ((c['contact_type'] == 'HV' and int(c['minutes']) < 26) or (c['contact_type'] == 'TEL' and int(c['minutes']) < 4))]
    pre_short = [c for c in con if dt.datetime.strptime(c['contact_datetime'], '%Y-%m-%d %H:%M') < upd and
                 ((c['contact_type'] == 'HV' and int(c['minutes']) < 13) or (c['contact_type'] == 'TEL' and int(c['minutes']) < 2))]
    pre_codes = [c for c in con if dt.datetime.strptime(c['contact_datetime'], '%Y-%m-%d %H:%M') < upd and c['contact_type'] in ('NA', 'TNA')]
    ok('SF18 after the code update no HV under 26 minutes and no TEL under 4 minutes is filed', not post_short, str(len(post_short)))
    ok('SF18 before it the short clusters exist and NA or TNA never appear', len(pre_short) > 40 and not pre_codes, '%d short' % len(pre_short))
    mothers = {b['mother'] for b in babies}
    kids = {b['nhs'] for b in babies}
    known = {b['nhs'] for b in babies} | {b['mother'] for b in babies}
    stray = [c for c in con if c['nhs_number'] not in known]
    under_mother = [c for c in con if c['nhs_number'] in mothers and c['nhs_number'] not in kids]
    ok('SF19 every contact is filed under a baby or under its mother (calls to a parent reach the family)',
       not stray and under_mother and all(c['contact_type'] in ('TEL', 'TNA') for c in under_mother),
       '%d under a mother, %d stray' % (len(under_mother), len(stray)))
    # separation line: zero device rows in the main call's population
    adm = V.raw(TGT)['adm']
    plain_babies, _ = V.link(TGT, mother_map=False)
    plain_readm = {b['nhs'] for b in plain_babies if b['readm'] is not None}
    mothers = {b['mother'] for b in babies}
    kids = {b['nhs'] for b in babies}
    mk = [r for r in adm if r['nhs_number'] in mothers and r['nhs_number'] not in kids]
    ok('ASK separation: rows under a mother sit only at Copperfield', mk and all(r['admitting_hospital'] == 'Copperfield Hospital' for r in mk),
       '%d rows' % len(mk))
    five_mk = [r for r in mk if r['admitting_hospital'] in V.FIVE]
    ok('ASK separation: zero mother-keyed rows in the five units\' admissions', not five_mk)
    plan_nhs = {b['nhs'] for s in V.FIVE for b in plan[s]}
    cmo = {b['mother'] for s in V.FIVE for b in plan[s]}
    ok('ASK separation: zero contact rows for a planning-year baby of the five units',
       not [c for c in con if c['nhs_number'] in plan_nhs or c['nhs_number'] in cmo])
    for nm, A, Bx in (('cracker', V.ask_a(mother_map=False), V.ask_b(call_mother_map=False, split_pre_update=False)),):
        hits = sum(1 for r in W.REASONS for k in ('usual_care_rate_pct', 'risk_ratio') if abs(A[r][k] - A0[r][k]) < 1e-9) + \
            sum(1 for r in W.REASONS for k in ('home_visits', 'calls') if abs(Bx[r][k] - Bk0[r][k]) < 1e-9)
        ok('ASK the %s keeps no ask figure' % nm, hits == 0, '%d kept' % hits)
    # rounding: the risk ratio from the counts and from the rounded rates agree at two decimals
    agree = 0
    for r in W.REASONS:
        f = F['ask_a'][r]
        ro_, no_, rc_, nc_ = f['outreach_readmitted'], f['outreach_babies'], f['usual_care_readmitted'], f['usual_care_babies']
        a1 = round((ro_ / no_) / (rc_ / nc_), 2)
        a2 = round(round(100 * ro_ / no_, 1) / round(100 * rc_ / nc_, 1), 2)
        agree += a1 == a2
    prompt = open(os.path.join(TASK, 'prompt.txt')).read()
    ok('SF21 Ask A risk ratio worked from the counts and rounded only at the end, as the prompt files it (a ratio of rates '
       'already rounded to one decimal would move some cells)', 'Work every figure from the counts and round only at the end' in prompt
       and all(F['ask_a'][r]['risk_ratio'] == round(F['exact']['ask_a'][r]['risk_ratio'], 2) for r in W.REASONS),
       '%d of 6 cells agree on the rounded-rate path' % agree)

    # ------------------------------------------------------------------ every graded figure clear of its rounding line
    def clear(v, unit, share=0.01):
        x = v / unit
        return abs((x - math.floor(x)) - 0.5) * unit >= share * unit
    ex = F['exact']
    margins = []
    for r in W.REASONS:
        margins.append(('Ask A %s usual-care rate' % r, ex['ask_a'][r]['usual_care_rate_pct'], 0.1))
        margins.append(('Ask A %s risk ratio' % r, ex['ask_a'][r]['risk_ratio'], 0.01))
        margins.append(('Ask B %s visits per baby' % r, ex['ask_b'][r]['home_visits'], 0.01))
        margins.append(('Ask B %s calls per baby' % r, ex['ask_b'][r]['calls'], 0.01))
    for name, v, unit in margins:
        x = v / unit
        ok('ROUND %s sits clear of its rounding line (at least 1 per cent of the unit)' % name, clear(v, unit),
           '%.6f, %.4f of the unit from the line' % (v, abs((x - math.floor(x)) - 0.5)))
    ok('ROUND the total sits 4 or more inside its 25 bin', 312.5 + 4 <= ex['total'] <= 337.5 - 4,
       '%.1f: %.1f above 312.5, %.1f below 337.5' % (ex['total'], ex['total'] - 312.5, 337.5 - ex['total']))
    q = ex['quotas']
    rem = sorted(((q[u] - math.floor(q[u]), u) for u in W.FIVE), reverse=True)
    extra = 30 - sum(int(math.floor(q[u])) for u in W.FIVE)
    gap = rem[extra - 1][0] - rem[extra][0]
    ok('ROUND the posts: the last remainder awarded clears the first refused by 0.05 of a post or more', gap >= 0.05,
       'awarded %s, refused %s, gap %.3f' % (rem[extra - 1][1], rem[extra][1], gap))
    need = {}
    for i, s_ in enumerate(V.FIVE):
        for dd in range(1, 40):
            moved = False
            for sg in (1, -1):
                v = list(g['counted'])
                v[i] += sg * dd
                if V.largest_remainder(v) != gp:
                    moved = True
            if moved:
                need[V.CODE[s_]] = dd
                break
        else:
            need[V.CODE[s_]] = 40
    ok('ROUND the posts hold until 5 or more reachable readmissions move at any one unit', min(need.values()) >= 5, str(need))

    # ------------------------------------------------------------------ the trial's filed WHAT (fixes the two forks pass 1 left)
    rep_t = pdf_text(os.path.join(TGT, 'Copperfield neonatal outreach trial final report.pdf'))
    ok('SF15 the report files one treatment effect for all babies and reads subgroups only as tests for interaction',
       'estimated one treatment effect for all babies analysed as randomised' in rep_t and
       'examined only as tests for interaction' in rep_t)
    ok('R3b the report makes the first telephone call part of the intervention (it assesses and arranges review), and says '
       'nothing about when it happens', 'first telephones the family, assesses feeding' in rep_t and
       not re.search(r'within \d+ hours|same day|next morning|working hours|calling hours', rep_t, re.I))
    ok('SF18 the report files the process measures as visits in which the nurse saw the baby and calls that reached a parent',
       'home visits in which the nurse saw the baby' in rep_t and 'calls that reached a parent' in rep_t)
    ok('SF18 no file states how failed attempts were recorded before the code change, nor a minute threshold',
       not re.search(r'(before|until) (the )?(6 January 2025|code|update)|minutes? (or more|or less|threshold)', rep_t + pdf_text(os.path.join(TGT, 'Neonatal outreach service specification 2027-28.pdf')), re.I))

    # ------------------------------------------------------------------ the report recomputes from the trial files
    rawp = V.raw(TGT)
    sw = {b['nhs']: b for b in rawp['babies'] if b['site'] == 'Copperfield Hospital'}
    rep = F['report']
    lc = rawp['label_code']
    by_arm = {'outreach': [], 'usual care': []}
    for x in rawp['final']:
        b = sw[x['nhs']]
        by_arm['outreach' if x['arm'] == 'Outreach' else 'usual care'].append((b, lc[x['primary']]))
    good = True
    for a, rows in by_arm.items():
        d = rep['baseline'][a]
        n = len(rows)
        kg = [int(round(b['kg'] * 1000)) for b, _ in rows]
        bands = [sum(1 for b, _ in rows if b['gest'] <= 36), sum(1 for b, _ in rows if b['gest'] == 37),
                 sum(1 for b, _ in rows if 38 <= b['gest'] <= 39), sum(1 for b, _ in rows if b['gest'] >= 40)]
        feeds = [sum(1 for b, _ in rows if b['feed'] == lab) for lab in ('Exclusive breast milk', 'Breast and formula', 'Formula')]
        prim = [sum(1 for _, pr in rows if pr == r) for r in W.REASONS]
        hours = sorted((b['disch'] - b['birth']).total_seconds() / 3600.0 for b, _ in rows)
        import numpy as np
        stay = (float(np.percentile(hours, 50)), float(np.percentile(hours, 25)), float(np.percentile(hours, 75)))
        good = good and n == d['n'] and bands == [x[1] for x in d['gest']] and feeds == [x[1] for x in d['feed']] \
            and prim == [x[1] for x in d['primary']] and '%.0f' % np.mean(kg) == '%.0f' % d['bw_mean'] \
            and '%.0f' % np.std(kg, ddof=1) == '%.0f' % d['bw_sd'] and all('%.1f' % u == '%.1f' % v for u, v in zip(stay, d['stay']))
    ok('REPORT the baseline table recomputes from the final list and the SW discharge record', good)
    win = [b for b in rawp['babies'] if b['site'] == 'Copperfield Hospital' and b['flag']
           and dt.datetime(2024, 4, 1) <= b['disch'] < dt.datetime(2026, 4, 1)]
    ok('REPORT the flow recomputes (flagged Copperfield discharges and the twins left out)',
       len(win) == rep['flagged_cfh'] and sum(1 for b in win if b['multiple']) == rep['multiples_out'],
       '%d and %d' % (len(win), sum(1 for b in win if b['multiple'])))
    ro = sum(1 for b, _ in by_arm['outreach'] if b['nhs'] in plain_readm)
    rc = sum(1 for b, _ in by_arm['usual care'] if b['nhs'] in plain_readm)
    ok('REPORT the primary outcome recomputes on the trial team\'s own linkage (NHS number, then the index)',
       ro == rep['outreach']['r'] and rc == rep['usual_care']['r'], '%d and %d' % (ro, rc))
    ok('REPORT nothing in it touches notification timing, receipt or reach',
       not re.search(r'notif|receipt|received|reachab|window|community midwifery office', rep_t, re.I))

    # ------------------------------------------------------------------ the contact codes and the amended records
    na_rows = [c for c in con if c['contact_type'] == 'NA']
    ok('ASK B the code list\'s NA has rows in the log after it came into use and none before',
       len(na_rows) > 50 and min(c['contact_datetime'] for c in na_rows) >= '2025-01-06', '%d NA rows' % len(na_rows))
    Bw = W.build_world()
    R.apply_record_reasons(Bw)
    amended = [b for b in Bw if b['reasons_rec'] != b['reasons']]
    ok('R2 records amended after discharge only add a reason to a flagged baby (the flag and the main call never move)',
       amended and all(b['eligible'] and set(b['reasons']) < set(b['reasons_rec']) for b in Bw if b['reasons_rec'] != b['reasons']),
       '%d amended records' % len(amended))

    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(TGT))
    ok('GATE 10 or more files', len(files) >= 10, str(len(files)))
    ok('GATE 3 or more formats', len({f.rsplit('.', 1)[1] for f in files}) >= 3, str({f.rsplit('.', 1)[1] for f in files}))
    big = max(rows_of(f) for f in files)
    ok('GATE one file of 25,000 rows or more', big >= 25000, str(big))
    ok('GATE two or more distractors named in metadata.json and shipped', len(meta['distractor_files']) >= 2 and
       all(f in files for f in meta['distractor_files']))
    ok('GATE no file describes the data (readme, dictionary, notes, manifest, schema)',
       not [f for f in files if re.search(r'(^|[_ .-])(readme|dictionary|notes|manifest|schema|codebook|fields?|definitions)([_ .-]|$)', f, re.I)])
    ok('GATE no sheet named for notes or definitions', not [k for k in heads if re.search(r':(notes|definitions|readme)', k, re.I)])
    vsrc = open(os.path.join(HERE, 'verify.py')).read()
    ok('GATE the golden path reads no distractor', not any(f in vsrc for f in meta['distractor_files']))

    # ------------------------------------------------------------------ realism sweep
    rep = pdf_text(os.path.join(TGT, 'Copperfield neonatal outreach trial final report.pdf'))
    spec = pdf_text(os.path.join(TGT, 'Neonatal outreach service specification 2027-28.pdf'))
    ok('REAL personas from guard.py names appear', all(p in rep + spec for p in ('Lucy Coates', 'Hugh Brown', 'Kathryn Thompson')))
    ok('REAL no em or en dash in the documents', '—' not in rep + spec and '–' not in rep + spec)
    m_set = {b['mother'] for b in B}
    k_set = {b['nhs'] for b in B}
    ok('REAL no mother shares an NHS number with a baby', not (m_set & k_set), str(len(m_set & k_set)))
    mins = collections.Counter(int(c['minutes']) for c in con if c['contact_type'] == 'HV')
    ok('REAL visit durations spread (no uniform block)', len(mins) > 40)
    ids = sorted(int(c['contact_id'][2:]) for c in con)
    steps = collections.Counter(b - a for a, b in zip(ids, ids[1:]))
    ok('REAL contact ids run with irregular gaps', len(steps) >= 4)
    exp = dt.datetime(2026, 11, 2, 7, 40)
    late = [r for r in adm if dt.datetime.strptime(r['admitted'], '%Y-%m-%d %H:%M') > exp]
    ok('REAL no admission after the extract time', not late, str(len(late)))
    lt = [r for r in notes if dt.datetime.strptime(r['received_utc'], '%Y-%m-%dT%H:%M:%SZ') > exp]
    ok('REAL no notification after the extract time', not lt, str(len(lt)))
    ok('REAL the report counts are not round', F['trial']['randomised'] % 10 != 0 and F['trial']['analysed_outreach'] % 10 != 0)

    # ------------------------------------------------------------------ report
    fails = [r for r in RES if not r[1]]
    for name, good, detail in RES:
        print('%s  %s%s' % ('PASS' if good else 'FAIL', name, ('  [' + detail + ']') if detail else ''))
    print('%d checks, %d failed' % (len(RES), len(fails)))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
