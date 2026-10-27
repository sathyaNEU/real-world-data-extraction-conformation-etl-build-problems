"""task270 documents: the federation's service specification for 2027-28, the integrated care board's compliance-aid
guidance for prescribers
and pharmacies, and a summary of the national community pharmacy contract (unused by the solution). No file
describes the data: every export names its own columns. The text is kept here as data so checks.py can quote it."""
from __future__ import annotations

import datetime as dt
import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2229")
GREY = colors.HexColor("#5d6570")
NHS = colors.HexColor("#005eb8")
RULE = colors.HexColor("#a5adb6")
HEAD = colors.HexColor("#e8edf2")

F_SPEC = "statin_adherence_support_service_specification_2027-28.pdf"
F_GUIDE = "compliance_aids_prescribing_and_supply_guidance_2025.pdf"
F_CPCF = "community_pharmacy_contractual_framework_summary_2024-26.pdf"


def styles(font, bold, size=10.2):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=6),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15, leading=19, textColor=NHS, spaceAfter=3),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.9, leading=11.8, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.8, leading=14, textColor=NHS, spaceBefore=8,
                          spaceAfter=3),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.8, leading=11, textColor=INK),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.8, leading=11, textColor=INK))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm, topMargin=2.0 * cm,
                             bottomMargin=2.0 * cm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="LibSans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(2.1 * cm, 1.2 * cm, left)
        canvas.drawRightString(A4[0] - 2.1 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def grid(rows, widths, st):
    data = [[Paragraph(esc(str(c)), st["cellb"] if k == 0 else st["cell"]) for c in row] for k, row in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("TOPPADDING", (0, 0), (-1, -1), 2.6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ---------------------------------------------------------------------------------------------- the specification
SPEC = [
    ("1. Purpose", [
        "1.1 Statins lower the risk of a heart attack or stroke only while they are taken. Many older patients collect "
        "their statin less often than their prescription needs, and the federation's pilot in Krathwold and "
        "Lathcombe, from October 2025 to September 2026, found that a conversation with a community pharmacist helps a patient who has fallen behind to start "
        "taking it again.",
        "1.2 From 1 April 2027 to 31 March 2028 the federation contracts community pharmacies to contact the patients this "
        "specification describes and offer them a consultation, and funds an enhanced tier in the primary care networks "
        "where the largest shares of those patients have fallen behind."]),
    ("2. Who the service is for", [
        "2.1 The service's population is the patients who, on 31 December 2026, were registered with one of the federation's member "
        "practices, were aged 65 or over (born in 1961 or earlier), had two or more statin items dispensed by a "
        "community pharmacy in 2026 (distance-selling pharmacies included), and collect and take their own statins. Patients living in a care home, and "
        "patients whose medicines a pharmacy packs into a compliance aid, are not in the population; their medicines are "
        "reviewed under the structured medication review service (section 7).",
        "2.2 A patient's adherence in 2026 is the proportion of days covered: the share of the days from the date of the "
        "patient's first statin item dispensed in 2026 to 31 December 2026, both included, on which the patient held "
        "statin. Each item covers its quantity divided by the tablets a day its dosage instructions give, or one tablet a "
        "day where they give none (such as \"as directed\"). An item dispensed before the patient's earlier supply has run "
        "out starts when that supply ends. Every statin counts, so a change of statin continues the supply. Items "
        "dispensed before 1 January 2026 are not counted.",
        "2.3 A patient whose proportion of days covered is under 80 per cent has fallen behind."]),
    ("3. The tiers", [
        "3.1 A primary care network is in the enhanced tier when 30 per cent or more of the service's population "
        "registered with its practices had fallen behind in 2026. Each network is read as its practices stood on "
        "31 December 2026.",
        "3.2 Every other network is in the standard tier.",
        "3.3 The federation's board approves the tier schedule before the service starts on 1 April 2027. It issues to "
        "the pharmacies with their service agreements on 1 March 2027 and holds for the service year."]),
    ("4. What pharmacies do", [
        "4.1 The patient's usual community pharmacy contacts each patient in the population who has fallen behind and "
        "offers a first consultation by 30 June 2027, face to face or by video, and a follow-up within six weeks of it.",
        "4.2 In the enhanced tier a pharmacist also holds a weekly session with each practice in the network to work "
        "through the practice's patients who have fallen behind."]),
    ("5. Payment", [
        "5.1 A first consultation is paid at £28 and a follow-up at £14, claimed through the federation's services portal "
        "by the fifth working day of the month after the consultation.",
        "5.2 Each enhanced-tier practice session is paid at £165."]),
    ("6. Data", [
        "6.1 The Iversford Vale Health Data Service, run by NHS Iversford Vale Integrated Care Board, supplies the "
        "community pharmacy dispensing data and the member practices' year-end lipid cohort lists to the federation's "
        "medicines optimisation team, pseudonymised, under the data sharing agreement between the board and the "
        "federation."]),
    ("7. Related services", [
        "7.1 The medicines of patients living in a care home, and of patients whose medicines a pharmacy packs into a "
        "compliance aid, are reviewed at least once a year under the structured medication review service delivered "
        "by each network's clinical pharmacists."]),
]

# ---------------------------------------------------------------------------------------------- the guidance
GUIDE = [
    ("Purpose", [
        "This guidance sets out how the board's practices and community pharmacies should prescribe and supply "
        "medicines for patients who use a compliance aid. It replaces the 2021 guidance."]),
    ("What a compliance aid is", [
        "A compliance aid (sometimes called a blister pack, dosette box or monitored dosage system) holds a patient's "
        "doses in compartments by day and time. A pharmacy that supplies a compliance aid fills it from the patient's "
        "prescriptions and supplies the filled packs; the patient, or a carer, then takes the doses from it.",
        "A compliance aid suits few patients. A pharmacist or practice clinician should first consider simpler help: "
        "large-print labels, easy-open tops, a reminder chart or a review that reduces the number of medicines."]),
    ("Supply", [
        "A pharmacy fills a week of doses in each pack and supplies the packs on the same day of the week for each "
        "patient, so the patient always has the next pack before the last one runs out. Where that day falls on a "
        "bank holiday the packs are supplied on the next day the pharmacy opens.",
        "Prescribers should issue 28-day prescriptions for patients who use a compliance aid. Four 7-day prescriptions "
        "were issued in the past to pay the pharmacy a fee for each week's supply; that is no longer the board's "
        "practice, although some prescriptions issued that way remain in use.",
        "Patients living in a care home receive their medicines on the home's own 28-day cycle, whether in a "
        "compliance aid or in original packs."]),
    ("Recording", [
        "Practices should record that a patient uses a compliance aid on the patient's record, so that the patient's "
        "clinicians and the structured medication review service know of it."]),
    ("Review", [
        "Every patient who uses a compliance aid should have a structured medication review at least once a year."]),
]

CPCF = [
    ("Essential services", [
        "Dispensing, repeat dispensing and electronic repeat dispensing, disposal of unwanted medicines, promotion of "
        "healthy lifestyles, signposting, support for self-care and the discharge medicines service."]),
    ("Advanced services", [
        "The New Medicine Service supports patients newly prescribed a medicine for a long-term condition, including "
        "a statin for raised cholesterol, through an engagement, an intervention and a follow-up over about five "
        "weeks.",
        "Other advanced services include the hypertension case-finding service, the contraception service, the "
        "flu vaccination service and Pharmacy First."]),
    ("Locally commissioned services", [
        "Integrated care boards may commission further services from community pharmacies under local terms, paid "
        "outside the national framework."]),
]


def _write(path, title, org, author, issued, paras_by_section, footer):
    st = styles("LibSans", "LibSans-Bold")
    doc = _doc(path, title, author)
    flow = [Paragraph(esc(title), st["h1"]),
            Paragraph(esc("%s. %s. Issued %s." % (org, author, K.uk_date(issued))), st["sub"])]
    for head, paras in paras_by_section:
        flow.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    doc.build(flow, onFirstPage=_footer(footer), onLaterPages=_footer(footer))


def write_all():
    os.makedirs(K.TARGET, exist_ok=True)
    _write(os.path.join(K.TARGET, F_SPEC), "Statin Adherence Support Service: service specification 2027-28",
           K.FEDERATION, "Medicines Optimisation Team", K.SPEC_DATE, SPEC,
           "Statin Adherence Support Service specification 2027-28, version 1.0")
    _write(os.path.join(K.TARGET, F_GUIDE), "Compliance aids: prescribing and supply",
           K.ICB, "Medicines Optimisation Team", K.GUIDANCE_DATE, GUIDE, "Compliance aids guidance, June 2025")
    _write(os.path.join(K.TARGET, F_CPCF), "The community pharmacy contractual framework 2024-26: a summary",
           K.ICB, "Primary Care Contracting", dt.date(2024, 9, 30),
           CPCF, "Community pharmacy contractual framework summary")
    return [F_SPEC, F_GUIDE, F_CPCF]
