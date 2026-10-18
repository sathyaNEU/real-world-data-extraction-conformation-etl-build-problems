"""task166's golden computation, from the shipped files only (no generator state): each pool's base-case expected cash
flows, the hedging policy's measure on them, every rung of the ladder and the rival routes.

The golden:
  T    contractual coupons and principal
  MBS  each pool's own speed over the last twelve factor months carried forward (the pools are as far out of the money
       under the planning base case as they were in 2026); cash a month after the factor month
  M    a prepayment model fitted to the servicing history: turnover by calendar month and loan age plus refinancing on
       an S-curve in the incentive (note rate less the bank's posted jumbo rate a month earlier), projected at the
       planning cycle's 6.25 per cent
  AUTO the portfolio's own monthly prepayment rate over the last twelve months
  CRE  each fixed-rate loan's balloon extended with the probability a logistic in refinance cover gives (the latest
       reviewed net operating income against a new loan of the balloon at the planning cycle's CRE rate on the bank's
       25-year amortisation), fitted on every maturity since 2015 and chosen out of sample against the rivals"""
from __future__ import annotations

import csv
import datetime as dt
import math
import os

import numpy as np
from scipy.optimize import minimize

HORIZON = 360
TENORS = None
ZEROS = None


# ------------------------------------------------------------------------------------------------- calendar helpers
def mo(y, m):
    return y * 12 + (m - 1)


def ym(o):
    return o // 12, o % 12 + 1


def ordinal(d):
    return mo(d.year, d.month)


def pdate(s):
    s = s.strip()
    if not s:
        return None
    if len(s) == 8 and s.isdigit():
        return dt.date(int(s[4:]), int(s[:2]), int(s[2:4]))
    return dt.date.fromisoformat(s[:10])


def month_days(o):
    y, m = ym(o)
    nxt = dt.date(y + (m // 12), m % 12 + 1, 1)
    return (nxt - dt.timedelta(days=1)).day


ASOF = mo(2026, 11)
START = ASOF + 1                       # December 2026, the first projected month
MEASURE = [mo(2027, k) for k in range(1, 13)]


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------------- the planning cycle
class Plan:
    pass


def load_plan(pack):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(pack, "planning_cycle_2027_base_case.xlsx"), data_only=True)
    P = Plan()
    z = [r for r in wb["Zero curve"].iter_rows(min_row=2, values_only=True) if r[0] is not None]
    P.tenors = [float(r[0]) for r in z]
    P.zeros = [float(r[1]) for r in z]
    pr = [r for r in wb["Product rates"].iter_rows(min_row=2, values_only=True) if r[0] is not None]
    P.mortgage = float(pr[-1][1])
    P.conf15 = float(pr[-1][2])
    P.cre = float(pr[-1][3])
    P.path = {ordinal(r[0]): (float(r[1]), float(r[2]), float(r[3])) for r in pr}
    return P


def weights(P, shift=0.02):
    """for a cash flow j months after a month-end: base discount factor less the shifted one"""
    t = np.arange(1, HORIZON + 1) / 12.0
    z = np.interp(t, P.tenors, P.zeros) / 100.0
    return np.exp(-z * t) - np.exp(-(z + shift) * t)


def measure(C, W, months=None):
    """the policy's loss averaged over the twelve month-ends of 2027; C[0] is December 2026"""
    C = np.asarray(C, float)
    vals = []
    for m in (months or MEASURE):
        k = m - START                  # index of month m in C; cash after it starts at k+1
        tail = C[k + 1:]
        vals.append(float((tail * W[:len(tail)]).sum()))
    return float(np.mean(vals)), vals


# ------------------------------------------------------------------------------------------------- rate sheets
def load_rates(pack):
    rows = read_csv(os.path.join(pack, "rate_sheet_archive.csv"))
    old = {"JMB30": "J30F", "JMB15": "J15F", "CNF30": "C30F", "CNF15": "C15F", "CRE5": "CRE5F"}
    acc = {}
    for r in rows:
        code = old.get(r["product_code"], r["product_code"])
        d = pdate(r["sheet_date"])
        acc.setdefault((code, ordinal(d)), []).append(float(r["rate"]))
    return {k: float(np.mean(v)) for k, v in acc.items()}


# ------------------------------------------------------------------------------------------------- level-pay projection
def level_pay(bal, rate, nrem, smm, curt=0.0, H=HORIZON):
    """aggregate cash flows of level-payment loans (30/360 monthly interest); smm: array [n, H] or [H] or scalar"""
    bal = np.asarray(bal, float).copy()
    r = np.asarray(rate, float) / 1200.0
    n = np.asarray(nrem, float).copy()
    smm = np.broadcast_to(np.asarray(smm, float), (H,) if np.ndim(smm) <= 1 else np.shape(smm)) \
        if np.ndim(smm) <= 1 else np.asarray(smm, float)
    C = np.zeros(H)
    for t in range(H):
        alive = (n > 0) & (bal > 0.005)
        if not alive.any():
            break
        pay = np.where(alive, bal * r / (1 - (1 + r) ** (-np.maximum(n, 1))), 0.0)
        intr = np.where(alive, bal * r, 0.0)
        sched = np.where(n <= 1, bal, np.minimum(pay - intr, bal))
        sched = np.where(alive, sched, 0.0)
        s = smm[:, t] if np.ndim(smm) == 2 else (smm[t] if np.ndim(smm) == 1 else smm)
        pre = (bal - sched) * np.minimum(1.0, s + curt)
        C[t] = float((intr + sched + pre).sum())
        bal = bal - sched - pre
        n -= 1
    return C


# ------------------------------------------------------------------------------------------------- Treasury ladder
def load_custody(pack):
    return read_csv(os.path.join(pack, "custody_holdings_20261130.csv"))


def treasury_cf(cust):
    C = np.zeros(HORIZON)
    par_total = 0.0
    for r in cust:
        if r["security_type"] != "UST":
            continue
        par = float(r["current_face"]) * 1000.0
        par_total += par
        cpn = float(r["coupon"])
        md = pdate(r["maturity_date"])
        mm = ordinal(md)
        o = mm
        while o > ASOF:
            C[o - START] += par * cpn / 200.0
            o -= 6
        C[mm - START] += par
    return C, par_total


# ------------------------------------------------------------------------------------------------- agency MBS
def load_factors(pack):
    out = {}
    for r in read_csv(os.path.join(pack, "agency_pool_factors.csv")):
        y, m = r["factor_month"].split("-")
        out.setdefault(r["pool_number"], {})[mo(int(y), int(m))] = (float(r["pool_factor"]), float(r["wac"]),
                                                                    int(r["wam"]))
    return out


def mbs_pools(cust):
    return [r for r in cust if r["security_type"] == "AGENCY MBS" and pdate(r["acquisition_date"]).year in (2020, 2021)]


def mbs_smm(fac, months):
    """monthly prepayment rates of one pool from its factors: the drop beyond the scheduled amortisation"""
    out = {}
    for o in months:
        if o not in fac or o - 1 not in fac:
            continue
        f0, wac, wam0 = fac[o - 1]
        f1 = fac[o][0]
        r = wac / 1200.0
        n = wam0                                   # remaining term after the earlier month's payment
        sched_ratio = ((1 + r) ** n - (1 + r)) / ((1 + r) ** n - 1)
        out[o] = 1.0 - (f1 / f0) / sched_ratio
    return out


def mbs_cf(cust, factors, smm_rule="trailing12", delay=1):
    C = np.zeros(HORIZON)
    face = 0.0
    for r in mbs_pools(cust):
        pn = r["pool_number"]
        fac = factors[pn]
        cf_now = float(r["current_face"]) * 1000.0
        face += cf_now
        f_last, wac, wam = fac[ASOF]
        cpn = float(r["coupon"])
        if smm_rule == "trailing12":
            sm = mbs_smm(fac, range(ASOF - 11, ASOF + 1))
            s = float(np.mean(list(sm.values())))
        elif smm_rule == "life":
            sm = mbs_smm(fac, range(min(fac) + 1, ASOF + 1))
            s = float(np.mean(list(sm.values())))
        else:
            s = float(smm_rule)
        B = cf_now
        n = wam
        rr = wac / 1200.0
        for t in range(HORIZON - delay):
            if n <= 0 or B <= 0.01:
                break
            pay = B * rr / (1 - (1 + rr) ** (-n))
            sched = B if n <= 1 else min(pay - B * rr, B)
            pre = (B - sched) * s
            C[t + delay] += B * cpn / 1200.0 + sched + pre
            B -= sched + pre
            n -= 1
    return C, face


# ------------------------------------------------------------------------------------------------- 2023-24 mortgages
class Mort:
    pass


def load_mortgages(pack):
    leg = read_csv(os.path.join(pack, "servicing_monthly_legacy_2023-01_2024-08.csv"))
    new = read_csv(os.path.join(pack, "servicing_monthly_2024-09_2026-11.csv"))
    xref = {r["legacy_loan_no"]: r["loan_id"] for r in read_csv(os.path.join(pack, "servicing_conversion_xref.csv"))}
    rows = []
    for r in leg:
        if r["LOAN_NO"] == "TRL" or r["PORTF"] != "PORT":
            continue
        lid = xref.get(r["LOAN_NO"], "L" + r["LOAN_NO"])
        cyc = r["CYCLE"]
        o = mo(int(cyc[:4]), int(cyc[4:]))
        rows.append((lid, o, pdate(r["ORIG_DT"]), int(r["TERM"]), float(r["NOTE_RT"]), float(r["BEG_PRIN"]),
                     float(r["SCHED_PRIN"]), float(r["CURTAIL"]), float(r["PIF_PRIN"]), float(r["END_PRIN"]),
                     1 if r["STAT"] == "P" else 2 if r["STAT"] == "S" else 0))
    for r in new:
        if r["investor_type"] != "PORTFOLIO":
            continue
        y, m = r["reporting_period"].split("-")
        o = mo(int(y), int(m))
        st = 0
        unsch = float(r["unscheduled_principal"])
        pif = 0.0
        curt = unsch
        if r["zero_balance_code"] == "01":
            st, pif, curt = 1, unsch, 0.0
        elif r["zero_balance_code"] == "15":
            st, pif, curt = 2, unsch, 0.0
        rows.append((r["loan_id"], o, pdate(r["origination_date"]), int(r["original_term_months"]),
                     float(r["interest_rate"]) * 100.0, float(r["beginning_principal"]), float(r["scheduled_principal"]),
                     curt, pif, float(r["ending_principal"]), st))
    M = Mort()
    M.rows = rows
    return M


def mortgage_panel(M, rates, lag=1):
    """loan-months exposed to a full prepayment (sales censored): incentive, calendar month, age, outcome"""
    inc, moy, age, y, w = [], [], [], [], []
    for (lid, o, od, term, note, beg, sched, curt, pif, end, st) in M.rows:
        if st == 2:
            continue
        rate = rates.get(("J30F", o - lag))
        if rate is None:
            continue
        inc.append((note - rate) / 100.0)
        moy.append(ym(o)[1])
        age.append(o - ordinal(od))
        y.append(1.0 if st == 1 else 0.0)
    return np.array(inc), np.array(moy), np.array(age, float), np.array(y)


def smm_model(theta, inc, moy, age):
    turn = math.exp(theta[0])
    season = np.exp(np.concatenate([[0.0], theta[1:12]]))
    season = season / season.mean()
    b = 1.0 / (1.0 + math.exp(-theta[12]))
    ramp = np.minimum(1.0, b + (1 - b) * age / 12.0)
    refi = math.exp(theta[13]) / (1.0 + np.exp(-(inc - theta[14]) / math.exp(theta[15])))
    return turn * season[moy - 1] * ramp + refi


def fit_mortgage(inc, moy, age, y):
    def nll(th):
        p = np.clip(smm_model(th, inc, moy, age), 1e-7, 0.5)
        return -float(np.sum(y * np.log(p) + (1 - y) * np.log1p(-p)))
    th0 = np.array([math.log(0.004)] + [0.0] * 11 + [0.0, math.log(0.04), 0.006, math.log(0.002)])
    res = minimize(nll, th0, method="L-BFGS-B", options=dict(maxiter=4000))
    return res.x, res.fun


def mortgage_pool(M):
    last = {}
    for row in M.rows:
        if row[1] == ASOF and row[9] > 0.005 and row[10] == 0:
            last[row[0]] = row
    out = []
    for lid, (lid_, o, od, term, note, beg, sched, curt, pif, end, st) in sorted(last.items()):
        out.append((lid, end, note, term - (ASOF - ordinal(od)), ASOF - ordinal(od)))
    return out


def curtail_rate(M, months=12):
    num = den = 0.0
    for (lid, o, od, term, note, beg, sched, curt, pif, end, st) in M.rows:
        if o > ASOF - months and st == 0:
            num += curt
            den += beg - sched
    return num / den


def mortgage_cf(pool, smm, curt):
    bal = np.array([p[1] for p in pool])
    note = np.array([p[2] for p in pool])
    nrem = np.array([p[3] for p in pool])
    return level_pay(bal, note, nrem, smm, curt)


def mortgage_smm_plan(theta, pool, plan_rate):
    note = np.array([p[2] for p in pool])
    age0 = np.array([p[4] for p in pool], float)
    S = np.zeros((len(pool), HORIZON))
    for t in range(HORIZON):
        o = START + t
        S[:, t] = smm_model(theta, (note - plan_rate) / 100.0, np.full(len(pool), ym(o)[1]), age0 + t + 1)
    return S


def pooled_smm(M, first, last):
    num = den = 0.0
    for (lid, o, od, term, note, beg, sched, curt, pif, end, st) in M.rows:
        if first <= o <= last and st != 2:
            num += pif
            den += beg - sched
    return num / den


# ------------------------------------------------------------------------------------------------- CRE
class Cre:
    pass


def load_cre(pack):
    from openpyxl import load_workbook
    C = Cre()
    C.pos = [r for r in read_csv(os.path.join(pack, "cre_term_loans_20261130.csv"))]
    st = {}
    for r in read_csv(os.path.join(pack, "cre_operating_statements.csv")):
        st.setdefault(r["property_number"], []).append((pdate(r["fiscal_year_end"]), float(r["net_operating_income"]),
                                                        pdate(r["review_completed"])))
    for k in st:
        st[k].sort(key=lambda x: (x[2], x[0]))
    C.stmts = st
    wb = load_workbook(os.path.join(pack, "cre_maturity_log.xlsx"), data_only=True)
    log = []
    code = {"PO": "PAID", "Paid at maturity": "PAID", "EXT": "EXTENDED", "Extended": "EXTENDED",
            "PO-EXT": "PAID_EXT", "Paid at extended maturity": "PAID_EXT"}
    ptype = {"MF": "Multifamily", "OFF": "Office", "RTL": "Retail", "IND": "Industrial", "MXD": "Mixed use"}
    for ws in wb.worksheets:
        for r in ws.iter_rows(min_row=2, values_only=True):
            if r[0] is None:
                continue
            d = r[5]
            if isinstance(d, dt.datetime):
                d = d.date()
            elif not isinstance(d, dt.date):
                d = pdate(str(d))
            log.append(dict(ob=str(r[0]), prop="P%05d" % int(str(r[1]).strip()), ptype=ptype.get(r[2], r[2]),
                            b0=float(r[3]), rate=float(r[4]), date=d, bal=float(r[6]), out=code[str(r[7]).strip()]))
    C.log = log
    return C


def stmt_before(C, prop, when, strict=True):
    s = [x for x in C.stmts.get(prop, []) if (x[2] < when if strict else x[2] <= when)]
    return s[-1][1] if s else None


def dconst(rate, n=300):
    r = rate / 1200.0
    return 12 * r / (1 - (1 + r) ** (-n))


def cre_history(C, rates, refi_lag=0, amort=300):
    """every original maturity since 2015 with its outcome and the covariates the routes use"""
    pos = {}
    for r in C.pos:
        pos[r["obligor_number"] + "-" + r["loan_number"][-2:]] = r
    H = []
    for e in C.log:
        if e["out"] == "PAID_EXT":
            continue
        noi = stmt_before(C, e["prop"], e["date"])
        refi = rates.get(("CRE5F", ordinal(e["date"]) - refi_lag), rates[("CRE5F", ordinal(e["date"]))])
        H.append(dict(ob=e["ob"], prop=e["prop"], date=e["date"], bal=e["bal"], y=1.0 if e["out"] == "EXTENDED" else 0.0,
                      noi=noi, refi=refi, cover=noi / (e["bal"] * dconst(refi, amort)), dy=noi / e["bal"],
                      gap=refi - e["rate"], cur=noi / (e["b0"] * dconst(e["rate"], 300)), ptype=e["ptype"],
                      rate=e["rate"]))
    return H


def logit_fit(X, y):
    X = np.column_stack([np.ones(len(X)), np.atleast_2d(np.asarray(X, float).T).T if np.ndim(X) > 1 else X])
    def nll(b):
        z = X @ b
        return float(np.sum(np.logaddexp(0, z) - y * z))
    def grad(b):
        z = X @ b
        p = 1 / (1 + np.exp(-z))
        return X.T @ (p - y)
    return minimize(nll, np.zeros(X.shape[1]), jac=grad, method="BFGS").x


def logit_pred(b, X):
    X = np.column_stack([np.ones(len(X)), X])
    return 1 / (1 + np.exp(-(X @ b)))


def cre_loans(C):
    """the fixed-rate pool: each loan's terms, its scheduled run, its balloon at the original and current maturity"""
    out = []
    for r in C.pos:
        if r["rate_type"] != "FIXED":
            continue
        L = dict(prop=r["property_number"], rate=float(r["note_rate"]), basis=r["interest_basis"],
                 bal=float(r["principal_balance"]), pay=float(r["monthly_payment"]),
                 omat=pdate(r["original_maturity_date"]), mat=pdate(r["maturity_date"]), orig=pdate(r["origination_date"]),
                 amort=int(r["amortization_months"]), b0=float(r["original_principal"]), ptype=r["property_type"])
        L["extended"] = L["mat"] != L["omat"]
        out.append(L)
    return out


def run_sched(L, months):
    """balance path and interest from December 2026 for the given number of months on the loan's payment"""
    B = L["bal"]
    bals, ints = [], []
    for k in range(months):
        o = START + k
        days = month_days(o - 1) if L["basis"] == "ACT/360" else 30
        it = B * L["rate"] / 100.0 * days / 360.0
        pr = min(L["pay"] - it, B)
        B -= pr
        bals.append(B)
        ints.append(it)
    return bals, ints


def cre_cf(loans, pfun, ext_months=36):
    """expected cash flows: payments to maturity; at the original maturity the balloon repays with probability 1-p
    and with p the loan runs ext_months more on its payment and repays then; extended loans repay at their date"""
    Cf = np.zeros(HORIZON)
    for L in loans:
        mat_o = ordinal(L["mat"])
        p = 0.0 if L["extended"] else float(pfun(L))
        last = mat_o + (ext_months if (p > 0) else 0)
        n = last - ASOF
        bals, ints = run_sched(L, n)
        prev = L["bal"]
        for k in range(n):
            o = START + k
            sched = prev - bals[k]
            if o < mat_o:
                Cf[k] += ints[k] + sched
            elif o == mat_o:
                Cf[k] += ints[k] + sched + (1 - p) * bals[k]
            elif o < last:
                Cf[k] += p * (ints[k] + sched)
            else:
                Cf[k] += p * (ints[k] + sched + bals[k])
            prev = bals[k]
    return Cf


def balloon(L):
    n = ordinal(L["omat"]) - ASOF
    bals, _ = run_sched(L, n)
    return bals[-1]


def cre_cover_now(C, L, rate, amort=300):
    noi = stmt_before(C, L["prop"], dt.date(2026, 12, 3), strict=False)
    return noi / (balloon(L) * dconst(rate, amort))


# ------------------------------------------------------------------------------------------------- auto
def load_auto(pack):
    tape = read_csv(os.path.join(pack, "indirect_auto_tape_20261130.csv"))
    roll = read_csv(os.path.join(pack, "indirect_auto_monthly_roll.csv"))
    return tape, roll


def auto_smm(roll, months=12):
    rs = roll[-months:]
    num = sum(float(r["prepaid_principal"]) for r in rs)
    den = sum(float(r["beginning_principal"]) - float(r["scheduled_principal"]) for r in rs)
    return num / den


def auto_cf(tape, smm):
    bal = np.array([float(r["principal_balance"]) for r in tape])
    apr = np.array([float(r["apr"]) for r in tape])
    nrem = np.array([int(r["term_months"]) - (ASOF - ordinal(pdate(r["contract_date"]))) for r in tape])
    return level_pay(bal, apr, nrem, smm)


# ------------------------------------------------------------------------------------------------- the whole golden
class Result:
    pass


def golden(pack, verbose=False):
    G = Result()
    P = load_plan(pack)
    G.plan = P
    W = weights(P)
    G.W = W
    rates = load_rates(pack)
    G.rates = rates
    cust = load_custody(pack)
    factors = load_factors(pack)
    # Treasury ladder
    Ct, G.par_T = treasury_cf(cust)
    G.T, _ = measure(Ct, W)
    # agency MBS
    Cm, G.face_MBS = mbs_cf(cust, factors)
    G.MBS, _ = measure(Cm, W)
    # 2023-24 mortgages
    M = load_mortgages(pack)
    inc, moy, age, y = mortgage_panel(M, rates)
    G.m_theta, _ = fit_mortgage(inc, moy, age, y)
    pool = mortgage_pool(M)
    G.m_pool = pool
    G.bal_M = sum(p[1] for p in pool)
    curt = curtail_rate(M)
    G.m_curt = curt
    S_plan = mortgage_smm_plan(G.m_theta, pool, P.mortgage)
    G.m_cf = mortgage_cf(pool, S_plan, curt)
    G.M, _ = measure(G.m_cf, W)
    bal = np.array([p[1] for p in pool])
    G.m_cpr_2027 = 1 - (1 - float((S_plan[:, 1:13].mean(axis=1) * bal).sum() / bal.sum())) ** 12
    # trailing-year speed (rung 0)
    s12 = pooled_smm(M, ASOF - 11, ASOF)
    G.m_smm_trailing = s12
    G.M_trailing, _ = measure(mortgage_cf(pool, s12, curt), W)
    # indirect auto
    tape, roll = load_auto(pack)
    G.bal_AUTO = sum(float(r["principal_balance"]) for r in tape)
    G.auto_smm = auto_smm(roll)
    G.AUTO, _ = measure(auto_cf(tape, G.auto_smm), W)
    # fixed-rate CRE
    C = load_cre(pack)
    G.cre = C
    loans = cre_loans(C)
    G.cre_loans = loans
    G.bal_CRE = sum(L["bal"] for L in loans)
    H = cre_history(C, rates)
    G.cre_hist = H
    X = np.array([h["cover"] for h in H])
    yy = np.array([h["y"] for h in H])
    G.cover_beta = logit_fit(X, yy)
    covers = {id(L): cre_cover_now(C, L, P.cre) for L in loans if not L["extended"]}
    G.cre_cover = covers

    def p_cover(L):
        return float(logit_pred(G.cover_beta, np.array([covers[id(L)]]))[0])
    G.cre_cf = cre_cf(loans, p_cover)
    G.CRE, _ = measure(G.cre_cf, W)
    G.CRE_contractual, _ = measure(cre_cf(loans, lambda L: 0.0), W)
    # the 2027 balloons: December 2026 to December 2027
    wall = [L for L in loans if not L["extended"] and ASOF < ordinal(L["omat"]) <= mo(2027, 12)]
    G.wall = wall
    bw = np.array([balloon(L) for L in wall])
    pw = np.array([p_cover(L) for L in wall])
    G.wall_balloon = float(bw.sum())
    G.wall_share = float((pw * bw).sum() / bw.sum())
    G.wall_extended = float((pw * bw).sum())
    G.pools = {"Treasury ladder": G.T, "Agency MBS": G.MBS, "2023-24 residential mortgages": G.M,
               "Indirect auto loans": G.AUTO, "Fixed-rate commercial real estate": G.CRE}
    G.principal = {"Treasury ladder": G.par_T, "Agency MBS": G.face_MBS, "2023-24 residential mortgages": G.bal_M,
                   "Indirect auto loans": G.bal_AUTO, "Fixed-rate commercial real estate": G.bal_CRE}
    G.call = max(G.pools, key=G.pools.get)
    if verbose:
        for k, v in G.pools.items():
            print("  %-36s principal %8.1fm  loss %7.2fm" % (k, G.principal[k] / 1e6, v / 1e6))
        print("  call:", G.call)
    return G


# ------------------------------------------------------------------------------------------------- the hedge programme (Ask A)
QUARTER_ENDS = [dt.date(2027, 3, 31), dt.date(2027, 6, 30), dt.date(2027, 9, 30), dt.date(2027, 12, 31)]
OVERLAY = dict(notional=1_200_000_000.0, eff=dt.date(2027, 1, 4), mat=dt.date(2031, 1, 6))
FUNDING_WORDS = ("certificates of deposit", "home loan bank advances", "advances")


def load_register(pack):
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(pack, "swap_register_20261130.xlsx"), data_only=True)
    ws = wb["Trades"]
    head = [c.value for c in ws[1]]
    out = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if r[0] is None:
            continue
        d = dict(zip(head, r))
        for k in ("Trade date", "Effective date", "Maturity date"):
            v = d[k]
            d[k] = v.date() if isinstance(v, dt.datetime) else v
        out.append(d)
    return out


def load_schedules(pack):
    s = {}
    for r in read_csv(os.path.join(pack, "swap_amortisation_schedules.csv")):
        s.setdefault(str(r["trade_number"]), []).append((pdate(r["period_start"]), pdate(r["period_end"]),
                                                         float(r["notional"])))
    return s


def load_clearing(pack):
    return read_csv(os.path.join(pack, "clearing_statement_20261130.csv"))


def programme_category(t):
    if t["Bank pays"] == "FLOAT":
        return "loan"
    item = (t["Hedged item"] or "").lower()
    return "funding" if any(w in item for w in FUNDING_WORDS) else "overlay"


def notional_in_effect(t, d, sched):
    if not (t["Effective date"] <= d < t["Maturity date"]):
        return 0.0
    rows = sched.get(str(t["Trade No."]))
    if rows:
        for a, b, n in rows:
            if a <= d < b:
                return n
        return 0.0
    return float(t["Notional (USD)"])


def programme(pack, read_backload=True, by="item", dedupe_terms=False, include_overlay=True):
    """the hedge programme's notional in effect at each 2027 quarter-end by part. read_backload: a live bilateral
    trade whose number the clearing broker holds as the client reference of a different cleared trade has been
    backloaded into clearing, and only the cleared trade is live. by: 'item' classifies pay-fixed swaps by what they
    are designated against, 'strategy' by the register's strategy code."""
    reg = load_register(pack)
    sched = load_schedules(pack)
    clr = load_clearing(pack)
    live = [t for t in reg if t["Book"] == "ALM" and t["Status"] == "LIVE"]
    if read_backload:
        held = {}
        for c in clr:
            held[c["client_trade_ref"]] = c["ccp_trade_id"]
        by_ccp = {str(t["Clearing ref"]): t for t in reg if t["Clearing ref"]}
        gone = set()
        for t in live:
            if t["Cleared"] == "N" and str(t["Trade No."]) in held:
                ct = by_ccp.get(held[str(t["Trade No."])])
                if ct is not None and ct["Trade No."] != t["Trade No."]:
                    gone.add(t["Trade No."])
        live = [t for t in live if t["Trade No."] not in gone]
    if dedupe_terms:
        seen, keep = set(), []
        for t in live:
            k = (t["Bank pays"], round(float(t["Notional (USD)"])), t["Effective date"], t["Maturity date"],
                 round(float(t["Fixed rate (%)"]), 4))
            if k in seen:
                continue
            seen.add(k)
            keep.append(t)
        live = keep
    out = {"overlay": [], "funding": [], "loan": []}
    for d in QUARTER_ENDS:
        tot = {"overlay": 0.0, "funding": 0.0, "loan": 0.0}
        for t in live:
            if by == "item":
                c = programme_category(t)
            else:
                c = "loan" if t["Bank pays"] == "FLOAT" else ("overlay" if t["Strategy"] == "OVERLAY" else "funding")
            tot[c] += notional_in_effect(t, d, sched)
        if include_overlay and OVERLAY["eff"] <= d < OVERLAY["mat"]:
            tot["overlay"] += OVERLAY["notional"]
        for c in tot:
            out[c].append(tot[c])
    return out


# ------------------------------------------------------------------------------------------------- out of sample
def oos_table(G, split=dt.date(2024, 12, 31)):
    """fit each extension route on the maturities to the end of 2024 and score it on 2025 and 2026 (Brier)"""
    H = G.cre_hist
    y = np.array([h["y"] for h in H])
    tr = np.array([h["date"] <= split for h in H])
    te = ~tr
    out = {}
    for nm in ("cover", "gap", "cur", "dy"):
        x = np.array([h[nm] for h in H])
        b = logit_fit(x[tr], y[tr])
        p = logit_pred(b, x[te])
        out[nm] = round(float(np.mean((p - y[te]) ** 2)), 5)
    rec = tr & np.array([h["date"] > dt.date(split.year - 1, 12, 31) for h in H])
    out["last_year_share"] = round(float(np.mean((y[rec].mean() - y[te]) ** 2)), 5)
    out["pooled_share"] = round(float(np.mean((y[tr].mean() - y[te]) ** 2)), 5)
    out["n_test"] = int(te.sum())
    out["n_train"] = int(tr.sum())
    return out


# ------------------------------------------------------------------------------------------------- rungs, rivals, family
def _fit_route(H, feat_h, sel=None):
    y = np.array([h["y"] for h in H])
    x = np.array([feat_h(h) for h in H])
    if sel is not None:
        x, y = x[sel], y[sel]
    return logit_fit(x, y)


GUESSES = [("one half", 0.5), ("three-fifths", 0.6), ("two-thirds", 2 / 3), ("0.7", 0.7), ("three-quarters", 0.75),
           ("four-fifths", 0.8), ("0.85", 0.85), ("nine-tenths", 0.9), ("all", 1.0)]
CUTS = [round(0.90 + 0.01 * i, 2) for i in range(46)]


def cre_linear(G):
    """the pool's averaged loss is linear in each future balloon's extension probability: the extended loans' part,
    and for every loan not yet extended its loss repaid when due (m0) and the change if it extends (d), in dollars"""
    if getattr(G, "_lin", None) is None:
        loans = G.cre_loans
        fut = [L for L in loans if not L["extended"]]
        base = measure(cre_cf([L for L in loans if L["extended"]], lambda L: 0.0), G.W)[0]
        m0 = np.array([measure(cre_cf([L], lambda L: 0.0), G.W)[0] for L in fut])
        m1 = np.array([measure(cre_cf([L], lambda L: 1.0), G.W)[0] for L in fut])
        G._lin = (fut, base, m0, m1 - m0)
    return G._lin


def cre_total(G, p):
    fut, base, m0, d = cre_linear(G)
    return float(base + (m0 + np.asarray(p, float) * d).sum()) / 1e6


def routes(G):
    """every extension construction: the probability rule it fits on the closed maturities, the pool's averaged loss
    it files ($ millions) and its hold-out Brier score (refitted on the maturities to December 2024 and scored on the
    2025 and 2026 maturities); the golden family, the routes kept outside the bin, the ladder's rivals and the
    constant-share guesses"""
    P, W, loans, H, C_ = G.plan, G.W, G.cre_loans, G.cre_hist, G.cre
    fut = cre_linear(G)[0]
    cov = np.array([G.cre_cover[id(L)] for L in fut])
    noi = np.array([stmt_before(C_, L["prop"], dt.date(2026, 12, 3), strict=False) for L in fut])
    bal = np.array([balloon(L) for L in fut])
    dy_now = noi / bal
    cur_now = noi / np.array([L["pay"] * 12 for L in fut])
    gap_now = np.array([P.cre - L["rate"] for L in fut])
    wall = np.array([ordinal(L["omat"]) <= mo(2027, 12) for L in fut])
    yrs = np.array([max(0.0, (ordinal(L["omat"]) - ASOF) / 12.0) for L in fut])
    y = np.array([h["y"] for h in H])
    since23 = np.array([h["date"] >= dt.date(2023, 1, 1) for h in H])
    rec = np.array([h["date"] > dt.date(2025, 11, 30) for h in H])
    tr = np.array([h["date"] <= dt.date(2024, 12, 31) for h in H])
    te = ~tr
    xs = np.array([h["cover"] for h in H])
    feats = {k: np.array([h[k] for h in H]) for k in ("cover", "dy", "cur", "gap")}

    def brier(p):
        return float(np.mean((np.asarray(p, float) - y[te]) ** 2))

    def logit_route(xh, xf, sel=None):
        s_ = np.ones(len(H), bool) if sel is None else sel
        b = logit_fit(xh[s_], y[s_])
        bt = logit_fit(xh[s_ & tr], y[s_ & tr])
        return logit_pred(b, xf), brier(logit_pred(bt, xh[te]))

    def bands(width, first):
        e = np.concatenate([[-np.inf], np.round(np.arange(first, 1.80, width), 3), [np.inf]])

        def shares(sel):
            sh = []
            for lo, hi in zip(e[:-1], e[1:]):
                s_ = sel & (xs >= lo) & (xs < hi)
                sh.append(float(y[s_].mean()) if s_.sum() else float("nan"))
            for i in range(len(sh)):
                if sh[i] != sh[i]:
                    sh[i] = sh[i - 1] if i else 1.0
            return np.array(sh)
        idx = lambda v: np.minimum(np.searchsorted(e, v, side="right") - 1, len(e) - 2)
        return shares(np.ones(len(H), bool))[idx(cov)], brier(shares(tr)[idx(xs[te])])
    F, O, S = {}, {}, {}
    pg = logit_pred(G.cover_beta, cov)
    F["cover, every maturity since 2015"] = pg
    S["cover, every maturity since 2015"] = logit_route(xs, cov)[1]
    F["cover, maturities since 2023"], S["cover, maturities since 2023"] = logit_route(xs, cov, since23)
    F["log cover"], S["log cover"] = logit_route(np.log(xs), np.log(cov))
    for w_, first, nm in ((0.05, 0.70, "cover bands of 0.05"), (0.05, 0.725, "cover bands of 0.05, offset"),
                          (0.10, 0.70, "cover bands of 0.10"), (0.10, 0.75, "cover bands of 0.10, offset")):
        F[nm], S[nm] = bands(w_, first)
    cut_te = {c: brier((xs[te] < c).astype(float)) for c in CUTS}
    cut_in = {c: float(np.mean(((xs < c).astype(float) - y) ** 2)) for c in CUTS}
    bt_, bi_ = min(cut_te.values()), min(cut_in.values())
    chosen = sorted(set(c for c in CUTS if cut_te[c] <= 1.1 * bt_ + 1e-12) | set(c for c in CUTS if cut_in[c] <= 1.1 * bi_ + 1e-12))
    for c in chosen:
        F["hard cut at %.2f" % c] = (cov < c).astype(float)
        S["hard cut at %.2f" % c] = cut_te[c]
    F["debt yield, maturities since 2023"], S["debt yield, maturities since 2023"] = logit_route(feats["dy"], dy_now, since23)
    X2 = np.column_stack([feats["dy"], [h["refi"] for h in H]])
    b2, b2t = logit_fit(X2, y), logit_fit(X2[tr], y[tr])
    F["debt yield and the refinance rate"] = logit_pred(b2, np.column_stack([dy_now, np.full(len(fut), P.cre)]))
    S["debt yield and the refinance rate"] = brier(logit_pred(b2t, X2[te]))
    F["cover, the 2027 balloons only"] = np.where(wall, pg, 0.0)
    S["cover, the 2027 balloons only"] = S["cover, every maturity since 2015"]
    Hf = cre_history(C_, G.rates, refi_lag=1)
    xl = np.array([h["cover"] for h in Hf])
    F["refinance rate a month before maturity"], S["refinance rate a month before maturity"] = logit_route(xl, cov)

    def stmt_fy(prop, when):
        s_ = [x for x in C_.stmts.get(prop, []) if x[0] < when]
        s_.sort(key=lambda x: x[0])
        return s_[-1][1] if s_ else None
    xfy = np.array([stmt_fy(h["prop"], h["date"]) / (h["bal"] * dconst(h["refi"])) for h in H])
    F["statement by fiscal year end"], S["statement by fiscal year end"] = logit_route(xfy, cov)
    X3 = np.column_stack([xs, feats["gap"]])
    b3, b3t = logit_fit(X3, y), logit_fit(X3[tr], y[tr])
    F["cover and rate gap"] = logit_pred(b3, np.column_stack([cov, gap_now]))
    S["cover and rate gap"] = brier(logit_pred(b3t, X3[te]))
    F["income trended at -2 per cent a year"] = logit_pred(G.cover_beta, cov * 0.98 ** yrs)
    S["income trended at -2 per cent a year"] = S["cover, every maturity since 2015"]
    fam = {k: cre_total(G, v) for k, v in F.items()}
    loans360 = [dict(L, basis="30/360") for L in loans]
    fam["interest on 30/360"] = measure(cre_cf(loans360, lambda L: float(logit_pred(G.cover_beta, np.array(
        [cre_cover_now(C_, L, P.cre)]))[0])), W)[0] / 1e6
    S["interest on 30/360"] = S["cover, every maturity since 2015"]
    # the routes the bin must not hold
    O["the 1.25 cover convention"] = (cov < 1.25).astype(float)
    S["the 1.25 cover convention"] = cut_te[1.25]
    O["the 1.00 cover rule"] = (cov < 1.00).astype(float)
    S["the 1.00 cover rule"] = cut_te[1.0]
    O["note-rate DSCR, every maturity"], S["note-rate DSCR, every maturity"] = logit_route(feats["cur"], cur_now)
    O["note-rate DSCR, maturities since 2023"], S["note-rate DSCR, maturities since 2023"] = logit_route(feats["cur"], cur_now, since23)
    O["debt yield, every maturity"], S["debt yield, every maturity"] = logit_route(feats["dy"], dy_now)
    O["rate gap, every maturity"], S["rate gap, every maturity"] = logit_route(feats["gap"], gap_now)
    O["rate gap, maturities since 2023"], S["rate gap, maturities since 2023"] = logit_route(feats["gap"], gap_now, since23)
    wb = bal * wall
    ws = float((wb * pg).sum() / wb.sum())
    O["the 2027 model share carried to every balloon"] = np.full(len(fut), ws)
    O["every balloon extended"] = np.ones(len(fut))
    S["every balloon extended"] = brier(np.ones(te.sum()))
    O["every 2027 balloon extended"] = wall.astype(float)
    O["the last twelve months' share"] = np.full(len(fut), float(y[rec].mean()))
    S["the last twelve months' share"] = brier(np.full(te.sum(), y[tr & np.array([h["date"] > dt.date(2023, 12, 31) for h in H])].mean()))
    O["the share since 2023"] = np.full(len(fut), float(y[since23].mean()))
    S["the share since 2023"] = brier(np.full(te.sum(), y[since23 & tr].mean()))
    O["the pooled share"] = np.full(len(fut), float(y.mean()))
    S["the pooled share"] = brier(np.full(te.sum(), y[tr].mean()))
    pt = {}
    for t in set(h["ptype"] for h in H):
        s_ = np.array([h["ptype"] == t for h in H]) & since23
        pt[t] = float(y[s_].mean()) if s_.sum() else 0.0
    O["property type shares since 2023"] = np.array([pt.get(L["ptype"], 0.0) for L in fut])
    O["repaid when due"] = np.zeros(len(fut))
    out = {k: cre_total(G, v) for k, v in O.items()}
    M0 = cre_total(G, np.zeros(len(fut)))
    S_all = cre_total(G, np.ones(len(fut))) - M0
    S_wall = cre_total(G, wall.astype(float)) - M0
    guesses = {nm: (M0 + g * S_all, M0 + g * S_wall) for nm, g in GUESSES}
    R = dict(family=fam, outside=out, score=S, chosen_cuts=chosen, cut_holdout=cut_te, cut_insample=cut_in,
             cut_figure={c: cre_total(G, (cov < c).astype(float)) for c in CUTS}, guesses=guesses, M0=M0,
             S_all=S_all, S_wall=S_wall, wall_model_share=ws, recent_share=float(y[rec].mean()))
    # the ladder's names for the rivals
    R["cre_contractual"] = out["repaid when due"]
    R["cre_recent"] = out["the last twelve months' share"]
    R["cre_since2023"] = out["the share since 2023"]
    R["cre_pooled"] = out["the pooled share"]
    R["cre_all_extend"] = out["every balloon extended"]
    R["cre_gap"] = out["rate gap, every maturity"]
    R["cre_gap_2023"] = out["rate gap, maturities since 2023"]
    R["cre_cur"] = out["note-rate DSCR, every maturity"]
    R["cre_cur_2023"] = out["note-rate DSCR, maturities since 2023"]
    R["cre_dy"] = out["debt yield, every maturity"]
    R["cre_ptype"] = out["property type shares since 2023"]
    R["cre_wall_only"] = fam["cover, the 2027 balloons only"]
    return R
