"""task183 pack: the evidence files written from the world and the simulation, each in the shape the producing
system exports it. The documents (PDF) are written by docs.py; the ask files by asks.py."""
from __future__ import annotations

import csv
import datetime as dt
import random

import openpyxl
from openpyxl.styles import Font

import asks as A
import sim as S
import world as W

FILES = dict(
    acct="business_account_transactions_2025-01_2026-09.csv",
    ms="merchant_services_daily_trade_2025-01_2026-09.csv",
    mreg="merchant_register_2026-10.xlsx",
    seg="cash_segment_review_list_2025-26.xlsx",
    till="till_service_daily_totals_2025-01_2026-09.csv",
    bcr="business_cash_review_standard_BCR-3.pdf",
    ap="an_post_business_lodgements_2025-10_2026-09.csv",
    apfee="an_post_agency_agreement_schedule_2_fees.pdf",
    tlog="till_service_z_report_log_2025-10_2026-10.csv",
    rsi="retail_sales_index_2024-01_2026-09.csv",
    orders="branch_cash_orders_2025-26.xlsx",
    offices="an_post_office_list_2026-10.xlsx",
)


def _csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def write_xlsx(path, sheets):
    """sheets: (name, title_rows, header, rows, widths)"""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, titles, header, rows, widths in sheets:
        ws = wb.create_sheet(name)
        for t in titles:
            ws.append(t)
            ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
        if titles:
            ws.append([])
        ws.append(header)
        hr = ws.max_row
        for c in ws[hr]:
            c.font = Font(bold=True)
        for row in rows:
            ws.append([None if v == "" else v for v in row])
        ws.freeze_panes = "A%d" % (hr + 1)
        for i, w in enumerate(widths or [max(10, min(40, len(str(h)) + 3)) for h in header]):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = w
    wb.save(path)


def first_working_of_month(d):
    x = d.replace(day=1)
    while not W.working(x):
        x += dt.timedelta(days=1)
    return x


def dmy(d):
    return d.strftime("%d/%m/%Y")


def eur(x):
    return "%.2f" % x if x else ""


# ---- terminals ------------------------------------------------------------------------------------------------
def mids():
    """Each customer's merchant ids (one or two terminals), in the acquirer's 10-digit form."""
    r = random.Random(W.SEED + 7)
    out = {}
    for c in W.CUSTOMERS:
        out[c["cid"]] = ["44%08d" % r.randint(10000000, 99999999) for _ in range(c["mids"])]
    return out


MIDS = mids()


def mid_day_split(c, t, d):
    """Split a customer's day of card trade across its terminals by its fixed shares; refunds on the first."""
    g = t["card"][d]
    shares = t["mid_share"]
    parts = [round(g * s, 2) for s in shares]
    if len(parts) > 1:
        parts[-1] = round(g - sum(parts[:-1]), 2)
    return parts


# ---- merchant services daily file ------------------------------------------------------------------------------
MS_HEADER = ["trading_date", "mid", "txn_count", "gross_sales_cent", "refunds_cent", "msc_cent", "net_settled_cent",
             "settlement_date"]


def ms_rows():
    T = S.truth()
    r = random.Random(W.SEED + 11)
    rows = []
    for c in sorted(W.CUSTOMERS, key=lambda x: x["cid"]):
        t = T.cust[c["cid"]]
        for d in W.days(W.HISTORY_START, W.EXPORT_END):
            parts = mid_day_split(c, t, d)
            for i, mid in enumerate(MIDS[c["cid"]]):
                g = parts[i]
                ref = t["refunds"].get(d, 0.0) if i == 0 else 0.0
                if g <= 0 and ref <= 0:
                    continue
                gc = int(round(g * 100))
                rc = int(round(ref * 100))
                msc = int(round((gc - rc) * t["msc_rate"]))
                net = gc - rc - msc
                n = max(1, int(round(g / r.uniform(9.0, 22.0)))) if g > 0 else 0
                rows.append([d.isoformat(), mid, n, gc, rc, msc, net, W.next_working(d).isoformat()])
    rows.extend(A.ms_extra_rows())
    rows.sort(key=lambda x: (x[0], x[1]))
    return rows


# ---- account export (the spine) -------------------------------------------------------------------------------
ACCT_HEADER = ["Account", "Sort Code", "Posting Date", "Value Date", "Transaction Ref", "Type", "Description",
               "Reference", "Debit", "Credit", "Balance"]


def acct_rows():
    """Every posting on each reviewed customer's current account(s), January 2025 to September 2026, as the core
    banking export writes it. The second quarter of 2026 was delivered twice and the two deliveries concatenated,
    so its rows stand in the file twice with their own transaction references."""
    T = S.truth()
    r = random.Random(W.SEED + 13)
    postings = []
    for c in W.CUSTOMERS:
        t = T.cust[c["cid"]]
        acct, sort = c["acct"], W.BRANCH[c["home"]][3]
        # card settlements: each terminal's trading-day batch credited the next working day, net of charges
        for d in W.days(W.HISTORY_START, W.EXPORT_END):
            parts = mid_day_split(c, t, d)
            for i, mid in enumerate(MIDS[c["cid"]]):
                g = parts[i]
                ref = t["refunds"].get(d, 0.0) if i == 0 else 0.0
                if g <= 0 and ref <= 0:
                    continue
                gc, rc = int(round(g * 100)), int(round(ref * 100))
                net = (gc - rc - int(round((gc - rc) * t["msc_rate"]))) / 100.0
                sd = W.next_working(d)
                if sd > W.EXPORT_END:
                    continue
                postings.append((sd, 1, acct, sort, "STL", "CARD SETTLEMENT", "LRMS %s B%s" % (mid, d.strftime("%y%m%d")),
                                 0.0, round(net, 2)))
        # cash lodgements
        for L in t["lodgements"]:
            if L["day"] < W.HISTORY_START:
                continue
            if L["channel"] == "branch":
                pd = L["day"]
                desc = "CASH LODGEMENT"
                refx = "%s %s" % (c["home"], L["time"].strftime("%H:%M"))
            else:
                pd = W.next_working(L["day"]) if L["day"].weekday() < 5 else W.next_working(L["day"])
                desc = "AN POST LODGEMENT"
                refx = "AP %s %s %s" % (L["office"], L["day"].strftime("%d/%m"), L["time"].strftime("%H:%M"))
            if pd > W.EXPORT_END:
                continue
            postings.append((pd, 0, acct, sort, "LDG", desc, refx, 0.0, L["amount"]))
        # the rest of the account's traffic: payments out in proportion to the business's trade
        weekly_out = (c["card_week"] * (1 + c["k"]) + c["inj"] * 2) * 0.88
        sup = r.choice(["MUSGRAVE WHOLESALE", "BWG FOODS", "STORE SUPPLIES LTD", "MIDLAND CASH AND CARRY",
                        "WESTERN DISTRIBUTORS", "PROFESSIONAL SALON SUPPLY", "AUTO VALET SUPPLIES"])
        for d in W.days(W.HISTORY_START, W.EXPORT_END):
            if not W.working(d):
                continue
            if d.weekday() == 2:
                postings.append((d, 2, acct, sort, "SCT", "SEPA CREDIT TRANSFER", sup,
                                 round(weekly_out * r.uniform(0.30, 0.42), 2), 0.0))
            if d.weekday() == 4 and (d.isocalendar()[1] % 2 == 0):
                postings.append((d, 2, acct, sort, "PAY", "PAYROLL", "WAGES WK%02d" % d.isocalendar()[1],
                                 round(weekly_out * r.uniform(0.70, 0.90), 2), 0.0))
            if d == first_working_of_month(d):
                postings.append((d, 2, acct, sort, "SO", "STANDING ORDER", "RENT %s" % d.strftime("%b").upper(),
                                 round(weekly_out * r.uniform(0.50, 0.65), 2), 0.0))
            if d.weekday() == 0 and r.random() < 0.55:
                postings.append((d, 2, acct, sort, "WDL", "CASH WITHDRAWAL", "%s FLOAT" % c["home"],
                                 round(r.choice((100, 150, 200, 250, 300)), 2), 0.0))
            if r.random() < 0.18:
                postings.append((d, 2, acct, sort, "POS", "DEBIT CARD", r.choice(
                    ["LIDL", "WOODIES", "SCREWFIX", "AMAZON EU", "CIRCLE K", "EUROGIANT", "TESCO"]),
                    round(r.uniform(12, 240), 2), 0.0))
            if d.day == 23 and d.month % 2 == 1:
                postings.append((d, 2, acct, sort, "DD", "DIRECT DEBIT", "REVENUE COMMISSIONERS VAT",
                                 round(weekly_out * r.uniform(0.9, 1.4), 2), 0.0))
            if d.day == 14:
                postings.append((d, 2, acct, sort, "DD", "DIRECT DEBIT", "REVENUE COMMISSIONERS PAYE",
                                 round(weekly_out * r.uniform(0.18, 0.28), 2), 0.0))
            if d.day in (8, 9) and d.weekday() < 5 and r.random() < 0.5:
                postings.append((d, 2, acct, sort, "DD", "DIRECT DEBIT", r.choice(["ENERGIA", "ELECTRIC IRELAND",
                                                                                     "SSE AIRTRICITY", "EIR"]),
                                 round(r.uniform(120, 680), 2), 0.0))
    # running balances, posting order within a day: lodgements, settlements, then debits
    postings.sort(key=lambda p: (p[2], p[0], p[1]))
    rows = []
    bal = {}
    seq = 0
    rr = random.Random(W.SEED + 17)
    rk = random.Random(W.SEED + 191)
    used = set()
    for p in postings:
        d, _, acct, sort, typ, desc, refx, dr, cr = p
        if acct not in bal:
            bal[acct] = round(rr.uniform(4000, 28000), 2)
        bal[acct] = round(bal[acct] + cr - dr, 2)
        seq += 1
        while True:
            k = rk.randint(1000000, 9999999)
            if (d.month, d.year, k) not in used:
                used.add((d.month, d.year, k))
                break
        txn = "TX%s%07d" % (d.strftime("%y%m"), k)
        rows.append([acct, sort, dmy(d), dmy(d), txn, typ, desc, refx, eur(dr), eur(cr), "%.2f" % bal[acct]])
    # the second quarter of 2026 delivered twice
    q2 = [x for x in rows if dt.datetime.strptime(x[2], "%d/%m/%Y").date() >= dt.date(2026, 4, 1)
          and dt.datetime.strptime(x[2], "%d/%m/%Y").date() <= dt.date(2026, 6, 30)]
    out = []
    for x in rows:
        out.append(x)
    out.extend(q2)
    out.sort(key=lambda x: (dt.datetime.strptime(x[2], "%d/%m/%Y").date(), x[0]))
    return out


# ---- registers ------------------------------------------------------------------------------------------------
MREG_HEADER = ["MID", "Customer ID", "Trading name", "MCC", "Terminal", "Settlement account", "Opened", "Status"]
MCC = {"cafe": "5814", "takeaway": "5814", "barber": "7230", "nails": "7230", "carwash": "7542",
       "convenience": "5499", "launderette": "7211"}


def mreg_rows():
    r = random.Random(W.SEED + 19)
    rows = []
    for c in sorted(W.CUSTOMERS, key=lambda x: x["cid"]):
        for i, mid in enumerate(MIDS[c["cid"]]):
            opened = max(c["onboarded"], dt.date(2016, 1, 1)) + dt.timedelta(days=r.randint(10, 400) + 300 * i)
            rows.append([mid, c["cid"], c["name"].split(",")[0], MCC[c["trade"]],
                         r.choice(["Countertop", "Portable", "SoftPOS"]) if i == 0 else "Portable",
                         "%s %s" % (W.BRANCH[c["home"]][3], c["acct"]), opened.strftime("%d/%m/%Y"), "Active"])
    rows.extend(A.mreg_extra_rows())
    rows.sort(key=lambda x: x[1])
    return rows


SEG_HEADER = ["Customer ID", "Trading name", "Legal form", "Trade", "Home branch", "Current account",
              "Second account", "Till service", "Customer since", "Risk rating"]


def seg_rows():
    rows = []
    for c in sorted(W.CUSTOMERS, key=lambda x: (x["home"], x["cid"])):
        rows.append([c["cid"], c["name"], c["legal"], c["trade_label"], W.BRANCH[c["home"]][1],
                     "%s %s" % (W.BRANCH[c["home"]][3], c["acct"]),
                     ("%s %s" % (W.BRANCH[c["home"]][3], c["second_acct"])) if c["second_acct"] else "",
                     "Yes" if c["till"] else "No", c["onboarded"].strftime("%d/%m/%Y"), "High"])
    return rows


# ---- till service daily totals --------------------------------------------------------------------------------
TILL_HEADER = ["till_account", "customer_id", "trading_date", "z_report_no", "cash_sales", "card_sales",
               "other_tenders", "paid_outs", "gross_sales"]


def till_rows():
    T = S.truth()
    rows = []
    zmap = A.seg_till_z()
    for c in sorted(W.CUSTOMERS, key=lambda x: x["cid"]):
        if not c["till"]:
            continue
        t = T.cust[c["cid"]]
        tacct = "TS-%d" % (700000 + int(c["cid"].split("-")[1]))
        for zz in zmap[c["cid"]]:
            d = zz["day"]
            cash_sales = round(t["cash"][d] + t["paid_out"][d], 2)
            card_sales = round(t["card"][d] - t["refunds"].get(d, 0.0), 2)
            other = zz["other"]
            rows.append([tacct, c["cid"], d.isoformat(), zz["z"], "%.2f" % cash_sales, "%.2f" % card_sales,
                         "%.2f" % other, "%.2f" % t["paid_out"][d], "%.2f" % (cash_sales + card_sales + other)])
    return rows


# ---- distractors: a retail sales index, the branches' cash orders, An Post's office list -----------------------
RSI_HEADER = ["month", "sector", "value_index", "volume_index"]
RSI_SECTORS = [("Food, beverages and tobacco in specialised stores", 0.012), ("Bars", 0.018),
               ("Non-specialised stores", 0.009), ("Hardware, paints and glass", 0.006),
               ("Pharmaceutical, medical and cosmetic articles", 0.015), ("Motor trades", -0.004)]


def rsi_rows():
    r = random.Random(W.SEED + 211)
    rows = []
    for name, drift in RSI_SECTORS:
        v, q = r.uniform(104, 118), r.uniform(98, 106)
        for y in (2024, 2025, 2026):
            for m in range(1, 13):
                if y == 2026 and m > 9:
                    break
                v *= 1 + drift / 12 + r.gauss(0, 0.011)
                q *= 1 + drift / 24 + r.gauss(0, 0.010)
                seas = 1.0 + (0.11 if m == 12 else 0.0) - (0.05 if m == 1 else 0.0)
                rows.append(["%d-%02d" % (y, m), name, "%.1f" % (v * seas), "%.1f" % (q * seas)])
    return rows


ORDERS_HEADER = ["Week commencing", "Branch", "EUR 50 notes", "EUR 20 notes", "EUR 10 notes", "EUR 5 notes",
                 "Coin bags", "Order value (EUR)"]


def orders_rows():
    r = random.Random(W.SEED + 223)
    rows = []
    d = dt.date(2025, 9, 29)
    while d <= dt.date(2026, 9, 28):
        for b in W.BRANCHES:
            n50, n20, n10, n5 = (r.randint(0, 6) * 100, r.randint(2, 14) * 100, r.randint(1, 9) * 100,
                                 r.randint(0, 6) * 100)
            bags = r.randint(4, 40)
            val = n50 * 50 + n20 * 20 + n10 * 10 + n5 * 5 + bags * r.choice((20, 25, 50))
            rows.append([d.strftime("%d/%m/%Y"), b[1], n50, n20, n10, n5, bags, val])
        d += dt.timedelta(days=7)
    return rows


OFFICES_HEADER = ["Office code", "Office", "County", "Office type", "Mon to Fri", "Saturday"]


def offices_rows():
    r = random.Random(W.SEED + 227)
    rows = []
    for code, town, county, _ in W.OFFICES:
        typ = "Company office" if r.random() < 0.4 else "Sub-office"
        rows.append([code, town, county, typ, "09:00 to 17:30" if typ == "Company office" else "09:00 to 17:00",
                     "09:00 to 13:00"])
    return rows
