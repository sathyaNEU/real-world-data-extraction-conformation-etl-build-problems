"""The asks' event streams: adverse events, anti-drug antibodies, the e-diaries, labs, infusions and endoscopy.

Each draws from its own keyed stream. The truth every ask is graded on is computed here, on the world, before any
file is written (truth_*), so pack_read and the golden have something exact to meet."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K

INFECT = [("Nasopharyngitis", 0.060), ("Upper respiratory tract infection", 0.045), ("Urinary tract infection", 0.022),
          ("Gastroenteritis", 0.014), ("Influenza", 0.012), ("Herpes zoster", 0.005)]
SERIOUS = [("Pneumonia", 0.010), ("Clostridioides difficile colitis", 0.008), ("Cellulitis", 0.006), ("Sepsis", 0.003),
           ("Appendicitis", 0.002)]
OTHER = [("Headache", 0.07), ("Arthralgia", 0.04), ("Colitis ulcerative", 0.06), ("Fatigue", 0.035), ("Nausea", 0.03),
         ("Anaemia", 0.025), ("Pyrexia", 0.02), ("Rash", 0.015)]
IRR_RATE = {True: 0.020, False: 0.012}        # per infusion, active and placebo
REACTION_PTS = ["Infusion related reaction", "Hypersensitivity", "Urticaria", "Flushing", "Chills", "Infusion site reaction"]
REACTION_P = [0.45, 0.15, 0.12, 0.10, 0.10, 0.08]
AE_SALT = 11          # the keyed draws the adverse event world was chosen on (every Ask A rung outside the bin)
AE_SALT_EV = 8


def adverse_events(W):
    """episodes: patient, term, onset study day, end study day (None ongoing), serious (may turn serious later),
    infusion-related flag; records are written in pack.py, one per visit while ongoing"""
    r = K.rng('ae', AE_SALT_EV)
    eps = []
    for i in range(W.N):
        last = int(W.disc[i] or W.vis[i, 3])
        act = bool(W.act[i])
        # pre-treatment events (screening), some worsening after the first infusion
        if r.random() < 0.10:
            term = OTHER[int(r.integers(0, len(OTHER)))][0]
            on = -int(r.integers(2, 20))
            eps.append(dict(i=i, term=term, onset=on, end=on + int(r.integers(3, 40)), serious=False, sday=None, irr=False))
            if r.random() < 0.3:
                w = int(r.integers(3, 30))
                eps[-1]['end'] = w
                eps.append(dict(i=i, term=term, onset=w, end=w + int(r.integers(2, 20)), serious=False, sday=None,
                                irr=False, worsened=True))
        # infections and skin reactions already present in the screening period
        if r.random() < 0.09:
            term = [t for t, _ in INFECT][int(r.integers(0, len(INFECT)))] if r.random() < 0.6 else \
                ("Urticaria", "Hypersensitivity", "Flushing")[int(r.integers(0, 3))]
            on = -int(r.integers(2, 14))
            dur = int(r.integers(10, 60))
            ser = term in ("Gastroenteritis", "Urinary tract infection", "Influenza") and r.random() < 0.45
            sday = on + int(r.integers(3, 14)) if ser else None      # admitted to hospital after the screening visit
            eps.append(dict(i=i, term=term, onset=on, end=on + max(dur, (sday or on) - on + 3), serious=ser,
                            sday=sday, irr=False))
        for term, p in INFECT + SERIOUS + OTHER:
            lam = p * (1.25 if (act and (term, p) in INFECT) else 1.0) * last / 84
            n = r.poisson(lam)
            for _ in range(n):
                on = int(r.integers(1, last + 25))
                dur = int(r.gamma(2.0, 6.0)) + 1
                ser = (term, p) in SERIOUS
                sday = None
                if not ser and term in ("Gastroenteritis", "Urinary tract infection", "Influenza") and r.random() < 0.12:
                    ser = True
                    sday = on + int(r.integers(2, 8))       # hospitalised later: becomes serious
                    dur = max(dur, sday - on + 3)
                eps.append(dict(i=i, term=term, onset=on, end=on + dur, serious=ser, sday=sday if sday else (on if ser else None), irr=False))
        for k, dday in enumerate((0, 28, 56)):
            if W.disc[i] and dday > W.disc[i]:
                break
            if r.random() < IRR_RATE[act] * 1.6:
                term = REACTION_PTS[int(r.choice(len(REACTION_PTS), p=REACTION_P))]
                on = dday + int(r.random() < 0.3)
                eps.append(dict(i=i, term=term, onset=on, end=on + int(r.integers(0, 2)), serious=False, sday=None, irr=True))
        for term in ("Urticaria", "Pruritus", "Flushing", "Hypersensitivity"):
            if r.random() < 0.035 * last / 84:
                on = int(r.integers(1, last + 1))
                dur = int(r.integers(1, 6)) if r.random() < 0.6 else int(r.integers(8, 40))
                eps.append(dict(i=i, term=term, onset=on, end=on + dur, serious=False, sday=None, irr=False))
    # one patient cannot carry two concurrent events of one term: the investigator records one
    keep, last_end = [], {}
    for e in sorted(eps, key=lambda z: (z['i'], z['term'], z['onset'])):
        k = (e['i'], e['term'])
        if k in last_end and e['onset'] <= last_end[k]:
            continue
        last_end[k] = e['end']
        keep.append(e)
    # an event starting after the patient's last visit is never reviewed; one that turned serious after the last
    # review is on file as it stood then
    keep = [e for e in keep if e['onset'] <= int(W.disc[e['i']] or W.vis[e['i'], 3])]
    for e in keep:
        if e['serious'] and e['sday'] is not None and e['sday'] > ae_visits(W, e)[-1]:
            e['serious'], e['sday'] = False, None
    eps = sorted(keep, key=lambda z: (z['i'], z['onset'], z['term']))
    rp = K.rng('ae_partial', AE_SALT)
    for e in eps:
        rec = ae_visits(W, e)
        e['nrec'] = len(rec)
        e['partial'] = bool(rp.random() < 0.08)
        # a partial date is completed at a later review when the site obtains the source (outside records)
        e['completed'] = bool(e['partial'] and len(rec) > 1 and rp.random() < 0.6)
        # the first review entered a later date as onset (the hospital admission for an infection that became
        # serious, else the visit date); source verification corrects it at the next review
        e['mis_on'] = None
        u = rp.random()
        if not e['partial'] and len(rec) > 1:
            if e['serious'] and e['sday'] is not None and e['sday'] > e['onset'] + 1 and rec[0] >= e['sday']:
                if u < 0.6:
                    e['mis_on'] = e['sday']
            elif rec[0] - e['onset'] > 1 and u < (0.45 if e['term'] in REACTION_PTS or e['onset'] < 0 else 0.12):
                e['mis_on'] = rec[0]
    return eps


def ae_visits(W, e):
    """the reviews (study days) at which an episode is recorded: every visit from onset until it is resolved"""
    i = e['i']
    visits = [-14, 28, 56, int(W.vis[i, 3])]
    if W.disc[i]:
        visits = [v for v in visits if v <= W.disc[i]] + [int(W.disc[i])]
    rec = []
    for v in visits:
        if v >= e['onset']:
            rec.append(v)
            if e['end'] <= v:
                break
    return rec


def imputed_onset(W, e):
    """the onset day after SAP 6.2's partial-date rule, as a study day"""
    if not e.get('partial') or e.get('completed'):
        return e['onset']
    import datetime as _dt
    r0 = K.day_date(W.rday[e['i']])
    on = r0 + _dt.timedelta(days=int(e['onset']))
    first = _dt.date(on.year, on.month, 1)
    if r0.year == on.year and r0.month == on.month:
        first = r0
    return (first - r0).days


def exposure_years(W, i):
    """from the first infusion to the earlier of 30 days after the last infusion and the last study contact"""
    last_inf = max(d for d in (0, 28, 56) if not (W.disc[i] and d > W.disc[i]))
    last_contact = int(W.disc[i] or W.vis[i, 3])
    return (min(last_inf + 30, last_contact) + 1) / 365.25


def truth_ae(W, eps):
    out = {}
    for arm in ('dovikizumab', 'placebo'):
        m = W.act if arm == 'dovikizumab' else ~W.act
        idx = set(np.where(m)[0])
        def te(e):
            i = e['i']
            last_inf = max(d for d in (0, 28, 56) if not (W.disc[i] and d > W.disc[i]))
            on = imputed_onset(W, e)
            return on >= 0 and on <= last_inf + 30 and on <= int(W.disc[i] or W.vis[i, 3])
        si = [e for e in eps if e['i'] in idx and te(e) and e['serious'] and e['term'] in {t for t, _ in INFECT + SERIOUS}]
        def on_inf(e):
            infs = [d for d in (0, 28, 56) if not (W.disc[e['i']] and d > W.disc[e['i']])]
            return any(0 <= imputed_onset(W, e) - d <= 1 for d in infs)
        irr = [e for e in eps if e['i'] in idx and te(e) and e['term'] in REACTION_PTS and on_inf(e)]
        py = sum(exposure_years(W, i) for i in idx)
        out[arm] = dict(n=len(idx), pts_si=len({e['i'] for e in si}), pts_irr=len({e['i'] for e in irr}),
                        events_si=len(si), py=py, rate_si=100 * len(si) / py)
    return out


def ada(W):
    """per patient per visit (0, 4, 8, 12): true status (screen positive, confirmed, titer) and the runs it went
    through; baseline-positive patients carry pre-existing reactivity, treatment raises titers in some"""
    r = K.rng('ada')
    rows = []
    for i in range(W.N):
        pre = r.random() < 0.06
        pre_t = int(2 ** r.integers(1, 4)) * 10 if pre else 0          # titers 20 to 80
        induced = (not pre) and r.random() < (0.075 if W.act[i] else 0.012)
        boosted = W.act[i] and pre and r.random() < 0.35
        nab = induced and r.random() < 0.4
        on = int(r.choice([28, 56, 84]))
        for k, d in enumerate((0, 28, 56, 84)):
            if W.disc[i] and d > W.disc[i]:
                break
            pos = pre
            t = pre_t
            if induced and d >= on:
                pos, t = True, int(2 ** r.integers(1, 5)) * 10
            if boosted and d >= on:
                pos, t = True, pre_t * int(2 ** r.integers(2, 4))
            if pre and not boosted and d > 0 and r.random() < 0.3:
                t = pre_t * 2                                          # one dilution of assay noise
            rows.append(dict(i=i, visit=k, day=d, pos=pos, titer=t if pos else 0, nab=bool(nab and pos and d >= on)))
    return rows


def truth_ada(W, rows):
    base = {(x['i']): x for x in rows if x['visit'] == 0}
    out = {}
    for arm in ('dovikizumab', 'placebo'):
        m = W.act if arm == 'dovikizumab' else ~W.act
        out[arm] = {}
        for k in (1, 2, 3):
            ev = [x for x in rows if x['visit'] == k and m[x['i']]]
            te = 0
            for x in ev:
                b = base.get(x['i'])
                if b is None:
                    continue
                if (not b['pos']) and x['pos']:
                    te += 1
                elif b['pos'] and x['pos'] and x['titer'] >= 4 * b['titer']:
                    te += 1
            out[arm][k] = dict(n=len([x for x in ev if x['i'] in base]), te=te)
        out[arm]['nab'] = len({x['i'] for x in rows if m[x['i']] and x['nab']})
    return out


def diaries(W):
    """daily stool count and rectal bleeding score from 14 days before the first infusion to the week-12 visit;
    the trajectory follows the patient's course (remission onset near the core's healing onset)"""
    r = K.rng('diary')
    out = []
    for i in range(W.N):
        normal = int(W.sf_normal[i])
        base_excess = 3 + int(W.mmayo0[i] >= 8) + int(r.integers(0, 3))
        rb0 = 1 + int(r.random() < 0.6)
        heal = float(W.onset[i]) + r.normal(0, 4)
        rem, resp = bool(W.rem[i]), bool(W.resp[i])
        last = int(W.disc[i] or W.vis[i, 3])
        for d in range(-14, last + 1):
            if d > 0:
                f = 0.0 if d < heal else (1 - np.exp(-(d - heal) / 9.0))
            else:
                f = 0.0
            if rem:
                ex = base_excess * (1 - 0.95 * f)
                rb = rb0 * (1 - f)
            elif resp:
                ex = base_excess * (1 - 0.5 * f)
                rb = rb0 * (1 - 0.6 * f)
            else:
                ex = base_excess * (1 - 0.1 * f)
                rb = rb0 * (1 - 0.1 * f)
            sf = max(0, int(round(normal + ex + r.normal(0, 1.0))))
            rbs = int(np.clip(round(rb + r.normal(0, 0.35)), 0, 3))
            missed = r.random() < 0.08
            out.append(dict(i=i, day=d, sf=sf, rb=rbs, missed=missed))
    return out


def subscores(sf_mean, rb_mean, normal):
    ex = int(np.floor(sf_mean + 0.5)) - normal
    sfs = 0 if ex <= 0 else (1 if ex <= 2 else (2 if ex <= 4 else 3))
    rbs = int(np.floor(rb_mean + 0.5))
    return sfs, rbs


def truth_symptomatic(W, D):
    """symptomatic remission at study days 42, 56 and 70 (weeks 6, 8 and 10): the three most recent diary days with an entry in the
    seven days before the reference day, stool-frequency subscore at most 1 and rectal bleeding 0"""
    by = {}
    for x in D:
        if not x['missed']:
            by.setdefault(x['i'], {})[x['day']] = x
    out = {}
    for arm in ('dovikizumab', 'placebo'):
        m = W.act if arm == 'dovikizumab' else ~W.act
        out[arm] = {}
        for _, ref in K.DIARY_WEEKS:
            n_rem = 0
            n_ev = 0
            for i in np.where(m)[0]:
                if W.disc[i] and W.disc[i] < ref:
                    continue
                n_ev += 1
                days = [d for d in range(ref - 1, ref - 8, -1) if d in by.get(i, {})][:3]
                if len(days) < 3:
                    continue
                sfm = np.mean([by[i][d]['sf'] for d in days])
                rbm = np.mean([by[i][d]['rb'] for d in days])
                s, b = subscores(sfm, rbm, int(W.sf_normal[i]))
                n_rem += int(s <= 1 and b == 0)
            out[arm][ref] = dict(n=n_ev, rem=n_rem)
    return out
