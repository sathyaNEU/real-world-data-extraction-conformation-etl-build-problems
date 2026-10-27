"""task304 goldens: the Credit Committee paper support_team_2027_placement_paper.pdf and the workbook
support_team_2027_workbook.xlsx, written from figures.json."""
import datetime
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess

PDF = "support_team_2027_placement_paper.pdf"
XLSX = "support_team_2027_workbook.xlsx"
REF = "CC/2026/47"
DATE = "23 October 2026"
STAMP = "2026-10-23"
AUTHOR = "Collections Analytics"
HEAD = PatternFill("solid", fgColor="DCE4EA")
TOT = Font(bold=True)
LINE = Border(top=Side(style="thin", color="8A8A8A"))
NAMES = {P.SHORT[b]: b for b in P.ORDER}


def c(x):
    return "{:,}".format(int(x))


def gbp(x):
    return "£{:,}".format(int(x))


def about(v):
    return "fewer than 5" if v < 5 else "about %d" % (int(round(v / 10.0)) * 10)


def chart_png(fig):
    BLUE, ORANGE, INK, MUTED, SURF = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#ffffff"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    f, ax = plt.subplots(figsize=(7.4, 3.6), dpi=170)
    f.patch.set_facecolor(SURF)
    ax.set_facecolor(SURF)
    keys = ["FTB", "HLTV", "SO", "BTL"]
    labels = ["First-time buyer\n2019-21", "High LTV\n2022-24", "Shared\nownership", "Buy to let"]
    x = list(range(len(keys)))
    w = 0.36
    g = [fig["call"]["avoided"][k] for k in keys]
    e = [fig["easy"]["avoided"][k] for k in keys]
    b1 = ax.bar([i - w / 2 - 0.015 for i in x], g, w, color=BLUE, zorder=3,
                label="Term increases carried by months since the increase")
    b2 = ax.bar([i + w / 2 + 0.015 for i in x], e, w, color=ORANGE, zorder=3,
                label="Arrears and payment rise only")
    for bar, v in zip(b1, g):          # the recommended forecast carries the labels, nearest ten as in the table
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4, about(v).replace("fewer than", "<")
                .replace("about ", ""), ha="center", va="bottom", fontsize=8.2, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, color=INK, fontsize=8.6)
    ax.set_ylabel("Possessions avoided in 2027", color=MUTED, fontsize=8.6)
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(axis="y", color="#e4e3df", linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#bdbcb6")
    ax.set_ylim(0, max(g + e) * 1.22)
    ax.yaxis.set_major_locator(MultipleLocator(5))
    ax.legend(frameon=False, loc="upper right", fontsize=8.2)
    f.subplots_adjust(left=0.09, right=0.99, top=0.97, bottom=0.17)
    buf = io.BytesIO()
    f.savefig(buf, format="png", facecolor=SURF, metadata={"Software": None})
    plt.close(f)
    buf.seek(0)
    return buf


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.6, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=9, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.6, textColor=colors.HexColor("#4a4a4a"))
    return body, h1, h2, small


def paper(path, fig):
    body, h1, h2, small = _styles()
    cl, ea, ex, A, B = fig["call"], fig["easy"], fig["ext"], fig["askA"], fig["askB"]
    av = cl["avoided"]

    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, "%s  |  Credit Committee  |  %s" % (P.ORG, REF))
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "%d" % d.page)
        canvas.restoreState()

    rows = [["Book", "Planning rate (plan, section 3)", "Possessions avoided in 2027"]]
    for k in ("FTB", "HLTV", "SO", "BTL"):
        rows.append([NAMES[k], "%.1f per cent" % cl["rate_pct"][k], about(av[k])])
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.8, leading=11)
    headc = ParagraphStyle("hc", parent=cell, fontName="Helvetica-Bold")
    t = Table([[Paragraph(v, headc if i == 0 else cell) for v in r] for i, r in enumerate(rows)],
              colWidths=[52 * mm, 58 * mm, 52 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#6b6b6b")),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#9a9a9a")),
                           ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#eaf1f9")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    img = Image(chart_png(fig), width=168 * mm, height=81.7 * mm)
    s = [Paragraph("The Financial Support Team should work the First-time buyer 2019-21 book in 2027", h1),
         Paragraph("Paper to the Credit Committee from %s, for %s, Head of Collections and Recoveries. %s. "
                   "Reference %s, in answer to CC/2026/41." % (AUTHOR, P.PEOPLE["head"], DATE, REF), small),
         Paragraph("1. Recommendation", h2),
         Paragraph("Place the team on the First-time buyer 2019-21 book. On the plan's own terms (the borrowers whose "
                   "account first reaches two payments in arrears during 2027, each taken on once, at the book's "
                   "planning rate, with the team cutting the chance of possession by %d per cent) it avoids %s possessions there, "
                   "against %s in High LTV 2022-24, the next best, and %s each in Shared ownership and Buy to let."
                   % (fig["basis"]["effect_pct"], about(av["FTB"]), about(av["HLTV"]), about(max(av["SO"], av["BTL"]))),
                   body),
         Paragraph("2. Why the first-time buyer book", h2),
         Paragraph("Most of the book's 2021 lending came off its five-year fixed rates between January and June 2026. "
                   "At the switch, %s of the %s accounts now on the book took a longer term under the Mortgage "
                   "Charter, a median %d years more, which held their payment rise to a median %d per cent against "
                   "%d per cent for the borrowers on the book who kept their term. Almost all of them were up to date "
                   "at 30 September 2026, and on their arrears and payment rise alone they look safer than the rest "
                   "of the book."
                   % (c(ex["ftb_raised_2026"]), c(ex["ftb_on_book"]), ex["years_added_median"],
                      ex["pay_rise_extended"], ex["pay_rise_kept"]), body),
         Paragraph("Our own history says otherwise. Of the %s accounts whose term was raised in 2024, %s two "
                   "payments or more in arrears at one of the eight month ends after the month of the increase, and %d at a "
                   "month end after it up to 30 September 2026: the longer term keeps a stretched budget current for a while, then the arrears "
                   "come. The 2026 extensions reach that point during 2027. Carried month by month on the "
                   "chance the earlier extensions show by months since the increase, the first-time buyer book "
                   "produces more borrowers newly two payments behind in 2027 than any other book, and at its "
                   "planning rate that is where the team avoids the most possessions."
                   % (c(ex["raised_2024"]), "none was" if ex["behind_8m"] == 0 else "%d were" % ex["behind_8m"],
                      ex["behind_by_asof"]), body),
         Paragraph("3. Possessions avoided by book", h2),
         t, Spacer(1, 6), img,
         Paragraph("Possessions avoided in 2027 by book, nearest ten (fewer than 5 marked &lt;5): the forecast that carries "
                   "each term increase by months since it (blue) and the same forecast on arrears and the payment rise "
                   "at the last switch only (orange). Source: mortgage book and payment history at 30 September 2026; "
                   "planning rates from CC/2026/41.", small),
         Paragraph("4. What the usual forecast would have said", h2),
         Paragraph("The same arrears forecast without the term increase, reading each account's payment rise at its last "
                   "switch, puts High LTV 2022-24 first at %s possessions avoided, with the first-time buyer book "
                   "well behind it. It reads the extended accounts' small payment rise as low risk, which is the one "
                   "thing the 2024 extensions show it is not." % about(ea["avoided"]["HLTV"]), body),
         Paragraph("5. The recoveries position", h2),
         Paragraph("The borrowers already in litigation stay with the recoveries team, and the workbook sets out the "
                   "court work and the cost of a possession in each owner-occupied book. From October 2025 to "
                   "September 2026 the courts made or varied %d possession orders in the first-time buyer book, %d in "
                   "High LTV and %d in Shared ownership, and at 30 September 2026 %d, %d and %d claims were open. A "
                   "possession sold in the same year cost an average of %s in the first-time buyer book, %s in High "
                   "LTV and %s in Shared ownership; %s fell short of the debt."
                   % (A["FTB"]["orders"], A["HLTV"]["orders"], A["SO"]["orders"], A["FTB"]["open"], A["HLTV"]["open"],
                      A["SO"]["open"], gbp(B["FTB"]["avg_loss"]), gbp(B["HLTV"]["avg_loss"]),
                      gbp(B["SO"]["avg_loss"]),
                      ("all %d of High LTV's sales" % B["HLTV"]["sold"]) if B["HLTV"]["at_loss"] == B["HLTV"]["sold"]
                      else ("%d of High LTV's %d sales" % (B["HLTV"]["at_loss"], B["HLTV"]["sold"]))), body),
         Paragraph("6. Basis", h2),
         Paragraph("Records at 30 September 2026: the mortgage book, the monthly payment history since January 2019, the "
                   "possession register, completed sales, LPA receiver appointments and the panel firms' litigation "
                   "actions. Payments in arrears are the arrears balance over the current contractual payment, "
                   "rounded down, at the month end (Arrears and Possessions Policy, section 2). The forecast fits the "
                   "monthly moves between nought, one and two or more payments behind on January 2024 to August 2026, "
                   "by book, the payment rise at the last switch and the months since a term increase (under 8, 8 to "
                   "15, 16 or more), leaving out the month an account closes, and carries the accounts on the book at "
                   "30 September 2026 that are not with the recoveries team through 2027, with no allowance for "
                   "accounts that close, counting each account's first entry once. Possessions avoided are rounded to "
                   "the nearest ten and losses to the nearest hundred pounds.", small)]
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Placing the Financial Support Team in 2027", author=AUTHOR,
                            creator=P.ORG, subject="Credit Committee paper %s" % REF, invariant=1)
    doc.build(s, onFirstPage=foot, onLaterPages=foot)
    postprocess.scrub(path, P.ORG, STAMP)


def _head(ws, row, cols):
    for j, h in enumerate(cols, 1):
        cc = ws.cell(row=row, column=j, value=h)
        cc.font = Font(bold=True)
        cc.fill = HEAD
        cc.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, w):
    for j, x in enumerate(w, 1):
        ws.column_dimensions[get_column_letter(j)].width = x


def workbook(path, fig, detail):
    A, B = fig["askA"], fig["askB"]
    oo = ["FTB", "HLTV", "SO"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Court work"
    ws["A1"] = "Possession orders made or varied at hearings, October 2025 to September 2026, and claims open at 30 September 2026"
    ws["A1"].font = Font(bold=True, size=12)
    _head(ws, 3, ["Book", "Orders made or varied at hearings", "Of which suspended on terms",
                  "Claims open at 30 Sep 2026"])
    ws.row_dimensions[3].height = 32
    for k in oo:
        ws.append([NAMES[k], A[k]["orders"], A[k]["suspended"], A[k]["open"]])
    ws.append(["Total", sum(A[k]["orders"] for k in oo), sum(A[k]["suspended"] for k in oo),
               sum(A[k]["open"] for k in oo)])
    for cc in ws[7]:
        cc.font = TOT
        cc.border = LINE
    _widths(ws, [26, 13, 18, 18])
    ws.freeze_panes = "A4"

    ws = wb.create_sheet("Sales Oct 2025-Sep 2026")
    ws["A1"] = "Possessions sold with completion from October 2025 to September 2026, by owner-occupied book"
    ws["A1"].font = Font(bold=True, size=12)
    _head(ws, 3, ["Book", "Possessions sold", "Sold at a loss", "Average loss per possession sold (£)"])
    ws.row_dimensions[3].height = 32
    for k in oo:
        ws.append([NAMES[k], B[k]["sold"], B[k]["at_loss"], B[k]["avg_loss"]])
    for row in ws.iter_rows(min_row=4, max_row=6, min_col=4, max_col=4):
        for cc in row:
            cc.number_format = "#,##0"
    _widths(ws, [26, 15, 13, 22])
    ws.freeze_panes = "A4"

    ws = wb.create_sheet("Orders detail")
    _head(ws, 1, ["Claim number", "Account number", "Book", "Hearing date", "Order", "Terms"])
    for r in detail["orders"]:
        ws.append([r["claim_number"], r["account_number"], r["book"], datetime.date.fromisoformat(r["date"]),
                   r["action"].replace("Possession order ", "").capitalize(), r["detail"]])
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=4, max_col=4):
        for cc in row:
            cc.number_format = "dd/mm/yyyy"
    _widths(ws, [16, 16, 26, 13, 10, 20])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:F%d" % ws.max_row

    ws = wb.create_sheet("Open claims detail")
    _head(ws, 1, ["Claim number", "Account number", "Book", "Order on the claim"])
    order_of = {"outright": "Outright", "suspended": "Suspended on terms", "none": "No order"}
    for r in sorted(detail["claims"], key=lambda r: (str(r["book"]), r["claim_number"])):
        if r["book"] in P.ORDER[:3]:
            ws.append([r["claim_number"], r["account_number"], r["book"], order_of[r["state"]]])
    _widths(ws, [16, 16, 26, 20])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:D%d" % ws.max_row

    ws = wb.create_sheet("Sales detail")
    _head(ws, 1, ["Completion date", "Account number", "Book", "Debt at possession, all loan parts (£)",
                  "Sale price (£)", "Selling costs (£)", "Loss written off (£)"])
    ws.row_dimensions[1].height = 30
    for r in detail["sales"]:
        ws.append([datetime.date.fromisoformat(r["completion_date"]), r["acct"], r["book"],
                   round(r["debt"], 2), round(r["sale_price"], 2), round(r["selling_costs"], 2), round(r["loss"], 2)])
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=4, max_col=7):
        for cc in row:
            cc.number_format = "#,##0.00"
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=1):
        for cc in row:
            cc.number_format = "dd/mm/yyyy"
    _widths(ws, [14, 16, 26, 20, 14, 15, 16])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:G%d" % ws.max_row

    ws = wb.create_sheet("Notes")
    notes = [
        ("Orders", "Possession orders made or varied at a hearing dated October 2025 to September 2026. When the court "
                   "corrects an order it re-seals it, and Pennant Moss logs the re-sealed copy as an order made again "
                   "with no hearing before it: that is the same order and is counted once. One panel firm reports each "
                   "action once per defendant."),
        ("Claims open", "A claim stays open until it is withdrawn, its order is discharged or set aside, or the property "
                        "is taken into possession (Arrears and Possessions Policy, section 5). The possession register "
                        "dates every possession; one panel firm's reports end at the warrant and carry no eviction."),
        ("Loss", "One possession per property sold. The debt at possession (balance, arrears and legal costs) is every "
                 "loan part's: an account with a further advance has a register row for each part, and the Society "
                 "issues a completion statement for each part showing the same sale. The loss is that debt less the "
                 "sale price net of the agent's and conveyancing fees, nil where the sale covers the debt (policy, "
                 "section 8). A corrected completion statement replaces the one before it; receivers' sales are "
                 "matched to the account through the receiver's appointment."),
        ("Book", "Each account's lending book as the payment history carries it. The possession register keeps the "
                 "book each row was entered under; before the April 2026 re-cut its first-time buyer book held all "
                 "lending to first-time buyers."),
        ("Sources", "Litigation actions, possession register, completed sales and LPA receiver appointments to 30 "
                    "September 2026; mortgage book and payment history at 30 September 2026."),
    ]
    _head(ws, 1, ["Item", "Note"])
    for a, b in notes:
        ws.append([a, b])
    for row in ws.iter_rows(min_row=2, min_col=2, max_col=2):
        for cc in row:
            cc.alignment = Alignment(wrap_text=True, vertical="top")
    _widths(ws, [16, 110])
    wb.properties.creator = AUTHOR
    wb.properties.lastModifiedBy = AUTHOR
    wb.save(path)
    postprocess.scrub(path, P.ORG, STAMP)
    postprocess.finish_office(path, "2026-10-21T09:05:00Z", "2026-10-23T16:20:00Z", P.ORG, person=AUTHOR)
