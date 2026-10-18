"""task247 simulator: the sea at the station's 16 reef sites from 2018 to the as-of, the cloud over them, the
near-real-time analysis that fills cloudy days by relaxing toward climatology, and the reprocessed record.

The truth is a daily climatology plus a slow background anomaly (a regional and a local part) plus each summer's
heat event. The near-real-time analysis reads the truth (a little warm) on a clear day; on a cloudy day it keeps its
previous anomaly and lets it decay toward climatology with an e-folding time of TAU days. The reprocessed record reads
the truth with a small error on every day, cloudy or clear."""
import datetime as dt

import numpy as np

import params as P

REGIONS = ("north", "central", "south")

# each heat season: the event's rise start, plateau start, plateau end, fall end, and its peak anomaly by region
EVENTS = {
    2018: ((7, 20), (8, 20), (9, 10), (10, 15), {"north": 0.35, "central": 0.40, "south": 0.40}),
    2019: ((7, 5), (8, 10), (9, 20), (10, 25), {"north": 0.70, "central": 0.65, "south": 0.80}),
    2020: ((7, 10), (8, 15), (9, 15), (10, 20), {"north": 0.55, "central": 0.60, "south": 0.60}),
    2021: ((7, 15), (8, 12), (9, 15), (10, 15), {"north": 0.85, "central": 0.55, "south": 0.50}),
    2022: ((7, 10), (8, 10), (9, 20), (10, 20), {"north": 0.45, "central": 0.55, "south": 0.95}),
    2023: ((7, 1), (8, 5), (9, 25), (10, 30), {"north": 1.05, "central": 1.15, "south": 1.25}),
    2024: ((7, 10), (8, 10), (9, 20), (10, 25), {"north": 0.80, "central": 0.70, "south": 0.90}),
    2025: ((7, 20), (8, 20), (9, 10), (10, 15), {"north": 0.40, "central": 0.45, "south": 0.45}),
    2026: ((7, 10), (8, 10), (9, 15), (10, 20), {"north": 0.50, "central": 0.60, "south": 0.55}),
}

# cloud: the chance a clear day turns cloudy and a cloudy day stays cloudy, by region; and the troughs
CLOUD = {"north": (0.13, 0.55), "central": (0.12, 0.52), "south": (0.15, 0.58)}
TROUGHS = [
    # sites, first day, last day, chance a day under it is cloudy
    ((10, 11, 12, 13, 14, 15), dt.date(2027, 8, 10), dt.date(2027, 9, 8), 0.80),
    ((12, 13, 14), dt.date(2022, 8, 18), dt.date(2022, 9, 4), 0.86),
    ((5, 6, 7), dt.date(2019, 8, 14), dt.date(2019, 8, 30), 0.86),
    ((0, 1, 2), dt.date(2021, 8, 22), dt.date(2021, 9, 8), 0.86),
    ((8, 9, 10), dt.date(2020, 8, 20), dt.date(2020, 9, 2), 0.86),
]


def cal_doy(d):
    """the day's position in a 365-day year, 29 February sharing 28 February's"""
    return dt.date(2019, d.month, min(d.day, 28) if d.month == 2 else d.day).timetuple().tm_yday


def days():
    n = (P.LAST_NRT_DAY - P.FIRST_DAY).days + 1
    return [P.FIRST_DAY + dt.timedelta(i) for i in range(n)]


def _ar(rng, phi, sd, n):
    x = np.zeros(n)
    e = rng.normal(0, sd * np.sqrt(1 - phi ** 2), n)
    x[0] = rng.normal(0, sd)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + e[t]
    return x


def _bump(D, year, a, b, c, d):
    """0 before a, rising to 1 at b, 1 to c, falling to 0 at d"""
    x = np.zeros(len(D))
    A, B, C, E = (dt.date(year, *m) for m in (a, b, c, d))
    for i, day in enumerate(D):
        if A <= day < B:
            x[i] = np.sin(0.5 * np.pi * (day - A).days / (B - A).days)
        elif B <= day < C:
            x[i] = 1.0
        elif C <= day < E:
            x[i] = np.cos(0.5 * np.pi * (day - C).days / (E - C).days)
    return x


def _shape(D, start, rise, hold, fall):
    """0 before start, rising over rise days to 1, held for hold days, falling over fall days to 0"""
    a = dt.date(2027, *start)
    b = a + dt.timedelta(rise)
    c = b + dt.timedelta(hold)
    e = c + dt.timedelta(fall)
    x = np.zeros(len(D))
    for i, day in enumerate(D):
        if a <= day < b:
            x[i] = np.sin(0.5 * np.pi * (day - a).days / rise) ** 2
        elif b <= day < c:
            x[i] = 1.0
        elif c <= day < e:
            x[i] = np.cos(0.5 * np.pi * (day - c).days / fall) ** 2
    return x


def make(seed=P.SIM_SEED, amp27=None):
    rng = np.random.default_rng(seed)
    D = days()
    T, N = len(D), P.NSITE
    doy = np.array([cal_doy(d) for d in D])
    region = [s[2] for s in P.SITES]
    # climatology: an annual harmonic peaking early September and a weak second harmonic
    base = rng.uniform(27.95, 28.25, N)
    a1 = rng.uniform(1.42, 1.58, N)
    a2 = rng.uniform(0.10, 0.16, N)
    ang = 2 * np.pi * (doy - 244) / 365.25
    clim = base[:, None] + a1[:, None] * np.cos(ang)[None, :] + a2[:, None] * np.cos(2 * ang + 0.6)[None, :]
    # background anomaly: regional and local, slow
    com = {r: _ar(rng, 0.985, 0.13, T) for r in REGIONS}
    anom = np.array([0.75 * com[region[s]] + _ar(rng, 0.97, 0.07, T) for s in range(N)])
    # heat events
    ev = np.zeros((N, T))
    for y, (a, b, c, d, peak) in EVENTS.items():
        bump = _bump(D, y, a, b, c, d)
        for s in range(N):
            ev[s] += peak[region[s]] * rng.uniform(0.85, 1.15) * bump
    # 2027: each site's sea rises to a plateau held amp27 degrees above its maximum monthly mean, then falls back
    if amp27 is None:
        amp27 = AMP27
    yr = np.array([d.year for d in D]); mon = np.array([d.month for d in D])
    y19 = yr == 2019
    mmm = np.array([max(clim[s, y19 & (mon == m)].mean() for m in range(1, 13)) for s in range(N)])
    shape27 = np.array([_shape(D, *EVENT27[s]) for s in range(N)])
    ev += shape27 * (mmm[:, None] - clim + np.asarray(amp27, float)[:, None])
    true = clim + anom + ev
    # cloud
    cloud = np.zeros((N, T), bool)
    for s in range(N):
        p_on, p_stay = CLOUD[region[s]]
        c = False
        for t in range(T):
            c = rng.random() < (p_stay if c else p_on)
            cloud[s, t] = c
    for sites, a, b, frac in TROUGHS:
        for s in sites:
            for i, day in enumerate(D):
                if a <= day <= b and rng.random() < frac:
                    cloud[s, i] = True
    # the near-real-time analysis as first issued, and the reprocessed record
    obsv = true + P.OBS_BIAS + rng.normal(0, P.OBS_SD, true.shape)
    nrt = np.zeros((N, T))
    for s in range(N):
        last = 0.0
        for t in range(T):
            if not cloud[s, t]:
                v = obsv[s, t]
                last = v - clim[s, t]
            else:
                last = last * np.exp(-1 / P.TAU)
                v = clim[s, t] + last
            nrt[s, t] = v
    rep = true + rng.normal(0, P.REP_SD, true.shape)
    # a pass that reached the analysis after the day was issued: the day is re-issued as observed (later days keep
    # the values they were issued with)
    late = cloud & (rng.random(cloud.shape) < P.LATE_SHARE)
    final = np.where(late, obsv, nrt)
    observed = ~cloud | late
    return dict(D=D, doy=doy, clim=clim, true=true, cloud=cloud, nrt=nrt, rep=rep, region=region, base=base,
                a1=a1, a2=a2, rng=rng, late=late, final=final, observed=observed, obsv=obsv, mmm=mmm, shape27=shape27)


# the 2027 heat at each site: the rise's first day, the days of rise, plateau and fall
EVENT27 = [
    ((8, 18), 12, 12, 14), ((8, 14), 12, 22, 14), ((8, 22), 12, 7, 14), ((8, 10), 14, 26, 15), ((8, 16), 12, 22, 14),
    ((7, 25), 16, 40, 18), ((7, 22), 16, 50, 18), ((7, 30), 16, 32, 18), ((7, 24), 16, 45, 18), ((7, 20), 16, 55, 18),
    ((7, 18), 15, 60, 18), ((7, 22), 15, 45, 18), ((7, 20), 15, 55, 18), ((7, 25), 15, 40, 18), ((7, 21), 15, 50, 18),
    ((7, 28), 15, 26, 16),
]
# the plateau's height above the maximum monthly mean at each site
AMP27 = [1.0869, 1.2467, 1.0733, 1.0701, 1.1273, 1.4500, 1.5168, 1.3943,
         1.4664, 1.5295, 1.0922, 1.0265, 1.0656, 1.0774, 1.1377, 1.0299]
