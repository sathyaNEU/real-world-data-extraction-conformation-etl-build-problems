"""task146 architecture 2: the data files of the pack, written from the world."""
import calendar
import csv
import datetime as dt
import json
import os

import numpy as np
from openpyxl import Workbook

import world as W

FILES = {
    "balances": "ia_month_end_balances_2021-2026.csv",
    "events": "ia_account_events_2021-2026.csv",
    "products": "savings_product_register.xlsx",
    "swaps": "structural_hedge_swap_register_2026-12.xlsx",
    "bonds": "fixed_rate_bond_openings_2021-2026.csv",
    "rates": "savings_rate_history_2021-2026.csv",
    "isa_in": "cash_isa_transfers_in_2026.csv",
    "policy": "trentmoor_alm_policy_structural_hedge_v4.pdf",
    "minutes": "board_minute_extract_2026-01-27.pdf",
    "email": "treasury_request_2026-12-03.eml",
}
DISTRACTORS = ("bonds", "rates", "isa_in")
# the 2025 product rationalisation: Easy Saver Online (ES02) merged into Easy Saver (ES01) on 1 July 2025 and its code
# was reused for Young Saver, which had been YS01
RECODE_DAY = dt.date(2025, 7, 1)
SWAPS = [  # trade date, notional GBP, maturity, fixed rate
    ("2024-01-29", 51_000_000, "2027-01-29", 0.04285),
    ("2025-01-28", 49_500_000, "2028-01-28", 0.04012),
    ("2026-01-27", 52_400_000, "2029-01-29", 0.03644),
]
NEXT_SWAPS = [  # outstanding after the January 2027 maturity
    s for s in SWAPS if s[2] > "2027-01-29"
]


def last_business_day(d):
    while d.weekday() >= 5 or (d.month == 12 and d.day in (25, 26)):
        d -= dt.timedelta(days=1)
    return d


def code_for(w, acct, day):
    """The product code the Society's systems carried for an account on a day."""
    a = w.accounts[acct]
    iss = a["issue"]
    if iss.startswith("LS"):
        return iss
    if iss == "ES":
        online = (acct % 7) in (2, 5)
        if online and day < RECODE_DAY:
            return "ES02"
        return "ES01"
    if iss == "IS":
        return "IS01"
    if iss == "YS":
        return "YS01" if day < RECODE_DAY else "ES02"
    return iss


def balances(w, path):
    rows = []
    for (acct, mi), b in w.balances.items():
        me = W.MONTHS[mi]
        rows.append((acct, mi, b))
    # closed accounts carried at zero for the month in which they closed
    closed = {}
    for a, v in w.accounts.items():
        if v["closed"] is not None:
            for mi, me in enumerate(W.MONTHS):
                if me >= v["closed"]:
                    if (me.year, me.month) == (v["closed"].year, v["closed"].month):
                        closed[(a, mi)] = 0.0
                    break
    for k, b in closed.items():
        if k not in w.balances:
            rows.append((k[0], k[1], 0.0))
    rows.sort(key=lambda r: (r[1], r[0]))
    with open(path, "w", newline="") as fh:
        c = csv.writer(fh)
        c.writerow(["month_end", "account_no", "product_code", "balance_gbp"])
        for acct, mi, b in rows:
            me = last_business_day(W.MONTHS[mi])
            c.writerow([me.isoformat(), acct, code_for(w, acct, W.MONTHS[mi]), "%.2f" % b])
    return len(rows)


def events(w, path):
    r = np.random.RandomState(W.SEED + 5)
    rows = []
    for (day, ev, acct, code, amount, how, pid) in w.events:
        if how == "switch":
            t = dt.time(2, 10, 0)      # the overnight batch that moves a member to the new issue
        else:
            h = int(r.choice([9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 23]))
            t = dt.time(h, int(r.randint(0, 60)), int(r.randint(0, 60)))
        local = dt.datetime.combine(day, t)
        utc = local - dt.timedelta(hours=1 if _bst(local) else 0)
        rows.append((utc, acct, ev, code_for(w, acct, day), int(round(amount * 100))))
    rows.sort()
    with open(path, "w", newline="") as fh:
        c = csv.writer(fh)
        c.writerow(["event_utc", "account_no", "event", "product_code", "amount_pence"])
        for utc, acct, ev, code, p in rows:
            c.writerow([utc.strftime("%Y-%m-%dT%H:%M:%SZ"), acct, ev, code, p])
    return len(rows)


def _bst(local):
    y = local.year
    def last_sunday(m):
        d = dt.date(y, m, calendar.monthrange(y, m)[1])
        return d - dt.timedelta(days=(d.weekday() + 1) % 7)
    start = dt.datetime.combine(last_sunday(3), dt.time(1, 0))
    end = dt.datetime.combine(last_sunday(10), dt.time(2, 0))
    return start <= local < end


def products(path, stamp):
    wb = Workbook()
    ws = wb.active
    ws.title = "Products"
    ws.append(["Product code", "Product", "Access", "Launched", "Withdrawn from sale", "Notes"])
    ws.append(["ES01", "Easy Saver", "Instant", "2009-03-02", "", "Branch and postal; Easy Saver Online merged in from 1 July 2025"])
    ws.append(["ES02", "Easy Saver Online", "Instant", "2014-06-16", "2025-06-30", "Merged into ES01 on 1 July 2025"])
    ws.append(["ES02", "Young Saver", "Instant", "2025-07-01", "", "Code reallocated at the 2025 product rationalisation"])
    ws.append(["YS01", "Young Saver", "Instant", "2011-09-05", "2025-06-30", "Re-coded ES02 from 1 July 2025"])
    ws.append(["IS01", "Easy Access Cash ISA", "Instant", "2012-04-06", "", ""])
    for y in range(2021, 2027):
        ws.append(["LS%02d" % (y % 100), "Loyalty Saver issue %d" % (y - 2016), "Instant",
                   "%d-04-01" % y, "%d-03-31" % (y + 1) if y < 2026 else "",
                   "Members only; one account per member per issue"])
    ws.append(["FR1Y", "Fixed Rate Bond 1 year", "None until maturity", "2016-01-04", "", "Held on the bond ledger"])
    ws.append(["FR2Y", "Fixed Rate Bond 2 year", "None until maturity", "2016-01-04", "", "Held on the bond ledger"])
    wb.properties.creator = "Product Governance"
    wb.properties.created = stamp[0]
    wb.properties.modified = stamp[1]
    wb.save(path)
    normalize_xlsx(path)


def swaps(path, stamp):
    wb = Workbook()
    ws = wb.active
    ws.title = "Swaps"
    ws.append(["Deal ref", "Trade date", "Effective", "Maturity", "Notional (GBP)", "Society receives", "Society pays",
               "Counterparty", "Purpose"])
    refs = ["TBS-SW-2024-01", "TBS-SW-2025-01", "TBS-SW-2026-01"]
    for ref, (td, n, mat, fx) in zip(refs, SWAPS):
        ws.append([ref, td, td, mat, n, "Fixed %.3f%%" % (fx * 100), "SONIA compounded", "Clearing (LCH)",
                   "Structural hedge, instant-access savings"])
    ws2 = wb.create_sheet("Notes")
    ws2.append(["Register as at 2 December 2026. Notionals do not amortise. Swaps are cleared; all mature on the last business day of January of the year shown."])
    wb.properties.creator = "Treasury"
    wb.properties.created = stamp[0]
    wb.properties.modified = stamp[1]
    wb.save(path)
    normalize_xlsx(path)


def bonds(w, path):
    r = np.random.RandomState(W.SEED + 9)
    rows = []
    for day, amt, pid in w.bonds:
        rows.append((day, amt))
    # bonds opened with money from outside the Society
    for mi in range(1, len(W.MONTHS)):
        for _ in range(int(r.poisson(24))):
            day = W.MONTHS[mi - 1] + dt.timedelta(days=int(r.randint(1, 28)))
            rows.append((day, round(float(np.exp(r.normal(10.4, 0.7))), 2)))
    rows.sort()
    with open(path, "w", newline="") as fh:
        c = csv.writer(fh)
        c.writerow(["opened", "bond_ref", "term", "principal_gbp", "matures"])
        for i, (day, amt) in enumerate(rows):
            term = "1Y" if (i * 7) % 5 < 3 else "2Y"
            mat = day.replace(year=day.year + (1 if term == "1Y" else 2)) if not (day.month == 2 and day.day == 29) else dt.date(day.year + 1, 3, 1)
            c.writerow([day.strftime("%d/%m/%Y"), "FRB%07d" % (2210000 + i * 3), term, "%.2f" % amt, mat.strftime("%d/%m/%Y")])
    return len(rows)


def rates(path):
    with open(path, "w", newline="") as fh:
        c = csv.writer(fh)
        c.writerow(["month", "bank_rate_pct", "ES01_pct", "LS_current_issue_pct", "IS01_pct", "young_saver_pct"])
        for mi, me in enumerate(W.MONTHS):
            br = W.BANK[mi]
            c.writerow([me.strftime("%Y-%m"), "%.2f" % (br * 100)] +
                       ["%.2f" % ((W.RATE[p] + 0.55 * br) * 100) for p in W.PRODUCTS])


def isa_in(path):
    r = np.random.RandomState(W.SEED + 13)
    with open(path, "w", newline="") as fh:
        c = csv.writer(fh)
        c.writerow(["received", "transfer_ref", "from_provider_code", "amount_gbp", "credited_to"])
        for i in range(int(r.poisson(310))):
            d = dt.date(2026, 1, 1) + dt.timedelta(days=int(r.randint(0, 334)))
            c.writerow([d.isoformat(), "ISAT%06d" % (51000 + i * 7), "P%03d" % int(r.randint(1, 140)),
                        "%.2f" % float(np.exp(r.normal(9.6, 0.8))), "IS01"])


def normalize_xlsx(path, stamp=(2026, 12, 2, 16, 47, 0)):
    """Rewrite an xlsx with fixed zip entry times so two builds are byte-identical."""
    import zipfile
    import io
    src = open(path, "rb").read()
    zin = zipfile.ZipFile(io.BytesIO(src))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in sorted(zin.infolist(), key=lambda i: i.filename):
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                import re
                iso = "%04d-%02d-%02dT%02d:%02d:%02dZ" % stamp
                data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)",
                              lambda mo: mo.group(1) + iso.encode() + mo.group(2), data)
            zi = zipfile.ZipInfo(item.filename, stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zout.writestr(zi, data)
    open(path, "wb").write(buf.getvalue())
