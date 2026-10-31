"""The clean truth: Dalisay City's barangays, the CBMS 2025 tables, weekly dengue transmission by place,
and every notified case with the barangay it was infected in (which no shipped file carries).

Exposure. Children, residents not working and the elderly are exposed in their home barangay. A working
resident is exposed at the place of work for a share PHI of the mosquito's feeding hours and at home for
the rest. Work in San Roque is work at the Dalisay Industrial Estate (an export processing zone inside the
barangay) except for San Roque's own residents, a part of whom work in the old village.
"""
import datetime as dt

import numpy as np

from common import rng, mw_start, all_weeks, MW1_START, WEEKS_IN

PHI = 0.60                     # a working resident's share of exposure spent at the workplace
REP = {"child": 0.30, "employed": 0.24, "other": 0.24, "elderly": 0.30}   # notified share of infections
GROUPS = ("child", "employed", "other", "elderly")
LAMBDA0 = 0.00058              # infections per person-week of full exposure at a season's peak, base 1.0

# name, role, population 2025, share of working residents employed in San Roque (the estate),
# share employed in the Poblacion, baseline multiplier
BARANGAYS = [
    ("San Roque", "estate_host", 8150, 0.18, 0.07, 0.95),
    ("Poblacion", "cbd", 9420, 0.04, 0.00, 0.70),
    ("Bagumbayan", "loc1", 46780, 0.04, 0.035, 1.00),
    ("Maligaya", "loc2", 30640, 0.03, 0.035, 1.00),
    ("Tabing-Ilog", "dorm", 22410, 0.313, 0.020, 0.70),
    ("Pulong Bayabas", "dorm", 19060, 0.381, 0.020, 0.68),
    ("Malinta", "dorm", 25330, 0.291, 0.020, 0.70),
    ("Kanluran", "dorm", 18240, 0.388, 0.020, 0.72),
    ("Burol", "dorm", 21290, 0.356, 0.020, 0.69),
    ("Silangan", "dorm", 24570, 0.296, 0.020, 0.68),
    ("San Isidro", "ordinary", 27310, 0.05, 0.042, 1.10),
    ("San Jose", "ordinary", 31480, 0.04, 0.038, 1.12),
    ("Santa Cruz", "ordinary", 23960, 0.03, 0.045, 1.05),
    ("San Antonio", "ordinary", 29870, 0.06, 0.035, 1.00),
    ("Rizal", "ordinary", 15420, 0.05, 0.042, 0.95),
    ("Mabini", "ordinary", 21170, 0.04, 0.038, 1.15),
    ("Bonifacio", "ordinary", 18830, 0.03, 0.032, 1.20),
    ("Masagana", "ordinary", 34650, 0.06, 0.028, 0.98),
    ("Pag-asa", "ordinary", 26210, 0.05, 0.035, 1.08),
    ("Sampaloc", "ordinary", 12940, 0.04, 0.045, 0.92),
    ("Dila", "ordinary", 20760, 0.07, 0.025, 1.02),
    ("Lumbia", "ordinary", 33190, 0.06, 0.032, 1.06),
    ("Parian", "ordinary", 16580, 0.03, 0.045, 1.25),
    ("Tagumpay", "ordinary", 28940, 0.05, 0.038, 0.97),
    ("Liwayway", "ordinary", 22330, 0.04, 0.035, 1.04),
    ("Bayanihan", "ordinary", 30120, 0.06, 0.032, 1.01),
    ("Santo Tomas", "ordinary", 17860, 0.04, 0.042, 0.99),
    ("Santo Tomas Norte", "ordinary", 11420, 0.05, 0.038, 1.09),
    ("Mangga", "ordinary", 24890, 0.03, 0.035, 0.93),
    ("Ilaya", "ordinary", 26740, 0.02, 0.028, 1.16),
    ("Malanday", "ordinary", 19480, 0.04, 0.032, 1.03),
    ("Talon", "ordinary", 25660, 0.05, 0.035, 0.96),
    ("Bulihan", "ordinary", 31950, 0.03, 0.038, 1.07),
    ("Halang", "ordinary", 14370, 0.06, 0.042, 1.12),
    ("Concepcion", "ordinary", 27820, 0.04, 0.045, 0.94),
    ("Santo Nino", "ordinary", 22190, 0.05, 0.035, 1.01),
]
NAMES = [b[0] for b in BARANGAYS]
N = len(NAMES)
IDX = {n: i for i, n in enumerate(NAMES)}
SR, POB = IDX["San Roque"], IDX["Poblacion"]
LOC1, LOC2 = IDX["Bagumbayan"], IDX["Maligaya"]
DORMS = [i for i, b in enumerate(BARANGAYS) if b[1] == "dorm"]
SPLIT_FROM, SPLIT_NEW = IDX["Santo Tomas"], IDX["Santo Tomas Norte"]
SPLIT_DATE = dt.date(2025, 3, 17)

GROUP_SHARE = {"child": 0.286, "employed": 0.402, "other": 0.247, "elderly": 0.065}
# the barangays of boarding houses beside the estate: young working residents, fewer children
GROUP_SHARE_DORM = {"child": 0.200, "employed": 0.605, "other": 0.115, "elderly": 0.050}

# the season: amplitude, peak week and width by year
SEASON = {2022: (1.05, 34, 7.0), 2023: (0.62, 36, 6.5), 2024: (0.92, 33, 7.5),
          2025: (0.78, 35, 7.0), 2026: (0.88, 34, 6.8), 2027: (1.18, 31, 6.2)}


def season(year, week):
    a, c, s = SEASON[year]
    return a * (0.16 + 0.84 * np.exp(-0.5 * ((week - c) / s) ** 2))


def population_tables():
    """CBMS 2025: residents by barangay and group, and the place-of-work matrix of working residents."""
    r = rng("cbms")
    pop = np.array([b[2] for b in BARANGAYS], dtype=float)
    grp = np.zeros((N, 4))
    for i in range(N):
        base_sh = GROUP_SHARE_DORM if BARANGAYS[i][1] == "dorm" else GROUP_SHARE
        sh = np.array([base_sh[g] for g in GROUPS]) * r.uniform(0.94, 1.06, 4)
        sh /= sh.sum()
        grp[i] = np.round(pop[i] * sh)
    # place of work, columns 0..N-1 the city's barangays, column N outside the city
    OWN = {"dorm": (0.03, 0.06), "ordinary": (0.18, 0.28), "loc1": (0.20, 0.26), "loc2": (0.20, 0.26),
           "estate_host": (0.10, 0.14), "cbd": (0.30, 0.34)}
    OUT = {"dorm": (0.15, 0.22), "ordinary": (0.30, 0.40), "loc1": (0.22, 0.28), "loc2": (0.22, 0.28),
           "estate_host": (0.14, 0.18), "cbd": (0.24, 0.28)}
    W = np.zeros((N, N + 1))
    for i, b in enumerate(BARANGAYS):
        role, est, cbd = b[1], b[3], b[4]
        own = r.uniform(*OWN[role])
        out = r.uniform(*OUT[role])
        W[i, SR] += est
        W[i, POB] += cbd
        if i not in (SR, POB):
            W[i, i] += own
        else:
            W[i, i] += own
        rest = max(0.02, 1.0 - W[i].sum() - out)
        # the dormitory barangays near the estate are residential and hold few jobs for anyone else
        others = [j for j in range(N) if j not in (SR, POB, i) and BARANGAYS[j][1] != "dorm"]
        W[i, others] += r.dirichlet(np.full(len(others), 0.7)) * rest
        W[i, N] = out
        W[i] /= W[i].sum()
    workers = np.round(grp[:, 1][:, None] * W)
    return pop, grp, W, workers


def past_outbreaks():
    """Residential outbreaks of earlier seasons: (year, barangay, peak week, peak multiplier)."""
    r = rng("outbreaks")
    out = []
    pool = [i for i in range(N) if i not in (SR,)]
    for y in (2022, 2023, 2024, 2025, 2026):
        k = int(r.integers(2, 4))
        for i in r.choice(pool, size=k, replace=False):
            out.append((y, int(i), int(r.integers(31, 39)), float(r.uniform(2.6, 4.4))))
    out.append((2027, LOC1, 37, 6.2))
    out.append((2027, LOC2, 38, 9.2))
    return out


def estate_multiplier(year, week):
    """The estate's own transmission relative to San Roque's village: ordinary until the 2027 works."""
    if year < 2027 or week < 29:
        return 0.8
    # the Phase 3 works' excavations hold water from July 2027
    ramp = {29: 3.0, 30: 5.6, 31: 9.7, 32: 14.2, 33: 20.5, 34: 27.5, 35: 35.8, 36: 44.7,
            37: 53.8, 38: 59.4, 39: 61.9, 40: 58.9}
    return ramp.get(week, 58.9)


def place_rates():
    """lam_home[w, j]: the rate of a person exposed all day in barangay j's homes;
    lam_work[w, j]: the rate at a workplace in j (the estate for j = San Roque)."""
    r = rng("rates")
    weeks = all_weeks()
    base = np.array([b[5] for b in BARANGAYS])
    noise = r.lognormal(0.0, 0.10, (len(weeks), N))
    ob = past_outbreaks()
    lam_home = np.zeros((len(weeks), N))
    lam_work = np.zeros((len(weeks), N))
    for t, (y, w) in enumerate(weeks):
        mult = np.ones(N)
        for (oy, i, pw, pm) in ob:
            if oy == y:
                mult[i] *= 1.0 + (pm - 1.0) * np.exp(-0.5 * ((w - pw) / 2.6) ** 2)
        lam_home[t] = LAMBDA0 * season(y, w) * base * mult * noise[t]
        lam_work[t] = lam_home[t] / mult * 0.85          # workplaces do not share a village's outbreak
        lam_work[t, SR] = LAMBDA0 * season(y, w) * base[SR] * noise[t, SR] * estate_multiplier(y, w)
    lam_out = LAMBDA0 * np.array([season(y, w) for (y, w) in weeks]) * 1.0
    return weeks, lam_home, lam_work, lam_out


def simulate_cases(world_seed=0):
    """Every notified case, 2022 week 1 to 2027 week 40, with its true place of infection.

    Returns a list of dicts: year, week, home (barangay index), group, place (barangay index or -1 for
    outside the city), and the person's attributes drawn later."""
    pop, grp, W, workers = population_tables()
    weeks, lam_home, lam_work, lam_out = place_rates()
    r = rng("cases%d" % world_seed)
    cases = []
    for t, (y, w) in enumerate(weeks):
        for i in range(N):
            # before the 2025 split the two Santo Tomas barangays were one; people lived in both parts
            for gi, g in enumerate(GROUPS):
                n_i = grp[i, gi]
                if g == "employed":
                    # home part
                    m_home = n_i * REP[g] * (1 - PHI) * lam_home[t, i]
                    k = r.poisson(m_home)
                    cases += [(y, w, i, g, i)] * int(k)
                    # work parts
                    shares = W[i, :N]
                    if i == SR:
                        # San Roque's own workers: 70 per cent at the estate, the rest in the village
                        m_est = n_i * REP[g] * PHI * shares[SR] * 0.70 * lam_work[t, SR]
                        m_vil = n_i * REP[g] * PHI * shares[SR] * 0.30 * lam_home[t, SR]
                        ks = r.poisson([m_est, m_vil])
                        cases += [(y, w, i, g, SR)] * int(ks[0] + ks[1])
                        shares = shares.copy()
                        shares[SR] = 0.0
                    m_work = n_i * REP[g] * PHI * shares * lam_work[t]
                    kw = r.poisson(m_work)
                    for j in np.nonzero(kw)[0]:
                        cases += [(y, w, i, g, int(j))] * int(kw[j])
                    m_out = n_i * REP[g] * PHI * W[i, N] * lam_out[t]
                    ko = r.poisson(m_out)
                    cases += [(y, w, i, g, -1)] * int(ko)
                else:
                    m = n_i * REP[g] * lam_home[t, i]
                    k = r.poisson(m)
                    cases += [(y, w, i, g, i)] * int(k)
    return cases, (pop, grp, W, workers), (weeks, lam_home, lam_work, lam_out)


AGE_BANDS = {
    "child": ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
              [2, 3, 4, 5, 6, 8, 9, 10, 10, 10, 10, 9, 9, 8, 7]),
    "employed": (list(range(17, 65)), None),
    "other": (list(range(15, 65)), None),
    "elderly": (list(range(65, 92)), None),
}


def draw_age(r, g):
    ages, wts = AGE_BANDS[g]
    if wts is None:
        if g == "employed":
            wts = [np.exp(-0.5 * ((a - 31) / 10.5) ** 2) for a in ages]
        elif g == "other":
            wts = [3.0 if a < 22 else (1.0 if a < 50 else 1.4) for a in ages]
        else:
            wts = [np.exp(-(a - 65) / 9.0) for a in ages]
    p = np.array(wts, dtype=float)
    p /= p.sum()
    return int(r.choice(ages, p=p))


# ---- the notification process: who saw each case, and when it reached the line list ----
DRUS = [
    ("Dalisay Medical Center", "hospital"),
    ("Dalisay Doctors' Hospital", "hospital"),
    ("City Health Center I", "rhu"), ("City Health Center II", "rhu"), ("City Health Center III", "rhu"),
    ("City Health Center IV", "rhu"), ("City Health Center V", "rhu"), ("City Health Center VI", "rhu"),
    ("Dalisay Family Clinic", "clinic"), ("Dalisay East Medical Clinic", "clinic"),
    ("Dalisay Diagnostic and Wellness Center", "clinic"),
]


def health_center_of(i):
    return 2 + (i * 7 + 3) % 6


def assign_attributes(cases, world_seed=0):
    """Attach to each case its person, dates, reporting unit, admission, classification and travel."""
    r = rng("attrs%d" % world_seed)
    out = []
    for k, (y, w, i, g, j) in enumerate(cases):
        age = draw_age(r, g)
        sex = "F" if r.random() < (0.47 if g == "employed" else 0.50) else "M"
        onset = mw_start(y, w) + dt.timedelta(days=int(r.integers(0, 7)))
        consult = onset + dt.timedelta(days=int(1 + r.poisson(2.1)))
        u = r.random()
        p_dmc = 0.30 if g != "employed" else 0.24
        p_ddh = 0.12 if g != "employed" else 0.24
        if u < p_dmc:
            dru = 0
        elif u < p_dmc + p_ddh:
            dru = 1
        elif u < p_dmc + p_ddh + 0.10:
            dru = 8 + int(r.integers(0, 3))
        else:
            dru = health_center_of(i)
        kind = DRUS[dru][1]
        if kind == "hospital":
            rep = consult + dt.timedelta(days=int(r.integers(0, 3) if dru == 0 else r.integers(1, 5)))
        elif kind == "rhu":
            # the centres send their week's notifications every Friday
            days_to_friday = (4 - consult.weekday()) % 7
            rep = consult + dt.timedelta(days=days_to_friday + (7 if r.random() < 0.18 else 0))
        else:
            rep = consult + dt.timedelta(days=int(r.integers(3, 13)))
        admitted = kind == "hospital" and r.random() < (0.78 if dru == 0 else 0.62)
        travel = r.random() < 0.028
        out.append({"k": k, "year": y, "week": w, "home": i, "group": g, "place": j, "age": age, "sex": sex,
                    "onset": onset, "consult": consult, "dru": dru, "reported": rep, "admitted": admitted,
                    "travel": travel})
    return out
