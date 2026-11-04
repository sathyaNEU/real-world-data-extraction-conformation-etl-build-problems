"""The two golden deliverables: the detection monitoring evaluation workbook and the October results chart."""
import datetime as dt
import math
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import postprocess as PP
import world as W

EV = [e["label"] for e in W.EVENTS]
NAMES = {"chloride": "Chloride", "sodium": "Sodium, dissolved", "boron": "Boron, dissolved"}
UNIT = {"chloride": "mg/L", "sodium": "mg/L", "boron": "ug/L"}


def s3(x):
    d = 3 - int(math.floor(math.log10(abs(x)))) - 1
    v = round(x, d)
    return float(("%%.%df" % max(d, 0)) % v)


def nfmt(x):
    d = max(0, 3 - int(math.floor(math.log10(abs(x)))) - 1)
    return "0" + ("." + "0" * d if d else "")


def workbook(path, g):
    wb = Workbook()
    ws = wb.active
    ws.title = "Evaluation"
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DDE3EA")
    thin = Side(style="thin", color="9AA3AD")
    box = Border(top=thin, bottom=thin, left=thin, right=thin)
    ws["A1"] = "Marten Creek Landfill, detection monitoring evaluation, October 2026 event"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Statistical Analysis Plan rev. 2, sections 4 to 6. Routine samples 6 to 8 October 2026."
    ws["A4"] = "Wells to resample within 60 days"
    ws["A4"].font = bold
    for i, w in enumerate(g["resample"]):
        params = [NAMES[k] for k in W.INDICATORS if g["exceed"][(w, k)]]
        ws.cell(row=5 + i, column=1, value=w)
        ws.cell(row=5 + i, column=2, value=", ".join(params))
    r0 = 6 + len(g["resample"])
    ws.cell(row=r0 + 1, column=1, value="Upper prediction limits").font = bold
    hdr = ["Indicator", "Units", "Background results", "UPL"]
    for j, h in enumerate(hdr):
        c = ws.cell(row=r0 + 2, column=1 + j, value=h)
        c.font = bold
        c.fill = head_fill
        c.border = box
    for i, k in enumerate(W.INDICATORS):
        row = [NAMES[k], UNIT[k], g["golden_n"][k], s3(g["golden"][k])]
        for j, v in enumerate(row):
            c = ws.cell(row=r0 + 3 + i, column=1 + j, value=v)
            c.border = box
        ws.cell(row=r0 + 3 + i, column=4).number_format = nfmt(g["golden"][k])
    r1 = r0 + 7
    ws.cell(row=r1, column=1, value="October 2026 results at the compliance wells").font = bold
    hdr = ["Well"] + ["%s (%s)" % (NAMES[k], UNIT[k]) for k in W.INDICATORS] + ["Over a limit"]
    for j, h in enumerate(hdr):
        c = ws.cell(row=r1 + 1, column=1 + j, value=h)
        c.font = bold
        c.fill = head_fill
        c.border = box
        c.alignment = Alignment(wrap_text=True, vertical="top")
    over_fill = PatternFill("solid", fgColor="FBE3D6")
    for i, w in enumerate(W.COMPLIANCE):
        ws.cell(row=r1 + 2 + i, column=1, value=w).border = box
        for j, k in enumerate(W.INDICATORS):
            v = g["october"][(w, k)]
            c = ws.cell(row=r1 + 2 + i, column=2 + j, value=s3(v))
            c.number_format = nfmt(v)
            c.border = box
            if g["exceed"][(w, k)]:
                c.fill = over_fill
                c.font = bold
        ex = [NAMES[k].split(",")[0].lower() for k in W.INDICATORS if g["exceed"][(w, k)]]
        ws.cell(row=r1 + 2 + i, column=5, value=", ".join(ex) if ex else "none").border = box
    r2 = r1 + 3 + len(W.COMPLIANCE)
    notes = ["Notes",
             "Background (SAP section 4): routine results at MW-1, MW-2 and MW-3, April 2018 to April 2026. Results from "
             "events when the well's head stood below its boundary piezometer's (PZ-1, PZ-2) drew water from beneath the "
             "waste and are not background; see sheet Background.",
             "Heads: depth to water from mcl_gauging_rounds_2018-2026.csv on the casing elevation in force on the gauging "
             "date (mcl_monitoring_points.xlsx, Survey).",
             "Results: reportable primary samples from both laboratories; boron in ug/L. MW-5R stands in MW-5's place. "
             "MW-3's April 2023 boron was not analysed.",
             "Limits are compared unrounded and shown to three significant figures. Prepared 4 November 2026."]
    for i, t in enumerate(notes):
        c = ws.cell(row=r2 + i, column=1, value=t)
        if i == 0:
            c.font = bold
    for col, wdt in zip("ABCDE", (34, 20, 20, 20, 22)):
        ws.column_dimensions[col].width = wdt

    wb2 = wb.create_sheet("Background")
    hdr = ["Event", "Well", "Boundary point", "Head difference (ft)", "Used", "Chloride (mg/L)",
           "Sodium, dissolved (mg/L)", "Boron, dissolved (ug/L)"]
    for j, h in enumerate(hdr):
        c = wb2.cell(row=1, column=1 + j, value=h)
        c.font = bold
        c.fill = head_fill
    rr = 2
    for ei in W.BG_EVENTS:
        for w in W.BACKGROUND:
            if not any((w, ei, k) in g["bg"] for k in W.INDICATORS):
                continue
            used = not g["rev"][(w, ei)]
            row = [EV[ei], w, W.BOUNDARY[w], g["head_diff"][(w, ei)], "yes" if used else "no, gradient reversed"]
            for k in W.INDICATORS:
                v = g["bg"].get((w, ei, k))
                row.append(None if v is None else s3(v))
            for j, v in enumerate(row):
                wb2.cell(row=rr, column=1 + j, value=v)
            wb2.cell(row=rr, column=4).number_format = "0.00"
            rr += 1
    for j, wdt in enumerate((10, 7, 14, 19, 22, 15, 22, 21)):
        wb2.column_dimensions[get_column_letter(1 + j)].width = wdt
    wb2.freeze_panes = "A2"

    wb3 = wb.create_sheet("Field")
    hdr = ["Well", "Meter", "Conductance as logged (uS/cm)", "Temperature (C)", "Specific conductance at 25 C (uS/cm)",
           "Counter at purge start (L)", "Counter at sample (L)", "Purge volume (gal)"]
    for j, h in enumerate(hdr):
        c = wb3.cell(row=1, column=1 + j, value=h)
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    order = [w for d in W.SAMPLING_ORDER for w in d]
    for i, w in enumerate(order):
        d = g["field_detail"][w]
        row = [w, d["meter"], d["recorded"], d["temp"], int(round(g["spc"][w])), round(d["start_l"], 2),
               round(d["end_l"], 2), round(g["purge"][w], 1)]
        for j, v in enumerate(row):
            wb3.cell(row=2 + i, column=1 + j, value=v)
        wb3.cell(row=2 + i, column=8).number_format = "0.0"
    for j, wdt in enumerate((8, 9, 16, 13, 20, 15, 14, 12)):
        wb3.column_dimensions[get_column_letter(1 + j)].width = wdt
    wb3.cell(row=3 + len(order), column=1,
             value="R-4471 logged conductivity uncorrected; specific conductance corrected to 25 C at 1.91 per cent per "
                   "degree (FS-03 section 4).")
    wb.save(path)
    PP.normalize_ooxml(path, W.PEOPLE["hydrogeologist"], W.PEOPLE["hydrogeologist"], "2026-11-03T15:20:00Z",
                       "2026-11-04T17:05:00Z", title="Detection monitoring evaluation, October 2026", excel=True,
                       company="Fieldstone Hydrogeology, LLC")


def chart(path, g):
    import matplotlib
    matplotlib.use("svg")
    matplotlib.rcParams["svg.hashsalt"] = "task193"
    matplotlib.rcParams["svg.fonttype"] = "none"
    import matplotlib.pyplot as plt
    blue, orange, ink, muted, grid = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 3.9))
    wells = W.COMPLIANCE
    listed = set(g["resample"])
    for ax, k in zip(axes, W.INDICATORS):
        lim = g["golden"][k]
        xs = list(range(len(wells)))
        for x, w in zip(xs, wells):
            v = g["october"][(w, k)]
            over = g["exceed"][(w, k)]
            if over:
                ax.plot([x], [v], marker="D", markersize=8, color=orange, markeredgecolor="white", markeredgewidth=1.0,
                        linestyle="none", zorder=3)
            elif w in listed:
                ax.plot([x], [v], marker="o", markersize=7, markerfacecolor="white", markeredgecolor=orange,
                        markeredgewidth=1.6, linestyle="none", zorder=3)
            else:
                ax.plot([x], [v], marker="o", markersize=7, color=blue, markeredgecolor="white", markeredgewidth=1.0,
                        linestyle="none", zorder=3)
        ax.axhline(lim, color=ink, linewidth=1.2, linestyle=(0, (5, 3)), zorder=2)
        ax.text(len(wells) - 0.55, lim * 1.025, "UPL %s %s" % ("%g" % s3(lim), UNIT[k]), va="bottom", ha="right", fontsize=8.5,
                color=ink)
        top = max(g["october"][(w, k)] for w in wells)
        ax.set_ylim(0, top * 1.12)
        ax.set_xticks(xs)
        ax.set_xticklabels(wells, rotation=45, ha="right", fontsize=8.5, color=muted)
        for lbl, w in zip(ax.get_xticklabels(), wells):
            if w in listed:
                lbl.set_fontweight("bold")
                lbl.set_color(ink)
        ax.tick_params(axis="y", labelsize=8.5, colors=muted)
        ax.set_title("%s (%s)" % (NAMES[k], UNIT[k]), fontsize=10, color=ink, loc="left")
        ax.grid(axis="y", color=grid, linewidth=0.8)
        ax.set_axisbelow(True)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color("#b9b8b2")
    from matplotlib.lines import Line2D
    handles = [Line2D([0], [0], marker="D", color=orange, linestyle="none", markersize=8, label="over its limit"),
               Line2D([0], [0], marker="o", markerfacecolor="white", markeredgecolor=orange, markeredgewidth=1.6,
                      linestyle="none", markersize=7, label="under, well resampled on another indicator"),
               Line2D([0], [0], marker="o", color=blue, linestyle="none", markersize=7, label="under every limit"),
               Line2D([0], [0], color=ink, linestyle=(0, (5, 3)), linewidth=1.2, label="upper prediction limit")]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8.5, bbox_to_anchor=(0.5, 0.0))
    fig.suptitle("%s go to verification resampling after the October 2026 event (wells to resample in bold)"
                 % (", ".join(g["resample"][:-1]) + " and " + g["resample"][-1]),
                 x=0.01, ha="left", fontsize=11.5, color=ink, y=0.985)
    fig.tight_layout(rect=(0, 0.07, 1, 0.94))
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    svg = open(path, encoding="utf-8").read().replace('id="matplotlib.axis_', 'id="axis_')
    assert "matplotlib" not in svg.lower()
    open(path, "w", encoding="utf-8").write(svg)


def write(g, gold):
    workbook(os.path.join(gold, "detection_eval_2026-10.xlsx"), g)
    chart(os.path.join(gold, "october_results_vs_limits.svg"), g)
