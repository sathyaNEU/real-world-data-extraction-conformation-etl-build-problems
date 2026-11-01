"""The golden deliverables, written from target/ alone: the ICAAP stress workbook and the board paper."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from docx import Document  # noqa: E402
from docx.enum.table import WD_TABLE_ALIGNMENT  # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH  # noqa: E402
from docx.shared import Pt, Cm, RGBColor  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side  # noqa: E402
from openpyxl.utils import get_column_letter  # noqa: E402

import params as P  # noqa: E402
import results as R  # noqa: E402
from io_util import save_docx, save_xlsx  # noqa: E402

XLSX = "orari_icaap_business_stress_2027.xlsx"
DOCX = "board_paper_business_stress_2027.docx"
SHORT = {"Construction": "Construction", "Manufacturing": "Manufacturing", "Trade and logistics": "Trade and logistics",
         "Hospitality, retail and leisure": "Hospitality, retail and leisure",
         "Business and property services": "Business and property services",
         "Health, education and personal services": "Health, education and personal services"}
NAVY = "1F3A5F"
THIN = Side(style="thin", color="B7C2CE")


def _hdr(ws, row, values, widths=None):
    for i, v in enumerate(values, start=1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = Font(bold=True, color="FFFFFF", size=10)
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if i > 1 else "left")
    if widths:
        for i, w in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = w


def workbook(F, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws["A1"] = "Orari Bank Limited - ICAAP 2026: business banking book under the severe scenario"
    ws["A1"].font = Font(bold=True, size=13, color=NAVY)
    ws["A2"] = ("Stress year 1 October 2026 to 30 September 2027. Book date 30 September 2026. Scenario approved by the "
                "Board on 24 September 2026 (BD-2026-09-07). Method per CR-ST-02 v3.1.")
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    ws["A4"] = "Stressed credit loss, business banking book (NZD million, nearest 0.5 million)"
    ws["A4"].font = Font(bold=True)
    ws["E4"] = F["total_half_m"]
    ws["E4"].number_format = "0.0"
    ws["E4"].font = Font(bold=True, size=12, color=NAVY)
    _hdr(ws, 6, ["Reporting segment", "Performing borrowers", "EAD (NZD m)", "Stressed loss (NZD m)",
                 "Stressed loss (NZD)", "Share of book loss"], [44, 13, 13, 15, 17, 13])
    r = 7
    for s in R.SEG_NAMES:
        ws.cell(row=r, column=1, value=s)
        ws.cell(row=r, column=2, value=F["n_seg"][s])
        ws.cell(row=r, column=3, value=round(F["ead_seg"][s] / 1e6, 1)).number_format = "#,##0.0"
        ws.cell(row=r, column=4, value=F["seg_m1"][s]).number_format = "0.0"
        ws.cell(row=r, column=5, value=round(F["seg"][s])).number_format = "#,##0"
        ws.cell(row=r, column=6, value=F["seg"][s] / F["total"]).number_format = "0.0%"
        r += 1
    ws.cell(row=r, column=1, value="Business banking book").font = Font(bold=True)
    ws.cell(row=r, column=2, value=F["n_perf"]).font = Font(bold=True)
    c = ws.cell(row=r, column=3, value=F["ead_m1"])
    c.number_format, c.font = "#,##0.0", Font(bold=True)
    c = ws.cell(row=r, column=4, value=F["total_half_m"])
    c.number_format, c.font = "0.0", Font(bold=True)
    c = ws.cell(row=r, column=5, value=round(F["total"]))
    c.number_format, c.font = "#,##0", Font(bold=True)
    c = ws.cell(row=r, column=6, value=1.0)
    c.number_format, c.font = "0.0%", Font(bold=True)
    for col in range(1, 7):
        ws.cell(row=r, column=col).border = Border(top=THIN)
    r += 2
    ws.cell(row=r, column=1, value=("The book total is stated to the nearest NZD 0.5 million and the segments to NZD 0.1 "
                                    "million, each rounded from the unrounded NZD figure in column E.")).font = Font(size=9, color="555555")
    ws.cell(row=r + 1, column=1, value=("Excluded under CR-ST-02 1.3: %d customers in default at the book date (risk grade D), "
                                        "individually provisioned." % F["n_default"])).font = Font(size=9, color="555555")
    ws.freeze_panes = "A7"

    wb2 = wb.create_sheet("Borrowers")
    cols = ["Customer no", "Customer name", "NZBN", "Own division", "Reporting segment", "Risk grade", "12-month PD",
            "Trading credits, year to 30 Sep 2026 (NZD)", "Paid by other divisions", "Paid by households",
            "Own division's scenario change", "Sales change through payers", "Table 2 multiplier", "Stressed PD",
            "EAD (NZD)", "Stressed loss (NZD)"]
    _hdr(wb2, 1, cols, [12, 40, 15, 9, 34, 8, 9, 16, 10, 10, 11, 11, 10, 9, 14, 14])
    wb2.row_dimensions[1].height = 45
    for i, x in enumerate(F["rows"], start=2):
        vals = [x["cust"], x["name"], x["nzbn"], x["div"], x["seg"], x["grade"], x["pd12"], round(x["sales"], 2),
                x["other_share"], x["hh_share"], x["own_change"] / 100.0, x["change"] / 100.0, x["mult"], x["pds"],
                round(x["ead"], 2), round(x["loss"], 2)]
        fmts = [None, None, "@", None, None, "0", "0.00%", "#,##0", "0%", "0%", "0.0%", "0.0%", "0.00", "0.00%",
                "#,##0", "#,##0"]
        for j, (v, f) in enumerate(zip(vals, fmts), start=1):
            c = wb2.cell(row=i, column=j, value=v)
            if f:
                c.number_format = f
    last = len(F["rows"]) + 1
    wb2.cell(row=last + 1, column=2, value="Total").font = Font(bold=True)
    c = wb2.cell(row=last + 1, column=15, value="=SUM(O2:O%d)" % last)
    c.number_format, c.font = "#,##0", Font(bold=True)
    c = wb2.cell(row=last + 1, column=16, value="=SUM(P2:P%d)" % last)
    c.number_format, c.font = "#,##0", Font(bold=True)
    wb2.freeze_panes = "C2"
    wb2.auto_filter.ref = "A1:P%d" % last

    ws3 = wb.create_sheet("Net credit losses")
    ws3["A1"] = "Net credit losses, business banking book, financial year to 30 September 2026 (NZD thousand)"
    ws3["A1"].font = Font(bold=True, color=NAVY)
    ws3["A2"] = ("Amounts written off in the half less recoveries received in the half on loans already written off "
                 "(CR-ST-02 4.2). H1 is October 2025 to March 2026, H2 April to September 2026.")
    ws3["A2"].font = Font(italic=True, size=9, color="555555")
    _hdr(ws3, 4, ["Reporting segment", "H1 written off", "H1 recovered", "H1 net credit loss", "H2 written off",
                  "H2 recovered", "H2 net credit loss"], [44, 13, 13, 15, 13, 13, 15])
    ws3.row_dimensions[4].height = 30
    a = F["ask_a"]
    r = 5
    tot = [0.0] * 6
    for s in R.SEG_NAMES:
        ws3.cell(row=r, column=1, value=s)
        vals = [a["written_off"].get((s, "H1"), 0.0), a["recovered"][(s, "H1")], a["net"][(s, "H1")],
                a["written_off"].get((s, "H2"), 0.0), a["recovered"][(s, "H2")], a["net"][(s, "H2")]]
        for j, v in enumerate(vals):
            tot[j] += v
            ws3.cell(row=r, column=2 + j, value=R.rhu(v / 1e3, 0)).number_format = "#,##0"
        r += 1
    ws3.cell(row=r, column=1, value="Business banking book").font = Font(bold=True)
    for j, v in enumerate(tot):
        c = ws3.cell(row=r, column=2 + j, value=R.rhu(v / 1e3, 0))
        c.number_format, c.font = "#,##0", Font(bold=True)
        c.border = Border(top=THIN)
    ws3.cell(row=r + 2, column=1, value=("Recoveries include guarantors' payments on their own collection cases, credited to "
                                         "the company they guaranteed, and the collection agency's remittances net of its "
                                         "commission; rural and commercial property write-offs are reported under CR-ST-03 "
                                         "and CR-ST-04.")).font = Font(size=9, color="555555")
    ws3.freeze_panes = "B5"

    ws4 = wb.create_sheet("Default back-test")
    ws4["A1"] = "Business borrowers by risk-grade band at 30 September 2025 and defaults in the following twelve months"
    ws4["A1"].font = Font(bold=True, color=NAVY)
    ws4["A2"] = ("Grade in force at 30 September 2025 (model grade or approved override, CR-ST-02 Table 1). Defaults "
                 "1 October 2025 to 30 September 2026 in the business and rural default registers.")
    ws4["A2"].font = Font(italic=True, size=9, color="555555")
    _hdr(ws4, 4, ["Risk-grade band", "Business borrowers at 30 Sep 2025", "Defaulted in the year", "Default share"],
         [22, 18, 14, 13])
    ws4.row_dimensions[4].height = 30
    r = 5
    for k, lab in enumerate(R.BAND_LABEL):
        n, d = F["ask_b"][k]
        ws4.cell(row=r, column=1, value=lab)
        ws4.cell(row=r, column=2, value=n)
        ws4.cell(row=r, column=3, value=d)
        ws4.cell(row=r, column=4, value=F["ask_b_share"][k] / 100.0).number_format = "0.0%"
        r += 1
    nt = sum(n for n, d in F["ask_b"].values())
    dtot = sum(d for n, d in F["ask_b"].values())
    ws4.cell(row=r, column=1, value="All graded borrowers").font = Font(bold=True)
    ws4.cell(row=r, column=2, value=nt).font = Font(bold=True)
    ws4.cell(row=r, column=3, value=dtot).font = Font(bold=True)
    c = ws4.cell(row=r, column=4, value=R.rhu(100.0 * dtot / nt, 1) / 100.0)
    c.number_format, c.font = "0.0%", Font(bold=True)
    ws4.cell(row=r + 2, column=1, value=("A connected group's cross-default is recorded against the group lead's customer "
                                         "number; each defaulted facility is counted for the customer that holds it. Customer "
                                         "numbers retired in the March 2026 merge are read through to their 2025 number.")
             ).font = Font(size=9, color="555555")

    ws5 = wb.create_sheet("Notes")
    notes = [
        ("Book", "Business lending system extract at 30 September 2026; facilities of customers in risk grade D excluded (CR-ST-02 1.3)."),
        ("Exposure at default", "Drawn balance; overdrafts and revolving credit facilities add 50 per cent of the undrawn limit (CR-ST-02 3.4)."),
        ("Own division", "ANZSIC 2006 division from the borrower's BIC code on the NZBN extract of 12 October 2026; the lending book's blank and 1993-coded industry fields are not used."),
        ("Sales change", "Each borrower's trading credits in the year to 30 September 2026 by payer: firms and public bodies matched to the NZBN extract by legal or trading name take their own division's scenario change; card settlements, branch cash and payments from individuals take the borrower's own division's change. Own-account transfers, GST refunds, insurance claims, loan advances and credit interest are not sales."),
        ("Stressed PD", "Table 1 PD times the Table 2 multiplier for the borrower's sales fall, capped at 100 per cent; no fall keeps the Table 1 PD."),
        ("Stressed LGD", "Table 3 by the facility's security code."),
        ("Rounding", "Half up throughout. Book total to the nearest NZD 0.5 million, segments to NZD 0.1 million, net credit losses to the nearest NZD thousand, default shares to one decimal of a per cent."),
    ]
    ws5.column_dimensions["A"].width = 20
    ws5.column_dimensions["B"].width = 110
    ws5["A1"], ws5["B1"] = "Item", "Basis"
    ws5["A1"].font = ws5["B1"].font = Font(bold=True)
    for i, (k, v) in enumerate(notes, start=2):
        ws5.cell(row=i, column=1, value=k).alignment = Alignment(vertical="top")
        ws5.cell(row=i, column=2, value=v).alignment = Alignment(wrap_text=True, vertical="top")
    for w in (ws, ws3, ws4):
        w.sheet_view.showGridLines = False
    save_xlsx(wb, path, "ICAAP 2026 business banking stress", "Capital Management", "2026-10-16T02:40:00Z")


def chart_png(F):
    segs = R.SEG_NAMES
    vals = [F["seg_m1"][s] for s in segs]
    labels = ["Construction", "Manufacturing", "Trade and\nlogistics", "Hospitality,\nretail, leisure",
              "Business and\nproperty", "Health, education\nand personal"]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "svg.hashsalt": "task133"})
    fig, ax = plt.subplots(figsize=(6.6, 3.0), dpi=150)
    bars = ax.bar(range(len(segs)), vals, width=0.62, color="#2F5D8A", zorder=2)
    for b_, v in zip(bars, vals):
        ax.text(b_.get_x() + b_.get_width() / 2, v + 0.06, f"{v:.1f}", ha="center", va="bottom", fontsize=9, color="#222222")
    ax.set_xticks(range(len(segs)))
    ax.set_xticklabels(labels, fontsize=7.8)
    ax.set_ylabel("NZD million")
    ax.set_ylim(0, max(vals) * 1.22)
    ax.grid(axis="y", color="#DDDDDD", linewidth=0.6, zorder=0)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)
    share = (F["seg"]["Hospitality, retail and leisure"] + F["seg"]["Construction"]) / F["total"]
    ax.set_title("Hospitality and construction carry %s of the stressed loss (NZD million, year to 30 Sep 2027)"
                 % ("over half" if share > 0.5 else "almost half"), fontsize=9.5, loc="left", color="#1F3A5F")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _para(doc, text, bold=False, size=10.5, italic=False, space_after=6, color=None, align=None):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold, run.italic = bold, italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)
    p.paragraph_format.space_after = Pt(space_after)
    if align:
        p.alignment = align
    return p


def _tbl(doc, header, rows, widths=None, bold_last=False):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    for i, h in enumerate(header):
        cell = t.rows[0].cells[i]
        cell.text = h
        for r_ in cell.paragraphs[0].runs:
            r_.bold = True
            r_.font.size = Pt(9)
    for k, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = str(v)
            para = cells[i].paragraphs[0]
            if i > 0:
                para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            for r_ in para.runs:
                r_.font.size = Pt(9)
                if bold_last and k == len(rows) - 1:
                    r_.bold = True
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    return t


def paper(F, path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.2)
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    hp = sec.header.paragraphs[0]
    hp.text = "Orari Bank Limited | Board of Directors | 26 November 2026 | Item 6.2 | In confidence"
    hp.runs[0].font.size = Pt(8)
    fp = sec.footer.paragraphs[0]
    fp.text = "ICAAP 2026: business banking stress | Capital Management"
    fp.runs[0].font.size = Pt(8)

    _para(doc, "Board paper", size=9, color="555555", space_after=2)
    _para(doc, "The severe scenario costs the business book NZD %.1f million in the stress year" % F["total_half_m"],
          bold=True, size=15, color="1F3A5F", space_after=4)
    _para(doc, "From: Capital Management    Date: 16 October 2026    For: decision    Paper: BD-2026-11-06", size=9,
          color="555555", space_after=10)

    _para(doc, "Decision sought", bold=True, size=11)
    _para(doc, ("That the Board adopts NZD %.1f million as the business banking book's stressed credit loss for the year to "
                "30 September 2027 under the severe scenario it approved on 24 September 2026, for use in the ICAAP capital "
                "plan." % F["total_half_m"]))

    _para(doc, "The stress result", bold=True, size=11)
    seg = F["seg_m1"]
    _para(doc, ("The %d performing business borrowers carry exposure at default of NZD %.1f million. Under CR-ST-02 each "
                "borrower's probability of default is scaled by the Table 2 multiplier for the fall in its own sales, and a "
                "business's sales are what its customers pay it. The operating-account credits for the year to 30 September "
                "2026 show who those customers are: %d per cent of the book's trading credits came from firms and public "
                "bodies outside the borrower's own industry division. The severe scenario cuts construction sales by 27.4 per "
                "cent and accommodation and food services by 22.6 per cent, so the transport, wholesale, labour-hire and "
                "engineering firms those builders, hotels and tour operators pay take steep multipliers even though their own "
                "divisions fall far less.") % (F["n_perf"], F["ead_m1"], F["other_share_pct"]))
    _para(doc, ("Hospitality, retail and leisure carries the largest loss at NZD %.1f million, followed by construction at "
                "NZD %.1f million and trade and logistics at NZD %.1f million. Health, education and personal services, "
                "whose revenue is mostly household and public spending that the scenario holds up, contributes NZD %.1f "
                "million.") % (seg["Hospitality, retail and leisure"], seg["Construction"], seg["Trade and logistics"],
                                seg["Health, education and personal services"]))
    rows = [[s, f"{F['n_seg'][s]:,}", f"{F['ead_seg'][s] / 1e6:,.1f}", f"{seg[s]:.1f}"] for s in R.SEG_NAMES]
    rows.append(["Business banking book", f"{F['n_perf']:,}", f"{F['ead_m1']:,.1f}", f"{F['total_half_m']:.1f}"])
    _tbl(doc, ["Reporting segment", "Borrowers", "EAD (NZD m)", "Stressed loss (NZD m)"], rows, [7.6, 2.4, 2.8, 3.6],
         bold_last=True)
    _para(doc, ("Source: business lending book at 30 September 2026; operating-account credits October 2025 to September "
                "2026; NZBN extract 12 October 2026. Total to the nearest NZD 0.5 million, segments to NZD 0.1 million. "
                "Facilities of the %d customers in default at the book date are individually provisioned and outside the "
                "stress (CR-ST-02 1.3).") % F["n_default"], size=8, italic=True, color="555555", space_after=8)
    doc.add_picture(io.BytesIO(chart_png(F)), width=Cm(16))
    _para(doc, "Figure 1. Stressed credit loss by reporting segment (NZD million).", size=8, italic=True, color="555555")

    _para(doc, "Realised losses and grade performance in 2026", bold=True, size=11)
    a = F["ask_a_k"]
    tot1 = R.rhu(sum(F["ask_a"]["net"][(s, "H1")] for s in R.SEG_NAMES) / 1e3, 0)
    tot2 = R.rhu(sum(F["ask_a"]["net"][(s, "H2")] for s in R.SEG_NAMES) / 1e3, 0)
    _para(doc, ("Net credit losses on the business book were NZD %s thousand in the first half of the financial year and NZD "
                "%s thousand in the second, with construction and hospitality write-offs rising through the year.")
          % (f"{tot1:,.0f}", f"{tot2:,.0f}"))
    rows = [[s, f"{a[(s, 'H1')]:,.0f}", f"{a[(s, 'H2')]:,.0f}"] for s in R.SEG_NAMES]
    rows.append(["Business banking book", f"{tot1:,.0f}", f"{tot2:,.0f}"])
    _tbl(doc, ["Reporting segment", "H1 FY2026 (NZD 000)", "H2 FY2026 (NZD 000)"], rows, [8.4, 3.8, 3.8], bold_last=True)
    _para(doc, ("Amounts written off less recoveries received on loans already written off (CR-ST-02 4.2); recoveries "
                "include guarantors' payments and the collection agency's remittances net of commission."), size=8,
          italic=True, color="555555", space_after=8)
    _para(doc, ("Defaults in the year rose with risk grade, from %.1f per cent of borrowers graded 1 to 3 at 30 September "
                "2025 to %.1f per cent of those graded 7 to 9.") % (F["ask_b_share"][0], F["ask_b_share"][4]))
    rows = []
    for k, lab in enumerate(R.BAND_LABEL):
        n, d = F["ask_b"][k]
        rows.append([lab, f"{n}", f"{d}", f"{F['ask_b_share'][k]:.1f}"])
    _tbl(doc, ["Risk-grade band at 30 Sep 2025", "Borrowers", "Defaulted", "Default share (%)"], rows,
         [6.2, 3.0, 3.0, 3.6])
    _para(doc, ("Grade in force at 30 September 2025, overrides included; defaults from both the business and rural "
                "registers, cross-defaults counted for each member of the connected group."), size=8, italic=True,
          color="555555", space_after=8)

    _para(doc, "Basis of preparation", bold=True, size=11)
    _para(doc, ("Book date 30 September 2026; stress year to 30 September 2027; CR-ST-02 version 3.1. Stressed loss is the "
                "stressed PD times the Table 3 stressed LGD times exposure at default, summed over facilities. Detail by "
                "borrower is in orari_icaap_business_stress_2027.xlsx."), size=9.5)
    save_docx(doc, path, "ICAAP 2026: business banking stress", "Capital Management", "2026-10-16T03:05:00Z")


def write(tdir, out):
    os.makedirs(out, exist_ok=True)
    F = R.compute(tdir)
    workbook(F, os.path.join(out, XLSX))
    paper(F, os.path.join(out, DOCX))
    return F


if __name__ == "__main__":
    write(sys.argv[1], sys.argv[2])
