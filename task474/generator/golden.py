"""The golden deliverables: the air-corridor workbook (each link's designation and the terminal operations figures)
and the designation memo for the Board (PDF with a bar chart of every link's NOx per mile against the program's
line), and generator/figures.json."""
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
import methods as M  # noqa: E402
import world as W    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ORANGE, BLUE, INK = colors.HexColor("#c8553d"), colors.HexColor("#4f7ca8"), colors.HexColor("#222222")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen"}
QNAME = {1: "Oct-Dec 2025", 2: "Jan-Mar 2026", 3: "Apr-Jun 2026", 4: "Jul-Sep 2026"}


def figures(target):
    rate = B.nox(target)
    links = sorted(rate)
    des = M.designated(rate)
    ga = B.gate_asks(target)
    key = lambda k: "%s Q%d" % k
    return dict(call=des, n_call=len(des), n_links=len(links), links=links, names={k: W.LINKS[k][0] for k in links},
                rate={k: round(rate[k], 2) for k in links}, line="%.2f" % W.LINE, days=len(W.DAYS),
                textbook_route=M.designated(B.nox(target, "textbook")), sections=DC.SECTIONS,
                terminals={t: W.TERMINALS[t][0] for t in W.TERMINALS}, quarters=QNAME,
                asks=dict(visits={key(k): v[0] for k, v in ga.items()},
                          turn={key(k): round(v[1], 1) for k, v in ga.items()}))


def write_workbook(path, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Links"
    ws.append(["Air Corridor Program 2027: roadway link designations (program year October 2025 to September 2026)"])
    ws.append([])
    ws.append(["Link ID", "Link", "Designated"])
    for c in ws[3]:
        c.font = Font(bold=True)
    for k in f["links"]:
        ws.append([k, f["names"][k], "Yes" if k in f["call"] else "No"])
    ws.append([])
    ws.append(["Designated: %d of %d links." % (f["n_call"], f["n_links"])])
    ws.column_dimensions["A"].width = 9
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 12
    tg = wb.create_sheet("Terminal gates")
    tg.append(["Truck visits by terminal and quarter, program year October 2025 to September 2026"])
    tg.append([])
    tg.append(["Terminal", "Quarter", "Truck visits", "Average turn time (min)"])
    for c in tg[3]:
        c.font = Font(bold=True)
    for t in sorted(f["terminals"]):
        for q in range(1, 5):
            k = "%s Q%d" % (t, q)
            tg.append([f["terminals"][t], f["quarters"][q], f["asks"]["visits"][k], f["asks"]["turn"][k]])
    for col, w in zip("ABCD", (40, 14, 13, 22)):
        tg.column_dimensions[col].width = w
    tg.append([])
    tg.append(["Prepared by %s, %s." % (W.PEOPLE["analyst"][0], W.MEMO_DATE)])
    wb.save(path)


def chart(f):
    ks = sorted(f["links"], key=lambda k: -f["rate"][k])
    w, h = 6.6 * inch, 3.2 * inch
    d = Drawing(w, h)
    left, bottom, top = .6 * inch, .5 * inch, .3 * inch
    lo, hi = 0.0, 7.0
    sy = lambda v: bottom + (v - lo) / (hi - lo) * (h - bottom - top)
    bw = (w - left - 10) / len(ks)
    for v in range(0, 8):
        d.add(Line(left, sy(v), w - 6, sy(v), strokeColor=colors.HexColor("#e2e5e8"), strokeWidth=.5))
        d.add(String(left - 6, sy(v) - 3, "%d" % v, fontName="Helvetica", fontSize=7, textAnchor="end", fillColor=INK))
    for i, k in enumerate(ks):
        x0 = left + i * bw + 3
        d.add(Rect(x0, bottom, bw - 6, sy(f["rate"][k]) - bottom, fillColor=ORANGE if k in f["call"] else BLUE,
                   strokeColor=None))
        d.add(String(x0 + (bw - 6) / 2, bottom - 11, k, fontName="Helvetica", fontSize=7, textAnchor="middle",
                     fillColor=INK))
    d.add(Line(left, sy(W.LINE), w - 6, sy(W.LINE), strokeColor=INK, strokeWidth=1, strokeDashArray=[3, 2]))
    d.add(String(w - 8, sy(W.LINE) + 3, "Program line, %.2f t per mile" % W.LINE, fontName="Helvetica-Bold",
                 fontSize=7, textAnchor="end", fillColor=INK))
    d.add(String(left, h - 12, "On-road NOx, tonnes per mile, October 2025 to September 2026; designated links in "
                 "orange", fontName="Helvetica", fontSize=7.5, fillColor=INK))
    return d


def write_memo(path, f):
    body = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=7)
    hd = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=BLUE)
    small = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=.9 * inch, rightMargin=.9 * inch, topMargin=.8 * inch,
                            bottomMargin=.8 * inch, title="Air Corridor Program 2027 designations", author=W.PORT,
                            creator=W.PORT, producer=W.PORT, subject="Air Corridor Program")
    des = f["call"]
    names = ", ".join(des[:-1]) + " and " + des[-1]
    s = [Paragraph("Air Corridor Program: 2027 link designations", hd),
         Paragraph("To: Board of Commissioners &nbsp;&nbsp; From: %s, %s &nbsp;&nbsp; Date: %s" % (
             W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][1], W.MEMO_DATE), small), Spacer(1, 8),
         Paragraph("I recommend designating %s of the %s port roadway links for the 2027 Air Corridor Program: %s. "
                   "Each carried %s tonnes of NOx per mile or more from on-road vehicles between October 2025 and "
                   "September 2026." % (WORDS[len(des)], WORDS[f["n_links"]], names, f["line"]), body),
         Paragraph("Each link was counted for two weekdays, and the year's traffic is built from those counts with the "
                   "state's continuous count stations. Trucks, which carry most of the NOx, run well above their "
                   "annual average on weekdays and fall away at weekends, while cars do much less of either, so the "
                   "trucks are expanded with the patterns the classifying stations measure for trucks and the cars "
                   "with the patterns for cars. Expanded with one pattern for all vehicles, every weekday count "
                   "carries too many trucks into the year, and the links where trucks are most of the traffic cross "
                   "the line without carrying the NOx to do so.", body),
         chart(f), Spacer(1, 6)]
    t = [["Link", "Name", "Designated"]]
    for k in f["links"]:
        t.append([k, f["names"][k], "Yes" if k in des else "No"])
    tb = Table(t, colWidths=[.6 * inch, 3.4 * inch, .9 * inch])
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
                       "2026-11-02T15:12:00Z", "2026-11-04T14:02:00Z", excel=True, company=W.PORT)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["memo"]), b"D:20261104091415-05'00'", b"D:20261104091415-05'00'")
    return f
