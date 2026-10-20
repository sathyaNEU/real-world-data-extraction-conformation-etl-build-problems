"""The golden deliverables: the conformed tract workbook and the recommendation memo to the council (PDF, with the
chart of each candidate tract's change and its 90 per cent interval), and generator/figures.json."""
import json
import math
import os

from reportlab import rl_config
rl_config.invariant = 1
from reportlab.graphics.shapes import Circle, Drawing, Line, Rect, String  # noqa: E402
from reportlab.lib import colors                                          # noqa: E402
from reportlab.lib.pagesizes import letter                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                           # noqa: E402
from reportlab.lib.units import inch                                      # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402
from openpyxl import Workbook                                             # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill                  # noqa: E402

import docs as DC   # noqa: E402
import pack as P    # noqa: E402
import world as W   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WORDS = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
         9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 28: "28", 29: "29", 30: "30"}
TEAL, GREY, INK = colors.HexColor("#1f6f8b"), colors.HexColor("#9aa4ab"), colors.HexColor("#222222")


def pct(v):
    return "%.1f" % (100 * v)


def figures(x):
    f = x["fig"]
    rows = []
    for r in f["rows"]:
        bgs = ""
        if r["split"]:
            t = next(t for t in x["ts"] if t.code10 == r["parent"])
            kid = next(b for c, b in t.children if c == r["tract"])
            bgs = ", ".join(str(b.num) for b in kid)
        rows.append(dict(nbhd=r["nbhd"], tract=P.tract_name(r["tract"]), geoid=r["geoid"], split=r["split"],
                         parent=P.tract_name(r["parent"]), bgs=bgs, r18=pct(r["r18"]), m18=pct(r["m18"]),
                         r23=pct(r["r23"]), m23=pct(r["m23"]), z="%.2f" % r["z"], high=r["high"], rise=r["rise"],
                         qual=r["qual"], d=100 * (r["r23"] - r["r18"]),
                         half=100 * math.sqrt(r["m18"] ** 2 + r["m23"] ** 2)))
    nb = []
    for n in W.NEIGHBOURHOODS:
        a, b = f["ask_a"][n], f["ask_b"][n]
        nb.append(dict(nbhd=n, count=f["count"][n], rec=n in f["designated"], open_props=a[0], days=int(round(a[1])),
                       dollars=int(round(b[0])), paid_props=b[1]))
    call = sorted(f["designated"])
    out = dict(rows=rows, nb=nb, call=call, n_call=len(call),
               runner=[n["nbhd"] for n in nb if not n["rec"] and n["count"] == max(m["count"] for m in nb
                                                                                      if not m["rec"])],
               threshold="20.0", level="90", z_line="%.3f" % W.Z90, sections=DC.SECTIONS)
    out["scored"] = dict(call=call, n_call=len(call),
                         tracts={r["geoid"]: dict(r18=r["r18"], m18=r["m18"], r23=r["r23"], m23=r["m23"],
                                                  qual=r["qual"]) for r in rows},
                         ask_a={n["nbhd"]: dict(props=n["open_props"], days=n["days"]) for n in nb},
                         ask_b={n["nbhd"]: dict(dollars=n["dollars"], props=n["paid_props"]) for n in nb},
                         count={n["nbhd"]: n["count"] for n in nb})
    return out


def write_workbook(path, g):
    wb = Workbook()
    ws = wb.active
    ws.title = "Tracts"
    head = ["Neighborhood", "2020 tract", "Tract GEOID", "Poverty rate 2014-2018 (%)", "Margin of error (%)",
            "Poverty rate 2019-2023 (%)", "Margin of error (%)", "Change (points)", "z", "Rate 20% or more",
            "Significant rise", "Qualifies", "2014-2018 source"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F6F8B")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for r in g["rows"]:
        src = ("2010 tract %s, block groups %s" % (r["parent"], r["bgs"])) if r["split"] else \
            "2010 tract %s" % r["tract"]
        ws.append([r["nbhd"], r["tract"], r["geoid"], float(r["r18"]), float(r["m18"]), float(r["r23"]),
                   float(r["m23"]), round(float(r["r23"]) - float(r["r18"]), 1), float(r["z"]),
                   "Yes" if r["high"] else "No", "Yes" if r["rise"] else "No", "Yes" if r["qual"] else "No", src])
    for col, w in zip("ABCDEFGHIJKLM", [17, 10, 14, 12, 10, 12, 10, 10, 7, 10, 10, 9, 34]):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row[3:8]:
            c.number_format = "0.0"
        row[8].number_format = "0.00"
        if row[11].value == "Yes":
            for c in row[:12]:
                c.font = Font(bold=True)
    ws.freeze_panes = "C2"
    ws2 = wb.create_sheet("Neighborhoods")
    ws2.append(["Neighborhood", "Qualifying tracts", "Recommended", "Residential properties with an open housing "
                "case, 31 Dec 2026", "Average days open", "Grant dollars paid, 2026", "Properties paid, 2026"])
    for c in ws2[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F6F8B")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for n in g["nb"]:
        ws2.append([n["nbhd"], n["count"], "Yes" if n["rec"] else "No", n["open_props"], n["days"], n["dollars"],
                    n["paid_props"]])
    ws2.append(["Total", sum(n["count"] for n in g["nb"]), "%d of 5" % g["n_call"],
                sum(n["open_props"] for n in g["nb"]), None, sum(n["dollars"] for n in g["nb"]),
                sum(n["paid_props"] for n in g["nb"])])
    for c in ws2[ws2.max_row]:
        c.font = Font(bold=True)
    for row in ws2.iter_rows(min_row=2):
        row[5].number_format = "$#,##0"
    for col, w in zip("ABCDEFG", [17, 11, 13, 22, 10, 14, 12]):
        ws2.column_dimensions[col].width = w
    ws2.freeze_panes = "B2"
    ws3 = wb.create_sheet("Notes")
    for line in [
        "Poverty rate: persons below the poverty level over persons for whom poverty status is determined (B17001; "
        "B17021 at block groups), guidelines 3.2.",
        "2014-2018 for a tract the 2020 census split: the sum of the 2010 block groups whose blocks make up the 2020 "
        "tract (2010 to 2020 block relationship file), margins as the root sum of squares.",
        "Tests (guidelines 3.1): 2019-2023 rate 20.0% or more, and z over 1.645 (the change over the root sum of the "
        "two squared standard errors). A neighborhood qualifies with three or more tracts meeting both.",
        "Open housing cases: status on 31 December 2026 from each case's event history; days from the case's opening; "
        "residential land uses only; properties counted once.",
        "Grant dollars: checks dated in 2026 that were not voided, whenever voided; a check reissued in 2026 counts "
        "in 2026.",
        "Prepared by the %s, %s." % (W.DEPT, W.MEMO_DATE)]:
        ws3.append([line])
    ws3.column_dimensions["A"].width = 120
    wb.save(path)


def chart(g):
    rows = g["rows"]
    n = len(rows)
    w, h = 6.6 * inch, 0.24 * inch * n + 0.9 * inch
    d = Drawing(w, h)
    left, right, top, bottom = 1.55 * inch, 0.25 * inch, 0.35 * inch, 0.5 * inch
    lo, hi = -40.0, 40.0
    sx = lambda v: left + (v - lo) / (hi - lo) * (w - left - right)
    step = (h - top - bottom) / n
    for v in range(-40, 41, 10):
        x = sx(v)
        d.add(Line(x, bottom, x, h - top, strokeColor=colors.HexColor("#e3e6e8") if v else INK,
                   strokeWidth=0.4 if v else 0.8))
        d.add(String(x, bottom - 12, "%+d" % v if v else "0", fontName="Helvetica", fontSize=7, textAnchor="middle",
                     fillColor=INK))
    d.add(String(sx(0), bottom - 25, "Change in poverty rate, 2014-2018 to 2019-2023 (percentage points), with its "
                 "90% interval", fontName="Helvetica", fontSize=7.5, textAnchor="middle", fillColor=INK))
    last = None
    for i, r in enumerate(rows):
        y = h - top - (i + 0.5) * step
        if r["nbhd"] != last:
            d.add(Line(4, y + step / 2, w - 4, y + step / 2, strokeColor=colors.HexColor("#c9ced2"), strokeWidth=0.4))
            last = r["nbhd"]
        col = TEAL if r["qual"] else GREY
        d.add(String(4, y - 2.5, "%s %s" % (r["nbhd"], r["tract"]), fontName="Helvetica-Bold" if r["qual"] else
                     "Helvetica", fontSize=6.8, fillColor=INK))
        a, b = max(lo, r["d"] - r["half"]), min(hi, r["d"] + r["half"])
        d.add(Line(sx(a), y, sx(b), y, strokeColor=col, strokeWidth=2))
        d.add(Circle(sx(r["d"]), y, 2.8, fillColor=col, strokeColor=colors.white, strokeWidth=0.8))
    d.add(Rect(left, h - 14, 8, 8, fillColor=TEAL, strokeColor=None))
    d.add(String(left + 12, h - 13, "Qualifies (2019-2023 rate 20% or more and a significant rise)",
                 fontName="Helvetica", fontSize=7, fillColor=INK))
    d.add(Rect(left + 3.2 * inch, h - 14, 8, 8, fillColor=GREY, strokeColor=None))
    d.add(String(left + 3.2 * inch + 12, h - 13, "Does not qualify", fontName="Helvetica", fontSize=7, fillColor=INK))
    return d


def write_memo(path, g):
    body = ParagraphStyle("b", fontName="Times-Roman", fontSize=10.5, leading=13.6, spaceAfter=7)
    small = ParagraphStyle("s", fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=colors.HexColor("#333333"))
    hd = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=TEAL)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                            topMargin=0.8 * inch, bottomMargin=0.8 * inch,
                            title="Neighborhood Stabilization Fund 2027 designations", author=W.PEOPLE["analyst"][0],
                            creator="City of %s" % W.CITY, producer="City of %s" % W.CITY, subject="Memo")

    def frame(c, d_):
        c.saveState()
        c.setFont("Helvetica", 7.5)
        c.drawString(0.95 * inch, 0.5 * inch, "%s, City of %s" % (W.DEPT, W.CITY))
        c.drawRightString(letter[0] - 0.95 * inch, 0.5 * inch, "Page %d" % d_.page)
        c.restoreState()
    rec = g["call"]
    nbs = {n["nbhd"]: n for n in g["nb"]}
    others = [n for n in W.NEIGHBOURHOODS if n not in rec]
    s = [Paragraph("City of %s, %s" % (W.CITY, W.DEPT), hd), Spacer(1, 6),
         Table([["To:", "City Council, through the Housing Committee"],
                ["From:", "%s, %s" % W.PEOPLE["analyst"]],
                ["Date:", W.MEMO_DATE],
                ["Re:", "Neighborhood Stabilization Fund, 2027 round: %s of 5 candidates recommended" % (
                    {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}[g["n_call"]])]],
               colWidths=[0.7 * inch, 5.9 * inch],
               style=TableStyle([("FONT", (0, 0), (0, -1), "Helvetica-Bold", 9.5), ("FONT", (1, 0), (1, -1),
                                                                                    "Helvetica", 9.5),
                                 ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("LINEBELOW", (0, -1), (-1, -1), 0.6,
                                                                         colors.black)])),
         Spacer(1, 10),
         Paragraph("The Department recommends designating <b>%s</b> for the 2027 round. %s, against the three the "
                   "guidelines require (section 3.1): tracts with a 2019 to 2023 poverty rate of 20 per cent or more "
                   "and a rise from 2014 to 2018 significant at the 90 per cent level. %s." % (
                       " and ".join(rec), "; ".join("%s has %s qualifying tracts" % (n, WORDS[nbs[n]["count"]])
                                                    for n in rec),
                       "; ".join("%s has %s" % (n, WORDS[nbs[n]["count"]]) for n in others)), body),
         Paragraph("%s of the %s listed tracts are halves of tracts the 2020 census split, with no 2014 to 2018 estimate "
                   "of their own. For "
                   "each of them we summed the 2014 to 2018 estimates of the 2010 block groups whose blocks make up "
                   "the new tract, rather than carrying the old tract's rate to both halves. In Kestrel Park and "
                   "Linden Row this decides the outcome: tract 403.02, the newer side of old tract 403, had a 2014 to "
                   "2018 rate of %s per cent on its own ground, not the old tract's %s, so its rise to %s is "
                   "significant; tract 303.01 in Linden Row already stood at %s per cent in 2014 to 2018, so its "
                   "%s per cent today is not a rise." % (
                       WORDS[sum(1 for r in g["rows"] if r["split"])].capitalize(), WORDS[len(g["rows"])], next(r["r18"] for r in g["rows"] if r["tract"] == "403.02"), g["parent403"],
                       next(r["r23"] for r in g["rows"] if r["tract"] == "403.02"),
                       next(r["r18"] for r in g["rows"] if r["tract"] == "303.01"),
                       next(r["r23"] for r in g["rows"] if r["tract"] == "303.01")), body),
         Spacer(1, 10)]
    t = [["Neighborhood", "Qualifying\ntracts", "Recommended", "Properties with an\nopen housing case,\n31 Dec 2026",
          "Average\ndays open", "Grant dollars\npaid, 2026", "Properties\npaid, 2026"]]
    for n in g["nb"]:
        t.append([n["nbhd"], str(n["count"]), "Yes" if n["rec"] else "No", str(n["open_props"]), str(n["days"]),
                  "${:,}".format(n["dollars"]), str(n["paid_props"])])
    tab = Table(t, colWidths=[1.25 * inch, 0.75 * inch, 0.85 * inch, 1.15 * inch, 0.7 * inch, 0.95 * inch,
                              0.75 * inch], repeatRows=1)
    tab.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.5), ("FONT", (0, 1), (-1, -1),
                                                                                 "Helvetica", 8.5),
                             ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                             ("VALIGN", (0, 0), (-1, 0), "BOTTOM")]))
    s += [Paragraph("Table 1. The candidates' results and the figures guidelines 4.2 asks for. Open cases are read "
                    "from each case's history as of 31 December 2026; grant dollars are checks dated in 2026 that "
                    "stood, net of voids made in 2027. The tract figures are in the attached workbook, %s." %
                    W.GOLDEN["workbook"], small), Spacer(1, 3), tab, PageBreak(),
          Paragraph("Three listed tracts each in Dunmore Heights and Kestrel Park rose significantly to 20 per cent or "
                    "more", ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=11, leading=14, spaceAfter=6)),
          chart(g),
          Paragraph("Figure 1. Each listed tract's change with its 90 per cent interval (the change plus or minus the "
                     "root sum of the two margins of error). Source: Census Bureau, ACS 2014-2018 and 2019-2023 "
                     "five-year estimates, tables B17001 and B17021; 2010 to 2020 block relationship file.", small)]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def build(gdir, x):
    if not os.path.exists(gdir):
        os.makedirs(gdir)
    g = figures(x)
    t403 = next(t for t in x["ts"] if t.code10 == "0403.00")
    e = x["tre"][(1, "0403.00")]
    g["parent403"] = pct(e.x / e.u)
    import postprocess as PP
    write_workbook(os.path.join(gdir, W.GOLDEN["workbook"]), g)
    PP.normalize_ooxml(os.path.join(gdir, W.GOLDEN["workbook"]), W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][0],
                       "2027-03-29T14:10:00Z", "2027-04-09T21:37:15Z", excel=True, company="City of Carrow")
    write_memo(os.path.join(gdir, W.GOLDEN["memo"]), g)
    PP.normalize_pdf(os.path.join(gdir, W.GOLDEN["memo"]), b"D:20270410102214-05'00'", b"D:20270410102214-05'00'")
    g["ask_a"], g["ask_b"] = g["scored"]["ask_a"], g["scored"]["ask_b"]
    g["tracts"] = {k: dict(r18=float(v["r18"]), m18=float(v["m18"]), r23=float(v["r23"]), m23=float(v["m23"]),
                           qual=v["qual"]) for k, v in g["scored"]["tracts"].items()}
    json.dump({k: v for k, v in g.items() if k not in ("rows", "nb")} | {"rows": g["rows"], "nb": g["nb"]},
              open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    return g
