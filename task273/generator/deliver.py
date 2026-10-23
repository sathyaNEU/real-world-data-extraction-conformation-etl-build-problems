"""The golden deliverables: fleet_safety_programme_2027.xlsx (the coverage test for each use, the miles by stratum
behind it, the people killed and seriously injured and the cost of the crashes each use's drivers caused) and
fleet_safety_programme_2027.pptx (the coverage briefing), plus figures.json."""
import io
import json
import os

import analysis as AN
import common as K

GREY_TEXT = "52514E"
INK = "0B0B0B"
BLUE = "2A78D6"
GREY_BAR = "B4B2AA"
DAY = {"wd": "Weekday", "we": "Weekend"}
WORD = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven"}


def r1(x):
    return AN.half_up(x, 1)


def joined(xs):
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


# the uses as a sentence names them; the short labels stay for table rows and chart ticks
PLAIN = {"Taxi": "taxicabs", "Ride-hail": "ride-hail", "Limousine": "limousines", "Airport shuttle": "airport shuttles",
         "Paratransit": "paratransit", "Parcel delivery": "parcel delivery", "App delivery": "app-based delivery"}


def said(labels):
    return joined([PLAIN[x] for x in labels])


def cap(s):
    return s[:1].upper() + s[1:]


def figures(D):
    g = AN.golden(D)
    people = AN.ask_people(D)
    cost, cost_raw = AN.ask_cost(D)
    region = sum(v for byy in D.vmt.values() for v in byy.values())
    per100 = {u: g["af"].get(u, 0) / g["miles"][u] * 100.0 for u in K.CODES + ["PV"]}
    out = dict(
        call=dict(count=len(g["covered"]), covered=[K.LABEL[u] for u in g["covered"]],
                  not_covered=[K.LABEL[u] for u in K.CODES if u not in g["covered"]]),
        uses={K.LABEL[u]: dict(crashes_caused=g["af"].get(u, 0), ratio=r1(g["ratio"][u]),
                               miles_millions=int(AN.half_up(g["miles"][u])), per_100m=r1(per100[u]),
                               covered=u in g["covered"]) for u in K.CODES},
        private=dict(crashes_caused=g["af"]["PV"], miles_millions=int(AN.half_up(g["miles"]["PV"])),
                     per_100m=r1(per100["PV"])),
        region_miles_millions=r1(region), threshold=K.THRESHOLD,
        asks=dict(ksi={K.LABEL[u]: people[u] for u in K.CODES},
                  cost_millions={K.LABEL[u]: cost[u] for u in K.CODES}),
    )
    mi, E, n, tot = D.miles()
    out["sample"] = dict(crashes_between_moving=sum(1 for _ in D.mv_crashes()), struck_vehicles=sum(tot.values()),
                         strata=len(tot))
    above = min((g["ratio"][u], u) for u in g["covered"])
    below = sorted(((g["ratio"][u], u) for u in K.CODES if u not in g["covered"]), reverse=True)
    # the uses under the line are stated by the tenth they all stay under, which every way of cutting the strata
    # keeps; their own tenths move between 1.2 and 1.3 with the cut (checks.py FAMILY)
    under = (int(below[0][0] * 10) + 1) / 10.0
    out["nearest"] = dict(above=[K.LABEL[above[1]], r1(above[0])], under=[[K.LABEL[u] for v, u in below], under])
    return out, g


def strata_rows(D):
    mi, E, n, tot = D.miles()
    rows = []
    for gr in K.GROUPS:
        for d in ("wd", "we"):
            for h in range(24):
                k = (gr, d, h)
                if k not in E:
                    continue
                t = tot.get(k, 0)
                row = [K.GROUP_NAME[gr], DAY[d], "%02d:00 to %02d:00" % (h, (h + 1) % 24), E[k], t]
                for u in K.CODES + ["PV"]:
                    x = n.get((u, k), 0)
                    row += [x, E[k] * x / t if t else 0.0]
                rows.append(row)
    return rows


# ------------------------------------------------------------------------------------------------ the workbook
def workbook(path, D, fig, g):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Coverage test"
    head_fill = PatternFill("solid", fgColor="1F4D3A")
    hit = PatternFill("solid", fgColor="E3EEF9")
    thin = Side(style="thin", color="9A9890")
    cov = fig["call"]["covered"]
    ws["A1"] = "Commercial Fleet Safety Programme: coverage test on the crashes of 2021 to 2025"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "%s of the seven uses meet the test: %s." % (WORD[len(cov)], said(cov))
    ws["A2"].font = Font(bold=True, color="1F4D3A")
    ws["A3"] = ("A use is covered when its drivers caused crashes at a rate per mile driven of at least 1.5 times "
                "private drivers' rate (coverage rule 3.1).")
    ws["A3"].font = Font(color=GREY_TEXT, italic=True)
    ws.append([])
    ws.append(["Use", "Crashes caused, 2021 to 2025", "Miles driven, 2021 to 2025 (millions)",
               "Crashes caused per 100 million miles", "Rate against private drivers'", "Covered"])
    hr = ws.max_row
    for c in ws[hr]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[hr].height = 32
    for u in sorted(K.CODES, key=lambda u: -g["ratio"][u]):
        f = fig["uses"][K.LABEL[u]]
        ws.append([K.RULE_NAME[u], f["crashes_caused"], f["miles_millions"], f["per_100m"], f["ratio"],
                   "Yes" if f["covered"] else "No"])
        if f["covered"]:
            for c in ws[ws.max_row]:
                c.fill = hit
    p = fig["private"]
    ws.append(["Private drivers (cars, SUVs, pickups and vans in personal use)", p["crashes_caused"],
               p["miles_millions"], p["per_100m"], 1.0, "Reference"])
    for c in ws[ws.max_row]:
        c.font = Font(italic=True)
        c.border = Border(top=thin)
    for row in ws.iter_rows(min_row=hr + 1, max_row=ws.max_row):
        row[1].number_format = "#,##0"
        row[2].number_format = "#,##0"
        row[3].number_format = "0.0"
        row[4].number_format = "0.0"
        row[5].alignment = Alignment(horizontal="center")
    ws.append([])
    for t in ["Crashes: between two or more motor vehicles in transport on public roads in Stonereach County (rule "
              "4.1), each counted once for every use whose driver the officer recorded at fault (rules 3.2 and 4.2); "
              "state crash records extract of 30 September 2026.",
              "Miles: no record counts them by use. In each road class, day type and hour, the Department's miles "
              "(Travel Monitoring Report Table 1, spread over the week by the class's 2025 count station hours) are "
              "shared among the uses in proportion to the vehicles at-fault drivers struck there; sheet Miles by "
              "stratum.",
              "Rates against private drivers' are shown to one decimal; the test is applied to the unrounded rates."]:
        ws.append([t])
        ws.cell(ws.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=6)
        ws.row_dimensions[ws.max_row].height = 44
        ws.cell(ws.max_row, 1).font = Font(color=GREY_TEXT, size=9)
    for col, wd in zip("ABCDEF", (56, 16, 20, 18, 16, 11)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = ws.cell(hr + 1, 2)
    ws.print_title_rows = "%d:%d" % (hr, hr)

    w2 = wb.create_sheet("Miles by stratum")
    cols = ["Road class", "Day type", "Hour", "Department miles, 2021 to 2025 (millions)", "Vehicles struck, all uses"]
    for u in K.CODES + ["PV"]:
        nm = K.LABEL.get(u, "Private drivers")
        cols += ["%s: vehicles struck" % nm, "%s: miles (millions)" % nm]
    w2.append(cols)
    for c in w2[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="center")
    w2.row_dimensions[1].height = 58
    for r in strata_rows(D):
        w2.append(r)
    last = w2.max_row
    for row in w2.iter_rows(min_row=2, max_row=last):
        row[3].number_format = "#,##0.0"
        row[4].number_format = "#,##0"
        for j in range(5, len(row)):
            row[j].number_format = "#,##0" if (j - 5) % 2 == 0 else "#,##0.0"
    tot = ["All strata", None, None]
    for j in range(4, len(cols) + 1):
        L = get_column_letter(j)
        tot.append("=SUM(%s2:%s%d)" % (L, L, last))
    w2.append(tot)
    for j, c in enumerate(w2[w2.max_row]):
        c.font = Font(bold=True)
        c.border = Border(top=thin)
        if j >= 3:
            c.number_format = "#,##0.0" if (j == 3 or (j >= 5 and (j - 5) % 2 == 1)) else "#,##0"
    w2.column_dimensions["A"].width = 42
    w2.column_dimensions["B"].width = 10
    w2.column_dimensions["C"].width = 15
    for j in range(4, len(cols) + 1):
        w2.column_dimensions[get_column_letter(j)].width = 13
    w2.freeze_panes = "D2"
    w2.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(cols)), last)

    w3 = wb.create_sheet("Harm and cost")
    w3.append(["Use", "People killed or seriously injured", "Cost of the crashes (USD millions)"])
    for c in w3[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="center")
    w3.row_dimensions[1].height = 32
    a = fig["asks"]
    for u in K.CODES:
        lab = K.LABEL[u]
        w3.append([K.RULE_NAME[u], a["ksi"][lab], a["cost_millions"][lab]])
    for row in w3.iter_rows(min_row=2):
        row[1].number_format = "#,##0"
        row[2].number_format = "#,##0.0"
    w3.append([])
    for t in ["Every crash of any kind in 2021 to 2025 in which the officer recorded a driver of the use at fault; a "
              "crash with drivers of two uses at fault counts for both.",
              "Killed: died within 30 days of the crash (the state's road fatality register). Seriously injured: "
              "suspected serious injury (A) as the person's latest record on the crash report has it.",
              "Cost: each crash once, at the Department's 2025 unit cost for its most severe injury (guidance note "
              "2025-03)."]:
        w3.append([t])
        w3.cell(w3.max_row, 1).font = Font(color=GREY_TEXT, size=9)
    w3.column_dimensions["A"].width = 58
    for col in "BC":
        w3.column_dimensions[col].width = 20
    w3.freeze_panes = "B2"

    w4 = wb.create_sheet("Notes")
    w4.append(["Item", "Note"])
    for c in w4[1]:
        c.font = Font(bold=True)
    for k, v in [
            ("Prepared by", "%s, Policy Adviser, for the notice to operators due by 15 January 2027" % K.REQUESTER),
            ("Rule", "Commercial Fleet Safety Programme: Coverage Rule, adopted 14 October 2026 (Resolution 2026-41)"),
            ("Crashes", "State crash records system, regional extract of 30 September 2026 (crashes of 2021 to 2025)"),
            ("Miles", "Department of Transportation, Travel Monitoring Report 2025 (Table 1), and the continuous count "
                      "stations' hourly volumes for 2025"),
            ("Uses on 2016 reports", "Vehicles for hire and delivery vehicles take the use of the operator named on the "
                                     "report (operator register, names on crash reports)"),
            ("Not counted", "Crashes with no driver recorded at fault; drivers who left the scene and were not "
                            "identified (rule 4.2)"),
            ("Rounding", "Rates against private drivers' to one decimal, miles to the million, costs to USD 0.1 "
                         "million")]:
        w4.append([k, v])
    w4.column_dimensions["A"].width = 24
    w4.column_dimensions["B"].width = 110
    w2.print_title_rows = "1:1"
    for sh in wb.worksheets:
        # printed landscape, one page wide, as the sheets are read in the briefing pack
        sh.page_setup.orientation = "landscape"
        sh.page_setup.fitToWidth = 1
        sh.page_setup.fitToHeight = 0
        sh.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


# ------------------------------------------------------------------------------------------------ the deck
def chart_png(g):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    order = sorted(K.CODES, key=lambda u: g["ratio"][u])
    vals = [g["ratio"][u] for u in order]
    colors = ["#" + (BLUE if u in g["covered"] else GREY_BAR) for u in order]
    fig, ax = plt.subplots(figsize=(9.6, 4.9), dpi=150)
    fig.patch.set_facecolor("#FCFCFB")
    ax.set_facecolor("#FCFCFB")
    bars = ax.barh(range(len(order)), vals, color=colors, height=0.62, edgecolor="#FCFCFB", linewidth=2)
    ax.axvline(K.THRESHOLD, color="#0B0B0B", linewidth=1.6)
    ax.text(K.THRESHOLD + 0.02, len(order) - 0.45, "Coverage line: 1.5 times private drivers' rate", fontsize=9,
            color="#0B0B0B", va="bottom")
    ax.axvline(1.0, color="#52514E", linewidth=1.0, linestyle=(0, (3, 3)))
    ax.text(1.0 + 0.02, -0.82, "Private drivers: 1.0", fontsize=8.5, color="#52514E", va="bottom")
    for b, v in zip(bars, vals):
        ax.text(v + 0.03, b.get_y() + b.get_height() / 2, "%.1f" % r1(v), va="center", fontsize=10, color="#0B0B0B")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([K.LABEL[u] for u in order], fontsize=10.5, color="#0B0B0B")
    ax.set_xlim(0, max(vals) + 0.5)
    ax.set_ylim(-0.95, len(order) - 0.05)
    ax.set_xlabel("Crashes caused per mile driven, 2021 to 2025, against private drivers' rate", fontsize=9.5,
                  color="#52514E")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#9A9890")
    ax.tick_params(axis="x", colors="#52514E", labelsize=9)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#E4E2DC", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def deck(path, fig, g):
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    from pptx.util import Inches, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, s, size=14, bold=False, color=INK):
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        for i, line in enumerate(s if isinstance(s, list) else [s]):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.text = line
            p.font.size = Pt(size)
            p.font.bold = bold
            p.font.color.rgb = RGBColor.from_string(color)
            p.font.name = "Calibri"
            p.space_after = Pt(8)
        return tb

    def strip(slide, n, src):
        text(slide, 0.6, 7.0, 11.0, 0.35, src, size=9, color=GREY_TEXT)
        text(slide, 12.3, 7.0, 0.6, 0.35, str(n), size=9, color=GREY_TEXT)

    def table(slide, x, y, w, rows, widths, size=12):
        t = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w),
                                   Inches(0.38 * len(rows))).table
        for j, wd in enumerate(widths):
            t.columns[j].width = Inches(wd)
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                cell = t.cell(i, j)
                cell.text = str(v)
                para = cell.text_frame.paragraphs[0]
                para.font.size = Pt(size)
                para.font.bold = i == 0
                para.font.name = "Calibri"
                para.font.color.rgb = RGBColor.from_string("FFFFFF" if i == 0 else INK)
                if j > 0:
                    para.alignment = PP_ALIGN.RIGHT
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor.from_string("1F4D3A" if i == 0 else
                                                                ("F4F3EF" if i % 2 == 0 else "FFFFFF"))

    cov = fig["call"]["covered"]
    s = prs.slides.add_slide(blank)
    text(s, 0.8, 2.3, 11.6, 1.4, "%s of the seven commercial uses meet the coverage test" % WORD[len(cov)], size=34,
         bold=True, color="1F4D3A")
    text(s, 0.8, 3.75, 11.6, 1.6, ["Commercial Fleet Safety Programme: the uses covered from 1 July 2027",
                                   "Briefing ahead of the notice to operators, due by 15 January 2027",
                                   "%s, Policy Adviser" % K.REQUESTER], size=16, color=GREY_TEXT)

    s = prs.slides.add_slide(blank)
    text(s, 0.6, 0.35, 12.1, 1.0, "%s cause crashes at 1.5 times private drivers' rate per mile or more" % cap(said(cov)),
         size=22, bold=True)
    s.shapes.add_picture(io.BytesIO(chart_png(g)), Inches(1.45), Inches(1.4), width=Inches(10.4))
    strip(s, 2, "Crashes between moving vehicles, 2021 to 2025 (state crash records extract); miles by road class, "
                "day type and hour (Department of Transportation).")

    s = prs.slides.add_slide(blank)
    above, below = fig["nearest"]["above"], fig["nearest"]["under"]
    text(s, 0.6, 0.35, 12.1, 1.0, "No record counts the miles each use drives, so the crash reports measure them",
         size=22, bold=True)
    text(s, 0.6, 1.5, 5.7, 5.2, [
        "A vehicle struck by an at-fault driver is a draw from the traffic around it, so a use's share of the "
        "vehicles struck on a class of road in a given hour is its share of the miles driven there.",
        "Crashes per mile are far from even: they run highest on urban arterials at night, so the struck vehicles "
        "over-represent the uses that work those streets and hours.",
        "The Department's miles for each road class, day type and hour are shared out by the vehicles struck there, "
        "and each use's shares add up to its miles.",
        "Closest to the line: %s at %.1f times private drivers' rate, covered; %s all under %.1f, not covered."
        % (cap(PLAIN[above[0]]), above[1], said(below[0]), below[1])], size=14)
    rows = [["Use", "Crashes caused", "Miles (millions)", "Per 100 million miles", "Against private"]]
    for u in sorted(K.CODES, key=lambda u: -g["ratio"][u]):
        f = fig["uses"][K.LABEL[u]]
        rows.append([K.LABEL[u], "{:,}".format(f["crashes_caused"]), "{:,}".format(f["miles_millions"]),
                     "%.1f" % f["per_100m"], "%.1f" % f["ratio"]])
    p = fig["private"]
    rows.append(["Private drivers", "{:,}".format(p["crashes_caused"]), "{:,}".format(p["miles_millions"]),
                 "%.1f" % p["per_100m"], "1.0"])
    table(s, 6.55, 1.55, 6.3, rows, [1.75, 1.15, 1.15, 1.25, 1.0], size=11)
    strip(s, 3, "Miles by stratum: fleet_safety_programme_2027.xlsx, sheet Miles by stratum.")

    s = prs.slides.add_slide(blank)
    top = max(K.CODES, key=lambda u: fig["asks"]["ksi"][K.LABEL[u]])
    top_cost = max(K.CODES, key=lambda u: fig["asks"]["cost_millions"][K.LABEL[u]])
    text(s, 0.6, 0.35, 12.1, 1.0, "%s drivers caused the crashes that killed or seriously injured the most people%s"
         % (cap(PLAIN[K.LABEL[top]]), ", and cost the most" if top_cost == top else ""), size=22, bold=True)
    rows = [["Use, 2021 to 2025", "People killed or seriously injured", "Cost (USD millions)"]]
    a = fig["asks"]
    for u in K.CODES:
        lab = K.LABEL[u]
        rows.append([lab, "{:,}".format(a["ksi"][lab]), "{:,.1f}".format(a["cost_millions"][lab])])
    table(s, 0.9, 1.55, 8.4, rows, [2.8, 3.2, 2.4], size=13)
    strip(s, 4, "Every crash of any kind in which a driver of the use was recorded at fault; deaths within 30 days; the "
                "Department's 2025 crash unit costs.")

    s = prs.slides.add_slide(blank)
    text(s, 0.6, 0.35, 12.1, 1.0, "What the operators are told by 15 January", size=22, bold=True)
    text(s, 0.6, 1.5, 12.0, 4.5, [
        "Covered from 1 July 2027: %s." % said(cov),
        "Not covered: %s." % said(fig["call"]["not_covered"]),
        "Operators of the covered uses fit telematics to every vehicle they run in the use and enrol its drivers in "
        "coaching. The test is run again every three years on the latest five years of crashes."], size=16)
    strip(s, 5, "Coverage rule, adopted 14 October 2026 (Resolution 2026-41).")
    prs.core_properties.author = K.REQUESTER
    prs.core_properties.title = "Commercial Fleet Safety Programme: coverage 2027"
    prs.save(path)


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")


def write(target, golden):
    D = AN.Data(target)
    fig, g = figures(D)
    os.makedirs(golden, exist_ok=True)
    workbook(os.path.join(golden, K.DELIVERABLES[0]), D, fig, g)
    deck(os.path.join(golden, K.DELIVERABLES[1]), fig, g)
    return fig, dict(D=D, g=g)
