"""The golden deliverables: the city estimates workbook (each city's population and tier, and the housing authorized
in 2025) and the tier memo for the Joint Committee (PDF with a bar chart of every city's estimate against the line),
and generator/figures.json."""
import json
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.graphics.shapes import Drawing, Line, Rect, String                       # noqa: E402
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import letter                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import inch                                                    # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402
from openpyxl import Workbook                                                           # noqa: E402
from openpyxl.styles import Font                                                        # noqa: E402

import bundle as B   # noqa: E402
import docs as DC    # noqa: E402
import world as W    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ORANGE, BLUE, INK = colors.HexColor("#c8553d"), colors.HexColor("#4f7ca8"), colors.HexColor("#222222")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve"}


def figures(target):
    pop = B.population(target)
    cities = sorted(pop)
    up = B.tier(pop)
    au = B.authorized(target)
    return dict(call=up, n_call=len(up), n_cities=len(cities), cities=cities,
                pop={c: int(round(pop[c])) for c in cities}, line="{:,}".format(W.LINE), line_n=W.LINE,
                dates=dict(census_year=W.CENSUS.year, est_day=W.EST.day, est_year=W.EST.year),
                textbook_route=B.tier(B.population(target, "textbook")), sections=DC.SECTIONS,
                asks=dict(single={c: au[c][0] for c in cities}, multi={c: au[c][1] for c in cities}))


def write_workbook(path, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tiers"
    ws.append(["2027 revenue-sharing tiers: cities near the 50,000 line, population on 1 April 2026"])
    ws.append([])
    ws.append(["City", "Upper tier"])
    for c in ws[3]:
        c.font = Font(bold=True)
    for c in f["call"]:
        ws.append([c, "Yes"])
    ws.append([])
    ws.append(["Upper tier: %d of %d cities." % (f["n_call"], f["n_cities"])])
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 12
    au = wb.create_sheet("Housing authorized 2025")
    au.append(["Housing units authorized by building permits first issued in 2025"])
    au.append([])
    au.append(["City", "Single-family units", "Multifamily units"])
    for c in au[3]:
        c.font = Font(bold=True)
    for c in f["cities"]:
        au.append([c, f["asks"]["single"][c], f["asks"]["multi"][c]])
    for col, w in zip("ABC", (18, 20, 18)):
        au.column_dimensions[col].width = w
    au.append([])
    au.append(["Prepared by %s, %s." % (W.PEOPLE["analyst"][0], W.MEMO_DATE)])
    wb.save(path)


def chart(f):
    cs = sorted(f["cities"], key=lambda c: -f["pop"][c])
    w, h = 6.6 * inch, 3.3 * inch
    d = Drawing(w, h)
    left, bottom, top = .7 * inch, .75 * inch, .3 * inch
    lo, hi = 46000, 54000
    sy = lambda v: bottom + (v - lo) / (hi - lo) * (h - bottom - top)
    bw = (w - left - 10) / len(cs)
    for v in range(lo, hi + 1, 2000):
        d.add(Line(left, sy(v), w - 6, sy(v), strokeColor=colors.HexColor("#e2e5e8"), strokeWidth=.5))
        d.add(String(left - 6, sy(v) - 3, "{:,}".format(v), fontName="Helvetica", fontSize=7, textAnchor="end",
                     fillColor=INK))
    for i, c in enumerate(cs):
        x0 = left + i * bw + 3
        d.add(Rect(x0, bottom, bw - 6, sy(f["pop"][c]) - bottom, fillColor=ORANGE if c in f["call"] else BLUE,
                   strokeColor=None))
        from reportlab.graphics.shapes import Group
        d.add(Group(String(0, 0, c, fontName="Helvetica", fontSize=6, textAnchor="end", fillColor=INK),
                    transform=(0.82, 0.57, -0.57, 0.82, x0 + (bw - 6) / 2, bottom - 6)))
    d.add(Line(left, sy(W.LINE), w - 6, sy(W.LINE), strokeColor=INK, strokeWidth=1, strokeDashArray=[3, 2]))
    d.add(String(w - 8, sy(W.LINE) + 3, "Upper tier, %s residents" % f["line"], fontName="Helvetica-Bold", fontSize=7,
                 textAnchor="end", fillColor=INK))
    d.add(String(left, h - 12, "Population on 1 April 2026; upper-tier cities in orange", fontName="Helvetica",
                 fontSize=7.5, fillColor=INK))
    return d


def write_memo(path, f):
    body = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=7)
    hd = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=BLUE)
    small = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=.9 * inch, rightMargin=.9 * inch, topMargin=.8 * inch,
                            bottomMargin=.8 * inch, title="2027 revenue-sharing tiers", author=W.OFFICE,
                            creator=W.OFFICE, producer=W.OFFICE, subject="Revenue-sharing tiers")
    up = f["call"]
    names = " and ".join(up) if len(up) == 2 else ", ".join(up[:-1]) + " and " + up[-1]
    s = [Paragraph("2027 revenue-sharing tiers: cities near the line", hd),
         Paragraph("To: Joint Committee on Local Government Finance &nbsp;&nbsp; From: %s, %s &nbsp;&nbsp; Date: %s" % (
             W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][1], W.MEMO_DATE), small), Spacer(1, 8),
         Paragraph("Of the %s cities near the line, %s stand at %s residents or more on 1 April 2026 and move to the "
                   "upper tier for 2027: %s." % (WORDS[f["n_cities"]], WORDS[f["n_call"]], f["line"], names), body),
         Paragraph("Several cities have opened large apartment buildings since 2024. Those buildings fill over a year or "
                   "more after they open, so their units are counted at the occupancy the buildings in the utility's "
                   "service records reached at the same age, not at the city's overall occupancy rate. Counted at the "
                   "overall rate, %s would each pass the line on households still waiting to move in." % (
                       ", ".join([c for c in f["textbook_route"] if c not in up][:-1]) + " and " +
                       [c for c in f["textbook_route"] if c not in up][-1]), body),
         chart(f), Spacer(1, 8)]
    t = [["City", "Upper tier"]] + [[c, "Yes" if c in up else "No"] for c in f["cities"]]
    tb = Table(t, colWidths=[1.6 * inch, 1.0 * inch])
    tb.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8), ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                            ("LINEBELOW", (0, 0), (-1, 0), .6, INK)]))
    s.append(tb)
    doc.build(s)


def build(gdir, e, target=None, figs=None):
    import postprocess as PP
    target = target or os.path.join(os.path.dirname(gdir), "target")
    figs = figs or os.path.join(HERE, "figures.json")
    os.makedirs(gdir, exist_ok=True)
    for fn in os.listdir(gdir):
        if fn not in W.GOLDEN.values():
            os.remove(os.path.join(gdir, fn))
    f = figures(target)
    json.dump(f, open(figs, "w", encoding="utf-8"), indent=1, sort_keys=True)
    write_workbook(os.path.join(gdir, W.GOLDEN["workbook"]), f)
    write_memo(os.path.join(gdir, W.GOLDEN["memo"]), f)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][0],
                       "2026-10-21T15:12:00Z", "2026-10-23T14:02:00Z", excel=True, company=W.OFFICE)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["memo"]), b"D:20261023091415-04'00'", b"D:20261023091415-04'00'")
    return f
