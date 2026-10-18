"""The world before any file is written: twelve states' business applications and the employer business formations
those applications produce, month by month from January 2021 to December 2027 (the truth runs past the release; only
what the October 2026 release could hold is ever shipped).

Ordinary applications in every state carry the texture a state series has: the state's own drift, a business cycle
every state shares, a slow wander of the state's own, month-to-month irregularity and counting noise. Formation rates
differ by state, drift slowly and move from one year's applications to the next.

Two kinds of application reach the statistics in Ohio, Pennsylvania and Michigan once their integrated formation
filings went live in 2023: the ordinary application, filed by a business that wanted an employer identification
number, and the application the integrated filing adds, filed for a new business whose owner ticked the federal EIN box
while forming the entity. The statistics never tell them apart: both carry the state's high-propensity, planned-wage
and corporate shares. The added application seldom becomes an employer: it forms within four quarters at REL_ADDED of
its state's ordinary rate. While each state's older filing route stayed open about three in ten formation filers
ticked the box; once the route closed (January to March 2026) every filer met the question, which adds about seven
applications for every ten ordinary ones, so that over the twelve months to September 2026 about a third of the state's
applications are added ones. From early 2026 every state's ordinary applications rose about a seventh on a common wave
(WAVE), each state by its own amount and a month apart at most; nothing in the record gives its cause."""
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
    base: float          # ordinary applications a month at the January 2021 level (seasonally average)
    y4: float            # ordinary formations within four quarters per application, at the 2023 level
    hba: float           # high-propensity share of applications
    trend: float         # yearly drift of ordinary applications
    rtrend: float        # yearly drift of the formation rate
    resp: float          # the state's response to the common factor
    region: str = ""


STATES = [
    State("OH", "39", "Ohio", 16180, 0.0716, 0.362, 0.015, 0.002, 1.00, "Great Lakes"),
    State("PA", "42", "Pennsylvania", 13760, 0.0741, 0.371, 0.012, -0.001, 1.02, "Mid-Atlantic"),
    State("MI", "26", "Michigan", 13410, 0.0698, 0.348, 0.016, 0.001, 0.98, "Great Lakes"),
    State("IN", "18", "Indiana", 7980, 0.0792, 0.377, 0.021, -0.004, 1.01, "Great Lakes"),
    State("MN", "27", "Minnesota", 5870, 0.0811, 0.383, 0.009, 0.003, 0.98, "Upper Midwest"),
    State("WI", "55", "Wisconsin", 4940, 0.0826, 0.392, 0.004, -0.002, 1.03, "Great Lakes"),
    State("KY", "21", "Kentucky", 4370, 0.0758, 0.366, 0.017, 0.005, 0.97, "Ohio Valley"),
    State("WV", "54", "West Virginia", 1262, 0.0803, 0.381, -0.014, -0.006, 1.00, "Ohio Valley"),
    State("TN", "47", "Tennessee", 8960, 0.0687, 0.344, 0.032, 0.001, 1.01, "Ohio Valley"),
    State("MO", "29", "Missouri", 7040, 0.0749, 0.358, 0.006, -0.003, 0.99, "Plains"),
    State("IA", "19", "Iowa", 2840, 0.0838, 0.396, -0.007, 0.004, 1.01, "Upper Midwest"),
    State("VA", "51", "Virginia", 10310, 0.0712, 0.355, 0.024, 0.002, 1.02, "Mid-Atlantic"),
]
BY = {s.usps: s for s in STATES}
REFORM = ("OH", "PA", "MI")
OTHERS = tuple(s.usps for s in STATES if s.usps not in REFORM)

# the integrated formation filings: go-live and the date each state closed its older filing route
LAUNCH = {"OH": (2023, 1, 9), "PA": (2023, 4, 3), "MI": (2023, 7, 10)}
RETIRE = {"OH": (2026, 1, 5), "PA": (2026, 2, 2), "MI": (2026, 3, 2)}
ADDED_MAX = {"OH": 0.744, "PA": 0.792, "MI": 0.696}   # added applications at full take-up, per ordinary application
VOLUNTARY = 0.34        # share of full take-up reached while the older route stayed open
TAU = 2.0               # months to take-up of the voluntary phase (1 - e^-1)
RETIRE_RAMP = 2.0       # months for filers to move once the older route closed (each state's own, about this)
TAKEUP_NOISE = 0.04     # month-to-month movement in take-up (log scale)
SURGE = 0.0             # take-up above the voluntary plateau in the launch months, fading with SURGE_TAU
SURGE_TAU = 6.0
REL_ADDED = 0.27        # an added application's formation rate within four quarters, relative to its state's ordinary rate

WAVE = 0.15             # the common rise in ordinary applications every state shows from early 2026
WAVE_FROM, WAVE_TO = (2026, 1), (2026, 4)
WAVE_SD = 0.05          # a state's own response to the wave, relative (its arrival differs by up to a month too)
# the business cycle every state shares (ordinary applications, by calendar year, interpolated through mid-years)
CYCLE = {2020: 1.050, 2021: 1.034, 2022: 0.997, 2023: 1.025, 2024: 1.008, 2025: 0.985, 2026: 1.000, 2027: 1.000,
         2028: 1.000}
# the formation rate's common movement from one year's applications to the next
RATE_CYCLE = {2020: 1.000, 2021: 1.004, 2022: 0.998, 2023: 1.001, 2024: 0.997, 2025: 1.002, 2026: 1.000,
              2027: 1.000, 2028: 1.000}
# a state's own texture, at a state of REF_SIZE ordinary applications a month; a larger state's series is the sum of
# more local markets and moves less (the sizes below scale with the square root of REF_SIZE over the state's size)
REF_SIZE = 4000.0
WANDER_RHO = 0.85       # persistence of a state's own wander (monthly, log)
WANDER_SD = 0.008       # monthly innovation of the wander
MONTH_NOISE = 0.018     # month-to-month irregularity in ordinary applications, beyond counting noise
RATE_SD = 0.012         # a state's formation rate from one application year to the next (log scale)

# seasonal profile of applications (unadjusted), January first; the added applications follow formation filings,
# with a slightly sharper January
SEAS = np.array([1.236, 1.031, 1.079, 1.012, 0.991, 0.968, 0.982, 1.003, 0.931, 0.968, 0.892, 0.907])
SEAS = SEAS / SEAS.mean()
SEAS_ADDED = np.array([1.312, 1.043, 1.071, 1.004, 0.982, 0.958, 0.977, 0.996, 0.925, 0.963, 0.880, 0.889])
SEAS_ADDED = SEAS_ADDED / SEAS_ADDED.mean()

# flags, shares of all applications of either kind: planned wages and corporations within high-propensity
WBA_OF_HBA = 0.312
CBA_OF_HBA = 0.168

TAIL8 = 0.112           # formations in quarters 5 to 8, per formation within four quarters
DUR4, DUR8 = 1.31, 1.69  # average duration to formation (quarters) among formations within four and eight quarters


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


def _yearly(table, t):
    """A yearly level read through mid-years: linear between the July of one year and the July of the next."""
    y, m = K.mfrom(t)
    pos = y + (m - 7) / 12.0
    y0 = int(math.floor(pos))
    w = pos - y0
    return (1 - w) * table[y0] + w * table[y0 + 1]


def wave(t, size=1.0, lag=0):
    return 1.0 + WAVE * size * _smooth(t, K.midx(WAVE_FROM) + lag, K.midx(WAVE_TO) + lag)


def common(t):
    """Common factor on ordinary applications in month index t: the shared cycle, then the early 2026 wave."""
    return _yearly(CYCLE, t) * wave(t)


def drift(t, s):
    return (1 + s.trend) ** (t / 12.0)


def take_up(t, usps, ramp=None):
    """Added applications per ordinary application at full take-up, as a share (0 before go-live)."""
    ramp = RETIRE_RAMP if ramp is None else ramp
    li, lf = _frac_month_after(LAUNCH[usps])
    ri, rf = _frac_month_after(RETIRE[usps])
    if t < li:
        return 0.0

    def voluntary(k):
        return VOLUNTARY * (1 - math.exp(-(k + 0.5) / TAU)) * (1 + SURGE * math.exp(-k / SURGE_TAU))

    if t < ri:
        v = voluntary(t - li)
        return v * lf if t == li else v
    # once the older route closes every filer goes through the integrated filing: take-up moves from where the
    # voluntary phase stood to full over RETIRE_RAMP months (the closing month counts by its share of days)
    v_r = voluntary(ri - li)
    done = (t - ri) + (rf if t == ri else 1.0)
    return v_r + (1.0 - v_r) * min(1.0, done / ramp)


def size_factor(s):
    return math.sqrt(REF_SIZE / s.base)


def wander(r, n, sd):
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = WANDER_RHO * x[t - 1] + sd * r.standard_normal()
    return np.exp(x - x[:24].mean())


def rate_path(s, r):
    """The ordinary formation rate within four quarters for each application month."""
    years = {y: float(np.exp(RATE_SD * size_factor(s) * r.standard_normal())) for y in range(2020, 2029)}
    out = np.zeros(K.NM)
    for t in range(K.NM):
        y, m = K.mfrom(t)
        out[t] = s.y4 * (1 + s.rtrend) ** ((t - K.midx(2023, 1)) / 12.0) * _yearly(RATE_CYCLE, t) * years[y]
    return out


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
    Y4: dict = field(default_factory=dict)     # the ordinary formation rate by application month


def simulate():
    W = World()
    for s in STATES:
        r = K.rng("apps", s.usps)
        rt = K.rng("texture", s.usps)
        wd = wander(rt, K.NM, WANDER_SD * size_factor(s))
        w_size = float(np.exp(WAVE_SD * rt.standard_normal()))
        w_lag = int(rt.integers(0, 2))
        level = np.array([s.base * drift(t, s) * wd[t] for t in range(K.NM)])
        g_mean = np.array([level[t] * (1 + (_yearly(CYCLE, t) - 1) * s.resp) * wave(t, w_size * s.resp, w_lag) *
                           SEAS[t % 12] for t in range(K.NM)])
        g_mean = g_mean * np.exp(MONTH_NOISE * size_factor(s) * rt.standard_normal(K.NM))
        if s.usps in REFORM:
            # take-up is per ordinary application at the state's own level (filers forming entities; the shared
            # cycle and the wave are not formation filings)
            ramp = RETIRE_RAMP * float(np.exp(0.25 * rt.standard_normal()))
            noise = np.exp(TAKEUP_NOISE * rt.standard_normal(K.NM))
            i_mean = np.array([level[t] * ADDED_MAX[s.usps] * take_up(t, s.usps, ramp) * noise[t] * SEAS_ADDED[t % 12]
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
        hi = rf.binomial(I, s.hba)
        W.HBA[s.usps] = hg + hi
        W.WBA[s.usps] = rf.binomial(hg, WBA_OF_HBA) + rf.binomial(hi, WBA_OF_HBA)
        W.CBA[s.usps] = rf.binomial(hg, CBA_OF_HBA) + rf.binomial(hi, CBA_OF_HBA)
        y4 = rate_path(s, K.rng("rates", s.usps))
        W.Y4[s.usps] = y4
        rb = K.rng("formations", s.usps)
        f4g = rb.binomial(G, y4)
        f4i = rb.binomial(I, y4 * REL_ADDED)
        W.F4G[s.usps], W.F4I[s.usps] = f4g, f4i
        W.F4[s.usps] = f4g + f4i
        rest = W.BA[s.usps] - W.F4[s.usps]
        W.F8[s.usps] = W.F4[s.usps] + rb.binomial(rest, np.clip(TAIL8 * W.F4[s.usps] / np.maximum(rest, 1), 0, 1))
        W.D4[s.usps] = np.round(DUR4 + 0.04 * rb.standard_normal(K.NM), 2)
        W.D8[s.usps] = np.round(DUR8 + 0.05 * rb.standard_normal(K.NM), 2)
    return W
