"""Write the pack: the dispensing extract, both template exports, the register, the policy, the thread, the dm+d list,
the SUS falls cohort with the provider sites, the falls dashboard's definitions, and two files the solution never uses."""
import csv
import datetime as dt
import hashlib
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import docs
import params as P
import postprocess
import sus as S
import world as W

FILES = P.FILES
PACK = list(FILES)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def _xlsx(path, sheets, made, saved, person):
    wb = Workbook()
    for i, (title, header, rows, widths) in enumerate(sheets):
        ws = wb.active if i == 0 else wb.create_sheet()
        ws.title = title
        ws.append(header)
        for c in ws[1]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="DCE6F0")
            c.alignment = Alignment(vertical="top", wrap_text=True)
        for r in rows:
            ws.append(list(r))
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = w
        ws.freeze_panes = "A2"
    wb.properties.creator = person
    wb.properties.lastModifiedBy = person
    wb.save(path)
    postprocess.scrub(path, P.ORG, saved[:10])
    postprocess.finish_office(path, made, saved, P.ORG, person=person)


def iso(d):
    return d.isoformat() if d else ""


def uk(d):
    return d.strftime("%d/%m/%Y") if d else ""


def dmd_rows():
    rs = np.random.default_rng(P.SEED + 11)
    out = []
    for vtm, vmp, cls, qty, nic, _ in P.DRUGS:
        vmp_id = "3%08d1000001%d" % (int(rs.integers(10 ** 7, 10 ** 8 - 1)), int(rs.integers(0, 10)))
        vtm_id = "7%07d" % int(rs.integers(10 ** 6, 10 ** 7 - 1))
        bnf = ("0401010" if cls == "Z-drug" or vtm in ("Temazepam", "Nitrazepam", "Lormetazepam") else "0402010")
        out.append([vmp_id, vmp, vtm_id, vtm, bnf + {"Zopiclone": "Z0", "Zolpidem": "Y0", "Temazepam": "T0",
                                                   "Diazepam": "D0", "Lorazepam": "L0", "Nitrazepam": "N0",
                                                   "Lormetazepam": "R0"}[vtm] + "AA", "Tablet", "Oral",
                    "Controlled Drug Schedule %s" % ("4 (Part 1)" if cls == "benzodiazepine" and vtm != "Temazepam"
                                                     else ("3" if vtm == "Temazepam" else "4 (Part 1)")),
                    qty, "%.2f" % nic])
    return out


def dashboard_rows(prs, disp):
    """Q2 2026 (April to June) prescribing by practice: items, patients aged 65 or over with an item, cost"""
    q = [r for r in disp if dt.date(2026, 4, 1) <= r["dispensed_date"] <= dt.date(2026, 6, 30)]
    by = {}
    for r in q:
        b = by.setdefault(r["practice_code"], dict(items=0, cost=0.0, pts=set(), pts65=set()))
        b["items"] += 1
        b["cost"] += r["nic_gbp"]
        b["pts"].add(r["patient_pseudo_id"])
        if r["year_of_birth"] <= 1961:
            b["pts65"].add(r["patient_pseudo_id"])
    names = {c: n for c, n, _, _ in P.LOCALITIES}
    rs = np.random.default_rng(P.SEED + 12)
    out = []
    for p in prs:
        b = by.get(p["code"], dict(items=0, cost=0.0, pts=set(), pts65=set()))
        starpu = int(round(len(b["pts"]) / 0.031 * (0.9 + 0.2 * rs.random()), -1))
        out.append([p["code"], p["name"], names[p["locality"]], b["items"], len(b["pts"]), len(b["pts65"]),
                    round(b["items"] * 28 / 1.0 / (starpu / 1000.0) / 91.0, 2), round(b["cost"], 2), starpu])
    return out


def referral_rows(prs):
    rs = np.random.default_rng(P.SEED + 13)
    out, k = [], 0
    codes = [p["code"] for p in prs]
    w = np.array([p["weight"] * dict((c, n) for c, _, n, _ in P.LOCALITIES)[p["locality"]] for p in prs])
    for _ in range(4120):
        k += 1
        d = P.FY_FROM + dt.timedelta(days=int(rs.integers(0, 365)))
        pc = codes[int(rs.choice(len(codes), p=w / w.sum()))]
        src = ["GP", "Emergency department", "Ambulance service", "Self or family", "Community nursing",
               "Social care"][int(rs.choice(6, p=[0.34, 0.18, 0.16, 0.10, 0.14, 0.08]))]
        seen = rs.random() < 0.82
        out.append(["FS%06d" % (204000 + k), iso(d), pc, ["65-74", "75-84", "85+"][int(rs.choice(3, p=[0.28, 0.42, 0.30]))],
                    src, ["Fall in last 12 months", "Fear of falling", "Unsteady gait"][int(rs.choice(3, p=[0.71, 0.13, 0.16]))],
                    "Y" if seen else "N", int(rs.integers(5, 70)) if seen else ""])
    out.sort(key=lambda r: (r[1], r[0]))
    return out


def build(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    prs = W.practices()
    us = W.users(prs)
    cur, leg, move = W.templates(us, prs)
    disp = W.dispensing(us)

    _csv(F["dispensing"], ["dispensed_date", "processing_month", "patient_pseudo_id", "practice_code", "product",
                           "quantity", "nic_gbp", "year_of_birth", "sex"],
         [[iso(r["dispensed_date"]), r["dispensed_date"].strftime("%Y%m"), r["patient_pseudo_id"], r["practice_code"],
           r["product"], r["quantity"], "%.2f" % r["nic_gbp"], r["year_of_birth"], r["sex"]] for r in disp])

    cur = sorted(cur, key=lambda t: (t["practice_code"], t["patient_pseudo_id"], t["authorised_from"], t["template_id"]))
    _csv(F["templates"], ["template_id", "patient_pseudo_id", "practice_code", "product", "directions", "quantity",
                          "issues_authorised", "authorised_from", "review_date", "ended_on", "end_reason",
                          "replaces_template_id", "migration_source_ref"],
         [[t["template_id"], t["patient_pseudo_id"], t["practice_code"], t["product"], t["directions"], t["quantity"],
           t["issues"], iso(t["authorised_from"]), iso(t["review_date"]), iso(t["ended_on"]), t["end_reason"],
           t["replaces_template_id"], t["migration_source_ref"]] for t in cur])

    leg = sorted(leg, key=lambda t: (t["practice_code"], t["template_ref"]))
    _csv(F["legacy"], ["TemplateRef", "PatientPseudoID", "PracticeCode", "DrugName", "Dosage", "Qty", "IssuesAllowed",
                       "StartDate", "ReviewDate", "EndDate", "EndReason", "SupersededRef"],
         [[t["template_ref"], t["patient_pseudo_id"], t["practice_code"], t["drug"], t["directions"], t["qty"],
           t["issues"], uk(t["start_date"]), uk(t["review_date"]), uk(t["end_date"]), t["end_reason"],
           t["superseded_ref"]] for t in leg])

    names = {c: n for c, n, _, _ in P.LOCALITIES}
    _xlsx(F["register"], [("Practices", ["Practice code", "Practice name", "Town", "Locality code", "Locality",
                                         "Previous practice codes"],
                           [[p["code"], p["name"], p["town"], p["locality"], names[p["locality"]], p["predecessor"]]
                            for p in sorted(prs, key=lambda p: (p["locality"], p["code"]))], [14, 32, 16, 13, 20, 22]),
                          ("Localities", ["Locality code", "Locality", "Practices"],
                           [[c, n, P.PRACTICES[c]] for c, n, _, _ in P.LOCALITIES], [13, 22, 10])],
          "2026-04-02T09:15:00Z", "2026-10-05T10:40:00Z", "Paula Marsh")

    docs.policy(F["policy"])
    postprocess.scrub(F["policy"], "Microsoft Word 2016", "2026-06-24T15:10:00")
    docs.falls_definition(F["falls_def"])
    postprocess.scrub(F["falls_def"], "Microsoft Word 2016", "2026-02-11T11:25:00")
    with open(F["thread"], "w", encoding="utf-8", newline="\n") as fh:
        fh.write(docs.thread())

    _csv(F["dmd"], ["vmp_id", "vmp_name", "vtm_id", "vtm_name", "bnf_code", "form", "route", "controlled_drug_category",
                    "pack_quantity", "nic_per_pack_gbp"], dmd_rows())

    g = S.build(prs)
    _csv(F["sus"], S.EP_COLS, [[iso(v) if isinstance(v, dt.date) else v for v in r] for r in S.rows(g)])
    _csv(F["providers"], ["provider_code", "site_code", "site_name", "site_type", "organisation_name"],
         [list(x) for x in S.PROVIDERS])

    _xlsx(F["dashboard"], [("Q2 2026 by practice", ["Practice code", "Practice name", "Locality",
                                                     "Items (benzodiazepines and Z-drugs)", "Patients with an item",
                                                     "Patients aged 65+ with an item", "ADQ per 1,000 STAR-PU a day",
                                                     "Cost (GBP)", "STAR-PU"],
                            dashboard_rows(prs, disp), [13, 30, 18, 14, 12, 14, 14, 12, 10])],
          "2026-07-20T08:30:00Z", "2026-07-22T14:05:00Z", P.PEOPLE["analyst"])
    _csv(F["referrals"], ["referral_id", "referral_date", "practice_code", "age_band", "referral_source", "reason",
                          "seen", "days_to_first_contact"], referral_rows(prs))
    return dict(prs=prs, users=us, templates=cur, legacy=leg, dispensing=disp, sus=g, move=move)
