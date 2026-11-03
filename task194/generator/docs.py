"""The one governing document: Leakage Procedure LP04 rev 3, as the department issues it."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

import world as W
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("Carlito", "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Bold", "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"))

SECTIONS = [
    ("1  Purpose", [
        "This procedure sets how Network Operations reads district metered area night flows each week and where the "
        "leak detection crew is sent. It replaces LP04 rev 2 (March 2024)."]),
    ("2  Areas and periods", [
        "A district metered area (area) is a part of the network supplied through the inlet meters listed for it in "
        "the DMA register. Where an area has more than one inlet meter, its inlet flow is the sum of its meters.",
        "Each allocation compares two sets of nights, the baseline nights and the comparison nights, listed for the "
        "allocation in Appendix B. A night is dated by the date on which its 03:00 falls. Days and months in this "
        "procedure and its records are local calendar days and months."]),
    ("3  Minimum night flow", [
        "An area's minimum night flow for a night is the mean of its inlet flow readings stamped from 03:00 up to but "
        "not including 04:00 local clock time. Its minimum night flow for a set of nights is the mean over those nights. "
        "Flows are worked in cubic metres an hour."]),
    ("4  Night use", [
        "4.1  Legitimate night use is the water customers draw during the night hour. It is part of an area's minimum "
        "night flow and is not leakage.",
        "4.2  Household night use is 1.7 litres an hour for each household property in the DMA register.",
        "4.3  Non-household night use is the metered consumption of the area's logged large users over the same hour, "
        "plus 6.0 litres an hour for each non-household property the register lists as not logged."]),
    ("5  Pressure", [
        "5.1  Leakage varies with pressure. Leakage for a set of nights is normalised to the area's mean pressure at "
        "its average zone night point (AZNP) over the baseline nights' night hour, using a leakage-pressure exponent "
        "N1 of 1.15: normalised leakage = leakage x (baseline AZNP pressure / AZNP pressure) ^ 1.15.",
        "5.2  AZNP pressure is the logger's mean for the night hour, in metres head."]),
    ("6  Crew allocation", [
        "6.1  The leak detection crew is sent for the allocation week to the area whose own leakage rose most between "
        "the baseline nights and the comparison nights. An area's own leakage is the water lost at night from the "
        "area's own mains and service pipes, normalised under 5.1.",
        "6.2  Leakage changes are reported in litres a second."]),
    ("7  Records", [
        "Inlet flows are taken from the SCADA historian, pressures from the AZNP logger export, large user consumption "
        "from the AMR head-end and property counts from the DMA register issue in force at the start of the "
        "baseline nights."]),
]


def build(path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Carlito", fontSize=9.5, leading=12.5, spaceAfter=5)
    h = ParagraphStyle("h", parent=ss["Heading3"], fontName="Carlito-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3)
    t = ParagraphStyle("t", parent=ss["Title"], fontName="Carlito-Bold", fontSize=14, alignment=0)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="LP04 Leakage procedure rev 3", author="Network Operations",
                            subject="Night flow assessment and crew allocation", creator="Microsoft Word",
                            producer="Microsoft: Print To PDF", invariant=1)
    st = [Paragraph("Arnvale Water", body), Paragraph("LP04 Night flow assessment and leak detection crew allocation", t)]
    ctl = Table([["Document", "LP04", "Revision", "3"], ["Owner", "Colin Ward, Leakage Manager", "Issued", "14 September 2026"],
                 ["Review", "September 2027", "Classification", "Internal"]], colWidths=[25 * mm, 62 * mm, 27 * mm, 46 * mm])
    ctl.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Carlito", 8.5), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                             ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke), ("BACKGROUND", (2, 0), (2, -1), colors.whitesmoke)]))
    st += [ctl, Spacer(1, 6)]
    for head, paras in SECTIONS:
        st.append(Paragraph(head, h))
        for p in paras:
            st.append(Paragraph(p, body))
    st.append(Paragraph("Appendix A  Allocation calendar, winter 2026", h))
    st.append(Paragraph("Allocations are made in the week before the crew week, from the export taken on its Tuesday morning.", body))
    st.append(Paragraph("Appendix B  Night sets for the week 46 allocation", h))
    tb = Table([["Allocation", "Crew week", "Baseline nights", "Comparison nights"],
                ["2026-46", "9 to 15 November 2026", "7 September to 4 October 2026", "12 October to 1 November 2026"]],
               colWidths=[24 * mm, 40 * mm, 52 * mm, 52 * mm])
    tb.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Carlito", 8.5), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                            ("FONT", (0, 0), (-1, 0), "Carlito-Bold", 8.5)]))
    st.append(tb)
    doc.build(st)
    reserialise(path, "LP04 Leakage procedure rev 3", "Network Operations")


def reserialise(path, title, author):
    """Rewrite the PDF through pypdf, so the writer's own header comment and producer go, with fixed metadata."""
    from pypdf import PdfReader, PdfWriter
    r = PdfReader(path)
    w = PdfWriter()
    for p in r.pages:
        w.add_page(p)
    w.add_metadata({"/Title": title, "/Author": author, "/Creator": "Microsoft Word",
                    "/Producer": "Microsoft: Print To PDF", "/CreationDate": "D:20260914101200+01'00'",
                    "/ModDate": "D:20260914101200+01'00'"})
    with open(path, "wb") as f:
        w.write(f)
