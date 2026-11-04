"""Maths staffing, the 2025-26 maths timetable, bell times and the support base sign-ins: the records behind the two
asks, built from the world's classes and removed pupils. Truth for both asks is computed here from the generating
events, never from the shipped rows."""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

import world as Wd

DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
LEFT_BEFORE = dt.date(2025, 8, 15)   # last day in post of the three teachers who left over the summer of 2025


def hh(s, n=8):
    return int(hashlib.sha1(s.encode()).hexdigest()[:n], 16)


def js_holder(day, period):
    """a job-share post's two holders split the week: the first holder works Monday, Tuesday and Wednesday morning
    (periods 1 to 4), the second Wednesday afternoon, Thursday and Friday; each teaches the post's classes on their
    own days under their own timetable code. A class meets on four different days, so both holders teach it."""
    return 0 if day in (0, 1) or (day == 2 and period <= 4) else 1


def bell_times():
    """asymmetric week: six periods Monday to Thursday, four on Friday; each school's start differs a little"""
    rows = []
    for k, (c, name, seed_code, host, rek, js) in enumerate(Wd.SCHOOLS):
        kk = 4 if c == 'SMO' else k   # St Moluag's shares the Lochbrannie campus and its bells
        st = [dt.datetime(2025, 8, 18, 8, 45), dt.datetime(2025, 8, 18, 8, 50), dt.datetime(2025, 8, 18, 8, 55)][kk % 3]
        mt = []
        t = st
        for p in range(1, 7):
            length = 55 if p in (1, 2, 3, 4) else 50
            mt.append((p, t, t + dt.timedelta(minutes=length)))
            t = t + dt.timedelta(minutes=length)
            if p == 2:
                t += dt.timedelta(minutes=15)
            if p == 4:
                t += dt.timedelta(minutes=40)
        fr = []
        t = st
        for p in range(1, 5):
            fr.append((p, t, t + dt.timedelta(minutes=50)))
            t += dt.timedelta(minutes=50)
            if p == 2:
                t += dt.timedelta(minutes=15)
        for p, a, b in mt:
            rows.append(dict(school=c, day_type='Mon-Thu', period=p, start=a.time(), end=b.time()))
        for p, a, b in fr:
            rows.append(dict(school=c, day_type='Fri', period=p, start=a.time(), end=b.time()))
    return pd.DataFrame(rows)


class Staffing:
    def __init__(self, w):
        self.w = w
        rng = np.random.default_rng(w.seed * 31 + 5)
        from faker import Faker
        fk = Faker('en_GB')
        fk.seed_instance(w.seed * 31 + 7)
        o = w.sess[2026]
        pp = o['pp']
        self.bells = bell_times()
        classes = (pp[['school', 'yg', 'maths_class']].drop_duplicates()
                   .sort_values(['school', 'yg', 'maths_class']).reset_index(drop=True))
        self.classes = classes
        # teachers: one person per four or five classes; a job-share post at five schools
        people, posts = [], []
        used = set()
        for c, name, seed_code, host, rek, js in Wd.SCHOOLS:
            ncls = int((classes['school'] == c).sum())
            nteach = max(4, int(round(ncls / 4.5)))
            for i in range(nteach):
                while True:
                    fem = rng.random() < 0.6
                    fn, sn = (fk.first_name_female() if fem else fk.first_name_male()), fk.last_name()
                    if (fn, sn) not in used:
                        used.add((fn, sn))
                        break
                people.append(dict(school=c, forename=fn, surname=sn, post='%s-MT%02d' % (c, i + 1), js=False, fem=fem))
            if js:
                pair = []
                for _ in range(2):
                    while True:
                        fem = rng.random() < 0.7
                        fn, sn = (fk.first_name_female() if fem else fk.first_name_male()), fk.last_name()
                        if (fn, sn) not in used:
                            used.add((fn, sn))
                            break
                    pair.append((fn, sn, fem))
                for fn, sn, fem in pair:
                    people.append(dict(school=c, forename=fn, surname=sn, post='%s-MT%02d' % (c, nteach + 1), js=True, fem=fem))
        self.people = pd.DataFrame(people)
        # the two January starters on the Christmas leavers' posts, and the two shared posts' teachers (own stream)
        fk2 = Faker('en_GB')
        fk2.seed_instance(w.seed * 31 + 9)
        r2 = np.random.default_rng(w.seed * 31 + 13)
        self.extra = {}
        for key in ('ARC', 'BAL', 'SH1', 'SH2'):
            while True:
                fem = r2.random() < 0.6
                fn, sn = (fk2.first_name_female() if fem else fk2.first_name_male()), fk2.last_name()
                if (fn, sn) not in used and sn not in set(self.people['surname']):
                    used.add((fn, sn))
                    break
            self.extra[key] = dict(forename=fn, surname=sn, fem=fem)
        # two teachers married over Christmas and teach on under their new surnames from January (same post)
        self.renamed = {}
        for c in ('TOR', 'LOC', 'SMO'):
            cand = self.people[(self.people['school'] == c) & ~self.people['js'] & self.people['fem']]
            cand = cand.sort_values('post')
            pick = cand.iloc[hh(c + 'renamed', 6) % len(cand)]
            while True:
                sn = fk2.last_name()
                if sn not in set(self.people['surname']) and all(sn != e['surname'] for e in self.extra.values()):
                    break
            self.renamed[(c, pick['post'])] = sn
        # three posts changed holder over the summer of 2025: the leaver's contract ran to 15 August, the new holder
        # started on the session's first day (18 August) and taught the classes all session; the autumn code sheet,
        # produced on 14 August, still carries the leaver's name on the code, and the establishment lists both
        self.stale = {}
        for c in ('GLW', 'MUI', 'KIL'):
            cand = self.people[(self.people['school'] == c) & ~self.people['js']].sort_values('post')
            cand = cand[[(c, p) not in self.renamed for p in cand['post']]]
            pick = cand.iloc[hh(c + 'stale', 6) % len(cand)]
            while True:
                fem = r2.random() < 0.5
                fn, sn = (fk2.first_name_female() if fem else fk2.first_name_male()), fk2.last_name()
                if (fn, sn) not in used and sn not in set(self.people['surname']):
                    used.add((fn, sn))
                    break
            self.stale[(c, pick['post'])] = dict(forename=fn, surname=sn, fem=fem)
        # timetable codes before 6 January: initials-free numeric codes, one a post; a job-share post's second holder
        # carries a code of their own (js_code_b), never one another code at the school already holds
        codes = {}
        for c in Wd.SCODES:
            sub = self.people[self.people['school'] == c]
            for post, g in sub.groupby('post', sort=True):
                codes[(c, post)] = 'T%04d' % (hh(c + post, 6) % 9000 + 1000)
        self.old_code = codes
        self.js_code_b = {}
        for (c, post), code in sorted(codes.items()):
            if self.people[(self.people['school'] == c) & (self.people['post'] == post)]['js'].any():
                taken = {v for (s, _), v in codes.items() if s == c} | set(self.js_code_b.values())
                salt = 0
                while True:
                    b = 'T%04d' % (hh(c + post + 'js%d' % salt, 6) % 9000 + 1000)
                    if b not in taken:
                        break
                    salt += 1
                self.js_code_b[(c, post)] = b
        # new codes from 6 January at the three schools whose timetables were rebuilt in the new package
        self.new_code = {}
        for (c, post), code in codes.items():
            rek = dict((s[0], s[4]) for s in Wd.SCHOOLS)[c]
            if rek:
                g = self.people[(self.people['school'] == c) & (self.people['post'] == post)].iloc[0]
                self.new_code[(c, post)] = (g['forename'][0] + g['surname'][:2]).upper()
            else:
                self.new_code[(c, post)] = code
        self._assign(rng)
        self._removals()

    def _assign(self, rng):
        """each class one post for the session; a Christmas replacement at two schools; the shared posts add a
        second teacher to the split classes from 6 January"""
        rows = []
        cls = self.classes
        posts_by_school = {c: sorted(self.people[self.people['school'] == c]['post'].unique()) for c in Wd.SCODES}
        repl = {}
        self.events = []
        for i, r in cls.iterrows():
            c = r['school']
            plist = posts_by_school[c]
            post = plist[hh(c + r['yg'] + r['maths_class'], 6) % len(plist)]
            cls.loc[i, 'post'] = post
        # Christmas replacement: one post at ARC and at BAL leaves at Christmas; a new teacher from 6 January
        self.replaced = {}
        for c in ('ARC', 'BAL'):
            plist = [p for p in posts_by_school[c] if not self.people[(self.people['school'] == c) & (self.people['post'] == p)]['js'].any()]
            self.replaced[c] = plist[hh(c + 'leaver', 6) % len(plist)]
        o = self.w.sess[2026]
        pp = o['pp']
        split_classes = set()
        for j in np.where(o['split'])[0]:
            split_classes.add((pp['school'].iloc[j], pp['yg'].iloc[j], pp['maths_class'].iloc[j]))
        self.split_classes = sorted(split_classes)
        self.cls = cls

    def persons_per_class(self):
        """truth for ask 2: the distinct people who were each class's timetabled maths teacher in the session"""
        out = {}
        for _, r in self.cls.iterrows():
            key = (r['school'], r['yg'], r['maths_class'])
            ppl = set()
            sub = self.people[(self.people['school'] == r['school']) & (self.people['post'] == r['post'])]
            if self.replaced.get(r['school']) == r['post']:
                ppl.add(('old', r['school'], r['post']))
                ppl.add(('new', r['school'], r['post']))
            else:
                for _, pr in sub.iterrows():
                    ppl.add((pr['forename'], pr['surname']))
            if key in self.split_classes:
                ppl.add(('shared', r['school']))
            out[key] = len(ppl)
        return out

    def _removals(self):
        """support base removal events from 3 November to the papers: a date, a period (any subject), a stay of
        one period or more; the base keeps a sign-in with the time in and, usually, the time out"""
        w = self.w
        o = w.sess[2026]
        pp = o['pp']
        rng = np.random.default_rng(w.seed * 31 + 11)
        days = Wd.school_days(Wd.BASES_OPEN, Wd.S25['paper'] - dt.timedelta(days=5), 2026)
        ev = []
        for j in np.where(o['removed'])[0]:
            k = 1 + rng.poisson(3.2)
            for _ in range(k):
                d = days[rng.integers(0, len(days))]
                nper = 4 if d.weekday() == 4 else 6
                p = int(rng.integers(1, nper + 1))
                stay = 1 + (rng.random() < 0.22) + (rng.random() < 0.07)
                ev.append(dict(j=int(j), scn=pp['scn'].iloc[j], school=pp['school'].iloc[j], yg=pp['yg'].iloc[j],
                               maths_class=pp['maths_class'].iloc[j], cls_aut=pp['maths_class_aut'].iloc[j],
                               date=d, period=p,
                               last=min(nper, p + stay - 1), mins_in=int(rng.integers(3, 36)),
                               card=bool(rng.random() > 0.13), u=rng.random()))
        self.removals = pd.DataFrame(ev).sort_values(['date', 'school', 'period', 'scn']).reset_index(drop=True)

    def maths_slots(self):
        """the 2025-26 maths timetable: each class four periods a week (S3 now four too); the slot pattern is fixed
        for the session, except that the three rebuilt schools' classes moved slots from 6 January"""
        rows = []
        for _, r in self.cls.iterrows():
            c, g, k = r['school'], r['yg'], r['maths_class']
            for phase in ('autumn', 'spring'):
                rek = dict((s[0], s[4]) for s in Wd.SCHOOLS)[c]
                seedkey = c + g + k + (phase if rek else 'autumn')
                cand = [(d, p) for d in range(4) for p in range(1, 7)] + [(4, p) for p in range(1, 5)]
                pick = []
                h0 = hh(seedkey, 8)
                r0 = np.random.default_rng(h0)
                order = r0.permutation(len(cand))
                used_days = set()
                for idx in order:
                    d, p = cand[idx]
                    if d in used_days:
                        continue
                    pick.append((d, p))
                    used_days.add(d)
                    if len(pick) == 4:
                        break
                rows.append(dict(school=c, yg=g, maths_class=k, phase=phase, slots=sorted(pick)))
        return pd.DataFrame(rows)

    def base_truth(self):
        """truth for ask 1: maths lessons each school's pupils missed while signed in to a base"""
        slots = self.maths_slots()
        sl = {(r['school'], r['yg'], r['maths_class'], r['phase']): set(r['slots']) for _, r in slots.iterrows()}
        seen = set()
        out = {c: 0 for c in Wd.SCODES}
        for _, e in self.removals.iterrows():
            phase = 'spring' if e['date'] >= Wd.SPLIT_FROM else 'autumn'
            k = e['maths_class'] if phase == 'spring' else e['cls_aut']
            s = sl[(e['school'], e['yg'], k, phase)]
            wd = e['date'].weekday()
            for p in range(e['period'], e['last'] + 1):
                key = (e['scn'], e['date'], p)
                if (wd, p) in s and key not in seen:
                    seen.add(key)
                    out[e['school']] += 1
        return out
