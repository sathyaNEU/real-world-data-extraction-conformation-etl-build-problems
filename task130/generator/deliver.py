"""The goldens, computed from the pack in target/: trust_funding_2027.xlsx (the contribution with the expected claims
and cost by entity and by specialty class, the emergence by month, the carrier loss run check and the September 2026
covered FTE) and trustees_paper_2027.pptx (the contribution, and the chart of each entity's expected cost by the month
the claims are made), plus generator/figures.json for the write-up."""
from __future__ import annotations

import io
import json
import math
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt     # noqa: E402
import openpyxl                     # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill   # noqa: E402
from openpyxl.utils import get_column_letter                # noqa: E402
from pptx import Presentation       # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.enum.text import PP_ALIGN  # noqa: E402
from pptx.util import Cm, Pt         # noqa: E402

import analysis as AN    # noqa: E402
import asks as A         # noqa: E402
import common as K       # noqa: E402
import postprocess as PP  # noqa: E402

BOOK, DECK = K.DELIVERABLES
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
NAVY, SLATE, PAPER, LINE = "#1f2f3f", "#5a6672", "#ffffff", "#d5dbe1"
ENTITY_COLOURS = {"TFH": "#2f5f8a", "AMC": "#7fa6c9", "CMG": "#c98b3f", "BCH": "#8a9a5b"}


def r1000(x):
    return int(math.floor(x / 1000.0 + 0.5) * 1000)


def r1(x):
    return math.floor(x * 10 + 0.5) / 10


def money(x):
    return "{:,}".format(r1000(x))


def long_date(d):
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def compute(target):
    m = AN.main_call(target)
    a = A.ask_a(target, m["rows"])
    b = A.ask_b(target)
    return dict(m=m, a=a, b=b)


def figures(c):
    m, a, b = c["m"], c["a"], c["b"]
    ex = m["ex"]
    fig = {"call": {"contribution": money(m["total"]), "contribution_usd": "$" + money(m["total"])}}
    fig["entities"] = {}
    for e in K.ENTITY_ORDER:
        v = m["ent"][e]
        fig["entities"][e] = {"name": K.ENTITIES[e]["name"], "transition": long_date(K.ENTITIES[e]["transition"]),
                              "fte_years_2027": "%.1f" % r1(v["fte_years"]), "expected_claims": "%.1f" % r1(v["count"]),
                              "expected_cost": money(v["cost"])}
    fig["classes"] = {}
    for k in K.CLASSES:
        v = m["cls"][k]
        fig["classes"][k] = {"name": K.CLASS_NAME[k], "fte_years_2027": "%.1f" % r1(v["fte_years"]),
                             "expected_claims": "%.1f" % r1(v["count"]), "expected_cost": money(v["cost"])}
    tot_n = sum(v["count"] for v in m["ent"].values())
    fig["totals"] = {"expected_claims": "%.1f" % r1(tot_n), "expected_cost": money(m["total"]),
                     "fte_years_2027": "%.1f" % r1(sum(v["fte_years"] for v in m["ent"].values()))}
    fig["experience"] = {"claims": len(ex), "claims_made_within_364_days": sum(1 for x in ex if x["lag"] <= 364),
                         "fte_years": "{:,.1f}".format(sum(m["E"].values())), "trend_pct": "5.0"}
    fig["by_month"] = {e: [money(x) for x in m["months"][e]] for e in K.ENTITY_ORDER}
    fig["ask_a"] = {}
    for e in K.ENTITY_ORDER:
        v = a[e]
        fig["ask_a"][e] = {"any_missing": "yes" if v["count"] else "no", "count": v["count"],
                           "reserves": money(v["reserves"]), "open_claims": v["open"],
                           "carrier": K.CARRIERS[K.ENTITIES[e]["carrier"]]}
    fig["ask_b"] = {e: "%.1f" % b["gold"][e] for e in K.ENTITY_ORDER}
    fig["ask_b_total"] = "%.1f" % r1(sum(b["raw"].values()))
    fig["rungs"] = {k: money(v) for k, v in m["rungs"].items()}
    return fig


# ------------------------------------------------------------------------------------------------ workbook
HEAD = PatternFill("solid", fgColor="DCE3EA")
TOTAL = PatternFill("solid", fgColor="F1F3F5")
B = Font(name="Calibri", size=11, bold=True)
T = Font(name="Calibri", size=14, bold=True)
NOTE_FONT = Font(name="Calibri", size=10, italic=True, color="595959")


def _head(ws, row, values):
    for c, v in enumerate(values, start=1):
        cell = ws.cell(row=row, column=c, value=v if v != "" else None)
        cell.font = B
        cell.fill = HEAD
        cell.alignment = Alignment(horizontal="left" if c == 1 else "right", wrap_text=True, vertical="bottom")


def write_book(path, c):
    m, a, b = c["m"], c["a"], c["b"]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contribution"
    ws["A1"] = "Corvane Professional Liability Trust: 2027 contribution"
    ws["A1"].font = T
    ws["A2"] = "Expected cost of the Claims first made against the Trust in 2027, at 2027 cost level (funding policy 3.1)"
    ws["A4"] = "2027 Contribution ($)"
    ws["A4"].font = B
    ws["B4"] = r1000(m["total"])
    ws["B4"].font = B
    ws["B4"].number_format = "#,##0"
    ws["A6"] = "By Participating Entity"
    ws["A6"].font = B
    _head(ws, 7, ["Participating Entity", "Joins the Trust", "Covered FTE-years in the Trust, 2027",
                  "Expected Claims", "Expected cost ($)"])
    r = 8
    for e in K.ENTITY_ORDER:
        v = m["ent"][e]
        for col, val, fmt in ((1, K.ENTITIES[e]["name"], None), (2, long_date(K.ENTITIES[e]["transition"]), None),
                              (3, r1(v["fte_years"]), "0.0"), (4, r1(v["count"]), "0.0"), (5, r1000(v["cost"]), "#,##0")):
            cell = ws.cell(row=r, column=col, value=val)
            if fmt:
                cell.number_format = fmt
            if col > 1:
                cell.alignment = Alignment(horizontal="right")
        r += 1
    tot_n = sum(v["count"] for v in m["ent"].values())
    tot_x = sum(v["fte_years"] for v in m["ent"].values())
    for col, val, fmt in ((1, "All entities", None), (3, r1(tot_x), "0.0"), (4, r1(tot_n), "0.0"),
                          (5, r1000(m["total"]), "#,##0")):
        cell = ws.cell(row=r, column=col, value=val)
        cell.font = B
        cell.fill = TOTAL
        if fmt:
            cell.number_format = fmt
    for col in (2,):
        ws.cell(row=r, column=col).fill = TOTAL
    r += 2
    ws.cell(row=r, column=1, value="By specialty class").font = B
    r += 1
    _head(ws, r, ["Specialty class", "", "Covered FTE-years in the Trust, 2027", "Expected Claims", "Expected cost ($)"])
    r += 1
    for k in K.CLASSES:
        v = m["cls"][k]
        ws.cell(row=r, column=1, value=K.CLASS_NAME[k])
        for col, val, fmt in ((3, r1(v["fte_years"]), "0.0"), (4, r1(v["count"]), "0.0"), (5, r1000(v["cost"]), "#,##0")):
            cell = ws.cell(row=r, column=col, value=val)
            cell.number_format = fmt
        r += 1
    for col, val, fmt in ((1, "All classes", None), (3, r1(tot_x), "0.0"), (4, r1(tot_n), "0.0"),
                          (5, r1000(m["total"]), "#,##0")):
        cell = ws.cell(row=r, column=col, value=val)
        cell.font = B
        cell.fill = TOTAL
        if fmt:
            cell.number_format = fmt
    ws.cell(row=r, column=2).fill = TOTAL
    r += 1
    ws.cell(row=r, column=1, value="Brennick Community Hospital joins on 1 October 2027: three months of exposure, and "
                                   "only the Claims made by 31 December count.").font = NOTE_FONT
    r += 1
    ws.cell(row=r, column=1, value="Source: risk management claims register extract valued 30 September 2026; legacy "
                                   "payroll 2017 to 2024; clinician staffing plan 2027, version 2026-09-29. Basis and "
                                   "definitions on the Notes sheet.").font = NOTE_FONT
    for col, wd in zip(range(1, 6), [34, 18, 22, 16, 18]):
        ws.column_dimensions[get_column_letter(col)].width = wd

    ws2 = wb.create_sheet("By month")
    ws2["A1"] = "Expected cost of the Trust's 2027 Claims by the month they are made ($)"
    ws2["A1"].font = T
    _head(ws2, 3, ["Month made"] + [K.ENTITIES[e]["name"] for e in K.ENTITY_ORDER] + ["All entities"])
    for i in range(12):
        ws2.cell(row=4 + i, column=1, value="%s 2027" % MONTH_NAMES[i])
        for j, e in enumerate(K.ENTITY_ORDER):
            cell = ws2.cell(row=4 + i, column=2 + j, value=r1000(m["months"][e][i]))
            cell.number_format = "#,##0"
        cell = ws2.cell(row=4 + i, column=6, value=r1000(sum(m["months"][e][i] for e in K.ENTITY_ORDER)))
        cell.number_format = "#,##0"
    ws2.cell(row=16, column=1, value="2027").font = B
    for j, e in enumerate(K.ENTITY_ORDER):
        cell = ws2.cell(row=16, column=2 + j, value=r1000(m["ent"][e]["cost"]))
        cell.number_format = "#,##0"
        cell.font = B
    cell = ws2.cell(row=16, column=6, value=r1000(m["total"]))
    cell.number_format = "#,##0"
    cell.font = B
    ws2.cell(row=18, column=1, value="Monthly figures are rounded separately and may not add to the year. Each entity "
                                     "counts from its Transition Date.").font = NOTE_FONT
    for col, wd in zip(range(1, 7), [14, 22, 24, 22, 26, 14]):
        ws2.column_dimensions[get_column_letter(col)].width = wd
    ws2.freeze_panes = "B4"

    ws3 = wb.create_sheet("Carrier loss runs")
    ws3["A1"] = "Open claims under each entity's occurrence policies missing from its carrier's latest loss run"
    ws3["A1"].font = T
    _head(ws3, 3, ["Participating Entity", "Carrier", "Latest loss run", "Open claims in the register",
                   "Missing from the loss run", "Our reserves on them ($)"])
    for i, e in enumerate(K.ENTITY_ORDER):
        v = a[e]
        vals = [K.ENTITIES[e]["name"], K.CARRIERS[K.ENTITIES[e]["carrier"]], "valued 30 September 2026", v["open"],
                v["count"] if v["count"] else "None", r1000(v["reserves"])]
        for col, val in enumerate(vals, start=1):
            cell = ws3.cell(row=4 + i, column=col, value=val)
            if col == 6:
                cell.number_format = "#,##0"
            if col >= 4:
                cell.alignment = Alignment(horizontal="right")
    rr = 10
    ws3.cell(row=rr - 1, column=1, value="Claims missing from the loss runs").font = B
    _head(ws3, rr, ["Participating Entity", "Claim number", "Incident number", "Claim made", "Matter type",
                    "Our reserves ($)"])
    rr += 1
    rows = m["rows"]
    for e in K.ENTITY_ORDER:
        line = K.ENTITIES[e]["line"]
        for ino in a[e]["missing"]:
            rs = [x for x in rows if x["incident_no"] == ino and x["coverage_line"] == line]
            first = sorted(rs, key=lambda x: (x["claim_made_date"], x["claim_no"]))[0]
            res = sum((x["indemnity_reserve"] or 0) + (x["defense_reserve"] or 0) for x in rs)
            for col, val in enumerate([K.ENTITIES[e]["name"], first["claim_no"], ino,
                                       first["claim_made_date"].strftime("%d %b %Y").lstrip("0"),
                                       first["matter_type"], r1000(res)], start=1):
                cell = ws3.cell(row=rr, column=col, value=val)
                if col == 6:
                    cell.number_format = "#,##0"
            rr += 1
    rr += 1
    for t in ("Quillan Mutual's latest run is the one valued 30 September 2026 (issued 6 October 2026); revision 1 of "
              "its 30 June 2026 run, issued 9 October 2026, is an earlier valuation.",
              "Claims that began as precautionary notices are carried on the runs under their notice numbers (RMN), "
              "which the notice log ties to incident numbers; a suit that followed an earlier claim number for the "
              "same incident stays under that earlier number. Stoneleigh drops the punctuation from references.",
              "Missing: open in the register at 30 September 2026 under the entity's coverage line, one per incident, "
              "with no record on the run. Reserves are the register's indemnity and defense reserves on our rows."):
        ws3.cell(row=rr, column=1, value=t).font = NOTE_FONT
        rr += 1
    for col, wd in zip(range(1, 7), [30, 44, 24, 18, 18, 22]):
        ws3.column_dimensions[get_column_letter(col)].width = wd

    ws4 = wb.create_sheet("Covered FTE Sep 2026")
    ws4["A1"] = "Covered Clinician FTE in September 2026, HCM pay lines"
    ws4["A1"].font = T
    _head(ws4, 3, ["Participating Entity", "Covered clinician FTE"])
    for i, e in enumerate(K.ENTITY_ORDER):
        ws4.cell(row=4 + i, column=1, value=K.ENTITIES[e]["name"])
        cell = ws4.cell(row=4 + i, column=2, value=b["gold"][e])
        cell.number_format = "0.0"
    ws4.cell(row=8, column=1, value="All entities").font = B
    cell = ws4.cell(row=8, column=2, value=r1(sum(b["raw"].values())))
    cell.number_format = "0.0"
    cell.font = B
    ws4.cell(row=10, column=1, value="One FTE per position held in September 2026, Schedule B jobs through the HCM job "
                                     "profile crosswalk, on the entity of the cost centre the position's lines are "
                                     "charged to.")
    for col, wd in zip(range(1, 3), [34, 24]):
        ws4.column_dimensions[get_column_letter(col)].width = wd

    ws5 = wb.create_sheet("Notes")
    ws5["A1"] = "Notes"
    ws5["A1"].font = T
    notes = [
        ("Claim", "As the Trust Agreement defines it (1.3): every demand, Early Resolution Program request or suit "
                  "from one Medical Incident is one Claim, first made on the date the earliest of them reached Risk "
                  "Management."),
        ("Covered Clinician", "Employed physicians and advanced practice clinicians in a Schedule B job. Residents, "
                              "fellows, psychologists and contracted or locum clinicians are excluded."),
        ("Window", "Each entity from its Transition Date (its Retroactive Date) to 31 December 2027: Claims made in "
                   "2027 from incidents on or after that date."),
        ("Experience", "The %d Claims from incidents in 2017 to 2024 naming Covered Clinicians, valued at paid plus "
                       "case reserves on the Covered Clinicians' rows of the register extract valued 30 September "
                       "2026, trended at 5.0%% a year from the incident year to 2027, against %s covered FTE-years in "
                       "the payroll for the same years, pooled within each specialty class (funding policy 3.2 and "
                       "3.4)." % (len(m["ex"]), "{:,.1f}".format(sum(m["E"].values())))),
        ("Exposure", "The staffing plan's covered FTE for each month from the Transition Date, one twelfth of an "
                     "FTE-year spread evenly over the month's days (funding policy 3.3)."),
        ("Expected cost", "Each day of exposure is charged the experience's cost per FTE-year of the Claims whose delay "
                          "from incident to first making, added to that day, falls on or before 31 December 2027; the "
                          "expected number of Claims is the same sum counting each Claim once."),
        ("Not included", "Administrative expenses, investment income, excess insurance and any margin (funding policy "
                         "3.5)."),
        ("Rounding", "Rounded once, from unrounded amounts: dollars to the nearest thousand, Claims and FTE to one "
                     "decimal."),
        ("As of", "Register extract run 2 October 2026, valued 30 September 2026; HCM pay lines to September 2026; "
                  "carrier loss runs received 5 to 9 October 2026."),
    ]
    for i, (k, t) in enumerate(notes, start=3):
        ws5.cell(row=i, column=1, value=k).font = B
        cell = ws5.cell(row=i, column=2, value=t)
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        ws5.cell(row=i, column=1).alignment = Alignment(vertical="top")
        ws5.row_dimensions[i].height = 15 * (1 + len(t) // 95)
    ws5.column_dimensions["A"].width = 18
    ws5.column_dimensions["B"].width = 100
    for sheet in wb.worksheets:
        sheet.page_setup.orientation = "landscape"
        sheet.page_setup.fitToWidth = 1
        sheet.page_setup.fitToHeight = 0
        sheet.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["requester"], K.PEOPLE["requester"], "2026-10-12T17:05:31Z",
                       "2026-10-14T00:41:09Z", excel=True)


# ------------------------------------------------------------------------------------------------ deck
def write_chart(buf, c):
    m = c["m"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "svg.hashsalt": "t130",
                         "axes.edgecolor": SLATE, "axes.labelcolor": SLATE, "xtick.color": NAVY, "ytick.color": SLATE})
    fig, ax = plt.subplots(figsize=(9.6, 4.6), dpi=200)
    fig.patch.set_facecolor(PAPER)
    ax.set_facecolor(PAPER)
    bottom = [0.0] * 12
    for e in K.ENTITY_ORDER:
        vals = [x / 1000.0 for x in m["months"][e]]
        ax.bar(MONTH_NAMES, vals, bottom=bottom, color=ENTITY_COLOURS[e], width=0.66, edgecolor=PAPER, linewidth=0.8,
               label="%s (from %s)" % (K.ENTITIES[e]["name"], long_date(K.ENTITIES[e]["transition"])))
        bottom = [b_ + v for b_, v in zip(bottom, vals)]
    for i, tot in enumerate(bottom):
        if tot > 0.5:
            ax.text(i, tot + max(bottom) * 0.012, "%d" % round(tot), ha="center", va="bottom", fontsize=8.5,
                    color=NAVY)
    top = max(bottom)
    for x, label in ((2.5, "Alderwick joins 1 Apr"), (5.5, "Medical group joins 1 Jul"), (8.5, "Brennick joins 1 Oct")):
        ax.axvline(x, color=SLATE, linewidth=0.8, linestyle=(0, (3, 3)))
        ax.text(x - 0.08, top * 1.05, label, ha="right", va="top", fontsize=8.2, color=SLATE)
    ax.set_ylabel("Expected cost of Claims made in the month ($000)")
    ax.yaxis.grid(True, color=LINE, linewidth=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="x", length=0)
    ax.set_ylim(0, max(bottom) * 1.12)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.86), frameon=False, fontsize=8.8)
    fig.tight_layout()
    fig.savefig(buf, format="png", facecolor=PAPER, metadata={"Software": None})
    plt.close(fig)


def write_deck(path, c, chart_png):
    m = c["m"]
    navy, slate, pale = RGBColor(0x1F, 0x2F, 0x3F), RGBColor(0x5A, 0x66, 0x72), RGBColor(0xEE, 0xF1, 0xF4)
    prs = Presentation()
    prs.slide_width, prs.slide_height = Cm(33.867), Cm(19.05)
    blank = prs.slide_layouts[6]

    def text(slide, x, y, w, h, runs, size=12, color=slate, bold=False):
        tf = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h)).text_frame
        tf.word_wrap = True
        for k, line in enumerate(runs if isinstance(runs, list) else [runs]):
            p = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = line
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = color
        return tf

    def frame(slide, n, title, sub):
        text(slide, 1.6, 0.9, 30.6, 1.6, title, size=24, color=navy, bold=True)
        text(slide, 1.6, 2.5, 30.6, 1.0, sub, size=13)
        text(slide, 1.6, 17.9, 30.6, 0.7, "Corvane Health, Risk Management and Insurance  |  Trustees of the Corvane "
             "Professional Liability Trust, 10 November 2026  |  %d" % n, size=9)

    s1 = prs.slides.add_slide(blank)
    frame(s1, 1, "2027 contribution to the Trust: $%s" % money(m["total"]),
          "Recommended: the Participating Entities contribute $%s for 2027, the expected cost of the Claims that will "
          "be first made against the Trust in its first Plan Year" % money(m["total"]))
    rows = [["Participating Entity", "Joins the Trust", "Covered FTE-years, 2027", "Expected Claims",
             "Expected cost ($)"]]
    for e in K.ENTITY_ORDER:
        v = m["ent"][e]
        rows.append([K.ENTITIES[e]["name"], long_date(K.ENTITIES[e]["transition"]), "%.1f" % r1(v["fte_years"]),
                     "%.1f" % r1(v["count"]), money(v["cost"])])
    rows.append(["All entities", "", "%.1f" % r1(sum(v["fte_years"] for v in m["ent"].values())),
                 "%.1f" % r1(sum(v["count"] for v in m["ent"].values())), money(m["total"])])
    widths = [8.4, 5.6, 6.0, 4.6, 5.6]
    tb = s1.shapes.add_table(len(rows), 5, Cm(1.6), Cm(4.3), Cm(sum(widths)), Cm(0.95 * len(rows))).table
    for j, wd in enumerate(widths):
        tb.columns[j].width = Cm(wd)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tb.cell(i, j)
            cell.text = val
            cell.fill.solid()
            last = i == len(rows) - 1
            cell.fill.fore_color.rgb = navy if i == 0 else (pale if last else RGBColor(0xFF, 0xFF, 0xFF))
            para = cell.text_frame.paragraphs[0]
            if not para.runs:
                para.add_run()
            run = para.runs[0]
            run.font.size = Pt(12 if i else 11)
            run.font.bold = i == 0 or last
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else navy
            if j >= 2:
                para.alignment = PP_ALIGN.RIGHT
    text(s1, 1.6, 11.0, 30.6, 6.0, [
        "Each entity joins on the day its occurrence policy expires, and the Trust is claims-made with each entity's "
        "Transition Date as its Retroactive Date: in 2027 it pays only for Claims made by 31 December from incidents "
        "after the entity joined.",
        "In the System's 2017 to 2024 experience the Claims made within a few months of their incident settled small, "
        "and most of the cost sits in Claims made a year or more after it. Costed claim by claim on that experience, "
        "the first year is a fraction of a mature year's cost.",
        "No provision for expenses, investment income, excess insurance or margin (funding policy 3.5)."], size=12)

    s2 = prs.slides.add_slide(blank)
    frame(s2, 2, "The 2027 cost builds through the year as each entity joins",
          "Expected cost of the Claims made against the Trust in each month of 2027, by entity, $000 at 2027 cost level")
    s2.shapes.add_picture(chart_png, Cm(2.6), Cm(3.5), width=Cm(27.6))
    text(s2, 1.6, 16.9, 30.6, 0.8, "Source: risk management claims register valued 30 September 2026 (incidents 2017 "
         "to 2024, trended at 5.0% a year); clinician staffing plan 2027. Each entity counts from its Transition Date.",
         size=9)
    prs.core_properties.title = "Trust contribution 2027"
    prs.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["requester"], K.PEOPLE["requester"], "2026-10-13T16:22:05Z",
                       "2026-10-14T01:10:47Z", title="Trust contribution 2027")


def main(target, golden, figures_path, world=None):
    os.makedirs(golden, exist_ok=True)
    c = compute(target)
    fig = figures(c)
    write_book(os.path.join(golden, BOOK), c)
    buf = io.BytesIO()
    write_chart(buf, c)
    buf.seek(0)
    write_deck(os.path.join(golden, DECK), c, buf)
    with open(figures_path, "w") as fh:
        json.dump(fig, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return c


if __name__ == "__main__":
    task = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(task, "target"), os.path.join(task, "golden"), os.path.join(task, "generator", "figures.json"))
