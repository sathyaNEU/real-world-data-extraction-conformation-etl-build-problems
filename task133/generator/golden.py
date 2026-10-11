"""The golden deliverables: the allowance workbook and the two board slides."""
import copy
import datetime as dt
import os
import sys

import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Cm, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import estimators as E
import officex as OX
import world as W
import postprocess as P

TASK = os.path.dirname(HERE)
PREPARED = dt.datetime(2026, 10, 9, 16, 20)
NAVY = RGBColor(0x1E, 0x2B, 0x3C)
GREY = RGBColor(0x5B, 0x66, 0x70)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
# the migration chart's four states, checked for colour-blind separation as a set: stage 1, stage 2, stage 3, closed
STATE = [RGBColor(0x2A, 0x78, 0xD6), RGBColor(0xED, 0xA1, 0x00), RGBColor(0xE3, 0x49, 0x48), RGBColor(0x62, 0x50, 0xD6)]
ORDER = [("PL36", 1), ("PL36", 2), ("PL60", 1), ("PL60", 2)]
NOW = ["stage 1", "stage 2", "stage 3", "closed"]


def k(x):
    return int(round(x / 1000.0)) * 1000


def money(x):
    return "${:,}".format(k(x))


def figures(target):
    s = E.solve(target)
    lgd = E.realised_lgd(target)
    fy = pd.read_csv(os.path.join(target, E.F["defaults"]))
    fy["q"] = [((int(m[5:7]) - 7) % 12) // 3 + 1 for m in fy["default_month"]]
    cells = fy.groupby(["product", "q"]).agg(loans=("loan_no", "size"), bal=("balance_at_default", "sum"))
    mig = E.migration(target)
    return dict(s=s, lgd=lgd, lgd_cells=cells, mig=mig)


def workbook(f, path):
    s, lgd, cells, mig = f["s"], f["lgd"], f["lgd_cells"], f["mig"]
    thin = Side(style="thin", color="BFC5CC")
    head_fill = PatternFill("solid", fgColor="1E2B3C")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Allowance"
    ws["A1"] = "Personal loans (PL36, PL60): collective ECL allowance at 30 September 2026"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Credit Risk Reporting, 9 October 2026. CRM-ECL-04 v4.2; scenarios approved 18 September 2026."
    ws["A2"].font = Font(italic=True, color="5B6670")
    rows = [("Collective ECL allowance (AUD)", k(s["total"]), '"$"#,##0'),
            ("Stage 1 allowance (AUD)", k(s["stage1"]), '"$"#,##0'),
            ("Stage 2 allowance (AUD)", k(s["stage2"]), '"$"#,##0'),
            (None, None, None),
            ("Loans in stage 1", s["n1"], "#,##0"),
            ("Loans in stage 2", s["n2"], "#,##0"),
            ("Loans in stage 3, assessed under CRM-ECL-06", s["n3"], "#,##0"),
            ("Probability-weighted PD multiplier", round(s["mult"], 2), "0.00")]
    for i, (lab, v, fmt) in enumerate(rows, 4):
        if lab is None:
            continue
        ws.cell(row=i, column=1, value=lab)
        c = ws.cell(row=i, column=2, value=v)
        c.number_format = fmt
    for c in (ws["A4"], ws["B4"]):
        c.font = Font(bold=True)
    ws["A13"] = ("Source: loan system extract ECL_QE_BOOK at close of business 30 September 2026 (run 1 October); "
                 "PLPD-2026.06 curve and development sample; Q1 FY27 scenario sheet.")
    ws["A13"].font = Font(italic=True, color="5B6670")
    ws.column_dimensions["A"].width = 46
    ws.column_dimensions["B"].width = 16

    ws = wb.create_sheet("Realised LGD")
    ws["A1"] = "2023-24 defaults: share of the balance at default not recovered, at 30 September 2026 (CRM-ECL-04 3.3)"
    ws["A1"].font = Font(bold=True, size=12)
    hdr = ["Product", "Quarter of default", "Loans", "Balance at default (AUD)", "Realised loss (%)", "LGD in use (%)"]
    ws.append([])
    ws.append(hdr)
    for j in range(1, len(hdr) + 1):
        c = ws.cell(row=3, column=j)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for p in ("PL36", "PL60"):
        for q in (1, 2, 3, 4):
            ws.append([p, E.QUARTERS[q], int(cells.loc[(p, q), "loans"]), round(float(cells.loc[(p, q), "bal"]), 2),
                       round(lgd[(p, q)], 1), int(round(E.LGD[p] * 100))])
    for r in ws.iter_rows(min_row=4, max_row=ws.max_row):
        r[2].number_format = "#,##0"
        r[3].number_format = "#,##0.00"
        r[4].number_format = "0.0"
        r[5].number_format = "0"
    for col, wd in zip("ABCDEF", [10, 19, 8, 22, 15, 13]):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[3].height = 30
    ws.freeze_panes = "A4"

    ws = wb.create_sheet("Stage migration")
    ws["A1"] = "Loans in stage 1 or 2 at 30 June 2026: where they stand at 30 September 2026"
    ws["A1"].font = Font(bold=True, size=12)
    ws.append([])
    hdr = ["Product", "Stage at 30 June", "Stage 1", "Stage 2", "Stage 3", "Closed", "Loans at 30 June"]
    ws.append(hdr)
    for j in range(1, len(hdr) + 1):
        c = ws.cell(row=3, column=j)
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for p, s0 in ORDER:
        vals = [mig[(p, s0, x)] for x in NOW]
        ws.append([p, "Stage %d" % s0] + vals + [sum(vals)])
    for r in ws.iter_rows(min_row=4, max_row=ws.max_row):
        for c in r[2:]:
            c.number_format = "#,##0"
            c.border = Border(bottom=thin)
    ws["A9"] = "Stage at 30 September under CRM-ECL-04 section 2; closed means repaid, settled or written off by then."
    ws["A9"].font = Font(italic=True, color="5B6670")
    for col, wd in zip("ABCDEFG", [10, 16, 10, 10, 10, 10, 16]):
        ws.column_dimensions[col].width = wd

    ws = wb.create_sheet("Method")
    notes = [
        "Scope: PL36 and PL60 loans open at close of business 30 September 2026. Loans 90 or more days past due are stage 3 "
        "and are assessed under CRM-ECL-06.",
        "Stage 2: 30 or more days past due, a hardship arrangement in force on the date (start to end, both included, not "
        "from the day it is cancelled), or a behaviour score 60 or more points below origination on v4 from the month-end "
        "run on the position at the date; v3 origination scores converted as 1.12 x v3 - 18, rounded. At 30 June the "
        "June month-end run (made 1 July) supplies the scores.",
        "PD(k): the PLPD-2026.06 curve gives, for every loan drawn in the development window, the share defaulted by each "
        "month on book. A loan a months on book that is still open and has not defaulted takes (C(a+k) - C(a+k-1)) / S(a), "
        "where S(a) is the share of the development sample still open and never defaulted at the end of month a "
        "(1 - C(a) less the share repaid in full by then). Stage 2 PD carries the 2.4 scalar. A loan past its maturity "
        "outside stage 3 has one month remaining (3.2).",
        "EAD re-amortises the current balance over the remaining term at the contract rate; each month is discounted at "
        "the contract rate; LGD 70 per cent PL36, 76 per cent PL60; scenarios 55 / 30 / 15 per cent on multipliers "
        "1.00 / 1.30 / 0.80 (weighted %.2f)." % s["mult"],
        "Realised loss (3.3): receipts after default to 30 September 2026 from the Collections receipts file, plus each "
        "sold account's share of the March 2026 sale (face value at cut-off x %.2f cents), each taken at the end of the "
        "month received and discounted to the default month end at the contract rate; cured loans lose nothing." % W.SALE_PRICE_CENTS,
        "Amounts are rounded to the nearest thousand dollars from loan-level results, so stage amounts may not add exactly.",
    ]
    for i, t in enumerate(notes, 1):
        ws.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 120
    # the quarter's workbook is rolled forward (save as) from the one Credit Risk Reporting set up in February 2023
    OX.xlsx_from_openpyxl(wb, path, "Joseph Mitchell", "Joseph Mitchell", dt.datetime(2023, 2, 6, 9, 31, 44), PREPARED, seed=1009)


def _nudge(label, dx, dy):
    """move one data label off its default spot by a fraction of the chart, as dragging it in PowerPoint records"""
    dLbl = label._get_or_add_dLbl()
    idx = dLbl.find(qn("c:idx"))
    lay = dLbl.find(qn("c:layout"))
    if lay is None:
        lay = dLbl.makeelement(qn("c:layout"), {})
        idx.addnext(lay)
    for ch in list(lay):
        lay.remove(ch)
    ml = lay.makeelement(qn("c:manualLayout"), {})
    lay.append(ml)
    for tag, v in (("c:x", dx), ("c:y", dy)):
        e = ml.makeelement(qn(tag), {"val": "%.4f" % v})
        ml.append(e)


def deck(f, path):
    s, mig = f["s"], f["mig"]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Cm(33.867), Cm(19.05)
    blank = prs.slide_layouts[6]

    def title(slide, text, sub=None):
        tb = slide.shapes.add_textbox(Cm(1.6), Cm(1.0), Cm(30.5), Cm(2.6))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = text
        r.font.size = Pt(24)
        r.font.bold = True
        r.font.color.rgb = NAVY
        if sub:
            p2 = tf.add_paragraph()
            r2 = p2.add_run()
            r2.text = sub
            r2.font.size = Pt(13)
            r2.font.color.rgb = GREY

    def footer(slide, n):
        tb = slide.shapes.add_textbox(Cm(1.6), Cm(17.7), Cm(30.5), Cm(0.8))
        r = tb.text_frame.paragraphs[0].add_run()
        r.text = "Bellbird Personal Finance  |  Board, 23 October 2026  |  Credit Risk Reporting  |  %d" % n
        r.font.size = Pt(9)
        r.font.color.rgb = GREY

    s1 = prs.slides.add_slide(blank)
    title(s1, "Book a collective ECL allowance of %s at 30 September 2026" % money(s["total"]),
          "Stage 1 %s and stage 2 %s; %s loans in stage 3 are assessed separately under CRM-ECL-06"
          % (money(s["stage1"]), money(s["stage2"]), "{:,}".format(s["n3"])))
    rows = [("", "Loans", "Allowance"),
            ("Stage 1", "{:,}".format(s["n1"]), money(s["stage1"])),
            ("Stage 2", "{:,}".format(s["n2"]), money(s["stage2"])),
            ("Collective allowance", "{:,}".format(s["n1"] + s["n2"]), money(s["total"]))]
    tbl = s1.shapes.add_table(len(rows), 3, Cm(1.6), Cm(5.4), Cm(19.0), Cm(5.2)).table
    for j, w in enumerate([8.6, 4.6, 5.8]):
        tbl.columns[j].width = Cm(w)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            cell = tbl.cell(i, j)
            cell.text = v
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if i == 0 else (RGBColor(0xEE, 0xF1, 0xF4) if i == len(rows) - 1 else RGBColor(0xFF, 0xFF, 0xFF))
            para = cell.text_frame.paragraphs[0]
            if not para.runs:
                para.add_run()
            para.runs[0].font.size = Pt(16)
            para.runs[0].font.bold = i in (0, len(rows) - 1)
            para.runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else NAVY
            if j >= 1:
                para.alignment = PP_ALIGN.RIGHT
    note = s1.shapes.add_textbox(Cm(1.6), Cm(11.6), Cm(30.5), Cm(4.0)).text_frame
    note.word_wrap = True
    r = note.paragraphs[0].add_run()
    r.text = ("Each performing loan's monthly default probability comes from the PLPD-2026.06 curve from its months on book, "
              "conditioned on the share of the development loans still open and not in default at that point; stage 2 "
              "carries the 2.4 scalar and the scenarios are weighted 55 / 30 / 15 per cent (multiplier %.2f). "
              "Amounts to the nearest thousand dollars." % s["mult"])
    r.font.size = Pt(12)
    r.font.color.rgb = GREY
    src = s1.shapes.add_textbox(Cm(1.6), Cm(16.8), Cm(30.5), Cm(0.8)).text_frame.paragraphs[0].add_run()
    src.text = "Source: loan system extract at 30 September 2026; PLPD-2026.06 curve; scenarios approved 18 September 2026"
    src.font.size = Pt(9)
    src.font.color.rgb = GREY
    footer(s1, 1)

    s2 = prs.slides.add_slide(blank)
    worse = sum(mig[(p, 1, x)] for p in ("PL36", "PL60") for x in ("stage 2", "stage 3"))
    back = sum(mig[(p, 2, "stage 1")] for p in ("PL36", "PL60"))
    title(s2, "%s stage 1 loans moved to stage 2 or 3 this quarter and %s stage 2 loans returned to stage 1"
          % ("{:,}".format(worse), "{:,}".format(back)),
          "Loans in stage 1 or stage 2 at 30 June 2026, by where they stand at 30 September 2026")
    cd = CategoryChartData()
    cd.categories = ["%s, stage %d at 30 June" % (p, s0) for p, s0 in ORDER]
    names = {"stage 1": "Stage 1 at 30 September", "stage 2": "Stage 2", "stage 3": "Stage 3", "closed": "Closed"}
    for x in NOW:
        cd.add_series(names[x], [mig[(p, s0, x)] for p, s0 in ORDER])
    gf = s2.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED_100, Cm(1.6), Cm(4.4), Cm(30.5), Cm(12.3), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.TOP
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(11)
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.tick_labels.number_format = "0%"
    ch.value_axis.tick_labels.number_format_is_linked = False
    ch.value_axis.tick_labels.font.size = Pt(10)
    ch.category_axis.tick_labels.font.size = Pt(11)
    ch.category_axis.reverse_order = True
    plot = ch.plots[0]
    plot.gap_width = 55
    plot.overlap = 100
    for ser, col, x in zip(plot.series, STATE, NOW):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = col
        ser.format.line.color.rgb = WHITE
        ser.format.line.width = Pt(1.5)
        for idx, (p, s0) in enumerate(ORDER):
            v = mig[(p, s0, x)]
            share = v / sum(mig[(p, s0, y)] for y in NOW)
            dl = ser.points[idx].data_label
            dl.has_text_frame = True
            dl.text_frame.text = "{:,}".format(v)
            run = dl.text_frame.paragraphs[0].runs[0]
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = WHITE if x != "stage 2" and share >= 0.03 else NAVY
            if share < 0.03:
                # too thin a sliver to hold its number: the label sits just below the bar
                dl.position = XL_LABEL_POSITION.CENTER
                _nudge(dl, 0.0, 0.085)
    src = s2.shapes.add_textbox(Cm(1.6), Cm(16.8), Cm(30.5), Cm(0.8)).text_frame.paragraphs[0].add_run()
    src.text = ("Source: loan system extracts at 30 June and 30 September 2026; June month-end scoring run (1 July); hardship "
                "register at 30 September. Stages under CRM-ECL-04 section 2; closed = repaid, settled or written off.")
    src.font.size = Pt(9)
    src.font.color.rgb = GREY
    footer(s2, 2)
    prs.core_properties.author = "Joseph Mitchell"
    prs.core_properties.last_modified_by = "Joseph Mitchell"
    prs.core_properties.title = "ECL allowance, Q1 FY27"
    prs.core_properties.created = PREPARED
    prs.core_properties.modified = PREPARED
    prs.core_properties.revision = 3
    prs.save(path)


def build(target=None, out=None):
    target = target or os.path.join(TASK, "target")
    out = out or os.path.join(TASK, "golden")
    os.makedirs(out, exist_ok=True)
    f = figures(target)
    wbp = os.path.join(out, "ecl_allowance_2026Q3.xlsx")
    workbook(f, wbp)
    dp = os.path.join(out, "board_ecl_q3_2026.pptx")
    deck(f, dp)
    P.office_container(dp, "Joseph Mitchell", "Joseph Mitchell", dt.datetime(2026, 10, 8, 16, 41), PREPARED,
                       "Microsoft Office PowerPoint", revision=3)
    P.deterministic_embeddings(dp, dt.datetime(2026, 10, 8, 16, 41))
    for p in (wbp, dp):
        ts = W.posix(PREPARED)
        os.utime(p, (ts, ts))
    return f


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    f = build(a.target, a.out)
    s = f["s"]
    print("total", k(s["total"]), "stage1", k(s["stage1"]), "stage2", k(s["stage2"]))
    print("lgd", {"%s Q%d" % key: round(v, 1) for key, v in sorted(f["lgd"].items())})
    print("migration", f["mig"])
