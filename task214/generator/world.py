"""Clean-truth simulator: a district council's drinking-water network and a spring cryptosporidiosis outbreak.

Six service reservoirs feed sixteen supply zones through feed mains; normally closed boundary mains
(interconnectors) join zones of different reservoirs and are opened to back-feed a zone while its own feed
main is shut for a repair. One boundary main carries a damaged air valve in a grazed paddock: whenever it
carries water within two days of heavy rain, runoff is drawn in. Cases follow the water each zone actually
received, through each case's own incubation period.

simulate(seed) returns the network, the day-by-day supply paths, rainfall, the operations and the cases.
"""
import datetime as dt

import numpy as np

D0 = dt.date(2027, 7, 1)          # first day of the record
SETTING = dt.date(2027, 10, 19)   # the decision date (Tuesday)
NDAYS = (SETTING - D0).days       # days 0 .. NDAYS-1 are 1 July .. 18 October

RES = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6']
# zone: (normal parent node, link main, properties, x km, y km)
ZONES = {
    'Z01': ('R1', 'FM01', 2600, 1.0, 9.0), 'Z02': ('Z01', 'LM02', 1900, 2.2, 8.1), 'Z03': ('R1', 'FM03', 2100, 0.6, 7.0),
    'Z04': ('R2', 'FM04', 2900, 3.1, 6.2), 'Z05': ('R2', 'FM05', 2400, 4.2, 5.0), 'Z06': ('Z05', 'LM06', 1500, 3.4, 4.1),
    'Z07': ('R3', 'FM07', 2200, 1.4, 4.6), 'Z08': ('R3', 'FM08', 1700, 0.8, 3.0),
    'Z09': ('R5', 'FM09', 2300, 2.6, 1.6), 'Z10': ('R5', 'FM10', 1800, 4.0, 1.0),
    'Z11': ('R4', 'FM11', 2500, 5.6, 4.0), 'Z12': ('Z11', 'LM12', 1600, 6.5, 3.2),
    'Z13': ('R5', 'FM13', 1400, 5.2, 2.2), 'Z14': ('R6', 'FM14', 2000, 7.2, 1.4),
    'Z15': ('R6', 'FM15', 1300, 7.8, 2.6), 'Z16': ('R6', 'FM16', 1700, 8.2, 0.6),
}
RES_XY = {'R1': (0.4, 8.6), 'R2': (3.0, 5.4), 'R3': (0.6, 4.0), 'R4': (6.2, 4.6), 'R5': (3.6, 2.0), 'R6': (7.6, 0.4)}
# boundary mains, normally closed: name -> (zone a, zone b)
ICS = {
    'BM1': ('Z03', 'Z04'), 'BM2': ('Z02', 'Z04'), 'BM3': ('Z05', 'Z11'), 'BM4': ('Z06', 'Z07'),
    'BM5': ('Z08', 'Z09'), 'BM6': ('Z10', 'Z13'), 'BM7': ('Z12', 'Z13'), 'BM8': ('Z13', 'Z14'),
    'BM9': ('Z15', 'Z12'), 'BM10': ('Z07', 'Z03'), 'BM11': ('Z16', 'Z10'),
}
BAD = 'BM3'                       # the boundary main with the damaged air valve
PLANNED = {('FM11', 0, 0, 'BM3'), ('LM12', 0, 0, 'BM7')}   # the renewal's arrangement, evaluated as one state
# usually resident population per occupied property, 2023 census, by zone (Stats NZ national mean about 2.6)
OCC = {'Z01': 2.71, 'Z02': 2.58, 'Z03': 2.33, 'Z04': 2.64, 'Z05': 2.77, 'Z06': 2.49, 'Z07': 2.86, 'Z08': 2.52,
       'Z09': 2.69, 'Z10': 2.61, 'Z11': 2.74, 'Z12': 2.43, 'Z13': 2.57, 'Z14': 2.38, 'Z15': 2.66, 'Z16': 2.55}


def residents():
    return {z: ZONES[z][2] * OCC[z] for z in ZONES}


def rainfall(rng):
    """Daily rainfall (mm), winter-spring, with the wet spell of 2 to 5 October fixed."""
    r = rng.gamma(0.55, 6.0, NDAYS) * (rng.random(NDAYS) < 0.55)
    for date, mm in ((dt.date(2027, 10, 2), 31.0), (dt.date(2027, 10, 3), 44.0), (dt.date(2027, 10, 4), 19.0),
                     (dt.date(2027, 10, 5), 8.0)):
        r[(date - D0).days] = mm
    return r


def repairs(rng):
    """Feed- and link-main repairs: (main, first day, last day, back-feed boundary main or None)."""
    mains = [ZONES[z][1] for z in ZONES]
    zone_of_main = {ZONES[z][1]: z for z in ZONES}
    out = []
    fixed = [('FM11', dt.date(2027, 10, 4), dt.date(2027, 10, 6), 'BM3'),
             ('FM11', dt.date(2027, 8, 10), dt.date(2027, 8, 11), 'BM3')]
    for m, a, b, bf in fixed:
        out.append((m, (a - D0).days, (b - D0).days, bf))
    quiet = {'FM05', 'FM11', 'LM12', 'FM13', 'FM15'}
    q_lo, q_hi = (dt.date(2027, 9, 20) - D0).days, NDAYS - 1
    n = rng.poisson(34)
    for _ in range(n):
        m = mains[rng.integers(len(mains))]
        z = zone_of_main[m]
        first = int(rng.integers(0, NDAYS - 3))
        last = first + int(rng.choice([0, 0, 1, 1, 2, 3, 4]))
        if m in quiet and not (last < q_lo or first > q_hi):
            continue
        cands = [k for k, (a, b) in ICS.items() if z in (a, b) and k != BAD]
        bf = cands[rng.integers(len(cands))] if cands and rng.random() < 0.8 else None
        # keep the record physical: no second repair on a main already shut
        if any(mm == m and not (last < f or first > l) for mm, f, l, _ in out):
            continue
        out.append((m, first, last, bf))
    return sorted(out, key=lambda t: (t[1], t[0]))


def paths(reps):
    """paths[d][zone] = tuple of assets the zone's water passed through on day d (reservoir first)."""
    shut = [dict() for _ in range(NDAYS)]
    for m, f, l, bf in reps:
        if l == f and f >= 0 and (m, f, l, bf) not in PLANNED:
            continue      # a repair shut and restored within the day leaves the day's supply as it was
        for d in range(max(f, 0), min(l, NDAYS - 1) + 1):
            shut[d][m] = bf
    P = []
    for d in range(NDAYS):
        closed = shut[d]
        open_bm = {bf for bf in closed.values() if bf}
        cache = {}

        def path(z, seen=()):
            if z in cache:
                return cache[z]
            parent, link, *_ = ZONES[z]
            if link not in closed:
                up = (parent,) if parent in RES else path(parent, seen + (z,))
                res = None if up is None else up + (link,)
            else:
                res = None
                for k in sorted(open_bm):
                    a, b = ICS[k]
                    if z in (a, b):
                        other = b if z == a else a
                        if other in seen:
                            continue
                        up = path(other, seen + (z,))
                        if up is not None and link not in up:
                            res = up + (k,)
                            break
            cache[z] = res
            return res
        P.append({z: path(z) for z in ZONES})
    return P


def incubation_pmf(median=7.0, sigma=0.38, kmax=14):
    k = np.arange(1, kmax + 1)
    from math import erf, log, sqrt
    cdf = lambda x: 0.5 * (1 + erf((log(x) - log(median)) / (sigma * sqrt(2))))
    p = np.array([cdf(i + 0.5) - cdf(i - 0.5) for i in k])
    return p / p.sum()


def simulate(seed=214, p_case=2.6e-3, bg_per_100k_year=32.0):
    rng = np.random.default_rng(seed)
    rain = rainfall(rng)
    reps = repairs(rng)
    P = paths(reps)
    pop = residents()
    rain48 = np.array([rain[max(d - 2, 0):d + 1].sum() for d in range(NDAYS)])
    inc = incubation_pmf()
    cases = []
    # outbreak: water through the bad boundary main within two days of heavy rain
    for d in range(NDAYS):
        if rain48[d] < 25.0:
            continue
        c = min((rain48[d] - 20.0) / 40.0, 1.5)
        for z, pth in P[d].items():
            if pth and BAD in pth:
                n = rng.poisson(pop[z] * p_case * c)
                for _ in range(n):
                    onset = d + 1 + int(rng.choice(len(inc), p=inc))
                    cases.append((z, onset, 'outbreak', d))
    # background: sporadic cases (farm animals, travel, recreational water), spring peak
    for z in ZONES:
        for d in range(NDAYS):
            month = (D0 + dt.timedelta(days=d)).month
            f = {7: 0.6, 8: 0.9, 9: 1.7, 10: 2.0}[month]
            n = rng.poisson(pop[z] * bg_per_100k_year / 1e5 / 365.0 * f)
            for _ in range(n):
                cases.append((z, d, 'background', None))
    # notification: report a few days after onset; only reports by 18 October are on file
    out = []
    for z, onset, kind, exp_day in cases:
        rep = onset + int(rng.integers(2, 10))
        if rep < NDAYS:
            out.append(dict(zone=z, onset=onset, report=rep, kind=kind, exposure_day=exp_day))
    return dict(seed=seed, rain=rain, rain48=rain48, reps=reps, P=P, pop=pop, cases=out, inc=inc)
