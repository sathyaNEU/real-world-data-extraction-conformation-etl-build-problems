"""task401 ask ceiling, measured on the cut pack under target/: each ask's figures under the routes a solver takes
(the no-repair read, the field shortcut, the careful cracker, the full includer who handles every device it can see,
the mirror that stops at the most attractive wrong rung), scored against the golden figure by figure (whole numbers:
a hit is the exact figure). Prints the sheet and returns it for checks.py and the design note's ask sheet.
The full includer notices every device a record or the hygiene battery surfaces and applies the natural repair:
typed names matched council-wide, own school, each school's bells, the timetable valid on the day, the next bell, each
pupil and period once, every name to its holder on the establishment with previous surnames; the platform's class_code
agrees with the roll on each pupil's class, so it keeps that class (the autumn class is recoverable only from which
classmates shared each week's review set, a reconstruction no record performs); and it reads a name change on a code,
with a leaver and a starter on the post, as a hand-over, the repair the Christmas replacements teach, never testing
the leaver's last day in post against the first lesson of the row (three leavers' contracts ended before the session)."""
import datetime as dt
import os

import pandas as pd

import golden as G

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
CAMPUS = {'Lochbrannie Campus Base': 'Lochbrannie High School'}


def _base_school(b):
    if b in CAMPUS:
        return CAMPUS[b]
    town = b.replace(' Base', '')
    roll = G.rd('pupil_roll_extract_2026-06-12.csv')
    return [s for s in sorted(set(roll['School'])) if s.startswith(town)][0]


def lessons(route):
    si = G.rd('support_base_signins_2025-11-03_to_2026-05-29.csv')
    roll = G.rd('pupil_roll_extract_2026-06-12.csv')
    by = roll.set_index('SCN')
    bsch = {b: _base_school(b) for b in sorted(set(si['Base']))}
    if route != 'no_repair':
        si = si.drop_duplicates()
    key = (roll['Forename'] + ' ' + roll['Surname']).str.lower() + '|' + roll['Stage']
    pool = {}
    for k, s, sch in zip(key, roll['SCN'], roll['School']):
        pool.setdefault(k, []).append((s, sch))
    def who(r):
        if r['SCN']:
            return r['SCN']
        if route == 'no_repair':
            return None
        c = pool.get(r['Name_Typed'].lower() + '|' + r['Year_Typed'], [])
        if route == 'cracker_base_scope':
            c = [x for x in c if x[1] == bsch[r['Base']]]
        if len(c) > 1:
            c = [x for x in c if x[1] == bsch[r['Base']] or bsch[r['Base']] in CAMPUS.values()]
        return c[0][0] if len(c) == 1 else None
    si = si.assign(scn=si.apply(who, axis=1))
    si = si[si['scn'].notna() & si['scn'].isin(by.index)]
    tt = G.rd('maths_timetable_2025-26.csv')
    tt['vf'] = pd.to_datetime(tt['Valid_From'], format='%d/%m/%Y').dt.date
    tt['vt'] = pd.to_datetime(tt['Valid_To'], format='%d/%m/%Y').dt.date
    slots = {}
    for _, r in tt.iterrows():
        slots.setdefault((r['School'], r['Class']), []).append((r['vf'], r['vt'], r['Day'], int(r['Period'])))
    bl = G.bells()
    out, seen = {}, set()
    for _, r in si.iterrows():
        scn = r['scn']
        p = by.loc[scn]
        d = dt.datetime.strptime(r['Date'], '%d/%m/%Y').date()
        b = bl[(p['School'], 'Friday' if d.weekday() == 4 else 'Monday to Thursday')]
        p0 = G.period_at(b, G.tmin(r['Time_In']))
        p1 = p0 if not r['Time_Out'] else G.period_at(b, G.tmin(r['Time_Out']), upto=True)
        if route in ('no_repair', 'first_period'):
            p1 = p0
        cls = p['Maths_Class']        # the roll's class, which the platform's class_code repeats on every row
        live = {(dd, pp) for vf, vt, dd, pp in slots[(p['School'], cls)] if vf <= d <= vt or route == 'no_repair'}
        for per in range(p0, p1 + 1):
            maths = (DAYS[d.weekday()], per) in live
            if maths and ((scn, d, per) not in seen or route == 'no_repair'):
                seen.add((scn, d, per))
                out[p['School']] = out.get(p['School'], 0) + 1
    return out


def classes(route):
    """no_repair: each timetable code a teacher; names_exact: each name string on the term's code sheet a teacher;
    cracker: names normalised to initial and surname, no establishment; full_includer: every name to its holder on the
    establishment, previous surnames included, and a name change on a code with a leaver and a starter on the post read
    as a hand-over, the repair the Christmas replacements teach, without testing the leaver's last day against the
    row's first lesson; literal: the same with that test (the golden's route, printed for reference)"""
    if route in ('full_includer', 'literal'):
        per = G.class_teachers(in_post=(route == 'literal'))
    else:
        tt, sh, est, terms = G.staff_tables()
        per = {}
        for _, r in tt.iterrows():
            f, t = G.dmy(r['Valid_From']), G.dmy(r['Valid_To'])
            ppl = per.setdefault((r['School'], r['Class']), set())
            for term, (a, b) in terms.items():
                if max(f, a) > min(t, b):
                    continue
                if route == 'no_repair':
                    ppl.add(r['Staff'])
                    continue
                s = sh[term]
                nm = s[(s['School'] == r['School']) & (s['Code'] == r['Staff'])]['Name'].iloc[0]
                ppl.add(nm if route == 'names_exact' else G.norm_staff(nm))
    out = {}
    for (sch, cls), ppl in per.items():
        out[sch] = out.get(sch, 0) + int(len(ppl) > 1)
    return out


ROUTES1 = ['no_repair', 'first_period', 'cracker_base_scope', 'cracker', 'full_includer']
ROUTES2 = ['no_repair', 'names_exact', 'cracker', 'full_includer']


def sheet(F=None):
    if F is None:
        F = G.run()
    g1, g2 = F['ask_lessons'], F['ask_classes']
    rows = {}
    for r in ROUTES1:
        v = lessons(r)
        rows[('lessons', r)] = (v, sum(int(v.get(s, 0) == g1[s]) for s in g1))
    for r in ROUTES2:
        v = classes(r)
        rows[('classes', r)] = (v, sum(int(v.get(s, 0) == g2[s]) for s in g2))
    return rows


def pair(rows, cracker=('cracker', 'cracker'), miss=('cracker', 'names_exact'), r=5.0):
    lc = (rows[('lessons', cracker[0])][1] + rows[('classes', cracker[1])][1]) / 16.0
    ls = (rows[('lessons', miss[0])][1] + rows[('classes', miss[1])][1]) / 16.0
    C = 38 + 7 + 55 * lc
    S = r + 7 + 55 * ls
    return dict(Lc=lc, Ls=ls, C=C, S=S, pair=(C + S) / 2)


if __name__ == '__main__':
    F = G.run()
    rows = sheet(F)
    for (a, r), (v, hits) in rows.items():
        print('%-8s %-20s hits %d/8  %s' % (a, r, hits, dict(sorted(v.items()))))
    print('golden lessons', dict(sorted(F['ask_lessons'].items())))
    print('golden classes', dict(sorted(F['ask_classes'].items())))
    for cr in (('cracker', 'cracker'), ('full_includer', 'full_includer')):
        for ms in (('cracker', 'names_exact'), ('cracker', 'cracker'), ('full_includer', 'full_includer')):
            print(cr, ms, {k: round(v, 3) for k, v in pair(rows, cr, ms).items()})
