"""task249 documents: the data manager's request (eml); the surrogate load procedure, the 2027 sediment report and the
laboratory's quality statement (pdf); the station register and the laboratory results (xlsx); the data dictionary
(md)."""
import os

from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


def _addr(who, domain=P.DOMAIN):
    return "%s <%s@%s>" % (who[0], who[1], domain)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.0, leading=9.8)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E3E8EF"))]))
    return t


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    return foot


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                             bottomMargin=18 * mm, title=title, author=author, creator=author, subject=subject,
                             invariant=1)


def _sections(s, sec, body, h2):
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))


def _build(doc, s, foot):
    doc.build(s, onFirstPage=_footer(foot), onLaterPages=_footer(foot))


# ------------------------------------------------------------------ the request (eml)
def request(path, F):
    text = f"""From: {_addr(P.DATA_MANAGER)}
To: Monitoring analytics <overvaking.analyse@{P.DOMAIN}>
Cc: {_addr(P.FIELD_LEAD)}
Date: Mon, 6 Mar 2028 08:12:44 +0100
Subject: Spring review of the 2027 sediment loads
Message-ID: <20280306081244.3187@{P.DOMAIN}>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Hi,

The 2027 sediment report went to Fjellbrekke Kraft on 15 February and their
flushing plan for Breiavatn and Djupevatn is fixed on 20 March, so the spring
review of the published loads (procedure section 8) has to be done before then.
For each of the 14 stations I need to know whether the 2027 load we published
misstates the sediment that actually passed the station by more than our 15 per
cent, and if so whether it is over or under; anything outside goes back to them
re-issued before the plan uses it.

The review sheet also carries two lines per station as every year: the
turbidity record's health over the calibration years, as the hours in 2025 and
2026 without a usable reading (section 5), and how many of the station's 2027
samples the laboratory weighed in a batch that failed its quality control
(section 4).

Everything is in the folder: the 15-minute record, Lise's sample sheet, the
laboratory's results, its batch export for 2027 and its quality statement, the
maintenance log, the station register, the procedure and the report itself.

Thanks,
Marianne

--
{P.DATA_MANAGER[0]}
Data manager, {P.PROGRAMME}
{P.ORG}
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


# ------------------------------------------------------------------ the procedure (pdf)
def procedure(path, F):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "SMP-03 Suspended sediment: surrogate load procedure, version 3", P.ORG, "Procedure")
    s = [Paragraph("%s, %s for %s" % (P.ORG, P.PROGRAMME, P.CLIENT), small),
         Paragraph("SMP-03 Suspended sediment: surrogate load procedure", h1),
         Paragraph("Version 3, January 2027. Replaces version 2 (March 2024). Owner: the programme's data manager.", small),
         Spacer(1, 4)]
    sec = [
        ("1. Purpose and scope",
         ["%s runs the suspended-sediment monitoring at %s's 14 stations on the rivers that feed Breiavatn, "
          "Kvitstølvatn and Djupevatn under contract (station register, %s). Each station's annual suspended-sediment "
          "load is published in the annual sediment report to the company and goes into the reservoirs' sediment "
          "budgets and flushing plans." % (P.ORG, P.CLIENT, F["register"])]),
        ("2. Station equipment",
         ["Each station logs discharge (pressure transducer and the station's rating; published to three significant "
          "figures, in cubic metres per second) and turbidity (FNU) every 15 minutes, time-stamped in UTC. The stations "
          "run %s sondes (range 0 to 4,000 FNU, optical window wiper), installed station by station in autumn 2026 "
          "together with new loggers; before that they ran %s sondes (range 0 to 1,000 FNU, no wiper)."
          % (P.NEW_SENSOR, P.OLD_SENSOR)]),
        ("3. Sampling",
         ["Calibration samples are depth-integrated across the section with a US DH-48 type sampler from the "
          "station's bridge or cableway. The field team samples on routine rounds, about monthly (the high glacier "
          "stations have no rounds from December to March), and goes out on flood callouts when the national flood "
          "forecasting service issues a flood-watch alert for the rivers. Each bottle carries a bottle number that "
          "restarts every year; the field app records the station, the time of sampling (Norwegian local time with "
          "its offset from UTC) and the trip (%s)." % F["field"]]),
        ("4. Laboratory analysis and quality control",
         ["%s determines suspended-sediment concentration by whole-sample filtration through 0.7 micrometre glass-fibre "
          "filters dried at 105 degrees C, and reports milligrams per litre (%s). Samples are weighed in batches. Each "
          "batch carries a blank filter and two aliquots of the laboratory's kaolin control suspension. A batch passes "
          "its quality control when the blank filter's mass changes by no more than 0.5 mg, each control aliquot is "
          "recovered at 90 to 110 per cent of the control suspension's concentration, and the two aliquots' "
          "concentrations differ by no more than 10 per cent of their mean. A sample weighed in a batch that fails a "
          "check keeps its result; the batch is listed in the spring review." % (P.LAB, F["lims"])]),
        ("5. The turbidity record",
         ["The 15-minute record (%s) holds one row per station and interval. An interval has no usable turbidity "
          "reading when the record holds no row for it, when its row carries the flag F (fouled optics) or M (sonde "
          "out of the water), or when its reading sits at the upper end of the sonde's range. The flag C marks a "
          "reading checked against a handheld turbidimeter and is usable. Field visits are entered in the maintenance "
          "log (%s)." % (F["record"], F["log"])]),
        ("6. Calibration",
         ["Each station's suspended-sediment concentration is related to its turbidity by an ordinary least-squares "
          "regression of log10 concentration on log10 turbidity, fitted to all of the station's accepted samples of "
          "the calibration years (2025 to 2027 for the 2027 loads), each sample paired with the station's 15-minute "
          "turbidity reading nearest its time. Predictions are retransformed with Duan's smearing estimate, the mean of "
          "10 raised to each sample's residual."]),
        ("7. Annual loads",
         ["A station's annual load is the sum over the year's 15-minute intervals, 1 January 00:00 to 31 December 23:45 "
          "UTC, of the predicted concentration (mg/L, equal to g per cubic metre) times the discharge times 900 "
          "seconds, reported in tonnes in the annual sediment report."]),
        ("8. Spring review of the published loads",
         ["The programme's data manager reviews the published loads each spring, before the company's flushing plan uses them. A "
          "station's published load is re-issued when it misstates the suspended sediment that passed the station in "
          "the year by more than 15 per cent, over or under."]),
    ]
    _sections(s, sec, body, h2)
    _build(doc, s, "SMP-03 v3  |  %s" % P.ORG)


# ------------------------------------------------------------------ the 2027 sediment report (pdf)
def report(path, F, pub):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Suspended sediment loads 2027", P.ORG, "Annual sediment report")
    s = [Paragraph("%s for %s, %s" % (P.ORG, P.CLIENT, P.PROGRAMME), small),
         Paragraph("Suspended sediment loads 2027", h1),
         Paragraph("Annual sediment report, issued 15 February 2028.", small), Spacer(1, 4),
         Paragraph("The table gives each station's 2027 suspended-sediment load, computed by procedure SMP-03 "
                   "version 3, sections 6 and 7: the station's regression of log10 concentration on log10 turbidity, "
                   "fitted to its accepted samples of 2025 to 2027, retransformed with Duan's smearing estimate and "
                   "applied to every 15-minute interval of 2027. Coefficients: log10 C = a + b log10 T.", body),
         Spacer(1, 3)]
    rows = [["Station", "Name", "Regime", "Samples", "a", "b", "Smearing", "R-squared", "Load 2027 (t)"]]
    for key, code, name, river, res, area, glac, _ in P.STATIONS:
        p = pub[key]
        rows.append([code, name, P.KIND_LABEL[P.SPEC[key][0]], p["n"], "%.4f" % p["a"], "%.4f" % p["b"],
                     "%.4f" % p["bcf"], "%.3f" % p["r2"], "{:,}".format(p["load_t"])])
    s.append(_grid(rows, [14 * mm, 38 * mm, 19 * mm, 16 * mm, 15 * mm, 14 * mm, 17 * mm, 17 * mm, 20 * mm], cell))
    s.append(Spacer(1, 5))
    s.append(Paragraph("Loads go into the reservoir sediment budgets (Breiavatn, Kvitstølvatn, Djupevatn) and the 2028 "
                       "flushing plan. The spring review (section 8) follows before the plan is fixed.", body))
    _build(doc, s, "Suspended sediment loads 2027  |  %s" % P.ORG)


# ------------------------------------------------------------------ the laboratory's quality statement (pdf)
def lab_statement(path, F, n27):
    body, h1, h2, small, cell = _styles()
    doc = _doc(path, "Quality statement 2027: suspended sediment", P.LAB, "Quality statement")
    s = [Paragraph(P.LAB, small),
         Paragraph("Quality statement 2027: suspended sediment for %s" % P.ORG, h1),
         Paragraph(P.PROGRAMME, small),
         Paragraph("18 January 2028. %s, quality manager." % P.LAB_QA[0], small), Spacer(1, 4)]
    sec = [
        ("Scope",
         ["This statement covers the suspended-sediment concentrations the laboratory reported to %s for samples "
          "received in 2027 (%d samples). The method is whole-sample filtration through 0.7 micrometre glass-fibre "
          "filters, dried to constant mass at 105 degrees C, accredited under NS-EN ISO/IEC 17025." % (P.ORG, n27)]),
        ("Control materials in use in 2027",
         ["Each batch carries two aliquots of a kaolin control suspension prepared and certified by the laboratory."]),
    ]
    _sections(s, sec, body, h2)
    rows = [["Lot", "Material", "Concentration (mg/L)", "In use"],
            ["KS-26-11", "kaolin in deionised water", "50.0", "4 January 2027 to 30 June 2027"],
            ["KS-27-06", "kaolin in deionised water", "54.0", "from 1 July 2027"]]
    s.append(_grid(rows, [25 * mm, 50 * mm, 35 * mm, 60 * mm], cell))
    sec = [
        ("Proficiency testing",
         ["The laboratory took part in two rounds of the national proficiency scheme for suspended solids in 2027: "
          "round 2027-1 (April), z-scores 0.4 and -0.7; round 2027-2 (October), z-scores 1.1 and 0.2."]),
        ("Results and quality control",
         ["The batch export gives every batch's blank and control results beside the samples weighed in it. No result "
          "was withdrawn in 2027."]),
    ]
    _sections(s, sec, body, h2)
    _build(doc, s, "Quality statement 2027  |  %s" % P.LAB)


# ------------------------------------------------------------------ workbooks
def _head(ws, row, head, widths):
    for j, h in enumerate(head, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True)
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w


def register_xlsx(path, df):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stations"
    head = list(df.columns)
    _head(ws, 1, head, [9, 28, 16, 14, 13, 13, 15, 16, 15, 32, 14])
    for i, r in enumerate(df.itertuples(index=False), 2):
        for j, x in enumerate(r, 1):
            ws.cell(row=i, column=j, value=x)
    ws.freeze_panes = "A2"
    wb.save(path)


def lims_xlsx(path, old, new):
    wb = Workbook()
    ws = wb.active
    ws.title = "2025"
    _head(ws, 1, list(old.columns), [11, 9, 12, 12, 12, 10, 18])
    for i, r in enumerate(old.itertuples(index=False), 2):
        for j, x in enumerate(r, 1):
            ws.cell(row=i, column=j, value=x)
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("2026-2027")
    _head(ws2, 1, list(new.columns), [12, 9, 12, 12, 12, 17, 10, 9, 34])
    for i, r in enumerate(new.itertuples(index=False), 2):
        for j, x in enumerate(r, 1):
            ws2.cell(row=i, column=j, value=x)
    ws2.freeze_panes = "A2"
    wb.save(path)


# ------------------------------------------------------------------ the data dictionary (md)
def dictionary(path, F):
    text = f"""# Sediment monitoring folder: data dictionary

{P.PROGRAMME}, {P.ORG}. Prepared for the spring review, March 2028.

## {F["record"]}

The stations' 15-minute logger record, 2025 to 2027, one row per station and interval as the logger network delivered it.

| Column | Meaning |
|---|---|
| station | station code (station register) |
| time_utc | start of the 15-minute interval, UTC |
| discharge_m3s | discharge, cubic metres per second, three significant figures |
| turbidity_fnu | turbidity, FNU |
| water_temp_c | water temperature, degrees C |
| flag | blank, or F fouled optics, M sonde out of the water, C checked against a handheld turbidimeter |

## {F["field"]}

The field app's export of every calibration bottle, 2025 to 2027.

| Column | Meaning |
|---|---|
| bottle_no | the bottle's number; numbers restart every year |
| station | station code |
| sampled | date and time of sampling as the field app records it: Norwegian local time with its offset from UTC |
| trip | routine round or flood callout |
| callout_ref | the callout, for bottles taken on a flood callout |
| sampler, crew, remarks | as entered in the field |

## {F["lims"]}

The laboratory's results. Sheet 2025 is the laboratory's former system (Prøvenr is the two-digit year and the bottle number, Stasjon the station, Prøvetatt the sampling date, Mottatt received, Analysert analysed, SS mg/l the concentration). Sheet 2026-2027 is the current system: sample_id is the year and the bottle number, ssc_mg_l the concentration in mg/L, status final for the result that stands or replaced for one superseded by it.

## {F["batches"]}

The laboratory's batch export for 2027, one line per sample: batch, the date the batch was weighed (dd.mm.yyyy), sample_id, and the batch's quality-control results given on every line of the batch: blank_change_mg (the blank filter's change in mass), control_lot, control_nominal_mg_l, and each control aliquot's net mass (mg) and volume (mL).

## {F["log"]}

The field team's maintenance log, Norwegian local time: date (dd.mm.yyyy), station, visit, the times the sonde came out of and went back into the water, technician, remarks.

## Other files

- {F["register"]}: one row per station, with the sonde and the date it was installed.
- {F["report"]}: the published 2027 loads and each station's regression.
- {F["procedure"]}: the surrogate load procedure.
- {F["statement"]}: the laboratory's quality statement for 2027.
- {F["precip"]}: daily precipitation and mean air temperature at Fjellbrekke Kraft's two weather stations, as their export writes it (semicolons, decimal commas).
- {F["reservoirs"]}: daily water level and stored volume of the three reservoirs.
- {F["request"]}: the request for the spring review.
"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
