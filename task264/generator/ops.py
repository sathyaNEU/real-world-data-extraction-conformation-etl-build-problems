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
JOINT = ("HNM", "WDS")                          # one shared finance service pays for both from January 2026
JOINT_PAYER = "HORNMERE&WENDSTOW SS"
SHORT_Q3 = "CHD"                                # paid its third instalment at the 2024-25 amount
PRIOR_Q4_ON_DUE = ["KDM", "RVW", "SNG", "LKS", "CHD", "FNC"]   # 2024-25 fourth instalments credited 31 March 2025
# each council's habit: the calendar days after an instalment's due date (before, if negative) its payment reached the
# bank, moved on to the next working day; Keldmere pays on its Tuesday payment run on or after the due date; the
# shared finance service Hornmere and Wendstow set up in January 2026 pays their fourth instalments (JOINT_DAYS)
HABIT = {"KDM": "tuesday", "RVW": (0, 3, 0, 0), "SNG": (0, 0, 0, 0), "LKS": (-4, -6, 0, 0), "GRB": (2, 0, 9, 8),
         "HNM": (0, 2, 0), "WDS": (-1, 2, 0), "CHD": (5, 0, -2, 0), "FNC": (1, 0, 0, 0)}
JOINT_DAYS = {4: 0}
MISKEYED = {("FNC", 4): "GRB"}                  # Ferncote's fourth payment quoted Grinbury's fourth invoice
# the reference each council's payments system writes: most quote the invoice; Keldmere its payment run, Ravenwick its
# remittance number and Chaldale its own description
REF_STYLE = {"KDM": "KDC PAYRUN %(d)s", "RVW": "RBC REMIT %(n)06d", "CHD": "CHALDALE DVRPA Q%(q)d"}
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


# the year's other invoices to member councils: the ranger service agreements (quarterly in advance), the rights of
# way maintenance contributions (raised with April's invoices) and recharges for events councils held at the visitor
# centres; each falls due 30 days after it is raised and takes the sales series' next numbers on its day
RANGER = {"KDM": 8412.50, "RVW": 6937.25, "GRB": 4861.75}
RANGER_RAISED = {1: (dt.date(2025, 4, 1), "INV25-%04d", 274, "April to June 2025"),
                 2: (dt.date(2025, 7, 1), "INV25-%04d", 738, "July to September 2025"),
                 3: (dt.date(2025, 10, 1), "INV25-%04d", 1166, "October to December 2025"),
                 4: (dt.date(2026, 1, 2), "INV26-%04d", 4, "January to March 2026")}
ROW = {"SNG": 5284.00, "LKS": 3917.60, "HNM": 4406.40, "WDS": 3652.80, "CHD": 2978.40, "FNC": 3215.20}
ROW_RAISED = (dt.date(2025, 4, 1), 277)
EVENTS = {"CHD": (dt.date(2025, 6, 2), 621, 1184.65, "17 May 2025"), "FNC": (dt.date(2025, 6, 2), 622, 846.30, "24 May 2025"),
          "HNM": (dt.date(2025, 9, 1), 1052, 2317.90, "9 August 2025"),
          "WDS": (dt.date(2025, 9, 1), 1053, 1968.45, "16 August 2025")}
# the sundry invoice a council's payment run took with an instalment
WITH = {("KDM", 1): ("ranger", 1), ("KDM", 2): ("ranger", 2), ("KDM", 3): ("ranger", 3),
        ("RVW", 1): ("ranger", 1), ("RVW", 2): ("ranger", 2), ("SNG", 1): ("row", 0), ("LKS", 1): ("row", 0),
        ("GRB", 1): ("ranger", 1), ("GRB", 2): ("ranger", 2), ("HNM", 2): ("row", 0), ("HNM", 3): ("events", 0),
        ("WDS", 2): ("row", 0), ("WDS", 3): ("events", 0), ("CHD", 1): ("row", 0), ("CHD", 2): ("events", 0),
        ("FNC", 1): ("row", 0), ("FNC", 2): ("events", 0)}
# the sundry invoices paid on their own, and the day each reached the bank
ALONE = {("KDM", "ranger", 4): dt.date(2026, 1, 27), ("RVW", "ranger", 3): dt.date(2025, 10, 30),
         ("RVW", "ranger", 4): dt.date(2026, 1, 29), ("GRB", "ranger", 3): dt.date(2025, 11, 12),
         ("GRB", "ranger", 4): dt.date(2026, 2, 16)}


def invoices():
    """The 2025-26 levy's instalment invoices."""
    amt, inst = W.levy_2025()
    out = []
    for q in (1, 2, 3, 4):
        issue, due, base = INV_BASE[q]
        for k, c in enumerate(K.CODES):
            no = ("INV26-%04d" if q == 4 else "INV25-%04d") % (base + k)
            out.append(dict(no=no, code=c, kind="levy", q=q, issue=issue, due=due, amount=inst[c][q - 1],
                            text="Levy 2025-26, instalment %d of 4" % q))
    return out


def sundry_invoices():
    out = []
    for q, (issue, fmt, base, period) in RANGER_RAISED.items():
        for k, c in enumerate(sorted(RANGER, key=K.CODES.index)):
            out.append(dict(no=fmt % (base + k), code=c, kind="ranger", q=q, issue=issue,
                            due=issue + dt.timedelta(days=30), amount=RANGER[c],
                            text="Ranger service agreement, %s" % period))
    issue, base = ROW_RAISED
    for k, c in enumerate(sorted(ROW, key=K.CODES.index)):
        out.append(dict(no="INV25-%04d" % (base + k), code=c, kind="row", q=0, issue=issue,
                        due=issue + dt.timedelta(days=30), amount=ROW[c],
                        text="Rights of way maintenance contribution 2025-26"))
    for c, (issue, n, a, when) in EVENTS.items():
        out.append(dict(no="INV25-%04d" % n, code=c, kind="events", q=0, issue=issue,
                        due=issue + dt.timedelta(days=30), amount=a,
                        text="Visitor centre event recharge, %s" % when))
    return out


def all_invoices():
    return invoices() + sundry_invoices()


def prior_invoices():
    amt, inst = W.levy_2024()
    issue, due, base = PRIOR_Q4
    return [dict(no="INV25-%04d" % (base + k), code=c, q=4, issue=issue, due=due, amount=inst[c][3])
            for k, c in enumerate(K.CODES)]


def value_day(c, q, due):
    """The day the bank credited council c's payment of instalment q."""
    h = HABIT[c]
    if h == "tuesday":
        d = due
        while d.weekday() != 1 or not working(d):
            d += dt.timedelta(days=1)
        return d
    return roll(due + dt.timedelta(days=h[q - 1]))


def payments(inv):
    """Every payment from a member council as it happened: who paid, the day the bank credited it (the value date),
    the reference quoted, the amount and the invoices it covers. Each council pays its instalments on its own habit,
    its payment run taking any sundry invoice it then had with the instalment and quoting the instalment; the shared
    finance service pays Hornmere's and Wendstow's fourth instalments in one transfer, quoting Hornmere's invoice;
    Ferncote's fourth payment quoted Grinbury's fourth invoice."""
    by = {(i["code"], i["kind"], i["q"]): i for i in inv}
    _, inst24 = W.levy_2024()
    rr = W.rng("payref")
    pays = []
    for i in prior_invoices():
        if i["code"] in PRIOR_Q4_ON_DUE:
            pays.append(dict(payer=i["code"], q=0, value=i["due"], ref="%s LEVY Q4" % i["no"], amount=i["amount"],
                             covers=[(i["no"], i["amount"])]))
    for q in (1, 2, 3, 4):
        for c in K.CODES:
            i = by[(c, "levy", q)]
            if c in JOINT and q == 4:
                continue
            amount = inst24[c][2] if (c == SHORT_Q3 and q == 3) else i["amount"]
            quoted = by[(MISKEYED[(c, q)], "levy", q)]["no"] if (c, q) in MISKEYED else i["no"]
            vd = value_day(c, q, i["due"])
            covers = [(i["no"], amount)]
            if (c, q) in WITH:
                s = by[(c,) + WITH[(c, q)]]
                covers.append((s["no"], s["amount"]))
            ref = (REF_STYLE[c] % dict(d=vd.strftime("%d%m%y"), n=int(rr.integers(100000, 999999)), q=q)
                   if c in REF_STYLE else "%s LEVY Q%d" % (quoted, q))
            pays.append(dict(payer=c, q=q, value=vd, ref=ref, amount=round(sum(a for _, a in covers), 2),
                             covers=covers))
        if q == 4:
            a, b = by[(JOINT[0], "levy", 4)], by[(JOINT[1], "levy", 4)]
            vd = roll(a["due"] + dt.timedelta(days=JOINT_DAYS[4]))
            pays.append(dict(payer="JOINT", q=4, value=vd, ref="%s DVRPA LEVY" % a["no"],
                             amount=round(a["amount"] + b["amount"], 2),
                             covers=[(a["no"], a["amount"]), (b["no"], b["amount"])]))
    for (c, kind, q), vd in sorted(ALONE.items(), key=lambda kv: kv[1]):
        s = by[(c, kind, q)]
        ref = (REF_STYLE[c] % dict(d=vd.strftime("%d%m%y"), n=int(rr.integers(100000, 999999)), q=q)
               if c in REF_STYLE else "%s DVRPA" % s["no"])
        pays.append(dict(payer=c, q=None, value=vd, ref=ref, amount=s["amount"], covers=[(s["no"], s["amount"])]))
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
                        i["text"], "%.2f" % i["amount"]])
    return len(inv)


def other_receipts(T, mrows, lines):
    """The rest of the account's credits, by the day the bank credited them, with the income account the finance
    team posts each to: the acquirer's card settlements two working days after the takings, cash banked from the
    machines each Tuesday, the app provider's monthly remittances, bookings, the cafe concession, rents and grants."""
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
        out.append((v, "BGC", ACQUIRER.upper()[:19], "SETTLEMENT %s" % v.strftime("%d%m"), round(amt - fee, 2),
                    "4410 Car parks: card takings"))
    d = K.YEAR0
    while d <= dt.date(2026, 4, 2):
        if d.weekday() == 1 and working(d):
            wk = sum(cash.get(d - dt.timedelta(days=k), 0) for k in range(1, 8))
            if wk:
                out.append((d, "CSH", "CASH PAID IN", "MACHINES WK %s" % d.strftime("%d%m"), round(wk, 2),
                            "4411 Car parks: cash takings"))
        d += dt.timedelta(days=1)
    bym = {}
    for ln in lines:
        bym[(ln["year"], ln["month"])] = bym.get((ln["year"], ln["month"]), 0) + ln["net"] * (1 + K.VAT)
    for (y, mo), v in sorted(bym.items()):
        pd_ = roll(dt.date(y + (mo == 12), mo % 12 + 1, 1) + dt.timedelta(days=13))
        out.append((pd_, "BGC", APP_PROVIDER.upper()[:19], "DVR-0412 %02d/%d" % (mo, y), round(v, 2),
                    "4412 Car parks: app takings"))
    kinds = [("WEDDING DEPOSIT", 950), ("WEDDING BALANCE", 4200), ("ROOM HIRE", 240), ("SCHOOL VISIT", 180),
             ("THRUSCOTE EVENTS", 1800), ("FILMING FEE", 3600)]
    for k in range(214):
        dd = roll(dt.date(2025, 3, 31) + dt.timedelta(days=int(r.integers(0, 368))))
        kind, base = kinds[int(r.choice(len(kinds), p=[.2, .16, .26, .22, .12, .04]))]
        out.append((dd, "FPI", kind, "BKG%05d" % int(r.integers(10000, 99999)),
                    round(base * float(r.uniform(.8, 1.3)), 2), "4510 Venue hire and events"))
    for mo in range(4, 16):
        y, m = 2025 + (mo > 12), (mo - 1) % 12 + 1
        out.append((roll(dt.date(y, m, 5)), "BGC", "HOBSIDE CAFE LTD", "CONCESSION FEE", 2875.00, "4520 Concessions"))
        if m in (4, 7, 10, 1):
            out.append((roll(dt.date(y, m, 1)), "BGC", "LOCKSHAW FARMS LTD", "TENANCY RENT QTR", 7850.00,
                        "4530 Rents and licences"))
    out.append((roll(dt.date(2025, 4, 25)), "BGC", "UPLAND MASTS LTD", "SITE 04471 ANNUAL", 11200.00,
                "4530 Rents and licences"))
    for d in (dt.date(2025, 5, 2), dt.date(2025, 11, 3)):
        out.append((roll(d), "FPI", "CROWSIDE GRAZIERS", "GRAZING LICENCE", 4180.00, "4530 Rents and licences"))
    out.append((dt.date(2025, 6, 24), "BGC", "NORTHERN UPLANDS TR", "GRANT 25/117 TRANCHE 1", 48500.00, "4610 Grants"))
    out.append((dt.date(2025, 12, 16), "BGC", "NORTHERN UPLANDS TR", "GRANT 25/117 TRANCHE 2", 36250.00, "4610 Grants"))
    return out


EXPORT_FROM, EXPORT_TO = dt.date(2025, 4, 1), dt.date(2026, 4, 7)
CASHBOOK_TO = dt.date(2026, 3, 31)              # the finance system's year, by posting date
LEVY_ACCOUNT = "1120 Levy debtors"
SUNDRY_ACCOUNT = "1130 Sundry debtors"


def credits(pays, others):
    """Every credit to the main account with its bank reference, in value-date order: the levy payments and the
    rest. The bank numbers its credits in the order it books them."""
    rows = []
    for p in pays:
        rows.append(dict(value=p["value"], type="BGC", remitter=BANK_NAME[p["payer"]], ref=p["ref"],
                         amount=float(p["amount"]), pay=p))
    for v, t, desc, ref, amt, acct in others:
        rows.append(dict(value=v, type=t, remitter=desc, ref=ref, amount=float(amt), account=acct))
    rows.sort(key=lambda x: (x["value"], x["remitter"], x["ref"], x["amount"]))
    r = W.rng("bankref")
    n = 41870 + int(r.integers(0, 900))
    for x in rows:
        n += 1 + int(r.random() < .3)
        x["bankref"] = "NB%07d" % n
        x["post"] = next_working(x["value"])
    return rows


def write_bank_credits(path, rows):
    """The bank's report of credits to the Authority's main account, by value date, as downloaded from online
    banking."""
    keep = [x for x in rows if EXPORT_FROM <= x["value"] <= EXPORT_TO]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Value date", "Type", "Remitter", "Reference", "Bank ref", "Amount"])
        for x in keep:
            w.writerow([x["value"].strftime("%d/%m/%Y"), x["type"], x["remitter"], x["ref"], x["bankref"],
                        "%.2f" % x["amount"]])
    return len(keep)


def write_cash_book(path, rows):
    """The finance system's receipts for the main account in its 2025-26 year, by the day each was posted from the
    bank's statement: a council's receipt on one line for each invoice it pays, the receipt's amount on every line
    as the receipts listing prints it, every other credit on one line to its income account."""
    names = dict(K.NAME)
    levy_nos = {i["no"] for i in invoices() + prior_invoices()}
    owner = {i["no"]: i["code"] for i in all_invoices() + prior_invoices()}
    out = []
    for x in rows:
        if not EXPORT_FROM <= x["post"] <= CASHBOOK_TO:
            continue
        if "pay" in x:
            for no, _amt in x["pay"]["covers"]:
                out.append((x["post"], x["bankref"], LEVY_ACCOUNT if no in levy_nos else SUNDRY_ACCOUNT,
                            names[owner[no]], no, x["ref"], x["amount"]))
        else:
            out.append((x["post"], x["bankref"], x["account"], "", "", "%s %s" % (x["remitter"], x["ref"]), x["amount"]))
    out.sort(key=lambda y: (y[0], y[1], y[4]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Posting date", "Receipt no", "Account", "Customer", "Invoice", "Narrative", "Amount"])
        seen = {}
        for k, y in enumerate(out):
            rno = seen.setdefault(y[1], "R%06d" % (250001 + len(seen)))
            w.writerow([y[0].strftime("%d/%m/%Y"), rno, y[2], y[3], y[4], y[5], "%.2f" % y[6]])
    return len(out)


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
