"""task118 documents: the board's hypnotics deprescribing policy (pdf), the falls dashboard's indicator definitions
(pdf) and the thread that put the placement to the commissioning support unit (eml)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.3, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.6, leading=17.5,
                        spaceAfter=3, textColor=colors.HexColor("#005EB8"))
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.6, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.4)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(18 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.6):
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=size, leading=size + 2.4)
    head = ParagraphStyle("head", parent=cell, fontName="Helvetica-Bold")
    rows = [[Paragraph(str(v), head if r == 0 else cell) for v in row] for r, row in enumerate(rows)]
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9A9A9A")),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EDEE")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, author, flow, footer):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, creator=author, invariant=1)
    doc.build(flow, onFirstPage=_footer(footer), onLaterPages=_footer(footer))


def policy(path):
    body, h1, h2, small = _styles()
    rr = P.RR
    s = [Paragraph("Benzodiazepines and Z-drugs in people aged 65 and over: deprescribing policy", h1),
         Paragraph("%s, Medicines Optimisation. Version 1.2, approved by the Medicines Optimisation Committee on 23 June "
                   "2026; next review June 2028. Owner: %s, Chief Pharmacist." % (P.ORG, P.PEOPLE["chief"]), small),
         Spacer(1, 4),
         Paragraph("1. Scope", h2),
         Paragraph("This policy covers benzodiazepines and Z-drugs (zopiclone and zolpidem) prescribed in primary care to "
                   "patients aged 65 or over, whether for sleep or for anxiety, and the board's pharmacist deprescribing "
                   "team. It does not cover melatonin, sedating antihistamines or antipsychotics, or patients under the "
                   "care of a specialist drug and alcohol service.", body),
         Paragraph("2. Why the board funds deprescribing", h2),
         Paragraph("Benzodiazepines and Z-drugs cause falls in older people through sedation the next day, slower "
                   "reactions and poorer balance at night. The harm is greatest soon after a patient starts the drug and "
                   "falls back the longer they take it, without returning to that of a patient who does not. Most "
                   "patients started for a short course and stayed on repeat prescriptions; many are glad to come off "
                   "with support.", body),
         Paragraph("3. The deprescribing team", h2),
         Paragraph("The team (six pharmacists and two pharmacy technicians) works in one locality for a calendar year. "
                   "Between January and March it invites every current user registered with the locality's practices to "
                   "a structured medication review and, with the patient and their GP, agrees a taper, usually over four "
                   "to twelve weeks. In the 2025 pilot at two of the board's practices, 45 of every 100 patients reviewed "
                   "came off the drug and stayed off it.", body),
         Paragraph("4. Definitions", h2),
         _table([["Term", "Meaning"],
                 ["Current user", "a patient aged 65 or over on 1 January 2027 with a benzodiazepine or Z-drug dispensed "
                                  "between 1 July and 30 September 2026"],
                 ["Locality", "the locality of the practice the patient is registered with, from the practice register"],
                 ["Coming off", "45 in every 100 current users the team reviews; a patient who comes off is off the drug "
                                "from 1 April 2027 to 31 December 2027"]], [34, 130]),
         Paragraph("5. Falls while taking a benzodiazepine or Z-drug", h2),
         Paragraph("Emergency admissions to hospital for a fall among patients aged 65 or over who are not taking a "
                   "benzodiazepine or Z-drug run at %.1f per 100 patients a year. A patient taking one is admitted for a "
                   "fall at a multiple of that rate, which depends on the time since the patient first started a "
                   "benzodiazepine or Z-drug:" % P.BASE, body),
         _table([["Time since the patient first started a benzodiazepine or Z-drug", "Rate ratio"],
                 ["Under %d months" % rr[0][0], "%.1f" % rr[0][1]],
                 ["%d months to under %d months" % (rr[0][0], rr[1][0]), "%.1f" % rr[1][1]],
                 ["%d months or more" % rr[1][0], "%.1f" % rr[2][1]]], [120, 30]),
         Spacer(1, 3),
         Paragraph("A patient who comes off the drug is admitted for a fall at the rate of a patient not taking one from "
                   "the day they are off it. The rate ratios are those of the board's falls evidence review (October "
                   "2025), from a cohort of patients aged 65 or over starting a benzodiazepine or Z-drug in UK primary "
                   "care; the rate for patients not taking one is from the board's own emergency admissions.", body),
         Paragraph("6. Placing the team", h2),
         Paragraph("The board places the team in the locality where it avoids the most emergency admissions for a fall "
                   "in 2027: the admissions the 45 in every 100 current users who come off would have had on the drug "
                   "from 1 April to 31 December 2027, less those they will have off it.", body),
         Paragraph("7. Monitoring", h2),
         Paragraph("Practices report reviews completed and patients off the drug at 3, 6 and 12 months. The falls "
                   "prevention lead reports emergency admissions for a fall in the locality on the falls dashboard's "
                   "definitions.", body)]
    _doc(path, "Benzodiazepines and Z-drugs in people aged 65 and over: deprescribing policy", P.ORG, s,
         "%s. Medicines Optimisation policy MO-17, version 1.2." % P.ORG)


def falls_definition(path):
    body, h1, h2, small = _styles()
    s = [Paragraph("Falls dashboard: indicator definitions", h1),
         Paragraph("%s, Falls Prevention Programme. Version 2, February 2026 (version 1, May 2024). Owner: %s, Falls "
                   "Prevention Lead. Source data: SUS admitted patient care, episode level." % (P.ORG, P.PEOPLE["falls"]),
                   small),
         Spacer(1, 4),
         Paragraph("F1. Emergency admissions for a fall, patients aged 65 to 79 and aged 80 or over", h2),
         _table([["Element", "Definition"],
                 ["Admission", "one stay in hospital care, from the day the patient is admitted as an emergency to the day "
                               "they leave hospital care. A patient discharged to another hospital is still in hospital "
                               "care, and the stay runs on to the day they leave the last hospital."],
                 ["Emergency", "admission method 21, 22, 23, 24, 25, 28, 2A, 2B, 2C or 2D"],
                 ["For a fall", "an external cause code W00 to W19 in any diagnosis position of the first episode of the "
                                "admission"],
                 ["Age", "the patient's age at the start of the admission"],
                 ["Year", "by the date of admission, 1 April to 31 March"],
                 ["Locality", "of the patient's registered practice at the start of the admission"]], [26, 138]),
         Paragraph("F2. Bed-days of emergency admissions for a fall", h2),
         Paragraph("For every admission in F1, the days from the day of admission to the day the patient leaves hospital "
                   "care; the day of leaving is not counted, so a patient who goes home the day they arrive uses no "
                   "bed-days.", body),
         Paragraph("F3. Emergency readmissions within 30 days of a fall admission", h2),
         Paragraph("The admissions in F1 after which the patient, alive on leaving hospital care, was admitted as an "
                   "emergency again on the day they left or in the 30 days after it. Each admission in F1 counts once "
                   "however many admissions follow it.", body),
         Paragraph("Changes in version 2", h2),
         Paragraph("Bed-days and readmissions added; ages split at 80 to match the national indicators.", body)]
    _doc(path, "Falls dashboard: indicator definitions", P.ORG, s, "%s. Falls Prevention Programme." % P.ORG)


def thread():
    pe = P.PEOPLE

    def addr(k):
        first, last = pe[k].split()
        return "%s <%s.%s@nhs.net>" % (pe[k], first.lower(), last.lower())

    hdr = ("From: %s\nTo: %s\nCc: %s, %s\nSubject: Re: Deprescribing team placement 2027\n"
           "Date: Mon, 19 Oct 2026 16:42:07 +0100\nMessage-ID: <LO4P265MB58730C2F91D4A6B3E7@LO4P265MB5873.GBRP265.PROD.OUTLOOK.COM>\n"
           "In-Reply-To: <LO2P265MB31840A7D55E2C19F04@LO2P265MB3184.GBRP265.PROD.OUTLOOK.COM>\nMIME-Version: 1.0\n"
           "Content-Type: text/plain; charset=\"utf-8\"\nContent-Transfer-Encoding: 8bit\n\n"
           % (addr("analyst"), addr("lead"), addr("chief"), addr("falls")))
    body = """Leon,

Everything is in the placement folder now: the data platform's dispensing extract for April to
September, the practices' repeat templates for hypnotics as at 1 October, the template export Mill Road Group Practice
took from its old clinical system before it moved over in July, the practice register, the dm+d list
for the products, and for Katherine the SUS falls cohort pull with the provider site list.
The Q2 prescribing dashboard and the falls service referrals are in there as well.

Glenn

--
Senior Analyst, Medicines and Primary Care | Glenn Pearce
Kestrel and Wold Commissioning Support Unit

On Fri, 16 Oct 2026 at 11:18, Katherine Watts <katherine.watts@nhs.net> wrote:
> For the same paper, can the placement workbook carry each locality's emergency admissions for a
> fall in 2025-26 by age band, with the bed-days and the 30-day readmissions, on the dashboard's
> version 2 definitions? The board should see the falls burden next to the placement.
>
> Katherine
>
> On Thu, 15 Oct 2026 at 09:03, Leon Ross <leon.ross@nhs.net> wrote:
>> Glenn, the board has agreed the team for 2027: one team, one locality, from January. Julia wants
>> the case for which locality at the November board, with the emergency fall admissions it avoids
>> there in 2027 worked on the policy, and the runner-up beside it. Could you pull what you need?
>>
>> Leon
>>
>> --
>> Medicines Optimisation Lead | Leon Ross
>> NHS Kestrel Vale Integrated Care Board

********************************************************************************************************
This message may contain confidential information. If you are not the intended recipient please inform
the sender that you have received the message in error before deleting it.
********************************************************************************************************
"""
    return hdr + body
