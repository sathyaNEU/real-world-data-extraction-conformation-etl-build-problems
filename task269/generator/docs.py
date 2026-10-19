"""The pack's documents: Pellbrook Metro's Bus Service Reliability Standard (version 4), the 2027 headway management
programme guidelines, the 2026 headway supervision pilot plan, the August 2026 service performance report and the
pack's contents list."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402
import world as W    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1c2428"), colors.HexColor("#5a646b"), colors.HexColor("#b4bdc3")
TEAL = colors.HexColor("#0f5c6e")
NAVY = colors.HexColor("#22395a")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=10, leading=13.8, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.8, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.6, leading=11.6, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.4, leading=10.6, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.4, leading=10.6, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.6)
        canvas.drawString(19 * mm, A4[1] - 11.5 * mm, left)
        canvas.drawRightString(A4[0] - 19 * mm, A4[1] - 11.5 * mm, right)
        canvas.drawRightString(A4[0] - 19 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


# ---------------------------------------------------------------------------------------------- the standard
def write_standard(path):
    S = styles("Serif", NAVY)
    doc = _doc(path, "Bus Service Reliability Standard", K.AGENCY)
    s = [Paragraph("Bus Service Reliability Standard", S["h1"]),
         Paragraph("%s, Network Performance. Version 4, approved by the Public Transport Committee of %s on "
                   "3 March 2025. Replaces version 3 (2022)." % (K.AGENCY, K.COUNCIL), S["meta"]),
         Paragraph("1. Purpose", S["h2"]),
         Paragraph("This standard sets how %s, %s's public transport business, measures the reliability of its "
                   "bus services as passengers meet them. It applies to every route the operator runs for the council "
                   "under the bus services contract." % (K.AGENCY, K.COUNCIL), S["body"]),
         Paragraph("2. Terms", S["h2"]),
         _clause(S, "2.1", "A <i>timing point</i> is a stop the timetable times buses at. Every other stop's times in "
                           "the timetable are spread between its timing points."),
         _clause(S, "2.2", "A <i>frequent route</i> is one of the routes Network Planning lists on the frequent "
                           "network; its <i>frequent corridor</i> is the run of its stops listed there for each "
                           "direction."),
         _clause(S, "2.3", "The <i>weekday peaks</i> are 7:00 am to 9:00 am and 3:30 pm to 6:00 pm, each from its "
                           "start up to but not including its end, local time."),
         _clause(S, "2.4", "A <i>boarding</i> is a tag-on the ticketing system records. A journey without a tag-off "
                           "is a boarding like any other; the ticketing system charges it the default fare."),
         _clause(S, "2.5", "The <i>census fortnight</i> is the fortnight the headway management programme's "
                           "guidelines name for the year."),
         Paragraph("3. Excess wait on frequent routes", S["h2"]),
         _clause(S, "3.1", "Excess wait is the extra time passengers spend waiting at the stop beyond what the "
                           "timetable in force would have them wait. Passengers on frequent routes are taken to "
                           "arrive at random, evenly through each peak."),
         _clause(S, "3.2", "Excess wait is measured at timing points. A boarding's excess wait is worked at the last "
                           "timing point at or before its stop in its direction of travel, for the peak and the "
                           "census day it boarded in, from the location vendor's revised departures and the "
                           "timetable in force that day, taking only headways that begin and end inside the peak. "
                           "A departure is the time a bus left the timing point; where a bus reopened its doors and "
                           "left twice, the later time."),
         _clause(S, "3.3", "A route's excess wait is the average over its boardings at stops on its frequent "
                           "corridor in the weekday peaks of the census fortnight, in minutes per boarding."),
         Paragraph("4. On-time running", S["h2"]),
         _clause(S, "4.1", "A departure from a timing point, other than a trip's last stop, is on time when it "
                           "leaves no more than 59 seconds early and no more than 5 minutes 59 seconds late against "
                           "the timetable in force."),
         _clause(S, "4.2", "On-time running is the share of departures on time. Network Performance reports it each "
                           "month for every route in the service performance report."),
         Paragraph("5. Data", S["h2"]),
         _clause(S, "5.1", "The location vendor releases each fortnight's departures about a week after it ends, and "
                           "a revised release once it has re-run the position reports it could not match to a trip "
                           "the first time. The revised release governs."),
         _clause(S, "5.2", "Boardings come from the ticketing system's journey extract. Times in both are local "
                           "(Australian Eastern Standard Time)."),
         Spacer(1, 8),
         Paragraph("Network Performance keeps this standard. Questions to networkperformance@pellbrookmetro.example.",
                   S["meta"])]
    doc.build(s, onFirstPage=_frame(K.AGENCY, "Bus Service Reliability Standard v4", "Serif"),
              onLaterPages=_frame(K.AGENCY, "Bus Service Reliability Standard v4", "Serif"))


# ---------------------------------------------------------------------------------------------- the guidelines
def write_guidelines(path):
    S = styles("Sans", TEAL)
    doc = _doc(path, "Headway management programme: guidelines for 2027", K.PEOPLE["manager"])
    rows = [["Route", "Frequent corridor", "Branches beyond the corridor"]]
    for rt in K.ROUTES:
        N = W.NET[rt]
        br = ", ".join(B["name"] for B in N["branches"].values()) if "branches" in N else "none (the whole route)"
        rows.append([rt, "%s, City Interchange to %s" % (N["road"], N["tps"][-1]), br])
    s = [Paragraph("Headway management programme: guidelines for 2027", S["h1"]),
         Paragraph("Mary Patton, Manager, Network Performance, %s. Issued 7 September 2026." % K.AGENCY, S["meta"]),
         Paragraph("1. The programme", S["h2"]),
         Paragraph("Supervisors posted at timing points in the weekday peaks keep buses on a frequent route evenly "
                   "spaced: they hold a bus that is catching the one ahead and send on one that has fallen behind. "
                   "%s provides the supervisor teams under the bus services contract; a team covers one route's "
                   "frequent corridor in both weekday peaks." % K.OPERATOR, S["body"]),
         Paragraph("2. Choosing the routes", S["h2"]),
         _clause(S, "2.1", "The programme serves the eight frequent routes on their frequent corridors, as Network "
                           "Planning lists them:"),
         _table(S, rows, [16, 92, 64]),
         Spacer(1, 6),
         _clause(S, "2.2", "Routes are chosen each year on the census fortnight, the first two full weeks of August. "
                           "For 2027 it is Monday 10 to Friday 21 August 2026."),
         _clause(S, "2.3", "The year's teams go to the routes whose excess wait per boarding on the frequent "
                           "corridor in the census fortnight is highest, measured under the Bus Service Reliability "
                           "Standard (section 3). The 2027 budget funds four teams."),
         Paragraph("3. Teams", S["h2"]),
         Paragraph("A team posts supervisors at the timing points of its route's corridor that the operator and "
                   "Network Performance agree for the route, and works with the control room on the day. Teams do not "
                   "change the timetable.", S["body"]),
         Paragraph("4. Timeline", S["h2"]),
         Paragraph("The routes go to the council's Public Transport Committee for approval at its meeting on "
                   "Tuesday 10 November 2026. The approved routes go into the contract variation with %s, priced "
                   "against the 2026 headway supervision pilot's record, and the teams start with the school year on "
                   "Monday 1 February 2027." % K.OPERATOR, S["body"])]
    doc.build(s, onFirstPage=_frame(K.AGENCY + ", Network Performance", "Headway management programme 2027", "Sans"),
              onLaterPages=_frame(K.AGENCY + ", Network Performance", "Headway management programme 2027", "Sans"))


# ---------------------------------------------------------------------------------------------- the pilot plan
def write_pilot_plan(path):
    S = styles("Sans", TEAL)
    doc = _doc(path, "Headway supervision pilot 2026: plan", K.PEOPLE["operator"])
    starts = {}
    for d0, rts in K.WAVES.items():
        for rt in rts:
            starts[rt] = d0
    rows = [["Route", "Post code (payroll)", "Post location (route and timing point)", "Starts"]]
    for rt in K.ROUTES:
        code, loc = W.POSTS[rt]
        rows.append([rt, code, "Route %s, %s" % (rt, loc), starts[rt].strftime("%A %d %B").replace(" 0", " ")])
    fee = [["Month", "Coordination fee"]] + [[dt.date(2026, m, 1).strftime("%B"), "$%s" % format(v, ",.2f")]
                                              for m, v in K.FEE.items()]
    s = [Paragraph("Headway supervision pilot 2026: plan", S["h1"]),
         Paragraph("Agreed between %s (Jason Neal, Operations Manager) and %s Network Performance (Mary Patton). "
                   "Final, 22 January 2026." % (K.OPERATOR, K.AGENCY), S["meta"]),
         Paragraph("What the pilot does", S["h2"]),
         Paragraph("One supervisor post on each frequent route, at the timing point below, staffed for the morning "
                   "peak (6:45 to 9:15 am) and the afternoon peak (3:15 to 6:15 pm) on weekdays from the route's "
                   "start to Friday 26 June 2026. Public holidays are off (Good Friday, Easter Monday and the King's "
                   "Birthday). Routes start in three waves so the operator can train relief supervisors as it goes.",
                   S["body"]),
         _table(S, rows, [14, 34, 86, 38]),
         Spacer(1, 6),
         Paragraph("Shifts", S["h2"]),
         Paragraph("A shift is one supervisor's time at a post in one peak. When a supervisor is relieved part way "
                   "through a peak, each supervisor's part is a shift. A peak the operator cannot cover is "
                   "recorded as cancelled. Depot supervisors' shifts are not part of the pilot.", S["body"]),
         Paragraph("Charges", S["h2"]),
         Paragraph("The operator charges $%s for each post on each pilot weekday (both peaks, whether or not a shift "
                   "was cancelled), invoiced monthly in arrears to the route's Network Performance cost centre. It "
                   "also charges a monthly coordination fee for the pilot, invoiced to the central cost centre:"
                   % format(K.POST_DAY, ",.2f"), S["body"]),
         _table(S, fee, [40, 40], right=(1,)),
         Spacer(1, 6),
         Paragraph("For reporting by route, each month's coordination fee is shared among the routes in proportion "
                   "to the shifts worked on each that month. The pilot's accounts close with the June invoices.",
                   S["body"])]
    doc.build(s, onFirstPage=_frame(K.OPERATOR + " and " + K.AGENCY, "Headway supervision pilot 2026", "Sans"),
              onLaterPages=_frame(K.OPERATOR + " and " + K.AGENCY, "Headway supervision pilot 2026", "Sans"))


# ---------------------------------------------------------------------------------------------- the monthly report
def write_report(path, otp, patronage, delivered):
    S = styles("Sans", NAVY)
    doc = _doc(path, "Service performance report, August 2026", K.AGENCY)
    rows = [["Route", "On-time running", "Weekday boardings (average)", "Trips delivered"]]
    for rt in K.ROUTES:
        rows.append([rt, "%.1f%%" % otp[rt], format(patronage[rt], ","), "%.1f%%" % delivered[rt]])
    s = [Paragraph("Service performance report: August 2026", S["h1"]),
         Paragraph("%s, Network Performance. Published 11 September 2026. Frequent routes." % K.AGENCY, S["meta"]),
         Paragraph("On-time running is measured under section 4 of the Bus Service Reliability Standard on the "
                   "location vendor's first release for the month; weekday boardings are tag-ons on the month's "
                   "weekdays, all day; trips delivered are the timetabled trips the operator ran.", S["body"]),
         _table(S, rows, [18, 40, 56, 40], right=(1, 2, 3)),
         Spacer(1, 8),
         Paragraph("The 17 August timetable added running time on the frequent corridors in the peaks. On-time "
                   "running on the frequent network rose in the second half of the month on most routes.", S["body"]),
         Paragraph("Next report: September 2026, published in October.", S["meta"])]
    doc.build(s, onFirstPage=_frame(K.AGENCY, "Service performance report", "Sans"),
              onLaterPages=_frame(K.AGENCY, "Service performance report", "Sans"))


def write_contents(path, rows):
    lines = ["Census 2026 working pack: headway management programme 2027",
             "Network Performance, %s. Assembled 2 October 2026." % K.AGENCY, ""]
    for name, desc in rows:
        lines.append(name)
        lines.append("    " + desc)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")
