"""task159 documents: the platform crowding standard, the autumn 2026 and spring 2027 service plans and the station
planning manual's vertical circulation chapter. Their text is kept here as data so checks.py can quote it."""
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

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402
import records as R         # noqa: E402
import world as W           # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1a1d21")
GREY = colors.HexColor("#5b6370")
ACCENT = colors.HexColor("#00543c")
RULE = colors.HexColor("#b9c2bd")
HEAD = colors.HexColor("#e4ece8")

F_STANDARD = "platform_crowding_standard_rev4.pdf"
F_PLAN_AUT = "service_plan_autumn_2026.pdf"
F_PLAN_SPR = "service_plan_spring_2027.pdf"
F_MANUAL = "station_planning_manual_ch5.pdf"


def styles(font="LibSans", bold="LibSans-Bold", size=9.8):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=5),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15.0, leading=19.0, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.6, leading=13.6, textColor=ACCENT, spaceBefore=7,
                          spaceAfter=3),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.2, leading=10.0, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=8.2, leading=10.0, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.2, leading=10.0, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=7.9, leading=10.0, textColor=GREY, spaceAfter=3))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=21 * mm, rightMargin=21 * mm, topMargin=19 * mm,
                             bottomMargin=18 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="LibSans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(21 * mm, 10 * mm, left)
        canvas.drawRightString(letter[0] - 21 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_stamp(d, hh=9, mi=0):
    off = K.us_eastern_offset(d, hh)
    return ("D:%04d%02d%02d%02d%02d00-%02d'00'" % (d.year, d.month, d.day, hh, mi, off)).encode()


def _table(st, head, rows, widths, right=()):
    data = [[Paragraph(esc(h), st["cellb"]) for h in head]]
    for r in rows:
        data.append([Paragraph(esc(str(x)), st["cellr"] if i in right else st["cell"]) for i, x in enumerate(r)])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2.6), ("RIGHTPADDING", (0, 0), (-1, -1), 2.6)]))
    return t


# ---------------------------------------------------------------------------------------------------- the standard
STANDARD_DATE = dt.date(2026, 8, 24)
STANDARD = [
    ("1. Purpose", [
        "This standard sets where Rail Operations posts platform conductors on weekday mornings. A platform conductor "
        "manages the platform while trains are boarding: spreading waiting customers along the platform, keeping the "
        "platform edge and the foot of the stairs clear, and holding customers at the stairs when the platform is full.",
    ]),
    ("2. Watch list", [
        "The standard applies to the platforms in the schedule. Revision 4 adds three Sallow Park platforms, counted "
        "at the request of the Sallow Park station manager in August 2026 after the Larch Hill and Tamsin Avenue "
        "housing opened.",
    ]),
    ("3. Accumulation", [
        "A platform's accumulation is the number of people on the platform as a train arrives, before its doors open. "
        "On an island platform it is everyone on the island, whichever train they are waiting for.",
        "A platform's morning peak is the highest mean accumulation over the trains arriving in a quarter-hour, among "
        "the quarter-hours starting at 07:00, 07:15 and so on to 09:30, local time.",
    ]),
    ("4. Posting", [
        "For each roster pick the station planning desk forecasts the morning peak of every platform in the schedule "
        "for an average Monday, Tuesday, Wednesday, Thursday and Friday of the pick. Every weekday on which the weekday "
        "timetable runs is a weekday of the pick.",
        "A conductor is posted on a platform on each weekday whose forecast morning peak is more than 85 per cent of "
        "the platform's rated capacity in the platform capacity register on the first day of the pick. One posting is "
        "one weekday-morning shift a week, 06:45 to 10:00, for the length of the pick. The pick notice gives the "
        "number of shifts a week.",
    ]),
    ("5. Rated capacity", [
        "A platform's rated capacity is the number of people it holds at one square metre each over its usable area: "
        "the platform less a 0.6 metre strip at each platform edge, the stair and escalator openings and fixed "
        "obstructions. Ratings are kept in the platform capacity register.",
    ]),
    ("6. Counts", [
        "Each autumn the count programme counts every platform in the schedule on two mornings from Tuesday to "
        "Thursday. On a Monday and a Friday it also counts the hybrid-day sample: in each complex in the schedule the "
        "year before, the platform with the highest accumulation in that year's counts.",
    ]),
]


def standard_schedule():
    rows = []
    for key, code, cap in W.WATCH:
        st, rest = key.split("|")
        rows.append((code, st, W._plat_label(key)))
    return rows


def write_standard(out):
    st = styles()
    path = os.path.join(out, F_STANDARD)
    doc = _doc(path, "Platform crowding standard", K.PEOPLE["planning_manager"])
    flow = [Paragraph("Platform crowding standard", st["h1"]),
            Paragraph("Revision 4. Station Planning, Rail Operations, %s. Issued 24 August 2026; in force from the "
                      "autumn 2026 pick (8 September 2026). Owner: %s, station planning manager."
                      % (K.ORG, K.PEOPLE["planning_manager"]), st["sub"])]
    for head, paras in STANDARD:
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    flow.append(Paragraph("Schedule. Platforms under the standard", st["h2"]))
    flow.append(_table(st, ["Code", "Complex", "Platform"], standard_schedule(), [22, 44, 70]))
    flow.append(Spacer(1, 6))
    flow.append(Paragraph(esc("Revision 3 (June 2025) is withdrawn. Questions to Station Planning."), st["small"]))
    foot = "VTC Rail Operations: platform crowding standard, revision 4"
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(STANDARD_DATE, 15, 12), pdf_stamp(STANDARD_DATE, 15, 12))


# ---------------------------------------------------------------------------------------------------- service plans
PERIODS = [("Early", "05:00-06:30"), ("AM peak", "06:30-09:30"), ("Shoulder", "09:30-10:30"),
           ("Midday", "10:30-15:30"), ("PM peak", "15:30-18:30"), ("Evening", "18:30-21:00"), ("Late", "21:00-01:00")]
_PMIN = [5 * 60, 6 * 60 + 30, 9 * 60 + 30, 10 * 60 + 30, 15 * 60 + 30, 18 * 60 + 30, 21 * 60]


def headway_table(plan):
    rows = []
    for l in ("1", "2", "3", "4", "5", "6"):
        hw = []
        for m in _PMIN:
            h = R.tt_headway(l, m, plan)
            hw.append(("%.1f" % h).rstrip("0").rstrip("."))
        rows.append(["Line %s" % l] + hw + [str(W.CARS[plan][l])])
    return rows


PLAN_TEXT = {
    "autumn2026": dict(
        title="Service plan, autumn 2026 pick", date=dt.date(2026, 7, 20),
        pick="The autumn 2026 pick runs from Tuesday 8 September to Friday 18 December 2026.",
        notes=[
            "The holiday timetable runs on Thanksgiving, Thursday 26 November, and on Friday 27 November. Columbus Day "
            "(12 October) and Veterans Day (11 November) run the weekday timetable.",
            "Line 5 continues to run six-car trains while the M26 cars are delivered and accepted.",
            "Ferrier Square: stair S5 to the Line 4 southbound platform closes for rebuilding from 14 September.",
        ]),
    "spring2027": dict(
        title="Service plan, spring 2027 pick", date=dt.date(2026, 12, 14),
        pick="The spring 2027 pick runs from Monday 1 March to Friday 25 June 2027.",
        notes=[
            "Line 5 runs eight-car trains in all service from 1 March, the M26 cars running with the M04 fleet. Line 5 "
            "platforms were built for eight cars and need no work.",
            "The holiday timetable runs on Memorial Day, Monday 31 May. Juneteenth is observed on Friday 18 June and "
            "runs the weekday timetable.",
            "Headways are unchanged from the autumn 2026 and winter 2026-27 plans on every line.",
        ]),
}


def write_plan(out, plan):
    T = PLAN_TEXT[plan]
    st = styles()
    f = F_PLAN_AUT if plan == "autumn2026" else F_PLAN_SPR
    path = os.path.join(out, f)
    doc = _doc(path, T["title"], K.PEOPLE["service_planner"])
    flow = [Paragraph(T["title"], st["h1"]),
            Paragraph("Service Planning, %s. Issued %s. Prepared by %s." % (
                K.ORG, T["date"].strftime("%-d %B %Y"), K.PEOPLE["service_planner"]), st["sub"]),
            Paragraph(esc(T["pick"]), st["body"]),
            Paragraph("Weekday service", st["h2"]),
            Paragraph(esc("Minutes between trains from each line's origin terminal, by period of departure, and cars "
                          "per train."), st["body"])]
    head = ["Line"] + ["%s %s" % p for p in PERIODS] + ["Cars"]
    flow.append(_table(st, head, headway_table(plan), [16, 17, 18, 18, 18, 18, 18, 17, 12],
                       right=tuple(range(1, 9))))
    flow.append(Spacer(1, 5))
    flow.append(Paragraph(esc("Origins: Line 1 Kettle Creek and Harbor Terminal; Line 2 Westmere and Shore Road; Line 3 "
                              "Northgate and Medical Center; Line 4 Arbor Mills and Wharf Street; Line 5 Ossory and "
                              "Bayfront; Line 6 Foundry Row and Harbor Terminal. Trip-level times are in the weekday "
                              "timetable."), st["small"]))
    flow.append(Paragraph("Notes", st["h2"]))
    for n in T["notes"]:
        flow.append(Paragraph(esc(n), st["body"]))
    foot = "VTC Service Planning: " + T["title"].lower()
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(T["date"], 11, 5), pdf_stamp(T["date"], 16, 40))


# ---------------------------------------------------------------------------------------------------- the manual
MANUAL_DATE = dt.date(2025, 11, 3)
MANUAL = [
    ("5.1 Scope", [
        "This chapter gives the flows Station Planning uses for stairs, escalators and elevators between platforms, "
        "mezzanines and the street.",
    ]),
    ("5.2 Stairs", [
        "A fixed stair carries 45 people a minute for each metre of clear width between handrails in the main direction "
        "of flow, and 35 when the flow runs both ways in similar numbers.",
    ]),
    ("5.3 Escalators", [
        "An escalator's rated flow depends on its step width: 40 people a minute for a 600 mm step, 60 for an 800 mm "
        "step and 80 for a 1,000 mm step at 0.5 metres a second, and in proportion to its speed at other speeds. An "
        "escalator carries its rated flow in the direction it is set to run.",
    ]),
    ("5.4 Elevators", [
        "An elevator is out of service whenever it is not in normal passenger service: from the moment it stops or is "
        "taken out of service to the moment it is back in normal passenger service.",
    ]),
]


def write_manual(out):
    st = styles()
    path = os.path.join(out, F_MANUAL)
    doc = _doc(path, "Station planning manual, chapter 5", K.PEOPLE["planning_manager"])
    flow = [Paragraph("Station planning manual", st["h1"]),
            Paragraph("Chapter 5. Vertical circulation. Station Planning, %s. Revised 3 November 2025." % K.ORG,
                      st["sub"])]
    for head, paras in MANUAL:
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    foot = "VTC station planning manual, chapter 5 (vertical circulation)"
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(MANUAL_DATE, 10, 20), pdf_stamp(MANUAL_DATE, 10, 20))


def write_all(out):
    write_standard(out)
    write_plan(out, "autumn2026")
    write_plan(out, "spring2027")
    write_manual(out)
