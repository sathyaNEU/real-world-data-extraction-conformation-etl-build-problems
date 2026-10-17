"""The platform's own capacity framework, quality standard, dictionary and bulletin."""
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Times-Roman", fontSize=9.5, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Times-Bold", fontSize=13, spaceAfter=8)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Times-Bold", fontSize=10.5, spaceAfter=4,
                    spaceBefore=8)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10.5)
CELL = ParagraphStyle("c", fontName="Times-Roman", fontSize=8, leading=10)
CELLB = ParagraphStyle("cb", fontName="Times-Bold", fontSize=8, leading=10)
TBL = TableStyle([("GRID", (0, 0), (-1, -1), 0.3, colors.Color(0.45, 0.45, 0.45)),
                  ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.90, 0.90, 0.88)),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                  ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)])


def wrap(rows):
    return [[Paragraph(str(c), CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(rows)]


def _doc(path, title):
    return SimpleDocTemplate(path, pagesize=A4, title=title, author="", subject="", creator="",
                             leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm)




def framework(target):
    path = os.path.join(target, "network_capacity_framework.pdf")
    d = _doc(path, "Network capacity framework")
    f = [Paragraph("%s: network capacity framework" % W.PLATFORM, H1),
         Paragraph("Issue 6, approved by the board, 14 October 2026. Parts 1, 2, 3 and 6 and the "
                   "annexes are not reproduced in this extract.", SMALL),
         Paragraph("Part 4 Interconnect capacity", H2),
         Paragraph("4.1 The capacity committee decides each quarter whether to fund an "
                   "interconnect augment. The decision is taken on the reporting quarter that has "
                   "closed, and the reporting quarters are the calendar quarters.", BODY),
         Paragraph("4.2 An augment is funded on an interconnect whose evening shortfall is larger "
                   "than the shortfall the network's own record shows the measurement produces "
                   "without congestion. The shortfall of an interconnect in an evening window is the "
                   "figure the delivered quality standard defines, and the figure the decision is "
                   "taken on is the largest any interconnect in service at the quarter end shows in "
                   "any evening window of the quarter.", BODY),
         Paragraph("4.3 The evening windows the planning desk reports on are 19:00 to 19:59, 20:00 "
                   "to 20:59 and 21:00 to 21:59, each in local time, and an evening is the local "
                   "calendar date its windows begin on.", BODY),
         Paragraph("4.4 An evening on which the network operations team had booked work inside an "
                   "evening window on that interconnect is not evidence of congestion there, and the "
                   "planning desk leaves those evenings out.", BODY),
         Paragraph("4.5 One augment is funded in a quarter, or none.", BODY),
         Paragraph("Part 5 Incidents", H2),
         Paragraph("5.1 The service restoration standard is four hours from the time an incident was "
                   "opened to the time service was restored. The time service was restored is the "
                   "time the duty engineer records, which is not the time the ticket was closed, and "
                   "an incident for which no restoration time was recorded is not counted as "
                   "restored inside the standard.", BODY),
         Paragraph("5.2 Every incident carries a recorded cause, and the dictionary says which "
                   "causes sit outside the platform.", BODY),
         Paragraph("Part 7 Peering commitments", H2),
         Paragraph("7.1 A peering or transit agreement is billed on the ninety-fifth percentile of "
                   "the quarter's five-minute samples of the traffic the platform sends the peer, "
                   "which is the 1,296th highest sample of the quarter, taken over the peer's "
                   "traffic and not over one port of it.", BODY),
         Paragraph("7.2 The commitment a peer is billed on is the commitment the platform and the "
                   "peer have both accepted and that is in force on the last day of the quarter, "
                   "and an amendment the peer has not accepted is not billed on. Where the "
                   "quarter's percentile is above the commitment, the overage "
                   "is the excess in whole megabits a second, after the percentile is taken to the "
                   "nearest whole megabit, at the agreement's own rate. A peer the "
                   "platform exchanges traffic with settlement free is billed nothing and carries "
                   "no commitment.", BODY)]
    d.build(f)
    return path


def standard(target):
    path = os.path.join(target, "delivered_quality_standard.pdf")
    d = _doc(path, "Delivered quality standard")
    f = [Paragraph("%s: delivered quality standard" % W.PLATFORM, H1),
         Paragraph("Streaming quality engineering, issue 11. How the client telemetry is reduced to "
                   "the figures the planning desk and the bulletin use.", SMALL),
         Paragraph("The minute value", H2),
         Paragraph("The client reports the bitrate it was delivered for each session. The minute "
                   "value for an interconnect is the median of those bitrates across the sessions "
                   "the interconnect carried in that minute, in kilobits a second, and it is the "
                   "only value the standard reduces further.", BODY),
         Paragraph("A band median", H2),
         Paragraph("The median of a band is the median of the band's minute values. The reference "
                   "band is 12:00 to 14:59 local time, which the platform uses because demand there "
                   "is a fraction of the evening's on every interconnect.", BODY),
         Paragraph("The shortfall", H2),
         Paragraph("The shortfall of an interconnect in an evening window is the median of the "
                   "reference band for that interconnect on that date, less the median of the "
                   "evening window, in kilobits a second. A positive shortfall is bitrate the "
                   "evening did not deliver and the reference band did.", BODY),
         Paragraph("What the standard does not define", H2),
         Paragraph("The standard reduces telemetry. It does not say what a shortfall is to be "
                   "compared against, which is the planning desk's own work under the capacity "
                   "framework.", BODY)]
    d.build(f)
    return path


def dictionary(target):
    path = os.path.join(target, "telemetry_dictionary.pdf")
    d = _doc(path, "Telemetry dictionary")
    rows = [["Field", "Meaning"],
            ["measured_at_utc", "the minute the client telemetry is stamped with, in UTC. The "
                                "framework's windows are local time, and the Netherlands moves to "
                                "summer time on the last Sunday in March"],
            ["port_code", "the interconnect port as the record carried it when it was written; the "
                          "interconnect register carries the port it now is"],
            ["sessions", "the sessions the port carried in the minute"],
            ["median_kbps, p10_kbps", "the minute value the delivered quality standard defines, and "
                                      "the tenth percentile of the same bitrates"],
            ["rebuffer_events", "the rebuffers the clients on that port reported in the minute"],
            ["evening_date_local, window_from", "the daily rollup's own evening and window, already "
                                                "in local time"],
            ["evening_median_kbps, reference_median_kbps", "the two band medians the daily rollup "
                                                           "keeps; the pipeline keeps minute rows "
                                                           "for ninety days and these for two years"],
            ["minutes_scheduled, minutes_captured", "what the collector was due to record and what "
                                                    "it did record"],
            ["out_mbps, in_mbps", "the edge's five-minute traffic samples, in megabits a second"],
            ["build_version, build_ref", "the client version string the session reports, and the "
                                         "build the release log identifies by its own reference and "
                                         "its rollout dates"],
            ["cause_category", "the recorded cause of an incident. Access network, transit provider, "
                               "customer premises, and power or facility sit outside the platform. "
                               "Origin service, packager, edge cache, client application and "
                               "configuration change sit inside it"],
            ["service_restored_at_utc", "the time the duty engineer recorded service as restored, "
                                        "which only some incidents carry"]]
    f = [Paragraph("%s: telemetry and operations dictionary" % W.PLATFORM, H1),
         Paragraph("The fields of the extracts the data platform hands over.", SMALL)]
    t = Table(wrap(rows), colWidths=[46 * mm, 128 * mm])
    t.setStyle(TBL)
    f.append(t)
    d.build(f)
    return path


def bulletin(target, series):
    """the platform's own published quarterly quality series, platform wide and by nothing else"""
    path = os.path.join(target, "published_quarterly_quality_report.pdf")
    d = _doc(path, "Quarterly quality report")
    rows = [["Quarter", "Median delivered bitrate, kbps", "Sessions, millions",
             "Rebuffer rate, per cent"]] + series
    f = [Paragraph("%s: quarterly quality report" % W.PLATFORM, H1),
         Paragraph("Published for subscribers and partners. Figures are platform wide across all "
                   "access networks and are not broken down by interconnect.", SMALL)]
    t = Table(wrap(rows), colWidths=[30 * mm, 56 * mm, 44 * mm, 44 * mm])
    t.setStyle(TBL)
    f.append(t)
    f.append(Spacer(1, 4 * mm))
    f.append(Paragraph("The platform reports the median delivered bitrate across every session it "
                       "served in the quarter. Quarter on quarter movement reflects the mix of "
                       "titles, devices and access networks as much as the network itself.", BODY))
    d.build(f)
    return path
