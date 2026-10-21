"""The pack's documents: the HLS methods note (2025 edition), the field instruction that capped first-interview visits
for the 2026/27 field year and the one it replaced, the data dictionary and the survey data office's extract notes."""
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                           # noqa: E402
from reportlab.lib.pagesizes import A4                                     # noqa: E402
from reportlab.lib.styles import ParagraphStyle                            # noqa: E402
from reportlab.lib.units import mm                                         # noqa: E402
from reportlab.pdfbase import pdfmetrics                                   # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                               # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import records as R    # noqa: E402
import world as W      # noqa: E402

METHODS = "hls_methods_note_2025.pdf"
FI_2026 = "field_instruction_FI-2026-04_first_interview_visits.pdf"
FI_2024 = "field_instruction_FI-2024-03_call_pattern.pdf"
DICTIONARY = "hls_data_dictionary.md"
NOTES = "extract_notes_2026-10-20.md"

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LiberationSans", FONT_DIR + "LiberationSans-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSans-Bold", FONT_DIR + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif", FONT_DIR + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("LiberationSerif-Bold", FONT_DIR + "LiberationSerif-Bold.ttf"))
SANS, SANS_B, SERIF, SERIF_B = "LiberationSans", "LiberationSans-Bold", "LiberationSerif", "LiberationSerif-Bold"
INK = colors.HexColor("#1b1f24")
GREY = colors.HexColor("#5c636a")
RULE = colors.HexColor("#a3abb3")

# the office's field instructions: serif, numbered paragraphs
A_BODY = ParagraphStyle("abody", fontName=SERIF, fontSize=10.4, leading=14, textColor=INK, spaceAfter=5)
A_PARA = ParagraphStyle("apara", parent=A_BODY, leftIndent=30, firstLineIndent=-30)
A_H1 = ParagraphStyle("ah1", fontName=SERIF_B, fontSize=14, leading=18, textColor=INK, spaceAfter=3)
A_H2 = ParagraphStyle("ah2", fontName=SERIF_B, fontSize=10.8, leading=14, textColor=INK, spaceBefore=8, spaceAfter=3)
A_META = ParagraphStyle("ameta", fontName=SERIF, fontSize=8.8, leading=11.5, textColor=GREY, spaceAfter=9)
# the methods division's: sans
S_BODY = ParagraphStyle("sbody", fontName=SANS, fontSize=9.4, leading=12.8, textColor=INK, spaceAfter=5)
S_H1 = ParagraphStyle("sh1", fontName=SANS_B, fontSize=14, leading=17.5, textColor=INK, spaceAfter=2)
S_H2 = ParagraphStyle("sh2", fontName=SANS_B, fontSize=10, leading=13.5, textColor=INK, spaceBefore=8, spaceAfter=3)
S_META = ParagraphStyle("smeta", fontName=SANS, fontSize=8, leading=10.5, textColor=GREY, spaceAfter=7)
CELL = ParagraphStyle("cell", fontName=SANS, fontSize=8.6, leading=10.4, textColor=INK)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName=SANS_B)
A_CELL = ParagraphStyle("acell", fontName=SERIF, fontSize=9.4, leading=11.6, textColor=INK)
A_CELLB = ParagraphStyle("acellb", parent=A_CELL, fontName=SERIF_B)


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                             bottomMargin=20 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(top_left, top_right, foot):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(SERIF, 8)
        if top_left:
            canvas.drawString(22 * mm, A4[1] - 12 * mm, top_left)
            canvas.drawRightString(A4[0] - 22 * mm, A4[1] - 12 * mm, top_right)
        canvas.setFont(SANS, 7.4)
        canvas.drawString(22 * mm, 11 * mm, foot)
        canvas.drawRightString(A4[0] - 22 * mm, 11 * mm, "%d" % doc.page)
        canvas.restoreState()
    return draw


def _grid(rows, widths, style_head=CELLB, style=CELL, align_from=1, box=False):
    data = [[Paragraph(str(c), style_head if i == 0 else style) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=widths, hAlign="LEFT")
    cmds = [("ALIGN", (align_from, 0), (-1, -1), "RIGHT"), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]
    if box:
        cmds += [("BOX", (0, 0), (-1, -1), 0.6, INK), ("INNERGRID", (0, 0), (-1, -1), 0.3, RULE),
                 ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eceef0"))]
    else:
        cmds += [("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, -1), (-1, -1), 0.5, RULE)]
    t.setStyle(TableStyle(cmds))
    return t


# ------------------------------------------------------------------------------------------------- the scheme
def _p(text, style=S_BODY):
    return Paragraph(text, style)


def write_methods(path):
    head, title = W.PEOPLE["methods"]
    doc = _doc(path, "Household Labour Survey: methods note", head)
    s = [_p("Merrowland Statistics", S_META), _p("Household Labour Survey: methods note", S_H1),
         _p("2025 edition, March 2025. %s, %s, Methods and Quality Division." % (head, title), S_META)]
    sec = [
        ("1. Design", [
            "The Household Labour Survey (HLS) measures employment and unemployment among people aged 15 and over "
            "living in private dwellings. Each quarter a new intake of addresses is drawn from the address register, "
            "about 6,400 addresses spread across the six regions in proportion to their population.",
            "An address stays in the survey for five consecutive quarters (waves 1 to 5). The household found at the "
            "address is interviewed face to face at wave 1 and by telephone at waves 2 to 5. A household that cannot "
            "be interviewed at a telephone wave leaves the survey; the address is not returned to the field.",
            "Every quarter's sample is therefore made of five intakes, one at each wave, and about a fifth of the "
            "sample is replaced each quarter."]),
        ("2. Fieldwork", [
            "First interviews follow the current field instruction on the call pattern, which sets how many visits an "
            "interviewer makes before an address is returned as a non-contact and when they are made. Telephone "
            "interviews are arranged at the first interview and made in the reference week's following fortnight.",
            "Interviews are recorded on the face-to-face (CAPI) and telephone (CATI) systems. Visits to addresses "
            "issued for a first interview are logged on the interviewer's tablet in the call-record application; a "
            "visit is identified by the address serial and its visit number."]),
        ("3. Definitions", [
            "Employed: did any work for pay or profit in the reference week, or had a job they were temporarily away "
            "from. Unemployed: without a job, actively sought work in the last four weeks and available to start in "
            "the next two. Everyone else aged 15 and over is not in the labour force.",
            "The unemployment rate is the unemployed as a percentage of the labour force (employed plus unemployed). "
            "The employment rate is the employed as a percentage of the population aged 15 and over."]),
        ("4. Estimation", [
            "Each responding person receives a design weight, equal within a region. The weights are then raked "
            "(iterative proportional fitting, to convergence) to two sets of population controls for the quarter: "
            "the population aged 15 and over in each region, and in each of seven age groups (15 to 24, 25 to 34, "
            "35 to 44, 45 to 54, 55 to 64, 65 to 74, 75 and over) by sex. Every estimate the office publishes from the "
            "HLS uses the raked weights.",
            "The controls come from the office's population estimates and projections and are revised when the "
            "population base is rebased; a revision applies from the quarter stated in the controls file."]),
        ("5. Sampling error", [
            "Sampling error on the national unemployment rate is about 0.2 percentage point (95 per cent margin about "
            "0.4); on a quarter-on-quarter change it is somewhat smaller, the samples sharing four intakes.",
            "Errors from sources other than sampling are not quantified. Quarter-on-quarter changes are published "
            "unadjusted for seasonality."]),
        ("6. Flows", [
            "Labour market flows between two quarters are counted on the people interviewed in both, matched person to "
            "person within the household; a flow rate is the number moving from one status to another as a percentage "
            "of those in the first status, unweighted. People not interviewed in the second quarter are left out."]),
        ("7. Release", [
            "Quarterly estimates are released about six weeks after the quarter ends, rounded to one decimal place; "
            "changes and differences are computed from unrounded estimates and rounded independently. Revisions to "
            "earlier quarters are made only when the population controls are rebased."]),
    ]
    for h, paras in sec:
        s.append(_p(h, S_H2))
        s += [_p(x) for x in paras]
    doc.build(s, onFirstPage=_frame("", "", "Merrowland Statistics | HLS methods note | 2025 edition"),
              onLaterPages=_frame("", "", "Merrowland Statistics | HLS methods note | 2025 edition"))


def _instruction(path, ref, title, date, paras, superseded=None):
    who, role = W.PEOPLE["field"] if "2026" in ref else W.PEOPLE["field_2024"]
    doc = _doc(path, "Field instruction %s: %s" % (ref, title), who)
    s = [_p("MERROWLAND STATISTICS · FIELD OPERATIONS", A_META), _p("Field instruction %s" % ref, A_H1),
         _p(title, A_H2), _p("Issued %s by %s, %s. To: all field interviewers and team leaders." % (date, who, role), A_META)]
    if superseded:
        s.append(_p(superseded, A_META))
    for k, x in enumerate(paras, start=1):
        s.append(Paragraph("%d.&nbsp;&nbsp;&nbsp;%s" % (k, x), A_PARA))
    doc.build(s, onFirstPage=_frame("Field instruction " + ref, date, "Field Operations | internal"),
              onLaterPages=_frame("Field instruction " + ref, date, "Field Operations | internal"))


def write_fi_2026(path):
    _instruction(path, "FI-2026/04", "First-interview visits from 1 April 2026", "11 March 2026", [
        "This instruction replaces FI-2024/03 for addresses issued for a first interview from 1 April 2026.",
        "Make no more than three visits to an address issued for a first interview. If no one has been contacted by "
        "the end of the third visit, record the outcome of that visit and return the address as a non-contact. "
        "Addresses are not reissued.",
        "Keep the call pattern of FI-2024/03 for the visits you make: at least one visit in the evening or at a "
        "weekend, and the visits spread over at least ten days where the fieldwork period allows.",
        "Telephone interviews at waves 2 to 5 are unchanged.",
        "The change is made to bring face-to-face fieldwork within the field budget for the 2026/27 field year "
        "(1 April 2026 to 31 March 2027). The visit pattern for 2027/28 will be set with that year's field budget.",
    ])


def write_fi_2024(path):
    _instruction(path, "FI-2024/03", "Call pattern for first interviews", "4 March 2024", [
        "Make up to six visits to an address issued for a first interview before returning it as a non-contact.",
        "Make at least two of the visits in the evening (after 5 pm) or at a weekend, and spread the visits over at "
        "least three weeks where the fieldwork period allows.",
        "Log every visit in the call-record application at the address, including visits where no one answers. A "
        "visit at which you speak to a household member is a contact, whatever its outcome.",
        "Telephone interviews at waves 2 to 5 are arranged at the first interview.",
    ], superseded="Superseded for first interviews issued from 1 April 2026 by FI-2026/04.")


def write_dictionary(path):
    rows = [
        ("# HLS analysis files: data dictionary", None),
        ("Survey Data Office, Merrowland Statistics. Applies to the extract of 20 October 2026.", None),
        ("## hls_person_quarter_2023q1_2026q3.parquet", None),
        ("One row per person aged 15 and over in a responding household, per quarter.", None),
        ("| column | content |", None), ("|---|---|", None),
        ("| quarter | survey quarter, YYYYQn |", None),
        ("| serial | address serial (see the extract notes for the July to September 2026 format) |", None),
        ("| person_no | person's line number in the household roster at the interview |", None),
        ("| wave | 1 to 5, the address's quarter in the survey |", None),
        ("| mode | CAPI (face to face) or CATI (telephone) |", None),
        ("| region | region code: " + ", ".join("%s %s" % (c, W.RNAME[c]) for c in W.RCODES) + " |", None),
        ("| sex | 1 male, 2 female |", None),
        ("| date_of_birth | as reported |", None),
        ("| age | age at the middle of the quarter |", None),
        ("| ilo_status | 1 employed, 2 unemployed, 3 not in the labour force (methods note, section 3) |", None),
        ("| actual_hours | hours actually worked in the reference week, all jobs; blank if not employed |", None),
        ("| weight | final person weight for the quarter |", None),
        ("## " + R.CALLS, None),
        ("One row per call record uploaded from the call-record application, for addresses issued for a first "
         "interview in the intakes of January to March 2025 to July to September 2026. Visits at earlier intakes "
         "are on the field's paper call sheets and are not in the analysis files.", None),
        ("| column | content |", None), ("|---|---|", None),
        ("| record_id | call record id, assigned on upload |", None),
        ("| serial | address serial |", None),
        ("| intake | quarter the address was issued |", None),
        ("| area_code | interviewer area; region and district from the address register |", None),
        ("| interviewer | interviewer id |", None),
        ("| visit_no | the visit's number at the address |", None),
        ("| visit_start | local date and time the visit started |", None),
        ("| outcome | 110 interview, 210 refusal, 310 no reply, 410 not eligible (vacant, demolished or not residential) |", None),
        ("| uploaded | local date and time the record reached the server |", None),
        ("## " + R.REGISTER, None),
        ("One row per address issued for a first interview, January to March 2025 to July to September 2026: "
         "serial, intake, area_code, region, urban_rural, dwelling_type.", None),
    ]
    out = []
    for k, (line, _) in enumerate(rows):
        out.append(line)
        nxt = rows[k + 1][0] if k + 1 < len(rows) else ""
        if not (line.startswith("|") and nxt.startswith("|")):
            out.append("")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out).rstrip() + "\n")


def write_notes(path):
    who, role = W.PEOPLE["data"]
    lines = [
        "# HLS extract notes, 20 October 2026",
        "",
        "Prepared by %s (%s) for the Labour Market Statistics team. The July to September 2026 processing run locked "
        "on 20 October 2026; the files below are the extract taken that day." % (who, role),
        "",
        "## Files",
        "",
        "- `%s`: person-quarter analysis file, January to March 2023 to July to September 2026." % R.PERSON,
        "- `%s`: call records for first-interview addresses, intakes January to March 2025 to July to September 2026." % R.CALLS,
        "- `%s`: the addresses issued in the same intakes." % R.REGISTER,
        "- `%s`: population controls (Population Estimates and Projections)." % R.CONTROLS,
        "- `%s`: the release tables for April to June 2026." % R.RELEASE,
        "- `%s`: Jobseeker Support claimants by region and month (Ministry of Social Development extract)." % R.CLAIMANTS,
        "- `%s`: field interviewers by region, October 2026." % R.STAFFING,
        "- `%s`, `%s`, `%s`, `%s`." % (METHODS, FI_2026, FI_2024, DICTIONARY),
        "",
        "## Changes in this run",
        "",
        "- From the July to September 2026 processing run, address serials carry a check digit as a tenth character. "
        "Records from earlier runs keep the nine-character serial; the address register is unchanged.",
        "- July to September 2026 is the second quarter whose wave-1 intake was issued under FI-2026/04.",
        "",
        "## Not in this extract",
        "",
        "- Interviewer workload and pay records.",
        "- Visit histories for intakes before January to March 2025. The call-record application replaced the field's "
        "paper call sheets at the January to March 2025 intake and the paper sheets were never keyed.",
        "- The October to December 2026 intake (issued 1 October; first call records arrive with the next run).",
    ]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
