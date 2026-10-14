"""The golden deliverables: occupation_coding_warnings_2026.xlsx (the warning list, every group's coding bias in the
release, the coding teams' October and the follow-up's October) and occupation_coding_bias_2026.png."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import docs
import postprocess
import world as W

XLSX = "occupation_coding_warnings_2026.xlsx"
PNG = "occupation_coding_bias_2026.png"
NAVY = "1F3A5F"
WARN = "B03A2E"
THIN = Side(style="thin", color="BFBFBF")


def _head(ws, row, labels, widths=None):
    for i, h in enumerate(labels, start=1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(vertical="center", wrap_text=True)
    if widths:
        for i, w in enumerate(widths):
            ws.column_dimensions[chr(65 + i)].width = w


def _cell(ws, r, c, v, fmt=None, bold=False, color=None):
    x = ws.cell(row=r, column=c, value=v)
    x.font = Font(name="Calibri", size=11, bold=bold, color=color)
    x.border = Border(bottom=THIN)
    if fmt:
        x.number_format = fmt
    return x


def workbook(path, A):
    wb = Workbook()
    ws = wb.active
    ws.title = "Warning list"
    ws["A1"] = "Six occupation groups carry the coding quality warning in the first occupation release (30 March 2027)"
    ws["A1"].font = Font(name="Calibri", bold=True, size=14, color=NAVY)
    ws["A2"] = ("Coding bias as defined in OQ-4: persons the release codes to the group less persons the reference coding "
                "puts there, as a percentage of the latter, over every person in employment enumerated by 31 October 2026 "
                "with an occupation write-in. Position at the coding extract of 13 November 2026.")
    ws["A2"].font = Font(name="Calibri", italic=True, size=10)
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 44
    ws["A4"] = "Groups carrying the coding quality warning: " + ", ".join(A["warned"][:-1]) + " and " + A["warned"][-1]
    ws["A4"].font = Font(name="Calibri", bold=True, size=12, color=WARN)
    _head(ws, 6, ["ISCO-08 sub-major group", "Title", "Coding bias in the release (%)", "Warning"], [14, 64, 18, 10])
    r = 7
    for g in A["warned"]:
        _cell(ws, r, 1, g, bold=True)
        _cell(ws, r, 2, W.SUB[g])
        _cell(ws, r, 3, A["bias_r"][g], "0.0", bold=True, color=WARN)
        _cell(ws, r, 4, "Yes", bold=True, color=WARN)
        r += 1
    ws.freeze_panes = "A7"
    ws2 = wb.create_sheet("All groups")
    _head(ws2, 1, ["ISCO-08 sub-major group", "Title", "Coding bias in the release (%)", "Warning"], [14, 64, 18, 10])
    for i, g in enumerate(W.GROUPS, start=2):
        warned = g in A["warned"]
        _cell(ws2, i, 1, g, bold=warned)
        _cell(ws2, i, 2, W.SUB[g])
        _cell(ws2, i, 3, A["bias_r"][g], "0.0", bold=warned, color=WARN if warned else None)
        _cell(ws2, i, 4, "Yes" if warned else "No", bold=warned, color=WARN if warned else None)
    ws2.freeze_panes = "A2"
    ws2.print_title_rows = "1:1"
    ws2.page_setup.orientation = "portrait"
    ws2.page_setup.fitToWidth = 1
    ws3 = wb.create_sheet("Release population")
    _head(ws3, 1, ["Response route", "Write-ins coded by 13 Nov", "Write-ins still to code", "Write-ins in the release"],
          [36, 22, 22, 22])
    names = {"O": "Online self-response", "P": "Paper self-response", "FS": "Follow-up, household member",
             "FP": "Follow-up, proxy"}
    for i, r_ in enumerate(("O", "P", "FS", "FP"), start=2):
        _cell(ws3, i, 1, names[r_])
        _cell(ws3, i, 2, A["coded"][r_], "#,##0")
        _cell(ws3, i, 3, A["still"][r_], "#,##0")
        _cell(ws3, i, 4, A["coded"][r_] + A["still"][r_], "#,##0")
    _cell(ws3, 6, 1, "All routes", bold=True)
    _cell(ws3, 6, 2, sum(A["coded"].values()), "#,##0", bold=True)
    _cell(ws3, 6, 3, sum(A["still"].values()), "#,##0", bold=True)
    _cell(ws3, 6, 4, sum(A["coded"].values()) + sum(A["still"].values()), "#,##0", bold=True)
    ws3.freeze_panes = "A2"
    ws4 = wb.create_sheet("Coding teams, October")
    _head(ws4, 1, ["Clerical coding team", "Occupation write-ins coded in October", "Hours on occupation coding in October"],
          [24, 22, 22])
    for i, t in enumerate(W.TEAMS, start=2):
        _cell(ws4, i, 1, t)
        _cell(ws4, i, 2, A["teams"][t][0], "#,##0")
        _cell(ws4, i, 3, A["teams"][t][1], "#,##0.00")
    n = len(W.TEAMS) + 2
    _cell(ws4, n, 1, "All five teams", bold=True)
    _cell(ws4, n, 2, sum(A["teams"][t][0] for t in W.TEAMS), "#,##0", bold=True)
    _cell(ws4, n, 3, round(sum(A["teams"][t][1] for t in W.TEAMS), 2), "#,##0.00", bold=True)
    ws4.freeze_panes = "A2"
    ws5 = wb.create_sheet("Follow-up, September")
    _head(ws5, 1, ["Region", "Follow-up calls in September", "Calls that made no contact"], [20, 22, 22])
    for i, (_, name, _) in enumerate(W.REGIONS, start=2):
        _cell(ws5, i, 1, name)
        _cell(ws5, i, 2, A["regions"][name][0], "#,##0")
        _cell(ws5, i, 3, A["regions"][name][1], "#,##0")
    n = len(W.REGIONS) + 2
    _cell(ws5, n, 1, "Aldmere", bold=True)
    _cell(ws5, n, 2, sum(v[0] for v in A["regions"].values()), "#,##0", bold=True)
    _cell(ws5, n, 3, sum(v[1] for v in A["regions"].values()), "#,##0", bold=True)
    ws5.freeze_panes = "A2"
    ws6 = wb.create_sheet("Notes")
    ws6.column_dimensions["A"].width = 112
    notes = [
        "Definitions and conventions",
        "Coding bias, release population and reference coding as in output quality standard OQ-4 (version 2.1): sections "
        "2.1, 3.1 to 3.3. The warning test (beyond plus or minus 2.0 per cent) is applied to the unrounded bias; biases "
        "are stated to one decimal place.",
        "The release population counts every person in employment enumerated by 31 October 2026 with an occupation "
        "write-in: %s write-ins coded by 13 November and %s still to code. Persons in employment with no write-in "
        "are imputed and are outside it." % ("{:,}".format(sum(A["coded"].values())), "{:,}".format(sum(A["still"].values()))),
        "Write-ins coded by 13 November keep their codes; write-ins coded from 16 November take the autocoder's suggestion "
        "at a score of 0.80 or more (processing plan, decision of 12 November 2026).",
        "Reference coding: the coding quality study's adjudicated code; each studied write-in stands for as many coded "
        "write-ins as its selection interval.",
        "Coding teams: a coder's team on each day from the coding staff movements log; hours are OCC timesheet lines whose "
        "shift started in October, team leads' correction lines included.",
        "Follow-up: calls with a call time in September, each call once where a replacement tablet re-sent it; a call that "
        "made no contact is outcome 31 (field manual 5.3).",
        "Prepared by the Methodology Division for the Deputy Registrar General (Census Outputs), 16 November 2026.",
    ]
    for i, t in enumerate(notes, start=1):
        c = ws6.cell(row=i, column=1, value=t)
        c.font = Font(name="Calibri", size=11, bold=(i == 1))
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.properties.creator = "Methodology Division"
    wb.properties.lastModifiedBy = "Methodology Division"
    wb.save(path)
    postprocess.scrub(path, "Methodology Division", "2026-11-16")
    postprocess.finish_office(path, "2026-11-16T09:10:00Z", "2026-11-16T16:45:00Z", docs.COMPANY)


def chart(path, A):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5})
    fig, ax = plt.subplots(figsize=(9.2, 10.5), dpi=150)
    gs = W.GROUPS[::-1]
    vals = [A["bias"][g] for g in gs]
    colors = ["#" + WARN if g in A["warned"] else "#8EA3B9" for g in gs]
    y = np.arange(len(gs))
    ax.barh(y, vals, color=colors, height=0.72, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(["%s  %s" % (g, _short(W.SUB[g])) for g in gs])
    for x_ in (-2.0, 2.0):
        ax.axvline(x_, color="#B03A2E", linestyle="--", linewidth=1.1, zorder=4)
    ax.text(2.05, len(gs) - 0.4, "warning line +2.0", color="#B03A2E", fontsize=8, va="bottom")
    ax.text(-2.05, len(gs) - 0.4, "warning line -2.0", color="#B03A2E", fontsize=8, va="bottom", ha="right")
    for yy, g, v in zip(y, gs, vals):
        if g in A["warned"]:
            ax.text(v + (0.12 if v > 0 else -0.12), yy, "%+.1f" % A["bias_r"][g], va="center",
                    ha="left" if v > 0 else "right", fontsize=8, color="#B03A2E", fontweight="bold")
    lim = max(abs(min(vals)), abs(max(vals))) + 1.2
    ax.set_xlim(-max(4.5, lim), lim)
    ax.axvline(0, color="#444444", linewidth=0.8, zorder=4)
    ax.grid(axis="x", color="#E5E5E5", zorder=0)
    ax.set_xlabel("Coding bias in the release (per cent of the reference count)")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout(rect=(0, 0, 1, 0.945))
    fig.text(0.015, 0.988, "Six occupation groups carry the coding quality warning in the first occupation release",
             fontsize=11.5, fontweight="bold", va="top")
    fig.text(0.015, 0.968, "Coding bias in the 2026 Census first occupation release (30 March 2027), by ISCO-08 sub-major "
                           "group, at the coding extract\nof 13 November 2026; a group beyond plus or minus 2.0 per cent "
                           "carries the warning (OQ-4).", fontsize=8.5, va="top", color="#333333", linespacing=1.4)
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def _short(t, n=46):
    return t if len(t) <= n else t[: n - 3].rsplit(" ", 1)[0] + "..."


def write(golden_dir, A):
    os.makedirs(golden_dir, exist_ok=True)
    workbook(os.path.join(golden_dir, XLSX), A)
    chart(os.path.join(golden_dir, PNG), A)
