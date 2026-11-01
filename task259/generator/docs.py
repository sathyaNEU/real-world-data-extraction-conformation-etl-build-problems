"""The documents in the pack: the department's administrative rule, the survey's technical note and its quarterly
release. Each states what its organisation states; none explains a file."""
import datetime
import os

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from reportlab import rl_config
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import common
import world

rl_config.invariant = 1

RULE_FILE = "TAR_24-30-104_PORTABLE_BENEFITS_PILOT_AREAS.docx"
NOTE_FILE = "HES_TECHNICAL_NOTE_2026-09.pdf"
RELEASE_FILE = "HES_RELEASE_2026Q3_PRELIMINARY.pdf"


def write_documents(W, tdir):
    write_rule(os.path.join(tdir, RULE_FILE))
    write_note(os.path.join(tdir, NOTE_FILE))
    write_release(W, os.path.join(tdir, RELEASE_FILE))


# ------------------------------------------------------------------------------------------------ the rule
def write_rule(path):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(11)

    def para(text, bold=False, center=False, size=None, space=6):
        p = d.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if center:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(space)
        return p

    para("TAMARACK ADMINISTRATIVE RULES", bold=True, center=True, size=12, space=2)
    para("TITLE 24  LABOR AND INDUSTRY", center=True, space=2)
    para("CHAPTER 30  PORTABLE BENEFITS PILOT", center=True, space=12)

    para("24.30.101  PURPOSE", bold=True)
    para("(1) This chapter implements 39-71-1204, Tamarack Code Annotated, which directs the department to run a "
         "portable benefits pilot for workers who hold more than one job, in workforce development areas certified "
         "under this chapter, for the pilot year beginning 1 January 2027.")
    para("24.30.102  DEFINITIONS", bold=True)
    para("As used in this chapter, the following definitions apply:")
    para("(1) \"Employed resident\" means a person aged 16 or over who lives in a housing unit in the workforce "
         "development area and who, in the survey reference week, did any work for pay or profit or had a job from "
         "which the person was temporarily absent.")
    para("(2) \"Holds more than one job\" means that, in the survey reference week, the employed resident had two or "
         "more jobs at the same time, counting self-employment as a job.")
    para("(3) \"Survey\" means the Tamarack Household Employment Survey conducted by the department's Labor Market "
         "Information Bureau.")
    para("(4) \"Workforce development area\" means an area designated under ARM 24.10.201 as the designation stood "
         "on 1 July 2026.")
    para("24.30.104  PILOT AREAS", bold=True)
    para("(1) The department shall certify as a pilot area for the 2027 pilot year each workforce development area "
         "in which at least 7.0 percent of employed residents hold more than one job.")
    para("(2) The percentage in (1) is estimated from the survey for the four calendar quarters ending 30 September "
         "2026, with each employed resident counted once in each quarter in which the resident's household was "
         "interviewed, using the survey's final weights.")
    para("(3) Whether an employed resident holds more than one job is counted as that resident would report it "
         "themselves.")
    para("24.30.105  CERTIFICATION", bold=True)
    para("(1) The commissioner shall certify the pilot areas by 1 December 2026 on the written recommendation of the "
         "Labor Market Information Bureau, which shall state for each workforce development area whether it "
         "qualifies under ARM 24.30.104.")
    para("(2) A certification is not revised during the pilot year.")
    para("History: 39-71-1204, MCA; IMP, 39-71-1204, MCA; NEW, 2026 TAR p. 1417, Eff. 9/4/26.", space=2)
    common.docx_props(d, "TDLI Legal Services", "ARM 24.30.101 to 24.30.105", created=(2026, 8, 28, 10, 12),
                      modified=(2026, 9, 4, 9, 30))
    d.save(path)
    common.normalise_zip(path, "2026-09-04T15:30:00Z", "Microsoft Office Word")


# ---------------------------------------------------------------------------------------------------- PDFs
def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=6)
    head = ParagraphStyle("h", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=10.5, leading=13,
                          spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle("t", parent=ss["Normal"], fontName="Helvetica-Bold", fontSize=14, leading=17, spaceAfter=4)
    small = ParagraphStyle("s", parent=ss["Normal"], fontName="Helvetica", fontSize=8, leading=10, spaceAfter=4)
    return body, head, title, small


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=0.9 * inch, rightMargin=0.9 * inch,
                             topMargin=0.8 * inch, bottomMargin=0.8 * inch, title=title, author=author,
                             creator="LMIB publishing", subject="", invariant=1)


def write_note(path):
    body, head, title, small = _styles()
    s = []
    s.append(Paragraph("Tamarack Household Employment Survey", title))
    s.append(Paragraph("Technical note, September 2026. Labor Market Information Bureau, Tamarack Department of Labor "
                       "and Industry", small))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Scope", head))
    s.append(Paragraph(
        "The survey covers the civilian population aged 16 and over living in housing units in Tamarack. People living "
        "in group quarters (dormitories, nursing facilities, correctional facilities, work camps) are out of scope. "
        "Estimates are published for the state and for its eight workforce development areas.", body))
    s.append(Paragraph("Sample", head))
    s.append(Paragraph(
        "Addresses are selected each quarter from the state's master address file, separately in each workforce "
        "development area. An address stays in the sample for four consecutive quarters and then leaves it; each "
        "quarter one rotation group enters and one leaves, so three quarters of the addresses in sample in one quarter "
        "were also in sample the quarter before. Smaller areas are sampled at higher rates so that every area "
        "yields estimates.", body))
    s.append(Paragraph("Interviewing", head))
    s.append(Paragraph(
        "The reference week is the calendar week, Sunday through Saturday, that contains the 12th day of the middle "
        "month of the quarter. Interviewers contact households in the two weeks after the reference week. The first "
        "interview at an address is by personal visit; later interviews are by personal visit or by telephone. Any "
        "household member aged 16 or over may answer for the household, and the person answering also gives the "
        "information for household members aged 16 or over who are not at home when the interview takes place. "
        "Questions about work refer to the reference week.", body))
    s.append(Paragraph("Weighting", head))
    s.append(Paragraph(
        "Each person in an interviewed household receives a final weight in three steps: a base weight equal to the "
        "housing units on the frame per address in sample, by area and quarter; an adjustment that spreads the "
        "weight of eligible households not interviewed over the households interviewed in the same area and quarter; "
        "and a ratio adjustment to the State Demographer's projections of adults aged 16 and over for the quarter, "
        "by area, age group and sex (July 2025 vintage). Final weights for the third quarter of 2026 were reissued on 16 October 2026 "
        "after the State Demographer revised the July 2025 estimate for Southwest Lakes; the reissued weights "
        "replace the first issue.", body))
    s.append(Paragraph("Response rates", head))
    s.append(Paragraph(
        "The household response rate is the number of interviewed households as a percent of eligible housing units, "
        "with each housing unit in sample counted once in each quarter. A housing unit is eligible in a quarter if it "
        "stood on the master address file on the date of the interviewer's visit and the interviewer did not find it "
        "vacant, demolished or not a housing unit. The master address file is taken as finally corrected: a removal "
        "later reversed as made in error counts as never having been made, from the date of the removal. The "
        "noncontact rate is the number of eligible housing units at which no one was at home at any contact, as a "
        "percent of eligible housing units.", body))
    s.append(Paragraph("Change of interviewing system", head))
    s.append(Paragraph(
        "From the second quarter of 2026 interviews are recorded in the department's new computer-assisted "
        "interviewing system (CAPI 2026), which went live on 27 April 2026. Household case numbers were reissued at "
        "the change, and disposition codes were renumbered. Questionnaire content did not change.", body))
    s.append(Paragraph("Reliability", head))
    s.append(Paragraph(
        "Survey estimates are subject to sampling and nonsampling error. Area estimates for a single quarter rest on "
        "a few hundred interviewed households and should be read with care; estimates for four quarters combined are "
        "more reliable.", body))
    s.append(Spacer(1, 8))
    s.append(Paragraph("Contact: Kylie Taylor, Survey Operations, Labor Market Information Bureau.", small))
    _doc(path, "HES technical note 2026", "LMIB").build(s)
    common.scrub_pdf(path, "20260921142000-06'00'", "TDLI LMIB publishing")


def write_release(W, path):
    """Statewide estimates as collected, on the weights in place at release (2 October 2026, before the reissue)."""
    body, head, title, small = _styles()
    rows = release_table(W)
    s = []
    s.append(Paragraph("Household Employment Survey: third quarter 2026 (preliminary)", title))
    s.append(Paragraph("Released 2 October 2026. Labor Market Information Bureau, Tamarack Department of Labor and "
                       "Industry", small))
    s.append(Spacer(1, 6))
    q3 = rows[-1]
    s.append(Paragraph(
        "Tamarack's household survey estimates %s thousand residents aged 16 and over were employed in the third "
        "quarter of 2026, and the unemployment rate was %s percent. The tables below are not seasonally adjusted; "
        "quarter-to-quarter movements partly reflect the season." % (q3[3], q3[4]), body))
    data = [["Quarter", "Population 16+\n(thousands)", "Labor force\n(thousands)", "Employed\n(thousands)",
             "Unemployment\nrate (%)", "Multiple jobholders\n(thousands)", "Multiple jobholders,\n% of employed"]]
    for r in rows:
        data.append(list(r))
    t = Table(data, colWidths=[0.75 * inch, 0.95 * inch, 0.9 * inch, 0.85 * inch, 0.9 * inch, 1.1 * inch, 1.1 * inch])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 7.5), ("FONT", (0, 1), (-1, -1), "Helvetica", 8.5),
                           ("ALIGN", (1, 0), (-1, -1), "RIGHT"), ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.black), ("VALIGN", (0, 0), (-1, 0), "BOTTOM")]))
    s.append(t)
    s.append(Spacer(1, 6))
    s.append(Paragraph(
        "Multiple jobholders are employed residents who had two or more jobs in the reference week, as collected in "
        "the survey interview. Third-quarter 2026 estimates are preliminary and use the first issue of that "
        "quarter's weights.", small))
    s.append(Paragraph("Contact: Damon Mcbride, Labor Market Information Bureau.", small))
    _doc(path, "HES release 2026 Q3", "LMIB").build(s)
    common.scrub_pdf(path, "20261002080000-06'00'", "TDLI LMIB publishing")


def release_table(W):
    """Computed from the clean truth's reports and the first-issue weights, the way the release was produced."""
    out = []
    for q in world.REF_QUARTERS:
        ps = [p for p in W["persons_q"] if p["q"] == q]
        w = W["wts"]
        pop = sum(w[(p["aid"], p["line"], q)] for p in ps)
        lf = sum(w[(p["aid"], p["line"], q)] for p in ps if p["lfs"] in (1, 2, 3))
        emp = sum(w[(p["aid"], p["line"], q)] for p in ps if p["lfs"] in (1, 2))
        mj = sum(w[(p["aid"], p["line"], q)] for p in ps if p["lfs"] in (1, 2) and p["mjh_rep"] == 1)
        out.append((q, "%.1f" % (pop / 1000), "%.1f" % (lf / 1000), "%.1f" % (emp / 1000),
                    "%.1f" % (100 * (lf - emp) / lf), "%.1f" % (mj / 1000), "%.1f" % (100 * mj / emp)))
    W["release_rows"] = out
    return out
