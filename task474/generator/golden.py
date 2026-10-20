"""The golden deliverables: the provider group workbook (designations and the pharmacy summary) and the designation
memo for the contracting committee (PDF with a bar chart of every group's cost per member-month against the
benchmark), and generator/figures.json."""
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
import world as W    # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ORANGE, BLUE, INK = colors.HexColor("#c8553d"), colors.HexColor("#4f7ca8"), colors.HexColor("#222222")
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve"}


def dollars(v):
    return int(math.floor(v + .5))


def figures(target):
    gs = B.groups(target)
    rate = B.pmpm(target, "golden")
    des = sorted(g for g in gs if rate[g] >= W.BENCHMARK)
    names = {g: W.GROUPS[g][0] for g in gs}
    ph = B.pharmacy(target)
    on, _grp = B.roster(target)
    net = B.member_lines(target)
    ex_g, ex_r = B.exposure(target, "golden"), B.exposure(target, "roster")
    return dict(call=des, n_call=len(des), n_groups=len(gs), groups=gs, names=names, year=W.YEAR,
                rate={g: round(rate[g], 2) for g in gs}, benchmark="%.2f" % W.BENCHMARK,
                roster_route=sorted(g for g in gs if B.pmpm(target, "roster")[g] >= W.BENCHMARK),
                member_months=dict(golden=sum(ex_g.values()), roster=sum(ex_r.values()),
                                   added=sum(1 for k, v in net.items() if v > 0 and k not in on),
                                   removed=sum(1 for k, v in net.items() if v < 0 and k in on)),
                sections=DC.SECTIONS,
                asks=dict(paid={c: dollars(v[0]) for c, v in ph.items()}, fills={c: v[1] for c, v in ph.items()},
                          paid_total=dollars(sum(v[0] for v in ph.values())), fills_total=sum(v[1] for v in ph.values())))


def write_workbook(path, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Groups"
    ws.append(["Cost Performance Program 2027: provider group designations (services January to June 2026)"])
    ws.append([])
    ws.append(["Group ID", "Group name", "Designated"])
    for c in ws[3]:
        c.font = Font(bold=True)
    for g in f["groups"]:
        ws.append([g, f["names"][g], "Yes" if g in f["call"] else "No"])
    ws.append([])
    ws.append(["Designated: %d of %d groups." % (f["n_call"], f["n_groups"])])
    ws.column_dimensions["A"].width = 10
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 12
    ph = wb.create_sheet("Pharmacy")
    ph.append(["Pharmacy fills dated January to June 2026, by drug class"])
    ph.append([])
    ph.append(["Drug class", "Paid ($)", "Fills"])
    for c in ph[3]:
        c.font = Font(bold=True)
    for c in sorted(f["asks"]["paid"]):
        ph.append([c, f["asks"]["paid"][c], f["asks"]["fills"][c]])
    ph.column_dimensions["A"].width = 26
    ph.column_dimensions["B"].width = 14
    ph.append([])
    ph.append(["Prepared by %s, %s." % (W.PEOPLE["analyst"][0], W.MEMO_DATE)])
    wb.save(path)


def chart(f):
    gs = sorted(f["groups"], key=lambda g: -f["rate"][g])
    w, h = 6.6 * inch, 3.2 * inch
    d = Drawing(w, h)
    left, bottom, top = .6 * inch, .5 * inch, .3 * inch
    lo, hi = 250.0, 500.0
    sy = lambda v: bottom + (v - lo) / (hi - lo) * (h - bottom - top)
    bw = (w - left - 10) / len(gs)
    for v in range(250, 501, 50):
        d.add(Line(left, sy(v), w - 6, sy(v), strokeColor=colors.HexColor("#e2e5e8"), strokeWidth=.5))
        d.add(String(left - 6, sy(v) - 3, "$%d" % v, fontName="Helvetica", fontSize=7, textAnchor="end", fillColor=INK))
    for i, g in enumerate(gs):
        x0 = left + i * bw + 4
        d.add(Rect(x0, bottom, bw - 8, sy(f["rate"][g]) - bottom, fillColor=ORANGE if g in f["call"] else BLUE,
                   strokeColor=None))
        d.add(String(x0 + (bw - 8) / 2, bottom - 11, g, fontName="Helvetica", fontSize=7, textAnchor="middle",
                     fillColor=INK))
    d.add(Line(left, sy(W.BENCHMARK), w - 6, sy(W.BENCHMARK), strokeColor=INK, strokeWidth=1, strokeDashArray=[3, 2]))
    d.add(String(w - 8, sy(W.BENCHMARK) + 3, "Benchmark, $%.2f" % W.BENCHMARK, fontName="Helvetica-Bold", fontSize=7,
                 textAnchor="end", fillColor=INK))
    d.add(String(left, h - 12, "Paid medical cost per member-month, January to June 2026; designated groups in orange",
                 fontName="Helvetica", fontSize=7.5, fillColor=INK))
    return d


def write_memo(path, f):
    body = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=7)
    hd = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=BLUE)
    small = ParagraphStyle("s", fontName="Helvetica", fontSize=8, leading=10)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=.9 * inch, rightMargin=.9 * inch, topMargin=.8 * inch,
                            bottomMargin=.8 * inch, title="Cost Performance Program 2027 designations", author=W.PLAN,
                            creator=W.PLAN, producer=W.PLAN, subject="Cost Performance Program")
    des = f["call"]
    names = ", ".join(des[:-1]) + " and " + des[-1]
    s = [Paragraph("Cost Performance Program: 2027 designations", hd),
         Paragraph("To: Network Contracting Committee &nbsp;&nbsp; From: %s, %s &nbsp;&nbsp; Date: %s" % (
             W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][1], W.MEMO_DATE), small), Spacer(1, 8),
         Paragraph("I recommend designating %s of our %s primary care groups for the 2027 Cost Performance Program: %s. "
                   "Each group's members cost $%s or more per member-month in paid medical claims for January to June "
                   "2026." % (WORDS[len(des)], WORDS[f["n_groups"]], names, f["benchmark"]), body),
         Paragraph("The member-months come from the months our members were covered, not only the months the roster "
                   "lists. Members who lost coverage at their annual renewal and were reinstated back to that date were "
                   "covered through months the roster never caught up with; the state paid us capitation for those "
                   "months later, and we paid their claims. The roster also kept some members for a month or more "
                   "after they died, months the state took its capitation back for. Counted on the roster alone, the "
                   "groups with the most renewal churn look costlier than they are and the groups caring for the most "
                   "frail members look cheaper.", body),
         chart(f), Spacer(1, 6)]
    t = [["Group", "Name", "Designated"]]
    for g in f["groups"]:
        t.append([g, f["names"][g], "Yes" if g in des else "No"])
    tb = Table(t, colWidths=[.7 * inch, 2.6 * inch, 1.0 * inch])
    tb.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8), ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                            ("LINEBELOW", (0, 0), (-1, 0), .6, INK)]))
    s.append(tb)
    doc.build(s)


def build(gdir, x, target=None, figs=None):
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
                       "2026-11-16T15:12:00Z", "2026-11-18T14:02:00Z", excel=True, company=W.PLAN)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["memo"]), b"D:20261118091415-06'00'", b"D:20261118091415-06'00'")
    return f
