"""Write the evidence pack's data files from the records: CSV exports as each system writes them, the EDC's status
workbook and the pharmacovigilance listing as their owners save them, and the site register as JSON."""
import csv
import datetime as dt
import json

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import postprocess as PP
import records as RC

FILES = {
    "charter": "talon2_dmc_charter_v3.0.pdf",
    "sap": "talon2_statistical_analysis_plan_v2.0.pdf",
    "schedule": "ashgrove_funding_agreement_schedule_2.pdf",
    "irt_rand": "talon2_irt_randomisation_export.csv",
    "bicr": "talon2_bicr_timepoint_reads.csv",
    "inv": "talon2_investigator_tumour_assessments.csv",
    "status": "talon2_edc_subject_status.xlsx",
    "screening": "talon2_screening_log.csv",
    "pv": "talon2_pv_sae_line_listing.xlsx",
    "ae": "talon2_edc_adverse_events.csv",
    "central": "talon2_central_lab_transfer.csv",
    "local": "talon2_edc_local_labs.csv",
    "samples": "talon2_edc_central_lab_kit_log.csv",
    "exposure": "talon2_edc_exposure.csv",
    "irt_admin": "talon2_irt_drug_administration.csv",
    "sites": "talon2_sites.json",
}
DISTRACTORS = ("inv", "ae")
DS = ("Initially unresectable", "Recurrent")
PS = ("Intrahepatic cholangiocarcinoma", "Extrahepatic cholangiocarcinoma", "Gallbladder cancer")
RESP_LONG = {"CR": "Complete response", "PR": "Partial response", "SD": "Stable disease", "PD": "Progressive disease",
             "NE": "Not evaluable"}


def iso(d):
    return d.isoformat() if d else ""


def dmy(d):
    return d.strftime("%d/%m/%Y") if d else ""


def dmon(d):
    return d.strftime("%d-%b-%Y").upper() if d else ""


def write_csv(path, header, rows, crlf=True):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n" if crlf else "\n")
        wr.writerow(header)
        for r in rows:
            wr.writerow(r)
    return len(rows)


def irt_rand(R, path):
    rows = []
    for p in R.w.pts:
        rows.append([p["rand_no"], p["screening_no"], p["site_id"], R.site[p["site"]]["country"],
                     p["rand_utc"].strftime("%Y-%m-%d %H:%M"), DS[p["irt_ds"]], PS[p["irt_ps"]],
                     "Ravolimab + gemcitabine/cisplatin" if p["arm"] == 1 else "Placebo + gemcitabine/cisplatin"])
    return write_csv(path, ["Randomisation Number", "Screening Number", "Site", "Country", "Randomisation Date/Time (UTC)",
                            "Stratum: Disease Status", "Stratum: Primary Tumour Site", "Treatment Arm"], rows)


def bicr(R, path):
    rows = sorted(R.bicr, key=lambda x: (x["rand_no"], x["scan_date"]))
    return write_csv(path, ["SUBJID", "TPT", "SCANDT", "BICR_OVRL_RESP", "READDT"],
                     [[x["rand_no"], x["timepoint"], iso(x["scan_date"]), x["response"], iso(x["read_date"])] for x in rows],
                     crlf=False)


def inv(R, path):
    rows = sorted(R.inv, key=lambda x: (x["rand_no"], x["assessment_date"]))
    return write_csv(path, ["Subject", "Visit", "Assessment date", "Investigator overall response (RECIST 1.1)"],
                     [[x["rand_no"], x["timepoint"], dmy(x["assessment_date"]), RESP_LONG[x["response"]]] for x in rows])


def _sheet(ws, header, rows, widths):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EE")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in rows:
        ws.append(r)
    for i, wdt in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = wdt
    ws.freeze_panes = "A2"


def status(R, path, stamp):
    w = R.w
    wb = Workbook()
    ws = wb.active
    ws.title = "Baseline"
    rows = []
    for p in w.pts:
        rows.append([p["rand_no"], p["site_id"], p["sex"], p["rand_date"].year - p["yob"] - 1, p["ecog"], DS[p["ds"]],
                     PS[p["ps"]], "Yes" if p["liver_mets"] else "No", p["weight"], p["height"]])
    _sheet(ws, ["Subject", "Site", "Sex", "Age (years)", "ECOG PS", "Disease status (eCRF)", "Primary tumour site (eCRF)",
                "Liver metastases", "Weight (kg)", "Height (cm)"], rows, [11, 7, 5, 8, 8, 22, 30, 10, 9, 9])
    ws = wb.create_sheet("Disposition")
    rows = []
    for p in w.pts:
        if p["on_treatment"]:
            tstat, tdate, treason = "Ongoing", None, ""
        elif p["first_dose"] is None:
            tstat, tdate, treason = "Not started", None, ""
        else:
            tstat = "Discontinued"
            tdate = p["last_dose"]
            if p["pd_cal"] is not None and p["last_dose"] >= p["pd_cal"] - dt.timedelta(days=30):
                treason = "Progressive disease"
            elif p["death_date"] is not None and p["last_dose"] >= p["death_date"] - dt.timedelta(days=40):
                treason = "Death"
            elif p["withdraw_date"] is not None:
                treason = "Withdrawal of consent"
            else:
                treason = "Adverse event"
        if p["death_date"] is not None:
            sstat = "Died"
        elif p["withdraw_date"] is not None:
            sstat = "Withdrew consent" if (p["i"] % 3) else "Lost to follow-up"
        else:
            sstat = "In follow-up"
        rows.append([p["rand_no"], tstat, tdate, treason, sstat, p["withdraw_date"] if sstat in ("Withdrew consent", "Lost to follow-up") else None])
    _sheet(ws, ["Subject", "Treatment status", "Date of last dose (if discontinued)", "Primary reason for discontinuation",
                "Study status", "Date of withdrawal or loss to follow-up"], rows, [11, 14, 16, 26, 18, 18])
    for r in ws.iter_rows(min_row=2):
        for c in (r[2], r[5]):
            c.number_format = "dd-mmm-yyyy"
    ws = wb.create_sheet("Deaths")
    rows = [[p["rand_no"], p["death_date"], p["death_cause"]] for p in w.pts if p["death_date"] is not None]
    _sheet(ws, ["Subject", "Date of death", "Primary cause of death"], rows, [11, 14, 30])
    for r in ws.iter_rows(min_row=2):
        r[1].number_format = "dd-mmm-yyyy"
    wb.save(path)
    PP.normalize_xlsx(path, "Chloe Ball", stamp[0], stamp[1], company="Kesterton University Cancer Trials Unit")


def screening(R, path):
    rows = []
    for a in R.screening:
        rows.append([a["screening_no"], a["site_id"], dmon(a["date"]), a["sex"], a["yob"], a["initials"], a["outcome"],
                     a["reason"]])
    return write_csv(path, ["Screening No", "Site", "Screening Date", "Sex", "Year of Birth", "Initials", "Outcome",
                            "Screen Failure Reason"], rows)


def pv(R, path, stamp):
    wb = Workbook()
    ws = wb.active
    ws.title = "SAE line listing"
    rows = []
    for x in sorted(R.pv, key=lambda x: (x["case_no"], x["receipt_date"])):
        rows.append([x["case_no"], x["version"], x["receipt_date"], x["site_id"], x["screening_no"],
                     "Male" if x["sex"] == "M" else "Female", x["year_of_birth"], x["reported_term"], x["meddra_pt"],
                     x["meddra_soc"], x["onset_date"], x["seriousness"], x["case_status"]])
    _sheet(ws, ["Case number", "Report version", "Date received", "Site", "Patient (screening number)", "Sex",
                "Year of birth", "Reported term", "MedDRA preferred term", "MedDRA system organ class", "Onset date",
                "Seriousness criterion", "Case status"], rows, [16, 13, 13, 7, 14, 8, 8, 26, 26, 36, 12, 16, 11])
    for r in ws.iter_rows(min_row=2):
        r[2].number_format = "dd/mm/yyyy"
        r[10].number_format = "dd/mm/yyyy"
    wb.save(path)
    PP.normalize_xlsx(path, "Pharmacovigilance Office", stamp[0], stamp[1], company="Kesterton University Cancer Trials Unit")
    return len(rows)


def ae(R, path):
    rows = sorted(R.ae_edc, key=lambda x: (x["rand_no"], x["onset"], x["term"]))
    out = []
    seq = {}
    for x in rows:
        seq[x["rand_no"]] = seq.get(x["rand_no"], 0) + 1
        out.append([x["rand_no"], seq[x["rand_no"]], x["term"], x["soc"], iso(x["onset"]), x["grade"], x["serious"]])
    return write_csv(path, ["USUBJID", "AESPID", "AEDECOD", "AESOC", "AESTDTC", "AETOXGR", "AESER"], out, crlf=False)


def central(R, path):
    rows = []
    for x in R.central:
        rows.append([x["lab"], x["accession_no"], x["screening_no"], x["visit"], iso(x["date"]), x["test_code"],
                     x["test_name"], x["result"], x["unit"], "" if x["ref_low"] is None else x["ref_low"], x["ref_high"]])
    return write_csv(path, ["LAB_NAME", "ACCESSION", "SCREENING_NO", "VISIT", "COLLECTION_DATE", "TEST_CODE", "TEST_NAME",
                            "RESULT", "UNITS", "REF_LOW", "REF_HIGH"], rows, crlf=False)


def local(R, path):
    rows = sorted(R.local, key=lambda x: (x["rand_no"], x["collected"], x["test_name"]))
    return write_csv(path, ["Subject", "Laboratory", "Sample date", "Test", "Result", "Unit", "Upper limit of normal"],
                     [[x["rand_no"], x["lab"], dmy(x["collected"]), x["test_name"], x["result"], x["unit"], x["uln"]]
                      for x in rows])


def samples(R, path):
    rows = sorted(R.sample_log, key=lambda x: (x["rand_no"], x["collected"]))
    return write_csv(path, ["Subject", "Visit", "Kit accession number", "Date sample collected", "Time collected"],
                     [[x["rand_no"], x["visit"], x["accession_no"], dmy(x["collected"]), x["time"]] for x in rows])


def exposure(R, path):
    rows = sorted(R.dose_edc, key=lambda x: (x["rand_no"], x["admin_date"], x["drug"]))
    return write_csv(path, ["Subject", "Visit", "Treatment", "Date administered", "Dose administered", "Unit"],
                     [[x["rand_no"], x["visit"], x["drug"], dmy(x["admin_date"]), ("%.0f" % x["dose"]), x["unit"]] for x in rows])


def irt_admin(R, path):
    rows = sorted(R.dose_irt, key=lambda x: (x["dispensed"], x["rand_no"], x["kit_no"]))
    return write_csv(path, ["Randomisation Number", "Site", "Visit", "Kit Number", "Transaction Date", "Kit Status"],
                     [[x["rand_no"], x["site_id"], x["visit"], x["kit_no"], iso(x["dispensed"]), x["status"]] for x in rows])


def sites(R, path):
    out = {"trial": "TALON-2", "sponsor": "University of Kesterton", "coordinating_centre": "Kesterton University Cancer Trials Unit",
           "sites": [{"site": s["site_id"], "country": s["country"], "city": s["city"], "time_zone": RC.TZ[s["city"]],
                      "activated": (R.w.fpi + dt.timedelta(days=int(s["activation"]) - 7)).isoformat(),
                      "central_laboratory": "Halden Bioanalytical, Melbourne" if s["code"] in ("AU", "NZ") else "Halden Bioanalytical, Edinburgh"}
                     for s in R.w.sites]}
    open(path, "w").write(json.dumps(out, indent=2) + "\n")
