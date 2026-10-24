"""The pack's documents: the Master Subscription Agreement (docx), the contractor's technical report, the professional
learning catalog and the billing system's credit memo import layout (pdf)."""
import datetime as dt

import docx
from docx.shared import Pt
import reportlab.rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, PageBreak

import world as W
import records as R
import pd as PD

reportlab.rl_config.invariant = 1

MSA = [
    ("h", "1. Definitions"),
    ("p", "1.1 “District” means the school district or system named on an Order Form. “Order Form” means the "
          "ordering document signed by the District and Lumenfold that states the Subscription Term, the Subscription "
          "Fee, the licensed seats, the hours of live professional learning, the Guarantee Benchmark and the Credit "
          "Percentage."),
    ("p", "1.2 “Subscription Term” means the period stated on the Order Form. “Subscription Fee” means the annual "
          "subscription fee stated on the Order Form for the Subscription Term, before any credit."),
    ("p", "1.3 “Assessment” means the Lumenfold Science Outcomes Assessment, administered online each spring to the "
          "students in the District's Lumenfold class sections, with the reporting scale and performance levels set out "
          "in the Assessment's technical report for that spring."),
    ("h", "2. Subscription and access"),
    ("p", "2.1 Lumenfold provides the District's students and teachers access to the Lumenfold platform for the "
          "Subscription Term for up to the licensed seats."),
    ("p", "2.2 The District uploads its class rosters and the student fields listed in section 11 at least once each "
          "term, and whenever students join its Lumenfold class sections."),
    ("h", "3. Fees and invoicing"),
    ("p", "3.1 Lumenfold invoices the Subscription Fee in advance, annually or in two equal semester instalments as the "
          "Order Form provides. 3.2 Invoices are due 45 days from the invoice date."),
    ("h", "8. Professional learning"),
    ("p", "8.1 Lumenfold delivers to the District the hours of live professional learning stated on the Order Form "
          "within the Subscription Term. Live professional learning is a session led by a Lumenfold facilitator, "
          "virtual or on site, attended by the District's teachers; recorded webinars and on-demand courses do not "
          "count toward the hours."),
    ("p", "8.2 A live session delivered to teachers of more than one district counts in full toward the hours of each "
          "district whose teachers attended it."),
    ("p", "8.3 Where the live professional learning delivered to the District within the Subscription Term, counted to "
          "the nearest half hour, falls short of the hours stated on the Order Form, Lumenfold credits the District USD "
          "250 for each hour of the shortfall."),
    ("h", "9. Outcomes guarantee"),
    ("p", "9.1 An “Eligible Student” is a student rostered to one of the District's Lumenfold class sections on 1 May "
          "2026 who completed at least 20 Lumenfold lessons from the start of the Subscription Term to 1 May 2026, as "
          "recorded in Lumenfold's guarantee eligibility file for the 2025-26 Subscription Term."),
    ("p", "9.2 The District's “Outcome Share” is the percentage of its Eligible Students who completed the spring "
          "2026 Assessment whose science achievement, on the Assessment's reporting scale, is at or above the "
          "Proficient level for their grade: 500 in grade 6, 520 in grade 7 and 540 in grade 8."),
    ("p", "9.3 If the District's Outcome Share is below the Guarantee Benchmark on its Order Form, Lumenfold credits "
          "the District the Credit Percentage on its Order Form of its 2025-26 Subscription Fee."),
    ("p", "9.4 Lumenfold sends the District a settlement statement for the 2025-26 Subscription Term by 30 November "
          "2026 and issues any credit under section 10 with it."),
    ("h", "10. Credits"),
    ("p", "10.1 Lumenfold applies a credit owed under section 8 or section 9 against the District's open subscription "
          "invoice for the following Subscription Term. Where no such invoice is open when the credit is issued, "
          "Lumenfold refunds the credit to the District within 30 days."),
    ("h", "11. Student data"),
    ("p", "11.1 The District shares, for each rostered student, the student's grade, economic disadvantage status, "
          "English learner status, disability status and performance level on the state's most recent mathematics or "
          "science assessment, under the data sharing addendum. Lumenfold and its assessment contractor use these "
          "fields for the Assessment and for Lumenfold's efficacy research."),
    ("h", "14. General"),
    ("p", "14.1 This Agreement and the Order Form are the entire agreement between the parties for the Subscription "
          "Term. 14.2 Where this Agreement and an Order Form conflict, the Order Form governs."),
]


def _core(d, author, when):
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.created = when
    cp.modified = when
    cp.revision = 6
    cp.title = ""
    cp.comments = ""


def msa_docx(path):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    d.add_heading("Lumenfold Learning, Inc. Master Subscription Agreement", level=1)
    d.add_paragraph("Version 4.0, effective 1 June 2025. Incorporated by reference in each 2025-26 Order Form. "
                    "Sections 4 to 7, 12 and 13 (privacy, security, acceptable use, warranties, liability and "
                    "termination) are unchanged from version 3.2 and are not reproduced here.")
    for kind, text in MSA:
        if kind == "h":
            d.add_heading(text, level=2)
        else:
            d.add_paragraph(text)
    _core(d, "Legal", dt.datetime(2025, 5, 28, 16, 40))
    d.save(path)


def _pdf(path, title, story, author, producer):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.7 * inch, bottomMargin=0.7 * inch, title=title, author=author, creator=author,
                            subject=title, producer=producer)

    def footer(canvas, doc_):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.75 * inch, 0.45 * inch, title)
        canvas.drawRightString(letter[0] - 0.75 * inch, 0.45 * inch, "Page %d" % doc_.page)
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def _table(rows, widths=None, fs=7.5, align_from=1):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", fs), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", fs),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.5, colors.black),
                           ("ALIGN", (align_from, 1), (-1, -1), "RIGHT"),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                           ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    return t


def tech_report_pdf(path, T):
    """Caldrith's technical report for the spring 2026 administration. T: the figures it reports."""
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontSize=9, leading=12, spaceAfter=5)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=11.5, spaceBefore=8, spaceAfter=4)
    cap = ParagraphStyle("c", parent=ss["Normal"], fontSize=8, leading=10, spaceBefore=4, spaceAfter=2,
                         fontName="Helvetica-Bold")
    src = ParagraphStyle("s", parent=ss["Normal"], fontSize=7, leading=9, textColor=colors.HexColor("#444444"))
    P = lambda t: Paragraph(t, body)
    s = [Paragraph("Lumenfold Science Outcomes Assessment", ss["Title"]),
         Paragraph("Spring 2026 Administration: Technical Report", ss["Heading2"]),
         P("Prepared for Lumenfold Learning, Inc. by Caldrith Assessment Partners. Final, 19 June 2026. This report "
           "documents the design, scoring and scaling of the spring 2026 administration and the results reported in "
           "Lumenfold's 2026 National Efficacy Report."),
         Paragraph("1. The administration", h2),
         P("The Lumenfold Science Outcomes Assessment (LSOA) measures the science achievement of students in grades 6, "
           "7 and 8 in Lumenfold's partner districts. The spring 2026 window ran from 13 April to 22 May 2026. "
           "%s students in %d partner districts in six states submitted a session; Table 1 gives the counts by "
           "grade and state." % ("{:,}".format(T["n_tested"]), len(W.DISTRICTS))),
         Paragraph("2. Design", h2),
         P("The item pool has 40 dichotomously scored items in eight modules of five. Each student takes two modules, "
           "so each of the 28 two-module forms is one pairing of modules; forms are spiralled within class sections, "
           "so every form is taken by students of every grade, state and district. A student's assessment is a "
           "single online session in Caldrith's delivery system. A session is scored when the student submits it. "
           "A session that is not submitted before the student's class closes the window is not scored; the student "
           "may begin a new session on the same form, which is scored if submitted."),
         P("Within a submitted session, an item the student left blank with a later item answered is omitted and is "
           "scored incorrect. Items left blank at the end of the session, after the last item the student answered, "
           "are not reached and are treated as not administered."),
         Paragraph("3. Scaling and the reporting scale", h2),
         P("Items are scaled with the two-parameter logistic model, P(correct) = 1 / (1 + exp(-a(theta - b))), with "
           "the scaling constant D = 1. Item parameters are fixed at the values from the 2024 base-year calibration "
           "(the file caldrith_item_parameters_2024.csv); the 2026 administration is not recalibrated. On the "
           "base-year scale theta has mean 0 and standard deviation 1 in the 2024 calibration sample. Scale scores are "
           "reported as 500 + 50 theta."),
         P("The 2024 standard setting set the Proficient level at 500 in grade 6, 520 in grade 7 and 540 in grade 8, "
           "and the Advanced level at 560, 580 and 600."),
         Paragraph("4. Population model and plausible values", h2),
         P("Each student answers ten items, too few to report a score for the student. The results in this report "
           "are estimated from a population model: a latent regression of theta on the conditioning variables in Table 6, "
           "theta = gamma'x + e with e normal with mean 0 and a common variance, fitted to every submitted session by "
           "marginal maximum likelihood with the EM algorithm on a quadrature grid of 179 points from -4.475 to "
           "4.475 with the item parameters fixed. The prior state-test band is read from the districts' roster "
           "uploads through the crosswalk in Table 5; students with no prior state-test result form their own "
           "category."),
         P("For each student Caldrith drew five plausible values from the posterior distribution of theta given "
           "the student's responses and conditioning variables, and reports them on the scale to one decimal "
           "(caldrith_plausible_values_2026.csv). Each result in Table 8 is computed five times, once with each "
           "plausible value, and the five results are averaged; its standard error combines the average sampling "
           "variance with the variance between the five results (Rubin, 1987)."),
         Paragraph("5. Results", h2),
         P("Table 8 gives the percentage of students at or above Proficient for their grade and the mean scale score "
           "for the partner districts' students and for the groups in the 2026 National Efficacy Report.")]
    # Table 1
    rows = [["State", "Districts", "Grade 6", "Grade 7", "Grade 8", "All"]]
    for st in W.STATES:
        c = T["counts"][st]
        rows.append([W.STATE_NAME[st], str(T["n_dist"][st])] + ["{:,}".format(x) for x in c] + ["{:,}".format(sum(c))])
    tot = [sum(T["counts"][st][k] for st in W.STATES) for k in range(3)]
    rows.append(["All", str(len(W.DISTRICTS))] + ["{:,}".format(x) for x in tot] + ["{:,}".format(sum(tot))])
    s += [Paragraph("Table 1. Students with a submitted session, by state and grade", cap), _table(rows),
          Paragraph("Source: Caldrith delivery system, sessions submitted 13 April to 22 May 2026.", src)]
    # Table 5
    rows = [["State", "State test", "Band 1", "Band 2", "Band 3", "Band 4"]]
    for st in W.STATES:
        name, lv = R.LEVELS[st]
        rows.append([W.STATE_NAME[st], name] + [", ".join(x) for x in lv])
    s += [Paragraph("Table 5. Prior state-test performance levels by band", cap),
          _table(rows, widths=[62, 78, 82, 78, 82, 88], fs=7, align_from=9),
          Paragraph("Bands are read from the most recent state science or mathematics result in the roster upload.",
                    src)]
    # Table 6
    rows = [["Conditioning variable", "Category", "Coefficient (scale points)"]]
    for lab, cat, val in T["gamma_rows"]:
        rows.append([lab, cat, ("%.1f" if lab == "Grade" else "%+.1f") % val])
    rows.append(["Residual standard deviation", "", "%.1f" % T["resid_sd"]])
    s += [Paragraph("Table 6. Population model: conditioning variables and estimated coefficients", cap),
          _table(rows, widths=[150, 150, 110]),
          Paragraph("Grade terms are the grade means for a student in North Carolina, band 1, with none of the three "
                    "status flags; the other coefficients are differences from that student.", src)]
    # Table 8
    rows = [["Group", "Students", "At or above Proficient (%)", "Mean scale score"]]
    for lab, n, pct, mean in T["results"]:
        rows.append([lab, "{:,}".format(n), "%.1f" % pct, "%.1f" % mean])
    s += [Paragraph("Table 8. Results, spring 2026", cap), _table(rows, widths=[170, 70, 110, 90]),
          Paragraph("Averages over the five plausible values. Proficient: 500, 520 and 540 in grades 6, 7 and 8.",
                    src)]
    _pdf(path, "LSOA Spring 2026 Technical Report", s, "Caldrith Assessment Partners", "Caldrith Assessment Partners")


def catalog_pdf(path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontSize=9, leading=12, spaceAfter=5)
    small = ParagraphStyle("t", parent=ss["Normal"], fontSize=7.5, leading=9)
    s = [Paragraph("Lumenfold Professional Learning Catalog, 2025-26", ss["Title"]),
         Paragraph("Partner Success, July 2025. Offerings are booked through your district's partner success manager; "
                   "sessions are scheduled with the district and appear on the district's professional learning "
                   "record when delivered.", body), Spacer(1, 6)]
    rows = [["Code", "Offering", "Format", "Sessions", "Hours per session", "Total hours"]]
    for code, title, fmt, n, h in PD.CATALOG:
        rows.append([code, Paragraph(title, small), fmt, str(n) if fmt in PD.LIVE else "", "%d" % h if fmt in PD.LIVE else "",
                     "%d" % (n * h)])
    s.append(_table(rows, widths=[46, 190, 82, 46, 66, 56], fs=7.5, align_from=3))
    s += [Spacer(1, 8),
          Paragraph("Series (Inquiry Labs, Coaching Cycle, Assessment for Learning) are booked as one offering and "
                    "scheduled as their sessions, two to four weeks apart. The Summer Science Institute runs in July on "
                    "two consecutive days, booked by day. Facilitators record each session's hours on the district's "
                    "professional learning record when it closes. Recorded webinars and on-demand courses are "
                    "self-paced and available all year; their hours are the running time.", body)]
    _pdf(path, "Professional Learning Catalog 2025-26", s, "Partner Success", "Lumenfold Partner Success")


def layout_pdf(path):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontSize=9, leading=12, spaceAfter=5)
    small = ParagraphStyle("t", parent=ss["Normal"], fontSize=7.5, leading=9)
    s = [Paragraph("Credit Memo Import: File Layout", ss["Title"]),
         Paragraph("Billing Operations, revision 3, 4 August 2026. Credit memos for customer accounts are loaded "
                   "into the billing system from a comma-separated file with a header row, one row per credit.",
                   body), Spacer(1, 4)]
    rows = [["Column", "Format", "Content"],
            ["memo_reference", "text", Paragraph("Reason code, the term and the four digits of the partner ID, "
                                                 "e.g. OG-2526-1234. Unique in the file.", small)],
            ["customer_account", "text", Paragraph("The account the credit memo posts to: the bill-to account on the "
                                                   "order form under which the credit was earned.", small)],
            ["reason_code", "OG or PL", Paragraph("OG: outcomes guarantee credit (MSA section 9). PL: professional "
                                                  "learning shortfall credit (MSA section 8.3).", small)],
            ["credit_amount", "0.00", Paragraph("The credit in US dollars, positive, two decimals.", small)],
            ["apply_to_invoice", "text", Paragraph("The invoice the credit is applied to: of the open subscription "
                                                   "invoices for the following subscription term on the same customer "
                                                   "account, the one with the earliest due date. Blank when the credit "
                                                   "is refunded.", small)],
            ["refund_method", "APPLY or CHECK", Paragraph("APPLY when the credit is applied to an invoice; CHECK when "
                                                          "it is refunded by check.", small)],
            ["credit_date", "YYYY-MM-DD", Paragraph("The date the credit memo is issued.", small)]]
    s.append(_table(rows, widths=[90, 80, 300], fs=7.5, align_from=9))
    s += [Spacer(1, 8),
          Paragraph("Rows are sorted by memo_reference. The import rejects a file with a duplicate memo_reference, a "
                    "credit applied to an invoice on another account, or a blank apply_to_invoice with APPLY.", body)]
    _pdf(path, "Credit Memo Import Layout", s, "Billing Operations", "Lumenfold Billing Operations")
