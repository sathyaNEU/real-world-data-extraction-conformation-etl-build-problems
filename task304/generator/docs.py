"""task304 architecture 5: the two documents, as PDFs (reportlab, invariant output): the national fund's bid guidance
(the governing document: the benefit, the record, the factors and the annex tables) and the county's 2026 junction
screening note (the list the bid chooses from)."""
import os

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
from io_util import scrub_pdf

rl_config.invariant = 1

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.2, spaceAfter=4)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=13.5, spaceBefore=6,
                    spaceAfter=3)


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=author,
                             producer=author)


def _table(rows, widths):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#999999")),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8ECEF"))]))
    return t


def guidance(out):
    path = os.path.join(out, "junction_safety_fund_guidance_2027.pdf")
    d = _doc(path, "Junction Safety Fund 2027 - guidance for highway authorities", "Junction Safety Fund programme team",
             "JSF-2027 bid guidance")
    s = [Paragraph("Junction Safety Fund 2027: guidance for highway authorities", H1),
         Paragraph("Issued by Cheryl Gregory, Programme Manager, Junction Safety Fund, 15 September 2026. Bids close on "
                   "29 January 2027.", SMALL), Spacer(1, 4),
         Paragraph("1. Purpose", H2),
         Paragraph("The fund pays for one roundabout in 2027 to 2028 on each participating highway authority's network, at "
                   "a junction where injury collisions can be expected to fall when priority control is replaced. It is "
                   "capital funding for construction; design and supervision are met by the authority.", BODY),
         Paragraph("2. Eligible junctions", H2),
         Paragraph("A junction is eligible when it is on a road the authority is the highway authority for, is now "
                   "controlled by give-way or stop lines, and was listed by the authority's latest network screening for "
                   "treatment study.", BODY),
         Paragraph("3. The scheme and its benefit", H2),
         Paragraph("3.1 Each authority may bid for one roundabout at one junction.", BODY),
         Paragraph("3.2 A scheme's benefit is the number of injury collisions it is expected to prevent each year: the "
                   "junction's expected annual injury collisions as it stands, at its 2026 traffic, times one less the "
                   "crash modification factor for its layout in Table 2.", BODY),
         Paragraph("3.3 A junction's expected annual injury collisions are the long-run yearly average that junction "
                   "would have as it stands, with its own layout and traffic. The injury collisions it recorded in the "
                   "years it was listed for are part of the evidence on that average and are not the average itself. "
                   "Expected collisions are estimated from the authority's validated collision record for the five years "
                   "2021 to 2025.", BODY),
         Paragraph("3.4 The bid names the junction with the largest benefit among those the screening listed, and gives "
                   "every listed junction's benefit.", BODY),
         Paragraph("Table 2. Crash modification factors for a roundabout replacing give-way or stop control "
                   "(injury collisions)", SMALL),
         _table([["Layout before", "Crash modification factor"],
                 ["Crossroads (four arms)", "%.2f" % P.CMF["X"]],
                 ["T junction or staggered junction", "%.2f" % P.CMF["T"]]], [95 * mm, 55 * mm]),
         Spacer(1, 4),
         Paragraph("4. Annex A: supporting tables", H2),
         Paragraph("A1. The authority's injury collisions on roads it is the highway authority for, in each quarter of "
                   "2026 to date, by severity. A collision's severity is that of its most severely injured casualty, and "
                   "a casualty who dies of their injuries within 30 days of the collision is killed, as in the national "
                   "road casualty statistics.", BODY),
         Paragraph("A2. The casualties of those collisions in each quarter by road user: pedestrians; pedal cyclists; "
                   "motorcyclists (riders and passengers of motorcycles of any engine size); and car occupants (drivers "
                   "and passengers of cars, taxis and private hire cars).", BODY),
         Paragraph("5. Timetable", H2),
         Paragraph("Bids close on 29 January 2027. The fund's panel decides in March 2027, and funded schemes are to be "
                   "open to traffic by 31 March 2028.", BODY)]
    d.build(s)


def screening(out, pack):
    path = os.path.join(out, "network_screening_2026.pdf")
    d = _doc(path, "Ardleshire junction screening 2026", "Halberd Transport Planning", "Road safety term contract, task 26-14")
    cands = sorted(pack.W.candidates(), key=lambda j: j["name"])
    rows = [["Junction", "Node", "District", "Layout", "Roads"]]
    lay = {"X": "Crossroads", "T": "T junction", "ST": "Staggered"}
    for j in cands:
        rows.append([j["name"], j["node"], j["district"], lay[j["layout"]],
                     "%s %s / %s" % (j["road"], j["road_name"], j["minor"])])
    s = [Paragraph("Ardleshire County Council: junction screening 2026", H1),
         Paragraph("Halberd Transport Planning for Ardleshire County Council, road safety engineering term contract, "
                   "task 26-14. Alison Hartley, 9 October 2026.", SMALL), Spacer(1, 4),
         Paragraph("1. What was screened", H2),
         Paragraph("Every junction on the county's principal road network that is controlled by give-way or stop lines, "
                   "using the county's validated collision record for 2021 to 2025 and the junction inventory. Roundabouts "
                   "and signal-controlled junctions are screened separately in the signals review.", BODY),
         Paragraph("2. The list", H2),
         Paragraph("The junctions below had twelve or more injury collisions in 2021 to 2025 and are listed for treatment "
                   "study. They are in alphabetical order.", BODY),
         _table(rows, [42 * mm, 15 * mm, 22 * mm, 22 * mm, 69 * mm]),
         Spacer(1, 4),
         Paragraph("3. Next steps", H2),
         Paragraph("The listed junctions are the candidates for the county's 2027 Junction Safety Fund bid. Site visits "
                   "were made in September 2026; each listed junction has room for a roundabout within highway land or "
                   "land the county holds.", BODY)]
    d.build(s)


def write_docs(out, pack):
    guidance(out)
    screening(out, pack)
    stamps = {"junction_safety_fund_guidance_2027.pdf": ("D:20260915101200+01'00'", "D:20260915142700+01'00'"),
              "network_screening_2026.pdf": ("D:20261009090600+01'00'", "D:20261009113800+01'00'")}
    for name, (created, modified) in stamps.items():
        scrub_pdf(os.path.join(out, name), created, modified)
