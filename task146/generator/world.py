"""The clean truth: every claims week from the week ended 4 January 2014 to a few weeks past the call, by region.

Initial claims are new claims (a claimant without an open benefit year) and additional claims (a claimant returning to
an open one). A new claim gets its monetary determination when it is taken; the claimant is found monetarily
ineligible when the base-period earnings fall below the minimum. A claimant refused because the recent earnings sat in
the quarter just after the base period can be admitted once a new quarter moves the base period forward, so in the
first claims weeks whose Sunday falls in a new quarter some of the closing quarter's refused claimants file again: a
share r0 of the closing quarter's monetarily ineligible determinations in the first such week, r1 in the second and r2
in the third. Nothing else in the world steps at a quarter turn."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# the quarter-turn refiling: shares of the closing quarter's monetarily ineligible determinations filed again in the
# first, second and third claims weeks of the new quarter
R_TURN = (0.0912, 0.0141, 0.0053)
REFILE_INELIGIBLE = 0.10          # share of the claims filed again that are refused a second time

# the ineligible share of new claims, quarter by quarter: a quiet level with episodes
INELIG_BASE = 0.152
INELIG_EPISODES = {(2014, 3): 0.236, (2015, 1): 0.255, (2015, 4): 0.087, (2016, 3): 0.091, (2017, 2): 0.248,
                   (2017, 4): 0.229, (2018, 2): 0.086, (2018, 4): 0.262, (2019, 1): 0.241, (2019, 3): 0.088,
                   (2020, 2): 0.330, (2020, 3): 0.298, (2021, 1): 0.262, (2022, 1): 0.239, (2022, 4): 0.093,
                   (2023, 2): 0.091, (2023, 4): 0.244, (2024, 2): 0.246, (2024, 4): 0.097, (2025, 1): 0.232,
                   (2025, 2): 0.094, (2026, 2): 0.171}
# July, August and September 2026: the building and hotel layoffs of staff taken on in 2025 and early 2026
INELIG_2026Q3_MONTH = {7: 0.262, 8: 0.334, 9: 0.401}
ADDITIONAL_SHARE = 0.213
ADVANCE_LATE = (0.0025, 0.0095)   # range of the share of a week's claims taken late and added at the revision


def _year_frac(d):
    return d.year + (d.timetuple().tm_yday - 1) / 365.25


LEVEL_KNOTS = [(2014.0, 11600.0), (2016.0, 11180.0), (2018.0, 10760.0), (2020.15, 10380.0), (2022.0, 10260.0),
               (2023.5, 10470.0), (2025.0, 10690.0), (2026.38, 10940.0), (2026.71, 12120.0), (2027.0, 12160.0)]
PANDEMIC_START = dt.date(2020, 3, 22)
PANDEMIC_MULT = [2.35, 2.28, 2.16, 2.02, 1.90, 1.81, 1.74, 1.68, 1.63, 1.59]


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
    # the January return: claims held over the shutdown are taken in the first weeks back
    d0 = (mid - dt.date(mid.year, 1, 1)).days
    if 3 <= d0 <= 40:
        s += 0.085 * math.exp(-(d0 - 3) / 18.0)
    return s


def holiday_effect(sun):
    """Claims lost in a week with public holidays, about half taken the week after; the Christmas shutdown."""
    lost = K.working_days_lost(sun)
    prev = K.working_days_lost(sun - dt.timedelta(days=7))
    h = -0.030 * lost + 0.015 * prev
    days = [sun + dt.timedelta(days=k) for k in range(7)]
    if any((d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 3) for d in days):
        h -= 0.075
    return h


class Truth:
    pass


def simulate():
    T = Truth()
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
    g = K.rng("national-dev")
    dev = np.zeros(n)
    for i in range(1, n):
        dev[i] = 0.95 * dev[i - 1] + g.normal(0, 0.0045)
    T.level, T.seas, T.hol, T.dev = lvl, seas, hol, dev
    rdev = {}
    for r in R:
        g = K.rng("region-dev", r)
        x = np.zeros(n)
        for i in range(1, n):
            x[i] = 0.93 * x[i - 1] + g.normal(0, 0.005)
        rdev[r] = x
    # regional shares drift slowly; the 2026 layoffs lean on Midlands, Western and Coastal
    share = {}
    for r in R:
        g = K.rng("share", r)
        drift = np.cumsum(g.normal(0, 0.0009, n))
        share[r] = K.REGION_SHARE[r] * np.exp(drift - drift.mean())
    lean = {"Midlands": 1.06, "Western": 1.07, "Coastal": 1.05, "Capital": 0.97}
    for i, s in enumerate(S):
        if s >= dt.date(2026, 6, 1):
            ramp = min(1.0, (s - dt.date(2026, 6, 1)).days / 70.0)
            for r, f in lean.items():
                share[r][i] *= 1.0 + (f - 1.0) * ramp
    tot = sum(share[r] for r in R)
    for r in R:
        share[r] = share[r] / tot
    T.share = share
    # the ineligible share of new claims, week by week
    quarters = sorted(set(T.quarter))
    g = K.rng("inelig-quarter")
    qlev = {}
    for q in quarters:
        qlev[q] = float(np.clip(INELIG_BASE + g.normal(0, 0.028), 0.095, 0.235))
    qlev.update(INELIG_EPISODES)
    T.qlev = qlev
    gm = K.rng("inelig-month")
    mshift = {}
    gw = K.rng("inelig-week")
    rfac = {"Northern": 1.02, "Capital": 0.91, "Eastern": 1.03, "Midlands": 1.01, "Western": 1.04, "Southern": 1.10,
            "Coastal": 1.12, "Island": 1.08}
    inel = {r: np.zeros(n) for r in R}
    for i, s in enumerate(S):
        q = T.quarter[i]
        key = (s.year, s.month)
        if key not in mshift:
            mshift[key] = gm.normal(0, 0.010)
        if q == (2026, 3):
            base = INELIG_2026Q3_MONTH[s.month]
        else:
            base = qlev[q] + mshift[key]
        e = gw.normal(0, 0.006)
        for r in R:
            inel[r][i] = float(np.clip(base * rfac[r] + e, 0.04, 0.6))
    T.inel_share = inel
    # draw the weeks in order, so each quarter's refiling rests on the closing quarter's determinations
    T.base_new = {r: np.zeros(n, dtype=int) for r in R}
    T.base_add = {r: np.zeros(n, dtype=int) for r in R}
    T.refile = {r: np.zeros(n, dtype=int) for r in R}
    T.inelig = {r: np.zeros(n, dtype=int) for r in R}
    T.exp_base = {r: np.zeros(n) for r in R}
    T.exp_refile = {r: np.zeros(n) for r in R}
    pool = {}
    pool_r = {}
    g = K.rng("claims")
    gi = K.rng("determinations")
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
                rf_mu = R_TURN[k] * pool_r[prevq][r]
            T.exp_refile[r][i] = rf_mu
            nr = int(g.poisson(rf_mu)) if rf_mu > 0 else 0
            T.base_new[r][i], T.base_add[r][i], T.refile[r][i] = nb, na, nr
            T.inelig[r][i] = int(gi.binomial(nb, inel[r][i]) + gi.binomial(nr, REFILE_INELIGIBLE))
        # close the quarter when its last week is drawn
        last = (i == n - 1) or (T.quarter[i + 1] != q)
        if last:
            idx = [j for j in range(i + 1) if T.quarter[j] == q]
            pool_r[q] = {r: float(sum(T.inelig[r][j] for j in idx)) for r in R}
            pool[q] = sum(pool_r[q].values())
    T.pool, T.pool_r = pool, pool_r
    # counts: new claims include the claims filed again; the revised count, and the advance taken before late claims
    T.new = {r: T.base_new[r] + T.refile[r] for r in R}
    T.additional = T.base_add
    T.revised = {r: T.new[r] + T.base_add[r] for r in R}
    ga = K.rng("advance")
    T.advance = {}
    T.late_share = np.array([ga.uniform(*ADVANCE_LATE) for _ in S])
    for r in R:
        late = np.array([ga.binomial(int(T.revised[r][i]), T.late_share[i]) for i in range(n)])
        T.advance[r] = T.revised[r] - late
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


def quarter_turn_rows(T, upto_sunday):
    """One row per quarter turn whose first claims week is published by upto_sunday: the first week, the week
    before, and the closing quarter's ineligible determinations and claims."""
    out = []
    for i, s in enumerate(T.sundays):
        if s > upto_sunday or i < 3 or T.kq[i] != 0:
            continue
        q = T.quarter[i]
        pq = K.prev_quarter(q)
        if pq not in T.pool:
            continue
        idx = [j for j in range(len(T.sundays)) if T.quarter[j] == pq]
        out.append(dict(q=q, i=i, pool=T.pool[pq], prevq_claims=int(sum(T.nat_revised[j] for j in idx))))
    return out


if __name__ == "__main__":
    T = simulate()
    ti = T.idx[K.TARGET_SUNDAY]
    print("target expected %.0f (base %.0f, refile %.0f); pool 2026Q3 %.0f" % (
        T.target_expected_revised, T.target_expected_base, T.target_expected_refile, T.pool[(2026, 3)]))
    for q in sorted(T.pool)[-12:]:
        print(q, round(T.pool[q]), round(T.qlev.get(q, 0), 3))
    for i in range(ti - 6, ti + 3):
        print(T.sundays[i], int(T.nat_revised[i]), int(T.nat_advance[i]), int(T.nat_refile[i]))
