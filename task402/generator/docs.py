"""task402 documents: the commissioner's improvement plan (docx) and the provider's provisional monthly KPI report
(pdf). The plan files the WHAT in the commissioner's own voice; the report is correct for what it measures."""
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

import postprocess as PP
import world as W

FONT_DIR = "/usr/share/fonts/truetype/crosextra"

PLAN_TITLE = "Fenwold Talking Therapies: improvement plan 2026-27"
PLAN = [
    ("title", PLAN_TITLE),
    ("small", "NHS Fenwold Integrated Care Board, mental health commissioning. Contract FTT-2023-07, NHS Talking "
              "Therapies for anxiety and depression (steps 2 and 3); provider Fenwold Wellbeing Partnership. Version 2.0, "
              "issued 28 April 2026; supersedes version 1.1 of 10 March 2026. Owner: Jemma Fletcher, Mental Health "
              "Commissioning Manager."),
    ("h", "1. Purpose"),
    ("p", "The service's recovery rate on the national measure fell between 2024-25 and 2025-26. Five things changed in the service during "
          "2025-26, and each has a fix that could be bought in 2026-27. The contract's improvement fund for 2026-27 "
          "(GBP 186,000, non-recurrent) will be committed at the contract review in June 2026 to the fix for one of "
          "them: the change that cost the service the most recoveries in 2025-26. The provider's review paper names that "
          "change and its cost."),
    ("h", "2. The changes under review"),
    ("table", [["", "Change", "In place from", "What the fund would buy"],
               ["A", "Agency high-intensity therapists on 12-week assignments, renewed quarter by quarter, to clear the "
                     "step 3 waiting list", "May 2025", "Fixed-term high-intensity posts"],
               ["B", "Telephone as the first offer for step 2 guided self-help", "1 April 2025",
                "Video and face-to-face as standard"],
               ["C", "The step 3 waiting list", "", "An additional block of step 3 sessions"],
               ["D", "Digital CBT moved to a new platform", "1 July 2025", "A return to the previous platform"],
               ["E", "Stress management groups withdrawn", "1 September 2025", "The groups reinstated"]]),
    ("h", "3. How the fund is decided"),
    ("p", "3.1 The year is 2025-26: the referrals whose course ended between 1 April 2025 and 31 March 2026 inclusive, by "
          "discharge date, as held in the service's refreshed extract of 6 May 2026. The provisional monthly reports are "
          "superseded by that extract."),
    ("p", "3.2 Recoveries are counted on the national measure set out in the annex."),
    ("p", "3.3 A change's cost is the number of recoveries the year's referrals would have had without the change, less "
          "the number they had. What a referral would have had is read from the year's other referrals at the same step."),
    ("p", "3.4 A referral is at step 3 if any of its treatment appointments was with a high-intensity therapist, and at "
          "step 2 otherwise."),
    ("p", "3.5 The fund goes to the change with the largest cost in recoveries. Cost per patient reached is not used."),
    ("h", "4. Timetable"),
    ("p", "The provider's review paper is due with the integrated care board by 29 May 2026. The contract review meets on "
          "17 June 2026; the fund is released from 1 July 2026 against the plan the review agrees."),
    ("h", "Annex: the national recovery measure"),
    ("p", "A referral counts as a recovery when it finished a course of treatment (two or more attended treatment "
          "appointments), was at caseness at its first attended treatment appointment (PHQ-9 total of 10 or more, or "
          "GAD-7 total of 8 or more), and was below caseness at its last attended treatment appointment (PHQ-9 total of "
          "9 or less and GAD-7 total of 7 or less)."),
]


def plan_docx(out):
    from docx import Document
    from docx.shared import Pt, Cm
    d = Document()
    for s in d.sections:
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = s.bottom_margin = Cm(2.0)
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for kind, val in PLAN:
        if kind == "title":
            d.add_heading(val, level=0)
        elif kind == "h":
            d.add_heading(val, level=2)
        elif kind == "small":
            p = d.add_paragraph()
            run = p.add_run(val)
            run.font.size = Pt(9)
        elif kind == "p":
            d.add_paragraph(val)
        elif kind == "table":
            t = d.add_table(rows=len(val), cols=len(val[0]))
            t.style = "Table Grid"
            for i, row in enumerate(val):
                for j, cell in enumerate(row):
                    t.cell(i, j).text = cell
                    for para in t.cell(i, j).paragraphs:
                        for run in para.runs:
                            run.font.size = Pt(9)
                            run.bold = i == 0
    path = os.path.join(out, "improvement_plan_2026-27.docx")
    d.save(path)
    PP.normalize_ooxml(path, "Jemma Fletcher", "Jemma Fletcher", "2026-03-04T10:12:00Z", "2026-04-28T15:47:00Z",
                       company="NHS Fenwold Integrated Care Board")
    PP.scrub_docx(path, total_time=212, title=PLAN_TITLE, company="NHS Fenwold Integrated Care Board")
    return path


def _pdf(path, title, author, blocks, created, modified, producer="Microsoft\xae Word for Microsoft 365"):
    from reportlab import rl_config
    rl_config.invariant = 1
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    pdfmetrics.registerFont(TTFont("Carlito", os.path.join(FONT_DIR, "Carlito-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("Carlito-Bold", os.path.join(FONT_DIR, "Carlito-Bold.ttf")))
    rl_config.canvas_basefontname = "Carlito"
    st = ParagraphStyle("b", fontName="Carlito", fontSize=9.6, leading=12.6, spaceAfter=5)
    h1 = ParagraphStyle("h1", fontName="Carlito-Bold", fontSize=14, leading=17, spaceAfter=6)
    h2 = ParagraphStyle("h2", fontName="Carlito-Bold", fontSize=10.6, leading=13.5, spaceBefore=7, spaceAfter=4)
    sm = ParagraphStyle("s", fontName="Carlito", fontSize=8.2, leading=10.4, textColor=colors.HexColor("#444444"))
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title=title, author=author, subject="", creator="")
    flow = []
    for kind, val in blocks:
        if kind == "h1":
            flow.append(Paragraph(val, h1))
        elif kind == "h2":
            flow.append(Paragraph(val, h2))
        elif kind == "p":
            flow.append(Paragraph(val, st))
        elif kind == "small":
            flow.append(Paragraph(val, sm))
        elif kind == "sp":
            flow.append(Spacer(1, val))
        elif kind == "table":
            t = Table(val, hAlign="LEFT", repeatRows=1)
            t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Carlito", 8.2),
                                   ("FONT", (0, 0), (-1, 0), "Carlito-Bold", 8.2),
                                   ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#5b6b7a")),
                                   ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#9aa5b1")),
                                   ("ALIGN", (1, 1), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                   ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2), ("TOPPADDING", (0, 0), (-1, -1), 2.2)]))
            flow.append(t)

    def _meta(c, d):
        c.setProducer(producer)
        c.setCreator(producer)
    doc.build(flow, onFirstPage=_meta, onLaterPages=_meta)
    PP.normalize_pdf(path, created, modified)


def kpi_pdf(out, m, w, rng):
    """The provider's provisional monthly report for March 2026, issued 14 April 2026 on the data recorded by then:
    a discharge is on the system from the day it is recorded, which runs a few days to a few weeks behind it."""
    lag = rng.integers(0, 26, size=len(m))
    rec_on = pd.to_datetime(m.end) + pd.to_timedelta(lag, unit="D")
    cut = pd.Timestamp(2026, 4, 10)
    pm = m[(rec_on <= cut).values]
    rows = [["Month", "Referrals received", "Entered treatment", "Finished treatment", "At caseness",
             "Recovered", "Recovery rate"]]
    refs = w.referrals
    mon = pd.period_range("2025-04", "2026-03", freq="M")
    rr = pd.to_datetime(refs.received).dt.to_period("M").value_counts()
    ent = pd.to_datetime(m[m.n_treat_att >= 1].start).dt.to_period("M").value_counts()
    tot = [0, 0, 0, 0, 0]
    for p in mon:
        f = pm[(pd.to_datetime(pm.end).dt.to_period("M") == p) & pm.finished]
        fc = int(f.fc.sum())
        rc = int(f.rec.sum())
        vals = [int(rr.get(p, 0)), int(ent.get(p, 0)), len(f), fc, rc]
        tot = [a + b for a, b in zip(tot, vals)]
        rows.append([p.strftime("%b %Y")] + ["{:,}".format(v) for v in vals] + ["%.1f%%" % (100 * rc / max(1, fc))])
    rows.append(["2025-26 to date"] + ["{:,}".format(v) for v in tot] + ["%.1f%%" % (100 * tot[4] / max(1, tot[3]))])
    fy = pm[(pm.fy == 25) & pm.finished]
    sg = [["Staff group of the discharging clinician", "Finished treatment at caseness", "Recovered", "Recovery rate"]]
    for k, lab in (("employed", "Substantive"), ("agency", "Agency")):
        g = fy[(fy.step == 3) & (fy.disch_kind == k) & fy.fc]
        sg.append(["Step 3, " + lab.lower(), "{:,}".format(len(g)), "{:,}".format(int(g.rec.sum())),
                   "%.1f%%" % (100 * g.rec.mean())])
    g2 = fy[(fy.step == 2) & fy.fc]
    sg.append(["Step 2, all", "{:,}".format(len(g2)), "{:,}".format(int(g2.rec.sum())), "%.1f%%" % (100 * g2.rec.mean())])
    blocks = [("h1", "Fenwold Talking Therapies: monthly performance report, March 2026 (provisional)"),
              ("small", "Fenwold Wellbeing Partnership. Prepared by Hollie Smith, Performance and Information Analyst. "
                        "Issued 14 April 2026 from the clinical system as recorded on 10 April 2026. Provisional: the figures "
                        "are refreshed from the clinical system after the year end."),
              ("h2", "1. Activity and recovery by month, 2025-26"),
              ("p", "A referral is counted in the month it was received, entered treatment in the month of its first attended "
                    "treatment appointment, and finished treatment, at caseness and recovered in the month it was "
                    "discharged."),
              ("table", rows),
              ("sp", 6),
              ("h2", "2. Recovery by step and by staff group, 2025-26 to date"),
              ("table", sg),
              ("sp", 6),
              ("small", "Recovery rate: recovered as a share of referrals that finished treatment at caseness, on the national "
                        "measure. Staff group is taken from the clinician recorded on the referral's last appointment.")]
    path = os.path.join(out, "monthly_performance_report_2026-03_provisional.pdf")
    _pdf(path, "Monthly performance report, March 2026 (provisional)", "Hollie Smith", blocks,
         b"D:20260414093112+01'00'", b"D:20260414094806+01'00'")
    return path
