"""The pack's documents: the research committee's site selection paper, the sponsor's site feasibility questionnaire,
the information team's guide to the extracts, and the pack's contents."""
from __future__ import annotations

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import mm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"),
              ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1f2428"), colors.HexColor("#5d646a"), colors.HexColor("#b8bfc4")
NHSBLUE = colors.HexColor("#005eb8")
DEEP = colors.HexColor("#2b3a67")
GREEN = colors.HexColor("#215c4a")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.8, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=14, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.4, leading=11.4, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.2, leading=10.4, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.2, leading=10.4, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right, font):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(20 * mm, A4[1] - 12 * mm, left)
        canvas.drawRightString(A4[0] - 20 * mm, A4[1] - 12 * mm, right)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm,
                             bottomMargin=17 * mm, title=title, author=author, subject="", creator="", producer="")


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


# ---------------------------------------------------------------------------------------------- the paper
def write_paper(path):
    S = styles("Sans", NHSBLUE)
    doc = _doc(path, "RC/26/11 Recruiting sites for ARV-1102", K.TRUST)
    clinics = [["Clinic", "Opened", "Records before 8 January 2024", "Records from 8 January 2024"]]
    for nm, cis, site, opened in K.CLINICS:
        clinics.append([nm, opened.strftime("%B %Y"), "CIS, clinic code %s" % cis if cis else "None (opened later)",
                        "EPR, site %s" % site])
    s = [Paragraph("Recruiting sites for ARV-1102: naming two memory clinics", S["h1"]),
         Paragraph("Research Committee paper RC/26/11, for decision on 21 October 2026. From %s, Lead for Dementia "
                   "Research, Research and Development, with %s, Clinical Lead, %s. 8 October 2026."
                   % (K.PEOPLE["lead"], K.PEOPLE["clinical"], K.SERVICE), S["meta"]),
         Paragraph("1. Purpose", S["h2"]),
         Paragraph("%s has offered the trust two recruiting sites for ARV-1102, its phase 3 trial of a "
                   "disease-modifying treatment in early Alzheimer's disease, which opens to recruitment in January "
                   "2027. Our %s runs eight memory clinics. This paper sets out how the committee will choose the two "
                   "that recruit and asks it to name them." % (K.SPONSOR, K.SERVICE), S["body"]),
         Paragraph("2. What the sponsor asks of a site", S["h2"]),
         Paragraph("The trial's primary endpoint is the change in cognition over 18 months, and its power rests on the "
                   "patients it enrols declining with their disease over that time. %s asks each trust to recruit "
                   "from the clinics whose patients' cognition has declined fastest with their disease, judged on the "
                   "trust's own records, and to return its site feasibility questionnaire for every clinic the trust "
                   "runs." % K.SPONSOR, S["body"]),
         Paragraph("3. How the committee will compare the clinics", S["h2"]),
         _clause(S, "3.1", "Each clinic's figure is the average, over its patients, of the rate at which each "
                           "patient's cognition declined between 1 January 2022 and 30 September 2026, in ACE-III "
                           "points a year, each patient's own rate counting once. The rate is the decline the "
                           "patient's disease produced: a change in a patient's scores that the test itself produces "
                           "is not part of it."),
         _clause(S, "3.2", "A clinic's patients are those whose latest diagnosis on the record on or before 30 "
                           "September 2026 is Alzheimer's disease (ICD-10 F00 or G30, mixed Alzheimer's and vascular "
                           "dementia included) or mild cognitive impairment (F06.7), and who completed two or more "
                           "ACE-III assessments in that period. A patient counts at the clinic that held their last "
                           "completed assessment in the period. An assessment stopped before all five domains were "
                           "scored is not a completed assessment."),
         _clause(S, "3.3", "The two clinics whose patients declined fastest are named. The committee compares the "
                           "clinics' figures unrounded and reports them to the nearest half point."),
         Paragraph("4. The clinics and their records", S["h2"]),
         Paragraph("The service's records were held on the trust's clinical information system (CIS) until 5 January "
                   "2024 and on the electronic patient record (EPR) from 8 January 2024. The information team's guide "
                   "of 6 October 2026 describes the extracts it has prepared for this paper.", S["body"]),
         _table(S, clinics, [30, 28, 56, 56]),
         Spacer(1, 4),
         Paragraph("Quarndale opened on 8 April 2024. It took the referrals from two districts each that Corvale and "
                   "Mosswick had served and from three districts the service took on that month; the patients "
                   "already under Corvale and Mosswick stayed with them.", S["body"]),
         Paragraph("5. The feasibility questionnaire", S["h2"]),
         Paragraph("The trust's return to %s's questionnaire (version 2.0, 21 September 2026) goes with the "
                   "nomination and gives the sponsor's population and diagnostic pathway figures for each of the "
                   "eight clinics, on the questionnaire's own definitions." % K.SPONSOR, S["body"]),
         Paragraph("6. Decision", S["h2"]),
         Paragraph("The committee is asked to name two clinics as recruiting sites for ARV-1102 and to approve the "
                   "questionnaire return.", S["body"])]
    doc.build(s, onFirstPage=_frame(K.TRUST, "Research Committee RC/26/11", "Sans"),
              onLaterPages=_frame(K.TRUST, "Research Committee RC/26/11", "Sans"))


# ---------------------------------------------------------------------------------------------- the questionnaire
def write_questionnaire(path):
    S = styles("Serif", DEEP)
    doc = _doc(path, "%s site feasibility questionnaire" % K.TRIAL, K.SPONSOR)
    s = [Paragraph("%s: site feasibility questionnaire" % K.TRIAL, S["h1"]),
         Paragraph("%s. A phase 3, randomised, placebo-controlled trial in early Alzheimer's disease. Version 2.0, "
                   "21 September 2026. Return one questionnaire for each trust by 30 October 2026." % K.SPONSOR,
                   S["meta"]),
         Paragraph("Section A. The trust", S["h2"]),
         Paragraph("A1 to A6 (trust details, principal investigator, research team, pharmacy and governance contacts) "
                   "are answered on the cover sheet.", S["body"]),
         Paragraph("Section B. Patient population", S["h2"]),
         Paragraph("Answer for each memory clinic the trust runs.", S["body"]),
         _clause(S, "B1", "The number of patients with Alzheimer's disease or mild cognitive impairment under the "
                          "clinic's follow-up on 30 September 2026. A patient is under a clinic's follow-up from the "
                          "clinic accepting their referral until the memory service discharges them, they die or "
                          "their care passes to another clinic or service. Count each patient once, at the clinic "
                          "following them on that day, by their latest recorded diagnosis on that day."),
         _clause(S, "B2", "Of the patients in B1, the number who will be 85 or under on 1 January 2027, the trial's "
                          "upper age limit when it opens."),
         _clause(S, "B3", "The clinic's experience of research in dementia since 2022 (studies, recruits, "
                          "withdrawals): answered on the cover sheet."),
         Paragraph("Section C. Diagnostic pathway", S["h2"]),
         Paragraph("Answer for each memory clinic, for the patients the clinic gave a diagnosis in the 12 months "
                   "from 1 October 2025 to 30 September 2026. A patient's diagnosis is the first the memory service "
                   "gave them on the referral, whatever it was (a finding of no dementia included).", S["body"]),
         _clause(S, "C1", "The share of those patients who received their diagnosis within 42 days (42 days or "
                          "fewer) of the clinic receiving their referral."),
         _clause(S, "C2", "The average number of days from the clinic receiving the referral to the patient receiving "
                          "their diagnosis."),
         Paragraph("Section D. Imaging, laboratory and rating", S["h2"]),
         Paragraph("D1 to D7 (MRI capacity and wait, amyloid PET or CSF access, blood biomarkers, certified raters "
                   "for the trial's cognitive battery) are answered by the trust's radiology and research teams on "
                   "the cover sheet.", S["body"]),
         Paragraph("Notes", S["h2"]),
         Paragraph("Days are calendar days. Give percentages to one decimal place and averages of days to one decimal "
                   "place. Where a figure rests on the trust's own records, keep the working: %s may ask to see it "
                   "at the site initiation visit." % K.SPONSOR, S["body"])]
    doc.build(s, onFirstPage=_frame(K.SPONSOR, "%s feasibility v2.0" % K.TRIAL, "Serif"),
              onLaterPages=_frame(K.SPONSOR, "%s feasibility v2.0" % K.TRIAL, "Serif"))


# ---------------------------------------------------------------------------------------------- the data guide
def write_guide(path):
    S = styles("Sans", GREEN)
    doc = _doc(path, "Memory Assessment Service: guide to the extracts", K.TRUST)
    F = K.FILES
    rows = [["File", "One row is", "Notes"],
            [F["cis_ace"], "an ACE-III form recorded on CIS, 14 April 2014 to 5 January 2024",
             "Dates day/month/year. form_status C (completed) or A (abandoned: the domains not reached are blank and "
             "the total is the sum of the domains scored). Patients are identified by their hospital patient number "
             "(hpn)."],
            [F["cis_dx"], "a diagnosis recorded on CIS", "diagnosis_status Provisional or Confirmed. Dates "
                                                         "day/month/year."],
            [F["epr_obs"], "one item of an ACE-III set recorded on the EPR, from 8 January 2024",
             "Six items a set: the five domain scores and the total (ACE3_TOTAL). set_status Final, Incomplete (the "
             "test was stopped; only the domains scored are present and the total is their sum) or Entered in error "
             "(recorded against the wrong patient; the set is on the right patient's record as well). performed_at "
             "is local time with its UTC offset."],
            [F["epr_dx"], "a problem on the EPR problem list", "source EPR, or CIS migration: the diagnosis current "
                                                               "on CIS for each patient the service was seeing on 8 "
                                                               "January 2024, recorded on that day."],
            [F["pmi"], "a hospital patient number", "record_status Active, or Merged into another number when one "
                                                   "patient had been registered twice; both numbers carry the same "
                                                   "NHS number. Dates of death come from the NHS Spine."],
            [F["episodes"], "an episode of care with the Memory Assessment Service",
             "From the clinic accepting the referral until the episode is ended on the EPR; episode_end is blank "
             "while the episode is open. migrated_from_cis Y for the episodes open on CIS on 8 January 2024."],
            [F["appts"], "an outpatient appointment booked on the EPR", "appointment_start is local time with its UTC "
                                                                       "offset; outcome is recorded by the clinic, "
                                                                       "blank for appointments still to come."],
            [F["tracker"], "a referral accepted by a memory clinic", "Kept by the information team for the six-week "
                                                                    "referral to diagnosis standard; one row per "
                                                                    "referral. Referral date is the day the clinic "
                                                                    "received the referral; Diagnosis date is the "
                                                                    "day the diagnosis was entered on the EPR "
                                                                    "problem list; Pathway status is awaiting "
                                                                    "assessment, assessed and awaiting a diagnosis, "
                                                                    "diagnosed, or discharged."],
            [F["clinics"], "a clinic, and a postcode district", "The districts sheet gives the clinic each district "
                                                               "was referred to, with the dates."],
            [F["audit"], "a clinic's figures for 2024-25", "The service's annual audit for the commissioners, "
                                                          "financial year 1 April 2024 to 31 March 2025."],
            [F["population"], "a postcode district", "Residents aged 65 and over and 80 and over, mid-2025, from the "
                                                    "trust's planning team."]]
    s = [Paragraph("Memory Assessment Service: guide to the extracts", S["h1"]),
         Paragraph("Information team, %s. Prepared by %s for the Research and Development site selection, 6 October "
                   "2026. EPR extracts taken on 2 October 2026; the CIS archive extract was taken on 5 January 2024."
                   % (K.TRUST, K.PEOPLE["analyst"]), S["meta"]),
         Paragraph("The service moved from the clinical information system (CIS) to the electronic patient record "
                   "(EPR) on 8 January 2024. CIS identifies a patient by the hospital patient number, the EPR by the "
                   "NHS number; the master patient index carries both. CIS clinic codes and EPR site codes are both in "
                   "the clinic register.", S["body"]),
         _table(S, rows, [48, 46, 76]),
         Spacer(1, 6),
         Paragraph("Questions about the extracts go to the information team, quoting the file name.", S["meta"])]
    doc.build(s, onFirstPage=_frame(K.TRUST, "Information team", "Sans"),
              onLaterPages=_frame(K.TRUST, "Information team", "Sans"))


def write_contents(path, items):
    with open(path, "w") as f:
        f.write("ARV-1102 site selection: working pack\n")
        f.write("Research and Development, %s, assembled %s\n\n" % (K.TRUST, K.ASSEMBLED.strftime("%d %B %Y").lstrip("0")))
        for name, desc in items:
            f.write("%s\n    %s\n" % (name, desc))
