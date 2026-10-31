"""The governing document in the pack: the Heat Resilience Fund's allocation terms (the board's paper, with
Table 1)."""
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W  # noqa: E402

NHS_BLUE = colors.HexColor("#005EB8")
SS = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=15, textColor=NHS_BLUE,
                    spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, textColor=NHS_BLUE,
                    spaceBefore=8, spaceAfter=3)
P = ParagraphStyle("p", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
SMALL = ParagraphStyle("s", parent=P, fontSize=8.4, leading=11, textColor=colors.HexColor("#425563"))
CELL = ParagraphStyle("c", parent=P, fontSize=8.4, leading=10.4, spaceAfter=0)


def _stamp(path, when, author):
    """same-length replacements, so the cross-reference offsets stay valid"""
    b = open(path, "rb").read()

    def same(m, new):
        old = m.group(0)
        return new.ljust(len(old))[:len(old)]
    b = re.sub(rb"ReportLab Generated PDF document \(opensource\)",
               lambda m: same(m, b"Microsoft: Print To PDF"), b)
    b = re.sub(rb"ReportLab generated PDF document -- digest \(opensource\)", lambda m: same(m, b"end"), b)
    b = re.sub(rb"\(anonymous\)", lambda m: same(m, b"(" + author.encode()[:9] + b")"), b)
    b = b.replace(b"D:20000101000000+00'00'", when)
    assert b"ReportLab" not in b and b"reportlab" not in b
    open(path, "wb").write(b)


def _table(rows, widths, head=True):
    data = [[Paragraph(str(c), CELL) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#AEB7BD")), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]
    if head:
        st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EDEE"))]
    t.setStyle(TableStyle(st))
    return t


def terms(T, path):
    flow = [Paragraph("NHS Ellesmoor Integrated Care Board", SMALL),
            Paragraph("Heat Resilience Fund 2027: allocation terms", H1),
            Paragraph("Approved by the Board on 24 June 2026 (paper B/26/41). Owner: Director of Population Health.",
                      SMALL), Spacer(1, 6),
            Paragraph("1. Purpose", H2),
            Paragraph("The fund helps the board's six places prepare for summer 2027: cool spaces, check-in calls for "
                      "people who live alone, and small home adaptations for residents at risk in hot weather. It is "
                      "allocated on what summer 2026 cost each place in deaths.", P),
            Paragraph("2. Grants", H2),
            Paragraph("Each qualifying place receives a heat resilience grant of GBP 300,000 for 2027. Every other "
                      "place receives the standard heat-health allocation of GBP 60,000.", P),
            Paragraph("3. Qualifying places", H2),
            Paragraph("A place qualifies when the deaths of its residents from 1 June to 31 August 2026 exceed its "
                      "expected deaths in Table 1 by 10 per cent or more. The excess is the deaths less the expected "
                      "deaths, expressed as a percentage of the expected deaths.", P),
            Paragraph("4. The deaths counted", H2),
            Paragraph("A death is counted for the place of the deceased person's usual address, by the date of death. "
                      "Every death that occurred in the period is counted, whether or not it has been registered by "
                      "the date of the count, and each death is counted once. The count is made from the mortality "
                      "records held by the population health intelligence team at the close of 9 October 2026 and is "
                      "taken to the Board on 26 November 2026.", P),
            Paragraph("5. Expected deaths", H2),
            Paragraph("Table 1 sets each place's expected deaths for 1 June to 31 August 2026: the mean of its "
                      "residents' deaths in the summers of 2021 to 2025, adjusted for population change. Table 1 is "
                      "fixed for this allocation and is not recalculated.", P),
            Spacer(1, 4),
            Paragraph("Table 1. Expected deaths of residents, 1 June to 31 August 2026", ParagraphStyle(
                "cap", parent=P, fontName="Helvetica-Bold", fontSize=9.2))]
    rows = [["Place", "Local authority code", "Expected deaths"]]
    for p in W.NAMES:
        rows.append([p, W.CODE[p], "{:,}".format(T.expected[p])])
    rows.append(["Ellesmoor", "", "{:,}".format(sum(T.expected.values()))])
    flow.append(_table(rows, [5.2 * cm, 4.2 * cm, 3.6 * cm]))
    flow += [Spacer(1, 8),
             Paragraph("6. Use of the grants", H2),
             Paragraph("Places report the use of their grants to the Heat Resilience Panel by 31 October 2027. Any "
                       "grant not committed by 30 September 2027 returns to the fund.", P)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2.2 * cm, rightMargin=2.2 * cm, topMargin=2 * cm,
                            bottomMargin=2 * cm, title="Heat Resilience Fund 2027: allocation terms",
                            author="Caroline Porter", subject="Board paper B/26/41", creator="Microsoft Word",
                            producer="Microsoft: Print To PDF")
    doc.build(flow)
    _stamp(path, b"D:20260624101522+01'00'", "Caroline Porter")
