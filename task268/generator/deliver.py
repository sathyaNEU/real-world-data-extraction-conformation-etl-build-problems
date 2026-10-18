"""The goldens: pilot_metro_2027.xlsx (each core's people present, delivery-weighted density and dense-tract share,
the tracts behind them, the premises and the competitors) and pilot_metro_board_2027.pptx (the deck to the board),
plus generator/figures.json and metadata.json. Every figure comes from analysis.py run on the shipped pack."""
import json
import os
import shutil

import analysis as A
import common as K
import postprocess as PP

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX, PPTX = "pilot_metro_2027.xlsx", "pilot_metro_board_2027.pptx"


def rnd(x, u):
    """Round half up to the unit u (people to the thousand, densities to the hundred)."""
    return int(x / u + 0.5) * u


def pct(x):
    return int(100 * x + 0.5)


def results(target):
    D = A.load(target)
    G = A.run(D, "golden")
    F = G["F"]
    order = G["order"]
    win, run = order[0], order[1]
    sh = A.shares(D, cells="gr")
    out = dict(D=D, G=G, order=order, win=win, runner=run,
               cores={m: dict(present=rnd(F[m]["present"], 1000), pwd=rnd(F[m]["pwd"], 100), dense=pct(F[m]["dense"]),
                              tracts=len(F[m]["tracts"]), land=sum(a for _, _, a, _ in F[m]["tracts"]))
                      for m in K.METRO_NAMES},
               gap=rnd(F[win]["pwd"] - F[run]["pwd"], 100),
               shares={"%s %s" % k: round(100 * v, 1) for k, v in sorted(sh.items())},
               rungs={r: A.run(D, r)["pick"] for r in ("cadp", "acs", "one", "pool", "ring")},
               ask_a=A.ask_a(D), ask_b=A.ask_b(D))
    return out


# ---------------------------------------------------------------------------------------------- the workbook
def workbook(path, o):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ink, accent = "1D2326", "8A4B12"
    thin = Side(style="thin", color="B7BEC4")
    head_fill = PatternFill("solid", fgColor="EFE7DD")
    pick_fill = PatternFill("solid", fgColor="FBEBD6")

    def header(ws, row, cols):
        ws.append(cols)
        for c in ws[row]:
            c.font = Font(bold=True, color=ink)
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)

    ws = wb.active
    ws.title = "Pilot metro"
    win, run = o["win"], o["runner"]
    ws["A1"] = "2027 weekday dark-store pilot: %s's core is the densest on an average weekday" % win
    ws["A1"].font = Font(bold=True, size=13, color=accent)
    ws["A2"] = ("Delivery-weighted density under section 4 of board paper BD-2026-41, the six candidate cores as the "
                "planning map lists them. Prepared for the meeting of 9 December 2026.")
    ws["A2"].font = Font(italic=True, size=9, color="5B646B")
    ws.append([])
    header(ws, 4, ["Metro", "Core tracts", "Land (km²)", "People present on an average weekday",
                   "Delivery-weighted density (people per km²)", "Share of people present in tracts of 20,000 or "
                   "more per km²", "Rank"])
    for i, m in enumerate(o["order"]):
        c = o["cores"][m]
        ws.append([m, c["tracts"], round(c["land"], 1), c["present"], c["pwd"], c["dense"] / 100.0, i + 1])
        r = ws.max_row
        ws.cell(r, 3).number_format = "0.0"
        ws.cell(r, 4).number_format = "#,##0"
        ws.cell(r, 5).number_format = "#,##0"
        ws.cell(r, 6).number_format = "0%"
        if m == win:
            for c2 in ws[r]:
                c2.fill = pick_fill
                c2.font = Font(bold=True, color=ink)
    ws.append([])
    ws.append(["%s leads %s by %s people per km²." % (win, run, format(o["gap"], ","))])
    ws.cell(ws.max_row, 1).font = Font(bold=True, color=ink)
    ws.append(["People present are rounded to the thousand, densities to the hundred per km² and shares to the whole "
               "per cent, each from unrounded figures; the tract sheet carries the detail."])
    ws.cell(ws.max_row, 1).font = Font(size=9, color="5B646B")
    for col, wdt in zip("ABCDEFG", [13, 8, 10, 16, 17, 20, 6]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A5"

    ws = wb.create_sheet("Core tracts")
    header(ws, 1, ["Metro", "Tract", "Land (km²)", "Residents (ACS 2018-2022)", "People present on an average weekday",
                   "People present per km²"])
    D = o["D"]
    for m in K.METRO_NAMES:
        for g, p, a, d in sorted(o["G"]["F"][m]["tracts"], key=lambda x: x[0]):
            ws.append([m, g, round(a, 3), D["pop"].get(g, 0), int(p + 0.5), int(d + 0.5)])
            r = ws.max_row
            ws.cell(r, 2).number_format = "@"
            ws.cell(r, 3).number_format = "0.000"
            ws.cell(r, 4).number_format = "#,##0"
            ws.cell(r, 5).number_format = "#,##0"
            ws.cell(r, 6).number_format = "#,##0"
    for col, wdt in zip("ABCDEF", [13, 14, 10, 14, 16, 14]):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:F%d" % ws.max_row

    ws = wb.create_sheet("Premises")
    header(ws, 1, ["Metro", "Ground-floor retail or flex units of 150 to 450 m² available to lease on 30 September 2026",
                   "Median asking rent ($ per m² a year)"])
    for m in K.METRO_NAMES:
        n, med = o["ask_a"][m]
        ws.append([m, n, int(med + 0.5) if med is not None else None])
        ws.cell(ws.max_row, 3).number_format = "#,##0"
    ws.append([])
    ws.append(["From the listing service's export of 1 October 2026. A floor listed whole beside its own suites is "
               "counted once, as its suites; rents quoted per square foot a month or as a monthly total are put on a "
               "yearly basis per m²."])
    ws.cell(ws.max_row, 1).font = Font(size=9, color="5B646B")
    for col, wdt in zip("ABC", [13, 34, 18]):
        ws.column_dimensions[col].width = wdt

    ws = wb.create_sheet("Competitors")
    header(ws, 1, ["Metro", "Tilldash dark stores delivering on 30 September 2026",
                   "Hopcrate dark stores delivering on 30 September 2026"])
    for m in K.METRO_NAMES:
        ws.append([m, o["ask_b"][(m, "Tilldash")], o["ask_b"][(m, "Hopcrate")]])
    ws.append([])
    ws.append(["From the market team's scrape of both store finders on 30 September 2026. Shops that appear in both "
               "finders at the same address and unit are independent partner stores, not either brand's dark stores."])
    ws.cell(ws.max_row, 1).font = Font(size=9, color="5B646B")
    for col, wdt in zip("ABC", [13, 22, 22]):
        ws.column_dimensions[col].width = wdt

    ws = wb.create_sheet("Notes")
    sh = o["shares"]
    lines = [
        "How people present were counted",
        "Residents: ACS 2018-2022 five-year total population of each core tract.",
        "Workers: primary jobs in the 2022 commuting extract (both parts), by home tract, work tract and industry group.",
        "A tract's people present: its residents, less its residents at a workplace in another tract, plus people from "
        "other tracts at a workplace in it. Each flow is carried at the share of weekdays its workers spend on the "
        "employer's premises, from the Work Location Survey (October 2025 to September 2026, weighted), for the "
        "flow's industry group and where its workers live relative to the workplace's metropolitan area (its central "
        "county, an outlying county, or outside it, by the July 2023 delineation).",
        "Shares of weekdays on the premises used (per cent): goods producing %s, %s, %s; trade, transportation and "
        "utilities %s, %s, %s; all other services %s, %s, %s (central county, outlying county, outside the area)."
        % tuple(sh["%s %s" % (g, r)] for g in K.GROUPS for r in ("C", "O", "X")),
        "Land: the 2022 gazetteer's land area; the two water-only tracts the planning map lists have no land and count "
        "for nothing.",
        "Delivery-weighted density: each tract's people present per km² of land, averaged over the core with each "
        "tract weighted by its people present.",
        "Prepared by Location Analytics for Network Expansion, October 2026."]
    for i, line in enumerate(lines):
        ws.append([line])
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
        if i == 0:
            ws.cell(ws.max_row, 1).font = Font(bold=True)
    ws.column_dimensions["A"].width = 120
    for s in wb.worksheets:
        s.page_setup.orientation = "landscape"
        s.page_setup.fitToWidth = 1
        s.page_setup.fitToHeight = 0
        s.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


# ---------------------------------------------------------------------------------------------- the deck
def deck(path, o):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    INK, GREY, ACC, MUTE = RGBColor(0x1D, 0x23, 0x26), RGBColor(0x5B, 0x64, 0x6B), RGBColor(0xB3, 0x5C, 0x12), RGBColor(0xA9, 0xB1, 0xB8)
    win, run = o["win"], o["runner"]

    def text(slide, x, y, w, h, s, size=14, bold=False, color=INK, align=None):
        tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = s
        p.font.size, p.font.bold, p.font.color.rgb = Pt(size), bold, color
        p.font.name = "Calibri"
        if align:
            p.alignment = align
        return tf

    def footer(slide, n):
        text(slide, 457200, 6400800, 9000000, 300000, "Network Expansion | Board of Directors, 9 December 2026 | Source: "
             "Location Analytics data pack, 6 October 2026", 9, color=GREY)
        text(slide, 11000000, 6400800, 800000, 300000, str(n), 9, color=GREY, align=PP_ALIGN.RIGHT)

    F = o["cores"]
    # 1. the call
    s = prs.slides.add_slide(blank)
    text(s, 457200, 1500000, 11200000, 900000, "Pilot the weekday dark store in %s" % win, 36, True, ACC)
    tf = text(s, 457200, 2600000, 11000000, 1800000,
              "%s's core has the highest delivery-weighted density of the six candidates: %s people per km² on an "
              "average weekday, %s ahead of %s's %s." % (win, format(F[win]["pwd"], ","), format(o["gap"], ","), run,
                                                         format(F[run]["pwd"], ",")), 20)
    p = tf.add_paragraph()
    p.text = ("The measure is section 4 of paper BD-2026-41. People present count residents at home and the people "
              "at their workplace on an average weekday, from the 2022 commuting table and the Work Location Survey's "
              "days on the premises.")
    p.font.size, p.font.color.rgb = Pt(14), GREY
    footer(s, 1)
    # 2. the chart
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "%s's core is the densest on an average weekday" % win, 26, True, INK)
    text(s, 457200, 950000, 11200000, 400000, "Delivery-weighted density, people present per km² of land", 13, color=GREY)
    cd = CategoryChartData()
    cd.categories = o["order"]
    cd.add_series("Delivery-weighted density", [F[m]["pwd"] for m in o["order"]])
    gf = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Emu(457200), Emu(1400000), Emu(11000000), Emu(4800000), cd)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = False
    plot = ch.plots[0]
    plot.gap_width = 60
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.number_format, dl.number_format_is_linked = "#,##0", False
    dl.position = XL_LABEL_POSITION.OUTSIDE_END
    dl.font.size, dl.font.color.rgb = Pt(12), INK
    ser = plot.series[0]
    for i, m in enumerate(o["order"]):
        pt = ser.points[i]
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = ACC if m == win else MUTE
    ca = ch.category_axis
    ca.reverse_order = True
    ca.tick_labels.font.size = Pt(13)
    ca.format.line.color.rgb = MUTE
    va = ch.value_axis
    va.has_major_gridlines = False
    va.visible = False
    footer(s, 2)
    # 3. the figures
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "Every core's weekday figures", 26, True, INK)
    rows = [["Metro", "People present on an average weekday", "Delivery-weighted density (per km²)",
             "Share in tracts of 20,000+ per km²"]]
    for m in o["order"]:
        rows.append([m, format(F[m]["present"], ","), format(F[m]["pwd"], ","), "%d%%" % F[m]["dense"]])
    tb = s.shapes.add_table(len(rows), 4, Emu(457200), Emu(1300000), Emu(11200000), Emu(3600000)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = tb.cell(i, j)
            c.text = v
            para = c.text_frame.paragraphs[0]
            para.font.size = Pt(14 if i else 13)
            para.font.bold = i == 0 or r[0] == win
            if j:
                para.alignment = PP_ALIGN.RIGHT
    footer(s, 3)
    # 4. sites and competition
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "Every core has ground-floor space on the market", 26, True, INK)
    rows = [["Metro", "Units of 150-450 m² on the market, 30 Sep", "Median asking rent ($/m² a year)",
             "Tilldash dark stores", "Hopcrate dark stores"]]
    for m in o["order"]:
        n, med = o["ask_a"][m]
        rows.append([m, str(n), format(int(med + .5), ","), str(o["ask_b"][(m, "Tilldash")]), str(o["ask_b"][(m, "Hopcrate")])])
    tb = s.shapes.add_table(len(rows), 5, Emu(457200), Emu(1300000), Emu(11200000), Emu(3600000)).table
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = tb.cell(i, j)
            c.text = v
            para = c.text_frame.paragraphs[0]
            para.font.size = Pt(14 if i else 12)
            para.font.bold = i == 0
            if j:
                para.alignment = PP_ALIGN.RIGHT
    text(s, 457200, 5100000, 11200000, 700000, "Premises and competition are reported for every core and do not decide "
         "the pilot (paper BD-2026-41, section 5).", 12, color=GREY)
    footer(s, 4)
    # 5. method
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "How people present were counted", 26, True, INK)
    sh = o["shares"]
    tf = text(s, 457200, 1300000, 11200000, 4500000,
              "Residents: ACS 2018-2022 population of each core tract; workers: 2022 primary jobs by home and work tract.", 15)
    for line in ["A tract's people present: its residents, less those at a workplace in another tract, plus people from "
                 "other tracts at a workplace in it.",
                 "Each commuting flow is carried at the Work Location Survey's share of weekdays on the employer's premises "
                 "for its industry group and where its workers live relative to the workplace's metropolitan area.",
                 "Office and other services workers come in %s%% of weekdays from the central county, %s%% from an outlying "
                 "county and %s%% from outside the metro; trade and transport workers %s%%, %s%% and %s%%."
                 % (sh["SI03 C"], sh["SI03 O"], sh["SI03 X"], sh["SI02 C"], sh["SI02 O"], sh["SI02 X"]),
                 "Counting every job as present every weekday would put %s first; one survey share per industry group, "
                 "%s." % (o["rungs"]["cadp"], o["rungs"]["pool"])]:
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(15)
        p.space_before = Pt(8)
    footer(s, 5)
    prs.save(path)


def figures(o):
    F = o["cores"]
    return {
        "call": dict(metro=o["win"], runner_up=o["runner"], gap=o["gap"], density=F[o["win"]]["pwd"],
                     runner_density=F[o["runner"]]["pwd"]),
        "cores": {m: dict(present=F[m]["present"], density=F[m]["pwd"], dense_share=F[m]["dense"]) for m in K.METRO_NAMES},
        "shares": o["shares"],
        "rungs": o["rungs"],
        "ask_a": {m: dict(units=o["ask_a"][m][0], median_rent=int(o["ask_a"][m][1] + 0.5)) for m in K.METRO_NAMES},
        "ask_b": {m: {b: o["ask_b"][(m, b)] for b in K.BRANDS} for m in K.METRO_NAMES},
        "params": dict(dense_cut="20,000", unit_min_m2=150, unit_max_m2=450),
        "paper": dict(sections=[K.CLAUSE[k] for k in ("pick", "density", "present")], pilot_year=K.PILOT_YEAR),
    }


def write(target, golden, T=None):
    o = results(target)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    workbook(os.path.join(golden, XLSX), o)
    deck(os.path.join(golden, PPTX), o)
    PP.COMPANY = K.ORG + " Inc."
    PP.normalize_ooxml(os.path.join(golden, XLSX), K.PEOPLE["analytics"], K.PEOPLE["analytics"], "2026-10-12T13:20:41Z",
                       "2026-10-14T18:05:16Z", excel=True)
    PP.normalize_ooxml(os.path.join(golden, PPTX), K.PEOPLE["vp"], K.PEOPLE["vp"], "2026-10-14T19:44:02Z",
                       "2026-10-15T12:31:57Z", title="2027 weekday pilot metro")
    json.dump(figures(o), open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    meta = {"distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS], "deliverables": [XLSX, PPTX],
            "stated_inputs": []}
    json.dump(meta, open(os.path.join(os.path.dirname(HERE), "metadata.json"), "w"), indent=2)
    return o
