"""The golden deliverables: Tarbert Economics' one-page client preview (PDF, the call first, a chart of the revision
record) and its tables workbook, and generator/figures.json with every figure the write-up states."""
from __future__ import annotations

import json
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.graphics.shapes import Drawing, Line, Rect, String                  # noqa: E402
from reportlab.lib import colors                                                     # noqa: E402
from reportlab.lib.pagesizes import A4                                               # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                      # noqa: E402
from reportlab.lib.units import mm                                                   # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import asks as A            # noqa: E402
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as D            # noqa: E402
import postprocess as PP    # noqa: E402

F_PDF = "gdp_preview_2026q2.pdf"
F_XLSX = "gdp_preview_2026q2_tables.xlsx"
TEAL = colors.HexColor("#0e4f5c")
AMBER = colors.HexColor("#c4801f")
INK = colors.HexColor("#1b1f24")
GREY = colors.HexColor("#646b73")
RULE = colors.HexColor("#b6bdc5")
LINE_LABELS = [("HFCE", "Household consumption"), ("GFCE", "Government consumption"),
               ("GFCF_DW", "Dwelling investment"), ("GFCF_ME", "Machinery and equipment"),
               ("GFCF_NDC", "Non-dwelling construction"), ("GFCF_IPP", "Intellectual property products"),
               ("GFCF_PUB", "Public investment"), ("CIPI_NF", "Business inventories"),
               ("CIPI_FO", "Farm and other inventories"), ("X_G", "Goods exports"), ("X_S", "Services exports"),
               ("M_G", "Goods imports"), ("M_S", "Services imports")]


def r1(x):
    return K.round_half_up(x, 1)


def r2(x):
    return K.round_half_up(x, 2)


def s1(x):
    v = r1(x)
    return ("+%.1f" % v) if v > 0 else ("%.1f" % v if v < 0 else "0.0")


def s2(x):
    v = r2(x)
    return ("+%.2f" % v) if v > 0 else ("%.2f" % v if v < 0 else "0.00")


def results(B):
    g = C.golden(B)
    figs_a, rec = A.ask_a(B)
    figs_b = A.ask_b(B)
    return {"golden": g, "a": figs_a, "rec": rec, "b": figs_b}


def chart(rec, width=170 * mm, height=58 * mm):
    """The revision record: each quarter's growth in its advance estimate and in the latest estimates, at an
    annualised rate."""
    d = Drawing(width, height)
    qs = A.QUARTERS_A
    vals = [v for q in qs for v in rec[q][:2]]
    lo, hi = min(-1.0, min(vals) - 0.5), max(vals) + 0.6
    x0, x1, y0, y1 = 14 * mm, width - 4 * mm, 12 * mm, height - 14 * mm
    ys = lambda v: y0 + (v - lo) / (hi - lo) * (y1 - y0)
    d.add(String(0, height - 4 * mm, "Growth in each quarter at an annualised rate, per cent: the advance estimate and "
                 "the latest estimates", fontName="Carlito-Bold", fontSize=8.2, fillColor=INK))
    for t in range(int(lo), int(hi) + 1):
        y = ys(t)
        d.add(Line(x0, y, x1, y, strokeColor=RULE if t else GREY, strokeWidth=0.3 if t else 0.6))
        d.add(String(x0 - 3 * mm, y - 1.2, "%d" % t, fontName="Carlito", fontSize=6.8, fillColor=GREY,
                     textAnchor="end"))
    slot = (x1 - x0) / len(qs)
    bw = slot * 0.32
    for i, q in enumerate(qs):
        a, l, _ = rec[q]
        cx = x0 + slot * (i + 0.5)
        for v, off, col in ((a, -bw / 2 - 0.4, AMBER), (l, bw / 2 + 0.4, TEAL)):
            yb, yt = ys(0), ys(v)
            d.add(Rect(cx + off - bw / 2, min(yb, yt), bw, abs(yt - yb), fillColor=col, strokeColor=None))
        lab = {"1": "Mar", "2": "Jun", "3": "Sep", "4": "Dec"}[q[-1]] + " " + q[2:4]
        d.add(String(cx, y0 - 4.5 * mm, lab, fontName="Carlito", fontSize=6.6, fillColor=GREY, textAnchor="middle"))
    lx, ly = x0, height - 9.5 * mm
    for lab, col in (("Advance estimate", AMBER), ("Latest estimates (annual national accounts, 21 July)", TEAL)):
        d.add(Rect(lx, ly, 2.6 * mm, 2.2 * mm, fillColor=col, strokeColor=None))
        d.add(String(lx + 3.6 * mm, ly + 0.5, lab, fontName="Carlito", fontSize=6.8, fillColor=INK))
        lx += 3.6 * mm + 6.8 * 0.48 * len(lab) + 6 * mm
    return d


def write_pdf(path, B, res):
    g, fa, rec, fb = res["golden"], res["a"], res["rec"], res["b"]
    c = g["contrib"]
    body = ParagraphStyle("b", fontName="Carlito", fontSize=9.4, leading=12.4, textColor=INK, spaceAfter=5)
    lead = ParagraphStyle("l", fontName="Carlito-Bold", fontSize=11.2, leading=14.6, textColor=INK, spaceAfter=6)
    h1 = ParagraphStyle("h", fontName="Carlito-Bold", fontSize=17, leading=21, textColor=TEAL, spaceAfter=3)
    sub = ParagraphStyle("s", fontName="Carlito", fontSize=8.4, leading=11, textColor=GREY, spaceAfter=7)
    cell = ParagraphStyle("c", fontName="Carlito", fontSize=7.8, leading=9.4, textColor=INK)
    cellr = ParagraphStyle("cr", fontName="Carlito", fontSize=7.8, leading=9.4, textColor=INK, alignment=2)
    cellb = ParagraphStyle("cb", fontName="Carlito-Bold", fontSize=7.8, leading=9.4, textColor=INK)
    cellbr = ParagraphStyle("cbr", fontName="Carlito-Bold", fontSize=7.8, leading=9.4, textColor=INK, alignment=2)
    e = D.esc
    tot_coal = fb[("total", "32")]
    tot_lng = fb[("total", "34")]
    s = [Paragraph("Tarbert Economics | GDP preview | Wednesday 29 July 2026, 18:00", sub),
         Paragraph(e("June quarter GDP: we expect %.1f%% annualised" % r1(g["ann"])), h1),
         Paragraph(e("We expect the Statistics Office's advance estimate, out at 10:45 tomorrow, to show real GDP "
                     "growth of %.1f%% at an annualised rate in the June quarter, %.2f%% on the March quarter."
                     % (r1(g["ann"]), r2(g["q"]))), lead),
         Paragraph(e("Net exports carry the quarter. Goods exports add %.2f percentage points, with the coal ports "
                     "back to full loadings after February's dip, and goods imports, down in volume as import prices "
                     "rose in March and again in June, add %.2f. Business inventories take %.2f points off. At home, "
                     "household spending adds %.2f and government spending %.2f, while machinery and equipment "
                     "investment takes %.2f off and dwelling investment %.2f."
                     % (r2(c["X_G"]), r2(c["M_G"]), -r2(c["CIPI_NF"]), r2(c["HFCE"]), r2(c["GFCE"]),
                        -r2(c["GFCF_ME"]), -r2(c["GFCF_DW"]))), body),
         Paragraph(e("TBS's June bulletin, out yesterday after its outage, carries business stocks at book value, "
                     "at what each business paid. We value each industry's end-March and end-June stocks at its "
                     "input prices over the months its stock-to-sales ratio covers, a method that rebuilds the "
                     "Office's estimates of the past 28 quarters with a root mean square error of $%.1f million. The "
                     "machinery, vehicle and household goods trades hold around two months of stock, much of it "
                     "bought before the March and June rises in import prices. On that basis business stocks fell by "
                     "$%s million at 2025 prices in the June quarter after a build of $%s million in the March "
                     "quarter."
                     % (round(C.backtest(B)["turnover"]["rmse"], 1), "{:,.0f}".format(-C.cipi(B, "2026Q2")),
                        "{:,.0f}".format(B["base"]["CIPI_NF"]))), body),
         Paragraph(e("The first print moves. Over the twelve quarters to March 2026 the advance estimate has been "
                     "revised by %.2f points on average, in either direction, and up by %.2f points on average; the "
                     "annual national accounts of 21 July revised the September and December quarters of 2025 by %s "
                     "and %s points and the March quarter of 2026 by %s."
                     % (r2(fa["mar"]), r2(fa["mean"]), s1(fa["2025Q3"]), s1(fa["2025Q4"]), s1(fa["2026Q1"]))), body),
         Paragraph(e("Coal and LNG shipped to Japan, China, Korea, India and Taiwan were up $%s million and $%s million "
                     "on the June quarter of 2025, when LNG loadings at Cape Mallory dropped in June; Japan took $%s "
                     "million more LNG." % ("{:,.1f}".format(r1(tot_coal)), "{:,.1f}".format(r1(tot_lng)),
                                    "{:,.1f}".format(r1(fb[("JP", "34")])))), body),
         chart(rec),
         Paragraph(e("Sources: Statistics Office real-time database of quarterly GDP estimates (advance estimates); "
                     "annual national accounts 2025, Table 3 (latest estimates)."), sub)]
    rows = [[Paragraph("Contribution to growth on the March quarter, percentage points", cellb),
             Paragraph("", cellbr)]]
    for code, lab in LINE_LABELS:
        rows.append([Paragraph(e(lab), cell), Paragraph(e("%.2f" % r2(c[code])), cellr)])
    rows.append([Paragraph("GDP, on the March quarter", cellb), Paragraph(e("%.2f" % r2(g["q"])), cellbr)])
    rows.append([Paragraph("GDP, at an annualised rate (per cent)", cellb), Paragraph(e("%.1f" % r1(g["ann"])), cellbr)])
    t = Table(rows, colWidths=[78 * mm, 22 * mm])
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.5, RULE), ("LINEABOVE", (0, -2), (-1, -2), 0.5, RULE),
                           ("TOPPADDING", (0, 0), (-1, -1), 0.9), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.9)]))
    s.append(t)
    s.append(Spacer(1, 3))
    s.append(Paragraph(e("Contributions may not add to the total because of rounding. Sources: Statistics Office, "
                         "TBS, Harbours Board, Tarbert Economics. Nicola Jones, Senior Economist. For clients of "
                         "Tarbert Bank; not investment advice."), sub))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=12 * mm,
                            bottomMargin=10 * mm, title="GDP preview, June quarter 2026", author="Tarbert Economics",
                            subject="", creator="", producer="")
    doc.build(s)
    PP.normalize_pdf(path, b"D:20260729174812+12'00'", b"D:20260729174812+12'00'")


def write_xlsx(path, B, res):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
    g, fa, rec, fb = res["golden"], res["a"], res["rec"], res["b"]
    bold = Font(bold=True)
    fill = PatternFill("solid", fgColor="DDE8EA")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Revision record"
    ws["A1"] = ("The advance estimate has been revised up by %.2f points on average over the twelve quarters to March "
                "2026" % r2(fa["mean"]))
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Growth at an annualised rate, per cent. Advance: each quarter on the one before in its advance "
                "estimate. Latest: the annual national accounts of 21 July 2026. Revision: latest less advance, "
                "percentage points, from the unrounded estimates.")
    for j, h in enumerate(["Quarter", "Advance estimate", "Latest estimate", "Revision"], 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font, c.fill = bold, fill
    for i, q in enumerate(A.QUARTERS_A):
        a, l, rv = rec[q]
        ws.cell(row=5 + i, column=1, value="%s Q%s" % (q[:4], q[-1]))
        for j, v in enumerate((a, l, rv), 2):
            ws.cell(row=5 + i, column=j, value=r2(v)).number_format = "0.00"
    r = 5 + len(A.QUARTERS_A) + 1
    ws.cell(row=r, column=1, value="Summary").font = bold
    for k, (lab, key, nd) in enumerate((("Revision, September quarter 2025", "2025Q3", 1),
                                        ("Revision, December quarter 2025", "2025Q4", 1),
                                        ("Revision, March quarter 2026", "2026Q1", 1),
                                        ("Mean revision, June 2023 to March 2026", "mean", 2),
                                        ("Mean absolute revision, June 2023 to March 2026", "mar", 2))):
        ws.cell(row=r + 1 + k, column=1, value=lab)
        c = ws.cell(row=r + 1 + k, column=4, value=K.round_half_up(fa[key], nd))
        c.number_format = "0.0" if nd == 1 else "0.00"
    ws.cell(row=r + 7, column=1, value="Sources: Statistics Office, real-time database of quarterly GDP estimates "
            "(advance estimates); annual national accounts 2025, Table 3 (latest estimates).").font = Font(italic=True,
                                                                                                       size=9)
    ws.column_dimensions["A"].width = 44
    for j in (2, 3, 4):
        ws.column_dimensions[get_column_letter(j)].width = 17
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Coal and LNG")
    ws2["A1"] = ("LNG shipped to Japan, China, Korea, India and Taiwan up $%s million on the June quarter of 2025, coal "
                 "up $%s million" % ("{:,.1f}".format(r1(fb[("total", "34")])), "{:,.1f}".format(r1(fb[("total", "32")]))))
    ws2["A1"].font = Font(bold=True, size=12)
    ws2["A2"] = ("$ million, original terms. June quarter 2026: TBS bulk download for April and May, TBS June "
                 "bulletin for June. "
                 "June quarter 2025: the bulk download's May, June and July months, each the month after the cargoes "
                 "sailed.")
    head = ["Market", "Coal, Jun qtr 2025", "Coal, Jun qtr 2026", "Coal, change", "LNG, Jun qtr 2025",
            "LNG, Jun qtr 2026", "LNG, change"]
    for j, h in enumerate(head, 1):
        c = ws2.cell(row=4, column=j, value=h)
        c.font, c.fill = bold, fill
        c.alignment = Alignment(wrap_text=True)
    for i, mk in enumerate(A.MARKETS):
        ws2.cell(row=5 + i, column=1, value=A.MARKET_NAMES[mk])
        for j, d in ((2, "32"), (5, "34")):
            for k, v in enumerate((A.quarter_2025(B, mk, d), A.quarter_2026(B, mk, d), fb[(mk, d)])):
                ws2.cell(row=5 + i, column=j + k, value=r1(v)).number_format = "#,##0.0;-#,##0.0"
    rr = 5 + len(A.MARKETS)
    ws2.cell(row=rr, column=1, value="Five markets").font = bold
    for j, d in ((2, "32"), (5, "34")):
        v25 = sum(A.quarter_2025(B, mk, d) for mk in A.MARKETS)
        v26 = sum(A.quarter_2026(B, mk, d) for mk in A.MARKETS)
        for k, v in enumerate((v25, v26, fb[("total", d)])):
            c = ws2.cell(row=rr, column=j + k, value=r1(v))
            c.number_format = "#,##0.0;-#,##0.0"
            c.font = bold
    ws2.column_dimensions["A"].width = 16
    for j in range(2, 8):
        ws2.column_dimensions[get_column_letter(j)].width = 14
    ws2.row_dimensions[4].height = 30
    ws2.freeze_panes = "B5"
    ws2.cell(row=rr + 2, column=1, value="Sources: TBS bulk download of trade by country and SITC division (pulled 24 "
             "June 2026), divisions 32 and 34; TBS, Merchandise trade and business stocks, June 2026, Table 4; "
             "Harbours Board bulk loadings.").font = Font(italic=True, size=9)
    ws3 = wb.create_sheet("Call")
    ws3["A1"] = "June quarter 2026: we expect GDP growth of %.1f%% at an annualised rate" % r1(g["ann"])
    ws3["A1"].font = Font(bold=True, size=12)
    ws3["A3"] = "GDP growth at an annualised rate, per cent"
    ws3["B3"] = r1(g["ann"])
    ws3["B3"].number_format = "0.0"
    ws3["A4"] = "GDP growth on the March quarter, per cent"
    ws3["B4"] = r2(g["q"])
    ws3["B4"].number_format = "0.00"
    ws3.cell(row=6, column=1, value="Contribution to growth on the March quarter, percentage points").font = bold
    for i, (code, lab) in enumerate(LINE_LABELS):
        ws3.cell(row=7 + i, column=1, value=lab)
        ws3.cell(row=7 + i, column=2, value=r2(g["contrib"][code])).number_format = "0.00"
    ws3.cell(row=7 + len(LINE_LABELS) + 1, column=1, value="Contributions may not add to the total because of "
             "rounding.").font = Font(italic=True, size=9)
    ws3.column_dimensions["A"].width = 58
    ws3.column_dimensions["B"].width = 12
    ws4 = wb.create_sheet("Notes")
    for i, n in enumerate([
            "Tarbert Economics, 29 July 2026. Prepared by Nicola Jones.",
            "The call: the desk's tracker for the lines TBS's June bulletin does not feed; goods trade from the bulletin "
            "by SITC section over the export and import price indexes rebased to 2025; business inventories from the "
            "bulletin's book values, each industry's end-March and end-June stock valued at its input price index "
            "averaged over the months its stock-to-sales ratio covers, less the March quarter's published change.",
            "The revision record and the coal and LNG table are described on their sheets."], 1):
        ws4.cell(row=i, column=1, value=n)
    ws4.column_dimensions["A"].width = 120
    wb.save(path)
    PP.normalize_ooxml(path, "Nicola Jones", "Nicola Jones", "2026-07-29T05:12:00Z", "2026-07-29T05:46:00Z",
                       title="GDP preview tables, June quarter 2026", excel=True, company="Tarbert Bank")


def figures(B, res, routes, backtest):
    g, fa, rec, fb = res["golden"], res["a"], res["rec"], res["b"]
    out = {
        "call": {"annualised_pct": r1(g["ann"]), "quarterly_pct": r2(g["q"]), "unrounded": g["ann"]},
        "contributions_pp": {k: r2(v) for k, v in g["contrib"].items()},
        "business_inventories_m": {"june_quarter_2026": round(C.cipi(B, "2026Q2"), 1),
                                   "march_quarter_2026_published": B["base"]["CIPI_NF"],
                                   "change": round(C.cipi(B, "2026Q2") - B["base"]["CIPI_NF"], 1)},
        "goods_m": {"exports_q2": round(C.goods(B, "2026Q2", "x"), 1), "imports_q2": round(C.goods(B, "2026Q2", "m"), 1),
                    "exports_q1": B["base"]["X_G"], "imports_q1": B["base"]["M_G"]},
        "gdp_q1_m": B["gdp_q1"],
        "tracker_sum_pp": r2(sum(v for k, v in g["contrib"].items() if k not in ("X_G", "M_G", "CIPI_NF"))),
        "inventories_drag_pp": -r2(g["contrib"]["CIPI_NF"]),
        "ask_a": {k: (K.round_half_up(v, 1) if k not in ("mean", "mar") else K.round_half_up(v, 2))
                  for k, v in fa.items()},
        "ask_a_record": {q: [r2(x) for x in v] for q, v in rec.items()},
        "ask_b": {"%s_%s" % (c, d): r1(v) for (c, d), v in fb.items()},
        "ask_b_levels": {"%s_%s" % (mk, d): [r1(A.quarter_2025(B, mk, d)), r1(A.quarter_2026(B, mk, d))]
                         for mk in A.MARKETS for d in ("32", "34")},
        "routes": {k: K.round_half_up(v[1], 1) for k, v in routes.items()},
        "routes_unrounded": {k: round(v[1], 3) for k, v in routes.items()},
        "backtest_rmse_m": {k: round(v["rmse"], 1) for k, v in backtest.items()},
        "backtest_last_m": {k: round(v["last"], 1) for k, v in backtest.items()},
    }
    return out


def write_all(golden_dir, gen_dir, B):
    res = results(B)
    write_pdf(os.path.join(golden_dir, F_PDF), B, res)
    write_xlsx(os.path.join(golden_dir, F_XLSX), B, res)
    routes = C.routes(B)
    bt = C.backtest(B)
    figs = figures(B, res, routes, bt)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8", newline="\n") as fh:
        json.dump(figs, fh, indent=1, ensure_ascii=False, sort_keys=True)
        fh.write("\n")
    return res, figs
