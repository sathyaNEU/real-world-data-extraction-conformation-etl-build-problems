"""task127: write the pack's data files from world.py and records.py (the PDFs are docs.py's)."""
import csv
import datetime as dt
import io
import os
import random
import zipfile

import openpyxl

import postprocess
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import world as W

STAMP = dt.datetime(2027, 1, 22, 9, 40, 0)


def money(x):
    return "%.2f" % x


def write_csv(path, header, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def sheet(ws, header, rows, widths=None):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EE")
    for r in rows:
        ws.append(r)
    for i, h in enumerate(header, start=1):
        ws.column_dimensions[get_column_letter(i)].width = (widths or {}).get(h, max(11, min(42, len(h) + 4)))
    ws.freeze_panes = "A2"


def wb_new(creator):
    wb = openpyxl.Workbook()
    wb.properties.creator = creator
    wb.properties.lastModifiedBy = creator
    wb.properties.created = STAMP
    wb.properties.modified = STAMP
    return wb


# ---- the ledger ---------------------------------------------------------------------------------------------
def write_ledger(rows, target):
    path = os.path.join(target, "business_account_transactions_2021-2026.csv")
    out = []
    r = random.Random(W.SEED + 3)
    tid = 40_118_204
    for i, (d, acct, code, amt, other, oacct, part, cd, ref) in enumerate(rows):
        # the core's sequence is shared with every retail and business account, so a business row's gap to the
        # last one is long-tailed and widens as the bank's volume grows
        tid += 1 + int(r.expovariate(1.0 / (18.0 + 6.0 * (d.year - 2021))))
        out.append(["T%08d" % tid, d.isoformat(), acct, code,
                    "CR" if amt > 0 else "DR", money(abs(amt)), other, oacct, part, cd, ref])
    return write_csv(path, ["txn_id", "posting_date", "account_number", "txn_code", "dr_cr", "amount_nzd",
                            "other_party", "other_party_account", "particulars", "code", "reference"], out)


# ---- customers, accounts, crosswalk ------------------------------------------------------------------------
def write_customers(w, target):
    path = os.path.join(target, "customer_master_2026-12.xlsx")
    wb = wb_new("Ruahine Bank Customer Data")
    ws = wb.active
    ws.title = "Customers"
    rows, arows = [], []
    for c in sorted(w.customers.values(), key=lambda x: x["cid"]):
        status = "Closed" if c["exit"] and c["exit"] <= W.END else "Active"
        rows.append([c["cid"], c["name"], c["trading"], c["nzbn"], c["sector"], W.SECTORS[c["sector"]], c["region"],
                     c["since"], status, c["exit"] if status == "Closed" else None])
        for a in c["accounts"]:
            arows.append([c["cid"], a["new"], a["kind"], a["opened"], a["closed"]])
    sheet(ws, ["customer_no", "legal_name", "trading_name", "nzbn", "anzsic_division", "division_name", "region",
               "customer_since", "status", "closed_date"], rows,
          {"legal_name": 40, "trading_name": 30, "division_name": 34})
    for r in ws.iter_rows(min_row=2):
        for c in r:
            if isinstance(c.value, dt.date):
                c.number_format = "dd/mm/yyyy"
    ws2 = wb.create_sheet("Accounts")
    sheet(ws2, ["customer_no", "account_number", "account_type", "opened", "closed"], arows)
    for r in ws2.iter_rows(min_row=2):
        for c in r:
            if isinstance(c.value, dt.date):
                c.number_format = "dd/mm/yyyy"
    wb.save(path)
    postprocess.scrub(path, "Ruahine Bank Customer Data", "2027-01-21")
    postprocess.finish_office(path, "2027-01-21T19:52:00Z", "2027-01-21T19:58:00Z", "Ruahine Bank")
    return len(rows), len(arows)


def write_crosswalk(w, target):
    rows = []
    for c in sorted(w.customers.values(), key=lambda x: x["cid"]):
        for a in c["accounts"]:
            if a["old"]:
                rows.append([a["old"], a["new"], W.MIGRATION.isoformat(), "CONVERTED"])
    rows.sort()
    return write_csv(os.path.join(target, "account_number_crosswalk_2023.csv"),
                     ["legacy_account", "new_account", "converted_on", "status"], rows)


# ---- defaults ------------------------------------------------------------------------------------------------
def loan_account(fid):
    return "%s-1299-%07d-%03d" % (W.BANK, int(fid[1:]) % 9999999, 1)


def arrears_account(c, df):
    """The account a 90-days-past-due row is raised on: the term loan or equipment finance account where the
    borrower has one in arrears, otherwise the cheque account its overdraft sits on."""
    loans = [f for f in c["facilities"] if not f["revolving"]]
    if loans and (df.get("loan_first") or df["kind"] in ("ordinary", "device_c2", "device_c2_redefault")):
        return loan_account(loans[0]["fid"])
    return c["accounts"][0]["new"]


def write_defaults(w, target):
    rows, crows = [], []
    r = random.Random(W.SEED + 5)
    seq = 5100
    teams = ["Credit Risk", "Business Recoveries", "Relationship Banking"]
    for df in sorted(w.defaults, key=lambda x: (x["first"], x["cid"])):
        c = w.customers[df["cid"]]
        ead = sum(f["ead"] for f in c["facilities"]) or 50_000
        for kind, d in df["triggers"]:
            seq += r.randint(1, 4)
            if kind == "UTP":
                rows.append(["DR%05d" % seq, c["cid"], c["name"], "UTP", d.isoformat(),
                             money(ead * r.uniform(0.96, 1.04)), r.choice(teams)])
            else:
                acct = arrears_account(c, df)
                ref = acct if r.random() < 0.7 else acct.replace("-", "")
                rows.append(["DR%05d" % seq, ref, "", "DPD90", d.isoformat(),
                             money(ead * r.uniform(0.5, 0.9)), "Collections"])
        if df["cure"]:
            crows.append([c["cid"], c["name"], df["first"].isoformat(), df["cure"].isoformat(),
                          r.choice([6, 6, 9, 12]), r.choice(["L. Middlemiss", "R. Okafor", "J. Tane"])])
    rows.sort(key=lambda x: (x[4], x[0]))
    crows.sort(key=lambda x: (x[3], x[0]))
    n1 = write_csv(os.path.join(target, "default_register_2021-2026.csv"),
                   ["register_id", "reference", "borrower", "trigger", "trigger_date", "exposure_nzd", "raised_by"], rows)
    n2 = write_csv(os.path.join(target, "default_cures_2021-2026.csv"),
                   ["customer_no", "borrower", "default_date", "cure_date", "probation_months", "approved_by"], crows)
    return n1, n2


def in_default(w, cid, day):
    for df in w.defaults:
        if df["cid"] == cid and df["first"] <= day and (df["cure"] is None or df["cure"] > day):
            return True
    return False


# ---- IFRS 9 runs ---------------------------------------------------------------------------------------------
def write_runs(w, target):
    r = random.Random(W.SEED + 7)
    out26, out24 = [], []
    for c in sorted(w.customers.values(), key=lambda x: x["cid"]):
        if not c["facilities"]:
            continue
        # December 2026
        on26 = c["since"] <= W.RUN26 and (c["exit"] is None or c["exit"] > W.RUN26)
        if on26:
            d26 = in_default(w, c["cid"], W.RUN26)
            for f in c["facilities"]:
                pd = 1.0 if d26 else c["pd"]
                stage = 3 if d26 else (2 if (c["role"] == "watch" or pd >= 0.08) else 1)
                life = 1.0 if d26 else min(0.95, 1 - (1 - pd) ** (2.6 if stage == 2 else 3.4))
                ecl = (pd if stage == 1 else life) * f["lgd"] * f["ead"]
                out26.append([W.RUN26.isoformat(), f["fid"], c["cid"], c["name"], f["product"], money(f["limit"]),
                              money(f["drawn"]), stage, "%.4f" % pd, "%.4f" % life, "%.3f" % f["lgd"],
                              money(f["ead"]), money(ecl)])
        # December 2024 (arrears cut-off 20 December)
        on24 = c["since"] <= W.RUN24 and (c["exit"] is None or c["exit"] > W.RUN24)
        if on24:
            d24 = in_default(w, c["cid"], W.RUN24_CUTOFF)
            cured24 = any(df["cid"] == c["cid"] and df["cure"] and W.D(2024, 1, 1) <= df["cure"] <= W.RUN24
                          for df in w.defaults)
            for f in c["facilities"]:
                pd = 1.0 if d24 else c["pd"]
                stage = 3 if d24 else (2 if (cured24 or pd >= 0.08) else 1)
                drawn = f["drawn"] * (1.08 if not f["revolving"] else r.uniform(0.8, 1.05))
                drawn = min(f["limit"] * (1.15 if not f["revolving"] else 1.0), drawn)
                ead = drawn + 0.6 * (f["limit"] - drawn) if f["revolving"] else drawn
                out24.append([W.RUN24.isoformat(), f["fid"], c["cid"], c["name"], c["sector"], f["product"],
                              money(f["limit"]), money(drawn), stage, "%.4f" % pd, "%.3f" % f["lgd"], money(ead)])
    n26 = write_csv(os.path.join(target, "ifrs9_facility_run_2026-12-31.csv"),
                    ["run_date", "facility_id", "customer_no", "borrower", "product", "limit_nzd", "drawn_nzd", "stage",
                     "pd_12m", "pd_lifetime", "lgd", "ead_nzd", "ecl_nzd"], out26)
    n24 = write_csv(os.path.join(target, "ifrs9_facility_run_2024-12-31.csv"),
                    ["run_date", "facility_id", "customer_no", "borrower", "anzsic_division", "product", "limit_nzd",
                     "drawn_nzd", "stage", "pd_12m", "lgd", "ead_nzd"], out24)
    return n26, n24


# ---- security register, titles, index ---------------------------------------------------------------------
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def val_ref(p, r):
    m = p["made"]
    v = p["valuer"]
    if v == "Telfer Young":
        return "TY %s/%04d val %s" % (m.strftime("%y"), r.randint(1, 3999), m.strftime("%d/%m/%Y"))
    if v == "Colliers":
        return "Colliers ref %04d-%02d inspected %d %s %d" % (r.randint(1, 9999), r.randint(1, 40), m.day,
                                                            MONTHS[m.month - 1][:3], m.year)
    if v == "JLL":
        return "JLL %d/%03d (%s %d)" % (m.year, r.randint(1, 499), MONTHS[m.month - 1], m.year)
    if v == "Bayleys Valuations":
        return "BV-%s-%03d" % (m.strftime("%y%m"), r.randint(1, 899))
    if v == "Knight Frank":
        return "KF %s" % m.strftime("%d.%m.%y")
    return "Blackmore desktop %s-%s" % (MONTHS[m.month - 1][:3], m.strftime("%y"))


def write_security(w, target):
    r = random.Random(W.SEED + 9)
    path = os.path.join(target, "security_register_2026-12.xlsx")
    wb = wb_new("Ruahine Bank Lending Services")
    ws = wb.active
    ws.title = "Properties"
    rows = []
    for p in w.props:
        recorded = W.MIGRATION if p["made"] < W.MIGRATION else p["made"]
        title = p["title"]
        if "/" in title and r.random() < 0.35:
            title = title.lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        prior = round(p["amount"] * r.uniform(0.3, 0.6) / 1000) * 1000 if p["priority"] == "2nd" else 0
        rows.append([p["sid"], p["cid"], title, p["address"], p["ptype"], p["region"], p["amount"], recorded,
                     p["valuer"], val_ref(p, r), p["priority"], prior, "Held"])
    sheet(ws, ["security_id", "customer_no", "title_reference", "address", "property_type", "region",
               "valuation_nzd", "valuation_date", "valuer", "valuation_reference", "priority", "prior_charges_nzd",
               "status"], rows, {"address": 30, "valuation_reference": 38})
    for row in ws.iter_rows(min_row=2):
        row[7].number_format = "dd/mm/yyyy"
        row[6].number_format = "#,##0"
    # guarantees
    ws2 = wb.create_sheet("Guarantees")
    grows, lrows = [], []
    cust = w.customers
    words = {250_000: "Two hundred and fifty thousand dollars", 300_000: "Three hundred thousand dollars",
             350_000: "Three hundred and fifty thousand dollars", 400_000: "Four hundred thousand dollars",
             500_000: "Five hundred thousand dollars", 650_000: "Six hundred and fifty thousand dollars",
             750_000: "Seven hundred and fifty thousand dollars", 900_000: "Nine hundred thousand dollars"}
    lseq = 880
    for g in sorted(w.guars, key=lambda x: x["gid"]):
        gc = cust[g["guarantor"]]
        name = gc["name"]
        for fn, chg in gc["former"]:
            if g["deed"] < chg:
                name = fn
        nzbn = gc["nzbn"] if g["deed"] >= W.D(2016, 1, 1) else ""
        if g["kind"] == "unlimited":
            lim = "Unlimited"
        else:
            a = g["amount"]
            k = r.random()
            if a in words and k < 0.4:
                lim = words[a] + (" plus interest and costs" if r.random() < 0.5 else "")
            elif k < 0.7:
                lim = "$%s plus interest and costs" % format(a, ",")
            else:
                lim = "$%s" % format(a, ",")
        gd = cust[g["guaranteed"]]
        gname = gd["trading"] if r.random() < 0.3 else gd["name"]
        grows.append([g["gid"], name.upper() if r.random() < 0.25 else name, nzbn, gd["cid"], gname,
                      g["kind"].capitalize(), lim, g["deed"], "Current"])
        lseq += r.randint(1, 5)
        lrows.append(["DL%05d" % lseq, g["gid"], "Executed", g["deed"], "Deed held at Lending Services"])
        if r.random() < 0.12 and g["deed"] < W.D(2025, 1, 1):
            lseq += r.randint(1, 5)
            lrows.append(["DL%05d" % lseq, g["gid"], "Varied", g["deed"] + dt.timedelta(days=r.randint(100, 900)),
                          "Deed of variation: guaranteed facilities restated"])
        if g["released"]:
            lseq += r.randint(1, 5)
            lrows.append(["DL%05d" % lseq, g["gid"], "Released", g["released"],
                          r.choice(["Release signed by credit officer", "Released on repayment of guaranteed loan",
                                    "Release executed, deed returned to guarantor"])])
    sheet(ws2, ["guarantee_id", "guarantor_name", "guarantor_nzbn", "guaranteed_customer_no", "guaranteed_customer",
                "guarantee_type", "limit", "deed_date", "status"], grows, {"guarantor_name": 36, "guaranteed_customer": 32,
                                                                          "limit": 48})
    for row in ws2.iter_rows(min_row=2):
        row[7].number_format = "dd/mm/yyyy"
    ws3 = wb.create_sheet("Deed log")
    lrows.sort(key=lambda x: (x[3], x[0]))
    sheet(ws3, ["log_id", "guarantee_id", "event", "event_date", "note"], lrows, {"note": 46})
    for row in ws3.iter_rows(min_row=2):
        row[3].number_format = "dd/mm/yyyy"
    wb.save(path)
    postprocess.scrub(path, "Ruahine Bank Lending Services", "2027-01-20")
    postprocess.finish_office(path, "2023-08-14T02:31:00Z", "2027-01-20T03:47:00Z", "Ruahine Bank")
    return len(rows), len(grows), len(lrows)


BANKS = ["ANZ Bank New Zealand Limited", "ASB Bank Limited", "Bank of New Zealand", "Westpac New Zealand Limited"]


def write_titles(w, target):
    r = random.Random(W.SEED + 11)
    rows = []
    inst = 11_204_000
    for p in sorted(w.props, key=lambda x: x["title"]):
        if p["priority"] == "2nd":
            inst += r.randint(11, 900)
            rows.append([p["title"], "%d.%d" % (inst, 1), "Mortgage", r.choice(BANKS),
                         (p["registered"] - dt.timedelta(days=r.randint(200, 3000))).isoformat(), ""])
        inst += r.randint(11, 900)
        rows.append([p["title"], "%d.%d" % (inst, r.choice([1, 2])), "Mortgage", "Ruahine Bank Limited",
                     p["registered"].isoformat(), p["discharged"].isoformat() if p["discharged"] else ""])
    return write_csv(os.path.join(target, "title_instruments_2026-12.csv"),
                     ["title_reference", "instrument_number", "instrument_type", "mortgagee", "registered_date",
                      "discharged_date"], rows)


def quarters():
    out = []
    for y in range(2015, 2027):
        for q in range(1, 5):
            out.append((y, q))
    return out


def index_series():
    """The regional commercial property index: one path per region and property type, every quarter published
    provisional and revised a quarter later; the latest quarter provisional only."""
    r = random.Random(W.SEED + 13)
    series = {}
    for reg in W.REGIONS:
        for pt in ("Industrial", "Commercial"):
            v = 1000.0
            out = {}
            for (y, q) in quarters():
                g = 0.019 if y <= 2021 else (0.006 if y == 2022 else (-0.021 if y == 2023 else (-0.004 if y == 2024 else 0.009)))
                g += {"Industrial": 0.003, "Commercial": -0.002}[pt] + {"Manawatū-Whanganui": 0.001, "Hawke's Bay": 0.0,
                                                                         "Wellington": -0.002, "Taranaki": 0.002}[reg]
                v *= 1 + g + r.uniform(-0.004, 0.004)
                out[(y, q)] = round(v, 1)
            series[(reg, pt)] = out
    return series


def write_index(target):
    r = random.Random(W.SEED + 17)
    s = index_series()
    rows = []
    qs = quarters()
    # one national release a quarter, about a fortnight after the quarter ends: the new quarter's provisional value
    # and the previous quarter revised, published together
    cal = random.Random(W.SEED + 171)
    pub = {}
    for (y, q) in qs:
        qend = W.D(y, 3 * q, 30 if q in (2, 3) else 31)
        pub[(y, q)] = qend + dt.timedelta(days=14 if (y, q) == (2026, 4) else cal.randint(11, 18))
    for (reg, pt), out in sorted(s.items()):
        for i, (y, q) in enumerate(qs):
            rev = out[(y, q)]
            prov = round(rev * (1 + r.uniform(-0.006, 0.006)), 1)
            if (y, q) != (2026, 4):
                r.randint(38, 46)   # the stream's old release-lag draw, kept so every provisional value keeps its draw
            rows.append([reg, pt, "%dQ%d" % (y, q), "%.1f" % prov, "Provisional", pub[(y, q)].isoformat()])
            if (y, q) != (2026, 4):
                rows.append([reg, pt, "%dQ%d" % (y, q), "%.1f" % rev, "Revised", pub[qs[i + 1]].isoformat()])
    return write_csv(os.path.join(target, "commercial_property_index_2015-2026.csv"),
                     ["region", "property_type", "quarter", "index_value", "release", "published"], rows), s


def write_companies(w, target):
    r = random.Random(W.SEED + 19)
    rows = []
    for c in sorted(w.customers.values(), key=lambda x: x["nzbn"]):
        former = "; ".join("%s (to %s)" % (fn.upper(), chg.strftime("%d/%m/%Y")) for fn, chg in c["former"])
        inc = W.D(min(c["since"].year, 2018) - r.randint(0, 6), r.randint(1, 12), r.randint(1, 28))
        rows.append([c["nzbn"], c["company_no"], c["name"].upper(), former, inc.strftime("%d/%m/%Y"),
                     "Removed" if (c["exit"] and r.random() < 0.3) else "Registered", c["region"]])
    return write_csv(os.path.join(target, "companies_register_extract_2026-12.csv"),
                     ["nzbn", "company_number", "entity_name", "previous_names", "incorporation_date", "entity_status",
                      "registered_office_region"], rows)


def write_regional(target):
    """A distractor: the regional economic series the sector appetite statement cites."""
    r = random.Random(W.SEED + 23)
    rows = []
    for reg in W.REGIONS:
        gdp = r.uniform(5_000, 21_000)
        une = r.uniform(3.4, 4.6)
        for y in range(2019, 2027):
            for q in range(1, 5):
                gdp *= 1 + r.uniform(-0.01, 0.018)
                une = max(2.8, min(6.5, une + r.uniform(-0.25, 0.3)))
                rows.append([reg, "%dQ%d" % (y, q), "%.0f" % gdp, "%.1f" % une, r.randint(180, 900)])
    return write_csv(os.path.join(target, "regional_economic_indicators_2019-2026.csv"),
                     ["region", "quarter", "gdp_nzd_m_chain_volume", "unemployment_rate_pct", "building_consents"], rows)
