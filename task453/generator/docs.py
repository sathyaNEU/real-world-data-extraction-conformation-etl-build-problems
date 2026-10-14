"""The pack's two documents: the Office's methodology note on the redesigned questionnaire (issued before the
introduction began) and the extract of the Regional Employment Support Act 2021, consolidated to 1 July 2025."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import world as W   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("LiberationSerif", "Regular"), ("LiberationSerif-Bold", "Bold"), ("LiberationSerif-Italic", "Italic"),
              ("LiberationSans", "Regular"), ("LiberationSans-Bold", "Bold"), ("LiberationSans-Italic", "Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + nm.split("-")[0] + "-" + f + ".ttf"))
INK = colors.HexColor("#1b1d20")
GREY = colors.HexColor("#5b6067")
TEAL = colors.HexColor("#0f4c5c")
S_BODY = ParagraphStyle("b", fontName="LiberationSans", fontSize=9.6, leading=13.6, textColor=INK, spaceAfter=6)
S_H1 = ParagraphStyle("h1", fontName="LiberationSans-Bold", fontSize=15, leading=19, textColor=TEAL, spaceAfter=4)
S_SUB = ParagraphStyle("sub", fontName="LiberationSans", fontSize=9.5, leading=13, textColor=GREY, spaceAfter=12)
S_H2 = ParagraphStyle("h2", fontName="LiberationSans-Bold", fontSize=10.5, leading=14, textColor=TEAL, spaceBefore=8,
                      spaceAfter=3)
S_CELL = ParagraphStyle("c", fontName="LiberationSans", fontSize=8.6, leading=11, textColor=INK)
L_BODY = ParagraphStyle("lb", fontName="LiberationSerif", fontSize=10.5, leading=14.5, textColor=INK, spaceAfter=6)
L_NUM = ParagraphStyle("ln", parent=L_BODY, leftIndent=22, firstLineIndent=-22)
L_SUB = ParagraphStyle("ls", parent=L_BODY, leftIndent=40, firstLineIndent=-18)
L_DEF = ParagraphStyle("ld", parent=L_BODY, leftIndent=40)
L_H1 = ParagraphStyle("lh1", fontName="LiberationSerif-Bold", fontSize=13.5, leading=17, textColor=INK, alignment=1,
                      spaceAfter=3)
L_CAP = ParagraphStyle("lc", fontName="LiberationSerif-Italic", fontSize=9.5, leading=12.5, textColor=GREY,
                       alignment=1, spaceAfter=14)
L_H2 = ParagraphStyle("lh2", fontName="LiberationSerif-Bold", fontSize=11, leading=15, textColor=INK, spaceBefore=7,
                      spaceAfter=4)


def _doc(path, title, author, footer, serif=False):
    def frame(canvas, doc):
        canvas.saveState()
        canvas.setFont("LiberationSerif" if serif else "LiberationSans", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(20 * mm, 12 * mm, footer)
        canvas.drawRightString(A4[0] - 20 * mm, 12 * mm, "%d" % doc.page)
        canvas.restoreState()
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                          bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")
    return d, frame


def write_note(path):
    title = "Labour Force Survey: the redesigned questionnaire and its introduction"
    doc, frame = _doc(path, title, "Labour Market Methods", "%s  |  Methodology note LMM 2025/04" % W.OFFICE)
    P = lambda t, s=S_BODY: Paragraph(t, s)
    s = [P(title, S_H1),
         P("Methodology note LMM 2025/04. Labour Market Methods, %s. Issued 16 June 2025. Author: %s." %
           (W.OFFICE, W.PEOPLE["methods"]), S_SUB),
         P("1  The survey", S_H2),
         P("The Labour Force Survey interviews the residents of about 85,000 private dwellings each month. The sample "
           "is drawn in primary sampling units, and within each unit in six rotation groups of about twelve sample "
           "references each (from nine to fifteen, depending on the size of the blocks). A dwelling stays in the sample for six consecutive months. Each month the dwellings of one "
           "rotation group complete their sixth interview and are replaced by newly selected dwellings in the same "
           "primary sampling units: group A's dwellings are replaced in January and July, group B's in February and August, and so on to group "
           "F's in June and December. The first interview is conducted face to face where possible and the later ones "
           "by telephone."),
         P("Each rotation group is weighted to the population aged 15 and over by region, sex and age band (the "
           "population benchmarks), so each group's weighted totals estimate the whole population. A published "
           "estimate is the average of the six rotation groups' estimates, and a published rate is the ratio of two "
           "such averages."),
         P("2  The redesigned questionnaire", S_H2),
         P("The labour force questions have been revised following the 2023 user consultation. Job search is asked as "
           "the specific active steps a person took in the last four weeks rather than as one general question, with "
           "the steps listed for the interviewer. From a dwelling's second interview the interviewer reads back each "
           "person's previous answers about work and job search and asks whether they still apply, recording a change "
           "only where the person reports one (dependent interviewing). The questions on employment and hours are "
           "unchanged. The redesigned questionnaire runs on the integrated collection system (ICS); the previous "
           "questionnaire runs on CAI 2014."),
         P("3  Introduction", S_H2),
         P("The redesigned questionnaire will be introduced with the rotation group replaced in July 2025. Dwellings "
           "entering the sample from July 2025 will be interviewed on it for all six of their interviews, and "
           "dwellings already in the sample will complete their interviews on the previous questionnaire in CAI 2014. "
           "The previous questionnaire therefore leaves the field with the November 2025 interviews, and from December "
           "2025 every rotation group will answer the redesigned questionnaire. Published estimates for July to "
           "November 2025 will combine the rotation groups answering each questionnaire, as the six groups stand in "
           "each month."),
         P("Both systems export estimation cells (weighted persons by region, rotation group, sex, age band and labour "
           "force status) to the estimation database: CAI 2014 for the groups answering the previous questionnaire, "
           "ICS for the groups answering the redesigned one."),
         P("4  The series on the redesigned basis", S_H2),
         P("The Regional Employment Support Act 2021 requires the Government Statistician to determine the change "
           "the redesigned questionnaire makes to the published unemployment rate before the first designation that "
           "reads rates measured on it. Once that change is determined the Office will publish the regional series on "
           "the redesigned basis from January 2024, to one decimal place as the release publishes it. Each month "
           "before July 2025 is restated by adding the change as the determination states it, in percentage points "
           "to one decimal place, to the rate as published, for every region alike: regional samples are too small "
           "to estimate a change region by region. July to November 2025, when both questionnaires were in the "
           "field, are carried as published and marked as the transition; from December 2025 the published rates "
           "are on the redesigned basis."),
         P("5  Regional classification", S_H2),
         P("The 2025 regional classification applies from January 2025. Its review renumbered the nine regions in a "
           "north-to-south order without changing their boundaries; the concordance with the 2019 classification is "
           "supplied with the estimation files."),
         P("6  Contacts", S_H2),
         P("Questions on this note: Labour Market Methods (%s). Survey operations: %s." %
           (W.PEOPLE["methods"], W.PEOPLE["operations"]))]
    doc.build(s, onFirstPage=frame, onLaterPages=frame)


def write_act(path):
    doc, frame = _doc(path, W.ACT, "Parliamentary Counsel Office",
                      "%s  |  Consolidated to 1 July 2025  |  Extract: sections 1 to 10" % W.ACT, serif=True)
    s = [Paragraph(W.ACT.upper(), L_H1),
         Paragraph("Consolidated to 1 July 2025. Extract of Part 1 (sections 1 to 10); Parts 2 to 4 (the regional wage "
                   "subsidy, payments and review) are not reproduced. This consolidation is not an official version.",
                   L_CAP)]
    N = lambda n, t: s.append(Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (n, t), L_NUM))
    M = lambda n, t: s.append(Paragraph("(%s)&nbsp;&nbsp;%s" % (n, t), L_SUB))
    D = lambda t: s.append(Paragraph(t, L_DEF))
    s.append(Paragraph("Part 1  Designation of regions", L_H2))
    N("1", "<b>Title.</b> This Act is the Regional Employment Support Act 2021.")
    N("2", "<b>Purpose.</b> The purpose of this Act is to direct the regional wage subsidy to regions where "
           "unemployment is high, as measured by the Labour Force Survey.")
    N("3", "<b>Interpretation.</b> In this Act,")
    D("<b>Labour Force Survey</b> means the household survey of the labour force conducted by the Government "
      "Statistician;")
    D("<b>region</b> means a region of the regional classification the Government Statistician uses for the Labour "
      "Force Survey;")
    D("<b>twelve-month average</b>, for a region and a calendar year, means the mean of the region's unemployment rates "
      "for the twelve months of that year;")
    D("<b>unemployment rate</b>, for a region or for the country and a month, means the rate of unemployment of persons "
      "aged 15 and over in that region or in the country in that month as published by the Government Statistician "
      "from the Labour Force Survey, to one decimal place.")
    N("4", "<b>Minister to designate.</b> The Minister must designate regions under section 7 for each year beginning "
           "on 1 April.")
    N("5", "<b>Publication.</b> The Minister must publish each designation in the Gazette before 1 April of the year to "
           "which it applies.")
    N("6", "<b>Consultation.</b> Before designating, the Minister must consult the Government Statistician on the "
           "unemployment rates the designation reads.")
    N("7", "<b>Designation.</b>")
    M("1", "The Minister must designate, for the year beginning on 1 April, every region whose twelve-month average for "
           "the preceding calendar year is at or above the trigger rate.")
    M("2", "A designation continues until the next designation is made.")
    N("8", "<b>Trigger rate.</b> The trigger rate is 6.0 per cent, or the rate as restated under section 9.")
    N("9", "<b>Restatement after a change to the survey.</b>")
    M("1", "Where the Government Statistician changes the Labour Force Survey in a way that changes the unemployment "
           "rates it publishes, the Government Statistician must, before the first designation that reads unemployment "
           "rates measured on the changed survey, determine and publish a restated trigger rate.")
    M("2", "The restated trigger rate is the trigger rate in force plus the number of percentage points by which the "
           "national unemployment rate published from the changed survey, once the change is in full use, differs from "
           "the rate the survey before the change would have published for the same months, rounded to one decimal "
           "place.")
    M("3", "The restated trigger rate applies to every designation made after its publication.")
    N("10", "<b>Regions.</b> Where the regional classification changes, a designation reads each region's unemployment "
            "rates on the classification in use for the year it reads.")
    doc.build(s, onFirstPage=frame, onLaterPages=frame)
