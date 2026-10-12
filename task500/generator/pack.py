"""Write the data files of the extract: the filer register, the returns, the treasury deposit ledger, the adopted
forecast and monthly report, the change list, and Appendix B of the two certified statements."""
import csv
import datetime as dt
import json
from pathlib import Path

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import calc
import world as W

F_REGISTER = "lodging_filer_register_2026-08.csv"
F_RETURNS = "lodging_tax_returns_fy2023-fy2026.csv"
F_LEDGER = "treasury_lodging_deposits_fy2025-fy2026.csv"
F_REPORT = "adopted_forecast_lodging_fy2026.csv"
F_CHANGES = "lodging_tax_changes_fy2024-fy2026.csv"
F_APPENDIX = "variance_statements_appendix_b_fy2024_fy2025.xlsx"


def _w(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


def due_date(period):
    nxt = dt.date(period.year + (period.month == 12), period.month % 12 + 1, 20)
    return nxt


class Writer:
    def __init__(self, state, target):
        self.m = state
        self.T = Path(target)

    def run(self):
        self.register()
        self.returns()
        self.ledger()
        self.report()
        self.changes()
        self.appendix()

    # ------------------------------------------------------------------ register
    def register(self):
        rows = []
        for f in sorted(self.m.register, key=lambda f: f["filer_id"]):
            rows.append([f["filer_id"], f["cls"], f["rooms"] if f["cls"] != "PF" else "", f["region"], f["county"],
                         f["opened"].isoformat(), f["closed"].isoformat() if f["closed"] else ""])
        _w(self.T / F_REGISTER, ["filer_id", "class", "rooms_or_units", "region", "county", "license_from",
                                 "license_to"], rows)

    # ------------------------------------------------------------------ returns
    def returns(self):
        rng = np.random.default_rng([W.SEED, 41])
        rows = []
        for r in sorted(self.m.returns, key=lambda r: (r["period"], r["filer_id"], r["county"])):
            filed = due_date(r["period"]) - dt.timedelta(days=int(rng.integers(0, 12)))
            if rng.random() < 0.05:
                filed = due_date(r["period"]) + dt.timedelta(days=int(rng.integers(3, 40)))
            filed = min(filed, dt.date(2026, 8, 12))      # the extract holds every return received by August 12
            r["filed"] = filed
            rows.append([r["filer_id"], W.ym(r["period"]), r["county"], "%.2f" % r["taxable_receipts"],
                         "%.4f" % r["rate"], "%.2f" % r["tax"], filed.isoformat()])
        _w(self.T / F_RETURNS, ["filer_id", "period", "county", "taxable_receipts", "tax_rate", "tax_due",
                                "filed_date"], rows)

    # ------------------------------------------------------------------ treasury ledger (fiscal 2025 and 2026 deposits)
    def ledger(self):
        rng = np.random.default_rng([W.SEED, 42])
        rows = []
        dep = 1
        start, end = dt.date(2024, 7, 1), dt.date(2026, 7, 31)
        for r in sorted(self.m.returns, key=lambda r: (r["period"], r["filer_id"], r["county"])):
            if r["period"] < dt.date(2024, 6, 1):
                continue
            paid = r["filed"] + dt.timedelta(days=int(rng.integers(0, 3)))
            if not (start <= paid <= end):
                continue
            rows.append(["D%07d" % dep, paid.isoformat(), r["filer_id"], W.ym(r["period"]), "TAX", "%.2f" % r["tax"], ""])
            dep += 1
            late = (paid - due_date(r["period"])).days
            if late > 0:
                pi = round(r["tax"] * (0.05 + 0.01 * late / 30), 2)
                pdate = paid + dt.timedelta(days=int(rng.integers(5, 25)))
                if pdate <= end:
                    rows.append(["D%07d" % dep, pdate.isoformat(), r["filer_id"], W.ym(r["period"]), "PEN_INT",
                                 "%.2f" % pi, ""])
                    dep += 1
            u = rng.random()
            if u < 0.008:        # overpayment refunded
                amt = -round(r["tax"] * float(rng.uniform(0.05, 0.3)), 2)
                rdate = paid + dt.timedelta(days=int(rng.integers(30, 70)))
                if rdate <= end:
                    rows.append(["D%07d" % dep, rdate.isoformat(), r["filer_id"], W.ym(r["period"]), "REFUND",
                                 "%.2f" % amt, ""])
                    dep += 1
            elif u < 0.022:      # amended return: one or two amendments, each restating the whole difference
                n_am = 1 if rng.random() < 0.7 else 2
                diff = round(r["tax"] * float(rng.uniform(-0.12, 0.18)), 2)
                dates = [paid + dt.timedelta(days=int(rng.integers(20, 50)) * (k + 1)) for k in range(n_am)]
                # a return's amendments are booked within one fiscal year and inside the ledger
                if dates[-1] > end or W.fy(dates[0]) != W.fy(dates[-1]):
                    dates = dates[:1]
                    if dates[0] > end:
                        dates = []
                for k, adate in enumerate(dates):
                    amt = diff if k == len(dates) - 1 else round(diff * float(rng.uniform(0.4, 0.9)), 2)
                    rows.append(["D%07d" % dep, adate.isoformat(), r["filer_id"], W.ym(r["period"]), "AMEND",
                                 "%.2f" % amt, "A%d" % (k + 1)])
                    dep += 1
        rows.sort(key=lambda x: (x[1], x[0]))
        _w(self.T / F_LEDGER, ["deposit_id", "deposit_date", "filer_id", "period", "type", "amount",
                               "amendment_seq"], rows)

    # ------------------------------------------------------------------ monthly report against the adopted forecast
    def report(self):
        rng = np.random.default_rng([W.SEED, 43])
        liab = {}
        for r in self.m.returns:
            liab[r["period"]] = liab.get(r["period"], 0.0) + r["tax"]
        rows = []
        for i in range(36, 48):
            m = W.MONTHS[i]
            prior = liab[W.MONTHS[i - 12]]
            fc = round(prior * float(rng.uniform(1.028, 1.040)) / 1000) * 1000
            rows.append([W.ym(m), "%d" % fc])
        self.forecast = {r[0]: int(r[1]) for r in rows}
        _w(self.T / F_REPORT, ["period", "adopted_forecast_tax"], rows)

    # ------------------------------------------------------------------ the change list
    def changes(self):
        rows = [[str(c["fy"]), c["code"], c["name"], c["effective"].isoformat(), "", c["touched"]]
                for c in W.CHANGES_PRIOR]
        rows += [["2026", c["code"], c["name"], c["effective"].isoformat(), c["end"].isoformat() if c["end"] else "",
                  c["touched"]] for c in W.CHANGES_FY2026]
        _w(self.T / F_CHANGES, ["fiscal_year", "code", "change", "effective", "ended", "filers_affected"], rows)

    # ------------------------------------------------------------------ Appendix B of the certified statements
    def appendix(self):
        lines = [(r["filer_id"], r["period"], r["county"], r["taxable_receipts"], r["tax"]) for r in self.m.returns]
        pn = calc.Panel(self.m.register, lines)
        wb = Workbook()
        wb.remove(wb.active)
        self.certified = {}
        for year, code, title in ((2024, "HW", "FY2024 Highway 14"), (2025, "SD", "FY2025 Stadium district")):
            total, det = calc.standing_method(pn, year, code, return_detail=True)
            self.certified[code] = (total, det)
            ws = wb.create_sheet(title)
            ws["A1"] = "Appendix B. Reference figures by filer, %s (certified)" % title.split(" ", 1)[1]
            ws["A1"].font = Font(bold=True, size=11)
            ws["A2"] = "Fiscal %d revenue variance statement. Window: effective month through June %d." % (year, year)
            ws["A2"].font = Font(italic=True, size=9, color="555555")
            head = ["Filer", "Class", "Region", "Window", "Actual taxable receipts", "Reference taxable receipts",
                    "Difference", "Tax effect"]
            for j, h in enumerate(head, 1):
                c = ws.cell(row=4, column=j, value=h)
                c.font = Font(bold=True, color="FFFFFF")
                c.fill = PatternFill("solid", fgColor="2F4858")
                c.alignment = Alignment(wrap_text=True, vertical="center")
            eff = calc.EFFECTIVE[code]
            win = "%s to %d-06" % (W.ym(eff), year)
            r = 5
            for fid in sorted(det, key=lambda k: (pn.f[k]["region"], pn.f[k]["cls"], k)):
                v = det[fid]
                row = [fid, pn.f[fid]["cls"], pn.f[fid]["region"], win, round(v["actual"]), round(v["reference"]),
                       round(v["actual"]) - round(v["reference"]), round(v["tax_effect"])]
                for j, x in enumerate(row, 1):
                    cell = ws.cell(row=r, column=j, value=x)
                    if j >= 5:
                        cell.number_format = "#,##0;-#,##0"
                r += 1
            ws.cell(row=r, column=1, value="Total").font = Font(bold=True)
            sums = (sum(det[k]["actual"] for k in det), sum(det[k]["reference"] for k in det))
            for j, x in ((5, sums[0]), (6, sums[1]), (7, sums[0] - sums[1]), (8, total)):
                cell = ws.cell(row=r, column=j, value=round(x))
                cell.number_format = "#,##0;-#,##0"
                cell.font = Font(bold=True)
            ws.cell(row=r + 2, column=1, value="Rows and totals are each rounded to the dollar from unrounded "
                                               "figures.").font = Font(italic=True, size=9, color="555555")
            for col, w in zip("ABCDEFGH", (11, 7, 22, 18, 14, 14, 12, 11)):
                ws.column_dimensions[col].width = w
            ws.freeze_panes = "A5"
        wb.save(self.T / F_APPENDIX)
