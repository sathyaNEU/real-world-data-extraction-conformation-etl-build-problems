"""The pack's documents: Workforce Planning's relief crew placement standard, Workforce Systems' notes on the KWS
call-in module, People and Payroll's summary of casual employment under the 2024 enterprise agreement, and the
extract's transmittal. The text is held here as data so checks.py can quote it and execute every filed sentence."""
from __future__ import annotations

import os
import re

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1f2329")
GREY = colors.HexColor("#5f6670")
GREEN = colors.HexColor("#1f5c3a")      # Kellaway's green
RULE = colors.HexColor("#a9b0b8")
HEAD = colors.HexColor("#e5ebe7")


def styles(font, bold, size=9.8):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=4),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15, leading=19, textColor=GREEN, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.4, textColor=GREY, spaceAfter=8),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.6, leading=13.6, textColor=GREEN, spaceBefore=6,
                          spaceAfter=2),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.4, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.4, leading=10.4, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=7.9, leading=10.0, textColor=GREY, spaceAfter=3))


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=17 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(19 * mm, 9 * mm, left)
        canvas.drawRightString(A4[0] - 19 * mm, 9 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def grid(rows, widths, st):
    data = []
    for k, row in enumerate(rows):
        data.append([Paragraph(esc(str(c)), st["cellb"] if k == 0 else st["cell"]) for c in row])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE), ("LINEBELOW", (0, -1), (-1, -1), 0.4, RULE),
                           ("BACKGROUND", (0, 0), (-1, 0), HEAD), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 1.8), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.8)]))
    return t


def sentences(paras):
    return [s for p in paras for s in re.split(r"(?<=\.)\s+(?=[A-Z(])", p)]


# ---------------------------------------------------------------------------------------------------- the standard
STANDARD_HEAD = ("Relief crew placement standard",
                 "Workforce Planning standard WP-04, version 4, 9 October 2026. Owner: Beth Hill, Workforce Planning "
                 "Manager. Approved: Belinda Friedman, General Manager, Retail Operations.")
STANDARD = [
    ("1. Scope", [
        "This standard sets how Workforce Planning places the relief crew for the four trading weeks to Christmas "
        "Eve. It covers the eight stores: Ballarat, Sunshine, Camberwell, Altona, Williamstown, Box Hill, Werribee and "
        "Ringwood."]),
    ("2. The crew", [
        "The relief crew is 25 relief staff engaged on fixed-term contracts for the four trading weeks. Crew members "
        "are rostered under the hours limits the enterprise agreement sets for casuals and can be rostered for any "
        "shift a store's roster lists."]),
    ("3. Placement", [
        "The crew is placed at one store for all four weeks. It goes to the store where it will work the most hours "
        "that would otherwise go unworked."]),
    ("4. What is counted", [
        "The crew works every shift the store's published Christmas roster lists as open, that is a roster line with "
        "no employee on it. Those shifts are not posted to call-in.",
        "The hours that would otherwise go unworked are the paid hours of those open shifts that the store's "
        "call-ins would leave unfilled. They are forecast for each store as if the crew were placed at none, with "
        "every store's open shifts posted to call-in.",
        "Shifts vacated after the roster is published, for an absence or for leave, are posted to call-in as usual. "
        "They are not crew work and are not counted.",
        "Paid hours are as the enterprise agreement defines them."]),
    ("5. Crew hours", [
        "The crew hours reported with the placement are the paid hours of the open shifts in the placed store's "
        "published Christmas roster."]),
    ("6. Christmas 2026", [
        "Trading weeks: Friday 27 November to Thursday 24 December 2026. All stores are closed on Christmas Day.",
        "Christmas rosters published for all four weeks: Thursday 12 November 2026, 10:00.",
        "Placement confirmed by Workforce Planning: Friday 13 November 2026.",
        "Open shifts at the other seven stores post to call-in: Monday 16 November 2026, 09:00."]),
]

# ---------------------------------------------------------------------------------------------------- the module notes
NOTES_HEAD = ("KWS Call-in: how the module works",
              "Workforce Systems, version 2.3, 4 August 2026. Contact: Meredith Stevens, Workforce Systems Lead.")
NOTES = [
    ("Call-ins", [
        "A call-in puts one shift out to casuals through KWS. Store managers raise call-ins for shifts vacated after "
        "a roster is published: a reported absence, or leave approved after publication. A line a published roster "
        "leaves open is raised as a call-in when the roster is published; for Christmas rosters this waits until "
        "the relief crew is placed.",
        "Absences of permanent staff are covered inside the store's permanent team and are not raised as call-ins."]),
    ("Who is offered the shift", [
        "KWS offers a call-in to one casual at a time. It goes first to the store's own casuals in order of service "
        "date, longest first, then to casuals of the store's call-in cluster who have opted in to sister-store "
        "call-ins, in order of service date. The West cluster is Altona, Sunshine, Werribee and Williamstown; the "
        "East cluster is Box Hill, Camberwell and Ringwood. Ballarat is in no cluster.",
        "A casual is skipped if their availability profile does not cover the whole shift on that date, if they are "
        "rostered or booked at an overlapping time, if the shift would take their paid hours over 11 for the day or "
        "38 for the roster week, or if they would have less than 10 hours between finishing one day and starting the "
        "next. A casual who has reported an absence for a day is not offered call-ins on that day."]),
    ("When offers go out", [
        "Offers go out by SMS and the KWS app between 07:00 and 21:00 store time. Outside those hours an offer waits "
        "until 07:00, unless the shift starts within 12 hours.",
        "The casual has 60 minutes to respond, or 20 minutes if the shift starts within 24 hours."]),
    ("Responses", [
        "Accepting books the shift to the casual. A decline is final for that shift. If there is no response in time "
        "the offer moves to the next casual, and the casual stays on the list.",
        "When the list runs out with no acceptance, the shift is offered again from the top of the list at 07:00 the "
        "next day to every casual who has not declined it. Offering stops 15 minutes before the shift starts and the "
        "call-in closes unfilled."]),
    ("Times and records", [
        "KWS stores times in UTC. Shift dates and times on rosters, in the offer history report and in availability "
        "profiles are store time.",
        "Call-in register: callin_id; location_id; shift_start_utc and shift_end_utc; reason (OPN an open roster "
        "line, ABS an absence, LVE leave approved after publication); absent_payroll_no, the payroll number on the "
        "vacated line; raised_at; closed_at; outcome (FILLED or UNFILLED); filled_by, the KWS person code.",
        "Offer history: offer_id; callin_id; location_id; shift_date, shift_start and shift_end; person_code; "
        "offered_at; response (ACCEPTED, DECLINED or NO RESPONSE); responded_at.",
        "People: person_code; payroll_no; home_location; cluster_callins (Y if opted in to sister-store call-ins); "
        "service_date; status.",
        "Rosters for roster weeks from Friday 27 February 2026 are built in KWS. Earlier rosters were built in the "
        "stores' legacy rostering tool and imported; its export gives Hrs as the length of the shift from start to "
        "finish."]),
]

# ---------------------------------------------------------------------------------------------------- the EA summary
EA_HEAD = ("Kellaway's Retail Enterprise Agreement 2024: casual employment",
           "People and Payroll summary for managers, 1 July 2026 (rates from the first full pay period on or after 1 "
           "July 2026). Contact: Kristina Patel, Payroll and HR Systems.")
EA = [
    ("Casual employment", [
        "Casual employees are paid a 25 per cent casual loading in place of paid leave. The minimum engagement is "
        "three hours.",
        "A casual may decline any shift offered outside their rostered hours."]),
    ("Hours", [
        "A casual may work no more than 11 paid hours in a day; two shifts may be worked on one day within that "
        "limit. A casual may work no more than 38 paid hours in a roster week, Friday to Thursday.",
        "There must be at least 10 hours between the end of one day's work and the start of the next day's."]),
    ("Breaks", [
        "A shift of more than five hours includes an unpaid meal break of 30 minutes. Paid hours are the length of "
        "the shift less any unpaid meal break.",
        "A paid rest break of 10 minutes is taken in each four hours worked."]),
]
EA_RATES = [["Time worked", "Casual rate (per cent of base, loading included)"],
            ["Monday to Friday, before 18:00", "125"], ["Monday to Friday, 18:00 to midnight", "137.5"],
            ["Saturday", "150"], ["Sunday", "175"], ["Public holiday", "275"]]
EA_JUNIOR = [["Age", "Per cent of adult rate"], ["Under 16", "50"], ["16", "60"], ["17", "70"], ["18", "80"],
             ["19", "90"], ["20 and over", "100"]]


def write_pdf(path, head, sections, footer, author, tables=(), font="Carlito", bold="Carlito-Bold"):
    st = styles(font, bold)
    doc = _doc(path, head[0], author)
    story = [Paragraph(esc(head[0]), st["h1"]), Paragraph(esc(head[1]), st["sub"])]
    for title, paras in sections:
        story.append(Paragraph(esc(title), st["h2"]))
        for p in paras:
            story.append(Paragraph(esc(p), st["body"]))
    for title, rows, widths in tables:
        story.append(Paragraph(esc(title), st["h2"]))
        story.append(grid(rows, widths, st))
        story.append(Spacer(1, 4))
    doc.build(story, onFirstPage=_footer(footer, font), onLaterPages=_footer(footer, font))


def transmittal(counts):
    lines = [
        "Kellaway's Workforce Systems",
        "Data extract WR-26-1187",
        "Requested by: Workforce Planning (B. Hill), 10/11/2026",
        "Extracted: 12/11/2026 18:40 by M. Stevens; payroll casual register extracted by Payroll (K. Patel) 12/11/2026",
        "Scope: call-ins and offers for shifts dated 29/08/2025 to 12/11/2026; rosters as published for the same dates;",
        "the Christmas 2026 rosters as published 12/11/2026; KWS people and availability profiles as at extraction.",
        "",
        "File                                              Rows      Source",
    ]
    src = {K.F_REGISTER: "KWS call-in register", K.F_OFFERS: "KWS offer history report",
           K.F_LEGACY: "legacy rostering tool export", K.F_KWS: "KWS roster lines", K.F_XMAS: "KWS roster report",
           K.F_PEOPLE: "KWS people", K.F_AVAIL: "KWS availability profiles", K.F_PAYROLL: "payroll",
           K.F_STORES: "store list", K.F_CAL: "Store Operations calendar", K.F_PLAN: "Store Operations"}
    for f in [K.F_REGISTER, K.F_OFFERS, K.F_LEGACY, K.F_KWS, K.F_XMAS, K.F_PEOPLE, K.F_AVAIL, K.F_PAYROLL, K.F_STORES,
              K.F_CAL, K.F_PLAN]:
        lines.append("%-48s %8s  %s" % (f, "{:,}".format(counts[f]) if f in counts else "", src[f]))
    lines += [
        "%-48s %8s  %s" % (K.F_STANDARD, "", "Workforce Planning"),
        "%-48s %8s  %s" % (K.F_NOTES, "", "Workforce Systems"),
        "%-48s %8s  %s" % (K.F_EA, "", "People and Payroll"),
        "",
        "Rows: data rows, header excluded. The Christmas workbook's rows are its roster lines across the eight sheets;",
        "the availability file's are people.",
        "KWS timestamps are UTC. Roster weeks run Friday to Thursday.",
        "Rosters before the roster week of 27/02/2026 come from the legacy rostering tool's weekly export.",
    ]
    return "\r\n".join(lines) + "\r\n"


PDF_STAMPS = {
    K.F_STANDARD: (b"D:20261009103211+11'00'", b"D:20261009103211+11'00'"),
    K.F_NOTES: (b"D:20260804144002+10'00'", b"D:20260804144002+10'00'"),
    K.F_EA: (b"D:20260701091530+10'00'", b"D:20260701091530+10'00'"),
}


def write_all(out, Wd, counts):
    write_pdf(os.path.join(out, K.F_STANDARD), STANDARD_HEAD, STANDARD, "Kellaway's Workforce Planning  WP-04 v4",
              "Beth Hill")
    write_pdf(os.path.join(out, K.F_NOTES), NOTES_HEAD, NOTES, "Kellaway's Workforce Systems  KWS Call-in v2.3",
              "Meredith Stevens", font="LibSans", bold="LibSans-Bold")
    write_pdf(os.path.join(out, K.F_EA), EA_HEAD, EA, "Kellaway's People and Payroll  EA 2024 casual summary",
              "Kristina Patel", tables=[("Casual rates", EA_RATES, [92, 70]), ("Junior rates", EA_JUNIOR, [92, 70])])
    for f, (c0, c1) in PDF_STAMPS.items():
        PP.normalize_pdf(os.path.join(out, f), c0, c1)
    with open(os.path.join(out, K.F_TRANSMIT), "w", encoding="utf-8", newline="") as fh:
        fh.write(transmittal(counts))
