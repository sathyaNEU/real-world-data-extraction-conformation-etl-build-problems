"""The pack's documents: the street lighting lifecycle model note (the program test), the luminaire maker's
certificates of conformance (one page a delivery lot) and the street lighting tariff, Schedule SL."""
from __future__ import annotations

import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import LETTER                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import params as P   # noqa: E402

FONT_DIR = next((d for d in ("/usr/share/fonts/truetype/liberation/", os.path.expanduser("~/Library/Fonts/"),
                              "/Library/Fonts/") if os.path.exists(d + "LiberationSerif-Regular.ttf")),
                "/usr/share/fonts/truetype/liberation/")
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1b2430"), colors.HexColor("#56616c"), colors.HexColor("#b8c0c8")
TEAL = colors.HexColor("#1d4e5a")
RUST = colors.HexColor("#6b3420")


def styles(face="Sans", accent=TEAL):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=10.0, leading=13.8, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=14.2, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.6, leading=14, textColor=INK, spaceBefore=8, spaceAfter=2,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.5, leading=11.3, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=8.1, leading=10.1, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=8.1, leading=10.1, textColor=INK),
        small=ParagraphStyle("s", fontName="Sans", fontSize=7.6, leading=9.6, textColor=GREY),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10.0, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=28, firstLineIndent=-28))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.5)
        canvas.drawString(0.9 * inch, LETTER[1] - 0.55 * inch, left)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, LETTER[1] - 0.55 * inch, right)
        canvas.drawRightString(LETTER[0] - 0.9 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=(), head=True):
    data = [[Paragraph(str(c), S["cellb"] if (i == 0 and head) else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1 if head else 0, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject, left, right, margins=0.9):
    return SimpleDocTemplate(path, pagesize=LETTER, leftMargin=margins * inch, rightMargin=margins * inch,
                             topMargin=0.85 * inch, bottomMargin=0.8 * inch, title=title, author=author,
                             subject=subject, creator=author, producer=author), _frame(left, right)


# ------------------------------------------------------------------------------------------ the lifecycle note
def write_note(path):
    S = styles("Serif", TEAL)
    doc, fr = _doc(path, "Street Lighting Lifecycle Model: Program Note SL-LM-04", P.PEOPLE["asset_engineer"],
                   "Group driver replacement program", "%s, Distribution Asset Management" % P.UTILITY,
                   "Program Note SL-LM-04, rev. 3")
    st = [Paragraph("Street Lighting Lifecycle Model: the Group Driver Replacement Program", S["h1"]),
          Paragraph("Program Note SL-LM-04, revision 3, 6 January 2027. Distribution Asset Management, street "
                    "lighting. Prepared by %s for the Asset Investment Committee. Revision 3 restates the program "
                    "test for the 2027 program year; revision 2 (January 2026) set the twelfth anniversary as the "
                    "horizon." % P.PEOPLE["asset_engineer"], S["meta"]),
          Paragraph("1. Purpose", S["h2"]),
          _clause(S, "1.1", "The street lighting lifecycle model projects driver failures in the LED luminaires the "
                            "Company installed in its 2021 to 2025 conversion of company streetlights from high-"
                            "pressure sodium (the conversion), and sets each year's group driver replacement program. "
                            "The Asset Investment Committee approves the program at its January meeting."),
          _clause(S, "1.2", "In a group replacement every luminaire of a conversion phase that is still on its "
                            "original driver is given a new driver in one planned campaign, scheduled by street. "
                            "Once failures in a phase climb, a campaign costs a fraction of the truck rolls the same "
                            "failures take one at a time, and it ends the outages they cause."),
          Paragraph("2. The program test", S["h2"]),
          _clause(S, "2.1", "A conversion phase enters the program year's group driver replacement when the expected "
                            "number of the phase's luminaires still on their original driver on 1 January of the "
                            "program year whose driver fails before the twelfth anniversary of the luminaire's "
                            "installation is more than 45 per cent of those luminaires."),
          _clause(S, "2.2", "A luminaire's original driver is the driver it was installed with. A driver failure is "
                            "an outage the luminaire's own driver caused, closed by a work order that replaced the "
                            "driver, and it dates from that work order's completion. A work order still open when "
                            "the record closes is not yet a failure."),
          _clause(S, "2.3", "A luminaire leaves the conversion when it is replaced, after a vehicle knockdown or under "
                            "the maker's warranty, or when its pole is removed; it leaves on the completion of the work "
                            "order that replaced or removed it. A luminaire installed in its place is not a "
                            "conversion luminaire."),
          _clause(S, "2.4", "Years of service run from the installation date the installer recorded, at 365.25 "
                            "days a year. A luminaire's phase is the conversion phase the installer recorded for it."),
          Paragraph("3. Projection", S["h2"]),
          _clause(S, "3.1", "Driver wear-out in years of service follows the two-parameter Weibull distribution, "
                            "fitted by maximum likelihood. A driver that has not failed is entered as a suspension at "
                            "its age on the day the record closes or the day its luminaire left the conversion."),
          _clause(S, "3.2", "Lifetimes are not estimated phase by phase: a phase's few years of record cannot carry a "
                            "twelve-year projection on its own."),
          _clause(S, "3.3", "For a program year the record closes on 31 December of the year before."),
          Paragraph("4. The 2027 program", S["h2"]),
          _clause(S, "4.1", "The 2027 campaign runs from March to October 2027. Field crews re-drive every original-"
                            "driver luminaire in each designated phase with the maker's service driver kit for its "
                            "wattage."),
          _clause(S, "4.2", "A phase that does not enter the program stays on spot replacement and is tested again "
                            "for the next program year."),
          Spacer(1, 8),
          Paragraph("Questions on this note go to Distribution Asset Management, street lighting (%s)."
                    % P.PEOPLE["asset_engineer"], S["note"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------ certificates
def write_coc(path, lots, rng):
    S = styles("Sans", RUST)
    doc, fr = _doc(path, "Certificates of Conformance, HRX roadway luminaires", P.MAKER, "Certificates of "
                   "conformance by delivery lot", "%s, Quality Assurance" % P.MAKER, "Certificates of Conformance",
                   margins=0.8)
    st = []
    # one purchase order a conversion phase, numbered in the utility's general series
    po_of, n = {}, 118230
    for pc in P.PHASE_CODES:
        n += int(rng.integers(900, 7400))
        po_of[pc] = "4500%06d" % n
    for k, L in enumerate(sorted(lots, key=lambda x: (x["ship"], x["lot"]))):
        ser0 = L["lot"].replace("HL", "HRX") + "-0001"
        ser1 = L["lot"].replace("HL", "HRX") + "-%04d" % L["qty"]
        drv_maker = P.DRV[L["src"]]
        led = "LM-%d-40K" % {40: 12, 70: 24, 110: 36}[L["watts"]]
        rev = str(rng.choice(["C", "C", "D"]))
        po = po_of[L["phase"]]
        rows = [["Component", "Part number", "Manufacturer", "Rev."],
                ["LED array", led, P.MAKER, rev],
                ["LED driver, programmable, 0-10 V dimming", L["drv_part"].rsplit("-", 1)[0], drv_maker,
                 L["drv_part"].rsplit("-", 1)[1]],
                ["Surge protective device, 10 kV / 5 kA", "SP-10K", P.MAKER, "B"],
                ["Photocontrol receptacle, 7-pin ANSI C136.41", "RCP-7P", "Lorand Controls", "A"],
                ["Housing and optic", "HRX-H%d" % {40: 2, 70: 3, 110: 4}[L["watts"]], P.MAKER, "E"]]
        tests = [["Sample", "Input W", "Power factor", "THD %", "Lumens"]]
        base = {40: 40.8, 70: 71.6, 110: 112.4}[L["watts"]]
        for s in range(1, 4):
            tests.append(["%d" % s, "%.1f" % (base + rng.normal(0, .5)), "%.3f" % (0.97 + rng.uniform(0, .025)),
                          "%.1f" % rng.uniform(5.5, 11.5), "%d" % int(base * 128 + rng.normal(0, 90))])
        st += [Paragraph("Certificate of Conformance", S["h1"]),
               Paragraph("%s, roadway luminaires. Lot <b>%s</b>." % (P.MAKER, L["lot"]), S["meta"]),
               _table(S, [["Customer", P.UTILITY], ["Purchase order", po],
                          ["Catalog number", P.CATALOG[L["watts"]]],
                          ["Driver output setting", "%d W" % L["watts"]], ["Quantity", "%d" % L["qty"]],
                          ["Serial numbers", "%s to %s" % (ser0, ser1)],
                          ["Date of shipment", L["ship"].strftime("%d %B %Y")]], [1.6, 4.6], head=False),
               Spacer(1, 8),
               Paragraph("Components fitted to every luminaire in this lot", S["h2"]),
               _table(S, rows, [2.4, 1.3, 1.9, 0.6]),
               Spacer(1, 6),
               Paragraph("Final test, three samples drawn from the lot", S["h2"]),
               _table(S, tests, [0.8, 1.1, 1.2, 0.9, 1.0], right=(1, 2, 3, 4)),
               Spacer(1, 8),
               Paragraph("LED driver rated life 100,000 hours at a case temperature of 75 &deg;C. The luminaires in "
                         "this lot conform to the purchase order and to ANSI C136.10, C136.37 and UL 1598. The "
                         "luminaire and its components are warranted for ten years from the date of shipment.",
                         S["body"]),
               Spacer(1, 10),
               Paragraph("Quality Assurance, %s, Plant 2." % P.MAKER, S["small"]),
               PageBreak()]
    doc.build(st[:-1], onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------ the tariff
def write_tariff(path):
    S = styles("Serif", TEAL)
    doc, fr = _doc(path, "Schedule SL, Street Lighting Service", P.UTILITY, "Tariff No. 7, Schedule SL",
                   "%s, Tariff No. 7" % P.UTILITY, "Schedule SL, effective 1 January 2026")
    rates = [["Luminaire", "Input watts", "Monthly rate per luminaire"],
             ["LED 40 W cobra-head", "%d" % P.INPUT_W[("LED", 40)], "$9.14"],
             ["LED 70 W cobra-head", "%d" % P.INPUT_W[("LED", 70)], "$11.02"],
             ["LED 110 W cobra-head", "%d" % P.INPUT_W[("LED", 110)], "$13.66"],
             ["HPS 70 W (closed to new service)", "%d" % P.INPUT_W[("HPS", 70)], "$10.48"],
             ["HPS 100 W (closed to new service)", "%d" % P.INPUT_W[("HPS", 100)], "$12.37"],
             ["HPS 150 W (closed to new service)", "%d" % P.INPUT_W[("HPS", 150)], "$15.11"],
             ["HPS 250 W flood (closed to new service)", "%d" % P.INPUT_W[("HPS", 250)], "$19.85"],
             ["MH 175 W shoebox (closed to new service)", "210", "$17.40"]]
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    abbr = ["Jan.", "Feb.", "Mar.", "Apr.", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
    burn = [["Month"] + abbr + ["Year"],
            ["Hours"] + ["%d" % h for h in P.BURN_H] + ["%s" % format(sum(P.BURN_H), ",")]]
    st = [Paragraph("Schedule SL: Street Lighting Service", S["h1"]),
          Paragraph("%s, Tariff No. 7. Effective with bills rendered on and after 1 January 2026." % P.UTILITY,
                    S["meta"]),
          Paragraph("1. Availability", S["h2"]),
          _clause(S, "1.1", "Available to municipalities for dusk-to-dawn lighting of public streets by Company-owned "
                            "luminaires on Company-owned or municipal poles. Sodium and metal halide luminaires are "
                            "closed to new service."),
          Paragraph("2. Monthly rates", S["h2"]),
          _clause(S, "2.1", "The monthly rate per luminaire covers energy, maintenance and the luminaire. Input "
                            "watts are the luminaire's input including its driver or ballast."),
          _table(S, rates, [3.0, 1.0, 1.9], right=(1, 2)),
          Paragraph("3. Energy accounting", S["h2"]),
          _clause(S, "3.1", "Energy for street lighting is accounted at each luminaire's input watts for the "
                            "dusk-to-dawn burning hours below, in proportion to the days of a month the luminaire "
                            "was in service. A luminaire is in service from the day it is energised to the day it is "
                            "removed, and an outage does not take it out of service."),
          _table(S, burn, [0.55] + [0.42] * 12 + [0.5], right=tuple(range(1, 14))),
          _clause(S, "3.2", "A luminaire on networked lighting controls is accounted at its dimmed input, its input "
                            "watts times the dimming level its control node records, for the dimmed hours the node "
                            "records in a month, and at its full input for its other burning hours."),
          Paragraph("4. Maintenance and repair", S["h2"]),
          _clause(S, "4.1", "The Company maintains its luminaires and replaces failed components at its cost."),
          _clause(S, "4.2", "The Company repairs an outage within 72 hours of the first report of it to the "
                            "Company. An outage found by Company patrol is repaired within 72 hours of being found."),
          Paragraph("5. Term", S["h2"]),
          _clause(S, "5.1", "Service is for an initial term of five years and continues month to month.")]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)
