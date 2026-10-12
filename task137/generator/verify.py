"""Independent verifier for task137. Reads only the shipped bundle (target/) and the golden workbook, imports nothing
from the generator, and recomputes on its own code path (csv, pypdf, openpyxl; no pandas): the do-not-call wash, the
dialling yields per mix of callable number types, the release share, the share of conversations that went to the
retention offer by 0.25-point band of drop, the hours by maturity month and the booking, the pooled-share default,
and both asks. Exits non-zero on any disagreement with the golden.

    python3 task137/generator/verify.py [target] [golden]"""
from __future__ import annotations

import csv
import datetime as dt
import math
import os
import re
import sys
from collections import defaultdict

import openpyxl
from pypdf import PdfReader

NOT_REACHED = {"NOA", "BSY", "VML", "DIS", "WNG"}
TALKED = {"RNW", "CHG", "DEC", "RTK", "RTW"}
RETENTION = {"RTK", "RTW"}
CUT = dt.date(2026, 11, 2)
PAST = ["2025Q1", "2025Q2", "2025Q3", "2025Q4", "2026Q1", "2026Q2", "2026Q3"]
LABEL = {"2025Q1": "January to March 2025", "2025Q2": "April to June 2025", "2025Q3": "July to September 2025",
         "2025Q4": "October to December 2025", "2026Q1": "January to March 2026", "2026Q2": "April to June 2026",
         "2026Q3": "July to September 2026"}

FAIL = []
PASSED = [0]


def check(cond, msg):
    if cond:
        PASSED[0] += 1
    else:
        FAIL.append(msg)


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def day(s):
    return dt.date.fromisoformat(s)


def digits(s):
    return "".join(ch for ch in s if ch.isdigit())


def phone(s):
    d = digits(s)
    if d.startswith("64"):
        d = d[2:]
    return "64" + d.lstrip("0")


def half_up(x, unit):
    return int(math.floor(x / unit + 0.5) * unit)


def card(path):
    text = " ".join(" ".join((pg.extract_text() or "").split()) for pg in PdfReader(path).pages)
    m = re.search(r"Rate % p\.a\. ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", text)
    if m:
        return {t: float(m.group(t)) for t in range(1, 6)}
    return {int(t): float(v) for t, v in re.findall(r"(\d) years? ([\d.]+)", text)}


def mix(types):
    return "-".join(sorted(types))


def main(target, golden):
    P = lambda f: os.path.join(target, f)
    cards = {q: card(P("harbourline_campaign_brief_%s.pdf" % q)) for q in PAST + ["2027Q1"]}
    check(all(len(c) == 5 for c in cards.values()), "a brief's card did not read")

    # ------------------------------------------------------------- the past lists (two layouts)
    listed = {}
    for r in rows(P("kbs_td_retention_lists_2025.csv")):
        q = r["Campaign"].replace("TDR ", "").replace("-Q", "Q")
        d, m, y = r["Maturity"].split("/")
        listed[(q, digits(r["Account No"]))] = dict(term=int(r["Term (mths)"]) // 12, rate=float(r["Rate %"]),
                                                    principal=float(r["Principal"].replace(",", "")),
                                                    maturity=dt.date(int(y), int(m), int(d)), cust=r["Customer No"])
    for r in rows(P("kbs_td_retention_lists_2026.csv")):
        listed[(r["campaign"].replace("TDR-", ""), r["account"])] = dict(
            term=int(r["term_months"]) // 12, rate=round(float(r["int_rate"]) * 100, 2),
            principal=float(r["principal"]), maturity=day(r["maturity_date"]), cust=r["customer_no"])

    # ------------------------------------------------------------- past cases
    close = {}
    for r in rows(P("harbourline_case_closeouts_2025q1-2026q3.csv")):
        close[(digits(r["kbs_ref"]), r["released"])] = r["case_ref"]
    per_case = defaultdict(lambda: [0, False, False])
    for r in rows(P("harbourline_dial_log_2025q1-2026q3.csv")):
        c = per_case[r["case_ref"]]
        if r["outcome"] in NOT_REACHED:
            c[0] += 1
        if r["outcome"] in TALKED:
            c[1] = True
        if r["outcome"] in RETENTION:
            c[2] = True
    yields = defaultdict(lambda: [0, 0.0, 0.0])
    conv_by_band = defaultdict(lambda: [0, 0])
    released = instructed = 0
    pooled = [0, 0]
    hi = [0, 0]
    for r in rows(P("kbs_case_release_log_2025q1-2026q3.csv")):
        q = r["campaign"].replace("TDR-", "")
        if r["status"] != "RELEASED":
            instructed += r["reason"] == "INSTRUCTED"
            continue
        released += 1
        types = [r["type_%d" % k][0] for k in range(1, 5) if r["type_%d" % k]]
        nr, talked, ret = per_case[close[(r["account"], r["release_date"])]]
        y = yields[mix(types)]
        y[0] += 1
        y[1] += nr
        y[2] += talked
        if talked:
            dep = listed[(q, r["account"])]
            drop = round(dep["rate"] - cards[q][dep["term"]], 2)
            b = conv_by_band[math.floor(drop / 0.25 + 1e-9)]
            b[0] += 1
            b[1] += ret
            pooled[0] += 1
            pooled[1] += ret
            if drop >= 2.5:
                hi[0] += 1
                hi[1] += ret
    R = released / (released + instructed)

    # ------------------------------------------------------------- the coming list
    blocked = set()
    for r in rows(P("kbs_do_not_call_register_2026-11-02.csv")):
        if day(r["recorded"]) <= CUT and (not r["withdrawn"] or day(r["withdrawn"]) > CUT):
            blocked.add(phone(r["number"]))
    numbers = defaultdict(list)
    for r in rows(P("kbs_contact_points_2026-11-02.csv")):
        if phone(r["number"]) not in blocked:
            numbers[r["customer_no"]].append(r["contact_type"][0].upper())
    minutes = defaultdict(float)
    conv = ret = 0.0
    nocall = 0
    special = 0
    fwd = rows(P("kbs_td_retention_list_2027Q1.csv"))
    for r in fwd:
        mth = day(r["maturity_date"]).month
        term = int(r["term_months"]) // 12
        rate = round(float(r["int_rate"]) * 100, 2)
        special += (term == 4 and rate == 5.65)
        types = numbers.get(r["customer_no"], [])
        if not types:
            nocall += 1
            continue
        y = yields[mix(types)]
        U, Cv = y[1] / y[0], y[2] / y[0]
        b = conv_by_band[math.floor(round(rate - cards["2027Q1"][term], 2) / 0.25 + 1e-9)]
        p = b[1] / b[0]
        minutes[mth] += R * (1.5 * U + Cv * (8 + 14 * p))
        conv += R * Cv
        ret += R * Cv * p
    hours = {m: v / 60.0 for m, v in minutes.items()}
    total = sum(hours.values())

    # ------------------------------------------------------------- ask A
    reinv, gone, opens, td = set(), defaultdict(list), {}, set()
    for r in rows(P("kbs_td_account_events_2025-01_2026-10.csv")):
        td.add(r["account"])
        if r["event_type"] == "REINVEST":
            reinv.add((r["account"], r["event_date"]))
        elif r["event_type"] in ("BREAK", "CLOSE"):
            gone[r["account"]].append(day(r["event_date"]))
        elif r["event_type"] == "OPEN":
            opens[r["account"]] = r["event_date"]
    paid = defaultdict(list)
    for r in rows(P("kbs_member_transfers_2025-01_2026-10.csv")):
        paid[(r["from_account"], r["value_date"])].append((r["to_account"], float(r["amount"])))
    ask_a = {}
    for q in PAST:
        n, amt = 0, 0.0
        for (qq, acct), dep in listed.items():
            if qq != q:
                continue
            m = dep["maturity"]
            alive = lambda a: not any(m < x <= m + dt.timedelta(days=30) for x in gone.get(a, []))
            kept = dep["principal"] if ((acct, m.isoformat()) in reinv and alive(acct)) else 0.0
            if not kept:
                kept = sum(v for to, v in paid.get((acct, m.isoformat()), [])
                           if opens.get(to) == m.isoformat() and alive(to))
            if kept > 0:
                n += 1
                amt += kept
        ask_a[q] = (n, half_up(amt, 1000))
    # the prompt's clause read on the extracts: a deposit counts when any of its principal sits on a term deposit
    # with the society (any account of the events extract, opened that day or not) 30 days after maturity, and only
    # that part counts; per deposit, as the lists carry one deposit per holder
    clause, kept_whole, holders = {}, {}, defaultdict(int)
    for q in PAST:
        n, amt, nw = 0, 0.0, 0
        for (qq, acct), dep in listed.items():
            if qq != q:
                continue
            holders[(q, dep["cust"])] += 1
            m = dep["maturity"]
            lim = m + dt.timedelta(days=30)
            alive = lambda a: not any(m < x <= lim for x in gone.get(a, []))
            kept = dep["principal"] if ((acct, m.isoformat()) in reinv and alive(acct)) else 0.0
            if not kept:
                for k in range(31):
                    kept += sum(v for to, v in paid.get((acct, (m + dt.timedelta(days=k)).isoformat()), [])
                                if to in td and to != acct and alive(to))
            if kept > 0:
                n += 1
                amt += kept
                nw += abs(kept - dep["principal"]) < 0.005
        clause[q] = (n, half_up(amt, 1000))
        kept_whole[q] = nw
    check(clause == ask_a, "ask A under the prompt's clause %s against %s" % (clause, ask_a))
    check(max(holders.values()) == 1, "a holder with two deposits on one campaign's list")
    check(all(kept_whole[q] < ask_a[q][0] for q in PAST), "ask A counting only deposits kept whole lands")

    # ------------------------------------------------------------- ask B
    seen, maturing = set(), defaultdict(float)
    for r in rows(P("kbs_term_holdings_2026-11-02.csv")):
        mdate = day(r["maturity_date"])
        if r["account"] in seen or not (dt.date(2027, 1, 1) <= mdate <= dt.date(2027, 3, 31)):
            continue
        seen.add(r["account"])
        maturing[mdate.month] += float(r["principal"])
    moved = {r["cert_no"] for r in rows(P("kip_migration_batches_2026.csv")) if r["status"] == "MIGRATED"}
    for r in rows(P("kip_certificate_register_2026-06-30.csv")):
        mdate = day(r["maturity_date"])
        if r["cert_no"] not in moved and dt.date(2027, 1, 1) <= mdate <= dt.date(2027, 3, 31):
            maturing[mdate.month] += float(r["principal"])
    on_list = defaultdict(float)
    for r in fwd:
        on_list[day(r["maturity_date"]).month] += float(r["principal"])
    ask_b = {m: (half_up(maturing[m], 1000), half_up(maturing[m] - on_list[m], 1000)) for m in (1, 2, 3)}

    # ------------------------------------------------------------- against the golden workbook
    wb = openpyxl.load_workbook(os.path.join(golden, "td_booking_q1_2027.xlsx"), data_only=True)
    ws = wb["Booking"]
    book = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=8).value for r in range(5, 9)}
    check(len(fwd) == 18400, "list size %d" % len(fwd))
    check(book["Quarter"] == half_up(total, 250), "booking %s against %d (%.1f)" % (book["Quarter"],
                                                                                   half_up(total, 250), total))
    for m, nm in ((1, "January"), (2, "February"), (3, "March")):
        check(book["%s 2027" % nm] == half_up(hours[m], 250), "%s %s against %.1f" % (nm, book["%s 2027" % nm],
                                                                                     hours[m]))
    check(half_up(total, 250) == sum(half_up(hours[m], 250) for m in (1, 2, 3)), "months do not add to the booking")
    check(abs(ws.cell(row=8, column=7).value - round(total, 1)) < 0.05, "unrounded hours")
    check(ws.cell(row=8, column=5).value == round(conv) and ws.cell(row=8, column=6).value == round(ret),
          "conversations")
    pooled_share = pooled[1] / pooled[0]
    check(pooled_share < 0.4 and ret / conv > 0.55, "shares %.3f %.3f" % (pooled_share, ret / conv))
    check(special > 9000 and nocall > 0, "special %d, no callable %d" % (special, nocall))
    check(hi[1] / hi[0] > 0.85, "share at drops of 2.5 or more %.3f" % (hi[1] / hi[0]))
    ws2 = wb["Kept at 30 days"]
    for r, q in enumerate(PAST, 5):
        check(ws2.cell(row=r, column=2).value == LABEL[q], "campaign label %s" % q)
        check((ws2.cell(row=r, column=4).value, ws2.cell(row=r, column=5).value) == ask_a[q],
              "ask A %s: workbook %s, verifier %s" % (q, (ws2.cell(row=r, column=4).value,
                                                         ws2.cell(row=r, column=5).value), ask_a[q]))
    ws3 = wb["Maturing Q1 2027"]
    for r, m in enumerate((1, 2, 3), 5):
        check((ws3.cell(row=r, column=2).value, ws3.cell(row=r, column=3).value) == ask_b[m],
              "ask B month %d: workbook %s, verifier %s" % (m, (ws3.cell(row=r, column=2).value,
                                                               ws3.cell(row=r, column=3).value), ask_b[m]))
    if FAIL:
        print("verify: %d checks failed" % len(FAIL))
        for f in FAIL:
            print("  " + f)
        raise SystemExit(1)
    print("verify: %d checks passed from the bundle alone (booking %d, months %s; total %.1f)" % (
        PASSED[0], half_up(total, 250), [half_up(hours[m], 250) for m in (1, 2, 3)], total))


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "target")
    gd = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "golden")
    main(t, gd)
