"""The pack's documents: the 2025 wave's analysis plan, the accuracy-based programme's report for event 2025-B, the
fieldwork close-out, the data dictionary, the manufacturer's customer notice, the 2021 wave's county tables (PDF) and
the pack's contents (TXT)."""
from __future__ import annotations

import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import letter                                          # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import inch                                                # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle   # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic"),
              ("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1c2329"), colors.HexColor("#5a646d"), colors.HexColor("#b9c1c8")
TEAL = colors.HexColor("#1f5560")
PLUM = colors.HexColor("#4a2c5e")
NAVY = colors.HexColor("#1d3557")


def styles(face="Sans", accent=NAVY):
    b = face + "-B"
    body = ParagraphStyle("b", fontName=face, fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=b, fontSize=14.5, leading=18, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=b, fontSize=10.4, leading=14, textColor=INK, spaceBefore=8, spaceAfter=2,
                          keepWithNext=1),
        meta=ParagraphStyle("m", fontName=face, fontSize=8.3, leading=11.2, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=7.8, leading=9.8, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=7.8, leading=9.8, textColor=INK),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.6, leading=9.8, textColor=GREY, spaceBefore=2,
                            spaceAfter=6),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.4)
        canvas.drawString(.8 * inch, letter[1] - .5 * inch, left)
        canvas.drawRightString(letter[0] - .8 * inch, letter[1] - .5 * inch, right)
        canvas.drawRightString(letter[0] - .8 * inch, .45 * inch, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=(), bold_last=False):
    data = [[Paragraph(str(c), S["cellb"] if (i == 0 or (bold_last and i == len(rows) - 1)) else S["cell"])
             for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject, left, right):
    return SimpleDocTemplate(path, pagesize=letter, leftMargin=.8 * inch, rightMargin=.8 * inch,
                             topMargin=.8 * inch, bottomMargin=.75 * inch, title=title, author=author,
                             subject=subject, creator=author, producer=author), _frame(left, right)


def _d(d):
    return d.strftime("%d %B %Y").lstrip("0")


def _n(x):
    return format(int(x), ",")


# ------------------------------------------------------------------------------------------------ the analysis plan
def write_plan(path):
    S = styles("Serif", TEAL)
    doc, fr = _doc(path, "MHNES 2025 analysis plan", K.REQUESTER, "Analysis plan", K.CENTER, "MHNES 2025 analysis plan")
    st = [Paragraph("%s, 2025 wave: analysis plan" % K.SURVEY, S["h1"]),
          Paragraph("%s, %s. Version 2.1, 14 March 2025. Owner: %s, Chief Statistician; approved by %s, "
                    "District Health Officer." % (K.DISTRICT, K.CENTER, K.REQUESTER, K.HEALTH_OFFICER), S["meta"]),
          Paragraph("1. The wave", S["h2"]),
          _clause(S, "1.1", "The 2025 wave samples adults aged 20 and over living in the district's eight counties. "
                            "Dwellings are screened and the adults to be interviewed are selected from each "
                            "dwelling's roster; each selected adult (a sample person) is asked for a household "
                            "interview and invited to an examination at the mobile examination centre (MEC)."),
          _clause(S, "1.2", "The MEC stands in one county at a time, in the order Wexmoor, Corvale, Lassiter, Ulverne, "
                            "Vellance, Quennel, Yarrowmere and Inskeep, for about five and a half weeks each. A "
                            "county's adults are examined during its stand."),
          Paragraph("2. Weights", S["h2"]),
          _clause(S, "2.1", "Interview weight WTINT2025: interviewed sample persons; for questionnaire measures."),
          _clause(S, "2.2", "Examination weight WTMEC2025: examined sample persons; for examination and laboratory "
                            "measures. Both weights are raked to each county's adults aged 20 and over (1 July "
                            "2025 estimates), so a county's weights sum to its adults."),
          Paragraph("3. Serum 25-hydroxyvitamin D", S["h2"]),
          _clause(S, "3.1", "Blood is drawn at the MEC. Serum goes into a primary vial, assayed for total serum "
                            "25-hydroxyvitamin D [25(OH)D] by %s, and a duplicate vial stored at -70 C in the "
                            "laboratory's biorepository." % K.LAB_SHORT),
          _clause(S, "3.2", "An examined adult's 25(OH)D for the wave's estimates is the result of their primary vial "
                            "that the laboratory released as final."),
          _clause(S, "3.3", "The cut-off of 20 ng/mL refers to the scale of the reference measurement procedure "
                            "(isotope-dilution liquid chromatography-tandem mass spectrometry). An adult is below the "
                            "cut-off when their 25(OH)D on that scale is below 20 ng/mL. The wave's estimates of "
                            "vitamin D status are on that scale."),
          _clause(S, "3.4", "The laboratory measures 25(OH)D by immunoassay. From 2025 it takes part in the %s's "
                            "accuracy-based vitamin D survey, whose samples carry values assigned by the reference "
                            "measurement procedure." % K.PROVIDER),
          _clause(S, "3.5", "Bridging sample: at the close of the wave, the stored duplicate vials of a random 20 per "
                            "cent of examined adults with a final result are assayed together in one run, for the "
                            "wave's standardisation."),
          _clause(S, "3.6", "A county's share below the cut-off is weighted with WTMEC2025 over its examined adults "
                            "with a final result."),
          Paragraph("4. Dietary supplements", S["h2"]),
          _clause(S, "4.1", "The household interview asks about each dietary supplement taken in the 30 days before "
                            "the interview: the product, the number of days it was taken and the number of units "
                            "(tablets, softgels, gummies, drops) taken on a day it was taken. Products are matched to "
                            "the label database; a product not found there is recorded as reported."),
          _clause(S, "4.2", "A nutrient's average daily intake from supplements is, summed over a person's products, "
                            "the amount in one unit times the units taken a day times the days taken, divided by 30. "
                            "Estimates use WTINT2025 over interviewed adults."),
          Paragraph("5. Response rates", S["h2"]),
          _clause(S, "5.1", "Response rates are unweighted, over sample persons aged 20 and over, leaving out those "
                            "found ineligible after selection (moved out of the district, died or entered an "
                            "institution before the interview). The interview response rate counts complete, partial "
                            "and proxy interviews; the examination response rate counts persons examined at the MEC."),
          Paragraph("6. Reporting", S["h2"]),
          Paragraph("Estimates are produced for the district and for each county. County estimates based on fewer "
                    "than 100 examined adults are flagged; none of the 2025 counties falls below that. Variance "
                    "estimation uses the design's strata and county stands as primary sampling units.", S["body"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ the check report
def write_check(path, check):
    S = styles("Sans", PLUM)
    doc, fr = _doc(path, "Accuracy-Based Vitamin D Survey, event %s: participant report" % K.CHECK_EVENT, K.PROVIDER,
                   "Participant report", K.PROVIDER, "Event %s" % K.CHECK_EVENT)
    lotno = K.REAGENT_LOTS[check["lot"]][0]
    hdr = [["Participant", "%s (participant no. 2214); director %s; contact %s, quality manager"
            % (K.LAB_SHORT, K.LAB_DIRECTOR, K.QUALITY)],
           ["Event", "%s, accuracy-based vitamin D survey (25-hydroxyvitamin D, total)" % K.CHECK_EVENT],
           ["Samples", "Five single-donor fresh-frozen serum samples, values assigned by the reference measurement "
                       "procedure (ID LC-MS/MS)"],
           ["Method reported", "Immunoassay, Varnholt iQ 820, %s" % K.ASSAY],
           ["Instrument", K.ANALYZERS[0][1]], ["Reagent lot", lotno],
           ["Date tested", _d(K.CHECK_RUN.date())], ["Report issued", _d(K.CHECK_REPORT_DATE)]]
    t = Table([[Paragraph("<b>%s</b>" % a, S["cell"]), Paragraph(b, S["cell"])] for a, b in hdr],
              colWidths=[1.3 * inch, 5.5 * inch], hAlign="LEFT")
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, -1), (-1, -1), .6, INK),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    rows = [["Sample", "Assigned value (ng/mL)", "Your result (ng/mL)", "Difference (%)"]]
    for i, (tg, lab, pc) in enumerate(zip(K.CHECK_TARGETS, check["lab"], check["pct"]), 1):
        rows.append(["VD-%s-%02d" % (K.CHECK_EVENT, i), "%.1f" % tg, "%.1f" % lab, "%+.1f" % pc])
    rows.append(["Mean", "", "", "%+.1f" % check["mean"]])
    peer = [["Peer group", "Laboratories", "Mean difference (%)", "SD of difference (%)"],
            ["Varnholt iQ 820, %s" % K.ASSAY, "23", "+11.6", "4.9"],
            ["All immunoassays", "141", "+7.3", "9.2"], ["LC-MS/MS", "38", "+0.9", "3.1"]]
    ok = abs(check["mean"]) <= 5.0
    st = [Paragraph("Accuracy-Based Vitamin D Survey: participant report", S["h1"]),
          Paragraph("%s. Event %s." % (K.PROVIDER, K.CHECK_EVENT), S["meta"]), t, Spacer(1, 8),
          Paragraph("Your results", S["h2"]), _table(S, rows, [1.6, 1.7, 1.7, 1.6], right=(1, 2, 3), bold_last=True),
          Paragraph("Difference is your result less the assigned value, divided by the assigned value. The mean is "
                    "the mean of the five differences.", S["note"]),
          Paragraph("Evaluation", S["h2"]),
          Paragraph("Performance criterion: mean difference within plus or minus 5.0 per cent of the assigned values. "
                    "Your mean difference: %+.1f per cent. Criterion %s." % (check["mean"], "met" if ok else "not met"),
                    S["body"]),
          Paragraph("Peer groups (event %s)" % K.CHECK_EVENT, S["h2"]),
          _table(S, peer, [2.6, 1.2, 1.5, 1.5], right=(1, 2, 3)),
          Paragraph("The survey's samples are commutable single-donor sera. Results are those the participant entered "
                    "on the program's portal by the closing date.", S["note"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ fieldwork close-out
def write_closeout(path, stands):
    S = styles("Sans", TEAL)
    doc, fr = _doc(path, "MHNES 2025 fieldwork close-out", K.FIELD_LEAD, "Close-out report", K.CENTER,
                   "Fieldwork close-out")
    rows = [["County", "Stand", "Exam days", "Examined", "Blood drawn", "Shipments", "Days lost"]]
    for s in stands:
        rows.append([s["name"], "%s to %s" % (s["a"].strftime("%d %b").lstrip("0"), s["b"].strftime("%d %b").lstrip("0")),
                     s["days"], _n(s["examined"]), _n(s["blood"]), s["ships"], s["lost"]])
    tot = [sum(s[k] for s in stands) for k in ("days", "examined", "blood", "ships", "lost")]
    rows.append(["District", "6 Jan to 4 Dec", tot[0], _n(tot[1]), _n(tot[2]), tot[3], tot[4]])
    st = [Paragraph("2025 wave: fieldwork close-out", S["h1"]),
          Paragraph("%s, %s. Prepared by %s, Field Operations Lead, for the Chief Statistician. %s."
                    % (K.DISTRICT, K.CENTER, K.FIELD_LEAD, _d(dt.date(2026, 1, 20))), S["meta"]),
          Paragraph("1. Summary", S["h2"]),
          Paragraph("The MEC completed all eight county stands between 6 January and 4 December 2025. Screening "
                    "and household interviewing ran ahead of each stand from about ten weeks before it opened. "
                    "This note closes the field year; the sample persons' final dispositions are in the case "
                    "management export of 9 January 2026.", S["body"]),
          Paragraph("2. MEC stands", S["h2"]),
          _table(S, rows, [1.1, 1.3, 0.8, 0.9, 0.9, 0.8, 0.8], right=(2, 3, 4, 5, 6), bold_last=True),
          Paragraph("Examined: adults examined at the MEC. Blood drawn: examined adults with a completed "
                    "venipuncture. Shipments: dry-ice shipments to the laboratory (Mondays and Thursdays). Days lost: "
                    "scheduled exam days the MEC did not open (weather, power and water faults).", S["note"]),
          Paragraph("3. Field notes", S["h2"]),
          _clause(S, "3.1", "Corvale: two exam days lost to the February ice storm; appointments moved to the "
                            "stand's last week."),
          _clause(S, "3.2", "Ulverne and Vellance: an evening session was added on Fridays to meet the stand's "
                            "targets."),
          _clause(S, "3.3", "Quennel: the MEC's water supply failed on two days in August; examinations resumed "
                            "the next morning."),
          _clause(S, "3.4", "Inskeep: the stand closed on 4 December as planned; no exams were moved into 2026."),
          Paragraph("4. Specimens", S["h2"]),
          Paragraph("Specimens were processed and frozen at the MEC and shipped on dry ice twice a week. Every "
                    "shipment arrived frozen. Specimen events are in the tracking export.", S["body"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ data dictionary
def write_dictionary(path):
    S = styles("Sans", NAVY)
    doc, fr = _doc(path, "MHNES 2025 data dictionary", K.REQUESTER, "Data dictionary", K.CENTER, "Data dictionary")
    F = K.FILES

    def block(title, grain, fields):
        out = [Paragraph(title, S["h2"]), Paragraph(grain, S["body"])]
        out.append(_table(S, [["Field", "Definition"]] + fields, [1.7, 5.1]))
        return out
    st = [Paragraph("2025 wave: data dictionary", S["h1"]),
          Paragraph("%s, %s. Release of 9 January 2026; laboratory files as received from %s."
                    % (K.DISTRICT, K.CENTER, K.LAB_SHORT), S["meta"])]
    st += block(F["persons"], "One row per examined sample person.",
                [["SEQN", "Sample person number"], ["COUNTY_CODE", "County of residence (county_codes.csv)"],
                 ["EXAM_DATE, EXAM_SESSION", "Date and session (AM, PM, EVE) of the MEC examination"],
                 ["AGE_YR", "Age in years at the examination"], ["SEX, RACE_ETH", "As reported at the interview"],
                 ["BLOOD_DRAWN", "Y when a venipuncture was completed"], ["WTMEC2025", "Examination weight"]])
    st += block(F["status"], "One row per sample person, as the case management system closed the case.",
                [["SEQN", "Sample person number"], ["SCREENER_ID", "The screening that selected the person"],
                 ["INT_STATUS", "Final interview disposition"], ["INT_DATE", "Date of the household interview"],
                 ["EXAM_STATUS, EXAM_DATE", "EXAMINED or NOT EXAMINED for interviewed persons, and the date"],
                 ["CASE_CLOSED", "Date the case was closed"], ["WTINT2025", "Interview weight (interviewed persons)"]])
    st += block(F["rosters"], "One row per person listed on a screener roster.",
                [["SCREENER_ID, DWELLING_ID", "The screening and the dwelling screened"],
                 ["SCREEN_DATE, INTERVIEWER", "Date of the screening and the field interviewer"],
                 ["LINE", "Roster line"], ["AGE, SEX, RELATIONSHIP", "As listed; age in years at the screening"],
                 ["SELECTED, SEQN", "Y and the sample person number for persons selected"]])
    st += block(F["tracking"], "One row per event on a vial. Times are local (Mountain).",
                [["BARCODE", "Vial label: the participant's label number and the vial (01 primary serum for "
                             "25(OH)D, 02 stored duplicate serum, 03 chemistry serum, 04 EDTA whole blood)"],
                 ["SEQN", "Sample person"],
                 ["EVENT", "COLLECTED, PROCESSED, FROZEN, REFRIGERATED, SHIPPED, RECEIVED, ACCESSIONED, ASSAYED, "
                           "REJECTED, STORED, PULLED, THAWED, RETURNED"],
                 ["REFERENCE", "Shipping box, accession number, biorepository position or rejection reason"]])
    st += block(F["results"], "One row per result the laboratory information system released for a primary vial.",
                [["SPECIMEN_ID", "Vial label without punctuation"],
                 ["RESULT", "ng/mL; outside the reportable range (4.0 to 150.0) as text"],
                 ["RESULT_STATUS", "F final; X voided"],
                 ["INSTRUMENT", "LIS code of the analyzer (instrument_register.csv)"],
                 ["REAGENT_LOT", "Reagent lot of the run"], ["RESULTED_AT", "Date and time released, local"]])
    st += block(F["bridge"], "One row per stored duplicate vial assayed in the bridging run.",
                [["SPECIMEN_ID", "Vial label without punctuation"], ["RESULT", "ng/mL"],
                 ["RESULTED_AT", "Date and time released, local"]])
    st += block(F["events"], "One row per event the analyzers' middleware logged. Times are UTC.",
                [["INSTRUMENT_SN", "Analyzer serial number"],
                 ["EVENT_TYPE", "CALIBRATION, CALIBRATOR_LOT, QC, REAGENT_LOAD, MAINTENANCE, ERROR"],
                 ["REAGENT_LOT, CALIBRATOR_LOT", "Lots in use for the event"], ["QC_LEVEL", "Control level 1 or 2"],
                 ["OUTCOME", "ACCEPTED or FAILED (calibration); PASS or FAIL (QC); DONE; REGISTERED"]])
    st += block(F["supplements"], "One row per product line a person reported.",
                [["DSQ_LINE", "Line within the person's report"],
                 ["PRODUCT_ID", "Label database identifier, or GENERIC when the product is recorded as reported"],
                 ["DAYS_TAKEN_30D", "Days the product was taken in the 30 days before the interview"],
                 ["UNITS_PER_DAY", "Units taken on a day it was taken"]])
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


# ------------------------------------------------------------------------------------------------ distractors
def write_notice(path):
    S = styles("Sans", NAVY)
    doc, fr = _doc(path, "Customer notification CN-25-014", K.MAKER, "Customer notification", K.MAKER,
                   "CN-25-014")
    st = [Paragraph("Customer notification CN-25-014", S["h1"]),
          Paragraph("%s. %s on the iQ 820 and iQ 840 analyzers. Issued 16 June 2025." % (K.MAKER, K.ASSAY), S["meta"]),
          Paragraph("What is changing", S["h2"]),
          Paragraph("Reagent lots of the %s assay manufactured from 30 June 2025, beginning with lot %s, are "
                    "restandardised to the reference measurement procedure. Calibrator values are unchanged; the "
                    "master curve shipped with each reagent lot carries the change." % (K.ASSAY, K.RESTANDARDISED_FROM),
                    S["body"]),
          Paragraph("What you may see", S["h2"]),
          Paragraph("On patient samples, results with the restandardised lots are expected to be about 8 per cent "
                    "lower on average than with earlier lots. Laboratories should verify the new lot against the lot "
                    "in use before reporting patient results, as for any lot change.", S["body"]),
          Paragraph("Action", S["h2"]),
          Paragraph("Please confirm receipt of this notification. No product is recalled.", S["body"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


def write_tables2021(path):
    S = styles("Serif", TEAL)
    doc, fr = _doc(path, "MHNES 2021 data brief tables", K.CENTER, "Data brief tables", K.CENTER, "MHNES 2021")
    rows = [["County", "Examined adults", "Below 20 ng/mL (%)", "95% CI", "Interview RR (%)", "Exam RR (%)"]]
    data = [("Wexmoor", 588, 31.4, "26.9 to 36.2", 81.4, 64.8), ("Corvale", 671, 27.6, "23.8 to 31.7", 79.6, 66.9),
            ("Lassiter", 552, 26.2, "21.9 to 31.0", 83.2, 68.2), ("Ulverne", 619, 21.8, "18.2 to 25.8", 80.7, 63.4),
            ("Vellance", 702, 18.9, "15.8 to 22.4", 76.4, 61.3), ("Quennel", 560, 22.7, "18.9 to 27.0", 84.3, 69.2),
            ("Yarrowmere", 604, 30.9, "26.6 to 35.6", 78.9, 62.9), ("Inskeep", 590, 29.3, "25.1 to 33.9", 82.4, 65.8)]
    for d in data:
        rows.append([d[0], _n(d[1]), "%.1f" % d[2], d[3], "%.1f" % d[4], "%.1f" % d[5]])
    st = [Paragraph("2021 wave: vitamin D status and response, by county", S["h1"]),
          Paragraph("%s, %s. Data brief 2022-3 tables, published 9 August 2022." % (K.DISTRICT, K.CENTER), S["meta"]),
          _table(S, rows, [1.2, 1.1, 1.2, 1.2, 1.1, 1.0], right=(1, 2, 4, 5)),
          Paragraph("Serum 25(OH)D for the 2021 wave was measured by LC-MS/MS at the State Public Health Laboratory. "
                    "Weighted with the 2021 examination weights; response rates unweighted. The 2021 wave sampled "
                    "adults aged 20 and over.", S["note"])]
    doc.build(st, onFirstPage=fr, onLaterPages=fr)


def write_contents(path, items):
    out = ["%s, %s: 2025 wave files for the 2027 vitamin D programme" % (K.DISTRICT, K.CENTER),
           "Assembled %s by %s." % (K.ASSEMBLED.strftime("%d %B %Y").lstrip("0"), K.REQUESTER), ""]
    for name, desc in items:
        out.append(name)
        out.append("    " + desc)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(out) + "\n")
