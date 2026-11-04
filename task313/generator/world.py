"""task313 clean truth: babies discharged home from six maternity units, the community midwifery office's
receipt of each discharge notification, every admission of a young baby to the system's hospitals, and the
Copperfield outreach trial. Nothing here is mess: the pack writer (build.py) applies the Layer 1 forms.

Times are naive Europe/London wall-clock datetimes unless a name ends in _utc.
"""
import datetime as dt
import numpy as np
from zoneinfo import ZoneInfo

LONDON = ZoneInfo('Europe/London')
UTC = dt.timezone.utc

UNITS = ['RRI', 'KUH', 'SDH', 'SAH', 'WCH', 'CFH']
FIVE = UNITS[:5]
NAME = {'RRI': 'Ravensby Royal Infirmary', 'KUH': 'Kellingworth University Hospital', 'SDH': 'Sedgefold Hospital',
        'SAH': "St Aldric's Hospital", 'WCH': 'Wennby Community Hospital', 'CFH': 'Copperfield Hospital'}
SYSTEM = {'RRI': 'A', 'KUH': 'A', 'SDH': 'B', 'SAH': 'B', 'WCH': 'B', 'CFH': 'B'}

START = dt.datetime(2024, 3, 27)          # first births whose discharges fall in the record
REC_START = dt.datetime(2024, 4, 1)       # first discharge in the extracts
REC_END = dt.datetime(2026, 10, 31, 23, 59)
PLAN_START = dt.datetime(2025, 10, 1)     # planning basis: discharges in the twelve months to 30 September 2026
PLAN_END = dt.datetime(2026, 10, 1)
TRIAL_START = dt.datetime(2024, 4, 1)
TRIAL_END = dt.datetime(2026, 4, 1)       # randomised 1 April 2024 to 31 March 2026

BIRTHS = {'RRI': 6350, 'KUH': 5180, 'SDH': 3420, 'SAH': 2990, 'WCH': 2560, 'CFH': 3780}   # births a year
LOS_MED_H = {'RRI': 31.0, 'KUH': 29.0, 'SDH': 22.0, 'SAH': 24.0, 'WCH': 18.0, 'CFH': 21.0}
# readmission risk multiplier on the baseline by unit (case mix not captured by the recorded reasons)
UNIT_RISK = {'RRI': 1.10, 'KUH': 1.02, 'SDH': 0.97, 'SAH': 1.06, 'WCH': 0.93, 'CFH': 0.98}
# how each unit's discharge notification reaches the community office: (electronic at discharge, electronic
# when the midwife closes the record at the end of her shift, paper with the signed discharge summary by post)
ROUTE = {'RRI': (0.30, 0.18, 0.52), 'KUH': (0.86, 0.11, 0.03), 'SDH': (0.88, 0.10, 0.02),
         'SAH': (0.34, 0.18, 0.48), 'WCH': (0.68, 0.18, 0.14), 'CFH': (0.97, 0.03, 0.00)}
# England bank holidays in the record (no ward round, no internal post)
BANK = {dt.date(2024, 5, 6), dt.date(2024, 5, 27), dt.date(2024, 8, 26), dt.date(2024, 12, 25), dt.date(2024, 12, 26),
        dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21), dt.date(2025, 5, 5), dt.date(2025, 5, 26),
        dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 4, 3),
        dt.date(2026, 4, 6), dt.date(2026, 5, 4), dt.date(2026, 5, 25), dt.date(2026, 8, 31)}


def working(d):
    return d.weekday() < 5 and d not in BANK


def next_working(d):
    d = d + dt.timedelta(days=1)
    while not working(d):
        d = d + dt.timedelta(days=1)
    return d
REASONS = ['LPT', 'BFP', 'EDC', 'WTL', 'VJD', 'SPH']   # late preterm, breastfed first baby, early discharge,
                                                      # weight loss 8 per cent or more, visible jaundice,
                                                      # sibling needed phototherapy
THETA = 0.40           # the outreach service's cut in the readmission risk after its first home visit
READM_MED_D, READM_SIG = 2.3, 0.80   # days from discharge to an unplanned readmission (lognormal)
SEED = 313031


def to_utc(t):
    return t.replace(tzinfo=LONDON).astimezone(UTC).replace(tzinfo=None)


def nhs_number(rng):
    while True:
        d = list(rng.integers(0, 10, 9))
        d[0] = int(rng.integers(4, 7))
        s = sum(int(x) * (10 - i) for i, x in enumerate(d))
        c = 11 - s % 11
        if c == 11:
            c = 0
        if c == 10:
            continue
        return ''.join(str(x) for x in d) + str(c)


def baby_rows(u, rng, nhs_seen):
    """All babies of unit u discharged home in the record window, with every clean attribute."""
    out = []
    per_day = BIRTHS[u] / 365.25
    day = START
    while day < dt.datetime(2026, 11, 1):
        season = 1.0 + 0.06 * np.sin(2 * np.pi * (day.timetuple().tm_yday - 200) / 365.25)
        n = rng.poisson(per_day * season * 0.94)          # 94 per cent of births go home from the postnatal ward
        for _ in range(n):
            birth = day + dt.timedelta(minutes=int(rng.integers(0, 1440)))
            gest = int(rng.choice([35, 36, 37, 38, 39, 40, 41], p=[0.022, 0.040, 0.105, 0.205, 0.275, 0.243, 0.110]))
            gest_d = int(rng.integers(0, 7))
            first = rng.random() < 0.41
            feed = rng.choice(['breast', 'formula', 'mixed'], p=[0.47, 0.33, 0.20])
            los_h = float(np.clip(np.exp(np.log(LOS_MED_H[u]) + 0.55 * rng.standard_normal()), 5.0, 120.0))
            if gest <= 36:
                los_h = max(los_h, 48.0 + 24.0 * rng.random())
            disch = birth + dt.timedelta(hours=los_h)
            disch = disch.replace(second=0, microsecond=0)
            if not (REC_START <= disch <= REC_END):
                continue
            bw = int(np.clip(rng.normal(3400 - 190 * (40 - gest), 430), 1900, 5200))
            wloss = float(np.clip(rng.normal(5.6 if feed == 'breast' else 4.2, 2.3), 0.0, 13.0)) if los_h >= 20 else float(np.clip(rng.normal(2.8, 1.6), 0.0, 9.0))
            rs = []
            if gest <= 36:
                rs.append('LPT')
            if feed == 'breast' and first:
                rs.append('BFP')
            if los_h < 18:
                rs.append('EDC')
            if wloss >= 8.0:
                rs.append('WTL')
            if rng.random() < 0.052:
                rs.append('VJD')
            if rng.random() < 0.035:
                rs.append('SPH')
            mother = nhs_number(rng)
            twin = rng.random() < 0.0075
            for k in range(2 if twin else 1):
                nhs = nhs_number(rng)
                while nhs in nhs_seen:
                    nhs = nhs_number(rng)
                nhs_seen.add(nhs)
                rk = list(rs)
                if twin and 'LPT' not in rk and gest <= 37:
                    rk.append('LPT')
                bk = birth + dt.timedelta(minutes=int(rng.integers(6, 40))) if k == 1 else birth
                out.append(dict(unit=u, birth=bk, disch=disch, gest=gest, gest_d=gest_d, first=first, feed=str(feed),
                                bw=int(bw * (0.86 if twin else 1.0)), wloss=round(wloss, 1), reasons=rk, eligible=bool(rk),
                                nhs=nhs, mother=mother, multiple=twin))
        day += dt.timedelta(days=1)
    return out


def notification(u, b, rng):
    """When the community office received the unit's discharge notification, by the route it travelled."""
    pe, pl, pp = ROUTE[u]
    x = rng.random()
    t0 = b['disch']
    if x < pe:                                   # electronic, sent as the baby leaves the ward
        route = 'electronic'
        t = t0 + dt.timedelta(minutes=float(rng.gamma(1.6, 25.0)) + 3.0)
    elif x < pe + pl:                            # electronic, sent when the midwife closes the record
        route = 'end of shift'
        end = dt.datetime(t0.year, t0.month, t0.day, 20, 0) if t0.hour < 19 else dt.datetime(t0.year, t0.month, t0.day, 8, 0) + dt.timedelta(days=1)
        t = end + dt.timedelta(minutes=float(rng.uniform(5, 110)))
    else:                                        # paper: signed at the next weekday ward round, then internal post
        route = 'paper'
        d = t0.date()
        rnd = d if (working(d) and t0.hour < 9) else next_working(d)
        if rng.random() < 0.12:                  # the summary waited for a second round
            rnd = next_working(rnd)
        post = next_working(rnd)
        if rng.random() < 0.08:                  # a day longer in the post
            post = next_working(post)
        t = dt.datetime(post.year, post.month, post.day, 9, 0) + dt.timedelta(minutes=float(rng.uniform(0, 150)))
    t = t.replace(second=int(rng.integers(0, 60)), microsecond=0)
    return t, route


CALL_OPEN, CALL_LAST = 8, 19     # the outreach line phones families from 08:00; receipts after 19:00 wait


def first_call(b, rng):
    """The outreach service's first contact, a telephone call to the family: within about two hours of the
    office receiving the notification when it arrives between 08:00 and 19:00, otherwise early next morning."""
    r = b['recv']
    if CALL_OPEN <= r.hour < CALL_LAST:
        t = r + dt.timedelta(minutes=int(rng.integers(20, 150)))
    else:
        d = r.date() if r.hour < CALL_OPEN else r.date() + dt.timedelta(days=1)
        t = dt.datetime(d.year, d.month, d.day, 8, 0) + dt.timedelta(minutes=int(rng.integers(10, 150)))
    return t.replace(second=0, microsecond=0)


def landmark(b):
    """The earliest the service could reach the family: the office's receipt in calling hours, else 08:00 next."""
    r = b['recv']
    if CALL_OPEN <= r.hour < CALL_LAST:
        return r
    d = r.date() if r.hour < CALL_OPEN else r.date() + dt.timedelta(days=1)
    return dt.datetime(d.year, d.month, d.day, 8, 0)


OUT_SEED = 36         # the outcome streams (notifications, trial allocation, readmissions)


def build_babies():
    seen = set()
    babies = []
    for u in UNITS:
        r = np.random.default_rng([SEED, UNITS.index(u)])
        babies.extend(baby_rows(u, r, seen))
    babies.sort(key=lambda b: (b['birth'], b['unit'], b['nhs']))
    # hospital numbers: the Ravensby and Kellingworth trust issues RK + 7 digits, the Sedgefold and Wennby trust
    # SW + 6 digits + a letter; numbers run in registration order with gaps (other patients take numbers too)
    rh = np.random.default_rng([SEED, 77])
    nxt = {'A': 4208113, 'B': 518204}
    letters = 'ABCDEFGHJKLMNPRSTUVWXYZ'
    for b in babies:
        s = SYSTEM[b['unit']]
        nxt[s] += int(rh.integers(1, 9)) if s == 'A' else int(rh.integers(1, 7))
        if s == 'A':
            b['hosp'] = 'RK%07d' % nxt[s]
        else:
            b['hosp'] = 'SW%06d%s' % (nxt[s], letters[nxt[s] % 23])
    babies.sort(key=lambda b: (b['disch'], b['unit'], b['nhs']))
    # an NHS number belongs to one person: a mother's number never repeats a baby's or another mother's (twins
    # share their mother); the few draws that collided are re-issued from a stream of their own
    rm = np.random.default_rng([SEED, 78])
    baby_nums = {b['nhs'] for b in babies}
    taken, reissued = {}, {}
    for b in sorted(babies, key=lambda x: (x['birth'], x['unit'], x['nhs'])):
        m, event = b['mother'], (b['unit'], b['disch'])        # twins share their mother and their discharge
        if (m, event) in reissued:
            b['mother'] = reissued[(m, event)]
            continue
        if m in baby_nums or (m in taken and taken[m] != event):
            new = nhs_number(rm)
            while new in baby_nums or new in taken:
                new = nhs_number(rm)
            reissued[(m, event)] = new
            taken[new] = event
            b['mother'] = new
        else:
            taken.setdefault(m, event)
    return babies


def build_world(babies=None):
    if babies is None:
        babies = build_babies()
    else:
        babies = [dict(b) for b in babies]
    rn = np.random.default_rng([OUT_SEED, 101])
    rr = np.random.default_rng([OUT_SEED, 102])
    rt = np.random.default_rng([OUT_SEED, 103])
    for b in babies:
        b['recv'], b['route'] = notification(b['unit'], b, rn)
        b['landmark'] = landmark(b)
        # trial and service (multiple births were outside the trial's protocol)
        in_trial = (b['unit'] == 'CFH' and b['eligible'] and not b['multiple']
                    and TRIAL_START <= b['disch'] < TRIAL_END)
        b['trial'] = in_trial
        b['arm'] = None
        b['service'] = False
        if in_trial:
            b['arm'] = 'outreach' if rt.random() < 0.5 else 'usual care'
            b['service'] = b['arm'] == 'outreach'
        elif b['unit'] == 'CFH' and b['eligible'] and b['disch'] >= TRIAL_END:
            b['service'] = True
        b['call1'] = first_call(b, rt) if b['service'] else None
        # readmission within 28 days (potential, without the service)
        nr = len(b['reasons'])
        base = 0.0235 if nr == 0 else (0.052 if nr == 1 else 0.074)
        if 'LPT' in b['reasons']:
            base += 0.020
        p = base * UNIT_RISK[b['unit']]
        b['readm_t'] = None
        b['cause'] = None
        if rr.random() < p:
            days = float(np.exp(np.log(READM_MED_D) + READM_SIG * rr.standard_normal()))
            if days < 27.95:
                t = b['disch'] + dt.timedelta(days=days)
                b['readm_t'] = t.replace(second=0, microsecond=0)
                b['cause'] = str(rr.choice(['jaundice', 'feeding', 'infection', 'other'], p=[0.44, 0.31, 0.15, 0.10]))
        prevented = False
        if b['service'] and b['readm_t'] is not None and b['readm_t'] > b['call1']:
            prevented = rr.random() < THETA
        else:
            rr.random()
        b['prevented'] = prevented
        if prevented:
            b['readm_t'] = None
            b['cause'] = None
        # a later admission (day 28 to 41) that is not an outcome
        b['late_t'] = None
        if rr.random() < 0.006:
            b['late_t'] = (b['disch'] + dt.timedelta(days=float(rr.uniform(28.2, 41.0)))).replace(second=0, microsecond=0)
        # planned day-case admissions (not an outcome)
        b['planned_t'] = None
        if rr.random() < 0.004:
            b['planned_t'] = (b['disch'] + dt.timedelta(days=float(rr.uniform(3.0, 26.0)))).replace(hour=8, minute=30, second=0, microsecond=0)
    # consent withdrawn after randomisation: the final list drops the baby, the interim list still carries it
    rw = np.random.default_rng([OUT_SEED, 105])
    for b in babies:
        b['withdrawn'] = bool(b['trial'] and rw.random() < 0.006)
    # keep every admission clear of the 28th calendar day after the discharge date, where 28 days counted from the
    # discharge instant and 28 whole calendar days disagree: a readmission inside the 28 days moves a day earlier, a
    # later admission a day later, so both readings count the same events (no draw depends on these times)
    for b in babies:
        if b['readm_t'] is not None:
            b['readm_t'] = clear_day28(b['readm_t'], b['disch'])
        if b['late_t'] is not None:
            b['late_t'] = clear_day28(b['late_t'], b['disch'])
    return babies


def clear_day28(t, disch):
    if t.date() != disch.date() + dt.timedelta(days=28):
        return t
    return t - dt.timedelta(days=1) if t <= disch + dt.timedelta(days=28) else t + dt.timedelta(days=1)


def analysed(b):
    return b['trial'] and not b['withdrawn']


def planning(babies, u):
    return [b for b in babies if b['unit'] == u and b['eligible'] and PLAN_START <= b['disch'] < PLAN_END]


if __name__ == '__main__':
    W = build_world()
    print(len(W), 'babies')
    for u in UNITS:
        P = planning(W, u)
        R = [b for b in P if b['readm_t'] is not None]
        post = [b for b in R if b['readm_t'] > b['landmark']]
        print(u, len(P), len(R), len(post), round(len(post) / max(1, len(R)), 3))
