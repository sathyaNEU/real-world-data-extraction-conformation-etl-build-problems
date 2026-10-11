"""The pack's documents, each in its own organisation's voice: the services agreement excerpt (recitals, signature
page and Schedule C), the consulting actuary's renewal letter, the stop-loss policy schedule, Northcourt's
implementation and outreach plan, Northcourt's three stratification exports, Quarrystone's rebate statement and the
benefits office's warehouse readme.

Each PDF is written as a Word document and converted by LibreOffice (containers.soffice_pdf); each workbook is
written by openpyxl and repacked the way Excel saves it (containers.repack)."""
import datetime as dt
import html
import os
import shutil
import tempfile

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import containers as C
import world as W
from providers import u01 as C_u01


def money(x, cents=False):
    return ("$%s" % format(x, ",.2f")) if cents else ("$%s" % format(int(round(x)), ","))


def local(*a):
    d = dt.datetime(*a)
    return d.replace(tzinfo=C.central(d))


# ------------------------------------------------------------------ Word documents for the PDFs
class Doc:
    """a Word document in one organisation's house style"""

    def __init__(self, font, size, margins=(1.0, 1.0, 0.9, 0.8)):
        self.d = Document()
        sec = self.d.sections[0]
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        sec.left_margin, sec.right_margin = Inches(margins[0]), Inches(margins[1])
        sec.top_margin, sec.bottom_margin = Inches(margins[2]), Inches(margins[3])
        st = self.d.styles["Normal"]
        st.font.name = font
        st.element.rPr.rFonts.set(qn("w:eastAsia"), font)
        st.element.rPr.rFonts.set(qn("w:hAnsi"), font)
        st.element.rPr.rFonts.set(qn("w:cs"), font)
        st.font.size = Pt(size)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.line_spacing = 1.08
        self.font, self.size = font, size

    def p(self, text="", bold=False, italic=False, size=None, align=None, after=None, before=None, indent=None,
          hanging=None, color=None, keep=False, newpage=False):
        para = self.d.add_paragraph()
        if newpage:
            para.paragraph_format.page_break_before = True
        if text:
            self.runs(para, text, bold, italic, size, color)
        pf = para.paragraph_format
        if align == "center":
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif align == "right":
            para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif align == "justify":
            para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if after is not None:
            pf.space_after = Pt(after)
        if before is not None:
            pf.space_before = Pt(before)
        if indent is not None:
            pf.left_indent = Inches(indent)
        if hanging is not None:
            pf.first_line_indent = Inches(-hanging)
        if keep:
            pf.keep_with_next = True
        return para

    def runs(self, para, text, bold=False, italic=False, size=None, color=None):
        """text with **bold** spans"""
        parts = text.split("**")
        for i, t in enumerate(parts):
            if not t:
                continue
            r = para.add_run(t)
            r.bold = bold or (i % 2 == 1)
            r.italic = italic
            if size:
                r.font.size = Pt(size)
            if color:
                r.font.color.rgb = RGBColor.from_string(color)
        return para

    def page_break(self):
        self.d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def table(self, rows, widths, header=True, size=None, bold_first_col=False, align_right_from=None, grid=True,
              shade=None):
        t = self.d.add_table(rows=len(rows), cols=len(rows[0]))
        t.alignment = WD_TABLE_ALIGNMENT.LEFT
        t.autofit = False
        tbl = t._tbl
        tblPr = tbl.tblPr
        if grid:
            borders = OxmlElement("w:tblBorders")
            for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
                el = OxmlElement("w:" + edge)
                el.set(qn("w:val"), "single")
                el.set(qn("w:sz"), "4")
                el.set(qn("w:space"), "0")
                el.set(qn("w:color"), "8C8C8C")
                borders.append(el)
            tblPr.append(borders)
        for gc, w in zip(tbl.tblGrid.findall(qn("w:gridCol")), widths):
            gc.set(qn("w:w"), str(int(w * 1440)))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                cell = t.rows[i].cells[j]
                cell.width = Inches(widths[j])
                para = cell.paragraphs[0]
                para.paragraph_format.space_after = Pt(1)
                para.paragraph_format.space_before = Pt(1)
                if align_right_from is not None and j >= align_right_from and (i > 0 or not header):
                    para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                self.runs(para, str(val), bold=(header and i == 0) or (bold_first_col and j == 0), size=size)
                if shade and header and i == 0:
                    tcPr = cell._tc.get_or_add_tcPr()
                    shd = OxmlElement("w:shd")
                    shd.set(qn("w:val"), "clear")
                    shd.set(qn("w:color"), "auto")
                    shd.set(qn("w:fill"), shade)
                    tcPr.append(shd)
        self.d.add_paragraph().paragraph_format.space_after = Pt(2)
        return t

    def _field(self, para, instr, size):
        r = para.add_run()
        r.font.size = Pt(size)
        b = OxmlElement("w:fldChar")
        b.set(qn("w:fldCharType"), "begin")
        r._r.append(b)
        r2 = para.add_run()
        r2.font.size = Pt(size)
        it = OxmlElement("w:instrText")
        it.set(qn("xml:space"), "preserve")
        it.text = " %s " % instr
        r2._r.append(it)
        r3 = para.add_run()
        r3.font.size = Pt(size)
        e = OxmlElement("w:fldChar")
        e.set(qn("w:fldCharType"), "end")
        r3._r.append(e)

    def footer(self, left, page_fmt="Page {PAGE} of {NUMPAGES}", size=8):
        f = self.d.sections[0].footer
        para = f.paragraphs[0]
        tab = OxmlElement("w:tabs")
        t = OxmlElement("w:tab")
        t.set(qn("w:val"), "right")
        sec = self.d.sections[0]
        t.set(qn("w:pos"), str(int((sec.page_width - sec.left_margin - sec.right_margin) / 635)))
        tab.append(t)
        para._p.get_or_add_pPr().append(tab)
        r = para.add_run(left + "\t")
        r.font.size = Pt(size)
        rest = page_fmt
        while rest:
            i = rest.find("{")
            if i < 0:
                para.add_run(rest).font.size = Pt(size)
                break
            if i:
                para.add_run(rest[:i]).font.size = Pt(size)
            j = rest.index("}")
            self._field(para, rest[i + 1:j], size)
            rest = rest[j + 1:]

    def header_lines(self, lines, align="left"):
        h = self.d.sections[0].header
        first = True
        for text, bold, size, color in lines:
            para = h.paragraphs[0] if first else h.add_paragraph()
            first = False
            para.paragraph_format.space_after = Pt(0)
            if align == "right":
                para.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            r = para.add_run(text)
            r.bold = bold
            r.font.size = Pt(size)
            if color:
                r.font.color.rgb = RGBColor.from_string(color)

    def save_pdf(self, path, title, author, when):
        self.d.core_properties.title = title
        self.d.core_properties.author = author
        self.d.core_properties.last_modified_by = author
        self.d.core_properties.created = when.replace(tzinfo=None)
        self.d.core_properties.modified = when.replace(tzinfo=None)
        self.d.core_properties.revision = 1
        work = tempfile.mkdtemp(prefix="doc-")
        try:
            src = os.path.join(work, os.path.splitext(os.path.basename(path))[0] + ".docx")
            self.d.save(src)
            C.soffice_pdf(src, path, when)
        finally:
            shutil.rmtree(work, ignore_errors=True)


# ------------------------------------------------------------------ the agreement excerpt
def agreement_pdf(path):
    D = Doc("Times New Roman", 11, margins=(1.0, 1.0, 0.9, 0.85))
    D.footer("Agreement No. RCV-2027-014")
    D.p("CARE MANAGEMENT SERVICES AGREEMENT", bold=True, size=13, align="center", after=4)
    D.p("between Independent School District No. 2817 (Red Cedar Valley Schools), Minnesota,", align="center", after=0)
    D.p("and Northcourt Care Partners, LLC", align="center", after=2)
    D.p("Agreement No. RCV-2027-014", align="center", after=10)
    D.p("Conformed copy for the District's benefits file: Recitals, signature page and Schedule C. The signed original, "
        "the body of the Agreement and Schedules A (Services), B (Administrative Fees), D (Data Exchange) and E (Business "
        "Associate Agreement) are held by the Business Office.", italic=True, size=9.5, after=10)
    D.p("RECITALS", bold=True, after=4, keep=True)
    rec = [
        ("A.", "The District sponsors the Red Cedar Valley Schools Employee Health Plan (the \"Plan\"), a self-insured "
               "group health plan for eligible employees, early retirees under age 65 and their dependents. Ellery Benefit "
               "Administrators administers medical claims and utilization review under the Plan and Quarrystone Rx "
               "administers pharmacy claims."),
        ("B.", "On 13 January 2025 the District issued Request for Proposals 2025-07 for high-cost care management "
               "services for a programme year beginning 1 April 2025 and received three proposals, one of them from "
               "Northcourt. On 8 April 2025 the District cancelled RFP 2025-07 before making an award, when the School "
               "Board froze new non-instructional contracts for the 2025-26 fiscal year."),
        ("C.", "On 2 September 2026 the District issued Request for Proposals 2026-11 for the same services for a "
               "programme year beginning 1 April 2027. The evaluation committee ranked Northcourt's proposal of 9 October "
               "2026 first, and this Agreement is made on the terms of that proposal as negotiated."),
        ("D.", "Northcourt will provide the Services as a business associate of the Plan and will receive eligibility "
               "and claims data for that purpose under Schedules D and E."),
        ("E.", "On 9 February 2027 the School Board approved this Agreement and authorised its Chair and the "
               "Superintendent to execute it on behalf of the District."),
    ]
    for k, t in rec:
        D.p(k + "\t" + t, indent=0.4, hanging=0.4, align="justify")
    D.p("NOW, THEREFORE, in consideration of the mutual promises in this Agreement, the District and Northcourt agree "
        "as follows.", align="justify")
    D.p("[Sections 1 to 14 of the Agreement not reproduced.]", italic=True, size=9.5, before=4, after=14)
    D.p("IN WITNESS WHEREOF, the parties have executed this Agreement as of the dates below.", keep=True, after=14)
    sig = [["INDEPENDENT SCHOOL DISTRICT NO. 2817", "NORTHCOURT CARE PARTNERS, LLC"],
           ["", ""],
           ["By: /s/ Deborah Johnson", "By: /s/ Phillip Alvarado"],
           ["Deborah Johnson", "Phillip Alvarado"],
           ["Chair, School Board", "Chief Operating Officer"],
           ["Date: 16 February 2027", "Date: 16 February 2027"],
           ["", ""],
           ["By: /s/ Sandra Lopez", ""],
           ["Sandra Lopez", ""],
           ["Superintendent", ""],
           ["Date: 16 February 2027", ""]]
    D.table(sig, [3.25, 3.25], header=True, grid=False)
    D.p("SCHEDULE C", bold=True, size=12, align="center", after=0, newpage=True)
    D.p("BASELINE AND SAVINGS", bold=True, size=12, align="center", after=10)
    D.p("C.1\t**Definitions.** In this Schedule:", indent=0.45, hanging=0.45)
    defs = [
        ("(a)", "\"Allowed Claims\" means the allowed amount of medical and pharmacy claims for covered services incurred "
                "by a member while the member is covered under the Plan, including the member's deductible, copayment and "
                "coinsurance. Pharmacy claims are taken before manufacturer rebates. Claims are taken net of replacement "
                "claims, voided claims and pharmacy reversals. No deduction is made for reimbursements under the "
                "District's stop-loss insurance. A medical claim is incurred on its first date of service and a pharmacy "
                "claim on its date of fill, and a claim incurred in a period counts in that period whether or not the "
                "month in which it is incurred is a Member Month for the member."),
        ("(b)", "\"Member Month\" means a calendar month in which a member is enrolled in the Plan on the first day of "
                "the month."),
        ("(c)", "\"Allowed Claims per Member Month\" of a group of members for a period means the Allowed Claims "
                "incurred in the period by the members of the group, divided by the total of their Member Months in the "
                "period. A member who is enrolled for part of the period is included for the Member Months in which the "
                "member is enrolled."),
        ("(d)", "\"Data Cut-Off Date\" means 28 February 2027."),
        ("(e)", "\"Final Enrolment List\" means the list of members delivered by Northcourt under Section 3.2, "
                "stratified on claims incurred in calendar year 2026 and paid through the Data Cut-Off Date. \"Enrolled "
                "Members\" means the members on the Final Enrolment List. \"Risk Tier\" means one of the four tiers into "
                "which Northcourt's acuity model places members by score, as described in Schedule A, and a member's Risk "
                "Tier is the tier assigned to the member on the Final Enrolment List."),
        ("(f)", "\"Programme\" means the Services described in Schedule A, and \"Programme Year\" means the twelve "
                "months from 1 April 2027 to 31 March 2028."),
        ("(g)", "\"Trend Factor\" means the annual medical and pharmacy trend rates adopted in the District's most "
                "recent renewal of Plan funding rates."),
        ("(h)", "\"Baseline PMPM\" means, for each Risk Tier and separately for medical and for pharmacy Allowed Claims, "
                "the Allowed Claims per Member Month that the Enrolled Members in that Risk Tier would be expected to "
                "incur in the Programme Year in the absence of the Programme. A Baseline PMPM is determined separately for "
                "each Risk Tier, from the experience of members in that Risk Tier. Experience from an earlier period that "
                "is used to determine a Baseline PMPM is taken on claims paid through the Data Cut-Off Date and is "
                "projected by multiplying it by one plus the Trend Factor, raised to the power of the number of months from "
                "the midpoint of that period to the midpoint of the Programme Year divided by twelve."),
        ("(i)", "\"Programme Baseline\" means the Baseline PMPMs averaged across the Risk Tiers, weighted by the number "
                "of Enrolled Members in each Risk Tier, for medical, for pharmacy and in total."),
        ("(j)", "\"Actual PMPM\" means, for each Risk Tier and separately for medical and for pharmacy, the Enrolled "
                "Members' Allowed Claims per Member Month for the Programme Year, on Allowed Claims incurred in the "
                "Programme Year and paid by 30 June 2028."),
    ]
    for k, t in defs:
        D.p(k + "\t" + t, indent=0.9, hanging=0.45, align="justify")
    clauses = [
        ("C.2", "**Certification.** Before the start of the Programme Year the District will certify to Northcourt in "
                "writing, following approval by the School Board, the Baseline PMPM for each Risk Tier and benefit and the "
                "Programme Baseline. The certification will also show, for each Risk Tier, the number of Enrolled Members "
                "and their Allowed Claims per Member Month for calendar year 2026 as paid through the Data Cut-Off Date, "
                "without completion. Amounts are stated in whole dollars and no amount is rounded before the final "
                "figure."),
        ("C.3", "**Savings.** For each Risk Tier and benefit, Savings equal the Baseline PMPM less the Actual PMPM, "
                "multiplied by the Enrolled Members' Member Months in the Programme Year in that Risk Tier. Programme "
                "Savings are the sum of Savings across Risk Tiers and benefits; a negative result for one Risk Tier or "
                "benefit reduces the total."),
        ("C.4", "**Shared Savings Fee.** Northcourt is entitled to 40 per cent of Programme Savings, if positive, up to "
                "a maximum of $900,000 for the Programme Year. The Shared Savings Fee is in addition to the administrative "
                "fee in Schedule B and is payable within 45 days after the reconciliation becomes final."),
        ("C.5", "**Reconciliation.** The District will deliver to Northcourt a reconciliation of Programme Savings by "
                "31 August 2028, on claims paid through 30 June 2028, with the member-level detail Northcourt reasonably "
                "needs to check it."),
        ("C.6", "**Disputes.** Either party may dispute the certification under C.2 or the reconciliation under C.5 by "
                "written notice within 30 days of receiving it. A dispute the parties do not settle within a further 30 "
                "days will be referred to an independent actuary who is a Fellow of the Society of Actuaries and a Member "
                "of the American Academy of Actuaries, appointed jointly by the parties. The actuary's determination is "
                "final and binding, and the parties share the actuary's fees equally."),
        ("C.7", "**Plan changes.** If the District changes Plan benefits during the Programme Year, the parties will "
                "adjust the affected Baseline PMPMs in good faith to reflect the change."),
    ]
    for k, t in clauses:
        D.p(k + "\t" + t, indent=0.45, hanging=0.45, align="justify")
    D.save_pdf(path, "Care Management Services Agreement RCV-2027-014 (conformed excerpt)", "Business Office",
               dt.datetime(2027, 2, 17, 10, 42, 18))


# ------------------------------------------------------------------ the renewal letter
def renewal_pdf(path, F):
    """F: figures computed from the shipped extracts at the letter's paid-through date (see estimators.letter_figures)"""
    D = Doc("Calibri", 10, margins=(1.0, 1.0, 1.0, 0.7))
    D.d.styles["Normal"].paragraph_format.space_after = Pt(5)
    D.header_lines([("LINDQVIST", True, 14, "1F3B57"), ("Benefits Consulting", False, 8.5, "1F3B57"),
                    ("80 South Eighth Street, Suite 2210, Minneapolis, MN 55402", False, 8, "555555")])
    D.footer("Red Cedar Valley Schools, 2027-28 renewal", page_fmt="{PAGE}", size=7.5)
    D.p("26 February 2027", before=2, after=8)
    D.p("Joyce Salinas", after=0)
    D.p("Director of Risk Management and Benefits", after=0)
    D.p("Red Cedar Valley Schools", after=8)
    D.p("cc: Anthony Olsen, Chief Financial Officer", size=9, after=10)
    D.p("**Re: Employee Health Plan, funding rates for the plan year 1 July 2027 to 30 June 2028**", after=8)
    D.p("Dear Joyce,")
    D.p("This letter sets out our recommended funding rates for the 2027-28 plan year. Anthony and I went through the "
        "draft on 23 February; the only change since the draft we sent on 19 February is the stop-loss premium, which "
        "Wyecliff confirmed on 22 February.")
    D.p("**Experience.** We used Ellery's medical claims and Quarrystone's pharmacy claims incurred from January 2025 to "
        "December 2026 and paid through 31 January 2027, with member months from Ellery's eligibility. Bramwell's 2024 "
        "history is not in the District's warehouse and we did not use it. Claims are taken at their allowed amounts, net "
        "of replacement and void claims and pharmacy reversals; pharmacy is before rebates, which we treat as a separate "
        "credit. Exhibit 1 summarises the experience. We completed 2026 medical claims with the factors in Exhibit 2, "
        "which we derived from the plan's own payment pattern on claims incurred in the second half of 2025. Pharmacy "
        "claims are paid at the point of sale and need no completion.")
    D.p("**Trend.** We are holding annual trend at %.1f per cent for medical and %.1f per cent for pharmacy, unchanged "
        "from last year's renewal. The pharmacy rate reflects GLP-1 and specialty growth on the Quarrystone formulary; we "
        "will look at it again after the 2026 rebate true-up in June." % (100 * (W.TREND_MED - 1), 100 * (W.TREND_RX - 1)))
    D.p("**Projection.** We projected the 2026 completed experience 18 months, from the middle of calendar 2026 to the "
        "middle of the 2027-28 plan year. That gives %s per member per month for medical and %s for pharmacy, %s in "
        "total, before fixed costs." % (money(F["proj_med"], True), money(F["proj_rx"], True),
                                        money(F["proj_med"] + F["proj_rx"], True)))
    D.p("**Fixed costs.** Ellery's administrative fee is $38.75 per employee per month from 1 January 2027. Wyecliff "
        "renewed the specific stop-loss for calendar 2027 at a $300,000 deductible with no individual lasers, at $78.20 "
        "per employee per month, and the aggregate cover at $4.15. Northcourt's administrative fee under the new care "
        "management agreement is budgeted outside the funding rates, as is any shared savings payment, and we have not "
        "taken credit for programme savings in the projection. We have kept the 3 per cent margin.")
    D.p("**Recommended rates.** On this basis we recommend the monthly funding rates below, an increase of %.1f per cent "
        "on the current rates on the District's enrolment as of February 2027." % F["rate_incr"], keep=True)
    rates = [["Coverage tier", "PPO 2026-27", "PPO 2027-28", "HSA plan 2026-27", "HSA plan 2027-28"]]
    for tier, label in (("EE", "Employee"), ("ES", "Employee + spouse"), ("EC", "Employee + child(ren)"), ("FAM", "Family")):
        rates.append([label, money(F["rates_now"]["PPO"][tier], True), money(F["rates_new"]["PPO"][tier], True),
                      money(F["rates_now"]["HDHP"][tier], True), money(F["rates_new"]["HDHP"][tier], True)])
    D.table(rates, [1.7, 1.15, 1.15, 1.2, 1.2], size=9.5, align_right_from=1, shade="DCE4EC")
    D.p("Please call me with any questions before the Board's 25 March meeting.", keep=True)
    D.p("Sincerely,", after=18, keep=True)
    D.p("Michael Perry, FSA, MAAA", after=0, keep=True)
    D.p("Principal and Consulting Actuary", after=0)
    D.page_break()
    D.p("**Exhibit 1. Experience, incurred January 2025 to December 2026, paid through 31 January 2027**", keep=True)
    e = [["", "2025", "2026"],
         ["Member months", format(F["mm"][2025], ","), format(F["mm"][2026], ",")],
         ["Medical allowed, paid", money(F["med_paid"][2025]), money(F["med_paid"][2026])],
         ["Medical allowed, completed", money(F["med_comp"][2025]), money(F["med_comp"][2026])],
         ["Pharmacy allowed, before rebates", money(F["rx"][2025]), money(F["rx"][2026])],
         ["Medical per member per month", money(F["med_comp"][2025] / F["mm"][2025], True), money(F["med_comp"][2026] / F["mm"][2026], True)],
         ["Pharmacy per member per month", money(F["rx"][2025] / F["mm"][2025], True), money(F["rx"][2026] / F["mm"][2026], True)],
         ["Total per member per month", money((F["med_comp"][2025] + F["rx"][2025]) / F["mm"][2025], True),
          money((F["med_comp"][2026] + F["rx"][2026]) / F["mm"][2026], True)]]
    D.table(e, [2.7, 1.5, 1.5], size=9.5, align_right_from=1, shade="DCE4EC")
    D.p("Member months and claims on the same basis as the 2026-27 renewal. 2025 medical claims are treated as complete.",
        size=8.5, italic=True)
    D.p("**Exhibit 2. Medical completion factors, 2026 incurred months, paid through 31 January 2027**", keep=True, before=6)
    cf = [["Incurred month", "Completion factor"]]
    for m in range(1, 13):
        cf.append([dt.date(2026, m, 1).strftime("%B 2026"), "%.3f" % F["cf"][m]])
    D.table(cf, [2.0, 1.4], size=9.5, align_right_from=1, shade="DCE4EC")
    D.p("Completed claims are paid claims divided by the factor. Factors are the share of the final allowed amount for "
        "claims incurred July to December 2025 that had been paid the same number of months after the incurred month.",
        size=8.5, italic=True)
    D.p("**Exhibit 3. Projection to the 2027-28 plan year (per member per month)**", keep=True, before=6)
    pj = [["", "Medical", "Pharmacy"],
          ["2026 completed experience", money(F["med_comp"][2026] / F["mm"][2026], True), money(F["rx"][2026] / F["mm"][2026], True)],
          ["Annual trend", "%.1f%%" % (100 * (W.TREND_MED - 1)), "%.1f%%" % (100 * (W.TREND_RX - 1))],
          ["Months, 1 July 2026 to 1 January 2028", "18", "18"],
          ["Projected 2027-28", money(F["proj_med"], True), money(F["proj_rx"], True)]]
    D.table(pj, [2.7, 1.5, 1.5], size=9.5, align_right_from=1, shade="DCE4EC")
    D.save_pdf(path, "RCV 2027-28 renewal", "Michael Perry", dt.datetime(2027, 2, 26, 16, 5, 41))


# ------------------------------------------------------------------ HTML documents printed by Chromium
def _esc(t):
    return html.escape(t, quote=False)


def _rows(rows, cls=""):
    return "".join("<tr>%s</tr>" % "".join(("<th>%s</th>" if j == 0 and cls == "kv" else "<td>%s</td>") % _esc(str(c))
                                            for j, c in enumerate(r)) for r in rows)


# ------------------------------------------------------------------ stop-loss policy schedule (Wyecliff's policy system)
def stoploss_pdf(path, census):
    kv = lambda rows: '<table class="kv">%s</table>' % _rows(rows, "kv")
    part1 = kv([["Specific deductible", "$300,000 per Covered Person per Policy Period"],
                ["Contract basis", "Claims incurred 1 January 2026 to 31 December 2027 and paid 1 January 2027 to "
                                   "31 December 2027 (24/12)"],
                ["Reimbursement", "100 per cent of Eligible Expenses in excess of the specific deductible"],
                ["Maximum benefit", "Unlimited per Covered Person"],
                ["Individual deductibles", "None. No Covered Person is subject to a separate specific deductible for this "
                                           "Policy Period."],
                ["Premium", "$78.20 per covered employee per month, composite"]])
    factors = ('<table class="grid"><tr><th>Coverage tier</th><th class="r">Monthly aggregate factor</th></tr>%s</table>'
               % "".join('<tr><td>%s</td><td class="r">%s</td></tr>' % (a, b) for a, b in
                         (("Employee", "$812.40"), ("Employee + spouse", "$1,690.10"), ("Employee + child(ren)", "$1,452.60"),
                          ("Family", "$2,371.30"))))
    part2 = kv([["Attachment point", "The sum over the Policy Period of the monthly aggregate factors times the covered "
                                     "employees in each tier in that month; not less than the minimum attachment point"],
                ["Minimum attachment point", "95 per cent of the first month's factors times 12"],
                ["Contract basis", "Claims incurred 1 January 2027 to 31 December 2027 and paid 1 January 2027 to "
                                   "31 March 2028 (12/15)"],
                ["Maximum benefit", "$1,000,000 per Policy Period"],
                ["Premium", "$4.15 per covered employee per month"]])
    defs = "".join("<p><b>%s.</b> %s</p>" % (_esc(k), _esc(t)) for k, t in [
        ("Eligible Expenses", "Amounts the Plan has paid for covered medical and prescription drug services under the terms "
                              "of the Plan Document in force at the start of the Policy Period, after member deductibles, "
                              "copayments and coinsurance, coordination of benefits, provider discounts and any "
                              "prescription drug rebates, administrative fees and cost-containment fees, and within the "
                              "contract basis above."),
        ("Covered Person", "An employee, early retiree or dependent covered under the Plan on the date a service is received."),
        ("Paid", "A claim is paid on the date the claims administrator releases the payment, provided funds are available "
                 "in the Plan's account when the payment clears."),
        ("Run-in", "Claims incurred in 2026 are eligible under the specific coverage only if paid within the Policy Period.")])
    premium = ('<table class="grid"><tr><th></th><th class="r">Covered employees (January 2027 census)</th>'
               '<th class="r">Monthly premium</th></tr>'
               '<tr><td>Specific</td><td class="r">%s</td><td class="r">%s</td></tr>'
               '<tr><td>Aggregate</td><td class="r">%s</td><td class="r">%s</td></tr>'
               '<tr class="tot"><td>Total</td><td></td><td class="r">%s</td></tr></table>'
               % (format(census, ","), money(census * 78.20, True), format(census, ","), money(census * 4.15, True),
                  money(census * 78.20 + census * 4.15, True)))
    doc = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Policy Schedule WSL 27 041188</title>
<style>
@page { size: 8.5in 11in; margin: 0.8in 0.85in 0.85in 0.85in;
  @bottom-left { content: "WLA-SL-SCH (01/26)    Policy WSL 27 041188"; font: 7.5pt Arial, sans-serif; color: #444; }
  @bottom-right { content: "Page " counter(page) " of " counter(pages); font: 7.5pt Arial, sans-serif; color: #444; } }
body { font-family: Arial, "Liberation Sans", sans-serif; font-size: 9.5pt; color: #111; line-height: 1.32; }
.co { text-align: center; font-weight: bold; font-size: 13pt; letter-spacing: 0.04em; margin: 0; }
.sub { text-align: center; margin: 2px 0 0 0; }
.doc { text-align: center; font-weight: bold; margin: 2px 0 14px 0; border-bottom: 1.5px solid #222; padding-bottom: 8px; }
h2 { font-size: 10pt; margin: 14px 0 5px 0; }
table { border-collapse: collapse; width: 100%%; margin: 0 0 8px 0; page-break-inside: avoid; }
table.kv th { text-align: left; width: 1.75in; vertical-align: top; padding: 3px 6px; border: 1px solid #999; background: #f2f2f2; }
table.kv td { padding: 3px 6px; border: 1px solid #999; }
table.grid { width: auto; min-width: 4.4in; }
table.grid th, table.grid td { border: 1px solid #999; padding: 3px 8px; }
table.grid th { background: #e6e6e6; text-align: left; }
.r { text-align: right; }
tr.tot td { font-weight: bold; }
p { margin: 0 0 6px 0; text-align: justify; }
.sig { margin-top: 16px; }
.small { font-size: 8pt; font-style: italic; }
</style></head><body>
<p class="co">WYECLIFF LIFE ASSURANCE COMPANY</p>
<p class="sub">Employer Medical Stop Loss Insurance</p>
<p class="doc">POLICY SCHEDULE</p>
%(head)s
<h2>Part 1. Specific stop loss</h2>
%(part1)s
<h2>Part 2. Aggregate stop loss</h2>
%(factors)s
%(part2)s
<h2>Part 3. Definitions used in this Schedule</h2>
%(defs)s
<h2>Part 4. Notification and claims</h2>
<p>The Policyholder or its claims administrator will notify the Company within 30 days after a Covered Person's paid
claims in the Policy Period reach $150,000, and within 30 days after any of the following is first coded on a claim: a
malignant neoplasm under active treatment, an organ or bone marrow transplant evaluation, end-stage renal disease or
dialysis, a neonatal intensive care stay over 10 days, a spinal cord or traumatic brain injury, or a specialty drug with an
annual cost above $100,000. Requests for reimbursement are submitted with an itemised claim history and proof of payment;
the Company pays within 30 days of a complete request.</p>
<h2>Part 5. Renewal</h2>
<p>The Company will offer renewal terms at least 60 days before the end of the Policy Period. Renewal terms may change the
deductible, factors, premiums and individual deductibles on the basis of the Plan's experience and the disclosure provided
with the renewal application.</p>
<h2>Part 6. Premium summary at issue</h2>
%(premium)s
<p class="sig">Signed for Wyecliff Life Assurance Company on 18 December 2026.</p>
<p style="margin:14px 0 0 0">/s/ Jonathan Hoffman</p>
<p style="margin:0">Jonathan Hoffman</p>
<p>Vice President, Stop Loss Underwriting</p>
<p class="small">This Schedule forms part of the Policy and should be read with the Policy form WLA-SL-1 (01/26).</p>
</body></html>""" % {"head": kv([["Policyholder", "Independent School District No. 2817 (Red Cedar Valley Schools), Minnesota"],
                                  ["Policy number", "WSL 27 041188"],
                                  ["Policy period", "12:01 a.m. 1 January 2027 to 12:00 midnight 31 December 2027, Central Time"],
                                  ["Plan", "Red Cedar Valley Schools Employee Health Plan (self-insured)"],
                                  ["Claims administrator", "Ellery Benefit Administrators (medical); Quarrystone Rx (prescription drugs)"],
                                  ["Producer of record", "Lindqvist Benefits Consulting, Minneapolis"],
                                  ["Covered benefits", "Medical and prescription drug"]]),
                         "part1": part1, "factors": factors, "part2": part2, "defs": defs, "premium": premium}
    C.chromium_pdf(doc, path, dt.datetime(2026, 12, 18, 9, 12, 7))


# ------------------------------------------------------------------ Northcourt's implementation and outreach plan (client portal)
def implementation_pdf(path):
    team = ('<table><tr><th>Name</th><th>Role</th><th>Contact</th></tr>%s</table>' % _rows([
        ["Allison Santiago", "Account Lead", "Direct line and secure email in the contact sheet sent 17 February"],
        ["Samantha Galvan, RN", "Clinical Manager, RN care management", "Escalations for Tier 1 and 2 members"],
        ["Edward Miller", "Member Outreach Supervisor", "Welcome letters, call scheduling, opt-outs"],
        ["Amy Kelley", "Clinical Analytics", "Enrolment list, data feeds, monthly reporting"],
        ["Phillip Alvarado", "Chief Operating Officer, executive sponsor", "Contract and escalation of last resort"]]))
    timeline = ('<table><tr><th>Date</th><th>Milestone</th><th>Owner</th></tr>%s</table>' % _rows([
        ["6 January 2027", "Interim business associate agreement signed; 2026 claims and eligibility files sent to Northcourt",
         "District, Ellery, Quarrystone"],
        ["14 January 2027", "Draft enrolment list on December paid claims sent to the District", "Northcourt"],
        ["16 February 2027", "Agreement executed", "District, Northcourt"],
        ["26 February 2027", "Schedule D file layouts confirmed for the weekly and monthly feeds", "Northcourt, Ellery"],
        ["5 March 2027", "Final Enrolment List delivered to the District", "Northcourt"],
        ["18 March 2027", "Care team introductions to District Human Resources", "Northcourt"],
        ["19 March 2027", "First weekly eligibility file sent to Northcourt", "Ellery"],
        ["22 March 2027", "Welcome letters mailed to enrolled members", "Northcourt"],
        ["1 April 2027", "Programme start", ""],
        ["1 to 16 April 2027", "Outreach wave 1: Risk Tiers 1 and 2", "RN care managers"],
        ["5 April to 7 May 2027", "Outreach wave 2: Risk Tiers 3 and 4", "Health coaches"],
        ["12 April 2027", "First monthly claims files from Ellery and Quarrystone", "Ellery, Quarrystone"],
        ["14 May 2027", "First monthly engagement report", "Northcourt"],
        ["30 June 2027", "Second letter to members not yet reached", "Northcourt"],
        ["22 July 2027", "First quarterly review with the District", "District, Northcourt"]]))
    doc = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>RCV implementation and outreach plan v1.2</title>
<style>
@page { size: 8.5in 11in; margin: 0.9in 0.85in 0.8in 0.85in;
  @top-left { content: "Northcourt Care Partners  |  Client Implementation"; font: bold 8.5pt Carlito, Calibri, sans-serif; color: #0b5563; }
  @bottom-left { content: "Northcourt Care Partners, LLC  |  Confidential: prepared for Red Cedar Valley Schools"; font: 7.5pt Carlito, Calibri, sans-serif; color: #555; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 7.5pt Carlito, Calibri, sans-serif; color: #555; } }
body { font-family: Carlito, Calibri, sans-serif; font-size: 10.5pt; color: #222; line-height: 1.3; }
h1 { font-size: 15pt; margin: 0 0 2px 0; color: #111; }
.lede { font-size: 12pt; color: #0b5563; margin: 0 0 4px 0; }
.ver { font-size: 9pt; font-style: italic; color: #444; margin: 0 0 14px 0; }
h2 { font-size: 11pt; color: #0b5563; margin: 14px 0 4px 0; }
p { margin: 0 0 7px 0; text-align: justify; }
table { border-collapse: collapse; width: 100%%; margin: 2px 0 8px 0; font-size: 9.5pt; }
th { background: #dcedef; text-align: left; padding: 4px 6px; border-bottom: 1px solid #8fb7bd; }
td { padding: 3px 6px; border-bottom: 1px solid #d6e3e5; vertical-align: top; }
ul { margin: 0 0 8px 0; padding-left: 18px; }
li { margin-bottom: 4px; text-align: justify; }
</style></head><body>
<h1>Red Cedar Valley Schools Employee Health Plan</h1>
<p class="lede">Care management programme, 1 April 2027 to 31 March 2028: implementation and member outreach plan</p>
<p class="ver">Version 1.2, 8 March 2027. Prepared by Allison Santiago, Account Lead, for Joyce Salinas, Director of Risk
Management and Benefits.</p>
<h2>1. Purpose</h2>
<p>This plan sets out how Northcourt will start the programme for Red Cedar Valley Schools under Agreement RCV-2027-014:
who on our side does what, the dates we are working to with the District, Ellery and Quarrystone, how we will contact the
members on the Final Enrolment List, and what the District will receive from us during the year. It replaces version 1.1
of 22 February, which had the outreach waves a week later.</p>
<h2>2. Account team</h2>
%(team)s
<h2>3. Timeline</h2>
%(timeline)s
<h2>4. Member outreach</h2>
<p>Each member on the Final Enrolment List is assigned to a care team before the welcome letter goes out. Members in Risk
Tiers 1 and 2 are assigned to a registered nurse care manager on RN Team A (cancer and transplant), RN Team B (heart,
kidney and diabetes) or RN Team C (all other conditions, and children); members in Risk Tiers 3 and 4 to a health coach on
Health Coach Team 1 or 2 by the employee's work location. The care team named on the list is the team that calls the
member, so a member who calls back reaches someone who already has the file.</p>
<p>We make three call attempts at different times of day over two weeks, then send a letter with a direct number. Calls to
a member under 18 go to the parent or guardian on the District's file. A member who declines is marked as opted out and is
not called again; the member can rejoin at any time by calling the team. We use an interpreter line for members who
prefer a language other than English, and we do not leave health details on voicemail.</p>
<h2>5. What the District receives</h2>
<ul>
<li>A monthly engagement report by the fourteenth of each month: members reached, members enrolled in a care plan and
members opted out, by Risk Tier and care team.</li>
<li>A quarterly review meeting with Risk Management and Benefits, with a short written summary of programme activity and
any issues with the data feeds.</li>
<li>Notice within two business days if a weekly eligibility file or a monthly claims file is late or fails our load
checks.</li>
</ul>
<h2>6. Data and privacy</h2>
<p>Northcourt receives eligibility and claims data only through the secure file transfer set up under Schedule D and
handles it under the business associate agreement in Schedule E. Care team members see the records of their own members
only. Nothing in this plan changes the terms of the Agreement.</p>
<h2>7. Holidays and cover</h2>
<p>The care teams are staffed Monday to Friday, 8:00 a.m. to 6:00 p.m. Central Time, except on federal holidays. Out of
hours, members reach Northcourt's nurse line, which has the care plan for every enrolled member.</p>
</body></html>""" % {"team": team, "timeline": timeline}
    C.chromium_pdf(doc, path, dt.datetime(2027, 3, 8, 14, 26, 52))


# ------------------------------------------------------------------ workbooks
THIN = Side(style="thin", color="A6A6A6")
HDR_FILL = PatternFill("solid", fgColor="DCE6F1")
ADD_FILL = PatternFill("solid", fgColor="FFF2CC")


def save_xlsx(wb, path, creator, last_by, created, modified):
    """an export as the organisation's system writes it (containers.library_xlsx)"""
    wb.save(path)
    C.library_xlsx(path, C.core_props(creator, last_by, created, modified), modified)


# workbook saves: (created, created by, modified, modified by)
LIST_SAVES = {
    "bid": (local(2025, 2, 21, 14, 37, 2), "Amy Kelley", local(2025, 3, 6, 15, 12, 40), "Tiffany Barrett"),
    "draft": (local(2027, 1, 14, 11, 20, 45), "Amy Kelley", local(2027, 1, 14, 11, 20, 45), "Amy Kelley"),
    "final": (local(2027, 3, 5, 9, 48, 30), "Amy Kelley", local(2027, 3, 5, 9, 48, 30), "Amy Kelley"),
}


def care_team(S, pid, tier, when):
    """the plan's assignment rule (Northcourt's implementation plan, section 4)"""
    p = S.people[pid]
    if tier >= 3:
        return "Health Coach Team " + ("1" if C_u01("site", S.fams[p.fid].emp) < 0.55 else "2")
    seen = S.cond_years.get((pid, 2026), set())
    if p.age(when) < 18:
        return "RN Team C"
    if "cancer" in seen or seen & {"kidney_tx", "liver_tx"}:
        return "RN Team A"
    if seen & {"cad", "chf", "afib", "esrd", "diabetes"}:
        return "RN Team B"
    return "RN Team C"


def data_book_records(S):
    """the RFP 2025-07 data book's record numbers: one per member in its census, in no particular order"""
    census = [p for p in S.people if p.legacy is not None]
    census.sort(key=lambda p: C_u01("databook", p.pid))
    return {p.pid: "%05d" % (10001 + i) for i, p in enumerate(census)}


def stratification_xlsx(path, kind, rows, S):
    """kind: bid, draft or final. rows: (rank, pid, ident, score, tier)"""
    people = S.people
    wb = Workbook()
    ws = wb.active
    ws.title = "Cover"
    tiers = "Tier 1: %.1f and above; Tier 2: %.1f to %.1f; Tier 3: %.1f to %.1f; Tier 4: below %.1f" % (
        W.TIERS[0][1], W.TIERS[1][1], W.TIERS[0][1] - 0.1, W.TIERS[2][1], W.TIERS[1][1] - 0.1, W.TIERS[2][1])
    if kind == "bid":
        meta = [
            ("Northcourt Care Partners", "Clinical Analytics"),
            ("Document", "RFP 2025-07 response, Attachment C: population stratification"),
            ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817)"),
            ("Prepared by", "Amy Kelley, Clinical Analytics; reviewed by Allison Santiago, Account Lead"),
            ("Date", "21 February 2025"),
            ("Data basis", "RFP 2025-07 data book issued 24 January 2025: medical and pharmacy claims incurred 1 January to "
                           "31 December 2024, paid through 31 December 2024; eligibility as of 1 January 2025"),
            ("Record", "Data book record number"),
            ("Model", "Northcourt Acuity Model 4.2, run on one calendar year of claims"),
            ("Score", "0 to 100, shown to one decimal; ranks use the unrounded score"),
            ("Selection", "The 140 highest-scoring members enrolled on 1 January 2025 (proposed programme capacity)"),
            ("Risk tiers", tiers),
            ("Proposed programme year", "1 April 2025 to 31 March 2026 (RFP 2025-07, Section 2: members listed on 2024 "
                                        "claims enrolled on 1 April 2025, savings measured on the programme year's claims)"),
            ("", ""),
            ("District copy", "Risk Management and Benefits added the last two columns of the Members sheet (Bramwell "
                              "member number and date of birth) on 6 March 2025 from the District's key to the data book "
                              "record numbers. Bidders were sent the data book without names, member numbers or birth "
                              "dates."),
            ("Confidential", "Contains protected health information."),
        ]
    elif kind == "draft":
        meta = [
            ("Northcourt Care Partners", "Clinical Analytics"),
            ("Document", "Stratification of 2026 claims: DRAFT for District review"),
            ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817)"),
            ("Prepared by", "Amy Kelley, Clinical Analytics; Allison Santiago, Account Lead"),
            ("Date", "14 January 2027"),
            ("Data basis", "Ellery medical and Quarrystone pharmacy claims incurred 1 January to 31 December 2026, paid "
                           "through 31 December 2026; members enrolled on 1 January 2027"),
            ("Member ID", "Ellery member ID"),
            ("Model", "Northcourt Acuity Model 4.2, run on one calendar year of claims"),
            ("Score", "0 to 100, shown to one decimal; ranks use the unrounded score"),
            ("Selection", "The 140 highest-scoring members enrolled on 1 January 2027"),
            ("Risk tiers", tiers),
            ("Status", "Draft. The enrolment list will be rerun on February paid claims."),
            ("", ""),
            ("Confidential", "Contains protected health information."),
        ]
    else:
        meta = [
            ("Northcourt Care Partners", "Clinical Analytics"),
            ("Document", "Final Enrolment List, Care Management Services Agreement RCV-2027-014, Section 3.2"),
            ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817)"),
            ("Prepared by", "Amy Kelley, Clinical Analytics; Allison Santiago, Account Lead"),
            ("Delivered", "5 March 2027"),
            ("Data basis", "Ellery medical and Quarrystone pharmacy claims incurred 1 January to 31 December 2026, paid "
                           "through 28 February 2027; members enrolled on 1 March 2027"),
            ("Member ID", "Ellery member ID"),
            ("Model", "Northcourt Acuity Model 4.2, run on one calendar year of claims"),
            ("Score", "0 to 100, shown to one decimal; ranks use the unrounded score"),
            ("Selection", "The 140 highest-scoring members enrolled on 1 March 2027"),
            ("Risk tiers", tiers),
            ("Programme Year", "1 April 2027 to 31 March 2028"),
            ("Care team", "Assigned under section 4 of the implementation plan"),
            ("Supersedes", "Draft stratification of 14 January 2027"),
            ("", ""),
            ("Confidential", "Contains protected health information."),
        ]
    for i, (k, v) in enumerate(meta, 1):
        ws.cell(row=i, column=1, value=k or None).font = Font(bold=True, name="Calibri", size=11 if i > 1 else 13)
        c = ws.cell(row=i, column=2, value=v or None)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=i, column=1).alignment = Alignment(vertical="top")
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 96
    lst = wb.create_sheet("Members")
    rel = {"E": "Subscriber", "R": "Subscriber", "S": "Spouse", "C": "Dependent"}
    if kind == "bid":
        hdr = ["Rank", "Record", "Relationship", "Age", "Sex", "Acuity score", "Risk tier", "Bramwell member no.",
               "Date of birth"]
        rec = data_book_records(S)
        census_day = dt.date(2024, 12, 31)
    else:
        hdr = ["Rank", "Member ID", "Relationship", "Date of birth", "Sex", "Acuity score", "Risk tier"]
        if kind == "final":
            hdr += ["Care team", "Enrolment effective"]
    lst.append(hdr)
    for rank, pid, ident, sc, tier in rows:
        p = people[pid]
        if kind == "bid":
            row = [rank, rec[pid], rel[p.rel], p.age(census_day), p.sex, sc, tier, ident, p.dob]
        else:
            row = [rank, ident, rel[p.rel], p.dob, p.sex, sc, tier]
            if kind == "final":
                row += [care_team(S, pid, tier, W.FINAL_ELIG), dt.date(2027, 4, 1)]
        lst.append(row)
    for j in range(1, len(hdr) + 1):
        c = lst.cell(row=1, column=j)
        c.font = Font(bold=True)
        c.fill = ADD_FILL if (kind == "bid" and j >= 8) else HDR_FILL
        c.border = Border(bottom=THIN)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    dcol = 9 if kind == "bid" else 4
    for r_ in range(2, len(rows) + 2):
        lst.cell(row=r_, column=dcol).number_format = "mm/dd/yyyy"
        lst.cell(row=r_, column=6).number_format = "0.0"
        if kind == "final":
            lst.cell(row=r_, column=9).number_format = "mm/dd/yyyy"
    widths = [7, 15, 13, 13, 6, 12, 10, 18, 18] if kind != "bid" else [7, 9, 13, 6, 6, 12, 10, 18, 13]
    for j, wdt in enumerate(widths[:len(hdr)], 1):
        lst.column_dimensions[get_column_letter(j)].width = wdt
    lst.freeze_panes = "A2"
    lst.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(hdr)), len(rows) + 1)
    sm = wb.create_sheet("Tier summary")
    sm.append(["Risk tier", "Score range", "Members"])
    for t, floor in W.TIERS:
        hi = {1: None, 2: W.TIERS[0][1], 3: W.TIERS[1][1], 4: W.TIERS[2][1]}[t]
        rng = ("%.1f and above" % floor) if t == 1 else ("below %.1f" % hi if t == 4 else "%.1f to %.1f" % (floor, hi - 0.1))
        sm.append([t, rng, sum(1 for r_ in rows if r_[4] == t)])
    sm.append(["Total", None, len(rows)])
    for j in range(1, 4):
        sm.cell(row=1, column=j).font = Font(bold=True)
        sm.cell(row=1, column=j).fill = HDR_FILL
    sm.cell(row=6, column=1).font = Font(bold=True)
    sm.cell(row=6, column=3).font = Font(bold=True)
    sm.column_dimensions["A"].width = 11
    sm.column_dimensions["B"].width = 18
    sm.column_dimensions["C"].width = 10
    created, by, modified, last_by = LIST_SAVES[kind]
    save_xlsx(wb, path, by, last_by, created, modified)


def rebate_xlsx(path, R):
    """R: per quarter and drug counts of net brand claims in 2026 (estimators.rebate_figures)"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    top = [("Quarrystone Rx", None), ("Client rebate statement, calendar year 2026", None),
           ("Client", "Red Cedar Valley Schools Employee Health Plan (ISD 2817), group RCV01"),
           ("Prepared", "19 February 2027 by Client Services (Michelle Peterson, Client Account Executive)"),
           ("Contract", "Pharmacy Benefit Services Agreement, Exhibit 4: minimum rebate guarantees per paid brand claim"),
           (None, None)]
    for k, v in top:
        ws.append([k, v])
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"].font = Font(bold=True)
    hdr = ["Quarter", "Brand claims, retail and mail", "Guarantee per claim", "Specialty claims", "Guarantee per claim",
           "Rebates earned", "Invoiced to manufacturers", "Received from Quarrystone", "Status"]
    ws.append(hdr)
    hr = ws.max_row
    for j in range(1, len(hdr) + 1):
        c = ws.cell(row=hr, column=j)
        c.font = Font(bold=True)
        c.fill = HDR_FILL
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    status = {1: ("05/14/2026", "08/21/2026", "Paid"), 2: ("08/13/2026", "11/20/2026", "Paid"),
              3: ("11/12/2026", "02/18/2027", "Paid"), 4: ("02/11/2027", None, "Invoiced; payment expected by 06/30/2027")}
    tot = [0, 0, 0.0]
    for q in (1, 2, 3, 4):
        b, sp = R["brand"][q], R["spec"][q]
        earned = b * R["g_brand"] + sp * R["g_spec"]
        tot[0] += b
        tot[1] += sp
        tot[2] += earned
        ws.append(["Q%d 2026" % q, b, R["g_brand"], sp, R["g_spec"], earned, status[q][0], status[q][1], status[q][2]])
    ws.append(["Total", tot[0], None, tot[1], None, tot[2], None, None, None])
    last = ws.max_row
    for r_ in range(hr + 1, last + 1):
        for col in (3, 5, 6):
            ws.cell(row=r_, column=col).number_format = '"$"#,##0.00'
        for col in (2, 4):
            ws.cell(row=r_, column=col).number_format = "#,##0"
    for col in range(1, 10):
        ws.cell(row=last, column=col).font = Font(bold=True)
        ws.cell(row=last, column=col).border = Border(top=THIN)
    ws.append([])
    notes = ["Counts are paid brand claims net of reversals, by date of service. Generic claims and compound claims are "
             "not rebatable.",
             "Specialty claims are claims dispensed by Quarrystone Specialty Pharmacy for drugs on the specialty list.",
             "Rebates are remitted to the plan quarterly in arrears and are not shown on claim records or in claim amounts.",
             "Q4 2026 amounts are minimum guarantees; any excess over guarantee is reconciled in the annual true-up in June 2027."]
    for n in notes:
        ws.append([n])
    for j, wdt in enumerate([13, 16, 13, 12, 13, 16, 16, 16, 36], 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.row_dimensions[hr].height = 45
    d = wb.create_sheet("By drug")
    hdr = ["Drug", "NDC", "Specialty", "Q1 2026", "Q2 2026", "Q3 2026", "Q4 2026", "Claims 2026", "Rebates earned"]
    d.append(hdr)
    for j in range(1, len(hdr) + 1):
        d.cell(row=1, column=j).font = Font(bold=True)
        d.cell(row=1, column=j).fill = HDR_FILL
    for name, ndc, spec, qs in R["by_drug"]:
        n = sum(qs)
        d.append([name, ndc, "Y" if spec else "N"] + list(qs) + [n, n * (R["g_spec"] if spec else R["g_brand"])])
    for r_ in range(2, d.max_row + 1):
        d.cell(row=r_, column=9).number_format = '"$"#,##0.00'
    for j, wdt in enumerate([40, 15, 10, 9, 9, 9, 9, 12, 15], 1):
        d.column_dimensions[get_column_letter(j)].width = wdt
    d.freeze_panes = "A2"
    save_xlsx(wb, path, "Michelle Peterson", "Michelle Peterson", local(2027, 2, 19, 8, 31, 54), local(2027, 2, 19, 8, 31, 54))


# ------------------------------------------------------------------ the benefits office's warehouse readme
README = """BENEFITS CLAIMS WAREHOUSE - README FOR THE MARCH 2027 PULL
Red Cedar Valley Schools, Risk Management and Benefits
Maintained by Tiffany Barrett, Benefits Analyst
Version of 8 March 2027 (covers the extracts pulled 1 to 3 March 2027)

Four files, all CSV with a header row, UTF-8, comma delimited, amounts in US dollars.

  medical_claim_lines_2025-01_2027-02.csv    Ellery Benefit Administrators, medical claim lines
  pharmacy_claims_2025-01_2027-02.csv        Quarrystone Rx, monthly claims file (PBM layout, unchanged)
  eligibility_spans_2027-02.csv              Ellery Benefit Administrators, eligibility
  tpa_conversion_crosswalk_2025-01-01.csv    Ellery's conversion file from the Bramwell Plan Services records

The warehouse feed started with Ellery's takeover on 1 January 2025. Bramwell's claims history (everything incurred
before 1 January 2025) was never loaded, so neither claims file has dates of service before 1 January 2025.


1. medical_claim_lines_2025-01_2027-02.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per line of an adjudicated claim. Every version of a claim that Ellery has adjudicated (original,
replacement, void) is its own claim number with its own lines. Claims paid or processed 1 January 2025 through
28 February 2027. Pulled 3 March 2027. A claim adjudicated after 28 February 2027 is not in the file.

claim_number            Ellery claim number. YYDDD of the date Ellery received the claim, then a sequence.
line_number             Line on the claim, from 1.
claim_type              P professional (CMS-1500 / 837P), I institutional (UB-04 / 837I).
bill_type               Institutional type of bill (UB-04 form locator 4), blank on professional claims. The third
                        digit repeats the claim frequency code.
claim_frequency_code    1 original claim
                        7 replacement of a prior claim
                        8 void / cancel of a prior claim
                        A replacement claim replaces every line of the claim named in original_claim_number; the
                        replaced claim's lines stay in the file as they were first adjudicated. A void claim's lines
                        repeat the voided claim's lines with every amount carrying the opposite sign.
original_claim_number   For frequency 7 and 8 claims, the claim number the claim replaces or voids. Blank otherwise.
member_id               Ellery member ID (RCV + 7 digits). Joins to eligibility_spans_2027-02.csv.
first_date_of_service   Earliest date of service on the claim (statement from date on institutional claims).
last_date_of_service    Latest date of service on the claim (statement through date; discharge date for a stay).
paid_date               Date of the Ellery check run that released payment. Ellery pays the District's claims once a
                        week, on Thursday, or on the next business day when the Thursday is a bank holiday. On a
                        fully denied claim, the check run whose remittance advice carried the denial.
place_of_service        CMS place of service code, professional claims only (11 office, 10 telehealth in the patient's
                        home, 20 urgent care, 21 inpatient hospital, 22 on-campus outpatient hospital, 23 emergency
                        department, 24 ambulatory surgery center, 31 skilled nursing facility, 41 ambulance, 61
                        inpatient rehabilitation facility, 81 independent laboratory).
revenue_code            NUBC revenue code, institutional claims only.
procedure_code          CPT or HCPCS code. Blank on revenue lines billed without one (room and board, supplies).
modifier                First procedure modifier, where billed (26 professional component, 76 the same reading repeated
                        on the same day, 95 telehealth, GP therapy plan of care, AA and QK anesthesia).
diagnosis_code_1        Principal or first-listed ICD-10-CM diagnosis on the claim (shown with the decimal point).
diagnosis_code_2        Second diagnosis on the claim, where there is one.
billing_npi             Billing provider NPI.
units                   Units of service (days for room and board and NICU lines, sessions for dialysis, minutes for
                        anesthesia lines, billing units of the HCPCS code for drug lines).
billed_amount           Provider's billed charge for the line.
allowed_amount          Ellery's allowed amount for the line. Professional lines: the network fee schedule, or the
                        billed charge if it is lower. Hospital outpatient lines: the hospital's contracted share of
                        charges. Inpatient stays, dialysis, skilled nursing and rehabilitation stays: the contracted
                        rate for the claim, shown on its lines in proportion to their charges. Blank on a denied line.
deductible_amount       Member deductible applied to the line.
copay_amount            Member copayment applied to the line.
coinsurance_amount      Member coinsurance applied to the line.
plan_paid_amount        Amount the plan paid on the line. On every line with an allowed amount,
                        allowed_amount = deductible_amount + copay_amount + coinsurance_amount + plan_paid_amount.
denial_reason_code      Claim adjustment reason code on a denied line; blank on a paid line. A denied line carries no
                        allowed amount and no member cost sharing, and plan_paid_amount is 0.00.
                          16   claim lacks information needed for adjudication (usually resubmitted as a new claim)
                          18   exact duplicate claim or service: the same claim submitted again; Ellery denies the
                               duplicate and the claim first adjudicated stands
                          27   expenses incurred after coverage terminated
                          97   payment included in the allowance for another service
                          204  service not covered under the current benefit plan


2. pharmacy_claims_2025-01_2027-02.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per PBM transaction, claims processed 1 January 2025 through 28 February 2027. Quarrystone's monthly
file, appended month by month with no changes to their layout. Dates are CCYYMMDD.

CLAIM_NBR            Quarrystone transaction number.
TXN_CD               B1 claim billing; B2 reversal of an earlier billing. A B2 carries the RX_NBR, FILL_NBR,
                     DATE_OF_SERVICE and pharmacy of the B1 it reverses and the same quantities, with every amount
                     carrying the opposite sign.
RX_NBR, FILL_NBR     Pharmacy prescription number and fill number (00 for the original fill, 01 onward for refills).
DATE_OF_SERVICE      Fill date.
DATE_PROCESSED       Date Quarrystone adjudicated the transaction.
CARDHOLDER_ID        District employee number of the subscriber, zero-filled to nine characters.
PERSON_CD            Person code: 01 subscriber, 02 spouse, 03 and up dependents, as on the eligibility Quarrystone
                     held on the date of service (Ellery sends it weekly).
PATIENT_DOB          Patient date of birth, as on the eligibility Quarrystone held on the date of service.
PATIENT_GENDER_CD    1 male, 2 female.
RELATIONSHIP_CD      1 cardholder, 2 spouse, 3 child.
PHARMACY_NPI         Dispensing pharmacy NPI.
PHARMACY_NCPDP_ID    Dispensing pharmacy NCPDP provider ID (the first two digits are the state code; 24 is Minnesota).
NDC                  National Drug Code, 11 digits in 5-4-2 form, of the package dispensed.
DRUG_NAME            Quarrystone's drug description.
BRAND_GENERIC_CD     B brand, G generic.
DAW_CD               Dispense as written code (0 no product selection indicated, 1 substitution not allowed by
                     prescriber).
QTY_DISPENSED        Metric quantity (tablets, capsules, mL or grams).
DAYS_SUPPLY          Days supply.
INGREDIENT_COST      Ingredient cost paid.
DISPENSING_FEE       Dispensing fee paid.
GROSS_AMT_DUE        INGREDIENT_COST + DISPENSING_FEE: the allowed amount of the claim.
PATIENT_PAY_AMT      Member copayment, coinsurance or deductible.
PLAN_PAY_AMT         GROSS_AMT_DUE - PATIENT_PAY_AMT.
                     All amounts are before manufacturer rebates. Rebates are remitted quarterly in arrears and are
                     reported on Quarrystone's rebate statements, not on claims.


3. eligibility_spans_2027-02.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per member per coverage span with Ellery. A new span starts whenever the plan, the coverage tier, the
employee class or the member's person code changes. Coverage that ends and starts again later (an employee rehired, a
dependent added back at a special enrolment) starts a new span after the gap, under the same member ID. Pulled 1 March
2027 from Ellery's eligibility as of 28 February 2027.

member_id           Ellery member ID.
employee_number     District employee number of the subscriber (six digits). Early retirees keep theirs.
person_code         Person code in effect during the span: 01 subscriber, 02 spouse, 03 and up dependents. Ellery
                    numbered dependents by date of birth at the conversion, and children added later take the next
                    number. When Ellery corrects a dependent's birth date, it renumbers the family's dependents in
                    birth order from the date of the correction.
relationship        SUB subscriber (employee or early retiree), SPS spouse, DEP dependent child.
birth_date          Date of birth as Ellery holds it at the pull, after any correction.
sex                 F or M.
employee_class      TCH licensed teacher, ESP education support professional, ADM administrator, RET early retiree,
                    COB continuation coverage under COBRA (a former employee, or a dependent, who elected to keep
                    Plan coverage; the span starts the day after the employee's own coverage ended).
coverage_tier       EE employee only, ES employee and spouse, EC employee and child(ren), FAM family.
plan_code           RCV-PPO (PPO plan) or RCV-HSA (high-deductible plan with HSA).
span_start          First day of coverage in the span. Spans start no earlier than 1 January 2025, the day Ellery took
                    over; a member covered before then starts on 1 January 2025.
span_end            Last day of coverage in the span (inclusive). Blank: coverage continuing at the pull.
                    Terminations take effect at month end (31 August for teachers who complete the school year),
                    except deaths, which end coverage on the date of death. A dependent dropped at open enrolment
                    ends on 30 June. Newborns are covered from the date of birth; a new spouse from the first of the
                    month after the marriage; a rehired employee and a dependent added back from the first of a month.


4. tpa_conversion_crosswalk_2025-01-01.csv
---------------------------------------------------------------------------------------------------------------------
Grain: one row per Bramwell member record converted to Ellery on 1 January 2025. Built by Ellery's implementation
team from Bramwell's final eligibility file and loaded once; not updated since. It goes out with every pull because it is
the only place a Bramwell member number meets an Ellery member ID, and the office still works paper that carries
Bramwell numbers: appeals and provider refunds on 2024 services, Bramwell's run-out and stop-loss settlement statements,
2024 audit and records requests.

prior_subscriber_number   Bramwell subscriber number (eight digits).
prior_member_suffix       Bramwell member suffix. Bramwell wrote a member number as the subscriber number and the
                          suffix, NNNNNNNN-SS, on its cards, reports and data books. Bramwell gave dependents suffixes
                          in the order it enrolled them, and the suffixes were not carried over: compare person_code.
member_id                 Ellery member ID issued at conversion.
employee_number           District employee number of the subscriber.
person_code               Ellery person code at conversion.
relationship              SUB, SPS or DEP.
birth_date                Date of birth as received from Bramwell (MM/DD/YYYY). Ellery has corrected a few since;
                          the eligibility file carries the corrected date.
conversion_note           MERGED DUPLICATE PRIOR RECORD where Bramwell held one member under two records; both prior
                          numbers map to the one Ellery member ID.

Questions on these files: Tiffany Barrett, ext. 4417.
"""


def readme_txt(path):
    with open(path, "w", newline="\n") as f:
        f.write(README)
