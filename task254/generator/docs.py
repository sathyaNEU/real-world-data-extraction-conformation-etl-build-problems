"""Controlled documents in the pack: RMP annex 7 (methods), the safety export field guide, the PSUR section 5
exposure method note, and the data package log."""
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

AUTHOR = "Lasse Christoffersen"

ANNEX = [
    ("title", "Lyrevo (RVB-417) Risk Management Plan, Annex 7"),
    ("sub", "Methods for characterising the important identified risks from post-marketing data"),
    ("meta", [["Document", "RVB-417-RMP-A7"], ["Version", "3.0"], ["Effective", "24 August 2026"],
              ["Prepared by", "Lasse Christoffersen, Safety Data Lead, Drug Safety and Pharmacovigilance"],
              ["Approved", "EU QPPV, Ravnsborg Pharma A/S"], ["Applies to", "RMP Part II SVII and Part V; PSUR from DLP 30 September 2026"]]),
    ("h", "Purpose"),
    ("p", "This annex fixes how Drug Safety derives, from the company safety database, the figures the RMP states for each "
          "important identified risk of Lyrevo: the time to onset of the risk's reactions, the routine monitoring windows, "
          "and the reporting rates. It replaces version 2.1 and applies from the PSUR with data lock point 30 September 2026."),
    ("h", "1  Case population"),
    ("p", "1.1  The analyses use the individual case safety reports for Lyrevo held in the company safety database "
          "(Argus Safety) at the data lock point (DLP) of the periodic safety update report."),
    ("p", "1.2  Each case is used as it stood at the DLP: the version of record is the latest version received on or "
          "before the DLP. Cases first received after the DLP are not used."),
    ("p", "1.3  Post-marketing cases are used: spontaneous reports, solicited reports (including the Lyrevo patient "
          "support programme) and literature reports. Reports from interventional or non-interventional studies, "
          "including the post-authorisation safety registry RVB-417-4103, are summarised in PSUR section 7 and are not "
          "used here."),
    ("h", "2  Case unit and safety concerns"),
    ("p", "2.1  Reports of the same patient and event that Case Processing has linked in the duplicate management "
          "register are one case, represented by the master case of the link."),
    ("p", "2.2  A reaction belongs to an identified risk when its MedDRA preferred term is mapped to that risk in the RMP "
          "term list in force at the DLP."),
    ("p", "2.3  Each case contributes one reaction to each identified risk it reports: the reaction with the earliest "
          "onset among the case's reactions mapped to the risk."),
    ("h", "3  Time to onset"),
    ("p", "3.1  Time to onset is counted in days of the treatment course in which the reaction began. The first dose of "
          "that course is day 1, so a reaction that begins on the day of the first dose has a time to onset of 1 day."),
    ("p", "3.2  A treatment course is a period of dosing with Lyrevo with no gap of more than 28 days. The gap is the "
          "number of days without a dose between the stop date of one dosage line and the start date of the next. A "
          "change of dose or of tablet strength does not start a new course. Courses are built from the dosage lines held "
          "for the case."),
    ("p", "3.3  Months of treatment are 30-day months counted from day 1: month 1 is days 1 to 30, month 2 is days 31 to "
          "60, and so on."),
    ("p", "3.4  A reaction is used for time to onset only when its onset date and the start date of its course are "
          "complete (day, month and year). Partial dates are not imputed."),
    ("h", "4  Reactions identified from a laboratory value"),
    ("p", "4.1  Solicited reports from the patient support programme's laboratory monitoring may report hepatotoxicity "
          "or neutropenia without an onset date, the reaction having been identified from a laboratory result transferred "
          "by the programme's contracted laboratory."),
    ("p", "4.2  For these reactions the onset date is the date of the first sample meeting the case definition: alanine "
          "aminotransferase above three times the upper limit of normal of the reporting laboratory for the patient's "
          "sex, or an absolute neutrophil count below 1.0 x 10^9/L. Units and reference limits are those of the PSP "
          "laboratory register."),
    ("h", "5  Monitoring windows"),
    ("p", "5.1  For each important identified risk the RMP states two windows: the first month of treatment by the end of "
          "which at least 80 per cent of the risk's reactions in treated patients have begun (the period of intensified "
          "monitoring), and the first month by the end of which at least 95 per cent have begun (the end of routine "
          "monitoring for the risk)."),
    ("p", "5.2  The windows are estimated from the post-marketing time to onset data of section 3 and section 4 without "
          "fitting a parametric model, and are stated in whole months of treatment."),
    ("h", "6  Reporting rates"),
    ("p", "6.1  A reporting rate is the number of cases reporting the risk per 1,000 patient-years of exposure, from launch "
          "(3 April 2023) to the DLP and for the PSUR reporting interval (1 October 2025 to 30 September 2026). A case "
          "counts in the interval when it was first received in the interval."),
    ("p", "6.2  Exposure is estimated as described in PSUR section 5."),
    ("h", "Change history"),
    ("table", [["Version", "Date", "Change"],
               ["1.0", "14 Feb 2023", "First issue with the initial RMP"],
               ["2.0", "19 Sep 2024", "Section 4 added for patient support programme laboratory monitoring"],
               ["2.1", "3 Apr 2025", "Duplicate handling aligned with the Case Processing register (section 2.1)"],
               ["3.0", "24 Aug 2026", "Monitoring windows at 80 and 95 per cent (section 5); term list v4 referenced"]]),
]

FIELD_GUIDE = [
    ("title", "Safety database export for the PSUR data package"),
    ("sub", "Field guide: line listing, dosage lines and patient support programme laboratory feed"),
    ("meta", [["Document", "DS-FG-021"], ["Version", "4"], ["Owner", "Lasse Christoffersen, Drug Safety"],
              ["Systems", "Argus Safety 8.4; PSP vendor laboratory transfer"]]),
    ("h", "Line listing (lyrevo_line_listing_PSUR6_DLP20260930.csv)"),
    ("p", "One row per reaction on each version of each Lyrevo case. The export holds every version of every case "
          "received up to the run of the export query, follow-ups included."),
    ("fields", [
        ["case_no", "Company case number: year of first receipt, RAV, sequence"],
        ["version_no", "Version of the case; each follow-up received creates the next version"],
        ["version_receipt_date", "Date the company received the information in this version"],
        ["initial_receipt_date", "Date the company first received the case"],
        ["report_type", "SP spontaneous; SO solicited (patient support programme, market research); LI literature; "
                        "ST study (interventional or non-interventional, registries included)"],
        ["primary_source", "Qualification of the primary source: 1 physician, 2 pharmacist, 3 other health "
                           "professional, 5 consumer or other non-health professional"],
        ["country", "Country where the reaction occurred, ISO 3166-1 alpha-2"],
        ["sex", "M or F"],
        ["age_years", "Age at onset in years; blank when not reported"],
        ["therapy_start_date", "Start date of the first Lyrevo dosage line held for the case"],
        ["therapy_stop_date", "Stop date of the last Lyrevo dosage line, as known at this version; blank when "
                              "ongoing or not reported"],
        ["reaction_pt", "Reaction, MedDRA preferred term (MedDRA 29.0)"],
        ["onset_date", "Onset date of the reaction as reported; blank when not reported"],
        ["serious", "Y or N, per reaction"],
        ["seriousness_criteria", "D death, LT life-threatening, H hospitalisation or prolongation, DI disability, "
                                 "CA congenital anomaly, OMI other medically important condition"],
        ["outcome", "Outcome of the reaction as reported; outcome_date where reported"],
        ["action_taken", "Action taken with Lyrevo: WITHDRAWN, INTERRUPTED, DOSE REDUCED, DOSE NOT CHANGED, "
                         "NOT APPLICABLE, UNKNOWN"],
    ]),
    ("p", "Dates are written YYYY-MM-DD. Where the reporter gave only the month or the year, the date is written "
          "YYYY-MM or YYYY."),
    ("h", "Dosage lines (lyrevo_dosage_lines_PSUR6.csv)"),
    ("p", "One row per Lyrevo dosage line held for the case at the run of the export. Lines are numbered in order of "
          "start date."),
    ("fields", [
        ["case_no", "Company case number"],
        ["line_no", "Dosage line number within the case"],
        ["start_date / stop_date", "First and last day of dosing on the line; stop_date blank when the line was "
                                   "ongoing at the latest information or the stop was not reported"],
        ["daily_dose, dose_unit", "Daily dose as reported, in mg or in tablets"],
        ["strength_mg", "Tablet strength of the line, 15 or 30"],
        ["line_end", "How the line ended: DOSE CHANGED (a line at another dose starts the next day), INTERRUPTED "
                     "(dosing paused), DISCONTINUED, ONGOING, UNKNOWN"],
    ]),
    ("h", "PSP laboratory feed (psp_lab_feed_2023-2026.csv)"),
    ("p", "Laboratory results the patient support programme vendor transfers for programme patients who have a "
          "safety case. Results are transferred for samples taken from 120 days before the onset reported to the "
          "vendor to 60 days after the case was first received."),
    ("fields", [
        ["psp_patient_ref", "The vendor's patient reference; one patient, one reference"],
        ["case_no", "Safety case of the patient"],
        ["sample_date", "Date the sample was taken"],
        ["analyte", "ALT alanine aminotransferase; NEUT absolute neutrophil count; LYMPH absolute lymphocyte count"],
        ["value, unit", "Result and unit as reported by the laboratory"],
        ["lab_code", "Reporting laboratory; units and reference limits in psp_laboratory_register.xlsx"],
    ]),
]

SECTION5 = [
    ("title", "PSUR 6, section 5: estimated exposure"),
    ("p", "Lyrevo (RVB-417), film-coated tablets 15 mg and 30 mg. Reporting interval 1 October 2025 to 30 September "
          "2026; cumulative from launch on 3 April 2023. Method note for the exposure tables, prepared by Drug Safety "
          "with Supply Chain Planning and Finance."),
    ("h", "Basis"),
    ("p", "Post-marketing exposure is estimated from the quantities of Lyrevo supplied, because Ravnsborg Pharma holds "
          "no patient-level dispensing data for most markets. The estimate counts every unit supplied for use by "
          "patients, through every channel by which Lyrevo reaches patients in each market."),
    ("h", "Counting rules"),
    ("b", "Supply is counted from launch up to and including the data lock point. For the interval tables, supply in "
          "the reporting interval is counted."),
    ("b", "Invoiced quantities are counted. Returns credited to customers are deducted in the period in which they are "
          "credited."),
    ("b", "Free-of-charge deliveries are supply and are counted: replacement packs and patient support programme "
          "starter packs."),
    ("b", "Quantities are converted to tablets with the number of tablets in each presentation."),
    ("b", "The recommended dose is one tablet daily, so one tablet is one patient-day of exposure for both strengths."),
    ("b", "Patient-years are patient-days divided by 365.25. Patient-years are reported to the nearest 10."),
    ("h", "Presentations"),
    ("p", "EU/1/23/1754/001 to 004. Pack sizes and strengths are those of the authorised presentations as held in the "
          "xEVMPD."),
    ("h", "Sources"),
    ("p", "Supply records as extracted for the PSUR data package; the market supply channel overview maintained by "
          "Supply Chain Planning describes which channel serves each market and from when."),
]


def _styles():
    ss = getSampleStyleSheet()
    return dict(
        title=ParagraphStyle("t", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=14.5, leading=18, alignment=0,
                             spaceAfter=2),
        sub=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=10.5, leading=13, spaceAfter=8,
                           textColor=colors.HexColor("#333333")),
        h=ParagraphStyle("h", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=8,
                         spaceAfter=3),
        p=ParagraphStyle("p", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=12.4, spaceAfter=4),
        b=ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=12.4, spaceAfter=3,
                         leftIndent=10, bulletIndent=0),
        small=ParagraphStyle("sm", parent=ss["Normal"], fontName="Helvetica", fontSize=8.2, leading=10.2),
    )


def _footer(label):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, "Ravnsborg Pharma A/S  |  %s  |  Confidential" % label)
        canvas.drawRightString(192 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _story(spec, st):
    out = []
    for kind, val in spec:
        if kind in ("title", "sub", "h", "p"):
            out.append(Paragraph(val, st[kind]))
        elif kind == "b":
            out.append(Paragraph(val, st["b"], bulletText="•"))
        elif kind == "meta":
            t = Table(val, colWidths=[30 * mm, 140 * mm])
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4),
                                   ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.4),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 1),
                                   ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#999999"))]))
            out += [t, Spacer(1, 6)]
        elif kind in ("table", "fields"):
            rows = [[Paragraph(c, st["small"]) for c in r] for r in val]
            widths = [22 * mm, 26 * mm, 122 * mm] if kind == "table" else [44 * mm, 126 * mm]
            t = Table(rows, colWidths=widths, repeatRows=1 if kind == "table" else 0)
            sty = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#bbbbbb")),
                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]
            if kind == "table":
                sty.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")))
            t.setStyle(TableStyle(sty))
            out += [t, Spacer(1, 5)]
    return out


def pdf(path, spec, label, title):
    st = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=AUTHOR, subject=title,
                            creator="Ravnsborg Pharma Document Control", producer="Ravnsborg Pharma Document Control")
    doc.build(_story(spec, st), onFirstPage=_footer(label), onLaterPages=_footer(label))


def annex_pdf(path):
    pdf(path, ANNEX, "RVB-417-RMP-A7 v3.0", "RVB-417 RMP Annex 7")


def field_guide_pdf(path):
    pdf(path, FIELD_GUIDE, "DS-FG-021 v4", "Safety export field guide")


def section5_docx(path):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for kind, val in SECTION5:
        if kind == "title":
            d.add_heading(val, level=1)
        elif kind == "h":
            d.add_heading(val, level=2)
        elif kind == "p":
            d.add_paragraph(val)
        elif kind == "b":
            d.add_paragraph(val, style="List Bullet")
    cp = d.core_properties
    cp.author = AUTHOR
    cp.last_modified_by = AUTHOR
    cp.title = "PSUR 6 section 5 exposure method"
    cp.comments = ""
    cp.subject = ""
    cp.keywords = ""
    cp.category = ""
    cp.created = dt.datetime(2026, 9, 21, 9, 14, 0)
    cp.modified = dt.datetime(2026, 10, 5, 15, 2, 0)
    cp.revision = 7
    d.save(path)
