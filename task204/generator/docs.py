"""PDF and DOCX documents of target/ (governing directive, station reference, planning note, school calendar)."""
import datetime as dt

from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import docx
from docx.shared import Pt

import params as P
import world_net as N
from pack_data import POLICE_STN, normalise_zip

rl_config.invariant = 1

SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.6, leading=12.6, spaceAfter=5)
HEAD = ParagraphStyle("h", parent=SS["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=3)
TITLE = ParagraphStyle("t", parent=SS["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4)
SMALL = ParagraphStyle("s", parent=SS["Normal"], fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444"))


def _pdf(path, story, title, author, producer):
    def meta(canvas, doc):
        canvas.setTitle(title)
        canvas.setAuthor(author)
        canvas.setCreator(author)
        canvas.setProducer(producer)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.8 * inch, 0.55 * inch, "%s  |  page %d" % (title, doc.page))

    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.8 * inch, rightMargin=0.8 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.8 * inch, title=title, author=author)
    doc.build(story, onFirstPage=meta, onLaterPages=meta)


DIRECTIVE_TEXT = [
    ("1. Purpose", "This directive sets how the Service assigns investigative resources to the offender groups behind "
                   "series of robbery and theft from a person, and what the Crime Analysis Unit's series assessment "
                   "for each seasonal deployment plan contains."),
    ("2. Scope", "The directive applies to robbery of a person (offence code ROB-PERS) and theft from a person "
                 "(THFT-PERS) in which a mobile phone was taken, whether the offence was reported to the Service or to "
                 "Carvale Transit Peace Officers. An offence reported to both is one offence."),
    ("3. Definitions", None),
    ("4. Series teams", "The Deputy Chief (Operations) assigns one series team to each offender group responsible for a "
                        "series in the review period. A series team's ground is every patrol district in which an "
                        "offence of its group's series in the review period took place. An offence that is not part of "
                        "a series stays with the investigators of the district where it took place."),
    ("5. Series assessment", "The Crime Analysis Unit prepares the series assessment for each seasonal deployment plan. "
                             "For each offender group it gives the group's ground and the number of offences of its "
                             "series in the review period, and it states the patrol districts with no series."),
    ("6. Team composition and funding", "A series team is one sergeant and six constables drawn from the Investigative "
                                        "Services pool. Series team hours are charged to the seasonal overtime "
                                        "allocation approved with the deployment plan. A team stands down when its "
                                        "group's series has been charged or when two review periods pass with no "
                                        "offence of the series."),
    ("7. Records", "Series assessments are retained with the deployment plan for seven years. Changes to this directive "
                   "are approved by the Deputy Chief (Operations)."),
]
DEFINITIONS = [
    ("Offender group", "two or more people who commit offences together."),
    ("Series", "three or more offences committed by the same offender group."),
    ("Review period", "the twelve completed weeks, Monday to Sunday, before the date of the series assessment."),
    ("Patrol district", "a district of the patrol district layout in force on the date of the series assessment."),
]


def directive_pdf(path):
    st = []
    st.append(Paragraph("Carvale Police Service", SMALL))
    st.append(Paragraph("Operational Directive OPS-41: Series Crime Response", TITLE))
    st.append(Paragraph("Issued 15 September 2025 &nbsp;&nbsp; Owner: Superintendent %s, Investigative Services "
                        "&nbsp;&nbsp; Approved: Deputy Chief (Operations) %s &nbsp;&nbsp; Version 2.1"
                        % (P.PEOPLE["directive_owner"], P.PEOPLE["deputy_chief"]), SMALL))
    st.append(Spacer(1, 8))
    for head, text in DIRECTIVE_TEXT:
        st.append(Paragraph(head, HEAD))
        if text:
            st.append(Paragraph(text, BODY))
        else:
            for term, defin in DEFINITIONS:
                st.append(Paragraph("<b>%s:</b> %s" % (term, defin), BODY))
    st.append(Spacer(1, 10))
    st.append(Paragraph("Version history: 1.0 (May 2022) first issue; 2.0 (March 2024) transit peace officer reports "
                        "brought into scope; 2.1 (September 2025) team stand-down rule added.", SMALL))
    _pdf(path, st, "OPS-41 Series Crime Response", "Carvale Police Service", "Carvale Police Service")


def station_reference_pdf(path):
    st = [Paragraph("Carvale Police Service - Crime Analysis Unit", SMALL),
          Paragraph("LRT station reference, patrol district layout of 1 January 2026", TITLE),
          Paragraph("Revised 6 April 2026 (Fairgrounds station added). For use with RMS location text.", SMALL),
          Spacer(1, 8)]
    rows = [["Station", "Line", "RMS location text", "Patrol district", "In service from"]]
    order = ["WG", "CS", "UY", "MB", "FG", "CB", "AR", "RV", "PG", "SH", "KP", "HL", "LM"]
    for s in order:
        line = "Eastline / Northline" if s == "CS" else ("Northline" if s in ("SH", "KP", "HL", "LM") else "Eastline")
        opened = "29 Mar 2026" if s == "FG" else ("23 Apr 2012" if s in ("RV", "PG") else "27 Apr 2008")
        d = N.district_of(N.STN[s]["x"], N.STN[s]["y"], P.D26)
        rows.append([N.STN[s]["name"], line, POLICE_STN[s], d, opened])
    t = Table(rows, colWidths=[1.25 * inch, 1.35 * inch, 1.9 * inch, 0.95 * inch, 1.05 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.4), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.4),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E6E6E6"))]))
    st.append(t)
    st.append(Spacer(1, 10))
    st.append(Paragraph("Centre Square is served by both lines; occurrences there are recorded under one location text.", BODY))
    _pdf(path, st, "CAU LRT station reference 2026", "Carvale Police Service Crime Analysis Unit", "Carvale Police Service")


def school_calendar_pdf(path):
    st = [Paragraph("Carvale Public School Division", SMALL), Paragraph("2025-2026 school year calendar", TITLE), Spacer(1, 6)]
    rows = [["Date", "Event"],
            ["2 Sep 2025", "First day of classes"], ["13 Oct 2025", "Thanksgiving, no school"],
            ["10-11 Nov 2025", "Remembrance Day break"], ["22 Dec 2025 - 2 Jan 2026", "Winter break"],
            ["30 Jan 2026", "Non-instructional day"], ["16 Feb 2026", "Family Day, no school"],
            ["26-27 Feb 2026", "Teachers' convention, no school"], ["30 Mar - 3 Apr 2026", "Spring break"],
            ["18 May 2026", "Victoria Day, no school"], ["26 Jun 2026", "Last day of classes"]]
    t = Table(rows, colWidths=[2.2 * inch, 3.6 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999"))]))
    st.append(t)
    st.append(Spacer(1, 8))
    st.append(Paragraph("Instructional hours: elementary 8:40 to 15:20, junior high 8:30 to 15:10, high school 8:15 to 15:05.", BODY))
    _pdf(path, st, "CPSD 2025-26 calendar", "Carvale Public School Division", "Carvale Public School Division")


def planning_note_docx(path):
    d = docx.Document()
    style = d.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    d.add_paragraph("Carvale Police Service").runs[0].bold = True
    d.add_paragraph("Planning note: summer deployment plan 2026")
    d.add_paragraph("From: Deputy Chief (Operations) %s\nTo: %s, Crime Analysis Unit\nDate: 4 May 2026"
                    % (P.PEOPLE["deputy_chief"], P.PEOPLE["cau_supervisor"]))
    paras = [
        "The summer deployment plan runs from 1 June to 27 September and I sign it on 28 May. Please have the OPS-41 "
        "series assessment to me by 22 May, dated today, 4 May, so that its review period is the twelve weeks to Sunday 3 May.",
        "Series team overtime is held in the seasonal allocation. Patrol and community response staffing for the "
        "summer is set separately and does not wait on the assessment.",
        "The Police Commission's June report sets each district's figures beside the offences OPS-41 covers that took "
        "place in the same weeks of last year, 10 February to 4 May 2025, so please include that comparison on the "
        "current district layout. Carvale Transit's security operations manager has also asked for the fare-gate entries and the number "
        "of scheduled Eastline train calls at each Eastline station over the same twelve weeks, for the platform "
        "staffing review the two agencies are running.",
        "Records will pull the occurrence extract on Monday 11 May, once the late reports for the period are in, and "
        "Steven House at Transit Security Operations will send the transit peace officers' log for both years the same day.",
    ]
    for t in paras:
        d.add_paragraph(t)
    d.add_paragraph("E. Wagner")
    cp = d.core_properties
    cp.author = "E. Wagner"
    cp.last_modified_by = "E. Wagner"
    cp.title = "Planning note: summer deployment plan 2026"
    cp.created = dt.datetime(2026, 5, 4, 8, 12, 0)
    cp.modified = dt.datetime(2026, 5, 4, 8, 31, 0)
    cp.revision = 2
    d.save(path)
    normalise_zip(path)
