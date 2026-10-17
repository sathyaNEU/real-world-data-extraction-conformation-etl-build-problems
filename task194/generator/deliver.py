"""The two deliverables: the placement workbook and the committee brief with its chart."""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

import world as W

BAR = "#1F5C9E"
BAR_OTHER = "#B4C4D6"
INK = "#333333"
GRID = "#E3E3E3"


def chart(path, g):
    """One bar for each eligible unit of the complications a placement there would avoid."""
    rows = sorted(g["units"], key=lambda d: d["avoided"])
    labels = ["%s %s" % (short(d["hospital"]), d["name"]) for d in rows]
    values = [round(d["avoided"]) for d in rows]
    pick = g["answer"]["unit"]
    colours = [BAR if d["unit"] == pick else BAR_OTHER for d in rows]
    fig, ax = plt.subplots(figsize=(6.9, 3.9), dpi=200)
    bars = ax.barh(labels, values, height=0.62, color=colours, linewidth=0)
    ax.set_xlabel("Complications avoided over the quarter from 1 April 2027", fontsize=8.5, color=INK)
    ax.xaxis.grid(True, color=GRID, linewidth=0.7)
    ax.set_axisbelow(True)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(axis="y", length=0, labelsize=8, colors=INK)
    ax.tick_params(axis="x", length=0, labelsize=8, colors=INK)
    ax.set_xlim(0, max(values) * 1.30)
    ax.set_xticks(range(0, max(values) + 6, 5))
    for d, bar in zip(rows, bars):
        if d["unit"] in (pick, g["runner"]["unit"]):
            ax.annotate("%d" % round(d["avoided"]), (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                        xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5,
                        color=BAR if d["unit"] == pick else INK,
                        fontweight="bold" if d["unit"] == pick else "normal")
    ax.annotate("recommended", (bars[-1].get_width(), bars[-1].get_y() + bars[-1].get_height() / 2),
                xytext=(22, 0), textcoords="offset points", va="center", fontsize=7.6, color=BAR)
    fig.tight_layout(pad=0.6, rect=(0, 0, 1, 0.918))
    # the finding runs across the figure, not the axes, so a long title is never clipped
    fig.text(0.011, 0.985, "Alderbrook Orthopaedics avoids %d complications, %d more than the closest unit"
             % (round(g["answer"]["avoided"]), g["gap"]), ha="left", va="top", fontsize=9.8, color=INK)
    fig.savefig(path, facecolor="white", metadata={"Software": None, "Creation Time": None})
    plt.close(fig)
    return path


def short(code):
    return {"H1": "Alderbrook", "H2": "Stonecreek", "H3": "Marrowfield", "H4": "Carrowdean"}[code]


HEAD = Font(bold=True, size=10)
TITLE = Font(bold=True, size=12)
NOTE = Font(italic=True, size=9)
FILL = PatternFill("solid", fgColor="E8E8E4")
THIN = Side(style="thin", color="BFBFBF")


def _sheet(ws, title, subtitle, header, rows, widths, formats):
    ws.append([title])
    ws.append([subtitle])
    ws.append([])
    ws.append(header)
    for r in rows:
        ws.append(r)
    ws["A1"].font = TITLE
    ws["A2"].font = NOTE
    for c in range(1, len(header) + 1):
        cell = ws.cell(row=4, column=c)
        cell.font = HEAD
        cell.fill = FILL
        cell.alignment = Alignment(wrap_text=True, vertical="bottom")
        cell.border = Border(bottom=THIN)
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for col, fmt in formats.items():
        for row in ws.iter_rows(min_row=5, min_col=col, max_col=col):
            row[0].number_format = fmt
    ws.freeze_panes = "A5"


def workbook(path, g):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Placement"
    a, r = g["answer"], g["runner"]
    rows = []
    for d in sorted(g["units"], key=lambda x: -x["avoided"]):
        rows.append([d["unit"], "%s %s" % (short(d["hospital"]), d["name"]), d["plan"],
                     round(d["expected_plan"], 1), round(d["ratio"], 2), round(d["avoided"])])
    _sheet(ws, "Cycle IP-10 placement: complications a placement would avoid, by unit",
           "Quarter from 1 April 2027. Eligible units under charter clause 4.2. Prepared by Clinical "
           "Improvement, 18 March 2027.",
           ["Cost centre", "Unit", "Planned separations", "Expected complications",
            "Standardised ratio, specification period", "Complications avoided"],
           rows, [12, 30, 13, 13, 15, 13],
           {3: "#,##0", 4: "0.0", 5: "0.00", 6: "#,##0"})
    n = len(rows)
    ws.append([])
    ws.append(["Recommendation", "%s %s (%s)" % (short(a["hospital"]), a["name"], a["unit"])])
    ws.append(["Complications avoided", round(a["avoided"])])
    ws.append(["Closest unit", "%s %s (%s)" % (short(r["hospital"]), r["name"], r["unit"])])
    ws.append(["Complications avoided there", round(r["avoided"])])
    ws.append(["Gap", g["gap"]])
    for i in range(n + 6, n + 11):
        ws.cell(row=i, column=1).font = HEAD
    ws.print_area = "A1:F%d" % (n + 10)

    hs = wb.create_sheet("Hospital year")
    _sheet(hs, "Adjusted complication rate by hospital, year ended 31 December 2026",
           "In-scope episodes under specification 4.0, counted at the site each unit reported under in the "
           "month of separation.",
           ["Hospital", "In-scope episodes", "Complications", "Adjusted rate per 1,000 episodes"],
           [[h["name"], h["episodes"], h["complications"], round(h["rate"], 1)] for h in g["hospitals"]],
           [24, 14, 13, 16], {2: "#,##0", 3: "#,##0", 4: "0.0"})

    os_ = wb.create_sheet("Outside the indicator")
    _sheet(os_, "Sub-acute and mental health activity, outside the complication indicator",
           "Distinct separations as the activity summary reports them, all care types.",
           ["Quarter", "Separations", "Episodes with a complication"],
           [[o["quarter"], o["separations"], o["with_complication"]] for o in g["outside"]],
           [14, 13, 18], {2: "#,##0", 3: "#,##0"})

    gs = wb.create_sheet("Complication groups")
    _sheet(gs, "In-scope episodes recording a complication, by reporting group",
           "Codes read against the national list revision in force at separation, Appendix B of "
           "specification 4.0.",
           ["Group", "Reporting group", "2025-26", "2026-27 to 31 December 2026"],
           [[x["group"], x["name"], x["fy2025"], x["fy2026"]] for x in g["groups"]],
           [9, 44, 12, 16], {3: "#,##0", 4: "#,##0"})

    notes = wb.create_sheet("Notes")
    for line in [["Item", "Note"],
                 ["Eligible units", "Charter clause 4.2: acute inpatient units with four or more closed "
                  "quarters on specification 4.0 and no placement in the previous twelve closed quarters. "
                  "Twelve units qualify for cycle IP-10."],
                 ["Expected complications", "Specification 3.4: planned separations times the unit's "
                  "expected complications per separation over the specification period to date."],
                 ["Standardised ratio", "Specification 3.2 and 3.3, over every closed quarter from "
                  "1 July 2024."],
                 ["Complications avoided", "Charter clause 4.3, over the assessment quarter."],
                 ["Cost centre 41510", "Reported under its own code since the Carrowdean medical wards were "
                  "amalgamated on 1 October 2025: five closed quarters."],
                 ["Data", "Episode extract and complication detail to 31 December 2026, exported "
                  "5 March 2027. Coding for the December quarter closed on 28 February 2027."]]:
        notes.append(line)
    notes.column_dimensions["A"].width = 26
    notes.column_dimensions["B"].width = 96
    notes["A1"].font = HEAD
    notes["B1"].font = HEAD
    for row in notes.iter_rows(min_row=2, min_col=2, max_col=2):
        row[0].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    return path


SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["BodyText"], fontName="Helvetica", fontSize=9.4, leading=13,
                      alignment=TA_JUSTIFY, spaceAfter=6, textColor=colors.HexColor("#222222"))
LEAD = ParagraphStyle("lead", parent=BODY, fontSize=10.2, leading=14.5)
TITLE_P = ParagraphStyle("t", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=17,
                         spaceAfter=4, textColor=colors.HexColor("#1F3C5A"))
KICKER = ParagraphStyle("k", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#5A5A5A"),
                        spaceAfter=10)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10, spaceBefore=9,
                    spaceAfter=3, textColor=colors.HexColor("#1F3C5A"))
FOOT = ParagraphStyle("f", parent=BODY, fontSize=7.6, leading=9.6, textColor=colors.HexColor("#5A5A5A"))
CELL = ParagraphStyle("c", fontName="Helvetica", fontSize=8.4, leading=11)
CELLB = ParagraphStyle("cb", fontName="Helvetica-Bold", fontSize=8.4, leading=11)
TBL = TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8899AA")),
                  ("LINEBELOW", (0, 1), (-1, -2), 0.25, colors.HexColor("#DDDDDD")),
                  ("VALIGN", (0, 0), (-1, -1), "TOP"),
                  ("ALIGN", (2, 1), (-1, -1), "RIGHT"),
                  ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4),
                  ("LEFTPADDING", (0, 0), (-1, -1), 2)])


def _page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.4)
    canvas.setFillColor(colors.HexColor("#6A6A6A"))
    canvas.drawString(20 * mm, 12 * mm, "Clinical Improvement Partnership, cycle IP-10")
    canvas.drawRightString(190 * mm, 12 * mm, "Page %d" % doc.page)
    canvas.restoreState()


def brief(path, g, chart_path):
    a, r = g["answer"], g["runner"]
    rung0, rung1, rung2 = g["rung0"], g["rung1"], g["rung2"]
    d = SimpleDocTemplate(path, pagesize=A4, title="Cycle IP-10 placement recommendation", author="",
                          subject="", creator="", leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=16 * mm, bottomMargin=20 * mm)
    tbl = [["Unit", "Cost centre", "Planned separations", "Expected complications",
            "Complications avoided"]]
    for x in sorted(g["units"], key=lambda u: -u["avoided"])[:5]:
        tbl.append(["%s %s" % (short(x["hospital"]), x["name"]), x["unit"], "{:,}".format(x["plan"]),
                    "{:.1f}".format(x["expected_plan"]), "%d" % round(x["avoided"])])
    flow = [
        Paragraph("Place the IP-10 team with Alderbrook Orthopaedics: %d complications avoided, %d more "
                  "than the closest unit" % (round(a["avoided"]), g["gap"]), TITLE_P),
        Paragraph("Clinical Improvement Partnership, cycle IP-10 (1 April to 30 June 2027). For the "
                  "Clinical Quality Committee, 24 March 2027. Prepared by Clinical Improvement.", KICKER),
        Paragraph("The team should embed with <b>Orthopaedics at Alderbrook Hospital, cost centre %s</b>. "
                  "The unit's planned %s separations for the quarter carry %.0f expected complications, it "
                  "has stood at %.2f times its expected complications across the ten closed quarters of "
                  "specification 4.0, and the %.1f complications that standing puts above expectation are the "
                  "largest avoidable number in the network. On what the partnership's seven closed "
                  "placements have taken off a unit's standing excess, the placement avoids <b>%d "
                  "complications</b> over the quarter, against %d at %s %s, the closest unit."
                  % (a["unit"], "{:,}".format(a["plan"]), a["expected_plan"], a["ratio"],
                     a["excess"], round(a["avoided"]), round(r["avoided"]),
                     short(r["hospital"]), r["name"]), LEAD),
        Spacer(1, 2),
        Image(chart_path, width=165 * mm, height=93.3 * mm),
        Spacer(1, 4),
        Paragraph("Every eligible unit, its planned activity for the quarter and what a placement there "
                  "would take off it, is in the placement workbook.", FOOT),
        Paragraph("The three units the committee asked about", H2),
        Paragraph("<b>%s %s</b> is carrying the most complications above expectation right now, %d of them "
                  "in the December quarter, and that is the placement the quarter in hand points to. Its own "
                  "ten quarters put %.1f above expectation on the quarter's planned activity, so most of what "
                  "it is carrying now is its own quarter-to-quarter movement rather than a position a "
                  "placement can work on: there, a placement avoids %d."
                  % (short(rung0["hospital"]), rung0["name"], round(rung0["last_excess"]),
                     rung0["excess"], round(rung0["avoided"])), BODY),
        Paragraph("<b>%s %s</b> stands worst of the twelve on its own record, but it is a small unit: its "
                  "planned %s separations for the quarter carry %.1f complications above expectation, so a "
                  "placement there avoids %d."
                  % (short(rung1["hospital"]), rung1["name"], "{:,}".format(rung1["plan"]),
                     rung1["excess"], round(rung1["avoided"])), BODY),
        Paragraph("<b>%s %s</b> will record more complications than any other unit next quarter on the "
                  "elective catch-up volume in the plan, and most of them are the complications its case "
                  "mix is expected to produce: %.1f sit above expectation, and a placement there avoids %d."
                  % (short(rung2["hospital"]), rung2["name"], rung2["excess"],
                     round(rung2["avoided"])), BODY),
        PageBreak(),
        Paragraph("How the figures were put together", H2),
        Paragraph(("Observed and expected complications are specification 4.0's, from the episode extract to "
                  "31 December 2026, and tie to the quarterly indicator series. Each unit's expected "
                  "complications for the quarter are clause 3.4's: the separations the activity plan carries "
                  "times the unit's expected complications per separation over the specification period. "
                  "What a placement takes off a unit's standing excess comes from the seven closed "
                  "placements in the register, each measured against what the unit stood at over its own "
                  "closed quarters before the team arrived."), BODY),
        Table([[Paragraph(c, CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(tbl)],
              colWidths=[56 * mm, 20 * mm, 30 * mm, 30 * mm, 28 * mm], style=TBL),
        Spacer(1, 6),
        Paragraph("Cost centre 41510 has reported under its own code since the Carrowdean medical wards "
                  "were amalgamated on 1 October 2025, and its five closed quarters meet clause 4.2. "
                  "Rehabilitation and Aged Care at Marrowfield, where the team is until 31 March, is not "
                  "eligible this cycle. Complications avoided are whole complications over the assessment "
                  "quarter; expected complications and complications above a standing are carried to one "
                  "decimal.", FOOT),
    ]
    d.build(flow, onFirstPage=_page, onLaterPages=_page)
    return path
