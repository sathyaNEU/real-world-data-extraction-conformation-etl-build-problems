"""The golden deliverables (the committee deck and the capacity workbook), figures.json and submission.md, all from
the golden analysis on the cut pack."""
import datetime as dt
import json
import os

import analysis as A
import pack as PK

DECK = "capital_allocation_2027.pptx"
BOOK = "strategy_capacity_2027.xlsx"
ORDER = ["SCM", "MCV", "LCQ"]


def m(x):
    return int(round(x / 1e6))


def figures(R):
    g = R["priced"]["golden"]
    fig = {"call": R["call"], "runner_up": R["runner"], "gap_gbp_m": m(g[R["call"]]["net"]) - m(g[R["runner"]]["net"]),
           "constants": {"aum_gbp_m": 400, "pence_per_pound": 100, "adv_sessions": 20, "vol_sessions": 60},
           "candidates": {c: dict(name=g[c]["name"], gross_gbp_m=m(g[c]["gross"]), cost_gbp_m=m(g[c]["cost"]),
                                  net_gbp_m=m(g[c]["net"]), traded_gbp_m=m(g[c]["traded"]),
                                  rebalances=g[c]["rebalances"]) for c in ORDER},
           "ask_shortfall_bps": {"%s Q%d" % (n, q): round(v, 1) for (n, q), v in sorted(R["ask_a"].items())},
           "ask_traded_gbp_m": {"%s H%d" % (n, h): m(v) for (n, h), v in sorted(R["ask_b"].items())},
           "routes": {k: {c: round(v[c]["net"] / 1e6, 2) for c in ORDER} for k, v in R["priced"].items()},
           "raw": {"net": {c: round(g[c]["net"] / 1e6, 3) for c in ORDER},
                   "cost": {c: round(g[c]["cost"] / 1e6, 3) for c in ORDER},
                   "shortfall": {"%s Q%d" % (n, q): round(v, 4) for (n, q), v in sorted(R["ask_a"].items())},
                   "traded": {"%s H%d" % (n, h): round(v / 1e6, 4) for (n, h), v in sorted(R["ask_b"].items())}}}
    return fig


def workbook(path, fig):
    c = fig["candidates"]
    alloc = [["Strategy", "Code", "Gross alpha a year (GBP m)", "Trading cost a year at GBP 400m (GBP m)",
              "Alpha kept a year (GBP m)", "Value traded in the twelve months (GBP m)", "Rebalances"]]
    for k in ORDER:
        alloc.append([c[k]["name"], k, c[k]["gross_gbp_m"], c[k]["cost_gbp_m"], c[k]["net_gbp_m"],
                      c[k]["traded_gbp_m"], c[k]["rebalances"]])
    alloc += [[], ["Recommended", c[fig["call"]]["name"]], ["Runner-up", c[fig["runner_up"]]["name"]],
              ["Difference (GBP m a year)", fig["gap_gbp_m"]],
              ["Basis", "IC-07: backtest gross alpha 2015 to 2026 less the shortfall the rebalances of December 2025 "
                        "to November 2026 would pay at GBP 400m, priced on the desk's 2025 and 2026 orders"]]
    sf = [["Live strategy", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026 (to 30 Nov)"]]
    for n in A.LIVE_NAMES:
        sf.append([n] + [fig["ask_shortfall_bps"]["%s Q%d" % (n, q)] for q in (1, 2, 3, 4)])
    sf += [[], ["Implementation shortfall, basis points, value-weighted, cost positive (TCA standard rev. 4)"]]
    tv = [["Live strategy", "H1 2026 (GBP m)", "H2 2026 to 30 Nov (GBP m)"]]
    for n in A.LIVE_NAMES:
        tv.append([n] + [fig["ask_traded_gbp_m"]["%s H%d" % (n, h)] for h in (1, 2)])
    PK.xlsx(path, [("Allocation", alloc, (34, 8, 24, 30, 22, 30, 11)), ("Shortfall 2026", sf, (26, 12, 12, 12, 20)),
                   ("Traded 2026", tv, (26, 18, 26))], "Wealdmoor Systematic Equities",
            dt.datetime(2026, 12, 3, 9, 20), dt.datetime(2026, 12, 4, 17, 46))


def deck(path, fig):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.util import Emu, Pt
    c = fig["candidates"]
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, s, size, bold=False, color="1D2B36"):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = s
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = RGBColor.from_string(color)
        return tf
    s1 = prs.slides.add_slide(blank)
    win, run = c[fig["call"]], c[fig["runner_up"]]
    text(s1, 457200, 380000, 11200000, 900000,
         "%s should launch the GBP 400m mandate: it keeps GBP %dm of alpha a year" % (win["name"], win["net_gbp_m"]),
         26, True)
    text(s1, 457200, 1250000, 11200000, 900000,
         "Runner-up: %s at GBP %dm a year, GBP %dm behind. Priced on the twelve months of rebalances to November "
         "2026 at GBP 400m, each trade at the shortfall the desk's own orders paid at its share of the stock's "
         "daily traded value." % (run["name"], run["net_gbp_m"], fig["gap_gbp_m"]), 14)
    cd = CategoryChartData()
    cd.categories = [c[k]["name"] for k in ORDER]
    cd.add_series("Gross alpha a year (GBP m)", [c[k]["gross_gbp_m"] for k in ORDER])
    cd.add_series("Alpha kept at GBP 400m (GBP m)", [c[k]["net_gbp_m"] for k in ORDER])
    gf = s1.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(2300000), Emu(11200000),
                             Emu(4200000), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    plot = ch.plots[0]
    plot.has_data_labels = True
    plot.data_labels.font.size = Pt(11)
    plot.data_labels.number_format = "0"
    plot.data_labels.number_format_is_linked = False
    for ser, col in zip(plot.series, ("9AA9B5", "1F5A85")):
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = RGBColor.from_string(col)
    ch.value_axis.has_major_gridlines = False
    ch.value_axis.tick_labels.font.size = Pt(10)
    ch.category_axis.tick_labels.font.size = Pt(11)
    s2 = prs.slides.add_slide(blank)
    text(s2, 457200, 380000, 11200000, 700000, "What each candidate keeps at GBP 400m", 24, True)
    rows = [["Strategy", "Gross alpha", "Trading cost", "Alpha kept", "Traded in the twelve months"]]
    for k in ORDER:
        rows.append([c[k]["name"], "GBP %dm" % c[k]["gross_gbp_m"], "GBP %dm" % c[k]["cost_gbp_m"],
                     "GBP %dm" % c[k]["net_gbp_m"], "GBP %dm" % c[k]["traded_gbp_m"]])
    tbl = s2.shapes.add_table(len(rows), 5, Emu(457200), Emu(1300000), Emu(11200000), Emu(2200000)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            cell = tbl.cell(i, j)
            cell.text = v
            cell.text_frame.paragraphs[0].font.size = Pt(13)
            cell.text_frame.paragraphs[0].font.bold = i == 0
    text(s2, 457200, 3700000, 11200000, 1600000,
         "The live books' 2026 shortfall by quarter and value traded by half year are in strategy_capacity_2027.xlsx.",
         13)
    prs.core_properties.author = "Carole Shaw"
    prs.core_properties.last_modified_by = "Carole Shaw"
    prs.core_properties.title = "2027 capital allocation"
    prs.core_properties.created = dt.datetime(2026, 12, 3, 10, 2)
    prs.core_properties.modified = dt.datetime(2026, 12, 4, 18, 11)
    prs.core_properties.revision = 7
    import io
    import re
    import zipfile
    buf = io.BytesIO()
    prs.save(buf)
    src = zipfile.ZipFile(io.BytesIO(buf.getvalue()))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for info in sorted(src.infolist(), key=lambda i: i.filename):
            data = src.read(info.filename)
            if info.filename == "docProps/app.xml":
                data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Office PowerPoint"
                              b"</Application>", data)
            if info.filename.endswith(".xlsx"):
                # the chart's embedded workbook carries the writer's clock: give it the deck's own save time
                inner = zipfile.ZipFile(io.BytesIO(data))
                ob = io.BytesIO()
                with zipfile.ZipFile(ob, "w", zipfile.ZIP_DEFLATED) as iz:
                    for ii in sorted(inner.infolist(), key=lambda i: i.filename):
                        d2 = inner.read(ii.filename)
                        if ii.filename == "docProps/core.xml":
                            d2 = re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)",
                                        b"\\g<1>2026-12-04T18:11:00Z\\g<2>", d2)
                        zj = zipfile.ZipInfo(ii.filename, date_time=(2026, 12, 4, 18, 11, 0))
                        zj.compress_type = zipfile.ZIP_DEFLATED
                        iz.writestr(zj, d2)
                data = ob.getvalue()
            zi = zipfile.ZipInfo(info.filename, date_time=(2026, 12, 4, 18, 11, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(zi, data)


def write_all(target, golden, task_dir):
    R = A.run(target)
    fig = figures(R)
    os.makedirs(golden, exist_ok=True)
    workbook(os.path.join(golden, BOOK), fig)
    deck(os.path.join(golden, DECK), fig)
    import writeup
    writeup.write(os.path.join(task_dir, "submission.md"), fig)
    return R, fig
