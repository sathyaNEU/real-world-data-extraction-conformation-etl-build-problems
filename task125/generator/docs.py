"""The pack's documents: the Crime Analysis Unit's designation protocol, Patrol Operations' measures directive, and the
Superintendent's request. Each carries its own save history; table cells wrap inside the page."""
import datetime as dt
import re
from email.message import EmailMessage
from email.utils import format_datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

INK = colors.HexColor("#1b2a38")
RULE = colors.HexColor("#7f909e")


def _styles():
    base = ParagraphStyle("p", fontName="Helvetica", fontSize=9.6, leading=13.1, textColor=INK, alignment=TA_LEFT,
                          spaceAfter=5)
    return {"t": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4),
            "s": ParagraphStyle("s", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#4c5d6a")),
            "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                                spaceBefore=6),
            "p": base,
            "cell": ParagraphStyle("cell", parent=base, fontSize=8.6, leading=11.0, spaceAfter=0),
            "head": ParagraphStyle("head", parent=base, fontName="Helvetica-Bold", fontSize=8.6, leading=11.0,
                                   spaceAfter=0)}


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _pdf(path, title, author, blocks, footer, created, modified):
    st = _styles()

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#5a6a76"))
        canvas.drawString(19 * mm, 10 * mm, footer)
        canvas.drawRightString(LETTER[0] - 19 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=LETTER, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, producer=author,
                            invariant=1)
    story = []
    width = LETTER[0] - 38 * mm
    for kind, val in blocks:
        if kind == "table":
            ncol = max(len(r) for r in val)
            if ncol == 2:
                widths = [42 * mm, width - 42 * mm]
            elif ncol == 3:
                widths = [24 * mm, 62 * mm, width - 86 * mm]
            else:
                widths = [width / ncol] * ncol
            data = [[Paragraph(_esc(c), st["head"] if i == 0 else st["cell"]) for c in r] for i, r in enumerate(val)]
            t = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
            story += [t, Spacer(1, 6)]
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    for sig in (b"ReportLab Generated PDF document (opensource)",
                b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + created.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + modified.encode() + b")", data)
    open(path, "wb").write(data)


def protocol(path):
    codes = [["Code", "Offence"]] + [[c, d] for c, d in W.PATROL.items()]
    blocks = [
        ("t", "Hot Spot Patrol Programme: designation protocol"),
        ("s", "Mountjoy Police Service, Crime Analysis Unit. 2027 edition, approved by the Chief of Police on "
              "10 November 2026. Owner: Eric Gordon, Manager, Crime Analysis Unit."),
        ("h", "1. Purpose"),
        ("p", "The Hot Spot Patrol Programme puts short, frequent directed patrols on the street segments where the "
              "city's street crime concentrates. A designated segment is visited by a two-officer car for about "
              "fifteen minutes at a time, at unpredictable times between 14:00 and 03:00, as the platoons' "
              "directed-patrol plan sets out. The programme's two cars have room for 20 segments."),
        ("h", "2. The designation"),
        ("p", "Once a year the Superintendent, Patrol Operations adopts the segments the programme patrols for the "
              "calendar year, with the platoons' deployment plan. "
              "The Crime Analysis Unit designates the 20 street segments with the highest expected patrol crimes in "
              "the year the designation covers, and puts the designation to the Superintendent with a chart of each "
              "candidate segment's expected patrol crimes against the cut, the designated segments marked."),
        ("h", "3. Definitions"),
        ("table", [["Term", "Meaning"],
                   ["Street segment", "A segment in the City of Mountjoy's street segment file: one street between "
                                      "two cross streets."],
                   ["Patrol crime", "An occurrence whose offence is one of the codes in Table 1. Occurrences entered "
                                    "in the records system before its migration on 1 March 2023 carry the legacy "
                                    "system's codes, which the 2023 offence code crosswalk reads into the codes in "
                                    "Table 1."],
                   ["Founded", "An occurrence counts unless its latest version records it as unfounded."],
                   ["Counting", "Each occurrence counts once, under the offence and on the segment of its latest "
                                "version."],
                   ["Date", "An occurrence belongs to the date it began, its occurred-from date. An occurrence the "
                            "records system holds no occurrence date for belongs to the date it was reported."],
                   ["Expected patrol crimes", "The number of founded patrol crimes a segment is expected to record "
                                              "in the calendar year the designation covers."],
                   ["Candidate segment", "A street segment that recorded at least 25 founded patrol crimes in at "
                                         "least one of the five calendar years before the designation."]]),
        ("h", "Table 1. Patrol crime offence codes"),
        ("table", codes),
        ("h", "4. Review"),
        ("p", "The Unit reviews the protocol each autumn with the Superintendent, Patrol Operations; a revised "
              "edition applies from the next designation."),
    ]
    _pdf(path, "Hot Spot Patrol Programme designation protocol, 2027 edition", "MPS Crime Analysis Unit", blocks,
         "Mountjoy Police Service  |  Crime Analysis Unit  |  Hot Spot Patrol Programme protocol, 2027 edition",
         "D:20261022141500-04'00'", "D:20261110093000-05'00'")


def directive(path):
    blocks = [
        ("t", "Directive PO-14: patrol workload and response measures"),
        ("s", "Mountjoy Police Service, Patrol Operations. Issued 3 March 2025 by the Chief of Police. Owner: the "
              "Superintendent, Patrol Operations."),
        ("h", "1. Purpose"),
        ("p", "This directive fixes how the Service measures the patrol workload calls for service bring and how fast "
              "officers reach emergencies, so that the figures the command team and the Police Services Board see "
              "from one year to the next are the same measures."),
        ("h", "2. Definitions"),
        ("table", [["Term", "Meaning"],
                   ["Call for service", "A request for police service received by the Communications Centre: by "
                                        "911, on the administrative line, from an alarm company or in person. An "
                                        "event an officer starts on view is not a call for service."],
                   ["Priority", "The priority at which the Communications Centre dispatched the call. Priority 1 "
                                "is an emergency."],
                   ["Response time", "The minutes from the receipt of the call to the arrival on scene of the first "
                                     "officer."],
                   ["Officer-hours on a call", "For each unit assigned to the call, the hours from the unit's "
                                               "dispatch to its clearing, times the number of officers on the "
                                               "unit."],
                   ["Period", "A call belongs to the local date on which it was received."],
                   ["Ward", "A ward's figures count the calls for service at addresses in that ward of the City "
                            "of Mountjoy. A call at an address outside the City's wards belongs to no ward."]]),
        ("h", "3. Tours"),
        ("p", "Patrol platoons work twelve-hour tours: day tours from 07:00 to 19:00 and night tours from 19:00 to "
              "07:00. A car is one-officer or two-officer as the platoon staffs it for the tour."),
        ("h", "4. Reporting"),
        ("p", "The Superintendent, Patrol Operations reports the measures by ward to the command team each year with "
              "the deployment plan, and to the Board on request."),
    ]
    _pdf(path, "Directive PO-14: patrol workload and response measures", "MPS Patrol Operations", blocks,
         "Mountjoy Police Service  |  Patrol Operations  |  Directive PO-14",
         "D:20250218101200-05'00'", "D:20250303154000-05'00'")


def request(path):
    m = EmailMessage()
    m["From"] = "Lindsey Turner <lindsey.turner@mountjoypolice.ca>"
    m["To"] = "Eric Gordon <eric.gordon@mountjoypolice.ca>"
    m["Subject"] = "2027 hot spot designation, for sign-off on 12 January"
    m["Date"] = format_datetime(dt.datetime(2027, 1, 6, 13, 42, 0, tzinfo=dt.timezone.utc))
    m["Message-ID"] = "<20270106134200.2214@mountjoypolice.ca>"
    m.set_content(
        "Eric,\n\n"
        "I sign off the 2027 hot spot designation on 12 January with the rest of the platoons' 2027 deployment plan. "
        "Please have the Unit put it together under the protocol, with the chart the protocol calls for, as a "
        "short deck.\n\n"
        "Information Management's usual extracts are in the folder: the RMS occurrences from 2022 to this morning's "
        "extract, the street segment file and the 2023 code crosswalk, the paid-duty register, and the "
        "Communications Centre's 2026 CAD export with the 2026 patrol roster. I have also put in the ward profiles and "
        "the streetlight requests the Downtown BIA sent us in the autumn.\n\n"
        "For the deployment plan the Chief wants the officer-hours each ward's calls for service took in each "
        "quarter of 2026, as Directive PO-14 defines them, in a CSV beside the deck.\n\n"
        "Thanks,\n\n"
        "Lindsey Turner\nSuperintendent, Patrol Operations\nMountjoy Police Service\n")
    open(path, "wb").write(m.as_bytes(policy=m.policy.clone(linesep="\n")))
