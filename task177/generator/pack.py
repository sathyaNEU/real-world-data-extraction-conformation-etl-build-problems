"""task177 pack: every file under target/, written from the world the way each system would export it.

Public side: the loan book at 31 December 2026 (legacy loans that were still open in June 2021 carried into the new
core under new numbers, the rest kept under their legacy numbers), the crosswalk, the Tesoreria's deduction returns,
the default register, the receipts on defaulted loans and the members' savings ledger.
Private side: the employers' payroll registers, the agreements register, the launch disbursement file, the savings
contribution schedules and the collection account statement.
Documents: the product rules, the data dictionary, the supervisor's annual return and the labour market bulletin."""
from __future__ import annotations

import datetime as dt
import math
import os

import numpy as np

import common as C
import world as W

TEND = W.TEND
LEGACY_END = C.mi(*C.CORE_MOVE) - 1      # June 2021, the legacy core's last month


def iso(d):
    return d.isoformat()


def mstr_old(i):
    y, m = C.ym(i)
    return "%04d%02d" % (y, m)


def mstr(i):
    y, m = C.ym(i)
    return "%04d-%02d" % (y, m)


# ------------------------------------------------------------------------------------------------- the loan book
def loan_numbers(P):
    rng = C.stream("loan_numbers")
    n = P["n"]
    legacy = np.array(["PL%07d" % x for x in rng.choice(np.arange(1_000_000, 9_999_999), n, replace=False)])
    newno = np.array([""] * n, dtype=object)
    # a loan disbursed from July 2021 has a new-core number; a legacy loan still open at the move got one too
    seq = 1
    order = np.argsort(P["disb"], kind="stable")
    closed_before = (P["end_m"] >= 0) & (P["end_m"] <= LEGACY_END)
    for i in order:
        if P["disb"][i] > LEGACY_END:
            y, _ = C.ym(int(P["disb"][i]))
            newno[i] = "LB%02d%06d" % (y % 100, seq)
            seq += 1
    seq_m = 1
    for i in order:
        if P["disb"][i] <= LEGACY_END and not closed_before[i]:
            newno[i] = "LB21M%05d" % seq_m
            seq_m += 1
    migrated = (P["disb"] <= LEGACY_END) & ~closed_before
    return legacy, newno, migrated, closed_before


def ref_at(P, legacy, newno, i, month):
    """the loan reference a system used in a month: legacy before the move, the new number after"""
    if P["disb"][i] > LEGACY_END:
        return newno[i]
    return legacy[i] if month <= LEGACY_END or not newno[i] else newno[i]


def write_loans(out, P, legacy, newno, migrated, closed_before):
    A = P["A"]
    rows = []
    rng = C.stream("loan_book")
    CT_NEW = {False: ("CARRERA", "LIBRE NOMBRAMIENTO"), True: ("TEMPORAL",)}
    for i in np.argsort(P["disb"], kind="stable"):
        legacy_row = P["disb"][i] <= LEGACY_END
        no = newno[i] if newno[i] else legacy[i]
        temp = bool(P["temp"][i])
        if legacy_row:
            ct = "T" if temp else "P"
        else:
            ct = CT_NEW[temp][0] if temp else CT_NEW[False][int(rng.random() < 0.18)]
        st = P["status"][i]
        end = P["end_m"][i]
        if P["dflt_m"][i] >= 0:
            channel, closed, reason = "COBRANZA", "", ""
        elif st == 1 and end <= TEND:
            channel, closed, reason = "CERRADO", iso(C.month_end(int(end))), "VENCIMIENTO"
        elif st == 2 and end <= TEND:
            channel, closed, reason = "CERRADO", iso(dt.date(*C.ym(int(end)), int(rng.integers(3, 27)))), "COMPRA DE CARTERA"
        elif st == 4 and end <= TEND:
            channel, closed, reason = "DEBITO DIRECTO", "", ""
        else:
            channel, closed, reason = "NOMINA", "", ""
        # the direct-billed loans that ran to maturity inside the record are closed
        if channel == "DEBITO DIRECTO" and P["disb"][i] + P["term"][i] <= TEND:
            channel, closed, reason = "CERRADO", iso(C.month_end(int(P["disb"][i] + P["term"][i]))), "VENCIMIENTO"
        scale = 1000.0 if legacy_row else 1.0
        prin = P["principal"][i] / scale
        inst = P["inst"][i] / scale
        rows.append((no, int(P["member"][i]), A[P["ag"][i]]["code"], A[P["ag"][i]]["type"], ct,
                     iso(C.month_start(int(P["hire"][i]))), int(P["birth"][i]),
                     ("%.1f" % (P["pay"][i] / 1000.0)) if legacy_row else "%d" % P["pay"][i],
                     iso(dt.date(*C.ym(int(P["disb"][i])), int(rng.integers(1, 26)))),
                     ("%.1f" % prin) if legacy_row else "%d" % prin, int(P["term"][i]), "%.4f" % P["rate"][i],
                     ("%.1f" % inst) if legacy_row else "%d" % inst, channel, closed, reason,
                     "LEGACY" if legacy_row else "CORE"))
    head = ("loan_no", "member_id", "payroll_unit", "unit_type", "contract_type", "hire_date", "birth_year",
            "net_pay_at_origination", "disbursement_date", "principal", "term_months", "monthly_rate", "instalment",
            "collection_channel", "closed_date", "closure_reason", "origin_system")
    return C.write_csv(os.path.join(out, C.F_LOANS), head, rows)


def write_crosswalk(out, P, legacy, newno, migrated):
    rows = [(legacy[i], newno[i], "2021-07-01") for i in np.argsort(P["disb"], kind="stable") if migrated[i]]
    return C.write_csv(os.path.join(out, C.F_XWALK), ("legacy_loan_no", "core_loan_no", "migrated_on"), rows)


def write_returns(out, P, legacy, newno):
    A = P["A"]
    rng = C.stream("returns")
    rows = []
    rets = sorted(P["returns"], key=lambda r: (r[1], A[P["ag"][r[0]]]["code"], r[0]))
    resent = {C.mi(2019, 8), C.mi(2022, 3), C.mi(2025, 10)}           # months the Tesoreria sent twice
    for i, t, code in rets:
        if t > TEND:
            continue
        old = t < C.mi(*C.RET_LAYOUT)
        ref = ref_at(P, legacy, newno, i, t)
        amt = P["inst"][i]
        r = (mstr_old(t) if old else mstr(t), A[P["ag"][i]]["code"], int(P["member"][i]), ref,
             ("%d" % amt) if old else "%.2f" % amt, ({"SIN SALARIO": "01", "SIN CUPO": "02"}[code]) if old else code)
        rows.append(r)
        if t in resent:
            rows.append(r)
    head = ("period", "payroll_unit", "national_id", "loan_reference", "amount", "reason")
    return C.write_csv(os.path.join(out, C.F_RETURNS), head, rows)


def default_balance(P, i):
    k = int(P["dflt_m"][i] - P["disb"][i]) - 3          # instalments paid before the three missed
    return C.balance_after(P["principal"][i], P["rate"][i], int(P["term"][i]), max(0, k))


def write_defaults(out, P, legacy, newno, cures):
    rows = []
    idx = [i for i in np.argsort(P["dflt_m"], kind="stable") if P["dflt_m"][i] >= 0]
    for i in idx:
        t = int(P["dflt_m"][i])
        ref = ref_at(P, legacy, newno, i, t)
        cure = cures.get(i)
        rows.append((ref, int(P["member"][i]), iso(C.month_end(t)), "%.0f" % default_balance(P, i),
                     iso(cure) if cure else ""))
    head = ("loan_reference", "member_id", "default_date", "balance_at_default", "cure_date")
    return C.write_csv(os.path.join(out, C.F_DEFAULTS), head, rows)


# --------------------------------------------------------------------------- recoveries on defaulted public loans
def recoveries(P):
    """receipts on every defaulted loan from January 2023, the members' savings and the netting of them"""
    rng = C.stream("recoveries")
    first = C.mi(2023, 1)
    idx = [i for i in range(P["n"]) if P["dflt_m"][i] >= 0 and P["dflt_m"][i] >= C.mi(2020, 1)]
    acct_used = set()

    def acct():
        while True:
            a = "0731-%08d" % int(rng.integers(10_000_000, 99_999_999))
            if a not in acct_used:
                acct_used.add(a)
                return a
    BANKS = ("0007", "0013", "0019", "0023", "0040", "0051", "0052", "0060", "0062")
    receipts = []      # (date, loan i, channel, origin, amount, kind)  kind: cash, own, other
    savings = {}       # member -> dict(acct, moves)
    cures = {}
    mem_of = {}
    for i in idx:
        m = int(P["member"][i])
        if m not in savings:
            bal = float(np.round(rng.lognormal(np.log(2_400_000), 0.65), -3)) if rng.random() < 0.82 else 0.0
            savings[m] = dict(acct=acct(), opening=bal, moves=[])
        mem_of[i] = m
    others = []         # members who pay for a relative from their own savings
    for _ in range(1400):
        m = int(rng.integers(10_000_000, 99_999_999))
        if m in savings:
            continue
        savings[m] = dict(acct=acct(), opening=float(np.round(rng.lognormal(np.log(3_100_000), 0.6), -3)), moves=[])
        others.append(m)
    for i in idx:
        t0 = int(P["dflt_m"][i])
        bal = default_balance(P, i)
        m = mem_of[i]
        sv = savings[m]
        owed = bal
        # netting of the member's own savings, one or two months after default
        if sv["opening"] >= 150_000 and rng.random() < 0.58:
            tn = t0 + int(rng.choice([1, 2]))
            amt = float(min(sv["opening"] * float(rng.uniform(0.85, 1.0)), owed))
            amt = float(np.round(amt, 0))
            d = C.business_day(dt.date(*C.ym(tn), int(rng.integers(2, 26))))
            receipts.append((d, i, "TRANSFERENCIA", sv["acct"], amt, "own"))
            sv["moves"].append((d, "RETIRO", -amt))
            owed -= amt
        # a payment plan, a settlement or nothing
        u = rng.random()
        if u < 0.36:
            start = t0 + int(rng.integers(1, 6))
            nmon = int(rng.integers(3, 20))
            pay = float(np.round(P["inst"][i] * float(rng.uniform(0.4, 1.0)), -3))
            src_kind = rng.random()
            for t in range(start, start + nmon):
                if owed <= 0:
                    break
                if rng.random() < 0.18:
                    continue
                d = C.business_day(dt.date(*C.ym(t), int(rng.integers(1, 28))))
                a = float(min(pay, owed))
                if src_kind < 0.55:
                    ch, org = "TRANSFERENCIA", "%s-%010d" % (BANKS[int(rng.integers(0, len(BANKS)))], int(rng.integers(10**9, 10**10 - 1)))
                elif src_kind < 0.88:
                    ch, org = "CAJA", ""
                else:
                    ch, org = "TRANSFERENCIA", "rel"
                receipts.append((d, i, ch, org, a, "cash" if org != "rel" else "other"))
                owed -= a
            if owed < 0.05 * bal and rng.random() < 0.7 and start + nmon <= TEND:
                cures[i] = dt.date(*C.ym(start + nmon), 28)
        elif u < 0.46:
            t = t0 + int(rng.integers(2, 20))
            a = float(np.round(owed * float(rng.uniform(0.55, 0.9)), -3))
            d = C.business_day(dt.date(*C.ym(t), int(rng.integers(1, 28))))
            org = "%s-%010d" % (BANKS[int(rng.integers(0, len(BANKS)))], int(rng.integers(10**9, 10**10 - 1)))
            if a > 0:
                receipts.append((d, i, "TRANSFERENCIA", org, a, "cash"))
    # every default year and unit type of 2023 and 2024 has at least one plan instalment paid from a relative's account
    A = P["A"]
    have = set()
    for r in receipts:
        if r[3] == "rel":
            have.add((C.ym(int(P["dflt_m"][r[1]]))[0], A[P["ag"][r[1]]]["type"]))
    for y in (2023, 2024):
        for typ in C.AGENCY_TYPES:
            if (y, typ) in have:
                continue
            cand = [k for k, r in enumerate(receipts) if r[5] == "cash" and r[2] == "TRANSFERENCIA" and
                    C.ym(int(P["dflt_m"][r[1]]))[0] == y and A[P["ag"][r[1]]]["type"] == typ and
                    C.mi(r[0].year, r[0].month) <= TEND]
            k = cand[int(rng.integers(0, len(cand)))]
            d, i, ch, org, a, kind = receipts[k]
            receipts[k] = (d, i, ch, "rel", a, "other")
    # a relative's own cooperative savings account pays some of the plan instalments
    rel_rows = []
    for r in receipts:
        if r[3] == "rel":
            m2 = others[int(rng.integers(0, len(others)))]
            savings[m2]["moves"].append((r[0], "RETIRO", -r[4]))
            rel_rows.append((r[0], r[1], r[2], savings[m2]["acct"], r[4], "other"))
        else:
            rel_rows.append(r)
    receipts = [r for r in rel_rows if C.mi(r[0].year, r[0].month) >= first and C.mi(r[0].year, r[0].month) <= TEND]
    return receipts, savings, cures


def write_receipts(out, P, legacy, newno, receipts):
    rng = C.stream("receipts_out")
    rows = []
    n = 0
    for d, i, ch, org, a, kind in sorted(receipts, key=lambda r: (r[0], r[1])):
        n += 1
        t = C.mi(d.year, d.month)
        ref = ref_at(P, legacy, newno, i, t)
        rid = "RC%02d%06d" % (d.year % 100, n)
        rows.append((rid, iso(d), ref, int(P["member"][i]), ch, org, "%.0f" % a))
        if ch == "TRANSFERENCIA" and kind == "cash" and rng.random() < 0.025:
            d2 = C.business_day(d + dt.timedelta(days=int(rng.integers(1, 4))))
            if C.mi(d2.year, d2.month) <= TEND:
                rows.append((rid + "R", iso(d2), ref, int(P["member"][i]), "REVERSO", org, "-%.0f" % a))
                n += 1
                d3 = C.business_day(d2 + dt.timedelta(days=int(rng.integers(2, 9))))
                if C.mi(d3.year, d3.month) <= TEND:
                    rows.append(("RC%02d%06d" % (d3.year % 100, n), iso(d3), ref, int(P["member"][i]), ch, org, "%.0f" % a))
    head = ("receipt_id", "receipt_date", "loan_reference", "member_id", "channel", "originating_account", "amount")
    return C.write_csv(os.path.join(out, C.F_RECEIPTS), head, rows)


def write_savings(out, savings):
    rng = C.stream("savings_ledger")
    rows = []
    start = dt.date(2023, 1, 1)
    for m in sorted(savings):
        sv = savings[m]
        bal = sv["opening"]
        moves = []
        # monthly contributions and the December interest credit, for members still contributing
        contrib = float(np.round(bal * 0.02, -3)) if bal > 0 else 0.0
        for t in range(C.mi(2023, 1), TEND + 1):
            y, mo = C.ym(t)
            if contrib and rng.random() < 0.65:
                moves.append((dt.date(y, mo, int(rng.integers(26, 29))), "APORTE", contrib))
            if mo == 12:
                moves.append((dt.date(y, 12, 31), "INTERES", None))
        for d, k, a in sv["moves"]:
            if d <= dt.date(2026, 12, 31):
                moves.append((d, k, a))
        if not sv["moves"] and rng.random() < 0.12:
            d = dt.date(2023 + int(rng.integers(0, 4)), int(rng.integers(1, 13)), int(rng.integers(1, 28)))
            moves.append((d, "RETIRO", -float(np.round(bal * float(rng.uniform(0.1, 0.4)), -3))))
        moves.sort(key=lambda r: (r[0], {"APORTE": 0, "RETIRO": 1, "INTERES": 2}[r[1]]))
        rows.append((sv["acct"], m, iso(start), "SALDO INICIAL", "%.0f" % bal, "%.0f" % bal))
        for d, k, a in moves:
            if k == "INTERES":
                a = float(np.round(max(bal, 0) * 0.035, 0))
            if a is None or a == 0:
                continue
            if k == "RETIRO" and -a > bal + 1:
                a = -float(np.round(bal, 0))
                if a == 0:
                    continue
            bal += a
            rows.append((sv["acct"], m, iso(d), k, "%.0f" % a, "%.0f" % bal))
    head = ("savings_account", "member_id", "movement_date", "movement", "amount", "balance")
    return C.write_csv(os.path.join(out, C.F_SAVINGS), head, rows)


# ---------------------------------------------------------------------------------------------- the private side
def emp_id(x, t):
    """the employee id as the intake portal stored it: with the document prefix and dots until June 2026"""
    if t < C.mi(*C.PORTAL_UPGRADE):
        return "CC " + C.dotted(x)
    return str(x)


def periods(e, t):
    """the pay periods of month t for an employer"""
    y, m = C.ym(t)
    last = C.month_end(t).day
    if e["freq"] == "F":
        return [(dt.date(y, m, 1), dt.date(y, m, 15), C.business_day(dt.date(y, m, 15), back=True)),
                (dt.date(y, m, 16), dt.date(y, m, last), C.business_day(dt.date(y, m, last), back=True))]
    pd_ = min(e["pay_day"], last)
    return [(dt.date(y, m, 1), dt.date(y, m, last), C.business_day(dt.date(y, m, pd_), back=True))]


def write_registers(out, E, people):
    rng = C.stream("registers")
    rows = []
    reg_no = {e["i"]: 1 for e in E}
    by_emp = {}
    for s in people:
        by_emp.setdefault(s["emp"], []).append(s)
    for e in E:
        staff = by_emp[e["i"]]
        for t in range(e["start"], TEND + 1):
            y, m = C.ym(t)
            ps = periods(e, t)
            for j, (a, b, pdate) in enumerate(ps):
                lastp = j == len(ps) - 1
                regs = []
                no = "%s-%04d" % (str(e["nit_base"])[-4:], reg_no[e["i"]])
                reg_no[e["i"]] += 1
                for s in staff:
                    if s["hire"] > t or (s["leave"] is not None and s["leave"] < t):
                        continue
                    if s["hire"] == t and e["freq"] == "F" and j == 0 and rng.random() < 0.5:
                        continue
                    if any(st <= t < st + d for st, d in s["unpaid"]):
                        continue
                    leaving = s["leave"] == t and lastp
                    if s["leave"] == t and not lastp and e["freq"] == "F" and rng.random() < 0.3:
                        continue
                    share = 0.5 if e["freq"] == "F" else 1.0
                    gross = s["base"] * share * float(rng.uniform(1.0, 1.12))
                    ptype = "NOMINA"
                    if leaving:
                        ptype = "LIQUIDACION"
                        gross += s["base"] * float(rng.uniform(0.6, 2.2))
                    ded = gross * float(rng.uniform(0.09, 0.13))
                    if s.get("join") is not None and s["join"] <= t and lastp and not leaving:
                        ded += s["saving"]
                    regs.append((e["nit"], no, iso(a), iso(b), iso(pdate), ptype, emp_id(s["id"], t),
                                 iso(C.month_start(s["hire"])), "%.0f" % s["base"], "%.0f" % gross, "%.0f" % ded,
                                 "%.0f" % (gross - ded)))
                rows.extend(regs)
                if rng.random() < 0.02:
                    rows.extend(regs)              # the employer uploaded the register twice
            if m in (6, 12):
                no = "%s-%04d" % (str(e["nit_base"])[-4:], reg_no[e["i"]])
                reg_no[e["i"]] += 1
                pdate = C.business_day(dt.date(y, m, 30 if m == 6 else 18), back=True)
                for s in staff:
                    if s["hire"] > t or (s["leave"] is not None and s["leave"] <= t):
                        continue
                    months = min(6, t - s["hire"] + 1)
                    g = s["base"] * months / 12.0
                    rows.append((e["nit"], no, iso(dt.date(y, m - 5, 1)), iso(C.month_end(t)), iso(pdate), "PRIMA",
                                 emp_id(s["id"], t), iso(C.month_start(s["hire"])), "%.0f" % s["base"], "%.0f" % g, "0",
                                 "%.0f" % g))
    head = ("employer_nit", "register_no", "period_start", "period_end", "pay_date", "payment_type", "employee_id",
            "hire_date", "base_salary", "gross_pay", "deductions", "net_pay")
    return C.write_csv(os.path.join(out, C.F_REGISTERS), head, rows)


def write_launch(out, E, B):
    rows = []
    for k, s in enumerate(sorted(B, key=lambda s: (E[s["emp"]]["nit"], s["id"]))):
        e = E[s["emp"]]
        rows.append(("LE27%05d" % (k + 1), s["id"], e["nit"], iso(C.month_start(s["hire"])),
                     iso(C.month_start(s["join"])), "%.0f" % s["net"], "%.0f" % s["principal"], s["term"],
                     "%.4f" % s["rate"], "%.0f" % s["inst"], iso(C.DISBURSE), "2027-02"))
    head = ("loan_no", "member_id", "employer_nit", "hire_date", "member_since", "certified_net_pay", "principal",
            "term_months", "monthly_rate", "instalment", "disbursement_date", "first_deduction_period")
    return C.write_csv(os.path.join(out, C.F_LAUNCH), head, rows)


def schedules(E, people):
    """the monthly savings contribution schedules, their corrections and supplements, and the transfers"""
    rng = C.stream("schedules")
    by_emp = {}
    for s in people:
        if s.get("join") is not None:
            by_emp.setdefault(s["emp"], []).append(s)
    sched = []      # dict(no, emp, period, rows[(id, amt)], kind 'first'|'replacement'|'supplement', filed date, replaces)
    seq = 1
    for e in E:
        members = by_emp.get(e["i"], [])
        for t in range(e["start"], TEND + 1):
            rows = []
            for s in members:
                if s["join"] <= t and (s["leave"] is None or s["leave"] > t) and not any(st <= t < st + d for st, d in s["unpaid"]):
                    rows.append((s["id"], s["saving"]))
            if not rows:
                continue
            y, m = C.ym(t)
            filed = C.month_end(t) + dt.timedelta(days=int(rng.integers(1, 6)))
            first = dict(no="PA%06d" % seq, emp=e["i"], period=t, rows=rows, kind="first", filed=filed, replaces=None)
            seq += 1
            sched.append(first)
            u = rng.random()
            if u < 0.075:
                # a corrected schedule for the period replaces the first: the same members, a few amounts changed,
                # one member dropped or added
                rows2 = [(i, a if rng.random() > 0.08 else float(np.round(a * float(rng.choice([0.5, 1.5, 2.0])), -3)))
                         for i, a in rows]
                if len(rows2) > 3 and rng.random() < 0.5:
                    rows2.pop(int(rng.integers(0, len(rows2))))
                sched.append(dict(no="PA%06d" % seq, emp=e["i"], period=t, rows=rows2, kind="replacement",
                                  filed=filed + dt.timedelta(days=int(rng.integers(2, 9))), replaces=first["no"]))
                seq += 1
                first["replaced"] = True
            elif u < 0.13 and len(rows) > 4:
                # members left off the month's schedule are filed in a supplement a few days later
                k = int(rng.integers(1, 4))
                pick = set(int(j) for j in rng.choice(len(rows), k, replace=False))
                extra = [r for j, r in enumerate(rows) if j in pick]
                first["rows"] = [r for j, r in enumerate(rows) if j not in pick]
                sched.append(dict(no="PA%06d" % seq, emp=e["i"], period=t, rows=extra, kind="supplement",
                                  filed=filed + dt.timedelta(days=int(rng.integers(3, 15))), replaces=None))
                seq += 1
    # every sector gets at least one corrected schedule in 2026
    for sec in C.SECTORS:
        cands = [x for x in sched if x["kind"] == "first" and E[x["emp"]]["sector"] == sec and x["period"] >= C.mi(2026, 1)]
        if not any(x.get("replaced") for x in cands):
            x = cands[int(rng.integers(0, len(cands)))]
            rows2 = [(i, a if j % 7 else float(np.round(a * 2, -3))) for j, (i, a) in enumerate(x["rows"])]
            sched.append(dict(no="PA%06d" % seq, emp=x["emp"], period=x["period"], rows=rows2, kind="replacement",
                              filed=x["filed"] + dt.timedelta(days=4), replaces=x["no"]))
            seq += 1
            x["replaced"] = True
    return sched


def transfers(E, sched):
    """the employers' transfers into the collection account: one per effective schedule, the groups' parents paying
    for their subsidiaries in one transfer, a few late, two employers behind, one transfer returned and sent again"""
    rng = C.stream("transfers")
    parent_of = {}
    for e in E:
        if e["group"]:
            parent = [x for x in E if x["name"] == W.GROUP_PARENT[e["group"]]][0]
            if parent["i"] != e["i"]:
                parent_of[e["i"]] = parent["i"]
    behind = {E[[x["name"] for x in E].index("Moda Urbana Sorana S.A.S.")]["i"]: (C.mi(2026, 8), C.mi(2026, 11)),
              E[[x["name"] for x in E].index("Escoltas y Custodia Monteralto Ltda.")]["i"]: (C.mi(2026, 5), C.mi(2026, 7))}
    eff = [x for x in sched if not x.get("replaced")]
    tot = lambda x: float(sum(a for _, a in x["rows"]))
    out = []          # (date, payer emp index, amount, period, covers [schedule nos])
    by_key = {}
    for x in eff:
        by_key.setdefault((x["emp"], x["period"], x["kind"] == "supplement"), []).append(x)
    done = set()
    for x in sorted(eff, key=lambda x: (x["period"], x["emp"], x["no"])):
        if x["no"] in done:
            continue
        e = x["emp"]
        payer = parent_of.get(e, e)
        covers = [x]
        if x["kind"] != "supplement":
            if payer == e:
                kids = [k for k, p in parent_of.items() if p == e]
                for k in kids:
                    for y in by_key.get((k, x["period"], False), []):
                        covers.append(y)
            else:
                # the subsidiary's schedule is paid with the parent's
                continue
        amt = sum(tot(c) for c in covers)
        if e in behind and behind[e][0] <= x["period"] <= behind[e][1]:
            continue
        lag = int(rng.choice([3, 5, 7, 9, 12, 16, 24, 38], p=[0.18, 0.2, 0.18, 0.14, 0.12, 0.08, 0.06, 0.04]))
        d = max(c["filed"] for c in covers) + dt.timedelta(days=lag)
        for c in covers:
            done.add(c["no"])
        out.append((d, payer, amt, x["period"], [c["no"] for c in covers]))
    # the arrears are paid off in two lumps, one of them after the year end
    for e, (a, b) in behind.items():
        owed = [x for x in eff if x["emp"] == e and a <= x["period"] <= b]
        part = owed[:2]
        out.append((dt.date(2026, 12, 21), parent_of.get(e, e), sum(tot(c) for c in part), part[0]["period"],
                    [c["no"] for c in part]))
    return out, parent_of


def write_schedules(out, E, sched):
    rows = []
    for x in sorted(sched, key=lambda x: (x["filed"], x["no"])):
        e = E[x["emp"]]
        for i, a in x["rows"]:
            rows.append((x["no"], e["nit"], mstr(x["period"]), iso(x["filed"]), i, "%.0f" % a))
    head = ("schedule_no", "employer_nit", "period", "filed_on", "member_id", "contribution")
    return C.write_csv(os.path.join(out, C.F_SCHED), head, rows)


def write_statement(out, E, tr, people):
    rng = C.stream("statement")
    lines = []
    for d, payer, amt, per, covers in tr:
        if C.business_day(d) > dt.date(2026, 12, 31):
            continue
        e = E[payer]
        y, m = C.ym(per)
        lines.append((C.business_day(d), "TRANSFERENCIA RECIBIDA", e["nit"], e["name"].upper().replace(".", ""), "APORTES %02d/%04d" % (m, y), amt, 0.0))
    # one transfer returned by the paying bank and sent again a few days later
    pick = [k for k, l in enumerate(lines) if dt.date(2026, 3, 1) <= l[0] <= dt.date(2026, 9, 30)]
    k = pick[int(rng.integers(0, len(pick)))]
    d, desc, nit, nm, ref, amt, _ = lines[k]
    lines.append((C.business_day(d + dt.timedelta(days=2)), "DEVOLUCION TRANSFERENCIA", nit, nm, ref, 0.0, amt))
    lines.append((C.business_day(d + dt.timedelta(days=6)), "TRANSFERENCIA RECIBIDA", nit, nm, ref, amt, 0.0))
    # members' own deposits and the account's charges
    mem = [s for s in people if s.get("join") is not None]
    for _ in range(2600):
        s = mem[int(rng.integers(0, len(mem)))]
        dd = C.business_day(dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(0, 728))))
        if s["join"] > C.mi(dd.year, dd.month):
            continue
        lines.append((dd, "CONSIGNACION", str(s["id"]), "", "APORTE VOLUNTARIO", float(np.round(float(rng.uniform(20, 400)), 0) * 1000), 0.0))
    for t in range(C.mi(2025, 1), TEND + 1):
        lines.append((C.month_end(t), "COMISION MANEJO CUENTA", "", "", "", 0.0, 38_500.0))
        lines.append((C.month_end(t), "GMF 4X1000", "", "", "", 0.0, float(np.round(float(rng.uniform(150_000, 420_000)), 0))))
    lines.sort(key=lambda l: (l[0], l[1], l[2]))
    rows = []
    bal = 0.0
    for d, desc, nit, nm, ref, cr, db in lines:
        bal += cr - db
        rows.append((iso(d), desc, nit, nm, ref, "%.0f" % cr if cr else "", "%.0f" % db if db else "", "%.0f" % bal))
    head = ("posting_date", "description", "payer_id", "payer_name", "reference", "credit", "debit", "balance")
    return C.write_csv(os.path.join(out, C.F_STMT), head, rows)


def write_labour(out):
    rng = C.stream("labour")
    rows = []
    secs = ("Comercio al por menor", "Servicios administrativos y de apoyo", "Transporte y almacenamiento",
            "Industria manufacturera de alimentos", "Actividades de atencion de la salud", "Administracion publica",
            "Educacion", "Total nacional")
    base = {s: float(rng.uniform(6.5, 13.5)) for s in secs}
    emp = {s: float(rng.uniform(250, 2600)) for s in secs}
    for y in (2023, 2024, 2025, 2026):
        for q in (1, 2, 3, 4):
            if y == 2026 and q == 4:
                continue
            for s in secs:
                u = base[s] + float(rng.normal(0, 0.45)) - 0.25 * (y - 2023)
                emp[s] *= float(1 + rng.normal(0.004, 0.006))
                rows.append(("%dT%d" % (y, q), s, "%.1f" % u, "%.1f" % emp[s]))
    head = ("trimestre", "rama_actividad", "tasa_desempleo_pct", "ocupados_miles")
    return C.write_csv(os.path.join(out, C.F_LABOUR), head, rows)


def build_pack(out):
    import docs
    os.makedirs(out, exist_ok=True)
    Wd = W.world()
    P, E, people, B = Wd["P"], Wd["E"], Wd["people"], Wd["B"]
    legacy, newno, migrated, closed_before = loan_numbers(P)
    receipts, savings, cures = recoveries(P)
    sched = schedules(E, people)
    tr, parent_of = transfers(E, sched)
    n = {}
    n[C.F_LOANS] = write_loans(out, P, legacy, newno, migrated, closed_before)
    n[C.F_XWALK] = write_crosswalk(out, P, legacy, newno, migrated)
    n[C.F_RETURNS] = write_returns(out, P, legacy, newno)
    n[C.F_DEFAULTS] = write_defaults(out, P, legacy, newno, cures)
    n[C.F_RECEIPTS] = write_receipts(out, P, legacy, newno, receipts)
    n[C.F_SAVINGS] = write_savings(out, savings)
    n[C.F_REGISTERS] = write_registers(out, E, people)
    n[C.F_LAUNCH] = write_launch(out, E, B)
    n[C.F_SCHED] = write_schedules(out, E, sched)
    n[C.F_STMT] = write_statement(out, E, tr, people)
    n[C.F_LABOUR] = write_labour(out)
    docs.write_agreements(out, E)
    docs.write_rules(out)
    docs.write_dictionary(out)
    docs.write_supervisor(out, P)
    return n


if __name__ == "__main__":
    import sys
    o = sys.argv[1]
    print(build_pack(o))


# ------------------------------------------------------------------------------------------- the asks' clean truth
def ask_truth():
    """Ask A and Ask B from the world's own objects (which schedule replaced which, which transfer paid which
    schedules, which receipts netted the member's own savings), before any file is written"""
    Wd = W.world()
    P, E, people = Wd["P"], Wd["E"], Wd["people"]
    sched = schedules(E, people)
    tr, parent_of = transfers(E, sched)
    eff = {x["no"]: x for x in sched if not x.get("replaced")}
    paid = set()
    for d, payer, amt, per, covers in tr:
        if C.business_day(d) <= dt.date(2026, 12, 31):
            paid.update(covers)
    ded = {s: 0.0 for s in C.SECTORS}
    out = {s: 0.0 for s in C.SECTORS}
    for no, x in eff.items():
        if C.ym(x["period"])[0] != 2026:
            continue
        sec = E[x["emp"]]["sector"]
        t = float(sum(a for _, a in x["rows"]))
        ded[sec] += t
        if no not in paid:
            out[sec] += t
    receipts, savings, cures = recoveries(P)
    A = P["A"]
    rec = {y: {k: 0.0 for k in C.AGENCY_TYPES} for y in (2023, 2024)}
    for d, i, ch, org, a, kind in receipts:
        y = C.ym(int(P["dflt_m"][i]))[0]
        if y in rec and kind != "own":
            rec[y][A[P["ag"][i]]["type"]] += float("%.0f" % a)
    return dict(deducted=ded, outstanding=out, recovered=rec, sched=sched, tr=tr, receipts=receipts,
                parent_of=parent_of)
