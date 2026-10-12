"""The goldens: the posting memo to the Head of Screening Operations (mobile_team_posting_summer_2027.pdf, two pages
with its chart) and the effect workbook (mobile_team_effect_2027.xlsx), from the figures analysis.py computes, and
generator/figures.json with every figure the write-up states."""
import io
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import openpyxl                                                            # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side     # noqa: E402
from reportlab import rl_config                                            # noqa: E402

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,  # noqa
                                TableStyle)

import analysis as AN      # noqa: E402
import docs as D           # noqa: E402
import postprocess as PP   # noqa: E402
import records as R        # noqa: E402
import world as W          # noqa: E402

PDF = "mobile_team_posting_summer_2027.pdf"
XLSX = "mobile_team_effect_2027.xlsx"
REF = "KAS-CP-2027-014"
INK, INK2, GRID = "#1c2228", "#59626b", "#e1e5e9"
PICK_C = ("#a8461f", "#c8714a", "#e3a98c")      # the pick: late June, July, August
REST_C = ("#3b5873", "#7590a8", "#b4c4d3")
PERIOD_LABEL = {"late June": "15-30 June", "July": "July", "August": "August"}

SANS, SANS_B = D.SANS, D.SANS_B
from reportlab.pdfbase.pdfmetrics import registerFontFamily   # noqa: E402

registerFontFamily(SANS, normal=SANS, bold=SANS_B, italic=SANS, boldItalic=SANS_B)
C_INK = colors.HexColor(INK)
C_GREY = colors.HexColor(INK2)
BODY = ParagraphStyle("body", fontName=SANS, fontSize=9.6, leading=13.2, textColor=C_INK, spaceAfter=6)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=8.2, leading=10.8, textColor=C_GREY, spaceAfter=4)
TITLE = ParagraphStyle("title", fontName=SANS_B, fontSize=13.6, leading=17, textColor=C_INK, spaceAfter=7)
H2 = ParagraphStyle("h2", fontName=SANS_B, fontSize=10, leading=13, textColor=C_INK, spaceBefore=6, spaceAfter=4)
META = ParagraphStyle("meta", fontName=SANS, fontSize=8.4, leading=11, textColor=C_GREY)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.6, leading=10.6, textColor=C_INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)
CELLR = ParagraphStyle("cellr", parent=CELL, alignment=2)
CELLRB = ParagraphStyle("cellrb", parent=CELLR, fontName=SANS_B)


def n0(x):
    return "{:,}".format(int(x))


def eur(x):
    return "{:,.2f}".format(x)


def chart_png(F):
    fig_ = AN.figures(F)
    order = sorted(W.CODES, key=lambda c: F["tot"]["interval"][c])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.4, "axes.edgecolor": INK2,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
    fig, ax = plt.subplots(figsize=(6.9, 3.05), dpi=170)
    ys = list(range(len(order)))
    for y, c in zip(ys, order):
        left = 0
        cols = PICK_C if c == F["pick"] else REST_C
        for k, (n, _, _) in enumerate(W.PERIODS):
            v = fig_["moved"][W.NAME[c]][n] / 1000.0
            ax.barh(y, v, left=left, color=cols[k], height=0.62, zorder=3,
                    label=PERIOD_LABEL[n] if c == order[0] else None)
            left += v
        tot = fig_["moved_total"][W.NAME[c]]
        ax.text(left + 4, y, n0(tot), va="center", fontsize=7.8, color=INK if c == F["pick"] else INK2,
                fontweight="bold" if c == F["pick"] else "normal")
    ax.set_yticks(ys)
    ax.set_yticklabels([W.NAME[c] for c in order])
    ax.set_xlabel("Passengers moved within the 20-minute standard, thousands")
    ax.set_xlim(0, 450)
    ax.xaxis.grid(True, color=GRID, linewidth=0.7, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(length=0)
    h, lab = ax.get_legend_handles_labels()
    ax.legend(h, lab, frameon=False, fontsize=7.6, loc="lower right", ncol=3)
    ax.set_title("Halloran Bay: the unit's three lanes all reach its morning and evening banks", fontsize=9.2,
                 color=INK, loc="left", fontweight="bold")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _grid(rows, widths, bold_rows=(), head=True):
    data = []
    for i, r in enumerate(rows):
        line = []
        for j, v in enumerate(r):
            st = (CELLB if (i == 0 and head) or i in bold_rows else CELL) if j == 0 else \
                (CELLRB if (i == 0 and head) or i in bold_rows else CELLR)
            line.append(Paragraph(str(v), st))
        data.append(line)
    t = Table(data, colWidths=widths, hAlign="LEFT")
    cmds = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0), ("LINEBELOW", (0, 0), (-1, 0), 0.7, C_INK),
            ("LINEBELOW", (0, -1), (-1, -1), 0.5, colors.HexColor("#a5adb5"))]
    for i in bold_rows:
        cmds.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#f6ebe5")))
    t.setStyle(TableStyle(cmds))
    return t


def write_pdf(path, F, png):
    fg = AN.figures(F)
    pick, runner = F["pick"], F["runner"]
    tot = F["tot"]["interval"]
    head = W.PEOPLE["head"]
    analyst = W.PEOPLE["analyst"]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title="Mobile screening unit: summer 2027 posting",
                            author=analyst[0], subject="", creator="", producer="")
    s = [Paragraph("%s · CAPACITY PLANNING" % W.AGENCY.upper(), META), Spacer(1, 4)]
    block = [["To", "%s, %s" % head], ["From", "%s, %s" % analyst], ["Date", W.MEMO_DATE.strftime("%-d %B %Y")],
             ["Reference", REF], ["Subject", "Mobile screening unit: posting for 15 June to 31 August 2027"]]
    mt = Table([[Paragraph(a, CELLB), Paragraph(b, CELL)] for a, b in block], colWidths=[24 * mm, 140 * mm],
               hAlign="LEFT")
    mt.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 0.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 0.6),
                            ("LINEBELOW", (0, -1), (-1, -1), 0.6, C_INK)]))
    s += [mt, Spacer(1, 8)]
    s.append(Paragraph("Post the unit to Halloran Bay: it moves %s passengers within the 20-minute standard this "
                       "summer, against %s at %s" % (n0(fg["pick_total"]), n0(fg["runner_total"]), W.NAME[runner]),
                       TITLE))
    s.append(Paragraph(
        "Posted to Halloran Bay from 15 June to 31 August, the unit would move %s passengers through screening within "
        "the 20-minute standard who would otherwise wait longer. The next best posting, %s, would move %s; every "
        "other airport less." % (n0(fg["pick_total"]), W.NAME[runner], n0(fg["runner_total"])), BODY))
    s.append(Paragraph(
        "On the summer roster patterns with the unit's three lanes added, %s would come first and Halloran Bay fifth. "
        "That is not what a posting adds. In every posting week last summer the host's duty managers stood down lanes "
        "of their own while the unit screened: at seven of the eight airports two lanes for the whole of the unit's "
        "day, and more in the quieter hours after the banks, so the unit added one lane at their banks, not three. "
        "Halloran Bay kept all five of its lanes open through both banks and stood its officers down only once each "
        "bank was over. With the new based operator's first full summer its banks are the heaviest against its lanes "
        "of the eight, and the unit's three lanes bring every passenger there within the standard."
        % W.NAME[F["rank"]["gross"][0]], BODY))
    s.append(Paragraph(
        "Spread evenly over the unit's day, Halloran Bay's stand-down looks like a little over two lanes and %s comes "
        "out ahead; but "
        "Halloran Bay releases four lanes for almost nine hours a day and none of them while its queues build, so the "
        "figures here take each host's stand-down interval by interval, as the lane counts show it." %
        W.NAME[F["rank"]["average"][0]], BODY))
    s.append(Image(io.BytesIO(png), width=170 * mm, height=170 * mm * 3.05 / 6.9))
    s.append(Paragraph("Design days of Capacity Planning's summer 2027 planning sheet, each standing for every day of "
                       "its period, run through KAS-STD-07 sections 4 and 6.", SMALL))
    s.append(Paragraph(
        "<b>How far the forecast can fall.</b> Halloran Bay stays the better posting unless its forecast passengers "
        "fall short by %d per cent or more across the summer, the smallest whole per cent shortfall at which a "
        "posting at %s would move more."
        % (fg["flip_pct"], W.NAME[runner]), BODY))
    s.append(PageBreak())
    s.append(Paragraph("Passengers the unit would move within the standard over the summer, by posting", H2))
    rows = [["Posting", "Host's own lanes stood down through its banks, 2026", "Lanes the unit adds at the banks",
             "Passengers moved, 15 June to 31 August 2027"]]
    order = sorted(W.CODES, key=lambda c: -tot[c])
    for c in order:
        r_all = W.RELEASE[c][0]
        rows.append([W.NAME[c], str(r_all), str(W.TEAM_LANES - r_all), n0(fg["moved_total"][W.NAME[c]])])
    s.append(_grid(rows, [40 * mm, 46 * mm, 36 * mm, 48 * mm], bold_rows=(1,)))
    s.append(Paragraph("Nearest hundred, from unrounded counts. Every host also stood down more lanes in the quieter "
                       "hours after its banks, which leaves the passengers moved unchanged.", SMALL))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Last summer at each airport", H2))
    a = fg
    wk = {c: sum(1 for p in F["posts"] if p["airport"] == c) for c in W.CODES}
    rows = [["Airport", "Passengers screened, 15 June to 31 August 2026", "Hotel cost per officer-night, EUR",
             "Posting weeks", "Expense claims per posting week, EUR"]]
    for c in order:
        rows.append([W.NAME[c], n0(a["passengers_2026"][W.NAME[c]]), eur(a["hotel_per_night"][W.NAME[c]]),
                     str(wk[c]), eur(a["claims_per_week"][W.NAME[c]])])
    s.append(_grid(rows, [34 * mm, 42 * mm, 34 * mm, 22 * mm, 38 * mm], bold_rows=(1,)))
    s.append(Paragraph(
        "Passengers screened: the checkpoint's passenger lanes and the unit's lanes while it was there; the staff and "
        "aircrew searched at the shift changes are not passengers. Hotel cost: every invoice and credit note on the "
        "posting's purchase order, as paid, over the officer-nights stayed. Claims: each claim line once, each claim "
        "with the posting it was made for, travel to and from the posting included.", SMALL))
    s.append(Paragraph("Method", H2))
    s.append(Paragraph(
        "Each checkpoint's lanes with the unit there are its summer 2027 roster pattern, less the lanes its duty "
        "managers stood down in each 15 minutes of every posted day last summer (the 2026 lane counts against the "
        "summer 2026 roster pattern), plus the unit's three lanes from 05:00 to 21:00. The stand-down was the same on "
        "every posted day at every host, Ardcarrig's two weeks running included. The passengers moved are those "
        "outside the standard on the roster pattern alone less those outside it with the unit, on each design day, "
        "times the days in the period (16, 31 and 31).", BODY))
    s.append(Paragraph(
        "At the other seven airports the unit's posting moves fewer passengers than at Halloran Bay in every period, "
        "because one lane at the banks is all it adds there.", BODY))
    s.append(Spacer(1, 6))
    s.append(Paragraph("%s<br/>%s" % analyst, BODY))

    def frame(canvas, doc_):
        canvas.saveState()
        canvas.setFont(SANS, 7.4)
        canvas.setFillColor(C_GREY)
        canvas.drawString(20 * mm, 10 * mm, "%s | Capacity Planning | %s" % (W.AGENCY, REF))
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d of 2" % doc_.page)
        canvas.restoreState()
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_xlsx(path, F):
    fg = AN.figures(F)
    tot = F["tot"]["interval"]
    order = sorted(W.CODES, key=lambda c: -tot[c])
    wb = openpyxl.Workbook()
    bold = Font(bold=True)
    thin = Side(style="thin", color="8C959E")
    ws = wb.active
    ws.title = "Posting effect"
    ws["A1"] = "Passengers the mobile unit would move within the 20-minute standard, summer 2027 posting"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Nearest hundred, from unrounded counts. %s, %s." % (REF, W.MEMO_DATE.strftime("%-d %B %Y"))
    ws.append([])
    ws.append(["Airport", "Code", "Host's own lanes stood down through its banks (2026)",
               "Lanes the unit adds at the banks", "Passengers moved, 15 Jun to 31 Aug 2027"])
    for cell in ws[4]:
        cell.font = bold
        cell.alignment = Alignment(horizontal="center", wrap_text=True, vertical="center")
        cell.border = Border(bottom=thin)
    ws.row_dimensions[4].height = 44
    for c in order:
        r_all = W.RELEASE[c][0]
        ws.append([W.NAME[c], c, r_all, W.TEAM_LANES - r_all, fg["moved_total"][W.NAME[c]]])
        ws.cell(row=ws.max_row, column=5).number_format = "#,##0"
    pick_row = 5
    for col in range(1, 6):
        ws.cell(row=pick_row, column=col).font = bold
        ws.cell(row=pick_row, column=col).fill = PatternFill("solid", fgColor="F6EBE5")
    ws.append([])
    ws.append(["Smallest whole per cent shortfall in Halloran Bay's forecast passengers at which another posting "
               "moves more", None, None, None, "%d%%" % fg["flip_pct"]])
    ws.cell(row=ws.max_row, column=5).alignment = Alignment(horizontal="right")
    for col, wdt in zip("ABCDE", (20, 7, 22, 16, 20)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A5"

    w2 = wb.create_sheet("Summer 2026")
    w2["A1"] = "Last summer at each airport"
    w2["A1"].font = Font(bold=True, size=12)
    w2.append([])
    w2.append(["Airport", "Code", "Passengers screened, 15 Jun to 31 Aug 2026", "Hotel cost per officer-night (EUR)",
               "Posting weeks 2026", "Expense claims per posting week (EUR)"])
    for cell in w2[3]:
        cell.font = bold
        cell.alignment = Alignment(horizontal="center", wrap_text=True, vertical="center")
        cell.border = Border(bottom=thin)
    w2.row_dimensions[3].height = 44
    wk = {c: sum(1 for p in F["posts"] if p["airport"] == c) for c in W.CODES}
    for c in order:
        w2.append([W.NAME[c], c, fg["passengers_2026"][W.NAME[c]], fg["hotel_per_night"][W.NAME[c]], wk[c],
                   fg["claims_per_week"][W.NAME[c]]])
        w2.cell(row=w2.max_row, column=3).number_format = "#,##0"
        w2.cell(row=w2.max_row, column=4).number_format = "#,##0.00"
        w2.cell(row=w2.max_row, column=6).number_format = "#,##0.00"
    for col, wdt in zip("ABCDEF", (20, 7, 20, 18, 12, 20)):
        w2.column_dimensions[col].width = wdt
    w2.freeze_panes = "A4"

    w3 = wb.create_sheet("Notes")
    notes = [
        "Notes",
        "Planning basis: KAS-STD-07 (2026 edition), sections 4 and 6; the design days of the summer 2027 planning "
        "sheet, each standing for every day of its period (15 to 30 June 16 days, July 31, August 31).",
        "Lanes with the unit posted: the summer 2027 roster pattern, less the lanes the host's duty managers stood "
        "down in each 15 minutes of every posted day in 2026 (lane counts against the summer 2026 roster pattern), "
        "plus the unit's three lanes from 05:00 to 21:00. The summer figure is the sum of the three periods' design "
        "days times their days, rounded once.",
        "Passengers screened in 2026: passenger lanes and the unit's lanes, 15 June to 31 August 2026; staff and "
        "aircrew searched at the shift changes excluded.",
        "Hotel cost per officer-night: invoices and credit notes on each posting's purchase order, as paid including "
        "VAT, over the officer-nights stayed.",
        "Expense claims per posting week: claim lines counted once, each claim with its posting, over the airport's "
        "posting weeks in 2026.",
        "Rounding: passengers to the nearest hundred, euros to the cent, the shortfall in whole per cent.",
    ]
    for i, t in enumerate(notes, start=1):
        w3.cell(row=i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    w3["A1"].font = Font(bold=True, size=12)
    w3.column_dimensions["A"].width = 110
    wb.save(path)


def main(golden, figures_path, F=None):
    F = F or AN.compute()
    os.makedirs(golden, exist_ok=True)
    png = chart_png(F)
    write_pdf(os.path.join(golden, PDF), F, png)
    PP.normalize_pdf(os.path.join(golden, PDF), b"D:20270430091412+01'00'", b"D:20270430091412+01'00'")
    write_xlsx(os.path.join(golden, XLSX), F)
    PP.normalize_ooxml(os.path.join(golden, XLSX), W.PEOPLE["analyst"][0], W.PEOPLE["analyst"][0],
                       "2027-04-28T15:02:11Z", "2027-04-30T08:11:40Z", excel=True)
    AN.write_figures(F, figures_path)
    return F
