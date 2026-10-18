"""The clean truth for task169: Calvermouth's six cycleways, their counters and the cyclists past them.

Everything the pack ships is cut from the arrays built here, by pack.py. Nothing in this module writes a file.
The truth is the world before any export mess: hourly cyclists by user group at each counter, the weather, the
calendar, the counters' capture, their outages, and the operating records (the maintenance log, the dashboard,
the volunteer count) generated from the same events.
"""
import math
from datetime import date, datetime, timedelta

import numpy as np

SEED = 169
SUMMERS = [2024, 2025, 2026]
AS_OF = date(2026, 10, 12)          # Monday: the request
PULL = date(2026, 10, 9)            # Friday: every export pulled
COMMITTEE = date(2026, 10, 26)

PURP = ["commute", "leisure", "utility"]
H_WINDOW = list(range(6, 22))       # clock hours beginning 06:00 .. 21:00 (06:00 to 22:00)

# ------------------------------------------------------------------ calendar (England, the city's schools)
BANK_HOLIDAYS = {date(2024, 1, 1), date(2024, 3, 29), date(2024, 4, 1), date(2024, 5, 6), date(2024, 5, 27),
                 date(2024, 8, 26), date(2024, 12, 25), date(2024, 12, 26),
                 date(2025, 1, 1), date(2025, 4, 18), date(2025, 4, 21), date(2025, 5, 5), date(2025, 5, 26),
                 date(2025, 8, 25), date(2025, 12, 25), date(2025, 12, 26),
                 date(2026, 1, 1), date(2026, 4, 3), date(2026, 4, 6), date(2026, 5, 4), date(2026, 5, 25),
                 date(2026, 8, 31), date(2026, 12, 25), date(2026, 12, 28)}
# school holidays (first and last weekday of each), the council's published term dates
SCHOOL_HOLIDAYS = [
    (date(2023, 12, 21), date(2024, 1, 3), "Christmas"),
    (date(2024, 2, 12), date(2024, 2, 16), "February half term"),
    (date(2024, 3, 29), date(2024, 4, 12), "Easter"),
    (date(2024, 5, 27), date(2024, 5, 31), "May half term"),
    (date(2024, 7, 23), date(2024, 9, 3), "Summer"),
    (date(2024, 10, 28), date(2024, 11, 1), "October half term"),
    (date(2024, 12, 23), date(2025, 1, 3), "Christmas"),
    (date(2025, 2, 17), date(2025, 2, 21), "February half term"),
    (date(2025, 4, 7), date(2025, 4, 21), "Easter"),
    (date(2025, 5, 26), date(2025, 5, 30), "May half term"),
    (date(2025, 7, 23), date(2025, 9, 2), "Summer"),
    (date(2025, 10, 27), date(2025, 10, 31), "October half term"),
    (date(2025, 12, 22), date(2026, 1, 2), "Christmas"),
    (date(2026, 2, 16), date(2026, 2, 20), "February half term"),
    (date(2026, 3, 30), date(2026, 4, 10), "Easter"),
    (date(2026, 5, 25), date(2026, 5, 29), "May half term"),
    (date(2026, 7, 23), date(2026, 9, 2), "Summer"),
    (date(2026, 10, 26), date(2026, 10, 30), "October half term"),
    (date(2026, 12, 21), date(2027, 1, 1), "Christmas"),
    (date(2027, 2, 15), date(2027, 2, 19), "February half term"),
    (date(2027, 3, 29), date(2027, 4, 9), "Easter"),
    (date(2027, 5, 31), date(2027, 6, 4), "May half term"),
    (date(2027, 7, 22), date(2027, 9, 1), "Summer"),
]


def in_school_holiday(d):
    for a, b, _ in SCHOOL_HOLIDAYS:
        if a <= d <= b:
            return True
    return False


def daytype(d):
    """we: Saturday, Sunday or a bank holiday; wk_hol: a weekday in a school holiday; wk_term: any other weekday."""
    if d.weekday() >= 5 or d in BANK_HOLIDAYS:
        return "we"
    return "wk_hol" if in_school_holiday(d) else "wk_term"


def summer_days(y):
    d, out = date(y, 6, 1), []
    while d <= date(y, 8, 31):
        out.append(d)
        d += timedelta(days=1)
    return out


def span_days(a, b):
    out, d = [], a
    while d <= b:
        out.append(d)
        d += timedelta(days=1)
    return out


# ------------------------------------------------------------------ the user groups
def _prof(pairs, night):
    v = np.zeros(24)
    for h, w in pairs.items():
        v[h] = w
    for h in range(24):
        if v[h] == 0:
            v[h] = night
    return v / v.sum()


PROF = {
    "commute": {"wk": _prof({6: .04, 7: .13, 8: .21, 9: .07, 10: .02, 11: .02, 12: .03, 13: .03, 14: .02, 15: .04,
                             16: .08, 17: .12, 18: .10, 19: .05, 20: .02, 21: .01, 22: .005}, 0.0012),
                "we": _prof({8: .06, 9: .09, 10: .10, 11: .10, 12: .10, 13: .10, 14: .10, 15: .10, 16: .09, 17: .08,
                             18: .05, 19: .03}, 0.0025)},
    "leisure": {"wk": _prof({6: .01, 7: .01, 8: .02, 9: .03, 10: .04, 11: .05, 12: .06, 13: .06, 14: .06, 15: .06,
                             16: .07, 17: .09, 18: .13, 19: .13, 20: .10, 21: .05, 22: .01}, 0.0015),
                "we": _prof({7: .01, 8: .03, 9: .06, 10: .09, 11: .11, 12: .12, 13: .12, 14: .12, 15: .11, 16: .09,
                             17: .07, 18: .04, 19: .02, 20: .01}, 0.0015)},
    "utility": {"wk": _prof({7: .01, 8: .015, 9: .025, 10: .10, 11: .115, 12: .125, 13: .125, 14: .115, 15: .105,
                             16: .085, 17: .05, 18: .04, 19: .03, 20: .02, 21: .01}, 0.0015),
                "we": _prof({8: .03, 9: .06, 10: .09, 11: .11, 12: .12, 13: .12, 14: .11, 15: .10, 16: .09, 17: .07,
                             18: .05, 19: .03, 20: .02}, 0.0015)},
}
# share of each group's riders travelling towards the city centre, by hour
def _inshare(p):
    v = np.full(24, 0.5)
    if p == "commute":
        v[5:10] = 0.78
        v[15:20] = 0.26
    return v


INSHARE = {p: _inshare(p) for p in PURP}
DTM = {"commute": {"wk_term": 1.0, "wk_hol": 0.80, "we": 0.16},
       "leisure": {"wk_term": 0.50, "wk_hol": 0.90, "we": 1.0},
       "utility": {"wk_term": 1.0, "wk_hol": 0.95, "we": 0.85}}
# weather response: log factor = a_wet * wet + a_t * (tmax - 20); wet is a day with 1.0 mm of rain or more
WX = {"commute": (-0.05, 0.001), "leisure": (-0.60, 0.08), "utility": (-0.15, 0.006)}
TREND = {"commute": 1.15, "leisure": 0.92, "utility": 0.98}
# outside June to August (headline counters only): month factors per group, June to August at 1.0
SEASON = {"commute": [.86, .88, .92, .95, .99, 1, 1, 1, .98, .95, .89, .78],
          "leisure": [.24, .30, .44, .64, .86, 1, 1, 1, .84, .58, .34, .24],
          "utility": [.82, .83, .88, .93, .97, 1, 1, 1, .97, .93, .91, .96]}
NOISE = {"day": 0.025, "purp": 0.020, "city": 0.012, "hour": 0.025}

# ------------------------------------------------------------------ weather
TNORM = [8.6, 9.1, 11.6, 14.3, 17.3, 20.0, 22.1, 21.8, 19.2, 15.4, 11.5, 9.0]   # mean daily maximum by month
PWET = [0.47, 0.40, 0.38, 0.34, 0.31, 0.30, 0.27, 0.30, 0.31, 0.39, 0.45, 0.45]
SUMMER_TARGET = {2024: (19.0, 0.40), 2025: (20.5, 0.30), 2026: (23.0, 0.17)}   # June to August: mean tmax, wet share
WEATHER_START, WEATHER_END = date(2024, 1, 1), date(2026, 9, 30)
WEATHER_MISSING = [date(2024, 3, 12), date(2024, 3, 13), date(2025, 7, 9), date(2025, 11, 20), date(2026, 6, 17),
                   date(2026, 2, 4)]


def make_weather(rng):
    days = span_days(WEATHER_START, WEATHER_END)
    n = len(days)
    e = np.zeros(n)
    e[0] = rng.normal(0, 2.6)
    for i in range(1, n):
        e[i] = 0.68 * e[i - 1] + rng.normal(0, 2.6 * math.sqrt(1 - 0.68 ** 2))
    # wet days by a two-state chain on the month's probability
    wet = np.zeros(n, bool)
    s = rng.random() < 0.4
    for i, d in enumerate(days):
        p = PWET[d.month - 1]
        p_wet = 0.56 if s else p * 0.62
        s = rng.random() < p_wet
        wet[i] = s
    tmax = np.array([TNORM[d.month - 1] for d in days]) + e - 1.4 * wet
    # summers held to their character: the summer's wet-day count and mean maximum
    idx = {d: i for i, d in enumerate(days)}
    for y, (tm, wf) in SUMMER_TARGET.items():
        ii = np.array([idx[d] for d in summer_days(y)])
        target = int(round(wf * len(ii)))
        u = rng.random(len(ii)) * 0.55 + 0.45 * wet[ii]
        order = np.argsort(-u)
        w = np.zeros(len(ii), bool)
        w[order[:target]] = True
        wet[ii] = w
        t = np.array([TNORM[days[i].month - 1] for i in ii]) + e[ii] - 1.4 * w
        t = t - t.mean() + tm
        tmax[ii] = t
    tmin = tmax - (7.5 + rng.normal(0, 1.4, n)) + 1.8 * wet
    rain = np.where(wet, 1.0 + rng.gamma(0.75, 6.0, n), np.where(rng.random(n) < 0.22, np.round(rng.uniform(0.1, 0.9, n), 1), 0.0))
    sun = np.clip(np.where(wet, rng.gamma(2.0, 1.4, n), 2.0 + rng.gamma(3.0, 1.9, n)) * (0.55 + 0.45 * np.array(
        [math.sin(math.pi * (d.timetuple().tm_yday - 1) / 365.0) for d in days])), 0, 15.8)
    return {"days": days, "idx": idx, "tmax": np.round(tmax, 1), "tmin": np.round(tmin, 1),
            "rain": np.round(rain, 1), "sun": np.round(sun, 1),
            "wet": np.round(rain, 1) >= 1.0}


# ------------------------------------------------------------------ the cycleways and their counters
# (segment code, segment name, capacity per hour both directions, daily mix commute/leisure/utility at the
#  weekday-term level, target busiest-cell flow over capacity on a dry 20 C day at the 2027 level)
CYCLEWAYS = [
    ("CW1", "Tolland Road", [
        ("TR1", "Cathedral Green to St Anne's Gate", 1400, (2900, 600, 2600), 0.66),
        ("TR2", "St Anne's Gate to Mill Lane", 1150, (2400, 500, 2000), 0.68),
        ("TR3", "Tolland Bridge", 650, (2050, 300, 2400), 1.10),
        ("TR4", "Mill Lane to Ashby Park", 900, (1700, 400, 1200), 0.66)]),
    ("CW2", "Brickfields", [
        ("BF1", "Station Square to Infirmary Road", 1400, (3600, 500, 900), 0.70),
        ("BF2", "Gasworks Lane", 650, (2050, 150, 250), 1.02),
        ("BF3", "Kiln Street to Brickfields Estate", 900, (2200, 300, 400), 0.72)]),
    ("CW3", "Estuary Path", [
        ("EP1", "Quayside", 1400, (1500, 4200, 1600), 0.62),
        ("EP2", "The Boardwalk", 650, (400, 3300, 400), 0.86),
        ("EP3", "Saltings to Heron Point", 900, (600, 3000, 600), 0.62),
        ("EP4", "Heron Point to Shingle Bay", 1150, (900, 3600, 900), 0.62)]),
    ("CW4", "Wardle Park", [
        ("WP1", "Exchange Street to Park Gates", 1150, (1800, 2600, 1300), 0.60),
        ("WP2", "Lido Gate", 650, (900, 2100, 700), 0.78),
        ("WP3", "Bandstand to Wardle Hill", 900, (1100, 2300, 800), 0.60)]),
    ("CW5", "Market Street", [
        ("MS1", "Corn Exchange", 1150, (1600, 900, 4200), 0.60),
        ("MS2", "Butter Market", 650, (700, 400, 3900), 0.92),
        ("MS3", "Guild Street", 900, (900, 500, 3000), 0.64),
        ("MS4", "Tanners Row", 900, (800, 500, 2600), 0.60),
        ("MS5", "Haymarket Steps", 650, (500, 300, 2400), 0.72)]),
    ("CW6", "Southfield", [
        ("SF1", "Southgate to Belvoir Road", 1150, (2400, 1200, 1300), 0.60),
        ("SF2", "Belvoir Road to Fenn Common", 900, (1600, 900, 800), 0.64),
        ("SF3", "Fenn Common Bridge", 650, (1200, 600, 500), 0.80)]),
]
HEADLINE = ["TR1", "BF1", "EP1", "WP1", "MS1", "SF1"]       # permanent dashboard counters, run all year
CAPACITY_BANDS = [(2.0, 2.5, 450), (2.5, 3.0, 650), (3.0, 3.5, 900), (3.5, 4.0, 1150), (4.0, 4.5, 1400),
                  (4.5, 5.0, 1650), (5.0, 9.9, 1900)]

SEGMENTS = {}
for cw, cwname, segs in CYCLEWAYS:
    for code, name, cap, mix, vc in segs:
        SEGMENTS[code] = dict(cw=cw, cwname=cwname, name=name, cap=cap, mix=mix, vc=vc)


def base_volumes():
    """daily volume per group at the 2026 level so that the busiest typical cell sits at the target ratio in 2027"""
    out = {}
    for code, s in SEGMENTS.items():
        best = 0.0
        for dt in ("wk_term", "we"):
            grp = "wk" if dt != "we" else "we"
            f = np.zeros(24)
            for pi, p in enumerate(PURP):
                f += s["mix"][pi] * DTM[p][dt] * TREND[p] * PROF[p][grp]
            best = max(best, f[6:22].max())
        k = s["vc"] * s["cap"] / best
        out[code] = np.array(s["mix"], float) * k
    return out


CAPTURE = {"TR1": 0.962, "BF1": 0.948, "EP1": 0.971, "WP1": 0.957, "MS1": 0.936, "SF1": 0.966}

# events in the city's programme that move riders past nearby counters: (date, counters, groups, hours, factor)
EP_ALL = ["EP1", "EP2", "EP3", "EP4"]
MS_ALL = ["MS1", "MS2", "MS3", "MS4", "MS5"]
EVENT_EFFECTS = []
for _d in (date(2024, 6, 15), date(2025, 6, 14), date(2026, 6, 13)):          # half marathon: path closed to cycles
    EVENT_EFFECTS.append((_d, EP_ALL, PURP, range(7, 13), 0.28))
for _d in (date(2024, 7, 6), date(2024, 7, 7), date(2025, 7, 5), date(2025, 7, 6), date(2026, 7, 4), date(2026, 7, 5)):
    EVENT_EFFECTS.append((_d, ["EP1", "EP2"], ["leisure"], range(10, 22), 1.28))   # harbour festival
for _d in (date(2024, 7, 20), date(2025, 7, 19), date(2026, 7, 18)):
    EVENT_EFFECTS.append((_d, ["WP1", "WP2", "WP3"], ["leisure"], range(16, 22), 1.38))   # proms in the park
for _d in (date(2024, 8, 10), date(2025, 8, 9), date(2026, 8, 8)):
    EVENT_EFFECTS.append((_d, ["MS1", "MS2"], ["utility"], range(9, 17), 1.14))   # food and makers market
for _d in (date(2024, 8, 24), date(2025, 8, 23), date(2026, 8, 22)):
    EVENT_EFFECTS.append((_d, MS_ALL, PURP, range(12, 16), 0.55))                  # pride parade: street closed
    EVENT_EFFECTS.append((_d, MS_ALL, ["leisure"], range(16, 20), 1.30))
for _d in (date(2025, 6, 28), date(2026, 6, 27)):
    EVENT_EFFECTS.append((_d, ["TR1"], ["leisure"], range(19, 22), 1.45))         # open air cinema


def event_factor(code, p, days):
    """days x 24 multiplicative factor on group p at counter code"""
    f = np.ones((len(days), 24))
    pos = {d: i for i, d in enumerate(days)}
    for d, codes, groups, hours, fac in EVENT_EFFECTS:
        if code in codes and p in groups and d in pos:
            for h in hours:
                f[pos[d], h] *= fac
    return f


# ------------------------------------------------------------------ simulation of hourly cyclists
def simulate_counter(rng, code, base, days, weather, city):
    """expected and drawn hourly cyclists by direction for one counter over a list of days.
    Returns (lam_in, lam_out, n_in, n_out, comps) with arrays days x 24."""
    n = len(days)
    W = weather
    ii = np.array([W["idx"][d] for d in days])
    wet = W["wet"][ii].astype(float)
    tmax = W["tmax"][ii]
    dts = [daytype(d) for d in days]
    grp = ["wk" if t != "we" else "we" for t in dts]
    cshock = rng.normal(0, NOISE["day"], n)
    lam_in = np.zeros((n, 24))
    lam_out = np.zeros((n, 24))
    comps = []
    for pi, p in enumerate(PURP):
        aw, at = WX[p]
        pshock = rng.normal(0, NOISE["purp"], n)
        dtm = np.array([DTM[p][t] for t in dts])
        seas = np.array([SEASON[p][d.month - 1] for d in days])
        yrs = np.array([(d - date(2026, 7, 16)).days / 365.25 for d in days])
        vol = base[pi] * dtm * seas * np.exp(aw * wet + at * (tmax - 20.0) + cshock + pshock + city) * TREND[p] ** yrs
        prof = np.array([PROF[p][g] for g in grp])
        c = vol[:, None] * prof * event_factor(code, p, days)
        comps.append(c)
        lam_in += c * INSHARE[p][None, :]
        lam_out += c * (1 - INSHARE[p][None, :])
    hn = np.exp(rng.normal(0, NOISE["hour"], (n, 24)))
    lam_in *= hn
    lam_out *= hn
    n_in = rng.poisson(lam_in)
    n_out = rng.poisson(lam_out)
    return lam_in, lam_out, n_in, n_out, comps


def build_truth():
    rng_w = np.random.default_rng([SEED, 1])
    W = make_weather(rng_w)
    base = base_volumes()
    rng_city = np.random.default_rng([SEED, 2])
    allyear = span_days(date(2024, 1, 1), date(2026, 9, 30))
    city_all = {d: v for d, v in zip(allyear, rng_city.normal(0, NOISE["city"], len(allyear)))}
    T = {"weather": W, "base": base, "summer": {}, "fullyear": {}}
    # summer counters (every counter) June to August: headline counters are cut from their full-year run
    for k, code in enumerate(SEGMENTS):
        if code in HEADLINE:
            continue
        T["summer"][code] = {}
        for y in SUMMERS:
            rng = np.random.default_rng([SEED, 10, k, y])
            ds = summer_days(y)
            city = np.array([city_all[d] for d in ds])
            T["summer"][code][y] = (ds,) + simulate_counter(rng, code, base[code], ds, W, city)
    for k, code in enumerate(HEADLINE):
        rng = np.random.default_rng([SEED, 20, k])
        city = np.array([city_all[d] for d in allyear])
        res = simulate_counter(rng, code, base[code], allyear, W, city)
        T["fullyear"][code] = (allyear,) + res
        T["summer"][code] = {}
        pos = {d: i for i, d in enumerate(allyear)}
        for y in SUMMERS:
            ds = summer_days(y)
            sl = np.array([pos[d] for d in ds])
            T["summer"][code][y] = (ds, res[0][sl], res[1][sl], res[2][sl], res[3][sl], [c[sl] for c in res[4]])
    return T


def summer_twoway(T):
    """counted cyclists both directions, days x 24, per counter per summer (before any export mess)"""
    return {code: {y: (T["summer"][code][y][3] + T["summer"][code][y][4]).astype(float) for y in SUMMERS}
            for code in SEGMENTS}


def cycleway_of(code):
    return SEGMENTS[code]["cw"]


def capacity_for_width(w):
    for lo, hi, cap in CAPACITY_BANDS:
        if lo <= w < hi:
            return cap
    raise ValueError(w)
