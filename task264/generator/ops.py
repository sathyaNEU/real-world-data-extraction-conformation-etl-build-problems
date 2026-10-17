"""The Authority's operating records: pay-machine transactions, the parking app's monthly statements, the car-park
counters' hourly counts, the asset register, the 2025-26 levy invoices, the bank's receipts export, the councils'
remittance advices, the supplier payments run, permit sales and the county's population estimates."""
from __future__ import annotations

import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import common as K
import world as W

APP_PROVIDER = "Quorvant Parking Ltd"
ACQUIRER = "Askvane Merchant Services"
JOINT = ("HNM", "WDS")                          # one shared finance service pays for both from July 2025
JOINT_PAYER = "HORNMERE&WENDSTOW SS"
SHORT_Q3 = "CHD"                                # paid its third instalment at the 2024-25 amount
PRIOR_Q4_ON_DUE = ["KDM", "RVW", "SNG", "LKS", "CHD", "FNC"]   # 2024-25 fourth instalments credited 31 March 2025
ADVICES = {"LKS": (1, 2, 3, 4), "GRB": (1, 2, 3, 4), "FNC": (2, 3, 4), "RVW": (1,)}   # the advices councils sent
SUPPLIERS = ["Elmthwaite Fencing Ltd", "Keldcote Tree Services", "Northern Grid Energy", "Askvane Merchant Services",
             "Hepsett Plant Hire", "Hornmere Print Co", "Ravenwick Waste Management", "Pudmere Builders Ltd",
             "Oakthwaite Ecology", "Ackhope Signs", "Clunside Water Services", "Lockstow Security"]
PAYERS = ["HOBSIDE CAFE LTD", "LOCKSHAW FARMS LTD", "UPLAND MASTS LTD", "CROWSIDE GRAZIERS", "NORTHERN UPLANDS TR"]
BANK_CLOSED = set(K.BANK_HOLIDAYS) | {dt.date(2025, 1, 1), dt.date(2026, 4, 3), dt.date(2026, 4, 6)}
# three machines, reconnected to the back office after its server was restored, sent their last few days' tickets
# again with the next night's upload
REPLAYS = [("PM-2102", dt.date(2025, 7, 15), dt.date(2025, 7, 19)), ("PM-2202", dt.date(2025, 8, 6), dt.date(2025, 8, 9)),
           ("PM-2402", dt.date(2025, 10, 28), dt.date(2025, 11, 2))]
SWAP_DW = dt.datetime(2025, 8, 18, 5, 40)        # UTC: C-04 out, C-09 in, before the gates opened
SWAP_LM_TH = dt.datetime(2025, 10, 14, 5, 50)     # UTC: C-07 from Thruscote to Lockshaw's valley car park
PARALLEL_GF = (dt.datetime(2026, 2, 3, 7, 0), dt.datetime(2026, 2, 24, 6, 30))   # C-10 in, C-05 out (UTC)


def _xl_header(ws, header, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2F5D50")
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.freeze_panes = "A2"


def utc(d, minute, second=0):
    """A local clock reading on date d (minutes after midnight) as a UTC datetime."""
    return dt.datetime(d.year, d.month, d.day) + dt.timedelta(minutes=int(minute) - 60 * W.utc_offset(d),
                                                              seconds=int(second))


# ---------------------------------------------------------------------------------------------- pay machines
def machine_rows(C):
    """The clean machine record: one row per machine payment, ticket numbers in sequence per machine."""
    r = W.rng("tickets")
    m = C["payer"] & ~C["app"]
    idx = np.nonzero(m)[0]
    rows = []
    for i in idx:
        d = C["date"][i]
        park = C["park"][i]
        band = int(C["band"][i])
        price = W.tariff(park, d)[band]
        paid = int(C["arrive"][i]) + int(r.integers(1, 9))
        sec = int(r.integers(0, 60))
        card = r.random() < (.85 if park == "DW" else .79)
        rows.append([str(C["machine"][i]), d, paid, sec, K.BANDS[band], price, "CARD" if card else "CASH",
                     str(C["cp"][i])])
    rows.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
    base = {}
    rb = W.rng("ticketbase")
    for x in rows:
        if x[0] not in base:
            base[x[0]] = int(rb.integers(20000, 60000))
        base[x[0]] += 1
        x.append(base[x[0]])
    return rows                  # machine, date, minute, second, band, price, method, car park, ticket


def write_transactions(path, rows):
    """The pay-machine back office's export, by upload: each machine uploads its day's tickets overnight, and three
    machines re-sent their last few days' tickets with a later night's upload."""
    by = {}
    for x in rows:
        by.setdefault((x[0], x[1]), []).append(x)
    uploads = []
    for (mid, d), xs in sorted(by.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        uploads.append((d + dt.timedelta(days=1), mid, d, xs))
    replay = {}
    for mid, a, b in REPLAYS:
        replay[(mid, b + dt.timedelta(days=1))] = [a + dt.timedelta(days=k) for k in range((b - a).days + 1)]
    out = []
    for up_date, mid, d, xs in uploads:
        batch = []
        for d0 in replay.get((mid, d), []):
            batch += by.get((mid, d0), [])
        batch += xs
        uploads_id = "%s-%s" % (mid.split("-")[1], (d + dt.timedelta(days=1)).strftime("%Y%m%d"))
        for x in batch:
            out.append((uploads_id, x))
    n = 0
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["txn_id", "upload_id", "machine_id", "ticket_no", "paid_at_utc", "tariff_code", "amount_gbp",
                    "payment_type"])
        for up, x in out:
            n += 1
            when = utc(x[1], x[2], x[3]).strftime("%Y-%m-%dT%H:%M:%SZ")
            w.writerow(["MT%08d" % (40117233 + n * 3 + (n % 7)), up, x[0], x[8], when, x[4], "%.2f" % x[5], x[6]])
    return n


# ---------------------------------------------------------------------------------------------- the parking app
def app_lines(C):
    """Sessions by calendar month, car park and tariff band, with the provider's figures: parking income stated
    without VAT, its commission at 9 per cent, and the net payable."""
    m = C["app"]
    agg = {}
    for i in np.nonzero(m)[0]:
        d = C["date"][i]
        key = (d.year, d.month, str(C["cp"][i]), int(C["band"][i]), W.tariff(str(C["park"][i]), d)[int(C["band"][i])])
        agg[key] = agg.get(key, 0) + 1
    lines = []
    for (y, mo, cp, b, price), n in sorted(agg.items()):
        inc = round(n * price / (1 + K.VAT), 2)
        com = round(inc * .09, 2)
        lines.append(dict(year=y, month=mo, cp=cp, band=K.BANDS[b], price=price, sessions=n, income=inc,
                          commission=com, net=round(inc - com, 2)))
    return lines


SITE_LABEL = {"GF-M": "DVRPA Gorthfield Main", "GF-L": "DVRPA Gorthfield Lakeside", "DW-1": "DVRPA Water Park",
              "LM-S": "DVRPA Lockshaw Summit", "LM-V": "DVRPA Lockshaw Valley", "TH-1": "DVRPA Thruscote Hall"}


def write_app(path, lines):
    wb = Workbook()
    ws = wb.active
    ws.title = "Statement lines"
    _xl_header(ws, ["Statement month", "Location", "Location code", "Tariff", "Sessions", "Parking income (GBP)",
                    "Commission (GBP)", "Net payable (GBP)"], [15, 28, 14, 16, 10, 18, 16, 16])
    for ln in lines:
        ws.append([dt.date(ln["year"], ln["month"], 1).strftime("%b %Y"), SITE_LABEL[ln["cp"]],
                   "LOC-%s" % ln["cp"].replace("-", ""), K.BAND_NAME[ln["band"]], ln["sessions"], ln["income"],
                   ln["commission"], ln["net"]])
    for row in ws.iter_rows(min_row=2, min_col=6, max_col=8):
        for c in row:
            c.number_format = "#,##0.00"
    ws2 = wb.create_sheet("Account")
    for line in ["Client: Daskbeck Valley Regional Park Authority (account DVR-0412)",
                 "Statement period: April 2025 to March 2026, one line per location, tariff and month of parking.",
                 "Commission: 9 per cent of parking income under the 2023 service agreement.",
                 "Prepared by %s client accounts, 8 April 2026." % APP_PROVIDER]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 100
    wb.save(path)
    return len(lines)


def write_tariffs(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tariffs 2025-26"
    _xl_header(ws, ["Car park", "Car park code", "Tariff", "Charge (GBP)", "Applies"], [32, 13, 16, 13, 30])
    for cp in K.CP_CODES:
        park = K.CP_PARK[cp]
        for b, band in enumerate(K.BANDS):
            if park in K.TARIFF_HIGH:
                ws.append([K.CP_NAME[cp], cp, K.BAND_NAME[band], K.TARIFF[park][b], "Outside 1 July to 31 August"])
                ws.append([K.CP_NAME[cp], cp, K.BAND_NAME[band], K.TARIFF_HIGH[park][b], "1 July to 31 August"])
            else:
                ws.append([K.CP_NAME[cp], cp, K.BAND_NAME[band], K.TARIFF[park][b], "All year"])
    for c in ws["D"][1:]:
        c.number_format = "0.00"
    ws2 = wb.create_sheet("Notes")
    for line in ["Car park charges from 1 April 2025, as approved by the Authority's members on 23 January 2025.",
                 "Charges include VAT at the standard rate of 20 per cent.",
                 "Annual permit holders and Blue Badge holders park free of charge.",
                 "Brathden Woods and Crowside Common car parks are free."]:
        ws2.append([line])
    ws2.column_dimensions["A"].width = 100
    wb.save(path)


# ---------------------------------------------------------------------------------------------- counters
def counts(C):
    """Hourly counts per counter as the loggers send them: entries at single-loop counters, every pass in and out
    at the Water Park's replacement loop; hours in UTC."""
    ent, ext = {}, {}
    for i in range(len(C["cp"])):
        d = C["date"][i]
        cp = str(C["cp"][i])
        a = utc(d, int(C["arrive"][i])).replace(minute=0, second=0)
        b = utc(d, int(C["leave"][i])).replace(minute=0, second=0)
        ent[(cp, a)] = ent.get((cp, a), 0) + 1
        ext[(cp, b)] = ext.get((cp, b), 0) + 1
    start = dt.datetime(2025, 3, 31, 23, 0)
    end = dt.datetime(2026, 3, 31, 22, 0)
    hours = []
    h = start
    while h <= end:
        hours.append(h)
        h += dt.timedelta(hours=1)
    plan = {"C-01": [("GF-M", start, None, False)],
            "C-05": [("GF-L", start, PARALLEL_GF[1], False)],
            "C-10": [("GF-L", PARALLEL_GF[0], None, False)],
            "C-04": [("DW-1", start, SWAP_DW, False)],
            "C-09": [("DW-1", SWAP_DW, None, True)],
            "C-06": [("LM-S", start, None, False)],
            "C-08": [("LM-V", start, SWAP_LM_TH, False)],
            "C-07": [("TH-1", start, SWAP_LM_TH, False), ("LM-V", SWAP_LM_TH, None, False)],
            "C-11": [("TH-1", SWAP_LM_TH, None, False)]}
    rows = []
    for cid, spans in plan.items():
        for h in hours:
            for cp, a, b, both in spans:
                if h >= a.replace(minute=0) and (b is None or h < b.replace(minute=0)):
                    n = ent.get((cp, h), 0) + (ext.get((cp, h), 0) if both else 0)
                    rows.append((cid, h, n))
                    break
    rows.sort(key=lambda x: (x[1], x[0]))
    return rows, ent, ext


def write_counts(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["counter_id", "hour_start_utc", "vehicles"])
        for cid, h, n in rows:
            w.writerow([cid, h.strftime("%Y-%m-%d %H:%M"), n])
    return len(rows)


def write_assets(path):
    rows = [
        ("PM-2101", "Pay machine", "GF-M", "Metric Elite 3", "2019-05-21", "", "In service"),
        ("PM-2102", "Pay machine", "GF-M", "Metric Elite 3", "2019-05-21", "", "In service"),
        ("PM-2103", "Pay machine", "DW-1", "Metric Elite 3", "2021-06-14", "", "In service"),
        ("PM-2104", "Pay machine", "GF-L", "Metric Elite 3", "2021-06-14", "", "In service"),
        ("PM-2201", "Pay machine", "DW-1", "Metric Elite 3", "2018-03-02", "", "In service"),
        ("PM-2202", "Pay machine", "DW-1", "Metric Elite 3", "2018-03-02", "", "In service"),
        ("PM-2203", "Pay machine", "DW-1", "Metric Elite 2", "2014-04-09", "2025-08-31", "Disposed"),
        ("PM-2301", "Pay machine", "LM-S", "Metric Elite 3", "2020-07-30", "", "In service"),
        ("PM-2302", "Pay machine", "LM-V", "Metric Elite 3", "2020-07-30", "", "In service"),
        ("PM-2401", "Pay machine", "TH-1", "Metric Elite 3", "2019-09-12", "", "In service"),
        ("PM-2402", "Pay machine", "TH-1", "Metric Elite 3", "2022-04-04", "", "In service"),
        ("C-01", "Vehicle counter", "GF-M", "SX-1", "2017-08-15", "", "In service"),
        ("C-04", "Vehicle counter", "DW-1", "SX-1", "2017-08-15", "2025-08-18", "Removed"),
        ("C-05", "Vehicle counter", "GF-L", "SX-1", "2017-08-16", "2026-02-24", "Removed"),
        ("C-06", "Vehicle counter", "LM-S", "SX-1", "2018-05-03", "", "In service"),
        ("C-07", "Vehicle counter", "LM-V", "SX-1", "2019-03-11", "", "In service"),
        ("C-08", "Vehicle counter", "LM-V", "SX-1", "2018-05-03", "2025-10-14", "Removed"),
        ("C-09", "Vehicle counter", "DW-1", "BX-2", "2025-08-18", "", "In service"),
        ("C-10", "Vehicle counter", "GF-L", "SX-2", "2026-02-03", "", "In service"),
        ("C-11", "Vehicle counter", "TH-1", "SX-2", "2025-10-14", "", "In service"),
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["asset_id", "asset_type", "site_code", "site_name", "model", "installed", "removed", "status"])
        for a in rows:
            w.writerow([a[0], a[1], a[2], K.CP_NAME[a[2]], a[3], a[4], a[5], a[6]])
    return len(rows)


# ---------------------------------------------------------------------------------------------- the 2025-26 levy
INV_BASE = {1: (dt.date(2025, 3, 3), dt.date(2025, 4, 15), 187), 2: (dt.date(2025, 6, 2), dt.date(2025, 7, 15), 612),
            3: (dt.date(2025, 9, 1), dt.date(2025, 10, 15), 1043), 4: (dt.date(2026, 2, 2), dt.date(2026, 3, 31), 141)}
PRIOR_Q4 = (dt.date(2025, 2, 3), dt.date(2025, 3, 31), 129)        # the 2024-25 fourth instalments


def working(d):
    return d.weekday() < 5 and d not in BANK_CLOSED


def next_working(d):
    d += dt.timedelta(days=1)
    while not working(d):
        d += dt.timedelta(days=1)
    return d


def roll(d):
    while not working(d):
        d += dt.timedelta(days=1)
    return d


def invoices():
    amt, inst = W.levy_2025()
    out = []
    for q in (1, 2, 3, 4):
        issue, due, base = INV_BASE[q]
        for k, c in enumerate(K.CODES):
            no = ("INV26-%04d" if q == 4 else "INV25-%04d") % (base + k)
            out.append(dict(no=no, code=c, q=q, issue=issue, due=due, amount=inst[c][q - 1]))
    return out


def prior_invoices():
    amt, inst = W.levy_2024()
    issue, due, base = PRIOR_Q4
    return [dict(no="INV25-%04d" % (base + k), code=c, q=4, issue=issue, due=due, amount=inst[c][3])
            for k, c in enumerate(K.CODES)]


def payments(inv):
    """Every levy payment as it happened: who paid, the day the bank credited it (the value date), the reference
    quoted, the amount and the invoices it covers. The fourth instalments were all paid on their due date, 31 March
    2026; the shared finance service pays for Hornmere and Wendstow in one transfer from July 2025."""
    r = W.rng("levypay")
    by = {(i["code"], i["q"]): i for i in inv}
    _, inst24 = W.levy_2024()
    pays = []
    for i in prior_invoices():
        if i["code"] in PRIOR_Q4_ON_DUE:
            pays.append(dict(payer=i["code"], q=0, value=i["due"], ref="%s LEVY Q4" % i["no"], amount=i["amount"],
                             covers=[(i["no"], i["amount"])]))
    for q in (1, 2, 3, 4):
        for c in K.CODES:
            i = by[(c, q)]
            if c in JOINT and q > 1:
                continue
            if q == 4:
                vd = i["due"]
            else:
                vd = roll(i["due"] + dt.timedelta(days=int(r.choice([-3, -2, -1, 0, 0, 0, 1, 2, 5, 9]))))
            amount = inst24[c][2] if (c == SHORT_Q3 and q == 3) else i["amount"]
            pays.append(dict(payer=c, q=q, value=vd, ref="%s LEVY Q%d" % (i["no"], q), amount=amount,
                             covers=[(i["no"], amount)]))
        if q > 1:
            a, b = by[(JOINT[0], q)], by[(JOINT[1], q)]
            vd = a["due"] if q == 4 else roll(a["due"] - dt.timedelta(days=1))
            pays.append(dict(payer="JOINT", q=q, value=vd, ref="%s DVRPA LEVY" % a["no"], amount=a["amount"] + b["amount"],
                             covers=[(a["no"], a["amount"]), (b["no"], b["amount"])]))
    for p in pays:
        p["post"] = next_working(p["value"])
    return pays


BANK_NAME = {"KDM": "KELDMERE DISTRICT C", "RVW": "RAVENWICK BC", "SNG": "SNELGARTH DC", "LKS": "LARKSTEAD BORO COUN",
             "GRB": "GRINBURY D C", "HNM": "HORNMERE DC", "CHD": "CHALDALE DISTRICT", "WDS": "WENDSTOW DC",
             "FNC": "FERNCOTE BOROUGH CO", "JOINT": JOINT_PAYER}


def write_invoices(path, inv):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["invoice_no", "customer_code", "customer", "issue_date", "due_date", "description", "amount_gbp"])
        for i in sorted(inv, key=lambda x: (x["issue"], x["no"])):
            w.writerow([i["no"], i["code"], K.NAME[i["code"]], i["issue"].isoformat(), i["due"].isoformat(),
                        "Levy 2025-26, instalment %d of 4" % i["q"], "%.2f" % i["amount"]])
    return len(inv)


def other_receipts(T, mrows, lines):
    """The rest of the account's credits, by the day the bank credited them: the acquirer's card settlements two
    working days after the takings, cash banked from the machines each Tuesday, the app provider's monthly
    remittances, bookings, the cafe concession and grants."""
    r = W.rng("otherreceipts")
    out = []
    card, cash = {}, {}
    for x in mrows:
        (card if x[6] == "CARD" else cash)[x[1]] = (card if x[6] == "CARD" else cash).get(x[1], 0) + x[5]
    settle = {}
    for d0, amt in card.items():
        v = next_working(next_working(d0))
        settle[v] = settle.get(v, 0) + amt
    for v, amt in sorted(settle.items()):
        fee = round(amt * .0145, 2)
        out.append((v, "BGC", ACQUIRER.upper()[:19], "SETTLEMENT %s" % v.strftime("%d%m"), round(amt - fee, 2)))
    d = K.YEAR0
    while d <= dt.date(2026, 4, 2):
        if d.weekday() == 1 and working(d):
            wk = sum(cash.get(d - dt.timedelta(days=k), 0) for k in range(1, 8))
            if wk:
                out.append((d, "CSH", "CASH PAID IN", "MACHINES WK %s" % d.strftime("%d%m"), round(wk, 2)))
        d += dt.timedelta(days=1)
    bym = {}
    for ln in lines:
        bym[(ln["year"], ln["month"])] = bym.get((ln["year"], ln["month"]), 0) + ln["net"] * (1 + K.VAT)
    for (y, mo), v in sorted(bym.items()):
        pd_ = roll(dt.date(y + (mo == 12), mo % 12 + 1, 1) + dt.timedelta(days=13))
        out.append((pd_, "BGC", APP_PROVIDER.upper()[:19], "DVR-0412 %02d/%d" % (mo, y), round(v, 2)))
    kinds = [("WEDDING DEPOSIT", 950), ("WEDDING BALANCE", 4200), ("ROOM HIRE", 240), ("SCHOOL VISIT", 180),
             ("THRUSCOTE EVENTS", 1800), ("FILMING FEE", 3600)]
    for k in range(214):
        dd = roll(dt.date(2025, 3, 31) + dt.timedelta(days=int(r.integers(0, 368))))
        kind, base = kinds[int(r.choice(len(kinds), p=[.2, .16, .26, .22, .12, .04]))]
        out.append((dd, "FPI", kind, "BKG%05d" % int(r.integers(10000, 99999)),
                    round(base * float(r.uniform(.8, 1.3)), 2)))
    for mo in range(4, 16):
        y, m = 2025 + (mo > 12), (mo - 1) % 12 + 1
        out.append((roll(dt.date(y, m, 5)), "BGC", "HOBSIDE CAFE LTD", "CONCESSION FEE", 2875.00))
        if m in (4, 7, 10, 1):
            out.append((roll(dt.date(y, m, 1)), "BGC", "LOCKSHAW FARMS LTD", "TENANCY RENT QTR", 7850.00))
    out.append((roll(dt.date(2025, 4, 25)), "BGC", "UPLAND MASTS LTD", "SITE 04471 ANNUAL", 11200.00))
    for d in (dt.date(2025, 5, 2), dt.date(2025, 11, 3)):
        out.append((roll(d), "FPI", "CROWSIDE GRAZIERS", "GRAZING LICENCE", 4180.00))
    out.append((dt.date(2025, 6, 24), "BGC", "NORTHERN UPLANDS TR", "GRANT 25/117 TRANCHE 1", 48500.00))
    out.append((dt.date(2025, 12, 16), "BGC", "NORTHERN UPLANDS TR", "GRANT 25/117 TRANCHE 2", 36250.00))
    return [(next_working(v), v, t, desc, ref, amt) for v, t, desc, ref, amt in out]


EXPORT_FROM, EXPORT_TO = dt.date(2025, 4, 1), dt.date(2026, 4, 7)


def write_receipts(path, pays, others):
    """The finance system's cash book for the main account: each credit as the morning's bank statement import
    posted it (Date) with the bank's value date, 1 April 2025 to 7 April 2026 by Date."""
    rows = []
    for p in pays:
        rows.append((p["post"], p["value"], "BGC", BANK_NAME[p["payer"]], p["ref"], float(p["amount"])))
    rows += others
    rows = [x for x in rows if EXPORT_FROM <= x[0] <= EXPORT_TO]
    rows.sort(key=lambda x: (x[0], x[1], x[3], x[5]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Date", "Value date", "Type", "Description", "Reference", "Amount"])
        for x in rows:
            w.writerow([x[0].strftime("%d/%m/%Y"), x[1].strftime("%d/%m/%Y"), x[2], x[3], x[4], "%.2f" % x[5]])
    return len(rows)


def write_remittances(path, pays, inv):
    """The remittance advices the finance team holds for 2025-26 levy payments: the shared finance service's, one
    line per invoice its transfer covers, and those some councils send with their payments."""
    r = W.rng("remit")
    nos = {i["no"] for i in inv}
    lines = []
    for p in pays:
        if p["payer"] != "JOINT" and p["q"] not in ADVICES.get(p["payer"], ()):
            continue
        if not all(no in nos for no, _ in p["covers"]):
            continue
        payer = "Hornmere and Wendstow Shared Services" if p["payer"] == "JOINT" else K.NAME[p["payer"]]
        adv = "RA%06d" % int(r.integers(100000, 999999))
        for no, amt in p["covers"]:
            lines.append((p["value"], payer, adv, no, amt))
    lines.sort(key=lambda x: (x[0], x[1], x[3]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["payment_date", "payer", "advice_ref", "invoice_no", "amount_gbp"])
        for x in lines:
            w.writerow([x[0].isoformat(), x[1], x[2], x[3], "%.2f" % x[4]])
    return len(lines)


def write_supplier_payments(path, inv):
    """The accounts-payable runs: suppliers, utilities and contractors, every Thursday."""
    r = W.rng("ap")
    sup = SUPPLIERS
    rows = []
    d = K.YEAR0
    while d <= dt.date(2026, 4, 7):
        if d.weekday() == 3:
            for _ in range(int(r.integers(4, 11))):
                s = str(r.choice(sup))
                rows.append((d, s, "AP%06d" % int(r.integers(100000, 999999)), "Invoice %s" % int(r.integers(1000, 99999)),
                             round(float(r.lognormal(7.4, 1.0)), 2)))
        d += dt.timedelta(days=1)
    rows.sort(key=lambda x: (x[0], x[2]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["payment_date", "payee", "payment_ref", "description", "amount_gbp"])
        for x in rows:
            w.writerow([x[0].isoformat(), x[1], x[2], x[3], "%.2f" % x[4]])
    return len(rows)


# ---------------------------------------------------------------------------------------------- distractors
def write_permits(path):
    """Annual parking permits sold for 2025-26, by the holder's home area."""
    r = W.rng("permits")
    share = {"KDM": .21, "RVW": .24, "SNG": .17, "LKS": .06, "GRB": .05, "HNM": .05, "CHD": .06, "WDS": .04,
             "FNC": .04, "OUT": .08}
    codes = list(share)
    p = np.array([share[c] for c in codes])
    p /= p.sum()
    rows = []
    for k in range(2683):
        d = K.YEAR0 + dt.timedelta(days=int(min(364, r.exponential(70))))
        kind = str(r.choice(["Standard", "Concession", "Second vehicle"], p=[.71, .21, .08]))
        rows.append((d, str(r.choice(["Gorthfield visitor centre", "Thruscote Hall shop", "Online"], p=[.3, .2, .5])),
                     str(r.choice(codes, p=p)), kind))
    rows.sort()
    price = {"Standard": "60.00", "Concession": "42.00", "Second vehicle": "30.00"}
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["permit_no", "issued_on", "issued_at", "holder_area", "permit_type", "valid_until", "price_gbp"])
        for k, (d, at, c, kind) in enumerate(rows):
            w.writerow(["AP25-%05d" % (k + 3101), d.isoformat(), at, c, kind,
                        (d.replace(year=d.year + 1) - dt.timedelta(days=1)).isoformat(), price[kind]])
    return len(rows)


def write_population(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Mid-year estimates"
    _xl_header(ws, ["Council", "Mid-2023", "Mid-2024", "Mid-2025"], [32, 12, 12, 12])
    for c in K.CODES:
        ws.append([K.NAME[c]] + list(W.POP[c]))
    ws2 = wb.create_sheet("Mid-2025 by age")
    _xl_header(ws2, ["Council", "0-15", "16-24", "25-44", "45-64", "65 and over", "All ages"], [32, 10, 10, 10, 10, 12, 11])
    r = W.rng("agesplit")
    for c in K.CODES:
        a16 = W.ADULTS[c]
        tot = W.POP[c][2]
        sh = np.array([.13, .31, .32, .24]) * r.lognormal(0, .04, 4)
        sh /= sh.sum()
        parts = [int(round(a16 * x)) for x in sh]
        parts[-1] = a16 - sum(parts[:-1])
        ws2.append([K.NAME[c], tot - a16] + parts + [tot])
    ws3 = wb.create_sheet("Notes")
    for line in ["Population estimates for the county's districts, usual residents at 30 June.",
                 "Prepared by the county council's research and intelligence team from the national mid-year "
                 "estimates; mid-2025 published 2 July 2026."]:
        ws3.append([line])
    ws3.column_dimensions["A"].width = 100
    wb.save(path)
