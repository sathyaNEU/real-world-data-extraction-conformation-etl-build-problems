"""The clean truth of task166's world: the credit union's posted rates, its members' home equity loans and the first
mortgages ahead of them, and every behaviour that generates their records. Nothing here ships as is; records.py writes
the pack from it in the systems' own layouts. Behaviour parameters live only here; calc.py estimates everything from
the shipped files.

A member pays a closed-end second off when the house is sold or when the member refinances the debt on it. The
refinance is driven by the whole stack: the first mortgage and the second at their balances, their blended rate against
a new first mortgage at the posted 30-year rate (a cash-out refinance prices a quarter point above it)."""
from __future__ import annotations

import datetime as dt
import math
from dataclasses import dataclass, field

import numpy as np

import common as K

mo, ym = K.mo, K.ym

# ------------------------------------------------------------------------------------------------- posted rates
ANNUAL_30 = {2002: 6.62, 2003: 5.93, 2004: 5.94, 2005: 5.97, 2006: 6.51, 2007: 6.44, 2008: 6.13, 2009: 5.14,
             2010: 4.79, 2011: 4.55, 2012: 3.76, 2013: 4.08, 2014: 4.27, 2015: 3.95, 2016: 3.75, 2017: 4.09,
             2018: 4.64}
MONTHLY_30 = {
    2019: [4.55, 4.47, 4.37, 4.24, 4.17, 3.90, 3.87, 3.72, 3.71, 3.79, 3.80, 3.82],
    2020: [3.72, 3.57, 3.55, 3.41, 3.33, 3.26, 3.12, 3.04, 2.99, 2.93, 2.87, 2.78],
    2021: [2.84, 2.91, 3.18, 3.16, 3.06, 3.08, 2.97, 2.94, 3.00, 3.17, 3.17, 3.20],
    2022: [3.55, 3.86, 4.27, 5.08, 5.33, 5.62, 5.51, 5.32, 6.21, 7.00, 6.91, 6.46],
    2023: [6.37, 6.36, 6.64, 6.44, 6.53, 6.81, 6.94, 7.17, 7.30, 7.72, 7.54, 6.92],
    2024: [6.84, 6.98, 7.02, 7.20, 7.26, 7.12, 7.05, 6.80, 6.58, 6.70, 7.01, 6.92],
    2025: [7.16, 7.04, 6.85, 6.93, 7.02, 7.02, 6.92, 6.85, 6.66, 6.58, 6.56, 6.59],
    2026: [6.64, 6.68, 6.75, 6.82, 6.86, 6.80, 6.72, 6.66, 6.62, 6.68, 6.74, 6.71],
}
# the planning cycle's base case, December 2026 then each month of 2027 (the 30-year fixed, monthly average)
PLAN_30 = [6.62, 6.45, 6.10, 5.85, 5.65, 5.55, 5.48, 5.42, 5.37, 5.32, 5.28, 5.24, 5.20]
HE_SPREAD = {120: 1.70, 180: 1.95, 240: 2.20}     # posted fixed home equity rate over the 30-year, by term
M15_SPREAD = 0.62                                  # the 15-year fixed below the 30-year
CASH_OUT = 0.25                                    # a cash-out refinance prices this far above the posted 30-year

START = mo(2002, 1)
END = mo(2027, 12)


def _rate_path():
    M = np.zeros(END + 1)
    g = K.rng(1)
    # annual levels interpolated through mid-year knots, with a small within-year wander
    xs = [mo(y, 7) for y in sorted(ANNUAL_30)] + [mo(2019, 1)]
    ys = [ANNUAL_30[y] for y in sorted(ANNUAL_30)] + [MONTHLY_30[2019][0]]
    for o in range(START, mo(2019, 1)):
        M[o] = float(np.interp(o, xs, ys)) + g.normal(0, 0.07)
    for y, vs in MONTHLY_30.items():
        for k, v in enumerate(vs):
            M[mo(y, k + 1)] = v
    for k, v in enumerate(PLAN_30):
        M[mo(2026, 12) + k] = v
    return np.round(M, 2)


M30 = _rate_path()


def m15(o):
    return round(M30[o] - M15_SPREAD, 2)


def he_posted(o, term):
    return round(M30[o] + HE_SPREAD[term], 2)


# ------------------------------------------------------------------------------------------------- behaviour (truth)
TH, TS, RMAX = 0.40, 0.15, 0.050      # the refinance response to the stack's incentive: threshold, scale, peak monthly
TURN = 0.0042                          # monthly sale rate of a settled household
TURN_YOUNG = 0.45                      # its multiple in the first two years after a purchase
CURT_P, CURT_LO, CURT_HI = 0.030, 0.005, 0.060
BIG_CURT_P = 0.0018                    # a large curtailment (a bonus, an inheritance), 20 to 50 per cent
CHARGE_OFF = 0.00008


def refi_h(I):
    return RMAX / (1.0 + np.exp(-(I - TH) / TS))


def turn_h(cal_month, months_since_purchase):
    seas = 1.0 + 0.35 * np.sin(2 * np.pi * (cal_month - 3) / 12.0)
    return TURN * seas * np.where(months_since_purchase < 24, TURN_YOUNG, 1.0)


def payment(P, rate, n):
    i = rate / 1200.0
    return P * i / (1.0 - (1.0 + i) ** (-n))


def sched_balance(P, rate, n, k):
    """scheduled balance after k payments of a level-payment loan (vectorised)"""
    i = np.asarray(rate, float) / 1200.0
    k = np.clip(np.asarray(k, float), 0, None)
    g = (1.0 + i) ** np.asarray(n, float)
    b = np.asarray(P, float) * (g - (1.0 + i) ** k) / (g - 1.0)
    return np.where(k >= n, 0.0, b)


# ------------------------------------------------------------------------------------------------- the stacks
# (region, kind, count, HE funded from, to, boom start or None, first opened from, to, share of 15-year firsts,
#  first original amount range, HE amount range, share of firsts the credit union holds)
STREAMS = [
    ("GR", "tap", 1300, mo(2023, 1), mo(2026, 11), mo(2024, 1), mo(2020, 3), mo(2021, 12), 0.10, (200e3, 340e3), (40e3, 110e3), 0.10),
    ("GR", "tap", 1100, mo(2023, 1), mo(2026, 11), mo(2024, 1), mo(2012, 1), mo(2016, 12), 0.05, (300e3, 450e3), (40e3, 110e3), 0.10),
    ("GR", "purchase", 1150, mo(2014, 1), mo(2026, 11), None, None, None, 0.0, (180e3, 360e3), (20e3, 55e3), 0.18),
    ("GR", "tap", 1200, mo(2014, 1), mo(2022, 6), None, mo(2009, 1), mo(2019, 12), 0.15, (150e3, 280e3), (30e3, 80e3), 0.10),
    ("GR", "seasoned", 300, mo(2016, 1), mo(2026, 11), None, mo(2003, 1), mo(2013, 12), 0.10, (90e3, 170e3), (50e3, 140e3), 0.12),
    ("GR", "tap", 380, mo(2009, 1), mo(2013, 12), None, mo(2002, 1), mo(2012, 12), 0.15, (130e3, 240e3), (25e3, 70e3), 0.10),
    ("LS", "purchase", 1800, mo(2024, 9), mo(2026, 11), None, None, None, 0.0, (260e3, 420e3), (20e3, 45e3), 0.15),
    ("LS", "purchase", 750, mo(2014, 1), mo(2024, 8), None, None, None, 0.0, (200e3, 360e3), (20e3, 55e3), 0.18),
    ("LS", "tap", 400, mo(2022, 7), mo(2026, 11), None, mo(2020, 3), mo(2021, 12), 0.10, (220e3, 340e3), (35e3, 90e3), 0.10),
    ("LS", "tap", 600, mo(2014, 1), mo(2022, 6), None, mo(2009, 1), mo(2019, 12), 0.15, (150e3, 280e3), (30e3, 80e3), 0.10),
    ("LS", "seasoned", 150, mo(2016, 1), mo(2026, 11), None, mo(2003, 1), mo(2013, 12), 0.10, (90e3, 170e3), (50e3, 140e3), 0.12),
    ("LS", "tap", 240, mo(2009, 1), mo(2013, 12), None, mo(2002, 1), mo(2012, 12), 0.15, (140e3, 250e3), (25e3, 70e3), 0.10),
    ("KB", "purchase", 1700, mo(2023, 8), mo(2023, 11), None, None, None, 0.0, (180e3, 300e3), (30e3, 60e3), 0.15),
    ("KB", "purchase", 600, mo(2014, 1), mo(2026, 11), None, None, None, 0.0, (160e3, 280e3), (20e3, 45e3), 0.18),
    ("KB", "tap", 600, mo(2014, 1), mo(2022, 6), None, mo(2009, 1), mo(2019, 12), 0.15, (120e3, 240e3), (30e3, 80e3), 0.10),
    ("KB", "tap", 200, mo(2022, 7), mo(2026, 11), None, mo(2020, 3), mo(2021, 12), 0.10, (150e3, 260e3), (30e3, 80e3), 0.10),
    ("KB", "seasoned", 150, mo(2016, 1), mo(2026, 11), None, mo(2003, 1), mo(2013, 12), 0.10, (90e3, 170e3), (50e3, 140e3), 0.12),
    ("KB", "tap", 300, mo(2009, 1), mo(2013, 12), None, mo(2002, 1), mo(2012, 12), 0.15, (110e3, 210e3), (25e3, 65e3), 0.10),
    ("MN", "seasoned", 1460, mo(2023, 1), mo(2026, 11), mo(2024, 6), mo(2010, 1), mo(2015, 12), 0.0, (110e3, 170e3), (70e3, 112e3), 0.12),
    ("MN", "seasoned", 120, mo(2014, 1), mo(2022, 12), None, mo(2003, 1), mo(2012, 12), 0.10, (90e3, 170e3), (50e3, 130e3), 0.12),
    ("MN", "purchase", 900, mo(2014, 1), mo(2026, 11), None, None, None, 0.0, (140e3, 260e3), (20e3, 45e3), 0.18),
    ("MN", "tap", 300, mo(2022, 7), mo(2026, 11), None, mo(2020, 3), mo(2021, 12), 0.10, (150e3, 260e3), (30e3, 80e3), 0.10),
    ("MN", "tap", 550, mo(2014, 1), mo(2022, 6), None, mo(2009, 1), mo(2019, 12), 0.15, (110e3, 220e3), (30e3, 75e3), 0.10),
    ("MN", "tap", 240, mo(2009, 1), mo(2013, 12), None, mo(2002, 1), mo(2012, 12), 0.15, (100e3, 190e3), (25e3, 65e3), 0.10),
]


@dataclass
class World:
    n: int = 0
    reg: np.ndarray = None          # region code
    kind: np.ndarray = None
    stream: np.ndarray = None
    o1: np.ndarray = None           # first mortgage opened (month)
    n1: np.ndarray = None
    r1: np.ndarray = None
    F0: np.ndarray = None
    cu_first: np.ndarray = None
    o2: np.ndarray = None           # home equity loan funded (month)
    d2: list = None                 # funded date
    n2: np.ndarray = None
    r2: np.ndarray = None
    H0: np.ndarray = None
    pmt2: np.ndarray = None
    score: np.ndarray = None
    tier: np.ndarray = None
    cltv: np.ndarray = None
    value: np.ndarray = None
    county: list = None
    city: list = None
    # outcomes
    exit_m: np.ndarray = None       # month of exit (payoff, charge-off or maturity), -1 if on the books at the as-of
    exit_kind: list = None          # "PAYOFF", "SALE", "REFI", "CHARGEOFF", "MATURED"
    exit_day: list = None
    exit_bal: np.ndarray = None     # principal retired at exit (the balance before the exit)
    bal: dict = field(default_factory=dict)       # (i, month) -> month-end balance, from 2019 on (and the funding month)
    curt: dict = field(default_factory=dict)      # (i, month) -> curtailment that month
    sched: dict = field(default_factory=dict)     # (i, month) -> scheduled principal that month


def _months_weights(lo, hi, boom):
    w = np.ones(hi - lo + 1)
    if boom is not None:
        w = np.where(np.arange(lo, hi + 1) >= boom, 1.0, 0.5)
    return w / w.sum()


def build_stacks():
    rows = []
    for si, (reg, kind, cnt, lo, hi, boom, flo, fhi, f15, Fr, Hr, cus) in enumerate(STREAMS):
        g = K.rng(10, si)
        w = _months_weights(lo, hi, boom)
        for j in range(cnt):
            o2 = int(g.choice(np.arange(lo, hi + 1), p=w))
            if kind == "purchase":
                o1 = o2 - int(g.integers(0, 3))
                n1 = 360
            else:
                top = min(fhi, o2 - 9)
                o1 = int(g.integers(flo, max(flo, top) + 1))
                n1 = 180 if g.random() < f15 else 360
            base1 = M30[o1] - (M15_SPREAD if n1 == 180 else 0.0)
            r1 = round(base1 + g.normal(0.0, 0.17), 3)
            F0 = round(float(g.uniform(*Fr)), -2)
            H0 = round(float(g.uniform(*Hr)), -2)
            n2 = int(g.choice([120, 180, 240], p=[0.30, 0.45, 0.25]))
            sc = int(np.clip(g.normal(752, 42), 620, 840))
            tier = "A" if sc >= 740 else ("B" if sc >= 680 else "C")
            adj = {"A": 0.0, "B": 0.50, "C": 1.25}[tier]
            r2 = round((he_posted(o2, n2) + adj + g.normal(0, 0.06)) / 0.05) * 0.05
            cu = bool(g.random() < cus)
            cltv = float(g.uniform(0.50, 0.89))
            cty = _pick(g, K.COUNTIES[reg])
            city = K.CITIES[cty][int(g.integers(0, len(K.CITIES[cty])))]
            rows.append((reg, kind, si, o1, n1, r1, F0, cu, o2, n2, round(r2, 2), H0, sc, tier, cltv, cty, city))
    W = World()
    W.n = len(rows)
    cols = list(zip(*rows))
    W.reg = np.array(cols[0])
    W.kind = np.array(cols[1])
    W.stream = np.array(cols[2])
    W.o1 = np.array(cols[3])
    W.n1 = np.array(cols[4])
    W.r1 = np.array(cols[5], float)
    W.F0 = np.array(cols[6], float)
    W.cu_first = np.array(cols[7])
    W.o2 = np.array(cols[8])
    W.n2 = np.array(cols[9])
    W.r2 = np.array(cols[10], float)
    W.H0 = np.array(cols[11], float)
    W.score = np.array(cols[12])
    W.tier = np.array(cols[13])
    W.cltv = np.array(cols[14], float)
    W.county = list(cols[15])
    W.city = list(cols[16])
    W.pmt2 = np.round(payment(W.H0, W.r2, W.n2), 2)
    # the first's balance when the home equity loan was funded, and the property value behind the stack
    Fapp = sched_balance(W.F0, W.r1, W.n1, W.o2 - W.o1)
    W.value = np.round((Fapp + W.H0) / W.cltv, -3)
    # funded dates: a business day in the funding month
    W.d2 = []
    for i in range(W.n):
        g = K.rng(11, i)
        y, m = ym(int(W.o2[i]))
        d = K.business_day(dt.date(y, m, int(g.integers(1, 26))))
        if d.month != m:
            d = K.business_day(dt.date(y, m, 1))
        W.d2.append(d)
    return W


def _pick(g, pairs):
    names = [a for a, _ in pairs]
    p = np.array([b for _, b in pairs], float)
    return names[int(g.choice(len(names), p=p / p.sum()))]


def first_balance(W, idx, t):
    return sched_balance(W.F0[idx], W.r1[idx], W.n1[idx], t - W.o1[idx])


def simulate(W):
    """month by month from the first funding to the as-of: scheduled amortisation, curtailments, sales, refinances,
    charge-offs and maturities. Each loan draws from its own keyed stream."""
    n = W.n
    B = np.zeros(n)                 # balance after the month
    alive = np.zeros(n, bool)
    W.exit_m = np.full(n, -1)
    W.exit_kind = [""] * n
    W.exit_day = [None] * n
    W.exit_bal = np.zeros(n)
    gens = [K.rng(20, i) for i in range(n)]
    t0 = int(W.o2.min())
    for t in range(t0, K.ASOF_M + 1):
        new = np.where(W.o2 == t)[0]
        B[new] = W.H0[new]
        alive[new] = True
        if t >= K.REC0 - 1:
            for i in new:
                W.bal[(int(i), t)] = float(B[i])
        idx = np.where(alive & (W.o2 < t))[0]
        if not len(idx):
            continue
        r = W.r2[idx]
        interest = B[idx] * r / 1200.0
        sched = np.minimum(W.pmt2[idx] - interest, B[idx])
        F = first_balance(W, idx, t)
        H = B[idx]
        blend = np.where(F + H > 0, (F * W.r1[idx] + H * r) / np.maximum(F + H, 1.0), r)
        I = blend - (M30[t - 1] + CASH_OUT)
        cal = t % 12 + 1
        since_purchase = t - W.o1[idx]
        h_sale = turn_h(cal, since_purchase)
        h_refi = refi_h(I)
        for k, i in enumerate(idx):
            g = gens[i]
            u = g.random(4)
            bal0 = B[i]
            if bal0 - sched[k] <= 0.5:              # the final scheduled payment
                W.exit_m[i], W.exit_kind[i], W.exit_bal[i] = t, "MATURED", bal0
                W.exit_day[i] = _day(g, t)
                alive[i] = False
                if t >= K.REC0 - 1:
                    W.sched[(int(i), t)] = float(bal0)
                    W.bal[(int(i), t)] = 0.0
                continue
            if t - W.o2[i] >= 6 and u[0] < CHARGE_OFF:
                W.exit_m[i], W.exit_kind[i], W.exit_bal[i] = t, "CHARGEOFF", bal0
                W.exit_day[i] = _day(g, t)
                alive[i] = False
                continue
            hs, hr = h_sale[k], h_refi[k]
            if u[1] < hs + hr:
                kind = "SALE" if u[1] < hs else "REFI"
                W.exit_m[i], W.exit_kind[i], W.exit_bal[i] = t, kind, bal0
                W.exit_day[i] = _day(g, t)
                alive[i] = False
                continue
            c = 0.0
            if u[2] < CURT_P:
                c = round(bal0 * g.uniform(CURT_LO, CURT_HI), -1)
            if u[3] < BIG_CURT_P:
                c += round(bal0 * g.uniform(0.20, 0.50), -2)
            b1 = bal0 - sched[k] - c
            if b1 <= 50.0:                          # a curtailment that clears the loan is a payoff
                W.exit_m[i], W.exit_kind[i], W.exit_bal[i] = t, "PAYOFF", bal0
                W.exit_day[i] = _day(g, t)
                alive[i] = False
                continue
            B[i] = round(b1, 2)
            if t >= K.REC0 - 1:
                W.bal[(int(i), t)] = float(B[i])
                W.sched[(int(i), t)] = float(round(sched[k], 2))
                if c:
                    W.curt[(int(i), t)] = float(c)
    W.book = np.where(alive)[0]
    W.book_bal = {int(i): float(B[i]) for i in W.book}
    return W


def _day(g, t):
    y, m = ym(int(t))
    d = K.business_day(dt.date(y, m, int(g.integers(1, 28))))
    if d.month != m:
        d = K.business_day(dt.date(y, m, 1))
    return d


# ------------------------------------------------------------------------------------------------- the truth's 2027
def truth_2027(W):
    """expected 2027 principal paid ahead of schedule by region under the true behaviour on the planning path:
    payoffs at the scheduled balance plus curtailments on the surviving balance (reference only; never shipped)"""
    idx = W.book
    S = np.ones(len(idx))
    H = np.array([W.book_bal[int(i)] for i in idx])
    out = {r: 0.0 for r in K.RCODE.values()}
    curt_rate = CURT_P * (CURT_LO + CURT_HI) / 2 + BIG_CURT_P * 0.35
    for t in K.FORE:
        F = first_balance(W, idx, t)
        r = W.r2[idx]
        interest = H * r / 1200.0
        sched = np.minimum(W.pmt2[idx] - interest, H)
        blend = (F * W.r1[idx] + H * r) / np.maximum(F + H, 1.0)
        I = blend - (M30[t - 1] + CASH_OUT)
        h = turn_h(t % 12 + 1, t - W.o1[idx]) + refi_h(I)
        pay = S * h * H
        cur = S * (1 - h) * curt_rate * H
        if t in K.YEAR:
            for rc in out:
                m = W.reg[idx] == rc
                out[rc] += float(pay[m].sum() + cur[m].sum())
        S = S * (1 - h)
        H = np.maximum(H - sched - curt_rate * H, 0.0)
    return {k: v / 1e6 for k, v in out.items()}


def simulate_world():
    W = build_stacks()
    simulate(W)
    return W


if __name__ == "__main__":
    import time
    t = time.time()
    W = simulate_world()
    print("stacks", W.n, "on book", len(W.book), "seconds", round(time.time() - t, 1))
    for rc in ["GR", "LS", "KB", "MN"]:
        m = [int(i) for i in W.book if W.reg[i] == rc]
        print(rc, len(m), round(sum(W.book_bal[i] for i in m) / 1e6, 1))
    print({k: round(v, 1) for k, v in truth_2027(W).items()})
