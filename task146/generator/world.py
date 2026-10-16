"""The clean truth: every claims week from the week ended 4 January 2014 to a few weeks past the call, by region.

Initial claims are new claims (a claimant without an open benefit year) and additional claims (a claimant returning to
an open one). A new claim gets its monetary determination when it is taken; the claimant is found monetarily
ineligible when the base-period earnings fall below the minimum. A claimant refused because the recent earnings sat in
the quarter just after the base period can be admitted once a new quarter moves the base period forward, so in the
first claims weeks whose Sunday falls in a new quarter some of the closing quarter's refused claimants file again.
How many come back differs by region and is stable within each: where the refused are mostly seasonal and short-tenure
workers whose last season's pay enters the base period at the turn (the tourism, fishing and building regions), a large
share files again; where they are mostly people with patchy earnings all year (the Capital, the manufacturing
regions), the move adds one thin quarter and drops another, and few come back. How many come back also depends on how
long ago they were refused: a claimant refused in the quarter's first weeks has mostly found other work or stopped
looking by the turn, one refused in its last weeks is still out of work and files again as soon as the base period
moves, so each refusal weighs exp(-d / TAU) by the weeks d from its claims week to the quarter's last. Layoffs come in
lumps, so a region's refusals move from month to month inside a quarter (the tourism and building regions together, as
a season ends or a project finishes), some quarters' late and others' early. A share R0[r] of a region's closing
quarter monetarily ineligible determinations, each weighted by how recently it was made (the weights averaging one over
a quarter's weeks), files again in the first such week, R1 and R2 of that in the second and third. Nothing else in the
world steps at a quarter turn."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# the quarter-turn refiling: the share of a region's closing-quarter monetarily ineligible determinations filed again
# in the first claims week of the new quarter; the second and third weeks take fixed fractions of it
R0 = {"Northern": 0.032, "Capital": 0.016, "Eastern": 0.027, "Midlands": 0.024, "Western": 0.2862, "Southern": 0.058,
      "Coastal": 0.3186, "Island": 0.34344}
TAU = 2.5                  # weeks: how fast the chance of filing again falls with the weeks since the refusal
R_LATER = (0.155, 0.058)
REFILE_INELIGIBLE = 0.10          # share of the claims filed again that are refused a second time

# the national ineligible share of new claims, quarter by quarter: a quiet level with episodes
INELIG_BASE = 0.152
INELIG_EPISODES = {(2014, 3): 0.236, (2015, 1): 0.255, (2015, 4): 0.087, (2016, 3): 0.091, (2017, 2): 0.248,
                   (2017, 4): 0.229, (2018, 2): 0.086, (2018, 4): 0.262, (2019, 1): 0.241, (2019, 3): 0.088,
                   (2020, 2): 0.330, (2020, 3): 0.298, (2021, 1): 0.262, (2022, 1): 0.239, (2022, 4): 0.093,
                   (2023, 2): 0.091, (2023, 4): 0.244, (2024, 2): 0.246, (2024, 4): 0.097, (2025, 1): 0.232,
                   (2025, 2): 0.094, (2025, 3): 0.119, (2025, 4): 0.113, (2026, 1): 0.124, (2026, 2): 0.131}
# each region's ineligible share relative to the national level, and the quarters a region's own layoffs lifted it
RFAC = {"Northern": 1.00, "Capital": 0.88, "Eastern": 1.01, "Midlands": 0.98, "Western": 0.99, "Southern": 1.07,
        "Coastal": 1.03, "Island": 1.01}
REGION_SHOCK_SD = 0.16
REGION_EPISODES = {("Western", (2016, 2)): 1.85, ("Coastal", (2017, 3)): 1.80, ("Island", (2019, 1)): 1.75,
                   ("Capital", (2018, 3)): 1.55, ("Midlands", (2021, 4)): 1.70, ("Southern", (2023, 1)): 1.80,
                   ("Coastal", (2024, 2)): 1.65, ("Western", (2022, 3)): 1.70, ("Northern", (2015, 3)): 1.65,
                   ("Eastern", (2025, 3)): 1.60, ("Island", (2015, 2)): 1.70, ("Capital", (2023, 3)): 1.45,
                   ("Western", (2019, 4)): 0.60, ("Coastal", (2021, 2)): 0.62, ("Midlands", (2016, 4)): 1.55,
                   ("Western", (2018, 2)): 1.75, ("Coastal", (2018, 2)): 1.85, ("Island", (2018, 2)): 1.80,
                   ("Western", (2019, 2)): 1.70, ("Coastal", (2019, 2)): 1.80, ("Island", (2019, 2)): 1.85,
                   ("Capital", (2021, 3)): 1.60, ("Midlands", (2021, 3)): 1.65, ("Northern", (2021, 3)): 1.50,
                   ("Capital", (2017, 1)): 1.55, ("Eastern", (2017, 1)): 1.60, ("Midlands", (2017, 1)): 1.45}
# when inside its quarter a region's layoff episode fell: the month weights of its refusals (late waves and early ones)
EPISODE_TIMING = {("Western", (2016, 2)): (0.4, 0.8, 1.8), ("Coastal", (2017, 3)): (0.4, 0.8, 1.8),
                  ("Western", (2018, 2)): (0.4, 0.8, 1.8), ("Coastal", (2018, 2)): (0.4, 0.8, 1.8),
                  ("Island", (2018, 2)): (0.4, 0.8, 1.8), ("Western", (2019, 2)): (1.6, 0.9, 0.5),
                  ("Coastal", (2019, 2)): (1.6, 0.9, 0.5), ("Island", (2019, 2)): (1.6, 0.9, 0.5),
                  ("Island", (2019, 1)): (1.5, 1.0, 0.5), ("Island", (2015, 2)): (1.5, 0.9, 0.6),
                  ("Western", (2022, 3)): (1.6, 0.9, 0.5), ("Coastal", (2024, 2)): (1.5, 1.0, 0.5)}
# 2025 to mid-2026: the building and tourism boom; recent hires in the boom regions carry full base periods
BOOM = {"Western": 0.806, "Coastal": 0.754, "Island": 0.78, "Capital": 1.18, "Midlands": 1.08, "Northern": 1.10,
        "Eastern": 1.12, "Southern": 0.92}
BOOM_QUARTERS = [(2025, 2), (2025, 3), (2025, 4), (2026, 1), (2026, 2)]
# July, August and September 2026: in the tourism and building regions the refusals stay near their usual level in July
# and August, and in September, as the winter season ends and the contractors and hotels shed staff taken on in 2025
# and early 2026, more than half of their new claims are refused; elsewhere they stay near their usual level
INELIG_2026Q3 = {"Northern": (0.145, 0.155, 0.170), "Capital": (0.130, 0.140, 0.155), "Eastern": (0.145, 0.160, 0.175),
                 "Midlands": (0.150, 0.165, 0.180), "Western": (0.135, 0.185, 0.545), "Southern": (0.155, 0.170, 0.185),
                 "Coastal": (0.145, 0.19, 0.56), "Island": (0.14, 0.195, 0.555)}
SEASONAL_REGIONS = ("Western", "Coastal", "Island")
SEASONAL_SD = 0.55
MONTH_SD = 0.28            # a region's month-to-month swing in the refused share (the timing of its layoffs)
SEASONAL_MONTH_SD = 0.50   # the tourism and building regions' common month-to-month swing (a season's end, a project's)
MONTH_DRAW = "s24"         # the realisation of the month swings' two streams
ADDITIONAL_SHARE = 0.213
ADVANCE_LATE = (0.0023, 0.0095)   # range of the share of a week's claims taken late and added at the revision


def _year_frac(d):
    return d.year + (d.timetuple().tm_yday - 1) / 365.25


LEVEL_KNOTS = [(2014.0, 11600.0), (2016.0, 11180.0), (2018.0, 10760.0), (2020.15, 10380.0), (2022.0, 10260.0),
               (2023.5, 10470.0), (2025.0, 10690.0), (2026.38, 10940.0), (2026.71, 12390.0), (2027.0, 12430.0)]
PANDEMIC_START = dt.date(2020, 3, 22)
PANDEMIC_MULT = [2.35, 2.28, 2.16, 2.02, 1.90, 1.81, 1.74, 1.68, 1.63, 1.59]
# the 2026 layoffs lean on the building and tourism regions
LEAN_2026 = {"Midlands": 1.06, "Western": 1.24, "Coastal": 1.28, "Island": 1.20, "Capital": 0.94}
LEAN_START, LEAN_DAYS = dt.date(2026, 6, 1), 70.0


def level_path(sun):
    x = _year_frac(sun + dt.timedelta(days=3))
    for (x0, y0), (x1, y1) in zip(LEVEL_KNOTS, LEVEL_KNOTS[1:]):
        if x0 <= x <= x1:
            lv = math.exp(math.log(y0) + (math.log(y1) - math.log(y0)) * (x - x0) / (x1 - x0))
            break
    else:
        lv = LEVEL_KNOTS[-1][1]
    k = (sun - PANDEMIC_START).days // 7
    if 0 <= k < len(PANDEMIC_MULT):
        lv *= PANDEMIC_MULT[k]
    elif k >= len(PANDEMIC_MULT):
        # the long tail: 1.55 at week 10 easing to 1 by the end of 2021
        lv *= 1.0 + 0.55 * math.exp(-(k - len(PANDEMIC_MULT)) / 30.0)
    return lv


def seasonal(sun):
    """The smooth seasonal shape (log), by the day of the year of the week's Wednesday: a winter peak in July, a
    spring and early summer low, the January return after the holiday shutdown."""
    mid = sun + dt.timedelta(days=3)
    doy = mid.timetuple().tm_yday
    a = 2 * math.pi * doy / 365.25
    s = (0.088 * math.cos(a - 2 * math.pi * 196 / 365.25) + 0.036 * math.cos(2 * a - 4 * math.pi * 30 / 365.25)
         - 0.018 * math.sin(3 * a))
    # the January return: claims held over the summer shutdown are taken once workplaces reopen in mid-January
    d0 = (mid - dt.date(mid.year, 1, 1)).days
    if 0 <= d0 <= 45:
        s += 0.070 * math.exp(-((d0 - 16) / 7.0) ** 2)
    return s


YEAR_END = 0.050   # the last claims week of June: fixed-term public-sector and university contracts end with the fiscal year


def holiday_effect(sun):
    """Claims lost in a week with public holidays, about half taken the week after; the summer shutdown from 24 December
    to 7 January; the
    separations at the fiscal year's end, filed in the last claims week of June."""
    lost = K.working_days_lost(sun)
    prev = K.working_days_lost(sun - dt.timedelta(days=7))
    h = -0.030 * lost + 0.015 * prev
    nxt = sun + dt.timedelta(days=7)
    if sun.month == 6 and nxt.month == 7:
        h += YEAR_END
    days = [sun + dt.timedelta(days=k) for k in range(7)]
    if any((d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 7) for d in days):
        h -= 0.075
    return h


class Truth:
    pass


def simulate(params=None):
    P = dict(R0=R0, R_LATER=R_LATER, RFAC=RFAC, REGION_SHOCK_SD=REGION_SHOCK_SD, REGION_EPISODES=REGION_EPISODES,
             INELIG_2026Q3=INELIG_2026Q3, LEAN_2026=LEAN_2026, LEAN_START=LEAN_START, LEAN_DAYS=LEAN_DAYS, BOOM=BOOM,
             SEASONAL_SD=SEASONAL_SD, EPISODE_TIMING=EPISODE_TIMING, TAU=TAU, MONTH_SD=MONTH_SD,
             SEASONAL_MONTH_SD=SEASONAL_MONTH_SD, seed_salt="")
    if params:
        P.update(params)
    salt = P["seed_salt"]
    T = Truth()
    T.params = P
    S = K.SIM_SUNDAYS
    n = len(S)
    R = K.REGIONS
    T.sundays = S
    T.idx = {s: i for i, s in enumerate(S)}
    T.quarter = [K.quarter_of(s) for s in S]
    # week index inside its quarter (by Sunday)
    T.kq = []
    for i, s in enumerate(S):
        T.kq.append(0 if i == 0 or T.quarter[i] != T.quarter[i - 1] else T.kq[-1] + 1)
    lvl = np.array([level_path(s) for s in S])
    seas = np.array([seasonal(s) for s in S])
    hol = np.array([holiday_effect(s) for s in S])
    # national persistent deviation and regional ones
    g = K.rng("national-dev", salt)
    dev = np.zeros(n)
    for i in range(1, n):
        dev[i] = 0.95 * dev[i - 1] + g.normal(0, 0.0045)
    T.level, T.seas, T.hol, T.dev = lvl, seas, hol, dev
    rdev = {}
    for r in R:
        g = K.rng("region-dev", r, salt)
        x = np.zeros(n)
        for i in range(1, n):
            x[i] = 0.93 * x[i - 1] + g.normal(0, 0.005)
        rdev[r] = x
    # regional shares drift slowly; the 2026 layoffs lean on the building and tourism regions
    share = {}
    for r in R:
        g = K.rng("share", r, salt)
        drift = np.cumsum(g.normal(0, 0.0009, n))
        share[r] = K.REGION_SHARE[r] * np.exp(drift - drift.mean())
    for i, s in enumerate(S):
        if s >= P["LEAN_START"]:
            ramp = min(1.0, (s - P["LEAN_START"]).days / P["LEAN_DAYS"])
            for r, f in P["LEAN_2026"].items():
                share[r][i] *= 1.0 + (f - 1.0) * ramp
    tot = sum(share[r] for r in R)
    for r in R:
        share[r] = share[r] / tot
    T.share = share
    # the ineligible share of new claims: the national level by quarter, each region's factor and its own shocks
    quarters = sorted(set(T.quarter))
    g = K.rng("inelig-quarter", salt)
    qlev = {}
    for q in quarters:
        qlev[q] = float(np.clip(INELIG_BASE + g.normal(0, 0.028), 0.095, 0.235))
    qlev.update(INELIG_EPISODES)
    T.qlev = qlev
    gr = K.rng("inelig-region", salt)
    rq = {}
    for q in quarters:
        for r in R:
            rq[(r, q)] = float(math.exp(gr.normal(0, P["REGION_SHOCK_SD"]) - 0.5 * P["REGION_SHOCK_SD"] ** 2))
    for key, m in P["REGION_EPISODES"].items():
        rq[key] = rq[key] * m
    # the tourism and building regions' refusals rise and fall together, quarter by quarter, with how many of their
    # claimants are short-tenure seasonal hires (a season's length, a building cycle), apart from the rest of the country
    gs_ = K.rng("inelig-seasonal-regions", salt)
    for q in quarters:
        f = float(gs_.normal(0, P["SEASONAL_SD"]))
        for r in SEASONAL_REGIONS:
            rq[(r, q)] = rq[(r, q)] * math.exp(f - 0.5 * P["SEASONAL_SD"] ** 2)
    for q in BOOM_QUARTERS:
        for r in R:
            rq[(r, q)] = rq[(r, q)] * P["BOOM"][r]
    T.rq = rq
    # the month inside the quarter: layoffs come in lumps, so a region's refusals move month to month, the tourism and
    # building regions' together (a common factor on its own stream), and the episodes fall late or early in their quarter
    gmr = K.rng("inelig-month-region", MONTH_DRAW, salt)
    gms = K.rng("inelig-month-seasonal", MONTH_DRAW, salt)
    mfac = {}
    for key in sorted({(s.year, s.month) for s in S}):
        fs = float(gms.normal(0, P["SEASONAL_MONTH_SD"]))
        for r in R:
            f = float(gmr.normal(0, P["MONTH_SD"]))
            v2 = P["MONTH_SD"] ** 2
            if r in SEASONAL_REGIONS:
                f += fs
                v2 += P["SEASONAL_MONTH_SD"] ** 2
            mfac[(r, key)] = math.exp(f - 0.5 * v2)
    for (r, q), wts in P["EPISODE_TIMING"].items():
        for j, wj in enumerate(wts):
            mfac[(r, (q[0], 3 * (q[1] - 1) + j + 1))] *= wj
    T.mfac = mfac
    gm = K.rng("inelig-month", salt)
    mshift = {}
    gw = K.rng("inelig-week", salt)
    inel = {r: np.zeros(n) for r in R}
    for i, s in enumerate(S):
        q = T.quarter[i]
        key = (s.year, s.month)
        if key not in mshift:
            mshift[key] = gm.normal(0, 0.010)
        e = gw.normal(0, 0.006)
        for r in R:
            if q == (2026, 3):
                v = P["INELIG_2026Q3"][r][s.month - 7] + e
            else:
                v = (qlev[q] + mshift[key]) * P["RFAC"][r] * rq[(r, q)] * mfac[(r, key)] + e
            inel[r][i] = float(np.clip(v, 0.04, 0.62))
    T.inel_share = inel
    # draw the weeks in order, so each quarter's refiling rests on the closing quarter's determinations; the claims filed
    # again and their determinations on their own streams, so the base claims never move with the refiling
    T.base_new = {r: np.zeros(n, dtype=int) for r in R}
    T.base_add = {r: np.zeros(n, dtype=int) for r in R}
    T.refile = {r: np.zeros(n, dtype=int) for r in R}
    T.inelig = {r: np.zeros(n, dtype=int) for r in R}
    T.exp_base = {r: np.zeros(n) for r in R}
    T.exp_refile = {r: np.zeros(n) for r in R}
    pool = {}
    pool_r = {}
    recent_r = {}
    tau = P["TAU"]
    wbar = sum(math.exp(-d / tau) for d in range(13)) / 13.0
    g = K.rng("claims", salt)
    gi = K.rng("determinations", salt)
    grf = K.rng("refile", salt)
    gri = K.rng("refile-determinations", salt)
    rates = [None, P["R_LATER"][0], P["R_LATER"][1]]
    for i, s in enumerate(S):
        q = T.quarter[i]
        k = T.kq[i]
        prevq = K.prev_quarter(q)
        for r in R:
            amp = K.REGION_AMP[r]
            mu = lvl[i] * share[r][i] * math.exp(amp * seas[i] + hol[i] + dev[i] + rdev[r][i])
            T.exp_base[r][i] = mu
            nb = int(g.poisson(mu * (1 - ADDITIONAL_SHARE)))
            na = int(g.poisson(mu * ADDITIONAL_SHARE))
            rf_mu = 0.0
            if k <= 2 and prevq in pool:
                rf_mu = P["R0"][r] * (1.0 if k == 0 else rates[k]) * recent_r[prevq][r]
            T.exp_refile[r][i] = rf_mu
            nr = int(grf.poisson(rf_mu)) if rf_mu > 0 else 0
            T.base_new[r][i], T.base_add[r][i], T.refile[r][i] = nb, na, nr
            T.inelig[r][i] = int(gi.binomial(nb, inel[r][i])) + (int(gri.binomial(nr, REFILE_INELIGIBLE)) if nr else 0)
        # close the quarter when its last week is drawn
        last = (i == n - 1) or (T.quarter[i + 1] != q)
        if last:
            idx = [j for j in range(i + 1) if T.quarter[j] == q]
            pool_r[q] = {r: float(sum(T.inelig[r][j] for j in idx)) for r in R}
            pool[q] = sum(pool_r[q].values())
            # the refused weigh by how recently they were refused: weeks from the refusal to the quarter's last week
            recent_r[q] = {r: float(sum(T.inelig[r][j] * math.exp(-(i - j) / tau) for j in idx)) / wbar for r in R}
    T.pool, T.pool_r, T.recent_r = pool, pool_r, recent_r
    # counts: new claims include the claims filed again; the revised count, and the advance taken before late claims
    T.new = {r: T.base_new[r] + T.refile[r] for r in R}
    T.additional = T.base_add
    T.revised = {r: T.new[r] + T.base_add[r] for r in R}
    ga = K.rng("advance", salt)
    T.advance = {}
    T.late = {}
    T.late_share = np.array([ga.uniform(*ADVANCE_LATE) for _ in S])
    for r in R:
        late = np.array([ga.binomial(int(T.revised[r][i]), T.late_share[i]) for i in range(n)])
        T.advance[r] = T.revised[r] - late
        T.late[r] = late
    # the late claims split between new and additional claims, and the determinations of the late new claims, each on
    # its own stream so that every draw above is unchanged: the advance count's new and additional claims, and the
    # ineligible determinations a month's figures carry for a week first published at its advance count
    gs = K.rng("advance-split", salt)
    gd = K.rng("advance-inelig", salt)
    T.adv_new, T.adv_add, T.adv_inelig = {}, {}, {}
    for r in R:
        ln = np.array([int(gs.hypergeometric(int(T.new[r][i]), int(T.additional[r][i]), int(T.late[r][i])))
                       if T.late[r][i] else 0 for i in range(n)])
        li = np.array([int(gd.hypergeometric(int(T.inelig[r][i]), int(T.new[r][i] - T.inelig[r][i]), int(ln[i])))
                       if ln[i] else 0 for i in range(n)])
        T.adv_new[r] = T.new[r] - ln
        T.adv_add[r] = T.additional[r] - (T.late[r] - ln)
        T.adv_inelig[r] = T.inelig[r] - li
    T.nat_revised = sum(T.revised[r] for r in R)
    T.nat_advance = sum(T.advance[r] for r in R)
    T.nat_inelig = sum(T.inelig[r] for r in R)
    T.nat_new = sum(T.new[r] for r in R)
    T.nat_refile = sum(T.refile[r] for r in R)
    ti = T.idx[K.TARGET_SUNDAY]
    T.target_expected_revised = sum(T.exp_base[r][ti] + T.exp_refile[r][ti] for r in R)
    T.target_expected_base = sum(T.exp_base[r][ti] for r in R)
    T.target_expected_refile = sum(T.exp_refile[r][ti] for r in R)
    T.target_late_share = float(np.mean(T.late_share[:ti]))
    return T


if __name__ == "__main__":
    T = simulate()
    ti = T.idx[K.TARGET_SUNDAY]
    print("target expected %.0f (base %.0f, refile %.0f); pool 2026Q3 %.0f" % (
        T.target_expected_revised, T.target_expected_base, T.target_expected_refile, T.pool[(2026, 3)]))
    for r in K.REGIONS:
        print("  %-9s pool %6.0f  refile %6.0f" % (r, T.pool_r[(2026, 3)][r], T.exp_refile[r][ti]))
    for q in sorted(T.pool)[-12:]:
        print(q, round(T.pool[q]), round(T.qlev.get(q, 0), 3))
    for i in range(ti - 6, ti + 3):
        print(T.sundays[i], int(T.nat_revised[i]), int(T.nat_advance[i]), int(T.nat_refile[i]))
