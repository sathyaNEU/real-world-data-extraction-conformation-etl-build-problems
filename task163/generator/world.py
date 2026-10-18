"""The world before any file is written: twelve states' business applications and the employer business formations
those applications produce, month by month from January 2021 to December 2027 (the truth runs past the release; only
what the October 2026 release could hold is ever shipped).

Two kinds of application reach the statistics in Ohio, Pennsylvania and Michigan once their integrated formation
filings went live in 2023: the ordinary application, filed by a business that wanted an employer identification
number, and the application the integrated filing adds, filed for a new business whose owner ticked the federal EIN box
while forming the entity. The statistics never tell them apart: both carry the same high-propensity, planned-wage and
corporate flags at much the same rates. The added application seldom becomes an employer: it forms within four
quarters at REL_ADDED of its state's ordinary rate. While each state's older filing route stayed open about three in
ten formation filers ticked the box; once the route closed (October 2025 to February 2026) every filer met the
question. From autumn 2025 every state's ordinary applications rose about an eighth on a common wave (WAVE)."""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

import common as K


@dataclass
class State:
    usps: str
    fips: str
    name: str
    base: float          # ordinary applications a month at the 2022 level (seasonally average)
    y4: float            # ordinary formations within four quarters per application
    hba: float           # high-propensity share of ordinary applications
    trend: float         # yearly drift of ordinary applications (on top of the common drift)
    resp: float          # the state's response to the common 2025 rise, relative to the common factor
    region: str = ""


STATES = [
    State("OH", "39", "Ohio", 16420, 0.0716, 0.362, 0.004, 1.00, "Great Lakes"),
    State("PA", "42", "Pennsylvania", 13880, 0.0741, 0.371, -0.002, 1.02, "Mid-Atlantic"),
    State("MI", "26", "Michigan", 13590, 0.0698, 0.348, 0.003, 0.98, "Great Lakes"),
    State("IN", "18", "Indiana", 8130, 0.0792, 0.377, 0.006, 1.01, "Great Lakes"),
    State("MN", "27", "Minnesota", 5910, 0.0811, 0.383, 0.004, 0.98, "Upper Midwest"),
    State("WI", "55", "Wisconsin", 4930, 0.0826, 0.392, 0.002, 1.03, "Great Lakes"),
    State("KY", "21", "Kentucky", 4460, 0.0758, 0.366, 0.005, 0.97, "Ohio Valley"),
    State("WV", "54", "West Virginia", 1218, 0.0803, 0.381, -0.006, 1.00, "Ohio Valley"),
    State("TN", "47", "Tennessee", 9310, 0.0687, 0.344, 0.011, 1.01, "Ohio Valley"),
    State("MO", "29", "Missouri", 7090, 0.0749, 0.358, 0.001, 0.99, "Plains"),
    State("IA", "19", "Iowa", 2790, 0.0838, 0.396, -0.001, 1.01, "Upper Midwest"),
    State("VA", "51", "Virginia", 10620, 0.0712, 0.355, 0.007, 1.02, "Mid-Atlantic"),
]
BY = {s.usps: s for s in STATES}
REFORM = ("OH", "PA", "MI")
OTHERS = tuple(s.usps for s in STATES if s.usps not in REFORM)

# the integrated formation filings: go-live and the date each state closed its older filing route
LAUNCH = {"OH": (2023, 1, 9), "PA": (2023, 4, 3), "MI": (2023, 7, 10)}
RETIRE = {"OH": (2025, 10, 1), "PA": (2025, 12, 1), "MI": (2026, 2, 2)}
ADDED_MAX = {"OH": 1.15, "PA": 1.21, "MI": 1.09}   # added applications at full take-up, per ordinary application
VOLUNTARY = 0.30        # share of full take-up reached while the older route stayed open
TAU = 2.0               # months to take-up of the voluntary phase (1 - e^-1)
RETIRE_RAMP = 2.0       # months for filers to move once the older route closed
REL_ADDED = 0.18        # an added application's formation rate within four quarters, relative to its state's ordinary rate

NATIONAL_RISE = 0.0     # an earlier common rise in ordinary applications (none in this world)
RISE_FROM, RISE_TO = (2023, 7), (2024, 6)
WAVE = 0.12             # the common rise in ordinary applications every state shows from autumn 2025
WAVE_FROM, WAVE_TO = (2025, 8), (2025, 11)
COMMON_DRIFT = 0.0      # yearly

# seasonal profile of applications (unadjusted), January first; the added applications follow formation filings,
# with a slightly sharper January
SEAS = np.array([1.236, 1.031, 1.079, 1.012, 0.991, 0.968, 0.982, 1.003, 0.931, 0.968, 0.892, 0.907])
SEAS = SEAS / SEAS.mean()
SEAS_ADDED = np.array([1.312, 1.043, 1.071, 1.004, 0.982, 0.958, 0.977, 0.996, 0.925, 0.963, 0.880, 0.889])
SEAS_ADDED = SEAS_ADDED / SEAS_ADDED.mean()

# flags on the two kinds of application (shares of all applications of that kind)
WBA_OF_HBA = 0.312      # ordinary: planned wages, within high-propensity
CBA_OF_HBA = 0.168      # ordinary: corporations, within high-propensity
ADDED_HBA = 0.438
ADDED_WBA_OF_HBA = 0.326
ADDED_CBA_OF_HBA = 0.071

TAIL8 = 0.112           # formations in quarters 5 to 8, per formation within four quarters
DUR4, DUR8 = 1.31, 1.69  # average duration to formation (quarters) among formations within four and eight quarters

MONTH_NOISE = 0.004     # idiosyncratic state-month variation in ordinary applications, beyond counting noise


def _frac_month_after(day_tuple):
    """(month index, share of that month's days on or after the date)."""
    y, m, d = day_tuple
    import calendar
    n = calendar.monthrange(y, m)[1]
    return K.midx(y, m), (n - d + 1) / n


def _smooth(t, a, b):
    if t <= a:
        return 0.0
    if t >= b:
        return 1.0
    x = (t - a) / (b - a)
    return x * x * (3 - 2 * x)


def national(t):
    """Common factor on ordinary applications in month index t: a smooth rise between RISE_FROM and RISE_TO and a
    second between WAVE_FROM and WAVE_TO, every state alike."""
    f1 = _smooth(t, K.midx(RISE_FROM), K.midx(RISE_TO))
    f2 = _smooth(t, K.midx(WAVE_FROM), K.midx(WAVE_TO))
    return (1.0 + NATIONAL_RISE * f1) * (1.0 + WAVE * f2)


def drift(t, s):
    return (1 + COMMON_DRIFT + s.trend) ** (t / 12.0)


def take_up(t, usps):
    """Added applications per ordinary application at full take-up, as a share (0 before go-live)."""
    li, lf = _frac_month_after(LAUNCH[usps])
    ri, rf = _frac_month_after(RETIRE[usps])
    if t < li:
        return 0.0

    def voluntary(k):
        return VOLUNTARY * (1 - math.exp(-(k + 0.5) / TAU))

    if t < ri:
        v = voluntary(t - li)
        return v * lf if t == li else v
    # once the older route closes every filer goes through the integrated filing: take-up moves from where the
    # voluntary phase stood to full over RETIRE_RAMP months (the closing month counts by its share of days)
    v_r = voluntary(ri - li)
    done = (t - ri) + (rf if t == ri else 1.0)
    return v_r + (1.0 - v_r) * min(1.0, done / RETIRE_RAMP)


@dataclass
class World:
    G: dict = field(default_factory=dict)      # ordinary applications by state (array over months)
    I: dict = field(default_factory=dict)      # added applications
    BA: dict = field(default_factory=dict)
    HBA: dict = field(default_factory=dict)
    WBA: dict = field(default_factory=dict)
    CBA: dict = field(default_factory=dict)
    F4G: dict = field(default_factory=dict)    # formations within four quarters of the ordinary applications
    F4I: dict = field(default_factory=dict)    # of the added applications
    F4: dict = field(default_factory=dict)
    F8: dict = field(default_factory=dict)
    D4: dict = field(default_factory=dict)
    D8: dict = field(default_factory=dict)
    EG: dict = field(default_factory=dict)     # expected ordinary applications (no counting noise)
    EI: dict = field(default_factory=dict)


def simulate():
    W = World()
    for s in STATES:
        r = K.rng("apps", s.usps)
        g_mean = np.array([s.base * drift(t, s) * (1 + (national(t) - 1) * s.resp) * SEAS[t % 12] for t in range(K.NM)])
        g_mean = g_mean * (1 + MONTH_NOISE * r.standard_normal(K.NM))
        if s.usps in REFORM:
            # take-up is per ordinary application at the 2023 level (filers forming entities, not the common rise)
            lvl = np.array([s.base * drift(t, s) for t in range(K.NM)])
            i_mean = np.array([lvl[t] * ADDED_MAX[s.usps] * take_up(t, s.usps) * SEAS_ADDED[t % 12]
                               for t in range(K.NM)])
        else:
            i_mean = np.zeros(K.NM)
        G = r.poisson(g_mean)
        I = r.poisson(i_mean)
        W.EG[s.usps], W.EI[s.usps] = g_mean, i_mean
        W.G[s.usps], W.I[s.usps] = G, I
        W.BA[s.usps] = G + I
        rf = K.rng("flags", s.usps)
        hg = rf.binomial(G, s.hba)
        hi = rf.binomial(I, ADDED_HBA)
        W.HBA[s.usps] = hg + hi
        W.WBA[s.usps] = rf.binomial(hg, WBA_OF_HBA) + rf.binomial(hi, ADDED_WBA_OF_HBA)
        W.CBA[s.usps] = rf.binomial(hg, CBA_OF_HBA) + rf.binomial(hi, ADDED_CBA_OF_HBA)
        rb = K.rng("formations", s.usps)
        f4g = rb.binomial(G, s.y4)
        f4i = rb.binomial(I, s.y4 * REL_ADDED)
        W.F4G[s.usps], W.F4I[s.usps] = f4g, f4i
        W.F4[s.usps] = f4g + f4i
        rest = W.BA[s.usps] - W.F4[s.usps]
        W.F8[s.usps] = W.F4[s.usps] + rb.binomial(rest, np.clip(TAIL8 * W.F4[s.usps] / np.maximum(rest, 1), 0, 1))
        W.D4[s.usps] = np.round(DUR4 + 0.04 * rb.standard_normal(K.NM), 2)
        W.D8[s.usps] = np.round(DUR8 + 0.05 * rb.standard_normal(K.NM), 2)
    return W
