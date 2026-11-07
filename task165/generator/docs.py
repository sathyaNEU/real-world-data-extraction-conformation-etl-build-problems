"""task165 documents: the winter maintenance plan, the road salt procurement procedure and the September dome
survey. Their text is kept here as data so checks.py and verify.py can quote it."""
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
import yards as Y           # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1e22")
GREY = colors.HexColor("#5c6470")
ACCENT = colors.HexColor("#1f4e79")
RULE = colors.HexColor("#b8c4cf")
HEAD = colors.HexColor("#e5ecf3")


def styles(font="LibSans", bold="LibSans-Bold", size=9.6):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.36, textColor=INK, spaceAfter=5),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15.0, leading=19.0, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.2, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.4, leading=13.4, textColor=ACCENT, spaceBefore=7,
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
    off = K.utc_offset_hours(dt.datetime.combine(d, dt.time(hh, mi)))
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


# ---------------------------------------------------------------------------------------------------- the plan
PLAN_DATE = dt.date(2026, 9, 18)


def plan_text(W):
    cc = sorted(W.contract_circuits)
    return [
    ("1. Scope", [
        "This plan sets how the Roads Division maintains the City's roads from 1 November 2026 to 31 March 2027. It "
        "replaces the 2025-26 plan. Winter operations run from the four works yards (Kelvin Road, Mapleford, Ridge "
        "and Lakeshore), each with its own salt dome and scale house, and from the Roads Operations Centre.",
    ]),
    ("2. Service levels", [
        "Priority 1: arterials, collectors carrying frequent transit service, hospital and ambulance access, and the "
        "hill streets and school bus routes the route audit designates. Plowed and salted to bare pavement after "
        "every event.",
        "Priority 2: other collectors. Salted at intersections, hills and curves during and after each event, once "
        "the Priority 1 roads are clear. Plowed when snow reaches 8 cm.",
        "Priority 3: local streets. Plowed when snow reaches 10 cm. Sand and salt on hills on request.",
        "Anti-icing brine is applied ahead of events on arterials and bridges only. Arterial tandems also pre-wet "
        "their rock salt at the spinner with plant brine at 40 litres to the tonne of salt (23 per cent salt by "
        "weight, 1.18 kg a litre); the single axles on the collector and local circuits spread dry salt.",
        "Spreader controllers are calibrated to the division's application rates, which are set in kilograms per "
        "lane-km for each material and pavement temperature range.",
    ]),
    ("3. Route audit", [
        "The route audit keeps each road segment's priority, yard and circuit in the winter route register and "
        "records every change in the revision log with its effective date. On 30 August 2026 the audit moved the "
        "collectors carrying Quellbrook Regional Transit's new frequent network to Priority 1. On 1 July 2026 the yard "
        "boundary was realigned and two Mapleford arterial circuits passed to Kelvin Road.",
    ]),
    ("4. Winter Severity Index", [
        "The Roads Operations Centre declares each winter event and scores it in event points when it stands the "
        "event down (procedure RO-OP-03). A season's Winter Severity Index (WSI) is the sum of the points of its "
        "events declared between 1 November and 31 March.",
        "Material planning uses the planning severity of 61.7 WSI points, the 1991 to 2020 average of the index "
        "rebuilt from the airport station's records, and plans each road's salt per WSI point.",
    ]),
    ("5. Materials", [
        "Roads are salted with bulk rock salt from the supply contract (material RS on the telematics platform, SALT on "
        "the old AVL). Priority 3 hills take a sand and salt mix made at the yards (SS, SAND/SALT).",
        "Each dome's stock is taken from its September survey and brought forward by the loads weighed in to it and "
        "out of it at the scale houses.",
        "Three arterial circuits (%s, %s and %s) are maintained under contract RW-2023-07; the contractor's trucks "
        "load at the City's domes and it reports its material monthly." % tuple(cc),
    ]),
    ]


def yard_table(W):
    rows = []
    for y in K.YARDS:
        art = sum(1 for rc, c in W.circuits.items() if c["kind"] == "ART" and
                  (W.realigned_codes.get(rc, rc)).startswith(y))
        col = sum(1 for rc, c in W.circuits.items() if c["kind"] in ("C", "S", "H") and c["yard"] == y)
        sc = "yes, replaced September 2026" if y == "LKS" else "yes"
        rows.append((K.YARD_NAMES[y].replace(" Yard", ""), y, str(art), str(col), sc))
    return rows


def write_plan(out, W):
    st = styles()
    path = os.path.join(out, "winter_maintenance_plan_2026-27.pdf")
    doc = _doc(path, "Winter maintenance plan 2026-27", K.PEOPLE["winter_manager"])
    flow = [Paragraph("Winter maintenance plan 2026-27", st["h1"]),
            Paragraph("%s, %s. Issued 18 September 2026. Owner: %s, manager, winter operations. Approved by %s, "
                      "director of roads." % (K.ORG, K.DEPT, K.PEOPLE["winter_manager"], K.PEOPLE["director"]),
                      st["sub"])]
    for head, paras in plan_text(W):
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    flow.append(Paragraph("6. Yards", st["h2"]))
    flow.append(_table(st, ["Yard", "Code", "Arterial circuits", "Collector and local circuits", "Scale house"],
                       yard_table(W), [30, 16, 30, 44, 50]))
    foot = "City of Quellbrook Roads Division: winter maintenance plan 2026-27"
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(PLAN_DATE, 14, 5), pdf_stamp(PLAN_DATE, 14, 5))
    return path


# ---------------------------------------------------------------------------------------------------- the procedure
PROC_DATE = dt.date(2025, 5, 12)
PROC = [
    ("1. Purpose", [
        "This procedure sets how Roads Operations buys bulk rock salt under the supply contract and commits the "
        "tonnage for each supply season.",
    ]),
    ("2. Supply season", [
        "The supply season runs from 1 October to 31 March. Deliveries are booked with the supplier's dispatch for "
        "each yard and weighed at the yard's scale house.",
    ]),
    ("3. Contract quantity", [
        "The contract quantity for a supply season rolls over on 1 October at the tonnage delivered in the season "
        "just closed.",
    ]),
    ("4. Seasonal tonnage", [
        "4.1 Salt needed above the contract quantity is committed with the supplier as seasonal tonnage by 1 October. "
        "Salt beyond the contract quantity and the seasonal tonnage is bought at the supplier's posted spot price.",
        "4.2 For each change in winter service approved since the last winter closed, Roads Operations commits the "
        "additional rock salt the roads the change moves will need from 1 November to 31 March, over what they needed "
        "before it, in a winter at the planning severity in the winter maintenance plan. Seasonal tonnage is "
        "committed in tonnes, rounded to the nearest 100 t.",
    ]),
    ("5. Approval", [
        "The manager, winter operations, prepares the commitment and reports it to Council, which approves spending "
        "above the contract quantity under the City's procurement by-law before the commitment goes "
        "to the supplier.",
    ]),
]


def write_procedure(out):
    st = styles()
    path = os.path.join(out, "road_salt_procurement_procedure_RO-PR-07.pdf")
    doc = _doc(path, "Road salt procurement, RO-PR-07", K.PEOPLE["director"])
    flow = [Paragraph("Road salt procurement", st["h1"]),
            Paragraph("Procedure RO-PR-07, revision 3. %s, %s. Approved 12 May 2025 by %s, director of roads."
                      % (K.ORG, K.DEPT, K.PEOPLE["director"]), st["sub"])]
    for head, paras in PROC:
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    flow.append(Spacer(1, 6))
    flow.append(Paragraph(esc("Revision 2 (March 2021) is withdrawn."), st["small"]))
    foot = "Roads Operations procedure RO-PR-07, revision 3"
    doc.build(flow, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    PP.normalize_pdf(path, pdf_stamp(PROC_DATE, 10, 40), pdf_stamp(PROC_DATE, 10, 40))
    return path


# ---------------------------------------------------------------------------------------------------- the survey
SURVEY_DATE = dt.date(2026, 9, 16)


def survey_rows():
    rows = []
    for y in K.YARDS:
        vol = Y.SURVEY_STOCK[y] / Y.BULK_DENSITY
        rows.append((K.YARD_NAMES[y], Y.SURVEY_DAY[y].strftime("%d %B %Y").lstrip("0"), "%s" % format(round(vol), ","),
                     "%.2f" % Y.BULK_DENSITY, "%s" % format(Y.SURVEY_STOCK[y], ",.1f")))
    return rows


def capture_rows():
    rows = []
    for i, y in enumerate(K.YARDS):
        (h0, m0), (h1, m1) = Y.CAPTURE[y]
        d = Y.SURVEY_DAY[y]
        a = K.to_utc(dt.datetime.combine(d, dt.time(h0, m0)))
        b = K.to_utc(dt.datetime.combine(d, dt.time(h1, m1)))
        rows.append(("TG-26-%03d" % (231 + i), K.YARD_NAMES[y], a.strftime("%Y-%m-%d %H:%M"), b.strftime("%H:%M"),
                     "%d" % (6 + i % 3), "%.3f" % (0.021 + 0.004 * i)))
    return rows


def write_survey(out):
    st = styles(font="Carlito", bold="Carlito-Bold", size=10.0)
    path = os.path.join(out, "dome_stock_survey_2026-09.pdf")
    doc = _doc(path, "Salt dome stock survey, September 2026", K.SURVEYOR)
    flow = [Paragraph("Salt dome stock survey", st["h1"]),
            Paragraph("Prepared for the %s, %s, by %s Report TG-2026-0917, issued 16 September 2026."
                      % (K.ORG, K.DEPT, K.SURVEYOR), st["sub"]),
            Paragraph("1. Results", st["h2"]),
            Paragraph(esc("Stockpile volumes were measured inside each dome by drone photogrammetry and converted to "
                          "tonnes at the bulk density agreed with the City for dry bulk rock salt."), st["body"]),
            _table(st, ["Yard", "Survey date", "Volume (m3)", "Density (t/m3)", "Stock (t)"], survey_rows(),
                   [40, 34, 28, 30, 30], right=(2, 3, 4)),
            Paragraph("2. Method", st["h2"]),
            Paragraph(esc("Each dome was flown once with the doors open and the loader parked outside. Ground control "
                          "points were surveyed by GNSS before each flight and the pile surface was triangulated "
                          "against the dome floor model from the 2024 baseline survey (the Lakeshore floor from the "
                          "January 2026 as-built). Volumes are reported to the nearest cubic metre."), st["body"]),
            Paragraph("Appendix A. Flight log", st["h2"]),
            _table(st, ["Flight", "Dome", "Capture start (UTC)", "Capture end (UTC)", "GCPs", "RMSE (m)"],
                   capture_rows(), [24, 34, 38, 30, 16, 20], right=(4, 5)),
            Spacer(1, 6),
            Paragraph(esc("%s, Kitchener, Ontario. Flight records and the point clouds are held on the City's project "
                          "site for seven years." % K.SURVEYOR), st["small"])]
    foot = "%s: report TG-2026-0917" % K.SURVEYOR
    doc.build(flow, onFirstPage=_footer(foot, "Carlito"), onLaterPages=_footer(foot, "Carlito"))
    PP.normalize_pdf(path, pdf_stamp(SURVEY_DATE, 15, 22), pdf_stamp(SURVEY_DATE, 15, 22))
    return path
