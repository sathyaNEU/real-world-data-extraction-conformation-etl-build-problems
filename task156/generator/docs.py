"""task156 documents: the council's charter and its 2027 handle-time standards, finance's envelope letter, the
moderation team's flag service standard and operations handbook, the data platform team's question count standard and
the 2026 member survey (unused by the solution). No file describes the data: every export names its own columns. Their
text is kept here as data so checks.py can quote and execute it."""
from __future__ import annotations

import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import inch                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2329")
GREY = colors.HexColor("#5f6670")
COUNCIL = colors.HexColor("#3b4a6b")
FIN = colors.HexColor("#245a4a")
RULE = colors.HexColor("#a3abb5")
HEAD = colors.HexColor("#e7ebf0")


def styles(font, bold, accent, size=10.2):
    return dict(
        body=ParagraphStyle("b" + font + str(size), fontName=font, fontSize=size, leading=size * 1.36, textColor=INK,
                            spaceAfter=6),
        h1=ParagraphStyle("h1" + font + str(size), fontName=bold, fontSize=14.0, leading=18.0, textColor=accent,
                          spaceAfter=3),
        sub=ParagraphStyle("s" + font + str(size), fontName=font, fontSize=8.9, leading=11.8, textColor=GREY,
                           spaceAfter=9),
        h2=ParagraphStyle("h2" + font + str(size), fontName=bold, fontSize=10.6, leading=14.0, textColor=accent,
                          spaceBefore=7, spaceAfter=3),
        cell=ParagraphStyle("c" + font + str(size), fontName=font, fontSize=8.8, leading=11.0, textColor=INK),
        cellb=ParagraphStyle("cb" + font + str(size), fontName=bold, fontSize=8.8, leading=11.0, textColor=INK),
        small=ParagraphStyle("sm" + font + str(size), fontName=font, fontSize=8.2, leading=10.6, textColor=GREY,
                             spaceAfter=4))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=1.0 * inch, rightMargin=1.0 * inch,
                             topMargin=0.8 * inch, bottomMargin=0.8 * inch, title=title, author=author, subject="",
                             creator="", producer="")


def _footer(left, font="Carlito"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(0.9 * inch, 0.5 * inch, left)
        canvas.drawRightString(letter[0] - 0.9 * inch, 0.5 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid(rows, widths, st, head=True):
    data = []
    for k, row in enumerate(rows):
        data.append([Paragraph(esc(str(c)), st["cellb"] if (head and k == 0) else st["cell"]) for c in row])
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1 if head else 0)
    style = [("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
             ("TOPPADDING", (0, 0), (-1, -1), 2.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    if head:
        style.append(("BACKGROUND", (0, 0), (-1, 0), HEAD))
    t.setStyle(TableStyle(style))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ---------------------------------------------------------------------------------------------------- the charter
F_CHARTER = "moderation_council_charter_2025.pdf"
CHARTER = [
    ("1. Purpose", [
        "The Moderation Council sets how much paid moderation Millrind's nine sites need each year, asks finance for "
        "it, and divides the pool finance funds among the sites. It does not moderate content and it does not manage "
        "the paid moderation team.",
    ]),
    ("2. Members", [
        "Two moderators elected by each site's community moderators for two-year terms, the head of moderation "
        "operations and the director of trust and safety. The chair is elected by the members each January.",
    ]),
    ("3. How work reaches the paid team", [
        "Every moderator flag goes to the paid moderation team. Every community review item (a close vote, a new "
        "account's first post, a post the platform scores as low quality, a suggested edit) goes first to the site's "
        "volunteer reviewers, and reaches the paid team when no volunteer has reviewed it 72 hours after it entered "
        "the site's review inbox.",
    ]),
    ("4. Need", [
        "A site's need for a year is the time the paid team will spend that year on the site's moderator flags and on "
        "the site's community review items that reach the team, each item priced at the handle-time standard the "
        "council has set for that year.",
        "A moderator flag counts when a paid moderator handles it. Flags the platform closes because the post was "
        "deleted before a moderator acted cost the team no time and do not count.",
        "An item counts in the year it entered the review inbox, and a flag in the year it was raised, both on UTC. "
        "The year's need includes the items and flags on posts and accounts that do not yet exist when the need is set.",
        "One FTE is 1,600 hours of need a year. Each site's need is stated in whole FTE, to the nearest whole FTE, and "
        "the council's request for the year is the sum of the nine site needs.",
    ]),
    ("5. The December sitting", [
        "The council votes its request for the next year at its December sitting and sends it to finance beside the "
        "envelope finance has set. The pool finance funds is divided among the sites in whole FTE in proportion to "
        "their needs.",
    ]),
    ("6. Standards", [
        "The council sets the handle-time standards for the next year at its June sitting, in minutes per item a paid "
        "moderator handles, and publishes them with the date they take effect.",
    ]),
]


def write_charter(path):
    st = styles("LibSerif", "LibSerif-Bold", COUNCIL, 10.3)
    s = [Paragraph("Millrind Moderation Council", st["h1"]),
         Paragraph("Charter, as amended at the March 2025 sitting (12 March 2025)", st["sub"])]
    for head, paras in CHARTER:
        s.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
    s.append(Spacer(1, 10))
    s.append(Paragraph(esc("Adopted by the members on 12 March 2025. Claudia Spence, Chair"), st["small"]))
    doc = _doc(path, "Moderation Council charter", K.PEOPLE["chair"])
    doc.build(s, onFirstPage=_footer("Millrind Moderation Council  |  Charter", "LibSerif"),
              onLaterPages=_footer("Millrind Moderation Council  |  Charter", "LibSerif"))


# ---------------------------------------------------------------------------------------------------- standards
F_STANDARDS = "handle_time_standards_2027.pdf"
STD_ROWS = [("Item handled by a paid moderator", "In force 1 January 2023 to 31 December 2026", "From 1 January 2027"),
            ("Moderator flag", "9.0", "9.0"),
            ("Close vote", "5.0", "2.0"),
            ("First post", "4.0", "4.0"),
            ("Low quality", "3.5", "3.5"),
            ("Suggested edit", "2.0", "2.0")]
STD_PARAS = [
    "Minutes per item. A standard prices an item the paid team handles; it is not a target for any moderator.",
    "Close vote: since August 2026 the review platform proposes the duplicate a question most likely repeats, with "
    "the matching answer, so a close item that reaches a paid moderator is now a confirmation in most cases. The "
    "council measured 214 close items handled with the proposal in the July pilot and set the 2027 standard at 2.0 "
    "minutes. Every other standard is unchanged.",
]


def write_standards(path):
    st = styles("LibSerif", "LibSerif-Bold", COUNCIL, 10.3)
    s = [Paragraph("Millrind Moderation Council", st["h1"]),
         Paragraph("Handle-time standards for 2027, set at the June sitting (17 June 2026)", st["sub"]),
         grid(STD_ROWS, [2.4, 2.25, 1.6], st)]
    s.append(Spacer(1, 8))
    for p in STD_PARAS:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph(esc("Claudia Spence, Chair, for the council"), st["small"]))
    doc = _doc(path, "Handle-time standards 2027", K.PEOPLE["chair"])
    doc.build(s, onFirstPage=_footer("Millrind Moderation Council  |  Standards 2027", "LibSerif"),
              onLaterPages=_footer("Millrind Moderation Council  |  Standards 2027", "LibSerif"))


# ---------------------------------------------------------------------------------------------------- envelope
F_ENVELOPE = "finance_envelope_2027_paid_moderation.pdf"
ENVELOPE_PARAS = [
    "Duane,",
    "The 2027 operating plan the leadership team approved on 29 September holds trust and safety's paid moderation "
    "at an envelope of %d FTE for the calendar year, against the %d FTE funded for 2026. The envelope is set at the "
    "network level; how it is divided among the sites stays with the council." % (K.ENVELOPE_2027, K.POOL_2026),
    "If the council's December request differs from the envelope, please send it with its figures by Friday 18 "
    "December, so the difference can go to the January plan review. The vendor rate for 2027 is unchanged.",
    "Thanks,",
]


def write_envelope(path):
    st = styles("Carlito", "Carlito-Bold", FIN, 10.6)
    s = [Paragraph("Millrind Finance", st["h1"]),
         Paragraph("30 September 2026  |  2027 envelope: paid moderation", st["sub"])]
    for p in ENVELOPE_PARAS:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph(esc("Natalie Maxwell, Finance Business Partner, Trust & Safety"), st["body"]))
    doc = _doc(path, "2027 envelope: paid moderation", K.PEOPLE["finance"])
    doc.build(s, onFirstPage=_footer("Millrind Finance"), onLaterPages=_footer("Millrind Finance"))


# ---------------------------------------------------------------------------------------------------- flag service
F_FLAGSTD = "flag_service_standard.pdf"
FLAGSTD_PARAS = [
    "Flag response is the moderation team's service measure to the sites: for each site and month, the share of the "
    "flags raised in the month, on UTC, that were answered within 24 hours.",
    "Flags the platform closed because the post was deleted before a moderator acted are left out of both counts.",
    "A flag is answered within 24 hours when a paid moderator's first action on it came within 24 hours of the flag "
    "being raised. A first action accepts the flag (and acts on the post) or declines it.",
    "The measure is reported to the council each quarter beside the sites' flag counts.",
]


def write_flagstd(path):
    st = styles("LibSans", "LibSans-Bold", COUNCIL, 10.0)
    s = [Paragraph("Moderation operations", st["h1"]),
         Paragraph("Flag service standard (revised 4 February 2026)", st["sub"])]
    for p in FLAGSTD_PARAS:
        s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph(esc("Duane Zamora, Head of Moderation Operations"), st["small"]))
    doc = _doc(path, "Flag service standard", K.PEOPLE["ops"])
    doc.build(s, onFirstPage=_footer("Millrind  |  Moderation operations"),
              onLaterPages=_footer("Millrind  |  Moderation operations"))


# ---------------------------------------------------------------------------------------------------- survey
F_SURVEY = "member_survey_2026_ai_assistants.pdf"
SURVEY_ROWS = [("Site", "Respondents", "Use an AI assistant for coding weekly", "Ask it before asking here",
                "Ask fewer questions here than in 2022"),
               ("Frontend & Web", "2,184", "81%", "74%", "63%"),
               ("Mobile Apps", "911", "79%", "70%", "59%"),
               ("Data & ML", "1,652", "84%", "66%", "47%"),
               ("Databases", "1,027", "71%", "58%", "41%"),
               ("Infrastructure & DevOps", "1,140", "73%", "57%", "39%"),
               ("Game Development", "498", "68%", "55%", "44%"),
               ("Security", "603", "62%", "44%", "26%"),
               ("Embedded & Hardware", "411", "57%", "39%", "21%"),
               ("Scientific Computing", "322", "61%", "41%", "19%")]
SURVEY_PARAS = [
    "Members who visited a site in April 2026 were invited at random; 8,748 completed the survey (a 6.1 per cent "
    "response). Figures are unweighted shares of respondents.",
    "Members who answer questions report the same pattern: 46 per cent of those who answered at least ten questions in "
    "2022 say they answer fewer now, most often because the questions they used to answer no longer arrive.",
]


def write_survey(path):
    st = styles("Carlito", "Carlito-Bold", COUNCIL, 10.2)
    s = [Paragraph("2026 member survey: AI assistants", st["h1"]),
         Paragraph("Community research, fieldwork 6 to 27 April 2026, published 2 June 2026", st["sub"])]
    s.append(Paragraph(esc(SURVEY_PARAS[0]), st["body"]))
    s.append(grid(SURVEY_ROWS, [1.55, 0.9, 1.35, 1.1, 1.4], st))
    s.append(Spacer(1, 8))
    s.append(Paragraph(esc(SURVEY_PARAS[1]), st["body"]))
    doc = _doc(path, "2026 member survey: AI assistants", "Community research")
    doc.build(s, onFirstPage=_footer("Millrind community research"), onLaterPages=_footer("Millrind community research"))


# ---------------------------------------------------------------------------------------------------- handbook
F_HANDBOOK = "moderation_operations_handbook_2026.pdf"
HANDBOOK = [
    ("The paid team", [
        "The paid team works three shift patterns on Toronto time: days from 08:00, lates from 15:30 and nights from "
        "23:00, each 8 paid hours with a 30-minute unpaid break. Part-time moderators work three shifts a week.",
        "Each moderator works one site's queues. Flags and routed review items reach the team through the moderation "
        "queue of the site they belong to.",
        "Statutory holidays observed in 2026 so far: 1 January, 16 February, 3 April, 18 May, 1 July, 3 August, "
        "7 September.",
    ]),
    ("Hours", [
        "The WFM system holds the shift lines. A line is approved by the moderator's lead the Monday after the shift, "
        "or on the day a correction is approved.",
        "When a week is corrected the WFM system re-sends the whole week: the original lines are kept, marked "
        "superseded, and the corrected lines come in approved. Only approved lines are hours worked.",
        "A shift's hours belong to the site the moderator worked for on that shift, and to the quarter in which the "
        "shift started, on Toronto time.",
    ]),
    ("Review access", [
        "Since 1 September 2026 review access on every site is given only by invitation of the site's elected "
        "moderators; members can no longer earn it with reputation. Invited reviewers appear on the reviewer roster "
        "like any other.",
    ]),
    ("Paid review hours", [
        "The council follows the paid team's review work as paid review hours: each moderator flag a paid moderator "
        "handled and each community item routed to the team, at the handle-time standard in force for its year "
        "(close votes at 5.0 minutes to the end of 2026, 2.0 from 2027), in the month the flag was raised or the item "
        "entered the inbox, on UTC. They are not the hours worked on the WFM lines.",
        "Months still to come are counted on the planning team's question plan, and October to December 2026 on its "
        "outlook.",
    ]),
]


def write_handbook(path):
    st = styles("LibSans", "LibSans-Bold", COUNCIL, 10.0)
    s = [Paragraph("Moderation operations handbook", st["h1"]),
         Paragraph("Team practice for the paid moderation team (revised 6 October 2026)", st["sub"])]
    for head, paras in HANDBOOK:
        s.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            s.append(Paragraph(esc(p), st["body"]))
    s.append(Paragraph(esc("Duane Zamora, Head of Moderation Operations"), st["small"]))
    doc = _doc(path, "Moderation operations handbook", K.PEOPLE["ops"])
    doc.build(s, onFirstPage=_footer("Millrind  |  Moderation operations"),
              onLaterPages=_footer("Millrind  |  Moderation operations"))


# ---------------------------------------------------------------------------------------------------- question counts
F_COUNTS = "question_count_standard_2024.pdf"
COUNTS = [
    "Questions are counted once each, in the month the question was first asked (UTC), on the site the question is on "
    "today.",
    "The posts warehouse replaced the old reporting jobs on 1 January 2024. For 2021 to 2023 the old review system's "
    "monthly queue workbook carries the question counts its statistics job reported.",
    "The old statistics job counted a question on every site it was posted to. A question moved to another site is "
    "posted there anew under a new question id, so the job counted it on its first site in the month it was asked and "
    "on its new site in the month it moved.",
    "Comparisons with 2021 to 2023 are made on the warehouse's basis.",
    "The planning team's question plan counts questions the way the warehouse does.",
    "Deleted questions are counted in the month they were asked.",
]


def write_counts(path):
    st = styles("Carlito", "Carlito-Bold", FIN, 10.4)
    s = [Paragraph("Question counts: the reporting basis", st["h1"]),
         Paragraph("Data platform team, issued with the posts warehouse (8 January 2024)", st["sub"])]
    for p in COUNTS:
        s.append(Paragraph(esc(p), st["body"]))
    doc = _doc(path, "Question counts: the reporting basis", "Data platform team")
    doc.build(s, onFirstPage=_footer("Millrind data platform"), onLaterPages=_footer("Millrind data platform"))


def write_all(out, n_rows):
    p = lambda f: os.path.join(out, f)
    write_charter(p(F_CHARTER))
    write_standards(p(F_STANDARDS))
    write_envelope(p(F_ENVELOPE))
    write_flagstd(p(F_FLAGSTD))
    write_survey(p(F_SURVEY))
    write_handbook(p(F_HANDBOOK))
    write_counts(p(F_COUNTS))
    stamps = {F_CHARTER: (b"D:20250312171400-04'00'", b"D:20250312171400-04'00'"),
              F_HANDBOOK: (b"D:20261006154000-04'00'", b"D:20261006154000-04'00'"),
              F_COUNTS: (b"D:20240108113000-05'00'", b"D:20240108113000-05'00'"),
              F_STANDARDS: (b"D:20260617193200-04'00'", b"D:20260617193200-04'00'"),
              F_ENVELOPE: (b"D:20260930141100-04'00'", b"D:20260930141100-04'00'"),
              F_FLAGSTD: (b"D:20260204103000-05'00'", b"D:20260204103000-05'00'"),
              F_SURVEY: (b"D:20260602120500-04'00'", b"D:20260602120500-04'00'")}
    for f, (c, m) in stamps.items():
        PP.normalize_pdf(p(f), c, m)
