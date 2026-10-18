"""task166 data files, written from the clean truth in each source system's own layout. Every layout quirk here is
how the system that writes the file writes it (the extract notes describe the fields); nothing is placed to be caught.

Files written here (the workbooks and documents are in docs.py):
  servicing_monthly_legacy_2023-01_2024-08.csv   legacy servicing platform, loan by month, to the August 2024 cycle
  servicing_monthly_2024-09_2026-11.csv          servicing platform from the September 2024 cycle
  servicing_conversion_xref.csv                  legacy loan numbers to loan ids at the conversion
  rate_sheet_archive.csv                         the bank's posted rate sheets, 2015 onward
  cre_term_loans_20261130.csv                    commercial real estate term loans at the close on 30 November
  cre_operating_statements.csv                   borrowers' annual operating statements as reviewed
  custody_holdings_20261130.csv                  the custodian's holdings of the investment portfolio, $ thousands
  agency_pool_factors.csv                        monthly factors of the agency pools held
  indirect_auto_tape_20261130.csv                indirect auto loans at the close on 30 November
  indirect_auto_monthly_roll.csv                 the indirect auto portfolio's monthly roll
  swap_amortisation_schedules.csv                notional schedules of the amortising swaps
  clearing_statement_20261130.csv                the clearing broker's statement of the bank's cleared swaps
  mortgage_lock_pipeline_20261130.csv            rate locks outstanding at the close on 30 November"""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import swaps as SW
import world as WD

mo, ym = K.mo, K.ym

F_LEGACY = "servicing_monthly_legacy_2023-01_2024-08.csv"
F_SERV = "servicing_monthly_2024-09_2026-11.csv"
F_XREF = "servicing_conversion_xref.csv"
F_RATES = "rate_sheet_archive.csv"
F_CRE = "cre_term_loans_20261130.csv"
F_STMT = "cre_operating_statements.csv"
F_CUSTODY = "custody_holdings_20261130.csv"
F_FACTORS = "agency_pool_factors.csv"
F_AUTO = "indirect_auto_tape_20261130.csv"
F_ROLL = "indirect_auto_monthly_roll.csv"
F_SCHED = "swap_amortisation_schedules.csv"
F_CLEAR = "clearing_statement_20261130.csv"
F_LOCKS = "mortgage_lock_pipeline_20261130.csv"

CONV_LAST = mo(2024, 8)        # the legacy platform's last cycle


def mdy(d):
    return "%02d%02d%04d" % (d.month, d.day, d.year)


def iso(d):
    return d.isoformat()


def m2(x):
    return "%.2f" % x


def day_in(o, day):
    y, m = ym(o)
    return dt.date(y, m, min(day, K.month_end(o).day))


# ------------------------------------------------------------------------------------------------- servicing
def _ids(W):
    """legacy loan numbers and platform loan ids, one per loan, both issued in no meaningful order"""
    g = K.rng(40)
    loans = W.m_loans + W.hfs
    leg = g.choice(np.arange(10_000_000, 99_999_999), size=len(loans), replace=False)
    new = g.choice(np.arange(10_000_000, 99_999_999), size=len(loans), replace=False)
    for L, a, b in zip(loans, leg, new):
        L["legacy_no"] = "007%07d" % (int(a) % 10_000_000)
        L["loan_id"] = "52%08d" % int(b)
    # the seven-digit tail can collide; re-issue any duplicate
    seen = set()
    for L in loans:
        while L["legacy_no"] in seen:
            L["legacy_no"] = "007%07d" % int(g.integers(0, 10_000_000))
        seen.add(L["legacy_no"])


def _hfs_hist(L):
    """a loan held for sale pays its first instalments and leaves when the agency purchase settles"""
    B = L["bal0"]
    rows = []
    for k in range(1, L["held"] + 1):
        o = L["orig"] + k
        if o > K.ASOF_M:
            break
        n = L["term"] - (k - 1)
        pay = float(WD.pmt(B, L["note"], n))
        sched = pay - B * L["note"] / 1200.0
        if k == L["held"]:
            rows.append((o, B, sched, 0.0, B - sched, 0.0, "S"))
            break
        rows.append((o, B, sched, 0.0, 0.0, B - sched, "C"))
        B -= sched
    return rows


def servicing_rows(W):
    _ids(W)
    by_lid = {L["lid"]: L for L in W.m_loans}
    hist = {}
    for (lid, o, B, sched, curt, pif, Bn, r, status) in W.m_hist:
        hist.setdefault(lid, []).append((o, B, sched, curt, pif, Bn, {"C": "C", "PIF": "P", "TRF": "S"}[status]))
    for L in W.hfs:
        hist[L["lid"]] = _hfs_hist(L)
    allloans = W.m_loans + W.hfs
    legacy, new, xref = [], [], []
    g = K.rng(41)
    for L in allloans:
        port = "PORT" if L["lid"] < 900000 else "HFS"
        od = day_in(L["orig"], L["day"])
        for (o, B, sched, curt, pif, Bn, st) in hist.get(L["lid"], []):
            liq = None
            if st in ("P", "S"):
                liq = day_in(o, int(g.integers(1, 29)))
            if o <= CONV_LAST:
                legacy.append([L["legacy_no"], "%04d%02d" % ym(o), port, mdy(od), m2(L["bal0"]), L["term"],
                               "%.3f" % L["note"], L["state"], L["occ"], L["purpose"], L["ltv"], L["fico"], m2(B),
                               m2(sched), m2(curt), m2(pif), m2(Bn), st, mdy(liq) if liq else ""])
            else:
                zb = {"C": "", "P": "01", "S": "15"}[st]
                new.append([L["loan_id"], "%04d-%02d" % ym(o), "PORTFOLIO" if port == "PORT" else "HELD FOR SALE",
                            iso(od), m2(L["bal0"]), L["term"], "%.5f" % (L["note"] / 100.0), L["state"],
                            {"P": "PRINCIPAL RESIDENCE", "S": "SECOND HOME", "I": "INVESTMENT"}[L["occ"]],
                            {"P": "PURCHASE", "R": "RATE/TERM REFINANCE", "C": "CASH-OUT REFINANCE"}[L["purpose"]],
                            L["ltv"], L["fico"], m2(B), m2(sched), m2(curt + pif), m2(Bn),
                            "ZERO BALANCE" if st != "C" else "CURRENT", iso(liq) if liq else "", zb])
        # converted: active at the end of the legacy platform's last cycle
        h = hist.get(L["lid"], [])
        last_leg = [x for x in h if x[0] <= CONV_LAST]
        if last_leg and last_leg[-1][6] == "C" and any(x[0] > CONV_LAST for x in h):
            xref.append([L["legacy_no"], L["loan_id"], m2(last_leg[-1][5]), "2024-08"])
        elif not last_leg and h and h[0][0] > CONV_LAST and L["orig"] <= CONV_LAST:
            # originated in August 2024: boarded on the legacy platform, first instalment on the new one
            xref.append([L["legacy_no"], L["loan_id"], m2(L["bal0"]), "2024-08"])
    # the legacy platform sorts by loan number within each cycle and writes a trailer
    legacy.sort(key=lambda r: (r[1], r[0]))
    tot = sum(float(r[16]) for r in legacy)
    legacy.append(["TRL", "%d" % len(legacy), "", "", "", "", "", "", "", "", "", "", "", "", "", "", m2(tot), "", ""])
    new.sort(key=lambda r: (r[1], r[0]))
    xref.sort(key=lambda r: r[0])
    return legacy, new, xref


LEGACY_COLS = ["LOAN_NO", "CYCLE", "PORTF", "ORIG_DT", "ORIG_AMT", "TERM", "NOTE_RT", "PROP_ST", "OCC", "PURP",
               "ORIG_LTV", "FICO", "BEG_PRIN", "SCHED_PRIN", "CURTAIL", "PIF_PRIN", "END_PRIN", "STAT", "LIQ_DT"]
SERV_COLS = ["loan_id", "reporting_period", "investor_type", "origination_date", "original_balance",
             "original_term_months", "interest_rate", "property_state", "occupancy_type", "loan_purpose",
             "ltv_at_origination", "credit_score_at_origination", "beginning_principal", "scheduled_principal",
             "unscheduled_principal", "ending_principal", "loan_status", "zero_balance_date", "zero_balance_code"]
XREF_COLS = ["legacy_loan_no", "loan_id", "converted_principal", "last_legacy_cycle"]


# ------------------------------------------------------------------------------------------------- rate sheets
OLD_CODE = {"J30F": "JMB30", "J15F": "JMB15", "C30F": "CNF30", "C15F": "CNF15", "CRE5F": "CRE5"}
DESC = {"J30F": "Portfolio jumbo 30-year fixed", "J15F": "Portfolio jumbo 15-year fixed",
        "C30F": "Conforming 30-year fixed", "C15F": "Conforming 15-year fixed",
        "CRE5F": "Commercial real estate 5-year fixed, 25-year amortization"}
RATE_COLS = ["sheet_date", "product_code", "product_description", "rate", "points", "lock_days"]


def rate_rows(W):
    rows = []
    for d, code, rate, pts in W.sheets:
        c = code if d >= dt.date(2024, 1, 1) else OLD_CODE[code]
        rows.append([iso(d), c, DESC[code], "%.3f" % rate, ("%.3f" % pts) if code != "CRE5F" else "",
                     "45" if code != "CRE5F" else "60"])
    return rows


# ------------------------------------------------------------------------------------------------- CRE
def cre_alive(L):
    if L["early"] is not None:
        return False
    if L["mat"] > K.ASOF_M:
        return True
    return bool(L["ext"]) and L["mat"] + L["ext_months"] > K.ASOF_M


def cre_extended_now(L):
    return L["mat"] <= K.ASOF_M and bool(L["ext"])


def cre_balance_asof(L):
    if cre_extended_now(L):
        return L["ext_path"][K.ASOF_M - L["mat"] - 1]
    k = K.ASOF_M - L["orig"]
    return L["bal_path"][k - 1]


def cre_terms_now(L):
    """the terms in force at the as-of: an extended loan carries its extension's rate, payment and maturity"""
    if cre_extended_now(L):
        return L["ext_rate"], L["ext_pay"], L["mat"] + L["ext_months"], (WD.EXT_AMORT if not L["sale"] else L["amort"])
    return L["r0"], L["payment"], L["mat"], L["amort"]


GRADE_STEPS = ((1.40, 3), (1.20, 4), (1.00, 5), (0.90, 6), (0.80, 7))


def risk_grade(L, noi=None):
    """the bank's scale of 1 to 9 on the in-place cover of the current payment, moved a grade either way by the
    credit officer's judgment in a few files; 6 watch, 7 special mention, 8 substandard"""
    rate, pay, _, _ = cre_terms_now(L)
    s = latest_stmt(L)
    dscr = (noi if noi is not None else s["noi"]) / (pay * 12)
    gr = 8
    for lo, g_ in GRADE_STEPS:
        if dscr >= lo:
            gr = g_
            break
    return int(min(8, max(2, gr + L.get("grade_adj", 0))))


def latest_stmt(L, by=None):
    by = by or K.PULL
    s = [x for x in L["stmts"] if x["review"] <= by]
    return s[-1] if s else None


def loan_number(L):
    return "44%06d%02d" % (L["obligor"], L["note_no"])


def obligation(L):
    return "%06d-%02d" % (L["obligor"], L["note_no"])


CRE_COLS = ["loan_number", "obligor_number", "property_number", "property_type", "msa", "state", "origination_date",
            "original_maturity_date", "maturity_date", "rate_type", "note_rate", "rate_index", "rate_spread",
            "interest_basis", "interest_only_months", "amortization_months", "original_principal", "principal_balance",
            "monthly_payment", "next_due_date", "risk_grade"]
PT_NAME = {"MF": "Multifamily", "OFF": "Office", "RET": "Retail", "IND": "Industrial", "MIX": "Mixed use"}


def cre_rows(W):
    rows = []
    for L in W.cre:
        if not cre_alive(L):
            continue
        od = day_in(L["orig"], L["oday"])
        omat = day_in(L["mat"], L["oday"])
        rate, pay, mat_o, amort = cre_terms_now(L)
        mat = day_in(mat_o, L["oday"])
        io = 0 if (cre_extended_now(L) and not L["sale"]) else L["io"]
        rows.append([loan_number(L), "%06d" % L["obligor"], "P%05d" % L["prop"], PT_NAME[L["ptype"]], L["msa"],
                     L["state"], iso(od), iso(omat), iso(mat), "FIXED", "%.3f" % rate, "", "", L["basis"], io,
                     amort, m2(L["b0"]), m2(cre_balance_asof(L)), m2(pay), "2026-12-%02d" % L["oday"],
                     risk_grade(L)])
    for F in W.cre_float:
        od = day_in(F["orig"], F["oday"])
        mat = day_in(F["orig"] + F["term"], F["oday"])
        rate = WD.SOFR[K.ASOF_M] + F["spread"]
        pay = float(WD.pmt(F["bal"], rate, 300 - (K.ASOF_M - F["orig"])))
        rows.append(["44%06d01" % F["obligor"], "%06d" % F["obligor"], "P%05d" % F["prop"], PT_NAME[F["ptype"]],
                     F["msa"], F["state"], iso(od), iso(mat), iso(mat), "FLOATING", "%.3f" % rate, "1M TERM SOFR",
                     "%.3f" % F["spread"], "ACT/360", 0, 300, m2(F["b0"]), m2(F["bal"]), m2(pay),
                     "2026-12-%02d" % F["oday"], F["grade"]])
    rows.sort(key=lambda r: r[0])
    return rows


def maturity_log(W):
    """the credit administration log's rows by year: every term loan that reached a maturity date from 2015, and the
    extended loans when they reached their extended date"""
    by_year = {}
    for L in W.cre:
        if L["outcome"] is None or L["mat"] < mo(2015, 1):
            continue
        md = day_in(L["mat"], L["oday"])
        bal = L["bal_mat"]
        if L["ext"]:
            new = day_in(L["mat"] + L["ext_months"], L["oday"])
            by_year.setdefault(md.year, []).append(dict(ob=obligation(L), prop=L["prop"], date=md, bal=bal,
                                                        out=L["outcome"], new=new, L=L))
            if L["outcome2"] is not None:
                bal2 = L["ext_path"][-1]
                by_year.setdefault(new.year, []).append(dict(ob=obligation(L), prop=L["prop"], date=new, bal=bal2,
                                                             out=L["outcome2"], new=None, L=L))
        else:
            by_year.setdefault(md.year, []).append(dict(ob=obligation(L), prop=L["prop"], date=md, bal=bal, out="PO",
                                                        new=None, L=L))
    for y in by_year:
        by_year[y].sort(key=lambda r: (r["date"], r["ob"]))
    return by_year


STMT_COLS = ["property_number", "fiscal_year_end", "statement_basis", "gross_revenue", "operating_expenses",
             "net_operating_income", "review_completed"]


def stmt_rows(W):
    rows = []
    for L in W.cre:
        if not (cre_alive(L) or (L["outcome"] is not None and L["mat"] >= mo(2015, 1))):
            continue
        for s in L["stmts"]:
            if s["review"] > K.PULL:
                continue
            last = (L["mat"] + (L["ext_months"] if L["ext"] else 0))
            if s["end_o"] > last:
                continue
            if s["end_o"] < mo(2013, 1):
                continue
            rows.append(["P%05d" % L["prop"], iso(s["end"]), s["basis"], "%.0f" % s["rev"], "%.0f" % s["exp"],
                         "%.0f" % s["noi"], iso(s["review"])])
    for F in W.cre_float:
        rows += F["stmt_rows"]
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def float_statements(W):
    """the floating-rate loans' reviewed statements, and each loan's grade on the latest one"""
    g = K.rng(42)
    ga = K.rng(43)
    for F in W.cre_float:
        noi = F["b0"] * WD.dc(5.5, 300) * 1.35 * float(np.exp(g.normal(0, 0.12)))
        fye = int(g.choice([12, 6, 9], p=[0.74, 0.16, 0.10]))
        F["stmt_rows"] = []
        last = None
        for fy in range(ym(F["orig"])[0] + 1, 2027):
            end = K.month_end(mo(fy, fye))
            rev_d = end + dt.timedelta(days=int(g.integers(70, 160)))
            if rev_d > K.PULL:
                continue
            n = noi * float(np.exp(g.normal(0, 0.05)))
            er = float(np.clip(g.normal(0.42, 0.05), 0.2, 0.65))
            rev = n / (1 - er)
            F["stmt_rows"].append(["P%05d" % F["prop"], iso(end), str(g.choice(["Borrower prepared", "CPA reviewed"])),
                                   "%.0f" % rev, "%.0f" % (rev - n), "%.0f" % n, iso(rev_d)])
            last = n
        rate = WD.SOFR[K.ASOF_M] + F["spread"]
        pay = float(WD.pmt(F["bal"], rate, 300 - (K.ASOF_M - F["orig"])))
        adj = int(ga.choice([-1, 0, 1], p=[0.12, 0.76, 0.12]))
        if last is None:
            F["grade"] = 5
            continue
        dscr = last / (pay * 12)
        gr = 8
        for lo, g_ in GRADE_STEPS:
            if dscr >= lo:
                gr = g_
                break
        F["grade"] = int(min(8, max(2, gr + adj)))


# ------------------------------------------------------------------------------------------------- securities
def cusip_check(base8):
    s = 0
    for i, ch in enumerate(base8):
        v = int(ch) if ch.isdigit() else ord(ch) - 55
        if i % 2 == 1:
            v *= 2
        s += v // 10 + v % 10
    return str((10 - s % 10) % 10)


def make_cusip(g, prefix):
    al = "0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
    body = prefix + "".join(al[int(g.integers(0, len(al)))] for _ in range(8 - len(prefix)))
    return body + cusip_check(body)


def other_securities(W):
    """the rest of the available-for-sale portfolio: newer agency pools, municipal bonds, agency multifamily"""
    g = K.rng(43)
    out = []
    for i in range(6):                      # agency pools bought in 2023 and 2024
        issue = mo(2023, 6) + int(g.integers(0, 16))
        cpn = float(g.choice([5.0, 5.5]))
        out.append(dict(kind="MBS", issue=issue, bought=issue + 1, cpn=cpn, wac=cpn + round(float(g.uniform(0.55, 0.80)), 3),
                        face=round(float(g.uniform(14, 28)) * 1e6, -5), wam0=int(g.integers(354, 359)), term=360,
                        agency=str(g.choice(["FNMA", "FHLMC"])), price=round(float(g.uniform(98.2, 100.6)) * 32) / 32))
    for i in range(14):
        y = int(g.integers(2029, 2041))
        out.append(dict(kind="MUNI", cpn=float(g.choice([3.0, 4.0, 5.0])), mat=dt.date(y, int(g.choice([2, 5, 8, 11])), 1),
                        par=round(float(g.uniform(8, 30)) * 1e6, -5), bought=mo(2019, 1) + int(g.integers(0, 60))))
    for i in range(8):
        y = int(g.integers(2029, 2034))
        out.append(dict(kind="CMBS", cpn=float(g.choice([2.1, 2.6, 4.4, 4.9])), mat=dt.date(y, int(g.integers(1, 13)), 1),
                        par=round(float(g.uniform(30, 70)) * 1e6, -5), bought=mo(2022, 3) + int(g.integers(0, 18))))
    # the newer pools' factors (the same lock-in behaviour as the old ones, their borrowers near the money)
    for P in out:
        if P["kind"] != "MBS":
            continue
        P["factors"] = {P["issue"]: 1.0}
        bal = 1.0
        for o in range(P["issue"] + 1, K.ASOF_M + 1):
            age = o - P["issue"]
            k = P["wam0"] - (age - 1)
            pay = float(WD.pmt(bal, P["wac"], k))
            sched = min(pay - bal * P["wac"] / 1200.0, bal)
            inc = (P["wac"] - W.C15.get(o - 1, 5.5) - 0.70) / 100.0
            smm = WD.M_TURN * 0.95 * WD.SEASON[ym(o)[1] - 1] + 0.030 / (1 + math.exp(-(inc - 0.0075) / 0.0022))
            smm *= math.exp(g.normal(0, 0.08))
            bal = (bal - sched) * (1 - smm)
            P["factors"][o] = bal
    return out


def prepare(W):
    """identifiers and the rest of the portfolio, built once so every file reads the same objects"""
    float_statements(W)
    W.other = other_securities(W)
    g = K.rng(47)
    used = set()
    for P in W.mbs + [x for x in W.other if x["kind"] == "MBS"]:
        pn = pool_number(g, P["agency"], P["term"] == 360)
        while pn in used:
            pn = pool_number(g, P["agency"], P["term"] == 360)
        used.add(pn)
        P["pool_no"] = pn


def pool_number(g, agency, thirty):
    if agency == "FNMA":
        pre = str(g.choice(["FM", "FS", "CA"])) if not thirty else str(g.choice(["FM", "BQ"]))
    else:
        pre = str(g.choice(["SB", "QK"])) if not thirty else str(g.choice(["SD", "QB"]))
    return pre + "%04d" % int(g.integers(1000, 9999))


CUSTODY_COLS = ["account", "cusip", "security_description", "security_type", "pool_number", "coupon",
                "maturity_date", "acquisition_date", "original_face", "factor", "current_face", "amortized_cost",
                "market_price", "market_value", "accrued_interest"]


def custody_rows(W):
    g = K.rng(44)
    rows = []
    # Treasury notes
    for (pm, cpn, md, par) in W.ust:
        cu = make_cusip(g, "91282C")
        acq = day_in(pm, int(g.integers(3, 27)))
        px = 100 * float(sum((cpn / 2) * K.discount((mo(md.year, md.month) - K.ASOF_M - 6 * j) / 12.0)
                             for j in range(0, 12) if mo(md.year, md.month) - 6 * j > K.ASOF_M)
                         + 100 * K.discount((mo(md.year, md.month) - K.ASOF_M) / 12.0)) / 100
        rows.append(["CVB-AFS-01", cu, "US TREASURY NOTE %.3f%% %s" % (cpn, md.strftime("%m/%d/%Y")), "UST", "",
                     "%.3f" % cpn, iso(md), iso(acq), "%.0f" % (par / 1000), "1.00000000", "%.0f" % (par / 1000),
                     "%.0f" % (par / 1000 * float(g.uniform(0.996, 1.004))), "%.4f" % px,
                     "%.0f" % (par / 1000 * px / 100), "%.0f" % (par / 1000 * cpn / 100 * float(g.uniform(0.05, 0.45)))])
    # the 2020-21 agency pools and the newer ones
    for P in W.mbs + [x for x in W.other if x["kind"] == "MBS"]:
        thirty = P["term"] == 360
        pn = P["pool_no"]
        cu = make_cusip(g, "3140" if P["agency"] == "FNMA" else "3132")
        f = P["factors"][K.ASOF_M]
        matd = K.month_end(P["issue"] + P["term"]).replace(day=1)
        desc = "%s UMBS %s %.1f%% %dYR" % (P["agency"], pn, P["cpn"], 30 if thirty else 15)
        acq = day_in(P["bought"], int(g.integers(5, 25)))
        cf = P["face"] * f
        mkt = 100.0 * (0.86 if P["cpn"] == 2.0 else 0.895) if P["cpn"] < 4 else 100.0 * (0.985 if P["cpn"] == 5.0 else 1.003)
        mkt = round(mkt * 32) / 32
        rows.append(["CVB-AFS-01", cu, desc, "AGENCY MBS", pn, "%.3f" % P["cpn"], iso(matd), iso(acq),
                     "%.0f" % (P["face"] / 1000), "%.8f" % f, "%.0f" % (cf / 1000),
                     "%.0f" % (cf / 1000 * (1 + (P["price"] - 100) / 100 * 0.45)), "%.5f" % mkt,
                     "%.0f" % (cf / 1000 * mkt / 100), "%.0f" % (cf / 1000 * P["cpn"] / 1200)])
    for P in W.other:
        if P["kind"] == "MBS":
            continue
        cu = make_cusip(g, "%d" % int(g.integers(10, 99)) + "%04d" % int(g.integers(1000, 9999)))
        if P["kind"] == "MUNI":
            desc = "%s GO BDS %.3f%% %s" % (str(g.choice(["ALLEGHENY CNTY PA", "BUTLER CNTY PA", "MONROEVILLE PA",
                                                           "CRANBERRY TWP PA", "PITTSBURGH PA SCH DIST",
                                                           "OHIO ST", "WASHINGTON CNTY PA"])), P["cpn"],
                                           P["mat"].strftime("%m/%d/%Y"))
            st = "MUNICIPAL"
        else:
            desc = "FNMA DUS %.2f%% %s" % (P["cpn"], P["mat"].strftime("%m/%d/%Y"))
            st = "AGENCY CMBS"
        acq = day_in(P["bought"], int(g.integers(3, 27)))
        px = round(float(g.uniform(88, 101)), 4)
        rows.append(["CVB-AFS-01", cu, desc, st, "", "%.3f" % P["cpn"], iso(P["mat"]), iso(acq),
                     "%.0f" % (P["par"] / 1000), "1.00000000", "%.0f" % (P["par"] / 1000),
                     "%.0f" % (P["par"] / 1000 * float(g.uniform(0.99, 1.02))), "%.4f" % px,
                     "%.0f" % (P["par"] / 1000 * px / 100), "%.0f" % (P["par"] / 1000 * P["cpn"] / 100 * 0.3)])
    rows.sort(key=lambda r: (r[3], r[1]))
    return rows


FACTOR_COLS = ["pool_number", "factor_month", "pool_factor", "wac", "wam", "wala"]


def factor_rows(W):
    rows = []
    pools = W.mbs + [x for x in W.other if x["kind"] == "MBS"]
    for P in pools:
        pn = P["pool_no"]
        for o, f in sorted(P["factors"].items()):
            if o < P["issue"] + 1:
                continue
            age = o - P["issue"]
            wam = P["wam0"] - age
            rows.append([pn, "%04d-%02d" % ym(o), "%.8f" % f, "%.3f" % P["wac"], wam, P["term"] - wam])
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


# ------------------------------------------------------------------------------------------------- auto
AUTO_COLS = ["account_number", "contract_date", "term_months", "apr", "amount_financed", "principal_balance",
             "next_payment_due", "dealer_number", "state", "collateral", "credit_tier", "days_past_due"]


def auto_rows(W):
    g = K.rng(45)
    rows = []
    ids = g.choice(np.arange(1_000_000, 9_999_999), size=len(W.auto_pool), replace=False)
    for a, n in zip(W.auto_pool, ids):
        cd = day_in(a["orig"], a["oday"])
        dpd = 0
        u = g.random()
        if u < 0.022:
            dpd = int(g.integers(1, 30))
        elif u < 0.027:
            dpd = int(g.integers(30, 60))
        elif u < 0.029:
            dpd = int(g.integers(60, 90))
        due = dt.date(2026, 12, min(a["oday"], 28))
        if dpd:
            due = due - dt.timedelta(days=30 * (1 + dpd // 30))
        rows.append(["%07d" % n, iso(cd), a["term"], "%.2f" % a["apr"], m2(a["bal0"]), m2(a["bal"]), iso(due),
                     "D%04d" % a["dealer"], a["state"], a["new"], a["fico"], dpd])
    rows.sort(key=lambda r: r[0])
    return rows


ROLL_COLS = ["month_end", "beginning_principal", "originations", "scheduled_principal", "prepaid_principal",
             "charge_offs", "ending_principal"]


def roll_rows(W):
    rows = []
    bal = 0.0
    for o in sorted(W.auto_roll):
        R = W.auto_roll[o]
        beg = bal
        end = beg + R["orig"] - R["sched"] - R["prepay"] - R["co"]
        bal = end
        if o >= mo(2023, 1):
            rows.append([iso(K.month_end(o)), m2(beg), m2(R["orig"]), m2(R["sched"]), m2(R["prepay"]), m2(R["co"]),
                         m2(end)])
    return rows


# ------------------------------------------------------------------------------------------------- swaps
SCHED_COLS = ["trade_number", "period_start", "period_end", "notional"]


def sched_rows(S):
    rows = []
    for key in ("OV23", "RF7"):
        t = [x for x in S["trades"] if x["key"] == key][0]
        rows += [[t["id"], iso(a), iso(b), "%.2f" % n] for a, b, n in S["sched"][key]]
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


CLEAR_COLS = ["clearing_account", "ccp_trade_id", "client_trade_ref", "cleared_on", "effective_date",
              "termination_date", "notional_usd", "fixed_rate", "client_pays", "index"]


def clear_rows(S):
    rows = []
    for t in S["trades"]:
        if not t["cleared"] or t["status"] != "LIVE":
            continue
        cur = SW.notional_on(t, K.AS_OF, S) if t["key"] in S["sched"] else t["notional"]
        rows.append(["CVB-H-0417" if t["book"] == "ALM" else "CVB-C-0418", t["ccp_id"], t["client_ref"],
                     iso(t["cleared_on"]), iso(t["eff"]), iso(t["mat"]), "%.2f" % cur, "%.4f" % t["rate"],
                     "FIXED" if t["dir"] == "PAY" else "FLOAT", "USD-SOFR-OIS COMPOUND"])
    rows.sort(key=lambda r: r[1])
    return rows


# ------------------------------------------------------------------------------------------------- lock pipeline
LOCK_COLS = ["lock_id", "lock_date", "lock_expiration", "product_code", "loan_amount", "locked_rate", "points",
             "channel", "investor_type"]


def lock_rows(W):
    g = K.rng(46)
    rows = []
    for i in range(int(g.poisson(410))):
        ld = dt.date(2026, 9, 15) + dt.timedelta(days=int(g.integers(0, 77)))
        code = str(g.choice(["J30F", "J15F", "C30F", "C15F"], p=[0.38, 0.06, 0.48, 0.08]))
        base = W.rate[(code, mo(ld.year, ld.month))]
        amt = round(float(np.exp(g.normal(math.log(420000 if code[0] == "J" else 285000), 0.35))) / 50) * 50
        rows.append(["L%07d" % int(g.integers(1_000_000, 9_999_999)), iso(ld),
                     iso(ld + dt.timedelta(days=int(g.choice([30, 45, 60], p=[0.2, 0.6, 0.2])))), code, m2(amt),
                     "%.3f" % (round((base + float(g.choice([-0.125, 0, 0.125]))) * 8) / 8),
                     "%.3f" % float(g.choice([0, 0.125, 0.25, 0.5])), str(g.choice(["RETAIL", "PRIVATE BANKING"],
                                                                                   p=[0.82, 0.18])),
                     "PORTFOLIO" if code[0] == "J" else "HELD FOR SALE"])
    rows.sort(key=lambda r: (r[1], r[0]))
    return rows
