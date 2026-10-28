"""The goldens: the frequency workbook and the decision deck, and generator/figures.json, from the golden's own run
on the bundle."""
import json
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import common as K

ROUTE_ORDER = ["Policyholder", "Third party", "Third-party insurer", "Solicitor practice", "Claims management company"]
HDR = PatternFill("solid", fgColor="1F4E5A")
PILOT = PatternFill("solid", fgColor="E3EFEC")
THIN = Side(style="thin", color="9AA9B0")


def r1(x):
    return float("%.1f" % (x + 1e-12))


def figures(R):
    g = R["freq"]["route"]
    F = {"call": R["call"], "third": R["third"],
         "frequency": {r: r1(g[r]) for r in K.REG},
         "frequency_unrounded": {r: round(g[r], 4) for r in K.REG},
         "gap": r1(R["gap"]),
         "earned_car_years": {r: round(R["cy"][r], 2) for r in K.REG},
         "notified_2025": R["notified"],
         "ultimate_2025": {r: round(R["est"]["route"][r], 1) for r in K.REG},
         "not_yet_notified_2025": {r: round(R["est"]["route"][r] - R["notified"][r], 1) for r in K.REG},
         "backtest_2022_route_pct": {r: round(R["bt"]["route"][r][2], 2) for r in K.REG},
         "backtest_2022_worst_pct": {h: round(max(abs(v[2]) for v in R["bt"][h].values()), 2) for h in R["bt"]},
         "final_2022": R["final22"],
         "default_pooled": {r: r1(R["freq"]["pooled"][r]) for r in K.REG},
         "default_head": {r: r1(R["freq"]["head"][r]) for r in K.REG},
         "default_notified_by": {r: r1(R["freq"]["notified_by"][r]) for r in K.REG},
         "route_factors": {k: round(v, 4) for k, v in R["factors_route"].items()},
         "cars_on_cover": {"%s|%s" % k: v for k, v in R["ask_a"].items()},
         "share_still_to_come_pct": {r: round(100 * (R["est"]["route"][r] - R["notified"][r]) / R["est"]["route"][r], 1) for r in K.REG}}
    return F


def _hdr(ws, row, cols):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row, i, c)
        cell.font = Font(bold=True, color="FFFFFF", name="Arial", size=10)
        cell.fill = HDR
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[row].height = 30


def _title(ws, title, sub):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=13, name="Arial", color="1F4E5A")
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9, name="Arial", color="5D666C")


def write_workbook(path, R, F):
    wb = Workbook()
    ws = wb.active
    ws.title = "Frequency 2025"
    _title(ws, "Private-car claim frequency, accident year 2025, by sales region",
           "Claims to 30 September 2026 and claims not yet notified (Motor Reserving Standard v4, development by "
           "notifying route); per 100 car-years earned in 2025. Pilot terms of 6 October 2026.")
    cols = ["Sales region", "Earned car-years 2025", "Claims notified to 30 Sep 2026",
            "Claims not yet notified (estimated)", "Claims, accident year 2025", "Frequency per 100 car-years",
            "Rank", "Pilot region"]
    _hdr(ws, 4, cols)
    order = R["order"]
    for i, r in enumerate(order):
        row = 5 + i
        vals = [r, R["cy"][r], R["notified"][r], R["est"]["route"][r] - R["notified"][r], R["est"]["route"][r],
                R["freq"]["route"][r], i + 1, "Yes" if r in R["call"] else "No"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row, j, v)
            c.font = Font(name="Arial", size=10, bold=(r in R["call"] and j in (1, 6, 8)))
            if r in R["call"]:
                c.fill = PILOT
        ws.cell(row, 2).number_format = "#,##0.00"
        ws.cell(row, 3).number_format = "#,##0"
        ws.cell(row, 4).number_format = "#,##0"
        ws.cell(row, 5).number_format = "#,##0"
        ws.cell(row, 6).number_format = "0.0"
    tr = 10
    ws.cell(tr, 1, "All regions").font = Font(bold=True, name="Arial", size=10)
    for j, col in ((2, "B"), (3, "C"), (4, "D"), (5, "E")):
        ws.cell(tr, j, "=SUM(%s5:%s9)" % (col, col)).font = Font(bold=True, name="Arial", size=10)
        ws.cell(tr, j).number_format = "#,##0.00" if j == 2 else "#,##0"
        ws.cell(tr, j).border = Border(top=THIN)
    ws.cell(tr, 6, "=E10/B10*100").number_format = "0.0"
    ws.cell(12, 1, "Gap, second region to third (%s to %s), per 100 car-years" % (order[1], order[2]))
    ws.cell(12, 6, R["gap"]).number_format = "0.0"
    ws.cell(14, 1, "Ranked on unrounded frequencies; the gap is taken before rounding.").font = Font(italic=True, size=9, name="Arial", color="5D666C")
    for j, wd in enumerate((16, 14, 16, 18, 15, 15, 7, 8), 1):
        ws.column_dimensions[get_column_letter(j)].width = wd
    ws.freeze_panes = "B5"

    ws2 = wb.create_sheet("Development")
    _title(ws2, "Development factors by notifying route, whole private-car book",
           "Closed accident years 2019 to 2022: claims at 21 months (30 September of the following year) and final.")
    _hdr(ws2, 4, ["Notifying route", "Claims at 21 months", "Final claims", "Factor, 21 months to final"] +
         ["2025 notified, %s" % r for r in K.REG])
    G = R["_G"]
    pos = {ay: G.position(ay) for ay in K.CLOSED}
    fin = {ay: G.final(ay) for ay in K.CLOSED}
    p25 = G.position(K.OPEN_YEAR)
    for i, rt in enumerate(ROUTE_ORDER):
        a = sum(int((pos[ay].route == rt).sum()) for ay in K.CLOSED)
        b = sum(int((fin[ay].route == rt).sum()) for ay in K.CLOSED)
        row = 5 + i
        ws2.cell(row, 1, rt)
        ws2.cell(row, 2, a).number_format = "#,##0"
        ws2.cell(row, 3, b).number_format = "#,##0"
        ws2.cell(row, 4, "=C%d/B%d" % (row, row)).number_format = "0.000"
        for j, r in enumerate(K.REG):
            ws2.cell(row, 5 + j, int(((p25.route == rt) & (p25.region == r)).sum())).number_format = "#,##0"
    ws2.cell(11, 1, "The notifying route is the notified-by field, with claims a representative notified split by the "
                    "firm type on claimant_representatives.csv.").font = Font(italic=True, size=9, name="Arial", color="5D666C")
    for j, wd in enumerate((26, 13, 12, 14, 13, 13, 13, 13, 13), 1):
        ws2.column_dimensions[get_column_letter(j)].width = wd
    ws2.freeze_panes = "B5"

    ws3 = wb.create_sheet("Back-test 2022")
    _title(ws3, "Standard 3.3: each development re-run on accident year 2022",
           "From 30 September 2023 with 2019 to 2021; estimate against the final count, per cent. Used only within "
           "two per cent in every region.")
    names = [("pooled", "Whole book, pooled"), ("head", "By head of claim"), ("notified_by", "By notified-by field"),
             ("representative", "By representative"), ("route", "By notifying route"),
             ("cmc_rest", "Claims-management companies against the rest"), ("route_head", "By notifying route and head")]
    _hdr(ws3, 4, ["Development"] + K.REG + ["Largest miss", "Passes"])
    for i, (h, nm) in enumerate(names):
        row = 5 + i
        ws3.cell(row, 1, nm)
        for j, r in enumerate(K.REG):
            ws3.cell(row, 2 + j, R["bt"][h][r][2] / 100).number_format = "+0.00%;-0.00%"
        worst = max(abs(v[2]) for v in R["bt"][h].values())
        ws3.cell(row, 7, worst / 100).number_format = "0.00%"
        ok = worst <= K.TOLERANCE
        ws3.cell(row, 8, "Yes" if ok else "No")
        if ok:
            for j in range(1, 9):
                ws3.cell(row, j).fill = PILOT
    ws3.cell(13, 1, "Final 2022 counts: " + ", ".join("%s %s" % (r, format(R["final22"][r], ",")) for r in K.REG)).font = Font(size=9, name="Arial")
    for j, wd in enumerate((40, 11, 11, 11, 11, 11, 13, 8), 1):
        ws3.column_dimensions[get_column_letter(j)].width = wd

    ws4 = wb.create_sheet("Cars on cover")
    _title(ws4, "Private cars on cover at 30 September 2026, for the Brackwell order",
           "Risk postcode district and cover as at 30 September 2026 (in-force file with the mid-term changes "
           "effective on or before that date).")
    _hdr(ws4, 4, ["Sales region", "COMP", "TPFT", "TPO", "All private cars"])
    for i, r in enumerate(K.REG):
        row = 5 + i
        ws4.cell(row, 1, r)
        for j, cv in enumerate(("COMP", "TPFT", "TPO")):
            ws4.cell(row, 2 + j, R["ask_a"][(r, cv)]).number_format = "#,##0"
        ws4.cell(row, 5, "=SUM(B%d:D%d)" % (row, row)).number_format = "#,##0"
    ws4.cell(10, 1, "Total").font = Font(bold=True, name="Arial", size=10)
    for j, col in ((2, "B"), (3, "C"), (4, "D"), (5, "E")):
        ws4.cell(10, j, "=SUM(%s5:%s9)" % (col, col)).number_format = "#,##0"
    for j, wd in enumerate((16, 12, 12, 12, 16), 1):
        ws4.column_dimensions[get_column_letter(j)].width = wd
    wb.save(path)


def write_deck(path, R, F):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.util import Emu, Pt

    TEAL, GREY, INKC = RGBColor(0x1F, 0x4E, 0x5A), RGBColor(0x9A, 0xA9, 0xB0), RGBColor(0x1D, 0x23, 0x27)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, s, size=14, bold=False, color=INKC):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        lines = s.split("\n")
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = ln
            p.font.size, p.font.bold, p.font.color.rgb, p.font.name = Pt(size), bold, color, "Arial"
        return tb

    def foot(slide, n):
        text(slide, 457200, 6400800, 9000000, 300000, "Corriven Insurance, telematics pilot 2027, 13 November 2026. "
             "Claims extract to 30 September 2026; pricing mart exposure.", 9, color=GREY)
        text(slide, 11000000, 6400800, 700000, 300000, str(n), 9, color=GREY)

    order, f = R["order"], R["freq"]["route"]
    share = {r: 100 * (R["est"]["route"][r] - R["notified"][r]) / R["est"]["route"][r] for r in K.REG}
    s = prs.slides.add_slide(blank)
    text(s, 457200, 1600000, 11000000, 1200000, "Mersey and Pennine host the 2027 telematics pilot", 34, True, TEAL)
    text(s, 457200, 2900000, 11000000, 1400000,
         "Their private cars had the highest claim frequency in accident year 2025: %.1f and %.1f claims per 100 "
         "car-years, against %.1f in %s, the next region.\nPaper for Damian Warren, Chief Underwriting Officer, 13 November 2026. "
         "Carol Thorpe, motor portfolio actuary." % (f[order[0]], f[order[1]], f[order[2]], order[2]), 16)
    foot(s, 1)

    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 900000, "Pennine is second once the 2025 claims still to come are counted by who "
         "notifies them", 24, True, TEAL)
    cd = CategoryChartData()
    cd.categories = order
    cd.add_series("Notified to 30 September 2026", [round(100 * R["notified"][r] / R["cy"][r], 2) for r in order])
    cd.add_series("Not yet notified (estimated)",
                  [round(100 * (R["est"]["route"][r] - R["notified"][r]) / R["cy"][r], 2) for r in order])
    ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Emu(457200), Emu(1300000), Emu(7000000), Emu(4900000), cd).chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.tick_labels.font.size = Pt(10)
    ch.category_axis.tick_labels.font.size = Pt(11)
    ch.plots[0].series[0].format.fill.solid()
    ch.plots[0].series[0].format.fill.fore_color.rgb = TEAL
    ch.plots[0].series[1].format.fill.solid()
    ch.plots[0].series[1].format.fill.fore_color.rgb = GREY
    text(s, 7700000, 1500000, 4000000, 4600000,
         "Claims per 100 car-years, accident year 2025\n" +
         "\n".join("%s  %.1f%s" % (r, f[r], "  (pilot)" if r in R["call"] else "") for r in order) +
         "\n\nGap, %s to %s: %.1f\n\nClaims-management companies notify injury claims months and years after the "
         "accident, and Pennine's 2025 injury claims came through them far more often than in earlier years: %.0f per "
         "cent of its 2025 claims are still to come, against %.0f to %.0f per cent in the other regions."
         % (order[1], order[2], R["gap"], share["Pennine"], min(v for r, v in share.items() if r != "Pennine"),
            max(v for r, v in share.items() if r != "Pennine")), 13)
    foot(s, 2)

    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 900000, "Only the development by notifying route reproduces 2022 within the "
         "Standard's two per cent", 24, True, TEAL)
    rows = [("Whole book, pooled", "pooled"), ("By head of claim", "head"), ("By notified-by field", "notified_by"),
            ("By representative", "representative"), ("By notifying route", "route")]
    tbl = s.shapes.add_table(len(rows) + 1, 4, Emu(457200), Emu(1400000), Emu(11200000), Emu(2800000)).table
    for j, h in enumerate(["Development of the claims not yet notified", "Largest 2022 miss (region)", "Pennine 2025",
                           "Severn 2025"]):
        tbl.cell(0, j).text = h
    for i, (nm, h) in enumerate(rows, 1):
        worst_r = max(K.REG, key=lambda r: abs(R["bt"][h][r][2]))
        tbl.cell(i, 0).text = nm
        tbl.cell(i, 1).text = "%+.2f per cent (%s)" % (R["bt"][h][worst_r][2], worst_r)
        tbl.cell(i, 2).text = "%.1f" % R["freq"][h]["Pennine"]
        tbl.cell(i, 3).text = "%.1f" % R["freq"][h]["Severn"]
    for row in tbl.rows:
        for c in row.cells:
            for p in c.text_frame.paragraphs:
                p.font.size, p.font.name = Pt(12), "Arial"
    text(s, 457200, 4500000, 11200000, 1600000,
         "Re-run on accident year 2022 from 30 September 2023 with 2019 to 2021, as the Standard (3.3) requires. "
         "Wessex had a wave of claims-management injury claims in 2022; every development that blends those firms "
         "with faster notifiers falls short there, and each of them would have put Severn in the pilot.", 13)
    foot(s, 3)

    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 900000, "The Brackwell order: private cars on cover at 30 September 2026", 24, True, TEAL)
    tbl = s.shapes.add_table(7, 5, Emu(457200), Emu(1400000), Emu(8000000), Emu(3200000)).table
    for j, h in enumerate(["Sales region", "COMP", "TPFT", "TPO", "All"]):
        tbl.cell(0, j).text = h
    tot = [0, 0, 0]
    for i, r in enumerate(K.REG, 1):
        vals = [R["ask_a"][(r, cv)] for cv in ("COMP", "TPFT", "TPO")]
        tot = [x + y for x, y in zip(tot, vals)]
        tbl.cell(i, 0).text = r + (" (pilot)" if r in R["call"] else "")
        for j, v in enumerate(vals + [sum(vals)], 1):
            tbl.cell(i, j).text = format(v, ",")
    tbl.cell(6, 0).text = "Total"
    for j, v in enumerate(tot + [sum(tot)], 1):
        tbl.cell(6, j).text = format(v, ",")
    for row in tbl.rows:
        for c in row.cells:
            for p in c.text_frame.paragraphs:
                p.font.size, p.font.name = Pt(12), "Arial"
    text(s, 8800000, 1500000, 2900000, 3600000, "Region and cover as they stood on 30 September, after the mid-term "
         "address and cover changes effective by then. The order is placed by cover because each cover has its own "
         "discount scale (terms 6).", 12)
    foot(s, 4)
    prs.save(path)


def write_all(golden_dir, gen_dir, R):
    os.makedirs(golden_dir, exist_ok=True)
    F = figures(R)
    write_workbook(os.path.join(golden_dir, K.GOLDEN), R, F)
    write_deck(os.path.join(golden_dir, K.DECK), R, F)
    with open(os.path.join(gen_dir, "figures.json"), "w") as f:
        json.dump(F, f, indent=1, sort_keys=True)
        f.write("\n")
    return F
