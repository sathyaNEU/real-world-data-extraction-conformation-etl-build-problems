"""The remote sites under the 2024 Operating Support Agreement: their sessions, the two operators' status
records and the district's maintenance approvals, with the clean truth of Support Year 2 (1 October 2025 to
30 September 2026, Pacific time).

Internal clock: every status spell is held in UTC; sessions are drawn in local daytime and converted. The
district's register was written when the agreement was signed in 2024: it carries each Northway site under the
station code Northway used then and each CFC site's charge points by the serials installed then. Northway
renumbered its stations in March 2025 and gave two of the freed codes to stations outside the district, and
added a second unit at Upper Mirren outside the agreement in May 2026; CFC replaced three charge points during
the year under new serials. CFC's remote sites ran a back-office fault from October 2025 to March 2026 that
split a session interrupted by a modem drop into two records, and CFC re-sent those months' records corrected.
"""
import datetime as dt
import numpy as np
import world as W

RNG = np.random.default_rng(W.SEED + 50)
H = dt.timedelta(hours=1)

# ---------------------------------------------------------------- clocks
def _second_sunday_march(y):
    d = dt.datetime(y, 3, 8)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d


def _first_sunday_nov(y):
    d = dt.datetime(y, 11, 1)
    while d.weekday() != 6:
        d += dt.timedelta(days=1)
    return d


def offset_local(t):
    """UTC offset (hours) of America/Vancouver at a valid local time t."""
    y = t.year
    return -7 if _second_sunday_march(y) + 2 * H <= t < _first_sunday_nov(y) + 2 * H else -8


def to_utc(t):
    return t - dt.timedelta(hours=offset_local(t))


def utc_offset(u):
    y = u.year
    return -7 if _second_sunday_march(y) + 10 * H <= u < _first_sunday_nov(y) + 9 * H else -8


def to_local(u):
    off = utc_offset(u)
    return u + dt.timedelta(hours=off), off


def fmt_local(u):
    t, off = to_local(u)
    return t.strftime('%Y-%m-%d %H:%M:%S') + ('-07:00' if off == -7 else '-08:00')


def fmt_utc(u):
    return u.strftime('%Y-%m-%dT%H:%M:%SZ')


# Support Year 2 quarters in Pacific time, held in UTC
_QL = [dt.datetime(2025, 10, 1), dt.datetime(2026, 1, 1), dt.datetime(2026, 4, 1), dt.datetime(2026, 7, 1),
       dt.datetime(2026, 10, 1)]
QUARTERS = [(to_utc(_QL[i]), to_utc(_QL[i + 1])) for i in range(4)]
QNAMES = ['Q1 (Oct to Dec 2025)', 'Q2 (Jan to Mar 2026)', 'Q3 (Apr to Jun 2026)', 'Q4 (Jul to Sep 2026)']
RATE = 0.085          # CAD per kWh delivered at a Schedule A charge point (Schedule B)
GATE = 0.95           # a quarter's availability below this withholds the quarter's support (Schedule B)

# ---------------------------------------------------------------- the sites
SITES = [
    dict(svrd='SV-RS-21', name='Wren Lake', addr='2210 Lakeshore Road, Wren Lake', op='CFC', code='CFC-0571',
         units=['CP2208815', 'CP2208843'], kw=50, lam=6.1, commissioned=dt.date(2024, 6, 18)),
    dict(svrd='SV-RS-22', name='Silverdale', addr='415 Main Street, Silverdale', op='NWE', code='NW-102',
         now='NW-138', units=['CA*NWE*E0102*1', 'CA*NWE*E0102*2'], kw=50, lam=5.2, commissioned=dt.date(2023, 11, 2)),
    dict(svrd='SV-RS-24', name='Beaton Creek', addr='88 Station Road, Beaton Creek', op='CFC', code='CFC-0588',
         units=['CP2210127'], kw=100, lam=4.4, commissioned=dt.date(2024, 8, 27)),
    dict(svrd='SV-RS-25', name='Holt Junction', addr='3190 Highway Services Road, Holt Junction', op='NWE',
         code='NW-107', now='NW-144', units=['CA*NWE*E0107*1', 'CA*NWE*E0107*2'], kw=50, lam=5.7,
         commissioned=dt.date(2023, 12, 6)),
    dict(svrd='SV-RS-27', name='Glenrae', addr='12 Community Hall Lane, Glenrae', op='CFC', code='CFC-0596',
         units=['CP2211068', 'CP2211094'], kw=50, lam=3.8, commissioned=dt.date(2024, 9, 10)),
    dict(svrd='SV-RS-28', name='Upper Mirren', addr='6005 Upper Mirren Road, Upper Mirren', op='NWE', code='NW-111',
         now='NW-111', units=['CA*NWE*E0111*1'], kw=75, lam=3.1, commissioned=dt.date(2024, 4, 15)),
]
SITE = {s['svrd']: s for s in SITES}
# CFC replaced three charge points during the year: (site, old serial, new serial, fault start local, swap local)
REPLACEMENTS = [
    ('SV-RS-27', 'CP2211068', 'CP2309562', dt.datetime(2026, 2, 21, 7, 48, 13), dt.datetime(2026, 2, 26, 10, 37, 41)),
    ('SV-RS-24', 'CP2210127', 'CP2312210', dt.datetime(2026, 5, 18, 18, 12, 52), dt.datetime(2026, 5, 21, 13, 5, 19)),
    ('SV-RS-21', 'CP2208843', 'CP2311847', dt.datetime(2026, 7, 9, 16, 21, 7), dt.datetime(2026, 7, 14, 8, 52, 30)),
]
# Northway's second unit at Upper Mirren, installed under its own programme, outside the agreement
UM_EXTRA = ('CA*NWE*E0111*2', dt.datetime(2026, 5, 19, 10, 14, 26), 50, 2.1)
# Northway stations outside the district in the same export (two of them hold the codes Northway freed)
NW_OTHER = [
    dict(code='NW-102', units=['CA*NWE*E0355*1', 'CA*NWE*E0355*2'], kw=50, lam=7.3),
    dict(code='NW-107', units=['CA*NWE*E0361*1', 'CA*NWE*E0361*2'], kw=100, lam=8.6),
    dict(code='NW-115', units=['CA*NWE*E0115*1', 'CA*NWE*E0115*2'], kw=50, lam=4.9),
    dict(code='NW-121', units=['CA*NWE*E0121*1'], kw=50, lam=2.6),
    dict(code='NW-129', units=['CA*NWE*E0129*1', 'CA*NWE*E0129*2'], kw=100, lam=6.4),
]
# district-approved maintenance windows (site, start local, end local, approved on)
MAINT = [
    ('SV-RS-27', dt.datetime(2025, 11, 4, 9, 0), dt.datetime(2025, 11, 5, 13, 0), dt.date(2025, 10, 21)),
    ('SV-RS-21', dt.datetime(2026, 3, 2, 8, 0), dt.datetime(2026, 3, 3, 17, 0), dt.date(2026, 3, 6)),
    ('SV-RS-22', dt.datetime(2026, 4, 14, 9, 0), dt.datetime(2026, 4, 14, 15, 30), dt.date(2026, 3, 30)),
    ('SV-RS-24', dt.datetime(2026, 5, 12, 8, 0), dt.datetime(2026, 5, 12, 16, 0), dt.date(2026, 4, 28)),
    ('SV-RS-28', dt.datetime(2026, 8, 25, 7, 30), dt.datetime(2026, 8, 25, 18, 30), dt.date(2026, 8, 11)),
]
# the work itself, as the operators logged it (site, start local, end local): it can start late or overrun
MAINT_WORK = {
    'SV-RS-27': (dt.datetime(2025, 11, 4, 9, 12, 40), dt.datetime(2025, 11, 5, 12, 31, 5)),
    'SV-RS-21': (dt.datetime(2026, 3, 2, 8, 6, 21), dt.datetime(2026, 3, 3, 15, 48, 37)),
    'SV-RS-22': (dt.datetime(2026, 4, 14, 9, 4, 55), dt.datetime(2026, 4, 14, 14, 57, 12)),
    'SV-RS-24': (dt.datetime(2026, 5, 12, 8, 9, 31), dt.datetime(2026, 5, 12, 15, 22, 48)),
    'SV-RS-28': (dt.datetime(2026, 8, 25, 7, 41, 3), dt.datetime(2026, 8, 25, 20, 12, 44)),
}
CFC_WIN = (to_utc(dt.datetime(2024, 11, 1)), to_utc(dt.datetime(2026, 11, 1)))
NWE_WIN = (to_utc(dt.datetime(2025, 9, 1)), to_utc(dt.datetime(2026, 11, 1)))
STATUS_WIN = (to_utc(dt.datetime(2025, 9, 1)), to_utc(dt.datetime(2026, 11, 1)))
SPLIT_WIN = (to_utc(dt.datetime(2025, 10, 1)), to_utc(dt.datetime(2026, 4, 1)))
RESEND_AT = dt.datetime(2026, 4, 22, 5, 41, 9)          # UTC, the corrected batch
HOLT_OUTAGE = (dt.datetime(2026, 2, 9, 5, 12, 44), dt.datetime(2026, 2, 13, 18, 47, 2))


# ---------------------------------------------------------------- units and their spells
class Unit:
    def __init__(self, uid, svrd, op, station, kw, lam, start, end, schedule_a):
        self.uid, self.svrd, self.op, self.station, self.kw, self.lam = uid, svrd, op, station, kw, lam
        self.start, self.end, self.schedule_a = start, end, schedule_a     # UTC service window
        self.spells = []          # (t0, t1, status, code) in UTC
        self.sessions = []


def _random_spells(u, lo, hi):
    t = lo + dt.timedelta(hours=float(RNG.uniform(5, 400)))
    out = []
    while True:
        t = t + dt.timedelta(hours=float(RNG.exponential(560)))
        if t >= hi:
            break
        mins = float(np.clip(RNG.lognormal(4.3, 0.95), 11, 60 * 26)) + float(RNG.uniform(0, 1))
        code = RNG.choice(['GroundFailure', 'InternalError', 'OtherError', 'PowerMeterFailure', 'ConnectorLockFailure',
                           'HighTemperature', 'EVCommunicationError'], p=[.16, .27, .18, .08, .11, .09, .11])
        out.append((t, t + dt.timedelta(minutes=mins), 'Faulted', str(code)))
        t = t + dt.timedelta(minutes=mins)
    return out


def build_units():
    units = []
    rep = {old: (site, new, to_utc(f0), to_utc(sw)) for site, old, new, f0, sw in REPLACEMENTS}
    for s in SITES:
        lam_u = s['lam'] / len(s['units'])
        if s['op'] == 'CFC':
            lo, hi = CFC_WIN
            for uid in s['units']:
                if uid in rep:
                    _, new, f0, sw = rep[uid]
                    a = Unit(uid, s['svrd'], 'CFC', s['code'], s['kw'], lam_u, lo, sw, True)
                    b = Unit(new, s['svrd'], 'CFC', s['code'], s['kw'], lam_u, sw, hi, True)
                    a.spells = [x for x in _random_spells(a, lo, f0 - dt.timedelta(hours=30))]
                    a.spells.append((f0, sw, 'Faulted', 'InternalError'))
                    b.spells = [x for x in _random_spells(b, sw + dt.timedelta(hours=40), hi)]
                    units += [a, b]
                else:
                    a = Unit(uid, s['svrd'], 'CFC', s['code'], s['kw'], lam_u, lo, hi, True)
                    a.spells = _random_spells(a, lo, hi)
                    units.append(a)
        else:
            lo, hi = NWE_WIN
            for uid in s['units']:
                a = Unit(uid, s['svrd'], 'NWE', s['now'], s['kw'], lam_u, lo, hi, True)
                a.spells = _random_spells(a, lo, hi)
                units.append(a)
            if s['svrd'] == 'SV-RS-28':
                uid, at, kw, lam = UM_EXTRA
                a = Unit(uid, 'SV-RS-28', 'NWE', s['now'], kw, lam, to_utc(at), hi, False)
                a.spells = _random_spells(a, to_utc(at) + dt.timedelta(hours=60), hi)
                units.append(a)
    for o in NW_OTHER:
        lo, hi = NWE_WIN
        for uid in o['units']:
            a = Unit(uid, None, 'NWE', o['code'], o['kw'], o['lam'] / len(o['units']), lo, hi, False)
            a.spells = _random_spells(a, lo, hi)
            units.append(a)
    # Holt Junction's supply failed in February: both units out together
    h0, h1 = to_utc(HOLT_OUTAGE[0]), to_utc(HOLT_OUTAGE[1])
    for u in units:
        if u.svrd == 'SV-RS-25':
            u.spells = [x for x in u.spells if x[1] < h0 - 6 * H or x[0] > h1 + 6 * H]
            u.spells.append((h0, h1, 'Faulted', 'PowerSwitchFailure' if u.uid.endswith('1') else 'OtherError'))
    # maintenance work as logged (the whole site out of service)
    for svrd, (w0, w1) in MAINT_WORK.items():
        a0, a1 = to_utc(w0), to_utc(w1)
        for u in units:
            if u.svrd == svrd and u.start <= a0 and a1 <= u.end:
                u.spells = [x for x in u.spells if x[1] < a0 - 3 * H or x[0] > a1 + 3 * H]
                u.spells.append((a0, a1, 'Unavailable', 'NoError'))
    for u in units:
        u.spells.sort()
        clean = []
        for x in u.spells:
            if clean and x[0] <= clean[-1][1] + dt.timedelta(minutes=10):
                continue
            clean.append(x)
        u.spells = clean
    return units


def _down(u, t0, t1):
    return any(a < t1 and t0 < b for a, b, *_ in u.spells)


# ---------------------------------------------------------------- sessions
def _token_pool(n):
    pool = []
    for _ in range(n):
        emsp = ['CFC', 'CFC', 'NWE', 'FLO', 'PLG', 'EVG'][RNG.integers(6)]
        model = W.FLEET_KEYS[RNG.choice(len(W.FLEET_KEYS), p=np.array([W.FLEET[k][5] for k in W.FLEET_KEYS]) /
                                       sum(W.FLEET[k][5] for k in W.FLEET_KEYS))]
        pool.append((f"CA*{emsp}*C{RNG.integers(10_000_000, 99_999_999)}*{RNG.integers(10)}", model))
    return pool


TOKENS = _token_pool(2400)


def build_sessions(units):
    for u in units:
        d = u.start.date()
        while dt.datetime.combine(d, dt.time()) < u.end + dt.timedelta(days=1):
            m = d.month
            season = 1.25 if m in (6, 7, 8) else (0.82 if m in (11, 12, 1, 2) else 1.0)
            for _ in range(RNG.poisson(u.lam * season)):
                t0l = dt.datetime.combine(d, dt.time()) + dt.timedelta(seconds=int(RNG.uniform(6.4 * 3600, 21.6 * 3600)))
                t0 = to_utc(t0l)
                tok, model = TOKENS[RNG.integers(len(TOKENS))]
                usable = W.FLEET[model][2]
                soc0 = float(RNG.uniform(0.08, 0.62))
                kwh = float(np.clip(RNG.gamma(4.2, 6.1), 3.2, min(72.0, (0.97 - soc0) * usable / 0.92)))
                soc1 = soc0 + kwh * 0.92 / usable
                mins = kwh / (0.82 * min(u.kw, 150)) * 60 * RNG.uniform(1.05, 1.35) + RNG.uniform(1.5, 4.0)
                t1 = t0 + dt.timedelta(minutes=mins)
                if t0 < u.start or t1 > u.end or _down(u, t0 - dt.timedelta(minutes=2), t1 + dt.timedelta(minutes=2)):
                    continue
                if any(x['start'] < t1 and t0 < x['end'] for x in u.sessions[-3:]):
                    continue
                stop = RNG.choice(['Local', 'EVDisconnected', 'Remote', 'SOCLimitReached'], p=[.46, .31, .08, .15])
                u.sessions.append(dict(unit=u, start=t0, end=t1, kwh=round(kwh, 3), soc0=soc0, soc1=soc1, token=tok,
                                       model=model, stop=str(stop)))
            d += dt.timedelta(days=1)
        u.sessions.sort(key=lambda x: x['start'])


def split_records(units):
    """CFC's remote back office split a session a modem drop interrupted into two records, October to March."""
    for u in units:
        if u.op != 'CFC':
            continue
        for x in u.sessions:
            x['split'] = None
            if SPLIT_WIN[0] <= x['end'] < SPLIT_WIN[1] and RNG.random() < 0.067 and x['end'] - x['start'] > 9 * 60 * dt.timedelta(seconds=1):
                frac = float(RNG.uniform(0.3, 0.78))
                cut = x['start'] + (x['end'] - x['start']) * frac
                gap = dt.timedelta(seconds=int(RNG.uniform(18, 75)))
                e1 = round(x['kwh'] * frac * float(RNG.uniform(0.97, 1.03)), 3)
                e1 = min(e1, round(x['kwh'] - 0.5, 3))
                x['split'] = dict(cut=cut, resume=cut + gap, e1=e1, e2=round(x['kwh'] - e1, 3))


# ---------------------------------------------------------------- status rows
def status_rows(units):
    """Each unit's status notifications inside the export window, with re-sent duplicates now and then."""
    cfc, nwe = [], []
    lo, hi = STATUS_WIN
    for u in units:
        if u.op == 'CFC' and u.svrd is None:
            continue
        rows = []
        first = max(u.start, lo)
        if u.start > lo:
            rows.append((u.start, 'Available', 'NoError'))
        else:
            rows.append((lo + dt.timedelta(minutes=float(RNG.uniform(30, 400))), 'Available', 'NoError'))
        for t0, t1, st, code in u.spells:
            if t1 < lo or t0 > hi:
                continue
            rows.append((t0, st, code))
            if t1 < u.end or u.end >= hi:
                rows.append((t1, 'Available', 'NoError'))
        # nightly reboots and reconnects re-send the current status now and then
        t = first
        while t < min(u.end, hi):
            t += dt.timedelta(hours=float(RNG.exponential(330)))
            if t >= min(u.end, hi):
                break
            cur = 'Available'
            for a, b, st, code in u.spells:
                if a <= t < b:
                    cur = st
            rows.append((t, cur, 'NoError' if cur != 'Faulted' else 'OtherError'))
        rows = [r for r in rows if lo <= r[0] < hi]
        rows.sort()
        for t, st, code in rows:
            if u.op == 'CFC':
                cfc.append(dict(t=t, cp=u.uid, status=st, code=code))
            else:
                nwe.append(dict(t=t, box=u.station, conn=int(u.uid.rsplit('*', 1)[1]), status=st, code=code))
    return cfc, nwe


# ---------------------------------------------------------------- clean truth of the two asks
def _overlap(a0, a1, b0, b1):
    return max(dt.timedelta(0), min(a1, b1) - max(a0, b0))


def truth(units):
    """Charge-point hours unavailable, availability and support by Schedule A site and quarter."""
    maint = {}
    for svrd, w0, w1, appr in MAINT:
        if appr < w0.date():
            maint.setdefault(svrd, []).append((to_utc(w0), to_utc(w1)))
    out = {}
    for s in SITES:
        su = [u for u in units if u.svrd == s['svrd'] and u.schedule_a]
        for qi, (q0, q1) in enumerate(QUARTERS):
            down = dt.timedelta(0)
            for u in su:
                for a, b, st, code in u.spells:
                    o0, o1 = max(a, q0, u.start), min(b, q1, u.end)
                    if o1 <= o0:
                        continue
                    span = o1 - o0
                    for m0, m1 in maint.get(s['svrd'], []):
                        span -= _overlap(o0, o1, m0, m1)
                    down += span
            hours = down.total_seconds() / 3600
            cap = len(s['units']) * (q1 - q0).total_seconds() / 3600
            avail = 1 - hours / cap
            kwh = sum(x['kwh'] for u in su for x in u.sessions if q0 <= x['end'] < q1)
            out[(s['svrd'], qi)] = dict(hours=hours, avail=avail, kwh=kwh,
                                        support=RATE * kwh if avail >= GATE else 0.0)
    return out


def build_all():
    units = build_units()
    build_sessions(units)
    split_records(units)
    cfc_status, nwe_status = status_rows(units)
    return units, cfc_status, nwe_status
