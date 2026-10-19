"""task248 simulator: each plant's inlet temperature, its town's shedding of SARS-CoV-2 RNA, the sewer's decay of that
RNA on the way to the plant, the twice-weekly 24-hour composites, and the paired upstream study.

The decay is first order over the plant's population-weighted travel time, at a rate that rises with the water's
temperature (K20 at 20 degrees, THETA per degree), so a plant at the end of a long trunk sewer loses far more of the
RNA in summer than in winter. PMMoV, the faecal marker, barely decays."""
import datetime as dt

import numpy as np

import params as P

LOG10E = np.log10(np.e)


def days():
    n = (P.LAST_DAY - P.FIRST_DAY).days + 1
    return [P.FIRST_DAY + dt.timedelta(i) for i in range(n)]


def k(T, k20=P.K20, theta=P.THETA):
    return k20 * theta ** (T - 20.0)


def _bump(t, c, w):
    return np.exp(-0.5 * ((t - c) / w) ** 2)


# the regional waves: centre (days from FIRST_DAY), width (days), name; each plant scales them by its own amplitude
def _c(d):
    return (d - P.FIRST_DAY).days


WAVES = [
    ("w26_winter", _c(dt.date(2026, 6, 28)), 26.0),
    ("w26_spring", _c(dt.date(2026, 9, 20)), 15.0),
    ("w27_autumn", _c(dt.date(2027, 4, 4)), 10.0),
    ("w27_main", _c(dt.date(2027, 6, 24)), 18.0),
    ("w27_late", _c(dt.date(2027, 9, 3)), 10.0),
    ("w28_autumn", _c(dt.date(2028, 3, 20)), 14.0),
]


def make(seed=P.SIM_SEED, amp=None, shift=None):
    """amp: per plant dict of wave amplitudes (log10 units at the wave's peak above the town's lull); shift: per plant
    dict of days added to a wave's centre"""
    rng = np.random.default_rng(seed)
    D = days()
    n, S = len(D), P.NPLANT
    t = np.arange(n, dtype=float)
    doy = np.array([d.timetuple().tm_yday for d in D], dtype=float)
    tt = np.array([p[4] for p in P.PLANTS], dtype=float) / 60.0             # hours
    pop = np.array([p[3] for p in P.PLANTS], dtype=float)
    # inlet temperature: each plant's mean and swing, warmest early February, coolest early August
    mu = rng.uniform(15.4, 17.6, S)
    sw = rng.uniform(4.9, 6.1, S)
    ph = rng.uniform(-6, 6, S)
    T = mu[:, None] + sw[:, None] * np.cos(2 * np.pi * (doy[None, :] - 36 - ph[:, None]) / 365.25)
    ar = np.zeros((S, n))
    e = rng.normal(0, 0.22, (S, n))
    for i in range(1, n):
        ar[:, i] = 0.8 * ar[:, i - 1] + e[:, i]
    T = T + ar
    # shedding: log10 gene copies per person per day, the town's lull plus the waves
    lull = rng.uniform(6.85, 7.25, S)
    jit = rng.integers(-4, 5, (S, len(WAVES)))
    if amp is None:
        amp = default_amp(rng)
    summer = -0.12 * np.clip(np.cos(2 * np.pi * (doy - 30) / 365.25), 0, None) ** 2      # the summer lull is the lowest
    shed = lull[:, None] + summer[None, :] + rng.normal(0, 0.03, (S, n))
    for s in range(S):
        for j, (name, c, w) in enumerate(WAVES):
            c2 = c + jit[s, j] + ((shift or {}).get(s, {}).get(name, 0))
            shed[s] += amp[s][name] * _bump(t, c2, w)
    # flow: about 230 litres a person a day in dry weather, more after rain
    rain = (rng.random(n) < 0.18) * rng.gamma(1.4, 9.0, n)
    wet = np.convolve(rain, [0.55, 0.3, 0.15], mode="full")[:n]
    infl = rng.uniform(0.15, 0.45, S)
    flow = pop[:, None] * 0.23 * (1 + infl[:, None] + wet[None, :] * rng.uniform(0.008, 0.02, S)[:, None]) * \
        np.exp(rng.normal(0, 0.04, (S, n)))                                    # m3 a day
    pmm = rng.uniform(9.45, 9.75, S)                                           # PMMoV, log10 copies a person a day
    return dict(D=D, T=T, tt=tt, pop=pop, shed=shed, flow=flow, pmm=pmm, lull=lull, amp=amp, jit=jit, mu=mu,
                rain=rain)


# each plant's 2027 main and late wave amplitudes (aimed with tune.py so every plant's winter count stands clear of
# the High and Low lines on both bases); the other waves are drawn
AMP27 = {"ASD": [1.3156, 0.2756], "BRK": [1.2833, 1.3257], "CRF": [1.1493, 0.4165], "DNK": [1.2852, 0.4726], "FNK": [1.1959, 1.1437], "GLO": [1.0717, 0.5359], "HOL": [1.3619, 1.1347], "INB": [1.0148, 0.449], "KSB": [1.2146, 0.5571], "LRF": [1.2885, 1.1833], "MRB": [1.3825, 0.526], "NTL": [1.2557, 0.5124], "ORB": [1.2081, 1.1496], "PLH": [1.2515, 0.3596], "QRM": [1.3285, 1.2252], "RVG": [1.1875, 0.4769], "ADN": [1.2578, 0.3589], "ADS": [0.7257, 0.2347], "ADE": [0.384, 0.6321], "ADW": [1.3786, 1.2484], "TRN": [0.3679, 0.756], "UWD": [1.1274, 0.2453], "CLF": [0.6373, 0.318], "SLT": [0.2881, 0.7365]}
SHIFT27 = {"ADW": {"w27_late": -13}, "HOL": {"w27_late": 6}}


def amp27(rng):
    amp = default_amp(rng)
    shift = {}
    for s, p in enumerate(P.PLANTS):
        amp[s]["w27_main"], amp[s]["w27_late"] = AMP27[p[0]]
        if p[0] in SHIFT27:
            shift[s] = SHIFT27[p[0]]
    return amp, shift


def default_amp(rng):
    out = []
    for s in range(P.NPLANT):
        out.append(dict(w26_winter=rng.uniform(1.2, 1.6), w26_spring=rng.uniform(0.5, 0.8),
                        w27_autumn=rng.uniform(0.15, 0.3), w27_main=rng.uniform(1.0, 1.6),
                        w27_late=rng.uniform(0.6, 1.3), w28_autumn=rng.uniform(0.4, 0.8)))
    return out


def hourly(W, seed=P.SIM_SEED + 1):
    """each plant's hourly inlet temperature and flow, on UTC hours from the first day's local midnight"""
    import clock
    rng = np.random.default_rng(seed)
    D = W["D"]
    u0 = clock.to_utc(dt.datetime.combine(D[0], dt.time(0)))
    u1 = clock.to_utc(dt.datetime.combine(D[-1] + dt.timedelta(days=1), dt.time(0)))
    H = int((u1 - u0).total_seconds() // 3600)
    hours = [u0 + dt.timedelta(hours=h) for h in range(H)]
    local = [clock.to_local(u) for u in hours]
    di = np.array([(lt.date() - D[0]).days for lt in local])
    lh = np.array([lt.hour + lt.minute / 60 for lt in local])
    S = P.NPLANT
    T = W["T"][:, di] + 0.35 * np.cos(2 * np.pi * (lh - 17) / 24.0)[None, :] + rng.normal(0, 0.05, (S, H))
    shape = 1 + 0.45 * np.sin(2 * np.pi * (lh - 4.5) / 24.0) + 0.25 * np.sin(4 * np.pi * (lh - 7) / 24.0)
    F = W["flow"][:, di] / 24.0 * shape[None, :] * np.exp(rng.normal(0, 0.03, (S, H)))      # m3 in the hour
    return dict(hours=hours, local=local, T=T, F=F)


def windows(W, Hh):
    """each composite: a 24-hour composite ending 08:00 local on Mondays and Thursdays; its UTC hour indexes"""
    import clock
    u0 = Hh["hours"][0]
    out = []
    for d in W["D"]:
        if d.weekday() not in (0, 3) or d == W["D"][0]:
            continue
        end = clock.to_utc(dt.datetime.combine(d, dt.time(8, 0)))
        start = clock.to_utc(dt.datetime.combine(d - dt.timedelta(days=1), dt.time(8, 0)))
        a = int((start - u0).total_seconds() // 3600)
        b = int((end - u0).total_seconds() // 3600)
        out.append((d, a, b))
    return out


def composites(W, Hh, seed=P.SIM_SEED + 2, k20=P.K20, theta=P.THETA):
    """each plant's composites: the window's mean inlet temperature and flow, the true shed log10 load per person, the
    measured N1 and PMMoV concentrations (gene copies a litre) after the sewer's decay"""
    rng = np.random.default_rng(seed)
    C = windows(W, Hh)
    S = P.NPLANT
    out = []
    D0 = W["D"][0]
    for d, a, b in C:
        i = (d - D0).days - 1                         # the composite's day of shedding is the day before collection
        Tw = Hh["T"][:, a:b].mean(1)
        Fw = Hh["F"][:, a:b].sum(1)                   # m3 over the 24 hours
        shed = W["shed"][:, i]
        surv = np.exp(-k(Tw, k20, theta) * W["tt"])
        noise = rng.normal(0, 0.075, S)
        load = shed + np.log10(surv) + noise           # log10 copies a person a day reaching the plant
        conc = 10 ** load * W["pop"] / (Fw * 1000.0)
        pm_load = W["pmm"] + rng.normal(0, 0.06, S) + np.log10(np.exp(-P.K_PMMOV * W["tt"]))
        pconc = 10 ** pm_load * W["pop"] / (Fw * 1000.0)
        out.append(dict(d=d, Tw=Tw, Fw=Fw, shed=shed, load=load, conc=conc, pconc=pconc, noise=noise))
    return out


STUDY_PLANTS = ("DNK", "NTL", "ADS", "CLF")


def study(W, Hh, seed=P.SIM_SEED + 3, k20=P.K20, theta=P.THETA):
    """the paired upstream study: fortnightly, a 24-hour composite at the trunk sewer's head where the town's sewage
    enters it, and the plant's composite lagged by the travel time; each analysed in triplicate. The trunk carries the
    town's whole flow and takes in nothing else on the way."""
    import clock
    rng = np.random.default_rng(seed)
    u0 = Hh["hours"][0]
    idx = [i for i, p in enumerate(P.PLANTS) if p[0] in STUDY_PLANTS]
    out = []
    d = P.STUDY[0]
    while d <= P.STUDY[1]:
        for s in idx:
            tt = W["tt"][s]
            start = clock.to_utc(dt.datetime.combine(d - dt.timedelta(days=1), dt.time(8, 0)))
            a = int((start - u0).total_seconds() // 3600)
            lag = int(round(tt))
            Tin = Hh["T"][s, a + lag:a + lag + 24].mean()                 # the plant's inlet over its composite
            Tup = Tin + rng.normal(0.25, 0.15)                             # the trunk's head runs a little warmer
            Ttr = 0.5 * (Tin + Tup)
            i = (d - W["D"][0]).days - 1
            up = W["shed"][s, i] + rng.normal(0, 0.035)                     # log10 copies a person a day entering
            pl = up + np.log10(np.exp(-k(Ttr, k20, theta) * tt)) + rng.normal(0, 0.035)
            pm_up = W["pmm"][s] + rng.normal(0, 0.03)
            pm_pl = pm_up + np.log10(np.exp(-P.K_PMMOV * tt)) + rng.normal(0, 0.03)
            Fw = Hh["F"][s, a + lag:a + lag + 24].sum()
            f = W["pop"][s] / (Fw * 1000.0)
            out.append(dict(site=P.PLANTS[s][0], s=s, d=d, tt=tt, Tin=Tin, Tup=Tup, up=10 ** up * f, pl=10 ** pl * f,
                            pm_up=10 ** pm_up * f, pm_pl=10 ** pm_pl * f))
        d += dt.timedelta(days=14)
    return out
