"""Renders the ask files (realised losses and the grade back-test) into target/."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font

import params as P
from io_util import write_csv, fmt_date, save_xlsx

OFFICERS = ["T Rees", "K Boyd", "D Moran", "S Hood", "L Woolley", "B Alexander", "P Nicol"]


def _dt(s):
    return dt.datetime.strptime(s, "%d/%m/%Y")


def write_loss_files(W, out):
    rng = np.random.default_rng(P.SEED + 303)
    rows = [[r["fac"], r["cust"], fmt_date(r["date"]), f"{r['amount']:.2f}", "Business"] for r in W.wo_rows]
    for k in range(34):
        d = dt.date(2023, 10, 1) + dt.timedelta(days=int(rng.integers(0, 1090)))
        rows.append(["F" + str(int(rng.integers(30000000, 39999999))), str(int(rng.integers(7100000, 7999999))),
                     fmt_date(d), f"{float(np.exp(rng.normal(np.log(P.WO_MEDIAN * 0.9), 0.8))):.2f}",
                     str(rng.choice(["Rural", "Commercial property"]))])
    rows.sort(key=lambda x: (_dt(x[2]), x[0]))
    write_csv(os.path.join(out, "write_offs_2023-10_to_2026-09.csv"),
              ["facility_no", "customer_no", "posting_date", "amount_nzd", "portfolio"], rows)

    crow = [[c["case"], c["cust"], fmt_date(c["opened"]), OFFICERS[int(rng.integers(len(OFFICERS)))], "Open"]
            for c in W.cases + W.gcases]
    rng.shuffle(crow)
    write_csv(os.path.join(out, "collections_cases_open_2026-09-30.csv"),
              ["case_no", "customer_no", "opened", "case_officer", "status"], crow)

    wb = Workbook()
    ws = wb.active
    ws.title = "Receipts"
    ws.append(["Business Banking Collections - receipts posted 1 October 2025 to 30 September 2026"])
    ws.append([])
    ws.append(["Receipt ID", "Case No", "Receipt Date", "Amount (NZD)", "Receipt Type", "Reference"])
    for c in ws[3]:
        c.font = Font(bold=True)
    rec = [r for r in W.coll_receipts if P.WIN_START <= r["date"] <= P.WIN_END]
    rec.sort(key=lambda r: (r["date"], r["case"], r["amount"]))
    used = set()
    for r in rec:
        while True:
            rid = f"R{int(rng.integers(5000000, 5999999))}"
            if rid not in used:
                used.add(rid)
                break
        ws.append([rid, r["case"], r["date"], round(r["amount"], 2), r["type"], r["ref"]])
    for row in ws.iter_rows(min_row=4):
        row[2].number_format = "dd/mm/yyyy"
        row[3].number_format = "#,##0.00"
    for col, w in (("A", 11), ("B", 14), ("C", 12), ("D", 14), ("E", 22), ("F", 12)):
        ws.column_dimensions[col].width = w
    save_xlsx(wb, os.path.join(out, "collections_receipts_FY2026.xlsx"), "Collections receipts FY2026",
              "Tania Rees", "2026-10-08T07:41:00Z")

    g = [[x["gno"], x["guarantor"], x["company"], x["fac"], f"{x['limit']:.0f}", fmt_date(x["signed"])] for x in W.guarantees]
    for k in range(60):
        b = W.borrowers[int(rng.integers(len(W.borrowers)))]
        g.append([f"G{int(rng.integers(40000, 69999))}", str(int(rng.integers(7100000, 7999999))), b["cust"],
                  b["facs"][0]["fac"], f"{round(b['ead_total'] * float(rng.uniform(.3, 1)), -3):.0f}",
                  fmt_date(dt.date(int(rng.integers(2016, 2026)), int(rng.integers(1, 13)), int(rng.integers(1, 28))))])
    g.sort(key=lambda x: x[0])
    write_csv(os.path.join(out, "guarantees_register_2026-09-30.csv"),
              ["guarantee_no", "guarantor_customer_no", "guaranteed_customer_no", "facility_no", "limit_nzd", "signed"], g)

    srow = []
    for s in W.realis:
        if s["date"] < P.WIN_START:
            continue
        srow.append([s["pref"], fmt_date(s["date"]), f"{s['gross']:.2f}", f"{s['costs']:.2f}", f"{s['net']:.2f}", s["fac"]])
    srow.sort(key=lambda x: (_dt(x[1]), x[0]))
    write_csv(os.path.join(out, "security_realisations_settled_FY2026.csv"),
              ["property_ref", "settlement_date", "gross_proceeds_nzd", "selling_costs_nzd", "net_proceeds_nzd",
               "facility_no"], srow)


def write_customer_master(W, out):
    rng = np.random.default_rng(P.SEED + 304)
    rows = []
    for b in W.borrowers:
        rows.append([b["cust"], "Business", b["firm"]["name"], b["firm"]["nzbn"], "Business", "Active"])
    for c in W.loss_cos:
        rows.append([c["cust"], "Business", c["ent"]["name"], c["ent"]["nzbn"], "Business", "Written off"])
    for p in W.persons:
        rows.append([p["cust"], "Personal", p["name"], "", "Retail", "Active"])
    merged = {m["retired"]: m["surviving"] for m in W.merge}
    for s in W.snap:
        if s["left"] and s["left"] != "wo":
            book = "Rural" if s["left"] == "rural" else "Business"
            status = {"repaid": "Closed", "refinanced": "Closed", "rural": "Active", "failed": "Closed"}[s["left"]]
            cno = merged.get(s["cust"], s["cust"])
            rows.append([cno, "Business", s["name"], s["nzbn"], book, status])
    rng.shuffle(rows)
    write_csv(os.path.join(out, "customer_master_extract_2026-10-09.csv"),
              ["customer_no", "customer_type", "customer_name", "nzbn", "book", "status"], rows)


def write_backtest_files(W, out):
    rng = np.random.default_rng(P.SEED + 305)
    rows = [[s["cust"], s["name"], s["model"], "BSM 4.2", "30/09/2025"] for s in W.snap]
    rng.shuffle(rows)
    write_csv(os.path.join(out, "risk_grade_snapshot_2025-09-30.csv"),
              ["customer_no", "customer_name", "model_grade", "model_version", "scored_date"], rows)
    wb = Workbook()
    ws = wb.active
    ws.title = "Overrides"
    ws.append(["Customer No", "Model Grade", "Override Grade", "Approved", "Removed", "Approver", "Reason"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for o in sorted(W.overrides, key=lambda o: (o["approved"], o["cust"])):
        ws.append([o["cust"], o["model"], o["override"], o["approved"], o["removed"],
                   str(rng.choice(["Credit Committee", "Head of Credit", "Senior Credit Manager"])), o["reason"]])
    for row in ws.iter_rows(min_row=2):
        row[3].number_format = "dd/mm/yyyy"
        row[4].number_format = "dd/mm/yyyy"
    save_xlsx(wb, os.path.join(out, "grade_overrides_2024-2026.xlsx"), "Grade overrides", "Marilyn Kendall",
              "2026-10-07T21:10:00Z")

    def reg_rows(events, prefix):
        out_rows = []
        ids = {}
        for e in events:
            key = (e["lead"], e["date"])
            if key not in ids:
                ids[key] = f"{prefix}{int(rng.integers(10000, 99999))}"
            out_rows.append([ids[key], e["lead"], e["fac"], fmt_date(e["date"]), e["trigger"]])
        out_rows.sort(key=lambda x: (_dt(x[3]), x[0], x[2]))
        return out_rows
    write_csv(os.path.join(out, "default_register_business_FY2026.csv"),
              ["event_id", "customer_no", "facility_no", "default_date", "trigger"], reg_rows(W.events_b, "DB"))
    write_csv(os.path.join(out, "default_register_rural_FY2026.csv"),
              ["event_id", "customer_no", "facility_no", "default_date", "trigger"], reg_rows(W.events_r + W.rural_own, "DR"))
    grows = []
    for g in W.groups:
        for k, m in enumerate(g["members"]):
            grows.append([g["gid"], m, "Lead" if k == 0 else "Member"])
    grows.sort(key=lambda x: (x[0], x[2] != "Lead", x[1]))
    write_csv(os.path.join(out, "connected_groups_2026-09-30.csv"), ["group_id", "customer_no", "role"], grows)
    write_csv(os.path.join(out, "customer_merge_log_2026-03-14.csv"),
              ["retired_customer_no", "surviving_customer_no", "merged_on"],
              [[m["retired"], m["surviving"], fmt_date(m["date"])] for m in W.merge])
