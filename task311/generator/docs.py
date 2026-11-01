"""The two governing documents: the centre's 2025 technical report and the foundation's boost terms."""
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP

SS = getSampleStyleSheet()
BODY = ParagraphStyle("body", parent=SS["Normal"], fontName="Times-Roman", fontSize=10.5, leading=13.6,
                      spaceAfter=6, alignment=TA_LEFT)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=14,
                    spaceBefore=8, spaceAfter=4)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=9, leading=11.4, textColor=colors.HexColor("#333333"))
CELL = ParagraphStyle("cell", parent=BODY, fontName="Helvetica", fontSize=8.8, leading=10.6, spaceAfter=0)


def _table(rows, widths, head=1):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8.8),
        ("FONT", (0, 0), (-1, head - 1), "Helvetica-Bold", 8.8),
        ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black),
        ("LINEBELOW", (0, head - 1), (-1, head - 1), 0.5, colors.black),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, colors.black),
        ("ALIGN", (1, head), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ]))
    return t


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.9 * inch, 0.55 * inch, text)
        canvas.drawRightString(7.6 * inch, 0.55 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def technical_report(path, fig):
    """fig: the published 2025 table and the design counts, from the shipped sample."""
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                            topMargin=0.85 * inch, bottomMargin=0.85 * inch,
                            title="Provincial Household Medicines Survey 2025: Technical Report",
                            author="Survey Research Centre, Halvorsen University", subject="PHMS 2025",
                            creator="Microsoft® Word for Microsoft 365", producer="Microsoft® Word for Microsoft 365", invariant=1)
    s = []
    s.append(Paragraph("Provincial Household Medicines Survey 2025", H1))
    s.append(Paragraph("Technical report", ParagraphStyle("sub", parent=H2, spaceBefore=0)))
    s.append(Paragraph("Survey Research Centre, Halvorsen University, for the Ministry of Health. "
                       "Released 18 November 2025.", SMALL))
    s.append(Spacer(1, 6))
    s.append(Paragraph("1. The survey", H2))
    s.append(Paragraph(
        "The Provincial Household Medicines Survey (PHMS) has been run by the Survey Research Centre for the "
        "Ministry of Health every year since 2019. In each sampled household it interviews the adult who looks "
        "after the household's medicines about prescriptions filled and not filled, what they cost and how they "
        "were paid for. The 2025 wave was in the field from 3 February to 13 June 2025. Northmark Field Research "
        "carried out the interviews in the North, Southern Uplands and Metro regions and Ostrander Data Collection, "
        "new to the survey in 2025, in the Central Valley and Lakeshore regions.", BODY))
    s.append(Paragraph("2. Sample design", H2))
    s.append(Paragraph(
        "The sample has two stages. The first-stage units are survey areas of about 150 to 800 occupied dwellings. "
        "The areas were selected in 2019 from an area frame built on the 2016 Census, with probability "
        "proportional to size within each health region, and the same areas are visited in every wave. In 2023 a "
        "supplement of 20 areas was added in the Central Valley, drawn from subdivisions on the municipal building "
        "permit registers that the 2016 frame did not cover; the supplement is a stratum of its own.", BODY))
    s.append(Paragraph(
        "Every area is relisted before each wave. Dwellings are selected at random from the listing and released "
        "to the field in batches until the area reaches the take of completed interviews set for its stratum; "
        "addresses still open at that point are withdrawn. A refusal may be reissued once to another interviewer. "
        "A dwelling selected in one wave is not selected again in a later wave.", BODY))
    t1 = [["Health region", "Strata", "Areas", "Completed interviews"]]
    for r in fig["design"]:
        t1.append([r["region"], r["strata"], str(r["areas"]), "{:,}".format(r["completes"])])
    t1.append(["All regions", "", str(sum(r["areas"] for r in fig["design"])),
               "{:,}".format(sum(r["completes"] for r in fig["design"]))])
    s.append(Paragraph("Table 1. Areas and completed interviews, 2025", SMALL))
    s.append(_table(t1, [1.7 * inch, 1.6 * inch, 0.7 * inch, 1.5 * inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("3. Weighting", H2))
    s.append(Paragraph(
        "Every completed interview in an area carries the same final weight: the area's design weight (the "
        "inverse of its probability of selection) times the number of occupied dwellings on the area's listing "
        "for the wave, divided by the number of completed interviews in the area. The weights are not calibrated "
        "to population totals.", BODY))
    s.append(Paragraph("4. Estimates and their standard errors", H2))
    s.append(Paragraph(
        "Regional estimates are weighted shares of households. Their standard errors are computed by Taylor "
        "linearisation with the survey areas as primary sampling units, treated as selected with replacement "
        "within strata. The strata are the five health regions, the Central Valley supplement being a stratum of "
        "its own. The design effect is the variance of an estimate divided by the variance a simple random sample "
        "of the same number of households answering would give. For planning, Table 2 also gives each region's "
        "intraclass correlation for the headline indicator, the share of the variance in households' answers that "
        "lies between survey areas rather than within them, estimated from the wave's interviews; an estimate below "
        "zero is shown as zero.", BODY))
    s.append(Paragraph("5. Response and completion", H2))
    s.append(Paragraph(
        "An interview is complete once it reaches the end of section D. An interview in which another adult of "
        "the household answers for the health contact is a complete interview. Partial interviews are not used. "
        "Answers of don't know and refusals at a question are left out of the estimates for that question. Of "
        "the eligible dwellings released in 2025, {rr} gave a complete interview.".format(rr=fig["rr_text"]), BODY))
    s.append(Paragraph("6. The headline indicator", H2))
    s.append(Paragraph(
        "The headline indicator is the share of households in which someone did not fill a prescription in the "
        "past 12 months because of its cost. Households with no prescription to fill in the period count among "
        "the households that did not go without.", BODY))
    t3 = [["Health region", Paragraph("<b>Households answering</b>", CELL), Paragraph("<b>Estimate (%)</b>", CELL),
           Paragraph("<b>Standard error (points)</b>", CELL), Paragraph("<b>Design effect</b>", CELL),
           Paragraph("<b>Intraclass correlation</b>", CELL)]]
    for r in fig["published"]:
        t3.append([r["region"], "{:,}".format(r["n"]), "%.1f" % r["est"], "%.2f" % r["se"], "%.2f" % r["deff"],
                   "%.3f" % r["icc"]])
    s.append(Paragraph("Table 2. Households in which someone did not fill a prescription because of its cost, "
                       "past 12 months, 2025", SMALL))
    s.append(_table(t3, [1.45 * inch, 1.0 * inch, 0.8 * inch, 1.05 * inch, 0.8 * inch, 1.05 * inch]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("7. Health regions", H2))
    s.append(Paragraph(
        "The Ministry's reorganisation of the health regions took effect on 1 April 2024. It moved several survey "
        "areas from one region to another, and the areas of each region were renumbered in one sequence. The 2024 "
        "estimates were published on the regions as they stood before the reorganisation. The 2025 estimates in "
        "this report are on the regions as reorganised.", BODY))
    doc.build(s, onFirstPage=_footer("PHMS 2025 Technical Report"), onLaterPages=_footer("PHMS 2025 Technical Report"))
    PP.normalize_pdf(path, b"D:20251118104512-06'00'", b"D:20251118110237-06'00'")


def boost_terms(path):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
                            topMargin=0.9 * inch, bottomMargin=0.9 * inch,
                            title="Grant terms: PHMS 2027 regional boost", author="Wexcombe Foundation",
                            subject="Grant WF-2026-117", creator="Microsoft® Word for Microsoft 365", producer="Microsoft® Word for Microsoft 365", invariant=1)
    s = []
    s.append(Paragraph("Wexcombe Foundation", ParagraphStyle("org", parent=H1, fontSize=14)))
    s.append(Paragraph("Health Access Programme", SMALL))
    s.append(Spacer(1, 10))
    s.append(Paragraph("Grant WF-2026-117. Terms for the 2027 regional boost to the Provincial Household Medicines "
                       "Survey", H2))
    s.append(Paragraph("9 October 2026", BODY))
    s.append(Paragraph("To: Heidi Roberts, Director, Survey Research Centre, Halvorsen University", BODY))
    s.append(Spacer(1, 4))
    s.append(Paragraph("1. Purpose", H2))
    s.append(Paragraph(
        "The grant improves the precision of one health region's estimate of households going without "
        "prescriptions because of their cost in the 2027 wave of the Provincial Household Medicines Survey, the "
        "survey's first wave since 2025.", BODY))
    s.append(Paragraph("2. The boost", H2))
    s.append(Paragraph(
        "The Foundation will pay for 1,200 completed interviews in addition to the 2027 wave's regular sample, all "
        "in one health region. They are taken in that region's 2025 sampled areas, the same number of additional "
        "completed interviews in each of those areas, and are weighted with the region's other 2027 interviews in "
        "the Centre's usual way. Apart from the boost, the 2027 wave repeats the design of the 2025 wave.", BODY))
    s.append(Paragraph("3. Where the boost goes", H2))
    s.append(Paragraph(
        "The boost goes to the health region in which it removes the largest share of the standard error of the "
        "region's 2027 estimate of the share of households in which someone did not fill a prescription in the "
        "past 12 months because of its cost. The share removed is one minus the ratio of the standard error that "
        "estimate would have with the boost to the standard error it would have without it, both reckoned in the "
        "same way for the 2027 design on the evidence of the 2025 wave, the standard error being the one the Centre "
        "publishes for a regional estimate (2025 Technical Report, section 4). Health regions are the regions as "
        "constituted by the Ministry of Health from 1 April 2024.", BODY))
    s.append(Paragraph("4. Timing and payment", H2))
    s.append(Paragraph(
        "The Centre will send the Foundation its placement, with its working, by 6 November 2026. The 2027 "
        "fieldwork contract will be let on that placement. The Foundation pays the Centre the contracted cost of "
        "the 1,200 interviews in two instalments, on the letting of the contract and on delivery of the 2027 "
        "regional estimates.", BODY))
    s.append(Spacer(1, 16))
    s.append(Paragraph("Jeremy Morris", BODY))
    s.append(Paragraph("Programme Director, Health Access", BODY))
    doc.build(s, onFirstPage=_footer("Wexcombe Foundation  WF-2026-117"), onLaterPages=_footer("Wexcombe Foundation  WF-2026-117"))
    PP.normalize_pdf(path, b"D:20261009151840-06'00'", b"D:20261009160514-06'00'")
