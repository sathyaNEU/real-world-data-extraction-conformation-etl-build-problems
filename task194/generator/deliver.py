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
    rows = sorted(g["units"], key=lambda d: d["avoidable"])
    labels = ["%s %s" % (short(d["hospital"]), d["name"]) for d in rows]
    values = [round(d["avoidable"]) for d in rows]
    pick = g["answer"]["unit"]
    colours = [BAR if d["unit"] == pick else BAR_OTHER for d in rows]
    fig, ax = plt.subplots(figsize=(6.9, 3.9), dpi=200)
    bars = ax.barh(labels, values, height=0.62, color=colours, linewidth=0)
    ax.set_xlabel("Avoidable complications on the separations planned for the quarter from 1 April 2027", fontsize=8.5, color=INK)
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
            ax.annotate("%d" % round(d["avoidable"]), (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                        xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5,
                        color=BAR if d["unit"] == pick else INK,
                        fontweight="bold" if d["unit"] == pick else "normal")
    ax.annotate("recommended", (bars[-1].get_width(), bars[-1].get_y() + bars[-1].get_height() / 2),
                xytext=(22, 0), textcoords="offset points", va="center", fontsize=7.6, color=BAR)
    fig.tight_layout(pad=0.6, rect=(0, 0, 1, 0.918))
    # the finding runs across the figure, not the axes, so a long title is never clipped
    fig.text(0.011, 0.985, "Alderbrook Orthopaedics avoids %d complications, %d more than the closest unit"
             % (round(g["answer"]["avoidable"]), round(g["gap"])), ha="left", va="top", fontsize=9.8, color=INK)
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
    for d in sorted(g["units"], key=lambda x: -x["avoidable"]):
        rows.append([d["unit"], "%s %s" % (short(d["hospital"]), d["name"]), d["plan"],
                     round(d["expected_plan"], 1), round(d["ratio"], 2), round(d["ratio_net"], 2),
                     round(d["avoidable"])])
    _sheet(ws, "Cycle IP-10 placement: avoidable complications by unit",
           "Quarter from 1 April 2027. Eligible units under charter clause 4.2. Prepared by Clinical "
           "Improvement, 18 March 2027.",
           ["Cost centre", "Unit", "Planned separations", "Expected complications",
            "Standardised ratio, published rates", "Standardised ratio, the network's own rates",
            "Avoidable complications"],
           rows, [12, 30, 13, 13, 15, 17, 14],
           {3: "#,##0", 4: "0.0", 5: "0.00", 6: "0.00", 7: "#,##0"})
    n = len(rows)
    ws.append([])
    ws.append(["Recommendation", "%s %s (%s)" % (short(a["hospital"]), a["name"], a["unit"])])
    ws.append(["Avoidable complications", round(a["avoidable"])])
    ws.append(["Closest unit", "%s %s (%s)" % (short(r["hospital"]), r["name"], r["unit"])])
    ws.append(["Avoidable complications there", round(r["avoidable"])])
    ws.append(["Gap", round(a["avoidable"]) - round(r["avoidable"])])
    for i in range(n + 6, n + 11):
        ws.cell(row=i, column=1).font = HEAD
    ws.print_area = "A1:G%d" % (n + 10)

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
                 ["Avoidable complications", "Charter clause 4.3: the complications the unit's own "
                  "patients had, less the complications that patients of the same risk band and age band "
                  "ordinarily have, counted patient by patient and summed, then carried onto the "
                  "separations planned for the assessment quarter."],
                 ["The network's own rates", "Complications per in-scope episode by risk band and age "
                  "band, from the episode extract over the ten closed quarters of specification 4.0. The "
                  "rates published with the specification were derived from activity in the year ended "
                  "30 June 2024 and clause 3.1 does not re-estimate them; the network's own rates now run "
                  "from 0.89 to 1.32 of them, band by band."],
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
    rung0, rung3 = g["rung0"], g["rung3"]
    f, demo = g["facts"], g["demo"]
    gap = round(a["avoidable"]) - round(r["avoidable"])
    d = SimpleDocTemplate(path, pagesize=A4, title="Cycle IP-10 placement recommendation", author="",
                          subject="", creator="", leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=16 * mm, bottomMargin=20 * mm)
    tbl = [["Unit", "Cost centre", "Planned separations", "Expected complications",
            "Avoidable complications"]]
    for x in sorted(g["units"], key=lambda u: -u["avoidable"])[:5]:
        tbl.append(["%s %s" % (short(x["hospital"]), x["name"]), x["unit"], "{:,}".format(x["plan"]),
                    "{:.1f}".format(x["expected_plan"]), "%d" % round(x["avoidable"])])
    flow = [
        Paragraph("Place the IP-10 team with Alderbrook Orthopaedics: %d avoidable complications, %d more "
                  "than the closest unit" % (round(a["avoidable"]), gap), TITLE_P),
        Paragraph("Clinical Improvement Partnership, cycle IP-10 (1 April to 30 June 2027). For the "
                  "Clinical Quality Committee, 24 March 2027. Prepared by Clinical Improvement.", KICKER),
        Paragraph("The team should embed with <b>Orthopaedics at Alderbrook Hospital, cost centre %s</b>. "
                  "Its own patients had %d complications over the ten closed quarters of specification "
                  "4.0. Patients in the same risk bands and age bands, across the network's own record "
                  "over the same quarters, had %.1f. On the %s separations the unit plans for the quarter "
                  "that difference is <b>%d avoidable complications</b>, against %d at %s %s, the closest "
                  "unit. The gap is %d complications, %.2f times, and %.1f standard errors of its own "
                  "sampling error, so it is not a difference the record could have produced by chance."
                  % (a["unit"], int(a["observed"]), a["expected_net"], "{:,}".format(a["plan"]),
                     round(a["avoidable"]), round(r["avoidable"]), short(r["hospital"]), r["name"],
                     gap, g["margin"], g["se_lead"]), LEAD),
        Spacer(1, 2),
        Image(chart_path, width=165 * mm, height=93.3 * mm),
        Spacer(1, 4),
        Paragraph("Every eligible unit, its planned activity for the quarter and the avoidable "
                  "complications it is carrying, is in the placement workbook.", FOOT),
        Paragraph("Why this is not the unit the quarterly indicator points at", H2),
        Paragraph("<b>%s %s</b>, cost centre %s, records %.1f complications above the published "
                  "expectation on the "
                  "quarter's planned activity, more than twice any other unit, and it is where the "
                  "indicator report points. Measured against the complications its own patients would "
                  "ordinarily have, it is carrying %d. The difference is its case mix. The stratum rates "
                  "published with specification 4.0 were derived from activity in the year ended 30 June "
                  "2024 and clause 3.1 does not re-estimate them; the network's own rates now run from "
                  "%.2f to %.2f of them, band by band, and the twelve units' surgical share of in-scope "
                  "episodes runs from %.0f per cent to %.0f per cent. A unit whose patients sit where the "
                  "published table has gone furthest out of date carries that gap as if it were its own "
                  "practice."
                  % (short(rung0["hospital"]), rung0["name"], rung0["unit"], rung0["published_excess"],
                     round(rung0["avoidable"]), f["drift_low"], f["drift_high"],
                     100 * f["surgical_low"], 100 * f["surgical_high"]), BODY),
        Paragraph("The clearest case is <b>%s %s</b>, cost centre %s, which treated the same number of "
                  "patients in every one of the ten quarters and changed nothing it does. For two of them "
                  "its orthopaedic theatre was closed and its beds carried the hospital's emergency "
                  "general surgical admissions instead. On the published expectation its complications "
                  "above expectation jump from between %.1f and %.1f a quarter to %.1f and %.1f. Measured "
                  "against what its own patients would ordinarily have, the figure holds between %.1f and "
                  "%.1f in every quarter, including those two."
                  % ("Marrowfield", demo["name"], demo["unit"], demo["published_low"],
                     sorted(r2["published"] for r2 in demo["rows"])[-3], demo["published_high"],
                     sorted(r2["published"] for r2 in demo["rows"])[-2], demo["internal_low"],
                     demo["internal_high"]), BODY),
        Paragraph("<b>%s %s</b>, cost centre %s, is the unit with the worst avoidable rate, %.1f "
                  "avoidable complications "
                  "per 1,000 separations against %.1f here. It is the smaller unit: on the separations "
                  "each plans for the quarter it is carrying %d avoidable complications against %d, so "
                  "the team avoids more here. The placement is a quarter of one team's time, and what it "
                  "buys is complications, not a rate."
                  % (short(rung3["hospital"]), rung3["name"], rung3["unit"], rung3["per_1000"],
                     a["per_1000"],
                     round(rung3["avoidable"]), round(a["avoidable"])), BODY),
        PageBreak(),
        Paragraph("How the figures were put together", H2),
        Paragraph(("Observed complications and the published expectation are specification 4.0's, from the "
                   "episode extract to 31 December 2026, and tie to the quarterly indicator series on all "
                   "215 unit-quarters. The complications patients of a risk band and age band ordinarily "
                   "have are the network's own: complications per in-scope episode in each of the 24 "
                   "strata, over every closed quarter of the specification period, from the same extract. "
                   "Each unit's avoidable complications are its own patients' complications less that "
                   "expectation, taken patient by patient and summed, then carried onto the separations "
                   "the activity plan plans for the quarter at the unit's own rate per separation, which "
                   "is clause 3.4's basis. The twelve eligible units are charter clause 4.2's."), BODY),
        Paragraph(("The ranking does not depend on how the comparison is drawn. Taking the network's own "
                   "rates over the last eight quarters, the last four, or the latest quarter alone; "
                   "leaving the unit's own patients out of the comparison; taking the unit's record over "
                   "any of those windows; and carrying the rate on in-scope episodes rather than on all "
                   "separations all put this unit first, by between 1.07 and 2.85 times."), BODY),
        Table([[Paragraph(c, CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(tbl)],
              colWidths=[56 * mm, 20 * mm, 30 * mm, 30 * mm, 28 * mm], style=TBL),
        Spacer(1, 6),
        Paragraph("Cost centre 41510 has reported under its own code since the Carrowdean medical wards "
                  "were amalgamated on 1 October 2025, and its five closed quarters meet clause 4.2. "
                  "Rehabilitation and Aged Care at Marrowfield, where the team is until 31 March, is not "
                  "eligible this cycle. Avoidable complications are whole complications on the quarter's "
                  "planned separations; expected complications and complications above the published "
                  "expectation are carried to one decimal.", FOOT),
    ]
    d.build(flow, onFirstPage=_page, onLaterPages=_page)
    return path
