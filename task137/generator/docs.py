"""The two documents: the driver handbook (its lighting section and Appendix C, the depots' sunrise and sunset) and the
board's claims fund terms for 2027 (the governing document)."""
import datetime as dt

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import astro as A
import common as CM
import params as P

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.6, spaceAfter=4)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=15, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
LI = ParagraphStyle("li", parent=BODY, leftIndent=12, bulletIndent=2)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                             bottomMargin=16 * mm, title=title, author=author, creator="Microsoft Word",
                             producer="Microsoft Word for Microsoft 365", subject="", keywords="")


def _hm(m):
    return "%02d:%02d" % (m // 60, m % 60)


def sun_table_rows():
    """Appendix C as printed: one row per seven-day block, sunrise and sunset in GMT at each depot."""
    rows = []
    for k, a, b in A.ROWS:
        lab = ("%d %s" % (a.day, a.strftime("%b"))) if a == b else ("%d %s to %d %s" % (a.day, a.strftime("%b"), b.day,
                                                                                       b.strftime("%b")))
        r = [lab]
        for code, *_ in P.DEPOTS:
            rise, sett = A.TABLE[(code, k)]
            r += [_hm(rise), _hm(sett)]
        rows.append(r)
    return rows


def handbook(path):
    when = dt.datetime(2026, 3, 9, 10, 20)
    S = [Paragraph("%s<br/>Driver handbook" % P.COMPANY, H1),
         Paragraph("2026 edition. Issued by %s, Transport Director, for every driver at Cramlington, Team Valley, Carlisle "
                   "and Darlington. Keep it in the cab with the vehicle's claims card." % P.PEOPLE["transport_director"],
                   SMALL),
         Paragraph("1. Before you drive", H2),
         Paragraph("Do the walkround check on the vehicle you are taking out before the first drop and record it on the "
                   "Gridtrak tablet: lights and indicators, tyres and wheel nuts, mirrors and cameras, the tail-lift and "
                   "its warning lights, load security and the fridge unit. A defect that makes the vehicle unroadworthy "
                   "means it does not leave the yard; tell the shift manager, who will give you the depot's spare.", BODY),
         Paragraph("2. Hours", H2),
         Paragraph("Our 7.5-tonne trucks are in scope of the EU and AETR rules as retained in Great Britain: no more than "
                   "4 hours 30 minutes driving without a 45-minute break, 9 hours driving a day (10 hours twice a week) "
                   "and the daily and weekly rests the tachograph records. Store routes are planned within these limits; "
                   "if a delay puts a break at risk, phone the depot rather than pressing on.", BODY),
         Paragraph("3. Lights", H2),
         Paragraph("Use dipped headlights from sunset to sunrise and whenever visibility is seriously reduced, and use "
                   "sidelights with them, as the Highway Code requires. Keep the lights, reflectors and number plate "
                   "clean. Appendix C gives sunrise and sunset at each depot through the year.", BODY),
         Paragraph("4. If you are involved in a collision", H2)]
    for t in ["Stop as soon as it is safe, switch on the hazard lights and put on your high-visibility vest. If anyone is "
              "hurt, call 999 first.",
              "Exchange names, addresses and registration numbers with anyone involved and take the other driver's "
              "insurer if you can. Do not admit fault or discuss blame.",
              "Take photographs on the tablet of the scene, both vehicles and any damage, and note the time.",
              "Phone %s's 24-hour claims line on the number on the claims card before the end of your shift. The "
              "claims handler records the date and time of the incident as you give them, and gives you a claim number "
              "to pass to the depot." % P.INSURER,
              "Tell your shift manager before you go home. If the truck needs repair, the workshop books it into %s, "
              "whose engineer inspects it under the claim number." % P.BODYSHOP]:
        S.append(Paragraph(t, LI, bulletText="•"))
    S += [Paragraph("5. Reversing and store yards", H2),
          Paragraph("Use the reversing camera and, where a store has one, the banksman. Never reverse into a store yard or "
                    "service road without checking it on foot first if you cannot see the whole of it.", BODY),
          PageBreak(),
          Paragraph("Appendix C. Sunrise and sunset at our depots", H2),
          Paragraph("Times are Greenwich Mean Time (GMT), for the middle day of each block. While British Summer Time is in "
                    "force, from 01:00 GMT on the last Sunday in March to 01:00 GMT on the last Sunday in October, add one "
                    "hour to read them on the clock. The times move by no more than a minute or two from one year to the "
                    "next; 29 February goes with the block for 28 February.", SMALL),
          Spacer(1, 3)]
    head = [["", "Cramlington", "", "Team Valley", "", "Carlisle", "", "Darlington", ""],
            ["Dates", "Sunrise", "Sunset", "Sunrise", "Sunset", "Sunrise", "Sunset", "Sunrise", "Sunset"]]
    t = Table(head + sun_table_rows(), colWidths=[34 * mm] + [17 * mm] * 8, repeatRows=2)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 7.4), ("FONT", (0, 0), (-1, 1), "Helvetica-Bold", 7.4),
                           ("SPAN", (1, 0), (2, 0)), ("SPAN", (3, 0), (4, 0)), ("SPAN", (5, 0), (6, 0)),
                           ("SPAN", (7, 0), (8, 0)), ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                           ("LINEBELOW", (0, 1), (-1, 1), 0.6, colors.black),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6), ("TOPPADDING", (0, 0), (-1, -1), 0.6),
                           ("ROWBACKGROUNDS", (0, 2), (-1, -1), [colors.white, colors.HexColor("#F2F2F2")])]))
    S.append(t)
    _doc(path, "Driver handbook 2026", P.PEOPLE["transport_director"]).build(S)
    CM.clean_pdf(path, when)


def terms(path):
    when = dt.datetime(2026, 10, 15, 9, 5)
    S = [Paragraph("%s<br/>Motor claims fund: terms for the 2027 fund year" % P.COMPANY, H1),
         Paragraph("Approved by the board of directors on 14 October 2026. Prepared by %s, Risk and Insurance Manager, "
                   "with %s, Finance Director." % (P.PEOPLE["risk_manager"], P.PEOPLE["finance_director"]), SMALL),
         Paragraph("1. Purpose", H2),
         Paragraph("%s carries the cost of repairing its own delivery trucks itself and insures its liability to third "
                   "parties with %s under motor fleet policy MF22190046. The board sets the motor claims fund for each "
                   "fund year from the number of claims the delivery trucks are expected to make in that year and what "
                   "those claims cost. The Risk and Insurance Manager prepares the estimate each October and the Finance "
                   "Director reviews it before it goes to the board." % (P.COMPANY, P.INSURER), BODY),
         Paragraph("2. Claims", H2),
         Paragraph("A claim is a collision involving one of the delivery trucks on the fleet register, whether a route "
                   "truck or a depot spare, that is notified to %s under the policy. A notification closed as a duplicate "
                   "of another notification, or withdrawn, is not a claim. The company cars are insured under the same "
                   "policy but are outside the fund." % P.INSURER, BODY),
         Paragraph("3. Fund year and quarters", H2),
         Paragraph("A claim belongs to the fund year and to the quarter in which the collision happened, by its incident "
                   "date in UK clock time, whenever it is notified. The 2027 fund year runs from 1 January to 31 December "
                   "2027, in calendar quarters.", BODY),
         Paragraph("4. The 2027 route schedule", H2),
         Paragraph("From 2 January 2027 every store route runs to the 2027 route schedule approved by the board with these "
                   "terms, on the delivery days of its 2027 calendar. The 2027 fund is set for that schedule.", BODY),
         Paragraph("5. Repair costs and recoveries", H2),
         Paragraph("All amounts are net of VAT, which the company recovers. The repair cost of a collision is what %s "
                   "invoices the company for repairing the truck, or for inspecting and storing it when it is a total "
                   "loss. Money another party's insurer pays towards the repair of a collision is credited to the quarter "
                   "of that collision." % P.BODYSHOP, BODY),
         Paragraph("6. Review", H2),
         Paragraph("The Finance Director reviews the fund against the claims listing at each quarter end and reports to the "
                   "board in the following month.", BODY)]
    _doc(path, "Motor claims fund terms 2027", P.PEOPLE["risk_manager"]).build(S)
    CM.clean_pdf(path, when)
