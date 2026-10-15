"""The golden deliverables, computed from the shipped bundle by methods.Bundle: the designation memorandum (PDF, with
the 2025 births and deaths chart) and the births workbook (county figures, 2025 figures, every new 2026 account);
and generator/figures.json, from which the write-up's figures are drafted."""
import io
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                                      # noqa: E402
from reportlab import rl_config                                                       # noqa: E402

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import letter                                            # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import docs  # noqa: E402,F401  (registers the fonts)
import methods as M  # noqa: E402
import world as W  # noqa: E402

MEMO = "formation_county_designation_2027.pdf"
BOOK = "lornock_establishment_births_2026.xlsx"
NAME = W.NAME
INK = colors.HexColor("#1d2329")
GREY = colors.HexColor("#5a636b")
NAVY = colors.HexColor("#1f3a5c")
SHADE = colors.HexColor("#e3ecf5")
BODY = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.8, leading=13.2, textColor=INK, spaceAfter=6)
SMALL = ParagraphStyle("sm", parent=BODY, fontSize=8.4, leading=11, textColor=GREY)
HEAD = ParagraphStyle("h", fontName="LiberationSans-Bold", fontSize=10.6, leading=14, textColor=NAVY, spaceBefore=6,
                      spaceAfter=3)
TOP = ParagraphStyle("t", fontName="LiberationSans-Bold", fontSize=13, leading=17, textColor=NAVY, spaceAfter=2)
CELL = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.8, leading=11, textColor=INK)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="LiberationSans-Bold")


def r1(x):
    return float("%.1f" % (x + 1e-12))


def compute(target):
    B = M.Bundle(target)
    g = B.golden()
    a = B.ask_a()
    b = B.ask_b()
    order = g["order"]
    cls = g["cls"]
    rows = []
    for acc in sorted(cls, key=lambda x: (B.county[x], B.first_m[B.ai[x]], x)):
        fm = int(B.first_m[B.ai[acc]])
        y, q = W.QUARTERS[fm // 3]
        month = 3 * (q - 1) + fm % 3 + 1
        kind = cls[acc]
        link = B.pred.get(acc, "") if kind == "filed" else (B.flow(acc)[0] if kind == "workforce" else "")
        rows.append({"account_no": acc, "county_code": B.county[acc], "county": NAME[B.county[acc]],
                     "first_month": "%d-%02d" % (y, month), "birth": "Yes" if kind == "birth" else "No",
                     "set_aside_as": {"birth": "", "filed": "Filed transfer (register predecessor)",
                                      "workforce": "Workforce continued from a closed account"}[kind],
                     "continues_account": link or ""})
    fig = {
        "designated": [NAME[c] for c in g["top3"]],
        "designated_order": [NAME[c] for c in order[:3]],
        "runner_up": NAME[g["runner_up"]],
        "gap": r1(g["gap"]),
        "counties": {},
        "y2025": {},
        "totals": {"new_2026": sum(g["new"].values()), "filed_2026": sum(g["filed"].values()),
                   "workforce_2026": sum(g["workforce"].values()), "births_2026": sum(g["births"].values()),
                   "set_aside_2026": sum(g["setaside"].values()),
                   "base_2025q4": sum(g["base"].values()), "births_2025": sum(a["births"].values()),
                   "deaths_2025": sum(b["deaths"].values()), "base_2024q4": sum(a["base"].values())},
        "new_accounts": len(rows),
        "rate_unit": 100,
    }
    for c in sorted(NAME):
        fig["counties"][NAME[c]] = {"code": c, "new": g["new"][c], "filed": g["filed"][c],
                                    "workforce": g["workforce"][c], "set_aside": g["setaside"][c],
                                    "births": g["births"][c], "base": g["base"][c], "rate": r1(g["rates"][c]),
                                    "rate_unrounded": round(g["rates"][c], 4), "rank": order.index(c) + 1}
        fig["y2025"][NAME[c]] = {"births": a["births"][c], "birth_rate": r1(a["rates"][c]), "deaths": b["deaths"][c],
                                 "death_rate": r1(b["rates"][c]), "base_2024q4": a["base"][c]}
    return B, g, a, b, rows, fig


def chart(fig):
    names = [n for _, n, _, _ in W.COUNTIES]
    births = [fig["y2025"][n]["births"] for n in names]
    deaths = [fig["y2025"][n]["deaths"] for n in names]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "t455"})
    f, ax = plt.subplots(figsize=(7.0, 3.0), dpi=150)
    x = range(len(names))
    w = 0.38
    b1 = ax.bar([i - w / 2 for i in x], births, w, label="Births", color="#2f6f9f")
    b2 = ax.bar([i + w / 2 for i in x], deaths, w, label="Deaths", color="#c07b38")
    for bars in (b1, b2):
        for r in bars:
            ax.annotate("%d" % r.get_height(), (r.get_x() + r.get_width() / 2, r.get_height()), ha="center",
                        va="bottom", fontsize=7.5, xytext=(0, 1.5), textcoords="offset points")
    ax.set_xticks(list(x))
    ax.set_xticklabels(names)
    ax.set_ylabel("Establishments")
    fewer = [n for n, b_, d_ in zip(names, births, deaths) if d_ > b_]
    worst = max(names, key=lambda n: fig["y2025"][n]["deaths"] - fig["y2025"][n]["births"])
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
    ax.set_title("In 2025 closures outnumbered births in %s counties, most of all in %s" % (words[len(fewer)], worst),
                 fontsize=9.5, loc="left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_ylim(0, max(births + deaths) * 1.18)
    ax.legend(frameon=False, ncol=2, loc="upper right")
    f.tight_layout()
    buf = io.BytesIO()
    f.savefig(buf, format="png", metadata={"Software": None})
    plt.close(f)
    buf.seek(0)
    return buf


def write_memo(path, fig):
    order = sorted(fig["counties"], key=lambda n: fig["counties"][n]["rank"])
    d1, d2, d3 = fig["designated_order"]
    ru = fig["runner_up"]

    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSans", 7.8)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 11 * mm, "Labor Market Information Bureau, Business Dynamics Unit. Contains no "
                                            "employer-level data.")
        canvas.drawRightString(letter[0] - 20 * mm, 11 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=18 * mm, title="Formation County designation, 2027 to 2029",
                            author=W.ORG_LMI, subject="", creator="", producer="")
    s = [Paragraph("Department of Workforce Services &nbsp;|&nbsp; Labor Market Information Bureau &nbsp;|&nbsp; "
                   "Memorandum", SMALL),
         Paragraph("%s, %s and %s had the highest establishment birth rates in 2026" % (d1, d2, d3), TOP),
         Paragraph("Formation County designation for the 2027 to 2029 grant period", SMALL), Spacer(1, 4)]
    meta = Table([[Paragraph("<b>To</b>", CELL), Paragraph("Secretary of Commerce", CELL)],
                  [Paragraph("<b>Copy</b>", CELL), Paragraph("%s, Program Director, Office of Business Development"
                                                             % W.PEOPLE["director"], CELL)],
                  [Paragraph("<b>From</b>", CELL), Paragraph("%s, Business Dynamics Economist" % W.PEOPLE["economist"],
                                                             CELL)],
                  [Paragraph("<b>Date</b>", CELL), Paragraph("4 June 2027", CELL)],
                  [Paragraph("<b>Basis</b>", CELL), Paragraph("Guideline FC-G-2027-01; UI register and reports as "
                                                              "extracted 14 May 2027", CELL)]],
                 colWidths=[22 * mm, 150 * mm])
    meta.setStyle(TableStyle([("BOTTOMPADDING", (0, 0), (-1, -1), 1.5), ("TOPPADDING", (0, 0), (-1, -1), 1.5),
                              ("LINEBELOW", (0, -1), (-1, -1), 0.6, NAVY)]))
    s += [meta, Spacer(1, 7)]
    s.append(Paragraph("Recommendation", HEAD))
    s.append(Paragraph("<b>Designate %s, %s and %s as Formation Counties for 2027 to 2029.</b> They had the highest "
                       "establishment birth rates in 2026: %s %.1f, %s %.1f and %s %.1f births per 100 establishments. "
                       "%s is the runner-up at %.1f, %.1f below %s, and would be designated if one of the three declines."
                       % (d1, d2, d3, d1, fig["counties"][d1]["rate"], d2, fig["counties"][d2]["rate"], d3,
                          fig["counties"][d3]["rate"], ru, fig["counties"][ru]["rate"], fig["gap"], d3), BODY))
    s.append(Paragraph("2026 establishment births by county", HEAD))
    hdr = ["County", "New accounts first employing in 2026", "Set aside: business operated before",
           "Births", "Establishments employing, 2025 Q4", "Birth rate per 100"]
    data = [[Paragraph("<b>%s</b>" % h, CELL) for h in hdr]]
    for n in order:
        c = fig["counties"][n]
        st = CELLB if n in fig["designated"] else CELL
        data.append([Paragraph(n + (" (designate)" if n in fig["designated"] else ""), st),
                     Paragraph("{:,}".format(c["new"]), st), Paragraph("{:,}".format(c["set_aside"]), st),
                     Paragraph("{:,}".format(c["births"]), st), Paragraph("{:,}".format(c["base"]), st),
                     Paragraph("%.1f" % c["rate"], st)])
    t = Table(data, colWidths=[36 * mm, 30 * mm, 33 * mm, 18 * mm, 30 * mm, 24 * mm], repeatRows=1)
    style = [("LINEBELOW", (0, 0), (-1, 0), 0.6, NAVY), ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 2.2),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2), ("LINEBELOW", (0, -1), (-1, -1), 0.4, GREY)]
    for i, n in enumerate(order, start=1):
        if n in fig["designated"]:
            style.append(("BACKGROUND", (0, i), (-1, i), SHADE))
    t.setStyle(TableStyle(style))
    s.append(t)
    s.append(Paragraph("Source: UI employer register, quarterly contribution reports and wage reports as extracted 14 "
                       "May 2027; definitions and base per guideline FC-G-2027-01. Rates are compared unrounded and "
                       "shown to one decimal. Accounts opened in 2026 that had not reported employment by the extract "
                       "are not counted.", SMALL))
    s.append(Spacer(1, 3))
    s.append(Paragraph(
        "A birth is an establishment that first reported employment in 2026 and whose business did not operate before "
        "under another employer account (guideline 3.3). Of the %d new employer accounts that first reported employment "
        "in 2026, %d continue a business the register records as their predecessor and %d continue a business the "
        "register does not link: more than half of the workers each paid in its first quarter were paid the quarter "
        "before by one account that then stopped reporting, as when a buyer re-registers a business it took over or a "
        "business re-registers where it moves. Caldmere's set-aside accounts include nineteen fuel and convenience "
        "stores re-registered by their buyer in April 2026, and Tolbeck's include businesses that moved into its "
        "enterprise park from the other counties. New businesses that opened in premises a closed business had left, "
        "most of them in Quarrin, hired mostly new staff and are births."
        % (fig["totals"]["new_2026"], fig["totals"]["filed_2026"], fig["totals"]["workforce_2026"]), BODY))
    s.append(KeepTogether([Paragraph("2025 for comparison", HEAD),
                           Image(chart(fig), width=170 * mm, height=72.9 * mm), Paragraph(
        "Births by the same definition for 2025. A death is an establishment whose last month with employment fell in "
        "2025, that reported none in 2026 and whose business did not go on under another account. Rates per 100 "
        "establishments employing in the fourth quarter of 2024 are in the workbook "
        "lornock_establishment_births_2026.xlsx, with every 2026 new account.", SMALL)]))
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_book(path, fig, rows):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Designation 2026"
    bold = Font(bold=True)
    fill = PatternFill("solid", fgColor="E3ECF5")
    ws.append(["Formation Counties: 2026 establishment birth rates, Lornock Valley Development Region"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Guideline FC-G-2027-01. UI employer register, quarterly contribution and wage reports as extracted "
               "14 May 2027. Rates per 100 establishments reporting employment in 2025 Q4, compared unrounded."])
    ws.append([])
    hdr = ["County", "County code", "New accounts first employing in 2026", "Set aside: filed transfer",
           "Set aside: workforce continued", "Set aside: total", "Births", "Establishments employing 2025 Q4",
           "Birth rate per 100", "Rank", "Designated"]
    ws.append(hdr)
    for c in ws[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    order = sorted(fig["counties"], key=lambda n: fig["counties"][n]["rank"])
    for n in order:
        c = fig["counties"][n]
        ws.append([n, c["code"], c["new"], c["filed"], c["workforce"], c["set_aside"], c["births"], c["base"],
                   c["rate"], c["rank"], "Yes" if n in fig["designated"] else None])
        ws.cell(ws.max_row, 9).number_format = "0.0"
        if n in fig["designated"]:
            for cell in ws[ws.max_row]:
                cell.fill = fill
    t = fig["totals"]
    ws.append(["Region", None, t["new_2026"], t["filed_2026"], t["workforce_2026"],
               t["filed_2026"] + t["workforce_2026"], t["births_2026"], t["base_2025q4"], None, None, None])
    for c in ws[ws.max_row]:
        c.font = bold
    ws.append([])
    ws.append(["Runner-up", fig["runner_up"], "Gap to the third designated county (rate points)", fig["gap"]])
    ws.cell(ws.max_row, 4).number_format = "0.0"
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        for cell in row[2:8]:
            if isinstance(cell.value, int):
                cell.number_format = "#,##0"
    for col, wdt in zip("ABCDEFGHIJK", (14, 9, 15, 13, 15, 11, 9, 15, 11, 7, 11)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "B5"
    ws.print_title_rows = "4:4"
    y = wb.create_sheet("2025 births and deaths")
    y.append(["2025 establishment births and deaths by county"])
    y["A1"].font = Font(bold=True, size=12)
    y.append(["Births as in guideline 3.3 for 2025. A death: last month with employment in 2025, no employment "
              "reported in 2026, business not continued under another account. Rates per 100 establishments "
              "reporting employment in 2024 Q4."])
    y.append([])
    y.append(["County", "County code", "Births 2025", "Birth rate per 100", "Deaths 2025", "Death rate per 100",
              "Establishments employing 2024 Q4"])
    for c in y[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for code, n, _, _ in W.COUNTIES:
        v = fig["y2025"][n]
        y.append([n, code, v["births"], v["birth_rate"], v["deaths"], v["death_rate"], v["base_2024q4"]])
        y.cell(y.max_row, 4).number_format = "0.0"
        y.cell(y.max_row, 6).number_format = "0.0"
    y.append(["Region", None, t["births_2025"], None, t["deaths_2025"], None, t["base_2024q4"]])
    for c in y[y.max_row]:
        c.font = bold
    for row in y.iter_rows(min_row=5, max_row=y.max_row):
        for cell in (row[2], row[4], row[6]):
            if isinstance(cell.value, int):
                cell.number_format = "#,##0"
    for col, wdt in zip("ABCDEFG", (14, 9, 10, 11, 10, 11, 16)):
        y.column_dimensions[col].width = wdt
    y.freeze_panes = "B5"
    a = wb.create_sheet("New accounts 2026")
    a.append(["Account", "County code", "County", "First month with employment", "Birth", "Set aside as",
              "Continues account"])
    for c in a[1]:
        c.font = bold
    for r in rows:
        a.append([r["account_no"], r["county_code"], r["county"], r["first_month"], r["birth"],
                  r["set_aside_as"] or None, r["continues_account"] or None])
    for col, wdt in zip("ABCDEFG", (12, 9, 12, 14, 7, 40, 16)):
        a.column_dimensions[col].width = wdt
    a.freeze_panes = "A2"
    a.auto_filter.ref = "A1:G%d" % a.max_row
    a.print_title_rows = "1:1"
    n = wb.create_sheet("Notes")
    for line in [
        "Sources: UI employer register extract, quarterly contribution reports (QCEW) and quarterly wage reports, "
        "fourth quarter of 2024 to fourth quarter of 2026, as extracted 14 May 2027; guideline FC-G-2027-01.",
        "New account: first month with employment (workers on the payroll for the pay period including the 12th) in "
        "2026, none reported before 2026.",
        "Set aside, filed transfer: the register records a predecessor account (experience transfer).",
        "Set aside, workforce continued: more than half of the workers the account paid in its first quarter with "
        "employment were paid the quarter before by one account that reported no employment from that first quarter "
        "on.",
        "County: the county in which the worksite lies (the register's geocoded county).",
        "Prepared by %s, Business Dynamics Unit, Labor Market Information Bureau." % W.PEOPLE["economist"],
    ]:
        n.append([line])
    n.column_dimensions["A"].width = 130
    wb.save(path)


def main(target, golden_dir, figures_path):
    os.makedirs(golden_dir, exist_ok=True)
    B, g, a, b, rows, fig = compute(target)
    write_memo(os.path.join(golden_dir, MEMO), fig)
    write_book(os.path.join(golden_dir, BOOK), fig, rows)
    with open(figures_path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
        f.write("\n")
    return {"B": B, "g": g, "a": a, "b": b, "rows": rows, "fig": fig}
