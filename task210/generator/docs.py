"""The governing document: Lindmarsh Water's procedure WW-ENV-PR-014 for storm overflow event duration monitoring,
the annual return and self-reporting. It files what the organisation itself defines (the reporting year, how
spills are counted, duration, monitor operational time, the dry-day annex, when a breach is self-reported) and
nothing about how a pumping station's pass forward flow is established."""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether, PageTemplate, Paragraph, Spacer, Table,
                                TableStyle)

import pack
import world as W

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.5, leading=12.6, alignment=TA_LEFT, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=6, textColor=colors.HexColor("#0B3D5C"))
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3,
                    textColor=colors.HexColor("#0B3D5C"))
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8.5, leading=10.5)
SMALLB = ParagraphStyle("smallb", fontName="Helvetica-Bold", fontSize=8.5, leading=10.5)


def cells(rows, bold_cols=(), bold_row0=False):
    out = []
    for i, r in enumerate(rows):
        out.append([Paragraph(str(v), SMALLB if (j in bold_cols or (bold_row0 and i == 0)) else SMALL)
                    for j, v in enumerate(r)])
    return out

DOC_NO = "WW-ENV-PR-014"
PAGES = [1]
REV = "4"
ISSUED = "03/11/2025"


def _frame(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(colors.HexColor("#0B3D5C"))
    canvas.rect(0, h - 18 * mm, w, 18 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(18 * mm, h - 11.5 * mm, W.COMPANY_SHORT)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawRightString(w - 18 * mm, h - 11.5 * mm, "Wastewater Environmental Compliance")
    canvas.setFillColor(colors.black)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18 * mm, 11 * mm, "%s  Rev %s  Issued %s  Uncontrolled when printed" % (DOC_NO, REV, ISSUED))
    canvas.drawRightString(w - 18 * mm, 11 * mm, "Page %d of %d" % (doc.page, PAGES[0]))
    canvas.restoreState()


def procedure(path):
    import io
    pack.ensure(path)
    buf = io.BytesIO()
    n = _procedure(buf)
    PAGES[0] = n
    _procedure(path)


def _procedure(path):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=26 * mm,
                          bottomMargin=20 * mm, title="Storm overflow event duration monitoring, annual return and self-reporting",
                          author=W.PEOPLE["compliance"], subject=DOC_NO, creator="", producer="", invariant=1)
    fr = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[fr], onPage=_frame)])
    s = []
    s.append(Paragraph("Storm overflow event duration monitoring: annual return and self-reporting", H1))
    meta = [["Document", DOC_NO, "Revision", REV],
            ["Owner", "%s, Wastewater Environmental Compliance Manager" % W.PEOPLE["compliance"], "Issued", ISSUED],
            ["Applies to", "Storm overflows on the wastewater network fitted with event duration monitors", "Next review", "11/2027"]]
    t = Table(cells(meta, bold_cols=(0, 2)), colWidths=[24 * mm, 92 * mm, 22 * mm, 34 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.5),
                           ("FONT", (2, 0), (2, -1), "Helvetica-Bold", 8.5), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF2F7")),
                           ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#EEF2F7"))]))
    s += [t, Spacer(1, 6)]
    s.append(Paragraph("1. Purpose", H2))
    s.append(Paragraph(
        "This procedure sets out how the company compiles the annual event duration monitoring (EDM) return for its "
        "storm overflows to the %s, and when a storm overflow's discharges are self-reported as a breach of its "
        "permit. It applies to every storm overflow on the wastewater network whose permit requires event duration "
        "monitoring." % W.REGULATOR, BODY))
    s.append(Paragraph("2. Reporting year", H2))
    s.append(Paragraph(
        "The reporting year runs from 00:00 on 1 January to 24:00 on 31 December, UK local time. A discharge is "
        "reported in the year in which it starts.", BODY))
    s.append(Paragraph("3. Counting spills", H2))
    s.append(Paragraph(
        "Spills are counted for each storm overflow by the 12/24 method. Counting begins at the start of the first "
        "discharge. Any discharge in the first 12 hours counts as one spill. Any discharge in each following 24-hour "
        "block counts as one further spill, block by block, for as long as each block contains discharge. When a full "
        "24-hour block passes with no discharge, the next discharge begins a new count.", BODY))
    s.append(Paragraph("4. Duration of discharge", H2))
    s.append(Paragraph(
        "The return states the total duration of discharge from each storm overflow in the reporting year, in hours, "
        "from the start of each discharge to its end, any period of discharge counted once.", BODY))
    s.append(Paragraph("5. Monitor operational time", H2))
    s.append(Paragraph(
        "The return states, for each storm overflow, the percentage of the hours in the reporting year during which "
        "its discharges were being monitored and the monitoring data reached the company. A day for which no "
        "monitoring data reached the company counts as a day with no monitoring.", BODY))
    s.append(Paragraph("6. Dry-day discharges", H2))
    s.append(Paragraph(
        "Discharges that begin on a dry day are listed in the return's dry-day annex with the operating explanation "
        "for each. A dry day is a UK local calendar day on which less than 0.25 mm of rain fell over the overflow's "
        "radar zone and on which the previous day also had less than 0.25 mm.", BODY))
    s.append(Paragraph("7. Permit conditions and self-reporting", H2))
    s.append(Paragraph(
        "Each storm overflow's permit sets the conditions under which it may discharge, and the consents register "
        "holds each permit's conditions as issued. Where a storm overflow has discharged in breach of a condition of "
        "its permit, the Wastewater Environmental Compliance Manager self-reports the breach to the %s with the "
        "annual return, naming the permit, the overflow, the condition breached and the discharges affected." % W.REGULATOR,
        BODY))
    s.append(Paragraph(
        "A self-report names one storm overflow and its permit. Investigation and any repair are raised separately "
        "under the network operations procedures.", BODY))
    s.append(Paragraph("8. Responsibilities", H2))
    resp = [["Role", "Responsibility"],
            ["Wastewater Environmental Compliance Manager", "Compiles and signs the annual EDM return; makes self-reports"],
            ["Network Operations Manager, each area", "Investigates breached overflows; keeps station records current"],
            ["Instrumentation team", "Maintains the EDM monitors and the pumping station outstations"]]
    t2 = Table(cells(resp, bold_row0=True), colWidths=[64 * mm, 108 * mm])
    t2.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2F7")),
                            ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s += [t2, Spacer(1, 8)]
    tail = [Paragraph("9. Revision history", H2)]
    hist = [["Rev", "Date", "Change", "Approved"],
            ["1", "14/02/2019", "First issue", "D. Okoro"],
            ["2", "09/03/2021", "Monitor operational time added to the return", "D. Okoro"],
            ["3", "21/02/2024", "12/24 counting brought in line with the Agency's current guidance", "P. Haddon"],
            ["4", ISSUED, "Dry-day annex added; self-reporting section rewritten", "P. Haddon"]]
    t3 = Table(cells(hist, bold_row0=True), colWidths=[12 * mm, 22 * mm, 108 * mm, 30 * mm])
    t3.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEF2F7"))]))
    tail += [t3, Spacer(1, 10)]
    sig = [["Prepared", "%s, Wastewater Environmental Compliance Manager" % W.PEOPLE["compliance"], "03/11/2025"],
           ["Approved", "P. Haddon, Head of Environmental Regulation", "03/11/2025"]]
    t4 = Table(cells(sig, bold_cols=(0,)), colWidths=[24 * mm, 118 * mm, 30 * mm])
    t4.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.5),
                            ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.grey)]))
    tail.append(t4)
    s.append(KeepTogether(tail))
    doc.build(s)
    return doc.page


def build(tgt, FILES):
    procedure(os.path.join(tgt, FILES["procedure"]))
