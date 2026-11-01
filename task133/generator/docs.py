"""Governing documents and the other organisation files: CR-ST-02 (DOCX), the board-approved severe scenario (XLSX),
the rural book's stress summary (PDF) and the business deposit listing (XLSX)."""
import datetime as dt
import os

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

import params as P
import taxonomy as T
from io_util import save_docx, save_xlsx

STANDARD = "CR-ST-02_ICAAP_stress_testing_business_banking_v3.1.docx"
SCENARIO = "ICAAP_2026_severe_scenario_board_approved.xlsx"
RURAL_PDF = "rural_book_stress_summary_ICAAP_2026.pdf"
DEPOSITS = "business_deposit_balances_2026-09-30.xlsx"

# The filed sentences the verifier reads back (positive controls and the WHAT)
S_SCOPE = ("1.2 The business banking book is every facility to a business customer held in the business lending "
           "system. The rural book and the commercial property book are stressed under CR-ST-03 and CR-ST-04.")
S_DEFAULT = ("1.3 A facility of a customer in default at the book date (risk grade D) carries an individually assessed "
             "provision and is outside this standard.")
S_YEAR = ("2.2 The stress year is the twelve months after the book date. For the 2026 ICAAP the book date is "
          "30 September 2026 and the stress year ends on 30 September 2027.")
S_FY = "2.3 The bank's financial year ends on 30 September; its halves end on 31 March and 30 September."
S_SCEN = ("2.1 The stress applies the severe scenario the Board approves for the year, which states for each ANZSIC "
          "2006 division the change in the division's sales in the stress year against the year to the book date.")
S_LOSS = ("3.1 The stressed loss of a facility is its stressed probability of default times its stressed loss given "
          "default times its exposure at default. The book's stressed loss is the sum over its facilities.")
S_PD = ("3.2 Table 1 gives the 12-month probability of default for each risk grade. A borrower's stressed probability "
        "of default is its 12-month probability of default times the multiplier in Table 2 for the fall in the "
        "borrower's own sales over the stress year under the scenario, and is at most 100 per cent. A borrower whose "
        "sales do not fall keeps its 12-month probability of default.")
S_GRADE = ("A borrower's risk grade is its model grade, or the override grade while an approved override is in force.")
S_LGD = "3.3 Table 3 gives the stressed loss given default for each security code held on a facility."
S_EAD = ("3.4 A revolving facility (a business overdraft or a revolving credit facility) is at its drawn balance plus "
         "50 per cent of its undrawn limit. Any other facility is at its drawn balance.")
S_SEG = ("4.1 The ICAAP paper to the Board reports the business book's stressed loss in total and by reporting "
         "segment. Table 4 assigns each ANZSIC 2006 division to a segment; a borrower's segment follows its own "
         "division on the NZBN register.")
S_NCL = ("4.2 Beside the stress, the paper reports the book's net credit losses for each half of the last financial year "
         "by segment: the amounts written off in the half less the recoveries the bank received in the half on loans "
         "already written off.")
S_BT = ("4.3 The paper also reports, for each risk-grade band at the previous book date, how many of the band's business "
        "borrowers defaulted in the following twelve months and that number as a share of the band's borrowers.")


def _p(doc, text, bold=False, size=10, align=None):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold = bold
    run.font.size = Pt(size)
    if align:
        para.alignment = align
    return para


def _table(doc, header, rows):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Table Grid"
    for i, h in enumerate(header):
        t.rows[0].cells[i].text = h
        for r in t.rows[0].cells[i].paragraphs[0].runs:
            r.bold = True
            r.font.size = Pt(9)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = str(v)
            for r in cells[i].paragraphs[0].runs:
                r.font.size = Pt(9)
    return t


def write_standard(out):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    _p(doc, "ORARI BANK LIMITED", bold=True, size=12)
    _p(doc, "Credit Risk Standard CR-ST-02: ICAAP Stress Testing - Business Banking", bold=True, size=12)
    _p(doc, "Version 3.1  |  Effective 1 July 2026  |  Owner: Head of Capital Management  |  "
            "Approved by the Board Risk Committee on 18 June 2026", size=9)
    _p(doc, "1. Purpose and scope", bold=True)
    _p(doc, "1.1 This standard sets how the business banking book is stressed for the bank's Internal Capital "
            "Adequacy Assessment Process (ICAAP), and what the ICAAP paper reports to the Board.")
    _p(doc, S_SCOPE)
    _p(doc, S_DEFAULT)
    _p(doc, "2. Scenario and stress year", bold=True)
    _p(doc, S_SCEN)
    _p(doc, S_YEAR)
    _p(doc, S_FY)
    _p(doc, "3. Expected credit loss in the stress year", bold=True)
    _p(doc, S_LOSS)
    _p(doc, S_PD)
    _p(doc, "Table 1. 12-month probability of default by risk grade", bold=True, size=9)
    _table(doc, ["Risk grade"] + [str(g) for g in range(1, 10)],
           [["PD (%)"] + [f"{P.GRADE_PD[g]:.2f}" for g in range(1, 10)]])
    _p(doc, S_GRADE, size=9)
    _p(doc, "Table 2. Multiplier on the 12-month probability of default", bold=True, size=9)
    rows = []
    for lo, hi, m in P.PD_BANDS:
        if hi > 100:
            rows.append([f"{lo:.0f} per cent or more", f"{m:.2f}"])
        elif lo == 0:
            rows.append([f"More than 0 and less than {hi:.0f} per cent", f"{m:.2f}"])
        else:
            rows.append([f"{lo:.0f} per cent or more and less than {hi:.0f} per cent", f"{m:.2f}"])
    _table(doc, ["Fall in the borrower's sales over the stress year", "Multiplier"], rows)
    _p(doc, S_LGD)
    _p(doc, "Table 3. Stressed loss given default by security code", bold=True, size=9)
    _table(doc, ["Security code", "Security held", "Stressed LGD (%)"],
           [[k, P.SECURITY_TEXT[k], f"{v * 100:.0f}"] for k, v in P.LGD.items()])
    _p(doc, S_EAD)
    _p(doc, "4. Reporting to the Board", bold=True)
    _p(doc, S_SEG)
    _p(doc, "Table 4. Reporting segments", bold=True, size=9)
    _table(doc, ["Segment", "ANZSIC 2006 divisions"],
           [[s, ", ".join(f"{d} {P.DIVISIONS[d]}" for d in ds)] for s, ds in P.SEGMENTS])
    _p(doc, S_NCL)
    _p(doc, S_BT)
    _p(doc, "5. Document history", bold=True)
    _table(doc, ["Version", "Date", "Change"], [
        ["2.4", "July 2024", "Stressed LGDs reset after the security valuation review."],
        ["3.0", "July 2025", "Probability of default stressed by the fall in the borrower's sales (Table 2) in place "
                             "of a single book-wide multiplier."],
        ["3.1", "June 2026", "Table 2 bands recalibrated on the 2019 to 2025 default experience; revolving facilities at "
                             "50 per cent of the undrawn limit."],
    ])
    path = os.path.join(out, STANDARD)
    save_docx(doc, path, "CR-ST-02 ICAAP Stress Testing - Business Banking", "Julie Dawick", "2026-06-11T03:20:00Z")
    return path


def write_scenario(out):
    wb = Workbook()
    ws = wb.active
    ws.title = "Industry sales"
    ws.append(["Orari Bank Limited - ICAAP 2026 severe scenario"])
    ws.append(["Approved by the Board on 24 September 2026 (paper BD-2026-09-07). Prepared by Economics."])
    ws.append([])
    ws.append(["ANZSIC 2006 division", "Division", "Sales, year to 30 September 2026 (NZD million, South Island)",
               "Change in sales, stress year to 30 September 2027 (%)"])
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    for d, name in P.DIVISIONS.items():
        ws.append([d, name, T.BASE_SALES[d], P.SCENARIO_CHANGE[d]])
    ws.column_dimensions["B"].width = 44
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 22
    ws2 = wb.create_sheet("Macroeconomic paths")
    ws2.append(["Quarter", "Real GDP, annual change (%)", "Unemployment rate (%)", "Official Cash Rate (%)",
                "CPI, annual change (%)", "House prices, annual change (%)", "International visitor arrivals, annual change (%)"])
    for c in ws2[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    path_rows = [("Sep 2026", 1.4, 4.9, 3.00, 2.6, 1.8, 7.2), ("Dec 2026", -0.9, 5.6, 2.50, 2.2, -4.1, -14.0),
                 ("Mar 2027", -3.2, 6.6, 1.75, 1.6, -9.6, -31.5), ("Jun 2027", -4.6, 7.5, 1.25, 1.1, -14.2, -37.8),
                 ("Sep 2027", -4.1, 7.9, 1.00, 0.9, -16.9, -33.0)]
    for r in path_rows:
        ws2.append(list(r))
    save_xlsx(wb, os.path.join(out, SCENARIO), "ICAAP 2026 severe scenario", "Wendy Russell", "2026-09-25T00:35:00Z")


def write_rural_pdf(out):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    path = os.path.join(out, RURAL_PDF)
    c = canvas.Canvas(path, pagesize=A4, invariant=1)
    c.setTitle("Rural book stress summary - ICAAP 2026")
    c.setAuthor("Orari Bank Limited, Rural Banking")
    c.setCreator("Orari Bank Limited")
    c.setProducer("Orari Bank Limited")
    w, h = A4
    y = h - 60
    lines = [("Helvetica-Bold", 12, "Orari Bank Limited - Rural book stress summary, ICAAP 2026 (CR-ST-03)"),
             ("Helvetica", 9, "Book date 30 September 2026. Severe scenario approved 24 September 2026."),
             ("Helvetica", 9, "Dairy payout NZD 6.10/kg MS in the stress year; farm land values down 22 per cent."),
             ("Helvetica-Bold", 10, "Stressed loss by rural sector (NZD million)"),
             ("Helvetica", 9, "Dairy farming                       14.8"),
             ("Helvetica", 9, "Sheep and beef farming               3.1"),
             ("Helvetica", 9, "Horticulture and viticulture         1.6"),
             ("Helvetica", 9, "Rural contractors and services       0.9"),
             ("Helvetica", 9, "Rural book total                    20.4"),
             ("Helvetica", 8, "Prepared by Rural Credit Risk, 9 October 2026. For the ICAAP paper to the Board, November 2026.")]
    for font, size, text in lines:
        c.setFont(font, size)
        c.drawString(56, y, text)
        y -= 18 if size >= 10 else 15
    c.showPage()
    c.save()
    return path


def write_deposits(W, out):
    rng = np.random.default_rng(P.SEED + 404)
    wb = Workbook()
    ws = wb.active
    ws.title = "Balances"
    ws.append(["Customer No", "Account No", "Account Type", "Balance 30/09/2026 (NZD)", "Interest Rate (%)"])
    for c in ws[1]:
        c.font = Font(bold=True)
    rows = []
    for b in W.borrowers:
        rows.append([b["cust"], b["acct"], "Business Cheque", round(float(np.exp(rng.normal(np.log(b["sales"] * 0.035), 0.6))), 2), 0.0])
        if rng.random() < 0.4:
            rows.append([b["cust"], b["acct"][:-2] + "25", "Business Saver", round(float(np.exp(rng.normal(np.log(b["sales"] * 0.02), 0.8))), 2),
                         round(float(rng.choice([2.10, 2.35, 2.60])), 2)])
    rows.sort(key=lambda r: r[1])
    for r in rows:
        ws.append(r)
    save_xlsx(wb, os.path.join(out, DEPOSITS), "Business deposit balances", "Keanu Boyd", "2026-10-06T19:02:00Z")
