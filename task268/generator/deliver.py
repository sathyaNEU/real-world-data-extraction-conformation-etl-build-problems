"""The goldens: ground_closure_2027.xlsx (each ground's stock by year and its fall, the survey by depth band, the
landings by port, the quota left by pool) and closure_committee_2027.pptx (the recommendation to the management
committee, with the chart of each ground's stock against its base), plus generator/figures.json and metadata.json.
Every figure comes from analysis.py run on the shipped pack."""
import json
import os
import shutil
from collections import defaultdict

import analysis as A
import common as K
import postprocess as PP

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX, PPTX = "ground_closure_2027.xlsx", "closure_committee_2027.pptx"


def whole(x):
    """Round half up to the whole unit (percent, point, tonne, pound)."""
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def results(target):
    D = A.load(target)
    ix = A.survey_index(D)
    f = A.falls(ix)
    c = A.call(f)
    base = {g: sum(ix[g][y] for y in K.BASE) / 3 for g in K.GROUND_NAMES}
    T = A.tows(D)
    bands = {}
    area = A.band_areas(D)
    ncell = defaultdict(int)
    for r in D["grid"]:
        ncell[(r["ground"], r["depth_band"])] += 1
    for g in K.GROUND_NAMES:
        tot = sum(area[(g, b)] for b in K.BANDS)
        for b in K.BANDS:
            means = {}
            tows = {}
            for y in K.YEARS:
                xs = [t["kg"] for t in T if t["ground"] == g and t["band"] == b and t["year"] == y]
                means[y], tows[y] = sum(xs) / len(xs), len(xs)
            bands[(g, b)] = dict(area=area[(g, b)], share=area[(g, b)] / tot, cells=ncell[(g, b)], means=means, tows=tows)
    rec = A.records(D)
    worked = {g: {y: len({r[2] for r in rec if r[1] == g and r[0] == y}) for y in K.YEARS} for g in K.GROUND_NAMES}
    rungs = A.ladder(D)
    return dict(D=D, ix=ix, f=f, call=c, base=base, bands=bands, worked=worked, rungs=rungs,
                falls={g: whole(100 * f[g]) for g in K.GROUND_NAMES}, gap=whole(100 * c["gap"]),
                pct={g: {y: 100 * ix[g][y] / base[g] for y in K.YEARS} for g in K.GROUND_NAMES},
                ask_a=A.ask_a(D), ask_b=A.ask_b(D),
                area={g: sum(area[(g, b)] for b in K.BANDS) for g in K.GROUND_NAMES},
                cpue=A.falls(A.cpue_index(D, "nominal")))


# ---------------------------------------------------------------------------------------------- the workbook
def workbook(path, o):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    ink, accent = "1C2428", "8E3B13"
    thin = Side(style="thin", color="B4BDC3")
    head_fill = PatternFill("solid", fgColor="E6EDF0")
    pick_fill = PatternFill("solid", fgColor="F8E5D8")
    c = o["call"]

    def header(ws, row, cols, height=30):
        for j, v in enumerate(cols, 1):
            cell = ws.cell(row=row, column=j, value=v)
            cell.font = Font(bold=True, color=ink)
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="top", horizontal="left" if j == 1 else "right")
            cell.border = Border(bottom=thin)
        ws.row_dimensions[row].height = height

    def landscape(ws):
        ws.page_setup.orientation = "landscape"
        ws.page_setup.paperSize = ws.PAPERSIZE_A4
        ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
        ws.sheet_properties.pageSetUpPr.fitToPage = True
        ws.print_title_rows = "4:4"

    def title(ws, text, sub):
        ws["A1"] = text
        ws["A1"].font = Font(bold=True, size=13, color=accent)
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, size=9, color="5A646B")

    # Grounds
    ws = wb.active
    ws.title = "Grounds"
    title(ws, "Close %s in 2027: its haddock stock has fallen furthest below its base" % c["pick"],
          "Autumn gear and bycatch survey, October 2019 to 2026. Stock: mean haddock catch per standard tow in each depth "
          "band, weighted by the band's share of the ground's stock area (Annex A). Base: average of 2019, 2020 and 2021.")
    cols = ["Ground", "Code", "Stock area (km²)"] + [str(y) for y in K.YEARS] + ["Base 2019-21", "2026 as % of base",
                                                                              "Fall from base (%)"]
    header(ws, 4, cols)
    r = 5
    for g in c["order"]:
        vals = [g, K.GROUND_CODE[g], round(o["area"][g])] + [round(o["ix"][g][y], 1) for y in K.YEARS] + \
               [round(o["base"][g], 1), round(o["pct"][g][2026]), o["falls"][g]]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=r, column=j, value=v)
            if j >= 3:
                cell.alignment = Alignment(horizontal="right")
                cell.number_format = "#,##0" if j in (3, 14, 15) else "0.0"
            if g == c["pick"]:
                cell.fill = pick_fill
                cell.font = Font(bold=True, color=ink)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Recommendation: close %s to members' towed gear from 1 January to 31 December 2027. "
            "Its fall is %d points more than %s's, the next largest." % (c["pick"], o["gap"], c["runner"])).font = Font(bold=True)
    ws.cell(row=r + 1, column=1, value="Stock figures are kg of haddock per standard 30-minute tow. In 2020 one station "
            "was not fished for weather and its band's mean is over the stations towed; two stations replaced in 2023 "
            "stand for their bands (field manual, revision 3).").font = Font(size=9, color="5A646B")
    widths = [17, 7, 10] + [8] * 8 + [10, 10, 10]
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = "B5"
    landscape(ws)

    # Survey by band
    ws = wb.create_sheet("Survey by band")
    title(ws, "Mean haddock catch per standard tow by depth band (kg)",
          "Depth bands from Annex A: A under 100 m, B 100 m to under 140 m, C 140 m and deeper. Twelve stations a band.")
    header(ws, 4, ["Ground", "Band", "Cells", "Area (km²)", "Share of stock area"] + [str(y) for y in K.YEARS])
    r = 5
    for g in K.GROUND_NAMES:
        for b in K.BANDS:
            x = o["bands"][(g, b)]
            vals = [g, b, x["cells"], round(x["area"]), round(x["share"], 3)] + [round(x["means"][y], 1) for y in K.YEARS]
            for j, v in enumerate(vals, 1):
                cell = ws.cell(row=r, column=j, value=v)
                if j >= 3:
                    cell.alignment = Alignment(horizontal="right")
                    cell.number_format = {3: "0", 4: "#,##0", 5: "0.0%"}.get(j, "0.0")
            r += 1
    for j, w in enumerate([17, 6, 7, 10, 10] + [8] * 8, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w
    ws.freeze_panes = "C5"
    landscape(ws)

    # Ports
    ws = wb.create_sheet("Ports")
    title(ws, "Haddock landed by members, 1 January to 30 September 2026",
          "Sales notes by landing date; live weight (gutted x 1.17); each landing's notes counted once, a corrected note "
          "in place of the note it corrects.")
    header(ws, 4, ["Port", "Landed (t, live weight)", "Value at first sale (£)"])
    r = 5
    for p in K.PORT_NAMES:
        t, v = o["ask_a"][p]
        for j, val in enumerate([p, whole(t), whole(v)], 1):
            cell = ws.cell(row=r, column=j, value=val)
            if j > 1:
                cell.alignment = Alignment(horizontal="right")
                cell.number_format = "#,##0" if j == 2 else "£#,##0"
        r += 1
    tt = sum(o["ask_a"][p][0] for p in K.PORT_NAMES)
    tv = sum(o["ask_a"][p][1] for p in K.PORT_NAMES)
    for j, val in enumerate(["All four ports", whole(tt), whole(tv)], 1):
        cell = ws.cell(row=r, column=j, value=val)
        cell.font = Font(bold=True)
        cell.border = Border(top=thin)
        if j > 1:
            cell.alignment = Alignment(horizontal="right")
            cell.number_format = "#,##0" if j == 2 else "£#,##0"
    for j, w in enumerate([16, 14, 16], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w

    # Pools
    ws = wb.create_sheet("Pools")
    title(ws, "Haddock quota left by pool, 30 September 2026",
          "Quota ledger 2026, entries with effect on or before 30 September (quota rules, section 3); each pool's 1 "
          "January allocation counted once.")
    header(ws, 4, ["Pool", "Name", "Quota left (t)"])
    r = 5
    for code, name in K.POOLS:
        for j, val in enumerate([code, name, whole(o["ask_b"][code])], 1):
            cell = ws.cell(row=r, column=j, value=val)
            if j == 3:
                cell.alignment = Alignment(horizontal="right")
                cell.number_format = "#,##0"
        r += 1
    for j, w in enumerate([6, 14, 12], 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w

    # Notes
    ws = wb.create_sheet("Notes")
    notes = [
        "Prepared by the science and sustainability office for the management committee meeting of 9 December 2026.",
        "Closure rule: Haddock Stock Recovery Plan, section 4.1 and 4.2 (adopted 24 March 2026).",
        "Grounds and stock areas: Annex A, ground_grid_annex_a.csv. Survey: survey_tows_2019_2026.csv, each tow placed "
        "in its grid cell by its shot position.",
        "Falls are rounded to the whole percent; the gap between the two largest falls is worked from the unrounded falls.",
        "Landings: sales_notes_2026.csv with member_vessels.xlsx (registration history) and conversion_factors.csv.",
        "Quota: quota_ledger_2026.csv under the quota management rules 2026.",
    ]
    ws["A1"] = "Notes"
    ws["A1"].font = Font(bold=True, size=13, color=accent)
    for k, t in enumerate(notes, 3):
        ws.cell(row=k, column=1, value=t)
    ws.column_dimensions["A"].width = 120
    wb.save(path)


# ---------------------------------------------------------------------------------------------- the deck
def deck(path, o):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.enum.dml import MSO_LINE_DASH_STYLE
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Emu, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(12192000), Emu(6858000)
    blank = prs.slide_layouts[6]
    INK, GREY, ACC = RGBColor(0x1C, 0x24, 0x28), RGBColor(0x5A, 0x64, 0x6B), RGBColor(0x8E, 0x3B, 0x13)
    c = o["call"]
    win, run = c["pick"], c["runner"]

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

    def footer(slide, n, source):
        text(slide, 457200, 6400800, 10300000, 300000, "Science and sustainability office | Management committee, "
             "9 December 2026 | Source: " + source, 9, color=GREY)
        text(slide, 11000000, 6400800, 800000, 300000, str(n), 9, color=GREY, align=PP_ALIGN.RIGHT)

    HEAD, BAND, PICK = RGBColor(0x24, 0x3B, 0x46), RGBColor(0xF2, 0xF4, 0xF5), RGBColor(0xF8, 0xE5, 0xD8)

    def table(slide, rows, x, y, w, h, bold_row=None, size=13, widths=None):
        shape = slide.shapes.add_table(len(rows), len(rows[0]), Emu(x), Emu(y), Emu(w), Emu(h))
        tb = shape.table
        tb.first_row = True
        tb.horz_banding = False
        if widths:
            for j, f in enumerate(widths):
                tb.columns[j].width = Emu(int(w * f))
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                cell = tb.cell(i, j)
                cell.text = v
                cell.fill.solid()
                cell.fill.fore_color.rgb = HEAD if i == 0 else (PICK if bold_row is not None and r[0] == bold_row
                                                                 else (BAND if i % 2 == 0 else RGBColor(0xFF, 0xFF, 0xFF)))
                para = cell.text_frame.paragraphs[0]
                para.font.size = Pt(size if i else size - 1)
                para.font.name = "Calibri"
                para.font.bold = i == 0 or (bold_row is not None and r[0] == bold_row)
                para.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else INK
                if j:
                    para.alignment = PP_ALIGN.RIGHT
        return tb

    F = o["falls"]
    # 1. the call
    s = prs.slides.add_slide(blank)
    text(s, 457200, 1300000, 11200000, 900000, "Close %s to towed gear in 2027" % win, 36, True, ACC)
    tf = text(s, 457200, 2450000, 11000000, 1500000,
              "%s's haddock stock in 2026 was %d%% below its 2019 to 2021 average, the largest fall of the six grounds "
              "and %d points more than %s's %d%%." % (win, F[win], o["gap"], run, F[run]), 20)
    p = tf.add_paragraph()
    p.text = ("Stock recovery plan, section 4: the ground whose haddock stock has fallen furthest below its base closes "
              "for the following year. Each ground's stock is read from the autumn survey's fixed stations across its "
              "whole stock area.")
    p.font.size, p.font.color.rgb = Pt(14), GREY
    rows = [["Ground"] + [g for g in c["order"]],
            ["Fall in haddock stock, 2026 against 2019 to 2021"] + ["%d%%" % F[g] for g in c["order"]]]
    table(s, rows, 457200, 4300000, 11200000, 900000, size=13, widths=[0.28] + [0.12] * 6)
    footer(s, 1, "autumn gear and bycatch survey 2019 to 2026")
    # 2. the chart
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "%s has fallen furthest below its 2019 to 2021 base" % win, 26, True, INK)
    text(s, 457200, 900000, 11200000, 400000, "Haddock stock on each ground, autumn survey, as a percentage of the ground's "
         "2019 to 2021 average (base = 100)", 13, color=GREY)
    cd = CategoryChartData()
    cd.categories = [str(y) for y in K.YEARS]
    order = [win, run] + [g for g in c["order"] if g not in (win, run)]
    for g in order:
        cd.add_series(g, [round(o["pct"][g][y], 1) for y in K.YEARS])
    cd.add_series("Base (2019 to 2021 average)", [100.0] * len(K.YEARS))
    gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Emu(457200), Emu(1350000), Emu(11200000), Emu(4900000), cd)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = True
    ch.legend.position = XL_LEGEND_POSITION.RIGHT
    ch.legend.include_in_layout = False
    ch.legend.font.size = Pt(12)
    palette = [RGBColor(0xB5, 0x48, 0x1C), RGBColor(0x2F, 0x6B, 0x8F), RGBColor(0x8A, 0x9A, 0x5B),
               RGBColor(0xB8, 0x9B, 0x5E), RGBColor(0x8C, 0x72, 0x98), RGBColor(0x6E, 0x86, 0x8F)]
    for k, ser in enumerate(ch.plots[0].series):
        ser.smooth = False
        line = ser.format.line
        if k < len(order):
            line.color.rgb = palette[k]
            line.width = Pt(3.25 if k == 0 else 2.0)
            ser.marker.format.fill.solid()
            ser.marker.format.fill.fore_color.rgb = palette[k]
            ser.marker.format.line.color.rgb = palette[k]
            ser.marker.size = 7 if k == 0 else 5
        else:
            line.color.rgb = GREY
            line.width = Pt(1.5)
            line.dash_style = MSO_LINE_DASH_STYLE.DASH
            from pptx.enum.chart import XL_MARKER_STYLE
            ser.marker.style = XL_MARKER_STYLE.NONE
    va = ch.value_axis
    va.minimum_scale, va.maximum_scale, va.major_unit = 20, 120, 20
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xDD, 0xE2, 0xE5)
    va.tick_labels.font.size = Pt(12)
    va.tick_labels.number_format, va.tick_labels.number_format_is_linked = "0", False
    ch.category_axis.tick_labels.font.size = Pt(12)
    footer(s, 2, "autumn gear and bycatch survey 2019 to 2026; ground_grid_annex_a.csv")
    # 3. every ground's fall
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "Every ground's fall, 2026 against its 2019 to 2021 average", 26, True, INK)
    rows = [["Ground", "Base 2019-21 (kg a tow)", "2026 (kg a tow)", "Fall"]]
    for g in c["order"]:
        rows.append([g, "%.1f" % o["base"][g], "%.1f" % o["ix"][g][2026], "%d%%" % F[g]])
    table(s, rows, 457200, 1300000, 11200000, 3300000, bold_row=win, size=15)
    text(s, 457200, 4900000, 11200000, 900000, "Stock is the mean haddock catch per standard tow in each depth band, "
         "weighted by the band's share of the ground's stock area. The gap between %s and %s is worked from the "
         "unrounded falls." % (win, run), 13, color=GREY)
    footer(s, 3, "autumn gear and bycatch survey 2019 to 2026; ground_grid_annex_a.csv")
    # 4. why not the catch rates
    s = prs.slides.add_slide(blank)
    hb = o["bands"]
    text(s, 457200, 300000, 11200000, 700000, "On %s the boats followed the fish into the deep band" % win, 26, True, INK)
    deep = hb[(win, "C")]
    cp = whole(100 * o["cpue"][win])
    moved = ("rose %d%%" % -cp) if cp < 0 else ("fell only %d%%" % cp)
    lines = [
        "Members towed %d of %s's %d cells in 2019 and %d in 2026. The cells they left are the ones the stock emptied "
        "first, so their catch per hour towed there %s while the stock fell %d%%." % (
            o["worked"][win][2019], win, sum(hb[(win, b)]["cells"] for b in K.BANDS), o["worked"][win][2026],
            moved, F[win]),
        "The survey tows the same twelve stations in each depth band every October, whatever they hold. Weighting each "
        "band by its share of the ground's area counts the deep band, %d%% of the area, for what it holds and no more."
        % whole(100 * deep["share"]),
    ]
    tf = text(s, 457200, 1250000, 11200000, 1900000, lines[0], 16)
    for line in lines[1:]:
        p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(16)
        p.space_before = Pt(10)
    rows = [["%s, depth band" % win, "Share of stock area", "2019 to 2021 (kg a tow)", "2026 (kg a tow)"]]
    for b in K.BANDS:
        x = hb[(win, b)]
        rows.append(["%s (%s)" % (b, K.BAND_TEXT[b]), "%d%%" % whole(100 * x["share"]),
                     "%.1f" % (sum(x["means"][y] for y in K.BASE) / 3), "%.1f" % x["means"][2026]])
    table(s, rows, 457200, 3500000, 11200000, 1700000, size=14, widths=[0.34, 0.2, 0.24, 0.22])
    footer(s, 4, "e-logbook and tow sheets 2019 to 2026; autumn survey 2019 to 2026")
    # 5. landings and quota
    s = prs.slides.add_slide(blank)
    text(s, 457200, 300000, 11200000, 700000, "Landings by port and quota left by pool", 26, True, INK)
    rows = [["Port", "Haddock landed Jan to Sep 2026 (t live)", "Value at first sale"]]
    for p in K.PORT_NAMES:
        t, v = o["ask_a"][p]
        rows.append([p, "{:,}".format(whole(t)), "£{:,}".format(whole(v))])
    table(s, rows, 457200, 1300000, 6300000, 2400000, size=13)
    rows = [["Pool", "Quota left 30 Sep 2026 (t)"]]
    for code, name in K.POOLS:
        rows.append(["%s (%s)" % (name, code), "{:,}".format(whole(o["ask_b"][code]))])
    table(s, rows, 7100000, 1300000, 4600000, 2800000, size=13)
    text(s, 457200, 4500000, 11200000, 1200000, "A closed ground's boats fish their remaining quota on the other five "
         "grounds; pools with quota left can lease to them under the quota rules.", 14, color=GREY)
    footer(s, 5, "sales notes 2026; quota ledger 2026")
    prs.save(path)


def figures(o):
    c = o["call"]
    return {
        "call": dict(ground=c["pick"], runner_up=c["runner"], gap=o["gap"], fall=o["falls"][c["pick"]],
                     runner_fall=o["falls"][c["runner"]]),
        "falls": o["falls"],
        "rungs": {r: dict(pick=A.call(f)["pick"], falls={g: round(100 * v, 1) for g, v in f.items()})
                  for r, f in o["rungs"].items()},
        "ask_a": {p: dict(tonnes=whole(o["ask_a"][p][0]), value=whole(o["ask_a"][p][1])) for p in K.PORT_NAMES},
        "ask_b": {p: whole(o["ask_b"][p]) for p in K.POOL_CODES},
        "params": dict(base_years=K.BASE, latest=K.LATEST, stations_per_band=K.STATIONS_PER_BAND, as_of="2026-09-30",
                       gutted_factor=1.17, deep_share=whole(100 * o["bands"][(c["pick"], "C")]["share"]),
                       plan_clauses=[float(K.PLAN_CLAUSES["closure"]), float(K.PLAN_CLAUSES["stock"])], chart_base=100),
    }


def write(target, golden, T=None):
    o = results(target)
    if os.path.exists(golden):
        shutil.rmtree(golden)
    os.makedirs(golden)
    workbook(os.path.join(golden, XLSX), o)
    deck(os.path.join(golden, PPTX), o)
    PP.COMPANY = K.ORG_LTD
    PP.normalize_ooxml(os.path.join(golden, XLSX), K.PEOPLE["science"], K.PEOPLE["science"], "2026-11-09T10:14:22Z",
                       "2026-11-20T16:41:05Z", excel=True)
    PP.normalize_ooxml(os.path.join(golden, PPTX), K.PEOPLE["science"], K.PEOPLE["ceo"], "2026-11-23T09:02:47Z",
                       "2026-12-01T17:26:31Z", title="Ground closure 2027")
    json.dump(figures(o), open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    meta = {"distractor_files": ["target/" + K.FILES[k] for k in K.DISTRACTORS], "deliverables": [XLSX, PPTX],
            "stated_inputs": []}
    json.dump(meta, open(os.path.join(os.path.dirname(HERE), "metadata.json"), "w"), indent=2)
    return o
