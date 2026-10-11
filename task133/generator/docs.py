"""Bellbird's documents: the ECL methodology, the scorecard migration note, the scenario workbook, the dictionary."""
import datetime as dt
import os
import shutil
import subprocess
import tempfile

import docx
import openpyxl
from docx.shared import Cm, Pt
from openpyxl.styles import Font, PatternFill

import world as W


def _doc(author, title, created, font="Calibri"):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = font
    st.font.size = Pt(10.5)
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = Cm(1.8)
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.created = created
    cp.modified = created
    cp.revision = 6
    cp.comments = cp.keywords = cp.subject = cp.category = ""
    return d


def _p(d, text, bold=False, size=None, after=4, italic=False):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.bold, r.italic = bold, italic
    if size:
        r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(after)
    return p


def methodology_docx(path):
    d = _doc("Matthew Gardner", "CRM-ECL-04 Expected credit loss: personal loans", dt.datetime(2026, 5, 12, 10, 40))
    _p(d, "Bellbird Personal Finance Ltd  |  Credit Risk Management", size=8.5, italic=True)
    _p(d, "CRM-ECL-04  Expected credit loss: unsecured personal loans (collective model)", bold=True, size=14, after=2)
    _p(d, "Version 4.1, effective for reporting dates from 30 June 2026. Owner: Credit Risk Modelling. Approved by the "
          "Audit and Risk Committee on 26 May 2026.", size=9, after=10)
    sections = [
        ("1. Scope",
         ["This method sets the collective expected credit loss (ECL) allowance under AASB 9 for PL36 and PL60 unsecured "
          "personal loans in stages 1 and 2. Loans in stage 3 (90 or more days past due) are assessed under CRM-ECL-06 "
          "and are outside this method."]),
        ("2. Staging",
         ["2.1 A loan is in stage 2 if, at the reporting date, any of the following holds: it is 30 or more days past "
          "due; a hardship arrangement is in force; or its current behaviour score is 60 or more points below its score "
          "at origination, both on the current (v4) scorecard. Otherwise it is in stage 1.",
          "2.2 A hardship arrangement is in force if the reporting date falls on or between its start and end dates and "
          "it was not cancelled.",
          "2.3 Origination scores recorded on the v3 scorecard are converted to v4 with the published migration formula "
          "before the comparison in 2.1."]),
        ("3. Expected credit loss",
         ["3.1 ECL = sum over future months k of PD(k) x LGD x EAD(k) x DF(k). Stage 1 loans use the next 12 months or "
          "the remaining term if shorter; stage 2 loans use the remaining term.",
          "3.2 PD(k), the probability of default in the k-th month after the reporting date, comes from the model team's "
          "cumulative default curve for the loan's product. Stage 2 loans carry the significant-increase scalar of 2.4 on "
          "PD(k). A loan's remaining term is its contractual term less the number of monthly repayments that have fallen "
          "due on or before the reporting date.",
          "3.3 LGD is 70 per cent for PL36 and 76 per cent for PL60.",
          "3.4 EAD(k) is the balance outstanding at the start of month k when the current balance is repaid over the "
          "remaining term in equal monthly instalments at the contract rate.",
          "3.5 DF(k) discounts month k at the contract rate: (1 + contract rate / 12) to the power -k."]),
        ("4. Forward-looking information",
         ["Each scenario in the quarter's approved scenario workbook scales PD(k) by its multiplier. The allowance is "
          "the probability-weighted sum of the scenario ECLs."]),
        ("5. Reporting",
         ["The allowance is reported to the Audit and Risk Committee in Australian dollars by stage and product, with "
          "the coverage ratio (allowance over gross carrying amount, the sum of current balances) for each."]),
    ]
    for head, paras in sections:
        _p(d, head, bold=True, size=11, after=3)
        for t in paras:
            _p(d, t, after=5)
    _p(d, "Changes in 4.1: hardship arrangements added to the stage 2 triggers; LGD for PL60 raised from 74 to 76 per cent.",
       size=8.5, italic=True, after=0)
    d.save(path)


def scorecard_pdf(path):
    d = _doc("Credit Risk Modelling", "Behaviour scorecard v4: migration note", dt.datetime(2024, 6, 20, 15, 0), font="Arial")
    _p(d, "Bellbird Personal Finance  ·  Credit Risk Modelling", size=8, italic=True)
    _p(d, "Behaviour and application scorecard v4: migration note", bold=True, size=13, after=6)
    _p(d, "20 June 2024", after=8)
    body = [
        "From 1 July 2024 all application and behaviour scores are produced on scorecard v4. Scores recorded before that "
        "date are on v3 and are not restated in the loan system.",
        "v4 is a recalibration of v3 on the same characteristics with a wider points scale. Where a v3 score must be "
        "compared with a v4 score, convert it as v4 = 1.12 x v3 - 18, rounded to the nearest whole point.",
        "Worked example: a v3 origination score of 615 converts to 1.12 x 615 - 18 = 670.8, which is 671 on v4.",
        "The cut-offs used in credit decisioning were re-set on v4 at the same approval rate and are listed in the "
        "credit policy, not here.",
    ]
    for t in body:
        _p(d, t, after=6)
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "note.docx")
    d.save(src)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.move(os.path.join(tmp, "note.pdf"), path)
    shutil.rmtree(tmp)


def scenarios_xlsx(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Q3 FY27 scenarios"
    ws.append(["IFRS 9 / AASB 9 forward-looking scenarios, reporting date 30 September 2026"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Approved by the Audit and Risk Committee, 18 September 2026"])
    ws.append([])
    ws.append(["Scenario", "Probability weight", "PD multiplier", "Unemployment rate, peak (%)", "Cash rate, end FY27 (%)"])
    for j in range(1, 6):
        ws.cell(row=4, column=j).font = Font(bold=True)
        ws.cell(row=4, column=j).fill = PatternFill("solid", fgColor="E5E9F0")
    macro = {"Base": (4.4, 3.35), "Downside": (6.1, 2.60), "Upside": (3.9, 3.60)}
    for name, w, m in W.SCENARIOS:
        ws.append([name, w, m, macro[name][0], macro[name][1]])
    for col, wd in zip("ABCDE", [14, 18, 14, 26, 22]):
        ws.column_dimensions[col].width = wd
    ws2 = wb.create_sheet("Q4 FY26 (prior)")
    ws2.append(["Scenarios used at 30 June 2026"])
    ws2.append([])
    ws2.append(["Scenario", "Probability weight", "PD multiplier"])
    for name, w, m in [("Base", 0.60, 1.00), ("Downside", 0.25, 1.25), ("Upside", 0.15, 0.85)]:
        ws2.append([name, w, m])
    wb.save(path)


def dictionary_txt(path):
    txt = """BELLBIRD PERSONAL FINANCE - LOAN SYSTEM EXTRACTS FOR THE QUARTER-END ECL RUN
Extracted 1 October 2026 07:30 (job ECL_QE_BOOK)

personal_loan_book_2026-09-30.csv: every loan open in the loan system at close of business 30 September 2026,
including loans in arrears that have not yet been written off (write-off at 180 days past due).
  loan_no                  loan number
  product                  PL36 (36-month term) or PL60 (60-month term)
  risk_grade               application risk grade, A (lowest risk) to E
  drawdown_date            date the loan was funded
  first_repayment_date     first monthly repayment due date; later repayments fall due on the same day each month
  term_months              contractual term
  contract_rate            fixed annual contract rate (decimal)
  original_amount          amount funded (AUD)
  current_balance          principal outstanding at close of business on the reporting date (AUD)
  days_past_due            days the oldest unpaid instalment is overdue
  origination_score        application score at origination, on the scorecard named in origination_scorecard
  origination_scorecard    v3 (loans funded before 1 July 2024) or v4
  current_score_v4         behaviour score at the reporting date, scorecard v4
  state, channel           customer state and origination channel

hardship_register_2026-09-30.xlsx: hardship arrangements recorded since 2019, one row per arrangement.

pd_curve_personal_loans_2026-06.csv: model output from Credit Risk Modelling, one row per product and month on book.
  cumulative_pd            probability that a new loan defaults (90 days past due) by the end of that month on book

pd_model_development_sample.parquet: loans funded October 2019 to September 2023 with their outcome to June 2026,
used to develop the curve.
"""
    open(path, "w").write(txt)
