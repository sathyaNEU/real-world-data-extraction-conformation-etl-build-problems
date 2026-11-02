"""The pack's documents: the company's network operations standard NOS 12, the outage plan for the Ferrars Lane
relining, and the 2024 trunk mains condition assessment. No document describes a data file."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif", FONT_DIR + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif-Bold", FONT_DIR + "LiberationSerif-Bold.ttf"))
SANS, SANS_B, SERIF, SERIF_B = "LiberationSans", "LiberationSans-Bold", "LiberationSerif", "LiberationSerif-Bold"
INK = colors.HexColor("#1b2430")
GREY = colors.HexColor("#5d6872")
BLUE = colors.HexColor("#0f4c81")
RULE = colors.HexColor("#9aa6ad")


def _styles(font, bold, size=10.0, accent=INK):
    body = ParagraphStyle("b", fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        num=ParagraphStyle("n", parent=body, leftIndent=28, firstLineIndent=-28),
        h1=ParagraphStyle("h1", fontName=bold, fontSize=size + 5, leading=size + 9, textColor=accent, spaceAfter=3),
        h2=ParagraphStyle("h2", fontName=bold, fontSize=size + 1, leading=size + 5, textColor=accent, spaceBefore=7,
                          spaceAfter=3),
        small=ParagraphStyle("s", fontName=font, fontSize=size - 1.6, leading=(size - 1.6) * 1.35, textColor=GREY,
                             spaceAfter=3),
        cell=ParagraphStyle("c", fontName=font, fontSize=size - 1.5, leading=(size - 1.5) * 1.25, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=bold, fontSize=size - 1.8, leading=(size - 1.8) * 1.25, textColor=INK),
    )


def _doc(path, title, author, subject, footer):
    def page(canvas, doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(18 * mm, 10 * mm, footer)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                          bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=author,
                          producer=W.COMPANY)
    return d, page


def _table(rows, widths, st, header_rows=1, zebra=False):
    data = []
    for i, r in enumerate(rows):
        data.append([Paragraph(str(c), st["cellb"] if i < header_rows else st["cell"]) for c in r])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=header_rows)
    style = [("LINEBELOW", (0, header_rows - 1), (-1, header_rows - 1), 0.6, RULE),
             ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.0),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0), ("LEFTPADDING", (0, 0), (-1, -1), 3),
             ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if zebra:
        for i in range(header_rows, len(rows)):
            if (i - header_rows) % 2 == 1:
                style.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f0f3f5")))
    t.setStyle(TableStyle(style))
    return t


# ------------------------------------------------------------------------------------------------ NOS 12
STANDARD_42 = ("A trunk main that the change would carry at a higher hourly flow than the highest hourly flow it "
               "carried in the twelve months to the end of the month before the outage plan is prepared shall be "
               "flushed before the change is made.")
STANDARD_43 = "Flows under the change are judged on the districts' recorded hourly inflows for the same dates a year earlier."
STANDARD_TRUNK = ("Trunk main: a main listed in the company's trunk mains register. The register's interconnectors are "
                  "trunk mains.")


def standard(path):
    st = _styles(SERIF, SERIF_B, 10.2, BLUE)
    d, page = _doc(path, "NOS 12 Planned changes to supply routes: discolouration", W.PEOPLE["wq"],
                   "Network Operations Standard", "%s | NOS 12 Planned changes to supply routes | Issue 3" % W.COMPANY)
    f = []
    f.append(Paragraph(W.COMPANY.upper(), st["small"]))
    f.append(Paragraph("Network Operations Standard NOS 12", st["h1"]))
    f.append(Paragraph("Planned changes to supply routes: discolouration", st["h2"]))
    f.append(_table([["Issue", "Effective", "Owner", "Approved"],
                     ["3", "1 April 2025", "%s, %s" % (W.PEOPLE["wq"], W.TITLES["wq"]),
                      "%s, %s" % (W.PEOPLE["head_ops"], W.TITLES["head_ops"])]], [14, 26, 64, 66], st))
    f.append(Spacer(1, 6))
    f.append(Paragraph("1  Purpose", st["h2"]))
    f.append(Paragraph("This standard sets how the company controls the risk of discoloured water reaching customers "
                       "when it changes the route by which water reaches them through the trunk mains.", st["body"]))
    f.append(Paragraph("2  Scope", st["h2"]))
    f.append(Paragraph("It applies to every planned change in the route by which water reaches one or more districts "
                       "through the trunk mains that is to last more than 24 hours: a planned outage of a trunk main, a "
                       "re-zoning, or the commissioning of a new interconnection.", st["body"]))
    f.append(Paragraph("3  Definitions", st["h2"]))
    f.append(Paragraph("3.1  " + STANDARD_TRUNK, st["num"]))
    f.append(Paragraph("3.2  District: a district metered area. Its inflow is the flow recorded by its inlet meter.",
                       st["num"]))
    f.append(Paragraph("3.3  Outage plan: the plan prepared by Network Operations that sets the valve operations and "
                       "the supply arrangements for a planned change.", st["num"]))
    f.append(Paragraph("4  Assessment before a planned change", st["h2"]))
    f.append(Paragraph("4.1  The outage plan for each planned change is assessed under this section before the change "
                       "is made, and the result is recorded with the plan.", st["num"]))
    f.append(Paragraph("4.2  " + STANDARD_42, st["num"]))
    f.append(Paragraph("4.3  " + STANDARD_43, st["num"]))
    f.append(Paragraph("4.4  Flushing under 4.2 is completed in the six weeks before the change, in sections, from "
                       "hydrants or washouts at the downstream end of each section, until the discharge stays below "
                       "1.0 NTU for ten minutes.", st["num"]))
    f.append(Paragraph("4.5  Customers in the districts whose route changes are told of the change at least 14 days "
                       "before it is made.", st["num"]))
    f.append(Paragraph("5  Routine flushing", st["h2"]))
    f.append(Paragraph("5.1  Distribution mains in districts with a record of discolouration contacts are flushed on a "
                       "rolling programme agreed each year between Water Quality and Network Operations and carried out "
                       "by the mains flushing contractor.", st["num"]))
    f.append(Paragraph("6  Records", st["h2"]))
    f.append(Paragraph("The assessment under section 4 records each trunk main assessed, the flows compared and "
                       "whether the main was flushed, and is kept with the outage plan for six years.", st["body"]))
    f.append(Spacer(1, 8))
    f.append(Paragraph("Issue history", st["h2"]))
    f.append(_table([["Issue", "Date", "Change"],
                     ["1", "June 2018", "First issue."],
                     ["2", "February 2021", "Interconnectors brought within the definition of a trunk main."],
                     ["3", "March 2025", "Reference period and the basis for judging flows under a change restated "
                                         "(4.2, 4.3); customer notice period added (4.5)."]], [14, 28, 128], st))
    d.build(f, onFirstPage=page, onLaterPages=page)


# ------------------------------------------------------------------------------------------------ the outage plan
def plan(path, vlist):
    st = _styles(SANS, SANS_B, 9.6, BLUE)
    vno = {(v["key"], v["end"]): v for v in vlist}
    d, page = _doc(path, "Ferrars Lane trunk main relining, phase 2: outage plan", W.PEOPLE["planner"],
                   "Outage plan", "%s | Network Operations | TM107 relining phase 2 outage plan | v1.0" % W.COMPANY)
    f = []
    f.append(Paragraph(W.COMPANY.upper() + "  |  NETWORK OPERATIONS", st["small"]))
    f.append(Paragraph("TM107 Ferrars Lane trunk main relining (phase 2): outage plan", st["h1"]))
    f.append(_table([["Version", "Date", "Prepared by", "Approved by"],
                     ["1.0", "16 November 2026", "%s, %s" % (W.PEOPLE["planner"], W.TITLES["planner"]),
                      "%s, %s" % (W.PEOPLE["head_ops"], W.TITLES["head_ops"])]], [16, 30, 64, 60], st))
    f.append(Paragraph("1  Scope of the works", st["h2"]))
    f.append(Paragraph("TM107, the Ferrars Lane main between Market Hill and Ferrars Corner (2,310 m of 375 mm cast "
                       "iron laid in 1931), is to be relined with a close-fit polyethylene lining as phase 2 of the trunk "
                       "mains relining programme. The contractor takes possession on 15 March 2027 and TM107 is out of service from 15 March to "
                       "15 September 2027.", st["body"]))
    f.append(Paragraph("2  Supply arrangements during the works", st["h2"]))
    f.append(Paragraph("The valves below are set on 15 March 2027 from 05:00, in this order. Every other valve stays "
                       "in its normal position for the duration, and each is returned on completion.", st["body"]))
    ops = [("X04", "B", "Open", "Coldharbour-Ferrars interconnector, boundary valve"),
           ("X02", "B", "Open", "Highfield-Sallowby interconnector, boundary valve"),
           ("T10", "A", "Shut", "Sallowby Road main"),
           ("T10", "B", "Shut", "Sallowby Road main"),
           ("T03", "A", "Shut", "Ferrars Lane main"),
           ("T03", "B", "Shut", "Ferrars Lane main")]
    rows = [["Step", "Valve", "Main", "Location", "Set to"]]
    for i, (k, end, op, desc) in enumerate(ops):
        v = vno[(k, end)]
        rows.append([str(i + 1), v["valve_no"], "%s %s" % (W.MAIN_ID[k], desc), v["location"], op])
    f.append(_table(rows, [11, 20, 82, 34, 20], st))
    f.append(Spacer(1, 4))
    f.append(Paragraph("Ferrars Corner and Mill Bridge are supplied from Coldharbour through IC05 for the duration. "
                       "The Sallowby districts are held on the Highfield feed through IC03, with TM115 shut at both ends "
                       "so that the two routes are kept apart.", st["body"]))
    f.append(Paragraph("3  Districts supplied by another route", st["h2"]))
    rows = [["District", "Name", "Supplied during the works through"]]
    for dk in W.REROUTED:
        rows.append([W.DCODE[dk], W.DISTRICTS[dk][1], "IC05 (Coldharbour)" if W.DNODE[dk] in ("N3", "N4")
                     else "IC03 (Highfield)"])
    f.append(_table(rows, [24, 40, 60], st, zebra=True))
    f.append(Paragraph("4  Water quality", st["h2"]))
    f.append(Paragraph("The arrangement in section 2 is a planned change under NOS 12. The assessment under NOS 12 "
                       "section 4 is to be completed and attached to this plan before the flushing works order is "
                       "raised; any flushing it requires is to be done between 1 February and 12 March 2027.",
                       st["body"]))
    f.append(Paragraph("5  Customers", st["h2"]))
    f.append(Paragraph("Every customer in the districts in section 3 is written to by 1 March 2027. Non-household "
                       "customers in those districts are contacted individually by the Business Customers team before "
                       "the works, with the water they used over the last twelve months, so that any with a continuous "
                       "process can plan for the change.", st["body"]))
    f.append(Paragraph("6  Key dates", st["h2"]))
    f.append(_table([["Date", "Step"],
                     ["15 January 2027", "Flushing works order placed with the mains flushing contractor"],
                     ["1 February to 12 March 2027", "Flushing, where the assessment requires it"],
                     ["1 March 2027", "Customer letters issued"],
                     ["15 March 2027, 05:00", "Valves set as in section 2; TM107 handed to the contractor"],
                     ["15 September 2027", "TM107 returned to service; valves in section 2 returned"]],
                    [52, 118], st))
    d.build(f, onFirstPage=page, onLaterPages=page)


# ------------------------------------------------------------------------------------------------ distractor
def condition(path, rows):
    st = _styles(SANS, SANS_B, 9.4, colors.HexColor("#3b5323"))
    d, page = _doc(path, "Trunk mains condition assessment 2024", W.PEOPLE["asset"], "Asset condition",
                   "%s | Asset Management | Trunk mains condition assessment 2024" % W.COMPANY)
    f = []
    f.append(Paragraph(W.COMPANY.upper() + "  |  ASSET MANAGEMENT", st["small"]))
    f.append(Paragraph("Trunk mains condition assessment 2024", st["h1"]))
    f.append(Paragraph("%s, %s. 23 September 2024." % (W.PEOPLE["asset"], W.TITLES["asset"]), st["small"]))
    f.append(Paragraph("1  Basis", st["h2"]))
    f.append(Paragraph("Each trunk main in the Stavenham register was graded on its structural condition from pipe "
                       "samples taken at planned excavations between 2021 and 2024, acoustic wall-thickness surveys "
                       "in 2023 and the joint leakage tests of 2024. Grade 1 is as new and grade 5 is at the end of its "
                       "life. Residual wall is the median remaining wall thickness against the original.", st["body"]))
    f.append(Paragraph("2  Findings", st["h2"]))
    hdr = [["Main", "Name", "DN", "Material", "Laid", "Grade", "Residual wall %", "Joints", "Residual life (yrs)",
            "Recommendation"]]
    f.append(_table(hdr + [list(r) for r in rows], [13, 34, 9, 15, 10, 10, 14, 20, 14, 31], st, zebra=True))
    f.append(Paragraph("3  Recommendations", st["h2"]))
    f.append(Paragraph("The Ferrars Lane main (TM107) and the Brook Street main (TM105) are at grade 4 and are "
                       "recommended for close-fit relining, TM105 first. The Mill Road main (TM108) follows in a third "
                       "phase. No other main needs structural intervention within the current asset plan period; the "
                       "interconnectors' valves should be exercised to the programme.", st["body"]))
    d.build(f, onFirstPage=page, onLaterPages=page)
