"""Writes the evidence pack under a target folder from the clean truth, the way each producing system
exports it. Nothing here describes the data; each file carries only its own system's conventions."""
import datetime as dt
import json
import os
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from common import (PROVIDERS, OTHER_PROVIDERS, ODS, RENAME, BOARD, SUPPLIER, CASEMIX, VOLUME_2027, FLOOR,
                    INDEX_STENOSIS, INDEX_DISC)
from world import stream, NEW_PLATFORM
from io_util import write_csv, repack_ooxml, write_pdf

D = dt.timedelta
F = {
    "spells": "apc_spells_lumbar_cohort_2022-26.csv",
    "proms_old": "mossgill_spinal_proms_2022-04_to_2025-03.xlsx",
    "proms_new": "mossgill_spinal_proms_2025-04_to_2026-09.csv",
    "link": "mossgill_nhs_number_link_2026-09.csv",
    "deaths": "cohort_deaths_linked_2026-09.csv",
    "policy": "spinal_contracting_policy_2027-28.pdf",
    "capacity": "spinal_capacity_returns_2027-28.xlsx",
    "providers": "provider_reference_2026-09.csv",
    "codes": "code_lookup.csv",
    "ptl": "ptl_spinal_month_end_2026-01_to_2026-03.csv",
    "removals": "ptl_spinal_removals_2025-11_to_2026-04.csv",
    "triage": "msk_triage_referrals_2023-06_to_2026-03.json",
    "fft": "fft_inpatient_spinal_2025-26.csv",
    "cqc": "cqc_locations_2026-09.json",
}
DISTRACTORS = ["fft", "cqc"]
PREFIX = {40117: "RV", 40152: "CM", 40188: "GD", 41206: "SH", 41231: "HP", 41274: "OB", 41309: "OX",
          41355: "PW", 41477: "PW", 41388: "TD", 41402: "TB"}


def dmy(d):
    return "" if d is None or (isinstance(d, float) and np.isnan(d)) else d.strftime("%d/%m/%Y")


def iso(d):
    return "" if d is None or (isinstance(d, float) and np.isnan(d)) else d.isoformat()


def spells_csv(A, path):
    s = A["spells"].copy()
    s = s.sort_values(["submitted", "spell_id"])
    rows = []
    for r in s.itertuples():
        rows.append([r.spell_id, r.pseudo, r.prov, dmy(r.adm), dmy(r.dis), r.meth, r.cls, r.diag, r.proc,
                     dmy(r.opdate) if r.proc else "", r.age, r.sex, "" if r.dis is None else r.dest, r.district,
                     iso(r.submitted)])
    return write_csv(path, ["spell_id", "pseudo_nhs_number", "provider_code", "admission_date", "discharge_date",
                            "admission_method", "patient_classification", "primary_diagnosis", "primary_procedure",
                            "procedure_date", "age_on_admission", "sex", "discharge_destination", "postcode_district",
                            "sus_submitted"], rows)


DUR_TEXT = {1: "Less than 3 months", 2: "3 to 12 months", 3: "1 to 2 years", 4: "More than 2 years"}


def proms_files(A, p_old, p_new):
    q = A["q"].copy()
    q = q.sort_values(["completed", "ref", "qtype"]).reset_index(drop=True)
    old = q[q.completed < NEW_PLATFORM]
    new = q[q.completed >= NEW_PLATFORM]
    wb = Workbook(write_only=True)
    ws = wb.create_sheet("Questionnaires")
    ws.append(["%s - Spinal Outcomes Programme" % SUPPLIER])
    ws.append(["Commissioner extract: %s | Questionnaires completed 01/04/2022 to 31/03/2025 | Produced 07/04/2025" % BOARD])
    ws.append([])
    ws.append(["PatientRef", "Site", "OperationDate", "Questionnaire", "Completed", "BirthYear", "Sex", "Smoker",
               "PreviousSpinalSurgery", "SymptomDuration"] + ["ODI%d" % i for i in range(1, 11)])
    for r in old.itertuples():
        pre = r.qtype == "pre"
        ws.append([r.ref, r.site, r.sup_op, "Pre-operative" if pre else "12 months", r.completed, int(r.yob),
                   "F" if r.sex == 2 else "M",
                   ("Yes" if r.smoker else "No") if pre else None,
                   ("Yes" if r.prev else "No") if pre else None,
                   DUR_TEXT[int(r.dur)] if pre else None] + list(r.ans))
    wb.save(p_old)
    repack_ooxml(p_old, SUPPLIER, "Mossgill Data Services", "2025-04-07T06:12:00Z", "2025-04-07T06:14:00Z",
                 "Spinal Outcomes Programme commissioner extract", SUPPLIER)
    rows = []
    for r in new.itertuples():
        pre = r.qtype == "pre"
        n = sum(v is not None for v in r.ans)
        rows.append([r.ref, r.site, dmy(r.sup_op), "PREOP" if pre else "M12", iso(r.completed), int(r.yob), int(r.sex),
                     ("Y" if r.smoker else "N") if pre else "", ("Y" if r.prev else "N") if pre else "",
                     int(r.dur) if pre else "", n, int(r.tot)])
    write_csv(p_new, ["patient_ref", "site_code", "operation_date", "questionnaire", "completed_date", "birth_year",
                      "sex", "smoker", "previous_spinal_surgery", "symptom_duration", "odi_sections_answered",
                      "odi_raw_score"], rows, newline="\n")
    return len(old), len(new)


def link_csv(A, path):
    reg = A["reg"].sort_values("ref")
    rows = [[r.ref, r.pseudo, "Linked" if r.pseudo else "No NHS number supplied", iso(r.linked_on) if r.pseudo else ""]
            for r in reg.itertuples()]
    return write_csv(path, ["patient_ref", "pseudo_nhs_number", "link_status", "linked_on"], rows, newline="\n")


def deaths_csv(A, path):
    d = A["deaths"].sort_values(["dod", "pseudo"])
    rows = [[r.pseudo, iso(r.dod), r.cause] for r in d.itertuples()]
    return write_csv(path, ["pseudo_nhs_number", "date_of_death", "underlying_cause"], rows, newline="\n")


def providers_csv(path):
    rows = []
    for p in PROVIDERS:
        k = p["key"]
        if k == RENAME["old_key"]:
            rows.append([k, p["name"], p["org"], "Independent sector", ODS[k], p["site"], "2004-06-01", "2025-03-31", ""])
            rows.append([RENAME["new_key"], RENAME["new_name"], RENAME["new_org"], "Independent sector", ODS[RENAME["new_key"]],
                         p["site"], "2025-04-01", "", k])
        else:
            rows.append([k, p["name"], p["org"], "NHS trust" if p["kind"] == "NHS" else "Independent sector", ODS[k],
                         p["site"], "2001-04-01" if p["kind"] == "NHS" else "2006-09-01", "", ""])
    for o in OTHER_PROVIDERS:
        rows.append([o["key"], o["name"], o["org"], "NHS trust" if o["kind"] == "NHS" else "NHS community hospital",
                     o["ods"], "", "2001-04-01", "", ""])
    rows.sort(key=lambda r: r[0])
    return write_csv(path, ["provider_code", "provider_name", "organisation", "sector", "ods_site_code",
                            "mossgill_site_code", "valid_from", "valid_to", "predecessor_provider_code"], rows, newline="\n")


CODES = [
    ("OPCS-4", "V253", "Primary posterior laminectomy decompression of lumbar spine"),
    ("OPCS-4", "V254", "Primary posterior decompression of lumbar spine NEC"),
    ("OPCS-4", "V255", "Primary lateral foraminotomy of lumbar spine"),
    ("OPCS-4", "V256", "Primary lateral recess decompression of lumbar spine"),
    ("OPCS-4", "V331", "Primary laminectomy excision of lumbar intervertebral disc"),
    ("OPCS-4", "V332", "Primary fenestration excision of lumbar intervertebral disc"),
    ("OPCS-4", "V337", "Primary microdiscectomy of lumbar intervertebral disc"),
    ("OPCS-4", "V264", "Revisional posterior decompression of lumbar spine NEC"),
    ("OPCS-4", "V347", "Revisional microdiscectomy of lumbar intervertebral disc"),
    ("OPCS-4", "A521", "Therapeutic lumbar epidural injection"),
    ("OPCS-4", "V544", "Injection around facet of lumbar spine"),
    ("OPCS-4", "C751", "Insertion of prosthetic replacement for lens"),
    ("OPCS-4", "T202", "Primary repair of inguinal hernia"),
    ("OPCS-4", "A651", "Carpal tunnel release"),
    ("OPCS-4", "H221", "Diagnostic endoscopic examination of colon"),
    ("OPCS-4", "H251", "Diagnostic endoscopic examination of lower bowel"),
    ("ICD-10", "M480", "Spinal stenosis"),
    ("ICD-10", "M511", "Lumbar and other intervertebral disc disorders with radiculopathy"),
    ("ICD-10", "M512", "Other specified intervertebral disc displacement"),
    ("ICD-10", "M541", "Radiculopathy"),
    ("ICD-10", "M544", "Lumbago with sciatica"),
    ("ICD-10", "M545", "Low back pain"),
    ("ICD-10", "T810", "Haemorrhage and haematoma complicating a procedure"),
    ("ICD-10", "T814", "Infection following a procedure"),
    ("ICD-10", "G970", "Cerebrospinal fluid leak from spinal puncture"),
    ("ICD-10", "I269", "Pulmonary embolism without mention of acute cor pulmonale"),
    ("ICD-10", "I802", "Phlebitis and thrombophlebitis of other deep vessels of lower extremities"),
    ("ICD-10", "R33X", "Retention of urine"),
    ("ICD-10", "N390", "Urinary tract infection, site not specified"),
    ("ICD-10", "R074", "Chest pain, unspecified"),
    ("ICD-10", "J189", "Pneumonia, unspecified"),
    ("ICD-10", "I480", "Paroxysmal atrial fibrillation"),
    ("ICD-10", "R55X", "Syncope and collapse"),
    ("ICD-10", "K358", "Acute appendicitis, other and unspecified"),
    ("ICD-10", "S720", "Fracture of neck of femur"),
    ("ICD-10", "I214", "Acute subendocardial myocardial infarction"),
    ("ICD-10", "J441", "Chronic obstructive pulmonary disease with acute exacerbation, unspecified"),
    ("ICD-10", "R104", "Other and unspecified abdominal pain"),
    ("ICD-10", "H251", "Senile nuclear cataract"),
    ("ICD-10", "K409", "Unilateral or unspecified inguinal hernia, without obstruction or gangrene"),
    ("ICD-10", "G560", "Carpal tunnel syndrome"),
    ("ICD-10", "K573", "Diverticular disease of large intestine without perforation or abscess"),
    ("ICD-10", "K621", "Rectal polyp"),
    ("ICD-10", "I219", "Acute myocardial infarction, unspecified"),
    ("ICD-10", "C349", "Malignant neoplasm of bronchus or lung, unspecified"),
    ("ICD-10", "J449", "Chronic obstructive pulmonary disease, unspecified"),
    ("ICD-10", "I64X", "Stroke, not specified as haemorrhage or infarction"),
    ("ICD-10", "C509", "Malignant neoplasm of breast, unspecified"),
    ("ICD-10", "F03X", "Unspecified dementia"),
    ("ICD-10", "I500", "Congestive heart failure"),
    ("ICD-10", "C189", "Malignant neoplasm of colon, unspecified"),
    ("ICD-10", "G309", "Alzheimer disease, unspecified"),
    ("Admission method", "11", "Elective admission: waiting list"),
    ("Admission method", "12", "Elective admission: booked"),
    ("Admission method", "13", "Elective admission: planned"),
    ("Admission method", "21", "Emergency admission: via Accident and Emergency"),
    ("Admission method", "22", "Emergency admission: via general practitioner"),
    ("Admission method", "23", "Emergency admission: via bed bureau"),
    ("Admission method", "24", "Emergency admission: via consultant outpatient clinic"),
    ("Admission method", "28", "Emergency admission: other means"),
    ("Admission method", "81", "Transfer of an admitted patient from another hospital provider"),
    ("Patient classification", "1", "Ordinary admission"),
    ("Patient classification", "2", "Day case admission"),
    ("Discharge destination", "19", "Usual place of residence"),
    ("Discharge destination", "51", "NHS other hospital provider: ward for general patients"),
    ("Discharge destination", "79", "Patient died"),
    ("Sex", "1", "Male"),
    ("Sex", "2", "Female"),
]


def codes_csv(path):
    return write_csv(path, ["code_system", "code", "description"], [list(c) for c in CODES], newline="\n")


def capacity_xlsx(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Returns"
    ws.append(["%s | Planned care | 2027-28 additional elective spinal capacity" % BOARD])
    ws.append(["Additional lumbar decompression and discectomy operations offered by each provider for 2027-28, as "
               "returned; not netted against activity contracted by other commissioners"])
    ws.append(["Version 1.2 | Refreshed 29/09/2026 | Owner: Planned care contracting team"])
    ws.append([])
    ws.append(["Provider", "ODS site code", "Q1 2027-28", "Q2 2027-28", "Q3 2027-28", "Q4 2027-28", "Total offered",
               "Return received"])
    for c in ws[5]:
        c.font = Font(bold=True)
    ws["A1"].font = Font(bold=True)
    r = stream(9990)
    order = sorted(PROVIDERS, key=lambda p: p["name"])
    for p in order:
        key = RENAME["new_key"] if p["key"] == RENAME["old_key"] else p["key"]
        name = RENAME["new_name"] if p["key"] == RENAME["old_key"] else p["name"]
        w = np.array([0.22, 0.27, 0.26, 0.25]) + r.normal(0, 0.012, 4)
        q = np.floor(p["cap"] * w / w.sum()).astype(int)
        q[int(np.argmax(w))] += p["cap"] - q.sum()
        rec = dt.date(2026, 8, 14) + D(days=int(r.integers(0, 30)))
        ws.append([name, ODS[key]] + [int(x) for x in q] + [int(p["cap"]), rec])
        ws.cell(row=ws.max_row, column=8).number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDEFGH", [34, 14, 12, 12, 12, 12, 14, 16]):
        ws.column_dimensions[col].width = wd
    wb.save(path)
    repack_ooxml(path, "Planned care contracting team", "Planned care contracting team", "2026-08-11T09:02:00Z",
                 "2026-09-29T15:47:00Z", "2027-28 spinal capacity returns", BOARD)


def pathway_ids(A):
    """Each provider's patient administration system numbers pathways across every specialty, so the spinal
    pathways it holds are increasing numbers with irregular gaps."""
    P = A["paths"]
    out = {}
    r = stream(9994)
    for prov, g in P.groupby(P.prov.map(lambda k: PREFIX[k])):
        g = g.sort_values(["receipt", "path"])
        start = int(r.integers(1_200_000, 4_800_000))
        gaps = r.geometric(1 / 41.0, size=len(g))
        for path, v in zip(g.path, start + np.cumsum(gaps)):
            out[path] = "%s%07d" % (prov, v)
    return out


def ptl_files(A, p_ptl, p_rem):
    pid = pathway_ids(A)
    ptl = A["ptl"].sort_values(["snap", "prov", "path"])
    ptl = ptl.assign(pw=ptl.path.map(pid)).sort_values(["snap", "prov", "pw"])
    rows = []
    for r in ptl.itertuples():
        rows.append([iso(r.snap), r.prov, r.pw, r.pseudo, r.yob, r.sex, r.district, r.gp,
                     r.route, dmy(r.receipt), dmy(r.clock_rec), r.weeks, r.proc, r.prio, dmy(r.tci) if r.tci else ""])
    n1 = write_csv(p_ptl, ["snapshot_date", "provider_code", "pathway_id", "pseudo_nhs_number", "birth_year", "sex",
                           "postcode_district", "gp_practice", "referral_route", "referral_received", "rtt_clock_start",
                           "weeks_waiting", "planned_procedure", "priority", "tci_date"], rows, newline="\r\n")
    rem = A["removals"].sort_values(["rec_on", "prov", "path"])
    rows = []
    for r in rem.itertuples():
        rows.append([r.prov, pid[r.path], r.pseudo, r.route, dmy(r.receipt), dmy(r.clock_rec),
                     dmy(r.removal), r.reason, r.dest, iso(r.rec_on)])
    n2 = write_csv(p_rem, ["provider_code", "pathway_id", "pseudo_nhs_number", "referral_route", "referral_received",
                           "rtt_clock_start", "removal_date", "removal_reason", "transferred_to", "recorded_on"], rows,
                   newline="\r\n")
    return n1, n2


def triage_json(A, path):
    t = A["triage"].copy()
    r = stream(9991)
    t["ref"] = ["MSK-%06d" % v for v in r.choice(np.arange(100000, 999999), size=len(t), replace=False)]
    t = t.sort_values(["received", "ref"])
    recs = []
    for x in t.itertuples():
        recs.append({"triage_ref": x.ref, "patient_token": x.token, "birth_year": int(x.yob),
                     "sex": "F" if x.sex == 2 else "M", "postcode_district": x.district, "gp_practice": x.gp,
                     "received": iso(x.received), "outcome": x.outcome, "routed_to": x.routed_to or None,
                     "outcome_date": iso(x.routed_on)})
    doc = {"service": "Quenmoor and Kirkbeck Community MSK Triage Service", "extract_run": "2026-04-14T07:05:00+01:00",
           "referrals": recs}
    head = json.dumps({k: v for k, v in doc.items() if k != "referrals"}, ensure_ascii=False)[:-1]
    body = ",\n".join(json.dumps(x, ensure_ascii=False, separators=(",", ":")) for x in recs)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(head + ',"referrals":[\n' + body + "\n]}\n")
    return len(recs)


def fft_csv(path):
    r = stream(9992)
    rows = []
    for p in sorted(PROVIDERS, key=lambda p: p["key"]):
        key = RENAME["new_key"] if p["key"] == RENAME["old_key"] else p["key"]
        base = 0.86 + 0.06 * r.random()
        for m in range(12):
            month = dt.date(2025 + (3 + m) // 12, (3 + m) % 12 + 1, 1)
            n = int(r.integers(18, 70))
            pv = np.array([base, 0.93 - base + 0.05, 0.03, 0.012, 0.008, 0.01]).clip(0.002)
            pv = pv / pv.sum()
            c = r.multinomial(n, pv)
            rows.append([ODS[key], month.strftime("%Y-%m"), n] + [int(v) for v in c])
    return write_csv(path, ["ods_site_code", "month", "responses", "very_good", "good", "neither_good_nor_poor",
                            "poor", "very_poor", "dont_know"], rows, newline="\n")


def cqc_json(path):
    r = stream(9993)
    rat = ["Outstanding", "Good", "Good", "Good", "Requires improvement"]
    locs = []
    allp = [(RENAME["new_key"] if p["key"] == RENAME["old_key"] else p["key"],
             RENAME["new_name"] if p["key"] == RENAME["old_key"] else p["name"]) for p in PROVIDERS]
    for key, name in sorted(allp):
        dom = {d: rat[int(r.integers(0, 5))] for d in ("safe", "effective", "caring", "responsive", "well_led")}
        overall = "Good" if list(dom.values()).count("Requires improvement") < 2 else "Requires improvement"
        insp = dt.date(2022, 1, 10) + D(days=int(r.integers(0, 1300)))
        locs.append({"location_name": name, "ods_site_code": ODS[key], "overall": overall,
                     "key_question_ratings": dom, "report_published": iso(insp)})
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump({"retrieved": "2026-09-30", "locations": locs}, f, indent=1)
        f.write("\n")
    return len(locs)


def write_pack(A, target):
    os.makedirs(target, exist_ok=True)
    for fn in os.listdir(target):
        os.remove(os.path.join(target, fn))
    n = {}
    n["spells"] = spells_csv(A, os.path.join(target, F["spells"]))
    n["proms_old"], n["proms_new"] = proms_files(A, os.path.join(target, F["proms_old"]), os.path.join(target, F["proms_new"]))
    n["link"] = link_csv(A, os.path.join(target, F["link"]))
    n["deaths"] = deaths_csv(A, os.path.join(target, F["deaths"]))
    n["providers"] = providers_csv(os.path.join(target, F["providers"]))
    n["codes"] = codes_csv(os.path.join(target, F["codes"]))
    capacity_xlsx(os.path.join(target, F["capacity"]))
    n["capacity"] = len(PROVIDERS)
    n["ptl"], n["removals"] = ptl_files(A, os.path.join(target, F["ptl"]), os.path.join(target, F["removals"]))
    n["triage"] = triage_json(A, os.path.join(target, F["triage"]))
    n["fft"] = fft_csv(os.path.join(target, F["fft"]))
    n["cqc"] = cqc_json(os.path.join(target, F["cqc"]))
    from policy import write_policy
    write_policy(os.path.join(target, F["policy"]))
    n["policy"] = 1
    return n
