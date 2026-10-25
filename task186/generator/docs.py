"""The pack's documents: the Prices Division's pass-through monitoring standard, Schedule 2 of the Carbon Levy
Regulation, and the extract notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import LETTER                                         # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W      # noqa: E402

STANDARD = "pass_through_monitoring_standard_PM-04.pdf"
SCHEDULE = "carbon_levy_regulation_schedule_2.pdf"
NOTES = "extract_notes_2026-11-16.md"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Serif", "LiberationSerif-Regular"),
              ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
INK, GREY = colors.HexColor("#1f2329"), colors.HexColor("#5d646c")

BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5)
CLAUSE = ParagraphStyle("c", parent=BODY, leftIndent=26, firstLineIndent=-26)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=14, leading=18, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.2, leading=13.5, textColor=INK, spaceBefore=8, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.2, leading=10.6, textColor=GREY, spaceAfter=8)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.8, leading=11.2, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")
SBODY = ParagraphStyle("sb", fontName="Serif", fontSize=10.2, leading=13.6, textColor=INK, spaceAfter=5)
SCL = ParagraphStyle("scl", parent=SBODY, leftIndent=22, firstLineIndent=-22)
SH1 = ParagraphStyle("sh1", fontName="Serif-B", fontSize=13, leading=17, textColor=INK, spaceAfter=3)
SMETA = ParagraphStyle("smeta", fontName="Serif", fontSize=8.6, leading=11, textColor=GREY, spaceAfter=8)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=24 * mm, rightMargin=24 * mm, topMargin=20 * mm,
                             bottomMargin=19 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot, font="Sans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.8)
        canvas.drawString(24 * mm, LETTER[1] - 11 * mm, top_left)
        canvas.drawRightString(LETTER[0] - 24 * mm, LETTER[1] - 11 * mm, top_right)
        canvas.setFont(font, 7.2)
        canvas.drawString(24 * mm, 10 * mm, foot)
        canvas.drawRightString(LETTER[0] - 24 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


STANDARD_CLAUSES = [
    ("1  Purpose", [
        ("1.1", "This standard sets how the Fuel Price Monitor measures, at each change of the provincial carbon levy, "
                "whether retail stations passed on more than the change to their pump prices, and how the Monitor's "
                "findings name the brand for the Fuel Price Commissioner's pass-through inquiry."),
    ]),
    ("2  Prices and margins", [
        ("2.1", "The Monitor measures regular gasoline at every retail station carrying a brand on the monitored "
                "brand register, from the price changes stations submit to the price reporting platform under the "
                "Fuel Price Transparency Act."),
        ("2.2", "A station's daily price is the time-weighted average of the regular prices in force at the station "
                "from 06:00 to 22:00 local time. A day on which the station had no price in force at 06:00 has no "
                "daily price."),
        ("2.3", "A station's daily margin is its daily price net of the 5 per cent sales tax, less the levy in force "
                "that day for gasoline under Schedule 2 of the Carbon Levy Regulation, less that day's rack price for "
                "regular at Port Ostley Terminal. On a day the terminal does not publish, its latest published price "
                "applies."),
    ]),
    ("3  Changes of the levy", [
        ("3.1", "At a levy change, a station's margin change is the mean of its daily margins over the 28 days from "
                "the change less the mean of its daily margins over the 28 days before it."),
        ("3.2", "A station is examined at a change when it carried a monitored brand on the station register on the "
                "day of the change and had a daily price on at least 20 of each of the two 28-day periods."),
        ("3.3", "A station passed on more than the levy rise when its margin rose across the change by more than it "
                "would have had the levy not changed. The Monitor reports these findings with the false discovery "
                "rate across every station examined at the change held at 5 per cent, by the Benjamini-Hochberg "
                "procedure."),
    ]),
    ("4  The pass-through inquiry", [
        ("4.1", "Before each levy change the Commissioner opens one pass-through inquiry. The Monitor recommends the "
                "brand with the largest share of its examined stations found under 3.3 at the previous change, "
                "provided that share is at least one in ten; if no brand reaches one in ten, it recommends that no "
                "inquiry be opened."),
        ("4.2", "The inquiry's information request covers the stations whose pump prices the brand sets."),
    ]),
    ("5  Records", [
        ("5.1", "The Monitor keeps the platform's price changes, the station register and the terminal's rack prices "
                "for at least three years, and works from the platform's records, not from the weekly bulletin."),
    ]),
]


def write_standard(path):
    who, role = W.PEOPLE["director"]
    title = "Levy pass-through monitoring"
    doc = _doc(path, title, who)
    s = [Paragraph(W.BUREAU.upper() + " · " + W.DIVISION.upper(), META), Paragraph("Standard PM-04: " + title, H1),
         Paragraph("Revision 2, effective 1 October 2025. Owner: %s, %s." % (who, role), META)]
    for head, items in STANDARD_CLAUSES:
        s.append(Paragraph(head, H2))
        for num, text in items:
            s.append(Paragraph("%s&nbsp;&nbsp;&nbsp;%s" % (num, text), CLAUSE))
    foot = W.BUREAU + " | Standard PM-04 | revision 2"
    doc.build(s, onFirstPage=_frame(W.DIVISION, "PM-04 rev. 2", foot), onLaterPages=_frame(W.DIVISION, "PM-04 rev. 2", foot))


def write_schedule(path):
    title = "Carbon Levy Regulation: Schedule 2, rates of levy"
    doc = _doc(path, title, "")
    rows = [[Paragraph(x, CELLB) for x in ("Calendar year", "Dollars a tonne of CO2e", "Gasoline, cents a litre",
                                             "Light fuel oil (diesel), cents a litre")]]
    for y in (2025, 2026, 2027):
        rows.append([Paragraph(x, CELL) for x in (str(y), "%d" % W.LEVY_PER_TONNE[y], "%.2f" % W.LEVY["gasoline"][y],
                                                     "%.2f" % W.LEVY["diesel"][y])])
    t = Table(rows, colWidths=[30 * mm, 40 * mm, 40 * mm, 52 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s = [Paragraph("CONSOLIDATED REGULATION · OFFICE CONSOLIDATION", SMETA), Paragraph(title, SH1),
         Paragraph("Current to 30 September 2026.", SMETA),
         Paragraph("1&nbsp;&nbsp;&nbsp;The levy on each litre of a fuel delivered out of a terminal in a calendar year "
                   "is the rate in the table for that fuel and year.", SCL),
         Paragraph("2&nbsp;&nbsp;&nbsp;A rate takes effect at 00:00 on 1 January of its year.", SCL),
         Spacer(1, 6), t, Spacer(1, 8),
         Paragraph("The per-litre rates are the dollars a tonne multiplied by the emission factor for the fuel set out in "
                   "Schedule 1, rounded to the hundredth of a cent.", SMETA)]
    foot = "Carbon Levy Regulation | Schedule 2"
    doc.build(s, onFirstPage=_frame("Office consolidation", "Schedule 2", foot, "Serif"),
              onLaterPages=_frame("Office consolidation", "Schedule 2", foot, "Serif"))


NOTES_TEXT = """# Extract for the 2027 pass-through recommendation

Pulled 16 Nov 2026 by {analyst} for {director}. Platform tables, survey files and the terminal's rack file as held
on the bureau's shared drive that morning.

Files:
- {log}: every regular-gasoline price change the platform received from 1 Jan 2025 to 15 Nov 2026.
- {rack}: the terminal's published rack prices, all three products.
- {register}: the platform's station table and brand history.
- {crosswalk}: old station numbers to the new ones issued on 8 Jun 2026.
- {survey}: the monthly fuel sales survey returns for 2026 to date.
- {frame}: the sales survey frame as at this month.
- {subs}: every submission received in November 2026, all grades.
- {brands}: the monitored brand register.
- {opslog}: platform operations log.
- {bulletin}: the weekly bulletin as published.
- {complaints}: the Commissioner's price complaints line, 2026 to date (sent over by the Commissioner's office).
- {standard}, {schedule}: the standard and the levy rates.

Things to know:
- effective_utc and received_utc are UTC. Local time is UTC-5, and UTC-4 from the second Sunday in March to the first
  Sunday in November.
- A row in the price files is one change as submitted: the price stands until the station's next change, or until
  the station closes (the register's closed date).
- Station numbers changed on 8 Jun 2026. Stations that closed before then keep their old number in the register.
- channel: API is a system-to-system submission, POS the forecourt terminal, PORTAL keyed on the web portal.
"""


def write_notes(path, names):
    open(path, "w").write(NOTES_TEXT.format(analyst=W.PEOPLE["analyst"][0], director=W.PEOPLE["director"][0],
                                            standard=STANDARD, schedule=SCHEDULE, **names))
