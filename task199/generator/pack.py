"""Write the Tawi Bank exports under a target directory from the clean truth (task199, architecture 2).

Each file carries its own conventions as the producing system writes them; nothing here describes the data.
"""
import csv
import datetime as dt
import io
import os

import numpy as np

import params as P
import world as W
import zipfix

LEGACY_CODES = {"TT_IN": "TTI", "TT_OUT": "TTO", "RTGS": "RTG", "EFT": "EFT", "PESALINK": "PSL", "CHQ": "CHQ",
                "CASH": "CSH", "MPESA": "MPS", "POS": "POS", "SWEEP": "IFT", "FX": "FXD", "CHG": "CHG",
                "BULK": "BLK", "KRA": "TAX"}
T24_CODES = [
    ("101", "Cash deposit"), ("102", "Cash withdrawal"), ("109", "Cash reversal"), ("213", "Inward telegraphic transfer"),
    ("214", "Outward telegraphic transfer"), ("330", "RTGS credit"), ("331", "RTGS debit"), ("410", "EFT credit"),
    ("411", "EFT debit"), ("420", "PesaLink credit"), ("421", "PesaLink debit"), ("440", "Cheque deposit"),
    ("501", "Mobile money settlement"), ("520", "Card acquiring settlement"), ("610", "Account transfer"),
    ("611", "Foreign exchange deal"), ("700", "Charges"), ("701", "Excise duty"), ("800", "Bulk payment"),
    ("810", "Tax payment"),
]


def t24_code(p):
    ch, cr = p["channel"], p["amount"] > 0
    if ch == "CASH":
        if p["kind"] == "reversal":
            return "109"
        return "101" if cr else "102"
    return {"TT_IN": "213", "TT_OUT": "214", "RTGS": "330" if cr else "331", "EFT": "410" if cr else "411",
            "PESALINK": "420" if cr else "421", "CHQ": "440", "MPESA": "501", "POS": "520", "SWEEP": "610",
            "FX": "611", "CHG": "701" if "EXCISE" in p["narrative"] else "700", "BULK": "800", "KRA": "810"}[ch]


def legacy_code(p):
    if p["channel"] == "CASH" and p["kind"] == "reversal":
        return "RVC"
    return LEGACY_CODES[p["channel"]]


def acct_no(p, d=None):
    d = d or p["value_date"]
    return p["acct"]["legacy"] if d < P.CUTOVER else p["acct"]["new"]


def acct_no_on(acct, d):
    return acct["legacy"] if d < P.CUTOVER else acct["new"]


def money(x):
    return "{:,.2f}".format(abs(x))


def ddmmyyyy(d):
    return d.strftime("%d/%m/%Y")


def write_csv(path, header, rows, quote_all=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, quoting=csv.QUOTE_ALL if quote_all else csv.QUOTE_MINIMAL, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def booking_date(world, p, rng):
    """Most entries book on their value date; a cheque books on the day it is lodged, two business days before it
    clears; an inward wire that reaches Tawi after the cut-off books the next morning with the earlier value date."""
    d = p["value_date"]
    if p["channel"] == "CHQ":
        b = d
        k = 0
        while k < 2:
            b -= W.DAY
            if W.is_business(b):
                k += 1
        if (b < P.CUTOVER) != (d < P.CUTOVER) or b < P.YEAR_START:
            return d
        return b
    if p["channel"] == "TT_IN" and rng.random() < 0.18:
        b = W.add_business(d, 1)
        if (b < P.CUTOVER) != (d < P.CUTOVER) or b > P.YEAR_END:
            return d
        return b
    return d


def build(world, target):
    os.makedirs(target, exist_ok=True)
    rng = np.random.default_rng([P.SEED, 500])
    for p in world.postings:
        p["booking_date"] = booking_date(world, p, rng)
    files = {}

    # ---------------- legacy core statement export, October 2025 to March 2026
    legacy = [p for p in world.postings if p["value_date"] < P.CUTOVER]
    names = {c["code"]: c["legacy_name"] for c in P.CUSTOMERS}
    rows = []
    for p in legacy:
        rows.append([p["cif"], p["acct"]["legacy"], names[p["code"]][:30], p["cur"], ddmmyyyy(p["booking_date"]),
                     ddmmyyyy(p["value_date"]), legacy_code(p), p["ref"], p["narrative"][:60],
                     money(p["amount"]) if p["amount"] < 0 else "", money(p["amount"]) if p["amount"] > 0 else ""])
    fn = "tawi_core_legacy_stmt_2025-10_2026-03.csv"
    write_csv(os.path.join(target, fn), ["CIF", "ACCOUNT_NO", "ACCOUNT_NAME", "CCY", "TXN_DATE", "VALUE_DATE",
                                         "TRAN_CODE", "TXN_REF", "NARRATION", "DEBIT", "CREDIT"], rows, quote_all=True)
    files[fn] = len(rows)

    # ---------------- T24 statement entries, April to September 2026
    t24 = [p for p in world.postings if p["value_date"] >= P.CUTOVER]
    rows = []
    seq = 128_441_000
    brng = np.random.default_rng([P.SEED, 501])
    for p in t24:
        seq += int(brng.integers(3, 40))
        if p["cur"] == "KES":
            fcy, lcy, rate = "", "%.2f" % p["amount"], ""
        else:
            r = round(W.rate_on(world.rates, p["cur"], p["value_date"]) + float(brng.normal(0, 0.03)), 4)
            fcy, lcy, rate = "%.2f" % p["amount"], "%.2f" % round(p["amount"] * r, 2), "%.4f" % r
        their = p.get("ref") if p["channel"] in ("TT_IN",) else ""
        rows.append(["%d.%06d" % (seq, int(brng.integers(10000, 99999))), p["acct"]["new"], p["cif"], p["cur"],
                     p["booking_date"].strftime("%Y%m%d"), p["value_date"].strftime("%Y%m%d"), t24_code(p), fcy, lcy,
                     rate, p["narrative"][:65], p["ref"] if p["channel"] != "TT_IN" else "FT26%07d"
                     % int(brng.integers(0, 9_999_999)), their])
    fn = "tawi_t24_stmt_2026-04_2026-09.csv"
    write_csv(os.path.join(target, fn), ["STMT.ENTRY.ID", "ACCOUNT.NUMBER", "CUSTOMER", "CURRENCY", "BOOKING.DATE",
                                         "VALUE.DATE", "TRANSACTION.CODE", "AMOUNT.FCY", "AMOUNT.LCY",
                                         "EXCHANGE.RATE", "NARRATIVE", "OUR.REFERENCE", "THEIR.REFERENCE"], rows)
    files[fn] = len(rows)

    # ---------------- T24 transaction code table
    fn = "t24_transaction_codes.csv"
    write_csv(os.path.join(target, fn), ["TRANSACTION.CODE", "DESCRIPTION"], T24_CODES)
    files[fn] = len(T24_CODES)

    # ---------------- account conversion at the T24 go-live
    rows = []
    for c in P.CUSTOMERS:
        for a in world.accts[c["code"]]:
            cat = {"CA": "1001", "CL": "1006", "FC": "1501"}[a["prod"]]
            rows.append([a["legacy"], a["new"], c["cif"], a["cur"], cat, "20260401"])
    fn = "t24_account_conversion_20260401.csv"
    write_csv(os.path.join(target, fn), ["LEGACY.ACCOUNT", "T24.ACCOUNT", "CUSTOMER", "CURRENCY", "CATEGORY",
                                         "CONVERSION.DATE"], rows)
    files[fn] = len(rows)

    # ---------------- SWIFT MT103 archives
    out_lines = []
    for m in sorted(world.swift_out, key=lambda m: (m["value_date"], m["ref"])):
        p = m["posting"]
        c = world.cust[p["code"]]
        acc = acct_no_on(p["acct"], m["value_date"])
        amt = ("%.2f" % m["amount"]).replace(".", ",")
        blk = ["{1:F01%sAXXX%010d}{2:I103%sXXXXN}{3:{108:%s}}{4:" % (P.BANK_BIC, int(m["ref"][-5:]) * 7919 % 10**10,
                                                                   m["bene_bic"], m["ref"][-16:]),
               ":20:%s" % m["ref"], ":23B:CRED", ":32A:%s%s%s" % (m["value_date"].strftime("%y%m%d"), m["cur"], amt),
               ":33B:%s%s" % (m["cur"], amt), ":50K:/%s" % acc, c["name"].upper()[:35],
               ("%s BRANCH" % c["branch"][1].upper())[:35], "NAIROBI KENYA" if c["branch"][0] not in ("MSA",)
               else "MOMBASA KENYA", ":57A:%s" % m["bene_bic"], ":59:/%s" % m["bene_acct"], m["beneficiary"][:35]]
        if m["bene_addr"]:
            blk.append(m["bene_addr"][:35])
        blk += [m["bene_city"][:35], ":70:%s" % m["remittance"][:35], ":71A:SHA", "-}"]
        out_lines.append("\n".join(blk))
    fn = "swift_mt103_outward_fy2026.txt"
    with open(os.path.join(target, fn), "w", encoding="ascii", newline="\n") as f:
        f.write("\n\n".join(out_lines) + "\n")
    files[fn] = len(out_lines)

    in_lines = []
    for m in sorted(world.swift_in, key=lambda m: (m["value_date"], m["ref"])):
        p = m["posting"]
        c = world.cust[p["code"]]
        acc = acct_no_on(p["acct"], m["value_date"])
        amt = ("%.2f" % m["amount"]).replace(".", ",")
        ins = ("%.2f" % m["instructed"]).replace(".", ",")
        blk = ["{1:F01%sAXXX%010d}{2:O1031030%s%sXXXX}{4:" % (P.BANK_BIC, int(sum(map(ord, m["ref"]))) * 104729 % 10**10,
                                                               m["value_date"].strftime("%y%m%d"), m["ordering_bic"]),
               ":20:%s" % m["ref"], ":23B:CRED", ":32A:%s%s%s" % (m["value_date"].strftime("%y%m%d"), m["cur"], amt),
               ":33B:%s%s" % (m["cur"], ins), ":50K:/%s" % m["ordering_acct"], m["ordering"][:35]]
        if m["ordering_addr"]:
            blk.append(m["ordering_addr"][:35])
        blk += [m["ordering_city"][:35], ":52A:%s" % m["ordering_bic"], ":59:/%s" % acc, c["name"].upper()[:35]]
        if m.get("return_of"):
            blk.append(":70:/RETN/AC04/%s" % m["return_of"])
        else:
            blk.append(":70:/RFB/%s" % ("SETTLEMENT %s" % m["ref"][-6:]))
        blk.append(":71A:SHA")
        if m["charges"] > 0:
            blk.append(":71F:%s%s" % (m["cur"], ("%.2f" % m["charges"]).replace(".", ",")))
        blk.append("-}")
        in_lines.append("\n".join(blk))
    fn = "swift_mt103_inward_fy2026.txt"
    with open(os.path.join(target, fn), "w", encoding="ascii", newline="\n") as f:
        f.write("\n\n".join(in_lines) + "\n")
    files[fn] = len(in_lines)

    # ---------------- CBK indicative rates
    rows = []
    cname = {"USD": "US DOLLAR", "EUR": "EURO", "GBP": "STG POUND"}
    for d in reversed(world.days_all):
        for cur in ("USD", "GBP", "EUR"):
            m = world.rates[cur][d]
            rows.append([ddmmyyyy(d), cname[cur], "%.4f" % m, "%.4f" % (m - P.FX_SPREAD[cur]),
                         "%.4f" % (m + P.FX_SPREAD[cur])])
    fn = "cbk_indicative_rates_2025-09_2026-10.csv"
    write_csv(os.path.join(target, fn), ["Date", "Currency", "Mean", "Buy", "Sell"], rows)
    files[fn] = len(rows)

    # ---------------- customer master extract
    rows = []
    regs = ["C.152218", "PVT-JZU3LQ8", "C.104563", "PVT-LKU93XN", "C.162907", "C.80114", "C.98710",
            "PVT-BN5Q2WR", "C.142336", "PVT-MU7P9LD", "C.65022", "PVT-Z8EAJ5H"]
    inc = ["2009-03-17", "2012-07-02", "2004-11-22", "2016-05-09", "2011-01-28", "1998-08-14", "2003-02-19",
           "2015-09-30", "2007-06-11", "2018-12-03", "1996-04-25", "2013-10-07"]
    for k, c in enumerate(P.CUSTOMERS):
        reg = regs[k]
        rows.append([c["cif"], c["name"], reg, c["kra"], inc[k], "BUSINESS BANKING", "%03d" % c["branch"][2],
                     "RM%03d" % (110 + (k * 17) % 60)])
    fn = "customer_master_extract_20261016.csv"
    write_csv(os.path.join(target, fn), ["CIF", "LEGAL_NAME", "REGISTRATION_NO", "KRA_PIN", "INCORPORATED",
                                         "SEGMENT", "HOME_BRANCH", "RM_CODE"], rows)
    files[fn] = len(rows)

    # ---------------- teller cash transactions
    rows = []
    trng = np.random.default_rng([P.SEED, 502])
    tel = sorted(world.teller, key=lambda t: (t["posting"]["value_date"], t["posting"]["ref"]))
    for t in tel:
        p = t["posting"]
        d = p["value_date"]
        if d.weekday() == 5:
            hh, mm = int(trng.integers(9, 12)), int(trng.integers(0, 60))
        else:
            hh, mm = int(trng.integers(8, 16)), int(trng.integers(0, 60))
        ts = dt.datetime(d.year, d.month, d.day, hh, mm, int(trng.integers(0, 60)))
        typ = {"DEP": "CDEP", "WDL": "CWDL", "REV": "REVERSAL"}[t["kind"]]
        rows.append(["%03d" % t["branch"], "T%03d%02d" % (t["branch"] % 1000, int(trng.integers(1, 9))),
                     ts.strftime("%Y-%m-%d %H:%M:%S"), acct_no_on(p["acct"], d), typ, "%.2f" % abs(p["amount"]),
                     p["ref"], t.get("reverses", "")])
    fn = "teller_cash_txn_2025-10_2026-09.csv"
    write_csv(os.path.join(target, fn), ["BRANCH", "TELLER_ID", "TXN_TIMESTAMP", "ACCOUNT", "TXN_TYPE", "AMOUNT_KES",
                                         "TXN_REF", "ORIG_REF"], rows)
    files[fn] = len(rows)

    # ---------------- KRA payment gateway log
    rows = []
    krng = np.random.default_rng([P.SEED, 503])
    for g in sorted(world.kra, key=lambda g: (g["pay_date"], g["prn"], g["part"])):
        c = world.cust[g["code"]]
        pin = c["kra"]
        u = krng.random()
        if u < 0.07:
            pin = pin.lower()
        elif u < 0.12:
            pin = pin[:6] + " " + pin[6:]
        y, m = g["period"]
        last = (dt.date(y + (m == 12), 1 if m == 12 else m + 1, 1) - W.DAY)
        acc = acct_no_on(world.acct(g["code"]), g["pay_date"])
        head = {"VAT": "VAT", "PAYE": "PAYE"}[g["head"]]
        rows.append([g["prn"], pin, head, dt.date(y, m, 1).isoformat(), last.isoformat(), "%.2f" % g["amount"],
                     g["pay_date"].isoformat(), acc, "INTERNET BANKING" if krng.random() < 0.8 else "BRANCH",
                     "KR%s%04d" % (g["pay_date"].strftime("%y%m%d"), int(krng.integers(0, 9999)))])
    fn = "kra_gateway_payments_2025-09_2026-10.csv"
    write_csv(os.path.join(target, fn), ["PRN", "TAXPAYER_PIN", "TAX_HEAD", "TAX_PERIOD_FROM", "TAX_PERIOD_TO",
                                         "AMOUNT_PAID", "PAYMENT_DATE", "DEBIT_ACCOUNT", "CHANNEL", "BANK_REF"], rows)
    files[fn] = len(rows)

    # ---------------- bulk salary uploads
    rows = []
    srng = np.random.default_rng([P.SEED, 504])
    banks = ["01", "03", "11", "12", "31", "57", "63", "68", "70", "72"]
    for r in sorted(world.payroll, key=lambda r: (r["pay_date"], r["batch"], r["nid"])):
        acc = acct_no_on(world.acct(r["code"]), r["pay_date"])
        rows.append([r["batch"], acc, r["pay_date"].isoformat(), r["name"], r["nid"],
                     banks[int(srng.integers(0, len(banks)))], "%012d" % int(srng.integers(10**10, 10**12 - 1)),
                     "%.2f" % r["amount"], r["narrative"]])
    fn = "bulk_salary_uploads_2026-07_2026-10.csv"
    write_csv(os.path.join(target, fn), ["BATCH_REF", "DEBIT_ACCOUNT", "VALUE_DATE", "PAYEE_NAME", "PAYEE_ID_NO",
                                         "PAYEE_BANK", "PAYEE_ACCOUNT", "AMOUNT_KES", "PAYMENT_DETAILS"], rows)
    files[fn] = len(rows)

    # ---------------- screening alerts (counterparty name screening), every one closed
    rows = []
    arng = np.random.default_rng([P.SEED, 505])
    cps = sorted({m["beneficiary"] for m in world.swift_out} | {m["ordering"] for m in world.swift_in})
    lists = ["UN CONSOLIDATED", "OFAC SDN", "EU CONSOLIDATED", "HMT", "PEP KENYA"]
    for k in range(214):
        d = world.year_days[int(arng.integers(0, len(world.year_days)))]
        c = P.CUSTOMERS[int(arng.integers(0, len(P.CUSTOMERS)))]
        cp = cps[int(arng.integers(0, len(cps)))]
        rows.append(["SA-%s-%04d" % (d.strftime("%y%m"), int(arng.integers(1, 9999))), d.isoformat(), c["cif"],
                     cp, lists[int(arng.integers(0, len(lists)))], "%d" % int(arng.integers(71, 93)),
                     "CLOSED - FALSE POSITIVE", "AN%02d" % int(arng.integers(1, 9))])
    rows.sort(key=lambda r: (r[1], r[0]))
    fn = "screening_alerts_fy2026.csv"
    write_csv(os.path.join(target, fn), ["ALERT_ID", "ALERT_DATE", "CIF", "MATCHED_NAME", "LIST", "SCORE",
                                         "DISPOSITION", "ANALYST"], rows)
    files[fn] = len(rows)

    # ---------------- workbooks and documents
    files.update(write_register(world, target))
    files.update(write_procedure(world, target))
    files.update(write_tariff(world, target))
    for fn in os.listdir(target):
        os.utime(os.path.join(target, fn), (P.EXPORT_MTIME.timestamp(), P.EXPORT_MTIME.timestamp()))
    return files


def write_register(world, target):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "Register"
    ws["A1"] = "Tawi Bank Limited - Financial Crime Compliance"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "EDD register, business customers rated high risk, review year to 30 September 2026"
    hdr = ["Customer number", "Customer name", "Sector", "Risk rating", "Onboarded", "Last review", "Home branch",
           "Relationship manager"]
    ws.append([])
    ws.append(hdr)
    for cell in ws[4]:
        cell.font = Font(bold=True)
    onb = ["2014-02-11", "2016-08-29", "2009-05-04", "2019-03-18", "2015-10-06", "2003-07-21", "2008-01-15",
           "2020-02-24", "2011-09-12", "2021-06-07", "2006-11-30", "2017-04-03"]
    for k, c in enumerate(P.CUSTOMERS):
        ws.append([c["cif"], c["name"], c["sector"], "High", onb[k], "2025-10-%02d" % (6 + k % 18),
                   c["branch"][1], "RM%03d" % (110 + (k * 17) % 60)])
    for col, wdt in zip("ABCDEFGH", (16, 38, 44, 11, 12, 12, 20, 20)):
        ws.column_dimensions[col].width = wdt
    ws2 = wb.create_sheet("Profiles")
    ws2["A1"] = "Customer profiles as refreshed at the last review"
    ws2["A1"].font = Font(bold=True)
    ws2.append([])
    hdr2 = ["Customer number", "Expected annual turnover (KES)", "Expected counterparties", "Main countries",
            "Accounts held with other institutions", "Profile refreshed"]
    ws2.append(hdr2)
    for cell in ws2[3]:
        cell.font = Font(bold=True)
    cps = {
        "C01": "Car buyers and dealers in Mombasa and Nairobi; exporters in Japan", "C02": "Retail customers via M-Pesa and cash; fleet accounts",
        "C03": "County governments, KeRRA, private developers", "C04": "Wholesale buyers in Nairobi and the region; suppliers in China",
        "C05": "Importers and shipping lines", "C06": "Tea buyers at the Mombasa auction and abroad",
        "C07": "Flower auction and wholesalers in Europe", "C08": "Retail customers; regional resellers",
        "C09": "Hospitals, clinics and pharmacies", "C10": "Refineries and bullion dealers in Dubai; licensed miners",
        "C11": "Tour operators and walk-in guests", "C12": "Contractors and hardware retailers in the North Rift",
    }
    for k, c in enumerate(P.CUSTOMERS):
        de = P.DECLARED_ELSEWHERE.get(c["code"])
        ws2.append([c["cif"], c["expected"], cps[c["code"]], c["countries"],
                    ("%s - %s" % (de["bank"], de["acct"])) if de else "None declared",
                    "2025-10-%02d" % (6 + k % 18)])
        ws2.cell(row=ws2.max_row, column=2).number_format = "#,##0"
    for col, wdt in zip("ABCDEF", (16, 26, 58, 34, 44, 16)):
        ws2.column_dimensions[col].width = wdt
    wb.properties.creator = "Tawi Bank Limited"
    wb.properties.lastModifiedBy = "Tawi Bank Limited"
    wb.properties.created = dt.datetime(2026, 10, 16, 14, 40)
    wb.properties.modified = dt.datetime(2026, 10, 16, 14, 40)
    fn = "edd_register_profiles_2026.xlsx"
    path = os.path.join(target, fn)
    wb.save(path)
    zipfix.normalise(path, app="Microsoft Excel")
    return {fn: len(P.CUSTOMERS)}


PROCEDURE = [
    ("1. Scope", [
        "Business customers rated high risk at onboarding or at their last review are held on the EDD register and "
        "reviewed once a year over the twelve months to 30 September (the review year). This revision governs the "
        "review of the year to 30 September 2026."]),
    ("2. The profile", [
        "Each customer's profile records the turnover the customer told the Bank it expected to put through its "
        "accounts with the Bank in a year (the expected annual turnover), its expected counterparties and countries, "
        "and the accounts it holds with other institutions. The profile is refreshed at each review and the figures "
        "recorded at the last review stand for the year under review."]),
    ("3. Third-party receipts", [
        "3.1 The review compares each customer's third-party receipts for the review year with its expected annual "
        "turnover. Third-party receipts are the credits to the customer's accounts with the Bank, by value date within "
        "the review year, that bring it funds from someone else. Funds that originate from the customer itself are not "
        "third-party receipts, however they reach the account; for example transfers between its own accounts with the "
        "Bank or with other institutions, and payments of its own that are returned or refunded to it.",
        "3.2 A credit in a foreign currency is taken in Kenya shillings at the Central Bank of Kenya mean rate for its "
        "value date, or the latest mean rate published before that date where none was published on it."]),
    ("4. Referral", [
        "4.1 The review refers to the Financial Investigations Unit the customer whose third-party receipts differ most "
        "from its expected annual turnover, the difference measured as the larger of the two divided by the smaller. "
        "The Unit opens one full investigation a cycle; the next customer in line is held for the following cycle.",
        "4.2 The referral note names the customer with its third-party receipts, its expected annual turnover and the "
        "ratio of receipts to expected turnover, and names the next customer in line with its ratio."]),
    ("5. Large cash transactions", [
        "5.1 A cash deposit or withdrawal of 10,000 United States dollars or more, or the equivalent in Kenya "
        "shillings, is reported to the Financial Reporting Centre. A customer's cash withdrawals on the same day are "
        "counted together and reported as one withdrawal, whichever of its accounts or branches they were made at. The "
        "shilling equivalent is taken at the Central Bank of Kenya mean rate for the day, or the latest mean rate "
        "published before it.",
        "5.2 The review records, for each customer, the withdrawals it reported or should have reported in the review "
        "year and their total."]),
    ("6. Footprint", [
        "6.1 The review records the people each customer pays a monthly salary through the Bank's salary upload "
        "service, for the last month of the review year, and what they were paid for that month. A salary is pay for "
        "a calendar month; weekly casual wages are not salaries.",
        "6.2 The review records the value added tax each customer paid through the KRA payment gateway, by tax period."]),
    ("7. Records", [
        "The review is prepared by the EDD analyst and approved by the Head of Financial Crime Compliance, who is the "
        "Bank's Money Laundering Reporting Officer. Working papers are retained for seven years."]),
]


def write_procedure(world, target):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    fn = "FCC-07_EDD_annual_review_rev4.pdf"
    path = os.path.join(target, fn)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                            bottomMargin=20 * mm, title="FCC-07 Enhanced due diligence: annual review",
                            author="Tawi Bank Limited", subject="Financial Crime Compliance", creator="Tawi Bank Limited",
                            producer="Tawi Bank Limited", invariant=1)
    h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=3)
    t = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4)
    b = ParagraphStyle("b", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=4)
    s = ParagraphStyle("s", fontName="Helvetica", fontSize=8.5, leading=11, textColor="#444444")
    story = [Paragraph("Tawi Bank Limited", t),
             Paragraph("FCC-07 Enhanced due diligence: annual review of high-risk business customers", h),
             Paragraph("Revision 4. Approved by the Board Audit and Risk Committee on 26 June 2025. Owner: Head of "
                       "Financial Crime Compliance. Supersedes revision 3 of 14 May 2024.", s), Spacer(1, 6)]
    for head, paras in PROCEDURE:
        story.append(Paragraph(head, h))
        for para in paras:
            story.append(Paragraph(para, b))
    doc.build(story)
    return {fn: 1}


def write_tariff(world, target):
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    fn = "tawi_tariff_business_2026.pdf"
    path = os.path.join(target, fn)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Tariff guide: business accounts", author="Tawi Bank Limited",
                            creator="Tawi Bank Limited", producer="Tawi Bank Limited", invariant=1)
    t = ParagraphStyle("t", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4)
    s = ParagraphStyle("s", fontName="Helvetica", fontSize=8.5, leading=11)
    data = [["Service", "Charge (KES unless stated)"],
            ["Monthly ledger fee, shilling account", "1,500"], ["Monthly ledger fee, foreign currency account", "USD 15"],
            ["RTGS transfer out", "750"], ["EFT transfer out", "200"], ["PesaLink transfer out", "120"],
            ["Outward telegraphic transfer", "2,500 plus 0.1% of the amount, capped at 12,000"],
            ["Inward telegraphic transfer", "Free (correspondent charges may apply)"],
            ["Cash withdrawal over the counter above KES 1,000,000", "0.25%, minimum 500"],
            ["Bulk payment upload, per beneficiary", "35"], ["KRA payment through the gateway", "Free"],
            ["Excise duty", "20% of each fee or commission"]]
    tbl = Table(data, colWidths=[95 * mm, 70 * mm])
    tbl.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9), ("FONT", (0, 1), (-1, -1), "Helvetica", 9),
                             ("GRID", (0, 0), (-1, -1), 0.3, "#999999"), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    doc.build([Paragraph("Tawi Bank Limited - Tariff guide, business accounts", t),
               Paragraph("Effective 1 January 2026. Charges are debited to the account on which the service is used.",
                         s), Spacer(1, 8), tbl])
    return {fn: 1}
