"""task464 architecture 9: the governing documents.

Two PDFs, each a filed fact about the world and neither a description of the data:

  statin_continuity_sessions_brief.pdf    the network board's brief: what the sessions are and the figure they
                                          are placed on (the estimand, at authority). It says nothing about how
                                          or when patients stop a statin.
  icb_cvd_repeat_return_2025_spec.pdf     the integrated care board's specification for the 2025 repeat return:
                                          the two measures the asks report.

No document states an expected count, a rate read off the record or a ranking of the practices.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import world as W

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
S = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=S["Heading1"], fontSize=13.5, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=S["Heading2"], fontSize=10.5, spaceBefore=9, spaceAfter=3)
BODY = ParagraphStyle("body", parent=S["BodyText"], fontSize=9.2, leading=12.8, spaceAfter=5)
LIST = ParagraphStyle("list", parent=BODY, leftIndent=12, bulletIndent=2, spaceAfter=2)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#555555"))

BRIEF = "statin_continuity_sessions_brief.pdf"
SPEC = "icb_cvd_repeat_return_2025_spec.pdf"


def _doc(name, title, author, flow):
    d = SimpleDocTemplate(os.path.join(OUT, name), pagesize=A4,
                          leftMargin=21 * mm, rightMargin=21 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                          title=title, author=author, subject="", creator="")
    d.build(flow)
    return name


def _table(data, widths):
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3), ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.black),
        ("LINEBELOW", (0, 1), (-1, -2), 0.2, colors.HexColor("#bbbbbb")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def brief():
    P = W.PEOPLE
    f = [Paragraph("Statin continuity sessions, January to June 2027", H1),
         Paragraph("%s. Brief for the network board, meeting of 10 December 2026. Prepared by %s, clinical "
                   "director, 3 December 2026." % (W.NETWORK, P["clinical_director"]), SMALL),
         Paragraph("The sessions", H2),
         Paragraph("From the week of 11 January to the end of June 2027 the network's lead clinical pharmacist, "
                   "%s, will hold two statin continuity sessions a week at one member practice. The sessions work "
                   "through that practice's patients who take a statin: patients are contacted, seen in clinic or "
                   "by telephone, and supported to keep taking it or to restart. The pharmacist's other sessions "
                   "stay where they are. One practice hosts all of them, because the pharmacist works from that "
                   "practice's clinical system and its list." % P["lead_pharmacist"], BODY),
         Paragraph("The figure the board places them on", H2),
         Paragraph("The board will place the sessions at the practice with the largest expected number of "
                   "patients who:", BODY),
         Paragraph("are registered with the practice on 30 November 2026 and were issued a statin by it from "
                   "1 September to 30 November 2026; and", LIST, bulletText="•"),
         Paragraph("are still registered with the same practice on 30 June 2027, and will have had no statin "
                   "issued to them from 1 March to 30 June 2027, for whatever reason.", LIST, bulletText="•"),
         Paragraph("A patient who leaves the practice or dies before 30 June 2027 is not counted. A patient first "
                   "issued a statin after 30 November 2026 is not in the figure. Each practice's figure is an "
                   "expected number of patients, rounded to the nearest 10; the practices are compared on their "
                   "figures before rounding.", BODY),
         Paragraph("A statin here is atorvastatin, simvastatin, rosuvastatin, pravastatin or fluvastatin, at any "
                   "strength, on an acute or a repeat prescription. Ezetimibe is not a statin.", BODY),
         Paragraph("Timetable", H2)]
    data = [["Date", "Step"],
            ["1 December 2026", Paragraph("Network searches of both clinical systems run (%s); they cover the "
                                          "period to the end of 30 November 2026." % P["data_lead"], BODY)],
            ["4 December 2026", Paragraph("Board papers issued.", BODY)],
            ["10 December 2026", Paragraph("Board places the sessions.", BODY)],
            ["11 January 2027", Paragraph("First session.", BODY)],
            ["30 June 2027", Paragraph("Last session; the network reviews the practice's figure against what "
                                       "happened.", BODY)]]
    f.append(_table(data, [32 * mm, 136 * mm]))
    f += [Spacer(1, 6),
          Paragraph("%s, clinical director, %s" % (P["clinical_director"], W.NETWORK), SMALL)]
    return _doc(BRIEF, "Statin continuity sessions, January to June 2027", W.NETWORK, f)


def spec():
    f = [Paragraph("CVD medicines: practice repeat return for calendar year 2025", H1),
         Paragraph("Integrated care board, medicines optimisation team. Specification, version 1.1, 15 July "
                   "2026. Version 1.1 moves the submission date to after the last course's anniversary; the "
                   "measures are unchanged from version 1.0.", SMALL),
         Paragraph("Purpose", H2),
         Paragraph("The integrated care board collects two measures of how cardiovascular medicines are issued on "
                   "repeat, once a year, from every practice through its primary care network. The 2025 return "
                   "covers adherence to ACE inhibitors and angiotensin II receptor blockers in calendar year "
                   "2025, and how long ticagrelor 90mg is issued after a heart attack for courses started from "
                   "1 July 2024 to 30 June 2025. Networks submit one file for their practices by 18 December "
                   "2026, once the last course in the return has passed its first anniversary.", BODY),
         Paragraph("Measure R1: ACE inhibitor or angiotensin II receptor blocker adherence, 2025", H2),
         Paragraph("<b>Denominator.</b> Patients registered with the practice throughout 2025, from 1 January to "
                   "31 December, who were issued an ACE inhibitor or an angiotensin II receptor blocker by the "
                   "practice in each of the four quarters of 2025.", BODY),
         Paragraph("<b>Numerator.</b> Those patients whose issues of these medicines covered at least 80 per cent "
                   "of the 365 days of 2025.", BODY),
         Paragraph("<b>Days covered.</b> Each issue covers the days its quantity lasts at the dose in the "
                   "directions on that prescription. It covers days from the day it was issued or, where the "
                   "patient still had supply of the same medicine (the same drug at any strength) from an earlier "
                   "issue, from the day after that supply ran out. Supply carried into 2025 from issues in 2024 "
                   "counts. A day is covered once however many issues cover it, and days after 31 December 2025 "
                   "are not counted. An item cancelled before it was dispensed was not issued.", BODY),
         Paragraph("Measure R2: ticagrelor 90mg after a heart attack", H2),
         Paragraph("Ticagrelor 90mg twice a day is given with aspirin for twelve months after a heart attack "
                   "(myocardial infarction).", BODY),
         Paragraph("<b>Denominator.</b> Patients who had a myocardial infarction and started ticagrelor 90mg "
                   "after it, both between 1 July 2024 and 30 June 2025, counted at the practice they were "
                   "registered with on the day they started it.", BODY),
         Paragraph("<b>Numerator.</b> Those issued ticagrelor 90mg, at any practice, on a day later than the "
                   "first anniversary of the day they started it. Ticagrelor 60mg is not part of this measure.", BODY),
         Paragraph("The return", H2),
         Paragraph("One row per practice, identified by its ODS code:", BODY)]
    data = [["Field", "Content"],
            ["ods_code", "The practice's ODS code"],
            ["r1_denominator", "R1 denominator, patients"],
            ["r1_numerator", "R1 numerator, patients"],
            ["r1_percent", "R1 numerator as a percentage of the denominator, one decimal place"],
            ["r2_denominator", "R2 denominator, patients"],
            ["r2_numerator", "R2 numerator, patients"],
            ["r2_percent", "R2 numerator as a percentage of the denominator, whole number"]]
    f.append(_table(data, [34 * mm, 134 * mm]))
    f += [Spacer(1, 6),
          Paragraph("The measures are reported to the integrated care board's prescribing group and are not "
                    "published by practice.", SMALL)]
    return _doc(SPEC, "CVD medicines: practice repeat return for calendar year 2025", "Medicines optimisation team", f)


def main():
    return [brief(), spec()]


if __name__ == "__main__":
    print(main())
