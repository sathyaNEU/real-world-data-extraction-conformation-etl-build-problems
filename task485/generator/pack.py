"""The pack's data files, each written the way the system that produces it writes it: the PBM's fiscal 2026 paid
claims extract, its drug file, its pharmacy network file, the plan's member roster from the new eligibility system,
and the PBM's quarterly rebate remittance statements."""
import csv
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import world as W

OLD_FORMAT_UNTIL = W.RENUMBER   # the claim platform's export changed on 1 January 2026


def _ndc_plain(ndc):
    return ndc.replace("-", "")


def _d(d, old):
    return d.strftime("%m/%d/%Y") if old else d.isoformat()


def claims_csv(path, w):
    """One row per adjudication: a paid row for every claim and, for a reversed claim, a reversal row carrying the
    original's claim number. Rows for service before 1 January 2026 carry the old group codes, cardholder numbers,
    person codes, hyphenated NDCs and US dates; later rows the new ones."""
    acc_old = {a[0]: a[1] for a in W.ACCOUNTS}
    acc_new = {a[0]: a[2] for a in W.ACCOUNTS}
    rows = []
    for c in w.claims:
        p = w.products[c["key"]]
        old = c["d"] < OLD_FORMAT_UNTIL
        person = c["person"]
        base = dict(rx_number="%07d" % c["rx"], fill_number=c["fill"], date_of_service=_d(c["d"], old),
                    group_id=acc_old[c["acc"]] if old else acc_new[c["acc"]],
                    cardholder_id=person["old_card"] if old else person["new_card"],
                    person_code=person["old_pc"] if old else person["new_pc"],
                    patient_dob=_d(person["dob"], old), patient_gender=person["sex"], pharmacy_npi=c["ph"]["npi"],
                    ndc=p["ndc"] if old else _ndc_plain(p["ndc"]),
                    product_name=claim_name(p),
                    days_supply=c["ds"], daw_code="0" if p["cls"] != "OTH" else ("1" if c["no"] % 23 == 0 else "0"),
                    compound_code="2" if c.get("compound") else "1")
        rows.append((c["paid"], c["no"], dict(base, claim_number=str(c["no"]), claim_status="P", reversal_of="",
                                              date_paid=_d(c["paid"], c["paid"] < OLD_FORMAT_UNTIL),
                                              quantity_dispensed=_q(c["qty"]), ingredient_cost_paid="%.2f" % c["ingr"],
                                              dispensing_fee_paid="%.2f" % c["fee"], patient_pay_amount="%.2f" % c["pay"],
                                              plan_paid_amount="%.2f" % c["plan"])))
        if c["rev"]:
            rows.append((c["rev"], c["rev_no"], dict(base, claim_number=str(c["rev_no"]), claim_status="R",
                                                     reversal_of=str(c["no"]),
                                                     date_paid=_d(c["rev"], c["rev"] < OLD_FORMAT_UNTIL),
                                                     quantity_dispensed=_q(-c["qty"]),
                                                     ingredient_cost_paid="%.2f" % -c["ingr"],
                                                     dispensing_fee_paid="%.2f" % -c["fee"],
                                                     patient_pay_amount="%.2f" % -c["pay"],
                                                     plan_paid_amount="%.2f" % -c["plan"])))
    rows.sort(key=lambda r: (r[0], r[1]))
    cols = ["claim_number", "claim_status", "reversal_of", "rx_number", "fill_number", "date_of_service", "date_paid",
            "group_id", "cardholder_id", "person_code", "patient_dob", "patient_gender", "pharmacy_npi", "ndc",
            "product_name", "quantity_dispensed", "days_supply", "daw_code", "compound_code", "ingredient_cost_paid",
            "dispensing_fee_paid", "patient_pay_amount", "plan_paid_amount"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(cols)
        for _, _, r in rows:
            wr.writerow([r[k] for k in cols])
    return len(rows)


def _q(x):
    s = ("%.3f" % x).rstrip("0").rstrip(".")
    return s


def claim_name(p):
    """The product name as the claim carries it: the proprietary name and the strength and form, upper case."""
    import re
    m = re.search(r"\d", p["inn"])
    strength = p["inn"][m.start():] if m else ""
    return ("%s %s" % (p["brand"], strength)).upper().replace("  ", " ")[:44]


def drug_file(path, w):
    """The PBM's drug file for the products the plan's members filled, one row per NDC, as the PBM's portal exports it
    (the class names are the PBM's own therapeutic classification)."""
    pbm_class = {"GLP1": "ANTIDIABETICS - GLP-1 RECEPTOR AGONISTS", "SGLT2": "ANTIDIABETICS - SGLT2 INHIBITORS",
                 "BASAL": "INSULINS - LONG ACTING", "DOAC": "ANTICOAGULANTS - FACTOR XA INHIBITORS",
                 "ICS": "ANTIASTHMATICS - CORTICOSTEROID/LABA COMBINATIONS", "ADA": "IMMUNOMODULATORS - TNF INHIBITORS",
                 "ONC": "ANTINEOPLASTICS - KINASE INHIBITORS", "MS": "MULTIPLE SCLEROSIS AGENTS",
                 "HIV": "ANTIRETROVIRALS - COMBINATIONS", "HCV": "HEPATITIS C AGENTS", "MIG": "MIGRAINE - CGRP ANTAGONISTS",
                 "PSO": "IMMUNOMODULATORS - INTERLEUKIN INHIBITORS", "AST": "ANTIASTHMATICS - MONOCLONAL ANTIBODIES",
                 "OTH": None}
    oth_class = {"OTH_01": "ADHD AGENTS - AMPHETAMINES", "OTH_02": "CONTRACEPTIVES - COMBINATIONS",
                 "OTH_03": "OPHTHALMIC - GLAUCOMA AGENTS", "OTH_04": "ANAPHYLAXIS - EPINEPHRINE",
                 "OTH_05": "ANTIHYPERLIPIDEMICS - COMBINATIONS", "OTH_06": "DERMATOLOGICS - PDE4 INHIBITORS",
                 "OTH_07": "ULCER DRUGS - PROTON PUMP INHIBITORS", "OTH_08": "MIGRAINE - CGRP ANTAGONISTS",
                 "OTH_09": "THYROID AGENTS", "OTH_10": "OPHTHALMIC - GLAUCOMA AGENTS",
                 "OTH_11": "ANTIASTHMATICS - LEUKOTRIENE MODIFIERS", "OTH_12": "MIGRAINE - SELECTIVE SEROTONIN AGONISTS"}
    wb = Workbook()
    ws = wb.active
    ws.title = "Drug File"
    hdr = ["NDC", "Labeler Code", "Labeler Name", "Proprietary Name", "Nonproprietary Name and Strength",
           "Package Description", "Package Quantity", "Unit of Measure", "Multi-Source Code", "Specialty Indicator",
           "Therapeutic Class", "Effective Date"]
    ws.append(hdr)
    eff = {"GLP_A": dt.date(2021, 4, 1), "INS_C": dt.date(2022, 11, 1), "ADA_B": dt.date(2023, 7, 1),
           "ADA_C": dt.date(2023, 7, 1)}
    for key in sorted(w.products, key=lambda k: w.products[k]["ndc"]):
        p = w.products[key]
        m = w.mfr[p["mfr"]]
        cls = pbm_class[p["cls"]] or oth_class[key]
        ws.append([_ndc_plain(p["ndc"]), m["labeler"], m["name"], p["brand"], p["inn"], p["pkg"],
                   p["units"], p["uom"], "N", "Y" if p["prof"] == "S" else "N", cls,
                   eff.get(key, dt.date(2019, 1, 1))])
    for i, wd in enumerate([13, 12, 32, 22, 52, 28, 16, 15, 17, 18, 48, 14], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in ws.iter_rows(min_row=2, min_col=12, max_col=12):
        for cell in row:
            cell.number_format = "mm/dd/yyyy"
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:L%d" % ws.max_row
    wb.save(path)
    return ws.max_row - 1


def pharmacy_network(path, w):
    """The PBM's pharmacy network file as of October 2026, pipe-delimited, one row per pharmacy and its current
    network."""
    rng = np.random.default_rng(W.SEED + 31)
    cities = ["Ashford", "Brookline", "Cedar Falls", "Danbury", "Elmwood", "Fairview", "Glenville", "Harrison",
              "Lakewood", "Milford", "Newport", "Oakdale", "Riverton", "Salem", "Troy", "Westfield"]
    lines = ["NPI|NCPDP_ID|PHARMACY_NAME|CITY|NETWORK|CHAIN_CODE|STATUS"]
    for k, ph in enumerate(w.pharmacies):
        ncpdp = "%07d" % int(rng.integers(1000000, 9999999))
        chain = ph["name"].split(" #")[0] if " #" in ph["name"] else ""
        code = {"Walgreens": "226", "CVS Pharmacy": "039", "Kroger Pharmacy": "108", "Walmart Pharmacy": "229",
                "Rite Aid": "181", "Costco Pharmacy": "253", "Publix Pharmacy": "302", "Meijer Pharmacy": "113"}.get(chain, "")
        city = cities[int(rng.integers(0, len(cities)))]
        lines.append("|".join([ph["npi"], ncpdp, ph["name"].upper(), city.upper(), ph["channel"], code, "ACTIVE"]))
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(lines) + "\r\n")
    return len(lines) - 1


def member_roster(path, w):
    """The new eligibility system's roster at 9 October 2026: every member covered on or after 1 January 2026 under
    the new cardholder numbers and person codes; the subscriber's row carries the cardholder number the old system
    used."""
    acc_new = {a[0]: a[2] for a in W.ACCOUNTS}
    rows = []
    for p in w.persons:
        if p["term"] and p["term"] < W.RENUMBER:
            continue
        eff = max(p["start"], dt.date(2026, 1, 1)) if p["start"] >= W.RENUMBER else dt.date(2026, 1, 1)
        rows.append([p["new_card"] + p["new_pc"], p["new_card"], p["new_pc"], p["rel"], p["dob"].isoformat(), p["sex"],
                     acc_new[p["acc"]], eff.isoformat(), "",
                     p["old_card"] if (p["rel"] == "E" and p["start"] < W.RENUMBER) else ""])
    rows.sort(key=lambda r: (r[6], r[1], r[2]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["member_id", "cardholder_id", "person_code", "relationship_code", "birth_date", "gender",
                     "group_id", "coverage_effective", "coverage_termination", "legacy_cardholder_id"])
        wr.writerows(rows)
    return len(rows)


PERIOD = {"2025Q1": ("January 1, 2025", "March 31, 2025", "Jan-Mar 2025"),
          "2025Q2": ("April 1, 2025", "June 30, 2025", "Apr-Jun 2025"),
          "2025Q3": ("July 1, 2025", "September 30, 2025", "Jul-Sep 2025"),
          "2025Q4": ("October 1, 2025", "December 31, 2025", "Oct-Dec 2025"),
          "2026Q1": ("January 1, 2026", "March 31, 2026", "Jan-Mar 2026"),
          "2026Q2": ("April 1, 2026", "June 30, 2026", "Apr-Jun 2026")}


def remittance(path, w, q):
    """One quarter's rebate remittance statement: each manufacturer's rebates by plan account, current-quarter lines
    for the quarter's claims and prior-period adjustment lines for earlier quarters' claims."""
    acc_name = {a[0]: a[3] for a in W.ACCOUNTS}
    new = q >= "2026Q1"
    acc_code = {a[0]: (a[2] if new else a[1]) for a in W.ACCOUNTS}
    lines = [l for l in w.statements if l["stmt"] == q]
    mfr_order = sorted(w.mfr, key=lambda m: w.mfr[m]["stmt"])
    wb = Workbook()
    ws = wb.active
    ws.title = "Remittance"
    a, b, _ = PERIOD[q]
    ws.append([W.PBM])
    ws.append(["Manufacturer Rebate Remittance Statement"])
    ws.append(["Client: %s, %s" % (W.OFFICE, W.PLAN)])
    ws.append(["Invoice period: %s - %s" % (a, b)])
    ws.append(["Remittance date: %s" % W.REMITTED[q].strftime("%B %d, %Y").replace(" 0", " ")])
    ws.append([])
    hdr = ["Manufacturer", "Account", "Account Name", "Line Type", "Service Period", "Rebate Amount (USD)"]
    ws.append(hdr)
    hrow = ws.max_row
    total = 0.0
    for m in mfr_order:
        ls = [l for l in lines if l["mfr"] == m]
        ls.sort(key=lambda l: (W.ACC.index(l["acc"]), 0 if l["kind"] == "CUR" else 1, l["svc"]))
        for l in ls:
            ws.append([w.mfr[m]["stmt"], acc_code[l["acc"]], acc_name[l["acc"]],
                       "Current Quarter" if l["kind"] == "CUR" else "Prior Period Adjustment", PERIOD[l["svc"]][2],
                       round(l["amount"], 2)])
            total += l["amount"]
    ws.append([])
    ws.append(["Total remitted", "", "", "", "", round(total, 2)])
    for cell in ws[hrow]:
        cell.font = Font(bold=True)
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"].font = Font(bold=True)
    for row in ws.iter_rows(min_row=hrow + 1, min_col=6, max_col=6):
        for cell in row:
            cell.number_format = "#,##0.00"
    for i, wd in enumerate([34, 10, 24, 25, 16, 20], 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A%d" % (hrow + 1)
    # the summary tab by manufacturer
    s2 = wb.create_sheet("Summary by Manufacturer")
    s2.append(["Manufacturer", "Current Quarter", "Prior Period Adjustments", "Total"])
    for cell in s2[1]:
        cell.font = Font(bold=True)
    for m in mfr_order:
        ls = [l for l in lines if l["mfr"] == m]
        if not ls:
            continue
        cur = sum(l["amount"] for l in ls if l["kind"] == "CUR")
        ppa = sum(l["amount"] for l in ls if l["kind"] != "CUR")
        s2.append([w.mfr[m]["stmt"], round(cur, 2), round(ppa, 2), round(cur + ppa, 2)])
    for row in s2.iter_rows(min_row=2, min_col=2, max_col=4):
        for cell in row:
            cell.number_format = "#,##0.00"
    for i, wd in enumerate([34, 18, 24, 18], 1):
        s2.column_dimensions[get_column_letter(i)].width = wd
    wb.save(path)
    return len(lines)
