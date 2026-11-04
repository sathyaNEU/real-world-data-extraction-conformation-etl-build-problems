"""The records the organisations keep, derived from the clean truth with each system's own forms (Layer 1).

Every function returns rows; build.py writes them. Each producing system gets its own random stream so a change
in one file never moves another.
"""
import datetime as dt
import numpy as np
import world as W

SITE_A = {'RRI': 'RVY', 'KUH': 'KLW'}                        # Ravensby and Kellingworth maternity system codes
SITE_B = {'SDH': 'Sedgefold', 'SAH': "St Aldric's", 'WCH': 'Wennby', 'CFH': 'Copperfield'}
OFFICE = {'RRI': 'RVY01', 'KUH': 'KLW02', 'SDH': 'SDF03', 'SAH': 'STA04', 'WCH': 'WNB05', 'CFH': 'CPF06'}
REASON_LABEL = {'LPT': 'Late preterm (35 to 36 weeks)', 'BFP': 'Breastfed first baby', 'EDC': 'Discharged under 18 hours',
                'WTL': 'Weight loss 8% or more', 'VJD': 'Visible jaundice at discharge', 'SPH': 'Sibling needed phototherapy'}
FEED_A = {'breast': 'Breast', 'formula': 'Formula', 'mixed': 'Mixed'}
FEED_B = {'breast': 'Exclusive breast milk', 'formula': 'Formula', 'mixed': 'Breast and formula'}
CAUSE_DX = {'jaundice': ['P59.9', 'P59.9', 'P59.9', 'P59.8', 'P55.1'], 'feeding': ['P92.5', 'P92.9', 'R63.4', 'P92.6'],
            'infection': ['P39.9', 'R50.9', 'P38', 'A41.9', 'J21.9'], 'other': ['R11.1', 'P78.3', 'R06.8', 'Z03.8', 'P96.8']}


def fmt_nhs_spaced(n):
    return '%s %s %s' % (n[:3], n[3:6], n[6:])


def transpose(n, rng):
    """A paper notification's NHS number keyed with two adjacent digits swapped (it then fails its check digit)."""
    for _ in range(20):
        i = int(rng.integers(0, 9))
        if n[i] != n[i + 1]:
            return n[:i] + n[i + 1] + n[i] + n[i + 2:]
    return n


APP_UPDATE = dt.datetime(2025, 1, 6)      # the outreach tablet app gained the no-access and no-answer codes
EXTRACT = dt.datetime(2026, 11, 2, 7, 40)  # every extract in the planning pack was pulled at this time


def mother_numbers(B):
    """Mothers' hospital numbers at the Sedgefold and Wennby trust (their own registrations)."""
    rng = np.random.default_rng([W.SEED, 405])
    out = {}
    n = 300118
    letters = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    for b in sorted(B, key=lambda x: (x['birth'], x['mother'])):
        if W.SYSTEM[b['unit']] == 'B' and b['mother'] not in out:
            n += int(rng.integers(1, 6))
            out[b['mother']] = 'SW%06d%s' % (n, letters[(n * 7) % 23])
    return out


def admissions(B):
    """Every admission of a baby under six weeks old to the six hospitals, as each trust's PAS records it."""
    rng = np.random.default_rng([W.SEED, 401])
    mum_no = mother_numbers(B)
    rows = []
    cross = {}                      # (nhs) -> number registered at the other trust
    nxt = {'A': 5120451, 'B': 640118}
    letters = 'ABCDEFGHJKLMNPRSTUVWXYZ'

    def number_at(b, site):
        trust = W.SYSTEM[site]
        if trust == W.SYSTEM[b['unit']]:
            return b['hosp']
        key = (b['nhs'], trust)
        if key not in cross:
            nxt[trust] += int(rng.integers(3, 40))
            cross[key] = ('RK%07d' % nxt[trust]) if trust == 'A' else ('SW%06d%s' % (nxt[trust], letters[nxt[trust] % 23]))
        return cross[key]

    for b in B:
        events = []
        if b['readm_t'] is not None:
            events.append(('readm', b['readm_t']))
        if b['late_t'] is not None:
            events.append(('late', b['late_t']))
        if b['planned_t'] is not None:
            events.append(('planned', b['planned_t']))
        for kind, t in events:
            u = b['unit']
            x = rng.random()
            if kind == 'planned':
                site = u if u != 'WCH' else 'SDH'
            elif x < 0.80:
                site = u if u != 'WCH' or rng.random() < 0.6 else 'SDH'
            elif x < 0.92:
                site = 'RRI' if u != 'RRI' else 'KUH'
            else:
                site = 'KUH' if u != 'KUH' else 'RRI'
            cause = b['cause'] if kind == 'readm' else ('other' if kind == 'late' else None)
            if kind == 'planned':
                method, ward, dx = rng.choice(['12', '13']), 'Paediatric day unit', str(rng.choice(['Q38.1', 'Q65.8', 'N47']))
                los = 0.3
            else:
                method = str(rng.choice(['21', '22', '28'], p=[0.46, 0.14, 0.40]))
                if cause == 'jaundice':
                    ward = str(rng.choice(['Postnatal ward', 'Paediatric ward', 'Neonatal unit'], p=[0.45, 0.35, 0.20]))
                elif cause == 'infection':
                    ward = str(rng.choice(['Paediatric ward', 'Neonatal unit'], p=[0.6, 0.4]))
                else:
                    ward = str(rng.choice(['Paediatric ward', 'Postnatal ward', 'Neonatal unit'], p=[0.6, 0.25, 0.15]))
                dx = str(rng.choice(CAUSE_DX[cause]))
                los = float(np.clip(rng.gamma(2.0, 0.9), 0.2, 9.0))
            if ward == 'Postnatal ward' and site in ('WCH',):
                ward = 'Paediatric ward'
            if site == 'WCH' and ward == 'Neonatal unit':
                ward = 'Paediatric ward'
            nhs = b['nhs']
            if W.SYSTEM[site] == 'B' and rng.random() < 0.015:
                nhs = ''
            elif W.SYSTEM[site] == 'A' and rng.random() < 0.005:
                nhs = ''
            disc = t + dt.timedelta(days=los)
            hosp = number_at(b, site)
            # Copperfield's PAS admits a baby who comes back to its postnatal ward under the mother's record
            if site == 'CFH' and ward == 'Postnatal ward' and kind != 'planned':
                nhs, hosp = b['mother'], mum_no[b['mother']]
            rows.append(dict(site=site, ward=ward, nhs=nhs, hosp=hosp, adm=t, method=method, dx=dx,
                             disc=disc.replace(second=0, microsecond=0), baby=b['nhs'], kind=kind))
            # a readmission at a smaller unit moved on to the Ravensby neonatal unit the same day
            if kind == 'readm' and site in ('SDH', 'SAH', 'WCH') and rng.random() < 0.07:
                t2 = (t + dt.timedelta(hours=float(rng.uniform(3, 10)))).replace(second=0, microsecond=0)
                rows[-1]['disc'] = t2
                rows.append(dict(site='RRI', ward='Neonatal unit', nhs=b['nhs'] if rng.random() < 0.97 else '',
                                 hosp=number_at(b, 'RRI'), adm=t2, method='81', dx=dx,
                                 disc=(t2 + dt.timedelta(days=float(rng.uniform(1, 6)))).replace(second=0, microsecond=0),
                                 baby=b['nhs'], kind='transfer'))
    rows.sort(key=lambda r: (r['adm'], r['site'], r['hosp']))
    rows = [r for r in rows if r['adm'] <= EXTRACT]
    for r in rows:
        if r['disc'] > EXTRACT:                       # still in hospital when the extract ran
            r['disc'] = None
    return rows, cross


def notifications(B):
    """The community midwifery office's receipt log: one row per notification it received."""
    rng = np.random.default_rng([W.SEED, 402])
    rows = []
    ref = 2400317
    for b in B:
        n = b['nhs']
        if b['route'] == 'paper' and rng.random() < 0.025:
            n = transpose(n, rng)
        rows.append(dict(t=b['recv'], site=b['unit'], nhs=n, hosp=b['hosp'], kind='Discharge home', baby=b['nhs']))
        if rng.random() < 0.02:
            t2 = (b['recv'] + dt.timedelta(hours=float(rng.uniform(5, 140)))).replace(microsecond=0)
            rows.append(dict(t=t2, site=b['unit'], nhs=b['nhs'], hosp=b['hosp'], kind='Amended', baby=b['nhs']))
    rows.sort(key=lambda r: (r['t'], r['site'], r['hosp']))
    out = []
    for r in rows:
        ref += int(rng.integers(1, 4))
        r['ref'] = 'CMO-%07d' % ref
        out.append(r)
        if rng.random() < 0.003:                      # the interface sent the same message twice
            out.append(dict(r))
    return [r for r in out if r['t'] <= EXTRACT]


def contacts(B):
    """The trial's outreach contact log (the nurses' tablet app): calls to a parent are filed under the number of
    the person phoned; the app re-sends a contact when a sync is interrupted."""
    rng = np.random.default_rng([W.SEED, 403])
    rows = []
    cid = 11800
    for b in B:
        # the trial's outreach arm, and from April 2026 the service Copperfield kept for every eligible baby
        if not ((b['trial'] and b['arm'] == 'outreach' and not b['withdrawn'])
                or (b['unit'] == 'CFH' and b['service'] and not b['trial'])):
            continue
        end = b['disch'] + dt.timedelta(days=28)
        stop = b['readm_t'] if b['readm_t'] is not None else end
        evs = [('TEL', b['call1'])]
        d1 = b['call1'] + dt.timedelta(days=float(rng.uniform(0.6, 2.0)))
        hv = dt.datetime(d1.year, d1.month, d1.day, int(rng.integers(9, 16)), int(rng.integers(0, 60)))
        if rng.random() < 0.06:
            evs.append(('NA', hv))
            hv = hv + dt.timedelta(days=1)
        evs.append(('HV', hv))
        rs = set(b['reasons'])
        p2 = min(0.88, 0.20 + 0.36 * ('LPT' in rs) + 0.31 * ('WTL' in rs) + 0.24 * ('VJD' in rs) + 0.09 * ('SPH' in rs))
        if rng.random() < p2:
            v2 = b['disch'] + dt.timedelta(days=float(rng.uniform(4, 9)))
            evs.append(('HV', dt.datetime(v2.year, v2.month, v2.day, int(rng.integers(9, 16)), int(rng.integers(0, 60)))))
            if 'LPT' in rs and rng.random() < 0.32:
                v3 = b['disch'] + dt.timedelta(days=float(rng.uniform(10, 16)))
                evs.append(('HV', dt.datetime(v3.year, v3.month, v3.day, int(rng.integers(9, 16)), int(rng.integers(0, 60)))))
        feed = 'BFP' in rs or 'WTL' in rs
        for day, p in ((3, 0.66 + 0.22 * feed), (7, 0.55 + 0.18 * feed + 0.12 * ('LPT' in rs)),
                       (14, 0.36 + 0.16 * ('LPT' in rs) + 0.12 * ('WTL' in rs)), (21, 0.22 + 0.15 * ('LPT' in rs))):
            if rng.random() < p:
                c = b['disch'] + dt.timedelta(days=day + float(rng.uniform(-0.6, 0.8)))
                evs.append(('TEL', dt.datetime(c.year, c.month, c.day, int(rng.integers(9, 18)), int(rng.integers(0, 60)))))
        if rng.random() < 0.05:                       # a family that rang the line back after day 28
            c = b['disch'] + dt.timedelta(days=float(rng.uniform(28.5, 34)))
            evs.append(('TEL', dt.datetime(c.year, c.month, c.day, int(rng.integers(9, 18)), int(rng.integers(0, 60)))))
        nurse = int(rng.integers(1, 10))                # the baby's named outreach nurse
        for kind, t in sorted(evs, key=lambda e: e[1]):
            if t > stop and t <= end:
                continue                               # the baby was back in hospital
            cid += int(rng.integers(1, 5))
            who = b['nhs']
            done = True
            if kind == 'TEL' and rng.random() < 0.09:  # nobody answered
                done = False
            if kind == 'NA':
                done = False
            if kind == 'TEL' and rng.random() < 0.46:  # the nurse rang the mother's mobile
                who = b['mother']
            if kind == 'TEL':
                mins = int(np.clip(round(np.exp(np.log(11.0) + 0.45 * rng.standard_normal())), 4, 48)) if done else 1
            elif kind == 'HV':
                mins = int(np.clip(round(np.exp(np.log(52.0) + 0.24 * rng.standard_normal())), 26, 125))
            else:
                mins = int(np.clip(round(rng.gamma(2.2, 2.2)), 2, 12))
            # before the app update a failed contact could only be filed as an ordinary call or visit
            if not done:
                if t < APP_UPDATE:
                    code = 'TEL' if kind == 'TEL' else 'HV'
                else:
                    code = 'TNA' if kind == 'TEL' else 'NA'
            else:
                code = kind
            nn = nurse if rng.random() < 0.78 else int(rng.integers(1, 10))
            row = dict(cid='OC%06d' % cid, sync='S%05d' % int(rng.integers(10000, 99999)), nhs=who, t=t, kind=code,
                       nurse='ON%02d' % nn, mins=mins, baby=b['nhs'], done=done, what=kind)
            rows.append(row)
            if rng.random() < 0.02:                    # the tablet re-sent the contact after a broken sync
                dup = dict(row)
                dup['sync'] = 'S%05d' % int(rng.integers(10000, 99999))
                rows.append(dup)
    rows.sort(key=lambda r: (r['t'], r['cid'], r['sync']))
    return [r for r in rows if r['t'] <= EXTRACT]


def trial_lists(B):
    """The final randomisation list (analysed babies) and the interim list as at 31 December 2025."""
    rng = np.random.default_rng([W.SEED, 404])
    T = sorted([b for b in B if b['trial']], key=lambda b: (b['disch'], b['hosp']))
    final, interim = [], []
    sid = 0
    for b in T:
        sid += 1
        rec = dict(sid='COT-%04d' % sid, hosp=b['hosp'], nhs=b['nhs'], date=b['disch'].date(),
                   arm='Outreach' if b['arm'] == 'outreach' else 'Usual care',
                   reason=REASON_LABEL[b['reasons'][0]], baby=b['nhs'])
        if not b['withdrawn']:
            final.append(dict(rec, status='Analysed'))
        if b['disch'] < dt.datetime(2026, 1, 1):
            iv = dict(rec, status='Consented')
            interim.append(iv)
    # four arms keyed wrongly at the interim and corrected before the final list
    idx = sorted(rng.choice(len(interim), 4, replace=False))
    for i in idx:
        interim[i]['arm'] = 'Usual care' if interim[i]['arm'] == 'Outreach' else 'Outreach'
    return final, interim
