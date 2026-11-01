"""The two golden deliverables: the placement workbook and the memo to the foundation with its chart."""
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import postprocess as PP
import world as W

ORDER = (1, 2, 3, 4, 5)
BOLD = Font(bold=True)
THIN = Side(style="thin", color="999999")


def _hdr(ws, row, cols, widths=None):
    for j, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=j, value=c)
        cell.font = BOLD
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.fill = PatternFill("solid", fgColor="DDE5EE")
        cell.border = Border(bottom=THIN)
    if widths:
        for j, wdt in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(j)].width = wdt


def workbook(path, F):
    """F: the figures (fig dict from build.py)."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Placement"
    ws["A1"] = "PHMS 2027 boost: share of each region's 2027 standard error the 1,200 interviews would remove"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Projected from the 2025 wave: each area's 2025 weight share and take, each region's intraclass "
                "correlation as published in Table 2 of the 2025 Technical Report, every 2025 area's take raised by "
                "the boost.")
    ws["A2"].alignment = Alignment(wrap_text=True)
    ws.merge_cells("A2:H2")
    ws.row_dimensions[2].height = 30
    cols = ["Health region", "2025 sampled areas", "2025 completed interviews", "Boost per area",
            "Between-area share of 2025 variance", "2027 SE with boost / without", "Share of 2027 SE removed",
            "Rank"]
    _hdr(ws, 4, cols, [18, 11, 13, 9, 15, 14, 13, 7])
    r0 = 5
    for i, r in enumerate(F["rank_order"]):
        x = F["regions"][r]
        ws.cell(row=r0 + i, column=1, value=W.RNAME[r])
        ws.cell(row=r0 + i, column=2, value=x["areas"])
        ws.cell(row=r0 + i, column=3, value=x["completes"]).number_format = "#,##0"
        ws.cell(row=r0 + i, column=4, value=x["add"])
        ws.cell(row=r0 + i, column=5, value=round(x["between_share"], 3)).number_format = "0.0%"
        ws.cell(row=r0 + i, column=6, value=round(1 - x["share"], 3)).number_format = "0.000"
        ws.cell(row=r0 + i, column=7, value=x["share_pct"] / 100.0).number_format = "0%"
        ws.cell(row=r0 + i, column=8, value=i + 1)
        if r == F["call"]:
            for j in range(1, 9):
                ws.cell(row=r0 + i, column=j).font = BOLD
    rr = r0 + 6
    ws.cell(row=rr, column=1, value="Fund").font = BOLD
    ws.cell(row=rr, column=2, value=W.RNAME[F["call"]]).font = BOLD
    ws.cell(row=rr + 1, column=1, value="Runner-up")
    ws.cell(row=rr + 1, column=2, value=W.RNAME[F["runner"]])
    ws.cell(row=rr + 2, column=1, value="Runner-up boost to do better")
    ws.cell(row=rr + 2, column=2, value=F["flip_per_area"])
    ws.cell(row=rr + 2, column=3, value="more interviews per area (%s in all across its %d areas)"
            % ("{:,}".format(F["flip_interviews"]), F["regions"][F["runner"]]["areas"]))

    ws2 = wb.create_sheet("2025 basis")
    _hdr(ws2, 1, ["Health region", "Households answering", "Estimate (%)", "Standard error (points)",
                  "Design effect", "Weighting effect", "Weighting effect at boosted takes",
                  "Intraclass correlation"], [18, 12, 10, 12, 10, 11, 14, 12])
    for i, r in enumerate(ORDER):
        x = F["regions"][r]
        vals = [W.RNAME[r], x["n"], round(x["est"], 1), round(x["se"], 2), round(x["deff"], 2),
                round(x["deffw"], 1), round(x["deffw_boost"], 1), round(x["rho"], 3)]
        for j, v in enumerate(vals, 1):
            c_ = ws2.cell(row=2 + i, column=j, value=v)
            fmt = {2: "#,##0", 3: "0.0", 4: "0.00", 5: "0.00", 6: "0.0", 7: "0.0", 8: "0.000"}.get(j)
            if fmt:
                c_.number_format = fmt
    ws2.cell(row=8, column=1, value=("Estimates, standard errors, design effects and intraclass correlations "
                                     "reproduce the 2025 Technical Report, Table 2."))

    ws3 = wb.create_sheet("2024 on current regions")
    _hdr(ws3, 1, ["Health region", "Completed interviews", "Estimate (%)", "Standard error (points)"],
         [18, 12, 10, 12])
    for i, r in enumerate(ORDER):
        x = F["ask"][r]
        ws3.cell(row=2 + i, column=1, value=W.RNAME[r])
        ws3.cell(row=2 + i, column=2, value=x["completes"]).number_format = "#,##0"
        ws3.cell(row=2 + i, column=3, value=round(x["est"], 1)).number_format = "0.0"
        ws3.cell(row=2 + i, column=4, value=round(x["se"], 2)).number_format = "0.00"
    ws3.cell(row=8, column=1, value=("2024 cases placed in the area they were assigned under: Northmark's cases "
                                     "assigned before 22 April 2024 carry pre-reorganisation area numbers."))
    ws.freeze_panes = "B5"
    ws2.freeze_panes = "B2"
    ws3.freeze_panes = "B2"
    wn = wb.create_sheet("Notes")
    notes = [
        "Prepared by the Survey Research Centre for the Wexcombe Foundation, grant WF-2026-117, 2 November 2026.",
        "Regions are those constituted by the Ministry of Health from 1 April 2024 (grant terms, section 3).",
        "The estimate is the share of households in which someone did not fill a prescription in the past 12 months "
        "because of its cost; households with no prescription to fill count among those that did not go without "
        "(Technical Report 2025, section 6).",
        "Complete and proxy interviews only; don't know and refused answers are left out (Technical Report, section 5).",
        "Weights: the area's design weight times its occupied dwellings over its completed interviews (section 3); for "
        "2027 the same rule at the boosted takes.",
        "Standard errors: Taylor linearisation, areas as primary sampling units within strata, the Central Valley "
        "supplement its own stratum (section 4).",
        "Shares are computed unrounded and rounded once for display.",
    ]
    for i, t in enumerate(notes, 1):
        wn.cell(row=i, column=1, value=t)
    wn.column_dimensions["A"].width = 120
    wb.save(path)
    PP.normalize_ooxml(path, creator="Jason Clarke", last_by="Heidi Roberts", created="2026-10-28T15:06:00Z",
                       modified="2026-11-02T21:41:00Z", title="PHMS 2027 boost placement", excel=True,
                       company="Halvorsen University")


def _chart(F):
    d = Drawing(460, 204)
    bc = HorizontalBarChart()
    bc.x, bc.y, bc.width, bc.height = 118, 34, 300, 132
    order = list(reversed(F["rank_order"]))
    vals = [F["regions"][r]["share_pct"] for r in order]
    bc.data = [vals]
    bc.categoryAxis.categoryNames = [W.RNAME[r] for r in order]
    bc.categoryAxis.labels.fontName = "Helvetica"
    bc.categoryAxis.labels.fontSize = 8.5
    bc.categoryAxis.labels.fillColor = colors.HexColor("#0b0b0b")
    bc.categoryAxis.strokeColor = colors.HexColor("#8a8984")
    bc.categoryAxis.strokeWidth = 0.6
    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 50
    bc.valueAxis.valueStep = 10
    bc.valueAxis.labels.fontName = "Helvetica"
    bc.valueAxis.labels.fontSize = 7.5
    bc.valueAxis.labels.fillColor = colors.HexColor("#52514e")
    bc.valueAxis.labelTextFormat = "%d%%"
    bc.valueAxis.strokeColor = colors.HexColor("#8a8984")
    bc.valueAxis.strokeWidth = 0.6
    bc.valueAxis.visibleGrid = 1
    bc.valueAxis.gridStrokeColor = colors.HexColor("#e4e3df")
    bc.valueAxis.gridStrokeWidth = 0.5
    bc.barWidth = 9
    bc.groupSpacing = 9
    bc.bars.strokeColor = None
    bc.bars[0].fillColor = colors.HexColor("#b9c7d8")
    bc.bars[(0, len(vals) - 1)].fillColor = colors.HexColor("#2a78d6")
    bc.barLabelFormat = "%d%%"
    bc.barLabels.fontName = "Helvetica"
    bc.barLabels.fontSize = 8
    bc.barLabels.fillColor = colors.HexColor("#0b0b0b")
    bc.barLabels.nudge = 11
    d.add(bc)
    d.add(String(0, 192, "The boost buys most precision in the %s" % W.RNAME[F["call"]], fontName="Helvetica-Bold",
                 fontSize=9.5, fillColor=colors.HexColor("#0b0b0b")))
    d.add(String(0, 180, "Share of the region's 2027 standard error removed by 1,200 more completed interviews",
                 fontName="Helvetica", fontSize=8, fillColor=colors.HexColor("#52514e")))
    d.add(String(118, 2, "Source: PHMS 2025 interviews, weights and areas; Survey Research Centre projection",
                 fontName="Helvetica", fontSize=7, fillColor=colors.HexColor("#52514e")))
    return d


def _page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#52514e"))
    canvas.drawString(0.95 * inch, 0.55 * inch, "Survey Research Centre, Halvorsen University. WF-2026-117")
    canvas.drawRightString(7.55 * inch, 0.55 * inch, "Page %d" % doc.page)
    canvas.restoreState()


def memo(path, F):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=10, leading=13.4, spaceAfter=7)
    h = ParagraphStyle("h", parent=body, fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceAfter=4)
    small = ParagraphStyle("s", parent=body, fontSize=8.5, leading=11)
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.95 * inch, rightMargin=0.95 * inch,
                            topMargin=0.85 * inch, bottomMargin=0.85 * inch, title="PHMS 2027 boost placement",
                            author="Survey Research Centre, Halvorsen University", subject="Grant WF-2026-117",
                            creator="Microsoft® Word for Microsoft 365", producer="Microsoft® Word for Microsoft 365", invariant=1)
    c, ru = F["call"], F["runner"]
    xc, xr, xn = F["regions"][c], F["regions"][ru], F["regions"][1]
    s = [Paragraph("Survey Research Centre, Halvorsen University", small),
         Paragraph("To: Jeremy Morris, Programme Director, Health Access, Wexcombe Foundation", small),
         Paragraph("From: Heidi Roberts, Director. 2 November 2026. Re: grant WF-2026-117, placing the 2027 boost",
                   small), Spacer(1, 8),
         Paragraph("The 1,200 interviews should go to the %s" % W.RNAME[c], h),
         Paragraph(
             "Spread as %d more completed interviews in each of its %d sampled areas, the boost removes %d per cent "
             "of the standard error of the %s's 2027 estimate of households going without a prescription because of "
             "its cost. %s is next at %d per cent, and only a boost of %d more interviews in each of its areas "
             "(%s in all) would remove a larger share there than 1,200 remove in the %s. The North, where the 2025 "
             "error is widest, gains %d per cent: most of its error lies between communities, and interviews added "
             "inside the same communities do not reach it."
             % (xc["add"], xc["areas"], xc["share_pct"], W.RNAME[c], W.RNAME[ru], xr["share_pct"],
                F["flip_per_area"], "{:,}".format(F["flip_interviews"]), W.RNAME[c], xn["share_pct"]), body),
         Paragraph(
             "The %s's error comes almost entirely from interviews within areas, and %d per cent of its households "
             "live in the 20 new-subdivision areas, interviewed five to an area. Each of those interviews carries "
             "about %d times the weight of a core interview, so an equal addition in every area quadruples the "
             "supplement's take and narrows the spread of the weights as well as adding sample: the weighting "
             "effect falls from %.1f to %.1f. A projection that holds the 2025 design effect's weighting part "
             "fixed misses this and puts %s first." % (W.RNAME[c], int(round(100 * xc["supp_share"])),
                                                         int(round(xc["weight_ratio"])), xc["deffw"], xc["deffw_boost"],
                                                         W.RNAME[ru]),
             body),
         _chart(F), Spacer(1, 4)]
    rows = [["Health region", "Boost per area", "Share of 2027 SE removed"]]
    for r in F["rank_order"]:
        rows.append([W.RNAME[r], str(F["regions"][r]["add"]), "%d%%" % F["regions"][r]["share_pct"]])
    t = Table(rows, colWidths=[1.9 * inch, 1.2 * inch, 1.7 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                           ("FONT", (0, 1), (-1, 1), "Helvetica-Bold", 9),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    s += [t, Spacer(1, 8),
          Paragraph("The projections rest on the 2025 wave as the terms ask: each region's 2025 areas, takes and "
                    "weights, the 2027 takes raised by the boost and the weights recomputed as the technical report "
                    "sets out, and each region's intraclass correlation as Table 2 of the report publishes it. The workbook "
                    "boost_region_2027.xlsx carries the working and each region's 2024 estimate on the current "
                    "regions.", body)]
    doc.build(s, onFirstPage=_page, onLaterPages=_page)
    PP.normalize_pdf(path, b"D:20261102154210-06'00'", b"D:20261102162047-06'00'")
