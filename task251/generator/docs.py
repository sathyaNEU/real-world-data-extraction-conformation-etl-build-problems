"""task251 documents: the region's counting standard TDP-03 (pdf), the maintenance contractor's mail fixing the spring
round (eml)."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.8, leading=13.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17,
                        spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.6, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.6)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 11 * mm, text)
        canvas.drawRightString(letter[0] - 20 * mm, 11 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.4):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.2)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def standard(path, F):
    body, h1, h2, small = _styles()
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=20 * mm, title="TDP-03 Permanent count stations", author=P.ORG,
                            creator=P.ORG, subject="Traffic Data Program Standard TDP-03, revision 4", invariant=1)
    s = [Paragraph(P.ORG + ", " + P.DEPT, small), Spacer(1, 2 * mm),
         Paragraph("Traffic Data Program Standard TDP-03: Permanent count stations", h1),
         Paragraph("Revision 4, issued 15 January 2026 by the Traffic Data Program; approved by the Director, "
                   "Transportation Services. Supersedes revision 3 (2022).", small),
         Paragraph("1. Purpose and scope", h2),
         Paragraph("This standard governs the Region's permanent count stations on Regional Roads: the hourly record "
                   "each station keeps, the summer validation programme, the accuracy a station's count for a year must "
                   "meet, and the annual count report the Region publishes and files with the Province.", body),
         Paragraph("2. Stations", h2),
         Paragraph("A permanent count station has an inductive loop in every lane in both directions, wired to a "
                   "roadside controller. The loops are cut to the Region's standard detail at every station, one 2.0 m "
                   "square loop of three turns in the centre of the lane to drawing TDP-07; the controller is a TCX-2 "
                   "or a TCX-4. The controller counts each vehicle that crosses a loop and measures the share "
                   "of time the loops are occupied. Stations are numbered by Regional Road; the station register gives "
                   "each station's road, kilometre point, location, district, lanes and controller. When a controller "
                   "is replaced the station keeps its loops and may be given a new number; the register records the "
                   "change and the date.",
                   body),
         Paragraph("3. The hourly record", h2),
         Paragraph("Each controller reports to %s, the Region's count management system, which keeps for each station "
                   "and direction the vehicles counted in every hour and the hour's occupancy, all lanes of the "
                   "direction together, under the station number in force for the hour. Occupancy is the share of the "
                   "hour the loops were occupied, in per cent, at the precision the controller reports it. Hours are "
                   "kept in local time and the export carries each hour's offset from "
                   "UTC. Under a station's new number the record continues from the date of the change." % P.SYSTEM,
                   body),
         Paragraph("A controller that is not counting reports nothing for the hour, and a part hour is discarded. A "
                   "TCX-2 has no standby supply: when its supply is interrupted it stops, discards the hour it is in "
                   "and reports no event of its own, so an interruption at a TCX-2 station shows only as hours absent "
                   "from the export. A TCX-4 carries a battery and counts through a short interruption on it.", body),
         Paragraph("4. Summer validation programme", h2),
         Paragraph("Every July and August the validation contractor films each station for 24 hours on a weekday "
                   "and counts every vehicle that passes in each direction, in 15-minute intervals from midnight to "
                   "midnight. For the same intervals the contractor records the loops' count with a pulse recorder "
                   "connected to the station's detector outputs in the cabinet. The contractor's counts and the loops' "
                   "counts are kept together in the contractor's workbook under its own site codes; the station "
                   "register gives each station's site code.", body),
         Paragraph("5. Accuracy of a station's count", h2),
         Paragraph("A station's count for a calendar year meets this standard when the vehicles it counted in the "
                   "hours of the year it counted, both directions and every lane together, are within 5 per cent, "
                   "either way, of the vehicles that passed it in those hours. The station's count error for the year "
                   "is the vehicles it counted divided by the vehicles that passed it in the same hours, less one, "
                   "expressed in per cent.", body),
         Paragraph("A station whose count does not meet the standard is flagged in the annual count report and is "
                   "recalibrated in the following spring's round by the maintenance contractor. The Traffic Data "
                   "Program sends the contractor the list of stations before the round.", body),
         Paragraph("6. Annual count report", h2),
         Paragraph("By 31 March the Region publishes the annual count report for the previous year, with each "
                   "station's annual average daily traffic and its flag and the maintenance figures of section 7, and "
                   "files it with the Ministry's municipal traffic data exchange.", body),
         Paragraph("7. Maintenance of the stations", h2),
         Paragraph("%s polls every station every fifteen minutes. It raises COMMS_LOST when a poll goes unanswered "
                   "and COMMS_OK at the first poll answered after it, and sets a controller's clock (CLOCK_SET) when "
                   "it finds it unset. A controller reports MAINS_FAIL and MAINS_OK when its supply is lost and "
                   "restored, RESET when it is reset, COLD_START when it starts without a set clock, and logs the "
                   "cabinet door switch (DOOR_OPEN, DOOR_CLOSE) on every opening and closing of the cabinet. The "
                   "station event log keeps what each controller reported and what %s raised itself, by the clock of "
                   "whichever raised it, in the order %s received them." % (P.SYSTEM, P.SYSTEM, P.SYSTEM), body),
         Paragraph("The maintenance contractor inspects every station each spring and autumn, attends faults, and "
                   "books its work against work orders. A maintenance visit is a day one of the maintenance "
                   "contractor's technicians is at a station; two technicians at one station on one day are one "
                   "visit, and work the contractor carries out from its own premises is not a visit. A power failure "
                   "is a loss of mains power at a station's controller, counted once however "
                   "long it lasts; a supply restored and lost again is a second failure. The annual count report "
                   "gives, for each district and calendar quarter, the "
                   "maintenance visits to the stations and the power failures the stations had.", body),
         Spacer(1, 4 * mm),
         _table([["Revision", "Date", "Change"],
                 ["1", "12 June 2014", "First issue"],
                 ["2", "3 March 2018", "Summer validation programme by contract"],
                 ["3", "21 April 2022", "%s replaces the previous count system" % P.SYSTEM],
                 ["4", "15 January 2026", "Accuracy stated for the calendar year; annual report filed with the "
                                          "Ministry; maintenance figures by district and quarter"]], [22, 32, 110])]
    doc.build(s, onFirstPage=_footer("TDP-03 rev. 4"), onLaterPages=_footer("TDP-03 rev. 4"))


def mail(path, F):
    sent = dt.datetime(2028, 2, 14, 9, 42)
    text = ("From: %(m)s <ylarson@carrick-signal.ca>\r\n"
            "To: %(c)s <miranda.harris@halbrookregion.ca>\r\n"
            "Subject: Spring recalibration round 2028, station list\r\n"
            "Date: Mon, 14 Feb 2028 09:42:00 -0500\r\n"
            "MIME-Version: 1.0\r\n"
            "Content-Type: text/plain; charset=utf-8\r\n"
            "Content-Transfer-Encoding: 8bit\r\n\r\n"
            "Hi Miranda,\r\n\r\n"
            "We are booking crews for the spring recalibration round, which starts the week of 10 April as in our "
            "schedule. Could you send me the list of count stations you want recalibrated by Friday 3 March? If "
            "there are none this year, a short note saying so is fine.\r\n\r\n"
            "Thanks,\r\n%(m)s\r\nService Manager, %(org)s\r\n") % dict(m=P.PEOPLE["maintenance"],
                                                                       c=P.PEOPLE["coordinator"],
                                                                       org=P.CONTRACTOR_MAINT)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return sent
