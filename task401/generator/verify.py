"""task401 verify: an independent recompute of the graded figures from target/ with its own code (standard library csv,
no golden.py import): the headline means and shares, each school's mean, and both asks. Exit 1 on any mismatch with
figures.json."""
import csv
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import openpyxl
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(os.path.dirname(HERE), 'target')


def rows(name):
    with open(os.path.join(T, name), newline='') as f:
        return list(csv.DictReader(f))


def sheet(name, ws=None):
    wb = openpyxl.load_workbook(os.path.join(T, name), read_only=True)
    out = {}
    for s in wb.sheetnames if ws is None else [ws]:
        it = wb[s].iter_rows(values_only=True)
        hdr = next(it)
        out[s] = [dict(zip(hdr, r)) for r in it]
    return out


def headline():
    res = {}
    r5 = {r['Pupil Ref']: r['Establishment'] for r in rows('pupil_roll_2024-25.csv')}
    tot5 = {}
    for r in rows('june_common_paper_marks_2025.csv'):
        if r['Attendance'] == 'P':
            tot5[r['Pupil Ref']] = sum(int(v) for k, v in r.items() if k.startswith('Q'))
    r6 = {r['SCN']: r['School'] for r in rows('pupil_roll_extract_2026-06-12.csv')}
    tot6 = defaultdict(int)
    for r in rows('june_common_paper_marks_2026.csv'):
        if r['Status'] == 'Present':
            tot6[r['SCN']] += int(r['Mark'])
    for yr, tot, sch in ((2025, tot5, r5), (2026, tot6, r6)):
        v = list(tot.values())
        res[str(yr)] = dict(sat=len(v), mean=sum(v) / len(v), share=100.0 * sum(x >= 36 for x in v) / len(v))
        by = defaultdict(list)
        for k, x in tot.items():
            by[sch[k]].append(x)
        res['by_' + str(yr)] = {s: sum(x) / len(x) for s, x in by.items()}
    return res


def tm(s):
    return int(s[:2]) * 60 + int(s[3:5])


def lessons():
    roll = {r['SCN']: r for r in rows('pupil_roll_extract_2026-06-12.csv')}
    names = defaultdict(list)
    for r in roll.values():
        names[(r['Forename'] + ' ' + r['Surname']).lower(), r['Stage']].append(r['SCN'])
    bells = defaultdict(list)
    for r in sheet('bell_times_2025-26.xlsx')['Bell times']:
        bells[r['School'], r['Days']].append((int(r['Period']), tm(r['Start']), tm(r['End'])))
    tt = defaultdict(list)
    for r in rows('maths_timetable_2025-26.csv'):
        f = dt.datetime.strptime(r['Valid_From'], '%d/%m/%Y').date()
        t = dt.datetime.strptime(r['Valid_To'], '%d/%m/%Y').date()
        tt[r['School'], r['Class']].append((f, t, r['Day'], int(r['Period'])))
    mb = pq.read_table(os.path.join(T, 'mathsbridge_homework_export_2025-26.parquet'),
                       columns=['glow_id', 'task_kind', 'set_on', 'units']).to_pylist()
    sig = defaultdict(list)
    for r in mb:
        if r['task_kind'] == 'Review' and r['set_on'] < '2026-01-06':
            sig[r['glow_id']].append((r['set_on'], r['units']))
    gl = {r['Glow_ID']: r for r in roll.values()}
    groups = defaultdict(list)
    for g, v in sig.items():
        groups[gl[g]['School'], gl[g]['Stage'], tuple(sorted(v))].append(gl[g]['Maths_Class'])
    autcls = {}
    for g, v in sig.items():
        mem = groups[gl[g]['School'], gl[g]['Stage'], tuple(sorted(v))]
        autcls[g] = max(sorted(set(mem)), key=mem.count)
    sign = rows('support_base_signins_2025-11-03_to_2026-05-29.csv')
    served = defaultdict(set)
    for r in sign:
        if r['SCN'] in roll:
            served[r['Base']].add(roll[r['SCN']]['School'])
    seen, out, done = set(), defaultdict(int), set()
    for r in sign:
        key = tuple(r.values())
        if key in done:
            continue
        done.add(key)
        if r['SCN']:
            if r['SCN'] not in roll:
                continue
            scn = r['SCN']
        else:
            c = names.get((r['Name_Typed'].lower(), r['Year_Typed']), [])
            if len(c) > 1:
                c = [x for x in c if roll[x]['School'] in served[r['Base']]]
            if len(c) != 1:
                continue
            scn = c[0]
        p = roll[scn]
        d = dt.datetime.strptime(r['Date'], '%d/%m/%Y').date()
        b = sorted(bells[p['School'], 'Friday' if d.weekday() == 4 else 'Monday to Thursday'])
        ti = tm(r['Time_In'])
        p0 = [q for q, a, e in b if a <= ti < e][0]
        p1 = p0 if not r['Time_Out'] else max(q for q, a, e in b if a < tm(r['Time_Out']))
        cls = p['Maths_Class'] if d >= dt.date(2026, 1, 6) else autcls.get(p['Glow_ID'], p['Maths_Class'])
        dn = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'][d.weekday()]
        for q in range(p0, p1 + 1):
            if any(f <= d <= t and dd == dn and pp == q for f, t, dd, pp in tt[p['School'], cls]) and (scn, d, q) not in seen:
                seen.add((scn, d, q))
                out[p['School']] += 1
    return dict(out)


def classes():
    """each class's teachers: for each timetable row and each term its validity runs through, the person that term's
    code sheet names on the code, matched to the establishment by first initial and surname or previous surname at the
    school, counted where that holder's time in post overlaps the row's days in the term"""
    codes = sheet('timetable_staff_codes_2025-26.xlsx')
    est = sheet('maths_staffing_establishment_2025-26.xlsx')['Mathematics posts']
    def key(name):
        w = name.replace('.', '').split()
        w = w[1:] if w[0] in ('Mr', 'Mrs', 'Ms', 'Miss', 'Dr') else w
        return w[0][0].upper(), w[-1].upper()
    def day(s):
        return dt.datetime.strptime(s, '%d/%m/%Y').date() if s else None
    name = {}
    for ph, s in (('aut', 'Autumn 2025'), ('spr', 'Spring 2026')):
        for r in codes[s]:
            name[ph, r['School'], r['Code']] = key(r['Name'])
    holders = defaultdict(list)
    for r in est:
        sur, fn = r['Holder'].split(', ')
        for s in {sur.upper(), (r['Previous_Surname'] or '').upper()} - {''}:
            for sch in r['School'].split(' / '):
                holders[sch, fn[0].upper(), s].append((day(r['In_Post_From']), day(r['In_Post_To'] or ''), r['Holder']))
    tt = rows('maths_timetable_2025-26.csv')
    ends = sorted({day(r['Valid_To']) for r in tt})
    starts = sorted({day(r['Valid_From']) for r in tt})
    terms = (('aut', starts[0], ends[0]), ('spr', starts[-1], ends[-1]))
    per = defaultdict(set)
    for r in tt:
        f, t = day(r['Valid_From']), day(r['Valid_To'])
        for ph, a, b in terms:
            lo, hi = max(f, a), min(t, b)
            if lo > hi:
                continue
            hs = holders[(r['School'],) + name[ph, r['School'], r['Staff']]]
            per[r['School'], r['Class']] |= {h for s0, s1, h in hs if s0 <= hi and (s1 is None or s1 >= lo)}
    out = defaultdict(int)
    for (s, c), v in per.items():
        out[s] += len(v) > 1
    return dict(out)


def main():
    F = json.load(open(os.path.join(HERE, 'figures.json')))
    bad = []
    H = headline()
    for yr in ('2025', '2026'):
        for k in ('sat', 'mean', 'share'):
            if abs(H[yr][k] - F['head'][yr][k]) > 1e-9:
                bad.append(('head', yr, k, H[yr][k], F['head'][yr][k]))
        for s, v in H['by_' + yr].items():
            if abs(v - F['by_school'][s][yr]) > 1e-9:
                bad.append(('school', s, yr))
    le, cl = lessons(), classes()
    if le != F['ask_lessons']:
        bad.append(('lessons', le, F['ask_lessons']))
    if cl != F['ask_classes']:
        bad.append(('classes', cl, F['ask_classes']))
    print('verify:', 'PASS' if not bad else bad)
    return 0 if not bad else 1


if __name__ == '__main__':
    sys.exit(main())
