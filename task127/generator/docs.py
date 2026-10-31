"""The documents: the board's Winter Discharge Fund 2026/27 allocation note."""
import io

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate

import core
import postprocess as PP

GUIDANCE = [
    ("t", "Winter Discharge Fund 2026/27: discharge-to-assess packages"),
    ("s", "Allocation note SF-2026-14. Issued 28 September 2026 by Lauren Simpson, Deputy Director of Finance, for the "
          "system coordination centre, the two acute trusts and Marchshire County Council."),
    ("h", "1. The fund"),
    ("p", "The board's winter discharge fund for 2026/27 buys 1,200 discharge-to-assess packages from the providers on "
          "Marchshire County Council's home care framework, under the council's call-off contract. The packages run "
          "from 1 December 2026 to 28 February 2027."),
    ("h", "2. What a package is"),
    ("p", "A discharge-to-assess package is up to four weeks of home care from a framework provider, available from "
          "the day a patient is medically optimised for discharge, so that waiting for a care provider to start does "
          "not keep the patient in hospital. The patient's longer-term care needs are assessed at home while the "
          "package runs, by the council's reablement and social work teams. Each package is used once, for one "
          "patient's discharge."),
    ("h", "3. Who the fund covers"),
    ("p", "Patients aged 65 and over discharged from Royal Marchford Hospital, Wendlebury Hospital, Ashby Vale "
          "Hospital, Cleeve Park Hospital or Holmford Infirmary on discharge pathway 1 who need a new package of home "
          "care to go home and who are registered with a general practice in Marchshire. A patient whose existing "
          "package of care restarts when they go home does not need a new package and is not covered."),
    ("h", "4. How the packages are split"),
    ("p", "The split is sized on last winter. For each hospital the board takes the patients the fund would have "
          "covered who were medically optimised for discharge from 1 December 2025 to 28 February 2026."),
    ("p", "Each hospital's packages are valued at the average, over those patients, of the number of nights by which "
          "a package would have shortened their stay."),
    ("p", "No hospital receives more packages than it had of those patients."),
    ("p", "The 1,200 packages are split between the hospitals to free as many occupied bed-days as possible. The "
          "occupied bed-days a hospital's packages free are its packages times their value; values are carried "
          "unrounded and the bed-days rounded to whole bed-days."),
    ("h", "5. Call-off and use"),
    ("p", "The board names each hospital's packages in the call-off to the framework providers by 30 October 2026. At "
          "each hospital, packages are offered to covered patients in the order they become medically optimised, "
          "until the hospital's packages are used. Packages a hospital has not used by 28 February 2027 lapse."),
    ("h", "6. Monitoring"),
    ("p", "The trusts report the packages used each week to the system coordination centre alongside the national "
          "discharge collection. The board reviews the split at the end of January 2027."),
    ("p", "Delayed discharge is reported as the national discharge collection counts it: a night a patient spends in "
          "hospital after their discharge ready date is dated to the evening it begins, and a patient counts as "
          "delayed in a month when at least one such night falls in it."),
    ("p", "The council reports the brokerage's waits for home care in calendar days, from the day the brokerage "
          "receives a referral to the day the provider's care starts, by the month the referral was received."),
]


def _styles():
    ss = getSampleStyleSheet()
    blue = colors.HexColor("#005EB8")
    return dict(
        body=ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=13.5, spaceAfter=7),
        head=ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                            spaceAfter=3, spaceBefore=6, textColor=blue),
        title=ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=19,
                             spaceAfter=5),
        small=ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica-Oblique", fontSize=8.8, leading=11.5,
                             spaceAfter=12),
        lh=ParagraphStyle("lh", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10, leading=12,
                          textColor=blue, alignment=2),
        lh2=ParagraphStyle("lh2", parent=ss["Normal"], fontName="Helvetica", fontSize=8.5, leading=10.5,
                           textColor=blue, alignment=2, spaceAfter=16),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(2.0 * cm, 1.2 * cm, text)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def guidance_pdf(path):
    st = _styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=1.6 * cm,
                            bottomMargin=2.0 * cm, title="Winter Discharge Fund 2026/27: discharge-to-assess packages",
                            author="System Flow, NHS Marchshire ICB", creator="System Flow, NHS Marchshire ICB",
                            producer="System Flow, NHS Marchshire ICB")
    story = [Paragraph(core.ICB, st["lh"]), Paragraph("System Flow, Marchford House, 14 Castle Street, Marchford",
                                                      st["lh2"])]
    for kind, text in GUIDANCE:
        sty = {"t": st["title"], "s": st["small"], "h": st["head"]}.get(kind, st["body"])
        story.append(Paragraph(text, sty))
    foot = _footer("Winter Discharge Fund 2026/27, allocation note SF-2026-14, 28 September 2026")
    doc.build(story, onFirstPage=foot, onLaterPages=foot)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_pdf(path, b"D:20260928101347+01'00'", "System Flow, NHS Marchshire ICB")


def guidance_text():
    return "\n".join(t for _, t in GUIDANCE)


