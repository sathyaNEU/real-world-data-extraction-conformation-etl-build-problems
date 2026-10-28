"""task270 documents: the service's emergency cover standard for the 2027-2031 plan, the on-call duty system policy,
and the county council's cabinet report on the plan. Their text is data here so checks.py and verify.py can quote and
execute it."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1d2329")
GREY = colors.HexColor("#5a6470")
ACCENT = colors.HexColor("#8a1c1c")
RULE = colors.HexColor("#b8c1c9")
HEAD = colors.HexColor("#f0e6e6")

# ------------------------------------------------------------------------------------------------- the standard
STANDARD_TITLE = "Emergency cover standard"
STANDARD_REF = "OFRS-RS-03 issue 1"
STANDARD = [
    ("1 Purpose", [
        "This standard sets how Ostrevale Fire and Rescue Service measures the emergency cover it gave each of the "
        "county's seven districts in a year. The community risk management plan 2027 to 2031 names every district "
        "whose cover for 2026 falls below the line in section 6, and the plan's response review proposes the changes "
        "for those districts."]),
    ("2 Homes", [
        "A home is an address the address register classes as a residential dwelling (classification codes beginning "
        "RD). A home belongs to the district its 2021 output area lies in. Other addresses are not homes."]),
    ("3 When a home is covered", [
        "A home is covered in a minute when a fire engine that is free at the start of that minute could reach it "
        "within ten minutes: its crew's turnout and its drive to the home together take ten minutes or less.",
        "A fire engine is free when the mobilising system shows it Available (status code 1). An engine that is "
        "mobilised, in attendance or off the run is not free."]),
    ("4 Turnout and drive", [
        "Turnout is two minutes for an engine crewed by wholetime firefighters and five minutes for an engine crewed "
        "by on-call firefighters, as the fleet list records its crewing.",
        "A drive is timed over the service's routing network, each link at the drive time it carries and only in the "
        "directions it may be driven, between the network nodes nearest its start and its end."]),
    ("5 A district's cover for a year", [
        "A district's cover for a year is the share of its homes covered, averaged over every minute of the year. For "
        "2026 that is the 525,600 minutes from 00:00 UTC on 1 January 2026."]),
    ("6 The line", [
        "A district whose cover for 2026 is below 75 per cent is named in the plan. A district is named on its "
        "unrounded cover."]),
]

# ------------------------------------------------------------------------------------------------- the policy
POLICY_TITLE = "On-call duty system: availability and crewing"
POLICY_REF = "Operational policy OP-14 issue 4"
POLICY = [
    ("1 Purpose", [
        "This policy sets how on-call firefighters make themselves available for calls and when an on-call fire "
        "engine is on the run. It applies at the eighteen stations crewed on the on-call duty system."]),
    ("2 Booking availability", [
        "On-call firefighters book the periods they are available for calls in the availability system, from their "
        "own phone or the station terminal. A firefighter booked available is within five minutes of the station and "
        "answers every alert in that period. Each firefighter agrees a number of hours a week in their contract."]),
    ("3 Crewing an engine", [
        "An on-call engine is on the run when four or more of its station's firefighters are booked available, among "
        "them a crew commander or watch commander, an LGV driver and two breathing apparatus wearers.",
        "When it is not, the availability system sets the engine's status in the mobilising system to Off the run "
        "(status code 8) with the reason Crew, and back to Available when the crew is complete."]),
    ("4 Defects and workshop", [
        "An engine taken out of service for a defect, or for its workshop service, is off the run with the reason "
        "Defect or Workshop for that time, whoever is booked."]),
    ("5 Officer in charge", [
        "Crew commanders and watch commanders may take charge of an on-call engine. A firefighter promoted to crew "
        "commander may take charge from the date the promotion takes effect."]),
]

# ------------------------------------------------------------------------------------------------- the cabinet report
CABINET_TITLE = "Community Risk Management Plan 2027 to 2031"
CABINET = [
    ("1 Purpose of the report", [
        "To ask Cabinet to approve the Community Risk Management Plan 2027 to 2031 for publication before 31 March "
        "2027."]),
    ("2 Recommendations", [
        "That Cabinet (a) approves the plan for publication; (b) notes that the plan's response review will name the "
        "districts whose 2026 cover falls below the line in the service's emergency cover standard, with its "
        "proposals for each, at Appendix B; and (c) delegates minor amendments before publication to the Chief Fire "
        "Officer in consultation with the Cabinet Member for Community Safety."]),
    ("3 Background", [
        "The Fire and Rescue National Framework for England requires every fire and rescue authority to publish a "
        "community risk management plan that identifies the risks its communities face and sets out how it will "
        "prevent, protect against and respond to them. Ostrevale County Council is the fire and rescue authority for "
        "the county; its current plan runs to 31 March 2027."]),
    ("4 The service", [
        "Ostrevale Fire and Rescue Service has 24 fire stations and 26 fire engines. Six stations are crewed by "
        "wholetime firefighters (Calderstow, Calderstow East, Tollesham, Wrenfold, Hollinbury and Pelmarsh) and "
        "eighteen by on-call firefighters, who live or work near their station and answer alerts on a pager. The "
        "control room mobilises the service's engines across the county's seven districts: Calderstow, Tollesham, "
        "Wrenfold, Hollinbury, Pelmarsh, Altmoor and Skirwold."]),
    ("5 The response review", [
        "The service adopted its emergency cover standard (OFRS-RS-03) in November 2026. It measures, for each "
        "district, the share of its homes a free fire engine could reach within ten minutes, averaged over every "
        "minute of the year. The review applies it to 2026 and names each district below 75 per cent.",
        "The review's evidence also covers the availability of the on-call engines in Altmoor and Skirwold, where "
        "every station is crewed on the on-call duty system, and the false alarms the service attends from fire alarm "
        "apparatus at non-domestic premises, which take engines away from emergencies."]),
    ("6 Consultation and timetable", [
        "The draft plan was consulted on from 5 October to 27 November 2026. Cabinet considers the final plan on 23 "
        "February 2027 with the response review's Appendix B, and the plan is published by 31 March 2027."]),
    ("7 Financial, legal and equality implications", [
        "The plan is delivered within the service's approved budget for 2027-28; proposals with a cost will come to "
        "Cabinet separately. Publishing the plan meets the council's duty under the Fire and Rescue Services Act 2004 "
        "and the National Framework. An equality impact assessment accompanies the plan."]),
]
CABINET_APPENDIX = [
    ("Non-domestic premises", "Addresses the address register classes commercial (classification codes beginning C)."),
    ("False alarms from fire alarm apparatus",
     "Incidents classified A01 up to 31 March 2024 and FAA from 1 April 2024 (incident classification codes)."),
]


def text_of_sections(secs):
    return " ".join(" ".join(ps) for _h, ps in secs)


# ------------------------------------------------------------------------------------------------- PDF writing
def _styles():
    return dict(
        title=ParagraphStyle("t", fontName="LibSans-Bold", fontSize=15, leading=19, textColor=INK, spaceAfter=4),
        sub=ParagraphStyle("s", fontName="LibSans", fontSize=9, leading=12, textColor=GREY, spaceAfter=10),
        h=ParagraphStyle("h", fontName="LibSans-Bold", fontSize=10.5, leading=14, textColor=ACCENT, spaceBefore=8,
                         spaceAfter=3),
        p=ParagraphStyle("p", fontName="LibSans", fontSize=9.5, leading=13.2, textColor=INK, spaceAfter=5),
        cell=ParagraphStyle("c", fontName="LibSans", fontSize=8.5, leading=10.5, textColor=INK),
    )


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("LibSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(2 * cm, 1.2 * cm, text)
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths):
    st = _styles()
    data = [[Paragraph(str(c), st["cell"]) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm,
                             bottomMargin=1.8 * cm, title=title, author=author, subject="", creator="", producer="")


def write_standard(path):
    st = _styles()
    doc = _doc(path, STANDARD_TITLE, K.SERVICE)
    flow = [Paragraph(K.SERVICE, st["sub"]), Paragraph(STANDARD_TITLE, st["title"]),
            Paragraph("%s. Community risk management plan 2027 to 2031. Approved by the Chief Fire Officer on 2 November "
                      "2026. Owner: %s, Area Manager, Response and Resilience." % (STANDARD_REF, K.PEOPLE["review"]),
                      st["sub"])]
    for head, paras in STANDARD:
        flow.append(Paragraph(head, st["h"]))
        for p in paras:
            flow.append(Paragraph(p, st["p"]))
    doc.build(flow, onFirstPage=_footer("%s  |  Official" % STANDARD_REF), onLaterPages=_footer("%s  |  Official" % STANDARD_REF))


def write_policy(path):
    st = _styles()
    doc = _doc(path, POLICY_TITLE, K.SERVICE)
    flow = [Paragraph(K.SERVICE, st["sub"]), Paragraph(POLICY_TITLE, st["title"]),
            Paragraph("%s, effective 1 April 2025. Owner: Area Manager, Response and Resilience." % POLICY_REF, st["sub"])]
    for head, paras in POLICY:
        flow.append(Paragraph(head, st["h"]))
        for p in paras:
            flow.append(Paragraph(p, st["p"]))
    doc.build(flow, onFirstPage=_footer("%s  |  Official" % POLICY_REF), onLaterPages=_footer("%s  |  Official" % POLICY_REF))


def write_cabinet(path):
    st = _styles()
    doc = _doc(path, CABINET_TITLE, K.COUNCIL)
    flow = [Paragraph("%s  |  Report to Cabinet, 23 February 2027  |  Agenda item 7" % K.COUNCIL, st["sub"]),
            Paragraph(CABINET_TITLE, st["title"]),
            Paragraph("Report of the Chief Fire Officer. Cabinet Member: Councillor %s, Community Safety. Key decision: "
                      "yes. Open report." % K.PEOPLE["cabinet"], st["sub"])]
    for head, paras in CABINET:
        flow.append(Paragraph(head, st["h"]))
        for p in paras:
            flow.append(Paragraph(p, st["p"]))
    flow.append(Paragraph("Appendix A. Terms used in the plan's risk profile", st["h"]))
    flow.append(_table([["Term", "Meaning"]] + [list(r) for r in CABINET_APPENDIX], [5.0 * cm, 12.0 * cm]))
    flow.append(Spacer(1, 6))
    flow.append(Paragraph("Appendix B. Response review: districts below the emergency cover standard (to follow).",
                          st["p"]))
    flow.append(Paragraph("Contact: Democratic Services, %s." % K.COUNCIL, st["sub"]))
    doc.build(flow, onFirstPage=_footer("Cabinet 23 February 2027  |  Item 7"),
              onLaterPages=_footer("Cabinet 23 February 2027  |  Item 7"))
