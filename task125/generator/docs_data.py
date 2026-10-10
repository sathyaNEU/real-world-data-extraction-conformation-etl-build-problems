"""Writers for the pack's data files: the spending file, the Tenancy Sustainment extract, the run log,
the payment calendar, Fernhollow's invoices, acknowledgements and rate cards, and the Household Support
Fund allocation workbook."""
import datetime as dt

import params as PR
import writers as WR
from world import DEPTS, DEPT_ORDER

SPINE_COLS = ["department", "service_area", "expense_type", "supplier_name", "vendor_no", "transaction_ref",
              "payment_date", "net_amount", "vat_amount"]


def pence(v):
    s = "-" if v < 0 else ""
    v = abs(v)
    return "%s%d.%02d" % (s, v // 100, v % 100)


def spine(path, world):
    rows = []
    for p in world.pay:
        rows.append(dict(department=DEPTS[p[0]][0], service_area=p[1], expense_type=p[2], supplier_name=p[3],
                         vendor_no=p[4], transaction_ref=p[9], payment_date=p[5].strftime("%d/%m/%Y"),
                         net_amount=pence(p[6]), vat_amount=pence(p[7])))
    return WR.write_csv(path, rows, SPINE_COLS)


def tsp_ledger(path, world):
    rows = [dict(case_ref=c, vendor_no=v, scheme_round=r, approved_on=a.isoformat(), payment_date=d.isoformat(),
                 amount=pence(amt)) for (c, v, r, a, d, amt) in sorted(world.tsp, key=lambda t: (t[4], t[0]))]
    return WR.write_csv(path, rows, ["case_ref", "vendor_no", "scheme_round", "approved_on", "payment_date",
                                     "amount"])


RUNLOG_COLS = ["run_ref", "run_month", "run_type", "run_completed", "department", "payments_in_range",
               "flagged_cell", "payments_routed", "batch_ref"]


def run_log(path, rows, when):
    wb = WR.xlsx_book(path, "Digit filter run log 2025/26", PR.PEOPLE["analyst"], "Wealdmoor County Council", when)
    ws = wb.add_worksheet("Run log")
    b = wb.add_format({"bold": True})
    hd = wb.add_format({"bold": True, "bg_color": "#D9E1F2", "border": 1})
    ws.write(0, 0, "Wealdmoor County Council, Exchequer Services", b)
    ws.write(1, 0, "Digit filter run log, 2025/26")
    ws.write(2, 0, "Cells applied: flagged cells notified from the 2023/24 screen (statement published July 2024). "
                   "The log records what each run screened and routed during 2025/26.")
    ws.write(3, 0, "Maintained by %s. Closed 7 April 2026 after the March 2026 run." % PR.PEOPLE["analyst"])
    for j, c in enumerate(RUNLOG_COLS):
        ws.write(5, j, c, hd)
    for i, r in enumerate(rows):
        for j, c in enumerate(RUNLOG_COLS):
            v = r[c]
            if c in ("payments_in_range", "payments_routed") or (c == "flagged_cell" and v != ""):
                ws.write_number(6 + i, j, int(v))
            else:
                ws.write_string(6 + i, j, str(v))
    ws.set_column(0, 0, 13)
    ws.set_column(1, 2, 13)
    ws.set_column(3, 3, 17)
    ws.set_column(4, 8, 15)
    ws.freeze_panes(6, 0)
    WR.close_xlsx(wb, path, "Wealdmoor County Council", when)
    return len(rows)


def calendar(path, when):
    wb = WR.xlsx_book(path, "BACS payment calendar", PR.PEOPLE["requester"], "Wealdmoor County Council", when)
    hd = wb.add_format({"bold": True, "bg_color": "#E2EFDA", "border": 1})
    n = 0
    for fy in ("2025/26", "2026/27", "2027/28"):
        a, b = PR.FY[fy]
        ws = wb.add_worksheet(fy.replace("/", "-"))
        rows = []
        for d in PR.creditor_runs(a, b):
            rows.append(("Creditors", d))
        for d in PR.sl_runs(a, b):
            rows.append(("Shared Lives carers", d))
        for (y, m) in PR.months(a, b):
            rows.append(("Direct payments", PR.dp_date(y, m)))
            rows.append(("Tenancy sustainment", PR.tsp_date(y, m)))
        rows.sort(key=lambda r: (r[1], r[0]))
        ws.write(0, 0, "Payment calendar %s: BACS payment dates and submission dates" % fy)
        for j, c in enumerate(["payment_type", "payment_date", "bacs_submission_date"]):
            ws.write(2, j, c, hd)
        for i, (t, d) in enumerate(rows):
            ws.write_string(3 + i, 0, t)
            ws.write_string(3 + i, 1, d.strftime("%d/%m/%Y"))
            ws.write_string(3 + i, 2, PR.wd_before(d, 2).strftime("%d/%m/%Y"))
        ws.set_column(0, 0, 22)
        ws.set_column(1, 2, 20)
        n += len(rows)
    WR.close_xlsx(wb, path, "Wealdmoor County Council", when)
    return n


INV_COLS = ["document_no", "document_type", "issue_date", "batch_ref", "description", "quantity", "unit_rate",
            "net_amount", "vat_amount", "related_document"]


def invoice_lines(path, rows):
    out = []
    for r in rows:
        r = dict(r)
        r["issue_date"] = dt.date.fromisoformat(r["issue_date"]).strftime("%d/%m/%Y")
        out.append(r)
    return WR.write_csv(path, out, INV_COLS)


def acknowledgements(path, acks, when):
    obj = {"provider": "Fernhollow Assurance Ltd", "customer": "Wealdmoor County Council",
           "framework_lot": "Lot 2 post-payment examination", "exported_at": when.strftime("%Y-%m-%dT%H:%M:%S"),
           "batches": [{k: v for k, v in a.items() if not k.startswith("_")} for a in acks]}
    WR.write_json(path, obj)
    return len(acks)


def rate_cards(path, when):
    wb = WR.xlsx_book(path, "Rate cards", PR.PEOPLE["provider"], "Fernhollow Assurance Ltd", when)
    hd = wb.add_format({"bold": True, "border": 1})
    for name, base, prem, frm, to, signed in (
            ("2025-26", PR.BASE_2526, PR.PREM_2526, "01/04/2025", "31/03/2026", "Countersigned 11/03/2025"),
            ("2026-27", PR.BASE_2627, PR.PREM_2627, "01/04/2026", "31/03/2027", "Delivered 17/02/2026")):
        ws = wb.add_worksheet(name)
        ws.write(0, 0, "Fernhollow Assurance Ltd: Payment Assurance Services Framework, Lot 2", hd)
        ws.write(1, 0, "Rate card %s, Wealdmoor County Council" % name.replace("-", "/"))
        rows = [("Effective from", frm), ("Effective to", to),
                ("Base rate per examination (GBP, excl. VAT)", base),
                ("Premium rate per examination (GBP, excl. VAT)", prem), ("Status", signed)]
        for i, (k, v) in enumerate(rows):
            ws.write_string(3 + i, 0, k)
            if isinstance(v, float):
                ws.write_number(3 + i, 1, v)
            else:
                ws.write_string(3 + i, 1, v)
        ws.set_column(0, 0, 48)
        ws.set_column(1, 1, 22)
    WR.close_xlsx(wb, path, "Fernhollow Assurance Ltd", when)
    return 2


def hsf_allocations(path, when):
    """Household Support Fund 2026/27: allocations by strand and district (voucher and grant strands)."""
    wb = WR.xlsx_book(path, "Household Support Fund 2026/27", PR.PEOPLE["hs"], "Wealdmoor County Council", when)
    hd = wb.add_format({"bold": True, "bg_color": "#FCE4D6", "border": 1})
    ws = wb.add_worksheet("Allocations")
    ws.write(0, 0, "Household Support Fund 2026/27: allocation by strand and district (Housing Support)")
    cols = ["district", "strand", "delivery_route", "allocation_gbp", "expected_awards", "typical_award_gbp"]
    for j, c in enumerate(cols):
        ws.write(2, j, c, hd)
    districts = ["Brendmere", "Coldbrook Vale", "Ferrowstead", "Lower Wealdmoor", "Orlwold", "Yeldthorpe"]
    strands = [("Food vouchers (school holidays)", "Supermarket e-voucher", 40, 15),
               ("Energy and water", "Supplier credit", 160, 3),
               ("Essential household items", "Grant via district council", 300, 2),
               ("Crisis support", "Grant via advice partner", 250, 2)]
    i = 0
    for k, dname in enumerate(districts):
        for s, route, typ, mult in strands:
            alloc = (38000 + 7300 * ((k * 5 + len(s)) % 7)) * mult // 3
            ws.write_string(3 + i, 0, dname)
            ws.write_string(3 + i, 1, s)
            ws.write_string(3 + i, 2, route)
            ws.write_number(3 + i, 3, alloc)
            ws.write_number(3 + i, 4, alloc // typ)
            ws.write_number(3 + i, 5, typ)
            i += 1
    ws.write(4 + i, 0, "Awards are made under the DWP grant conditions for 2026/27 and are paid by the "
                       "delivery partners from the grant.")
    ws.set_column(0, 2, 30)
    ws.set_column(3, 5, 16)
    WR.close_xlsx(wb, path, "Wealdmoor County Council", when)
    return i
