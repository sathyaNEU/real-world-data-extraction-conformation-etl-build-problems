"""The pack's governing and reference documents: the Source Water Protection Plan (revision 2), the carbon-feed
procedure SOP-WQ-07 and the intake tower's record drawing sheet S-4."""
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP
import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.3, leading=12.6,
                      alignment=TA_JUSTIFY, spaceAfter=4.5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13, spaceAfter=3)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=9.9, spaceAfter=3,
                    spaceBefore=7)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.9, leading=10)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=8.0, leading=9.8)
CELLB = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8.0, leading=9.8)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.5, 0.5, 0.5)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.91, 0.91, 0.89)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])


def wrap(rows, widths=None):
    t = Table([[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)],
              colWidths=widths, hAlign="LEFT")
    t.setStyle(TBL)
    return t


def footer(doc_id):
    def draw(canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 7.4)
        canv.setFillColor(colors.Color(0.35, 0.35, 0.35))
        canv.drawString(0.9 * inch, 0.5 * inch, doc_id)
        canv.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d of %s" % (doc.page, doc._pages_total))
        canv.drawString(0.9 * inch, letter[1] - 0.48 * inch, W.DEPT)
        canv.line(0.9 * inch, letter[1] - 0.53 * inch, letter[0] - 0.9 * inch, letter[1] - 0.53 * inch)
        canv.restoreState()
    return draw


def two_pass(path, story_fn, doc_id, title, created, modified):
    """Build twice so the footer can print the page total."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    total = "?"
    for _ in range(2):
        d = SimpleDocTemplate(path, pagesize=letter, title=title, author="", subject="", creator="",
                              leftMargin=0.9 * inch, rightMargin=0.9 * inch, topMargin=0.8 * inch,
                              bottomMargin=0.75 * inch)
        d._pages_total = total
        d.build(story_fn(), onFirstPage=footer(doc_id), onLaterPages=footer(doc_id))
        total = str(d.page)
    PP.normalize_pdf(path, created, modified)


def signatures(rows):
    return wrap([["Role", "Name", "Signature", "Date"]] + rows, widths=[1.9 * inch, 1.7 * inch, 1.6 * inch, 1.2 * inch])


def plan(path):
    def story():
        s = [Paragraph("Source Water Protection Plan: Lake Merrin", H1),
             Paragraph("Document SWP-01, revision 2. Adopted by the Board of Water Commissioners on 18 March 2025. "
                       "This copy carries sections 1 to 7 and Table 2; the appendices (landowner contacts and the "
                       "2023 delineation maps) are held by the source water protection coordinator.", SMALL),
             Paragraph("1 Purpose", H2),
             Paragraph("1.1 Lake Merrin is the City of Brennick's only source of supply. The Merrin Water Treatment "
                       "Plant draws it through the intake tower at Merrin Dam. This plan sets how the department "
                       "watches the lake's tributaries for the herbicides used on the watershed's corn and how it "
                       "spends its source water money on the farms that drain to them.", BODY),
             Paragraph("1.2 Atrazine is the herbicide the plan is mainly concerned with. When the plant's raw water "
                       "carries more than the plant's carbon-feed trigger (SOP-WQ-07), powdered activated carbon is "
                       "fed, at the treatment budget's expense.", BODY),
             Paragraph("2 The sub-watersheds", H2),
             Paragraph("2.1 The plan divides the lake's watershed into the five sub-watersheds of Table 2, each the "
                       "land draining to its tributary above the tributary's monitoring station. The lake's direct "
                       "drainage, about 6 square miles of shoreline parcels and Merrin Park, is not a program "
                       "sub-watershed.", BODY),
             wrap([["Sub-watershed", "Area above station (sq mi)", "Monitoring station", "Sampling site code"],
                   ["Tessel River", "%.1f" % (W.AREA_KM2["TES"] / 2.589988), "TR-01 Tessel River at Halvard Bridge", "TES-HB"],
                   ["Fennick Creek", "%.1f" % (W.AREA_KM2["FEN"] / 2.589988), "FC-02 Fennick Creek at County Road W38", "FEN-38"],
                   ["Oxley Creek", "%.1f" % (W.AREA_KM2["OXL"] / 2.589988), "OC-03 Oxley Creek at Lisle", "OXL-LS"],
                   ["Dunmore Creek", "%.1f" % (W.AREA_KM2["DUN"] / 2.589988), "DC-04 Dunmore Creek at 230th Street", "DUN-230"],
                   ["Ladd Branch", "%.1f" % (W.AREA_KM2["LAD"] / 2.589988), "LB-05 Ladd Branch at Merrin Park Road", "LAD-MP"]],
                  widths=[1.3 * inch, 1.5 * inch, 2.6 * inch, 1.2 * inch]),
             Paragraph("Table 2. Program sub-watersheds.", SMALL),
             Paragraph("3 Monitoring", H2),
             Paragraph("3.1 TR-01, FC-02, OC-03 and DC-04 are sampled on Tuesdays from the last week of March to "
                       "the end of October, and after storms from late April to September they are sampled again at "
                       "intervals of several hours while they run high. LB-05 records flow and temperature only. "
                       "Routine bottles go to the State Hygienic Laboratory for GC/MS analysis; storm bottles are run "
                       "by ELISA in the department's laboratory, with about one in four also sent to the State "
                       "laboratory.", BODY),
             Paragraph("3.2 Where both laboratories analysed a bottle, the State Hygienic Laboratory's result is "
                       "used. A result reported as not detected counts as zero in load calculations.", BODY),
             Paragraph("3.3 Flows at TR-01, FC-02 and OC-03 are published by the department's hydrometric network. "
                       "DC-04 and LB-05 are logger stations rated by the department.", BODY),
             Paragraph("4 The atrazine cost-share program", H2),
             Paragraph("4.1 The program pays farm operators in one sub-watershed for three seasons of changed "
                       "practice: atrazine rates cut to a half pound or less, applications moved after planting, "
                       "alternative products, and filter strips on fields that drain directly to the tributary. It is "
                       "funded from the treatment budget at up to $185,000 a year.", BODY),
             Paragraph("4.2 Sign-up runs from 1 December to 15 March, so that practice changes are in place before "
                       "the April applications.", BODY),
             Paragraph("5 Placement", H2),
             Paragraph("5.1 Each year the program goes to one sub-watershed: the one whose atrazine was behind the "
                       "most days of the last completed season on which the plant's raw water was above the "
                       "carbon-feed trigger. A day counts for a sub-watershed when the raw water would have stayed "
                       "at or below the trigger that day without that sub-watershed's atrazine.", BODY),
             Paragraph("5.2 The season runs from 15 April to 31 October, when the plant screens its raw water every "
                       "day. A day's raw-water result is the one SOP-WQ-07 sets.", BODY),
             Paragraph("6 Records", H2),
             Paragraph("6.1 Station records, sampling records and laboratory reports are kept for ten years. The "
                       "coordinator reports the season's results to the Board each November.", BODY),
             Paragraph("7 Review", H2),
             Paragraph("7.1 The plan is reviewed every three years or when the watershed's land use changes "
                       "materially.", BODY),
             Spacer(1, 6),
             wrap([["Rev", "Date", "Change"],
                   ["0", "14 May 2019", "First issue."],
                   ["1", "9 February 2022", "Ladd Branch added as a sub-watershed; storm sampling added."],
                   ["2", "18 March 2025", "Cost-share program and its placement rule (sections 4 and 5); DC-04 and "
                                         "LB-05 stations added."]], widths=[0.5 * inch, 1.3 * inch, 4.8 * inch]),
             Spacer(1, 8),
             signatures([["Prepared", "Brandi Dougherty", "", "4 March 2025"],
                         ["Reviewed", "Carl Newman", "", "6 March 2025"],
                         ["Adopted", "Board of Water Commissioners", "Resolution 2025-07", "18 March 2025"]])]
        return s
    two_pass(path, story, "SWP-01 rev 2", "Source Water Protection Plan: Lake Merrin",
             b"D:20250318150212-05'00'", b"D:20250318150212-05'00'")


def sop(path):
    def story():
        return [Paragraph("SOP-WQ-07 Powdered Activated Carbon Feed", H1),
                Paragraph("Merrin Water Treatment Plant standard operating procedure, revision 4, effective 2 April "
                          "2024.", SMALL),
                Paragraph("1 Purpose", H2),
                Paragraph("1.1 This procedure sets when the plant feeds powdered activated carbon (PAC) for atrazine in "
                          "the raw water, at what dose, and when the feed stops.", BODY),
                Paragraph("2 Raw-water atrazine", H2),
                Paragraph("2.1 The raw water is sampled at the raw-water tap (RAW-01) each morning before 08:00. From "
                          "15 April to 31 October the sample is screened for atrazine by ELISA every day; outside "
                          "that season it is screened on Tuesdays.", BODY),
                Paragraph("2.2 A screen of 2.5 ug/L or more is confirmed by GC/MS at the State Hygienic Laboratory "
                          "from the same sample, and the Tuesday sample of every even-numbered week is confirmed in any "
                          "case.", BODY),
                Paragraph("2.3 A day's raw-water result is the GC/MS confirmation where one was run on that day's "
                          "sample, otherwise the ELISA screen.", BODY),
                Paragraph("3 Trigger and dose", H2),
                Paragraph("3.1 The carbon-feed trigger is a day's raw-water result above 3.0 ug/L.", BODY),
                Paragraph("3.2 When a day's result is above the trigger the shift lead starts the feed, or changes "
                          "its dose, by Table 1. The dose is entered as a setpoint at the PAC feeder panel and applies "
                          "to the plant's raw-water flow; the feeder delivers dose (mg/L) x raw-water flow (MGD) x 8.34 "
                          "pounds a day.", BODY),
                wrap([["Day's result (ug/L)", "PAC dose (mg/L)"], ["above 3.0 to 4.0", "12"], ["above 4.0 to 5.5", "18"],
                      ["above 5.5", "25"]], widths=[2.0 * inch, 1.6 * inch]),
                Paragraph("Table 1. PAC dose.", SMALL),
                Paragraph("3.3 The feed stops after two days in a row whose results are at or below 2.5 ug/L.", BODY),
                Paragraph("4 Records", H2),
                Paragraph("4.1 Setpoint changes are recorded by SCADA. The shift lead notes PAC deliveries in the "
                          "chemical log.", BODY),
                Spacer(1, 6),
                wrap([["Rev", "Date", "Change"],
                      ["2", "11 April 2019", "ELISA screening added."],
                      ["3", "3 March 2021", "Trigger aligned with the plant's 3.0 ug/L operating limit."],
                      ["4", "2 April 2024", "Even-week confirmation; Table 1 doses revised."]],
                     widths=[0.5 * inch, 1.3 * inch, 4.8 * inch]),
                Spacer(1, 8),
                signatures([["Prepared", "Brandi Dougherty", "", "25 March 2024"],
                            ["Approved", "Carl Newman", "", "28 March 2024"]])]
    two_pass(path, story, "SOP-WQ-07 rev 4", "SOP-WQ-07 Powdered Activated Carbon Feed",
             b"D:20240402091544-05'00'", b"D:20240402091544-05'00'")


def drawing(path):
    """A record drawing sheet: an elevation schedule, notes and a title block, landscape."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    pw, ph = landscape(letter)
    c = rl_canvas.Canvas(path, pagesize=(pw, ph), invariant=1)
    c.setTitle("Merrin Dam intake tower, sheet S-4")
    c.setAuthor("")
    c.setCreator("")
    c.setLineWidth(1.2)
    c.rect(0.4 * inch, 0.4 * inch, pw - 0.8 * inch, ph - 0.8 * inch)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.7 * inch, ph - 0.85 * inch, "INTAKE TOWER: ELEVATION SCHEDULE AND NOTES")
    rows = [("Top of tower deck", 868.74), ("Operating floor", 866.24), ("Spillway crest (reference)", 863.24),
            ("Trash rack, top", 831.74), ("Intake port centreline", 829.24), ("Intake port invert", 827.24),
            ("Bottom outlet conduit invert", 803.24), ("Tower foundation, top of footing", 798.74)]
    y = ph - 1.35 * inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.8 * inch, y, "ITEM")
    c.drawString(4.0 * inch, y, "ELEVATION (FT)")
    c.setLineWidth(0.5)
    c.line(0.75 * inch, y - 4, 5.4 * inch, y - 4)
    c.setFont("Helvetica", 9)
    for name, el in rows:
        y -= 0.27 * inch
        c.drawString(0.8 * inch, y, name)
        c.drawString(4.0 * inch, y, "%.2f" % el)
    y -= 0.5 * inch
    c.setFont("Helvetica-Bold", 9)
    c.drawString(0.8 * inch, y, "NOTES")
    notes = ["1. ELEVATIONS ON THIS SHEET ARE NAVD88, CONVERTED IN 2011 FROM THE 1968 CONTRACT DRAWINGS (NGVD29).",
             "2. AT BENCHMARK MD-3 ON THE DAM CREST, NAVD88 = NGVD29 + 0.24 FT.",
             "3. ONE INTAKE PORT, 48 IN. DIA., WITH SLIDE GATE G-2. PORTS G-1 AND G-3 ABANDONED AND BULKHEADED 1994.",
             "4. RAW-WATER MAIN TO PLANT: 30 IN. DIP, 2,960 FT.",
             "5. BOTTOM OUTLET: 42 IN. RCP CONDUIT THROUGH THE EMBANKMENT, SLUICE GATE G-5 AT THE TOWER."]
    c.setFont("Helvetica", 8.5)
    for n in notes:
        y -= 0.24 * inch
        c.drawString(0.8 * inch, y, n)
    # elevation sketch
    x0 = 7.2 * inch
    c.setLineWidth(0.8)
    c.rect(x0, 1.9 * inch, 1.1 * inch, 4.9 * inch)
    for name, el in rows[:7]:
        yy = 1.9 * inch + (el - 798.74) / (868.74 - 798.74) * 4.9 * inch
        c.line(x0 - 0.15 * inch, yy, x0 + 1.25 * inch, yy)
        c.setFont("Helvetica", 6.5)
        c.drawString(x0 + 1.3 * inch, yy - 2, "EL %.2f" % el)
    c.circle(x0 + 0.55 * inch, 1.9 * inch + (829.24 - 798.74) / 70.0 * 4.9 * inch, 0.12 * inch)
    # title block
    tb_x, tb_y, tb_w, tb_h = pw - 4.6 * inch, 0.4 * inch, 4.2 * inch, 1.35 * inch
    c.setLineWidth(1.0)
    c.rect(tb_x, tb_y, tb_w, tb_h)
    c.line(tb_x, tb_y + 0.45 * inch, tb_x + tb_w, tb_y + 0.45 * inch)
    c.line(tb_x, tb_y + 0.9 * inch, tb_x + tb_w, tb_y + 0.9 * inch)
    c.line(tb_x + 2.9 * inch, tb_y, tb_x + 2.9 * inch, tb_y + 0.9 * inch)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(tb_x + 0.1 * inch, tb_y + 1.12 * inch, "CITY OF BRENNICK WATER DEPARTMENT: MERRIN DAM")
    c.setFont("Helvetica", 7.5)
    c.drawString(tb_x + 0.1 * inch, tb_y + 0.97 * inch, "INTAKE TOWER RECORD DRAWINGS")
    c.drawString(tb_x + 0.1 * inch, tb_y + 0.65 * inch, "BALL & FRYE ENGINEERS, DES MOINES, IOWA")
    c.drawString(tb_x + 0.1 * inch, tb_y + 0.52 * inch, "REV C  2011-08-15  DATUM CONVERSION")
    c.drawString(tb_x + 0.1 * inch, tb_y + 0.25 * inch, "DRAWN: C. BALL    CHECKED: B. FRYE")
    c.drawString(tb_x + 0.1 * inch, tb_y + 0.1 * inch, "PROJECT 11-0347")
    c.setFont("Helvetica-Bold", 14)
    c.drawString(tb_x + 3.15 * inch, tb_y + 0.42 * inch, "S-4")
    c.setFont("Helvetica", 7)
    c.drawString(tb_x + 3.05 * inch, tb_y + 0.15 * inch, "SHEET 9 OF 22")
    c.showPage()
    c.save()
    PP.normalize_pdf(path, b"D:20110815103000-05'00'", b"D:20110815103000-05'00'")


def build(target, paths):
    plan(paths["plan"])
    sop(paths["sop"])
    drawing(paths["drawing"])
