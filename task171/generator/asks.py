"""The asks' golden figures, reconstructed from the pack the way the SAP and the systems' records support, and the
ladder each ask's natural wrong handlings land on (the ladder never ships)."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

import numpy as np

import common as K
import pack_read as PR

INFECTION_SOC = "Infections and infestations"
SERIOUS_INFECTION_PTS = None
IRR_PTS = ("Infusion related reaction", "Hypersensitivity", "Urticaria", "Flushing", "Chills", "Infusion site reaction")


def first_last_infusion(P):
    fi, li = {}, {}
    for (ss, vis), r in P['inf'].items():
        d = dt.date.fromisoformat(r['infusion_start_local'][:10])
        fi[ss] = min(fi.get(ss, d), d)
        li[ss] = max(li.get(ss, d), d)
    return fi, li


def last_contact(P, target):
    """the week-12 visit date, or the early-termination visit, from the efficacy and laboratory records"""
    out = {}
    for r in PR.rd(target, K.VISITS):
        d = dt.date.fromisoformat(r['visit_date'])
        out[r['site_subject']] = max(out.get(r['site_subject'], d), d)
    return out


def impute_onset(s, first_inf):
    """SAP 6.2: an unknown day is the first of the month, unless the first infusion fell in that month, when it is
    the date of the first infusion"""
    if s.endswith('UN'):
        y, m = int(s[:4]), int(s[5:7])
        if first_inf.year == y and first_inf.month == m:
            return first_inf
        return dt.date(y, m, 1)
    return dt.date.fromisoformat(s)


VIS_ORDER = {"Screening": 0, "Week 4": 1, "Week 8": 2, "Week 12": 3, "Early termination": 3}


def episodes(rows, how):
    """adverse event episodes from the review log. The golden chains a patient's records of one preferred term from
    review to review while the event is ongoing, and takes the form as it stood at the latest review (its onset, any
    serious record); rival handlings key the records by what they carry"""
    eps = {}
    if how in ('golden', 'first_onset'):
        rows = sorted(rows, key=lambda r: (r['site_subject'], VIS_ORDER[r['recorded_at_visit']], int(r['ae_number'])))
        open_ = {}
        n = 0
        for r in rows:
            k = (r['site_subject'], r['preferred_term'])
            e = open_.get(k)
            if e is None or e['last_vis'] >= VIS_ORDER[r['recorded_at_visit']]:
                n += 1
                e = eps[n] = dict(ss=r['site_subject'], pt=r['preferred_term'], soc=r['system_organ_class'],
                                  onset=r['onset_date'], serious=False, first_serious=r['serious'] == 'Y')
            elif how == 'golden':
                e['onset'] = r['onset_date']
            e['last_vis'] = VIS_ORDER[r['recorded_at_visit']]
            e['serious'] = e['serious'] or r['serious'] == 'Y'
            if r['ongoing'] == 'Y':
                open_[k] = e
            else:
                open_.pop(k, None)
        return list(eps.values())
    for r in rows:
        ss = r['site_subject']
        if how == 'records':
            key = (ss, r['ae_number'])
        elif how == 'by_term':
            key = (ss, r['preferred_term'])
        else:   # onset_key and the rest: patient, term and onset as recorded
            key = (ss, r['preferred_term'], r['onset_date'])
        e = eps.setdefault(key, dict(ss=ss, pt=r['preferred_term'], soc=r['system_organ_class'], onset=r['onset_date'],
                                     serious=False, first_serious=r['serious'] == 'Y'))
        e['serious'] = e['serious'] or r['serious'] == 'Y'
    return list(eps.values())


def ask_a(P, target, how='golden'):
    rows = PR.rd(target, K.AE)
    fi, li = first_last_infusion(P)
    lc = last_contact(P, target)
    base = 'golden' if how in ('first_record', 'irr_term_only', 'irr_list_any_day') else how
    eps = episodes(rows, base)
    infd = {}
    for (s_, v_), rr in P['inf'].items():
        infd.setdefault(s_, set()).add(dt.date.fromisoformat(rr['infusion_start_local'][:10]))
    out = {}
    for arm in ('dovikizumab', 'placebo'):
        subj = [ss for ss, a in P['arm'].items() if a == arm]
        sset = set(subj)
        py = 0.0
        for ss in subj:
            if ss not in fi:
                continue
            end = min(li[ss] + dt.timedelta(days=30), lc.get(ss, li[ss]))
            py += ((end - fi[ss]).days + 1) / 365.25
        def te(e):
            ss = e['ss']
            if ss not in fi:
                return False
            on = impute_onset(e['onset'], fi[ss])
            end = min(li[ss] + dt.timedelta(days=30), lc.get(ss, li[ss]))
            return fi[ss] <= on <= end
        def on_inf(e):
            on = impute_onset(e['onset'], fi[e['ss']])
            return any(0 <= (on - d).days <= 1 for d in infd.get(e['ss'], ()))
        ser_flag = (lambda e: e['first_serious']) if how == 'first_record' else (lambda e: e['serious'])
        mine = [e for e in eps if e['ss'] in sset and e['ss'] in fi]
        si = [e for e in mine if e['soc'] == INFECTION_SOC and ser_flag(e) and te(e)]
        if how == 'irr_term_only':
            irr = [e for e in mine if e['pt'] == "Infusion related reaction" and te(e)]
        elif how == 'irr_list_any_day':
            irr = [e for e in mine if e['pt'] in IRR_PTS and te(e)]
        else:
            irr = [e for e in mine if e['pt'] in IRR_PTS and te(e) and on_inf(e)]
        out[arm] = dict(pts_si=len({e['ss'] for e in si}), pts_irr=len({e['ss'] for e in irr}), events_si=len(si),
                        py=py, rate_si=100 * len(si) / py)
    return out


def ask_b(P, target, how='golden'):
    """treatment-emergent ADA incidence at weeks 4, 8 and 12 by arm, per cent of patients with an evaluable baseline
    and an evaluable sample at the visit. The golden takes each draw (patient and visit) whole, whichever aliquot a
    tier was run on, and each tier's result from its latest accepted run; rival handlings key the tiers by sample or
    ignore the run outcome"""
    res = PR.rd(target, K.ADA)
    runs = {r['run_id']: r for r in PR.rd(target, K.ADA_RUNS)}
    by = defaultdict(list)
    if how == 'golden':
        # a draw is the patient's blood on a collection date, whichever aliquot and manifest carried it; its visit is
        # the scheduled label one of its aliquots bears
        lab = defaultdict(set)
        for r in res:
            if r['manifest_visit'] != 'Unscheduled':
                lab[(r['randomisation_number'], r['collection_date'])].add(r['manifest_visit'])
        for r in res:
            v = lab.get((r['randomisation_number'], r['collection_date']))
            if v:
                by[(r['randomisation_number'], min(v))].append(r)
    else:
        key = (lambda r: (r['sample_id'],)) if how in ('per_sample', 'latest', 'first', 'any') else (lambda r: ())
        for r in res:
            if r['manifest_visit'] != 'Unscheduled':
                by[(r['randomisation_number'], r['manifest_visit']) + key(r)].append(r)
    status = {}
    for k, rr in by.items():
        tiers = {}
        for t in ("screening", "confirmatory", "titer", "neutralising"):
            cand = [r for r in rr if r['tier'] == t]
            if how in ('golden', 'per_sample'):
                cand = [r for r in cand if runs[r['run_id']]['plate_acceptance'] == 'accepted']
            cand.sort(key=lambda r: (runs[r['run_id']]['run_date'], r['run_id']))
            if how == 'first':
                cand = cand[:1]
            if how == 'any':
                tiers[t] = cand
            elif cand:
                tiers[t] = [cand[-1]]
        if 'screening' not in tiers or not tiers['screening']:
            if how in ('golden',):
                continue
        def pos_of(sc, cf):
            return float(sc['result']) >= 1.32 and cf is not None and float(cf['result']) >= 18.5
        scs = tiers.get('screening', [])
        cfs = tiers.get('confirmatory', [])
        pos = any(pos_of(sc, cf) for sc in scs for cf in cfs) if scs else False
        titer = max([int(t['result'].split(':')[1]) for t in tiers.get('titer', [])] or [0]) if pos else 0
        sk = k[:2]
        if not scs and how != 'golden':
            # a sample with no screening result of its own is not a result for the visit
            continue
        old = status.get(sk)
        if old is None or (pos and not old[0]) or (pos == old[0] and titer > old[1]):
            status[sk] = (pos, titer)
    out = {}
    for arm in ('dovikizumab', 'placebo'):
        rnos = [rno for rno, ss in P['rno2ss'].items() if P['arm'][ss] == arm]
        out[arm] = {}
        for vis in ('Week 4', 'Week 8', 'Week 12'):
            n = te = 0
            for rno in rnos:
                b = status.get((rno, 'Week 0'))
                x = status.get((rno, vis))
                if b is None or x is None:
                    continue
                n += 1
                if (not b[0] and x[0]) or (b[0] and x[0] and x[1] >= 4 * b[1]):
                    te += 1
            out[arm][vis] = dict(n=n, te=te, pct=100.0 * te / n if n else 0.0)
    return out


def ask_c(P, target, how='golden'):
    """patients in symptomatic remission on the e-diary at weeks 6, 8 and 10 by arm: the device a patient held on each
    diary date, the patient's last entry for each date, the three most recent dates with an entry in the seven days
    before the reference day"""
    disp = PR.rd(target, K.DEVICES)
    ent = PR.rd(target, K.DIARY)
    # a registration the trial database does not know is the patient who handed the same handset over that day
    known = set(P['arm'])
    link = {}
    if how != 'drop_unmatched':
        changed = True
        while changed:
            changed = False
            for r in disp:
                u = r['site_subject']
                if u in known or u in link:
                    continue
                for q in disp:
                    w = link.get(q['site_subject'], q['site_subject'])
                    if q['handset_serial'] == r['handset_serial'] and q['returned_on'] == r['dispensed_on'] and w in known:
                        link[u] = w
                        changed = True
                        break
    held = defaultdict(list)
    for r in disp:
        held[r['handset_serial']].append((r['dispensed_on'], r['returned_on'], link.get(r['site_subject'], r['site_subject'])))
    latest_holder = {s: sorted(v)[-1][2] for s, v in held.items()}
    day = {}
    for r in ent:
        ser, dd = r['handset_serial'], r['diary_date']
        if how == 'current_holder':
            owners = [latest_holder[ser]]
        elif how == 'all_holders':
            owners = [h[2] for h in held[ser]]
        else:
            owners = [h[2] for h in held[ser] if h[0] <= dd < h[1]]
        for ss in owners:
            k = (ss, dd)
            if how == 'first_entry':
                if k not in day or r['recorded_at'] < day[k][0]:
                    day[k] = (r['recorded_at'], int(r['stool_frequency']), int(r['rectal_bleeding']))
            else:
                if k not in day or r['recorded_at'] > day[k][0]:
                    day[k] = (r['recorded_at'], int(r['stool_frequency']), int(r['rectal_bleeding']))
    rand = {ss: dt.date.fromisoformat(r) for ss, r in ((r_['site_subject'], r_['randomised_on']) for r_ in PR.rd(target, K.RAND))}
    fi, li = first_last_infusion(P)
    lc = last_contact(P, target)
    out = {}
    for arm in ('dovikizumab', 'placebo'):
        out[arm] = {}
        for wk, ref in K.DIARY_WEEKS:
            n = rem = 0
            for ss, a in P['arm'].items():
                if a != arm or ss not in fi:
                    continue
                d0 = fi[ss]
                refd = d0 + dt.timedelta(days=ref)
                if lc.get(ss, d0) < refd:
                    continue
                n += 1
                got = []
                for back in range(1, 8):
                    k = (ss, str(refd - dt.timedelta(days=back)))
                    if k in day:
                        got.append(day[k])
                    if len(got) == 3:
                        break
                if len(got) < 3:
                    continue
                sfm = np.mean([g[1] for g in got])
                rbm = np.mean([g[2] for g in got])
                normal = int(P['base'][ss]['normal_stool_frequency'])
                ex = int(np.floor(sfm + 0.5)) - normal
                sfs = 0 if ex <= 0 else (1 if ex <= 2 else (2 if ex <= 4 else 3))
                rbs = int(np.floor(rbm + 0.5))
                rem += int(sfs <= 1 and rbs == 0)
            out[arm][wk] = dict(n=n, rem=rem)
    return out
