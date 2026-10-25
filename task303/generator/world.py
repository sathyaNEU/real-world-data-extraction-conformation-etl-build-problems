"""task303's outage process: the base process on every day (losses of a substation's supply, which every feeder there
records at its breaker in the same minute; backbone faults cleared by the feeder breaker or a line recloser; tap faults
at a fixed set of fuses; transformer and service outages), the district's storm days on their own random stream, and
the system's major event days (the district's storm days and the system's others). Ported from scratch
p303uo/world6.py; seed 154 is the scan's pick (scan6b.py)."""
import math
import datetime as dt
from collections import defaultdict
import numpy as np

import params as P

SIM0 = P.SIM0
REC0 = P.REC0
END = P.END
NDAY = (END - SIM0).days
YEARS = P.YEARS
NY = P.NY

SUBS = {
    'PLC': dict(lam=1.55, mins=88, sd=0.42,
                mix={'tree': .44, 'wind': .15, 'animal': .03, 'lightning': .24, 'equipment': .09, 'unknown': .05}),
    'SRH': dict(lam=0.12, mins=55, sd=0.4, mix={'equipment': .55, 'lightning': .35, 'unknown': .10}),
    'BYM': dict(lam=0.45, mins=70, sd=0.4,
                mix={'lightning': .45, 'wind': .15, 'tree': .15, 'equipment': .18, 'unknown': .07}),
    'HLF': dict(lam=0.25, mins=60, sd=0.4, mix={'lightning': .5, 'equipment': .4, 'unknown': .1}),
    'KTR': dict(lam=1.05, mins=80, sd=0.42,
                mix={'tree': .40, 'wind': .16, 'lightning': .26, 'equipment': .12, 'unknown': .06}),
    'WYX': dict(lam=0.18, mins=55, sd=0.4, mix={'equipment': .5, 'lightning': .4, 'unknown': .1}),
}
FEEDERS = {
    'F-112': ('PLC', 2210, 12.6, 31, 0.68, (1.0, 0.47, 0.21), 0.55, True),
    'F-114': ('PLC', 1730, 11.2, 24, 0.64, (1.0, 0.52, 0.24), 0.58, True),
    'F-117': ('PLC', 1490, 9.6, 20, 0.60, (1.0, 0.55, None), 0.60, False),
    'F-205': ('SRH', 2300, 14.4, 33, 0.52, (1.0, 0.66, 0.33), 1.00, True),
    'F-208': ('SRH', 1910, 12.4, 27, 0.40, (1.0, 0.60, 0.28), 1.00, True),
    'F-209': ('SRH', 1350, 8.7, 18, 0.33, (1.0, 0.52, None), 1.00, False),
    'F-301': ('BYM', 2050, 14.2, 29, 0.47, (1.0, 0.64, 0.31), 1.10, True),
    'F-303': ('BYM', 1620, 10.5, 22, 0.38, (1.0, 0.57, 0.26), 1.00, True),
    'F-304': ('BYM', 1180, 7.9, 15, 0.35, (1.0, 0.50, None), 1.00, False),
    'F-411': ('HLF', 2330, 12.9, 33, 0.36, (1.0, 0.61, 0.29), 1.00, False),
    'F-412': ('HLF', 1760, 10.8, 25, 0.30, (1.0, 0.56, None), 1.00, False),
    'F-415': ('HLF', 1290, 8.1, 17, 0.27, (1.0, 0.52, None), 1.00, False),
    'F-521': ('KTR', 1980, 13.1, 30, 0.62, (1.0, 0.63, 0.30), 0.70, False),
    'F-522': ('KTR', 1540, 10.2, 21, 0.58, (1.0, 0.58, None), 0.70, False),
    'F-525': ('KTR', 1210, 8.4, 16, 0.55, (1.0, 0.51, None), 0.70, False),
    'F-631': ('WYX', 2140, 11.6, 28, 0.23, (1.0, 0.60, 0.28), 1.00, False),
    'F-632': ('WYX', 1670, 9.9, 23, 0.26, (1.0, 0.55, None), 1.00, False),
    'F-636': ('WYX', 1150, 7.4, 14, 0.21, (1.0, 0.50, None), 1.00, False),
}
K_TREE = 0.060
ZONEW = {'F-205': (0.72, 0.18, 0.10), 'F-112': (0.38, 0.36, 0.26), 'F-114': (0.40, 0.35, 0.25)}
BB_OTHER = {'wind': 0.0055, 'animal': 0.0060, 'lightning': 0.0050, 'equipment': 0.0070, 'vehicle': 0.0025,
            'unknown': 0.0035}
LAT_RATE = 0.115
LAT_MIX = {'tree': .38, 'animal': .22, 'wind': .10, 'equipment': .14, 'lightning': .06, 'vehicle': .03, 'unknown': .07}
MINS = {'tree': 165, 'wind': 150, 'animal': 95, 'lightning': 120, 'equipment': 155, 'vehicle': 200, 'unknown': 105}
ADDR = P.ADDRESSED
CAND = [f for f, fp in FEEDERS.items() if fp[7]]
SUBFEEDERS = defaultdict(list)
for _f, _fp in FEEDERS.items():
    SUBFEEDERS[_fp[0]].append(_f)
SYS_CUST = sum(fp[1] for fp in FEEDERS.values())

# storms
STORMS_A_YEAR = 3.6
STORM_LAT = 0.42        # tap faults per lateral mile on a storm day of severity 1
STORM_BB = 0.045        # backbone faults per backbone mile on a storm day of severity 1
STORM_MIX = {'tree': .52, 'wind': .30, 'lightning': .12, 'unknown': .06}
TX_RATE = 0.0105        # transformer and service outages a customer a year
TX_MIX = {'equipment': .46, 'animal': .20, 'tree': .12, 'lightning': .10, 'unknown': .08, 'vehicle': .04}
STORM_TX = 0.0042       # transformer and service outages a customer on a storm day of severity 1
ELSEWHERE_MEDS = 1.1    # system major event days a year from storms that miss the district


def bb_rates(canopy, factor):
    r = {'tree': K_TREE * canopy * factor}
    r.update(BB_OTHER)
    return r


def taps(seed):
    """each feeder's tap fuses: number, the backbone zone it hangs off, its customers"""
    rng = np.random.default_rng([seed, 3])
    out = {}
    for f, fp in FEEDERS.items():
        s, cust, bb, lat, can, zones, fac, cand = fp
        n = int(round(lat * 1.25))
        zs = [z for z in range(3) if zones[z] is not None]
        excl = []
        for z in zs:
            nxt = zones[z + 1] if z + 1 < 3 and zones[z + 1] is not None else 0.0
            excl.append(zones[z] - nxt)
        p = np.array(excl) / sum(excl)
        w = rng.gamma(1.6, 1.0, size=n)
        tap_cust = np.maximum(4, np.round(w / w.sum() * cust * 0.78)).astype(int)
        lengths = rng.gamma(2.0, 1.0, size=n)
        lengths = lengths / lengths.sum()
        out[f] = []
        for k in range(n):
            out[f].append(dict(n=k + 1, zone=int(rng.choice(zs, p=p)), cust=int(tap_cust[k]), w=float(lengths[k])))
    return out


def storm_days(seed):
    rng = np.random.default_rng([seed, 4])
    days = {}
    for y in range(SIM0.year, END.year):
        d0 = (dt.date(y, 1, 1) - SIM0).days
        nd = (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
        k = rng.poisson(STORMS_A_YEAR)
        # summer thunderstorms and the autumn tropical season carry most storms
        doy = rng.choice(nd, size=k, replace=False, p=season_p(nd))
        for x in doy:
            days[int(d0 + x)] = dict(sev=float(np.clip(rng.lognormal(0.0, 0.45), 0.45, 2.6)),
                                     onset=int(rng.integers(5 * 60, 16 * 60)), spread=int(rng.integers(150, 420)))
    return days


def fold(m, onset, top):
    """a storm's tickets stay on its day: one that would begin after the day's last minutes is folded back into the
    evening"""
    m = int(m)
    if m <= top:
        return m
    return top - (m - top) % max(1, top - onset)


def season_p(nd):
    x = np.arange(nd)
    p = 0.35 + np.exp(-((x - 200) / 45.0) ** 2) + 0.8 * np.exp(-((x - 255) / 25.0) ** 2) + 0.4 * np.exp(-((x - 30) / 25.0) ** 2)
    return p / p.sum()


def simulate(seed, storm_seed=None):
    rng = np.random.default_rng([seed, 1])
    tp = taps(seed)
    ev = []

    def pick(mix):
        k = list(mix)
        p = np.array([mix[x] for x in k], float)
        p /= p.sum()
        return k[rng.choice(len(k), p=p)]
    yrs = NDAY / 365.25
    for s, sp in SUBS.items():
        for _ in range(rng.poisson(sp['lam'] * yrs)):
            d = int(rng.integers(0, NDAY))
            minute = int(rng.integers(0, 1440))
            dur = max(12, int(round(rng.lognormal(math.log(sp['mins']), sp['sd']))))
            cause = pick(sp['mix'])
            offs = rng.permutation(len(SUBFEEDERS[s])) * int(rng.integers(2, 6))
            for f, o in zip(SUBFEEDERS[s], offs):
                ev.append(dict(feeder=f, sub=s, day=d, minute=minute, mins=dur + int(o), cust=FEEDERS[f][1],
                               cause=cause, device='breaker', zone=0, tap=None, kind='supply', storm=False))
    for f, fp in FEEDERS.items():
        s, cust, bb, lat, can, zones, fac, cand = fp
        zs = [z for z in range(3) if zones[z] is not None]
        wz = ZONEW.get(f)
        for cause, r in bb_rates(can, fac).items():
            for _ in range(rng.poisson(r * bb * yrs)):
                d = int(rng.integers(0, NDAY))
                if wz is None:
                    zi = int(rng.choice(zs))
                else:
                    p = np.array([wz[z] for z in zs])
                    zi = int(rng.choice(zs, p=p / p.sum()))
                ev.append(dict(feeder=f, sub=s, day=d, minute=int(rng.integers(0, 1440)),
                               mins=max(15, int(round(rng.lognormal(math.log(MINS[cause]), 0.5)))),
                               cust=int(round(cust * zones[zi] * rng.uniform(0.93, 1.0))), cause=cause,
                               device='breaker' if zi == 0 else 'recloser', zone=zi, tap=None, kind='backbone',
                               storm=False))
        tw = np.array([t['w'] for t in tp[f]])
        for _ in range(rng.poisson(LAT_RATE * lat * yrs)):
            d = int(rng.integers(0, NDAY))
            cause = pick(LAT_MIX)
            t = tp[f][int(rng.choice(len(tp[f]), p=tw))]
            ev.append(dict(feeder=f, sub=s, day=d, minute=int(rng.integers(0, 1440)),
                           mins=max(15, int(round(rng.lognormal(math.log(MINS[cause] * 0.8), 0.5)))),
                           cust=t['cust'], cause=cause, device='fuse', zone=t['zone'], tap=t['n'], kind='lateral',
                           storm=False))
        for _ in range(rng.poisson(TX_RATE * cust * yrs)):
            d = int(rng.integers(0, NDAY))
            cause = pick(TX_MIX)
            t = tp[f][int(rng.choice(len(tp[f]), p=tw))]
            ev.append(dict(feeder=f, sub=s, day=d, minute=int(rng.integers(0, 1440)),
                           mins=max(12, int(round(rng.lognormal(math.log(140), 0.55)))),
                           cust=int(rng.choice([1, 1, 2, 3, 4, 5, 6, 8, 11])), cause=cause, device='transformer',
                           zone=t['zone'], tap=t['n'], kind='tx', storm=False))
    # storm days: their own stream
    sd = storm_days(seed)
    srng = np.random.default_rng([seed if storm_seed is None else storm_seed, 2])
    for d, st in sorted(sd.items()):
        sev = st['sev']
        for f, fp in FEEDERS.items():
            s, cust, bb, lat, can, zones, fac, cand = fp
            zs = [z for z in range(3) if zones[z] is not None]
            tw = np.array([t['w'] for t in tp[f]])
            k_lat = srng.poisson(STORM_LAT * lat * sev * (0.6 + can))
            for _ in range(k_lat):
                t = tp[f][int(srng.choice(len(tp[f]), p=tw))]
                m = fold(st['onset'] + abs(srng.normal(0, st['spread'])), st['onset'], 1405)
                cause = list(STORM_MIX)[int(srng.choice(len(STORM_MIX), p=np.array(list(STORM_MIX.values()))))]
                ev.append(dict(feeder=f, sub=s, day=d, minute=m,
                               mins=max(40, int(round(srng.lognormal(math.log(330 * (0.7 + 0.3 * sev)), 0.55)))),
                               cust=t['cust'], cause=cause, device='fuse', zone=t['zone'], tap=t['n'], kind='lateral',
                               storm=True))
            for _ in range(srng.poisson(STORM_TX * cust * sev)):
                t = tp[f][int(srng.choice(len(tp[f]), p=tw))]
                m = fold(st['onset'] + abs(srng.normal(0, st['spread'])), st['onset'], 1405)
                cause = list(STORM_MIX)[int(srng.choice(len(STORM_MIX), p=np.array(list(STORM_MIX.values()))))]
                ev.append(dict(feeder=f, sub=s, day=d, minute=m,
                               mins=max(40, int(round(srng.lognormal(math.log(380 * (0.7 + 0.3 * sev)), 0.55)))),
                               cust=int(srng.choice([1, 1, 2, 3, 4, 5, 6, 8, 11])), cause=cause, device='transformer',
                               zone=t['zone'], tap=t['n'], kind='tx', storm=True))
            k_bb = srng.poisson(STORM_BB * bb * sev * (0.6 + can))
            for _ in range(k_bb):
                zi = int(srng.choice(zs))
                m = fold(st['onset'] + abs(srng.normal(0, st['spread'] * 0.7)), st['onset'], 1400)
                cause = list(STORM_MIX)[int(srng.choice(len(STORM_MIX), p=np.array(list(STORM_MIX.values()))))]
                ev.append(dict(feeder=f, sub=s, day=d, minute=m,
                               mins=max(45, int(round(srng.lognormal(math.log(260 * (0.7 + 0.3 * sev)), 0.5)))),
                               cust=int(round(cust * zones[zi] * srng.uniform(0.93, 1.0))), cause=cause,
                               device='breaker' if zi == 0 else 'recloser', zone=zi, tap=None, kind='backbone',
                               storm=True))
    return ev, sd, tp


def med_days(seed, sd):
    """the commission's accepted major event days: the district's storm days and the system's other ones"""
    rng = np.random.default_rng([seed, 5])
    out = {d for d in sd if d >= (REC0 - SIM0).days}
    for y in YEARS:
        d0 = (dt.date(y, 1, 1) - SIM0).days
        nd = (dt.date(y + 1, 1, 1) - dt.date(y, 1, 1)).days
        for _ in range(rng.poisson(ELSEWHERE_MEDS)):
            x = int(d0 + rng.choice(nd, p=season_p(nd)))
            if x not in sd and x - 1 not in sd and x + 1 not in sd:
                out.add(x)
    return out





def in_record(e):
    return e['day'] >= (REC0 - SIM0).days


def cmi(e):
    return e['cust'] * e['mins']


def shared(ev, tol=0, need=None):
    starts = defaultdict(list)
    for e in ev:
        starts[(e['sub'], e['day'])].append((e['minute'], e['feeder']))
    out = []
    for e in ev:
        sibs = set(SUBFEEDERS[e['sub']])
        hit = {f for (m, f) in starts[(e['sub'], e['day'])] if abs(m - e['minute']) <= tol}
        out.append(len(hit) >= need if need else hit >= sibs)
    return out


def figure(ev, medset, exclude_shared, tol=0, need=None, causes=ADDR, devices=('breaker', 'recloser')):
    rec = [e for e in ev if in_record(e) and e['day'] not in medset]
    fl = shared(rec, tol, need) if exclude_shared else [False] * len(rec)
    out = defaultdict(float)
    for e, sh in zip(rec, fl):
        if sh:
            continue
        if e['device'] in devices and e['cause'] in causes:
            out[e['feeder']] += cmi(e)
    return {f: P.PREVENTED * out[f] / NY for f in CAND}
