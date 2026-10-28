"""task270 world: the network's twelve areas and their SA2s, every resident born in or before 1966 followed person
by person from 1 January 2016 to 30 June 2027 (birth date, sex, SA2, aged care entry, arrival, departure, death), the
younger residents as cohorts, and the after-hours service's 2026 attendances.

Each area's residents aged 60 and over in 2016 carry its history in their cohorts' sizes: the coast's retirement
arrivals of the 1990s and 2000s (born about 1937 to 1943) are reaching 85 during 2024 to 2026, Spraymouth's earlier
arrivals (born about 1931) are in their nineties, and Cobbleton's and the inland areas' cohorts born after the late
1930s left young. Deaths follow a Gompertz hazard that decelerates at the oldest ages, improves 1.2 per cent a year,
peaks in winter and is higher in residential aged care; every person keeps one exponential draw, so a change in an
area's mortality level moves its deaths smoothly (tune.py)."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

D0 = dt.date(2016, 1, 1)
D_END = dt.date(2027, 7, 1)          # the person record runs to 30 June 2027
B_GOMP = 0.100                        # Gompertz slope at old ages
GAMMA = 0.45                          # old-age deceleration
IMPROVE = 0.012                       # mortality improvement a year
SEX_F = {"M": 1.20, "F": 0.87}
RACF_F = 1.55                         # mortality in residential aged care against the same age at home
SEASON = np.array([0.93, 0.92, 0.95, 0.99, 1.04, 1.10, 1.14, 1.12, 1.04, 0.98, 0.94, 0.95])
SEASON = SEASON / SEASON.mean()
HIST_LEVEL = 0.080                    # the rate at 85 the cohorts' survival to 2016 is taken at (fixed, so tuning an
#                                       area's current level moves its deaths and not its population)
OLD_SHARE = {"coast": 0.41, "city": 0.27, "inland": 0.35, "peri": 0.28}   # share of 2026 residents born by 1966


def days(d):
    return (d - D0).days


def from_days(n):
    return D0 + dt.timedelta(days=int(n))


def nat_index(c):
    """Births in New South Wales by year of birth, relative: the Depression dip of the early 1930s and the rise after
    1938 (a smooth stand-in for the registered series)."""
    xs = [1880, 1890, 1900, 1910, 1914, 1920, 1925, 1929, 1932, 1935, 1939, 1942, 1946, 1950, 1955, 1961, 1966]
    ys = [0.38, 0.45, 0.55, 0.70, 0.78, 0.90, 0.88, 0.84, 0.74, 0.76, 0.84, 0.95, 1.10, 1.18, 1.22, 1.30, 1.27]
    return np.interp(c, xs, ys)


def wave(c, waves):
    f = np.ones_like(np.asarray(c, dtype=float))
    for amp, centre, sd in waves:
        f = f + amp * np.exp(-0.5 * ((np.asarray(c, dtype=float) - centre) / sd) ** 2)
    return f


def hazard(level, age, year_frac, sexf, racf):
    """Annual death rate at an exact age and calendar time (old ages); level is the area's rate at 85 in mid 2025."""
    x = level * sexf * np.exp(B_GOMP * (age - 85.0))
    h = x / (1.0 + GAMMA * x) * np.exp(-IMPROVE * (year_frac - 2025.5))
    return h * np.where(racf, RACF_F, 1.0)


class Area:
    def __init__(self, i, row):
        self.i = i
        self.name, self.code, self.type, sa2names, self.pop2026, self.waves, self.interstate = row
        sa4 = "130" if self.type == "inland" else "129"
        self.sa2 = []
        for j, nm in enumerate(sa2names):
            sa3 = "%02d" % (1 + (i % 6))
            self.sa2.append(("%s%s%04d" % (sa4, sa3, 1001 + 10 * (i // 6) * 7 + j * 3 + i % 3), nm))
        n = len(self.sa2)
        g = K.rng("sa2w", self.name)
        # SA2 weights: the town SA2s hold more of the old and the aged care beds, the surrounds more of the young
        self.w_old = np.array([1.4 if ("Surrounds" not in nm) else 0.8 for _, nm in self.sa2]) * g.uniform(0.7, 1.3, n)
        self.w_old /= self.w_old.sum()
        self.w_young = np.array([1.0 if ("Surrounds" not in nm) else 1.3 for _, nm in self.sa2]) * g.uniform(0.7, 1.3, n)
        self.w_young /= self.w_young.sum()


def areas():
    return [Area(i, row) for i, row in enumerate(K.AREAS)]


# ------------------------------------------------------------------------------------------------- the old (person by person)
def survival_hist(level, sexf, c, to_age):
    """Survival of a cohort born in year c from 60 to an exact age, at the mortality of the decades it lived through
    (1.5 per cent a year higher for each year before 2016)."""
    s = 0.0
    a = 60.0
    while a < to_age - 1e-9:
        step = min(1.0, to_age - a)
        yr = c + a + step / 2
        h = level * sexf * math.exp(B_GOMP * (a + step / 2 - 85.0))
        h = h / (1 + GAMMA * h) * math.exp(0.015 * (2016 - yr)) if yr < 2016 else h / (1 + GAMMA * h)
        s += h * step
        a += step
    return math.exp(-s)


def _poisson_q(u, lam):
    """The Poisson quantile at a fixed uniform: the count moves monotonically with its mean, so a change in an area's
    mortality level moves its cohorts' sizes smoothly."""
    if lam <= 0:
        return 0
    if lam > 50:
        return max(0, int(round(lam + math.sqrt(lam) * math.sqrt(2) * _erfinv(min(max(2 * u - 1, -0.999999), 0.999999)))))
    k, p = 0, math.exp(-lam)
    c = p
    while c < u and k < 100000:
        k += 1
        p *= lam / k
        c += p
    return k


def _erfinv(y):
    a = 0.147
    ln = math.log(1 - y * y)
    t = 2 / (math.pi * a) + ln / 2
    return math.copysign(math.sqrt(math.sqrt(t * t - ln / a) - t), y)


def _draw(cols, a, sex, n, key, entry_day=None, dob=None, mover=0):
    """n people of one area, sex and cohort (or arrival year), each with draws from its own stream so no other
    cohort's size moves them."""
    g = K.rng(*key)
    pool = max(n, 1)
    doy = g.integers(0, 365, pool)[:n]
    sa2u = g.random(pool)[:n]
    racf = (83 + g.exponential(16.0, pool))[:n]
    ed = g.exponential(1.0, pool)[:n]
    ee = g.exponential(1.0, pool)[:n]
    if n == 0:
        return
    cols["area"].append(np.full(n, a.i))
    cols["sex"].append(np.full(n, 0 if sex == "F" else 1))
    cols["dob"].append(dob if dob is not None else doy)
    cw = np.cumsum(a.w_old)
    cols["sa2"].append(np.minimum(np.searchsorted(cw, sa2u * cw[-1]), len(a.sa2) - 1))
    cols["entry"].append(entry_day if entry_day is not None else np.zeros(n, dtype=int))
    cols["racf_age"].append(racf)
    cols["e_death"].append(ed)
    cols["e_exit"].append(ee)
    cols["mover"].append(np.full(n, mover))


def build_people(A, levels, scale=None):
    """The person file. levels: area -> its mortality level (the rate at 85 in mid 2025). scale: area -> the size of its
    cohorts at 60 per unit of the national index (calibrate_scale sets it so each area's 2026 residents born by 1966 are
    OLD_SHARE of its 2026 population)."""
    cols = {k: [] for k in ("area", "sex", "dob", "sa2", "entry", "racf_age", "e_death", "e_exit", "mover")}
    if scale is None:
        scale = {a.name: 1.0 for a in A}
    for a in A:
        for sex in ("F", "M"):
            sexf = SEX_F[sex]
            share = 0.505 if sex == "F" else 0.495
            for c in range(1890, 1967):
                age16 = 2016 - c - 0.5
                base = scale[a.name] * share * float(nat_index(c)) * float(wave(c, a.waves))
                base *= 1.0 + K.rng("coh", a.name, sex, c).normal(0, 0.035)
                if age16 >= 60:
                    base *= survival_hist(HIST_LEVEL, sexf, c, age16)
                n = _poisson_q(K.rng("n", a.name, sex, c).random(), max(base, 0.0))
                g = K.rng("dob", a.name, sex, c)
                doy = g.integers(0, 365, max(n, 1))[:n]
                dob = np.array([days(dt.date(c, 1, 1)) + int(x) for x in doy], dtype=int)
                _draw(cols, a, sex, n, ("person", a.name, sex, c), dob=dob)
        # arrivals 2016 to 2026 at 60 to 74: retirees to the coast and the fringe, fewer elsewhere
        rate = {"coast": 0.0075, "peri": 0.0040, "city": 0.0020, "inland": 0.0010}[a.type]
        for y in range(2016, 2027):
            for sex in ("F", "M"):
                band = sum(float(nat_index(c)) * float(wave(c, a.waves)) for c in range(y - 74, y - 59))
                n = _poisson_q(K.rng("n_arr", a.name, sex, y).random(), scale[a.name] * 0.5 * rate * band)
                g = K.rng("arr", a.name, sex, y)
                age = g.uniform(60, 75, max(n, 1))[:n]
                entry_day = np.array([days(dt.date(y, 1, 1)) + int(x) for x in g.integers(0, 365, max(n, 1))[:n]],
                                     dtype=int)
                dob = (entry_day - age * 365.25).astype(int)
                keep = dob <= days(dt.date(1966, 12, 31))
                if keep.sum() == 0:
                    continue
                k = int(keep.sum())
                _draw(cols, a, sex, k, ("arrival", a.name, sex, y), entry_day=entry_day[keep], dob=dob[keep],
                      mover=1)
    P = {k: np.concatenate(v) for k, v in cols.items()}
    P["e_death"] = P["e_death"].astype(float)
    return P


def simulate(P, A, levels):
    """Death and departure days for every person, monthly steps from 1 January 2016 (or arrival) to 30 June 2027."""
    n = len(P["dob"])
    lev = np.array([levels[a.name] for a in A])[P["area"]]
    sexf = np.where(P["sex"] == 1, SEX_F["M"], SEX_F["F"])
    atype = np.array([a.type for a in A])[P["area"]]
    exit_base = np.where(atype == "coast", 0.0030, np.where(atype == "city", 0.0035,
                                                             np.where(atype == "inland", 0.0065, 0.0040)))
    Hd = np.zeros(n)
    He = np.zeros(n)
    death = np.full(n, -1, dtype=int)
    gone = np.full(n, -1, dtype=int)
    y, m = 2016, 1
    while (y, m) < (2027, 7):
        start = days(dt.date(y, m, 1))
        nm = dt.date(y + (m == 12), m % 12 + 1, 1)
        end = days(nm)
        mlen = end - start
        alive = (death < 0) & (gone < 0) & (P["entry"] < end)
        frac_start = np.clip(P["entry"], start, end)
        active = np.where(alive, (end - frac_start) / 365.25, 0.0)
        mid = (frac_start + end) / 2.0
        age = (mid - P["dob"]) / 365.25
        yf = y + (m - 0.5) / 12.0
        racf = age >= P["racf_age"]
        hd = hazard(lev, age, yf, sexf, racf) * SEASON[m - 1]
        he = np.where(age < 75, exit_base, np.where(age < 85, 0.0015, 0.0006))
        nd = Hd + hd * active
        ne = He + he * active
        cross_d = alive & (nd >= P["e_death"])
        cross_e = alive & (ne >= P["e_exit"])
        # the time within the month each crossing happens; the earlier event wins
        td = np.where(cross_d, frac_start + (P["e_death"] - Hd) / np.maximum(hd, 1e-12) * 365.25, np.inf)
        te = np.where(cross_e, frac_start + (P["e_exit"] - He) / np.maximum(he, 1e-12) * 365.25, np.inf)
        dies = cross_d & (td <= te)
        leaves = cross_e & (te < td)
        death[dies] = np.minimum(np.floor(td[dies]).astype(int), end - 1)
        gone[leaves] = np.minimum(np.floor(te[leaves]).astype(int), end - 1)
        Hd, He = nd, ne
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    P["death"] = death
    P["gone"] = gone
    return P


def alive_on(P, day):
    """Residents on a day (arrived on or before it, not dead or gone before it)."""
    d = days(day)
    return (P["entry"] <= d) & ((P["death"] < 0) | (P["death"] >= d)) & ((P["gone"] < 0) | (P["gone"] >= d))


def ages_on_fast(P, day):
    """Age in completed years on a day, vectorised over the person file."""
    dob_dates = P["_dob_ymd"]
    yy, mm, dd = dob_dates
    return day.year - yy - (((day.month < mm) | ((day.month == mm) & (day.day < dd))).astype(int))


def add_ymd(P):
    ds = [from_days(x) for x in P["dob"]]
    P["_dob_ymd"] = (np.array([d.year for d in ds]), np.array([d.month for d in ds]), np.array([d.day for d in ds]))
    return P


def calibrate_scale(A, levels):
    """The size of each area's cohorts at 60 per unit of the national index, so its 2026 residents born by 1966 are
    OLD_SHARE of the 2026 population (one pass at unit scale, then proportional)."""
    unit = {a.name: 100.0 for a in A}
    ref = {a.name: HIST_LEVEL for a in A}
    P = simulate(add_ymd(build_people(A, ref, unit)), A, ref)
    on = alive_on(P, dt.date(2026, 6, 30))
    out = {}
    for a in A:
        n = int((on & (P["area"] == a.i)).sum())
        out[a.name] = 100.0 * OLD_SHARE[a.type] * a.pop2026 / max(n, 1)
    return out


# ------------------------------------------------------------------------------------------------- the young (cohorts)
def young_shape(area_type, age):
    """Relative size of the cohorts born from 1967 by age in 2026, by kind of area."""
    a = np.asarray(age, dtype=float)
    base = 1.0 + 0.0 * a
    if area_type == "city":
        base = base + 0.35 * np.exp(-0.5 * ((a - 24) / 6) ** 2) - 0.05
    elif area_type == "coast":
        base = base - 0.30 * np.exp(-0.5 * ((a - 26) / 6) ** 2) + 0.18 * np.exp(-0.5 * ((a - 54) / 6) ** 2)
    elif area_type == "inland":
        base = base - 0.38 * np.exp(-0.5 * ((a - 25) / 6) ** 2) + 0.06 * np.exp(-0.5 * ((a - 52) / 8) ** 2)
    else:
        base = base + 0.20 * np.exp(-0.5 * ((a - 40) / 8) ** 2) + 0.12 * np.exp(-0.5 * ((a - 8) / 6) ** 2) \
            - 0.15 * np.exp(-0.5 * ((a - 22) / 4) ** 2)
    return np.clip(base, 0.4, None)


def young_rate(age, sex):
    a = np.asarray(age, dtype=float)
    r = np.where(a < 1, 0.0042, 0.00010 + 0.0000060 * np.exp(0.1 * a) + np.where((a > 15) & (a < 30), 0.00035, 0.0))
    return r * (1.55 if sex == "M" else 1.0)


def young_migration(area_type, age):
    """Net migration a year by single age for the residents born from 1967: the inland and the coast lose their young
    adults, the city gains students and loses graduates, the fringe gains families; the coast gains working-age
    families and people in their fifties."""
    a = np.asarray(age, dtype=float)
    bump = lambda c, s: np.exp(-0.5 * ((a - c) / s) ** 2)
    if area_type == "inland":
        return -0.055 * bump(20, 2.5) + 0.010 * bump(35, 6) + 0.006 * bump(8, 4)
    if area_type == "coast":
        return -0.040 * bump(20, 2.5) + 0.028 * bump(36, 8) + 0.024 * bump(54, 5) + 0.012 * bump(6, 4)
    if area_type == "city":
        return 0.050 * bump(19, 2) - 0.012 * bump(26, 3) + 0.016 * bump(34, 7) + 0.008 * bump(6, 4)
    return 0.034 * bump(33, 7) + 0.022 * bump(6, 4) - 0.020 * bump(21, 3)


def young_cohorts(A, n1966):
    """Births by year (1967 to 2026) per area, carried through the area's net migration by age, sized so the cohort
    born in 1967 continues the person file's cohort born in 1966: n1966 holds that cohort's residents by sex at 30 June
    of each year from 2016 to 2026, and from 49 to 59 each later cohort follows the same path and sex mix."""
    out = {}
    for a in A:
        g = K.rng("young", a.name)
        births = np.array([float(nat_index(min(c, 1966))) * (1.0 + 0.004 * max(0, c - 1966)) for c in range(1967, 2027)])
        births *= 1 + g.normal(0, 0.06, len(births))
        mig = young_migration(a.type, np.arange(60))
        n = n1966[a.name]["F"] + n1966[a.name]["M"]
        surv = np.ones(60)
        for x in range(1, 50):
            surv[x] = surv[x - 1] * (1 + mig[x - 1])
        for x in range(50, 60):
            surv[x] = surv[49] * n[x - 49] / n[0]
        m49 = n1966[a.name]["M"][0] / n[0]
        male = np.array([0.513 + (m49 - 0.513) * x / 49 if x <= 49 else n1966[a.name]["M"][x - 49] / n[x - 49]
                         for x in range(60)])
        scale = n[0] / (births[0] * surv[49])
        out[a.name] = {"births": births * scale, "surv": surv, "male": male,
                       "noise": {s: 1 + g.normal(0, 0.012, (len(births), 61)) for s in ("F", "M")}}
    return out


def young_pop(Y, area, sex, year, on_census=False):
    """Population by single age (to 59) at 30 June of a year, or on census night 2021, for the residents born from
    1967: each birth cohort carried through the area's net migration at each age. At 30 June half of a year's births
    have had their birthday; on census night 222 of 365 days' births have."""
    y = Y[area]
    first = 222 / 365 if on_census else 0.5        # the share of a cohort past its birthday on the day

    def cohort(c, age):
        if c < 1967 or c > 2026 or age < 0 or age > 59:
            return 0.0
        share = y["male"][age] if sex == "M" else 1 - y["male"][age]
        return y["births"][c - 1967] * share * y["surv"][age] * y["noise"][sex][c - 1967, min(year - 2016, 10)]
    out = np.zeros(116)
    for age in range(60):
        out[age] = first * cohort(year - age, age) + (1 - first) * cohort(year - age - 1, age)
    return out
