"""task483 governing document: the federation's UTI pathway specification for 2027-28 (three pages, ReportLab).

It files the WHAT in the federation's own genre: the courses the pathway covers, what makes a course mismatched,
the one figure per antibacterial the federation uses, the planning basis and the placement. It names no culture,
no window for the cultures, no antibiogram and no prescribing history.
"""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

BODY = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=13.2, alignment=TA_LEFT, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14.5, leading=18, spaceAfter=4,
                    textColor=colors.HexColor("#1F3A5F"))
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.6, leading=14, spaceBefore=7, spaceAfter=3,
                    textColor=colors.HexColor("#1F3A5F"))
SMALL = ParagraphStyle("small", fontName="Helvetica", fontSize=8.2, leading=10.6, textColor=colors.HexColor("#444444"))


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.6)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(18 * mm, 10 * mm, "Hollinbrook Health Federation  |  UTI pathway specification 2027-28  |  v1.2")
    canvas.drawRightString(192 * mm, 10 * mm, "Page %d" % doc.page)
    canvas.restoreState()


def write_spec(path):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="UTI pathway specification 2027-28",
                            author="Hollinbrook Health Federation", subject="", creator="", producer="",
                            invariant=1)
    s = []
    s.append(Paragraph("Hollinbrook Health Federation", SMALL))
    s.append(Paragraph("Urinary tract infection pathway: service specification 2027-28", H1))
    meta = [["Version", "1.2 (approved)"], ["Owner", "Josephine James, Antimicrobial Stewardship Lead"],
            ["Approved by", "Federation Clinical Director, 3 December 2026"],
            ["Pathway year", "1 April 2027 to 31 March 2028"],
            ["Funding", "ICB primary care antimicrobial stewardship allocation 2027-28 (two pharmacist posts, 1.0 WTE each)"]]
    t = Table(meta, colWidths=[34 * mm, 136 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.6), ("FONT", (0, 0), (0, -1), "Helvetica-Bold", 8.6),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA8B8")),
                           ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EEF2F7")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s.append(t)
    s.append(Spacer(1, 4 * mm))

    s.append(Paragraph("1. Purpose", H2))
    s.append(Paragraph(
        "The pathway funds two antimicrobial stewardship pharmacists for the 2027-28 pathway year. Each pharmacist works "
        "for the whole year with the practices of one primary care network, reviewing first courses for uncomplicated "
        "lower urinary tract infection in women aged 16 to 64 with prescribers and supporting them to issue "
        "nitrofurantoin, the federation's first-line choice, in place of other antibacterials. The pharmacists also "
        "advise the network's practices on urinary infection in patients outside the pathway's own courses.", BODY))
    s.append(Paragraph(
        "The federation's primary care antimicrobial guideline follows NICE NG109: nitrofurantoin for non-pregnant women "
        "with eGFR of 45 or more, with pivmecillinam, fosfomycin and trimethoprim as alternatives where nitrofurantoin is "
        "unsuitable. This specification does not change the guideline.", BODY))

    s.append(Paragraph("2. The courses the pathway covers", H2))
    s.append(Paragraph(
        "2.1 A first course is an acute issue of a pathway antibacterial, linked to a lower UTI problem, to a woman aged "
        "16 to 64 on the date of issue, where no issue of a pathway antibacterial linked to a lower UTI problem was made "
        "to her in the 28 days before it. The pathway antibacterials and the lower UTI problems are those in the pathway "
        "code lists (uti_pathway_code_lists_2027-28.xlsx). A course linked to a pregnancy problem is not a pathway "
        "course.", BODY))
    s.append(Paragraph(
        "2.2 A course issued by the federation's extended access hub belongs to the practice the woman is registered "
        "with. A practice belongs to the primary care network the member practice register gives it for 2027-28; "
        "Stanbridge Road Surgery's patients belong to Hollin Lane Medical Practice from the merger of 1 July 2026, and "
        "their earlier courses with them.", BODY))
    s.append(Paragraph(
        "2.3 The planning basis for the 2027-28 year is the first courses issued in calendar year 2026.", BODY))

    s.append(Paragraph("3. Mismatched first courses", H2))
    s.append(Paragraph(
        "3.1 A first course is mismatched when the woman's infection carries an organism the laboratory reports "
        "resistant to the antibacterial issued. Resistance includes resistance the laboratory reports by expert rule. An "
        "organism reported susceptible, or susceptible at increased exposure, is not resistant, and a urine with no "
        "significant growth or with mixed growth carries no resistant organism.", BODY))
    s.append(Paragraph(
        "3.2 For each pathway antibacterial the federation uses one figure: the chance that a first course on it meets "
        "an organism the laboratory reports resistant to it, taken over all the federation's first courses whichever "
        "antibacterial each was in fact issued. The figure is estimated for the federation as a whole, over 2024 to "
        "2026, and the same figure is used for every network.", BODY))

    s.append(Paragraph("4. Placing the pharmacists", H2))
    s.append(Paragraph(
        "4.1 A network's mismatched courses stopped are its 2026 first courses on antibacterials other than "
        "nitrofurantoin, each counted at its antibacterial's chance (3.2) less nitrofurantoin's chance. A course on an "
        "antibacterial whose chance is below nitrofurantoin's counts against the network.", BODY))
    s.append(Paragraph(
        "4.2 The pharmacists are placed in the two networks with the most mismatched courses stopped, one pharmacist in "
        "each, from 1 April 2027 for the whole pathway year. No network has two pharmacists.", BODY))

    s.append(Paragraph("5. Monitoring", H2))
    s.append(Paragraph(
        "The stewardship lead reports first courses by antibacterial for each network quarterly to the Clinical "
        "Director, against the 2026 basis. The pharmacists record each prescriber review in the pathway log.", BODY))

    s.append(Paragraph("6. Information governance", H2))
    s.append(Paragraph(
        "Prescribing and laboratory data are used under the ICB's linked primary care data agreement. Extracts carry a "
        "pseudonym in place of the NHS number, and no record leaves the federation's secure environment. The pathology "
        "network's consultant microbiologist, Andrew Gibson, advises the pathway on laboratory reporting.", BODY))
    s.append(Spacer(1, 3 * mm))
    s.append(Paragraph("Document control: v1.0 draft 4 November 2026; v1.1 comments from the network clinical directors "
                       "19 November 2026; v1.2 approved 3 December 2026.", SMALL))
    doc.build(s, onFirstPage=_footer, onLaterPages=_footer)
