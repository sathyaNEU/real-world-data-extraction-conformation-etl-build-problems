"""The payoff desk's records behind the ask: the payoff statement system's log from October 2025 and the desk's manual
log for the fortnight in March 2026 when the statement system was down for its upgrade. Every payoff statement is
generated from an event in the clean truth (a closing on a sale or a refinance, a member paying a loan off, a closing that
fell through), so the log ties to the core's payoffs wherever a statement was issued."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np

import common as K
import records as R
import world as WD

F_LOG = "payoff_statement_log_2025-10_2026-11.csv"
F_MANUAL = "payoff_statements_manual_2026-03.xlsx"

WIN0 = dt.date(2025, 10, 1)
WIN1 = dt.date(2026, 11, 30)
OUT0 = dt.date(2026, 3, 9)          # the statement system's upgrade outage, both days included
OUT1 = dt.date(2026, 3, 20)
QUARTERS = [("2025Q4", dt.date(2025, 10, 1), dt.date(2025, 12, 31)), ("2026Q1", dt.date(2026, 1, 1), dt.date(2026, 3, 31)),
            ("2026Q2", dt.date(2026, 4, 1), dt.date(2026, 6, 30)), ("2026Q3", dt.date(2026, 7, 1), dt.date(2026, 9, 30))]

AGENCIES = {
    "GR": ["Larchwick Title Agency", "Ironbridge Title & Escrow", "Northgate Settlement Co.", "Cedar Lantern Title"],
    "LS": ["Bluewater Escrow & Title", "Dune Grass Title Agency", "Foxglove Closing Services"],
    "KB": ["Kettle Creek Title Co.", "Harvest Moon Title Agency", "Ironbridge Title & Escrow"],
    "MN": ["Pine Barrens Title Agency", "Sandhill Closing Services", "Northgate Settlement Co."],
}
STAFF = ["CL", "MV", "TR", "JD", "AK"]
NATIONAL = ["Ashgrove National Title", "Centerline Settlement Services"]


def eastern_offset(d):
    """hours to add to Eastern local time to get UTC"""
    y = d.year
    mar = dt.date(y, 3, 8)
    while mar.weekday() != 6:
        mar += dt.timedelta(days=1)
    nov = dt.date(y, 11, 1)
    while nov.weekday() != 6:
        nov += dt.timedelta(days=1)
    return 4 if mar <= d < nov else 5


def stamp(d, g):
    hh = int(g.integers(8, 18))
    mm = int(g.integers(0, 60))
    ss = int(g.integers(0, 60))
    local = dt.datetime(d.year, d.month, d.day, hh, mm, ss)
    return local + dt.timedelta(hours=eastern_offset(d))


def payoff_amount(bal, rate, days):
    return round(bal + bal * rate / 100.0 / 365.0 * days + 25.0, 2)


class Event:
    __slots__ = ("i", "kind", "close", "he_bal", "mtg", "mtg_bal", "heloc", "heloc_bal", "who")


def events(W, ids, heloc):
    """every closing or payoff that asked for a statement in the window, with what each statement had to cover"""
    ev = []
    for i in range(W.n):
        ex = int(W.exit_m[i])
        if ex < 0 or W.exit_kind[i] not in ("SALE", "REFI", "PAYOFF"):
            continue
        d = W.exit_day[i]
        if not (WIN0 + dt.timedelta(days=6) <= d <= WIN1 + dt.timedelta(days=45)):
            continue
        e = Event()
        e.i, e.kind, e.close = i, W.exit_kind[i], d
        e.he_bal = float(W.exit_bal[i])
        e.mtg = ids.mtg_loan.get(i) if W.exit_kind[i] in ("SALE", "REFI") else None
        e.mtg_bal = float(WD.sched_balance(W.F0[i], W.r1[i], W.n1[i], ex - int(W.o1[i]))) if e.mtg else 0.0
        e.heloc, e.heloc_bal, e.who = None, 0.0, "agency"
        if W.exit_kind[i] == "PAYOFF":
            e.who = "member" if K.rng(60, i).random() < 0.55 else None
            if e.who is None:
                continue
        ev.append(e)
    return ev


def log_rows(W, ids, heloc):
    """the statement system's rows (the outage fortnight's requests go to the manual log instead)"""
    rows, manual = [], []
    sid = 2510000
    hel = [h for h in heloc]
    for e in sorted(events(W, ids, None), key=lambda x: (x.close, x.i)):
        g = K.rng(61, e.i)
        i = e.i
        rc = W.reg[i]
        first = K.business_day(e.close - dt.timedelta(days=int(g.integers(8, 41))), back=True)
        dates = [first]
        k = int(g.choice([0, 1, 2, 3], p=[0.40, 0.38, 0.16, 0.06]))
        for _ in range(k):
            nxt = K.business_day(dates[-1] + dt.timedelta(days=int(g.integers(5, 16))))
            if nxt >= e.close:
                break
            dates.append(nxt)
        if e.who == "member":
            requester = "MEMBER REQUEST"
        else:
            pool = AGENCIES[rc] + NATIONAL
            requester = pool[int(g.integers(0, len(pool)))]
        # a title search that found the second lien late: the first statement quoted the first mortgage alone and the
        # update quoted both liens
        first_only = False
        if e.mtg and K.rng(66, i).random() < 0.22:
            if len(dates) == 1:
                nxt = K.business_day(first + dt.timedelta(days=int(K.rng(66, i, 1).integers(3, 10))))
                if nxt < e.close:
                    dates.append(nxt)
            first_only = len(dates) > 1
        if e.mtg:
            ref, prod = e.mtg, "MTG"
        else:
            u = g.random()
            pre = int(W.o2[i]) < K.CONV_M
            ref = ids.legacy_loan[i] if (pre and u < 0.16) else ids.new_loan[i]
            prod = "HE"
        channel = ["PORTAL", "FAX", "EMAIL"][int(g.choice(3, p=[0.70, 0.18, 0.12]))]
        for n, d in enumerate(dates):
            if d < WIN0 or d > WIN1 or d < W.d2[i]:
                continue
            good = K.business_day(d + dt.timedelta(days=int(g.integers(10, 31))))
            days = (good - d).days
            # the balance the statement quotes: the loan's principal at the month-end before the statement, or the amount
            # funded for a loan funded earlier in the month
            tm = K.mo(d.year, d.month)
            if tm == int(W.o2[i]):
                hb = float(W.H0[i])
            else:
                hb = W.bal.get((i, tm - 1), e.he_bal) if tm <= int(W.exit_m[i]) else e.he_bal
            amt = payoff_amount(hb, W.r2[i], days)
            alone = first_only and n == 0
            if e.mtg:
                mb = float(WD.sched_balance(W.F0[i], W.r1[i], W.n1[i], tm - 1 - int(W.o1[i])))
                amt = payoff_amount(mb, W.r1[i], days) if alone else round(amt + payoff_amount(mb, W.r1[i], days) - 25.0, 2)
            if OUT0 <= d <= OUT1:
                manual.append([d, requester if e.who != "member" else "Member (walk-in)", ids.surname[i],
                               "%s, %s %s" % (ids.street[i], W.city[i], ids.zip[i]),
                               ("1st mortgage" if alone else "1st mortgage + home equity") if e.mtg else "Home equity loan",
                               amt, good, STAFF[int(g.integers(0, len(STAFF)))]])
                continue
            ts = stamp(d, g)
            sid += int(g.integers(1, 4))
            rows.append([str(sid), ts.strftime("%Y-%m-%dT%H:%M:%SZ"), channel, requester, ref, prod,
                         good.isoformat(), "%.2f" % amt, "ISSUED" if n == 0 else "UPDATED",
                         STAFF[int(g.integers(0, len(STAFF)))]])
    # closings that fell through: a statement, sometimes an update, and no payoff
    g = K.rng(62)
    alive = [int(i) for i in W.book]
    for k in range(int(len(rows) * 0.11)):
        i = alive[int(g.integers(0, len(alive)))]
        d = K.business_day(WIN0 + dt.timedelta(days=int(g.integers(0, (WIN1 - WIN0).days - 5))))
        bal = W.bal.get((i, K.mo(d.year, d.month) - 1))
        if bal is None or bal <= 0:
            continue
        rc = W.reg[i]
        pool = AGENCIES[rc] + NATIONAL
        good = K.business_day(d + dt.timedelta(days=int(g.integers(10, 31))))
        amt = payoff_amount(bal, W.r2[i], (good - d).days)
        mtg = ids.mtg_loan.get(i)
        ref, prod = (mtg, "MTG") if (mtg and g.random() < 0.8) else (ids.new_loan[i], "HE")
        alone = prod == "MTG" and K.rng(67, k).random() < 0.5
        if prod == "MTG":
            fb = float(WD.sched_balance(W.F0[i], W.r1[i], W.n1[i], K.mo(d.year, d.month) - 1 - int(W.o1[i])))
            fpay = payoff_amount(fb, W.r1[i], (good - d).days)
            amt = fpay if alone else round(amt + fpay - 25.0, 2)
        if OUT0 <= d <= OUT1:
            manual.append([d, pool[int(g.integers(0, len(pool)))], ids.surname[i], "%s, %s %s" % (ids.street[i], W.city[i], ids.zip[i]),
                           ("1st mortgage" if alone else "1st mortgage + home equity") if prod == "MTG" else "Home equity loan",
                           amt, good, STAFF[int(g.integers(0, len(STAFF)))]])
            continue
        ts = stamp(d, g)
        rows.append(["", ts.strftime("%Y-%m-%dT%H:%M:%SZ"), ["PORTAL", "FAX", "EMAIL"][int(g.integers(0, 3))],
                     pool[int(g.integers(0, len(pool)))], ref, prod, good.isoformat(), "%.2f" % amt, "ISSUED",
                     STAFF[int(g.integers(0, len(STAFF)))]])
    # members with a home equity loan behind the credit union's first mortgage who asked for the first mortgage's payoff
    # alone (a refinance of the first shopped elsewhere, a payoff from savings considered); the home equity loan stays
    for i in sorted(ids.mtg_loan):
        gq = K.rng(68, i)
        if gq.random() > 0.10:
            continue
        d = K.business_day(WIN0 + dt.timedelta(days=int(gq.integers(0, (WIN1 - WIN0).days - 5))))
        tm = K.mo(d.year, d.month)
        hb = W.bal.get((i, tm - 1))
        if hb is None or hb <= 0 or (int(W.exit_m[i]) >= 0 and int(W.exit_m[i]) <= tm + 1):
            continue
        fb = float(WD.sched_balance(W.F0[i], W.r1[i], W.n1[i], tm - 1 - int(W.o1[i])))
        if fb <= 0:
            continue
        good = K.business_day(d + dt.timedelta(days=int(gq.integers(10, 31))))
        amt = payoff_amount(fb, W.r1[i], (good - d).days)
        pool = AGENCIES[W.reg[i]] + NATIONAL + ["MEMBER REQUEST"] * 2
        req = pool[int(gq.integers(0, len(pool)))]
        if OUT0 <= d <= OUT1:
            manual.append([d, "Member (walk-in)" if req == "MEMBER REQUEST" else req, ids.surname[i],
                           "%s, %s %s" % (ids.street[i], W.city[i], ids.zip[i]), "1st mortgage", amt, good,
                           STAFF[int(gq.integers(0, len(STAFF)))]])
            continue
        ts = stamp(d, gq)
        rows.append(["", ts.strftime("%Y-%m-%dT%H:%M:%SZ"), ["PORTAL", "FAX", "EMAIL"][int(gq.integers(0, 3))], req,
                     ids.mtg_loan[i], "MTG", good.isoformat(), "%.2f" % amt, "ISSUED", STAFF[int(gq.integers(0, len(STAFF)))]])
    # the credit union's first mortgages with no home equity loan behind them: closings and requests that fell through
    stacked = set(ids.mtg_loan.values())
    for j, m in enumerate(R.servicing_rows(W, ids)):
        if m[0] in stacked:
            continue
        gm = K.rng(69, j)
        nd = dt.date.fromisoformat(m[5])
        o1 = K.mo(nd.year, nd.month)
        F0, r1, n1 = float(m[6]), float(m[7]), int(m[8])
        if m[10] == "PAID IN FULL":
            close = dt.date.fromisoformat(m[11])
            first = K.business_day(close - dt.timedelta(days=int(gm.integers(8, 41))), back=True)
            dates = [first]
            for _ in range(int(gm.choice([0, 1, 2], p=[0.5, 0.38, 0.12]))):
                nxt = K.business_day(dates[-1] + dt.timedelta(days=int(gm.integers(5, 16))))
                if nxt >= close:
                    break
                dates.append(nxt)
        elif gm.random() < 0.05:
            dates = [K.business_day(WIN0 + dt.timedelta(days=int(gm.integers(0, (WIN1 - WIN0).days - 5))))]
        else:
            continue
        pool = sum(AGENCIES.values(), []) + NATIONAL + ["MEMBER REQUEST"]
        req = pool[int(gm.integers(0, len(pool)))]
        for n, d in enumerate(dates):
            if d < WIN0 or d > WIN1:
                continue
            tm = K.mo(d.year, d.month)
            fb = float(WD.sched_balance(F0, r1, n1, tm - 1 - o1))
            if fb <= 0:
                continue
            good = K.business_day(d + dt.timedelta(days=int(gm.integers(10, 31))))
            amt = payoff_amount(fb, r1, (good - d).days)
            if OUT0 <= d <= OUT1:
                manual.append([d, "Member (walk-in)" if req == "MEMBER REQUEST" else req, SURNAME_FOR(gm),
                               "%s, %s %s" % (m[2], m[3], m[4]), "1st mortgage", amt, good,
                               STAFF[int(gm.integers(0, len(STAFF)))]])
                continue
            ts = stamp(d, gm)
            rows.append(["", ts.strftime("%Y-%m-%dT%H:%M:%SZ"), ["PORTAL", "FAX", "EMAIL"][int(gm.integers(0, 3))], req,
                         m[0], "MTG", good.isoformat(), "%.2f" % amt, "ISSUED" if n == 0 else "UPDATED",
                         STAFF[int(gm.integers(0, len(STAFF)))]])
    # home equity lines share the desk
    for h in hel:
        gh = K.rng(63, int(h[0][1:]))
        if gh.random() > 0.30:
            continue
        d = K.business_day(WIN0 + dt.timedelta(days=int(gh.integers(0, (WIN1 - WIN0).days - 5))))
        good = K.business_day(d + dt.timedelta(days=int(gh.integers(10, 31))))
        bal = float(h[4]) or float(h[3]) * 0.2
        amt = payoff_amount(bal, 7.25, (good - d).days)
        pool = sum(AGENCIES.values(), []) + NATIONAL
        req = pool[int(gh.integers(0, len(pool)))]
        if OUT0 <= d <= OUT1:
            manual.append([d, req, SURNAME_FOR(gh), "%d %s %s, %s" % (int(gh.integers(100, 9900)), R.STREETS[int(gh.integers(0, 40))],
                                                                  R.SUFFIX[int(gh.integers(0, 10))], h[11]),
                           "HELOC", amt, good, STAFF[int(gh.integers(0, len(STAFF)))]])
            continue
        ts = stamp(d, gh)
        rows.append(["", ts.strftime("%Y-%m-%dT%H:%M:%SZ"), ["PORTAL", "FAX", "EMAIL"][int(gh.integers(0, 3))], req,
                     h[0], "HE", good.isoformat(), "%.2f" % amt, "ISSUED", STAFF[int(gh.integers(0, len(STAFF)))]])
    # requests voided before a statement was issued (a wrong or closed account, a request sent twice)
    gv = K.rng(64)
    for k in range(int(len(rows) * 0.035)):
        src = rows[int(gv.integers(0, len(rows)))]
        ts = dt.datetime.strptime(src[1], "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(minutes=int(gv.integers(3, 50)))
        rows.append(["", ts.strftime("%Y-%m-%dT%H:%M:%SZ"), src[2], src[3], src[4], src[5], "", "0.00", "VOID",
                     STAFF[int(gv.integers(0, len(STAFF)))]])
    # statement ids are issued in time order
    rows.sort(key=lambda r: (r[1], r[4]))
    n = 2510001
    for r in rows:
        r[0] = str(n)
        n += int(K.rng(65, n).integers(1, 3))
    manual.sort(key=lambda r: (r[0], r[2]))
    return rows, manual


def SURNAME_FOR(g):
    return R.SURNAMES[int(g.integers(0, len(R.SURNAMES)))]


LOG_COLS = ["statement_id", "issued_utc", "channel", "requested_by", "account_reference", "product_on_file",
            "good_through_date", "statement_amount", "statement_status", "prepared_by"]


def write_manual(path, manual):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Payoff requests"
    ws.append(["Payoff statements prepared by hand while the statement system was down (9 to 20 March 2026)"])
    ws.append([])
    ws.append(["Date received", "Requested by", "Borrower", "Property", "Liens", "Amount quoted", "Good through",
               "Prepared by"])
    for c in ws[3]:
        c.font = Font(bold=True)
    for r in manual:
        ws.append([r[0], r[1], r[2], r[3], r[4], round(float(r[5]), 2), r[6], r[7]])
    for row in ws.iter_rows(min_row=4):
        row[0].number_format = "m/d/yyyy"
        row[6].number_format = "m/d/yyyy"
        row[5].number_format = "#,##0.00"
    for col, w in zip("ABCDEFGH", (13, 30, 16, 40, 26, 15, 13, 11)):
        ws.column_dimensions[col].width = w
    ws["A1"].font = Font(bold=True)
    wb.save(path)
    return len(manual)


def write_all(out, W, ids, heloc):
    rows, manual = log_rows(W, ids, heloc)
    n = {F_LOG: K.write_csv(os.path.join(out, F_LOG), LOG_COLS, rows)}
    n[F_MANUAL] = write_manual(os.path.join(out, F_MANUAL), manual)
    return n
