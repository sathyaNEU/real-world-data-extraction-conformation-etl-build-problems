"""The servicing extracts, the loan master, the guarantee register and the small files around them.

The bank converted its core in October 2017 and ran both systems in parallel that month, so October 2017 is in both
extracts. The legacy core keyed a loan by its legacy number and kept balances in cents and rates as fractions; the
current system keys the note number and keeps dollars and percent. The loan master is SBA Lending's portfolio register
of every 7(a) loan approved since October 2009, with all three numbers. The guarantee register is the loan documentation
system's record of each guaranty, by SBA loan number."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import cast as CA
import common as K

F_CURRENT = "servicing_history_2017-10_2026-09.parquet"
F_LEGACY = "legacy_loan_history_200910_201710.parquet"
F_MASTER = "sba_loan_master.csv"
F_REGISTER = "guarantee_register.xlsx"
F_CODES = "servicing_status_codes.csv"
F_1502 = "form1502_2026-09.csv"
F_SECMKT = "secondary_market_settlements.csv"
F_MANIFEST = "export_manifest.csv"

CONVERSION = 96                     # October 2017, the parallel-run month
CODE_CUR = {1: "CUR", 2: "D30", 3: "D60", 4: "D90", 5: "ACC", 6: "LIQ", 7: "CO", 8: "PIF", 9: "MAT"}
CODE_LEG = {1: "CURR", 2: "DLQ1", 3: "DLQ2", 4: "DLQ3", 5: "ACCL", 6: "LIQD", 7: "CHGO", 8: "PDOF", 9: "MATR"}
CODE_TEXT = {1: "Current", 2: "30 to 59 days past due", 3: "60 to 89 days past due", 4: "90 or more days past due",
             5: "Accelerated (loan called due)", 6: "In liquidation", 7: "Charged off", 8: "Paid in full",
             9: "Matured, paid at maturity"}


class Ids:
    pass


def ids(W):
    """SBA loan numbers by approval date, legacy numbers for loans booked before the conversion, note numbers for
    loans on the current system."""
    rg = K.rng("ids")
    order = sorted(range(W.n), key=lambda i: (W.appr_date[i], i))
    sba = [None] * W.n
    base = 3_861_000
    for i in order:
        base += int(rg.integers(20, 260))
        chk = int(rg.integers(0, 10))
        sba[i] = "%07d%03d" % (base, 1 + chk)
    on_current = np.zeros(W.n, bool)
    on_legacy = np.zeros(W.n, bool)
    R = W.rec
    on_current[np.unique(R["i"][R["t"] >= CONVERSION])] = True
    on_legacy[np.unique(R["i"][R["t"] <= CONVERSION])] = True
    leg = [None] * W.n
    note = [None] * W.n
    n_leg = 4100
    n_note = 7300004000
    for i in sorted(range(W.n), key=lambda i: (W.disb_date[i], i)):
        if W.disb_m[i] <= CONVERSION:
            n_leg += int(rg.integers(1, 4))
            leg[i] = "21-%06d" % n_leg
    conv = [i for i in range(W.n) if on_current[i] and W.disb_m[i] <= CONVERSION]
    rg.shuffle(conv)
    for i in conv:                                  # the conversion numbered the open book in one run
        n_note += int(rg.integers(1, 3))
        note[i] = "%010d" % n_note
    for i in sorted([i for i in range(W.n) if W.disb_m[i] > CONVERSION], key=lambda i: (W.disb_date[i], i)):
        n_note += int(rg.integers(1, 5))
        note[i] = "%010d" % n_note
    I = Ids()
    I.sba, I.leg, I.note, I.on_current, I.on_legacy = sba, leg, note, on_current, on_legacy
    return I


def _rows_by_loan(W):
    R = W.rec
    o = np.lexsort((R["t"], R["i"]))
    return {k: R[k][o] for k in R}


def write_current(path, W, I):
    R = _rows_by_loan(W)
    m = R["t"] >= CONVERSION
    idx = R["i"][m]
    t = R["t"][m]
    code = R["code"][m]
    dpd = R["dpd"][m].astype(np.int32)
    closed_or_liq = np.isin(code, (6, 7, 8, 9))
    note = np.array([I.note[i] for i in idx], dtype=object)
    period = np.array([K.month_end(int(x)) for x in np.unique(t)], dtype="datetime64[D]")
    pmap = dict(zip(np.unique(t), period))
    pe = np.array([pmap[x] for x in t], dtype="datetime64[D]")
    bal = np.round(R["bal"][m], 2)
    rate = np.round(R["rate"][m].astype(float), 3)
    tab = pa.table({
        "note_no": pa.array(note, pa.string()),
        "period_end": pa.array(pe, pa.date32()),
        "status": pa.array([CODE_CUR[int(c)] for c in code], pa.string()),
        "dpd": pa.array(np.where(closed_or_liq, None, dpd).tolist(), pa.int32()),
        "principal_bal": pa.array(bal, pa.float64()),
        "note_rate": pa.array(rate, pa.float64()),
    })
    pq.write_table(tab, path, compression="zstd", row_group_size=250_000, use_dictionary=["status"], write_statistics=True)
    return tab.num_rows


def write_legacy(path, W, I):
    R = _rows_by_loan(W)
    m = R["t"] <= CONVERSION
    idx = R["i"][m]
    t = R["t"][m]
    code = R["code"][m]
    y = np.array([K.ym(int(x))[0] * 100 + K.ym(int(x))[1] for x in range(K.H)])
    tab = pa.table({
        "LOAN_NO": pa.array([I.leg[i] for i in idx], pa.string()),
        "PERIOD": pa.array(y[t], pa.int32()),
        "STAT_CD": pa.array([CODE_LEG[int(c)] for c in code], pa.string()),
        "DAYS_DLQ": pa.array(np.where(np.isin(code, (6, 7, 8, 9)), 0, R["dpd"][m]).astype(np.int32), pa.int32()),
        "PRIN_BAL_CENTS": pa.array(np.round(R["bal"][m] * 100).astype(np.int64), pa.int64()),
        "INT_RT": pa.array(np.round(R["rate"][m].astype(float) / 100.0, 5), pa.float64()),
    })
    pq.write_table(tab, path, compression="zstd", row_group_size=250_000, use_dictionary=["STAT_CD"], write_statistics=True)
    return tab.num_rows


MASTER_COLS = ["sba_loan_no", "legacy_loan_no", "note_no", "borrower_name", "naics", "city", "state", "approval_date",
               "first_disbursement_date", "first_payment_date", "maturity_date", "term_months", "loan_amount",
               "guaranty_pct", "rate_type", "spread", "initial_rate", "program"]


def master_rows(W, I, C):
    out = []
    for i in sorted(range(W.n), key=lambda i: (W.appr_date[i], I.sba[i])):
        if W.status[i] == 0:
            continue
        fp = K.month_first(int(W.fp_m[i]))
        fpd = dt.date(fp.year, fp.month, int(W.due_day[i]))
        mat_m = int(W.fp_m[i] + W.term[i] - 1)
        mf = K.month_first(mat_m)
        town = C.loan_town[i]
        out.append({
            "sba_loan_no": I.sba[i], "legacy_loan_no": I.leg[i] or "", "note_no": I.note[i] or "",
            "borrower_name": C.loan_name[i], "naics": W.naics[i], "city": town[0], "state": town[1],
            "approval_date": W.appr_date[i].isoformat(), "first_disbursement_date": W.disb_date[i].isoformat(),
            "first_payment_date": fpd.isoformat(), "maturity_date": dt.date(mf.year, mf.month, int(W.due_day[i])).isoformat(),
            "term_months": int(W.term[i]), "loan_amount": "%.2f" % W.amt[i], "guaranty_pct": "%d" % round(100 * (1 - W.ug[i])),
            "rate_type": "V" if W.var[i] else "F", "spread": ("%.2f" % W.spread[i]) if W.var[i] else "",
            "initial_rate": "%.3f" % initial_rate(W, i), "program": "7(a) PLP",
        })
    return out


def initial_rate(W, i):
    a = W.appr_date[i]
    if W.var[i]:
        return K.prime_on(a) + W.spread[i]
    return round((K.prime_on(a) + W.spread[i] + 0.5) * 8) / 8


REGISTER_COLS = ["SBA Loan No", "Borrower", "Party No", "Guarantor", "Type", "TIN (last 4)", "Ownership %", "Guaranty",
                 "Executed", "Released"]


def register_rows(W, I, C):
    rg = K.rng("register")
    out = []
    end = K.month_end(K.T_END)
    for g in sorted(C.by_g):
        loans = C.by_g[g]
        gs = C.group_guarantors[g]
        for k, i in enumerate(loans):
            if W.status[i] == 0:
                continue
            here = [(p, sc) for p, sc in gs if sc == "all" or k in sc]
            inds = [p for p, sc in here if p.kind == "I"]
            shares = _shares(rg, len(inds))
            closed = W.status[i] in (3, 4, 5)
            rel = ""
            if W.status[i] in (4, 5) and W.end_m[i] >= 0:
                rel_d = K.month_end(int(W.end_m[i])) + dt.timedelta(days=int(rg.integers(3, 40)))
                rel = min(rel_d, end).isoformat()
            ex = W.disb_date[i] - dt.timedelta(days=int(rg.integers(0, 3)))
            si = 0
            for p, sc in here:
                if p.kind == "I":
                    own = shares[si]
                    si += 1
                    gt = "Unlimited" if own >= 20 else ("Limited" if rg.random() < 0.6 else "Unlimited")
                else:
                    own = 100
                    gt = "Unlimited"
                out.append({"SBA Loan No": I.sba[i], "Borrower": C.loan_name[i], "Party No": p.party,
                            "Guarantor": CA.typed(rg, p),
                            "Type": "Individual" if p.kind == "I" else "Entity", "TIN (last 4)": p.tin4,
                            "Ownership %": own, "Guaranty": gt, "Executed": ex, "Released": rel or None})
    return out


def _shares(rg, n):
    if n <= 0:
        return []
    if n == 1:
        return [100]
    cuts = sorted(int(x) for x in rg.choice(np.arange(10, 91), size=n - 1, replace=False))
    parts = [b - a for a, b in zip([0] + cuts, cuts + [100])]
    return parts


def code_rows():
    out = []
    for c in range(1, 10):
        out.append({"system": "Current (from October 2017)", "code": CODE_CUR[c], "description": CODE_TEXT[c]})
    for c in range(1, 10):
        out.append({"system": "Legacy core (to October 2017)", "code": CODE_LEG[c], "description": CODE_TEXT[c]})
    return out


F1502_COLS = ["gp_number", "lender_loan_no", "borrower_name", "report_period", "gty_pct", "gty_portion_bal",
              "installment_amt", "paid_to_date", "status_cd"]


def form1502_rows(W, I, C):
    """The September 2026 Form 1502 report: guaranteed-portion balances and SBA status codes for the loans in
    regular servicing or liquidation."""
    R = W.rec
    m = R["t"] == K.T_END
    out = []
    sbacode = {1: "1", 2: "2", 3: "3", 4: "4", 5: "9", 6: "9"}
    for i, c, b, pay in zip(R["i"][m], R["code"][m], R["bal"][m], R["pay"][m]):
        if c in (7, 8, 9):
            continue
        g = 1 - W.ug[i]
        due = K.month_first(K.T_END)
        ptd = dt.date(due.year, due.month, int(W.due_day[i])) if c == 1 else None
        out.append({"gp_number": I.sba[i], "lender_loan_no": I.note[i], "borrower_name": C.loan_name[i],
                    "report_period": "2026-09", "gty_pct": "%d" % round(100 * g), "gty_portion_bal": "%.2f" % (g * b),
                    "installment_amt": "%.2f" % pay, "paid_to_date": ptd.isoformat() if ptd else "",
                    "status_cd": sbacode[int(c)]})
    out.sort(key=lambda r: r["gp_number"])
    return out


SECMKT_COLS = ["settlement_date", "sba_loan_no", "gty_portion_sold", "price", "premium", "dealer"]


def sold(W):
    """Which guaranteed portions were sold, and when: most are sold a month or two after disbursement; about half of
    the loans of $150,000 or less are held."""
    rg = K.rng("secmkt")
    out = {}
    for i in range(W.n):
        held = W.amt[i] <= 150000 and rg.random() < 0.55
        sd = W.disb_date[i] + dt.timedelta(days=int(rg.integers(25, 75)))
        price = round(float(np.clip(rg.normal(109.5 if sd.year < 2020 else 111.0, 1.4), 104.0, 114.5)) * 8) / 8
        dealer = int(rg.integers(0, 5))
        if W.status[i] != 0 and not held and sd <= K.RESERVE_DATE and (W.def_m[i] < 0 or K.m_of(sd) < W.def_m[i]):
            out[i] = (sd, price, dealer)
    return out


def secmkt_rows(W, I, S):
    dealers = ["BD-03", "BD-07", "BD-11", "BD-14", "BD-22"]
    out = []
    for i in sorted(S):
        sd, price, dealer = S[i]
        g = (1 - W.ug[i]) * W.amt[i]
        out.append({"settlement_date": sd.isoformat(), "sba_loan_no": I.sba[i], "gty_portion_sold": "%.2f" % g,
                    "price": "%.3f" % price, "premium": "%.2f" % (g * (price - 100) / 100.0), "dealer": dealers[dealer]})
    out.sort(key=lambda r: (r["settlement_date"], r["sba_loan_no"]))
    return out
