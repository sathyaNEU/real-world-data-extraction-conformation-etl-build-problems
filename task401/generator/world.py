"""Strathcorrie Council, S1 to S3 mathematics, sessions 2024-25 and 2025-26: the world behind the pack.

Every draw is seeded. A pupil's grip on each topic of their year group's June paper depends on their ability, the
topic's difficulty, a gap of their own on some topics (a misconception that shows in their first homework on it),
forgetting between teaching and June, and the retrieval practice that came back to the topic. In 2024-25 the
council's homework platform (Corvella) drew each pupil's weekly retrieval questions from the topics that pupil had
got wrong; from August 2025 Mathsbridge sets each class one mixed review of earlier units. The 2025-26 changes:
A the new framework (four topics a year group rewritten), B the platform switch, C the asymmetric week (S3 maths five
periods to four), D the support bases (from 3 November), E two shared maths posts (classes split from 6 January).
The truth for each change is the session re-run on the same draws with that change switched off."""
import datetime as dt
import hashlib

import numpy as np
import pandas as pd

SHIP_SEED = 18

SCHOOLS = [  # code, name, seed code, base host, January timetable rebuild (re-keyed staff codes), job-share post
    ('ARC', 'Ardcorrie Academy', '5531428', 'ARC', False, True),
    ('BAL', 'Balmorran High School', '5531630', 'BAL', True, False),
    ('GLW', 'Glenwhinnie Academy', '5532041', 'GLW', False, True),
    ('KIL', 'Kilbraith Academy', '5532246', 'KIL', True, False),
    ('LOC', 'Lochbrannie High School', '5532548', 'LOC', False, True),
    ('MUI', 'Muirlees High School', '5532742', 'MUI', False, True),
    ('SMO', "St Moluag's High School", '5533048', 'LOC', False, True),
    ('TOR', 'Torranbrae High School', '5533242', 'TOR', True, False),
]
SCODES = [s[0] for s in SCHOOLS]
SPLIT_SCHOOLS = ('GLW', 'KIL', 'MUI', 'TOR')  # the two shared posts serve Kilbraith-Torranbrae and Glenwhinnie-Muirlees
YG = ('S1', 'S2', 'S3')
U = 12                     # topics on each year group's June paper
ITEM_MAX = (1, 2, 2)       # three items a topic, five marks a topic, sixty a paper
PAPER_MAX = U * sum(ITEM_MAX)
SECURE = 36

TOPICS = {
    'S1': ['Whole numbers and place value', 'Rounding and estimation', 'Negative numbers', 'Fractions of amounts',
           'Decimals', 'Percentages', 'Expressions', 'Equations', 'Angles', 'Perimeter and area', 'Coordinates',
           'Interpreting data'],
    'S2': ['Multiples, factors and primes', 'Integer calculation', 'Fraction calculation', 'Percentage change',
           'Ratio and proportion', 'Expanding brackets', 'Solving equations', 'Sequences', 'Area of compound shapes',
           'Volume', 'Scale drawing', 'Averages and range'],
    'S3': ['Powers and roots', 'Scientific notation', 'Proportion problems', 'Factorising', 'Linear equations',
           'Straight-line graphs', 'Inequations', 'Pythagoras', 'Circles', 'Similar shapes', 'Probability',
           'Statistical diagrams'],
}

P = dict(gap_rate=0.25, gap_mu=1.9, gap_sd=0.35, noise_sd=0.25, rev_q=6, k_r=0.030, pers_pow=3.0,
         decay=0.45, a1=0.65, comp_boost=0.2, A1=0.10, A_grad=0.45, C=0.07, D=0.30, E=0.08, yeff=0.012,
         eng_slope=0.6)

S24 = dict(session='2024-25', year=2025, start=dt.date(2024, 8, 19), paper=dt.date(2025, 6, 3))
S25 = dict(session='2025-26', year=2026, start=dt.date(2025, 8, 18), paper=dt.date(2026, 6, 2))
BASES_OPEN = dt.date(2025, 11, 3)
SPLIT_FROM = dt.date(2026, 1, 6)
SPRING_WEEK = SPLIT_FROM - dt.timedelta(days=SPLIT_FROM.weekday())   # the teaching week the spring term opens in
HOLIDAYS = {
    2025: [(dt.date(2024, 10, 14), dt.date(2024, 10, 25)), (dt.date(2024, 12, 23), dt.date(2025, 1, 3)),
           (dt.date(2025, 2, 10), dt.date(2025, 2, 14)), (dt.date(2025, 4, 4), dt.date(2025, 4, 18)),
           (dt.date(2025, 5, 5), dt.date(2025, 5, 5))],
    2026: [(dt.date(2025, 10, 13), dt.date(2025, 10, 24)), (dt.date(2025, 12, 22), dt.date(2026, 1, 5)),
           (dt.date(2026, 2, 9), dt.date(2026, 2, 13)), (dt.date(2026, 4, 3), dt.date(2026, 4, 17)),
           (dt.date(2026, 5, 4), dt.date(2026, 5, 4))],
}


def lg(x):
    return 1.0 / (1.0 + np.exp(-x))


def school_days(start, end, year):
    out, d = [], start
    while d <= end:
        if d.weekday() < 5 and not any(a <= d <= b for a, b in HOLIDAYS[year]):
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def teaching_weeks(sess):
    """Mondays of the weeks homework is set, from the second week to the week before the papers."""
    days = school_days(sess['start'] + dt.timedelta(days=7), sess['paper'] - dt.timedelta(days=8), sess['year'])
    mondays = sorted({d - dt.timedelta(days=d.weekday()) for d in days})
    return mondays


def h(s, n=8):
    return hashlib.sha1(s.encode()).hexdigest()[:n]


class World:
    def __init__(self, seed=SHIP_SEED, params=None):
        self.seed = seed
        self.P = dict(P)
        if params:
            self.P.update(params)
        self.rng = np.random.default_rng(seed)
        self._people()
        self._curriculum()
        self.sess = {}
        for s in (S24, S25):
            self.sess[s['year']] = self._session(s)

    # ---------------------------------------------------------------- pupils, classes, staff
    def _people(self):
        rng = self.rng
        from faker import Faker
        fk = Faker('en_GB')
        fk.seed_instance(self.seed * 7 + 1)
        pupils, scn_used = [], set()
        smean = {c: rng.normal(0, 0.15) for c in SCODES}
        sdep = {c: rng.normal(0, 0.35) for c in SCODES}
        for c in SCODES:
            for entry in (2022, 2023, 2024, 2025):
                n = int(rng.integers(150, 231))
                for _ in range(n):
                    while True:
                        scn = str(int(rng.integers(100000000, 199999999)))
                        if scn not in scn_used:
                            scn_used.add(scn)
                            break
                    th = rng.normal(smean[c], 1.0)
                    sex = 'F' if rng.random() < 0.49 else 'M'
                    fn = fk.first_name_female() if sex == 'F' else fk.first_name_male()
                    pupils.append(dict(scn=scn, school=c, entry=entry, theta=th, sex=sex, forename=fn,
                                       surname=fk.last_name(),
                                       fsm=bool(rng.random() < lg(-1.1 - 0.6 * th + sdep[c])),
                                       asn=bool(rng.random() < lg(-0.55 - 0.35 * th)),
                                       eal=bool(rng.random() < 0.07),
                                       simd=int(np.clip(round(5.5 + 1.6 * th - 3.0 * sdep[c] + rng.normal(0, 2.2)), 1, 10)),
                                       incomer=bool(rng.random() < 0.05),
                                       p7noise=rng.normal(0, 0.45)))
        df = pd.DataFrame(pupils)
        df['mis_ref'] = ['SC' + str(700000 + i * 7 + int(rng.integers(0, 7))) for i in range(len(df))]
        df['p7_numeracy'] = np.where(df['incomer'], np.nan, np.round(100 + 15 * (df['theta'] + df['p7noise'])))
        self.pupils = df

    def _curriculum(self):
        rng = self.rng
        self.rewritten = {g: sorted(rng.choice(U, 4, replace=False).tolist()) for g in YG}
        self.b = {g: rng.normal(0, 0.45, U) for g in YG}
        self.e = {g: rng.normal(0, 0.35, (U, 3)) for g in YG}
        self.yeff = {2025: rng.normal(0, self.P['yeff']), 2026: rng.normal(0, self.P['yeff'])}
        # Corvella skill codes (three a topic) and the new framework's unit codes
        self.cv_skill = {g: [['CV%s%02d%d' % (g[1], t + 1, k) for k in range(3)] for t in range(U)] for g in YG}
        self.mb_unit = {g: ['%s.%02d' % ('N' + g[1], t + 1) for t in range(U)] for g in YG}
        self.old_unit = {g: ['%s-U%02d' % (g, t + 1) for t in range(U)] for g in YG}

    # ---------------------------------------------------------------- one session
    def _session(self, s):
        rng = np.random.default_rng(self.seed * 1000 + s['year'])
        Pp = self.P
        year = s['year']
        ent = {'S1': year - 1, 'S2': year - 2, 'S3': year - 3}
        rows = []
        for g in YG:
            sub = self.pupils[self.pupils['entry'] == ent[g]].copy()
            sub['yg'] = g
            rows.append(sub)
        pp = pd.concat(rows, ignore_index=True)
        N = len(pp)
        # movement within the session: a few leave before the papers, a few join after the start
        pp['left'] = rng.random(N) < 0.018
        pp['joined_late'] = rng.random(N) < 0.02
        pp['absent_paper'] = (~pp['left']) & (rng.random(N) < lg(-3.6 - 0.4 * pp['theta'].values))
        # classes: about 26 a class, mixed attainment, class codes like 2M3
        cls = np.empty(N, dtype=object)
        for (c, g), idx in pp.groupby(['school', 'yg']).groups.items():
            idx = np.array(sorted(idx))
            k = int(np.ceil(len(idx) / 26.0))
            perm = rng.permutation(len(idx))
            for j, ii in enumerate(perm):
                cls[idx[ii]] = '%s%s%d' % (g[1], 'M', j % k + 1)
        pp['maths_class'] = cls
        th = pp['theta'].values
        ygi = pp['yg'].map({'S1': 0, 'S2': 1, 'S3': 2}).values
        bb = np.stack([self.b[g] for g in YG])[ygi]
        # gaps of each pupil's own (independent of topic difficulty)
        ngap = rng.choice([2, 3, 3, 3, 4], size=N)
        gap = np.argsort(rng.random((N, U)), axis=1) < ngap[:, None]
        sev = rng.normal(Pp['gap_mu'], Pp['gap_sd'], (N, U))
        noise = rng.normal(0, Pp['noise_sd'], (N, U))
        sgap = np.where(gap, sev, 0.0)
        u_comp = rng.random((N, U))
        u_hw = rng.random((N, U, 10))
        u_rev = rng.random((N, 60))
        u_revc = rng.random((N, 60))
        u_item = rng.random((N, U, 3, 2))
        u_rem = rng.random(N)
        weeks = teaching_weeks(s)
        nw = len(weeks)
        tweek = np.array([int(t * nw / U) for t in range(U)])            # first week each topic is taught
        months = np.array([(s['paper'] - weeks[w]).days / 30.4 for w in tweek])
        out = dict(s=s, pp=pp, N=N, th=th, ygi=ygi, bb=bb, gap=gap, sgap=sgap, vtop=noise, u_comp=u_comp, u_hw=u_hw,
                   u_rev=u_rev, u_revc=u_revc, u_item=u_item, u_rem=u_rem, weeks=weeks, tweek=tweek, months=months)
        # support base removals (2025-26 only, from 3 November)
        if year == 2026:
            fsm = pp['fsm'].values
            removed = (u_rem < lg(-3.2 - 0.6 * th + 0.4 * fsm)) & (~pp['left'].values)
            out['removed'] = removed
            # split classes from 6 January: one class in four at the four schools the shared posts serve
            split = np.zeros(N, bool)
            for (c, g, k), idx in pp.groupby(['school', 'yg', 'maths_class']).groups.items():
                if c in SPLIT_SCHOOLS and int(h(c + g + k, 6), 16) % 4 == 0:
                    split[np.array(list(idx))] = True
            out['split'] = split
            # set changes at the start of January: the roll keeps each pupil's class from 6 January; a pupil moved
            # then sat in another class of the same year group before it (own stream, the session's draws untouched)
            rm = np.random.default_rng(self.seed * 1000 + 7)
            aut = pp['maths_class'].values.copy()
            mv = (rm.random(N) < lg(-2.8 - 0.5 * th + 1.6 * removed)) & ~pp['joined_late'].values & ~pp['left'].values
            for (c, g), idx in pp.groupby(['school', 'yg']).groups.items():
                idx = np.array(sorted(idx))
                ks = sorted(set(pp['maths_class'].values[idx]))
                for i in idx[mv[idx]]:
                    oth = [k for k in ks if k != aut[i]]
                    aut[i] = oth[int(rm.integers(0, len(oth)))]
            pp['maths_class_aut'] = aut
            out['moved'] = mv
        else:
            out['removed'] = np.zeros(N, bool)
            out['split'] = np.zeros(N, bool)
            pp['maths_class_aut'] = pp['maths_class'].values
            out['moved'] = np.zeros(N, bool)
        out['on'] = dict(A=True, B=True, C=True, D=True, E=True)
        self._learn(out, out['on'])
        return out

    def _learn(self, o, on):
        """first homework, review allocation, June item marks for one session under the switches in `on`."""
        Pp = self.P
        year = o['s']['year']
        N, th, bb = o['N'], o['th'], o['bb']
        fsm = o['pp']['fsm'].values
        newp = (year == 2026 and on['B'])
        p0 = lg(0.8 + th[:, None] - bb - o['sgap'] - o['vtop'])
        comp = lg(1.6 + Pp['eng_slope'] * th - 0.5 * fsm + (Pp['comp_boost'] if newp else 0.0))
        done = o['u_comp'] < comp[:, None]
        late = o['pp']['joined_late'].values
        done = done & ~(late[:, None] & (np.arange(U)[None, :] < 3))
        k0 = (o['u_hw'] < p0[:, :, None]).sum(axis=2)
        acc0 = np.where(done, k0 / 10.0, np.nan)
        # review questions over the year: each week from the fourth, six questions on topics already taught
        nw = len(o['weeks'])
        R = np.zeros((N, U))
        rev_topics = []
        cls = o['pp']['maths_class'].values
        clsa = o['pp']['maths_class_aut'].values
        sch = o['pp']['school'].values
        for w in range(3, nw):
            taught = np.where(o['tweek'] < w)[0]
            if len(taught) == 0:
                rev_topics.append(None)
                continue
            if newp:  # one set per class: three taught topics, two questions each, same for every pupil in the class
                clw = clsa if o['weeks'][w] < SPRING_WEEK else cls
                picks = {}
                for key in sorted(set(zip(sch, o['ygi'], clw))):
                    hh = int(h('%s%d%s%d%d' % (key[0], key[1], key[2], w, self.seed), 8), 16)
                    r = np.random.default_rng(hh)
                    picks[key] = r.choice(taught, size=min(3, len(taught)), replace=False)
                tp = np.array([picks[(a, b_, c)] if len(taught) >= 3 else np.resize(taught, 3)
                               for a, b_, c in zip(sch, o['ygi'], clw)])
                q = np.repeat(tp, 2, axis=1)
            else:      # each pupil's own: weighted by how much of the topic they got wrong first time
                wt = np.where(np.isnan(acc0[:, taught]), 0.3, 1 - acc0[:, taught]) + 0.05
                wt = wt ** Pp['pers_pow']
                wt = wt / wt.sum(axis=1, keepdims=True)
                cw = np.cumsum(wt, axis=1)
                q = np.empty((N, Pp['rev_q']), dtype=int)
                for j in range(Pp['rev_q']):
                    u = o['u_rev'][:, (w * Pp['rev_q'] + j) % 60]
                    q[:, j] = taught[np.minimum((cw < u[:, None]).sum(axis=1), len(taught) - 1)]
            did = o['u_revc'][:, w % 60] < comp
            for j in range(q.shape[1]):
                np.add.at(R, (np.arange(N)[did], q[did, j]), 1.0)
            rev_topics.append((q, did))
        rem = 1 - np.exp(-(Pp['k_r'] * R) ** 2)
        s = o['sgap']
        lat = th[:, None] - bb - s * (1 - rem) - o['vtop'] - Pp['decay'] * o['months'][None, :] / 10.0
        lat = lat + self.yeff[year]
        if year == 2026:
            ygi = o['ygi']
            rw = np.zeros((N, U), bool)
            for gi, g in enumerate(YG):
                rw[np.ix_(ygi == gi, self.rewritten[g])] = True
            if on['A']:
                lat = lat - Pp['A1'] * np.clip(1.0 - Pp['A_grad'] * th, 0.2, 2.5)[:, None] * rw
            if on['C']:
                lat = lat - Pp['C'] * (ygi == 2)[:, None]
            if on['D']:
                lat = lat - Pp['D'] * o['removed'][:, None]
            if on['E']:
                lat = lat - Pp['E'] * o['split'][:, None]
        ygi = o['ygi']
        e = np.stack([self.e[g] for g in YG])[ygi]
        pj = lg(Pp['a1'] + lat[:, :, None] - e)
        mx = np.array(ITEM_MAX)
        marks = (o['u_item'][..., 0] < pj).astype(int) + ((o['u_item'][..., 1] < pj) & (mx[None, None, :] == 2)).astype(int)
        sat = ~(o['pp']['left'].values | o['pp']['absent_paper'].values)
        res = dict(acc0=acc0, done=done, comp=comp, R=R, marks=marks, sat=sat, rev_topics=rev_topics, p0=p0,
                   total=np.where(sat, marks.sum(axis=(1, 2)), -1))
        if on == o['on']:
            o.update(res)
        return res

    # ---------------------------------------------------------------- truth
    def truth_costs(self):
        o = self.sess[2026]
        base = o['total'][o['sat']].sum()
        out = {}
        for k in 'ABCDE':
            on = dict(o['on']); on[k] = False
            r = self._learn(o, on)
            out[k] = int(r['total'][o['sat']].sum() - base)
        return out


if __name__ == '__main__':
    import time
    t = time.time()
    w = World()
    print('built in %.1fs' % (time.time() - t))
    for y in (2025, 2026):
        o = w.sess[y]
        tot = o['total'][o['sat']]
        print(y, 'pupils', o['N'], 'sat', int(o['sat'].sum()), 'mean %.2f' % tot.mean(), 'secure %.3f' % (tot >= SECURE).mean())
    print('truth', w.truth_costs())
