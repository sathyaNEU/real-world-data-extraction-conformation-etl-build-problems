"""The golden deliverables: the notification under Schedule 2 (docx), the quarter's network workbook (xlsx) and the
ten-minute traces through every detection (svg), every figure taken from the golden computed on target/."""
import datetime as dt
import io
import os
import re

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Mm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import postprocess as PP
import world as W

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"
LINE, MARK = "#2a78d6", "#c2410c"
NAMES = {c: n for c, n, *_ in W.STATIONS}


def local(t):
    return W.Q_START + dt.timedelta(minutes=10 * int(t)) + W.BST


def episodes(g, code):
    """(date, start t, end t, peak) per detection day, in date order."""
    out = []
    v = g["vals"][code]
    for s, e, f in g["call"][code]["episodes"]:
        out.append(((W.Q_START + dt.timedelta(minutes=10 * s)).date(), s, e, int(round(np.nanmax(v[s:e])))))
    days = {}
    for d, s, e, p in out:
        if d in days:
            d0, s0, e0, p0 = days[d]
            days[d] = (d, s0, max(e0, e), max(p0, p))
        else:
            days[d] = (d, s, e, p)
    return [days[d] for d in sorted(days)]


def write_docx(g, path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Mm(297), Mm(210)
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)

    def para(text, bold=False, size=None, space=6, color=None, align=None):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if color:
            r.font.color.rgb = RGBColor.from_string(color)
        p.paragraph_format.space_after = Pt(space)
        if align:
            p.alignment = align
        return p

    para(W.LAB, bold=True, size=12.5, space=0, color="1F3A5F")
    para("%s  |  Department of Physics, %s" % (W.NETWORK, W.UNIVERSITY), size=8.5, space=14,
         color="52514E")
    para("To: %s, Clerk to the %s" % (W.PEOPLE["clerk"], W.COMMITTEE), space=2)
    para("From: %s, Duty Radiation Scientist" % W.PEOPLE["duty"], space=2)
    para("Date: 9 October 2026", space=2)
    para("Our reference: MVGN-NOT-2026-03", space=12)
    para("Notification under Schedule 2, paragraph 2.2: increases of artificial origin, 1 July to 30 September 2026",
         bold=True, size=11, space=10)
    codes = g["call_codes"]
    n_days = sum(len(g["call"][c]["dates"]) for c in codes)
    para("Two stations of the network recorded increases in the ambient dose equivalent rate of artificial origin in "
         "the quarter: %s (%s) and %s (%s), on %d days in all. No other station recorded an increase of artificial "
         "origin; every other increase in the quarter's record was natural." % (
             NAMES[codes[1]], codes[1], NAMES[codes[0]], codes[0], n_days), space=8)
    tbl = doc.add_table(rows=1, cols=3)
    tbl.style = "Table Grid"
    for i, h in enumerate(["Station", "Date of increase", "Highest ten-minute value that day (nSv/h)"]):
        c = tbl.rows[0].cells[i]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        c.paragraphs[0].runs[0].font.size = Pt(8.5)
    for code in (codes[1], codes[0]):
        for d, s, e, p in episodes(g, code):
            row = tbl.add_row().cells
            vals = ["%s, %s" % (code, NAMES[code]), d.strftime("%d/%m/%Y"), "%d" % p]
            for i, v in enumerate(vals):
                row[i].text = v
                row[i].paragraphs[0].runs[0].font.size = Pt(8.5)
                if i == 2:
                    row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    para("", space=2)
    para("Highest ten-minute value during each station's increases: %s %d nSv/h (%s); %s %d nSv/h (%s)." % (
        codes[1], g["call"][codes[1]]["peak"], g["peak_day"][codes[1]].strftime("%d/%m/%Y"),
        codes[0], g["call"][codes[0]]["peak"], g["peak_day"][codes[0]].strftime("%d/%m/%Y")), bold=True, space=10)
    para("How the origin was established. Rain brings radon decay products down onto the ground around a probe, and "
         "the excess it adds can only go away as lead-214 and bismuth-214 decay: from one ten-minute value to the "
         "next it falls by about a quarter at most, and through the quarter no natural increase at any station fell "
         "by more than %d per cent in a step. Each increase listed above ended within a single ten-minute interval, "
         "the excess falling by %d per cent or more in one step and staying down, which radon decay products "
         "cannot do. They came at %s in July and August and at %s from late August to mid-September, in the evenings "
         "and the small hours, wet and dry alike: on %d of the %d days the nearest rain gauge recorded rain within an hour of the increase." % (
             g["nat_max_fall"], g["art_min_fall"], NAMES[codes[1]], NAMES[codes[0]],
             g["routes"]["wet_days"], n_days), space=8)
    para("The source has not been identified. The shape of the increases is that of a gamma source switched on and "
         "off near the probe; we have asked both councils' environmental health teams whether any work with gamma "
         "sources was permitted near the two sites in the quarter, and will report what we learn in the quarterly "
         "report.", space=12)
    para(W.PEOPLE["duty"], bold=True, space=0)
    para("Duty Radiation Scientist, %s" % W.LAB, size=9, space=0, color="52514E")
    para("cc %s, Network Manager" % W.PEOPLE["manager"], size=8.5, space=0, color="52514E")
    buf = io.BytesIO()
    doc.save(buf)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_ooxml(path, W.PEOPLE["duty"], W.PEOPLE["duty"], "2026-10-08T14:12:00Z", "2026-10-09T08:31:00Z",
                       title="Notification, increases of artificial origin, Q3 2026", excel=False,
                       company=W.UNIVERSITY)


def write_xlsx(g, path):
    wb = Workbook()
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="E8EEF5")

    def sheet(ws, header, rows, widths, fmts=None):
        ws.append(header)
        for c in ws[1]:
            c.font = bold
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in rows:
            ws.append(list(r))
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w
        ws.freeze_panes = "A2"
        for col, f in (fmts or {}).items():
            for row in ws.iter_rows(min_row=2, min_col=col + 1, max_col=col + 1):
                for c in row:
                    c.number_format = f

    ws = wb.active
    ws.title = "Detections"
    rows = []
    for code in (g["call_codes"][1], g["call_codes"][0]):
        for d, s, e, p in episodes(g, code):
            rows.append((code, NAMES[code], d.strftime("%d/%m/%Y"), p))
    sheet(ws, ["Station", "Site", "Date", "Highest ten-minute value that day (nSv/h)"], rows, [9, 18, 11, 18])
    ws = wb.create_sheet("Source checks")
    rows = []
    for code in sorted(g["checks"]):
        c = g["checks"][code]
        rows.append((code, NAMES[code], c["date"].strftime("%d/%m/%Y"), c["kit"], c["source"], c["cert"], c["jig"],
                     round(c["net"]), round(c["expected"]), round(c["pct"], 1), "Pass" if c["passed"] else "Fail"))
    sheet(ws, ["Station", "Site", "Date", "Kit", "Source", "Certificate", "Jig", "Check reading (nSv/h)",
               "Expected (nSv/h)", "Per cent of expected", "Result"], rows, [9, 18, 11, 7, 9, 16, 5, 12, 12, 11, 8],
          {9: "0.0"})
    ws = wb.create_sheet("Telemetry")
    rows = []
    for code in sorted(g["timely"]):
        t = g["timely"][code]
        rows.append((code, NAMES[code], W.N10, t["timely"], round(t["pct"], 1)))
    sheet(ws, ["Station", "Site", "Intervals in the quarter", "Values received within 60 minutes",
               "Per cent received within 60 minutes"], rows, [9, 18, 12, 14, 14], {4: "0.0"})
    ws = wb.create_sheet("Air filters")
    rows = []
    for fid in sorted(g["air"]):
        a = g["air"][fid]
        rows.append((a["sampler"], fid, (a["on"] + W.BST).strftime("%d/%m/%Y %H:%M"),
                     (a["off"] + W.BST).strftime("%d/%m/%Y %H:%M"), round(a["volume"], 1), round(a["activity"], 3),
                     round(a["conc"], 2)))
    sheet(ws, ["Sampler", "Filter", "On (BST)", "Off (BST)", "Air drawn (m3)", "Gross beta (Bq)",
               "Gross beta (mBq/m3)"], rows, [8, 12, 16, 16, 11, 11, 12], {4: "0.0", 5: "0.000", 6: "0.00"})
    buf = io.BytesIO()
    wb.save(buf)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_ooxml(path, W.PEOPLE["duty"], W.PEOPLE["duty"], "2026-10-07T09:44:00Z", "2026-10-09T08:26:00Z",
                       title="Network quarter, Q3 2026", excel=True, company=W.UNIVERSITY)


def write_svg(g, path):
    plt.rcParams["svg.hashsalt"] = "task211-golden"
    plt.rcParams["font.family"] = "DejaVu Sans"
    panels = []
    for code in (g["call_codes"][1], g["call_codes"][0]):
        for d, s, e, p in episodes(g, code):
            panels.append((code, d, s, e, p))
    ncol = 4
    nrow = int(np.ceil(len(panels) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(12.4, 2.55 * nrow + 1.2), dpi=100, sharey=True)
    fig.patch.set_facecolor(SURF)
    axes = axes.ravel()
    for ax, (code, d, s, e, p) in zip(axes, panels):
        a, b = s - 12, e + 12
        v = g["vals"][code][a:b]
        x = np.arange(a, b)
        hrs = [(local(t) - local(s)).total_seconds() / 3600.0 for t in x]
        ax.set_facecolor(SURF)
        ax.plot(hrs, v, color=LINE, lw=1.4, drawstyle="steps-post")
        fi = e - a
        ax.plot([hrs[fi - 1]], [v[fi - 1]], marker="o", ms=4, color=MARK)
        ax.plot([hrs[fi]], [v[fi]], marker="o", ms=4, color=MARK)
        ax.set_title("%s  %s  peak %d" % (code, d.strftime("%d %b"), p), fontsize=8.5, color=INK, loc="left")
        ax.grid(axis="y", color=GRID, lw=0.6)
        for sp in ("top", "right"):
            ax.spines[sp].set_visible(False)
        for sp in ("left", "bottom"):
            ax.spines[sp].set_color(GRID)
        ax.tick_params(labelsize=7.5, colors=INK2, length=2)
        ax.set_xlabel("hours from %s BST" % local(s).strftime("%H:%M"), fontsize=7.5, color=MUTED)
    for ax in axes[len(panels):]:
        ax.set_visible(False)
    for r in range(nrow):
        axes[r * ncol].set_ylabel("nSv/h", fontsize=8, color=INK2)
    fig.suptitle("Every increase of artificial origin ends within one ten-minute step: the excess falls by %d per "
                 "cent or more at once,\nwhere rain-washed radon decay products never fell by more than %d per cent "
                 "in a step" % (g["art_min_fall"], g["nat_max_fall"]), x=0.012, ha="left", fontsize=10.5,
                 color=INK, y=0.995, linespacing=1.35)
    fig.text(0.012, 0.012, "Ten-minute ambient dose equivalent rate, %s and %s, Q3 2026; the two marked values are "
             "either side of the step in which each increase ended. Source: %s platform export, 09/10/2026."
             % (g["call_codes"][1], g["call_codes"][0], W.NETWORK_SHORT), fontsize=7.5, color=MUTED)
    fig.subplots_adjust(left=0.055, right=0.99, top=0.86, bottom=0.11, hspace=0.75, wspace=0.12)
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None, "Contributor": None}, facecolor=SURF)
    plt.close(fig)
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r"<!-- Created with matplotlib.*?-->\n?", "", svg)
    svg = re.sub(r"<metadata>.*?</metadata>\s*", "", svg, flags=re.S)
    svg = re.sub(r'id="matplotlib\.axis_(\d+)"', r'id="axis_\1"', svg)
    open(path, "w", encoding="utf-8").write(svg)


def write(g, gold):
    write_docx(g, os.path.join(gold, "artificial_detections_2026Q3.docx"))
    write_xlsx(g, os.path.join(gold, "network_quarter_2026Q3.xlsx"))
    write_svg(g, os.path.join(gold, "excursion_traces_2026Q3.svg"))
