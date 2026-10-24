"""Writers for the pack's data files (the documents are in docs.py)."""
import csv
import datetime as dt
import io
import json
import os

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

import world as W
import records as R

EPOCH = dt.datetime(2026, 12, 31, 18, 0, 0)


def d8(d):
    return d.strftime("%Y%m%d") if d else " " * 8


def iso(d):
    return d.isoformat() if d else ""


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def extract_txt(path, rows):
    lines = ["H01WENDLEGLEN HOSPICE & PALLIATIVE CARE     HOSPICE BENEFIT PERIODS   RUN 20270105  DATA THRU 20261231"]
    for r in rows:
        lines.append("D%s%03d%s%s%s%s%04d%s   " % (r["mbi"], r["bp"], d8(r["elect"]), r["ccn"], d8(r["start"]),
                                                d8(r["end"]), r["days"], d8(r["dod"])))
    lines.append("T%09d" % (len(lines) - 1))
    with open(path, "w", encoding="ascii", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")


def emr_csv(path, rows):
    header = ["episode_id", "mrn", "medicare_id", "provider_number", "program", "admission_type", "admit_date",
              "discharge_date", "discharge_reason", "primary_dx", "birth_date", "sex", "payer"]
    out = [[r["episode_id"], r["mrn"], r["medicare_id"], r["provider_number"], r["program"], r["admission_type"],
            iso(r["admit_date"]), iso(r["discharge_date"]), r["discharge_reason"], r["primary_dx"], iso(r["birth_date"]),
            r["sex"], r["payer"]] for r in rows]
    write_csv(path, header, out)


def legacy_xlsx(path, rows):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Census Export"
    ws["A1"] = "FALLOWMERE HOSPICE INC  -  ADMISSION/DISCHARGE REGISTER"
    ws["A2"] = "Report run 02/28/2025 23:41   Medicare   Admissions active on or after 10/01/2016"
    ws["A1"].font = Font(bold=True)
    hdr = ["Pt Acct No", "Medicare No", "DOB", "Sex", "Admit Dt", "Disch Dt", "Disch Status", "Prim Dx", "Payer"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True)
    for i, r in enumerate(rows, 5):
        vals = [r["acct"], r["medicare_no"], r["dob"], r["sex"], r["admit"], r["disch"], r["status"], r["dx"], r["payer"]]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=i, column=j, value=v)
            if isinstance(v, dt.date):
                c.number_format = "mm/dd/yyyy"
    for j, wdt in enumerate([12, 14, 11, 5, 11, 11, 12, 9, 7], 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    wb.properties.creator = "FHI Census"
    wb.properties.lastModifiedBy = "FHI Census"
    wb.properties.created = dt.datetime(2025, 2, 28, 23, 41)
    wb.properties.modified = dt.datetime(2025, 2, 28, 23, 41)
    wb.save(path)


def crosswalk_csv(path, rows):
    write_csv(path, ["hicn", "mbi"], [[r["hicn"], r["mbi"]] for r in rows])


def dx_csv(path, rows):
    write_csv(path, ["icd10_code", "description", "census_group"], [[r["code"], r["description"], r["group"]] for r in rows])


def runs(days, lv):
    """(first day, days) of each run of consecutive days at one level of care: a level-of-care line on the claim."""
    out, start, n = [], None, 0
    for d, x, hi, q in days:
        if x == lv:
            if start is None:
                start, n = d, 0
            n += 1
        elif start is not None:
            out.append((start, n))
            start = None
    if start is not None:
        out.append((start, n))
    return out


def claim_lines_csv(path, claims):
    header = ["claim_key", "prior_claim_key", "type_of_bill", "provider_number", "mbi", "statement_from",
              "statement_through", "revenue_code", "hcpcs", "line_date", "units", "line_charge", "submitted_on",
              "clearinghouse_status"]
    out = []
    for c in sorted(claims, key=lambda c: (c["submitted"], c["key"])):
        base = [c["key"], c["prior"] or "", R.tob(c), R.CCN[c["code"]], c["mbi"], iso(c["frm"]), iso(c["thru"])]
        tail = [iso(c["submitted"]), "Accepted"]
        lines = []
        for rev, lv, hcpcs in (("0651", "R", c["loc"]), ("0655", "I", "Q5004"), ("0656", "G", c["gip_loc"])):
            for first, n in runs(c["days"], lv):
                lines.append((rev, first, [rev, hcpcs, iso(W.date_of(first)), n, "%.2f" % (n * R.CHARGE[rev])]))
        for d, x, hi, q in c["days"]:
            if x == "C":
                lines.append(("0652", d, ["0652", c["loc"], iso(W.date_of(d)), q, "%.2f" % (q * R.CHARGE["0652"])]))
        for rev, first, ln in sorted(lines, key=lambda t: (t[0], t[1])):
            out.append(base + ln + tail)
    write_csv(path, header, out)
    return len(out)


def remittance_csv(path, rows):
    header = ["remit_date", "record_type", "icn", "patient_control_no", "provider_number", "mbi", "statement_from",
              "statement_through", "type_of_bill", "claim_status", "paid_amount", "adj_carc_253", "plb_reason", "plb_amount"]
    out = []
    for r in sorted(rows, key=lambda r: (r["remit_date"], r["provider_number"], r["record"], r["patient_control_no"])):
        if r["record"] == "CLP":
            out.append([iso(r["remit_date"]), "CLP", r["icn"], r["patient_control_no"], r["provider_number"], r["mbi"],
                        iso(r["stmt_from"]), iso(r["stmt_thru"]), r["tob"], r["claim_status"], "%.2f" % r["paid"],
                        "%.2f" % r["sequestration"], "", ""])
        else:
            out.append([iso(r["remit_date"]), "PLB", r["icn"], r["patient_control_no"], r["provider_number"], "",
                        "", "", "", "", "", "", "L6", "%.2f" % r["paid"]])
    write_csv(path, header, out)
    return len(out)


def npi(base9):
    """A ten-digit NPI: nine digits and the Luhn check digit computed with the 80840 prefix."""
    digits = [int(c) for c in "80840" + base9]
    total = 0
    for k, d in enumerate(reversed(digits)):
        if k % 2 == 0:
            d *= 2
            d = d - 9 if d > 9 else d
        total += d
    return base9 + str((10 - total % 10) % 10)


def register_json(path, wi):
    progs = []
    for code in W.CODES:
        progs.append({"provider_number": R.CCN[code], "program": R.PROGRAM[code],
                      "fy2026_wage_index_applied": wi[code],
                      "owned_since": "2025-03-01" if code == "FAL" else "1998-07-01" if code in ("BRK", "COR") else "2004-01-01",
                      "notes": ("Change of ownership 1 March 2025; provider agreement assigned to Wendleglen, records before "
                                "that date held in the seller's census system" if code == "FAL" else "")})
    doc = {"organisation": "Wendleglen Hospice & Palliative Care", "as_of": "2026-12-31", "provider_numbers": progs}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2)
