"""Independent verifier for task166: reads only the shipped bundle (no generator module), on its own code path (pandas,
numpy, scipy), and recomputes the designation, the designated pool's loss bin, the default path's answer, the decisive
step's out-of-sample choice and Ask A. It reads every format the pack ships, each with a positive control.

    python3 verify.py <target_dir>"""
from __future__ import annotations

import datetime as dt
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy.optimize import minimize

PACK = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                          "target")
OUT = []


def ok(label, cond, detail=""):
    OUT.append(bool(cond))
    print("%s  %-46s %s" % ("PASS" if cond else "FAIL", label, detail))


def f(name):
    return os.path.join(PACK, name)


def ordm(d):
    return d.year * 12 + d.month - 1


ASOF = 2026 * 12 + 10
FIRST = ASOF + 1
H = 360

# ------------------------------------------------------------------------------------------------- formats, with controls
from pypdf import PdfReader    # noqa: E402
policy = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(f("balance_sheet_hedging_policy.pdf")).pages))
alm = re.sub(r"\s+", " ", " ".join(p.extract_text() for p in PdfReader(f("alm_report_2026_q3.pdf")).pages))
notes = re.sub(r"\s+", " ", open(f("extract_notes.txt"), encoding="utf-8").read())
ok("PDF policy read", "the same zero rates at every month-end" in policy and "before credit losses" in policy,
   "measure sentence and cash flow definition found")
ok("PDF policy Schedule A", all(w in policy for w in ("Treasury ladder", "Agency MBS", "2023-24 residential mortgages",
                                                      "Indirect auto loans", "Fixed-rate commercial real estate")), "")
ok("PDF ALM report read", "77 per cent" in alm and "30 September" in alm, "control phrase found")
ok("TXT notes read", "client_trade_ref" in notes and "36 months" in notes, "")
plan = pd.read_excel(f("planning_cycle_2027_base_case.xlsx"), sheet_name=None)
zc = plan["Zero curve"]
pr = plan["Product rates"]
ok("XLSX planning workbook", len(zc) == 13 and len(pr) == 13, "13 tenors, 13 months")
TEN = zc.iloc[:, 0].astype(float).values
ZER = zc.iloc[:, 1].astype(float).values
MORT, CONF15, CRER = [float(pr.iloc[-1, k]) for k in (1, 2, 3)]
t = np.arange(1, H + 1) / 12
z = np.interp(t, TEN, ZER) / 100
WGT = np.exp(-z * t) - np.exp(-(z + 0.02) * t)


def loss(cf):
    cf = np.asarray(cf, float)
    out = []
    for k in range(1, 13):                      # month-ends of January to December 2027; cf[0] is December 2026
        tail = cf[k + 1:]
        out.append((tail * WGT[:len(tail)]).sum())
    return float(np.mean(out)) / 1e6


def level(bal, rate, n, smm):
    bal = np.array(bal, float)
    r = np.array(rate, float) / 1200
    n = np.array(n, float)
    cf = np.zeros(H)
    for k in range(H):
        a = (n > 0) & (bal > 0.005)
        if not a.any():
            break
        pay = np.where(a, bal * r / (1 - (1 + r) ** (-np.maximum(n, 1))), 0)
        it = np.where(a, bal * r, 0)
        sc = np.where(a, np.where(n <= 1, bal, np.minimum(pay - it, bal)), 0)
        s = smm[:, k] if np.ndim(smm) == 2 else (smm[k] if np.ndim(smm) == 1 else smm)
        pp = (bal - sc) * s
        cf[k] = (it + sc + pp).sum()
        bal = bal - sc - pp
        n = n - 1
    return cf


# rate sheet monthly averages
rs = pd.read_csv(f("rate_sheet_archive.csv"))
rs["code"] = rs["product_code"].replace({"JMB30": "J30F", "JMB15": "J15F", "CNF30": "C30F", "CNF15": "C15F",
                                          "CRE5": "CRE5F"})
rs["m"] = pd.to_datetime(rs["sheet_date"]).map(ordm)
RATE = rs.groupby(["code", "m"])["rate"].mean().to_dict()

# ------------------------------------------------------------------------------------------------- Treasury and MBS
cu = pd.read_csv(f("custody_holdings_20261130.csv"))
ust = cu[cu.security_type == "UST"]
cf_t = np.zeros(H)
for _, r in ust.iterrows():
    par = r.current_face * 1000
    m = ordm(pd.Timestamp(r.maturity_date))
    k = m
    while k > ASOF:
        cf_t[k - FIRST] += par * r.coupon / 200
        k -= 6
    cf_t[m - FIRST] += par
L_T = loss(cf_t)
fa = pd.read_csv(f("agency_pool_factors.csv"))
fa["m"] = fa.factor_month.map(lambda s: int(s[:4]) * 12 + int(s[5:]) - 1)
mbs = cu[(cu.security_type == "AGENCY MBS") & (pd.to_datetime(cu.acquisition_date).dt.year.isin([2020, 2021]))]
cf_m = np.zeros(H)
for _, r in mbs.iterrows():
    g = fa[fa.pool_number == r.pool_number].set_index("m").sort_index()
    sm = []
    for m in range(ASOF - 11, ASOF + 1):
        f0, w0, n0 = g.loc[m - 1, "pool_factor"], g.loc[m - 1, "wac"], g.loc[m - 1, "wam"]
        rr = w0 / 1200
        ratio = ((1 + rr) ** n0 - (1 + rr)) / ((1 + rr) ** n0 - 1)
        sm.append(1 - g.loc[m, "pool_factor"] / f0 / ratio)
    s = np.mean(sm)
    B = r.current_face * 1000
    n = g.loc[ASOF, "wam"]
    rr = g.loc[ASOF, "wac"] / 1200
    for k in range(H - 1):
        if n <= 0 or B < 0.01:
            break
        pay = B * rr / (1 - (1 + rr) ** (-n))
        sc = B if n <= 1 else min(pay - B * rr, B)
        pp = (B - sc) * s
        cf_m[k + 1] += B * r.coupon / 1200 + sc + pp
        B -= sc + pp
        n -= 1
L_MBS = loss(cf_m)

# ------------------------------------------------------------------------------------------------- 2023-24 mortgages
lg = pd.read_csv(f("servicing_monthly_legacy_2023-01_2024-08.csv"), dtype={"LOAN_NO": str, "ORIG_DT": str})
lg = lg[(lg.LOAN_NO != "TRL") & (lg.PORTF == "PORT")]
xr = pd.read_csv(f("servicing_conversion_xref.csv"), dtype=str)
lg["id"] = lg.LOAN_NO.map(dict(zip(xr.legacy_loan_no, xr.loan_id))).fillna("L" + lg.LOAN_NO)
lg["m"] = lg.CYCLE.astype(int).map(lambda c: (c // 100) * 12 + c % 100 - 1)
lg["orig"] = lg.ORIG_DT.map(lambda s: int(s[4:]) * 12 + int(s[:2]) - 1)
lg["note"] = lg.NOTE_RT.astype(float)
lg["pif"] = (lg.STAT == "P").astype(int)
lg["sold"] = (lg.STAT == "S").astype(int)
lg["beg"], lg["sch"], lg["cur"], lg["end"] = lg.BEG_PRIN, lg.SCHED_PRIN, lg.CURTAIL, lg.END_PRIN
nw = pd.read_csv(f("servicing_monthly_2024-09_2026-11.csv"), dtype={"loan_id": str, "zero_balance_code": str})
nw = nw[nw.investor_type == "PORTFOLIO"].copy()
nw["id"] = nw.loan_id
nw["m"] = nw.reporting_period.map(lambda s: int(s[:4]) * 12 + int(s[5:]) - 1)
nw["orig"] = pd.to_datetime(nw.origination_date).map(ordm)
nw["note"] = nw.interest_rate * 100
nw["pif"] = (nw.zero_balance_code == "01").astype(int)
nw["sold"] = (nw.zero_balance_code == "15").astype(int)
nw["beg"], nw["sch"], nw["end"] = nw.beginning_principal, nw.scheduled_principal, nw.ending_principal
nw["cur"] = np.where(nw.pif == 1, 0.0, nw.unscheduled_principal)
cols = ["id", "m", "orig", "note", "pif", "sold", "beg", "sch", "cur", "end"]
mm = pd.concat([lg[cols], nw[cols]])
ok("CSV servicing stacked", mm.groupby(["id", "m"]).size().max() == 1, "%d loan-months, one per loan and month" % len(mm))
pnl = mm[mm.sold == 0].copy()
pnl["rate"] = [RATE.get(("J30F", m - 1)) for m in pnl.m]
pnl = pnl.dropna(subset=["rate"])
inc = ((pnl.note - pnl.rate) / 100).values
moy = (pnl.m % 12).values
age = (pnl.m - pnl.orig).values.astype(float)
y = pnl.pif.values.astype(float)


def smm_f(th, inc, moy, age):
    se = np.exp(np.concatenate([[0.0], th[1:12]]))
    se = se / se.mean()
    b = 1 / (1 + np.exp(-th[12]))
    return np.exp(th[0]) * se[moy] * np.minimum(1, b + (1 - b) * age / 12) + \
        np.exp(th[13]) / (1 + np.exp(-(inc - th[14]) / np.exp(th[15])))


def nll(th):
    p = np.clip(smm_f(th, inc, moy, age), 1e-7, 0.5)
    return -np.sum(y * np.log(p) + (1 - y) * np.log1p(-p))


th = minimize(nll, np.array([np.log(0.004)] + [0.0] * 11 + [0.0, np.log(0.04), 0.006, np.log(0.002)]),
              method="L-BFGS-B", options=dict(maxiter=4000)).x
pool = mm[(mm.m == ASOF) & (mm.end > 0.005) & (mm.sold == 0) & (mm.pif == 0)]
recent = mm[(mm.m > ASOF - 12) & (mm.pif == 0) & (mm.sold == 0)]
curt = recent.cur.sum() / (recent.beg - recent.sch).sum()
note = pool.note.values
age0 = (ASOF - pool.orig).values.astype(float)
S = np.zeros((len(pool), H))
for k in range(H):
    S[:, k] = np.minimum(1, smm_f(th, (note - MORT) / 100, np.full(len(pool), (FIRST + k) % 12), age0 + k + 1) + curt)
nrem = 0
termmap = pd.concat([lg[["id"]].assign(term=lg.TERM), nw[["id"]].assign(term=nw.original_term_months)]).drop_duplicates("id")
tm = dict(zip(termmap.id, termmap.term))
nrem = np.array([tm[i] - (ASOF - o) for i, o in zip(pool.id, pool.orig)])
L_M = loss(level(pool.end.values, note, nrem, S))
tr = mm[(mm.m > ASOF - 12) & (mm.sold == 0)]
s12 = tr.pif.mul(tr.beg - tr.sch).sum() / (tr.beg - tr.sch).sum()
L_M12 = loss(level(pool.end.values, note, nrem, np.full(H, min(1, s12 + curt))))

# ------------------------------------------------------------------------------------------------- auto
tape = pd.read_csv(f("indirect_auto_tape_20261130.csv"))
roll = pd.read_csv(f("indirect_auto_monthly_roll.csv"))
r12 = roll.tail(12)
sa = r12.prepaid_principal.sum() / (r12.beginning_principal - r12.scheduled_principal).sum()
L_A = loss(level(tape.principal_balance.values, tape.apr.values,
                 tape.term_months.values - (ASOF - pd.to_datetime(tape.contract_date).map(ordm).values), np.full(H, sa)))

# ------------------------------------------------------------------------------------------------- CRE
pos = pd.read_csv(f("cre_term_loans_20261130.csv"), dtype={"loan_number": str, "obligor_number": str})
fx = pos[pos.rate_type == "FIXED"].copy()
st = pd.read_csv(f("cre_operating_statements.csv"))
st["fye"] = pd.to_datetime(st.fiscal_year_end)
st["rev"] = pd.to_datetime(st.review_completed)
xl = pd.read_excel(f("cre_maturity_log.xlsx"), sheet_name=None)
logs = []
for name, df in xl.items():
    df = df.copy()
    df.columns = ["ob", "prop", "ptype", "b0", "rate", "date", "bal", "out", "new"]
    logs.append(df)
lgc = pd.concat(logs)
lgc["prop"] = "P" + lgc["prop"].astype(str).str.zfill(5)
lgc["date"] = pd.to_datetime(lgc["date"])
lgc["out"] = lgc["out"].replace({"PO": "PAID", "Paid at maturity": "PAID", "EXT": "EXT", "Extended": "EXT",
                                  "PO-EXT": "PX", "Paid at extended maturity": "PX"})
lgc = lgc[lgc.out != "PX"]
ok("XLSX maturity log", len(lgc) >= 600 and set(lgc.out) == {"PAID", "EXT"}, "%d maturities, %d extended" % (
    len(lgc), (lgc.out == "EXT").sum()))


def dcon(rate, n=300):
    r = rate / 1200
    return 12 * r / (1 - (1 + r) ** (-n))


def latest(prop, before, strict=True):
    s = st[(st.property_number == prop) & ((st.rev < before) if strict else (st.rev <= before))]
    return s.sort_values(["rev", "fye"]).net_operating_income.iloc[-1]


lgc["noi"] = [latest(p, d) for p, d in zip(lgc.prop, lgc.date)]
lgc["refi"] = [RATE[("CRE5F", ordm(d))] for d in lgc.date]
lgc["cover"] = lgc.noi / (lgc.bal * dcon(lgc.refi))
lgc["gap"] = lgc.refi - lgc.rate
lgc["dy"] = lgc.noi / lgc.bal
lgc["dscr"] = lgc.noi / (lgc.b0 * dcon(lgc.rate))
lgc["y"] = (lgc.out == "EXT").astype(float)


def irls(x, y, it=60):
    X = np.column_stack([np.ones(len(x)), x])
    b = np.zeros(2)
    for _ in range(it):
        p = 1 / (1 + np.exp(-(X @ b)))
        w = np.clip(p * (1 - p), 1e-9, None)
        b = b + np.linalg.solve(X.T @ (X * w[:, None]) + 1e-9 * np.eye(2), X.T @ (y - p))
    return b


def pred(b, x):
    return 1 / (1 + np.exp(-(b[0] + b[1] * np.asarray(x, float))))


trn = lgc.date <= "2024-12-31"
brier = {}
for c in ("cover", "gap", "dy", "dscr"):
    b = irls(lgc.loc[trn, c].values, lgc.loc[trn, "y"].values)
    brier[c] = float(np.mean((pred(b, lgc.loc[~trn, c].values) - lgc.loc[~trn, "y"].values) ** 2))
ok("OOS cover chosen", all(brier["cover"] < 0.5 * brier[c] for c in ("gap", "dy", "dscr")),
   ", ".join("%s %.3f" % kv for kv in brier.items()))
beta = irls(lgc.cover.values, lgc.y.values)
fx["mat"] = pd.to_datetime(fx.maturity_date)
fx["omat"] = pd.to_datetime(fx.original_maturity_date)
fx["ext"] = fx.mat != fx.omat


def run(r, months):
    B = r.principal_balance
    out = []
    for k in range(months):
        m = FIRST + k - 1
        yy, mo_ = divmod(m, 12)
        days = (pd.Timestamp(yy, mo_ + 1, 1) + pd.offsets.MonthEnd(0)).day if r.interest_basis == "ACT/360" else 30
        it = B * r.note_rate / 100 * days / 360
        pr_ = min(r.monthly_payment - it, B)
        B -= pr_
        out.append((it, pr_, B))
    return out


def cre_loss(pfun):
    cf = np.zeros(H)
    for _, r in fx.iterrows():
        mat = ordm(r.mat)
        p = 0.0 if r.ext else pfun(r)
        last = mat + (36 if p > 0 else 0)
        for k, (it, pr_, B) in enumerate(run(r, last - ASOF)):
            m = FIRST + k
            if m < mat:
                cf[k] += it + pr_
            elif m == mat:
                cf[k] += it + pr_ + (1 - p) * B
            elif m < last:
                cf[k] += p * (it + pr_)
            else:
                cf[k] += p * (it + pr_ + B)
    return loss(cf)


bal_cache = {}


def balloon(r):
    if r.loan_number not in bal_cache:
        bal_cache[r.loan_number] = run(r, ordm(r.omat) - ASOF)[-1][2]
    return bal_cache[r.loan_number]


pull = pd.Timestamp("2026-12-03")


def cover_now(r):
    return latest(r.property_number, pull, strict=False) / (balloon(r) * dcon(CRER))


L_CRE = cre_loss(lambda r: float(pred(beta, cover_now(r))))
L_CRE0 = cre_loss(lambda r: 0.0)
recent_share = lgc[lgc.date > "2025-11-30"].y.mean()
L_CREr = cre_loss(lambda r: recent_share)
ok("CRE recomputed", abs(L_CRE - 150.9) < 1.5, "%.2f" % L_CRE)
gold = {"Treasury ladder": L_T, "Agency MBS": L_MBS, "2023-24 residential mortgages": L_M, "Indirect auto loans": L_A,
        "Fixed-rate commercial real estate": L_CRE}
top = max(gold, key=gold.get)
ok("CALL designation", top == "Fixed-rate commercial real estate" and 25 * round(L_CRE / 25) == 150,
   "%s $%d million (%s)" % (top, 25 * round(L_CRE / 25), ", ".join("%s %.1f" % (k.split()[0], v) for k, v in gold.items())))
dflt = dict(gold, **{"Fixed-rate commercial real estate": L_CREr})
d_top = max(dflt, key=dflt.get)
ok("DEFAULT path files Agency MBS", d_top == "Agency MBS" and 25 * round(L_MBS / 25) == 100,
   "Agency MBS %.1f, CRE at the recent share %.1f" % (L_MBS, L_CREr))
r0 = dict(gold, **{"Fixed-rate commercial real estate": L_CRE0, "2023-24 residential mortgages": L_M12})
ok("R0 last year's speeds file the mortgages", max(r0, key=r0.get) == "2023-24 residential mortgages",
   "mortgages %.1f" % L_M12)

# ------------------------------------------------------------------------------------------------- Ask A
rg = pd.read_excel(f("swap_register_20261130.xlsx"), sheet_name="Trades", dtype={"Trade No.": str, "Clearing ref": str})
cl = pd.read_csv(f("clearing_statement_20261130.csv"), dtype={"ccp_trade_id": str, "client_trade_ref": str})
sc = pd.read_csv(f("swap_amortisation_schedules.csv"), dtype={"trade_number": str})
alm_ = rg[(rg.Book == "ALM") & (rg.Status == "LIVE")].copy()
ccp_of = dict(zip(cl.client_trade_ref, cl.ccp_trade_id))
reg_ccp = dict(zip(rg["Clearing ref"].fillna(""), rg["Trade No."]))
gone = [tn for tn, c in zip(alm_["Trade No."], alm_.Cleared) if c == "N" and tn in ccp_of and
        reg_ccp.get(ccp_of[tn], tn) != tn]
alm_ = alm_[~alm_["Trade No."].isin(gone)]
ok("XLSX register and statement", len(gone) == 4, "%d bilateral trades held by the broker under cleared trades" % len(gone))


def part(r):
    if r["Bank pays"] == "FLOAT":
        return "loan"
    h = str(r["Hedged item"]).lower()
    return "funding" if ("deposit" in h or "advances" in h) else "overlay"


QE = [pd.Timestamp(d) for d in ("2027-03-31", "2027-06-30", "2027-09-30", "2027-12-31")]
res = {"overlay": [], "funding": [], "loan": []}
for d in QE:
    tot = {"overlay": 0.0, "funding": 0.0, "loan": 0.0}
    for _, r in alm_.iterrows():
        if not (pd.Timestamp(r["Effective date"]) <= d < pd.Timestamp(r["Maturity date"])):
            continue
        s = sc[sc.trade_number == r["Trade No."]]
        if len(s):
            s = s[(pd.to_datetime(s.period_start) <= d) & (d < pd.to_datetime(s.period_end))]
            n = float(s.notional.iloc[0])
        else:
            n = float(r["Notional (USD)"])
        tot[part(r)] += n
    tot["overlay"] += 1.2e9
    for k in tot:
        res[k].append(round(tot[k] / 1e6, 1))
ok("ASK A recomputed", res == {"overlay": [3127.8, 3114.3, 3101.2, 3088.4], "funding": [437.5, 437.5, 537.5, 537.5],
                               "loan": [2047.5, 1647.5, 1313.2, 1313.2]}, str(res))
fails = OUT.count(False)
print("verify: %d passed, %d failed" % (OUT.count(True), fails))
sys.exit(1 if fails else 0)
