"""task401 checks: every assertion the design note stands on (the five go/no-go screens and the coordinator's readers,
the semantic fork table SF1 to SF11 and the ask forks AF1 to AF7, the separation line, the readability screen, the
input gates and the ask ceiling), run on the shipped seed and the shipped files at every build. Exit 1 on a failure."""
import json
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

import ceiling as CE
import golden as G
import readers as R
import screens as S
import staffing as St
import world as Wd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = G.T
FAILS = []
NAME = {s[0]: s[1] for s in Wd.SCHOOLS}


def ok(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        FAILS.append(msg)


def doc_text(path):
    if path.endswith('.docx'):
        z = zipfile.ZipFile(path)
        return re.sub(r'<[^>]+>', ' ', z.read('word/document.xml').decode('utf8'))
    if path.endswith('.pdf'):
        from pypdf import PdfReader
        return ' '.join(p.extract_text() for p in PdfReader(path).pages)
    if path.endswith('.xlsx'):
        return ' '.join(' '.join(map(str, df.columns)) + ' ' + ' '.join(map(str, df.head(400).values.ravel()))
                        for df in pd.read_excel(path, sheet_name=None).values())
    if path.endswith('.csv'):
        return open(path).read(20000)
    if path.endswith('.parquet'):
        return ' '.join(pd.read_parquet(path).columns)
    return ''


def literal_classes_by_day():
    """AF7's literal executor, written apart from golden.py: walk every school day of the session; on each, every
    timetable row valid that day and meeting that weekday names a code; the code sheet of the term the day falls in
    names a person; the establishment's holder of that name (surname or previous surname, same first initial) who was
    in post that day taught the lesson. A class's teachers are everyone who taught one of its lessons."""
    import datetime as dt
    tt = G.rd('maths_timetable_2025-26.csv')
    xl = os.path.join(T, 'timetable_staff_codes_2025-26.xlsx')
    name = {}
    for term, sheet in (('autumn', 'Autumn 2025'), ('spring', 'Spring 2026')):
        for _, r in pd.read_excel(xl, sheet_name=sheet, dtype=str).iterrows():
            name[term, r['School'], r['Code']] = G.norm_staff(r['Name'])
    est = pd.read_excel(os.path.join(T, 'maths_staffing_establishment_2025-26.xlsx'), dtype=str).fillna('')
    hold, post_of, on_post = {}, {}, {}
    for _, r in est.iterrows():
        sur, fn = r['Holder'].split(', ')
        span = (G.dmy(r['In_Post_From']), G.dmy(r['In_Post_To']))
        post_of[r['Holder']] = r['Post_Ref']
        on_post.setdefault(r['Post_Ref'], []).append((span, r['Holder']))
        for key in {sur.upper(), r['Previous_Surname'].upper()} - {''}:
            for sch in r['School'].split(' / '):
                hold.setdefault((sch, fn[0].upper(), key), []).append((span, r['Holder']))
    rows = {}
    for _, r in tt.iterrows():
        rows.setdefault((r['School'], r['Class']), []).append(
            (G.dmy(r['Valid_From']), G.dmy(r['Valid_To']), r['Day'], int(r['Period']), r['Staff']))
    aut_end = min(G.dmy(x) for x in tt['Valid_To'])
    first, last = min(G.dmy(x) for x in tt['Valid_From']), max(G.dmy(x) for x in tt['Valid_To'])
    days = Wd.school_days(first, last, 2026)
    dn = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
    per, lessons, unnamed = {}, 0, {}
    for key, rr in rows.items():
        ppl = per.setdefault(key, set())
        for d in days:
            term = 'autumn' if d <= aut_end else 'spring'
            for vf, vt, day, p, code in rr:
                if vf <= d <= vt and day == dn[d.weekday()]:
                    named = hold[(key[0],) + name[term, key[0], code]]
                    assert len({h for _, h in named}) == 1, (key, d, p, code, named)
                    who = {h for (a, b), h in named if a <= d and (b is None or b >= d)}
                    ppl |= who
                    lessons += 1
                    if not who:
                        # the sheet names someone no longer in post: the holder of that person's post that day
                        stand = {h for (a, b), h in on_post[post_of[named[0][1]]] if a <= d and (b is None or b >= d)}
                        assert len(stand) == 1, (key, d, code, stand)
                        unnamed.setdefault(key, set()).update(stand)
    return per, lessons, unnamed


def af7(F, st, tr):
    """the classes ask: its literal execution equals the golden and the generating posts school by school, and each
    other reading of the records breaks a shipped fact"""
    per, lessons, unnamed = literal_classes_by_day()
    lit = {}
    for (s, c), ppl in per.items():
        lit[s] = lit.get(s, 0) + int(len(ppl) > 1)
    ok(lit == F['ask_classes'] == tr,
       'AF7: the classes ask executed literally, lesson by lesson (%d lessons: code, the term\'s code sheet, the holder of '
       'that name in post that day) equals the golden and the generating posts school by school %s'
       % (lessons, {s: (lit.get(s), F['ask_classes'].get(s)) for s in sorted(F['ask_classes'])}))
    ok(len(unnamed) > 0 and all(v <= per[k] for k, v in unnamed.items()),
       'AF7: the %d classes whose autumn lessons the code sheet gives to a holder who had left were taught by the holder '
       'in post on that post, already one of the class\'s teachers, so resolving those lessons by the post moves no count'
       % len(unnamed))
    est = pd.read_excel(os.path.join(T, 'maths_staffing_establishment_2025-26.xlsx'), dtype=str).fillna('')
    tt = G.rd('maths_timetable_2025-26.csv')
    first = min(G.dmy(x) for x in tt['Valid_From'])
    # the hand-over reading: every person a code sheet names on a class's code, in post or not
    ho = {}
    for (s, c), ppl in G.class_teachers(in_post=False).items():
        ho[s] = ho.get(s, 0) + int(len(ppl) > 1)
    left = est[est['In_Post_To'] != '']
    early = left[left['In_Post_To'].map(G.dmy) < first]
    ok(len(early) == 3 and set(early['In_Post_To']) == {'15/08/2025'} and
       all(((est['Post_Ref'] == r['Post_Ref']) & (est['In_Post_From'] == first.strftime('%d/%m/%Y'))).sum() == 1
           for _, r in early.iterrows()),
       'AF7: three holders\' last day in post (15/08/2025) falls before the first lesson (%s), each post\'s next holder '
       'starting that day; read as hand-overs they add classes at %s, which the establishment\'s dates rule out'
       % (first.strftime('%d/%m/%Y'), {s: (ho[s], F['ask_classes'][s]) for s in sorted(ho) if ho[s] != F['ask_classes'][s]}))
    diff = {s for s in ho if ho[s] != F['ask_classes'][s]}
    ok(diff == {s for s in early['School']}, 'AF7: the hand-over reading differs from the golden only at the three '
       'schools whose leaver left before the session %s' % sorted(diff))
    # renames: the autumn sheet's surname on the code is the holder's Previous_Surname
    prev = est[est['Previous_Surname'] != '']
    ok(len(prev) == 3, 'AF7: three holders carry a Previous_Surname on the establishment %s'
       % sorted(zip(prev['Holder'], prev['Previous_Surname'])))
    # job-shares: each holder's own code on their own days, so every class of a job-share post shows both codes
    xl = os.path.join(T, 'timetable_staff_codes_2025-26.xlsx')
    aut = pd.read_excel(xl, sheet_name='Autumn 2025', dtype=str)
    half = est[est['FTE'].astype(float) < 1.0]
    js_ok, js_n = True, 0
    for ref, g in half.groupby('Post_Ref'):
        sch = g['School'].iloc[0]
        codes = set()
        for h in g['Holder']:
            sur, fn = h.split(', ')
            hit = [r['Code'] for _, r in aut[aut['School'] == sch].iterrows() if G.norm_staff(r['Name']) == (fn[0].upper(), sur.upper())]
            js_ok &= len(hit) == 1
            codes |= set(hit)
        for cls, gg in tt[(tt['School'] == sch) & tt['Staff'].isin(codes)].groupby('Class'):
            js_n += 1
            js_ok &= set(gg['Staff']) >= codes
    ok(js_ok and half['Post_Ref'].nunique() == 5, 'AF7: five job-share posts, each holder on the code sheets with a code '
       'of their own and every one of the posts\' %d classes showing both holders\' codes' % js_n)
    # every code on the timetable is on its term's sheet; one establishment person per name at a school
    spr = pd.read_excel(xl, sheet_name='Spring 2026', dtype=str)
    have = {('autumn', r['School'], r['Code']) for _, r in aut.iterrows()} | {('spring', r['School'], r['Code']) for _, r in spr.iterrows()}
    aut_end = min(G.dmy(x) for x in tt['Valid_To'])
    need = set()
    for _, r in tt.iterrows():
        if G.dmy(r['Valid_From']) <= aut_end:
            need.add(('autumn', r['School'], r['Staff']))
        if G.dmy(r['Valid_To']) > aut_end:
            need.add(('spring', r['School'], r['Staff']))
    ok(need <= have, 'AF7: every timetable code is on its term\'s code sheet (%d term codes)' % len(need))
    keys = {}
    for _, r in est.iterrows():
        sur, fn = r['Holder'].split(', ')
        for k in {sur.upper(), r['Previous_Surname'].upper()} - {''}:
            for sch in r['School'].split(' / '):
                keys.setdefault((sch, fn[0].upper(), k), set()).add(r['Holder'])
    ok(all(len(v) == 1 for v in keys.values()), 'AF7: at each school a first initial and a surname or previous surname '
       'name one establishment holder')
    ok(len(st.renamed) == 3 and len(st.stale) == 3, 'AF7: the world carries three Christmas name changes and three '
       'summer changes of holder')


def run(F, w=None, st=None):
    w = w or Wd.World()
    st = st or St.Staffing(w)
    # ------------------------------------------------------------------ the golden reproduces from the shipped files
    gw = R.golden(w)
    ok(all(abs(F['costs'][k] - gw[k]) <= 1e-6 * max(1.0, abs(gw[k])) for k in gw),
       'golden costs from target/ equal the world readers golden %s' % {k: round(v) for k, v in F['costs'].items()})
    ok(F['call'] == 'B', 'golden call is the platform switch (B)')
    # ------------------------------------------------------------------ screens on the shipped seed
    sc = S.screen_seed(w.seed)
    ok(sc['truth_top'] == 'B', 'screen 1: truth names B on the shipped seed %s' % sc['truth'])
    ok(sc['top'] == 'B' and sc['margin'] >= 1.5, 'screen 1: golden names B, margin %.2f >= 1.5' % sc['margin'])
    ok(sc['family_all_B'], 'screen 2: all 24 golden-family specifications name B (SF4, SF5, SF6)')
    ok(sc['first_look'] != 'B', 'screen 3: first look files %s' % sc['first_look'])
    ok(sc['careful'] != 'B', 'screen 4: careful reader files %s' % sc['careful'])
    ok(all(c != 'B' for c in sc['interaction']), 'coordinator 1: interaction readers file %s (z %.2f)' % (sc['interaction'], sc['z']))
    ok(all(c[1] != 'B' for c in sc['constructing']), 'coordinator 2: constructing readers file %s' % sc['constructing'])
    ok(all(c != 'B' for c in sc['literal']), 'screen 5: literal executions file %s' % sc['literal'])
    ok(sc['per_pupil_top'] != 'B', 'SF1 open reading (per pupil reached) names %s, so the remit closes it' % sc['per_pupil_top'])
    cheap = [sc['first_look'], sc['careful']] + sc['interaction'] + [c[1] for c in sc['constructing']] + sc['literal']
    ok(sum(c == 'B' for c in cheap) <= 1, 'Gate F: cheap routes landing B on the clean truth: %d of %d' % (sum(c == 'B' for c in cheap), len(cheap)))
    # ------------------------------------------------------------------ the 20 redraws (screens.py, saved)
    s20 = json.load(open(os.path.join(HERE, 'screens20.json')))
    ok(s20['runs'] == 20 and s20['truth_B'] == 20 and s20['golden_B'] == 20, 'redraws: truth and golden name B 20 of 20')
    ok(s20['margin_15'] >= 19 and s20['family_B'] == 20, 'redraws: margin >= 1.5 in %d, family unanimous in %d' % (s20['margin_15'], s20['family_B']))
    ok(s20['first_look_wrong'] == 20 and s20['careful_wrong'] == 20 and s20['literal_wrong'] == 20,
       'redraws: first look, careful reader and literal execution wrong 20 of 20')
    ok(s20['interaction_wrong'] >= 19, 'redraws: interaction readers wrong %d of 20 (z %.1f to %.1f)' % (s20['interaction_wrong'], s20['z_min'], s20['z_max']))
    ok(s20['construct_i_wrong'] == 20 and s20['construct_ii_wrong'] == 20, 'redraws: both constructing readers wrong 20 of 20')
    ok(s20['per_pupil_B'] == 0, 'redraws: the per-pupil reading never names B (SF1 needs the remit, which files it)')
    # ------------------------------------------------------------------ semantic forks on the main call
    reg = doc_text(os.path.join(T, 's1-s3_maths_change_register_2025-26.docx'))
    reg = re.sub(r'\s+', ' ', reg)
    ok('the total, over the S1 to S3 pupils who sat a June 2026 paper and whom the change reached, of the marks those pupils lost'
       in reg, 'SF1 SF2: the remit files the cost as total marks over the sitting pupils reached')
    ok('were the same papers as June 2025' in reg, 'SF11: the remit files the comparison papers')
    sh = {k: v / 60.0 for k, v in F['costs'].items()}
    ok(max(sh, key=sh.get) == F['call'], 'SF3: costs as shares of the paper give the same call')
    si = G.rd('support_base_signins_2025-11-03_to_2026-05-29.csv')
    roll = G.rd('pupil_roll_extract_2026-06-12.csv')
    ev = st.removals.groupby('scn').size()
    ok(all(int(roll.set_index('SCN').loc[s, 'Base_Referrals']) == int(n) for s, n in ev.items()) and
       int(roll['Base_Referrals'].astype(int).sum()) == len(st.removals),
       'SF7: Base_Referrals on the roll equals each pupil\'s S1 to S3 sign-in events (D\'s reach the same either way)')
    # SF8: E's reach read as classes showing two codes on the timetable instead of the register's list
    tt = G.rd('maths_timetable_2025-26.csv')
    two = {(s, c) for (s, c), g in tt.groupby(['School', 'Class']) if g['Staff'].nunique() > 1}
    L = G.load()
    S6, S5 = G.session_arrays(L, 2026), G.session_arrays(L, 2025)
    e5, e6 = G.p7_resid(S5), G.p7_resid(S6)
    m6 = np.array([(s, c) in two for s, c in zip(S6['school'], S6['cls'])])
    cE = -(e6[m6].mean() - e6[~m6].mean()) * m6.sum()
    alt = dict(F['costs'])
    alt['E'] = cE
    ok(max(alt, key=alt.get) == 'B', 'SF8: E\'s reach read off the timetable codes (%d classes) gives E %.0f, call still B' % (len(two), cE))
    prompt = open(os.path.join(TASK, 'prompt.txt')).read()
    ok('36 of 60 or more' in prompt and F['head']['2026']['secure'] == int((S6['total'] >= 36).sum()),
       'SF9: the prompt files 36 of 60 or more, and the share counts 36 itself')
    ok(S6['n'] == F['head']['2026']['sat'] and S5['n'] == F['head']['2025']['sat'], 'SF10: means over the pupils who sat')
    # ------------------------------------------------------------------ asks
    bt = st.base_truth()
    ok({NAME[k]: v for k, v in bt.items()} == F['ask_lessons'] and F['ask_lessons_unresolved'] == 0,
       'ask 1: golden lessons equal the generating events %s' % bt)
    ppc = st.persons_per_class()
    tr = {}
    for (c, g, k), n in ppc.items():
        tr[NAME[c]] = tr.get(NAME[c], 0) + int(n > 1)
    ok(tr == F['ask_classes'], 'ask 2: golden classes equal the generating posts %s' % tr)
    guide = re.sub(r'\s+', ' ', doc_text(os.path.join(T, 'support_base_guidance_2025-10.pdf')))
    ok('misses each lesson they are signed in for any part of' in guide, 'AF2: the guidance files a missed lesson')
    ok('taken to have gone back to class at the next bell' in guide, 'AF3: the guidance files a pupil not signed out')
    bl = G.bells()
    edges = {(s, d): {G.tmin(a) for _, a, _ in v} | {G.tmin(b) for _, _, b in v} for (s, d), v in bl.items()}
    by = roll.set_index('SCN')
    on_bell = 0
    for _, r in si[(si['Time_Out'] != '') & si['SCN'].isin(by.index)].iterrows():
        dd = pd.to_datetime(r['Date'], format='%d/%m/%Y').date()
        k = (by.loc[r['SCN'], 'School'], 'Friday' if dd.weekday() == 4 else 'Monday to Thursday')
        on_bell += G.tmin(r['Time_Out']) in edges[k]
    ok(on_bell == 0, 'AF4: no S1 to S3 sign-out falls on a bell (no zero-length overlap to read two ways)')
    aut, purity = G.autumn_classes(roll, purity=True)
    g_of = dict(zip(roll['SCN'], roll['Glow_ID']))
    pp6 = w.sess[2026]['pp']
    wrong = sum(aut[g_of[s]] != a for s, a in zip(pp6['scn'], pp6['maths_class_aut']) if g_of[s] in aut)
    mv = int((w.sess[2026]['moved'] & w.sess[2026]['removed']).sum())
    ok(wrong == 0 and purity.min() > 0.6,
       'AF5: each pupil\'s autumn class rebuilt from the classmates who shared each week\'s review set: %d wrong of %d, '
       'least group purity %.2f (%d base-referred pupils changed set in January)' % (wrong, len(aut), purity.min(), mv))
    mbc = pd.read_parquet(os.path.join(T, 'mathsbridge_homework_export_2025-26.parquet'), columns=['glow_id', 'class_code'])
    rc = dict(zip(roll['Glow_ID'], roll['School'].map({v: k for k, v in NAME.items()}) + '-' + roll['Maths_Class']))
    ok(bool((mbc['class_code'] == mbc['glow_id'].map(rc)).all()),
       'AF5: the platform\'s class_code repeats the roll\'s June class on every row (no record states the autumn class)')
    af7(F, st, tr)
    # ------------------------------------------------------------------ the ask ceiling on the cut pack
    rows = CE.sheet(F)
    p1 = CE.pair(rows, ('full_includer', 'full_includer'), ('full_includer', 'full_includer'))
    p0 = CE.pair(rows, ('cracker', 'cracker'), ('cracker', 'cracker'))
    fi = rows[('lessons', 'full_includer')][1] + rows[('classes', 'full_includer')][1]
    ok(fi <= 6, 'ceiling: the full includer keeps %d of 16 ask figures (<= 6, two fifths)' % fi)
    ok(p0['Lc'] <= 0.4, 'ceiling: the cracker keeps %.2f of the ask figures (<= 0.40)' % p0['Lc'])
    ok(p1['pair'] <= 60, 'ceiling: pair with the full includer on the call and the full includer off it %.1f (<= 60)' % p1['pair'])
    both = (45 + 55 * p1['Lc'] + 45 + 55 * p1['Lc']) / 2
    print('INFO ceiling: both full includers on the call %.1f; both careful crackers on the call %.1f'
          % (both, 45 + 55 * p0['Lc']))
    # the mirror stops at the most attractive wrong rung of each ask: taken here as whichever wrong route keeps most
    m1 = max(rows[('lessons', r)][1] for r in CE.ROUTES1)
    m2 = max(rows[('classes', r)][1] for r in CE.ROUTES2)
    mirror = m1 + m2
    ok(mirror / 16.0 < 0.5, 'ceiling: the mirror (the most-keeping wrong route on each ask) keeps %d of 16 (%d and %d)'
       % (mirror, m1, m2))
    F['mirror'] = mirror
    F['pair_both_on_call'] = both
    F['ceiling'] = {'%s|%s' % k: v[1] for k, v in rows.items()}
    F['pair'] = dict(careful=p0, full_includer=p1)
    # ------------------------------------------------------------------ readability screen and input gates
    bad = re.compile(r'adaptiv|personali[sz]|tailor|individuali[sz]|own (mistakes|errors|wrong)|got wrong|wrong answers|'
                     r'each pupil\W{0,3}s (mistakes|errors)', re.I)
    hits = [f for f in sorted(os.listdir(T)) if bad.search(doc_text(os.path.join(T, f)))]
    ok(not hits, 'readability: no shipped file describes either platform as adaptive, personalised or built from a pupil\'s errors %s' % hits)
    files = sorted(os.listdir(T))
    ext = {f.rsplit('.', 1)[1] for f in files}
    big = max(sum(1 for _ in open(os.path.join(T, f))) for f in files if f.endswith('.csv'))
    ok(len(files) >= 10 and len(ext) >= 3 and big >= 25000, 'inputs: %d files, %d formats, largest csv %d rows' % (len(files), len(ext), big))
    dash = [f for f in files if ('\u2014' in doc_text(os.path.join(T, f)) or '\u2013' in doc_text(os.path.join(T, f)))]
    ok(not dash, 'no em or en dash in any shipped text %s' % dash)
    ok(F['head']['2026']['mean'] < F['head']['2025']['mean'], 'the fall is real: %.2f to %.2f' % (F['head']['2025']['mean'], F['head']['2026']['mean']))
    # ------------------------------------------------------------------ bins: edge distance of every printed headline and chart figure
    def edge(v, u):
        return u / 2 - abs(v - round(v / u) * u)
    ok('shares are whole per cents' in prompt, 'bins: the prompt grades the two shares in whole per cents')
    sh_edges = {yr: edge(F['head'][yr]['share'], 1.0) for yr in F['head']}
    ok(min(sh_edges.values()) >= 0.25, 'bins: shares at whole per cents clear their edges by %.3f or more (of 0.5) %s'
       % (min(sh_edges.values()), {k: round(v, 3) for k, v in sh_edges.items()}))
    mn_edges = {yr: edge(F['head'][yr]['mean'], 0.1) for yr in F['head']}
    ok(min(mn_edges.values()) >= 0.03, 'bins: council means clear their 0.1 edges by %.4f or more' % min(mn_edges.values()))
    ch = sorted((edge(m, 0.1), s, yr) for s, v in F['by_school'].items() for yr, m in v.items())
    print('INFO bins: tightest chart means %s' % [(round(e, 4), s, yr) for e, s, yr in ch[:3]])
    # the chart means are exact arithmetic on a population with one reading, so a tight edge cannot be crossed by a
    # defensible reading: every pupil who sat is on the session's roll once, sat whole papers, and keeps one school
    r5 = pd.read_csv(os.path.join(T, 'pupil_roll_2024-25.csv'), dtype=str)
    r6 = pd.read_csv([os.path.join(T, f) for f in sorted(os.listdir(T)) if f.startswith('pupil_roll_extract_')][0], dtype=str)
    m25 = pd.read_csv(os.path.join(T, 'june_common_paper_marks_2025.csv'), dtype=str)
    m26 = pd.read_csv(os.path.join(T, 'june_common_paper_marks_2026.csv'), dtype=str)
    st26 = m26.groupby('SCN')['Status'].nunique()
    both = r5.merge(r6, left_on='Pupil Ref', right_on='MIS_Ref')
    sat5 = set(m25.loc[m25['Attendance'] == 'P', 'Pupil Ref'])
    sat6 = set(m26.loc[m26['Status'] == 'Present', 'SCN'])
    ok(not r5['Pupil Ref'].duplicated().any() and not r6['SCN'].duplicated().any() and not m25['Pupil Ref'].duplicated().any()
       and not m26.duplicated(['SCN', 'Question']).any(), 'bins: one row per pupil on each roll and each paper')
    ok(int(st26.max()) == 1, 'bins: every 2026 pupil is wholly present or wholly absent')
    ok(sat5 <= set(r5['Pupil Ref']) and sat6 <= set(r6['SCN']), 'bins: every pupil who sat is on that session\'s roll')
    ok(int((both['Establishment'] != both['School']).sum()) == 0, 'bins: no pupil on both rolls changes school')
    ok(r5.loc[r5['Pupil Ref'].isin(sat5), 'Leaving Date'].isna().all() and r6.loc[r6['SCN'].isin(sat6), 'Date_Left'].isna().all(),
       'bins: no pupil who sat carries a leaving date')
    return FAILS


if __name__ == '__main__':
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    f = run(F)
    print('checks: %d failed' % len(f))
    sys.exit(1 if f else 0)
