"""The golden on the clean truth: each unit's posts, the readmissions avoided, the two trial asks, and the
deliverables. verify.py recomputes all of it from the shipped pack on its own code path."""
import datetime as dt
import json
import math
import os
import numpy as np
import world as W
import records as R

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
GOLD = os.path.join(TASK, 'golden')
POSTS = 30
TOTAL_STEP = 25


def largest_remainder(values, total=POSTS):
    v = np.array(values, float)
    q = total * v / v.sum()
    fl = np.floor(q).astype(int)
    rem = q - fl
    k = int(total - fl.sum())
    order = sorted(range(len(v)), key=lambda i: (-rem[i], i))
    out = fl.copy()
    for i in order[:k]:
        out[i] += 1
    return [int(x) for x in out], [float(x) for x in q]


def nearest(x, step):
    return int(math.floor(x / step + 0.5) * step)


def readmitted(b):
    return b['readm_t'] is not None


def reached(b):
    """The baby is readmitted after the earliest moment the outreach line could have reached the family."""
    return b['readm_t'] is not None and b['readm_t'] > b['landmark']


def report_missed(B):
    """Babies whose readmission the trial team's linkage (NHS number, then the index) did not find: Copperfield's
    PAS holds a baby back on its postnatal ward under the mother's record."""
    rows, _ = R.admissions(B)
    return frozenset(r['baby'] for r in rows if r['site'] == 'CFH' and r['ward'] == 'Postnatal ward' and r['kind'] == 'readm')


def trial_stats(B, missed=frozenset()):
    def readmitted(b):
        return b['readm_t'] is not None and b['nhs'] not in missed
    T = [b for b in B if W.analysed(b)]
    arms = {a: [b for b in T if b['arm'] == a] for a in ('outreach', 'usual care')}
    out = {'randomised': sum(1 for b in B if b['trial']), 'withdrawn': sum(1 for b in B if b['trial'] and b['withdrawn']),
           'rand_o': sum(1 for b in B if b['trial'] and b['arm'] == 'outreach'),
           'rand_c': sum(1 for b in B if b['trial'] and b['arm'] == 'usual care')}
    for a, A in arms.items():
        out[a] = dict(n=len(A), r=sum(readmitted(b) for b in A))
    o, c = out['outreach'], out['usual care']
    rr = (o['r'] / o['n']) / (c['r'] / c['n'])
    se = math.sqrt(1 / o['r'] - 1 / o['n'] + 1 / c['r'] - 1 / c['n'])
    out['rr'] = rr
    out['ci'] = (math.exp(math.log(rr) - 1.96 * se), math.exp(math.log(rr) + 1.96 * se))
    # pre-specified subgroups: gestation, feeding at discharge, and the primary risk reason (below)
    subs = {}
    for name, f in (('Born at 35 to 37 weeks', lambda b: b['gest'] <= 37), ('Born at 38 weeks or later', lambda b: b['gest'] >= 38),
                    ('Exclusively breast fed', lambda b: b['feed'] == 'breast'), ('Not exclusively breast fed', lambda b: b['feed'] != 'breast')):
        so = [b for b in arms['outreach'] if f(b)]
        sc = [b for b in arms['usual care'] if f(b)]
        ro, rc = sum(readmitted(b) for b in so), sum(readmitted(b) for b in sc)
        subs[name] = dict(no=len(so), ro=ro, nc=len(sc), rc=rc, rr=(ro / len(so)) / (rc / len(sc)) if rc and len(so) else float('nan'))
    out['subgroups'] = subs

    def interaction(a, b2):
        x, y = subs[a], subs[b2]
        def lv(s):
            return math.log(s['rr']), 1 / s['ro'] - 1 / s['no'] + 1 / s['rc'] - 1 / s['nc']
        (l1, v1), (l2, v2) = lv(x), lv(y)
        z = abs(l1 - l2) / math.sqrt(v1 + v2)
        return math.erfc(z / math.sqrt(2))
    out['p_interaction'] = {'gestation': interaction('Born at 35 to 37 weeks', 'Born at 38 weeks or later'),
                            'feeding': interaction('Exclusively breast fed', 'Not exclusively breast fed')}
    # heterogeneity across the primary risk reason recorded at randomisation (Cochran's Q on the log risk ratios of
    # the reasons with readmissions in both arms)
    from scipy.stats import chi2
    xs = []
    for r in W.REASONS:
        so = [b for b in arms['outreach'] if b['reasons'][0] == r]
        sc = [b for b in arms['usual care'] if b['reasons'][0] == r]
        ro, rc = sum(readmitted(b) for b in so), sum(readmitted(b) for b in sc)
        if ro and rc:
            xs.append((math.log((ro / len(so)) / (rc / len(sc))), 1 / ro - 1 / len(so) + 1 / rc - 1 / len(sc)))
    wsum = sum(1 / v for _, v in xs)
    mean = sum(x / v for x, v in xs) / wsum
    q = sum((x - mean) ** 2 / v for x, v in xs)
    out['p_interaction']['primary reason'] = float(chi2.sf(q, len(xs) - 1))
    return out


def theta_post(B):
    T = [b for b in B if W.analysed(b)]
    rates = {}
    for a in ('outreach', 'usual care'):
        A = [b for b in T if b['arm'] == a and not (b['readm_t'] is not None and b['readm_t'] <= b['landmark'])]
        rates[a] = sum(readmitted(b) for b in A) / len(A)
    return 1 - rates['outreach'] / rates['usual care'], rates


def ask_a(B):
    """By risk reason on the discharge record: the usual-care readmission rate and the risk ratio for outreach."""
    T = [b for b in B if W.analysed(b)]
    out = {}
    for r in W.REASONS:
        o = [b for b in T if b['arm'] == 'outreach' and r in b['reasons']]
        c = [b for b in T if b['arm'] == 'usual care' and r in b['reasons']]
        ro, rc = sum(readmitted(b) for b in o), sum(readmitted(b) for b in c)
        out[r] = dict(no=len(o), ro=ro, nc=len(c), rc=rc, rate_c=round(100.0 * rc / len(c), 1),
                      rr=round((ro / len(o)) / (rc / len(c)), 2), rr_exact=(ro / len(o)) / (rc / len(c)))
    return out


def ask_b(B, contact_rows):
    T = {b['nhs']: b for b in B if W.analysed(b) and b['arm'] == 'outreach'}
    mother_of = {}
    for b in T.values():
        mother_of[b['mother']] = b['nhs']
    seen = set()
    hv, tel = {}, {}
    for c in contact_rows:
        if c['cid'] in seen:
            continue
        seen.add(c['cid'])
        baby = c['nhs'] if c['nhs'] in T else mother_of.get(c['nhs'])
        if baby is None:
            continue
        b = T[baby]
        if not (b['disch'] < c['t'] <= b['disch'] + dt.timedelta(days=28)):
            continue
        # a visit made and a call that reached the family; attempts that failed are neither, whatever code the
        # application gave them
        if c['what'] == 'HV' and c['done']:
            hv[baby] = hv.get(baby, 0) + 1
        elif c['what'] == 'TEL' and c['done']:
            tel[baby] = tel.get(baby, 0) + 1
    out = {}
    for r in W.REASONS:
        babies = [n for n, b in T.items() if r in b['reasons']]
        out[r] = (round(sum(hv.get(n, 0) for n in babies) / len(babies), 2), round(sum(tel.get(n, 0) for n in babies) / len(babies), 2), len(babies))
    return out


def call(B):
    P = {u: W.planning(B, u) for u in W.FIVE}
    all_r = [sum(readmitted(b) for b in P[u]) for u in W.FIVE]
    post = [sum(reached(b) for b in P[u]) for u in W.FIVE]
    posts, quotas = largest_remainder(post)
    th, rates = theta_post(B)
    total = th * sum(post)
    st = trial_stats(B)
    itt = 1 - st['rr']
    rep = trial_stats(B, report_missed(B))
    naive_posts, naive_q = largest_remainder(all_r)
    naive_total = (1 - rep['rr']) * sum(all_r)          # the default path reads the report's risk ratio
    return dict(eligible=[len(P[u]) for u in W.FIVE], readmissions=all_r, reached=post, posts=posts, quotas=quotas,
                theta=th, total=total, total_rounded=nearest(total, TOTAL_STEP), itt=itt, naive_posts=naive_posts,
                naive_total=naive_total, naive_total_rounded=nearest(naive_total, TOTAL_STEP), rates=rates,
                report_rr=rep['rr'], report_total=(1 - rep['rr']) * sum(post), theta_pct=int(round(100 * th)))


def main(B, counts):
    import deliver
    os.makedirs(GOLD, exist_ok=True)
    C = call(B)
    A = ask_a(B)
    contact_rows = R.contacts(B)
    Bk = ask_b(B, contact_rows)
    st = trial_stats(B, report_missed(B))
    figs = {
        'call': {'posts': dict(zip(W.FIVE, C['posts'])), 'readmissions_avoided_2027_28': C['total_rounded']},
        'units': {u: W.NAME[u] for u in W.FIVE},
        'eligible': dict(zip(W.FIVE, C['eligible'])), 'eligible_total': sum(C['eligible']),
        'components': {'trial_post_call_reduction_pct': round(100 * C['theta']), 'trial_itt_reduction_pct': round(100 * C['itt']),
                       'reached_share_pct': {u: round(100.0 * r / a) for u, r, a in zip(W.FIVE, C['reached'], C['readmissions'])}},
        'default_path': {'posts': dict(zip(W.FIVE, C['naive_posts'])), 'readmissions_avoided': C['naive_total_rounded']},
        'trial': {'randomised': st['randomised'], 'withdrawn': st['withdrawn'], 'analysed_outreach': st['outreach']['n'],
                  'analysed_usual_care': st['usual care']['n'], 'rr': round(st['rr'], 2)},
        'ask_a': {r: {'usual_care_rate_pct': A[r]['rate_c'], 'risk_ratio': A[r]['rr'], 'outreach_babies': A[r]['no'],
                      'outreach_readmitted': A[r]['ro'], 'usual_care_babies': A[r]['nc'], 'usual_care_readmitted': A[r]['rc']}
                  for r in W.REASONS},
        'ask_b': {r: {'home_visits': Bk[r][0], 'calls': Bk[r][1]} for r in W.REASONS},
        'reason_labels': R.REASON_LABEL,
        'counts': counts,
        'constants': {'posts': POSTS, 'total_step': TOTAL_STEP, 'window_days': 28, 'planning_basis': '1 October 2025 to 30 September 2026'},
    }
    with open(os.path.join(HERE, 'figures.json'), 'w') as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    deliver.workbook(os.path.join(GOLD, 'outreach_posts_2027-28.xlsx'), C, A, Bk)
    deliver.chart(os.path.join(GOLD, 'outreach_posts_by_unit.svg'), C)
    return C, A, Bk
