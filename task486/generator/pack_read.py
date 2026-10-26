"""The cut pack read back into plain rows, as a solver would read it: the two PAYE extracts in their own layouts, the
two list extracts, the six districts' accounts with their property references resolved to UARNs through the lists,
the companies register and the centre schedule."""
import csv
import datetime as dt
import json
import os
import re

import openpyxl

MON = {m: i + 1 for i, m in enumerate(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])}
BA_DISTRICT = {"5110": "RKG", "5120": "DOR", "5130": "GLN", "5140": "ING", "5150": "NSH", "5160": "SKL"}
SHEET_DISTRICT = {"Rookgate": "RKG", "Dorrstead": "DOR", "Glenskarn": "GLN", "Ingmouth": "ING", "Neshdale": "NSH",
                  "Skelrigg": "SKL"}


def date(v):
    if v is None or v == "":
        return None
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    s = str(v).strip()
    m = re.fullmatch(r"(\d{2})/(\d{2})/(\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.fullmatch(r"(\d{2})-([A-Z][a-z]{2})-(\d{4})", s)
    if m:
        return dt.date(int(m.group(3)), MON[m.group(2)], int(m.group(1)))
    raise ValueError(s)


def paye(target):
    out = {"22": [], "26": []}
    with open(os.path.join(target, "paye_returns_m12_2021-22.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out["22"].append(dict(ref=r["scheme_ref"], name=r["employer_name"], trading="", crn=r["company_no"],
                                  sic=r["sic2007"], pc=r["scheme_postcode"], n=int(r["employees_paid"])))
    with open(os.path.join(target, "paye_returns_m12_2025-26.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out["26"].append(dict(ref="%s/%s" % (r["tax_office"], r["employer_ref"]), name=r["employer_name"],
                                  trading=r["trading_name"], crn=r["crn"], sic=r["sic_2007"], pc=r["paye_postcode"],
                                  n=int(r["paid_employees"])))
    return out


def lists(target):
    out = {"17": [], "23": []}
    with open(os.path.join(target, "rating_list_2017_extract_20220404.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out["17"].append(dict(uarn=int(r["UARN"]), district=BA_DISTRICT[r["BA_CODE"]], baref=r["BA_REFERENCE"],
                                  pc=r["POSTCODE"], d=r["DESCRIPTION_CODE"], a=float(r["TOTAL_AREA"]),
                                  basis=r["AREA_BASIS"], rv=int(r["RATEABLE_VALUE"]), frm=date(r["EFFECTIVE_DATE"]),
                                  to=date(r["EFFECTIVE_TO"])))
    with open(os.path.join(target, "rating_list_2023_extract_20260413.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out["23"].append(dict(uarn=int(r["uarn"]), district=BA_DISTRICT[r["billing_authority"]], baref=r["ba_ref"],
                                  pc=r["postcode"], d=r["primary_desc_code"], a=float(r["floor_area_m2"]),
                                  basis=r["measurement_basis"], rv=int(r["rateable_value"]), frm=date(r["effective_from"]),
                                  to=date(r["effective_to"])))
    return out


def in_force(entries, day):
    """uarn -> the entry in force on the day"""
    out = {}
    for e in entries:
        if e["frm"] <= day and (e["to"] is None or e["to"] >= day):
            out[e["uarn"]] = e
    return out


def accounts(target, L):
    baref = {}
    for k in ("17", "23"):
        for e in L[k]:
            baref[(e["district"], e["baref"])] = e["uarn"]
    wb = openpyxl.load_workbook(os.path.join(target, "business_rates_accounts_2017-2026.xlsx"), read_only=True)
    out = []
    for sheet, d in SHEET_DISTRICT.items():
        ws = wb[sheet]
        rows = ws.iter_rows(values_only=True)
        head = list(next(rows))
        for r in rows:
            if r[0] is None:
                continue
            x = dict(zip(head, r))
            if d == "RKG":
                acc = dict(acct=x["Account Number"], uarn=int(x["UARN"]), name=x["Liable Party"], crn=x["Company Number"] or "",
                           frm=date(x["Liability Start"]), to=date(x["Liability End"]), status=None, relief=x["Relief"] or "")
            elif d == "GLN":
                acc = dict(acct=x["Acct"], uarn=baref[(d, x["Property Reference"])], name=x["Ratepayer"], crn=x["Co. Reg. No."] or "",
                           frm=date(x["From"]), to=date(x["To"]), status=None, relief=x["Reliefs"] or "")
            elif d == "DOR":
                acc = dict(acct=x["Account No"], uarn=baref[(d, x["Prop Ref"])], name=x["Ratepayer Name"], crn="",
                           frm=date(x["Start Date"]), to=date(x["End Date"]), status=None, relief=x["Relief Code"] or "")
            elif d == "ING":
                acc = dict(acct=x["account_ref"], uarn=int(x["uarn"]), name=x["ratepayer"], crn=x["company_no"] or "",
                           frm=date(x["liable_from"]), to=date(x["liable_to"]), status=None, relief=x["relief"] or "")
            elif d == "NSH":
                acc = dict(acct=x["Account"], uarn=baref[(d, x["Property"])], name=x["Name"], crn="",
                           frm=date(x["Liability Start"]), to=date(x["Liability End"]), status=None, relief=x["Relief Type"] or "")
            else:
                acc = dict(acct=x["AccountId"], uarn=int(x["UARN"]), name=x["RatepayerName"], crn=x["CompanyRegNo"] or "",
                           frm=date(x["StartDate"]), to=date(x["EndDate"]), status=None, relief=x["ReliefCode"] or "")
            acc["district"] = d
            out.append(acc)
    return out


def companies(target):
    out = {}
    with open(os.path.join(target, "companies_register_extract_20260501.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            prev = [re.sub(r"\s*\(TO \d{2}/\d{2}/\d{4}\)$", "", p.strip()) for p in r["previous_names"].split(";") if p.strip()]
            out[r["company_number"]] = dict(name=r["company_name"], prev=prev, status=r["company_status"],
                                            sic=r["sic_codes"].split(";"), psc=r["psc_corporate"])
    return out


def schedule(target):
    pcs, centres = {}, {}
    with open(os.path.join(target, "town_centre_schedule_2026.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            pcs[r["postcode"]] = r["centre_code"]
            centres[r["centre_code"]] = (r["centre_name"], r["district"])
    return pcs, dict(sorted(centres.items()))


def read(target):
    L = lists(target)
    pcs, centres = schedule(target)
    return dict(paye=paye(target), lists=L, accounts=accounts(target, L), companies=companies(target), pcs=pcs,
                centres=centres)
