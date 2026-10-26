"""The two governing documents: the clinic's 2025-26 annual report and the ICB's planning assumptions."""
import calendar
import datetime as dt
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.5, leading=12.5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=14, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=11, spaceBefore=8, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
TS = TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.3), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.3),
                 ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                 ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)])


def clean(path, when, tz):
    """The writing library leaves its name in two comments and a fixed 2000 date in the document information; overwrite
    them in place at equal length, so every byte offset (and the cross-reference table) stays where it was."""
    import re
    b = open(path, "rb").read()
    n0 = len(b)
    for tag in (b" ReportLab Generated PDF document (opensource)", b" ReportLab generated PDF document -- digest (opensource)"):
        b = b.replace(tag, b" " * len(tag))
    stamp = ("D:%s%s" % (when.strftime("%Y%m%d%H%M%S"), tz)).encode()
    b = re.sub(rb"D:20000101000000\+00'00'", stamp, b)
    assert len(b) == n0 and b"ReportLab" not in b and b"D:2000" not in b
    open(path, "wb").write(b)


def doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator="Microsoft Word",
                             producer="Microsoft Word for Microsoft 365", subject="", keywords="")


def annual_report(path, monthly, yearly):
    S = [Paragraph("%s<br/>Outpatient Phlebotomy Service: annual report 2025-26" % P.HOSPITAL, H1),
         Paragraph("%s, Phlebotomy Service Manager. Reviewed by %s, Pathology Operations Lead. Presented to the Clinical "
                   "Support Services divisional board, 19 May 2026." % (P.PEOPLE["manager"], P.PEOPLE["ops_lead"]), SMALL),
         Spacer(1, 6), Paragraph("1. The service", H2),
         Paragraph("The walk-in clinic in Outpatients block A takes adults with a blood test request from a GP practice or "
                   "a hospital outpatient clinic, Monday to Friday, 07:30 to 15:30, with the ticket kiosk switched on at "
                   "07:15. It is closed on bank holidays. The clinic has seven phlebotomist posts, one senior phlebotomist "
                   "at Band 3 and six phlebotomists at Band 2, and the bank office covers gaps when a bank phlebotomist is "
                   "free. Each morning the senior phlebotomist sets the day's walk-in tickets at 40 for each substantive "
                   "phlebotomist on the floor and 32 for each bank phlebotomist. When the last ticket has gone, reception "
                   "tells anyone else arriving that the clinic is full and offers a booked appointment at %s; reception "
                   "records the patients turned away for the PALS monthly return. Most of the catchment's practices run "
                   "their own phlebotomy clinics under the local enhanced service." % P.SATELLITE, BODY),
         Paragraph("The queue system changed in November 2024: the new kiosk went live on 18 November and the old system "
                   "was switched off after the session on 29 November. For those two weeks reception keyed every ticket "
                   "into the old system as well, so both systems hold those visits.", BODY),
         Paragraph("2. Activity in 2025-26", H2)]
    rows = [["Month", "Clinic days", "GP seen", "Hospital seen", "GP turned away", "Hospital turned away",
             "Days tickets ran out"]]
    tot = [0] * 6
    for r in monthly:
        y, m = r["ym"]
        vals = [r["days"], r["gp_seen"], r["h_seen"], r["gp_away"], r["h_away"], r["ro"]]
        tot = [a + b for a, b in zip(tot, vals)]
        rows.append(["%s %d" % (calendar.month_abbr[m], y)] + ["{:,}".format(v) for v in vals])
    rows.append(["2025-26"] + ["{:,}".format(v) for v in tot])
    t = Table(rows, colWidths=[22 * mm, 19 * mm, 19 * mm, 22 * mm, 25 * mm, 28 * mm, 29 * mm])
    t.setStyle(TS)
    t.setStyle(TableStyle([("FONT", (0, -1), (-1, -1), "Helvetica-Bold", 8.3), ("LINEABOVE", (0, -1), (-1, -1), 0.6, colors.black)]))
    S += [t, Spacer(1, 3), Paragraph("Seen are completed visits from the queue system, by the request form the patient "
                                     "brought. Turned away are from the reception log.", SMALL)]
    S.append(Paragraph("3. Three years of activity", H2))
    rows = [["", "2023-24", "2024-25", "2025-26"],
            ["GP-referred patients seen (thousands)"] + ["%.1f" % (yearly[k]["gp"] / 1000) for k in (2023, 2024, 2025)],
            ["Hospital-clinic patients seen (thousands)"] + ["%.1f" % (yearly[k]["h"] / 1000) for k in (2023, 2024, 2025)]]
    t = Table(rows, colWidths=[62 * mm, 24 * mm, 24 * mm, 24 * mm])
    t.setStyle(TS)
    S.append(t)
    S.append(Paragraph("4. Staffing", H2))
    S.append(Paragraph("One Band 2 post was vacant from 14 July to 12 September 2025; the bank office covered the line on "
                       "most of those days. The service reports sickness absence as "
                       "the hours lost to sickness as a percentage of the hours rostered to the substantive team: every "
                       "clinic day of every filled post at 7.5 hours, leave and sickness included, with vacant posts and "
                       "bank shifts left out.", BODY))
    S.append(Paragraph("5. Patient experience", H2))
    S.append(Paragraph("The June 2025 patient survey (412 responses) rated the clinic good or very good in 78 per cent of "
                       "responses; 41 per cent of respondents reported waiting more than 45 minutes after taking a ticket, "
                       "and the commonest comment asked for bookable appointments.", BODY))
    S.append(Paragraph("6. The community hub", H2))
    S.append(Paragraph("The business case for a community phlebotomy hub at Kingsmead Health Village was approved in March "
                       "2026. From 1 April 2027 the hub takes every patient with a GP request and will be staffed so that "
                       "it does not run out of tickets; its booked slots are for those same patients, who can book rather "
                       "than queue. Patients sent from hospital clinics keep using "
                       "the clinic in Outpatients block A, and the booked clinic at %s carries on as now. Its "
                       "activity plan is to be set from 2025-26 with the integrated care board's planning assumption for "
                       "GP direct access phlebotomy." % P.SATELLITE, BODY))
    doc(path, "Outpatient Phlebotomy annual report 2025-26", P.PEOPLE["manager"]).build(S)
    clean(path, dt.datetime(2026, 5, 14, 9, 42, 10), "+01'00'")


def icb_letter(path):
    S = [Paragraph("%s<br/>Pathology demand planning assumptions, 2026-27 to 2028-29" % P.ICB, H1),
         Paragraph("Issued by %s, Head of Planned Care, to provider trusts' planning leads, 12 February 2026." % P.PEOPLE["icb_lead"], SMALL),
         Spacer(1, 6),
         Paragraph("These are the annual growth assumptions the board will use when it agrees providers' 2027-28 activity "
                   "plans for pathology. They are to be applied to 2025-26, the last complete year, for each year to the "
                   "plan year, and cover demography, the growth in long-term condition monitoring and the changes in "
                   "testing already agreed for the system.", BODY), Spacer(1, 4)]
    rows = [["Service line", "Growth a year", "Notes"],
            ["GP direct access phlebotomy", "3.5%", "community and hospital sites"],
            ["Hospital outpatient phlebotomy", "2.0%", "outpatient follow-up growth"],
            ["Direct access pathology tests", "4.5%", "tests per request rising"],
            ["Anticoagulation INR testing", "-12.0%", "moving to community pharmacy"],
            ["Inpatient phlebotomy rounds", "1.0%", "bed base unchanged"]]
    t = Table(rows, colWidths=[62 * mm, 26 * mm, 62 * mm])
    t.setStyle(TS)
    t.setStyle(TableStyle([("ALIGN", (2, 0), (2, -1), "LEFT")]))
    S += [t, Spacer(1, 6),
          Paragraph("Working days are not adjusted for: the assumptions are annual. Questions to the planned care team.", BODY)]
    doc(path, "Pathology demand planning assumptions 2026-27 to 2028-29", P.PEOPLE["icb_lead"]).build(S)
    clean(path, dt.datetime(2026, 2, 12, 8, 55, 31), "+00'00'")
