"""task170 pack: every file the CMS quantification unit pulled on 2 September 2026, written from the records."""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter

import calc as K
import common as C
import docs as DOC
import ladder as LD
import postprocess as PP
import records as R
import world as WD
import world_log as WL

D = dt.date

F_LEG = "paed_register_visits_legacy_2023-01_2024-06.csv"
F_EPR = "paed_register_visits_epr_2024-06_2026-08.csv"
F_PTS = "paed_register_patients_2026-09-02.csv"
F_CW = "art_number_crosswalk_2024-06.csv"
F_PROJ = "art_patient_projection_2026-09_2027-06.xlsx"
F_STOCK = "cms_stock_status_2026-08-31.xlsx"
F_DEL = "cms_deliveries_tld_2025-07_2026-08.csv"
F_POD = "cms_pod_2025-07_2026-08.csv"
F_ACC = "cms_customer_accounts_2026-09-02.csv"
F_LMIS = "lmis_monthly_reports_2025-07_2026-08.json"
F_REG = "facility_registry_extract_2026-09-01.csv"
F_VL = "paed_viral_load_2025-07_2026-08.csv"
F_DICT = "data_dictionary.xlsx"
F_MAN = "extract_manifest_2026-09-02.csv"
F_CODES = "national_regimen_codes_2025.csv"
DISTRACTORS = [F_VL, DOC.F_EST]

HEAD_FILL = PatternFill("solid", fgColor="DCE6E0")
BOLD = Font(name="Calibri", bold=True, size=11)
BODY = Font(name="Calibri", size=11)


def _csv(path, head, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(head)
    for r in rows:
        w.writerow([r[h] for h in head] if isinstance(r, dict) else r)
    open(path, "w", encoding="utf-8", newline="").write(buf.getvalue())
    return len(rows)


def _sheet(ws, head, rows, widths=None, start_row=1, fmt=None):
    for j, h in enumerate(head):
        c = ws.cell(row=start_row, column=j + 1, value=h)
        c.font = BOLD
        c.fill = HEAD_FILL
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = ws.cell(row=start_row + 1 + i, column=j + 1, value=v)
            c.font = BODY
            if isinstance(v, D):
                c.number_format = "dd/mm/yyyy"
            elif fmt and j in fmt:
                c.number_format = fmt[j]
    for j, h in enumerate(head):
        ws.column_dimensions[get_column_letter(j + 1)].width = (widths[j] if widths else max(10, len(h) + 2))


def _save(wb, path, creator, last_by, created, modified):
    wb.save(path)
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=C.ORG)


# ---------------------------------------------------------------------------------------------------- world
def make_world():
    W = WD.simulate()
    rng = np.random.default_rng(C.SEED + 101)
    leg, epr, pts, cw, clean = R.register(W, rng)
    S = R.supply(W, rng)
    acc = R.accounts(S, rng)
    lines, pods = R.deliveries(S, rng)
    rep = R.lmis(S, rng)
    kids, visits = R.clean_view(W, clean)
    return dict(W=W, rng=rng, leg=leg, epr=epr, pts=pts, cw=cw, clean=clean, S=S, acc=acc, lines=lines, pods=pods,
                rep=rep, kids=kids, visits=visits)


def adult_need(proj):
    tot = [sum(proj[r][k] for r in C.REGIONS) for k in range(10)]
    return sum(tot) + C.MAX_MONTHS * tot[-1], tot


def place_order(Wd):
    """Fix the third confirmed lot of the C6 order so that the middle of the family's orders, its members and the
    two compound choices that push the need furthest up and down, sits at the centre of its 5,000-bottle step, a
    multiple of 5,000 (the lot stays a multiple of the 96-bottle carton)."""
    S = Wd["S"]
    fam, c = LD.family(Wd["kids"], Wd["visits"])
    an, _ = adult_need(S["proj"])
    soh = sum(b["qty"] for b in S["batches"] if b["status"] == "Usable")
    conf = [s for s in S["ship"] if s["status"] == "Confirmed"]
    lo, hi = LD.extreme_pairs(fam)
    v_lo = LD.compound(Wd["kids"], Wd["visits"], lo)
    v_hi = LD.compound(Wd["kids"], Wd["visits"], hi)
    span = [fam[k] for k in LD.FAMILY] + [v_lo, v_hi]
    mid = (min(span) + max(span)) / 2
    u = an + mid - soh - sum(s["qty"] for s in conf)
    target = C.LOT * np.round(u / C.LOT)
    lot3 = conf[-1]
    q = lot3["qty"] + (u - target)
    lot3["qty"] = int(round(q / 96.0)) * 96
    Wd["family"] = fam
    Wd["ctx"] = c
    return fam


# ---------------------------------------------------------------------------------------------------- register
def write_register(out, Wd):
    n = {}
    n[F_LEG] = _csv(os.path.join(out, F_LEG), ["record_no", "art_no", "facility_code", "visit_date", "visit_type",
                                                "weight_kg", "regimen", "months_dispensed", "next_visit"], Wd["leg"])
    n[F_EPR] = _csv(os.path.join(out, F_EPR), ["encounter_id", "upid", "facility_code", "visit_date", "encounter_type",
                                                "weight_kg", "regimen_code", "months_dispensed", "next_appointment",
                                                "synced_at"], Wd["epr"])
    n[F_PTS] = _csv(os.path.join(out, F_PTS), ["upid", "sex", "date_of_birth", "dob_estimated", "art_start_date",
                                                "current_facility", "outcome", "outcome_date", "outcome_entered"],
                    sorted(Wd["pts"], key=lambda r: r["upid"]))
    n[F_CW] = _csv(os.path.join(out, F_CW), ["art_no", "upid", "facility_code"], Wd["cw"])
    n[F_CODES] = _csv(os.path.join(out, F_CODES), ["regimen_code", "line", "regimen", "weight_band", "legacy_register_text"],
                      [list(r) for r in C.REGIMENS])
    return n


# ---------------------------------------------------------------------------------------------------- projection
def write_projection(out, S):
    wb = Workbook()
    ws = wb.active
    ws.title = "Projection"
    months = [D(2026, 9, 1)] + [D(2026 + (8 + k) // 12, (8 + k) % 12 + 1, 1) for k in range(1, 10)]
    head = ["Region"] + [m.strftime("%b %Y") for m in months]
    rows = [[r] + S["proj"][r] for r in C.REGIONS]
    rows.append(["National"] + [sum(S["proj"][r][k] for r in C.REGIONS) for k in range(10)])
    ws.cell(row=1, column=1, value="Patients on TLD at the end of each month: projection, September 2026 to June 2027").font = BOLD
    ws.cell(row=2, column=1, value="Patients aged 15 and over on 31 August 2026 and every patient starting treatment "
                                   "from 1 September 2026. Children aged under 15 on 31 August 2026 are not included.").font = BODY
    _sheet(ws, head, rows, [12] + [10] * 10, start_row=4, fmt={k: "#,##0" for k in range(1, 11)})
    ws.freeze_panes = "B5"
    ns = wb.create_sheet("Notes")
    notes = [["Prepared by", C.PEOPLE["me"] + ", monitoring officer, " + C.PROG],
             ["Base", "Patients on TLD at 31 August 2026 from the programme's monthly site returns"],
             ["Method", "Programme model: retention by region from the last four quarters' returns, new initiations "
                        "at the 2026 targets, regimen shares from the July 2026 returns"],
             ["Regions", "As drawn from 1 April 2026"],
             ["Version", "2026-09-01 (projection round of September 2026)"]]
    _sheet(ns, ["Item", "Note"], notes, [16, 110])
    _save(wb, os.path.join(out, F_PROJ), C.PEOPLE["me"], C.PEOPLE["me"], "2026-08-27T08:10:00Z", "2026-09-01T13:42:00Z")
    return 7


# ---------------------------------------------------------------------------------------------------- stock status
def monthly_issues(lines, kind="LF"):
    """Bottles by posting month: issued to facilities (LF, customer deliveries, not the depot's restocking) or
    returned by facilities (LR)."""
    out = {}
    for ln in lines:
        if ln["delivery_type"] != kind:
            continue
        d = D.fromisoformat(ln["posting_date"])
        out[(d.year, d.month)] = out.get((d.year, d.month), 0) + ln["qty"]
    return out


def write_stock(out, S, lines, rng):
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    iss = monthly_issues(lines)
    last6 = [(2026, m) for m in range(3, 9)]
    amc = sum(iss[k] for k in last6) / 6.0
    usable = sum(b["qty"] for b in S["batches"] if b["status"] == "Usable")
    ws.cell(row=1, column=1, value="Stock status at the count of 31 August 2026").font = BOLD
    ws.cell(row=2, column=1, value="Stock at the CMS warehouses at the count; months of stock on the average of the last "
                                   "six months' issues to facilities; stock held at facilities is not included.").font = BODY
    rows = [["ARV0412", "TDF/3TC/DTG 300/300/50 mg tablets, 30", "Bottle", usable,
             round(amc), round(usable / amc, 1)]]
    others = [("ARV0388", "ABC/3TC 600/300 mg tablets, 30"), ("ARV0391", "ABC/3TC 120/60 mg dispersible tablets, 60"),
              ("ARV0407", "DTG 10 mg dispersible tablets, 90"), ("ARV0365", "LPV/r 100/25 mg tablets, 60")]
    for code, desc in others:
        a = int(rng.integers(3000, 21000))
        s = int(a * float(rng.uniform(3.0, 7.5)))
        rows.append([code, desc, "Bottle", s, a, round(s / a, 1)])
    _sheet(ws, ["Product code", "Product", "Unit", "Usable stock", "Average monthly issues", "Months of stock"], rows,
           [13, 40, 8, 13, 22, 15], start_row=4, fmt={3: "#,##0", 4: "#,##0", 5: "0.0"})
    ws.cell(row=11, column=1, value="Version 2026-09-02. Prepared by %s, quantification lead." % C.PEOPLE["quant_lead"]).font = BODY
    w2 = wb.create_sheet("Stock on hand")
    rows = [[b["warehouse"], "ARV0412", b["batch"], b["expiry"], b["status"], b["qty"]]
            for b in sorted(S["batches"], key=lambda b: (b["warehouse"], b["expiry"], b["batch"]))]
    _sheet(w2, ["Warehouse", "Product code", "Batch", "Expiry", "Status", "Bottles"], rows, [17, 13, 12, 12, 13, 11],
           fmt={5: "#,##0"})
    w3 = wb.create_sheet("On order")
    rows = [[s["po"], s["lot"], "ARV0412", s["qty"], s["due"], s["status"]] for s in S["ship"]]
    _sheet(w3, ["Order", "Lot", "Product code", "Bottles", "Due", "Status"], rows, [15, 6, 13, 11, 12, 12],
           fmt={3: "#,##0"})
    w4 = wb.create_sheet("Movements")
    # closing stock month by month, back from the count: received lots (C5 order and C6 lot 0) and issues by posting
    recv = {k: 0 for k in last6}
    for k in ((2026, 3), (2026, 4), (2026, 6), (2026, 7)):
        recv[k] = int(rng.integers(3500, 4400)) * 96
    ret = monthly_issues(lines, "LR")
    closing = {}
    cur = usable + sum(b["qty"] for b in S["batches"] if b["status"] == "Quarantined")
    for (y, m) in reversed(last6):
        closing[(y, m)] = cur
        cur = cur - recv[(y, m)] - ret.get((y, m), 0) + iss[(y, m)]
    rows = [[D(y, m, 1).strftime("%b %Y"), recv[(y, m)], ret.get((y, m), 0), iss[(y, m)], closing[(y, m)]]
            for (y, m) in last6]
    _sheet(w4, ["Month", "Received from suppliers", "Returned by facilities", "Issued to facilities", "Closing stock"],
           rows, [11, 22, 21, 20, 15], fmt={1: "#,##0", 2: "#,##0", 3: "#,##0", 4: "#,##0"})
    w4.cell(row=9, column=1, value="TLD 30s, both warehouses. Issues by posting date; the depot's restocking from the Main "
                                   "warehouse is a transfer and is not an issue.").font = BODY
    _save(wb, os.path.join(out, F_STOCK), C.PEOPLE["quant_lead"], C.PEOPLE["quant_lead"], "2026-03-03T07:55:00Z",
          "2026-09-02T09:18:00Z")
    return 5


# ---------------------------------------------------------------------------------------------------- supply side
def write_supply(out, Wd):
    S = Wd["S"]
    n = {}
    acc_region = {a["account"]: a["delivery_region"] for a in Wd["acc"]}
    acc_name = {a["account"]: a["account_name"] for a in Wd["acc"]}
    acc_route = {a["account"]: a["route"] for a in Wd["acc"]}
    rows = []
    for ln in Wd["lines"]:
        r = dict(ln)
        r["ship_to_name"] = acc_name[ln["customer"]]
        r["delivery_region"] = acc_region[ln["customer"]]
        r["route"] = acc_route[ln["customer"]]
        r["material_description"] = R.TLD_DESC
        r["uom"] = "BOT"
        rows.append(r)
    rows.sort(key=lambda r: (r["posting_date"], r["delivery_no"], r["item"]))
    n[F_DEL] = _csv(os.path.join(out, F_DEL), ["delivery_no", "item", "plant", "delivery_type", "posting_date",
                                                "customer", "ship_to_name", "delivery_region", "route", "material",
                                                "material_description", "batch", "qty", "uom"], rows)
    n[F_POD] = _csv(os.path.join(out, F_POD), ["delivery_no", "customer", "signed_on", "signed_by", "vehicle"],
                    sorted(Wd["pods"], key=lambda r: r["delivery_no"]))
    n[F_ACC] = _csv(os.path.join(out, F_ACC), ["account", "account_name", "mfl_code", "delivery_region", "route",
                                                "opened_on", "status", "closed_on"], Wd["acc"])
    # LMIS: requisitions with their line items
    reqs = {}
    for r in Wd["rep"]:
        k = r["report_id"]
        if k not in reqs:
            reqs[k] = dict(id=k, facilityCode=r["facility_code"], period=r["period"], region=r["region"],
                           status=r["status"], submittedAt=r["submitted_at"], reviewedOn=r["reviewed_on"] or None,
                           lineItems=[])
        reqs[k]["lineItems"].append(dict(productCode=r["product_code"], product=r["product"],
                                         beginningBalance=r["opening_balance"], quantityReceived=r["received"],
                                         quantityDispensed=r["dispensed"],
                                         totalLossesAndAdjustments=r["losses_adjustments"],
                                         stockOnHand=r["closing_balance"], stockoutDays=r["stockout_days"]))
    doc = dict(source="eLMIS national instance", program="ART", exportedAt="2026-09-02T06:40:00+02:00",
               requisitions=sorted(reqs.values(), key=lambda q: (q["period"], q["facilityCode"], q["submittedAt"])))
    open(os.path.join(out, F_LMIS), "w", encoding="utf-8").write(json.dumps(doc, indent=1, ensure_ascii=False))
    n[F_LMIS] = len(reqs)
    rows = []
    for rec in sorted(S["recs"], key=lambda r: (r["mfl"], r["opened"])):
        rows.append(dict(mfl_code=rec["mfl"], facility_type=rec["type"],
                         ownership={"Mission hospital": "Faith-based", "Private clinic": "Private"}.get(rec["type"], "Government"),
                         district=[d[1] for d in C.DISTRICTS if d[0] == rec["district"]][0], region=rec["region"],
                         region_since="2026-04-01" if rec["region"] != rec["region_old"] else "2014-07-01",
                         status="Closed" if rec["closed"] else "Operational", opened_on=rec["opened"].isoformat(),
                         closed_on=rec["closed"].isoformat() if rec["closed"] else ""))
    n[F_REG] = _csv(os.path.join(out, F_REG), ["mfl_code", "facility_type", "ownership", "district", "region",
                                                "region_since", "status", "opened_on", "closed_on"], rows)
    return n


# ---------------------------------------------------------------------------------------------------- distractors
def write_vl(out, Wd, rng):
    """Viral load results for children and adolescents in the register (unused by the order)."""
    rows = []
    pts = {p["upid"]: p for p in Wd["pts"]}
    epr = [r for r in Wd["epr"] if r["encounter_type"] == "Clinical visit"]
    for r in epr[::9]:
        if rng.random() < 0.55:
            continue
        d = D.fromisoformat(r["visit_date"])
        if d < D(2025, 7, 1):
            continue
        u = rng.random()
        res = "<50" if u < 0.71 else ("TND" if u < 0.78 else str(int(np.exp(rng.uniform(np.log(60), np.log(250000))))))
        rows.append(dict(upid=r["upid"], facility_code=r["facility_code"], sample_date=d.isoformat(),
                         result_copies_ml=res, regimen_code=r["regimen_code"],
                         result_date=(d + dt.timedelta(days=int(rng.integers(6, 40)))).isoformat()))
    rows = [r for r in rows if D.fromisoformat(r["result_date"]) <= C.PULL]
    rows.sort(key=lambda r: (r["sample_date"], r["upid"]))
    return _csv(os.path.join(out, F_VL), ["upid", "facility_code", "sample_date", "result_copies_ml", "regimen_code",
                                          "result_date"], rows)


def estimates(S, rng):
    tot_on = sum(S["adults"].values())
    age = []
    for g, share, cov in (("0-14", 0.052, 0.66), ("15-24", 0.118, 0.81), ("25-49", 0.611, 0.90), ("50+", 0.219, 0.93)):
        plhiv = int(round(tot_on * 1.12 * share / 0.93 * float(rng.uniform(0.97, 1.03)), -2))
        age.append([g, "{:,}".format(plhiv), "{:,}".format(int(plhiv * 0.91 // 100 * 100)),
                    "{:,}".format(int(plhiv * 1.10 // 100 * 100)), "{:,}".format(int(round(plhiv * cov, -2))),
                    "%.0f" % (100 * cov)])
    reg = []
    for r in C.REGIONS:
        on = sum(v for k, v in S["adults"].items() if [x for x in S["recs"] if x["rid"] == k][0]["region"] == r)
        p = int(round(on * 1.14, -2))
        reg.append([r, "{:,}".format(p), "{:,}".format(int(p * 0.9 // 100 * 100)), "{:,}".format(int(p * 1.11 // 100 * 100)),
                    "%.1f" % float(rng.uniform(7.0, 13.5))])
    trend = []
    ni0, ni1, d0, d1 = 1900.0, 14100.0, 1300.0, 6800.0
    for y in range(2021, 2026):
        trend.append([str(y), "{:,}".format(int(round(ni0, -1))), "{:,}".format(int(round(ni1, -1))),
                      "{:,}".format(int(round(d0, -1))), "{:,}".format(int(round(d1, -1)))])
        ni0 *= float(rng.uniform(0.86, 0.93)); ni1 *= float(rng.uniform(0.90, 0.96))
        d0 *= float(rng.uniform(0.84, 0.92)); d1 *= float(rng.uniform(0.90, 0.96))
    return dict(age=age, region=reg, trend=trend)


# ---------------------------------------------------------------------------------------------------- build
def build_pack(out):
    os.makedirs(out, exist_ok=True)
    Wd = make_world()
    place_order(Wd)
    rng = np.random.default_rng(C.SEED + 202)
    n = {}
    n.update(write_register(out, Wd))
    n[F_PROJ] = write_projection(out, Wd["S"])
    n[F_STOCK] = write_stock(out, Wd["S"], Wd["lines"], rng)
    n.update(write_supply(out, Wd))
    n[F_VL] = write_vl(out, Wd, rng)
    DOC.write_dosing(out)
    DOC.write_sop(out)
    DOC.write_estimates(out, estimates(Wd["S"], rng))
    n[F_DICT] = write_dictionary(out)
    n[F_MAN] = write_manifest(out, n)
    return n, Wd


# ---------------------------------------------------------------------------------------------------- dictionary, manifest
DICT = [
    (F_LEG, None, "One row per visit recorded in the legacy paediatric ART register, January 2023 to the system's "
                  "retirement on 30 June 2024. A child has one ART number at each facility where it was registered."),
    (F_LEG, "record_no", "Legacy register record number"),
    (F_LEG, "art_no", "ART number: facility code and the facility's patient serial"),
    (F_LEG, "facility_code", "Facility registry (MFL) code of the facility where the visit took place"),
    (F_LEG, "visit_date", "Date of the visit, day/month/year"),
    (F_LEG, "visit_type", "C clinical visit; P medicines collected by a caregiver"),
    (F_LEG, "weight_kg", "Weight recorded at the visit, kg; blank when no weight was taken"),
    (F_LEG, "regimen", "Regimen dispensed, as the legacy register's regimen list names it"),
    (F_LEG, "months_dispensed", "Months of medicines dispensed at the visit"),
    (F_LEG, "next_visit", "Next appointment date, day/month/year"),
    (F_EPR, None, "One row per encounter in the national EPR's paediatric and adolescent ART module, from its go-live on "
                  "1 June 2024 to 31 August 2026. Visits in June 2024 were also entered in the legacy register."),
    (F_EPR, "encounter_id", "EPR encounter identifier"),
    (F_EPR, "upid", "National patient identifier"),
    (F_EPR, "facility_code", "Facility registry (MFL) code"),
    (F_EPR, "visit_date", "Date of the encounter"),
    (F_EPR, "encounter_type", "Clinical visit, or Medication collection (medicines collected by a caregiver)"),
    (F_EPR, "weight_kg", "Weight recorded at the encounter, kg, to 0.1 kg; blank when no weight was taken"),
    (F_EPR, "regimen_code", "Regimen dispensed, national regimen code"),
    (F_EPR, "months_dispensed", "Months of medicines dispensed"),
    (F_EPR, "next_appointment", "Next appointment date"),
    (F_EPR, "synced_at", "Time the encounter reached the national server from the facility's tablet, UTC"),
    (F_PTS, None, "One row per child or adolescent in the register with a visit since January 2023, as the EPR held it "
                  "on 2 September 2026. The register covers patients under 20."),
    (F_PTS, "upid", "National patient identifier"),
    (F_PTS, "sex", "F or M"),
    (F_PTS, "date_of_birth", "Date of birth"),
    (F_PTS, "dob_estimated", "Y when the date of birth was estimated at registration (recorded as 1 July of the year)"),
    (F_PTS, "art_start_date", "Date antiretroviral treatment started"),
    (F_PTS, "current_facility", "Facility registry code of the facility the patient attends"),
    (F_PTS, "outcome", "Lost to follow-up, Transferred out, Died, Transferred to adult care; blank while on treatment"),
    (F_PTS, "outcome_date", "Date of the outcome. Lost to follow-up is dated 28 days after the first appointment missed"),
    (F_PTS, "outcome_entered", "Date the outcome was entered in the EPR"),
    (F_CW, None, "One row per legacy ART number, with the national patient identifier the EPR migration linked it to"),
    (F_CODES, None, "One row per regimen in the national code list, with the legacy register's name for it"),
    (F_PROJ, None, "Projection sheet: one row per region (and the national total), one column per month; patients on TLD at "
                   "the end of the month"),
    (F_STOCK, None, "Stock status of the 31 August 2026 count. Stock on hand: one row per warehouse and batch. On order: one "
                    "row per lot of an order. Movements: TLD 30s by month."),
    (F_DEL, None, "One row per item of a CMS delivery document for TLD 30s, July 2025 to August 2026, from the warehouse "
                  "system: deliveries to customers (LF), stock transfers between CMS warehouses (NL) and returns from "
                  "customers (LR)."),
    (F_DEL, "delivery_no", "Delivery note number"),
    (F_DEL, "item", "Item of the delivery note"),
    (F_DEL, "plant", "Issuing warehouse: M01 Main warehouse, N01 Northern depot"),
    (F_DEL, "delivery_type", "LF customer delivery; NL stock transfer; LR return from a customer"),
    (F_DEL, "posting_date", "Date the goods issue was posted in the warehouse system"),
    (F_DEL, "customer", "CMS customer account"),
    (F_DEL, "ship_to_name", "Account name"),
    (F_DEL, "delivery_region", "The customer's region in the CMS customer master"),
    (F_DEL, "route", "Delivery route in the customer master"),
    (F_DEL, "material", "CMS material number"),
    (F_DEL, "material_description", "Material description"),
    (F_DEL, "batch", "Manufacturer's batch"),
    (F_DEL, "qty", "Quantity issued, bottles"),
    (F_DEL, "uom", "Unit of measure (BOT bottle)"),
    (F_POD, None, "One row per delivery note signed for, from the drivers' proof-of-delivery app"),
    (F_POD, "signed_on", "Date the receiving facility or warehouse signed the proof of delivery"),
    (F_POD, "signed_by", "Role of the officer who signed, as the driver entered it"),
    (F_ACC, None, "One row per CMS customer account, open or closed, from the customer master"),
    (F_ACC, "mfl_code", "Facility registry code the account was opened for"),
    (F_ACC, "delivery_region", "Region recorded on the account"),
    (F_LMIS, None, "One requisition per facility, month and submission (the ART programme's monthly report and order), "
                   "with a line item per product, from the eLMIS, July 2025 to the reports submitted by 2 September 2026."),
    (F_LMIS, "period", "Month reported, YYYY-MM"),
    (F_LMIS, "region", "Region of the requisition group the report was submitted to"),
    (F_LMIS, "status", "Approved, Returned (sent back to the facility by the district reviewer), Submitted (awaiting review)"),
    (F_LMIS, "quantityDispensed", "Quantity dispensed to patients in the month, in the product's unit (bottles)"),
    (F_LMIS, "stockOnHand", "Physical count at the end of the month"),
    (F_REG, None, "One row per facility record in the Ministry's facility registry (master facility list), ART sites, "
                  "operational and closed, as at 1 September 2026"),
    (F_REG, "region", "Region of the facility's district"),
    (F_REG, "region_since", "Date the facility's district took its current region"),
    (F_REG, "opened_on", "Date the facility opened"),
    (F_REG, "closed_on", "Date the facility closed"),
    (F_VL, None, "One row per viral load result for a patient in the register, samples from July 2025"),
    (DOC.F_DOSING, None, "National guidelines 2025, Annex 7, paediatric dosing"),
    (DOC.F_SOP, None, "CMS standard operating procedure QP-04 version 3"),
    (DOC.F_EST, None, "National ART Programme, HIV estimates 2026 round, summary tables"),
]


def write_dictionary(out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Fields"
    rows = [[f, fld or "(file)", desc] for f, fld, desc in DICT]
    _sheet(ws, ["File", "Field", "Description"], rows, [44, 26, 110])
    ws.freeze_panes = "A2"
    _save(wb, os.path.join(out, F_DICT), C.PEOPLE["quant_lead"], C.PEOPLE["quant_lead"], "2026-03-05T09:00:00Z",
          "2026-09-02T10:05:00Z")
    return len(rows)


MANIFEST = [
    (F_LEG, "Legacy paediatric ART register (retired 30 June 2024)", "Paediatric ART programme", "2026-09-02",
     "Visits 1 January 2023 to 30 June 2024"),
    (F_EPR, "National EPR, paediatric and adolescent ART module", "Paediatric ART programme", "2026-09-02",
     "Encounters 1 June 2024 to 31 August 2026"),
    (F_PTS, "National EPR, paediatric and adolescent ART module", "Paediatric ART programme", "2026-09-02",
     "Patients with a visit since 1 January 2023"),
    (F_CW, "National EPR migration tables", "Paediatric ART programme", "2026-09-02", "Legacy ART numbers"),
    (F_CODES, "National regimen code list, 2025", "National ART Programme", "2026-09-02", "All codes"),
    (F_PROJ, "ART programme projection, September 2026 round", "National ART Programme", "2026-09-01",
     "September 2026 to June 2027"),
    (F_STOCK, "CMS stock status report", "CMS Quantification Unit", "2026-09-02", "Count of 31 August 2026"),
    (F_DEL, "CMS warehouse system, outbound deliveries", "CMS Warehouse Operations", "2026-09-02",
     "Posting dates 1 July 2025 to 31 August 2026, material ARV0412"),
    (F_POD, "Proof-of-delivery app", "CMS Distribution", "2026-09-02", "Delivery notes of the delivery extract"),
    (F_ACC, "CMS warehouse system, customer master", "CMS Warehouse Operations", "2026-09-02", "All accounts"),
    (F_LMIS, "eLMIS national instance, ART programme requisitions", "CMS Quantification Unit", "2026-09-02",
     "Periods July 2025 to August 2026, submissions to 2 September 2026"),
    (F_REG, "Ministry of Health facility registry", "Health Information Unit", "2026-09-01", "ART sites"),
    (F_VL, "National laboratory information system", "Paediatric ART programme", "2026-09-02",
     "Samples from 1 July 2025, results by 2 September 2026"),
    (DOC.F_DOSING, "National guidelines, 2025 edition", "National ART Programme", "2025-07-01", "Annex 7"),
    (DOC.F_SOP, "CMS document register", "CMS Quantification Unit", "2026-03-01", "QP-04 v3"),
    (DOC.F_EST, "HIV estimates, 2026 round", "Strategic Information Unit", "2026-07-30", "Summary tables"),
    (F_DICT, "CMS Quantification Unit", "CMS Quantification Unit", "2026-09-02", "Fields of every file"),
]


def write_manifest(out, counts):
    rows = []
    for f, src, owner, date, cov in MANIFEST:
        rows.append([f, src, owner, date, cov, counts.get(f, "")])
    rows.append([F_MAN, "This manifest", "CMS Quantification Unit", "2026-09-02", "Files of the 2 September 2026 pull", ""])
    return _csv(os.path.join(out, F_MAN), ["file", "source", "compiled_by", "extracted_on", "coverage", "rows"], rows)
