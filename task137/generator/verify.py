"""Independent verifier for task137. Reads only the shipped bundle (target/) and the golden workbook, imports nothing
from the generator, and recomputes on its own code path (csv, pypdf, openpyxl; no pandas): the do-not-call wash, the
dialling yields per mix of callable number types, the release share, each deposit's class (money a special won: a rate
0.40 points or more above the lowest rate of the same list's deposits of its term opened in the same quarter), the
share of conversations that went to the retention offer by class and 0.25-point band of drop, the hours by maturity
month and the booking, the pooled and drop-only defaults, and both asks. Exits non-zero on any disagreement with the
golden.

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
GAP = 0.40

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


def dmy(s):
    d, m, y = s.split("/")
    return dt.date(int(y), int(m), int(d))


def digits(s):
    return "".join(ch for ch in s if ch.isdigit())


def phone(s):
    d = digits(s)
    if d.startswith("64"):
        d = d[2:]
    return "64" + d.lstrip("0")


def half_up(x, unit):
    return int(math.floor(x / unit + 0.5) * unit)


def quarter(d):
    return (d.year, (d.month - 1) // 3)


def card(path):
    text = " ".join(" ".join((pg.extract_text() or "").split()) for pg in PdfReader(path).pages)
    m = re.search(r"Rate % p\.a\. ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+) ([\d.]+)", text)
    if m:
        return {t: float(m.group(t)) for t in range(1, 6)}
    return {int(t): float(v) for t, v in re.findall(r"(\d) years? ([\d.]+)", text)}


def mix(types):
    return "-".join(sorted(types))


def classify(deps):
    """deps: list of dicts with term, rate, opened. Sets dep['special']."""
    low = {}
    for d in deps:
        k = (d["term"], quarter(d["opened"]))
        low[k] = min(low.get(k, 99.0), d["rate"])
    for d in deps:
        d["special"] = d["rate"] - low[(d["term"], quarter(d["opened"]))] >= GAP - 1e-9


def main(target, golden):
    P = lambda f: os.path.join(target, f)
    cards = {q: card(P("harbourline_campaign_brief_%s.pdf" % q)) for q in PAST + ["2027Q1"]}
    check(all(len(c) == 5 for c in cards.values()), "a brief's card did not read")

    # ------------------------------------------------------------- the past lists (two layouts), classed per list
    listed = {}
    for r in rows(P("kbs_td_retention_lists_2025.csv")):
        q = r["Campaign"].replace("TDR ", "").replace("-Q", "Q")
        listed[(q, digits(r["Account No"]))] = dict(term=int(r["Term (mths)"]) // 12, rate=float(r["Rate %"]),
                                                    principal=float(r["Principal"].replace(",", "")),
                                                    opened=dmy(r["Opened"]), maturity=dmy(r["Maturity"]),
                                                    cust=r["Customer No"], q=q)
    for r in rows(P("kbs_td_retention_lists_2026.csv")):
        q = r["campaign"].replace("TDR-", "")
        listed[(q, r["account"])] = dict(term=int(r["term_months"]) // 12, rate=round(float(r["int_rate"]) * 100, 2),
                                         principal=float(r["principal"]), opened=day(r["start_date"]),
                                         maturity=day(r["maturity_date"]), cust=r["customer_no"], q=q)
    for q in PAST:
        classify([d for (qq, _), d in listed.items() if qq == q])

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
    by_class = defaultdict(lambda: [0, 0])
    by_band = defaultdict(lambda: [0, 0])
    released = instructed = 0
    pooled = [0, 0]
    special_conv = [0, 0]
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
            band = math.floor(round(dep["rate"] - cards[q][dep["term"]], 2) / 0.25 + 1e-9)
            for tally in (by_class[(dep["special"], band)], by_band[band], pooled):
                tally[0] += 1
                tally[1] += ret
            if dep["special"]:
                special_conv[0] += 1
                special_conv[1] += ret
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
    fwd = rows(P("kbs_td_retention_list_2027Q1.csv"))
    deps = [dict(term=int(r["term_months"]) // 12, rate=round(float(r["int_rate"]) * 100, 2),
                 opened=day(r["start_date"]), month=day(r["maturity_date"]).month, cust=r["customer_no"],
                 principal=float(r["principal"])) for r in fwd]
    classify(deps)
    minutes, minutes_pooled, minutes_drop = defaultdict(float), 0.0, 0.0
    conv = ret = 0.0
    nocall = special = 0
    p_pool = pooled[1] / pooled[0]
    for d in deps:
        special += d["special"]
        types = numbers.get(d["cust"], [])
        if not types:
            nocall += 1
            continue
        y = yields[mix(types)]
        U, Cv = y[1] / y[0], y[2] / y[0]
        band = math.floor(round(d["rate"] - cards["2027Q1"][d["term"]], 2) / 0.25 + 1e-9)
        t = by_class[(d["special"], band)]
        p = t[1] / t[0]
        minutes[d["month"]] += R * (1.5 * U + Cv * (8 + 14 * p))
        minutes_pooled += R * (1.5 * U + Cv * (8 + 14 * p_pool))
        b = by_band[band]
        minutes_drop += R * (1.5 * U + Cv * (8 + 14 * b[1] / b[0]))
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
    direct = defaultdict(list)
    for r in rows(P("kbs_member_transfers_2025-01_2026-10.csv")):
        ref = re.search(r"(\d{2}-\d{4}-\d{7}-\d{3})", r["narrative"])
        src = digits(ref.group(1)) if ref else r["from_account"]
        paid[(src, r["value_date"])].append((r["to_account"], float(r["amount"])))
        direct[(r["from_account"], r["value_date"])].append(r["to_account"])
    ask_a, own_only = {}, {}
    for q in PAST:
        n, amt, n_own = 0, 0.0, 0
        for (qq, acct), dep in listed.items():
            if qq != q:
                continue
            m = dep["maturity"]
            alive = lambda a: not any(m < x <= m + dt.timedelta(days=30) for x in gone.get(a, []))
            kept = dep["principal"] if ((acct, m.isoformat()) in reinv and alive(acct)) else 0.0
            n_own += kept > 0
            if not kept:
                kept = sum(v for to, v in paid.get((acct, m.isoformat()), [])
                           if opens.get(to) == m.isoformat() and alive(to))
            if kept > 0:
                n += 1
                amt += kept
        ask_a[q] = (half_up(amt, 1000), n)
        own_only[q] = n_own
    check(all(own_only[q] < ask_a[q][1] for q in PAST), "ask A: own accounts alone keep as many deposits")
    listed_accts = {a for (_, a) in listed}
    check(not any(opens.get(to) for (acct, _), tos in direct.items() if acct in listed_accts for to in tos),
          "ask A: a listed deposit pays its proceeds straight into a new account")

    # ------------------------------------------------------------- ask B
    seen, maturing, core_kic = set(), defaultdict(float), set()
    for r in rows(P("kbs_term_holdings_2026-11-02.csv")):
        if r["product"] == "KIC":
            core_kic.add((r["start_date"], r["maturity_date"], round(float(r["int_rate"]) * 100, 2),
                          int(r["term_months"])))
        mdate = day(r["maturity_date"])
        if r["account"] in seen or not (dt.date(2027, 1, 1) <= mdate <= dt.date(2027, 3, 31)):
            continue
        seen.add(r["account"])
        maturing[mdate.month] += float(r["principal"])
    moved = {r["cert_no"] for r in rows(P("kip_migration_batches_2026.csv")) if r["status"] == "MIGRATED"}
    by_hand = 0
    for r in rows(P("kip_certificate_register_2026-06-30.csv")):
        mdate = day(r["maturity_date"])
        if not (dt.date(2027, 1, 1) <= mdate <= dt.date(2027, 3, 31)) or r["cert_no"] in moved:
            continue
        if (r["issue_date"], r["maturity_date"], round(float(r["rate"]), 2), int(r["term_months"])) in core_kic:
            by_hand += 1
            continue
        maturing[mdate.month] += float(r["principal"])
    check(by_hand > 5, "ask B: no certificate moved by hand (%d)" % by_hand)
    off = sum(maturing.values()) - sum(d["principal"] for d in deps)
    ask_b = {m: half_up(maturing[m], 1000) for m in (1, 2, 3)}

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
    for nm, h in (("pooled share", minutes_pooled / 60.0), ("share by drop", minutes_drop / 60.0)):
        check(half_up(h, 250) <= half_up(total, 250) - 500, "the %s books %d, within two bins of %d" % (
            nm, half_up(h, 250), half_up(total, 250)))
    check(special_conv[1] / special_conv[0] > 0.8 > 0.3 > p_pool, "special money's share %.3f, pooled %.3f" % (
        special_conv[1] / special_conv[0], p_pool))
    check(special > 9000 and nocall > 0, "special %d, no callable %d" % (special, nocall))
    ws2 = wb["Kept at 30 days"]
    for r, q in enumerate(PAST, 5):
        check(ws2.cell(row=r, column=2).value == LABEL[q], "campaign label %s" % q)
        check((ws2.cell(row=r, column=4).value, ws2.cell(row=r, column=5).value) == ask_a[q],
              "ask A %s: workbook %s, verifier %s" % (q, (ws2.cell(row=r, column=4).value,
                                                         ws2.cell(row=r, column=5).value), ask_a[q]))
    ws3 = wb["Maturing Q1 2027"]
    for r, m in enumerate((1, 2, 3), 5):
        check(ws3.cell(row=r, column=2).value == ask_b[m], "ask B month %d: workbook %s, verifier %s" % (
            m, ws3.cell(row=r, column=2).value, ask_b[m]))
    check(ws3.cell(row=10, column=2).value == half_up(off, 1000), "ask B off the list: workbook %s, verifier %s" % (
        ws3.cell(row=10, column=2).value, half_up(off, 1000)))
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
