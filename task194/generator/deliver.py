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
    values = [round(d["avoidable"], 1) for d in rows]
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
    ax.set_xticks(range(0, int(max(values)) + 6, 5))
    for d, bar in zip(rows, bars):
        if d["unit"] in (pick, g["runner"]["unit"]):
            ax.annotate("%.1f" % d["avoidable"], (bar.get_width(), bar.get_y() + bar.get_height() / 2),
                        xytext=(4, 0), textcoords="offset points", va="center", fontsize=8.5,
                        color=BAR if d["unit"] == pick else INK,
                        fontweight="bold" if d["unit"] == pick else "normal")
    ax.annotate("recommended", (bars[-1].get_width(), bars[-1].get_y() + bars[-1].get_height() / 2),
                xytext=(22, 0), textcoords="offset points", va="center", fontsize=7.6, color=BAR)
    fig.tight_layout(pad=0.6, rect=(0, 0, 1, 0.918))
    # the finding runs across the figure, not the axes, so a long title is never clipped
    fig.text(0.011, 0.985, "%s %s carries %.1f avoidable complications, %.1f more than the closest unit"
             % (short(g["answer"]["hospital"]), g["answer"]["name"], g["answer"]["avoidable"],
                g["answer"]["avoidable"] - g["runner"]["avoidable"]),
             ha="left", va="top", fontsize=9.8, color=INK)
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
                     round(d["expected_plan"], 1), round(d["as_recorded"], 1), round(d["ratio"], 3),
                     round(d["ratio_developed"], 3), round(d["avoidable"], 1)])
    _sheet(ws, "Cycle IP-11 placement: avoidable complications by unit",
           "Quarter from 1 April 2027. Eligible units under charter clause 4.2. Prepared by Clinical "
           "Improvement, 18 March 2027.",
           ["Cost centre", "Unit", "Planned separations", "Expected complications",
            "On the record as it stands", "Standardised ratio, as recorded",
            "Standardised ratio, developed", "Avoidable complications"],
           rows, [12, 30, 13, 13, 15, 15, 15, 14],
           {3: "#,##0", 4: "0.0", 5: "0.0", 6: "0.000", 7: "0.000", 8: "0.0"})
    n = len(rows)
    ws.append([])
    ws.append(["Recommendation", "%s %s (%s)" % (short(a["hospital"]), a["name"], a["unit"])])
    ws.append(["Avoidable complications", round(a["avoidable"], 1)])
    ws.append(["Closest unit", "%s %s (%s)" % (short(r["hospital"]), r["name"], r["unit"])])
    ws.append(["Avoidable complications there", round(r["avoidable"], 1)])
    ws.append(["Gap", round(round(a["avoidable"], 1) - round(r["avoidable"], 1), 1)])
    for i in range(n + 6, n + 11):
        ws.cell(row=i, column=1).font = HEAD
    ws.print_area = "A1:H%d" % (n + 10)

    hs = wb.create_sheet("Hospital year")
    _sheet(hs, "What the complication indicator does not measure, by hospital, year ended "
               "31 December 2026",
           "The separations the activity summary reports, every unit at the site and all care types, "
           "less the in-scope episodes the indicator measured under specification 4.0 clauses 2.1 to "
           "2.3, counted at the site each unit reported under in the month. The episode extract is one "
           "row per record the warehouse received and is not the authority on separations.",
           ["Hospital", "Separations not measured", "Of those, with a complication"],
           [[h["name"], h["separations"], h["complications"]] for h in g["hospitals"]],
           [24, 16, 18], {2: "#,##0", 3: "#,##0"})

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
           [[x["group"], x["name"], x["fy2025"], x["fy2026"]] for x in g["groups_by_year"]],
           [9, 44, 12, 16], {3: "#,##0", 4: "#,##0"})

    notes = wb.create_sheet("Notes")
    for line in [["Item", "Note"],
                 ["Eligible units", "Charter clause 4.2: acute inpatient units with four or more closed "
                  "quarters on specification 4.0 and no placement in the previous twelve closed quarters. "
                  "Twelve units qualify for cycle IP-11."],
                 ["Expected complications", "Specification 3.4: planned separations times the unit's "
                  "expected complications per separation over the specification period to date."],
                 ["Standardised ratio", "Specification 3.2 and 3.3, over every closed quarter from "
                  "1 July 2024."],
                 ["Avoidable complications", "Charter clause 4.3: the complications the unit's own "
                  "patients had, less the complications that patients of the same risk band and age band "
                  "are expected to have under the published stratum table, counted patient by patient and "
                  "summed, then carried onto the separations planned for the assessment quarter. Stated "
                  "to one decimal."],
                 ["The expectation", "Specification 3.1 and Appendix A: the published stratum table, "
                  "complications per episode by risk band and age band, derived from network activity in "
                  "the year ended 30 June 2024 and not re-estimated between specifications. Every unit "
                  "here is expected at that table."],
                 ["Developing the record", "A complication is coded from the clinical documentation, so a "
                  "quarter's count keeps growing after its own coding close. The coding close-out register "
                  "publishes each quarter at its close and restates it at every close after that; a "
                  "quarter whose last two publications agree has settled. Five of the ten closed quarters "
                  "have not, and the register holds each of the five at a different close: the most "
                  "recent at its first publication alone. Each cost centre's own finished quarters give "
                  "the growth still to come."],
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
    canvas.drawString(20 * mm, 12 * mm, "Clinical Improvement Partnership, cycle IP-11")
    canvas.drawRightString(190 * mm, 12 * mm, "Page %d" % doc.page)
    canvas.restoreState()


def brief(path, g, chart_path):
    a, r = g["answer"], g["runner"]
    rung0 = g["rung0"]
    R = {k.split()[0]: v for k, v in g["routes"].items()}
    recency = R["R1"]
    by = {d["unit"]: d for d in g["units"]}
    gap = round(round(a["avoidable"], 1) - round(r["avoidable"], 1), 1)
    uq = len(g["bundle"]["panel"])
    # every quarter the register still shows moving is still filling, and the one it holds at its own
    # close alone is the shortest of them, so no filter on the publication index belongs here
    moving = sorted(g["lags"])
    up = g["pick_uplift_by_quarter"]
    shortest = max(up, key=lambda q: up[q]["uplift"])
    settled = min(up, key=lambda q: up[q]["uplift"])
    f_pick = g["factors"][(a["unit"], 0)]
    f_run = g["factors"][(r["unit"], 0)]
    margins = sorted(v["margin"] for v in g["convergence"].values())
    d = SimpleDocTemplate(path, pagesize=A4, title="Cycle IP-11 placement recommendation", author="",
                          subject="", creator="", leftMargin=20 * mm, rightMargin=20 * mm,
                          topMargin=16 * mm, bottomMargin=20 * mm)
    tbl = [["Unit", "Cost centre", "Planned separations", "On the record as it stands",
            "Avoidable complications"]]
    for x in sorted(g["units"], key=lambda u: -u["avoidable"])[:5]:
        tbl.append(["%s %s" % (short(x["hospital"]), x["name"]), x["unit"], "{:,}".format(x["plan"]),
                    "{:.1f}".format(x["as_recorded"]), "{:.1f}".format(x["avoidable"])])
    flow = [
        Paragraph("Place the IP-11 team with %s %s: %.1f avoidable complications, %.1f more than the "
                  "closest unit" % (short(a["hospital"]), a["name"], a["avoidable"], gap), TITLE_P),
        Paragraph("Clinical Improvement Partnership, cycle IP-11 (1 April to 30 June 2027). For the "
                  "Clinical Quality Committee, 24 March 2027. Prepared by Clinical Improvement.", KICKER),
        Paragraph("The team should embed with <b>%s at %s Hospital, cost centre %s</b>. Over the ten "
                  "closed quarters of specification 4.0 its patients had %.0f complications once the "
                  "quarters still being coded are carried to what they will reach, against the %.1f the "
                  "published stratum table expects of patients of the same risk band and age band. "
                  "Carried onto the %s separations the activity plan plans for the quarter, that is "
                  "<b>%.1f avoidable complications</b>, against %.1f at %s %s (%s), the closest unit."
                  % (a["name"], short(a["hospital"]), a["unit"], a["developed"], a["expected"],
                     "{:,}".format(a["plan"]), a["avoidable"], r["avoidable"],
                     short(r["hospital"]), r["name"], r["unit"]), LEAD),
        Image(chart_path, width=170 * mm, height=96 * mm),
        Paragraph("Every eligible unit, its planned activity for the quarter and the avoidable "
                  "complications it carries. Charter clause 4.2 leaves twelve units eligible.", FOOT),
        Paragraph("Why this is not the unit the quarterly indicator points at", H2),
        Paragraph("On the complications the extract records today, <b>%s %s</b>, cost centre %s, carries "
                  "%.1f on its planned separations, the most of the twelve, and this unit carries %.1f "
                  "and sits %d of 12. The record is not finished. A hospital-acquired complication is "
                  "coded from what the clinician wrote, so a quarter keeps being added to after its own "
                  "coding close, and the coding close-out register shows it: it publishes each quarter "
                  "when its coding closes and restates it at every close after that, and <b>%d</b> of "
                  "the ten closed quarters (%s) have not yet stopped moving."
                  % (short(rung0["hospital"]), rung0["name"], rung0["unit"], rung0["as_recorded"],
                     a["as_recorded"], g["recorded_rank"], len(moving), ", ".join(moving)), BODY),
        Paragraph("How much is still to come is not the same for every unit, because it depends on how "
                  "the ward records. Measured on its own finished quarters, a quarter of this unit's "
                  "coding still has to be multiplied by <b>%.4f</b> at its own close to reach what it "
                  "settles at; at %s the same multiplier is %.4f. Developing each cost centre's short "
                  "quarters on its own record adds %.2f complications to this unit's ten quarters and "
                  "%.2f to %s's. That is the whole of the difference between the two rankings."
                  % (f_pick, rung0["unit"], f_run, a["uplift"], rung0["uplift"], rung0["unit"]), BODY),
        Paragraph("The five are not interchangeable, because the record holds each of them at a different "
                  "close. %s has been through every close the register runs to and adds nothing; %s has "
                  "been through one and adds <b>%.2f</b> of the %.2f, more than half. A reading that "
                  "develops only the quarters with several publications behind them leaves most of the "
                  "answer on the table."
                  % (settled, shortest, up[shortest]["uplift"], a["uplift"]), BODY),
        Paragraph("The most recent year on its own is the worst reading of the three, not the best. Taking "
                  "only the four most recent closed quarters as the record carries them puts <b>%s %s "
                  "(%s)</b> first at %.1f and this unit last of twelve, because this unit's rate rose "
                  "through exactly the quarters the pull date cuts short: the record shows it improving "
                  "while it was getting worse."
                  % (short(by[recency["first"]]["hospital"]), by[recency["first"]]["name"],
                     recency["first"], recency["first_value"]), BODY),
        Paragraph("How the figures were put together", H2),
        Paragraph(("Observed complications and the expected count are specification 4.0's, from the "
                   "episode extract to 31 December 2026, and tie to the quarterly indicator series on all "
                   "%d unit-quarters. The expectation is the published stratum table of Appendix A, which "
                   "clause 3.1 does not re-estimate between specifications. The complications a quarter's "
                   "patients had are the complications coded so far, carried to the quarter's ultimate by "
                   "the growth that cost centre's own finished quarters show in the coding close-out "
                   "register: for a finished quarter the count at each publication and the count it "
                   "settled at are both printed, so the growth is a ratio of two figures the register "
                   "carries and nothing is estimated. Each unit's avoidable complications are its own "
                   "patients' complications less the expectation, taken patient by patient and summed, "
                   "then carried onto the separations the activity plan plans for the quarter at the "
                   "unit's own rate per separation, which is clause 3.4's basis.") % uq, BODY),
        Paragraph(("The ranking does not depend on how the growth is read. All <b>%d</b> readings the "
                   "register leaves open put this unit first: the finished quarters' ratios pooled over "
                   "their counts or averaged across the quarters, the growth read through each "
                   "intervening publication rather than in one step, and either weighting taken over "
                   "only the later finished quarters. Carrying the excess on in-scope episodes rather "
                   "than on all separations, and not carrying it at all, also put it first."
                   % len(g["convergence"])), BODY),
        Table([[Paragraph(c, CELLB if i == 0 else CELL) for c in row] for i, row in enumerate(tbl)],
              colWidths=[52 * mm, 18 * mm, 28 * mm, 30 * mm, 28 * mm], style=TBL),
        Spacer(1, 6),
        Paragraph("Cost centre 41510 has reported under its own code since the Carrowdean medical wards "
                  "were amalgamated on 1 October 2025, and its closed quarters meet clause 4.2. "
                  "Rehabilitation and Aged Care at Marrowfield, where the team is until 31 March, is not "
                  "eligible this cycle. Avoidable complications, the figures on the record as it stands "
                  "and expected complications are all stated to one decimal on the quarter's planned "
                  "separations.", FOOT),
    ]
    d.build(flow, onFirstPage=_page, onLaterPages=_page)
    return path
