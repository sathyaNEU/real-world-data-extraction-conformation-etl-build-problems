"""task237 documents: the translation and adaptation standard and the BCS-12 technical manual (pdf), the translation
register and the vendors' codebook (xlsx), the data dictionary and the readme (md)."""
import datetime as dt

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import postprocess

NEG_CODES = ", ".join(P.ITEMS[i][0] for i in P.NEG[:-1]) + " and " + P.ITEMS[P.NEG[-1]][0]


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, spaceBefore=8,
                        spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10, textColor=colors.HexColor("#444444"))
    return dict(body=body, h1=h1, h2=h2, small=small)


def _footer(text):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(letter[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(rows, widths, size=8.0):
    t = Table(rows, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEF0")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, author, foot, story, stamp):
    doc = SimpleDocTemplate(path, pagesize=letter, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, invariant=1)
    doc.build(story, onFirstPage=_footer(foot), onLaterPages=_footer(foot))
    postprocess.scrub(path, author, stamp)


# ------------------------------------------------------------------ the translation and adaptation standard
def standard(path):
    S = _styles(); b, h1, h2, sm = S["body"], S["h1"], S["h2"], S["small"]
    st = [Paragraph("Translation and adaptation standard for the BCS-12", h1),
          Paragraph("%s, %s. Standard TAS-4, in force from 1 September 2026 (replaces TAS-3 of June 2024). Owner: %s, "
                    "translation quality lead." % (P.SURVEY, P.CENTRE, P.PEOPLE["quality"]), sm),
          Spacer(1, 4),
          Paragraph("1. Scope", h2),
          Paragraph("This standard governs every new language version of the %s used in the %s: how it is translated, "
                    "piloted and released for fieldwork. It applies to the versions added for wave %d and later waves." %
                    (P.SCALE, P.SURVEY, P.WAVE), b),
          Paragraph("2. Translation", h2),
          Paragraph("Two translators prepare independent forward translations, which the translation coordinator reconciles "
                    "with a reviewer fluent in both languages. A third translator back-translates the reconciled version "
                    "into English for the review, and every query raised is settled before the pilot. A version to be "
                    "fielded by interviewers is pretested in a small number of interviews before its pilot. The "
                    "translation register records each step and the version's pilot fieldwork dates.", b),
          Paragraph("3. The pilot", h2),
          Paragraph("Each version is piloted with at least 400 valid completes, through the online panel or by "
                    "interviewers according to the mode the version will be fielded in. The fieldwork vendors deliver "
                    "their files to the pilot fieldwork manager with a codebook.", b),
          Paragraph("4. Valid completes", h2),
          Paragraph("A pilot interview of a version is a valid complete when the respondent was 18 or older, the interview "
                    "took place within the version's pilot fieldwork dates in the translation register, and it reached the "
                    "end of the BCS-12 module in that version (a respondent who switched the questionnaire to another "
                    "language before the end of the module is not a complete of the version). For an online panel pilot, a "
                    "panel member counts once, at their first valid complete of the version. For an interviewer-administered "
                    "pilot, an interview the vendor's back-check reports as not confirmed is not valid; an interview not "
                    "selected for back-check, or whose respondent the back-check could not reach, stays valid.", b),
          Paragraph("5. Scoring", h2),
          Paragraph("Items %s are reverse-scored: the item score is 6 minus the answer. An answer of prefer not to say, "
                    "don't know or refused leaves the item unanswered. The total score is the sum of the twelve item scores "
                    "(12 to 60). A respondent with one or two unanswered items is given the mean of their answered item "
                    "scores times twelve; a respondent with three or more unanswered items has no score. A version's pilot "
                    "mean score is the mean total score of its valid completes that have a score." % NEG_CODES, b),
          Paragraph("6. The release gate", h2),
          Paragraph("A version's reliability is the share of the variance of its total score, across its valid completes "
                    "who answered all twelve items, that is due to differences between those respondents in "
                    "connectedness, compared unrounded with these bands:", b),
          _table([["Reliability", "Decision", "What follows"],
                  ["0.80 or more", "Release", "the version is fielded in the wave"],
                  ["0.70 to under 0.80", "Hold", "cognitive interviews on the items, then a second pilot"],
                  ["under 0.70", "Rework", "the version goes back to the translation team for retranslation"]],
                 [40 * mm, 26 * mm, 104 * mm]),
          Spacer(1, 6),
          Paragraph("The translation quality lead signs off every version's decision before the wave's fieldwork launches "
                    "and reports, for each version, its decision, its valid pilot completes and its pilot mean score.", b),
          Paragraph("7. Roles", h2),
          _table([["Role", "Holder", "In this standard"],
                  ["Translation quality lead", P.PEOPLE["quality"], "signs off the release decisions (s.6)"],
                  ["Translation coordinator", P.PEOPLE["coordinator"], "keeps the translation register (s.2)"],
                  ["Pilot fieldwork manager", P.PEOPLE["pilot"], "receives the vendors' files and codebook (s.3)"]],
                 [46 * mm, 34 * mm, 90 * mm]),
          ]
    _doc(path, "Translation and adaptation standard TAS-4", P.PEOPLE["quality"],
         "TAS-4 | %s | %s" % (P.SURVEY, P.CENTRE), st, "2026-08-24")


# ------------------------------------------------------------------ the technical manual (English edition)
def manual(path, english):
    S = _styles(); b, h1, h2, sm = S["body"], S["h1"], S["h2"], S["small"]
    rows = [["Item", "Statement", "Keying"]] + [[c, t, "positive" if k > 0 else "negative (reverse-scored)"]
                                               for c, t, k in P.ITEMS]
    st = [Paragraph("Belonging and Connection Scale (BCS-12): technical manual, English edition", h1),
          Paragraph("%s. Second edition, March 2022." % P.CENTRE, sm),
          Spacer(1, 4),
          Paragraph("1. What the scale measures", h2),
          Paragraph("The BCS-12 measures connectedness: how far a person feels close to, supported by and part of the "
                    "people and places around them. It was developed for the %s, a household survey of adults run every "
                    "two years, and has been its core measure since wave 1." % P.SURVEY, b),
          Paragraph("2. Items", h2),
          Paragraph("Twelve statements answered on a five-point scale from strongly disagree (1) to strongly agree (5). "
                    "Six statements are worded towards connectedness and six away from it, alternating, so that agreeing "
                    "with everything does not raise the score.", b),
          _table(rows, [16 * mm, 110 * mm, 44 * mm]),
          Spacer(1, 6),
          Paragraph("3. Scoring", h2),
          Paragraph("The six negatively worded items are reverse-scored and the twelve item scores summed (12 to 60); "
                    "higher scores mean more connectedness. Survey publications report the mean score.", b),
          Paragraph("4. Development and validation", h2),
          Paragraph("The items were drafted from 41 candidate statements after focus groups in 2019 and tested in two "
                    "rounds. In the English validation sample (%s adults, 2021) the twelve items formed a single factor, "
                    "and the reliability of the total score was %s. Scores correlate 0.58 with the survey's single-item "
                    "loneliness question and -0.41 with its psychological distress screener." %
                    (format(english["n"], ","), english["rel"]), b),
          Paragraph("5. Other languages", h2),
          Paragraph("A French version has been fielded since wave 1. New language versions are translated, piloted and "
                    "released under the centre's translation and adaptation standard.", b),
          ]
    _doc(path, "BCS-12 technical manual, English edition", "Survey Research Centre",
         "BCS-12 technical manual | %s" % P.CENTRE, st, "2022-03-14")


# ------------------------------------------------------------------ the translation register
def register(path, reg):
    wb = Workbook(); ws = wb.active; ws.title = "Register"
    cols = list(reg.columns)
    ws.append(cols)
    for r in reg.itertuples(index=False):
        ws.append([getattr(r, c) for c in cols])
    for c in ws[1]:
        c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="E8EEF0")
    for i, w in enumerate([9, 30, 30, 20, 22, 14, 12, 26, 12, 12, 70], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    for row in ws.iter_rows(min_row=2):
        row[-1].alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "B2"
    nt = wb.create_sheet("About")
    for line in ("Translation register, BCS-12 language versions added for wave %d of the %s." % (P.WAVE, P.SURVEY),
                 "Kept by the translation coordinator (%s). Dates are Eastern dates." % P.PEOPLE["coordinator"],
                 "Pilot start and end are the version's pilot fieldwork dates under TAS-4 section 4."):
        nt.append([line])
    nt.column_dimensions["A"].width = 110
    wb.save(path)
    postprocess.scrub(path, P.PEOPLE["coordinator"], "2027-02-20")
    postprocess.finish_office(path, "2026-10-05T14:10:00Z", "2027-02-20T16:45:00Z", P.CENTRE)


# ------------------------------------------------------------------ the vendors' codebook
def codebook(path):
    wb = Workbook(); ws = wb.active; ws.title = "Online panel (NCP)"
    ws.append(["variable", "label", "values"])
    ws.append(["respondent_id", "id of the survey entry", ""])
    ws.append(["survey_code", "survey link: CCS6-BCS- and the version code", ""])
    ws.append(["status", "interview status", "complete (reached the end of the questionnaire); partial (left before the end "
               "of the questionnaire); screened out (under 18)"])
    ws.append(["start_utc, end_utc", "entry and completion times, UTC", "end_utc blank unless complete"])
    ws.append(["ui_language_at_end", "questionnaire language when the respondent left the survey", "version code, or en"])
    ws.append(["age", "age in years (screener)", ""])
    for c, t, k in P.ITEMS:
        ws.append([c, t, "1 Strongly disagree; 2 Disagree; 3 Neither agree nor disagree; 4 Agree; 5 Strongly agree; "
                         "9 Prefer not to say; blank: not reached"])
    ws.append(["sex", "sex", "F, M, X; blank: not reached"])
    ws.append(["hh_size", "people in the household, including the respondent", "1 to 9 (9: nine or more); blank: not reached"])
    ws.append(["yrs_in_canada", "years lived in Canada", "whole years; blank: not reached"])
    w2 = wb.create_sheet("Interviewer (FLR)")
    w2.append(["variable", "label", "values"])
    w2.append(["case_id", "sample case (the address issued to the interviewer)", ""])
    w2.append(["version", "version code", ""])
    w2.append(["interviewer_id", "interviewer", ""])
    w2.append(["interview_date", "date of interview (Eastern)", ""])
    w2.append(["variable, value", "one row per questionnaire variable reached", ""])
    w2.append(["RESULT", "interview outcome, recorded by the interviewer", "1 Full interview; 2 Partial interview (broken off)"])
    w2.append(["AGE", "age in years (screener)", ""])
    for c, t, k in P.ITEMS:
        w2.append([c, t, "1 Strongly disagree; 2 Disagree; 3 Neither agree nor disagree; 4 Agree; 5 Strongly agree; "
                         "-8 Don't know; -9 Refused"])
    w2.append(["SEX", "sex", "1 Male; 2 Female; 3 Another gender"])
    w2.append(["HHSIZE", "people in the household, including the respondent", "1 to 9 (9: nine or more)"])
    w2.append(["YRSCAN", "years lived in Canada", "whole years"])
    for sh in (ws, w2):
        for c in sh[1]:
            c.font = Font(bold=True); c.fill = PatternFill("solid", fgColor="E8EEF0")
        for i, w in enumerate([20, 62, 96], 1):
            sh.column_dimensions[get_column_letter(i)].width = w
        sh.freeze_panes = "A2"
    w3 = wb.create_sheet("Questionnaire")
    for line in (["Pilot questionnaire, both modes, in this order:"],
                 ["1", "Screener", "age (respondents under 18 are screened out)"],
                 ["2", "BCS-12 module", "BCS01 to BCS12, the version's translation"],
                 ["3", "Background", "sex, people in the household, years lived in Canada"]):
        w3.append(line)
    for i, w in enumerate([8, 18, 70], 1):
        w3.column_dimensions[get_column_letter(i)].width = w
    wb.save(path)
    postprocess.scrub(path, P.PEOPLE["pilot"], "2027-01-12")
    postprocess.finish_office(path, "2027-01-08T15:00:00Z", "2027-01-12T18:20:00Z", P.CENTRE)


# ------------------------------------------------------------------ the dictionary and the readme
def dictionary(files):
    return """# Data dictionary

Dates are Eastern dates (Toronto time) unless a field says UTC.

## {online}

Nesscroft Panels' export of the online pilots, one row per entry to the survey (every status). Answers as given, on the
codes in {codebook}.

## {ledger}

Nesscroft Panels' incentive ledger for the pilots, sent with its invoice (the centre pays the panel's incentives at cost):
one row per survey entry with the panel member who made it and the points credited.

| field | meaning |
|---|---|
| panel_member_id | the panel member's account; the panel merges a second account it finds a member holding into that member's account |
| respondent_id | the survey entry (as in the export); blank on a merged row |
| survey_code | the survey link; blank on a merged row |
| activity_utc | when the entry ended, or when the account was merged, UTC |
| outcome | complete, partial, screened out, or merged (the account's points moved to the account it was merged into) |
| points | points credited (negative on a merged row) |
| merged_into | on a merged row, the account it was merged into |
| payment_batch | the month the points are paid in |

## {para}

Nesscroft Panels' paradata for the pilots: platform (mobile, desktop or tablet), time on the survey and on the BCS-12
module, back-button uses.

## {capi}

Fernlow Research's interviewer-administered pilot and pretest interviews, one row per interview and questionnaire
variable reached (RESULT, AGE, the twelve BCS-12 items and the background questions), on the codes in {codebook}.

## {bc}

Fernlow Research's back-check log: one row per interview selected for back-check, with the case, the interviewer
whose interview was checked, the date and method of the check, and its outcome (confirmed, not confirmed, not reached).

## {reg}

Sheet Register: one row per version, with its translation steps and pilot fieldwork dates. Sheet About.

## {codebook}

Each vendor's variables and answer codes (one sheet per vendor) and the pilot questionnaire's order (sheet
Questionnaire).

## {wave5}

Wave 5 BCS-12 results by region and version (English, French): respondents, mean score and its standard error.
""".format(**files)


def readme(files):
    return """# BCS-12 wave {wave} language versions: pilot files for the release decisions

Compiled by the pilot fieldwork manager on Friday 26 February 2027 from the two vendors' final pilot files, for the
translation quality lead's release decisions before the wave {wave} fieldwork (launching Monday 22 March 2027).

- `{std}`: the translation and adaptation standard (TAS-4).
- `{manual}`: the BCS-12 technical manual, English edition.
- `{reg}`: the translation register.
- `{online}`: Nesscroft Panels' online pilot export.
- `{ledger}`: Nesscroft Panels' incentive ledger, sent with its invoice for the pilots.
- `{para}`: Nesscroft Panels' paradata.
- `{capi}`: Fernlow Research's interviewer-administered pilot file.
- `{bc}`: Fernlow Research's back-check log.
- `{codebook}`: the vendors' codebook.
- `{wave5}`: wave 5 results by region, for reference.
- `DATA_DICTIONARY.md`: the files and their fields.
""".format(wave=P.WAVE, **files)
