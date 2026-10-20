"""The golden deliverables: the combined-cycle NOx inventory workbook and the designation memo to the Board (PDF with a
bar chart of every unit's 2026 ozone-season NOx rate against the target), and generator/figures.json."""
import io
import json
import math
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
import methods as M  # noqa: E402
import world as W    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ORANGE, BLUE, INK = colors.HexColor("#c8553d"), colors.HexColor("#4f7ca8"), colors.HexColor("#222222")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def half_up(v):
    return int(math.floor(v + .5))


def figures(target):
    rec = B.record(target)
    units = sorted(rec)
    rate = {u: M.rate(rec[u], "golden") for u in units}
    load_rate = {u: M.rate(rec[u], "load") for u in units}
    des = sorted(u for u in units if rate[u] >= W.TARGET)
    a, b = B.ask_a(target), B.ask_b(target)
    rows = {u: dict(mwh=half_up(sum(rec[u]["load"])), hours=len(rec[u]["load"]), designated=u in des,
                    fuel=half_up(a[u]), forced=int(b.get(u, 0)), plant=W.CC[u][0]) for u in units}
    gaps = dict(all=sum(v is None for u in units for v in rec[u]["nox"]),
                start=sum(v is None and 1 <= s <= 3 for u in units for v, s in zip(rec[u]["nox"], rec[u]["since"])))
    return dict(call=des, gaps=gaps, n_call=len(des), n_units=len(units), units=units, rows=rows,
                rate={u: round(rate[u], 4) for u in units}, load_route=sorted(u for u in units if load_rate[u] >= W.TARGET),
                target="%.3f" % W.TARGET, sections=DC.SECTIONS,
                asks=dict(fuel={u: rows[u]["fuel"] for u in units}, forced={u: rows[u]["forced"] for u in units},
                          fuel_total=sum(r["fuel"] for r in rows.values()),
                          forced_total=sum(r["forced"] for r in rows.values())))


def write_workbook(path, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Units"
    ws.append(["Combined-cycle units: 2026 ozone season (1 May to 30 September)"])
    ws.append([])
    hdr = ["Unit", "Facility", "Designated for SCR upgrade", "Fuel cost ($)", "Forced outage hours"]
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True)
    for u in f["units"]:
        r = f["rows"][u]
        ws.append([u, r["plant"], "Yes" if r["designated"] else "No", r["fuel"], r["forced"]])
    ws.append([])
    ws.append(["Designated: %s (%d of %d)." % (", ".join(f["call"]), f["n_call"], f["n_units"])])
    ws.append(["Prepared by %s, %s." % (W.PEOPLE["engineer"][0], W.MEMO_DATE)])
    for col, w in zip("ABCDE", (8, 16, 26, 14, 20)):
        ws.column_dimensions[col].width = w
    wb.save(path)


def chart(f):
    units = sorted(f["units"], key=lambda u: -f["rate"][u])
    w, h = 6.6 * inch, 3.2 * inch
    d = Drawing(w, h)
    left, bottom, top = .55 * inch, .5 * inch, .3 * inch
    hi = .30
    sy = lambda v: bottom + v / hi * (h - bottom - top)
    bw = (w - left - 10) / len(units)
    for v in (0, .05, .10, .15, .20, .25, .30):
        d.add(Line(left, sy(v), w - 6, sy(v), strokeColor=colors.HexColor("#e2e5e8"), strokeWidth=.5))
        d.add(String(left - 6, sy(v) - 3, "%.2f" % v, fontName="Helvetica", fontSize=7, textAnchor="end", fillColor=INK))
    for i, u in enumerate(units):
        v = f["rate"][u]
        x0 = left + i * bw + 4
        d.add(Rect(x0, bottom, bw - 8, sy(v) - bottom, fillColor=ORANGE if u in f["call"] else BLUE, strokeColor=None))
        d.add(String(x0 + (bw - 8) / 2, bottom - 11, u, fontName="Helvetica", fontSize=7, textAnchor="middle",
                     fillColor=INK))
    d.add(Line(left, sy(W.TARGET), w - 6, sy(W.TARGET), strokeColor=INK, strokeWidth=1, strokeDashArray=[3, 2]))
    d.add(String(w - 8, sy(W.TARGET) + 3, "Target, %.3f lb/MWh" % W.TARGET, fontName="Helvetica-Bold", fontSize=7,
                 textAnchor="end", fillColor=INK))
    d.add(String(left, h - 12, "2026 ozone-season NOx rate by unit (lb per gross MWh); designated units in orange",
                 fontName="Helvetica", fontSize=7.5, fillColor=INK))
    return d


def write_memo(path, f):
    body = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=7)
    hd = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=BLUE)
    small = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=.9 * inch, rightMargin=.9 * inch, topMargin=.8 * inch,
                            bottomMargin=.8 * inch, title="SCR Upgrade Program 2027 designations", author=W.COOP,
                            creator=W.COOP, producer=W.COOP, subject="SCR Upgrade Program")
    des = f["call"]
    names = ", ".join(des[:-1]) + " and " + des[-1]
    s = [Paragraph("SCR Upgrade Program: 2027 designations", hd),
         Paragraph("To: Board of Directors &nbsp;&nbsp; From: %s, %s &nbsp;&nbsp; Date: %s" % (
             W.PEOPLE["engineer"][0], W.PEOPLE["engineer"][1], W.MEMO_DATE), small), Spacer(1, 8),
         Paragraph("I recommend designating %s of our %s combined-cycle units for the 2027 SCR Upgrade Program: %s. "
                   "Each emitted %s lb of NOx per gross MWh or more over the 2026 ozone season." % (
                       WORDS[len(des)], WORDS[f["n_units"]], names, f["target"]), body),
         Paragraph("The analyzers were out for part of every unit's operating hours, and the outages are not spread "
                   "evenly: most fall in the first hours after a unit starts, when the catalyst is still cold and NOx "
                   "runs several times its steady level. I filled each hour without a measurement from the same unit's "
                   "measured hours at the same point after a start. A fill from each unit's NOx at the same load puts "
                   "steady-state NOx into those hours and would have left the units that cycle hardest under the "
                   "target.", body),
         chart(f), Spacer(1, 6)]
    t = [["Unit", "Facility", "Designated", "Fuel cost", "Forced outage hours"]]
    for u in f["units"]:
        r = f["rows"][u]
        t.append([u, r["plant"], "Yes" if r["designated"] else "No", "${:,}".format(r["fuel"]), str(r["forced"])])
    tb = Table(t, colWidths=[.7 * inch, 1.6 * inch, 1.0 * inch, 1.2 * inch, 1.4 * inch])
    tb.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8), ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                            ("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("ALIGN", (2, 0), (-1, -1), "RIGHT")]))
    s.append(tb)
    doc.build(s)


def build(gdir, x, target=None, figs=None):
    import postprocess as PP
    target = target or os.path.join(os.path.dirname(gdir), "target")
    figs = figs or os.path.join(HERE, "figures.json")
    os.makedirs(gdir, exist_ok=True)
    f = figures(target)
    json.dump(f, open(figs, "w", encoding="utf-8"), indent=1, sort_keys=True)
    write_workbook(os.path.join(gdir, W.GOLDEN["workbook"]), f)
    write_memo(os.path.join(gdir, W.GOLDEN["memo"]), f)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["engineer"][0], W.PEOPLE["engineer"][0],
                       "2026-11-06T15:12:00Z", "2026-11-09T14:02:00Z", excel=True, company=W.COOP)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["memo"]), b"D:20261109091415-06'00'", b"D:20261109091415-06'00'")
    return f
