"""The two files the solution never reads: the communicable disease team's foodborne illness investigations and the
2026 annual permit fee invoices."""
import datetime as dt
import os

import openpyxl

import pack as P
import postprocess as PP
import world as W


def write_illness(R, target):
    r = W.rng("illness")
    rows = []
    n = 0
    for inc in R["incidents"]:
        if inc["cat"] != "Illness" or inc["times"][0].date() < W.RECORD or r.random() > 0.22:
            continue
        pm = R["permits"][inc["permit"]]
        opened = inc["times"][0].date() + dt.timedelta(days=int(r.integers(0, 3)))
        cases = int(r.choice([2, 2, 3, 3, 4, 5, 6, 8, 11, 14]))
        path = str(r.choice(["Norovirus", "Norovirus", "Salmonella", "Campylobacter", "Not identified",
                             "Not identified", "Clostridium perfringens"]))
        out = str(r.choice(["Closed, no common source found", "Food worker exclusion", "Closed, common meal identified",
                            "Referred to state epidemiologist"]))
        n += 1
        rows.append(["FBI-%d-%03d" % (opened.year, n), opened, pm["name"], pm["new"], cases, path, out,
                     opened + dt.timedelta(days=int(r.integers(9, 60)))])
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Investigations"
    P._sheet(ws, ["Investigation", "Opened", "Establishment", "Permit", "Reported ill", "Pathogen", "Outcome",
                  "Closed"], rows, [14, 12, 34, 12, 12, 24, 34, 12])
    for col in ("B", "H"):
        for cell in ws[col][1:]:
            cell.number_format = "mm/dd/yyyy"
    p = os.path.join(target, P.FILES["illness"])
    wb.save(p)
    PP.normalize_xlsx(p, "Juan Dalton", "2027-01-05T21:30:00Z", "2027-01-06T00:12:00Z", company=W.COUNTY)
    return len(rows)


FEE_BY_RISK = {1: 295, 2: 520, 3: 745}


def write_invoices(R, target):
    r = W.rng("invoices")
    prem = {p["pid"]: p for p in R["premises"]}
    rows = []
    k = 61203
    for pm in sorted(R["permits"], key=lambda x: x["new"] or "~"):
        if not pm["new"] or pm["start"] > dt.date(2025, 11, 1) or (pm["end"] and pm["end"] < dt.date(2026, 1, 1)):
            continue
        p = prem[pm["prem"]]
        amt = FEE_BY_RISK[p["risk"]] / (2 if p["seasonal"] else 1)
        k += 1 + (1 if r.random() < 0.02 else 0)
        issued = dt.date(2025, 11, 3) + dt.timedelta(days=int(r.integers(0, 4)))
        paid_day = None if r.random() < 0.03 else issued + dt.timedelta(days=int(r.integers(5, 95)))
        late = 75 if paid_day and paid_day > dt.date(2026, 2, 1) else 0
        rows.append(["PF26-%05d" % k, pm["new"], pm["name"], p["risk"], "%.2f" % amt, issued.isoformat(),
                     "2026-01-31", paid_day.isoformat() if paid_day else "", "%.2f" % late])
    P._w(os.path.join(target, P.FILES["invoices"]),
         ["invoice_no", "permit_id", "establishment", "risk_category", "permit_fee_usd", "issued_on", "due_on",
          "paid_on", "late_fee_usd"], rows)
    return len(rows)
