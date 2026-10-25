"""The pack's documents: the Commission's technical guidance on the electorate forecast with its letter fixing the
Lorrimere review's dates, and the council's report on the 2025 annual canvass."""
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

reportlab.rl_config.invariant = 1
STY = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=STY["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.8, spaceAfter=6)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10)
H = ParagraphStyle("h", parent=STY["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=4)
T = ParagraphStyle("t", parent=STY["Title"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=10, alignment=0)
STAMPS = {"guidance": b"D:20260302094500+00'00'", "canvass": b"D:20251212112000+00'00'"}
COMMISSION = "Local Government Boundary Commission"
COUNCIL = "Lorrimere District Council"


def _pdf(path, title, story, author, org):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=org, subject=title, producer=org)

    def footer(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(20 * mm, 11 * mm, org + "  |  " + title)
        c.drawRightString(A4[0] - 20 * mm, 11 * mm, "%d" % d.page)
        c.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def P(text, style=BODY):
    return Paragraph(text, style)


def _table(rows, widths=None, size=8.5):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def guidance_pdf(path):
    s = [P("Electoral reviews: the electorate forecast", T),
         P("Technical guidance note 3, 2024 edition. " + COMMISSION + ". This note replaces the 2019 edition.", SMALL),
         P("1. What the forecast is for", H),
         P("The Commission bases its recommendations on the number of electors it expects in each area five years after "
           "the date on which it expects to publish its final recommendations, so that the pattern it recommends still "
           "gives good electoral equality when it has been in place for some years. The forecast date is fixed for each "
           "review in the Commission's letter to the council at the start of the review."),
         P("The electorate is the number of local government electors aged 18 or over on the revised register published on "
           "1 December of the forecast year. Attainers, and overseas electors registered for parliamentary elections only, "
           "are not electors for this purpose. Electors registered for local government elections only are."),
         P("2. Electoral equality", H),
         P("For each ward the Commission divides the forecast electorate by the number of councillors the ward elects, "
           "and compares the result with the average for the authority: the authority's whole forecast electorate divided "
           "by its council size. A ward whose electors per councillor lie more than 10 per cent above or below that "
           "average does not provide good electoral equality. At the start of a review the Commission tests the authority's "
           "existing wards, with their existing boundaries and numbers of councillors, against the forecast."),
         P("3. What the forecast counts", H),
         P("The forecast covers the electors expected on the forecast-year register at every dwelling then in use in the "
           "authority: the dwellings in use today, and the new dwellings the council's housing trajectory expects to be "
           "completed by the date of the forecast-year register, as the trajectory phases them. Sites without planning "
           "permission or an allocation are not counted, and the Commission does not substitute its own view of when a "
           "site will deliver for the council's."),
         P("4. What the Commission asks the council for", H),
         P("The register at property level for each of the last six revised registers, with each property's unique property "
           "reference number (UPRN); an extract of the local land and property gazetteer; the council's completions "
           "monitoring and housing trajectory; and the current polling district scheme. Where the register has moved "
           "between electoral management systems, the council should send the cross-reference it holds between the "
           "systems' property references."),
         P("5. How the forecast is checked", H),
         P("Officers check the forecast against the registers and the council's monitoring before the Commission relies on "
           "it, and may prepare the forecast themselves from the council's data. The forecast is published with the "
           "Commission's draft recommendations."),
         Spacer(1, 10),
         P("Annex: letter to the Chief Executive, " + COUNCIL + ", 2 March 2026", H),
         P("The Commission will begin an electoral review of Lorrimere District in April 2026. The council size remains "
           "43 councillors for the purposes of the review. The Commission expects to publish its final recommendations in "
           "June 2027, and the forecast date for the review is accordingly the register to be published on 1 December "
           "2032. The Commission will meet on 17 November 2026 to consider the existing wards against the forecast and to "
           "agree the areas its draft recommendations will address. Megan Stewart, Review Manager, will be the council's "
           "contact for the review.", BODY)]
    _pdf(path, "Electoral reviews: the electorate forecast", s, "Megan Stewart", COMMISSION)


def canvass_pdf(path, stats):
    s = [P("Annual canvass 2025: report to the Electoral Registration Officer", T),
         P(COUNCIL + ", Electoral Services. Donald Hayes, Electoral Services Manager. 12 December 2025.", SMALL),
         P("1. Timetable", H),
         P("The property database is refreshed from the local land and property gazetteer every week. The canvass covers "
           "every residential property on the database on 31 August. Before canvass communications were issued the "
           "register was matched against national and local data, and properties whose electors all matched were sent a "
           "canvass communication A (route 1); other properties were sent canvass communication B (route 2), followed by "
           "reminders and a household visit where no response was received; flats in sheltered housing schemes were "
           "canvassed through the scheme manager (route 3). Invitations to register were sent to each new person a response "
           "named. The revised register was published on 1 December 2025 and includes every application determined by 31 "
           "October."),
         P("Properties that come into use after 31 August are canvassed in the following year. Residents may apply to "
           "register at any time, and applications determined after the revised register is published appear in the "
           "monthly notices of alteration from January to September."),
         P("2. The canvass in numbers", H),
         _table([["", "Properties", "Share"],
                 ["Route 1 (canvass communication A)", "{:,}".format(stats["r1"]), "%.1f%%" % (100.0 * stats["r1"] / stats["props"])],
                 ["Route 2 (canvass communication B)", "{:,}".format(stats["r2"]), "%.1f%%" % (100.0 * stats["r2"] / stats["props"])],
                 ["Route 3 (scheme manager)", "{:,}".format(stats["r3"]), "%.1f%%" % (100.0 * stats["r3"] / stats["props"])],
                 ["All residential properties canvassed", "{:,}".format(stats["props"]), "100.0%"]],
                widths=[95 * mm, 35 * mm, 25 * mm]),
         Spacer(1, 6),
         P("Route 2 properties returned a response or were visited in %.1f per cent of cases. Electors on the revised "
           "register: %s local government electors, %s attainers and %s overseas electors." % (
               stats["resp"], "{:,}".format(stats["lg"]), "{:,}".format(stats["att"]), "{:,}".format(stats["ov"]))),
         P("3. Changes for 2026", H),
         P("The 2026 canvass will follow the same timetable. The review of polling districts and places that took effect "
           "with the 2023 register is not due to be repeated until 2028. The register at property level for 2020 and 2021 "
           "remains available from the archive of the Electra system, which the council replaced in March 2022.")]
    _pdf(path, "Annual canvass 2025", s, "Donald Hayes", COUNCIL)
