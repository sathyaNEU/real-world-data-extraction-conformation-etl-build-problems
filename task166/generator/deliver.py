"""task166 golden deliverables, computed from the shipped pack by calc.py: the designation workbook and the two ALCO
slides, and generator/figures.json, from which the write-up's blocks are drafted.

    python3 deliver.py <target> <golden_dir> <figures.json>"""
from __future__ import annotations

import json
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.util import Emu, Inches, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import postprocess as PP    # noqa: E402

F_BOOK = "overlay_designation_2027.xlsx"
F_DECK = "overlay_designation_alco.pptx"
OWNER = "Guy Morrison"
ORDER = ["Fixed-rate commercial real estate", "Agency MBS", "2023-24 residential mortgages", "Treasury ladder",
         "Indirect auto loans"]
PARTS = [("overlay", "Overlays, the new overlay included"), ("funding", "Funding hedges"), ("loan", "Loan hedges")]
QLAB = ["31 Mar 2027", "30 Jun 2027", "30 Sep 2027", "31 Dec 2027"]


def r10(x):
    return int(10 * round(x / 10.0))


SHARE_WORDS = [(0.5, "half"), (0.6, "three-fifths"), (2 / 3, "two-thirds"), (0.75, "three-quarters"),
               (0.8, "four-fifths"), (0.9, "nine-tenths"), (0.97, "nearly all")]


def share_words(x):
    return min(SHARE_WORDS, key=lambda t: abs(t[0] - x))[1]


def figures(G, prog):
    f = {}
    f["call_pool"] = G.call
    f["call_loss_musd_nearest10"] = r10(G.CRE / 1e6)
    f["call_loss_musd_unrounded"] = round(G.CRE / 1e6, 2)
    f["runner_up"] = "Agency MBS"
    f["runner_up_loss_musd_nearest10"] = int(10 * round(G.MBS / 1e7))
    f["pools"] = {k: dict(principal_musd=round(G.principal[k] / 1e6, 1), loss_musd_nearest10=r10(G.pools[k] / 1e6),
                          loss_musd=round(G.pools[k] / 1e6, 2)) for k in ORDER}
    f["wall_balloon_busd"] = round(G.wall_balloon / 1e9, 1)
    f["wall_extended_busd"] = round(G.wall_extended / 1e9, 1)
    f["wall_share"] = round(G.wall_share, 3)
    f["wall_loans"] = len(G.wall)
    f["wall_share_words"] = share_words(G.wall_share)
    f["m_cpr_2027_pct"] = int(round(100 * G.m_cpr_2027))
    f["m_cpr_trailing_pct"] = int(round(100 * (1 - (1 - G.m_smm_trailing) ** 12)))
    f["planning_cre_rate_pct"] = G.plan.cre
    f["planning_mortgage_rate_pct"] = G.plan.mortgage
    f["programme_musd"] = {k: [round(v / 1e6, 1) for v in prog[k]] for k, _ in PARTS}
    f["quarter_ends"] = QLAB
    f["oos_brier"] = G.oos
    f["oos_brier_2dp"] = {k: round(v, 2) for k, v in G.oos.items() if isinstance(v, float)}
    f["notional_busd"] = 1.2
    f["shock_bp"] = 200
    f["extension_months"] = 36
    f["amortization_years"] = 25
    f["treasury_loss_musd_about"] = r10(G.T / 1e6)
    f["mortgage_loss_musd_about"] = r10(G.M / 1e6)
    f["auto_loss_musd_about"] = r10(G.AUTO / 1e6)
    f["programme_total_musd"] = [round(sum(prog[k][j] for k, _ in PARTS) / 1e6, 1) for j in range(4)]
    f["programme_total_busd"] = [round(sum(prog[k][j] for k, _ in PARTS) / 1e9, 1) for j in range(4)]
    return f


def write_book(path, G, prog, f):
    wb = Workbook()
    ws = wb.active
    ws.title = "Designation"
    bold = Font(name="Calibri", size=11, bold=True)
    head = PatternFill("solid", fgColor="DCE6EC")
    pick = PatternFill("solid", fgColor="F3E7D3")
    ws["A1"] = "Designate the overlay against fixed-rate commercial real estate"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="1F4E5F")
    ws["A2"] = ("$1.2 billion four-year pay-fixed overlay: trades Tuesday 15 December 2026, starts Monday 4 January "
                "2027. Positions at the close on Monday 30 November 2026.")
    ws["A4"] = "Designated pool"
    ws["B4"] = f["call_pool"]
    ws["A5"] = "Averaged +200 bp loss in economic value, $ millions"
    ws["B5"] = f["call_loss_musd_nearest10"]
    ws["C5"] = "to the nearest 10 (policy measure, section 3)"
    ws["C5"].font = Font(name="Calibri", size=10, italic=True, color="5A626B")
    for c in ("A4", "A5", "B4", "B5"):
        ws[c].font = bold
    ws["B5"].alignment = Alignment(horizontal="left")
    hdr = ["Pool", "Principal at 30 Nov 2026 ($ millions)", "Averaged +200 bp loss ($ millions)", "Rank"]
    for j, h in enumerate(hdr):
        c = ws.cell(row=7, column=j + 1, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, k in enumerate(ORDER):
        p = f["pools"][k]
        r = 8 + i
        ws.cell(row=r, column=1, value=k)
        ws.cell(row=r, column=2, value=p["principal_musd"]).number_format = "#,##0.0"
        ws.cell(row=r, column=3, value=p["loss_musd_nearest10"]).number_format = "#,##0"
        ws.cell(row=r, column=4, value=i + 1)
        if i == 0:
            for j in range(4):
                ws.cell(row=r, column=j + 1).fill = pick
    ws.cell(row=13, column=1, value="Losses in the table are rounded to the nearest $10 million.").font = \
        Font(name="Calibri", size=10, italic=True, color="5A626B")
    lines = [
        ("Fixed-rate commercial real estate",
         "%s of balloons fall due from December 2026 to December 2027 (%d loans, mostly the push of December 2021 to "
         "April 2022). At the planning cycle's %.2f per cent five-year rate about %s of that principal is expected to "
         "take the bank's 36-month extension (a tenth paid down, the rest at the posted rate on 25 years): the "
         "extension share each loan's refinance cover carries in the maturity log since 2015. Loans already extended "
         "repay at their extended maturity."
         % ("$%.1f billion" % f["wall_balloon_busd"], f["wall_loans"], f["planning_cre_rate_pct"],
            f["wall_share_words"])),
        ("2023-24 residential mortgages",
         "Expected to prepay about %d per cent a year in 2027 at the planning cycle's %.2f per cent, against about %d "
         "per cent over the last twelve months." % (f["m_cpr_2027_pct"], f["planning_mortgage_rate_pct"],
                                                    f["m_cpr_trailing_pct"])),
        ("Agency MBS", "Each 2020-21 pool at its own prepayment rate over the last twelve factor months; under the "
                       "base case the pools stay as far out of the money as in 2026."),
        ("Treasury ladder", "Contractual coupons and principal."),
        ("Indirect auto loans", "The portfolio's monthly prepayment rate over the last twelve months."),
    ]
    ws.cell(row=15, column=1, value="Run-off behind each figure").font = bold
    for i, (a, b) in enumerate(lines):
        ws.cell(row=16 + i, column=1, value=a).alignment = Alignment(vertical="top")
        c = ws.cell(row=16 + i, column=2, value=b)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=16 + i, start_column=2, end_row=16 + i, end_column=4)
        ws.row_dimensions[16 + i].height = 15 * (len(b) // 88 + 1) + 4
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 34
    ws.column_dimensions["C"].width = 34
    ws.column_dimensions["D"].width = 9
    ws.freeze_panes = "A8"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    p2 = wb.create_sheet("Programme")
    p2["A1"] = "Hedge programme: notional in effect at each quarter-end of 2027"
    p2["A1"].font = Font(name="Calibri", size=14, bold=True, color="1F4E5F")
    p2["A2"] = "$ millions; the treasury system's ALM book, with the new overlay at $1.2 billion from 4 January 2027"
    p2["A2"].font = Font(name="Calibri", size=10, italic=True, color="5A626B")
    for j, h in enumerate(["Part"] + QLAB):
        c = p2.cell(row=4, column=j + 1, value=h)
        c.font = bold
        c.fill = head
        c.alignment = Alignment(horizontal="left" if j == 0 else "right")
    for i, (k, lab) in enumerate(PARTS):
        p2.cell(row=5 + i, column=1, value=lab)
        for j, v in enumerate(f["programme_musd"][k]):
            p2.cell(row=5 + i, column=2 + j, value=v).number_format = "#,##0.0"
    p2.cell(row=8, column=1, value="Programme").font = bold
    for j in range(4):
        c = p2.cell(row=8, column=2 + j, value=round(sum(prog[k][j] for k, _ in PARTS) / 1e6, 1))
        c.number_format = "#,##0.0"
        c.font = bold
    notes = ["The four trades the register carries both as bilateral trades with Ostrander Securities and as cleared "
             "trades are counted once, as cleared: the clearing statement holds the bilateral trade numbers as the "
             "client references of the cleared trades."]
    for t in C.load_register(G.pack):
        if t["Book"] == "ALM" and t["Bank pays"] == "FIXED" and t["Strategy"] == "FUNDING" and \
                C.programme_category(t) == "overlay":
            notes.append("Swap %s is counted as an overlay: it is designated against %s." %
                         (t["Trade No."], t["Hedged item"][0].lower() + t["Hedged item"][1:]))
    notes.append("Amortizing swaps at the notional of the calculation period in effect on each date.")
    for i, n in enumerate(notes):
        c = p2.cell(row=10 + i, column=1, value=n)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        p2.merge_cells(start_row=10 + i, start_column=1, end_row=10 + i, end_column=5)
        p2.row_dimensions[10 + i].height = 32
    p2.column_dimensions["A"].width = 38
    for col in "BCDE":
        p2.column_dimensions[col].width = 15
    p2.freeze_panes = "B5"
    p2.page_setup.orientation = "landscape"
    p2.page_setup.fitToWidth = 1
    p2.page_setup.fitToHeight = 0
    p2.sheet_properties.pageSetUpPr.fitToPage = True
    p3 = wb.create_sheet("Notes")
    nl = [
        ("Measure", "The hedging policy, section 3: a pool's loss in economic value at a month-end is the present value "
                    "of its base-case expected cash flows after that month-end on the planning cycle's base-case zero "
                    "curve, less the same on the curve 200 bp higher, averaged over the month-ends of January to "
                    "December 2027."),
        ("Base case", "ALCO planning cycle for the 2027 plan, approved 21 September 2026: the zero curve, %.2f per cent "
                      "for portfolio jumbo mortgages, %.2f per cent for 15-year conforming loans, %.2f per cent for "
                      "five-year commercial real estate, held after December 2027." %
         (f["planning_mortgage_rate_pct"], G.plan.conf15, f["planning_cre_rate_pct"])),
        ("Pools", "Schedule A of the policy. Agency MBS is the 2020-21 purchases only; the 2023-24 agency pools, "
                  "municipal bonds and agency multifamily securities in the account are not in it. Floating-rate "
                  "commercial real estate loans are not in the fixed-rate pool."),
        ("Eligibility", "Every pool holds more than the $1.2 billion notional at the as-of."),
        ("Credit", "Cash flows before credit losses, as the policy defines them."),
        ("Files", "Pulled Thursday 3 December 2026; positions at the close on Monday 30 November 2026."),
    ]
    for i, (a, b) in enumerate(nl):
        p3.cell(row=1 + i, column=1, value=a).font = bold
        c = p3.cell(row=1 + i, column=2, value=b)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        p3.row_dimensions[1 + i].height = 46 if len(b) > 110 else 18
    p3.column_dimensions["A"].width = 14
    p3.column_dimensions["B"].width = 110
    p3.page_setup.orientation = "landscape"
    p3.page_setup.fitToWidth = 1
    p3.page_setup.fitToHeight = 0
    p3.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def write_deck(path, G, f):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    ink = RGBColor(0x1D, 0x23, 0x2A)
    grey = RGBColor(0x5A, 0x62, 0x6B)
    accent = RGBColor(0x1F, 0x4E, 0x5F)

    def text(slide, x, y, w, h, lines, size=18, bold_first=False, color=ink, after=8):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, ln in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = ln
            p.font.size = Pt(size)
            p.font.name = "Calibri"
            p.font.color.rgb = color
            p.font.bold = bold_first and i == 0
            p.space_after = Pt(after)
        return tb

    def strip(slide, n, src):
        text(slide, 0.6, 7.0, 11.0, 0.35, [src], size=10, color=grey)
        text(slide, 12.2, 7.0, 0.6, 0.35, [str(n)], size=10, color=grey)

    s1 = prs.slides.add_slide(blank)
    text(s1, 0.6, 0.4, 12.1, 1.0, ["Designate the $1.2 billion overlay against fixed-rate commercial real estate"],
         size=30, bold_first=True, color=accent)
    text(s1, 0.6, 1.35, 12.1, 0.6, ["Averaged +200 bp loss in economic value over the month-ends of 2027: $%d million "
                                    "(to the nearest $10 million)" % f["call_loss_musd_nearest10"]],
         size=22, bold_first=True)
    text(s1, 0.6, 2.25, 6.6, 4.4, [
        "About $%.1f billion of the pool's balloons fall due from December 2026 to December 2027, most of them "
        "written in the early-2022 push on pro forma rents. At the planning cycle's %.2f per cent few of those "
        "properties' incomes can carry a new loan of their balance; about %s of that principal is expected to take "
        "the bank's 36-month extension." % (f["wall_balloon_busd"], f["planning_cre_rate_pct"], f["wall_share_words"]),
        "Agency MBS is next, at about $%d million." % f["runner_up_loss_musd_nearest10"],
        "The 2023-24 mortgages lose most at last year's prepayment speed, but at %.2f per cent they are expected to "
        "prepay about %d per cent a year in 2027." % (f["planning_mortgage_rate_pct"], f["m_cpr_2027_pct"]),
    ], size=17, after=12)
    rows, cols = 6, 3
    tbl = s1.shapes.add_table(rows, cols, Inches(7.6), Inches(2.35), Inches(5.1), Inches(2.6)).table
    tbl.columns[0].width = Inches(2.9)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.1)
    hd = ["Pool", "Principal, $ bn", "Loss, $ m"]
    for j, h in enumerate(hd):
        cell = tbl.cell(0, j)
        cell.text = h
        cell.text_frame.paragraphs[0].font.size = Pt(13)
        cell.text_frame.paragraphs[0].font.bold = True
    for i, k in enumerate(ORDER):
        p = f["pools"][k]
        vals = [k, "%.2f" % (p["principal_musd"] / 1000.0), "%d" % p["loss_musd_nearest10"]]
        for j, v in enumerate(vals):
            cell = tbl.cell(i + 1, j)
            cell.text = v
            cell.text_frame.paragraphs[0].font.size = Pt(13)
            cell.text_frame.paragraphs[0].font.bold = i == 0
    text(s1, 7.6, 5.05, 5.1, 0.5, ["Losses to the nearest $10 million; principal at 30 November 2026."], size=11,
         color=grey)
    text(s1, 0.6, 6.45, 12.1, 0.4, ["$1.2 billion pay-fixed for four years: trades Tuesday 15 December 2026, starts "
                                    "Monday 4 January 2027."], size=14, color=grey)
    strip(s1, 1, "Source: ALM analysis of positions at 30 November 2026; hedging policy section 3; 2027 planning "
                 "cycle, base case.")
    s2 = prs.slides.add_slide(blank)
    tot = [sum(f["programme_musd"][k][j] for k, _ in PARTS) for j in range(4)]
    text(s2, 0.6, 0.35, 12.1, 0.9, ["The programme's notional runs from $%.1f billion to $%.1f billion through 2027 "
                                    "as loan hedges mature" % (tot[0] / 1000.0, tot[-1] / 1000.0)],
         size=26, bold_first=True, color=accent)
    cd = CategoryChartData()
    cd.categories = QLAB
    for k, lab in PARTS:
        cd.add_series(lab, f["programme_musd"][k], number_format="#,##0.0")
    gf = s2.shapes.add_chart(XL_CHART_TYPE.COLUMN_STACKED, Inches(0.7), Inches(1.25), Inches(11.9), Inches(5.6), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(14)
    cols_ = [RGBColor(0x1F, 0x4E, 0x5F), RGBColor(0x8A, 0xA8, 0xB8), RGBColor(0xC9, 0x8B, 0x3B)]
    for s, c in zip(ch.plots[0].series, cols_):
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = c
    pl = ch.plots[0]
    pl.gap_width = 70
    pl.has_data_labels = True
    dl = pl.data_labels
    dl.number_format = "#,##0.0"
    dl.number_format_is_linked = False
    dl.font.size = Pt(13)
    dl.position = XL_LABEL_POSITION.CENTER
    va = ch.value_axis
    va.has_major_gridlines = True
    va.tick_labels.font.size = Pt(12)
    va.tick_labels.number_format = "#,##0"
    va.tick_labels.number_format_is_linked = False
    va.has_title = True
    va.axis_title.text_frame.text = "$ millions"
    va.axis_title.text_frame.paragraphs[0].font.size = Pt(12)
    ch.category_axis.tick_labels.font.size = Pt(14)
    strip(s2, 2, "Source: treasury system swap register, amortization schedules and clearing statement at 30 "
                 "November 2026; the new overlay included from 4 January 2027.")
    prs.save(path)


def fix_embedded(path, created, modified):
    """the chart's embedded workbook carries its writer's clock: give it the deck's owner and stamps"""
    import tempfile
    import zipfile
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    out = []
    for name, data in items:
        if name.startswith("ppt/embeddings/") and name.endswith(".xlsx"):
            tmp = tempfile.mkdtemp(prefix="b166_emb_")
            p = os.path.join(tmp, "e.xlsx")
            open(p, "wb").write(data)
            PP.normalize_ooxml(p, OWNER, OWNER, created, modified, company="Carrick Valley Bank")
            data = open(p, "rb").read()
            os.remove(p)
            os.rmdir(tmp)
        out.append((name, data))
    with zipfile.ZipFile(path, "w") as z:
        for name, data in out:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def main(target, golden, fig_path):
    os.makedirs(golden, exist_ok=True)
    G = C.golden(target)
    G.pack = target
    G.oos = C.oos_table(G)
    prog = C.programme(target)
    f = figures(G, prog)
    write_book(os.path.join(golden, F_BOOK), G, prog, f)
    write_deck(os.path.join(golden, F_DECK), G, f)
    PP.normalize_ooxml(os.path.join(golden, F_BOOK), OWNER, OWNER, "2026-12-04T14:12:00Z", "2026-12-11T21:37:00Z",
                       excel=True, company="Carrick Valley Bank")
    fix_embedded(os.path.join(golden, F_DECK), "2026-12-07T15:02:00Z", "2026-12-11T22:05:00Z")
    PP.normalize_ooxml(os.path.join(golden, F_DECK), OWNER, OWNER, "2026-12-07T15:02:00Z", "2026-12-11T22:05:00Z",
                       company="Carrick Valley Bank")
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return f


if __name__ == "__main__":
    main(*sys.argv[1:4])
