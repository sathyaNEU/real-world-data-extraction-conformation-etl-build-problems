"""task271 documents: the society's catchable trout allocation policy (the tiers and what a lake's angler-hours are) and
the creel survey's 2026 field protocol (how the counts and the interviews are made). Neither describes a file or says
how anything is estimated; their text is kept here as data so checks.py can quote it."""
from __future__ import annotations

import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import cm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2421")
GREY = colors.HexColor("#5b625d")
GREEN = colors.HexColor("#2e5233")
BLUE = colors.HexColor("#24476b")
RULE = colors.HexColor("#a9b0aa")
HEAD = colors.HexColor("#e7ece8")


def styles(font, bold, accent, size=10.4):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=6),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15, leading=19, textColor=accent, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=9, leading=12, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.8, leading=14, textColor=accent, spaceBefore=7,
                          spaceAfter=3),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=9, leading=11.4, textColor=INK),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=9, leading=11.4, textColor=INK))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=2.4 * cm, rightMargin=2.4 * cm, topMargin=2.1 * cm,
                             bottomMargin=2.0 * cm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(2.2 * cm, 1.2 * cm, left)
        canvas.drawRightString(letter[0] - 2.2 * cm, 1.2 * cm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid(rows, widths, st):
    data = [[Paragraph(esc(str(c)), st["cellb"] if k == 0 else st["cell"]) for c in row] for k, row in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("TOPPADDING", (0, 0), (-1, -1), 2.6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z0-9(])", p)]


# ---------------------------------------------------------------------------------------------------- the policy
F_POLICY = "catchable_allocation_policy_2026.pdf"
POLICY = [
    ("1. Purpose", [
        "This policy sets how the Pelloran Plateau Fisheries Society shares the catchable rainbow trout raised at "
        "Quillet Creek Hatchery among the lakes it stocks. It applies to the lakes in the society's lake register "
        "that take catchables; lakes stocked only with fingerlings by air fall outside it.",
    ]),
    ("2. Tiers", [
        "2.1 Each stocked lake is placed in one of two tiers for each stocking year: high use or standard.",
        "2.2 A lake is in the high-use tier for a stocking year when anglers fished it for 500 or more angler-hours per "
        "hectare of its surface area in the open-water season before that year. Every other stocked lake is in the "
        "standard tier.",
        "2.3 A lake's angler-hours for a season are the number of anglers fishing it in each hour of the angling day, "
        "05:00 to 22:00, added up over every hour of every day of the open-water season, 15 May to 31 August. An angler "
        "fishing from a boat and an angler fishing from shore count the same.",
        "2.4 A lake's surface area is the area the lake register gives for it.",
        "2.5 Angler-hours are estimated from the society's creel survey of that season.",
    ]),
    ("3. Allocation by tier", [
        "3.1 A high-use lake receives 120 catchables per hectare in the stocking year, in two releases: one in May or "
        "June and one in July or August.",
        "3.2 A standard lake receives 45 catchables per hectare in the stocking year, in one spring release.",
        "3.3 Where the hatchery cannot meet every allocation, each lake's allocation is reduced in the same proportion.",
    ]),
    ("4. Timing and approval", [
        "4.1 The stocking program manager takes each lake's tier and the stocking plan for the coming year to the board "
        "at its November meeting.",
        "4.2 The society files its stocking application for the coming year, giving each lake's tier and allocation, "
        "with the Ministry by 1 December.",
    ]),
]


def write_policy(path):
    st = styles("Carlito", "Carlito-Bold", GREEN)
    s = [Paragraph("Pelloran Plateau Fisheries Society", st["h1"]),
         Paragraph("Catchable Trout Allocation Policy. Revision adopted by the board on 12 March 2026; replaces the "
                   "revision of 2 February 2023. Owner: stocking program manager.", st["sub"])]
    for head, paras in POLICY:
        s.append(Paragraph(esc(head), st["h2"]))
        for para in paras:
            s.append(Paragraph(esc(para), st["body"]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Revision history", st["h2"]))
    s.append(grid([["Revision", "Adopted", "Change"],
                   ["2019", "14 March 2019", "First allocation policy; tiers set on stocking requests"],
                   ["2023", "2 February 2023", "Tiers set on the creel survey's angler-hours per hectare"],
                   ["2026", "12 March 2026", "High-use line moved from 450 to 500 angler-hours per hectare; "
                                             "standard allocation raised from 40 to 45 per hectare"]],
                  [2.2, 3.4, 10.4], st))
    doc = _doc(path, "Catchable Trout Allocation Policy", K.PEOPLE["stocking"])
    f = _footer("Pelloran Plateau Fisheries Society  |  Catchable Trout Allocation Policy  |  2026 revision", "Carlito")
    doc.build(s, onFirstPage=f, onLaterPages=f)


# ---------------------------------------------------------------------------------------------------- the protocol
F_PROTOCOL = "creel_survey_protocol_2026.pdf"
PROTOCOL = [
    ("1. Survey period and survey days", [
        "The 2026 creel survey covers the open-water season, 15 May to 31 August, on every lake in the lake register.",
        "Survey days were drawn at random before the season: three weekdays and three weekend days in each month. "
        "Victoria Day (18 May), Canada Day (1 July) and BC Day (3 August) are taken as weekend days.",
    ]),
    ("2. Aerial counts", [
        "On each survey day Vellacott Air flies two count loops over the plateau with a society observer on board. "
        "The morning loop leaves the Pelloran Lake float base at 09:20 and the afternoon loop at 14:15. Each loop "
        "passes the lakes in the order of their Vellacott numbers, which the operator re-issued for the 2026 route.",
        "Over each lake the observer counts the boats with anglers in them and the anglers fishing from shore, and "
        "notes the time the aircraft was over the lake, in Pacific time. A loop that does not fly, or a lake that "
        "cannot be seen through cloud, fog or smoke, is entered with no count.",
    ]),
    ("3. Access interviews", [
        "On each interview day two clerks work one lake's main access: the early shift from 06:00 to 14:00 and the "
        "late shift from 14:00 to 22:00. They interview each angling party that leaves the lake by that access, once "
        "the party has finished fishing.",
        "For each party the clerk records the party size, whether it fished from a boat or from shore, the time it "
        "started fishing and the time it finished, the rainbow trout it kept and released, and how many of the kept "
        "fish had a clipped adipose fin. Where a party cannot give a start time the clerk records the hours it "
        "fished. The clerk also records the party's home postal area and licence type.",
        "Clerks are scheduled so that the lakes take turns for interview days, each lake having about the same number "
        "of weekday interview days and of weekend interview days over the season.",
    ]),
    ("4. Records", [
        "The observer keys the counts into the survey's count file after each loop. The clerks' tablets upload "
        "their interviews each evening; each interview is numbered by the clerk's initials, the date and the "
        "clerk's sequence that day. The creel survey coordinator exports the season's files after the season.",
    ]),
]


def write_protocol(path):
    st = styles("LibSans", "LibSans-Bold", BLUE, 9.8)
    s = [Paragraph("Pelloran Plateau Creel Survey 2026", st["h1"]),
         Paragraph("Field protocol. Issued 28 April 2026 by the creel survey coordinator, %s." % K.PEOPLE["creel"],
                   st["sub"])]
    for head, paras in PROTOCOL:
        s.append(Paragraph(esc(head), st["h2"]))
        for para in paras:
            s.append(Paragraph(esc(para), st["body"]))
    s.append(Spacer(1, 4))
    s.append(Paragraph("Contacts", st["h2"]))
    s.append(grid([["Role", "Name"],
                   ["Creel survey coordinator", K.PEOPLE["creel"]],
                   ["Stocking program manager", K.PEOPLE["stocking"]],
                   ["Hatchery manager", K.PEOPLE["hatchery"]],
                   ["Observers", ", ".join(K.OBSERVERS)]], [6.0, 10.0], st))
    doc = _doc(path, "Pelloran Plateau Creel Survey 2026 field protocol", K.PEOPLE["creel"])
    f = _footer("Pelloran Plateau Fisheries Society  |  Creel survey field protocol 2026", "LibSans")
    doc.build(s, onFirstPage=f, onLaterPages=f)


def all_sentences():
    return {F_POLICY: sentences([p for _, ps in POLICY for p in ps]),
            F_PROTOCOL: sentences([p for _, ps in PROTOCOL for p in ps])}


def write_all(out):
    p = lambda f: os.path.join(out, f)
    write_policy(p(F_POLICY))
    write_protocol(p(F_PROTOCOL))
    stamps = {F_POLICY: (b"D:20260312152200-07'00'", b"D:20260312152200-07'00'"),
              F_PROTOCOL: (b"D:20260428101400-07'00'", b"D:20260428101400-07'00'")}
    for f, (c, m) in stamps.items():
        PP.normalize_pdf(p(f), c, m)
    return {F_POLICY: 1, F_PROTOCOL: 1}
