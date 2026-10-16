"""The asks' files: SBA's fiscal transfer agent's Section 1112 remittance detail in its CARES Act and Economic Aid Act
layouts, the SBA settlement account's ACH credits, the special assets ledger and the bank's payments to SBA.

The agent paid most instalments in the month they fell due, one instalment to a disbursement. A loan whose data reached
it late, a new loan's first payment and the first payment of each Economic Aid Act tranche were paid as catch-ups, one
disbursement covering two to four instalments. The agent's detail export prints one line per instalment and carries
the disbursement's amount on each line of it.

Special Assets moved its workout records to a new module on 3 April 2023 for the cases it opened from that date; cases
opened earlier stayed in the old module until they closed. The old module posts a liquidation receipt at the bank's
share; the new one posts the receipt as received, and SBA's share is paid from the liquidation account and recorded
with the bank's other payments to SBA. Treasury offset collections on charged-off loans reach the bank as
SBA's remittance of the lender's share to the settlement account and are posted by loan operations."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as WD

F_CARES = "fta_1112_detail_cares.csv"
F_EAA = "fta_1112_detail_eaa.xlsx"
F_CREDITS = "sba_settlement_account_credits.csv"
F_LEDGER = "special_assets_ledger_fy2020_fy2026.csv"
F_PAYSBA = "payments_to_sba.csv"
MODULE_SWITCH = dt.date(2023, 4, 3)
ASK_A_FIRST, ASK_A_LAST = K.m_of(dt.date(2020, 4, 1)), K.m_of(dt.date(2021, 12, 1))
ASK_B_FYS = (2023, 2024, 2025, 2026)


def weekday(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def batch_dates(m):
    """The agent's two payment runs in month m."""
    f = K.month_first(m)
    return weekday(dt.date(f.year, f.month, 8)), weekday(dt.date(f.year, f.month, 22))


class Ask:
    pass


def build_1112(W, I, C):
    """Every instalment SBA paid, the disbursements that paid them and the agent's lines."""
    rg = K.rng("fta")
    R = W.rec
    m = R["sba"]
    inst = {}
    for i, t, pay, cp in zip(R["i"][m], R["t"][m], R["pay"][m], R["capped"][m]):
        amt = round(min(float(pay), WD.EAA_CAP) if cp else float(pay), 2)
        inst.setdefault(int(i), []).append((int(t), amt))
    A = Ask()
    A.instalments = []        # (loan, month, amount, due date, program)
    A.disb = []               # (loan, remit date, trace, [months], total, program)
    traces = {}

    def trace_for(d, prog):
        key = (d, prog)
        if key not in traces:
            traces[key] = "0910%04d%07d" % (len(traces) + 17, int(rg.integers(0, 10 ** 7)))
        return traces[key]

    for i in sorted(inst):
        paid = dict(inst[i])
        due_day = int(W.due_day[i])
        appr = W.appr_date[i]
        new_loan = (WD.CARES_ENACTED <= appr <= WD.CARES_NEW_END) or (WD.EAA_NEW_START <= appr <= WD.EAA_NEW_END)
        for s0, e0, cp, prog in W.windows[i]:
            run = [(mm, paid[mm]) for mm in range(s0, e0 + 1) if mm in paid]
            if not run:
                continue
            first_new = new_loan and run[0][0] == int(W.fp_m[i])
            u = rg.random()
            if first_new:
                k = int(rg.choice([1, 2, 3, 4], p=[0.4, 0.3, 0.2, 0.1]))
            elif prog == "cares":
                k = 2 if u < 0.22 else (3 if u < 0.32 else 1)
            elif run[0][0] == WD.FEB21:
                k = 2 if u < 0.7 else 1
            else:
                k = 2 if u < 0.5 else 1
            k = min(k, len(run))
            # a catch-up pays each instalment it covers at the amount of the first (the instalment on the agent's file)
            groups = [[(mm, run[0][1]) for mm, _ in run[:k]]] + [[x] for x in run[k:]]
            for gp in groups:
                d1, d2 = batch_dates(gp[-1][0])
                rd = d1 if due_day <= 12 else d2
                tr = trace_for(rd, prog)
                tot = round(sum(a for _, a in gp), 2)
                A.disb.append((i, rd, tr, [mm for mm, _ in gp], tot, prog))
                for mm, a in gp:
                    f = K.month_first(mm)
                    A.instalments.append((i, mm, a, dt.date(f.year, f.month, due_day), prog, rd, tr, tot))
    return A


CARES_COLS = ["remit_date", "trace_no", "sba_loan_no", "borrower", "installment_due", "pmt_amount"]
EAA_COLS = ["Remit Date", "ACH Trace", "SBA Loan Number", "Borrower Name", "Due Date", "Payment Amount (cents)"]


def cares_rows(W, I, C, A):
    out = []
    for i, mm, a, due, prog, rd, tr, tot in A.instalments:
        if prog != "cares":
            continue
        out.append({"remit_date": rd.strftime("%m/%d/%Y"), "trace_no": tr, "sba_loan_no": I.sba[i],
                    "borrower": C.loan_name[i].upper(), "installment_due": due.strftime("%m/%d/%Y"), "pmt_amount": "%.2f" % tot})
    out.sort(key=lambda r: (r["remit_date"][6:] + r["remit_date"][:5], r["trace_no"], r["sba_loan_no"], r["installment_due"][6:] + r["installment_due"][:5]))
    return out


def eaa_rows(W, I, C, A):
    out = []
    for i, mm, a, due, prog, rd, tr, tot in A.instalments:
        if prog != "eaa":
            continue
        s = I.sba[i]
        out.append({"Remit Date": rd, "ACH Trace": tr, "SBA Loan Number": s[:7] + "-" + s[7:], "Borrower Name": C.loan_name[i],
                    "Due Date": due, "Payment Amount (cents)": int(round(tot * 100))})
    out.sort(key=lambda r: (r["Remit Date"], r["ACH Trace"], r["SBA Loan Number"], r["Due Date"]))
    return out


def build_workout(W, I, C, S):
    """Charge-offs, liquidation receipts with SBA's shares, Treasury offset shares and guaranty purchases."""
    rg = K.rng("workout")
    B = Ask()
    B.co = []          # (loan, posted date, amount)
    B.receipts = []    # (loan, date, gross, bank share, sba share, kind)
    B.top = []         # (loan, date, bank share)
    B.purch = []       # (loan, date, amount)
    B.miskeys = []     # (right loan, wrong loan, date, amount)
    for i, t, kind in W.events:
        if kind != "co":
            continue
        co_m = int(t)
        if co_m < K.m_of(dt.date(2016, 10, 1)):
            continue
        f = K.month_first(co_m)
        nd = (K.month_end(co_m) - f).days + 1
        posted = weekday(f + dt.timedelta(days=int(rg.integers(3, nd - 2))))
        if posted > K.month_end(co_m):
            posted = K.month_end(co_m) - dt.timedelta(days=2)
            posted = weekday(posted) if weekday(posted) <= K.month_end(co_m) else posted - dt.timedelta(days=1)
        ug_p = round(float(W.ug[i]) * float(W.def_bal[i]), 2)
        B.co.append((i, posted, ug_p))
        # liquidation receipts after the charge-off
        if rg.random() < 0.72:
            total = float(W.def_bal[i]) * float(rg.beta(1.3, 5.5))
            nrc = int(rg.choice([1, 2, 3, 4], p=[0.4, 0.3, 0.2, 0.1]))
            parts = rg.dirichlet(np.ones(nrc) * 1.5) * total
            days = sorted(int(x) for x in np.minimum(20 + rg.exponential(420.0, nrc), 1600).astype(int))
            for k in range(1, nrc):
                days[k] = max(days[k], days[k - 1] + 35)
            for p, dd in zip(parts, days):
                d = posted + dt.timedelta(days=dd)
                if d > K.RESERVE_DATE - dt.timedelta(days=12):
                    continue
                gross = round(max(float(p), 150.0), 2)
                bank = round(gross * float(W.ug[i]), 2)
                kind = str(rg.choice(["COLLATERAL SALE", "GUARANTOR PMT", "GUARANTOR PMT", "BORROWER PMT", "SETTLEMENT"]))
                B.receipts.append((i, weekday(d), gross, bank, round(gross - bank, 2), kind))
        # Treasury offset collections once SBA has referred the debt
        ref = posted + dt.timedelta(days=int(rg.integers(150, 420)))
        if rg.random() < 0.55:
            y = ref.year + (1 if ref.month > 3 else 0)
            while y <= 2026:
                if rg.random() < 0.45:
                    d = weekday(dt.date(y, int(rg.integers(2, 6)), int(rg.integers(1, 28))))
                    if d <= K.RESERVE_DATE and d > ref:
                        amt = round(float(W.ug[i]) * float(rg.uniform(400, 9000)), 2)
                        B.top.append((i, d, amt))
                y += 1
    # guaranty purchases on held guaranteed portions
    for i in range(W.n):
        if i in S or W.def_m[i] < 0 or W.status[i] not in (2, 3):
            continue
        d = weekday(K.month_first(int(W.def_m[i])) + dt.timedelta(days=int(rg.integers(95, 240))))
        if d > K.RESERVE_DATE:
            continue
        g = 1 - float(W.ug[i])
        accr = float(W.def_bal[i]) * float(W.rate[i]) / 1200.0 * float(rg.uniform(2.0, 4.0))
        B.purch.append((i, d, round(g * (float(W.def_bal[i]) + accr), 2)))
    # three charge-offs keyed first to another loan's note and reversed the next day
    pool_co = [x for x in B.co if 2019 <= W.fy[x[0]] <= 2021 and x[1].year >= 2023 and x[1].day <= 24 and
               not (MODULE_SWITCH - dt.timedelta(days=6) <= x[1] <= MODULE_SWITCH)]
    perf_pool = [i for i in range(W.n) if 2019 <= W.fy[i] <= 2021 and W.status[i] == 1 and I.note[i]]
    for x in [pool_co[int(k)] for k in rg.choice(len(pool_co), size=3, replace=False)]:
        wrong = perf_pool[int(rg.integers(0, len(perf_pool)))]
        while W.fy[wrong] == W.fy[x[0]]:
            wrong = perf_pool[int(rg.integers(0, len(perf_pool)))]
        B.miskeys.append((x[0], wrong, x[1], x[2]))
    return B


LEDGER_COLS = ["posted", "case_no", "note_no", "borrower", "code", "description", "amount"]


def ledger_rows(W, I, C, B):
    rg = K.rng("ledger")
    case = {}
    seq = [24000]

    def case_of(i):
        if i not in case:
            seq[0] += int(rg.integers(1, 4))
            case[i] = "SA-%05d" % seq[0]
        return case[i]
    rows = []
    lo, hi = dt.date(2019, 10, 1), K.RESERVE_DATE
    mis = {x[0]: x for x in B.miskeys}
    for i, d, amt in sorted(B.co, key=lambda x: (x[1], x[0])):
        if not (lo <= d <= hi):
            continue
        if i in mis:
            _, wrong, _, _ = mis[i]
            rows.append((d, case_of(i), I.note[wrong], C.loan_name[wrong], "CO", "CHARGE-OFF UNGUAR PRINCIPAL", amt))
            rows.append((weekday(d + dt.timedelta(days=1)), case_of(i), I.note[wrong], C.loan_name[wrong], "REV",
                         "REVERSE CO POSTED TO WRONG NOTE", -amt))
            rows.append((weekday(d + dt.timedelta(days=1)), case_of(i), I.note[i], C.loan_name[i], "CO",
                         "CHARGE-OFF UNGUAR PRINCIPAL", amt))
        else:
            rows.append((d, case_of(i), I.note[i] or I.leg[i], C.loan_name[i], "CO", "CHARGE-OFF UNGUAR PRINCIPAL", amt))
    co_date = {i: d for i, d, amt in B.co}
    for i, d, gross, bank, sba, kind in sorted(B.receipts, key=lambda x: (x[1], x[0])):
        if not (lo <= d <= hi):
            continue
        amt = gross if co_date[i] >= MODULE_SWITCH else bank       # cases opened in the new module post receipts as received
        rows.append((d, case_of(i), I.note[i] or I.leg[i], C.loan_name[i], "RCV", kind, -amt))
    rows.sort(key=lambda r: (r[0], r[1], r[4] != "CO"))
    return [{"posted": r[0].isoformat(), "case_no": r[1], "note_no": r[2], "borrower": r[3], "code": r[4],
             "description": r[5], "amount": "%.2f" % r[6]} for r in rows]


PAYSBA_COLS = ["paid", "reference", "sba_loan_no", "purpose", "amount"]


def fee_rate(amt, appr):
    """Upfront guaranty fee on the guaranteed portion: waived at approval from 1 March 2021 to 30 September 2021 (the
    loans approved from 28 December 2020 to the end of February paid it and SBA refunded it)."""
    if dt.date(2021, 3, 1) <= appr <= dt.date(2021, 9, 30):
        return 0.0
    if amt <= 150000:
        return 0.0 if appr >= dt.date(2018, 10, 1) else 0.02
    if amt <= 700000:
        return 0.03
    return 0.035


def paysba_rows(W, I, B):
    rg = K.rng("paysba")
    rows = []
    lo = dt.date(2019, 10, 1)
    n = [880000]

    def ref():
        n[0] += int(rg.integers(1, 9))
        return "WT%07d" % n[0]
    last = dt.date(2026, 9, 30)
    for i, d, gross, bank, sba, kind in B.receipts:
        p = weekday(d + dt.timedelta(days=int(rg.integers(5, 26))))
        if p > last:
            p = last
        if lo <= p <= K.RESERVE_DATE:
            rows.append((p, ref(), I.sba[i], "SBA SHARE OF RECOVERY", sba))
    for i in range(W.n):
        a = W.appr_date[i]
        p = weekday(W.disb_date[i] + dt.timedelta(days=int(rg.integers(5, 30))))
        if W.status[i] == 0:
            continue
        r = fee_rate(W.amt[i], a)
        if r > 0 and lo <= p <= K.RESERVE_DATE:
            rows.append((p, ref(), I.sba[i], "UPFRONT GUARANTY FEE", round(r * (1 - W.ug[i]) * W.amt[i], 2)))
    for m in range(K.m_of(lo), K.T_END + 1):
        f = K.month_first(m)
        p = weekday(dt.date(f.year, f.month, 18))
        rows.append((p, ref(), "", "ON-GOING SERVICING FEE (1502)", round(float(rg.uniform(52000, 78000)), 2)))
    rows.sort(key=lambda r: (r[0], r[1]))
    return [{"paid": r[0].isoformat(), "reference": r[1], "sba_loan_no": r[2], "purpose": r[3], "amount": "%.2f" % r[4]}
            for r in rows]


CREDIT_COLS = ["settlement_date", "trace_no", "originator", "entry_description", "amount", "addenda"]


def credit_rows(W, I, A, B, S):
    rg = K.rng("credits")
    rows = []
    lo = dt.date(2019, 10, 1)
    batch = {}
    for i, rd, tr, months, tot, prog in A.disb:
        key = (rd, tr)
        batch.setdefault(key, [0.0, prog])
        batch[key][0] += tot
    for (rd, tr), (tot, prog) in batch.items():
        rows.append((rd, tr, "SBA FTA", "1112 PMT" if prog == "cares" else "1112 EAA", round(tot, 2),
                     "SEC 1112 BORROWER PMT BATCH"))
    seqn = [5100000]

    def tr():
        seqn[0] += int(rg.integers(1, 40))
        return "0910%011d" % seqn[0]
    for i, d, amt in B.top:
        if lo <= d:
            rows.append((d, tr(), "SBA DFC", "CS COLL", amt, "LN %s LNDR PRO RATA SHR TOP OFFSET" % I.sba[i]))
    for i, d, amt in B.purch:
        if lo <= d:
            rows.append((d, tr(), "SBA DFC", "GTY PURCH", amt, "LN %s GUARANTY PURCHASE" % I.sba[i]))
    for i in range(W.n):
        a = W.appr_date[i]
        if dt.date(2020, 12, 28) <= a <= dt.date(2021, 2, 28) and W.amt[i] > 150000 and W.status[i] != 0:
            d = weekday(dt.date(2021, 4, 1) + dt.timedelta(days=int(rg.integers(0, 75))))
            r = 0.03 if W.amt[i] <= 700000 else 0.035
            rows.append((d, tr(), "SBA DFC", "FEE RFND", round(r * (1 - W.ug[i]) * W.amt[i], 2),
                         "LN %s UPFRONT FEE REFUND" % I.sba[i]))
    for i, (sd, price, dealer) in S.items():
        if lo <= sd:
            g = (1 - W.ug[i]) * W.amt[i]
            rows.append((sd, tr(), "SBA FTA", "SEC MKT SETL", round(g * price / 100.0, 2), "LN %s GTD PORTION SALE" % I.sba[i]))
    rows = [r for r in rows if lo <= r[0] <= K.RESERVE_DATE]
    rows.sort(key=lambda r: (r[0], r[1]))
    return [{"settlement_date": r[0].isoformat(), "trace_no": r[1], "originator": r[2], "entry_description": r[3],
             "amount": "%.2f" % r[4], "addenda": r[5]} for r in rows]


def old_module(B):
    """Loans whose case the old module carries: charged off before the new module went live."""
    return {i for i, d, amt in B.co if d < MODULE_SWITCH}


def ask_goldens(W, A, B):
    """Ask A by the instalment's fiscal quarter; Ask B by fiscal year and approval fiscal year (pool loans only)."""
    pool = lambda i: K.POOL_FY[0] <= W.fy[i] <= K.POOL_FY[1]
    qa = {}
    for i, mm, a, due, prog, rd, tr, tot in A.instalments:
        if pool(i) and ASK_A_FIRST <= mm <= ASK_A_LAST:
            q = K.fq_label(mm)
            qa[q] = qa.get(q, 0.0) + a
    nb = {(fy, v): 0.0 for fy in ASK_B_FYS for v in range(K.POOL_FY[0], K.POOL_FY[1] + 1)}
    for i, d, amt in B.co:
        f = K.fy_of_date(d)
        if pool(i) and (f, int(W.fy[i])) in nb:
            nb[(f, int(W.fy[i]))] += amt
    for i, d, gross, bank, sba, kind in B.receipts:
        f = K.fy_of_date(d)
        if pool(i) and (f, int(W.fy[i])) in nb:
            nb[(f, int(W.fy[i]))] -= bank
    for i, d, amt in B.top:
        f = K.fy_of_date(d)
        if pool(i) and (f, int(W.fy[i])) in nb:
            nb[(f, int(W.fy[i]))] -= amt
    return dict(sorted(qa.items())), nb
