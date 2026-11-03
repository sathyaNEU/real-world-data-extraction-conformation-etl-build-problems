"""The golden figures, computed forward from the clean truth with the fund's own mechanics, and the two golden
deliverables: change_pricing_2025-26.xlsx and board_review_2025-26.pptx."""
import json
import os

import numpy as np

import fund as F
import postprocess as PP
import records as R
import world as W
from world import D, DAYS, IDX

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
CHANGES = [("A", "Value sleeve to a tracker"), ("B", "Growth sleeve to a tracker"), ("C", "Higher trigger (12%)"),
           ("D", "Earlier restoration (within 6%)"), ("E", "Equitised liquidity sleeve")]
NAMES = dict(CHANGES)


def r10(x):
    return int(np.floor(x / 10 + 0.5) * 10)


def episodes(state, i0):
    """(first reduced valuation point, first full valuation point after) for each reduction in a state list"""
    out, start = [], None
    for j, s in enumerate(state):
        if s == "REDUCED" and start is None:
            start = j
        if s != "REDUCED" and start is not None:
            out.append((DAYS[i0 + start], DAYS[i0 + j]))
            start = None
    if start is not None:
        out.append((DAYS[i0 + start], None))
    return out


def main_figures(S):
    act, world, inp = S["act"], S["world"], S["inp"]
    rec = act["rec"]
    i0, i1 = F.YEAR0, F.YEAR1
    pb = rec["price"]["B Acc"]
    RB = pb[i1] / pb[i0] - 1
    tr = world["ix"]["tr_noon"]
    Rbench = tr[i1] / tr[i0] - 1
    out = dict(R_bacc=RB, R_bench=Rbench, short=(Rbench - RB) * 1e4)
    reps = {}
    for ch, _ in CHANGES:
        rp = F.replay(inp, ch)
        reps[ch] = rp
        out["R_" + ch] = rp["price"][-1] / rp["price"][0] - 1
        out["bp_" + ch] = (out["R_" + ch] - RB) * 1e4
        out["ep_" + ch] = episodes(rp["state"], i0)
    ranked = sorted((c for c, _ in CHANGES), key=lambda c: -out["bp_" + c])
    out["call"], out["runner_up"] = ranked[0], ranked[1]
    out["gap"] = out["bp_" + ranked[0]] - out["bp_" + ranked[1]]
    out["ranked"] = ranked
    # the year as it ran: the trigger, the reduction and the restoration
    st = rec["state"]
    out["ep_actual"] = episodes(st[i0:i1 + 1], i0)
    trig = [DAYS[i] for i in range(i0, i1 + 1) if rec["dd"][i] > W.DD_IN and st[i] == "FULL"]
    out["trigger_day"] = trig[0]
    out["dd_trigger"] = rec["dd"][IDX[trig[0]]]
    # the replay with the value sleeve as a tracker: its deepest fall below the 63-point high
    p = reps["A"]["price"]
    hist = [round(x, 2) for x in pb[i0 - W.WINDOW + 1:i0 + 1]]
    worst, wday = 0.0, None
    for j in range(1, len(p)):
        hist.append(round(p[j], 2))
        x = 1 - hist[-1] / max(hist[-W.WINDOW:])
        if x > worst:
            worst, wday = x, DAYS[i0 + j]
    out["A_worst"], out["A_worst_day"] = worst, wday
    hist = [round(x, 2) for x in pb[i0 - W.WINDOW + 1:i1 + 1]]
    out["actual_worst"] = max(rec["dd"][i0:i1 + 1])
    return out, reps


def ask_figures(S):
    act, world = S["act"], S["world"]
    inc = R.income_golden(act)
    cost = R.costs_golden(act)
    aim = R.aim_golden(world, act, S["settled"])
    return inc, cost, aim


def all_figures(S, target):
    M, reps = main_figures(S)
    inc, cost, aim = ask_figures(S)
    Fg = dict(M=M, reps=reps, inc=inc, cost=cost, aim=aim)
    gold = os.path.join(TASK, "golden")
    os.makedirs(gold, exist_ok=True)
    workbook(os.path.join(gold, "change_pricing_2025-26.xlsx"), S, Fg)
    deck(os.path.join(gold, "board_review_2025-26.pptx"), S, Fg)
    figs = figures_json(Fg)
    with open(os.path.join(HERE, "figures.json"), "w") as f:
        json.dump(figs, f, indent=1, sort_keys=True)
    Fg["figs"] = figs
    return Fg


def figures_json(Fg):
    M = Fg["M"]
    f = {"short_bp": r10(M["short"]), "R_bacc_pct": round(M["R_bacc"] * 100, 1),
         "R_bench_pct": round(M["R_bench"] * 100, 1), "call": M["call"], "runner_up": M["runner_up"],
         "gap_bp": r10(M["gap"]), "dd_trigger_pct": round(M["dd_trigger"] * 100, 1),
         "A_worst_pct": round(M["A_worst"] * 100, 1), "trigger_line_pct": 8, "restore_line_pct": 4,
         "defensive_pct": 40, "window": 63, "higher_trigger_pct": 12}
    for c, _ in CHANGES:
        f["bp_" + c] = r10(M["bp_" + c])
        f["R_%s_pct" % c] = round(M["R_" + c] * 100, 1)
    for (tag, q), v in Fg["inc"].items():
        f["inc_%s_%s" % (tag, q)] = int(round(v / 1000) * 1000)
    for (tag, q), v in Fg["cost"].items():
        f["cost_%s_%s" % (tag, q)] = int(round(v / 100) * 100)
    for q, (n, sh) in Fg["aim"].items():
        f["aim_n_" + q] = n
        f["aim_pct_" + q] = round(sh * 100, 1)
    return f


# ------------------------------------------------------------------------------------------------ the workbook
def workbook(path, S, Fg):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    M, reps = Fg["M"], Fg["reps"]
    act, world = S["act"], S["world"]
    rec = act["rec"]
    i0, i1 = F.YEAR0, F.YEAR1
    bold = Font(bold=True)
    head = PatternFill("solid", fgColor="DDE4EE")
    wb = Workbook()
    ws = wb.active
    ws.title = "Changes"
    ws["A1"] = "Thornbury Managed Risk UK Equity Fund: changes before the board, priced on 2025-26"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("B Accumulation, 12:00 on 30 Sep 2025 to 12:00 on 30 Sep 2026. Benchmark Larkspur UK All-Share TR at "
                "12:00: %.2f%%. B Acc as it ran: %.2f%%. Shortfall: %d bp." % (M["R_bench"] * 100, M["R_bacc"] * 100,
                                                                                  r10(M["short"])))
    ws.append([])
    hdr = ["Change", "B Acc return with the change (%)", "Shortfall removed (bp)", "Rank", "Exposure reduced from",
           "Full exposure again from"]
    ws.append(hdr)
    for c in ws[4]:
        c.font, c.fill = bold, head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for c in M["ranked"]:
        ep = M["ep_" + c]
        a = ep[0][0].strftime("%d %b %Y") if ep else "not reduced"
        b = (ep[0][1].strftime("%d %b %Y") if ep[0][1] else None) if ep else None
        ws.append([NAMES[c], round(M["R_" + c] * 100, 2), r10(M["bp_" + c]), M["ranked"].index(c) + 1, a, b])
    ws.append([])
    ws.append(["As it ran", round(M["R_bacc"] * 100, 2), None, None, M["ep_actual"][0][0].strftime("%d %b %Y"),
               M["ep_actual"][0][1].strftime("%d %b %Y")])
    ws.append([])
    ws.append(["Recommended: %s, %d bp; runner-up %s, %d bp; difference %d bp."
               % (NAMES[M["call"]].lower(), r10(M["bp_" + M["call"]]), NAMES[M["runner_up"]].lower(),
                  r10(M["bp_" + M["runner_up"]]), r10(M["gap"]))])
    for col, w in zip("ABCDEF", [34, 18, 14, 7, 18, 18]):
        ws.column_dimensions[col].width = w

    ws = wb.create_sheet("Replay")
    ws.append(["Valuation date", "B Acc as it ran (p)", "Drawdown as it ran (%)", "Exposure as it ran (%)"]
              + ["%s: B Acc (p)" % NAMES[c] for c, _ in CHANGES] + ["%s: exposure (%%)" % NAMES[c] for c, _ in CHANGES])
    for c in ws[1]:
        c.font, c.fill = bold, head
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for j, i in enumerate(range(i0, i1 + 1)):
        row = [DAYS[i], round(rec["price"]["B Acc"][i], 2), round(rec["dd"][i] * 100, 2), round(rec["expo"][i] * 100, 1)]
        row += [round(float(reps[c]["price"][j]), 2) for c, _ in CHANGES]
        row += [round(float(reps[c]["expo"][j]) * 100, 1) for c, _ in CHANGES]
        ws.append(row)
        ws.cell(row=ws.max_row, column=1).number_format = "dd/mm/yyyy"
    ws.freeze_panes = "B2"
    ws.column_dimensions["A"].width = 13

    ws = wb.create_sheet("Dividend income")
    ws.append(["Dividend income by ex-dividend date, paid or still to be paid (GBP)"])
    ws["A1"].font = bold
    ws.append(["Sleeve", "Oct-Dec 2025", "Jan-Mar 2026", "Apr-Jun 2026", "Jul-Sep 2026", "Year"])
    for c in ws[2]:
        c.font, c.fill = bold, head
    for tag, nm in (("V", "Value (Ashcombe)"), ("G", "Growth (Fennick)")):
        vals = [int(round(Fg["inc"][(tag, q)] / 1000) * 1000) for q in ("Q1", "Q2", "Q3", "Q4")]
        ws.append([nm] + vals + [sum(vals)])
        for cell in ws[ws.max_row][1:]:
            cell.number_format = "#,##0"
    ws.column_dimensions["A"].width = 20

    ws = wb.create_sheet("Dealing costs")
    ws.append(["Commission and stamp duty reserve tax by quarter of trade (GBP)"])
    ws["A1"].font = bold
    ws.append(["Sleeve", "Oct-Dec 2025", "Jan-Mar 2026", "Apr-Jun 2026", "Jul-Sep 2026", "Year"])
    for c in ws[2]:
        c.font, c.fill = bold, head
    for tag, nm in (("V", "Value (Ashcombe)"), ("G", "Growth (Fennick)")):
        vals = [int(round(Fg["cost"][(tag, q)] / 100) * 100) for q in ("Q1", "Q2", "Q3", "Q4")]
        ws.append([nm] + vals + [sum(vals)])
        for cell in ws[ws.max_row][1:]:
            cell.number_format = "#,##0"
    ws.column_dimensions["A"].width = 20

    ws = wb.create_sheet("AIM holdings")
    ws.append(["Growth sleeve holdings quoted on AIM, custodian's settled holdings at close"])
    ws["A1"].font = bold
    ws.append(["Quarter-end", "Holdings on AIM", "Share of sleeve (%)"])
    for c in ws[2]:
        c.font, c.fill = bold, head
    for q, d in (("Q1", "31 Dec 2025"), ("Q2", "31 Mar 2026"), ("Q3", "30 Jun 2026"), ("Q4", "30 Sep 2026")):
        n, sh = Fg["aim"][q]
        ws.append([d, n, round(sh * 100, 1)])
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["C"].width = 18
    wb.save(path)
    PP.normalize_ooxml(path, "Carol Rowe", "Carol Rowe", "2026-10-26T09:05:00Z", "2026-11-02T17:12:00Z",
                       excel=True, company="Thornbury Fund Managers Limited")


# ------------------------------------------------------------------------------------------------ the deck
def deck(path, S, Fg):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    M, reps = Fg["M"], Fg["reps"]
    rec = S["act"]["rec"]
    i0 = F.YEAR0
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]

    def title(slide, text, sub=None):
        tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size, p.font.bold = Pt(24), True
        p.font.color.rgb = RGBColor(0x1F, 0x2A, 0x44)
        if sub:
            p2 = tf.add_paragraph()
            p2.text = sub
            p2.font.size = Pt(13)
            p2.font.color.rgb = RGBColor(0x55, 0x5B, 0x66)

    def body(slide, lines, top=1.6):
        tb = slide.shapes.add_textbox(Inches(0.7), Inches(top), Inches(12.0), Inches(5.2))
        tf = tb.text_frame
        tf.word_wrap = True
        for k, line in enumerate(lines):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            p.text = line
            p.font.size = Pt(16)
            p.space_after = Pt(10)

    c, ru = M["call"], M["runner_up"]
    s = prs.slides.add_slide(blank)
    title(s, "Assessment of value 2025-26: the change for 2026-27",
          "Thornbury Managed Risk UK Equity Fund, board meeting 19 November 2026")
    body(s, ["Recommendation: run the value sleeve as a tracker of the benchmark. On 2025-26 it removes %d bp of the "
             "B Accumulation shares' %d bp shortfall against the Larkspur UK All-Share."
             % (r10(M["bp_" + c]), r10(M["short"])),
             "Runner-up: raising the overlay's trigger to 12%%, %d bp. Difference: %d bp."
             % (r10(M["bp_" + ru]), r10(M["gap"])),
             "With the value sleeve tracking the benchmark, the B Acc price's deepest fall below its 63-day high is %.1f%% "
             "(%s), so the overlay never cuts exposure and the fund is fully invested through the April to June "
             "rebound." % (M["A_worst"] * 100, M["A_worst_day"].strftime("%d %B %Y").lstrip("0")),
             "As the year ran, the price closed %.1f%% below its high on %s; exposure was cut to 40%% from %s until full exposure was restored on %s."
             % (M["dd_trigger"] * 100, M["trigger_day"].strftime("%d %B").lstrip("0"),
                M["ep_actual"][0][0].strftime("%d %B").lstrip("0"),
                (M["ep_actual"][0][1]).strftime("%d %B").lstrip("0"))])

    s = prs.slides.add_slide(blank)
    title(s, "Shortfall each change would have removed, 2025-26 (bp)",
          "Each change replayed from 30 September 2025 with the fund run as its prospectus requires")
    cd = CategoryChartData()
    order = M["ranked"]
    cd.categories = [NAMES[x] for x in order]
    cd.add_series("Shortfall removed (bp)", [r10(M["bp_" + x]) for x in order])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.4), cd)
    ch = gf.chart
    ch.has_legend = False
    pl = ch.plots[0]
    pl.has_data_labels = True
    pl.data_labels.number_format = '#,##0" bp"'
    pl.data_labels.number_format_is_linked = False
    pl.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    pl.data_labels.font.size = Pt(13)
    ch.category_axis.reverse_order = True
    ch.category_axis.tick_labels.font.size = Pt(13)
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "Basis points of the year's B Acc return"
    ch.value_axis.tick_labels.font.size = Pt(11)
    ch.value_axis.has_major_gridlines = False
    pl.series[0].format.fill.solid()
    pl.series[0].format.fill.fore_color.rgb = RGBColor(0x2F, 0x5D, 0x8A)

    s = prs.slides.add_slide(blank)
    title(s, "B Acc price below its 63-day high, February to June 2026 (%)",
          "As it ran, and replayed with the value sleeve as a tracker; the overlay cuts exposure beyond 8%")
    a, b = IDX[D(2026, 2, 2)], IDX[D(2026, 6, 30)]
    pa = reps["A"]["price"]
    hist = [round(x, 2) for x in rec["price"]["B Acc"][i0 - W.WINDOW + 1:i0 + 1]]
    dda = []
    for j in range(1, len(pa)):
        hist.append(round(pa[j], 2))
        dda.append(1 - hist[-1] / max(hist[-W.WINDOW:]))
    cd = CategoryChartData()
    cd.categories = [DAYS[i].strftime("%d %b") for i in range(a, b + 1)]
    cd.add_series("As it ran", [round(-rec["dd"][i] * 100, 2) for i in range(a, b + 1)])
    cd.add_series("Value sleeve as a tracker", [round(-dda[i - i0 - 1] * 100, 2) for i in range(a, b + 1)])
    cd.add_series("Trigger (8%)", [-8.0 for i in range(a, b + 1)])
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE, Inches(0.8), Inches(1.6), Inches(11.6), Inches(5.4), cd)
    ch = gf.chart
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.BOTTOM
    ch.legend.include_in_layout = False
    ch.value_axis.has_title = True
    ch.value_axis.axis_title.text_frame.text = "Per cent below the 63-day high"
    ch.value_axis.has_major_gridlines = False
    ch.category_axis.tick_labels.font.size = Pt(9)
    for k, col in enumerate([RGBColor(0x8A, 0x2F, 0x2F), RGBColor(0x2F, 0x5D, 0x8A), RGBColor(0x88, 0x88, 0x88)]):
        ser = ch.plots[0].series[k]
        ser.format.line.color.rgb = col
        ser.format.line.width = Pt(2.25 if k < 2 else 1.25)
        ser.smooth = False

    s = prs.slides.add_slide(blank)
    title(s, "Workings in change_pricing_2025-26.xlsx")
    body(s, ["Changes: each change's B Acc return for the year and the shortfall it removes; Replay: every valuation "
             "point, price and exposure, as it ran and under each change.",
             "Dividend income, dealing costs and the growth sleeve's AIM holdings by quarter are on their own sheets."])
    prs.save(path)
    PP.normalize_ooxml(path, "Carol Rowe", "Carol Rowe", "2026-10-28T10:40:00Z", "2026-11-03T08:55:00Z",
                       title="Assessment of value 2025-26", company="Thornbury Fund Managers Limited")
    PP.scrub_pptx(path, total_time=86, company="Thornbury Fund Managers Limited")
