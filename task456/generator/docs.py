"""The bundle's two documents: the Ridgeline ICU Surge Compact (October 2025) and its data annex (November 2025)."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1c1f24")
GREY = colors.HexColor("#5e636b")
NAVY = colors.HexColor("#1f3a5f")
L_BODY = ParagraphStyle("lb", fontName="LiberationSerif", fontSize=10.5, leading=14.6, textColor=INK, spaceAfter=6)
L_NUM = ParagraphStyle("ln", parent=L_BODY, leftIndent=24, firstLineIndent=-24)
L_H1 = ParagraphStyle("lh1", fontName="LiberationSerif-Bold", fontSize=14, leading=18, textColor=INK, alignment=1,
                      spaceAfter=3)
L_CAP = ParagraphStyle("lc", fontName="LiberationSerif-Italic", fontSize=9.6, leading=12.6, textColor=GREY,
                       alignment=1, spaceAfter=14)
L_H2 = ParagraphStyle("lh2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=8,
                      spaceAfter=4)
S_BODY = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6)
S_H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=14, leading=18, textColor=NAVY, spaceAfter=3)
S_SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.2, leading=12.8, textColor=GREY, spaceAfter=12)
S_H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=NAVY, spaceBefore=8,
                      spaceAfter=3)
S_CELL = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.8, leading=11.2, textColor=INK)


def _doc(path, title, author, footer, serif):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSerif" if serif else "LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(22 * mm, 12 * mm, footer)
        canvas.drawRightString(letter[0] - 22 * mm, 12 * mm, "%d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=24 * mm, rightMargin=24 * mm, topMargin=20 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def write_compact(path):
    d, frame = _doc(path, W.COMPACT, W.ALLIANCE, "%s, effective 1 October 2025" % W.COMPACT, True)
    P = lambda t, s=L_BODY: Paragraph(t, s)
    story = [P(W.COMPACT.upper(), L_H1),
             P("Among the member hospitals of the %s. Adopted by the alliance's board on 16 September 2025; effective "
               "1 October 2025." % W.ALLIANCE, L_CAP),
             P("Article 1. Purpose", L_H2),
             P("1.1&nbsp;&nbsp;The member hospitals agree to share adult intensive care capacity when a region's units "
               "are under sustained strain. Strain is regional: one region's units fill while another's have room, and "
               "the compact moves patients, staff and ambulances between regions.", L_NUM),
             P("1.2&nbsp;&nbsp;Outside an activation the compact changes no hospital's own admission, transfer or "
               "staffing policy.", L_NUM),
             P("Article 2. Definitions", L_H2),
             P("2.1&nbsp;&nbsp;A <i>compact hospital</i> is a member hospital with adult intensive care beds, as listed "
               "in the alliance's facility crosswalk.", L_NUM),
             P("2.2&nbsp;&nbsp;A <i>region</i> is one of the eight surge regions of Annex A, each a set of Tennessee "
               "counties. A hospital, a member or not, belongs to the region of the county it stands in.", L_NUM),
             P("2.3&nbsp;&nbsp;A <i>hospital-day</i> is one compact hospital on one calendar day of the hospital's own "
               "local time.", L_NUM),
             P("2.4&nbsp;&nbsp;A <i>full day</i> is a hospital-day on which every staffed adult intensive care bed of "
               "the hospital was occupied at some time, so that the unit could take no new patient because every "
               "staffed bed was occupied.", L_NUM),
             P("Article 3. The operations committee", L_H2),
             P("3.1&nbsp;&nbsp;The operations committee, one member from each region and the alliance's chief "
               "operating officer, meets each Tuesday (the <i>review</i>).", L_NUM),
             P("3.2&nbsp;&nbsp;The alliance's data team prepares each review from the feeds the data annex describes "
               "and publishes the activation notice the day after the review.", L_NUM),
             P("Article 4. Activation", L_H2),
             P("4.1&nbsp;&nbsp;At each review the committee activates the compact in every region where at least one "
               "in three of the region's hospital-days in the 28 days ending on the Sunday before the review were full "
               "days.", L_NUM),
             P("4.2&nbsp;&nbsp;An activation runs for the four weeks from the Monday after the review. A region may be "
               "activated again at a later review.", L_NUM),
             P("4.3&nbsp;&nbsp;The activation notice states each region's share of full hospital-days and whether it "
               "is activated.", L_NUM),
             P("Article 5. What activation does", L_H2),
             P("5.1&nbsp;&nbsp;Transfers. When an activated region's hospitals ask, the %s places the region's adult "
               "intensive care patients with hospitals in other regions before the region's own." % W.CENTER, L_NUM),
             P("5.2&nbsp;&nbsp;Staff. The alliance's pooled travel nurses are assigned to the activated region's "
               "hospitals for the activation.", L_NUM),
             P("5.3&nbsp;&nbsp;Ambulances. The transfer center coordinates the activated region's emergency department "
               "diversion with the regional emergency medical services.", L_NUM),
             P("Article 6. Costs", L_H2),
             P("6.1&nbsp;&nbsp;Each hospital bears its own costs of an activation; the pooled travel nurses are paid "
               "from the alliance's surge fund at the rates in its staffing agreement.", L_NUM),
             P("Article 7. Term", L_H2),
             P("7.1&nbsp;&nbsp;The compact runs until 30 September 2027 and continues from year to year unless the "
               "board ends it. A member may leave at ninety days' notice.", L_NUM),
             P("Annex A. The surge regions", L_H2),
             P("Annex A is kept as the alliance's region file (<i>compact_regions_counties.csv</i>): every Tennessee "
               "county with its region. The regions are Northeast, East, Southeast, Upper Cumberland, Mid-State, "
               "South Central, West and Memphis Delta.", L_BODY),
             Spacer(1, 8),
             P("For the alliance: %s, chair of the operations committee." % W.PEOPLE["chair"], L_BODY)]
    d.build(story, onFirstPage=frame, onLaterPages=frame)


def write_annex(path):
    d, frame = _doc(path, "Compact data annex", W.PEOPLE["data"], "%s data annex, 3 November 2025" % W.COMPACT, False)
    P = lambda t, s=S_BODY: Paragraph(t, s)
    tbl = Table([[Paragraph(x, S_CELL) for x in r] for r in [
        ["Feed", "Recorded by", "What it records", "Clock"],
        ["Census survey", "each compact hospital's house supervisor, each morning by 11:00",
         "staffed adult ICU beds and adult ICU patients counted at 07:00, with the other units' counts",
         "the hospital's own time"],
        ["Bed-status board", "each hospital's bed managers and supervisors, at any time",
         "each unit's status: Open, Limited or Closed (emergency departments Open, Advisory or Divert), with an "
         "optional reason", "UTC"],
        ["Transfer center", "the center's transfer nurses, for every placement request",
         "the hospitals called for each request, in turn, and each answer with its reason code", "Central time"]]],
        colWidths=[28 * mm, 42 * mm, 64 * mm, 22 * mm])
    tbl.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, NAVY), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    story = [P("Compact data annex: the feeds each review is prepared from", S_H1),
             P("%s, %s. Version of 3 November 2025, prepared by %s for the operations committee." % (
                 W.COMPACT, W.ALLIANCE, W.PEOPLE["data"]), S_SUB),
             P("1. The three feeds", S_H2), tbl, Spacer(1, 6),
             P("2. The census survey", S_H2),
             P("Each compact hospital reports each morning, by 11:00, its staffed adult ICU beds and its adult ICU "
               "patients as counted at 07:00, with the counts of its other units; a unit that fills after 07:00 is "
               "not seen until the next morning's count. A hospital may correct a report; the later submission for a "
               "date replaces the earlier one. From 1 December 2025 the survey moves to its new form; the export's "
               "column names change and the counts do not."),
             P("3. The bed-status board", S_H2),
             P("Each hospital sets the status of each of its units on the regional bed-status board. A status stands "
               "until the hospital changes it, and the board asks each unit to confirm its status at least every "
               "eight hours. A hospital closes its adult ICU when it can take no transfer: when every staffed bed is "
               "occupied, and also when it keeps its last staffed beds for its own patients. Not every supervisor "
               "closes the unit when it fills. The board logs every change, and every confirmation, in UTC."),
             P("4. The transfer center", S_H2),
             P("For each request to place a patient the %s calls hospitals in turn and logs each answer. A hospital "
               "that declines gives a reason code; from 1 December 2025 the code is CAP when it has no staffed bed of "
               "the level of care asked for (before then NB, no bed, or NS, no staff). A request is placed when a "
               "called hospital accepts it; an acceptance the sending hospital later cancels is not a placement. A "
               "patient's region is the region of the hospital that asks the center for the placement. The center "
               "hears from a hospital only when it calls it about a request." % W.CENTER),
             P("5. The feeds and the review", S_H2),
             P("None of the three feeds is a record of full days, and a count or a decline is now and then entered "
               "in error. Every compact hospital reports through the same census form, the same board and the same "
               "transfer center, under the same instructions, in every region."),
             P("6. Days and times", S_H2),
             P("The review counts each hospital's own calendar days, in the hospital's own time zone: the Northeast "
               "and East regions, and the Southeast region's hospitals in Hamilton, Bradley, McMinn, Polk, Meigs and "
               "Rhea counties, keep Eastern time; every other compact hospital keeps Central time. The facility "
               "crosswalk gives each hospital's time zone.")]
    d.build(story, onFirstPage=frame, onLaterPages=frame)
