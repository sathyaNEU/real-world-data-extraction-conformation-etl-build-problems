"""The pack's documents: an excerpt of the Municipal Road Aid Act and the Center's statement of its 2026 municipal
estimates program, each in its own office's voice."""
from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors                                    # noqa: E402
from reportlab.lib.pagesizes import letter                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                     # noqa: E402
from reportlab.lib.units import inch                                # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer  # noqa: E402

import world as W  # noqa: E402

BODY = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=14, spaceAfter=6)
SEC = ParagraphStyle("s", fontName="Times-Bold", fontSize=10.5, leading=14, spaceBefore=6, spaceAfter=3)
TITLE = ParagraphStyle("t", fontName="Times-Bold", fontSize=13, leading=17, spaceAfter=2, alignment=1)
SUB = ParagraphStyle("u", fontName="Times-Italic", fontSize=9.5, leading=12, spaceAfter=10, alignment=1)
HB = ParagraphStyle("hb", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceBefore=8, spaceAfter=3)
HBODY = ParagraphStyle("hbody", fontName="Helvetica", fontSize=9.6, leading=13, spaceAfter=6)
HTITLE = ParagraphStyle("ht", fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=3)
HSUB = ParagraphStyle("hs", fontName="Helvetica", fontSize=8.8, leading=11.5, textColor=colors.HexColor("#3a4a5a"),
                      spaceAfter=10)


def _doc(path, title, author, footer):
    d = SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch, topMargin=0.9 * inch,
                          bottomMargin=0.9 * inch, title=title, author=author, creator=author, producer=author,
                          subject=title)

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(1.0 * inch, 0.55 * inch, footer)
        c.drawRightString(letter[0] - 1.0 * inch, 0.55 * inch, "%d" % d_.page)
        c.restoreState()
    return d, frame


ACT = [
    ("84.21 Definitions.", "In this subchapter:"),
    ("", "(1) \"Aid year\" means the calendar year for which aid is paid."),
    ("", "(2) \"Department\" means the department of transportation."),
    ("", "(3) \"Municipality\" means a city, village or town."),
    ("", "(4) \"Population\" means the number of residents of a municipality on July 1 of the year before the aid "
         "year, as certified by the state data center under s. 84.27."),
    ("", "(5) \"Local road\" means a public highway under the jurisdiction of a municipality."),
    ("", "(6) \"Urban municipality\" means a municipality whose population is 10,000 or more."),
    ("84.23 General transportation aid.", "(1) The department shall pay to each municipality for each aid year the "
     "greater of the amount computed under sub. (2) or the amount computed under sub. (3)."),
    ("", "(2) For a municipality other than an urban municipality, the rate per mile under s. 84.25 (1) times the "
         "miles of local road under its jurisdiction on January 1 of the year before the aid year."),
    ("", "(3) For an urban municipality, the rate per mile under s. 84.25 (2) times those miles, plus the urban street "
         "allowance under s. 84.25 (3) for each 1,000 of population."),
    ("84.25 Rates.", "(1) The rural rate is the amount per mile appropriated for the aid year divided as the "
     "department determines under s. 84.23 (2)."),
    ("", "(2) The urban rate per mile is 1.35 times the rural rate."),
    ("", "(3) The urban street allowance is the amount the department determines for the aid year for each 1,000 of "
         "an urban municipality's population."),
    ("84.27 Certification of population.", "(1) On or before December 15 of each year the state data center shall "
     "certify to the secretary the population of each municipality for the next aid year."),
    ("", "(2) A certified population is final for the aid year it serves and may not be revised for that aid year."),
    ("", "(3) A municipality's classification as an urban municipality for an aid year follows the population "
         "certified for that aid year, whatever its classification in an earlier aid year."),
]


def write_act(path):
    title = "Municipal Road Aid Act (excerpt)"
    d, frame = _doc(path, title, "Legislative Reference Bureau",
                    "Statutes, ch. 84, subch. II (Municipal Road Aid). Unofficial text, updated through Act 112 of 2025.")
    s = [Paragraph("CHAPTER 84", TITLE), Paragraph("SUBCHAPTER II: MUNICIPAL ROAD AID", TITLE),
         Paragraph("Unofficial text prepared by the Legislative Reference Bureau. Updated through 2025 Act 112.", SUB)]
    for head, text in ACT:
        if head:
            s.append(Paragraph("<b>%s</b> %s" % (head, text), BODY))
        else:
            s.append(Paragraph(text, BODY))
    s.append(Spacer(1, 6))
    s.append(Paragraph("History: 1997 a. 27; 2005 a. 25; 2013 a. 20; 2025 a. 112.", SUB))
    d.build(s, onFirstPage=frame, onLaterPages=frame)


def write_statement(path):
    title = "Municipal Population Estimates Program: the 2026 Estimates"
    lead, role = W.PEOPLE["demographer"]
    mgr, mrole = W.PEOPLE["estimates"]
    d, frame = _doc(path, title, "%s, %s" % (W.OFFICE, W.DEPT),
                    "%s, %s  |  Municipal Population Estimates Program, 2026 estimates" % (W.CENTER, W.OFFICE))
    s = [Paragraph("Municipal Population Estimates Program", HTITLE),
         Paragraph("Statement of the 2026 estimates. %s, %s, %s. Issued 3 August 2026." % (W.CENTER, W.OFFICE, W.DEPT),
                   HSUB),
         Paragraph("1. The estimates", HB),
         Paragraph("Each year the Center estimates the population of every city, village and town in the state on 1 July "
                   "and certifies the estimates to the Secretary of Transportation by 15 December, under s. 84.27 of the "
                   "Municipal Road Aid Act, for the next aid year. The estimates of 1 July 2026 serve the 2027 aid "
                   "year.", HBODY),
         Paragraph("2. What an estimate counts", HB),
         Paragraph("A municipality's estimate is the number of its residents on 1 July: the persons whose usual residence "
                   "on that date is a dwelling in the municipality, and the residents of its group quarters. A dwelling "
                   "is in the municipality if it lies within the municipality's boundaries in force on 1 July. The "
                   "residents of group quarters are those recorded for the municipality's facilities by the Center's "
                   "annual survey of group quarters.", HBODY),
         Paragraph("Each estimate is certified as a whole number of residents. A certified estimate is final for the aid "
                   "year it serves; the Center does not revise it when later information arrives, and the next year's "
                   "estimate stands on its own.", HBODY),
         Paragraph("3. Births and deaths", HB),
         Paragraph("With the estimates the Center reports each municipality's resident births and resident deaths for the "
                   "estimate year, 1 July 2025 to 30 June 2026. A birth is counted by its date in the municipality in "
                   "which the mother lived, each live-born child one birth; a death by its date in the municipality in "
                   "which the decedent lived, a resident of group quarters in the municipality of the facility.", HBODY),
         Paragraph("4. Records the Center uses", HB),
         Paragraph("County real property rolls; certificates of occupancy and demolition permits from municipal building "
                   "inspectors; the 2020 census and earlier censuses; the state's register of municipal boundary changes; "
                   "the Center's annual survey of group quarters; county address points; and the State Registrar's "
                   "resident birth and death files.", HBODY),
         Paragraph("5. Schedule for 2026", HB),
         Paragraph("Records requested from counties: 1 to 31 August 2026. Preliminary estimates to municipalities for "
                   "review: 16 October 2026. Municipal challenges close: 20 November 2026. Certification to the "
                   "Secretary: 15 December 2026.", HBODY),
         Spacer(1, 8),
         Paragraph("%s, %s<br/>Questions: %s, %s" % (lead, role, mgr, mrole), HBODY)]
    d.build(s, onFirstPage=frame, onLaterPages=frame)
