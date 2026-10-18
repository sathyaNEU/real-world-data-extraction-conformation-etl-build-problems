"""The clean truth of task166's world: the bank's rate sheets, its five fixed-rate pools and every behaviour that
generates their records. Nothing here is shipped as is; records.py writes the pack from it in the systems' own layouts.
Behaviour parameters live only here; the golden (calc.py) estimates everything from the shipped files.

Pools at the close on 30 November 2026:
  T    Treasury ladder (available-for-sale notes bought 2021 to 2026)
  MBS  agency pass-throughs bought in 2020 and 2021 (mostly 15-year)
  M    2023-24 residential mortgages held for investment (portfolio jumbo)
  AUTO indirect auto loans
  CRE  fixed-rate commercial real estate term loans"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

mo, ym = K.mo, K.ym


def path(knots, start, end):
    """monthly path, linear between (year, month) knots, as {ordinal: value}"""
    xs = [mo(y, m) for (y, m) in knots]
    ys = list(knots.values())
    return {o: float(np.interp(o, xs, ys)) for o in range(start, end + 1)}


# ------------------------------------------------------------------------------------------------- rate targets
# the bank's posted 30-year portfolio jumbo rate, monthly level the weekly sheets move around, per cent
J30_TARGET = {mo(2022, 1) + i: v for i, v in enumerate([
    3.55, 3.95, 4.45, 5.05, 5.35, 5.75, 5.55, 5.40, 6.05, 6.95, 6.80, 6.45,        # 2022
    6.30, 6.40, 6.55, 6.40, 6.60, 6.75, 6.85, 7.05, 7.20, 7.40, 7.25, 6.95,        # 2023
    7.05, 7.10, 7.15, 7.25, 7.20, 7.05, 6.90, 6.55, 6.25, 6.50, 6.90, 6.95,        # 2024
    7.00, 6.90, 6.85, 6.95, 7.00, 6.95, 6.90, 6.75, 6.45, 6.40, 6.70, 6.80,        # 2025
    6.75, 6.80, 6.85, 6.80, 6.75, 6.70, 6.65, 6.70, 6.75, 6.80, 6.85])}           # 2026 to November
# the 15-year conforming rate (the agency pools' borrowers), per cent
C15_TARGET = {mo(2019, 1) + i: v for i, v in enumerate(
    list(np.round(np.interp(np.arange(36), [0, 8, 14, 20, 24, 30, 35], [4.05, 3.15, 2.95, 2.55, 2.30, 2.25, 2.35]), 2)) +
    [2.85, 3.25, 3.70, 4.30, 4.55, 4.90, 4.75, 4.65, 5.20, 6.10, 6.00, 5.70,      # 2022
     5.60, 5.75, 5.85, 5.70, 5.90, 6.05, 6.15, 6.45, 6.65, 7.00, 6.75, 6.10,      # 2023
     5.95, 6.10, 6.15, 6.40, 6.35, 6.20, 6.05, 5.75, 5.40, 5.60, 6.00, 6.05,      # 2024
     6.15, 6.05, 5.95, 5.95, 6.00, 5.95, 5.85, 5.75, 5.55, 5.50, 5.65, 5.85,      # 2025
     6.00, 6.10, 6.20, 6.25, 6.30, 6.30, 6.25, 6.15, 6.10, 6.05, 6.00])}          # 2026 to November
# the bank's posted five-year fixed CRE rate, per cent
CRE5_TARGET = path({(2007, 1): 6.30, (2009, 1): 5.95, (2010, 6): 5.45, (2012, 6): 4.45, (2013, 1): 4.25,
                    (2013, 9): 4.95, (2015, 1): 4.45, (2016, 7): 3.95, (2017, 1): 4.55, (2018, 11): 5.30,
                    (2019, 9): 4.15, (2020, 3): 3.80, (2020, 8): 3.25, (2021, 6): 3.35, (2021, 12): 3.65,
                    (2022, 3): 4.30, (2022, 6): 5.30, (2022, 10): 6.45, (2023, 3): 6.65, (2023, 10): 7.45,
                    (2024, 1): 6.75, (2024, 4): 7.05, (2024, 9): 6.35, (2025, 1): 6.90, (2025, 9): 6.55,
                    (2026, 3): 6.85, (2026, 11): 6.80}, mo(2007, 1), K.ASOF_M)
# one-month SOFR (floating CRE coupons), per cent
SOFR = path({(2022, 1): 0.05, (2022, 6): 1.50, (2022, 12): 4.30, (2023, 7): 5.30, (2024, 8): 5.33, (2024, 12): 4.45,
             (2025, 9): 4.30, (2025, 12): 3.90, (2026, 6): 3.75, (2026, 11): 3.70}, mo(2022, 1), K.ASOF_M)
# market capitalisation rate behind the bank's appraisals (truth only), per cent
CAP = path({(2007, 1): 6.6, (2009, 6): 7.8, (2012, 1): 7.0, (2015, 1): 6.3, (2019, 1): 6.0, (2020, 6): 6.1,
            (2021, 6): 5.4, (2022, 3): 4.85, (2022, 9): 5.3, (2023, 6): 6.1, (2024, 6): 6.6, (2026, 11): 6.7},
           mo(2007, 1), K.ASOF_M)
# property income level of the bank's markets (truth only): flat to 2016, up to 2020, a dip, the 2021-22 surge,
# then expenses (insurance, taxes, payroll) running ahead of rents from 2023
NOI_IDX = path({(2006, 1): 0.92, (2009, 6): 0.86, (2012, 1): 0.92, (2016, 1): 1.02, (2019, 12): 1.08, (2020, 6): 1.03,
                (2021, 6): 1.06, (2022, 4): 1.15, (2023, 6): 1.16, (2024, 6): 1.14, (2025, 6): 1.12, (2026, 11): 1.09},
               mo(2006, 1), K.ASOF_M)

SEASON = [0.74, 0.80, 0.96, 1.06, 1.16, 1.24, 1.26, 1.20, 1.06, 0.96, 0.84, 0.72]   # home-sale turnover by month


# ------------------------------------------------------------------------------------------------- the rate sheets
# product code, first sheet month, target path, rounding step, spread to the target
PRODUCTS = [
    ("J30F", mo(2022, 1), "J30", 0.125, 0.0),     # portfolio jumbo 30-year fixed
    ("J15F", mo(2022, 1), "J30", 0.125, -0.55),   # portfolio jumbo 15-year fixed
    ("C30F", mo(2019, 1), "C15", 0.125, 0.70),    # conforming 30-year fixed
    ("C15F", mo(2019, 1), "C15", 0.125, 0.0),     # conforming 15-year fixed
    ("CRE5F", mo(2015, 1), "CRE5", 0.05, 0.0),    # commercial real estate five-year fixed
]


def mondays(o_start, o_end):
    y, m = ym(o_start)
    d = dt.date(y, m, 1)
    d += dt.timedelta(days=(7 - d.weekday()) % 7)
    end = K.month_end(o_end)
    out = []
    while d <= end:
        out.append(d)
        d += dt.timedelta(days=7)
    return out


def build_rate_sheets(W):
    """weekly sheets (a Monday sheet, and an extra mid-week re-price in volatile weeks); the monthly rate the
    behaviour reads is the average of the sheets issued in the month."""
    g = K.rng(10)
    tgt = {"J30": J30_TARGET, "C15": C15_TARGET, "CRE5": CRE5_TARGET}
    sheets = []
    for code, start, key, step, spread in PRODUCTS:
        T = tgt[key]
        for d in mondays(start, K.ASOF_M):
            o = mo(d.year, d.month)
            frac = (d.day - 1) / 31.0
            nxt = T.get(o + 1, T[o])
            prv = T.get(o - 1, T[o])
            # the sheet sits on the month's level, leaning toward its neighbours at the month's edges
            lvl = T[o] + (nxt - T[o]) * max(0.0, frac - 0.5) * 0.6 + (prv - T[o]) * max(0.0, 0.5 - frac) * 0.6
            lvl += spread + g.normal(0, 0.035 if step < 0.1 else 0.045)
            rate = round(lvl / step) * step
            pts = round(float(g.choice([0.0, 0.125, 0.25, 0.375, 0.5], p=[0.30, 0.20, 0.25, 0.15, 0.10])), 3) \
                if code != "CRE5F" else 0.0
            sheets.append((d, code, round(rate, 3), pts))
            if g.random() < 0.06:                      # a mid-week re-price
                d2 = d + dt.timedelta(days=int(g.integers(2, 4)))
                if mo(d2.year, d2.month) <= K.ASOF_M:
                    r2 = round((lvl + g.normal(0, 0.06)) / step) * step
                    sheets.append((d2, code, round(r2, 3), pts))
    sheets.sort(key=lambda s: (s[0], s[1]))
    W.sheets = sheets
    mon = {}
    for d, code, rate, pts in sheets:
        mon.setdefault((code, mo(d.year, d.month)), []).append(rate)
    W.rate = {k: float(np.mean(v)) for k, v in mon.items()}
    W.J30 = {o: W.rate[("J30F", o)] for o in range(mo(2022, 1), K.ASOF_M + 1)}
    W.C15 = {o: W.rate[("C15F", o)] for o in range(mo(2019, 1), K.ASOF_M + 1)}
    # the CRE rate before the archive starts is the target path itself (origination rates only)
    W.CRE5 = {o: (W.rate[("CRE5F", o)] if o >= mo(2015, 1) else CRE5_TARGET[o]) for o in range(mo(2007, 1), K.ASOF_M + 1)}


# ------------------------------------------------------------------------------------------------- loan arithmetic
def dc(r_pct, n=300):
    """annual debt-service constant of a level-payment loan, rate in per cent"""
    r = np.asarray(r_pct, float) / 1200.0
    return 12 * r / (1 - (1 + r) ** (-n))


def pmt(bal, r_pct, n):
    r = np.asarray(r_pct, float) / 1200.0
    n = np.maximum(np.asarray(n, float), 1)
    return bal * r / (1 - (1 + r) ** (-n))


def days_in(o):
    return K.month_end(o).day


def run_balance(b0, r_pct, payment, o_first, n, basis):
    """balance after each of n monthly payments starting in month o_first; interest on the basis (ACT/360 counts the
    month's days, 30/360 thirty); the payment is fixed, principal is what it leaves after interest."""
    B = b0
    out = []
    for k in range(n):
        o = o_first + k
        days = days_in(o - 1) if basis == "ACT/360" else 30      # interest accrues over the month before the payment
        intr = B * r_pct / 100.0 * days / 360.0
        prin = min(payment - intr, B)
        B = B - prin
        out.append(B)
    return out


# ------------------------------------------------------------------------------------------------- behaviour (truth)
M_TURN = 0.0046            # monthly turnover hazard at full seasoning, average month
M_REFI = 0.0480            # refinancing hazard ceiling
M_MID, M_W = 0.0062, 0.0021  # incentive midpoint and width (fractions)
M_CURTAIL = 0.0004         # monthly partial prepayment, share of balance
M_SCALE = 1.14             # loan size (design): sets the pool's level so the ladder's margins hold


def m_smm(incent, month_of_year, age):
    ramp = np.minimum(1.0, 0.45 + 0.55 * np.asarray(age, float) / 12.0)
    turn = M_TURN * np.asarray([SEASON[(k - 1) % 12] for k in np.atleast_1d(month_of_year)]) * ramp
    refi = M_REFI / (1.0 + np.exp(-(np.asarray(incent, float) - M_MID) / M_W))
    return turn + refi


CRE_C0, CRE_S = 1.10, 0.012  # extension: logistic in refinance cover
# the push loans' income scale: the one design parameter set against the golden, by a rule written before any route
# was measured: solved so the file-built cover-logit figure sits within $0.5 million of $150 million, the centre of
# its $10 million reporting bin
PUSH_SCALE = 1.011
CRE_EXT_MONTHS = 36
CRE_EARLY = 0.0006          # monthly hazard of an early sale payoff (with the prepayment premium)
# the fixed-rate book's origination intensity (loans a month): before 2013, 2013-18, 2019-20, 2021 to November
CRE_LAM = (3.4, 4.8, 6.2, 7.5)
# the push: five-year fixed loans from December 2021 to April 2022, underwritten on pro forma rents; the cash-out
# deals took the credit box's full proceeds, the rate-and-term refinances (half the push) far less. After the push the
# bank wrote floating-rate CRE only (build_cre_floating).
PUSH_FROM, PUSH_TO, PUSH_LAM = mo(2021, 12), mo(2022, 4), 120.0
PUSH_PROFORMA = 1.18
PUSH_FIT, PUSH_LOWLEV_P, PUSH_LOWLEV = (0.97, 1.0), 0.50, (0.55, 0.70)
# term mix (five, seven, ten years); borrowers locked longer terms at the 2020-21 lows
TERMS, LATE_TERMS = [0.64, 0.23, 0.13], [0.35, 0.45, 0.20]
NOI_SD, NOI_SHOCK_P, NOI_SHOCK = 0.03, 0.02, (0.66, 0.86)


def cre_p_ext(cover):
    return 1.0 / (1.0 + np.exp((np.asarray(cover, float) - CRE_C0) / CRE_S))


AUTO_ABS = 0.0128           # auto prepayments: share of original balance each month


# ------------------------------------------------------------------------------------------------- the pools
class World:
    pass


STATES_M = (["PA"] * 70 + ["OH"] * 18 + ["WV"] * 7 + ["MD"] * 3 + ["NY"] * 2)


def build_mortgages(W):
    """2023-24 portfolio jumbo originations, simulated month by month to the as-of."""
    g = K.rng(11)
    loans = []
    lid = 0
    for o in range(mo(2023, 1), mo(2024, 12) + 1):
        y, m = ym(o)
        lam = 198 if y == 2023 else 261
        lam *= 1.0 + 0.22 * math.sin((m - 3) / 12 * 2 * math.pi)
        for _ in range(g.poisson(lam)):
            lid += 1
            term = int(g.choice([360, 240, 180], p=[0.88, 0.05, 0.07]))
            adj = g.choice([-0.125, 0.0, 0.125, 0.25, 0.375, 0.5], p=[0.12, 0.30, 0.24, 0.17, 0.11, 0.06])
            base = W.J30[o] - (0.55 if term == 180 else 0.25 if term == 240 else 0.0)
            note = round((base + adj) * 8) / 8
            bal0 = float(np.clip(np.exp(g.normal(math.log(395000), 0.42)), 120000, 2600000)) * M_SCALE
            bal0 = round(bal0 / 50) * 50
            loans.append(dict(lid=lid, orig=o, term=term, note=note, bal0=bal0))
    W.m_loans = loans
    hist = []
    for L in loans:
        B = L["bal0"]
        n = L["term"]
        r = L["note"]
        L["exit"] = None
        for o in range(L["orig"] + 1, K.ASOF_M + 1):
            age = o - L["orig"]
            k = n - (age - 1)
            pay = float(pmt(B, r, k))
            intr = B * r / 1200.0
            sched = min(pay - intr, B)
            curt = M_CURTAIL * (B - sched) * (g.random() < 0.35) * 2.6
            inc = (r - W.J30[o - 1]) / 100.0
            smm = float(m_smm(inc, ym(o)[1], age)[0])
            u = g.random()
            status = "C"
            if u < smm:
                status = "PIF"     # paid in full
            elif u < smm + 0.00012:
                status = "TRF"     # servicing released (loan sold)
            if status == "C":
                Bn = B - sched - curt
                hist.append((L["lid"], o, B, sched, curt, 0.0, Bn, r, status))
                B = Bn
            else:
                hist.append((L["lid"], o, B, sched, 0.0, B - sched, 0.0, r, status))
                L["exit"] = (o, status)
                B = 0.0
                break
        L["bal_asof"] = B
    W.m_hist = hist
    W.m_pool = [L for L in loans if L["exit"] is None]
    # loan attributes the servicing system carries (none moves behaviour)
    ga = K.rng(18)
    for L in loans:
        L["state"] = str(ga.choice(STATES_M))
        L["occ"] = str(ga.choice(["P", "S", "I"], p=[0.90, 0.08, 0.02]))
        L["ltv"] = int(np.clip(round(ga.normal(72, 9)), 35, 90))
        L["fico"] = int(np.clip(round(ga.normal(768, 28)), 660, 840))
        L["purpose"] = str(ga.choice(["P", "R", "C"], p=[0.74, 0.16, 0.10]))
        L["day"] = int(ga.integers(1, 29))     # origination day of month


def build_hfs(W):
    """conforming loans originated for sale in 2023-24: the servicing system carries them until the agency purchase
    settles, usually inside two months."""
    g = K.rng(17)
    rows = []
    lid = 900000
    for o in range(mo(2023, 1), mo(2024, 12) + 1):
        y, m = ym(o)
        lam = 105 if y == 2023 else 132
        lam *= 1.0 + 0.25 * math.sin((m - 3) / 12 * 2 * math.pi)
        for _ in range(g.poisson(lam)):
            lid += 1
            term = int(g.choice([360, 180], p=[0.86, 0.14]))
            note = round((W.C15[o] + (0.70 if term == 360 else 0.0) + g.choice([-0.125, 0, 0.125, 0.25])) * 8) / 8
            bal0 = round(float(np.clip(np.exp(g.normal(math.log(285000), 0.35)), 80000, 766550)) / 50) * 50
            months_held = int(g.choice([1, 2, 3], p=[0.55, 0.38, 0.07]))
            rows.append(dict(lid=lid, orig=o, term=term, note=note, bal0=bal0, held=months_held,
                             state=str(g.choice(STATES_M)), occ="P", ltv=int(np.clip(round(g.normal(78, 10)), 40, 97)),
                             fico=int(np.clip(round(g.normal(742, 35)), 620, 830)),
                             purpose=str(g.choice(["P", "R", "C"], p=[0.70, 0.18, 0.12])), day=int(g.integers(1, 29))))
    W.hfs = rows


PTYPES = ["MF", "OFF", "RET", "IND", "MIX"]
MSAS = [("Pittsburgh", "PA", 0.52), ("Cleveland", "OH", 0.14), ("Columbus", "OH", 0.10), ("Erie", "PA", 0.06),
        ("Morgantown", "WV", 0.06), ("Wheeling", "WV", 0.04), ("Youngstown", "OH", 0.04), ("State College", "PA", 0.04)]


def build_cre(W):
    g = K.rng(12)
    rows = []
    lid = 0
    for o in range(mo(2007, 1), mo(2024, 12) + 1):
        y, m = ym(o)
        lam = CRE_LAM[0] if y < 2013 else CRE_LAM[1] if y < 2019 else CRE_LAM[2]
        if mo(2021, 1) <= o <= mo(2021, 11):
            lam = CRE_LAM[3]
        push = PUSH_FROM <= o <= PUSH_TO
        if push:
            lam = PUSH_LAM       # the bank's fixed-rate CRE push, before the programme moved to floating
        if o > PUSH_TO:
            lam = 0.0            # floating only from May 2022
        for _ in range(g.poisson(lam)):
            lid += 1
            late = mo(2020, 1) <= o <= mo(2021, 11)
            term = int(g.choice([60, 84, 120], p=[1.0, 0.0, 0.0] if push else LATE_TERMS if late else TERMS))
            amort = int(g.choice([300, 240, 360], p=[0.78, 0.12, 0.10]))
            r0 = round((W.CRE5[o] + g.normal(0.05, 0.12)) * 100) / 100
            noi0 = float(np.exp(g.normal(math.log(560000), 0.62))) * (PUSH_SCALE if push else 1.0)
            value = noi0 / (CAP[o] / 100.0 * math.exp(g.normal(0, 0.05)))
            if o >= mo(2021, 12):
                ltv_max, dscr_min = 0.72, 1.25
            elif o >= mo(2020, 4):
                ltv_max, dscr_min = 0.62, 1.25      # pandemic caution
            elif o >= mo(2017, 7):
                ltv_max, dscr_min = 0.75, 1.20      # the 2017-19 credit box
            else:
                ltv_max, dscr_min = 0.70, 1.25
            uw_noi = noi0 * (PUSH_PROFORMA if push else 1.0)   # the push was sized on pro forma rents
            b_ltv = ltv_max * uw_noi / (CAP[o] / 100.0 * math.exp(g.normal(0, 0.05)))
            b_dscr = uw_noi / (dscr_min * float(dc(r0, amort)))
            if push:      # cash-out deals took the box's full proceeds; rate-and-term refinances took far less
                fit = g.uniform(*PUSH_LOWLEV) if g.random() < PUSH_LOWLEV_P else g.uniform(*PUSH_FIT)
            else:
                fit = g.uniform(0.86, 1.0)
            b0 = min(b_ltv, b_dscr) * fit
            b0 = round(b0 / 1000) * 1000
            ptype = str(g.choice(PTYPES, p=[0.34, 0.18, 0.20, 0.18, 0.10]))
            rows.append(dict(lid=lid, orig=o, term=term, amort=amort, r0=r0, noi0=noi0, b0=b0, value0=value,
                             ptype=ptype, push=push, fit=fit))
    # property income by the borrower's fiscal year (annual reviews), a random walk on the market index
    for L in rows:
        fy_start = ym(L["orig"])[0]
        walk = 1.0
        L["noi"] = {}
        for fy in range(fy_start, 2027):
            walk *= math.exp(g.normal(0, NOI_SD))
            if g.random() < NOI_SHOCK_P:
                walk *= g.uniform(*NOI_SHOCK)     # a tenant lost, a cost shock the rents never caught
            L["noi"][fy] = walk                   # the walk only; the level comes with the fiscal year's midpoint
    # life: early sale payoff, maturity outcome (extension once, 36 months at the note rate), repayment
    for L in rows:
        L["mat"] = L["orig"] + L["term"]
        L["early"] = None
        for o in range(L["orig"] + 1, min(L["mat"], K.ASOF_M + 1)):
            if g.random() < CRE_EARLY:
                L["early"] = o
                break
    # attributes, identifiers, the day count, statements (a second stream: the behaviour's draws stay put)
    ga = K.rng(19)
    obligors = []
    for L in rows:
        y, m = ym(L["orig"])
        L["basis"] = "ACT/360" if L["orig"] >= mo(2012, 1) else "30/360"
        L["oday"] = int(ga.integers(1, 29))
        msa = MSAS[int(ga.choice(len(MSAS), p=[x[2] for x in MSAS]))]
        L["msa"], L["state"] = msa[0], msa[1]
        if obligors and ga.random() < 0.08:
            L["obligor"] = obligors[int(ga.integers(0, len(obligors)))]
        else:
            L["obligor"] = int(ga.integers(100000, 999999))
            obligors.append(L["obligor"])
        L["fye"] = int(ga.choice([12, 6, 9], p=[0.74, 0.16, 0.10]))
        L["exp_ratio"] = float(np.clip(ga.normal({"MF": 0.46, "OFF": 0.44, "RET": 0.36, "IND": 0.30, "MIX": 0.42}[L["ptype"]],
                                                 0.05), 0.18, 0.68))
        L["review_lag"] = [int(ga.integers(70, 160)) for _ in range(30)]
        L["basis_stmt"] = [str(ga.choice(["Borrower prepared", "CPA reviewed", "Audited"], p=[0.55, 0.35, 0.10]))
                           for _ in range(30)]
    seen = {}
    for L in rows:
        k = (L["obligor"])
        seen[k] = seen.get(k, 0) + 1
        L["note_no"] = seen[k]
    for i, L in enumerate(rows):
        L["prop"] = 10000 + i * 7 + int(ga.integers(0, 7))
        L["payment"] = float(np.round(pmt(L["b0"], L["r0"], L["amort"]), 2))
        n_pay = min(L["term"] + CRE_EXT_MONTHS, L["amort"])
        L["bal_path"] = run_balance(L["b0"], L["r0"], L["payment"], L["orig"] + 1, n_pay, L["basis"])
        L["bal_mat"] = L["bal_path"][L["term"] - 1]
    # each fiscal year's statement: the twelve months to the borrower's year end, reviewed some months later
    for L in rows:
        st = []
        oy = ym(L["orig"])[0]
        for j, fy in enumerate(range(oy, 2027)):
            end_o = mo(fy, L["fye"])
            if end_o < L["orig"] + 12:              # the first statement covers a full year on the bank's loan
                continue
            mid = end_o - 6
            lvl = L["noi0"] * NOI_IDX[min(mid, K.ASOF_M)] / NOI_IDX[L["orig"]] * L["noi"][fy]
            rev = lvl / (1.0 - L["exp_ratio"])
            end_d = K.month_end(end_o)
            rdate = end_d + dt.timedelta(days=L["review_lag"][j % 30])
            st.append(dict(fy=fy, end=end_d, end_o=end_o, noi=lvl, rev=rev, exp=rev - lvl, review=rdate,
                           basis=L["basis_stmt"][j % 30]))
        L["stmts"] = st
    # the decision at maturity reads the latest statement reviewed before the maturity date
    for L in rows:
        L["mat_date"] = dt.date(*ym(L["mat"]), L["oday"])
        L["ext"] = None
        L["outcome"] = None
        if L["early"] is None and L["mat"] <= K.ASOF_M:
            prior = [s for s in L["stmts"] if s["review"] < L["mat_date"]]
            s = prior[-1]
            L["noi_review"] = s["noi"]
            L["cover"] = L["noi_review"] / (L["bal_mat"] * float(dc(W.CRE5[L["mat"]], 300)))
            L["p_ext"] = float(cre_p_ext(L["cover"]))
            L["ext"] = bool(g.random() < L["p_ext"])
            L["outcome"] = "EXTENDED" if L["ext"] else "PAID"
    W.cre = rows


def build_cre_floating(W):
    """floating-rate CRE term loans, the programme from May 2022 (five and seven years): positions only."""
    g = K.rng(16)
    out = []
    lid = 0
    for o in range(mo(2022, 5), K.ASOF_M + 1):
        for _ in range(g.poisson(5.6)):
            lid += 1
            term = int(g.choice([60, 84], p=[0.8, 0.2]))
            spread = round(float(g.uniform(2.35, 3.10)) * 20) / 20
            b0 = round(float(np.exp(g.normal(math.log(4.6e6), 0.6))) / 1000) * 1000
            msa = MSAS[int(g.choice(len(MSAS), p=[x[2] for x in MSAS]))]
            amort = 300
            # principal amortises on a 25-year schedule at the rate in force; approximate the balance
            age = K.ASOF_M - o
            bal = b0 * (1 - age / amort * 0.55)
            out.append(dict(lid=lid, orig=o, term=term, spread=spread, b0=b0, bal=round(bal, 2), msa=msa[0],
                            state=msa[1], ptype=str(g.choice(PTYPES, p=[0.38, 0.12, 0.14, 0.26, 0.10])),
                            oday=int(g.integers(1, 29)), obligor=int(g.integers(100000, 999999)),
                            prop=60000 + lid * 5 + int(g.integers(0, 5))))
    W.cre_float = out


def build_mbs(W):
    g = K.rng(13)
    pools = []
    for i in range(30):
        issue = mo(2020, 3) + int(g.integers(0, 19))
        thirty = i % 6 == 2
        cpn = 2.0 if g.random() < 0.55 else 2.5
        wac = cpn + round(g.uniform(0.62, 0.85) if thirty else g.uniform(0.50, 0.68), 3)
        face = round(float(g.uniform(64, 128)) * 1e6, -5)
        wam0 = int(g.integers(349, 358)) if thirty else int(g.integers(171, 180))
        pools.append(dict(pid=i, issue=issue, cpn=cpn, wac=wac, face=face, wam0=wam0, term=360 if thirty else 180))
    for P in pools:
        P["factors"] = {P["issue"]: 1.0}
        bal = 1.0
        for o in range(P["issue"] + 1, K.ASOF_M + 1):
            age = o - P["issue"]
            k = P["wam0"] - (age - 1)
            pay = float(pmt(bal, P["wac"], k))
            intr = bal * P["wac"] / 1200.0
            sched = min(pay - intr, bal)
            inc = (P["wac"] - W.C15.get(o - 1, 5.5) - (0.70 if P["term"] == 360 else 0.0)) / 100.0
            lock = 0.62 if inc < -0.02 else 0.8 if inc < -0.01 else 1.0
            smm = M_TURN * 0.95 * SEASON[ym(o)[1] - 1] * lock + 0.030 / (1 + math.exp(-(inc - 0.0075) / 0.0022))
            smm *= math.exp(g.normal(0, 0.08))
            bal = (bal - sched) * (1 - smm)
            P["factors"][o] = bal
    # purchase dates and prices (the bank bought each pool within a few months of issue)
    ga = K.rng(20)
    for P in pools:
        P["bought"] = P["issue"] + int(ga.integers(0, 4))
        P["price"] = round(float(ga.uniform(101.6, 104.4)) * 32) / 32
        P["agency"] = str(ga.choice(["FNMA", "FHLMC"], p=[0.6, 0.4]))
    W.mbs = pools


def build_treasuries(W):
    # (purchase month, coupon %, maturity date, par $): one rung a half-year, 2027 to 2032
    W.ust = [
        (mo(2021, 3), 0.750, dt.date(2027, 3, 31), 140_000_000),
        (mo(2021, 9), 1.125, dt.date(2027, 8, 31), 135_000_000),
        (mo(2022, 2), 1.875, dt.date(2028, 2, 29), 145_000_000),
        (mo(2023, 5), 3.625, dt.date(2028, 5, 31), 120_000_000),
        (mo(2023, 10), 4.875, dt.date(2028, 10, 31), 115_000_000),
        (mo(2024, 4), 4.625, dt.date(2029, 4, 30), 130_000_000),
        (mo(2024, 10), 3.875, dt.date(2029, 9, 30), 125_000_000),
        (mo(2025, 3), 4.000, dt.date(2030, 2, 28), 135_000_000),
        (mo(2025, 6), 4.000, dt.date(2030, 5, 31), 120_000_000),
        (mo(2025, 9), 3.625, dt.date(2030, 8, 31), 125_000_000),
        (mo(2025, 11), 3.750, dt.date(2031, 5, 31), 130_000_000),
        (mo(2026, 4), 4.125, dt.date(2031, 10, 31), 125_000_000),
        (mo(2026, 8), 4.000, dt.date(2032, 7, 31), 115_000_000),
    ]


def build_auto(W):
    """indirect auto originations from December 2020, run to the as-of under ABS prepayment and charge-offs
    (vectorised by origination month); the monthly portfolio roll is kept for the run-off report."""
    g = K.rng(15)
    lid = 0
    keep = []
    roll = {}
    for o in range(mo(2020, 12), K.ASOF_M + 1):
        y, m = ym(o)
        lam = 1450 if y >= 2024 else 1200
        n = int(g.poisson(lam))
        if n == 0:
            continue
        term = g.choice([60, 72, 75, 84], size=n, p=[0.30, 0.46, 0.14, 0.10]).astype(float)
        mu = 3.9 if y <= 2021 else 5.6 if y == 2022 else 7.6 if y <= 2024 else 7.1
        apr = np.round(np.clip(g.normal(mu, 1.4, n), 1.9, 13.5), 2)
        bal0 = np.round(np.clip(np.exp(g.normal(math.log(33500), 0.38, n)), 7000, 95000), 2)
        ids = np.arange(lid + 1, lid + n + 1)
        lid += n
        roll.setdefault(o, dict(orig=0.0, sched=0.0, prepay=0.0, co=0.0, n_orig=0))
        roll[o]["orig"] += float(bal0.sum())
        roll[o]["n_orig"] += n
        B = bal0.copy()
        alive = np.ones(n, bool)
        r = apr / 1200.0
        for t in range(o + 1, K.ASOF_M + 1):
            age = t - o
            k = term - (age - 1)
            alive &= k > 0
            pay = np.where(alive, B * r / (1 - (1 + r) ** (-np.maximum(k, 1))), 0.0)
            sched = np.where(alive, np.minimum(pay - B * r, B), 0.0)
            smm = np.minimum(1.0, AUTO_ABS * bal0 / np.maximum(B, 1.0))
            u = g.random(n)
            pre = alive & (u < smm)
            co = alive & ~pre & (g.random(n) < 0.0011)
            R = roll.setdefault(t, dict(orig=0.0, sched=0.0, prepay=0.0, co=0.0, n_orig=0))
            R["sched"] += float(sched[alive & ~pre & ~co].sum())
            R["prepay"] += float(B[pre].sum())
            R["co"] += float(B[co].sum())
            alive &= ~pre & ~co
            B = np.where(alive, B - sched, 0.0)
            done = alive & (B <= 1)
            alive &= B > 1
        for j in np.nonzero(alive)[0]:
            keep.append(dict(lid=int(ids[j]), orig=o, term=int(term[j]), apr=float(apr[j]), bal0=float(bal0[j]),
                             bal=float(B[j]), age=K.ASOF_M - o))
    W.auto_roll = roll
    W.auto_pool = keep
    ga = K.rng(21)
    for a in keep:
        a["dealer"] = int(ga.integers(1000, 1460))
        a["state"] = str(ga.choice(["PA", "OH", "WV", "MD", "NY"], p=[0.66, 0.21, 0.09, 0.02, 0.02]))
        a["new"] = str(ga.choice(["NEW", "USED"], p=[0.38, 0.62]))
        a["fico"] = str(ga.choice(["<620", "620-679", "680-739", "740+"], p=[0.04, 0.18, 0.36, 0.42]))
        a["oday"] = int(ga.integers(1, 29))


def simulate():
    W = World()
    build_rate_sheets(W)
    build_mortgages(W)
    build_hfs(W)
    build_cre(W)
    build_cre_floating(W)
    build_mbs(W)
    build_treasuries(W)
    build_auto(W)
    return W
