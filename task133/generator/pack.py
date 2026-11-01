"""Writes target/ for task133 architecture 3 from the world (main-call files and the ask files)."""
import datetime as dt
import os

import numpy as np

import params as P
import taxonomy as T
from io_util import write_csv, fmt_date, set_mtime
from names import bank_party

ENTITY_TYPE = {"gov": None, "acquirer": "NZ Limited Company", "insurer": "NZ Limited Company",
               "payer": "NZ Limited Company", "borrower": "NZ Limited Company", "filler": "NZ Limited Company"}


def gov_type(e):
    if "Council" in e["name"]:
        return "Local Authority"
    if e["bic"].startswith("K") or e["bic"].startswith("Q"):
        return "Crown Entity"
    return "Government Department"


def write_register(W, out):
    rng = np.random.default_rng(P.SEED + 11)
    rows = []
    order = rng.permutation(len(W.reg))
    for i in order:
        e = W.reg[int(i)]
        et = gov_type(e) if e["kind"] == "gov" else "NZ Limited Company"
        removed = ""
        status = e["status"]
        if status == "Removed":
            if e["kind"] == "former":
                # struck off after the liquidation that followed the default
                lo = e["default"] + dt.timedelta(days=120)
                hi = min(e["wo"] + dt.timedelta(days=400), dt.date(2026, 10, 2))
                if lo <= hi:
                    removed = fmt_date(lo + dt.timedelta(days=int(rng.integers(0, (hi - lo).days + 1))), "iso")
                else:
                    status = "Registered"
                    rng.integers(0, 640)
            else:
                removed = fmt_date(dt.date(2025, 1, 1) + dt.timedelta(days=int(rng.integers(0, 640))), "iso")
        rows.append([e["nzbn"], e["name"], et, status, fmt_date(e["registered"], "iso"), removed,
                     e["bic"], T.BIC[e["bic"]], e["trading"] or "", e["city"]])
    path = os.path.join(out, "nzbn_extract_canterbury_otago_southland_2026-10-12.csv")
    write_csv(path, ["nzbn", "entity_name", "entity_type", "entity_status", "registration_date", "removal_date",
                     "bic_code", "bic_description", "trading_names", "registered_office_city"], rows)
    return path


def write_lending_book(W, out):
    rng = np.random.default_rng(P.SEED + 12)
    rows = []
    for b in W.borrowers:
        name = b["firm"]["name"]
        if rng.random() < 0.38:
            name = name.replace(" Limited", " Ltd")
        code = b["bic"]
        u = rng.random()
        legacy = T.ANZSIC93.get(b["bic"])
        if legacy and u < 0.45:
            code = legacy
            b["code_shown"] = "legacy"
        elif u > 0.94:
            code = ""
            b["code_shown"] = "blank"
        else:
            b["code_shown"] = "bic"
        grade = "D" if b["in_default"] else str(b["grade"])
        for r in b["facs"]:
            nxt = dt.date(2026, 10, 1) + dt.timedelta(days=int(rng.integers(5, 360)))
            rows.append([r["fac"], b["cust"], name, b["firm"]["nzbn"], code, r["product"],
                         f"{r['limit']:.2f}", f"{r['drawn']:.2f}", r["security"], grade, b["branch"],
                         fmt_date(r["start"], "dmy_slash"), fmt_date(nxt, "dmy_slash")])
    rows.sort(key=lambda x: (x[10], x[1], x[0]))
    path = os.path.join(out, "business_lending_book_2026-09-30.csv")
    write_csv(path, ["facility_no", "customer_no", "customer_name", "nzbn", "industry_code", "product",
                     "limit_nzd", "drawn_nzd", "security_code", "risk_grade", "branch", "facility_start",
                     "next_review"], rows)
    return path


def party_for(W, ent, rng, cache):
    """The account name a payer's bank sends: its legal name, or its trading name if it trades under one."""
    k = ent["idx"]
    if k not in cache:
        use_trading = bool(ent.get("trading")) and rng.random() < P.TRADING_NAME_SHARE
        cache[k] = bank_party(ent["trading"] if use_trading else ent["name"])
    return cache[k]


def write_credits(W, out):
    rng = np.random.default_rng(P.SEED + 13)
    cache = {}
    acq_party = {W.acq[0]["idx"]: "KAHU MERCHANT SVCS", W.acq[1]["idx"]: "TUSSOCK PAYMENTS"}
    bmap = {b["cust"]: b for b in W.borrowers}
    rows = []
    for r in W.credits:
        b = bmap[r["cust"]]
        src = r["src"]
        if src == "B2B":
            e = W.reg[r["ent"]]
            party = party_for(W, e, rng, cache)
            if e["kind"] == "gov":
                part, code, ref = "PAYMENT", str(int(rng.integers(100000, 999999))), "REMIT"
            elif e["kind"] == "insurer":
                part, code, ref = "INV " + str(int(rng.integers(1000, 9999))), "REPAIR", "CLM" + str(int(rng.integers(10000, 99999)))
            else:
                part, code, ref = "INV " + str(int(rng.integers(1000, 99999))), "", b["firm"]["name"].split()[0].upper()[:12]
            tt = "DC"
        elif src == "CARD":
            party = acq_party[r["ent"]]
            part, code, ref = "SETTLEMENT", "MID" + b["cust"][-5:], "BATCH " + str(int(rng.integers(100, 999)))
            tt = "MS"
        elif src == "PRIV":
            fn, ln = r["payer"]
            u = rng.random()
            if u < 0.45:
                party = f"{fn[0]} {ln}".upper()
            elif u < 0.75:
                party = f"{ln} {fn[0]}".upper()
            elif u < 0.9:
                party = f"{fn} {ln}".upper()
            else:
                party = f"{fn[0]} {ln} AND {W.namer.fk.first_name()[0]} {ln}".upper()
            party = party[:20].rstrip()
            part, code, ref = ("INV " + str(int(rng.integers(100, 9999)))) if rng.random() < .6 else ln.upper()[:12], "", ""
            tt = "DC"
        elif src == "CASH":
            party, part, code, ref, tt = "BRANCH DEPOSIT", "CASH", b["branch"].upper()[:12], "", "DEP"
        elif src == "TFR":
            party, part, code, ref, tt = bank_party(b["firm"]["name"]), "TRANSFER", "FROM SAVINGS", "", "TFR"
        elif src == "IRD":
            party, part, code, ref, tt = "INLAND REVENUE DEPT", "GST REFUND", "", "", "DC"
        elif src == "LOAN":
            party, part, code, ref, tt = "ORARI BANK LTD", "LOAN ADVANCE", "", "", "LN"
        elif src == "CLAIM":
            ins = W.ins[int(rng.integers(len(W.ins)))]
            party, part, code, ref, tt = bank_party(ins["name"]), "CLAIM " + str(int(rng.integers(10000, 99999))), "SETTLED", "", "DC"
        elif src == "INT":
            party, part, code, ref, tt = "ORARI BANK LTD", "CREDIT INTEREST", "", "", "INT"
        else:
            raise ValueError(src)
        rows.append((r["date"], b["cust"], b["acct"], tt, party, part, code, ref, r["amount"]))
    rows.sort(key=lambda x: (x[0], x[2], x[3], x[4], x[8]))
    path = os.path.join(out, "operating_account_credits_2025-10_to_2026-09.csv")
    write_csv(path, ["posted_date", "customer_no", "account_no", "tran_type", "other_party", "particulars", "code",
                     "reference", "amount_nzd"],
              [[fmt_date(d, "dmy_slash"), c, a, t, p, pa, co, re_, f"{amt:.2f}"] for d, c, a, t, p, pa, co, re_, amt in rows])
    return path


def write_industry_series(W, out):
    """Quarterly sales by ANZSIC division for the South Island regions, NZD million (the region's published series)."""
    rng = np.random.default_rng(P.SEED + 14)
    quarters = []
    y, q = 2021, 4
    while (y, q) <= (2026, 3):
        quarters.append((y, q))
        q += 1
        if q == 5:
            y, q = y + 1, 1
    seas = {1: 1.02, 2: 0.96, 3: 0.97, 4: 1.05}
    rows = []
    for d, name in P.DIVISIONS.items():
        base = T.BASE_SALES[d]   # the year to Sep 2026
        yoy = T.YOY_PATH[d]      # years to Sep 2022..2026
        # annual totals back from the base
        annual = {2026: base}
        for k in range(4, 0, -1):
            annual[2021 + k] = annual[2022 + k] / (1 + yoy[k] / 100.0)
        annual[2021] = annual[2022] / (1 + yoy[0] / 100.0)
        for (yy, qq) in quarters:
            fy = yy + (1 if qq == 4 else 0)   # year to September
            fy = min(max(fy, 2022), 2026)
            sh = seas[qq] / 4.0
            if d == "H":
                sh = {1: 0.29, 2: 0.22, 3: 0.24, 4: 0.25}[qq]
            v = annual[fy] * sh * float(np.exp(rng.normal(0, 0.012)))
            flag = "P" if (yy, qq) == (2026, 3) else ("R" if (yy, qq) in ((2026, 2), (2026, 1)) else "")
            rows.append([f"{yy}Q{qq}", d, name, f"{v:.1f}", flag])
    path = os.path.join(out, "industry_sales_quarterly_south_island_2021Q4-2026Q3.csv")
    write_csv(path, ["quarter", "anzsic06_division", "division_name", "sales_nzd_million", "status"], rows)
    return path
