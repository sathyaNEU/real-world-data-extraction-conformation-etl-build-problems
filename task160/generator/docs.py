"""task160 documents: the 2026-27 winter pool agreement, the surge plan register and the agencies' 2026-27 rate
schedule. Their text is kept here as data so checks.py and verify.py can quote it."""
from __future__ import annotations

import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import letter                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as C          # noqa: E402
import postprocess as PP    # noqa: E402
import world as W           # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSerif", "liberation/LiberationSerif-Regular.ttf"), ("LibSerif-Bold", "liberation/LiberationSerif-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1e24")
GREY = colors.HexColor("#5a616d")
ACCENT = colors.HexColor("#173f6b")
RULE = colors.HexColor("#b7c0cc")
HEAD = colors.HexColor("#e3e9f1")

F_AGREEMENT = "winter_pool_agreement_2026-27.pdf"
F_REGISTER = "surge_plan_register_2026-27.pdf"
F_RATES = "agency_rate_schedule_2026-27.pdf"

AGREEMENT_DATE = dt.date(2026, 9, 24)
REGISTER_DATE = dt.date(2026, 11, 2)
RATES_DATE = dt.date(2026, 10, 1)


def styles(font="Carlito", bold="Carlito-Bold", size=10.2):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.33, textColor=INK, spaceAfter=4.5),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=14.5, leading=18.0, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.8, leading=11.4, textColor=GREY, spaceAfter=9),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.8, leading=13.8, textColor=ACCENT, spaceBefore=6,
                          spaceAfter=2.5),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.3, leading=10.0, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=8.3, leading=10.0, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.3, leading=10.0, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=8.0, leading=10.2, textColor=GREY, spaceAfter=3))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=19 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="Carlito"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(22 * mm, 10 * mm, left)
        canvas.drawRightString(letter[0] - 22 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(st, head, rows, widths, right=()):
    data = [[Paragraph(esc(h), st["cellb"]) for h in head]]
    for r in rows:
        data.append([Paragraph(esc(str(x)), st["cellr"] if i in right else st["cell"]) for i, x in enumerate(r)])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.1), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.1),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2.6), ("RIGHTPADDING", (0, 0), (-1, -1), 2.6)]))
    return t


def pdf_stamp(d, hh=9, mi=0):
    off = W.us_eastern_offset(dt.datetime.combine(d, dt.time(hh, mi)))
    return ("D:%04d%02d%02d%02d%02d00%+03d'00'" % (d.year, d.month, d.day, hh, mi, off)).encode()


# ---------------------------------------------------------------------------------------------------- the agreement
AGREEMENT = [
    ("1. Definitions", [
        "1.1 The Pool season runs from 1 November 2026 to 31 March 2027.",
        "1.2 A Member is a hospital listed in Schedule A, from its Pool start date.",
        "1.3 A Member's surge unit is the unit its surge plan opens, as listed in the Association's surge plan register.",
        "1.4 A shift is one nurse for one scheduled shift, 07:00 to 19:00 or 19:00 to 07:00. Times in this agreement "
        "are Eastern Time.",
        "1.5 A Member's surge plan is active from the declaration of its activation to the declaration of its "
        "stand-down, as entered in the Association's capacity system at the 06:45 bed huddle or the 14:45 bed meeting.",
    ]),
    ("2. Supply and reporting", [
        "2.1 On a surge request from a Member the Agencies supply registered nurses for the Member's surge unit at the "
        "staffing in the surge plan register. Each Agency fills the slots Schedule A assigns it on each shift.",
        "2.2 Each Agency reports to the Association, each week, every shift its nurses work at a Member, whoever it "
        "bills for the shift.",
    ]),
    ("3. What the Pool funds", [
        "3.1 The Pool funds the agency RN shifts that staff a Member's surge unit and start while the Member's surge "
        "plan is active.",
        "3.2 Shifts on a Member's other units, and shifts on a surge unit that start while its plan is not active, are "
        "the Member's.",
    ]),
    ("4. Rates", [
        "4.1 The Agencies bill at the rates in their rate schedule for the season. Spot shifts are those outside the "
        "Block and those beyond an Agency's share of it.",
    ]),
    ("5. The January Block", [
        "5.1 The January Block covers every Member's surge unit for the four weeks from the first Monday in January: "
        "Monday 4 January to Sunday 31 January 2027.",
        "5.2 The Association files the Block with the Agencies by Tuesday 22 December 2026. The Block is set at the "
        "Pool's expected draw over the Block weeks, rounded to the nearest 50 shifts. The Pool's draw is the shifts the "
        "Pool funds under clause 3.1 that start in the Block weeks.",
        "5.3 The Block is divided between the Agencies in proportion to the surge unit slots Schedule A assigns each. "
        "An Agency's Block shifts left unused at the end of the Block weeks are charged at 60 per cent of its block "
        "rate.",
    ]),
    ("6. Billing and settlement", [
        "6.1 The Agencies bill the Pool for shifts booked against a Member's surge request and bill the Member for "
        "other shifts.",
        "6.2 The Association settles each Agency's billing monthly against the declarations in the capacity system. An "
        "agency shift billed to the Pool that the Pool does not fund is returned to the Member's account, and a shift "
        "the Pool funds that was billed to a Member is charged to the Pool.",
    ]),
    ("7. Term", [
        "7.1 This agreement governs the 2026-27 Pool season. It replaces the 2025-26 agreement, whose terms it repeats "
        "but for Schedule A.",
    ]),
]


def schedule_a(hs):
    rows = []
    for h in hs:
        start = "1 Nov 2026" if h["region"] == "NO" else "1 Nov 2021"
        prim = C.AG_C if h["agency"] == "C" else C.AG_I
        rows.append((h["name"], C.REGIONS[h["region"]], h["city"], start, prim))
    return rows


def write_agreement(out, hs):
    st = styles()
    path = os.path.join(out, F_AGREEMENT)
    doc = _doc(path, "Winter Surge Staffing Pool Agreement 2026-27", C.PEOPLE["pool_manager"])
    flow = [Paragraph("Winter Surge Staffing Pool Agreement 2026-27", st["h1"]),
            Paragraph("Between the %s, the Members listed in Schedule A, %s LLC and %s, Inc. Approved by the Pool "
                      "Members' meeting on 24 September 2026. Pool manager: %s." % (
                          C.ORG, C.AG_C, C.AG_I, C.PEOPLE["pool_manager"]), st["sub"])]
    for head, paras in AGREEMENT:
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    flow.append(Paragraph("Schedule A. Members", st["h2"]))
    flow.append(Paragraph(esc("Each surge unit slot on a shift is filled alternately by the Member's primary agency and "
                              "the other Agency, the primary agency taking the first."), st["small"]))
    flow.append(_table(st, ["Member", "Region", "City", "Pool start", "Primary agency"], schedule_a(hs),
                       [52, 30, 30, 22, 38]))
    foot = "TPHA Winter Surge Staffing Pool Agreement 2026-27"
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(AGREEMENT_DATE, 16, 10), pdf_stamp(AGREEMENT_DATE, 16, 10))


# ---------------------------------------------------------------------------------------------------- the register
REGISTER_INTRO = [
    "Every Member works to the Association's model surge plan (revision 3, March 2021). A Member declares Level 1 "
    "when its midnight census has been at or above 95 per cent of its staffed beds on two consecutive census nights, "
    "and Level 2 at or above 101 per cent; it steps down from Level 2 when the census falls below 98 per cent and "
    "stands down when it falls below 93 per cent. Declarations are made at the 06:45 bed huddle or the 14:45 bed "
    "meeting and entered in the capacity system.",
    "Agency staffing is the agency RN shifts a day the surge unit takes at each level, day and night shifts equal.",
]


HOLIDAYS = {dt.date(2021, 9, 6), dt.date(2021, 11, 25), dt.date(2021, 12, 24), dt.date(2022, 5, 30), dt.date(2022, 7, 4),
            dt.date(2022, 9, 5), dt.date(2022, 11, 24), dt.date(2023, 5, 29), dt.date(2023, 7, 4), dt.date(2023, 9, 4),
            dt.date(2023, 11, 23), dt.date(2024, 5, 27), dt.date(2024, 7, 4), dt.date(2024, 9, 2), dt.date(2024, 11, 28),
            dt.date(2025, 5, 26), dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2026, 9, 7)}


def _workday(r, a, b):
    """A working day drawn between a and b (Monday to Friday, the association's holidays out)."""
    while True:
        d = a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))
        if d.weekday() < 5 and d not in HOLIDAYS:
            return d


def plan_history(hs):
    """Each member's surge plan revisions as the pool office holds them: the plans of the founding members adopted in the
    weeks before the first pool season and revised since when a member re-planned its surge unit, the North's plans
    registered as each hospital joined in autumn 2026."""
    r = W.rng(80)
    out = {}
    for h in hs:
        if h["region"] == "NO":
            out[h["facility_id"]] = (1, _workday(r, dt.date(2026, 9, 8), dt.date(2026, 10, 23)))
            continue
        dates = [_workday(r, dt.date(2021, 9, 13), dt.date(2021, 10, 22))]
        for _ in range(int(r.choice([0, 0, 0, 1, 1, 1, 1, 2, 2, 3]))):
            dates.append(_workday(r, dt.date(2022, 3, 1), dt.date(2025, 10, 31)))
        out[h["facility_id"]] = (len(dates), max(dates))
    return out


def register_rows(hs):
    hist = plan_history(hs)
    rows = []
    for h in hs:
        rev, d = hist[h["facility_id"]]
        rows.append((h["name"], h["surge_unit"], h["grid"][0], h["grid"][1], rev, "%d %s" % (d.day, d.strftime("%b %Y"))))
    return rows


def write_register(out, hs):
    st = styles()
    path = os.path.join(out, F_REGISTER)
    doc = _doc(path, "Surge plan register 2026-27", C.PEOPLE["pool_manager"])
    flow = [Paragraph("Surge plan register 2026-27", st["h1"]),
            Paragraph("%s, Winter Surge Staffing Pool. Issued 2 November 2026." % C.ORG, st["sub"])]
    for p in REGISTER_INTRO:
        flow.append(Paragraph(esc(p), st["body"]))
    flow.append(_table(st, ["Member", "Surge unit", "Agency RN shifts a day, Level 1", "Agency RN shifts a day, Level 2",
                            "Plan rev.", "Revised"], register_rows(hs), [50, 33, 25, 25, 13, 22], right=(2, 3, 4)))
    foot = "TPHA surge plan register 2026-27"
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(REGISTER_DATE, 11, 30), pdf_stamp(REGISTER_DATE, 11, 30))


# ---------------------------------------------------------------------------------------------------- the rates
RATES = [
    (C.AG_C, "88.50", "112.00", "53.10"),
    (C.AG_I, "84.00", "107.50", "50.40"),
]


def write_rates(out):
    st = styles()
    path = os.path.join(out, F_RATES)
    doc = _doc(path, "Agency rate schedule 2026-27", "Shawn Whitaker")
    flow = [Paragraph("Agency rate schedule, Pool season 2026-27", st["h1"]),
            Paragraph("%s, Finance. Issued 1 October 2026 for the season 1 November 2026 to 31 March 2027." % C.ORG,
                      st["sub"]),
            Paragraph(esc("Hourly rates for registered nurses on Members' surge units, billed per 12-hour shift. Rates "
                          "include the Agencies' travel and lodging for nurses placed more than 60 miles from home."),
                      st["body"]),
            _table(st, ["Agency", "Block rate, per hour ($)", "Spot rate, per hour ($)", "Unused Block shift, per hour ($)"],
                   RATES, [50, 36, 36, 42], right=(1, 2, 3)),
            Spacer(1, 6),
            Paragraph(esc("A shift a Member cancels less than two hours before it starts is billed at four hours of the "
                          "applicable rate. Holiday premiums (Thanksgiving, Christmas Day, New Year's Day) add 50 per "
                          "cent."), st["body"])]
    foot = "TPHA Finance: agency rate schedule 2026-27"
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(RATES_DATE, 10, 40), pdf_stamp(RATES_DATE, 10, 40))
