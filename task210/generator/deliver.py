"""The golden deliverables: the self-report letter (docx), the return's lines (csv) and the monthly hours of
discharge (svg), every figure taken from the golden computed on target/."""
import csv
import io
import os
import re
import zipfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor, Mm

import postprocess as PP
import world as W

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab",
       "#184f95", "#104281", "#0d366b"]
INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#fcfcfb"


def r0(x):
    return int(round(x))


def lines_table(g):
    out = []
    for code in sorted(g["stations"], key=lambda c: g["cons"][c]["permit"]):
        L = g["lines"][code]
        out.append(dict(permit_ref=g["cons"][code]["permit"], overflow=g["cons"][code]["discharge"], station_code=code,
                        pass_forward_permitted_ls=r0(g["pff"][code]), pass_forward_delivered_ls=r0(g["delivered"][code]),
                        met_permit="No" if code in g["breach"] else "Yes", spills_12_24=L["spills"],
                        discharge_hours="%.1f" % L["hours"], monitoring_operational_pct="%.1f" % L["operational"]))
    return out


def write_csv(g, path):
    rows = lines_table(g)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()), lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)


def write_svg(g, path):
    plt.rcParams["svg.hashsalt"] = "task210-golden"
    plt.rcParams["font.family"] = "DejaVu Sans"
    order = sorted(g["stations"], key=lambda c: g["stations"][c]["name"])
    data = [[g["lines"][c]["months"][m] for m in range(12)] for c in order]
    vmax = max(max(r) for r in data)
    cmap = LinearSegmentedColormap.from_list("seq", ["#f4f8fd"] + SEQ)
    fig, ax = plt.subplots(figsize=(11.2, 7.4), dpi=100)
    fig.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            frac = (v / vmax) ** 0.55 if vmax else 0
            ax.add_patch(plt.Rectangle((j + 0.03, i + 0.03), 0.94, 0.94, facecolor=cmap(frac) if v > 0 else "#f1f0ec",
                                       edgecolor="none"))
            if v > 0:
                ax.text(j + 0.5, i + 0.52, "%.1f" % v, ha="center", va="center", fontsize=8,
                        color="#ffffff" if frac > 0.58 else INK)
    ax.set_xlim(0, 12)
    ax.set_ylim(len(order), 0)
    ax.set_xticks([j + 0.5 for j in range(12)])
    ax.set_xticklabels(MONTHS, fontsize=9, color=INK2)
    ax.set_yticks([i + 0.5 for i in range(len(order))])
    names = []
    for c in order:
        names.append("%s  (%s)" % (g["stations"][c]["name"], g["cons"][c]["permit"]))
    ax.set_yticklabels(names, fontsize=9, color=INK2)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    totals = {c: sum(g["lines"][c]["months"]) for c in order}
    top = max(order, key=lambda c: totals[c])
    area = sum(totals.values())
    winter = sum(g["lines"][c]["months"][m] for c in order for m in (0, 1, 2, 10, 11))
    fig.suptitle("%s discharged for %.1f hours in 2026, %d per cent of the area's pumping station overflow hours;\n"
                 "%d per cent of all the hours fell in January to March and in November and December"
                 % (g["stations"][top]["name"], totals[top], round(100 * totals[top] / area), round(100 * winter / area)),
                 x=0.015, ha="left", fontsize=10.5, color=INK, y=0.99, linespacing=1.35)
    ax.set_title("Hours of discharge by month (UK local time), every monitor that watched each overflow in 2026",
                 loc="left", fontsize=9, color=INK2, pad=8)
    ax.set_xlabel("Month of 2026", fontsize=9, color=INK2)
    # legend: the scale as a small strip
    cax = fig.add_axes([0.83, 0.075, 0.15, 0.016])
    import numpy as np
    cax.imshow([np.linspace(0, 1, 120)], aspect="auto", cmap=cmap)
    cax.set_yticks([])
    cax.set_xticks([0, 119])
    cax.set_xticklabels(["0 h", "%.0f h" % vmax], fontsize=8, color=MUTED)
    for s in cax.spines.values():
        s.set_visible(False)
    fig.text(0.015, 0.02, "Source: %s event duration monitoring platform and asset register, export 15/01/2027. "
             "Hours rounded to one decimal; a grey cell is a month with no discharge." % W.COMPANY_SHORT,
             fontsize=7.5, color=MUTED)
    fig.subplots_adjust(left=0.30, right=0.985, top=0.855, bottom=0.15)
    fig.savefig(path, format="svg", metadata={"Date": None, "Creator": None, "Contributor": None},
                facecolor=SURF)
    plt.close(fig)
    svg = open(path, encoding="utf-8").read()
    svg = re.sub(r"<!-- Created with matplotlib.*?-->\n?", "", svg)
    svg = re.sub(r"<metadata>.*?</metadata>\s*", "", svg, flags=re.S)
    svg = re.sub(r'id="matplotlib\.axis_(\d+)"', r'id="axis_\1"', svg)
    open(path, "w", encoding="utf-8").write(svg)


def write_docx(g, path):
    k = g["call_code"]
    st = g["stations"][k]
    L = g["lines"][k]
    cons = g["cons"][k]
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Mm(297), Mm(210)
    sec.left_margin = sec.right_margin = Mm(22)
    style = doc.styles["Normal"]
    style.font.name = "Arial"
    style.font.size = Pt(10.5)

    def para(text, bold=False, size=None, align=None, space=6, color=None):
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

    para(W.COMPANY, bold=True, size=13, space=0, color="0B3D5C")
    para("Wastewater Environmental Compliance, Lindmarsh House, Anchor Street, Lincoln", size=9, space=14, color="52514E")
    para("To: %s, Area Environment Management team (Lincolnshire and the Wolds)" % W.REGULATOR, space=2)
    para("From: %s, Wastewater Environmental Compliance Manager" % W.PEOPLE["compliance"], space=2)
    para("Date: 15 January 2027", space=2)
    para("Our reference: WW-ENV-SR-2027-003", space=12)
    para("Self-report: %s, permit %s, condition 2.3.1 (pass forward flow), 2026" % (cons["discharge"], cons["permit"]),
         bold=True, size=11.5, space=10)
    rated = st["rated"][1]
    para("We are reporting that the storm overflow at %s pumping station (site %s, discharging to %s) operated in 2026 "
         "while the station was passing forward less than the %d litres per second that condition 2.3.1 of permit %s "
         "requires before the overflow may discharge. Every one of the overflow's %d spills in 2026, counted by the "
         "12/24 method, began with the station below that flow, and the overflow discharged for %.1f hours in total."
         % (st["name"], "WW-SO-" + k[3:], W.RECEIVING[k], r0(g["pff"][k]), cons["permit"], L["spills"], L["hours"]), space=8)
    para("The station has no flow meter on its rising main. Its pass forward flow was measured from the telemetry "
         "outstation's pump start and stop records: between the duty pump's stop and start levels the wet well holds "
         "a fixed volume, so each pump cycle's filling time gives the inflow and its drawing-down time gives the rate "
         "the running pump moves. Both pumps at %s delivered %d litres per second through 2026, against the %.1f "
         "litres per second rated duty in our asset register and the %d litres per second the permit sets. Either pump "
         "running alone, which is the station's design, passed forward %d per cent of the permitted flow."
         % (st["name"], r0(g["delivered"][k]), rated, r0(g["pff"][k]), r0(100 * g["delivered"][k] / g["pff"][k])),
         space=8)
    t = g["tightest"]
    para("We applied the same measurement to the other thirteen pumping station overflows in the area. Each passed "
         "forward at least its permitted flow, the closest being %s at %d litres per second against %d. The "
         "dry-day discharges at %s in January to March are listed in the return's dry-day annex: the station was "
         "pumping at its full delivered rate throughout them." % (g["stations"][t]["name"], r0(g["delivered"][t]),
                                                                 r0(g["pff"][t]), g["stations"]["SPS0415"]["name"]),
         space=8)
    para("The discharges affected, as the overflow's event duration monitor (serial %s) recorded them, in UK local "
         "time:" % st["edm"], space=4)
    recs = sorted(g["log"][st["edm"]])
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = "Table Grid"
    hdr = ["", "Discharge start", "Discharge end", "Duration (hours)"]
    for i, h in enumerate(hdr):
        cell = tbl.rows[0].cells[i]
        cell.text = h
        cell.paragraphs[0].runs[0].bold = True
        cell.paragraphs[0].runs[0].font.size = Pt(9)
    import golden as G
    for n, (a, b) in enumerate(recs, 1):
        row = tbl.add_row().cells
        vals = [str(n), G.utc_to_local(a).strftime("%d/%m/%Y %H:%M"), G.utc_to_local(b).strftime("%d/%m/%Y %H:%M"),
                "%.2f" % ((b - a) / 3600.0)]
        for i, v in enumerate(vals):
            row[i].text = v
            row[i].paragraphs[0].runs[0].font.size = Pt(9)
            if i == 3:
                row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    para("", space=2)
    para("Durations are from each record's start to its end; the %d records give the %d spills of the return's "
         "12/24 count." % (len(recs), L["spills"]), size=9, space=10, color="52514E")
    para("The cause of the shortfall at %s has not yet been established. Network Operations have raised an "
         "investigation of the pumps and the rising main under the area's operations procedures and will write to you "
         "with its findings and the repair date. The overflow's lines in the 2026 event duration monitoring return are "
         "attached." % st["name"], space=12)
    para("Harriet Kirk", bold=True, space=0)
    para("Wastewater Environmental Compliance Manager, %s" % W.COMPANY, size=9.5, space=0, color="52514E")
    para("cc %s, Network Operations Manager, %s" % (W.PEOPLE["network"], W.AREA), size=9, space=0, color="52514E")
    doc.core_properties.author = W.PEOPLE["compliance"]
    buf = io.BytesIO()
    doc.save(buf)
    open(path, "wb").write(buf.getvalue())
    PP.normalize_ooxml(path, W.PEOPLE["compliance"], W.PEOPLE["compliance"], "2027-01-14T15:20:00Z",
                       "2027-01-15T08:47:00Z", title="Self-report, %s" % cons["discharge"], excel=False,
                       company=W.COMPANY)


def write(g, gold):
    write_docx(g, os.path.join(gold, "overflow_self_report_2026.docx"))
    write_csv(g, os.path.join(gold, "overflow_return_lines_2026.csv"))
    write_svg(g, os.path.join(gold, "spill_hours_by_month_2026.svg"))
