"""task401 golden: every figure computed from the shipped files under target/ alone (no world object), written to
figures.json by build.py. Costs are total marks across the pupils a change reached (the register's remit)."""
import datetime as dt
import os
import re

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), 'target')
YG = ('S1', 'S2', 'S3')
SECURE = 36


def rd(name, **kw):
    return pd.read_csv(os.path.join(T, name), dtype=str, keep_default_na=False, **kw)


# ------------------------------------------------------------------------------------------------ the main call
def load():
    xl = os.path.join(T, 'common_paper_and_unit_map.xlsx')
    pmap = {g: pd.read_excel(xl, sheet_name=g + ' paper', dtype=str) for g in YG}
    skills = pd.read_excel(xl, sheet_name='Corvella skills', dtype=str)
    topics = {g: list(dict.fromkeys(pmap[g]['Topic'])) for g in YG}
    tix = {g: {t: i for i, t in enumerate(sorted(topics[g]))} for g in YG}       # topics indexed alphabetically
    qtop = {g: dict(zip(pmap[g]['Question'], pmap[g]['Topic'])) for g in YG}
    qmax = {g: dict(zip(pmap[g]['Question'], pmap[g]['Marks'].astype(int))) for g in YG}
    old2t = {g: dict(zip(pmap[g]['Unit 2024-25'], pmap[g]['Topic'])) for g in YG}
    new2t = {g: dict(zip(pmap[g]['Unit 2025-26'], pmap[g]['Topic'])) for g in YG}
    sk2u = dict(zip(skills['Corvella skill'], skills['Unit 2024-25']))
    r6 = rd('pupil_roll_extract_2026-06-12.csv')
    r5 = rd('pupil_roll_2024-25.csv')
    return dict(pmap=pmap, tix=tix, qtop=qtop, qmax=qmax, old2t=old2t, new2t=new2t, sk2u=sk2u, r6=r6, r5=r5)


def session_arrays(L, year):
    """per sitting pupil: topic shares of June marks (pupil x 12), first-homework accuracy by topic, P7, FSM, keys"""
    if year == 2026:
        roll = L['r6'].rename(columns={'SCN': 'scn', 'Stage': 'yg', 'P7_Numeracy_SS': 'p7', 'FSM': 'fsm',
                                       'School': 'school', 'Maths_Class': 'cls', 'MIS_Ref': 'ref'})
        roll['fsm'] = roll['fsm'] == 'Y'
        m = rd('june_common_paper_marks_2026.csv')
        m = m.rename(columns={'SCN': 'scn'})
        m['Question'] = 'Q' + m['Question'].str[1:].str.zfill(2)
        sat = set(m.loc[m['Status'] == 'Present', 'scn'])
        m = m[m['Status'] == 'Present']
        key = 'scn'
    else:
        roll = L['r5'].rename(columns={'Candidate No': 'scn', 'Pupil Ref': 'ref', 'Year': 'yg', 'P7 Numeracy': 'p7',
                                       'FME': 'fsm', 'Establishment': 'school', 'Maths Set': 'cls'})
        roll['fsm'] = roll['fsm'] == 'Yes'
        w = rd('june_common_paper_marks_2025.csv')
        w = w[w['Attendance'] == 'P']
        sat = set(w['Pupil Ref'])
        m = w.melt(id_vars=['Pupil Ref', 'Year', 'Attendance'], var_name='Question', value_name='Mark')
        m = m.rename(columns={'Pupil Ref': 'ref'})
        key = 'ref'
    roll = roll[roll[key].isin(sat)].reset_index(drop=True)
    n = len(roll)
    pos = {k: i for i, k in enumerate(roll[key])}
    yg_of = dict(zip(roll[key], roll['yg']))
    y = np.zeros((n, 12))
    mm = m.copy()
    mm['i'] = mm[key].map(pos)
    mm['g'] = mm[key].map(yg_of)
    mm['Mark'] = mm['Mark'].astype(int)
    tot = mm.groupby('i')['Mark'].sum()
    for g in YG:
        sub = mm[mm['g'] == g]
        t = sub['Question'].map(L['qtop'][g]).map(L['tix'][g]).values
        np.add.at(y, (sub['i'].values, t), sub['Mark'].values)
    tmax = np.zeros(12)
    for q, t in L['qtop']['S1'].items():
        tmax[L['tix']['S1'][t]] += L['qmax']['S1'][q]
    y = y / tmax[None, :]
    total = tot.reindex(range(n)).values.astype(float)
    # first homework accuracy by topic
    acc = np.full((n, 12), np.nan)
    if year == 2026:
        hw = pd.read_parquet(os.path.join(T, 'mathsbridge_homework_export_2025-26.parquet'))
        hw = hw[(hw['task_kind'] == 'Unit') & (hw['status'] == 'Completed')]
        g2s = dict(zip(L['r6']['Glow_ID'], L['r6']['SCN']))
        hw = hw.assign(k=hw['glow_id'].map(g2s))
        hw = hw[hw['k'].isin(pos)]
        for g in YG:
            sub = hw[hw['k'].map(yg_of) == g]
            t = sub['units'].map(L['new2t'][g]).map(L['tix'][g]).values
            acc[sub['k'].map(pos).values, t] = sub['score_pct'].values / 100.0
    else:
        hw = rd('corvella_homework_export_2024-25.csv')
        hw = hw[(hw['TaskType'] == 'Homework') & (hw['Status'] == 'Complete')]
        hw = hw[hw['LearnerID'].isin(pos)]
        unit = hw['Skills'].str.split(';').str[0].map(L['sk2u'])
        for g in YG:
            sel = (hw['LearnerID'].map(yg_of) == g).values
            sub = hw[sel]
            t = unit[sel].map(L['old2t'][g]).map(L['tix'][g]).values
            acc[sub['LearnerID'].map(pos).values, t] = sub['CorrectFirstAttempt'].astype(int).values / sub['Questions'].astype(int).values
    p7 = pd.to_numeric(roll['p7'], errors='coerce').values
    return dict(roll=roll, n=n, y=y, total=total, acc=acc, p7=p7, fsm=roll['fsm'].values.astype(float),
                yg=roll['yg'].values, school=roll['school'].values, cls=roll['cls'].values)


def weak(acc, q=1 / 3):
    ok = ~np.isnan(acc)
    with np.errstate(all='ignore'):
        cut = np.nanquantile(np.where(ok, acc, np.nan), q, axis=1)
    return ok & (acc <= cut[:, None]), ok


def within(y, a, b):
    na, nb = a.sum(1), b.sum(1)
    ma = np.where(na > 0, (y * a).sum(1) / np.maximum(na, 1), np.nan)
    mb = np.where(nb > 0, (y * b).sum(1) / np.maximum(nb, 1), np.nan)
    return np.nanmean(ma - mb)


def wsum(y, wk, ok):
    na, nb = wk.sum(1), (ok & ~wk).sum(1)
    ma = np.where(na > 0, (y * wk).sum(1) / np.maximum(na, 1), np.nan)
    mb = np.where(nb > 0, (y * (ok & ~wk)).sum(1) / np.maximum(nb, 1), np.nan)
    return np.nanmean(na * (ma - mb))


def p7_resid(S):
    have = ~np.isnan(S['p7'])
    x = np.where(have, (S['p7'] - 100) / 15.0, 0.0)
    X = np.column_stack([np.ones(S['n']), x, (~have).astype(float), S['fsm']])
    b = np.linalg.lstsq(X, S['total'], rcond=None)[0]
    return S['total'] - X @ b


def rewritten_topics(L):
    """from the change register's section 4: the new unit codes of the rewritten units"""
    import docx
    d = docx.Document(os.path.join(T, 's1-s3_maths_change_register_2025-26.docx'))
    rw = {g: set() for g in YG}
    for p in d.paragraphs:
        m = re.match(r'^(S[123]): (.*)\.$', p.text)
        if m:
            for code in re.findall(r'N[123]\.\d\d', m.group(2)):
                rw[m.group(1)].add(L['tix'][m.group(1)][L['new2t'][m.group(1)][code]])
    return rw


def split_classes():
    import docx
    d = docx.Document(os.path.join(T, 's1-s3_maths_change_register_2025-26.docx'))
    out, on = set(), False
    for p in d.paragraphs:
        if p.text.startswith('5. Change E'):
            on = True
            continue
        if on and p.text.startswith('6.'):
            break
        if on and ':' in p.text:
            sch, rest = p.text.split(': ', 1)
            for k in rest.rstrip('.').split(', '):
                out.add((sch, k))
    return out


def main_call(L, mode=1 / 3):
    S5, S6 = session_arrays(L, 2025), session_arrays(L, 2026)
    wk5, ok5 = weak(S5['acc'], mode)
    wk6, ok6 = weak(S6['acc'], mode)
    costB = -(wsum(S6['y'], wk6, ok6) - wsum(S5['y'], wk5, ok5)) * 5 * S6['n']
    rw = rewritten_topics(L)
    def rmask(S):
        m = np.zeros((S['n'], 12), bool)
        for g in YG:
            for t in rw[g]:
                m[S['yg'] == g, t] = True
        return m
    rw5, rw6 = rmask(S5), rmask(S6)
    exA = within(S6['y'], rw6, ~rw6) - within(S5['y'], rw5, ~rw5)
    costA = -exA * 5 * rw6.sum()
    e5, e6 = p7_resid(S5), p7_resid(S6)
    def did(m6, m5=None):
        a = e6[m6].mean() - e6[~m6].mean()
        if m5 is not None:
            a -= e5[m5].mean() - e5[~m5].mean()
        return -a * m6.sum()
    refs = dict(zip(L['r6']['SCN'], L['r6']['Base_Referrals'].astype(int)))
    removed = np.array([refs[s] > 0 for s in S6['roll']['scn']])
    sp = split_classes()
    split = np.array([(s, c) in sp for s, c in zip(S6['school'], S6['cls'])])
    costs = dict(A=costA, B=costB, C=did(S6['yg'] == 'S3', S5['yg'] == 'S3'), D=did(removed), E=did(split))
    head = {}
    for yr, S in ((2025, S5), (2026, S6)):
        head[yr] = dict(sat=int(S['n']), mean=float(S['total'].mean()), secure=int((S['total'] >= SECURE).sum()),
                        share=float(100.0 * (S['total'] >= SECURE).mean()))
    by_school = {}
    for yr, S in ((2025, S5), (2026, S6)):
        for sch in sorted(set(S['school'])):
            by_school.setdefault(sch, {})[yr] = float(S['total'][S['school'] == sch].mean())
    reach = dict(A=int(rw6.sum()), B=int(S6['n']), C=int((S6['yg'] == 'S3').sum()), D=int(removed.sum()), E=int(split.sum()))
    extra = dict(exB_2025=float(within(S5['y'], wk5, ok5 & ~wk5)), exB_2026=float(within(S6['y'], wk6, ok6 & ~wk6)),
                 exA=float(exA), n_rewritten_cells=int(rw6.sum()))
    order = sorted(costs, key=costs.get)
    return dict(costs={k: float(v) for k, v in costs.items()}, head=head, by_school=by_school, reach=reach, extra=extra,
                call=order[-1], runner=order[-2])


# ------------------------------------------------------------------------------------------------ ask 1: base lessons
def bells():
    b = pd.read_excel(os.path.join(T, 'bell_times_2025-26.xlsx'), dtype=str)
    out = {}
    for _, r in b.iterrows():
        out.setdefault((r['School'], r['Days']), []).append((int(r['Period']), r['Start'], r['End']))
    return out


def tmin(s):
    h, m = s.split(':')
    return int(h) * 60 + int(m)


def period_at(bl, t, upto=False):
    """the period whose span holds time t; with upto (a time out), the last period that started before t, so a pupil
    signed out on the bell is not signed in for any part of the next period"""
    best = None
    for p, a, b in sorted(bl):
        if not upto and tmin(a) <= t < tmin(b):
            return p
        if upto and tmin(a) < t:
            best = p
    return best


def autumn_classes(roll, purity=False):
    mb = pd.read_parquet(os.path.join(T, 'mathsbridge_homework_export_2025-26.parquet'),
                         columns=['glow_id', 'task_kind', 'set_on', 'units'])
    rv = mb[(mb['task_kind'] == 'Review') & (mb['set_on'] < '2026-01-06')].sort_values(['glow_id', 'set_on'])
    sig = (rv['set_on'] + ':' + rv['units']).groupby(rv['glow_id']).agg('|'.join)
    r2 = roll.set_index('Glow_ID')
    df = pd.DataFrame({'sig': sig.values, 'school': r2.loc[sig.index, 'School'].values,
                       'stage': r2.loc[sig.index, 'Stage'].values, 'june': r2.loc[sig.index, 'Maths_Class'].values},
                      index=sig.index)
    grp = df.groupby(['school', 'stage', 'sig'])['june']
    mode = grp.agg(lambda v: v.value_counts().sort_index().idxmax())
    share = grp.agg(lambda v: v.value_counts().max() / len(v))
    out = {g: mode[(r['school'], r['stage'], r['sig'])] for g, r in df.iterrows()}
    return (out, share) if purity else out


def ask_lessons():
    si = rd('support_base_signins_2025-11-03_to_2026-05-29.csv').drop_duplicates()
    roll = rd('pupil_roll_extract_2026-06-12.csv')
    byscn = roll.set_index('SCN')
    key = (roll['Forename'] + ' ' + roll['Surname']).str.lower() + '|' + roll['Stage']
    name2scn = roll.groupby(key)['SCN'].agg(list).to_dict()
    served = {}
    for _, r in si[si['SCN'].isin(byscn.index)].iterrows():
        served.setdefault(r['Base'], set()).add(byscn.loc[r['SCN'], 'School'])
    tt = rd('maths_timetable_2025-26.csv')
    tt['vf'] = pd.to_datetime(tt['Valid_From'], format='%d/%m/%Y').dt.date
    tt['vt'] = pd.to_datetime(tt['Valid_To'], format='%d/%m/%Y').dt.date
    slots = {}
    for _, r in tt.iterrows():
        slots.setdefault((r['School'], r['Class']), []).append((r['vf'], r['vt'], r['Day'], int(r['Period'])))
    bl = bells()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    # each pupil's class on a date: the roll and the platform both carry the class as at June; in the autumn term a
    # pupil sat with the classmates who were set the same review each week, so their autumn class is the June class most
    # of those classmates still hold
    aut = autumn_classes(roll)
    g_of = dict(zip(roll['SCN'], roll['Glow_ID']))
    def class_on(scn, d):
        if d >= dt.date(2026, 1, 6):
            return byscn.loc[scn, 'Maths_Class']
        return aut.get(g_of[scn], byscn.loc[scn, 'Maths_Class'])
    seen, unresolved = set(), 0
    out = {}
    for _, r in si.iterrows():
        if r['SCN']:
            scn = r['SCN']
            if scn not in byscn.index:      # an S4 to S6 pupil
                continue
        else:
            if r['Year_Typed'] not in YG:
                continue
            c = name2scn.get(r['Name_Typed'].lower() + '|' + r['Year_Typed'], [])
            if len(c) > 1:
                c = [x for x in c if byscn.loc[x, 'School'] in served[r['Base']]]
            if len(c) != 1:
                unresolved += 1
                continue
            scn = c[0]
        p = byscn.loc[scn]
        d = dt.datetime.strptime(r['Date'], '%d/%m/%Y').date()
        dk = 'Friday' if d.weekday() == 4 else 'Monday to Thursday'
        b = bl[(p['School'], dk)]
        p0 = period_at(b, tmin(r['Time_In']))
        p1 = p0 if not r['Time_Out'] else period_at(b, tmin(r['Time_Out']), upto=True)
        dn = days[d.weekday()]
        live = {(dd, pp) for vf, vt, dd, pp in slots[(p['School'], class_on(scn, d))] if vf <= d <= vt}
        for per in range(p0, p1 + 1):
            if (dn, per) in live and (scn, d, per) not in seen:
                seen.add((scn, d, per))
                out[p['School']] = out.get(p['School'], 0) + 1
    return out, unresolved


# ------------------------------------------------------------------------------------------------ ask 2: classes
def norm_staff(name):
    """(first initial, surname) from 'Mrs A. Williams' or 'Aimee Williams'"""
    parts = name.replace('.', '').split()
    if parts[0] in ('Mr', 'Mrs', 'Ms', 'Miss', 'Dr'):
        parts = parts[1:]
    return parts[0][0].upper(), ' '.join(parts[1:]).upper()


def dmy(s):
    return dt.datetime.strptime(s, '%d/%m/%Y').date() if s else None


def staff_tables():
    """the timetable, the two terms' staff code sheets and the establishment, with each term's dates read off the
    timetable's own validity windows (the autumn rows end and the spring rows begin at the Christmas holiday)"""
    tt = rd('maths_timetable_2025-26.csv')
    xl = os.path.join(T, 'timetable_staff_codes_2025-26.xlsx')
    sheets = {'autumn': pd.read_excel(xl, sheet_name='Autumn 2025', dtype=str),
              'spring': pd.read_excel(xl, sheet_name='Spring 2026', dtype=str)}
    est = pd.read_excel(os.path.join(T, 'maths_staffing_establishment_2025-26.xlsx'), dtype=str).fillna('')
    est['ini'] = est['Holder'].str.split(', ').str[1].str[0].str.upper()
    est['sur'] = est['Holder'].str.split(', ').str[0].str.upper()
    est['prev'] = est['Previous_Surname'].str.upper()
    est['from'] = est['In_Post_From'].map(dmy)
    est['to'] = est['In_Post_To'].map(dmy)
    vf = sorted({dmy(x) for x in tt['Valid_From']})
    vt = sorted({dmy(x) for x in tt['Valid_To']})
    terms = {'autumn': (vf[0], vt[0]), 'spring': (vf[-1], vt[-1])}
    return tt, sheets, est, terms


def holders_named(est, sheets, school, term, code):
    """the establishment rows of the person a term's code sheet names on a code: same first initial, and the surname
    the holder carries or carried before (Previous_Surname)"""
    sh = sheets[term]
    nm = sh[(sh['School'] == school) & (sh['Code'] == code)]['Name'].iloc[0]
    ini, sur = norm_staff(nm)
    cand = est[est['School'].str.contains(school, regex=False) & (est['ini'] == ini) &
               ((est['sur'] == sur) | (est['prev'] == sur))]
    assert cand['Holder'].nunique() == 1, (school, term, code, nm, list(cand['Holder']))
    return cand


def class_teachers(in_post=True):
    """each class's teachers in the session: every timetable row, for each term its validity runs through, the person
    that term's code sheet names on the row's code; with in_post, only where that person held a post on a day of the
    row's window in that term (a holder whose contract ended before the row's first lesson taught none of it)"""
    tt, sheets, est, terms = staff_tables()
    out = {}
    for _, r in tt.iterrows():
        f, t = dmy(r['Valid_From']), dmy(r['Valid_To'])
        ppl = out.setdefault((r['School'], r['Class']), set())
        for term, (a, b) in terms.items():
            lo, hi = max(f, a), min(t, b)
            if lo > hi:
                continue
            cand = holders_named(est, sheets, r['School'], term, r['Staff'])
            if in_post:
                cand = cand[(cand['from'] <= hi) & cand['to'].map(lambda x: x is None or x >= lo)]
            ppl |= set(cand['Holder'])
    return out


def ask_classes():
    out = {}
    for (sch, cls), ppl in sorted(class_teachers().items()):
        out[sch] = out.get(sch, 0) + int(len(ppl) > 1)
    return out


def run():
    L = load()
    F = main_call(L)
    les, unres = ask_lessons()
    F['ask_lessons'] = les
    F['ask_lessons_unresolved'] = unres
    F['ask_classes'] = ask_classes()
    return F


if __name__ == '__main__':
    import json
    F = run()
    print(json.dumps(F, indent=1, default=str)[:3000])
