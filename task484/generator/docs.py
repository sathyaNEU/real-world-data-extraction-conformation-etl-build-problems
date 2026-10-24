"""The pack's three documents: the maintenance plan's chapter on residential wood combustion with the county's changeout
fund ordinance, the survey vendor's methods note, and the state tool's documentation."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import pack as P
import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10)
VENDOR = "Arrowleaf Survey Research"


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch, topMargin=0.7 * inch,
                            bottomMargin=0.7 * inch, title=title, author=author, creator=author, subject=title,
                            producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(0.8 * inch, 0.45 * inch, org + "  |  " + title)
        c.drawRightString(letter[0] - 0.8 * inch, 0.45 * inch, "Page %d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def _table(rows, widths=None):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.5),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def plan_pdf(path):
    rows = [["Burn zone", "Allotment (tons of PM2.5 per heating season)"]]
    rows += [[W.ZNAME[z], "%.1f" % W.ALLOTMENT[z]] for z in W.ZC]
    s = [Paragraph("Halvard Valley PM2.5 Maintenance Plan, Chapter 4: Residential Wood Combustion", T),
         Paragraph("Chapter 4 as amended by the Board of County Commissioners on 14 March 2023, with Halvard County Code "
                   "section 8.30.140 (Changeout fund) as amended on the same date.", BODY),
         Paragraph("4.1 Burn zones", H),
         Paragraph("The maintenance area is divided into five burn zones: Valley Floor North, Valley Floor South, East "
                   "Bench, West Bench and Upper Valley. A parcel's burn zone is the zone the program's burn zone parcel "
                   "list gives it.", BODY),
         Paragraph("4.2 Zone allotments", H),
         Paragraph("Each burn zone carries an allotment of PM2.5 from residential wood combustion for a heating season "
                   "(1 October to 30 April), Table 4-2. The allotments were set in 2023 so that the maintenance area's "
                   "total stays below the motor vehicle and area source budget of Chapter 6 with the margin that chapter "
                   "describes.", BODY),
         _table(rows, [2.2 * inch, 3.6 * inch]),
         Spacer(1, 4), Paragraph("Table 4-2. Zone allotments.", SMALL),
         Paragraph("4.3 A zone's PM2.5 from residential wood combustion", H),
         Paragraph("A burn zone's PM2.5 from residential wood combustion in a heating season is the PM2.5 emitted from "
                   "the wood burned that season by the wood-burning appliances in use in the zone, at the 2023 emission "
                   "factors by source classification code (Table 4-3, the program's 2023 factor table). The appliances "
                   "are the solid fuel devices in the county registry, each in use in the season it was installed before "
                   "and not removed during; the registry's device codes carry the source classification codes.", BODY),
         Paragraph("4.4 Other residential and commercial heating", H),
         Paragraph("The program's inventory also carries residential and commercial propane and natural gas heating for "
                   "the maintenance area. These categories are reported with the inventory and do not count against the "
                   "allotments. The inventory the program submits to the department covers the whole county, the county "
                   "outside the maintenance area on the department's residential wood combustion tool.", BODY),
         Paragraph("Halvard County Code 8.30.140 Changeout fund", H),
         Paragraph("A. Each year the program determines, for the latest complete heating season, which burn zones' "
                   "PM2.5 from residential wood combustion exceeded the zone's allotment in Table 4-2 of the maintenance "
                   "plan.", BODY),
         Paragraph("B. The changeout fund for the next changeout season, which opens on 1 November, is divided equally "
                   "among those zones and is spent only on changeouts in them. If no zone exceeded its allotment the fund "
                   "carries over to the following year.", BODY),
         Paragraph("C. The fund for the 2026-27 changeout season is USD %s." % format(W.FUND, ","), BODY)]
    _pdf(path, "Maintenance plan, Chapter 4", s, W.PEOPLE["lead"], W.PROGRAM)


def survey_methods_pdf(path):
    s = [Paragraph("2024-25 Household Heating Survey: Methods and Estimates", T),
         Paragraph("Prepared for the %s by %s, August 2025. Contact: %s." % (W.PROGRAM, VENDOR, W.PEOPLE["inventory"]),
                   BODY),
         Paragraph("Frame and sample", H),
         Paragraph("The frame is the county registry's solid fuel devices in use in the 2024-25 heating season (1 October "
                   "2024 to 30 April 2025), drawn from the registry on 1 May 2025, by burn zone. Within each zone a simple "
                   "random sample of devices was drawn and the household at each sampled device was surveyed by mail with "
                   "a telephone follow-up from 12 May to 27 June 2025. The response file carries each responding "
                   "device's registry id and the appliance as the frame codes it.", BODY),
         Paragraph("Questions", H),
         Paragraph("Households reported their home's main heating fuel and how much wood they burned in the sampled "
                   "appliance in the 2024-25 heating season, in the unit of their choice: cords, face cords or pickup "
                   "loads for cordwood, tons or 40-pound bags for pellets. A face cord is one third of a cord and a "
                   "pickup load half a cord.", BODY),
         Paragraph("Weights and estimates", H),
         Paragraph("Each respondent's weight is its zone's frame devices over its zone's respondents. The survey's "
                   "estimate of the wood burned in the 2024-25 heating season by an appliance of a class in a zone is "
                   "the weighted mean of the zone's respondents with that class, in cords (pellet stoves in tons). A "
                   "class with fewer than %d respondents in a zone takes the weighted mean of the class's respondents in "
                   "all five zones." % W.SMALL_CELL, BODY),
         Paragraph("Response", H),
         _table([["Burn zone", "Frame devices", "Sampled", "Responded"]] +
                [[W.ZNAME[z], format(W.SURVEY_FRAME[z], ","), format(W.SURVEY_SAMPLED[z], ","),
                  format(W.SURVEY_RESP[z], ",")] for z in W.ZC], [2.0 * inch, 1.2 * inch, 1.2 * inch, 1.2 * inch])]
    _pdf(path, "Survey methods", s, VENDOR, VENDOR)


def tool_pdf(path):
    hd = ParagraphStyle("th", parent=SMALL, fontName="Helvetica-Bold", fontSize=8, leading=9.5)
    cellp = ParagraphStyle("td", parent=SMALL, fontSize=8.5, leading=10)
    rows = [[Paragraph(x, hd) for x in ("Appliance", "SCC", "Seasonal heating efficiency", "Share of main-heat households",
                                         "Share of secondary households", "Use, main heat", "Use, secondary")]]
    for c in W.CL:
        scc, desc, code, eff, ef, med, sub = W.CLASSES[c]
        rows.append([Paragraph(P.SURVEY_LABEL[c], cellp), scc, ("%d%%" % round(eff * 100)) if eff else "not a heating appliance",
                     "%.2f" % P.TOOL_SHARE[True][c], "%.2f" % P.TOOL_SHARE[False][c],
                     "%.1f" % P.TOOL_USE[True][c], "%.2f" % P.TOOL_USE[False][c]])
    s = [Paragraph("Montana Residential Wood Combustion Estimating Tool, 2023 edition: Documentation", T),
         Paragraph("%s, Air Quality Bureau, Emission Inventory Section. November 2023." % W.STATE_DEQ, BODY),
         Paragraph("1. Purpose", H),
         Paragraph("The tool estimates residential wood combustion by county for the state's submissions to the "
                   "national emissions inventory. Counties and local programs with their own registry and survey may "
                   "submit their own estimates for the areas those cover.", BODY),
         Paragraph("2. Appliances and fuel", H),
         Paragraph("The appliance classes, their source classification codes and characteristics are in Table 1. Use is "
                   "in cords a year (pellet stoves in tons of pellets). A cord of the state's mixed softwoods (lodgepole "
                   "pine, Douglas fir and western larch, seasoned) holds %.1f million Btu and weighs %.3f tons; a ton of "
                   "pellets holds %.1f million Btu. Seasonal heating efficiency is the share of the fuel's heat the "
                   "appliance delivers to the home over a heating season." % (W.CORD_MMBTU, W.TONS_PER_CORD,
                                                                             W.PELLET_MMBTU_TON), BODY),
         _table(rows, [1.7 * inch, 0.8 * inch, 1.35 * inch, 0.85 * inch, 0.85 * inch, 0.6 * inch, 0.75 * inch]),
         Spacer(1, 4), Paragraph("Table 1. Appliance classes.", SMALL),
         Paragraph("3. Areas without a local survey", H),
         Paragraph("Households heating mainly with wood are the American Community Survey's table B25040 (house heating "
                   "fuel: wood) for each block group, from the five-year release whose final year is two years before the "
                   "first year of the inventory season. Households burning wood as a secondary heat source are %.1f "
                   "times the main-heat households. Each group is split across the appliance classes by the shares in "
                   "Table 1 and each appliance burns the use shown. A block group divided by the boundary of an area a "
                   "local program covers is taken by its share of housing units outside that area, from the county "
                   "assessor's housing unit counts." % P.TOOL_SECONDARY, BODY),
         Paragraph("4. Emission factors", H),
         Paragraph("The tool applies the department's 2023 factors in pounds per ton of wood burned by source "
                   "classification code.", BODY)]
    _pdf(path, "RWC tool documentation", s, "Emission Inventory Section", W.STATE_DEQ)
