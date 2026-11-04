"""task401 pack: renders the world (world.py) and the staffing records (staffing.py) into Strathcorrie Council's own
files under target/, on its own random stream (the world's draws are never re-drawn). Called by build.py."""
import datetime as dt
import os

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

import docs
import staffing as St
import world as Wd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, 'target')
U = Wd.U
NAME = {s[0]: s[1] for s in Wd.SCHOOLS}
BASE = {'ARC': 'Ardcorrie Base', 'BAL': 'Balmorran Base', 'GLW': 'Glenwhinnie Base', 'KIL': 'Kilbraith Base',
        'LOC': 'Lochbrannie Campus Base', 'MUI': 'Muirlees Base', 'TOR': 'Torranbrae Base'}
SUBJECTS = ['English', 'Science', 'Social Subjects', 'French', 'Spanish', 'PE', 'Art and Design', 'Music', 'Technical',
            'Computing Science', 'RMPS', 'Drama', 'Home Economics', 'PSE', 'Business']
REASONS = ['Disruption', 'Refusal to work', 'Dysregulated', 'Conflict with peer', 'Defiance', 'Disruption']
END = dt.date(2026, 6, 26)
STAMP = (2026, 6, 15, 9, 30, 0)
OWNER = 'Aimee Williams'


def wcsv(df, name, crlf=False):
    df.to_csv(os.path.join(T, name), index=False, lineterminator='\r\n' if crlf else '\n')


def write_parquet(df, path):
    tbl = pa.Table.from_pandas(df, preserve_index=False).replace_schema_metadata(None)
    pq.write_table(tbl, path, compression='snappy', version='2.6')
    b = open(path, 'rb').read()
    flen = int.from_bytes(b[-8:-4], 'little')
    foot = b[-8 - flen:-8]
    i = foot.find(b'parquet-cpp-arrow version')
    new = b'parquet-mr version 1.12.3 (build f8dced182c4c1fbdec6ccb3185537b5a01e6ed6b)'
    foot2 = foot[:i - 1] + bytes([len(new)]) + new + foot[i + foot[i - 1]:]
    open(path, 'wb').write(b[:-8 - flen] + foot2 + len(foot2).to_bytes(4, 'little') + b'PAR1')


def write_xlsx(path, sheets, created, modified):
    with pd.ExcelWriter(path, engine='openpyxl') as xw:
        for name, df in sheets:
            df.to_excel(xw, sheet_name=name, index=False)
            ws = xw.sheets[name]
            for col in ws.columns:
                width = max(len(str(c.value)) if c.value is not None else 0 for c in col)
                ws.column_dimensions[col[0].column_letter].width = min(48, max(9, width + 2))
            ws.freeze_panes = 'A2'
    docs.scrub_xlsx(path, OWNER, created, modified, STAMP)


def yn(x):
    return np.where(x, 'Y', 'N')


def ddmmyyyy(d):
    return d.strftime('%d/%m/%Y') if d is not None else ''


# ------------------------------------------------------------------------------------------------ dates on the roll
def roll_dates(o, rng):
    """join dates for late joiners (after the third unit's homework was set) and leaving dates for leavers"""
    weeks, tw = o['weeks'], o['tweek']
    pp = o['pp']
    join = [None] * o['N']
    left = [None] * o['N']
    for i in range(o['N']):
        if pp['joined_late'].iloc[i]:
            join[i] = weeks[tw[2]] + dt.timedelta(days=7 + int(rng.integers(0, 5)))
        if pp['left'].iloc[i]:
            left[i] = weeks[tw[8]] + dt.timedelta(days=int(rng.integers(0, 70)))
    return join, left


def school_day(d, year=2026):
    while d.weekday() > 4 or any(a <= d <= b for a, b in Wd.HOLIDAYS[year]):
        d += dt.timedelta(days=1)
    return d


def on_roll(join, left, i, d):
    return (join[i] is None or d >= join[i]) and (left[i] is None or d < left[i])


# ------------------------------------------------------------------------------------------------ rolls
def roll_2026(w, o, st, join, left):
    pp = o['pp']
    refs = st.removals.groupby('scn').size()
    p7 = pp['p7_numeracy'].values
    df = pd.DataFrame({
        'SCN': pp['scn'].values, 'MIS_Ref': pp['mis_ref'].values, 'Forename': pp['forename'].values,
        'Surname': pp['surname'].values, 'School': pp['school'].map(NAME).values, 'Stage': pp['yg'].values,
        'Maths_Class': pp['maths_class'].values, 'Sex': pp['sex'].values, 'FSM': yn(pp['fsm'].values),
        'ASN': yn(pp['asn'].values), 'EAL': yn(pp['eal'].values), 'SIMD_Decile': pp['simd'].values,
        'P7_Numeracy_SS': [('' if np.isnan(x) else str(int(x))) for x in p7],
        'Glow_ID': ['gw%08d' % (St.hh('g' + s, 7) % 90000000 + 10000000) for s in pp['scn']],
        'Date_Joined': [d.isoformat() if d else '' for d in join],
        'Date_Left': [d.isoformat() if d else '' for d in left],
        'Base_Referrals': [int(refs.get(s, 0)) for s in pp['scn']]})
    df['_k'] = pp['school'].map({c: i for i, c in enumerate(Wd.SCODES)}).values
    df = df.sort_values(['_k', 'Stage', 'Surname', 'Forename', 'SCN']).drop(columns='_k')
    wcsv(df, 'pupil_roll_extract_2026-06-12.csv')
    return df


def roll_2025(w, o, join, left):
    pp = o['pp']
    p7 = pp['p7_numeracy'].values
    df = pd.DataFrame({
        'Candidate No': pp['scn'].values, 'Pupil Ref': pp['mis_ref'].values,
        'Pupil Name': [s.upper() + ', ' + f for s, f in zip(pp['surname'], pp['forename'])],
        'Establishment': pp['school'].map(NAME).values, 'Year': pp['yg'].values, 'Maths Set': pp['maths_class'].values,
        'Gender': pp['sex'].values, 'FME': np.where(pp['fsm'].values, 'Yes', ''), 'ASN': np.where(pp['asn'].values, 'Yes', ''),
        'EAL': np.where(pp['eal'].values, 'Yes', ''), 'SIMD': pp['simd'].values,
        'P7 Numeracy': [('' if np.isnan(x) else str(int(x))) for x in p7],
        'Start Date': [ddmmyyyy(d) if d else '' for d in join],
        'Leaving Date': [ddmmyyyy(d) if d else '' for d in left]})
    df = df.sort_values(['Establishment', 'Year', 'Pupil Name', 'Candidate No'])
    wcsv(df, 'pupil_roll_2024-25.csv', crlf=True)
    return df


# ------------------------------------------------------------------------------------------------ the June papers
def item_order(w):
    """question numbers on each year group's paper: (topic, item) pairs in the paper's own order"""
    r = np.random.default_rng(w.seed * 17 + 3)
    return {g: r.permutation(U * 3) for g in Wd.YG}


def marks_2025(w, o, order):
    pp = o['pp']
    keep = ~pp['left'].values
    rows = {'Pupil Ref': pp['mis_ref'].values[keep], 'Year': pp['yg'].values[keep],
            'Attendance': np.where(o['sat'][keep], 'P', 'A')}
    idx = np.where(keep)[0]
    ygi = o['ygi'][idx]
    for q in range(U * 3):
        col = []
        for n, i in enumerate(idx):
            pair = order[Wd.YG[ygi[n]]][q]
            col.append(str(int(o['marks'][i, pair // 3, pair % 3])) if o['sat'][i] else '')
        rows['Q%02d' % (q + 1)] = col
    df = pd.DataFrame(rows).sort_values(['Year', 'Pupil Ref'])
    wcsv(df, 'june_common_paper_marks_2025.csv', crlf=True)
    return df


def marks_2026(w, o, order):
    pp = o['pp']
    idx = np.where(~pp['left'].values)[0]
    scn = np.repeat(pp['scn'].values[idx], U * 3)
    yg = np.repeat(pp['yg'].values[idx], U * 3)
    qn = np.tile(np.arange(1, U * 3 + 1), len(idx))
    ygi = o['ygi'][idx]
    ordm = np.stack([order[g] for g in Wd.YG])[ygi]            # (n, 36) pair index of each question
    mk = o['marks'][idx].reshape(len(idx), U * 3)
    val = np.take_along_axis(mk, ordm, axis=1).reshape(-1)
    sat = np.repeat(o['sat'][idx], U * 3)
    df = pd.DataFrame({'SCN': scn, 'Stage': yg, 'Question': ['Q%d' % q for q in qn],
                       'Mark': pd.array(np.where(sat, val, 0), dtype='Int64'),
                       'Status': np.where(sat, 'Present', 'Absent')})
    df.loc[~sat, 'Mark'] = pd.NA
    df = df.sort_values(['Stage', 'SCN'], kind='stable')
    wcsv(df, 'june_common_paper_marks_2026.csv')
    return df


def paper_map(w, order):
    sheets = []
    for g in Wd.YG:
        rows = []
        for q in range(U * 3):
            pair = order[g][q]
            t, k = pair // 3, pair % 3
            rows.append(dict(Question='Q%02d' % (q + 1), Marks=Wd.ITEM_MAX[k], Topic=Wd.TOPICS[g][t],
                             **{'Unit 2024-25': w.old_unit[g][t], 'Unit 2025-26': w.mb_unit[g][t]}))
        sheets.append((g + ' paper', pd.DataFrame(rows)))
    sk = []
    for g in Wd.YG:
        for t in range(U):
            for k in range(3):
                sk.append({'Corvella skill': w.cv_skill[g][t][k], 'Stage': g, 'Unit 2024-25': w.old_unit[g][t],
                           'Topic': Wd.TOPICS[g][t]})
    sheets.append(('Corvella skills', pd.DataFrame(sk)))
    write_xlsx(os.path.join(T, 'common_paper_and_unit_map.xlsx'), sheets, '2025-06-20T10:02:00Z', '2025-08-11T14:40:00Z')


# ------------------------------------------------------------------------------------------------ homework platforms
def _k0(o):
    return np.round(np.nan_to_num(o['acc0'], nan=0.0) * 10).astype(int)


def corvella(w, o, join, left, rng):
    pp = o['pp']
    N = o['N']
    ygi = o['ygi']
    k0 = _k0(o)
    cls = pp['maths_class'].values
    ref = pp['mis_ref'].values
    cv = np.array([[w.cv_skill[g][t][k] for t in range(U) for k in range(3)] for g in Wd.YG])
    parts = []
    for t in range(U):
        d0 = o['weeks'][o['tweek'][t]]
        dset = [school_day(d0 + dt.timedelta(days=int(St.hh(pp['school'].iloc[i] + cls[i] + str(t), 4) % 3)), 2025)
                for i in range(N)]
        keep = np.array([on_roll(join, left, i, dset[i]) for i in range(N)])
        done = o['done'][:, t]
        sk = pd.Series(cv[ygi, t * 3]) + ';' + pd.Series(cv[ygi, t * 3 + 1]) + ';' + pd.Series(cv[ygi, t * 3 + 2])
        df = pd.DataFrame({'LearnerID': ref, 'Group': cls, 'TaskType': 'Homework',
                           'TaskName': [Wd.TOPICS[Wd.YG[ygi[i]]][t] for i in range(N)],
                           'DateSet': [d.isoformat() for d in dset], 'Skills': sk.values, 'Questions': 10,
                           'CorrectFirstAttempt': pd.array(np.where(done, k0[:, t], 0), dtype='Int64'),
                           'Status': np.where(done, 'Complete', 'Not attempted')})
        df.loc[~done, 'CorrectFirstAttempt'] = pd.NA
        parts.append(df[keep])
    for widx, ent in enumerate(o['rev_topics']):
        if ent is None:
            continue
        q, did = ent
        wk = widx + 3
        d = o['weeks'][wk] + dt.timedelta(days=4)
        keep = np.array([on_roll(join, left, i, d) for i in range(N)])
        sk = pd.Series(cv[ygi, q[:, 0] * 3 + 0])
        for j in range(1, q.shape[1]):
            sk = sk + ';' + pd.Series(cv[ygi, q[:, j] * 3 + j % 3])
        pj = np.clip(np.take_along_axis(o['p0'], q, axis=1) + 0.1, 0, 0.97)
        corr = (rng.random(q.shape) < pj).sum(axis=1)
        df = pd.DataFrame({'LearnerID': ref, 'Group': cls, 'TaskType': 'Retrieval', 'TaskName': 'Weekly retrieval',
                           'DateSet': d.isoformat(), 'Skills': sk.values, 'Questions': q.shape[1],
                           'CorrectFirstAttempt': pd.array(np.where(did, corr, 0), dtype='Int64'),
                           'Status': np.where(did, 'Complete', 'Not attempted')})
        df.loc[~did, 'CorrectFirstAttempt'] = pd.NA
        parts.append(df[keep])
    df = pd.concat(parts, ignore_index=True).sort_values(['LearnerID', 'DateSet', 'TaskType'], kind='stable')
    wcsv(df, 'corvella_homework_export_2024-25.csv')
    return df


def mathsbridge(w, o, roll, join, left, rng):
    pp = o['pp']
    N = o['N']
    ygi = o['ygi']
    k0 = _k0(o)
    glow = dict(zip(roll['SCN'], roll['Glow_ID']))
    gid = np.array([glow[s] for s in pp['scn']])
    ccode_spr = (pp['school'] + '-' + pp['maths_class']).values
    ccode_aut = (pp['school'] + '-' + pp['maths_class_aut']).values
    mb = np.array([[w.mb_unit[g][t] for t in range(U)] for g in Wd.YG])
    parts = []
    for t in range(U):
        d0 = o['weeks'][o['tweek'][t]]
        cset = ccode_aut if d0 < Wd.SPRING_WEEK else ccode_spr
        dset = [school_day(d0 + dt.timedelta(days=int(St.hh(cset[i] + str(t), 4) % 3))) for i in range(N)]
        ccode = ccode_spr
        keep = np.array([on_roll(join, left, i, dset[i]) for i in range(N)])
        done = o['done'][:, t]
        df = pd.DataFrame({'glow_id': gid, 'class_code': ccode, 'task_kind': 'Unit',
                           'task_code': ['MB-' + u + '-H' for u in mb[ygi, t]], 'set_on': [d.isoformat() for d in dset],
                           'units': mb[ygi, t], 'n_questions': 10,
                           'score_pct': np.where(done, k0[:, t] * 10.0, np.nan),
                           'status': np.where(done, 'Completed', 'Not started')})
        parts.append(df[keep])
    for widx, ent in enumerate(o['rev_topics']):
        if ent is None:
            continue
        q, did = ent
        wk = widx + 3
        d = o['weeks'][wk] + dt.timedelta(days=3)
        if o['weeks'][wk] == Wd.SPRING_WEEK:
            d = Wd.SPLIT_FROM        # the first review of the spring term goes out on its first day
        ccode = ccode_spr
        keep = np.array([on_roll(join, left, i, d) for i in range(N)])
        un = pd.Series(mb[ygi, q[:, 0]]) + ';' + pd.Series(mb[ygi, q[:, 2]]) + ';' + pd.Series(mb[ygi, q[:, 4]])
        pj = np.clip(np.take_along_axis(o['p0'], q, axis=1) + 0.1, 0, 0.97)
        corr = (rng.random(q.shape) < pj).sum(axis=1)
        df = pd.DataFrame({'glow_id': gid, 'class_code': ccode, 'task_kind': 'Review',
                           'task_code': 'MB-REV-W%02d' % (wk + 1), 'set_on': d.isoformat(), 'units': un.values,
                           'n_questions': q.shape[1],
                           'score_pct': np.where(did, np.round(100.0 * corr / q.shape[1]), np.nan),
                           'status': np.where(did, 'Completed', 'Not started')})
        parts.append(df[keep])
    df = pd.concat(parts, ignore_index=True).sort_values(['class_code', 'glow_id', 'set_on', 'task_kind'], kind='stable')
    write_parquet(df.reset_index(drop=True), os.path.join(T, 'mathsbridge_homework_export_2025-26.parquet'))
    return df


# ------------------------------------------------------------------------------------------------ staffing files
TITLES_F = ['Mrs', 'Mrs', 'Ms', 'Ms', 'Miss', 'Mrs', 'Dr']


def styled(fn, sn, fem, key):
    t = TITLES_F[St.hh(key, 5) % len(TITLES_F)] if fem else ('Dr' if St.hh(key, 5) % 23 == 0 else 'Mr')
    return '%s %s. %s' % (t, fn[0], sn)


def staff_codes(st):
    """every (school, post) code and person by phase; job-share posts carry one code; the shared posts from January"""
    rek = {s[0]: s[4] for s in Wd.SCHOOLS}
    out = []  # (phase, school, code, forename, surname, fem, post)
    used = {c: set() for c in Wd.SCODES}
    for (c, post), code in sorted(st.old_code.items()):
        p = st.people[(st.people['school'] == c) & (st.people['post'] == post)].iloc[0]
        a = st.stale.get((c, post), dict(forename=p['forename'], surname=p['surname'], fem=bool(p['fem'])))
        out.append(('autumn', c, code, a['forename'], a['surname'], bool(a['fem']), post))
        if st.replaced.get(c) == post:
            p = st.extra[c]
            p = dict(forename=p['forename'], surname=p['surname'], fem=p['fem'])
        else:
            p = dict(forename=p['forename'], surname=st.renamed.get((c, post), p['surname']), fem=bool(p['fem']))
        if rek[c]:
            nc = (p['forename'][0] + p['surname'][:2]).upper()
            while nc in used[c]:
                nc = nc[:2] + chr(ord(nc[2]) + 1) if nc[2] < 'Z' else nc + '2'
            used[c].add(nc)
        else:
            nc = code
        out.append(('spring', c, nc, p['forename'], p['surname'], p['fem'], post))
    for key, pair in (('SH1', ('KIL', 'TOR')), ('SH2', ('GLW', 'MUI'))):
        p = st.extra[key]
        for c in pair:
            if rek[c]:
                nc = (p['forename'][0] + p['surname'][:2]).upper()
                while nc in used[c]:
                    nc = nc[:2] + chr(ord(nc[2]) + 1)
                used[c].add(nc)
            else:
                nc = 'T%04d' % (St.hh(key + c, 6) % 9000 + 1000)
            out.append(('spring', c, nc, p['forename'], p['surname'], p['fem'], key))
    return pd.DataFrame(out, columns=['phase', 'school', 'code', 'forename', 'surname', 'fem', 'post'])


def timetable(st, codes):
    slots = st.maths_slots()
    sl = {(r['school'], r['yg'], r['maths_class'], r['phase']): r['slots'] for _, r in slots.iterrows()}
    cd = {(r['phase'], r['school'], r['post']): r['code'] for _, r in codes.iterrows()}
    shared = {'KIL': 'SH1', 'TOR': 'SH1', 'GLW': 'SH2', 'MUI': 'SH2'}
    split = set(st.split_classes)
    rows = []
    for _, r in st.cls.iterrows():
        c, g, k, post = r['school'], r['yg'], r['maths_class'], r['post']
        room = 'M%d' % (St.hh(c + g + k, 4) % 7 + 1)
        aut = [(d, p, cd[('autumn', c, post)]) for d, p in sl[(c, g, k, 'autumn')]]
        spr_slots = sl[(c, g, k, 'spring')]
        spr = []
        sh_pick = set()
        if (c, g, k) in split:
            order = sorted(range(4), key=lambda j: St.hh(c + g + k + str(j), 6))
            sh_pick = set(order[:2])
        for j, (d, p) in enumerate(spr_slots):
            code = cd[('spring', c, shared[c])] if j in sh_pick else cd[('spring', c, post)]
            spr.append((d, p, code))
        if aut == spr:
            for d, p, code in aut:
                rows.append((c, k, d, p, code, room, '18/08/2025', '26/06/2026'))
        else:
            for d, p, code in aut:
                rows.append((c, k, d, p, code, room, '18/08/2025', '19/12/2025'))
            for d, p, code in spr:
                rows.append((c, k, d, p, code, room, '06/01/2026', '26/06/2026'))
    df = pd.DataFrame(rows, columns=['School', 'Class', 'Day', 'Period', 'Staff', 'Room', 'Valid_From', 'Valid_To'])
    df['School'] = df['School'].map(NAME)
    df['Day'] = df['Day'].map(dict(enumerate(St.DAYS)))
    df.insert(4, 'Subject', 'Mathematics')
    df = df.sort_values(['School', 'Class', 'Valid_From', 'Day', 'Period'], kind='stable')
    wcsv(df, 'maths_timetable_2025-26.csv')
    return df


def staff_list(st, codes):
    rek = {s[0]: s[4] for s in Wd.SCHOOLS}
    sheets = []
    for phase, label in (('autumn', 'Autumn 2025'), ('spring', 'Spring 2026')):
        sub = codes[codes['phase'] == phase].drop_duplicates(['school', 'code'])
        rows = []
        for _, r in sub.iterrows():
            if phase == 'spring' and rek[r['school']]:
                name = r['forename'] + ' ' + r['surname']
            else:
                name = styled(r['forename'], r['surname'], r['fem'], r['forename'] + r['surname'])
            rows.append(dict(School=NAME[r['school']], Code=r['code'], Name=name, Department='Mathematics'))
        df = pd.DataFrame(rows).sort_values(['School', 'Code'])
        sheets.append((label, df))
    write_xlsx(os.path.join(T, 'timetable_staff_codes_2025-26.xlsx'), sheets, '2025-08-14T08:55:00Z', '2026-01-08T16:21:00Z')


def establishment(st, rng):
    rows = []
    for c in Wd.SCODES:
        sub = st.people[st.people['school'] == c]
        posts = sorted(sub['post'].unique())
        for n, post in enumerate(posts):
            title = 'Principal Teacher Mathematics' if n == 0 else 'Teacher of Mathematics'
            hold = sub[sub['post'] == post]
            fte = 1.0 / len(hold)
            for _, p in hold.iterrows():
                start = dt.date(2008 + int(St.hh(p['forename'] + p['surname'], 5) % 17), 8, 1 + int(St.hh(p['surname'], 3) % 20))
                if (c, post) in st.stale:
                    start = dt.date(2025, 8, 18)
                end = ''
                if st.replaced.get(c) == post:
                    end = '19/12/2025'
                sn = st.renamed.get((c, post), p['surname'])
                rows.append(dict(Post_Ref='MA-%s-%02d' % (St.hh(c, 4) % 90 + 10, n + 1), School=NAME[c], Post_Title=title,
                                 FTE=round(fte, 1), Holder=sn.upper() + ', ' + p['forename'],
                                 In_Post_From=ddmmyyyy(start), In_Post_To=end))
            if st.replaced.get(c) == post:
                e = st.extra[c]
                rows.append(dict(Post_Ref='MA-%s-%02d' % (St.hh(c, 4) % 90 + 10, n + 1), School=NAME[c], Post_Title=title,
                                 FTE=1.0, Holder=e['surname'].upper() + ', ' + e['forename'], In_Post_From='06/01/2026',
                                 In_Post_To=''))
    for key, pair, ref in (('SH1', ('KIL', 'TOR'), 'MA-SH-01'), ('SH2', ('GLW', 'MUI'), 'MA-SH-02')):
        e = st.extra[key]
        rows.append(dict(Post_Ref=ref, School=NAME[pair[0]] + ' / ' + NAME[pair[1]], Post_Title='Teacher of Mathematics (shared)',
                         FTE=1.0, Holder=e['surname'].upper() + ', ' + e['forename'], In_Post_From='06/01/2026', In_Post_To=''))
    df = pd.DataFrame(rows)
    write_xlsx(os.path.join(T, 'maths_staffing_establishment_2025-26.xlsx'), [('Mathematics posts', df)],
               '2025-08-04T11:10:00Z', '2026-01-12T09:47:00Z')
    return df


def bells(st):
    b = st.bells.copy()
    b['School'] = b['school'].map(NAME)
    b['Days'] = b['day_type'].map({'Mon-Thu': 'Monday to Thursday', 'Fri': 'Friday'})
    b['Period'] = b['period']
    b['Start'] = [t.strftime('%H:%M') for t in b['start']]
    b['End'] = [t.strftime('%H:%M') for t in b['end']]
    df = b[['School', 'Days', 'Period', 'Start', 'End']]
    write_xlsx(os.path.join(T, 'bell_times_2025-26.xlsx'), [('Bell times', df)], '2025-06-12T13:20:00Z', '2025-06-12T13:20:00Z')


def signins(st, rng):
    """the bases' kiosk export: a card scan logs the SCN; with no card, base staff type the name and year"""
    w = st.w
    pp = w.sess[2026]['pp'].set_index('scn')
    slots = st.maths_slots()
    sl = {(r['school'], r['yg'], r['maths_class'], r['phase']): set(r['slots']) for _, r in slots.iterrows()}
    bt = {(r['school'], r['day_type'], r['period']): (r['start'], r['end']) for _, r in st.bells.iterrows()}
    staff = {c: [a + b for a, b in zip('KDLJMSRA', 'MRBTHCWF')][St.hh(c, 3) % 6: St.hh(c, 3) % 6 + 3] for c in BASE}
    rows = []
    for _, e in st.removals.iterrows():
        c = e['school']
        base = 'LOC' if c == 'SMO' else c
        d = e['date']
        dtp = 'Fri' if d.weekday() == 4 else 'Mon-Thu'
        s0, _ = bt[(c, dtp, int(e['period']))]
        _, e1 = bt[(c, dtp, int(e['last']))]
        tin = (dt.datetime.combine(d, s0) + dt.timedelta(minutes=int(e['mins_in']))).time()
        single = int(e['last']) == int(e['period'])
        if single and e['u'] < 0.3:
            tout = ''
        else:
            tout = (dt.datetime.combine(d, e1) - dt.timedelta(minutes=1 + int(St.hh(e['scn'] + str(d), 3) % 7))).strftime('%H:%M')
        p = pp.loc[e['scn']]
        if e['card']:
            scn, typed, yr = e['scn'], '', ''
        else:
            nm = p['forename'] + ' ' + p['surname']
            typed = nm.lower() if St.hh(e['scn'] + 'case', 3) % 5 == 0 else nm
            scn, yr = '', p['yg']
        stf = staff[base][St.hh(e['scn'] + str(d) + 's', 3) % len(staff[base])]
        rea = REASONS[St.hh(e['scn'] + str(d) + 'r', 3) % len(REASONS)]
        row = (BASE[base], d.strftime('%d/%m/%Y'), tin.strftime('%H:%M'), tout, scn, typed, yr, rea, stf)
        rows.append(row)
        if e['card'] and rng.random() < 0.02:
            rows.append(row)
    # the bases serve the whole school: S4 to S6 pupils' sign-ins sit in the same export (no S1 to S3 roll entry)
    from faker import Faker
    fk = Faker('en_GB')
    fk.seed_instance(w.seed * 31 + 21)
    days = Wd.school_days(Wd.BASES_OPEN, Wd.S25['paper'] - dt.timedelta(days=5), 2026)
    for n in range(int(0.55 * len(st.removals))):
        c = Wd.SCODES[int(rng.integers(0, len(Wd.SCODES)))]
        base = 'LOC' if c == 'SMO' else c
        d = days[int(rng.integers(0, len(days)))]
        dtp = 'Fri' if d.weekday() == 4 else 'Mon-Thu'
        per = int(rng.integers(1, 5 if dtp == 'Fri' else 7))
        s0, e1 = bt[(c, dtp, per)]
        tin = (dt.datetime.combine(d, s0) + dt.timedelta(minutes=int(rng.integers(3, 36)))).strftime('%H:%M')
        tout = '' if rng.random() < 0.2 else (dt.datetime.combine(d, e1) - dt.timedelta(minutes=int(rng.integers(1, 8)))).strftime('%H:%M')
        yr = ['S4', 'S5', 'S6'][int(rng.integers(0, 3))]
        if rng.random() < 0.87:
            scn, typed, ytyp = str(int(rng.integers(100000000, 199999999))), '', ''
        else:
            scn, typed, ytyp = '', (fk.first_name() + ' ' + fk.last_name()), yr
        rows.append((BASE[base], d.strftime('%d/%m/%Y'), tin, tout, scn, typed, ytyp,
                     REASONS[int(rng.integers(0, len(REASONS)))], staff[base][int(rng.integers(0, len(staff[base])))]))
    rows.sort(key=lambda r: (r[1][6:] + r[1][3:5] + r[1][:2], r[2], r[0]))
    df = pd.DataFrame(rows, columns=['Base', 'Date', 'Time_In', 'Time_Out', 'SCN', 'Name_Typed', 'Year_Typed',
                                     'Reason', 'Staff'])
    wcsv(df, 'support_base_signins_2025-11-03_to_2026-05-29.csv')
    return df


# ------------------------------------------------------------------------------------------------ distractors
def attendance(w, rng):
    rows = []
    for year, months in ((2025, [(2024, m) for m in range(8, 13)] + [(2025, m) for m in range(1, 7)]),
                         (2026, [(2025, m) for m in range(8, 13)] + [(2026, m) for m in range(1, 7)])):
        for c in Wd.SCODES:
            base = 92.4 + (St.hh(c, 4) % 30) / 10.0 - 1.5
            for g in Wd.YG:
                for (y, m) in months:
                    seas = {8: 1.2, 9: 0.6, 10: 0.1, 11: -0.4, 12: -1.6, 1: -1.1, 2: -0.6, 3: -0.3, 4: 0.0, 5: -0.2, 6: -1.9}[m]
                    v = base + seas - 0.9 * Wd.YG.index(g) + rng.normal(0, 0.45)
                    poss = int(rng.integers(3600, 5200)) if m not in (8, 6) else int(rng.integers(900, 2400))
                    rows.append(dict(Session='%d-%02d' % (year - 1, year % 100), Month='%d-%02d' % (y, m), School=NAME[c],
                                     Stage=g, Possible_Half_Days=poss, Attendance_Pct=round(v, 1)))
    wcsv(pd.DataFrame(rows), 'attendance_by_month_2024-25_2025-26.csv')


def survey(w, rng):
    items = ['I complete my maths homework most weeks', 'My maths homework is about the right length',
             'I know where to get help with my maths homework', 'The homework website is easy to use',
             'I feel confident in maths']
    lift = [3.0, 4.0, 0.5, 6.0, -0.5]
    rows = []
    for c in Wd.SCODES:
        for g in Wd.YG:
            n5, n6 = int(rng.integers(70, 160)), int(rng.integers(70, 160))
            for it, lf in zip(items, lift):
                a = 58 + rng.normal(0, 6)
                rows.append({'School': NAME[c], 'Stage': g, 'Statement': it, 'Responses 2025': n5,
                             'Agree % 2025': round(a, 0), 'Responses 2026': n6,
                             'Agree % 2026': round(a + lf + rng.normal(0, 3), 0)})
    write_xlsx(os.path.join(T, 'pupil_homework_survey_2025_2026.xlsx'), [('Survey results', pd.DataFrame(rows))],
               '2026-04-02T10:15:00Z', '2026-04-20T15:03:00Z')


# ------------------------------------------------------------------------------------------------ documents
def change_register(w, st):
    rw = []
    for g in Wd.YG:
        rw.append('%s: %s.' % (g, '; '.join('%s %s' % (w.mb_unit[g][t], Wd.TOPICS[g][t]) for t in w.rewritten[g])))
    sp = {}
    for c, g, k in st.split_classes:
        sp.setdefault(c, []).append(k)
    split_lines = ['%s: %s.' % (NAME[c], ', '.join(sorted(v))) for c, v in sorted(sp.items(), key=lambda kv: Wd.SCODES.index(kv[0]))]
    blocks = [
        ('title', 'S1 to S3 Mathematics: change register, session 2025-26'),
        ('sub', 'Strathcorrie Council Education Service, Performance and Improvement. Kept by Aimee Williams, Performance '
                'and Improvement Lead. Last updated 15 June 2026.'),
        ('h', '1. Purpose'),
        ('p', 'This register records each change the Education Service made to S1 to S3 mathematics for session 2025-26: '
              'what changed, the date it took effect and the pupils it reached. It is the starting point for the review of '
              'the June 2026 common papers that the Education Committee asked for at its meeting on 9 June 2026.'),
        ('h', '2. Remit for the review'),
        ('p', 'Every S1, S2 and S3 pupil sits the council\'s common June paper for their year group. The June 2026 papers '
              'were the same papers as June 2025, marked to the same scheme, each out of 60 marks. For each change in this '
              'register the review is to report the marks the change cost in the June 2026 papers: the total, over the S1 '
              'to S3 pupils who sat a June 2026 paper and whom the change reached, of the marks those pupils lost because '
              'the change was made. The committee will recommend that the 2027-28 budget, set in February 2027, reverses '
              'the change that cost the most marks.'),
        ('h', '3. Changes'),
        ('table', [['Ref', 'Change', 'In force from', 'Pupils reached'],
                   ['A', 'New BGE mathematics framework (the Strathcorrie Mathematics Pathway) in place of the 2019 course '
                         'plans. Every unit recoded; four units in each year group rewritten from scratch (section 4), the '
                         'rest carried over.', '18 August 2025', 'All S1 to S3 pupils'],
                   ['B', 'Homework platform: Mathsbridge in place of Corvella, whose contract ended on 31 July 2025. '
                         'Mathsbridge sets each class a homework on each unit and a weekly review of earlier units. Pupil '
                         'accounts are held against Glow IDs.', '18 August 2025', 'All S1 to S3 pupils'],
                   ['C', 'Asymmetric week in every secondary: 28 periods, six a day Monday to Thursday and four on Friday. '
                         'S3 mathematics from five periods a week to four; S1 and S2 stay at four.', '18 August 2025',
                    'S3 pupils'],
                   ['D', 'Support bases: a pupil whose behaviour disrupts a lesson may be sent to a support base staffed by '
                         'pupil support workers (guidance issued October 2025). Each referral is entered in SEEMiS.',
                    '3 November 2025', 'Pupils referred to a base at least once (Base_Referrals on the pupil roll)'],
                   ['E', 'Shared mathematics posts: one teacher shared between Kilbraith Academy and Torranbrae High '
                         'School and one between Glenwhinnie Academy and Muirlees High School, to cover vacancies; the '
                         'classes in section 5 split between their own teacher and the shared teacher.', '6 January 2026',
                    'Pupils in the split classes']]),
        ('h', '4. Change A: units rewritten from scratch'),
    ] + [('p', x) for x in rw] + [
        ('p', 'Every other unit carried over with its content unchanged and a new code (the unit map gives both codes).'),
        ('h', '5. Change E: classes split from 6 January 2026'),
    ] + [('p', x) for x in split_lines] + [
        ('h', '6. Records held'),
        ('p', 'Pupil rolls for both sessions (SEEMiS); June common paper marks for 2025 and 2026; the Corvella and '
              'Mathsbridge homework exports; the paper and unit map; support base sign-ins; the timetable exports, staff '
              'codes and the mathematics staffing establishment; monthly attendance; the pupil homework survey.'),
    ]
    docs.write_docx(os.path.join(T, 's1-s3_maths_change_register_2025-26.docx'), blocks, OWNER, STAMP,
                    '2025-08-20T09:12:00Z')


def base_guidance():
    blocks = [
        ('title', 'Support bases: guidance for school staff'),
        ('sub', 'Strathcorrie Council Education Service. Issued October 2025, for use from 3 November 2025.'),
        ('h', 'What a base is for'),
        ('p', 'A support base gives a pupil whose behaviour is disrupting a lesson a calm place to settle, with a pupil '
              'support worker, so that the lesson can carry on and the pupil can go back to class as soon as they are ready.'),
        ('h', 'Sending a pupil'),
        ('p', 'The class teacher sends the pupil with a referral slip, or calls the base. The school office enters each '
              'referral in SEEMiS by the end of the week.'),
        ('h', 'Signing in and out'),
        ('p', 'The pupil scans their school card at the base kiosk, which records their Scottish Candidate Number and the '
              'time. If the pupil has no card, base staff type the pupil\'s name and year group instead.'),
        ('p', 'A pupil signed in to a base misses each lesson they are signed in for any part of. Base staff sign the pupil '
              'out when they go back to class. A pupil who has not been signed out is taken to have gone back to class at '
              'the next bell.'),
        ('h', 'Follow-up'),
        ('p', 'Pastoral staff review base use each fortnight and contact parents or carers after a third referral in a '
              'term. A pupil should not spend more than half a day in a base without a plan agreed with their guidance '
              'teacher.'),
    ]
    docs.write_pdf(os.path.join(T, 'support_base_guidance_2025-10.pdf'), 'Support bases: guidance for school staff',
                   'Elliot Davies', blocks, '20251020093000Z')


# ------------------------------------------------------------------------------------------------ all
def write_all(w, st):
    os.makedirs(T, exist_ok=True)
    for f in os.listdir(T):
        os.remove(os.path.join(T, f))
    rng = np.random.default_rng(w.seed + 77)
    o5, o6 = w.sess[2025], w.sess[2026]
    j5, l5 = roll_dates(o5, rng)
    j6, l6 = roll_dates(o6, rng)
    roll6 = roll_2026(w, o6, st, j6, l6)
    roll_2025(w, o5, j5, l5)
    order = item_order(w)
    marks_2025(w, o5, order)
    marks_2026(w, o6, order)
    paper_map(w, order)
    corvella(w, o5, j5, l5, rng)
    mathsbridge(w, o6, roll6, j6, l6, rng)
    codes = staff_codes(st)
    timetable(st, codes)
    staff_list(st, codes)
    establishment(st, rng)
    bells(st)
    signins(st, rng)
    attendance(w, rng)
    survey(w, rng)
    change_register(w, st)
    base_guidance()
    return dict(order=order, codes=codes)


if __name__ == '__main__':
    import time
    t0 = time.time()
    w = Wd.World()
    st = St.Staffing(w)
    write_all(w, st)
    print('pack %.1fs' % (time.time() - t0))
    for f in sorted(os.listdir(T)):
        print('%-55s %10d' % (f, os.path.getsize(os.path.join(T, f))))
