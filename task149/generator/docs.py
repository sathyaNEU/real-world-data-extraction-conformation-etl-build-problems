"""The governing documents and the notes: Ostrander's OSHA recordkeeping procedure EHS-RK-01, the draft Lindqvist
programme agreement (the estimand's filing), the export notes and the export manifest."""
from __future__ import annotations

import csv
import datetime as dt
import io
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import common as K
import world as WD

F_PROC = "EHS-RK-01_osha_recordkeeping_procedure_rev7.pdf"
F_AGREE = "lindqvist_program_agreement_fy2027_draft.pdf"
F_NOTES = "export_notes.txt"
F_MANIFEST = "folder_index_2026-11-02.csv"

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=12.2, alignment=TA_LEFT, spaceAfter=4)
HEAD = ParagraphStyle("head", fontName="Helvetica-Bold", fontSize=10.2, leading=13, spaceBefore=6, spaceAfter=3)
TITLE = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4)
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#333333"))


def _pdf(path, story, title, author, subject, stamp):
    def on_page(c, d):
        c.setFont("Helvetica", 7.5)
        c.drawString(0.75 * inch, 0.5 * inch, "%s  |  page %d" % (subject, d.page))

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.75 * inch,
                            bottomMargin=0.75 * inch, title=title, author=author, subject=subject, creator=author,
                            producer=author, invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    fix_pdf(path, stamp)


def fix_pdf(path, stamp):
    """The writer's comment line and the fixed invariant-mode dates replaced at equal byte length (the xref offsets
    stay valid): the comment's text after its marker, the dates by the document's own save time."""
    b = open(path, "rb").read()

    def same_length(m):
        rep = b"Document management export"
        return (rep + b" " * len(m.group(0)))[:len(m.group(0))]

    b = re.sub(rb"ReportLab [Gg]enerated PDF document[^\n]*", same_length, b)
    old = b"D:20000101000000+00'00'"
    new = ("D:%s+00'00'" % stamp.strftime("%Y%m%d%H%M%S")).encode()
    assert len(old) == len(new)
    b = b.replace(old, new)
    assert b"ReportLab" not in b and b"reportlab" not in b
    with open(path, "wb") as f:
        f.write(b)


def write_procedure(W, out):
    s = []
    s.append(Paragraph("Ostrander Logistics - Environmental Health and Safety", SMALL))
    s.append(Paragraph("EHS-RK-01 OSHA Injury and Illness Recordkeeping", TITLE))
    s.append(Paragraph("Revision 7, effective 01/01/2025. Owner: Director, Environmental Health and Safety. Supersedes revision 6 (07/01/2024).", SMALL))
    s.append(Spacer(1, 6))
    secs = [
        ("1 Purpose", ["How Ostrander distribution centers record work-related injuries and illnesses on OSHA Forms 300, 300A and 301 under 29 CFR Part 1904, and where the records are kept."]),
        ("2 Scope", ["Every Ostrander distribution center (DC). Each DC is a separate establishment and keeps its own OSHA 300 Log. The DC safety coordinator maintains the log; the DC general manager certifies the annual summary."]),
        ("3 What is recorded", [
            "3.1 A case is recorded when a work-related injury or illness results in death, days away from work, restricted work or transfer to another job, medical treatment beyond first aid, loss of consciousness, or a significant injury or illness diagnosed by a physician or other licensed health care professional (1904.7). First aid alone is not recorded; the EHS system keeps first-aid cases with the classification First Aid.",
            "3.2 Each recorded case is classified by its most serious outcome: days away from work, job transfer or restriction, or other recordable case.",
            "3.3 Temporary associates supplied by a staffing agency and supervised day to day by Ostrander are recorded on the log of the DC where they work (1904.31).",
            "3.4 Injuries and illnesses are both recorded. Illnesses are entered by the Form 300 illness type (skin disorder, respiratory condition, poisoning, hearing loss, all other illnesses)."]),
        ("4 Dates", [
            "4.1 Enter a recordable case within seven calendar days of receiving information that it occurred (1904.29(b)(3)).",
            "4.2 A case is entered on the log of the year in which the injury occurred or the illness began, under its date of injury or onset."]),
        ("5 Privacy cases", ["For a privacy concern case the associate's name is withheld on the log (1904.29(b)(6) to (9)); the case is otherwise entered as any other and counts as any other."]),
        ("6 Work-relatedness", ["If a recorded case is later determined not to be work-related, the coordinator changes its status to Removed - not work-related with the reason. The case stays in the EHS system and comes off the log."]),
        ("7 System of record", ["Cases with a date of injury up to 06/30/2024 are in the legacy incident database. Cases from 07/01/2024 are in the EHS platform. Cases open on 06/30/2024 were migrated to the platform with platform case numbers; the platform keeps the legacy case number as the legacy reference. Closed cases were not migrated."]),
        ("8 Rates", ["A DC's recordable case rate is its recordable cases x 200,000 / total hours worked. Hours worked are the workforce-management system's hours for every department and pay code, agency associates' hours included."]),
        ("9 Counting days", ["Days away from work and days of job transfer or restriction are calendar days, counted from the day after the injury or the onset of the illness, whether or not the associate was scheduled to work. The count ends when the associate returns to full duty or leaves employment, or when the days away and the days of transfer or restriction together reach 180 (1904.7(b)(3) and (4)). Status changes are recorded by the return-to-work program's case managers; the coordinator updates the counts on the case."]),
        ("10 Annual summary", ["Form 300A for each DC covers the calendar year, is certified by the DC general manager, posted from February 1 to April 30, and submitted to OSHA's Injury Tracking Application by March 2."]),
    ]
    for h, paras in secs:
        s.append(Paragraph(h, HEAD))
        for p in paras:
            s.append(Paragraph(p, BODY))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Revision history: rev 6 (07/01/2024) added section 7 for the EHS platform go-live; rev 7 (01/01/2025) aligned section 9 with the return-to-work program.", SMALL))
    _pdf(os.path.join(out, F_PROC), s, "EHS-RK-01 OSHA Injury and Illness Recordkeeping, rev 7", K.ORG, "EHS-RK-01 rev 7",
         dt.datetime(2024, 12, 18, 9, 30, 15))


def write_agreement(W, out):
    info = W.dcs.set_index("dc_no")
    s = []
    s.append(Paragraph("Draft for signature, 10/29/2026", SMALL))
    s.append(Paragraph("Ergonomics Program Services Agreement - Fiscal 2027", TITLE))
    s.append(Paragraph("between Ostrander Logistics, LLC (Client) and Lindqvist Ergonomics Group, Inc. (Lindqvist)", BODY))
    s.append(Spacer(1, 4))
    secs = [
        ("1 Services", ["Lindqvist delivers its ergonomics program at the Program Sites in Schedule A: job and slot assessments, lift assists at heavy-case slots, job rotation design, and coaching for selectors, loaders and receivers, with a monthly report to Client's Director, Environmental Health and Safety."]),
        ("2 Term", ["Client's fiscal 2027, Sunday 12/27/2026 to Saturday 12/25/2027."]),
        ("3 Fees", ["Client pays the Program Fee in Schedule B in twelve equal installments, one per Client fiscal period, net 30."]),
        ("4 Client data", ["Client provides by 12/04/2026, for each Program Site: its fiscal 2026 recordable cases with their days away from work, job transfer or restriction to 10/31/2026; and its fiscal 2026 cases picked, by item, to 10/31/2026, with item weights. Lindqvist uses Client data for program design only."]),
        ("5 Confidentiality", ["Each party keeps the other's information confidential for three years after the Term."]),
    ]
    for h, paras in secs:
        s.append(Paragraph(h, HEAD))
        for p in paras:
            s.append(Paragraph(p, BODY))
    s.append(Paragraph("Schedule A - Program Sites", HEAD))
    data = [["DC", "Site", "City", "State"]]
    for dn in sorted(W.prog):
        no = WD.RECODE_NEW_NO if dn == WD.RECODE_DC else dn
        data.append([str(no), info.ehs_site[dn], info.city[dn], info.state[dn]])
    t = Table(data, colWidths=[0.6 * inch, 2.1 * inch, 1.8 * inch, 0.6 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.5)]))
    s.append(t)
    s.append(Paragraph("Schedule B - Program Fee", HEAD))
    for p in [
        "B1 The Program Fee is USD 2,140 per Forecast Recordable Case.",
        "B2.1 Forecast Recordable Cases means the number of recordable cases that Client expects the Program Sites to enter on their OSHA 300 Logs with a date of injury or illness in Client's fiscal 2027.",
        "B2.2 The forecast is made on Client's FY2027 operating plan for the Program Sites as approved before signing, on the plan's volumes and labor hours for each site and fiscal period.",
        "B2.3 The forecast is Client's expected value, rounded to the nearest hundred cases, and is entered in this Schedule at signing: Forecast Recordable Cases ________.",
        "B3 After the Term, Lindqvist's program review compares the Forecast Recordable Cases with the recordable cases the Program Sites entered on their fiscal 2027 OSHA 300 Logs. No fee is adjusted on the comparison.",
    ]:
        s.append(Paragraph(p, BODY))
    s.append(Spacer(1, 10))
    s.append(Paragraph("For Lindqvist: Tracy Curtis, Account Director. For Client: Director, Environmental Health and Safety; Procurement.", SMALL))
    _pdf(os.path.join(out, F_AGREE), s, "Ergonomics Program Services Agreement FY2027 (draft)", "Lindqvist Ergonomics Group",
         "Lindqvist - Ostrander FY2027 draft", dt.datetime(2026, 10, 29, 16, 12, 4))


NOTES = """EXPORT NOTES - folder for the FY2027 ergonomics program forecast
Built 11/02/2026 by Safety Analytics (J. Delgado). Source systems as listed in folder_index_2026-11-02.csv.

ehs_legacy_case_export_fy21_2024-06-30.csv  (legacy incident database, one row per case)
  CASE_NO            legacy case number: location code - two-digit year - sequence
  ESTABLISHMENT      the DC's establishment name on its OSHA log
  INCIDENT_DATE      date of injury or onset, MM/DD/YYYY, DC local
  INCIDENT_TIME      HH:MM, DC local, 24-hour
  EMPLOYEE_NO        associate number (A = Ostrander, T = agency); names removed for this extract
  EMPLOYER           Ostrander Logistics or the staffing agency
  DEPT               RCV PUT SEL LOD (direct), INV MNT SAN TRN (indirect)
  CLASSIFICATION     FIRST AID or RECORDABLE
  OSHA_CASE_TYPE     DAYS AWAY / RESTRICTED-TRANSFER / OTHER RECORDABLE (recordable cases)
  INJURY_ILLNESS     INJURY or the Form 300 illness type
  EVENT_CODE..BODY_PART  OIICS 2.01 event code and title, nature, part of body
  DAYS_AWAY, DAYS_RESTRICTED   the log's day counts as held at 06/30/2024
  CASE_STATUS        OPEN / CLOSED / NOT WORK RELATED
  PRIVACY_CASE       Y/N
  DATE_ENTERED       date the case was entered, MM/DD/YYYY

ehs_platform_cases_2024-07-01_2026-11-02.json  (EHS platform, full case extract incl. migrated cases)
  case_id                         platform case number
  legacy_case_ref                 legacy CASE_NO for cases migrated at go-live, else null
  site.site_code / establishment  DC number as DCnnn / establishment name
  occurred_at, reported_at        UTC (ISO 8601, Z)
  person.associate_no, employer, job_title, department
  classification.category         Recordable or First Aid; osha_case_type; injury_illness_type
  oiics.*                         OIICS 2.01 event code and title, nature, body part
  osha_log.days_away_from_work, days_job_transfer_restriction, days_last_updated, privacy_case
  status                          Open / Closed / Removed - not work-related

wfm_hours_by_dept_week_fy21_fy26.csv  (workforce-management system, weekly labor hours)
  DC_NO, FISCAL_YEAR, FISCAL_WEEK, WEEK_ENDING (Saturday), DEPT
  REG_HRS, OT_HRS   hours paid to Ostrander associates, regular and overtime
  AGY_HRS           agency associates' hours badged through the WFM system
  Fiscal years end on the last Saturday of December; FY2022 has 53 weeks. Rockford is DC 311 to FY2025 week 13 and
  DC 318 from week 14.

wms_cases_shipped_by_category_week.parquet  (WMS, weekly throughput)
  loc_code, fiscal_year, fiscal_week, category_code, cases_shipped
  Category codes from FY2023 week 27: AMB, CHL, FRZ, HVB. Before: DRYG, PERI, FROZ, BULK (item hierarchy v4 to v5).
  Rockford is RKF1 to FY2025 week 13 and RKF2 from week 14.

rtw_work_status_log_fy2026.csv  (return-to-work program, case management system; files opened from 12/28/2025)
  RTW_CASE_ID, EHS_CASE_NO (platform case number where the file was opened from an EHS case), ASSOCIATE_NO,
  HOME_DC (the associate's home DC), STATUS (AWAY, RESTRICTED, TRANSFER, TRANSFER OUT, FULL DUTY, SEPARATED),
  EFFECTIVE_DATE (first day of the status), ENTERED_ON, CASE_MANAGER, NOTE

wms_item_master_2026-11-01.csv  (WMS item master, each SKU with the item it carries now)
  SKU, DESCRIPTION, CATEGORY, CASE_WEIGHT, CASE_CUBE_FT3, WEIGHT_SOURCE (CUBISCAN, BUYER, PORTAL),
  SETUP_DATE, STATUS (ACTIVE, DISCONTINUED)
  CASE_WEIGHT        CUBISCAN and BUYER weights in lb; PORTAL weights load as the vendor supplies them, kg since
                     portal onboarding (03/03/2025)
wms_item_master_history.csv  (every item version with its effective dates)
wms_sku_picks_fy2026_p01_p11.parquet  (program DCs, cases picked by SKU and fiscal period; period 11 = week 44 only)
"""


def write_notes(out):
    with open(os.path.join(out, F_NOTES), "w", newline="\n", encoding="utf-8") as f:
        f.write(NOTES)


def write_manifest(out, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["file", "source_system", "pulled", "covers", "owner"])
    for r_ in rows:
        w.writerow(r_)
    with open(os.path.join(out, F_MANIFEST), "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
