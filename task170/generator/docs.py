"""task170 documents: the plan rules, the 2027 amendment and the pay scales. Their text is kept here as data so
checks.py and verify.py can quote it."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                        # noqa: E402
from reportlab.lib.pagesizes import A4                                                  # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                         # noqa: E402
from reportlab.lib.units import mm                                                      # noqa: E402
from reportlab.pdfbase import pdfmetrics                                                # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                            # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as C          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf"),
               ("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1f24")
GREY = colors.HexColor("#5a6068")
ACCENT = colors.HexColor("#163f6b")
RULE = colors.HexColor("#b7c2cf")
HEAD = colors.HexColor("#e3eaf2")

F_RULES = "vch_savings_plan_rules_2024.pdf"
F_AMEND = "vch_savings_plan_amendment_2027.docx"
F_SCALE = "vch_pay_scales_2026_2027.pdf"
RULES_DATE = dt.date(2024, 2, 6)
AMEND_DATE = dt.date(2026, 9, 22)
SCALE_DATE = dt.date(2026, 6, 18)


def styles(font="LibSans", bold="LibSans-Bold", size=9.6):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.34, textColor=INK, spaceAfter=4),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=13.5, leading=17.0, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=8.6, leading=11.0, textColor=GREY, spaceAfter=8),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=10.2, leading=13.0, textColor=ACCENT, spaceBefore=5,
                          spaceAfter=2.5),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.4, leading=10.2, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=8.4, leading=10.2, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.4, leading=10.2, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=7.8, leading=10.0, textColor=GREY, spaceAfter=3))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=19 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="LibSans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.4)
        canvas.setFillColor(GREY)
        canvas.drawString(22 * mm, 9.5 * mm, left)
        canvas.drawRightString(A4[0] - 22 * mm, 9.5 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _table(st, head, rows, widths, right=()):
    data = [[Paragraph(esc(h), st["cellb"]) for h in head]]
    for r in rows:
        data.append([Paragraph(esc(str(x)), st["cellr"] if i in right else st["cell"]) for i, x in enumerate(r)])
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.0), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.0),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def pdf_stamp(d, hh=9, mi=0):
    return ("D:%04d%02d%02d%02d%02d00+01'00'" % (d.year, d.month, d.day, hh, mi)).encode()


# ---------------------------------------------------------------------------------------------------- plan rules (pdf)
RULES_TITLE = "VCH Supplementary Savings Plan: plan rules (consolidated February 2024)"
RULES = [
    ("1. Who may join", [
        "Every employee of Vindeholm County Hospitals may join the plan from the first day of employment. Membership "
        "is voluntary: an employee joins by electing a contribution rate in the HR portal, and nobody is enrolled "
        "without an election.",
    ]),
    ("2. Contributions", [
        "A member contributes a whole percentage of basic pay from 1 to 10 per cent. Basic pay is the monthly salary "
        "for the member's grade and contracted hours on the pay scale in force, across every post the member holds "
        "with the employer, including bank posts. Overtime, allowances and arrears of other pay are not pensionable.",
        "A member may change the rate, or stop contributing, at any time in the HR portal.",
    ]),
    ("3. Timing", [
        "Salaries are paid monthly on the 25th, or the working day before when the 25th falls on a weekend. An "
        "election or a change received by the 10th of a month applies to that month's payroll; one received later "
        "applies to the next month's.",
    ]),
    ("4. The employer's match", [
        "For every month a member contributes, the employer pays into the member's account 100 per cent of the "
        "member's contribution up to 3 per cent of basic pay and 50 per cent of the contribution between 3 and 6 per "
        "cent of basic pay. Contributions above 6 per cent are not matched. The match is paid through the same "
        "payroll as the contribution.",
    ]),
    ("5. Leaving and rejoining", [
        "Membership ends when employment ends; the account stays invested as a deferred account until the member "
        "transfers or draws it. A former employee who is rehired may join again by making a new election, which opens "
        "a new membership under the same member number.",
    ]),
    ("6. Administration", [
        "Ledstrand Pension Administration keeps the member register and the accounts on the employer's behalf from the "
        "monthly contribution file payroll sends after each payroll.",
    ]),
]


def write_rules(out):
    st = styles()
    path = out + "/" + F_RULES
    doc = _doc(path, RULES_TITLE, C.ORG)
    flow = [Paragraph(esc(RULES_TITLE), st["h1"]),
            Paragraph("Vindeholm County Hospitals, HR and Reward. Consolidated text of 6 February 2024, replacing the "
                      "rules of 2012 as amended in 2017 and 2021.", st["sub"])]
    for head, paras in RULES:
        flow.append(Paragraph(esc(head), st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    flow.append(Spacer(1, 6))
    flow.append(Paragraph("Worked example. A member on a basic pay of TNK 30,000 a month contributing 5 per cent pays "
                          "TNK 1,500; the employer pays TNK 900 on the first 3 per cent and TNK 300 on the next 2, a "
                          "match of TNK 1,200.", st["small"]))
    doc.build(flow, onFirstPage=_footer("VCH Supplementary Savings Plan rules, February 2024"),
              onLaterPages=_footer("VCH Supplementary Savings Plan rules, February 2024"))
    PP.normalize_pdf(path, pdf_stamp(RULES_DATE, 14, 22), pdf_stamp(RULES_DATE, 14, 22))


# ---------------------------------------------------------------------------------------------------- pay scales (pdf)
SCALE_TITLE = "Pay scales 2026 and 2027: monthly basic salary by grade"


def write_scales(out):
    st = styles()
    path = out + "/" + F_SCALE
    doc = _doc(path, SCALE_TITLE, C.ORG)
    flow = [Paragraph(esc(SCALE_TITLE), st["h1"]),
            Paragraph("Extract from the collective agreement between Vindeholm County Council and the health sector "
                      "unions, signed 16 June 2026. Full-time monthly basic salary in TNK; part-time posts are paid "
                      "pro rata to contracted hours.", st["sub"])]
    rows = [[g, "{:,}".format(C.SCALE_2026[g]), "{:,}".format(C.SCALE_2027[g])] for g in C.GRADES]
    flow.append(_table(st, ["Grade", "From 1 January 2026", "From 1 January 2027"], rows, [30, 45, 45], right=(1, 2)))
    flow.append(Spacer(1, 6))
    for p in ["The 2027 scale applies to every payroll from January to December 2027. No further award falls in 2027.",
              "Bank posts are paid at the grade of the post on the same scale."]:
        flow.append(Paragraph(esc(p), st["body"]))
    doc.build(flow, onFirstPage=_footer("Collective agreement 2026 to 2027, pay scale extract"),
              onLaterPages=_footer("Collective agreement 2026 to 2027, pay scale extract"))
    PP.normalize_pdf(path, pdf_stamp(SCALE_DATE, 10, 5), pdf_stamp(SCALE_DATE, 10, 5))


# ---------------------------------------------------------------------------------------------------- amendment (docx)
AMEND_TITLE = "VCH Supplementary Savings Plan: automatic enrolment of new hires from 1 January 2027"
AMEND = [
    ("1. Decision", "The county council's employment committee approved on 15 September 2026 that new hires are "
     "enrolled in the plan automatically from 1 January 2027. The plan rules of February 2024 apply unchanged except "
     "as set out here."),
    ("2. Who is enrolled", "Every employee whose employment starts on or after 1 January 2027 is enrolled, including "
     "a former employee rehired from that date. Staff whose employment started before 1 January 2027 are not "
     "enrolled; their elections stand as they are."),
    ("3. How enrolment works", "A new hire is enrolled at a contribution of 3 per cent of basic pay from the first "
     "payroll of the employment, and the employer's match applies as for every member (rules, section 4). The new "
     "hire may at any time choose another rate from 1 to 10 per cent, or opt out, in the HR portal; the choice applies "
     "from the payroll the rules' timing gives it (section 3). Opting out stops contributions from that payroll; "
     "contributions already paid stay in the account and are not refunded."),
    ("4. Budget", "Finance's FY2027 budget (the January to December 2027 payrolls) carries the employer's match on the "
     "2027 intake as a line of its own, by hospital. The intake is the approved requisitions in the 2027 hiring plan, "
     "each filled at its planned start date and paid at the 2027 pay scale for its grade and FTE. The line is "
     "forecast from the experience of the group's hires since January 2019, all six hospitals taken together, and "
     "counts nobody hired before 2027. The committee reviews the line before it signs off the FY2027 pay budget in "
     "December 2026."),
    ("5. Communication", "Each new hire receives the enrolment notice with the contract and a reminder in the induction "
     "pack. Payroll services sets up the default deduction at onboarding."),
]


def write_amendment(out):
    from docx import Document
    from docx.shared import Pt
    path = out + "/" + F_AMEND
    d = Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading(AMEND_TITLE, level=1)
    d.add_paragraph("HR and Reward, Vindeholm County Hospitals. Committee paper as approved, 22 September 2026. "
                    "Contact: %s, reward and pensions." % C.PEOPLE["me"])
    for head, para in AMEND:
        d.add_heading(head, level=2)
        d.add_paragraph(para)
    d.core_properties.title = AMEND_TITLE
    d.save(path)
    PP.normalize_docx(path, C.PEOPLE["me"], C.PEOPLE["me"], "2026-08-27T07:12:00Z", "2026-09-22T13:41:00Z", 9, 268,
                      seed=C.SEED, title=AMEND_TITLE, company=C.ORG)
