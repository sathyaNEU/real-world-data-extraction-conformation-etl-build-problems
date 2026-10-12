"""Yacaaba's legacy general ledger, July 2025 to September 2026, and its trial balances.
Every fixed-asset line is posted from the legacy truth (ledger.Engine with TRUTH); everything else is
the practice's ordinary business at a realistic scale, balanced journal by journal."""
import datetime as dt
from collections import defaultdict
from decimal import Decimal

import ledger as L
from params import ACCOUNTS, ACCOUNT_NAMES, SITES, RECLASS_POSTED

D = Decimal
Z = D("0")

NAMES = dict(ACCOUNT_NAMES)
NAMES.update({
    "1-1110": "Cheque Account - CBA", "1-1120": "Medicare EFT Clearing", "1-1200": "Trade Debtors",
    "1-1310": "Prepayments", "2-1200": "Trade Creditors", "2-1330": "GST Paid", "2-1310": "GST Collected",
    "2-1410": "PAYG Withholding Payable", "2-1420": "Superannuation Payable", "2-1510": "Accrued Expenses",
    "2-1810": "Intercompany - Quandong Imaging Group", "2-1820": "Intercompany - Bremer Radiology",
    "3-1000": "Share Capital", "3-8000": "Retained Earnings",
    "4-1110": "Fees - MRI", "4-1120": "Fees - CT", "4-1130": "Fees - General X-ray", "4-1140": "Fees - Ultrasound",
    "4-1150": "Fees - Mammography", "4-1160": "Fees - Fluoroscopy", "4-1170": "Fees - OPG & Bone Density",
    "4-1900": "Other Income", "8-1000": "Gain on Disposal of Assets",
    "5-1100": "Radiologist Reporting Fees", "5-1200": "Contrast & Consumables", "5-1300": "Equipment Service Contracts",
    "6-1100": "Wages - Clinical", "6-1110": "Wages - Admin & Reception", "6-1200": "Superannuation",
    "6-1300": "Rent", "6-1400": "Electricity & Gas", "6-1500": "IT & Software Subscriptions", "6-1600": "Insurance",
    "6-1700": "Management Fee - QIG", "6-2900": "Loss on Disposal of Assets", "6-3100": "Bank Fees",
    "6-3200": "Cleaning", "6-3300": "Repairs & Maintenance",
})

MODALITY_ACC = {"MRI": "4-1110", "CT": "4-1120", "XR": "4-1130", "US": "4-1140", "MG": "4-1150", "FL": "4-1160", "OD": "4-1170"}
SITE_MODS = {"CHA": ["MRI", "CT", "XR", "US", "MG", "FL"], "MAI": ["MRI", "CT", "XR", "US", "MG", "OD"],
             "CES": ["CT", "XR", "US", "OD"], "RAY": ["CT", "XR", "US", "OD"]}
DAILY = {"MRI": (9000, 26000), "CT": (6000, 15000), "XR": (2500, 7200), "US": (3500, 9800), "MG": (1600, 4800),
         "FL": (700, 2600), "OD": (300, 1700)}


def mrange():
    return L.REPLAY


def month_end(i):
    y, m = L.ym(i)
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


class GL:
    def __init__(self, w, eng, rng):
        self.w, self.eng, self.rng = w, eng, rng
        self.lines = []
        self.jn = 0

    def journal(self, date, src, rows, memo, period=None):
        """rows: [(account, debit, credit, job, memo or None)]"""
        self.jn += 1
        jid = "%s%06d" % (src, self.jn)
        dr = sum((r[1] for r in rows), Z)
        cr = sum((r[2] for r in rows), Z)
        assert dr == cr, (memo, dr, cr)
        for acc, d_, c_, job, m in rows:
            self.lines.append(dict(date=date, period=period or "%04d-%02d" % (date.year, date.month), journal=jid, src=src,
                                   account=acc, account_name=NAMES[acc], job=job or "", memo=m or memo,
                                   debit=d_, credit=c_))

    # ------------------------------------------------------------------ fixed assets
    def asset_balances(self, m):
        """Cost and accumulated balances by account at the end of month m, from the truth."""
        cost, acc = defaultdict(lambda: Z), defaultdict(lambda: Z)
        for a in self.w.ledger_assets():
            if L.mdate(a["acquired"]) > m:
                continue
            if a["disposed"] and L.mdate(a["disposed"]) <= m:
                continue
            ca, aa, _ = ACCOUNTS[a["category"]]
            cost[ca] += a["cost"]
            acc[aa] += self.eng.accumulated(a, m)
        return cost, acc

    def build(self):
        rng = self.rng
        w = self.w
        first = L.REPLAY[0]
        opening_date = dt.date(2025, 7, 1)
        # opening balances: fixed assets from the truth at 30 June 2025, the rest plausible
        cost, acc = self.asset_balances(L.JUN25)
        ob = []
        for k in sorted(cost):
            ob.append((k, cost[k], Z, "", "Opening balance"))
        for k in sorted(acc):
            ob.append((k, Z, acc[k], "", "Opening balance"))
        other = [("1-1110", D("1843226.17"), Z), ("1-1120", D("212880.42"), Z), ("1-1200", D("2671354.09"), Z),
                 ("1-1310", D("184400.00"), Z), ("2-1200", Z, D("1129087.63")), ("2-1310", Z, D("2140.55")),
                 ("2-1330", D("61377.20"), Z), ("2-1410", Z, D("188912.00")), ("2-1420", Z, D("141006.84")),
                 ("2-1510", Z, D("402215.00")), ("2-1810", Z, D("6400000.00")), ("3-1000", Z, D("1000.00"))]
        for k, d_, c_ in other:
            ob.append((k, d_, c_, "", "Opening balance"))
        dr = sum((r[1] for r in ob), Z)
        cr = sum((r[2] for r in ob), Z)
        ob.append(("3-8000", Z, dr - cr, "", "Opening balance")) if dr > cr else ob.append(("3-8000", cr - dr, Z, "", "Opening balance"))
        self.journal(opening_date, "OB", ob, "Opening balance")

        # asset additions in the window (purchase invoices), disposals, the Bremer transfer
        for a in sorted(w.ledger_assets(), key=lambda x: (x["acquired"], x["id"])):
            m = L.mdate(a["acquired"])
            if not (L.REPLAY[0] <= m <= L.REPLAY[-1]):
                continue
            ca = ACCOUNTS[a["category"]][0]
            if a["kind"] == "transfer_in":
                t = a["transfer"]
                nbv = a["cost"] - t["bf_accum"]
                memo = ("IC transfer in - Voluson E10 SN %s from Bremer %s (in service %s, 6 yr life), cost and accum dep b/f"
                        % (a["serial"], t["source_no"], t["source_in_service"].strftime("%d/%m/%Y")))
                self.journal(a["acquired"], "GJ", [(ca, a["cost"], Z, a["site"], memo),
                                                   (ACCOUNTS[a["category"]][1], Z, t["bf_accum"], a["site"], memo),
                                                   ("2-1820", Z, nbv, "", memo)], memo)
                continue
            gst = L.r2(a["cost"] * D("0.1"))
            memo = "%s %s - %s" % (a["supplier"], a["invoice"], a["description"])
            self.journal(a["acquired"], "PJ", [(ca, a["cost"], Z, a["site"], memo), ("2-1330", gst, Z, "", memo),
                                               ("2-1200", Z, a["cost"] + gst, "", memo)], memo)
        for a in sorted(w.disposed_window, key=lambda x: x["disposed"]):
            ca, aa, _ = ACCOUNTS[a["category"]]
            m = L.mdate(a["disposed"])
            accum = self.eng.accumulated(a, m)
            nbv = a["cost"] - accum
            p = a.get("proceeds", Z)
            memo = "Disposal - asset %s %s" % (a["id"], a["description"])
            rows = [(aa, accum, Z, a["site"], memo), (ca, Z, a["cost"], a["site"], memo)]
            if p:
                rows.append(("1-1110", p, Z, "", memo))
            if nbv > p:
                rows.append(("6-2900", nbv - p, Z, a["site"], memo))
            elif p > nbv:
                rows.append(("8-1000", Z, p - nbv, a["site"], memo))
            self.journal(a["disposed"], "GJ", rows, memo)

        # monthly depreciation from the truth, one journal per month, a pair of lines per category account
        for m in L.REPLAY:
            exp = defaultdict(lambda: Z)
            for a in w.ledger_assets():
                x = self.eng.posting(a, m)
                if x:
                    _, aa, ea = ACCOUNTS[a["category"]]
                    exp[(ea, aa)] += x
            rows = []
            y, mo = L.ym(m)
            memo = "Depreciation %s %d" % (dt.date(y, mo, 1).strftime("%B"), y)
            for (ea, aa) in sorted(exp):
                rows.append((ea, exp[(ea, aa)], Z, "", memo))
            for (ea, aa) in sorted(exp, key=lambda k: k[1]):
                rows.append((aa, Z, exp[(ea, aa)], "", memo))
            self.journal(month_end(m), "GJ", rows, memo)

        self.business()
        self.lines.sort(key=lambda r: (r["date"], r["journal"]))
        return self.lines

    # ------------------------------------------------------------------ ordinary business
    def business(self):
        rng = self.rng
        d0, d1 = dt.date(2025, 7, 1), dt.date(2026, 9, 30)
        days = [d0 + dt.timedelta(days=k) for k in range((d1 - d0).days + 1)]
        holidays = {dt.date(2025, 10, 6), dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1),
                    dt.date(2026, 1, 26), dt.date(2026, 4, 3), dt.date(2026, 4, 6), dt.date(2026, 4, 25),
                    dt.date(2026, 6, 8), dt.date(2025, 8, 4)}
        trading = [d for d in days if d.weekday() < 5 and d not in holidays]
        sat = [d for d in days if d.weekday() == 5 and d not in holidays]
        season = {1: 0.82, 2: 0.97, 3: 1.04, 4: 0.93, 5: 1.05, 6: 1.0, 7: 1.02, 8: 1.04, 9: 1.03, 10: 1.02, 11: 1.03, 12: 0.85}
        for d in trading + sat:
            for site, mods in SITE_MODS.items():
                if d.weekday() == 5 and site not in ("CHA", "MAI"):
                    continue
                f = season[d.month] * (0.55 if d.weekday() == 5 else 1.0)
                rows, tot = [], Z
                for mod in mods:
                    lo, hi = DAILY[mod]
                    v = D(int(rng.uniform(lo, hi) * f * (1.35 if site == "CHA" else 1.0))) + D(rng.randint(0, 99)) / 100
                    rows.append((MODALITY_ACC[mod], Z, v, site, None))
                    tot += v
                bulk = L.r2(tot * D(rng.uniform(0.52, 0.62)))
                dva = L.r2(tot * D(rng.uniform(0.02, 0.05)))
                pat = tot - bulk - dva
                memo = "Billing summary %s %s" % (SITES[site], d.strftime("%d/%m/%Y"))
                rows = [("1-1120", bulk, Z, site, "Medicare bulk billed"), ("1-1200", pat, Z, site, "Patient and insurer billed"),
                        ("1-1200", dva, Z, site, "DVA / WorkCover")] + rows
                self.journal(d, "BIL", rows, memo)
                # receipts two banking days later
                rd = d + dt.timedelta(days=2 if d.weekday() < 3 else 4)
                if rd <= d1:
                    m2 = "Banking %s %s" % (SITES[site], rd.strftime("%d/%m/%Y"))
                    got = L.r2(pat * D(rng.uniform(0.86, 0.97)))
                    self.journal(rd, "CR", [("1-1110", bulk + got + dva, Z, site, m2), ("1-1120", Z, bulk, site, "Medicare EFT"),
                                            ("1-1200", Z, got, site, "EFTPOS and cheques"), ("1-1200", Z, dva, site, "DVA remittance")], m2)
        # payroll, fortnightly on Thursdays
        pay = dt.date(2025, 7, 3)
        while pay <= d1:
            for site in SITES:
                big = {"CHA": 2.6, "MAI": 1.8, "CES": 1.0, "RAY": 1.0}[site]
                cl = D(int(rng.uniform(118000, 132000) * big)) + D(rng.randint(0, 99)) / 100
                ad = D(int(rng.uniform(31000, 36000) * big)) + D(rng.randint(0, 99)) / 100
                sup = L.r2((cl + ad) * D("0.12"))
                payg = L.r2((cl + ad) * D(rng.uniform(0.205, 0.225)))
                memo = "Payroll %s pay ending %s" % (SITES[site], (pay - dt.timedelta(days=4)).strftime("%d/%m/%Y"))
                self.journal(pay, "PY", [("6-1100", cl, Z, site, None), ("6-1110", ad, Z, site, None), ("6-1200", sup, Z, site, None),
                                         ("2-1410", Z, payg, "", None), ("2-1420", Z, sup, "", None),
                                         ("1-1110", Z, cl + ad - payg, "", None)], memo)
            pay += dt.timedelta(days=14)
        # monthly suppliers, management fee, accruals, tax remittances
        suppliers = [("Merewether Reporting Radiologists Pty Ltd", "5-1100", (390000, 455000), None),
                     ("Bayer Australia", "5-1200", (52000, 71000), None), ("GE Healthcare Australia", "5-1300", (38000, 41000), None),
                     ("Siemens Healthcare Pty Ltd", "5-1300", (61000, 64000), None), ("Philips Electronics Australia", "5-1300", (9000, 9800), None),
                     ("Canon Medical Systems ANZ", "5-1300", (14000, 15200), None), ("Medshop Australia", "5-1200", (11000, 19000), None),
                     ("Ausgrid / Origin Energy", "6-1400", (21000, 33000), None), ("Broadmeadow IT Services", "6-1500", (18000, 26000), None),
                     ("Pearson Street Medical Chambers Pty Ltd", "6-1300", (61800, 61800), "CHA"), ("High Street Maitland Holdings Pty Ltd", "6-1300", (38250, 38250), "MAI"),
                     ("Vincent Street Property Trust", "6-1300", (14900, 14900), "CES"), ("Port Stephens Commercial Holdings", "6-1300", (19650, 19650), "RAY"),
                     ("Lakeside Commercial Cleaning", "6-3200", (12000, 14500), None), ("Medifit Interiors", "6-3300", (2000, 9000), None)]
        for m in L.REPLAY:
            y, mo = L.ym(m)
            me = month_end(m)
            for sup, acc, (lo, hi), site in suppliers:
                d = dt.date(y, mo, rng.randint(3, 26))
                v = D(int(rng.uniform(lo, hi))) + (D(rng.randint(0, 99)) / 100 if lo != hi else Z)
                g = Z if acc == "5-1100" else L.r2(v * D("0.1"))
                memo = "%s INV %d" % (sup, rng.randint(10000, 99999))
                self.journal(d, "PJ", [(acc, v, Z, site or "", None)] + ([("2-1330", g, Z, "", None)] if g else []) +
                             [("2-1200", Z, v + g, "", None)], memo)
                pd_ = min(d + dt.timedelta(days=rng.randint(14, 30)), dt.date(2026, 9, 30))
                self.journal(pd_, "CD", [("2-1200", v + g, Z, "", None), ("1-1110", Z, v + g, "", None)], "Payment " + memo)
            self.journal(me, "GJ", [("6-1700", D("185000.00"), Z, "", None), ("2-1810", Z, D("185000.00"), "", None)],
                         "Management fee QIG %s" % me.strftime("%b %Y"))
            acc_amt = D(int(rng.uniform(140000, 175000)))
            self.journal(me, "GJ", [("5-1100", acc_amt, Z, "", None), ("2-1510", Z, acc_amt, "", None)],
                         "Accrue radiologist reporting %s" % me.strftime("%b %Y"))
            if m < L.REPLAY[-1]:
                nd = month_end(m) + dt.timedelta(days=1)
                self.journal(nd, "GJ", [("2-1510", acc_amt, Z, "", None), ("5-1100", Z, acc_amt, "", None)],
                             "Reverse accrual radiologist reporting %s" % me.strftime("%b %Y"))
            ins = D("21840.00")
            self.journal(dt.date(y, mo, 1), "GJ", [("6-1600", ins, Z, "", None), ("1-1310", Z, ins, "", None)], "Insurance amortisation")
            fee = D(int(rng.uniform(900, 1700))) + D(rng.randint(0, 99)) / 100
            self.journal(me, "CD", [("6-3100", fee, Z, "", None), ("1-1110", Z, fee, "", None)], "Bank fees %s" % me.strftime("%b %Y"))
            # BAS: GST input credits refunded quarterly (imaging services are GST-free), PAYG and super monthly
            if mo in (1, 4, 7, 10):
                gst_bal = sum((r["debit"] - r["credit"] for r in self.lines if r["account"] == "2-1330"), Z)
                if gst_bal > 0:
                    self.journal(dt.date(y, mo, 26), "CR", [("1-1110", gst_bal, Z, "", None), ("2-1330", Z, gst_bal, "", None)],
                                 "ATO BAS refund")
            payg_bal = sum((r["credit"] - r["debit"] for r in self.lines if r["account"] == "2-1410"), Z)
            sup_bal = sum((r["credit"] - r["debit"] for r in self.lines if r["account"] == "2-1420"), Z)
            rd = dt.date(y, mo, 21)
            if payg_bal > 0:
                self.journal(rd, "CD", [("2-1410", payg_bal, Z, "", None), ("1-1110", Z, payg_bal, "", None)], "ATO PAYG remittance")
            if sup_bal > 0:
                self.journal(rd, "CD", [("2-1420", sup_bal, Z, "", None), ("1-1110", Z, sup_bal, "", None)], "Super clearing house")


def trial_balance(lines, extra=None, fy_start=dt.date(2026, 7, 1)):
    """Balances at 30 September 2026: profit and loss accounts for the current financial year only,
    the FY2026 result closed to retained earnings at 30 June 2026."""
    bal = defaultdict(lambda: Z)
    for r in lines:
        if r["account"][0] in "4568" and r["date"] < fy_start:
            bal["3-8000"] += r["debit"] - r["credit"]
            continue
        bal[r["account"]] += r["debit"] - r["credit"]
    for acc, amt in (extra or []):
        bal[acc] += amt
    out = []
    for acc in sorted(bal):
        v = bal[acc]
        out.append(dict(account=acc, name=NAMES[acc], debit=v if v > 0 else Z, credit=-v if v < 0 else Z))
    assert sum((r["debit"] for r in out), Z) == sum((r["credit"] for r in out), Z)
    return out


def reclass_entries(w, eng):
    """Posted on 8 October 2026 into September: the Charlestown reception joinery moves from furniture to
    leasehold improvements, cost and accumulated depreciation, after the FY26 audit query."""
    a = w.joinery
    acc = eng.accumulated(a, L.SEP26)
    return [("1-6150", -a["cost"]), ("1-6140", a["cost"]), ("1-6155", acc), ("1-6145", -acc)]
