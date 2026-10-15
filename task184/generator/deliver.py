"""The two goldens: the tasking paper the community safety manager puts to the partnership board, and the workbook
behind it."""
import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import analysis as AN   # noqa: E402
import docs as D        # noqa: E402,F401  (registers the Liberation fonts this paper is set in)
import world as W       # noqa: E402

PAPER = "harbourgate_patrol_slate_2027.pdf"
BOOK = "harbourgate_slot_weights.xlsx"

INK, GREY, RULE = colors.HexColor("#1b2733"), colors.HexColor("#59636f"), colors.HexColor("#97a1ab")
MARK = colors.HexColor("#1f5c86")
BODY = ParagraphStyle("b", fontName="Sans", fontSize=9.8, leading=13.4, textColor=INK, spaceAfter=5)
H1 = ParagraphStyle("h1", fontName="Sans-B", fontSize=14.2, leading=18, textColor=INK, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="Sans-B", fontSize=10.4, leading=13.8, textColor=INK, spaceBefore=9, spaceAfter=3)
META = ParagraphStyle("m", fontName="Sans", fontSize=8.4, leading=10.8, textColor=GREY, spaceAfter=9)
CELL = ParagraphStyle("cell", fontName="Sans", fontSize=8.4, leading=10.2, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Sans-B")
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
CELLRB = ParagraphStyle("cellrb", parent=CELLB, alignment=2)
FOOT = ParagraphStyle("foot", fontName="Sans", fontSize=7.8, leading=10.0, textColor=GREY, spaceBefore=3,
                      spaceAfter=6)

BANDS = list(range(0, 24, W.SLOT_H))


def fifty(x):
    return int(round(x / 50.0) * 50)


def band_label(h):
    return "%02d:00 to %02d:00" % (h, (h + W.SLOT_H) % 24)


def heatmap(path, weights, slate):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.0, "svg.hashsalt": "184"})
    grid = [[weights[(d, h)] for d in range(7)] for h in BANDS]
    fig, ax = plt.subplots(figsize=(6.9, 2.9))
    im = ax.imshow(grid, cmap="Blues", aspect="auto", vmin=0, vmax=max(weights.values()))
    ax.set_xticks(range(7), [d[:3] for d in W.DAYS])
    ax.set_yticks(range(len(BANDS)), [band_label(h) for h in BANDS])
    for i, h in enumerate(BANDS):
        for d in range(7):
            v = weights[(d, h)]
            commissioned = (d, h) in slate
            ax.text(d, i, "%d" % fifty(v), ha="center", va="center", fontsize=7.0,
                    color="white" if v > 0.62 * max(weights.values()) else "#1b2733",
                    fontweight="bold" if commissioned else "normal")
            if commissioned:
                ax.add_patch(plt.Rectangle((d - 0.5, i - 0.5), 1, 1, fill=False, edgecolor="#b4421f", lw=1.6))
    ax.set_title("Contracted offences a season met in each patrol slot; the eight commissioned are outlined",
                 fontsize=8.4, pad=6)
    fig.colorbar(im, ax=ax, shrink=0.82, label="offences a season")
    fig.tight_layout()
    fig.savefig(path, dpi=130, metadata={"Software": None})
    plt.close(fig)


def _table(rows, widths, aligns=None):
    data = []
    for i, r in enumerate(rows):
        row = []
        for j, c in enumerate(r):
            right = aligns and aligns[j] == "r"
            style = (CELLRB if right else CELLB) if i == 0 else (CELLR if right else CELL)
            row.append(Paragraph(str(c), style))
        data.append(row)
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2.8), ("LINEBELOW", (0, 0), (-1, 0), 0.7, INK),
                           ("LINEBELOW", (0, 1), (-1, -2), 0.3, RULE)]))
    return t


def paper(path, fig, lad, tmp):
    g = lad["golden"]
    w, slate = g["weights"], g["slate"]
    order = sorted(w.items(), key=lambda kv: -kv[1])
    runner = order[W.CAP]
    png = os.path.join(tmp, "week.png")
    heatmap(png, w, set(slate))
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                          bottomMargin=16 * mm, title="Harbourgate hotspot patrol: 2027 tasking slate",
                          author=W.PARTNERSHIP, subject="", creator="", producer="")
    man, man_role = W.PEOPLE["manager"]
    f = [Paragraph("The 2027 Harbourgate patrol slate moves into the small hours", H1),
         Paragraph("%s, %s. For the council's community safety committee at the annual review, %s."
                   % (man, man_role, W.PAPER_DATE.strftime("%d %B %Y")), META),
         Paragraph("Recommendation", H2),
         Paragraph("Commission the eight slots in the table below: Saturday, Sunday and Friday through the late "
                   "evening and the small hours, "
                   "the two early-morning slots as the market opens, and the Wednesday and Thursday evenings. The "
                   "agreement covers %s recorded offences a season in the "
                   "quarter, and over a season those eight slots would have a patrol on the ground for %s of them, "
                   "against %s for the eight slots the windows' midpoints put first. The ninth slot by weight is "
                   "%s, at %s against the %s of the weakest of the eight, so "
                   "the eight are not finely balanced and the slate should hold for the whole season, as clause 6.1 "
                   "requires."
                   % ("{:,}".format(fig["context"]["contracted_offences_a_season"]),
                      "{:,}".format(fifty(g["files"])), "{:,}".format(fifty(lad["rung2_midpoint"]["meets"])),
                      "%s %02d:00 to %02d:00" % (W.DAYS[runner[0][0]], runner[0][1],
                                                 (runner[0][1] + W.SLOT_H) % 24),
                      "{:,}".format(fifty(runner[1])), "{:,}".format(fifty(w[slate[-1]]))), BODY),
         Paragraph("The eight slots", H2)]
    rows = [["Slot", "Offences a season met in it"]]
    for s in slate:
        rows.append(["%s %02d:00 to %02d:00" % (W.DAYS[s[0]], s[1], (s[1] + W.SLOT_H) % 24),
                     "{:,}".format(fifty(w[s]))])
    rows.append(["The eight together", "{:,}".format(fifty(g["files"]))])
    f.append(_table(rows, [64, 52], aligns=[None, "r"]))
    f.append(Paragraph("Source: the records management extract of 22 January 2027, offences of the classes at Annex "
                       "B recorded at the five locations in the quarter's location register, 1 April to 30 "
                       "September 2025 and 2026. Figures are one season, the mean of the two on record, to the "
                       "nearest fifty offences.", FOOT))
    f.append(Spacer(1, 7))
    f.append(Paragraph("The week", H2))
    f.append(Image(png, width=167 * mm, height=70 * mm))
    f.append(Paragraph("How the figures are built", H2))
    f.append(Paragraph("Almost none of these offences was seen happening. A business is shut at ten and open at "
                       "seven and the shutter has been forced; a car is left at the Quayside at half past eight and "
                       "the window is out by one. The record holds the two times the victim can vouch for and "
                       "nothing between them, and for nine in ten of the covered offences they are more than four "
                       "hours apart, so a single offence belongs to more than one patrol slot. Each offence is "
                       "therefore counted into every slot its occurrence window touches, in proportion to the share "
                       "of the window that falls in that slot, and a slot's figure is the sum of those shares over "
                       "the two seasons on record, divided by two. The workbook %s carries the figure for every "
                       "slot in the week, and the volume, location and footfall tables behind this paper." % BOOK,
                       BODY))
    f.append(Paragraph("Taking the earliest time each offence can have happened as the time it happened would put "
                       "the whole slate on the seven evening slots and Friday morning, and would credit it with "
                       "%s offences a season. Those eight slots would in fact have a patrol present for %s, a "
                       "fifth less than the slate above."
                       % ("{:,}".format(fifty(lad["rung0_window_start"]["files"])),
                          "{:,}".format(fifty(lad["rung0_window_start"]["meets"]))), BODY))
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.4)
        canvas.drawString(20 * mm, A4[1] - 11 * mm, W.PARTNERSHIP)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 11 * mm, "2027 tasking slate")
        canvas.setFont("Sans", 7.0)
        canvas.drawString(20 * mm, 9 * mm, "HG/PAT/2027 slate paper")
        canvas.drawRightString(A4[0] - 20 * mm, 9 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    d.build(f, onFirstPage=frame, onLaterPages=frame)


def workbook(path, lad, a1, a2, a3, fig=None):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

    g = lad["golden"]
    w, slate = g["weights"], set(g["slate"])
    wb = Workbook()
    head = Font(name="Calibri", size=11, bold=True)
    bold = Font(name="Calibri", size=11, bold=True)
    fill = PatternFill("solid", fgColor="DCE6F1")
    thin = Border(bottom=Side(style="thin", color="8EA9C1"))

    def sheet(title, header, rows, widths):
        ws = wb.create_sheet(title)
        ws.append(list(header))
        for c in ws[1]:
            c.font = head
            c.border = thin
            c.alignment = Alignment(horizontal="left")
        for r in rows:
            ws.append(list(r))
        for i, wd in enumerate(widths, start=1):
            ws.column_dimensions[chr(64 + i)].width = wd
        ws.freeze_panes = "A2"
        return ws

    wb.remove(wb.active)
    rows = []
    for d in range(7):
        for h in BANDS:
            rows.append([W.DAYS[d], "%02d:00 to %02d:00" % (h, (h + W.SLOT_H) % 24), fifty(w[(d, h)]),
                         "commissioned" if (d, h) in slate else None])
    ws = sheet("Week", ("Day", "Slot", "Offences a season", "2027 slate"), rows, [12, 18, 19, 15])
    for r in range(2, 2 + len(rows)):
        if ws.cell(r, 4).value:
            for c in range(1, 5):
                ws.cell(r, c).fill = fill
    srows = [["%s %02d:00 to %02d:00" % (W.DAYS[s[0]], s[1], (s[1] + W.SLOT_H) % 24), fifty(w[s])]
             for s in g["slate"]]
    srows.append(["The eight together", fifty(g["files"])])
    ws = sheet("Commissioned", ("Slot", "Offences a season"), srows, [26, 19])
    ws.cell(1 + len(srows), 1).font = bold
    ws.cell(1 + len(srows), 2).font = bold
    rows = [[c, 2025 + si, int(round(a1[(c, si)], -1))] for c in W.CLASSES for si in range(len(W.SEASONS))]
    sheet("Offences by class", ("Home Office class", "Season", "Offences recorded in the quarter"), rows,
          [30, 10, 31])
    rows = [[loc, 2025 + si, round(a2[(loc, si)], 1)] for loc in W.LOCATIONS for si in range(len(W.SEASONS))]
    sheet("Location shares", ("Location", "Season", "Share of the quarter's offences, per cent"), rows, [26, 10, 36])
    rows = [[sid, 2025 + si, int(round(a3[(sid, si)], -1))]
            for sid in sorted(W.SENSORS) for si in range(len(W.SEASONS))]
    sheet("Footfall", ("Sensor", "Season", "Footfall per trading hour"), rows, [12, 10, 26])
    notes = wb.create_sheet("Notes")
    notes["A1"] = "Harbourgate patrol slot weights: what is in this workbook"
    notes["A1"].font = Font(name="Calibri", size=12, bold=True)
    for i, line in enumerate([
            "Prepared for the annual review of the Harbourgate hotspot patrol, 29 January 2027.",
            "Source: kcp_rms_offence_extract_2027-01-22.csv, with kcp_cis_offence_extract_2025.csv for the classes "
            "the crime information system still held in the 2025 season.",
            "Population: offences of the classes at Annex B of the tasking agreement, at the five locations in "
            "harbourgate_location_register.csv, occurring between 1 April and 30 September in 2025 and in 2026.",
            "Slot figures are one season, the mean of the two seasons on record, to the nearest fifty offences. "
            "An offence whose occurrence window touches more than one slot is counted into each in proportion to "
            "the share of the window falling in it.",
            "The Cranstoun length of Harbourgate Street, above number 178, is outside the quarter and outside "
            "every figure here.",
            "Offence counts by class are to the nearest ten and count one offence once, whichever system holds it; "
            "the three classes written to both systems in the fortnight of 14 to 27 July 2025 are counted once.",
            "Shoplifting was recorded once per incident before the move to the records management system and once "
            "per victim after it, so its two seasons are not comparable.",
            "Location shares are to one decimal place and are shares of the quarter's recorded offences of all "
            "classes in the season.",
            "Footfall is the business improvement district's feed, stamped in UTC and an hour behind local time, "
            "over the quarter's trading hours. The hours the supplier's fault log covers are out of both the "
            "count and the hours, because what the head reported for them is a part of the footfall that passed.",
            ], start=3):
        notes.cell(i, 1).value = line
        notes.cell(i, 1).alignment = Alignment(vertical="top", wrap_text=True)
    notes.column_dimensions["A"].width = 118
    for ws_ in wb.worksheets:
        if ws_.title == "Notes":
            continue
        ws_.print_title_rows = "1:1"
        for row in ws_.iter_rows(min_row=2):
            for cell in row:
                if isinstance(cell.value, int) and cell.value >= 1000:
                    cell.number_format = "#,##0"
                elif isinstance(cell.value, float):
                    cell.number_format = "0.0"
    wb.properties.creator = W.PEOPLE["analyst"][0]
    wb.properties.lastModifiedBy = W.PEOPLE["analyst"][0]
    wb.properties.created = dt.datetime(2027, 1, 28, 16, 12, 0)
    wb.properties.modified = dt.datetime(2027, 1, 29, 9, 41, 0)
    wb.properties.title = "Harbourgate patrol slot weights"
    wb.save(path)
