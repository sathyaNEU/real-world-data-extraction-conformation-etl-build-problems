"""The utility's filed procedure: DRP-04, the Distribution Reliability Procedure (an extract)."""
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP
import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.2, leading=12.4,
                      alignment=TA_JUSTIFY, spaceAfter=4.5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, spaceAfter=3)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=9.8, spaceAfter=3,
                    spaceBefore=7)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.8, leading=10)
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.6)
CELLB = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=7.8, leading=9.6)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.5, 0.5, 0.5)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.91, 0.91, 0.89)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)])


def wrap(rows):
    return [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]


def build(path, t_med, n_sys):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    d = SimpleDocTemplate(path, pagesize=letter, title="DRP-04 Distribution Reliability Procedure", author="",
                          subject="", creator="", leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                          topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    rev = [["Rev", "Issued", "Change"],
           ["4", "9 January 2024", "Storm patrol added (section 6)."],
           ["5", "14 January 2025", "Major event day threshold for 2025; customers counted as service points."],
           ["6", "12 January 2026", "Major event day threshold and daily denominator for 2026; patrol assignment "
                                    "moved to Wednesday."]]
    f = [Paragraph("%s, %s" % (W.UTILITY, W.DIVISION), SMALL),
         Paragraph("DRP-04 Distribution Reliability Procedure", H1),
         Paragraph("Revision 6, issued 12 January 2026. Prepared by Kelsey Sanford, Distribution Reliability "
                   "Engineer; approved by Shawn Hartman, Superintendent, Electric Distribution. This extract carries "
                   "sections 1 to 6; sections 7 (reporting to the Utility Board) and 8 (retention) are not "
                   "reproduced.", SMALL),
         Paragraph("1 Scope", H2),
         Paragraph("1.1 This procedure applies to the 12.47 kV distribution feeders of the Bluffview, Cotter Road, "
                   "Millrace, North Yard and Sycamore substations. It sets how the division measures the reliability "
                   "of supply on each feeder and how the overhead line patrol crew and the storm patrol are "
                   "assigned.", BODY),
         Paragraph("2 Definitions", H2),
         Paragraph("2.1 A customer is a metered service point. The customers served by a feeder are the service "
                   "points it supplies on the last day of the reporting period.", BODY),
         Paragraph("2.2 An interruption is the loss of supply to one or more customers. A sustained interruption "
                   "lasts more than five minutes; a momentary interruption lasts five minutes or less. Planned "
                   "interruptions, taken for work on the system, are counted like any other.", BODY),
         Paragraph("2.3 A customer interruption is one customer losing supply in a sustained interruption.", BODY),
         Paragraph("2.4 Customer minutes of interruption are the minutes each interrupted customer was without "
                   "supply, summed over the customers.", BODY),
         Paragraph("2.5 A momentary interruption event is one or more momentary interruptions of a customer's "
                   "supply within five minutes of the first of them. Momentary interruptions of a customer that end "
                   "in a sustained interruption of that customer are part of the sustained interruption and are not "
                   "a momentary interruption event.", BODY),
         Paragraph("2.6 An interruption belongs to the local calendar day, Central time, on which it began.", BODY),
         Paragraph("2.7 An interruption's start and end are the times the outage management system records for it. "
                   "Interruptions the outage management system does not record, as with every momentary "
                   "interruption, take their times from the SCADA sequence-of-events log, and a recloser's momentary "
                   "interruptions from the recloser's own event log. A sustained interruption the outage management "
                   "system does not record runs, for the indices, from the opening that locked out its breaker or "
                   "recloser, as the outage management system times those it records; the trips and recloses before "
                   "that lockout are part of it under 2.5, not momentary interruption events, and do not move its "
                   "start.", BODY),
         Paragraph("3 Reliability indices", H2),
         Paragraph("3.1 For a reporting period, with major event days left out (section 4): SAIFI is the customer "
                   "interruptions divided by the customers served; SAIDI is the customer minutes of interruption "
                   "divided by the customers served; MAIFI<sub>E</sub> is the customers' momentary interruption "
                   "events, summed over the customers, divided by the customers served; and CEMI-n is reported as "
                   "the number of customers served who had more than n sustained interruptions in the period.", BODY),
         Paragraph("3.2 A feeder's customer interruptions, customer minutes and momentary interruption events are "
                   "those of the interruptions on the feeder as it stood when each began. Its customers served, and "
                   "the customers counted in its CEMI-n, are the service points it supplies on the last day of the "
                   "period, each with every sustained interruption that customer had in the period.", BODY),
         Paragraph("4 Major event days", H2),
         Paragraph("4.1 Major event days are identified by the 2.5 beta method of IEEE Std 1366. The threshold for "
                   "the 2026 reporting year, T<sub>MED</sub>, is %.2f minutes of daily system SAIDI, computed from "
                   "the daily SAIDI values of 2021 to 2025." % t_med, BODY),
         Paragraph("4.2 Daily system SAIDI for a 2026 day is the customer minutes of the interruptions that began "
                   "on that day, across the system, divided by %s, the customers served by the system on 31 "
                   "December 2025. A day whose daily system SAIDI exceeds T<sub>MED</sub> is a major event day, and "
                   "every interruption that began on a major event day is left out of the indices." %
                   format(n_sys, ","), BODY),
         Paragraph("5 Overhead line patrol", H2),
         Paragraph("5.1 The overhead line patrol crew works one feeder a week. The distribution reliability "
                   "engineer assigns it each Wednesday for the week that follows.", BODY),
         Paragraph("5.2 The patrol goes to the feeder where a component on the overhead line is breaking down, so "
                   "that it is found and replaced before it fails outright. When no feeder has one, the crew is "
                   "released to the construction section for the week.", BODY),
         Paragraph("5.3 Storm damage, animal contacts and contacts with trees are not the patrol's work: they are "
                   "the storm patrol's, the animal guard programme's and the line clearance programme's.", BODY),
         Paragraph("5.4 The assignment names the feeder and the stretch of it to walk, given as the zone of a "
                   "breaker, recloser or fuse: the line from it to the next breakers, reclosers or fuses beyond it, "
                   "with the taps fused off that line.", BODY),
         Paragraph("6 Storm patrol", H2),
         Paragraph("6.1 On the day after a storm day the storm patrol inspects the feeders of the substations the "
                   "storm touched. A storm day for a substation is a local calendar day on which the lightning "
                   "detection network logged a cloud-to-ground stroke within five miles of the substation, or on "
                   "which the airport weather station reported a gust of 40 mph or more.", BODY),
         Spacer(1, 6),
         Table(wrap(rev), colWidths=[0.45 * inch, 1.25 * inch, 4.9 * inch], style=TBL, hAlign="LEFT")]
    d.build(f)
    PP.normalize_pdf(path, b"D:20260112091406-06'00'", b"D:20260112091406-06'00'")
    return path
