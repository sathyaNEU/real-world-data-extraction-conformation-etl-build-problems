"""task166's golden computation, from the shipped files only (no generator state): the loan-month history since 2019,
each first mortgage's rate recovered from the senior lien the lending system took from the credit report, the payoff
hazard read off the stack's blended rate against the posted 30-year rate, projected month by month on the planning
cycle's base case; and every rung of the ladder and the rival routes on the same history.

The golden:
  each fixed-rate home equity loan's monthly payoff probability is a logistic in the stack's refinancing incentive
  (the blended rate of the first mortgage and the home equity loan at their balances, less the posted 30-year rate a
  month earlier; a piecewise-linear spline, knots at -1, 0, 0.5, 1, 1.5 and 2 points), with calendar-month seasonality
  (one sine and cosine pair) and a marker for a first mortgage opened less than 24 months before; fitted on every
  loan-month from January 2019 to November 2026; curtailments at the new core's monthly rate on the surviving balance;
  the loans on the books at 30 November 2026 run from December 2026 through December 2027 on the base case."""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import re

import numpy as np
import pandas as pd

KNOTS = [-1.0, 0.0, 0.5, 1.0, 1.5, 2.0]
ASOF = (2026, 11)
YEAR = 2027
REG_ORDER = ["Grand Rapids", "The Lakeshore", "Kalamazoo and Battle Creek", "Muskegon and the North"]

F_LEGACY = "legacy_he_loans_2019-01_2024-08.csv"
F_CORE = "core_he_trial_balance_2024-09_2026-11.csv"
F_XREF = "core_conversion_xref.csv"
F_LOS = "he_lending_file_2009-2026.csv"
F_MAP = "county_region_map.csv"
F_RATES = "posted_rate_sheets_2018-12_2026-11.csv"
F_PLAN = "planning_cycle_2027_rates.xlsx"


def mo(y, m):
    return y * 12 + (m - 1)


def ym(o):
    return o // 12, o % 12 + 1


def mmyyyy(s):
    s = str(s).strip().zfill(6)
    return mo(int(s[2:]), int(s[:2]))


# ------------------------------------------------------------------------------------------------- reading the pack
def read_rates(target):
    """the posted 30-year rate's monthly average, each sheet in effect from its date to the next, day-weighted"""
    r = pd.read_csv(os.path.join(target, F_RATES))
    r30 = r[r["product"] == "30 YR FIXED MORTGAGE"].copy()
    r30["d"] = pd.to_datetime(r30.effective_date)
    r30 = r30.sort_values("d")
    days = pd.date_range("2018-12-01", "2026-11-30", freq="D")
    eff = pd.Series(np.nan, index=days)
    idx = np.searchsorted(r30.d.values, days.values, side="right") - 1
    vals = r30.rate_pct.values
    s = pd.Series(np.where(idx >= 0, vals[np.clip(idx, 0, None)], np.nan), index=days)
    s = s.bfill()
    m = s.groupby([s.index.year, s.index.month]).mean()
    return {mo(y, mm): float(v) for (y, mm), v in m.items()}


def read_plan(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, F_PLAN), read_only=True, data_only=True)
    ws = wb["Base case"]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        d = row[0]
        out[mo(d.year, d.month)] = float(row[1])
    wb.close()
    return out


def read_region(target):
    mp = pd.read_csv(os.path.join(target, F_MAP))
    return dict(zip(mp.county, mp.regional_lending_center))


def amort_balance(A, rate, n, k):
    i = np.asarray(rate, float) / 1200.0
    g = (1.0 + i) ** np.asarray(n, float)
    k = np.clip(np.asarray(k, float), 0, None)
    b = np.asarray(A, float) * (g - (1.0 + i) ** k) / (g - 1.0)
    return np.where(k >= np.asarray(n, float), 0.0, b)


def solve_rate(A, B, n, k):
    """the note rate (per cent) at which a level-payment loan of A over n months has balance B after k payments"""
    lo = np.full(len(A), 0.25)
    hi = np.full(len(A), 14.0)
    for _ in range(60):
        mid = (lo + hi) / 2
        bm = amort_balance(A, mid, n, k)
        # the balance after k payments rises with the rate
        hi = np.where(bm > B, mid, hi)
        lo = np.where(bm > B, lo, mid)
    return (lo + hi) / 2


def solve_payment_rate(A, pay, n):
    """the rate at which a level payment on A over n months equals the reported payment"""
    lo = np.full(len(A), 0.25)
    hi = np.full(len(A), 20.0)
    for _ in range(60):
        mid = (lo + hi) / 2
        i = mid / 1200.0
        pm = A * i / (1 - (1 + i) ** -n)
        hi = np.where(pm > pay, mid, hi)
        lo = np.where(pm > pay, lo, mid)
    return (lo + hi) / 2


def first_mortgages(los, by_payment=False, blank_360=False, one_fewer=False):
    """each funded loan's first mortgage from the senior lien fields: the rate by the amortization identity on the
    original amount, the term and the balance at its reported month (a blank term is the one of 360 and 180 months
    whose rate the reported principal-and-interest payment can carry). by_payment solves the rate from the reported
    payment instead, blank_360 reads every blank term as 360 months, and one_fewer counts one payment fewer by the
    reported month (the other readings checks.py runs)."""
    A = los.senior_lien_original_amount.astype(float).values
    B = los.senior_lien_balance.astype(float).values
    o1 = np.array([mmyyyy(x) for x in los.senior_lien_opened])
    ob = np.array([mmyyyy(x) for x in los.senior_lien_balance_as_of])
    k = ob - o1
    if one_fewer:
        k = np.maximum(k - 1, 1)
    term = los.senior_lien_term_months
    pay = los.senior_lien_monthly_payment.astype(float).values
    n = np.where(term.isna(), 360, term.fillna(360)).astype(float)
    r = solve_rate(A, B, n, k)
    if by_payment:
        r = solve_payment_rate(A, pay, n)
    given = los.senior_lien_note_rate_pct.astype(float).values
    r = np.where(np.isnan(given), r, given)
    blank = term.isna().values
    if blank.any() and not blank_360:
        r15 = solve_rate(A, B, np.full(len(A), 180.0), k)
        pi30 = A * (r / 1200) / (1 - (1 + r / 1200) ** -360)
        pi15 = A * (r15 / 1200) / (1 - (1 + r15 / 1200) ** -180)
        # the term whose principal and interest sits nearest the reported payment without exceeding it
        use15 = blank & (np.abs(pay - pi15) < np.abs(pay - pi30)) & (pi15 <= pay + 1.0)
        n = np.where(use15, 180.0, n)
        r = np.where(use15, r15, r)
    return pd.DataFrame({"o1": o1, "n1": n, "r1": r, "A1": A}, index=los.index)


def load(target, **fm):
    """the loan table (one row per fixed-rate home equity loan in either core), its region and first mortgage, and the
    month-end balances and payoffs the cores record"""
    leg = pd.read_csv(os.path.join(target, F_LEGACY), dtype={"LOAN_NO": str, "MBR_NO": str})
    core = pd.read_csv(os.path.join(target, F_CORE), dtype={"LoanNumber": str, "MemberNumber": str})
    xref = pd.read_csv(os.path.join(target, F_XREF), dtype=str)
    los = pd.read_csv(os.path.join(target, F_LOS), dtype={"loan_number": str, "member_number": str,
                                                           "senior_lien_opened": str, "senior_lien_balance_as_of": str})
    region = read_region(target)
    x = dict(zip(xref.legacy_loan_no, xref.loan_number))
    los["key"] = [x.get(v, v) for v in los.loan_number]
    los = los.join(first_mortgages(los, **fm))
    los["region"] = los.property_county.map(region)
    los = los.set_index("key")
    leg["key"] = [x.get(v, v) for v in leg.LOAN_NO]
    for c in ("ORIG_AMT",):
        leg[c] = leg[c].astype(str).str.replace(",", "").astype(float)
    return leg, core, los


def history(target, leg, core, los, rates, legacy_from_funding=False, exits_as_payoffs=False, drop_conversion=False):
    """one row per loan per month from January 2019 to November 2026 that the loan began on the books: the balance at
    the start of the month, and whether the loan was paid in full by the member in the month. Legacy months carry the
    balance the loan's schedule gives from its 2018 year-end balance or its funding; new core months the recorded
    month-end balance."""
    rows = []
    # legacy core, January 2019 to August 2024
    lg = leg.copy()
    lg["open_m"] = [mo(int(d[6:]), int(d[:2])) for d in lg.OPEN_DT]
    lg["close_m"] = [mo(int(d[6:]), int(d[:2])) if isinstance(d, str) and d else -1 for d in lg.CLOSE_DT.fillna("")]
    lg["rate"] = lg.NOTE_RT.astype(float)
    lg["n"] = lg.TERM_MOS.astype(int)
    lg["b18"] = pd.to_numeric(lg.BAL_12_31_2018, errors="coerce")
    conv_last = mo(2024, 8)
    for r in lg.itertuples(index=False):
        start = max(r.open_m + 1, mo(2019, 1))
        end = r.close_m if r.close_m >= 0 else conv_last
        if end < start:
            continue
        ts = np.arange(start, end + 1)
        if r.open_m < mo(2019, 1) and not legacy_from_funding:
            # balances after the 2018 year-end balance, on the schedule from there
            k = ts - 1 - mo(2018, 12)
            rem = r.n - (mo(2018, 12) - r.open_m)
            bal = amort_balance(r.b18, r.rate, rem, k)
        else:
            k = ts - 1 - r.open_m
            bal = amort_balance(r.ORIG_AMT, r.rate, r.n, k)
        y = np.zeros(len(ts), int)
        drop = np.zeros(len(ts), bool)
        if r.close_m >= 0:
            if r.CLOSE_CD == "PIF" or exits_as_payoffs:
                y[-1] = 1
            else:
                drop[-1] = True
        keep = ~drop
        rows.append(pd.DataFrame({"key": r.key, "t": ts[keep], "H": bal[keep], "y": y[keep]}))
    leg_hist = pd.concat(rows, ignore_index=True)
    # new core, September 2024 to November 2026: the balance at the prior month-end
    c = core.copy()
    c["t"] = [mo(int(d[:4]), int(d[5:7])) for d in c.AsOfDate]
    c = c.sort_values(["LoanNumber", "t"])
    c["prev"] = c.groupby("LoanNumber").PrincipalBalance.shift(1)
    first_core = c.groupby("LoanNumber").t.transform("min")
    # the first core month of a converted loan begins at its conversion balance
    conv = leg.set_index("key").BAL_AT_CONV
    c.loc[(c.t == mo(2024, 9)) & c.LoanNumber.isin(conv.dropna().index), "prev"] = \
        c.loc[(c.t == mo(2024, 9)) & c.LoanNumber.isin(conv.dropna().index), "LoanNumber"].map(conv).astype(float)
    if drop_conversion:
        c = c[c.t > mo(2024, 9)]
    c = c[c.prev.notna() & (c.prev > 0)]
    if not exits_as_payoffs:
        c = c[~c.LoanStatus.isin(["MAT", "CHGOFF"])]
    core_hist = pd.DataFrame({"key": c.LoanNumber.values, "t": c.t.values, "H": c.prev.values,
                              "y": (c.LoanStatus != "ACTIVE").astype(int).values})
    H = pd.concat([leg_hist, core_hist], ignore_index=True)
    H = H[H.key.isin(los.index)]
    return H


def features(df, los, rates):
    L = los.loc[df.key]
    df = df.copy()
    df["region"] = L.region.values
    df["r2"] = L.note_rate_pct.astype(float).values
    df["n2"] = L.term_months.astype(int).values
    df["r1"] = L.r1.values
    df["F"] = amort_balance(L.A1.values, L.r1.values, L.n1.values, df.t.values - 1 - L.o1.values)
    df["m1"] = [rates[t - 1] for t in df.t]
    df["blend"] = (df.F * df.r1 + df.H * df.r2) / (df.F + df.H) - df.m1
    df["first"] = df.r1 - df.m1
    spread = {120: 1.70, 180: 1.95, 240: 2.20}
    df["cal"] = df.t % 12 + 1
    df["s1"] = np.sin(2 * np.pi * df.cal / 12.0)
    df["s2"] = np.cos(2 * np.pi * df.cal / 12.0)
    df["young"] = ((df.t - L.o1.values) < 24).astype(float)
    return df


def spline(x, knots):
    x = np.asarray(x, float)
    return np.column_stack([x] + [np.maximum(x - k, 0.0) for k in knots])


def design(df, cov, knots=KNOTS, seasonal=True, young=True, fe=False):
    import statsmodels.api as sm
    X = [spline(df[c].values, knots) for c in cov]
    if young:
        X.append(df[["young"]].values)
    if seasonal:
        X.append(df[["s1", "s2"]].values)
    if fe:
        for r in REG_ORDER[1:]:
            X.append((df.region.values == r).astype(float)[:, None])
    return sm.add_constant(np.column_stack(X), has_constant="add")


def fit(H, cov, link=None, **kw):
    import statsmodels.api as sm
    X = design(H, cov, **kw)
    fam = sm.families.Binomial() if link is None else sm.families.Binomial(link=link)
    return sm.GLM(H.y.values, X, family=fam).fit()


def curtailment_rate(core):
    c = core.copy()
    c = c[c.LoanStatus == "ACTIVE"].copy()
    c["t"] = [mo(int(d[:4]), int(d[5:7])) for d in c.AsOfDate]
    c = c.sort_values(["LoanNumber", "t"])
    c["prev"] = c.groupby("LoanNumber").PrincipalBalance.shift(1)
    c = c[c.prev.notna() & (c.prev > 0)]
    extra = (c.PrincipalPaid - c.ScheduledPrincipal).clip(lower=0).sum()
    return float(extra / c.prev.sum())


def book(core):
    b = core[(core.AsOfDate == "2026-11-30") & (core.LoanStatus == "ACTIVE")]
    return pd.DataFrame({"key": b.LoanNumber.values, "bal": b.PrincipalBalance.values.astype(float),
                         "rate": b.InterestRate.values.astype(float) * 100, "n": b.TermMonths.values.astype(int),
                         "pmt": b.PaymentAmount.values.astype(float), "open": b.OpenDate.values})


def forward(bk, los, rates, plan):
    """the book's monthly frame from December 2026 to December 2027: the scheduled balance at the start of each month"""
    months = [mo(2026, 12)] + [mo(YEAR, k) for k in range(1, 13)]
    allr = dict(rates)
    allr.update(plan)
    frames = []
    for j, t in enumerate(months):
        # balance at the start of month t: the as-of balance run on its payment for j months
        i = bk.rate.values / 1200.0
        b = bk.bal.values.copy()
        for _ in range(j):
            b = np.maximum(b - (bk.pmt.values - b * i), 0.0)
        frames.append(pd.DataFrame({"key": bk.key.values, "t": t, "H": b}))
    FW = pd.concat(frames, ignore_index=True)
    FW = FW[FW.H > 0]
    FW = features(FW.assign(y=0), los, allr)
    return FW


def project(FW, h, curt):
    """2027 principal paid ahead of schedule by region: each month's payoffs at the start-of-month balance and the
    curtailments of the loans that survive the month"""
    F2 = FW.assign(h=np.asarray(h, float)).sort_values(["key", "t"])
    S = F2.groupby("key").h.transform(lambda s: np.concatenate([[1.0], np.cumprod(1 - s.values)[:-1]]))
    F2["pay"] = S * F2.h * F2.H
    F2["cur"] = S * (1 - F2.h) * curt * F2.H
    F2 = F2[F2.t >= mo(YEAR, 1)]
    tot = (F2.pay + F2.cur).groupby(F2.region).sum() / 1e6
    return tot.reindex(REG_ORDER)


def golden(target, verbose=False):
    rates = read_rates(target)
    plan = read_plan(target)
    leg, core, los = load(target)
    H = features(history(target, leg, core, los, rates), los, rates)
    f = fit(H, ["blend"])
    curt = curtailment_rate(core)
    bk = book(core)
    FW = forward(bk, los, rates, plan)
    out = project(FW, f.predict(design(FW, ["blend"])), curt)
    ctx = dict(rates=rates, plan=plan, leg=leg, core=core, los=los, H=H, FW=FW, curt=curt, model=f, book=bk)
    return out, ctx


if __name__ == "__main__":
    import sys
    import time
    t = time.time()
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    out, ctx = golden(target)
    print(out.round(3))
    print("curtailment rate", round(ctx["curt"], 6), "history rows", len(ctx["H"]), "events", int(ctx["H"].y.sum()),
          "seconds", round(time.time() - t, 1))


# ------------------------------------------------------------------------------------------------- the ladder and the rivals
HE_SPREAD = None


def he_posted_monthly(target):
    """the posted fixed home equity rate's monthly average by term (10, 15, 20 years), day-weighted like the 30-year"""
    r = pd.read_csv(os.path.join(target, F_RATES))
    out = {}
    for term, prod in ((120, "HOME EQUITY FIXED 10 YR"), (180, "HOME EQUITY FIXED 15 YR"), (240, "HOME EQUITY FIXED 20 YR")):
        x = r[r["product"] == prod].copy()
        x["d"] = pd.to_datetime(x.effective_date)
        x = x.sort_values("d")
        days = pd.date_range("2018-12-01", "2026-11-30", freq="D")
        idx = np.searchsorted(x.d.values, days.values, side="right") - 1
        s = pd.Series(np.where(idx >= 0, x.rate_pct.values[np.clip(idx, 0, None)], np.nan), index=days).bfill()
        m = s.groupby([s.index.year, s.index.month]).mean()
        out[term] = {mo(y, mm): float(v) for (y, mm), v in m.items()}
    return out


def plan_he(target):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(target, F_PLAN), read_only=True, data_only=True)
    ws = wb["Base case"]
    out = {120: {}, 180: {}, 240: {}}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] is None:
            continue
        t = mo(row[0].year, row[0].month)
        out[120][t], out[180][t], out[240][t] = float(row[3]), float(row[4]), float(row[5])
    wb.close()
    return out


def add_own(df, he, plan_h=None):
    """the home equity loan's own incentive: its note rate less the posted home equity rate for its term a month earlier"""
    allh = {k: dict(v) for k, v in he.items()}
    if plan_h:
        for k in allh:
            allh[k].update(plan_h[k])
    p = np.array([allh[n][t - 1] for n, t in zip(df.n2.values, df.t.values)])
    df = df.copy()
    df["p1"] = p
    df["own"] = df.r2 - p
    # each lien against its own posted rate, weighted by balance
    df["walt"] = (df.F * (df.r1 - df.m1) + df.H * (df.r2 - df.p1)) / (df.F + df.H)
    return df


def routes(target, ctx=None):
    """every rung and rival on the shipped files: region totals for 2027 (USD millions)"""
    import statsmodels.api as sm
    if ctx is None:
        _, ctx = golden(target)
    H, FW, curt = ctx["H"], ctx["FW"], ctx["curt"]
    he = he_posted_monthly(target)
    ph = plan_he(target)
    H = add_own(H, he)
    FW = add_own(FW, he, ph)
    out = {}
    for name, cov, kw in [("golden: blended stack", ["blend"], {}),
                          ("rung 0: own rate (default path)", ["own"], {}),
                          ("rung 2: first mortgage alone", ["first"], {}),
                          ("own and first together", ["own", "first"], {}),
                          ("each lien at its own rate", ["walt"], {}),
                          ("own rate, region effects", ["own"], {"fe": True}),
                          ("first alone, region effects", ["first"], {"fe": True}),
                          ("blended, region effects", ["blend"], {"fe": True}),
                          ("blended, no seasonality", ["blend"], {"seasonal": False}),
                          ("blended, no purchase marker", ["blend"], {"young": False}),
                          ("blended, three knots", ["blend"], {"knots": [0.0, 1.0, 2.0]})]:
        f = fit(H, cov, **kw)
        out[name] = project(FW, f.predict(design(FW, cov, **kw)), curt)
        out[name]["deviance"] = round(f.deviance, 1)
    f = fit(H, ["blend"], link=sm.families.links.CLogLog())
    out["blended, complementary log-log"] = project(FW, f.predict(design(FW, ["blend"])), curt)
    out["blended, complementary log-log"]["deviance"] = round(f.deviance, 1)
    # rung 1: the trailing twelve months' payoff rate by region on the book
    tr = H[(H.t >= mo(2025, 12))]
    rate = tr[tr.y == 1].groupby("region").H.sum() / (tr.groupby("region").H.sum() / 12.0)
    bk = ctx["book"].merge(ctx["los"][["region"]], left_on="key", right_index=True)
    out["rung 1: trailing payoff rate"] = (rate * bk.groupby("region").bal.sum() / 1e6).reindex(REG_ORDER)
    out["trailing payoffs, Dec 2025 to Nov 2026"] = (tr[tr.y == 1].groupby("region").H.sum() / 1e6).reindex(REG_ORDER)
    R = pd.DataFrame(out).T
    return R


if __name__ == "__main__" and "--routes" in __import__("sys").argv:
    pass


# ------------------------------------------------------------------------------------------------- the ask: payoff statements
F_LOG = "payoff_statement_log_2025-10_2026-11.csv"
F_MANUAL = "payoff_statements_manual_2026-03.xlsx"
F_SERV = "first_mortgage_servicing_2026-11.csv"
QUARTERS = [("2025Q4", dt.date(2025, 10, 1), dt.date(2025, 12, 31)), ("2026Q1", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            ("2026Q2", dt.date(2026, 4, 1), dt.date(2026, 6, 30)), ("2026Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30))]


def eastern_date(ts):
    """a UTC timestamp's calendar date in Grand Rapids (Eastern time, daylight saving from the second Sunday of March to
    the first Sunday of November)"""
    t = dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")
    y = t.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    start = dt.datetime(y, mar.month, mar.day, 7)      # 2 a.m. EST in UTC
    end = dt.datetime(y, nov.month, nov.day, 6)        # 2 a.m. EDT in UTC
    off = 4 if start <= t < end else 5
    return (t - dt.timedelta(hours=off)).date()


def quarter_of(d):
    for q, a, b in QUARTERS:
        if a <= d <= b:
            return q
    return None


def norm_addr(s):
    s = str(s).upper().replace(".", "").replace(",", " ")
    return re.sub(r"\s+", " ", s).strip()


def statement_loans(target, los=None, core=None, with_mortgages=True, with_manual=True, reconcile=True, loose=False):
    """the fixed-rate home equity loans a payoff statement was issued for, with the Eastern date it was issued:
    statements naming the loan (by its new or legacy number), statements on one of the credit union's first mortgages
    whose amount also paid the member's home equity loan on the same property, and the statements prepared by hand
    during the March 2026 outage. reconcile=False counts every first-mortgage statement on a property with a home equity
    loan on the books, whatever its amount (a route checks.py and ceiling.py price); loose=True counts a statement whose
    amount exceeds the first mortgage's scheduled balance in the statement's month by more than half the home equity
    balance (a coarser reconciliation checks.py shows converges)"""
    if los is None or core is None:
        _, core, los = load(target)
    xref = pd.read_csv(os.path.join(target, F_XREF), dtype=str)
    x = dict(zip(xref.legacy_loan_no, xref.loan_number))
    he_keys = set(los.index)
    log = pd.read_csv(os.path.join(target, F_LOG), dtype={"account_reference": str, "statement_id": str})
    log = log[log.statement_status.isin(["ISSUED", "UPDATED"])].copy()
    log["d"] = [eastern_date(s) for s in log.issued_utc]
    out = []
    for r in log.itertuples(index=False):
        ref = x.get(r.account_reference, r.account_reference)
        if ref in he_keys:
            out.append((ref, r.d, "named"))
    if with_mortgages:
        serv = pd.read_csv(os.path.join(target, F_SERV), dtype={"mortgage_loan_number": str, "member_number": str})
        addr = {}
        for k, row in los.iterrows():
            addr.setdefault((norm_addr(row.property_street), str(row.property_zip)), []).append(k)
        bal = he_balance_lookup(core, target)
        sv = serv.set_index("mortgage_loan_number")
        for r in log[log.product_on_file == "MTG"].itertuples(index=False):
            if r.account_reference not in sv.index:
                continue
            m = sv.loc[r.account_reference]
            cands = addr.get((norm_addr(m.property_street), str(m.property_zip)), [])
            days = (dt.date.fromisoformat(r.good_through_date) - r.d).days
            mb = mortgage_balance(m, r.d)
            rest = float(r.statement_amount) - mb * (1 + float(m.note_rate_pct) / 36500.0 * days) - 25.0
            for k in cands:
                hb = bal(k, r.d)
                if hb is None:
                    continue
                # the quoted amount covers the first mortgage and the home equity loan behind it, to the dollar
                he = hb * (1 + float(los.loc[k].note_rate_pct) / 36500.0 * days)
                if loose:
                    hit = float(r.statement_amount) > mortgage_balance(m, r.d, 0) + 0.5 * hb
                else:
                    hit = abs(rest - he) <= 1.0
                if not reconcile or hit:
                    out.append((k, r.d, "mortgage"))
    if with_manual:
        from openpyxl import load_workbook
        wb = load_workbook(os.path.join(target, F_MANUAL), read_only=True, data_only=True)
        ws = wb.active
        addr2 = {}
        for k, row in los.iterrows():
            addr2.setdefault(norm_addr("%s %s %s" % (row.property_street, row.property_city, row.property_zip)), []).append(k)
        bal = he_balance_lookup(core, target)
        for row in ws.iter_rows(min_row=4, values_only=True):
            if row[0] is None or not row[4] or "home equity" not in str(row[4]).lower():
                continue
            d = row[0].date() if isinstance(row[0], dt.datetime) else row[0]
            for k in addr2.get(norm_addr(row[3]), []):
                if bal(k, d) is not None:
                    out.append((k, d, "manual"))
        wb.close()
    S = pd.DataFrame(out, columns=["key", "d", "how"])
    S["region"] = S.key.map(los.region)
    S["quarter"] = [quarter_of(d) for d in S.d]
    return S


def he_balance_lookup(core, target):
    """a loan's principal balance on a date: the core's prior month-end balance while the loan is on the books, and the
    amount funded for a loan funded earlier in the date's month"""
    c = core[["LoanNumber", "AsOfDate", "PrincipalBalance", "LoanStatus"]]
    tbl = {}
    for r in c.itertuples(index=False):
        tbl[(r.LoanNumber, r.AsOfDate[:7])] = (float(r.PrincipalBalance), r.LoanStatus)
    opened = {r.LoanNumber: (r.OpenDate, float(r.OriginalAmount))
              for r in core[["LoanNumber", "OpenDate", "OriginalAmount"]].drop_duplicates("LoanNumber").itertuples(index=False)}

    def f(key, d):
        y, m = d.year, d.month
        pm = (y, m - 1) if m > 1 else (y - 1, 12)
        v = tbl.get((key, "%04d-%02d" % pm))
        if v is None:
            o = opened.get(key)
            if o is not None and o[0][:7] == "%04d-%02d" % (y, m) and o[0] <= d.isoformat():
                return o[1]
            return None
        if v[0] <= 0:
            return None
        return v[0]
    return f


def mortgage_balance(m, d, back=1):
    """a credit union first mortgage's scheduled balance at the month-end before a date (back=0: after the date's
    month's payment)"""
    nd = dt.date.fromisoformat(m.note_date)
    k = (d.year - nd.year) * 12 + (d.month - nd.month) - back
    return float(amort_balance(float(m.original_amount), float(m.note_rate_pct), int(m.term_months), k))


def ask_counts(S):
    """distinct loans a statement was issued for, by region and quarter"""
    S = S[S.quarter.notna()]
    g = S.groupby(["region", "quarter"]).key.nunique()
    return {(r, q): int(g.get((r, q), 0)) for r in REG_ORDER for q, _, _ in QUARTERS}


def paid_by_asof(core):
    """the loans the new core shows paid in full by the member on or before 30 November 2026"""
    p = core[(core.LoanStatus == "PIF") & (core.CloseDate.fillna("") <= "2026-11-30")]
    return set(p.LoanNumber)


def ask_table(S, paid):
    """per center and quarter: loans quoted (distinct), and how many of those were paid in full by 30 November 2026"""
    S = S[S.quarter.notna()]
    out = {}
    for r in REG_ORDER:
        for q, _, _ in QUARTERS:
            ks = set(S[(S.region == r) & (S.quarter == q)].key)
            out[(r, q)] = (len(ks), len(ks & paid))
    return out


def simple_rates(target):
    """the month's posted 30-year rate as the plain average of the sheets dated in it (a mishandled reading)"""
    r = pd.read_csv(os.path.join(target, F_RATES))
    r = r[r["product"] == "30 YR FIXED MORTGAGE"]
    m = r.groupby([d[:7] for d in r.effective_date]).rate_pct.mean()
    return {mo(int(k[:4]), int(k[5:7])): float(v) for k, v in m.items()}


def variant(target, cache=None, rates_mode="day", lag=1, hist=None, fm=None, model=None, curtail=True,
            with_december=False, cov=("blend",)):
    """the golden with one convention or reading changed: the rates' basis and lag, the history's construction, the first
    mortgages' recovery, the model's form, curtailments, December 2026 in the window"""
    import statsmodels.api as sm
    hist = hist or {}
    fm = fm or {}
    model = dict(model or {})
    rates = read_rates(target)
    if rates_mode != "day":
        rates.update(simple_rates(target))
    plan = read_plan(target)
    key = ("load", tuple(sorted(fm.items())))
    if cache is not None and key in cache:
        leg, core, los = cache[key]
    else:
        leg, core, los = load(target, **fm)
        if cache is not None:
            cache[key] = (leg, core, los)
    allr = dict(rates)
    allr.update(plan)
    H = history(target, leg, core, los, rates, **hist)
    H = features(H, los, rates)
    bk = book(core)
    FW = forward(bk, los, rates, plan)
    if lag != 1:
        for df in (H, FW):
            df["m1"] = [allr.get(t - lag, allr[min(allr)]) for t in df.t]
            df["blend"] = (df.F * df.r1 + df.H * df.r2) / (df.F + df.H) - df.m1
            df["first"] = df.r1 - df.m1
    link = model.pop("link", None)
    f = fit(H, list(cov), link=link, **model)
    h = f.predict(design(FW, list(cov), **model))
    curt = curtailment_rate(core) if curtail else 0.0
    if not with_december:
        return project(FW, h, curt), f
    F2 = FW.assign(h=np.asarray(h, float)).sort_values(["key", "t"])
    S = F2.groupby("key").h.transform(lambda s: np.concatenate([[1.0], np.cumprod(1 - s.values)[:-1]]))
    v = S * F2.h * F2.H + S * (1 - F2.h) * curt * F2.H
    return (v.groupby(F2.region).sum() / 1e6).reindex(REG_ORDER), f
